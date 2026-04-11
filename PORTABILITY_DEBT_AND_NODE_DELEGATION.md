# Portability Debt and Node Atomic Delegation

> **Version**: v1.0.0 (April 11, 2026)
> **Owner**: primalSpring (upstream gap registry)
> **Audience**: All primal teams, especially barraCuda, coralReef, toadStool, NestGate
> **See also**: `ECOBIN_ARCHITECTURE_STANDARD.md`, `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md`

## Summary

ecoPrimals has three classes of non-portable external dependency. Class 1 (C crypto)
was solved by the Tower Atomic delegation pattern (BearDog + RustCrypto + IPC).
Class 2 (GPU/Vulkan dynamic linking) is the same category of problem and requires
the same category of solution: **Node Atomic delegation**. Class 3 (remaining C
surfaces) contains a mix of policy gaps and acceptable feature-gated exceptions.

This document defines the Node Atomic delegation pattern, maps the resolution path,
and assigns ownership to primal teams.

---

## The Pattern: Delegation over Internalization

The ecosystem's answer to non-portable dependencies is always the same:

1. **Identify** the non-portable surface (C/ASM, FFI, dynamic loading)
2. **Centralize** the capability in one primal (the specialist)
3. **Expose** via JSON-RPC IPC (capability-based discovery)
4. **Ban** direct usage in consumers (`deny.toml`)
5. **Degrade** gracefully when the specialist is absent (pure-Rust fallback)

### Tower Atomic: The Proven Instance

```
Problem:  ring (C/ASM crypto) blocked musl cross-compile
Solution: BearDog provides RustCrypto in-process
          Other primals delegate crypto via JSON-RPC IPC
          deny.toml bans ring/openssl/aws-lc-sys ecosystem-wide
Result:   Any primal can run on any platform — crypto is universal
```

### Node Atomic: The Same Pattern for Compute

```
Problem:  wgpu → wgpu-hal → ash → libloading → dlopen(libvulkan.so)
          musl-static binaries cannot load GPU drivers at runtime
Solution: barraCuda provides math in pure Rust (WGSL + scalar fallback)
          GPU dispatch delegated to toadStool + coralReef via JSON-RPC IPC
          coralReef compiles WGSL → native GPU binary (sovereign compiler)
          toadStool discovers and manages hardware (DRM/VFIO)
Result:   Math is universal — barraCuda computes on any hardware
```

---

## The Dependency Chain (Why It Breaks)

### wgpu's transitive dlopen requirement

```
barraCuda (default `gpu` feature)
  └─ wgpu 28.0.0
       └─ wgpu-hal 28.0.1
            ├─ ash 0.38.0 (Vulkan bindings)
            │    └─ libloading 0.8.9
            │         └─ dlopen("libvulkan.so.1")  ← FAILS on musl-static
            ├─ metal 0.33.0 (Apple frameworks)
            ├─ windows-rs (DX12)
            └─ renderdoc-sys
```

### Why musl-static can never dlopen

musl's `dlopen` implementation cannot load glibc-linked shared objects.
GPU ICDs (`libvulkan.so.1`, `libnvidia-glcore.so`, etc.) are built against glibc.
This is a fundamental incompatibility — not a bug, not a misconfiguration.

**Consequence**: ecoBin musl-static binaries (the deployment standard) will
**never** access GPU hardware through the wgpu codepath. This is true for
barraCuda, toadStool (when `wgpu` feature enabled), and petalTongue (GUI mode).

---

## Resolution Architecture

### The Four-Tier Fallback Chain

barraCuda's `Auto::new()` currently tries two paths and gives up. The target
state is a four-tier fallback that ensures math always computes:

```
Tier 1: WgpuDevice (GPU)
  ↓ wgpu adapter found? (glibc host with GPU drivers)
  │ YES → dispatch via Vulkan/Metal/DX12 — fastest path
  ↓ NO

Tier 2: WgpuDevice (CPU software rasterizer)
  ↓ wgpu CPU adapter found? (llvmpipe/lavapipe on host)
  │ YES → dispatch via software Vulkan — slow but correct
  ↓ NO

Tier 3: SovereignDevice (IPC delegation)         ← NEW: BC-07
  ↓ toadStool + coralReef available via IPC?
  │ YES → barraCuda sends WGSL to coralReef (compile),
  │        toadStool dispatches to hardware — GPU via IPC
  ↓ NO

Tier 4: CpuExecutor + naga-exec (pure Rust)      ← NEW: BC-08
  ↓ cpu-shader feature enabled?
  │ YES → naga interprets WGSL on CPU — same math, scalar speed
  │ NO  → scalar Rust implementations of each op — baseline
```

### What Needs to Change

