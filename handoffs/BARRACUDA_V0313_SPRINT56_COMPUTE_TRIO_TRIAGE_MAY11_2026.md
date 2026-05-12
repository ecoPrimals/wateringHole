# barraCuda v0.3.13 — Compute Trio Wave 8 Audit Triage

**Date**: 2026-05-11  
**Sprint**: 56  
**Audit source**: primalSpring downstream — Compute Trio Evolution Wave 8  
**Primal**: barraCuda (WHAT — math/physics domain)

---

## Item 1: Absorb bearDog crypto IPC (Wave 101) — DEFERRED

### Finding

primalSpring requests that barraCuda delegate embedded `chacha20poly1305`/`hkdf`/`hmac`
deps in `barracuda-core` to bearDog IPC, citing Wave 101 availability of
`crypto.hkdf_sha256` and `crypto.hmac_verify`.

### Investigation

| Crypto usage | Location | Call frequency | bearDog IPC available? |
|---|---|---|---|
| `hkdf::Hkdf<Sha256>` | `btsp.rs` L559-569 | **One-shot per connection** | Yes (`crypto.hkdf_sha256`) |
| `hmac::Hmac<Sha256>` | `btsp_frame.rs` L18,26 | **Per-frame** (hot path) | Yes (`crypto.hmac_verify`) |
| `chacha20poly1305::ChaCha20Poly1305` | `btsp_frame.rs` L14-17 | **Per-frame** (hot path) | **No** — no AEAD surface |

### Conclusion

1. **HKDF** (one-shot per connection): *Could* be delegated to `crypto.hkdf_sha256`, but
   it's 4 lines of inline code executed once per BTSP negotiation. The IPC roundtrip
   (UDS connect → serialize → dispatch → deserialize) adds complexity and a bearDog
   availability dependency for no practical gain.

2. **HMAC** (per-frame): `crypto.hmac_verify` exists, but delegating per-frame HMAC
   verification to IPC introduces a full roundtrip per message. At 10k+ msgs/sec
   throughput targets, this is prohibitive.

3. **ChaCha20-Poly1305** (per-frame AEAD): bearDog does **not** expose
   `crypto.aead_encrypt`/`crypto.aead_decrypt`. Even if it did, per-frame IPC
   delegation for AEAD is architecturally unsound (same latency argument as HMAC).

4. **Dependency elimination impossible**: Even delegating HKDF wouldn't remove any
   `Cargo.toml` deps — `hmac`, `sha2`, and `chacha20poly1305` remain for per-frame ops.

### Status: DEFERRED

Consistent with May 11 crypto dedup triage. Correct long-term path remains a shared
`btsp-crypto` crate at ecosystem level, not IPC delegation for hot-path operations.

---

## Item 2: Wire SovereignDevice through trio IPC — ALREADY DONE

### Finding

primalSpring requests that `SovereignDevice` call `shader.compile.wgsl` on coralReef
and `compute.dispatch.submit` on toadStool via IPC.

### Investigation

Both paths are **fully implemented** since Sprint 48:

| Path | Implementation | Discovery |
|---|---|---|
| `shader.compile.wgsl` → coralReef | `coral_compiler/mod.rs` → `GLOBAL_CORAL.compile_wgsl_direct()` | Capability-based: env → UDS socket → manifest scan → port probe |
| `compute.dispatch.submit` → toadStool | `sovereign_device.rs` → `submit_dispatch()` | Capability-based: env → manifest scan (`compute.dispatch*`) |

The E2E sovereign path matches the primalSpring contract:

```
SovereignDevice::dispatch_compute()
  → live_compile() → GLOBAL_CORAL.compile_wgsl_direct("shader.compile.wgsl")
  → submit_dispatch() → TcpStream POST ("compute.dispatch.submit")
  → readback output_buffers
```

Feature gate: `sovereign-dispatch` (enabled with `gpu` feature).

### Status: ALREADY IMPLEMENTED — no action required

---

## Item 3: Exercise 4-tier fallback — ALREADY IMPLEMENTED

### Finding

primalSpring requests `Auto::new()` correctly tries sovereign → wgpu → cpu → scalar.

### Investigation

`Auto::new()` in `crates/barracuda/src/device/mod.rs` implements:

1. **wgpu GPU** (Vulkan/Metal/DX12) — fastest local path
2. **wgpu CPU** (software rasterizer) — universal fallback
3. **SovereignDevice IPC** (compile + dispatch peers) — when no local GPU
4. **Err** → caller degrades to cpu-shader (scalar tier)

The order is intentionally wgpu-first for latency (local GPU < IPC roundtrip). The
"scalar" tier is handled at `BarraCudaPrimal::start` level — if `Auto::new()` errors,
the primal runs degraded with cpu-shader only.

### Status: ALREADY IMPLEMENTED — architecturally correct order

---

## Item 4: Gate 3 — stats.mean — ALREADY PASSING

### Finding

primalSpring Compute Trio Gate 3: `stats.mean([2, 4, 6, 8]) = 5.0` round-trip.

### Investigation

- `stats.mean` registered in method table (1 of 71 methods)
- Dispatched to `math::stats_mean` in `mod.rs`
- 3 coverage tests pass: `stats_mean_happy_path`, `stats_mean_missing_data`, `stats_mean_empty_data`
- CPU fallback always works — no GPU required

### Status: ALREADY PASSING — no action required

---

## Summary

| Audit Item | Status | Action Required |
|---|---|---|
| bearDog crypto IPC delegation | **DEFERRED** | None — per-frame IPC latency prohibitive; no AEAD surface in bearDog |
| Wire SovereignDevice through trio IPC | **ALREADY DONE** | None — compile + dispatch wired since Sprint 48 |
| 4-tier fallback exercise | **ALREADY DONE** | None — wgpu → cpu → sovereign → scalar degradation live |
| Gate 3: `stats.mean` | **ALREADY PASSING** | None — 3 tests pass |

**barraCuda is compute trio ready.** The sovereign dispatch E2E path will activate
automatically when coralReef and toadStool are both discoverable in the composition.
No code changes required on our side.
