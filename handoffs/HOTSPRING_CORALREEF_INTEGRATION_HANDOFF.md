# hotSpring × coralReef Integration Handoff

**Date:** March 9, 2026
**hotSpring:** v0.6.24 | **barraCuda:** v0.3.3 (`27011af`) | **coralReef:** Phase 10, Iter 26
**License:** AGPL-3.0-only

---

## Executive Summary

coralReef is now live and integrated with hotSpring via barraCuda's IPC client.
The full sovereign pipeline — WGSL → native GPU binary — is operational for
44/46 standalone hotSpring physics shaders across SM70 (Titan V) and SM86 (RTX 3090)
targets (Iter 26 fixed f64 Min/Max/Abs/Clamp → `batched_hfb_energy_f64` now compiles).
`ComputeDevice: Send + Sync` resolved — full `GpuBackend` trait implemented via
`Mutex<GpuContext>`. GPU dispatch awaits coral-driver DRM backend maturation.

## What Was Done

### Phase 1: Build and Start coralReef Daemon
- Built `coralreef-core` from local checkout (`cargo build --release -p coralreef-core`)
- Started daemon: JSON-RPC on TCP + Unix socket, tarpc on Unix socket
- Doctor check: all capabilities healthy, SM70-SM89 architectures supported
- Discovery manifest auto-written to `$XDG_RUNTIME_DIR/ecoPrimals/coralreef-core.json`
- Hello-compiler showcase: compiled WGSL to 288-byte SM86 SASS binary (10 instructions, 22 GPR)

### Phase 2: Discovery Fix and E2E Validation
**Discovery gap found and fixed**: barraCuda's `discovery.rs` expected pre-Phase 10
manifest format (`"capabilities"` array, string `transports.jsonrpc`), but coralReef
Phase 10 uses `"provides"` array and object-form transports (`{"tcp": "...", "path": "..."}`).

**Local evolution in barraCuda** (2 files):
- `discovery.rs`: `read_capability_transport()` now checks both `"provides"` and `"capabilities"`
- `discovery.rs`: `read_jsonrpc_from_value()` extracts `tcp` field from object-form transport
- `mod.rs`: `test_reset_allows_rediscovery` accepts both `"coralReef"` and `"coralreef-core"` names

**Result**: barraCuda's 15/15 coral_compiler tests pass with coralReef live.
hotSpring's 769/769 lib tests pass. coralReef server logs show active compilation
requests during hotSpring runs.

### Phase 3: Benchmarks with coralReef Live

| Lattice | CPU ms/traj | GPU ms/traj | Speedup | ΔPlaq |
|---------|------------|-------------|---------|-------|
| 4^4 | 73.2 | 10.7 | 6.9× | 0.000991 |
| 8^4 | 1213.0 | 33.3 | 36.5× | 0.000681 |

Sovereign FMA benchmark: 498 FMA fusions across 46 standalone shaders (10.8 avg/shader).

### Phase 4: Sovereign Dispatch Proof of Concept

**New feature**: `sovereign-dispatch` in barraCuda and hotSpring
- `coral-gpu` added as optional dependency via path patches (`.cargo/config.toml`)
- `CoralReefDevice` evolved from scaffold to functional in-process compiler
- `validate_sovereign_compile` binary: compiles 46 hotSpring physics WGSL shaders
  to native SM70/SM86 SASS binaries via coral-gpu (no daemon, no Vulkan, no vendor SDK)

**Compilation results (Iter 26)**: 44/46 shaders compile to native binaries per target.
~213 KB total native binary output per architecture.

### Iter 26 Blockers Resolved

1. **f64 Min/Max/Abs/Clamp** — root cause of log2 panic. `Min`, `Max`, `Abs`, `Clamp`
   were truncating f64 to 1 component. Fixed via `OpDSetP` + per-component `OpSel`.
   `batched_hfb_energy_f64` now compiles.
2. **`ComputeDevice: Send + Sync`** — trait bound added in coral-driver. `CoralReefDevice`
   now holds `Mutex<GpuContext>` and implements full `GpuBackend` trait.
3. **Nouveau compute subchannel** — `create_channel()` now binds compute engine class
   based on SM version. Still EINVAL on GV100 — deeper kernel-side NVIF setup needed.

### Remaining coralReef Gaps

1. **`deformed_potentials_f64`** — panics at `func_math_helpers.rs:143` with SSARef
   index out of bounds. Different code path from the Iter 26 f64 fix.
2. **DRM dispatch maturity**:
   - nouveau: compute subchannel bound but channel creation EINVAL on GV100
   - nvidia-drm: UVM integration not implemented for buffer allocation
   - amdgpu: E2E ready (verified in coralReef Phase 10)

## Files Changed

### barraCuda (local evolution for upstream absorption)
- `crates/barracuda/src/device/coral_compiler/discovery.rs` — Phase 10 manifest compat
- `crates/barracuda/src/device/coral_compiler/mod.rs` — health name assertion fix
- `crates/barracuda/src/device/coral_reef_device.rs` — sovereign-dispatch PoC impl
- `crates/barracuda/src/device/mod.rs` — coral_gpu re-export
- `crates/barracuda/Cargo.toml` — coral-gpu optional dep + sovereign-dispatch feature
- `.cargo/config.toml` — coralReef path patches

### hotSpring
- `barracuda/Cargo.toml` — sovereign-dispatch feature propagation
- `barracuda/.cargo/config.toml` — coralReef path patches
- `barracuda/src/bin/validate_sovereign_compile.rs` — PoC compilation binary
- `barracuda/ABSORPTION_MANIFEST.md` — coralReef integration documentation

## Write-Absorb-Lean Status

| Change | Status | Upstream Target |
|--------|--------|----------------|
| Discovery Phase 10 compat | **Write** (local) | barraCuda `discovery.rs` |
| Health name assertion | **Write** (local) | barraCuda `mod.rs` |
| `sovereign-dispatch` feature | **Write** (local) | barraCuda `Cargo.toml` |
| `CoralReefDevice` impl | **Write** (local) | barraCuda `coral_reef_device.rs` |
| `coral_gpu` re-export | **Write** (local) | barraCuda `device/mod.rs` |
| f64 Min/Max/Abs/Clamp | ✅ **Resolved** (Iter 26) | coralReef `func_math.rs` |
| `ComputeDevice: Send + Sync` | ✅ **Resolved** (Iter 26) | coral-driver `lib.rs` |
| `CoralReefDevice` full GpuBackend | **Write** (local) | barraCuda `coral_reef_device.rs` |
| `deformed_potentials_f64` SSARef gap | **Filed** | coralReef `func_math_helpers.rs` |
| DRM dispatch maturity | **In progress** (upstream) | coral-driver backends |