| Gap | Owner | Change | Effort |
|-----|-------|--------|--------|
| BC-07 | barraCuda team | Wire `SovereignDevice::with_auto_device()` into `Auto::new()` fallback between Tier 2 and Tier 4. The trait, impl, and IPC wiring already exist — they're just not connected in the failure path | Small — plumbing only |
| BC-08 | barraCuda team | Make `cpu-shader` feature default-on in `crates/barracuda/Cargo.toml`. All batch ops already have `#[cfg(feature = "cpu-shader")]` paths with scalar Rust fallbacks | Small — feature flag flip + CI validation |
| BC-06 | Documentation | Architectural constraint, not a code fix. Document that ecoBin musl-static = CPU-only for wgpu. The fix IS Tiers 3 and 4 | None (doc only) |
| CR-01 | coralReef team | Add `ring`/`openssl`/`aws-lc-sys` ban list to `deny.toml` matching the ecosystem standard | Small — policy alignment |
| NG-08 | NestGate team | Switch `rustls` to explicit `rustls-rustcrypto` provider (like Songbird) or replace `reqwest` with `ureq` for IPC HTTP. `ring` v0.17.14 is live in production despite `deny.toml` ban | Medium — dependency surgery |

### The Ring Parallel (Side by Side)

| Aspect | Tower Atomic (SOLVED) | Node Atomic (TO SOLVE) |
|--------|----------------------|----------------------|
| Non-portable dep | `ring` (C/ASM crypto) | `wgpu` → `ash` → `libloading` → `dlopen` |
| Specialist primal | BearDog (RustCrypto) | toadStool (hardware) + coralReef (compiler) |
| Consumer | Every primal needing crypto | barraCuda (math), springs needing GPU |
| IPC method | `btsp.session.create`, `crypto.encrypt` | `shader.compile.wgsl`, `compute.dispatch.submit` |
| Pure-Rust fallback | RustCrypto in-process | `cpu-shader` (naga-exec) + scalar Rust |
| Ban policy | `deny.toml` bans `ring` | Future: consumers ban direct `wgpu` import |
| Degradation | Works without BearDog (self-contained crypto) | Works without toadStool/coralReef (CPU fallback) |

---

## Class 3: Remaining C Surfaces

### Active Gaps (require action)

**NG-08: NestGate `ring` transitive leak** — **RESOLVED** (April 11, 2026)

`ring` v0.17.14 was present in NestGate's production build via
`ring` → `rustls` → `hyper-rustls` → `reqwest` → `nestgate-rpc` → binary.

**Fix applied**: Option 2 — `reqwest` replaced with `ureq` 3.3 (`rustls-no-provider` +
`rustls-webpki-roots`) + `rustls-rustcrypto` 0.0.2-alpha as explicit crypto provider.
`fetch_external.rs` refactored: synchronous `ureq` agent wrapped in
`tokio::task::spawn_blocking` for async compatibility. Verified:
- `cargo tree -i ring --edges normal` → "did not match any packages"
- `cargo tree -i aws-lc-rs` → no matches
- `cargo tree -i openssl` → no matches
- `cargo deny check bans` → PASS
- All `nestgate-rpc` tests pass

**CR-01: coralReef missing `deny.toml` C/FFI ban list** (Medium severity)

coralReef's `deny.toml` contains only license and advisory checks — no ban list
for `ring`, `openssl`, `native-tls`, or other C/FFI crates. Every other primal
in the ecosystem has this ban list. This is a policy gap that could allow C
dependencies to enter coralReef undetected.

**Fix**: Add the standard ecoBin v3 ban block matching barraCuda/NestGate/Songbird.

### Acceptable (feature-gated or target-gated)

| Primal | Dep | Why Acceptable |
|--------|-----|----------------|
| coralReef | `cudarc` (CUDA) | Behind `cuda` feature; sovereign `coral-gpu` path is pure Rust |
| toadStool | `wgpu`/`ash`/`vulkano`/`wasmtime`/`esp-idf-sys` | All behind feature gates; core crate pure Rust |
| petalTongue | eframe/egui/glow | Inherent to GUI; headless mode avoids entirely |
| bearDog | `ndk-sys`/`security-framework-sys` | Target-gated (Android/macOS); Linux ecoBin unaffected |
| sweetGrass | `ring` (via testcontainers) | Dev-deps only; not in production binary |
| Songbird | `ring-crypto` feature | Opt-in; default path uses `rustls_rustcrypto` |

---

## Verification Commands

Primal teams should run these to verify compliance:

```bash
# Check for ring in production dependency graph
cargo tree -i ring --edges normal
# Expected: "did not match any packages" (clean)

# Check for C-linked shared objects in binary
ldd target/x86_64-unknown-linux-musl/release/<binary>
# Expected: "not a dynamic executable"

# Check deny.toml enforcement
cargo deny check bans
# Expected: zero violations

# Check for dlopen calls in dependency tree
cargo tree --workspace | grep -i 'libloading\|dlopen'
# Informational: shows where dynamic loading exists
```

---

## Timeline and Ownership

| Phase | What | Owner | When |
|-------|------|-------|------|
| 1 | Document debt (this doc + PRIMAL_GAPS.md) | primalSpring | **Done** (April 11) |
| 2 | NG-08 ring elimination | NestGate team | **Done** (April 11) — `reqwest` → `ureq` + `rustls-rustcrypto` |
| 3 | CR-01 deny.toml alignment | coralReef team | Next sprint |
| 4 | BC-08 cpu-shader default-on | barraCuda team | Next sprint |
| 5 | BC-07 SovereignDevice fallback wiring | barraCuda team | Sprint+1 |
| 6 | Ecosystem `cargo deny check` CI enforcement | primalSpring (infra) | Sprint+2 |
