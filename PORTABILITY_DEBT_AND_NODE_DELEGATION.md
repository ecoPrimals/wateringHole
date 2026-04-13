# Portability Debt and Node Atomic Delegation

> **Version**: v1.1.0 (April 12, 2026)
> **Owner**: primalSpring (upstream gap registry)
> **Audience**: All primal teams, especially barraCuda, coralReef, toadStool, NestGate
> **See also**: `ECOBIN_ARCHITECTURE_STANDARD.md`, `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md`

## Summary

ecoPrimals had three classes of non-portable external dependency. **All three are
now resolved or documented as acceptable**:
- **Class 1 (C crypto)**: RESOLVED — Tower Atomic delegation (BearDog + RustCrypto + IPC).
  13/13 primals ring-free. NestGate NG-08 was the last, fixed April 11.
- **Class 2 (GPU/Vulkan dynamic linking)**: RESOLVED — Node Atomic delegation.
  barraCuda Sprint 41 wired `SovereignDevice` as tier 3 in `Auto::new()`. Full
  3-tier fallback: wgpu GPU → wgpu CPU → SovereignDevice IPC. cpu-shader default-on.
- **Class 3 (remaining C surfaces)**: RESOLVED/ACCEPTABLE — deny.toml enforced across
  ecosystem (CR-01 Iter 79), typed errors complete (CR-04 Wave 4), dead code removed
  (CR-05). Transitive `libc` via tokio/mio deferred until upstream mio→rustix (mio#1735).

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
| BC-07 | barraCuda team | ~~Wire `SovereignDevice::with_auto_device()` into `Auto::new()` fallback between Tier 2 and Tier 4~~ **RESOLVED** Sprint 41 — `Auto::new()` returns `DiscoveredDevice` enum with 3-tier fallback (wgpu GPU → wgpu CPU → SovereignDevice IPC → Err) | ~~Small~~ Done |
| BC-08 | barraCuda team | ~~Make `cpu-shader` feature default-on~~ **RESOLVED** Sprint 40 — `cpu-shader` is in `default = ["gpu", "domain-models", "cpu-shader"]` | ~~Small~~ Done |
| BC-06 | Documentation | ~~Architectural constraint, not a code fix~~ **RESOLVED** Sprint 41 — documented in README + CONTEXT | ~~None~~ Done |
| CR-01 | coralReef team | ~~Add `ring`/`openssl`/`aws-lc-sys` ban list to `deny.toml`~~ **RESOLVED** Iter 79 — 14-crate C/FFI ban list enforced, `cargo deny check` passes | ~~Small~~ Done |
| NG-08 | NestGate team | ~~Switch `rustls` to explicit `rustls-rustcrypto` provider~~ **RESOLVED** April 11 — `reqwest` replaced with `ureq` + `rustls-rustcrypto` | ~~Medium~~ Done |

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

**CR-01: coralReef `deny.toml` C/FFI ban list** — **RESOLVED** (Iter 79, April 11 2026)

coralReef's `deny.toml` now enforces a 14-crate C/FFI ban list matching the
ecosystem standard: `ring`, `openssl-sys`, `aws-lc-sys`, `native-tls`, `cmake`,
`pkg-config`, `bindgen`, `vcpkg`, `bzip2-sys`, `curl-sys`, `libz-sys`,
`zstd-sys`, `lz4-sys`, `libsqlite3-sys`. `cargo deny check` passes.

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
| 2b | Cross-spring storage IPC + ionic bond ledger | NestGate team | **Done** (April 11) — `storage.retrieve_range`, `storage.object.size`, `bonding.ledger.{store,retrieve,list}` |
| 3 | CR-01 deny.toml alignment | coralReef team | **Done** (Iter 79, April 11) |
| 4 | BC-08 cpu-shader default-on | barraCuda team | **Done** (Sprint 40, April 11) |
| 5 | BC-07 SovereignDevice fallback wiring | barraCuda team | **Done** (Sprint 41, April 11) |
| 6 | Ecosystem `cargo deny check` CI enforcement | primalSpring (infra) | Sprint+2 |
