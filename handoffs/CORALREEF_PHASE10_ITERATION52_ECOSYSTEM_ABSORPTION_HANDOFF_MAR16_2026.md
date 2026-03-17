# coralReef — Phase 10 Iteration 52 Handoff

**Date**: March 16, 2026  
**Iteration**: 52 — Ecosystem Absorption + Glowplug JSON-RPC 2.0 + Typed IPC Errors  
**Tests**: 2185 passing (+48 VFIO), 0 failed, 90 ignored  
**Clippy**: Zero warnings (pedantic)  
**Format**: Clean (`cargo fmt`)

---

## Summary

Major ecosystem absorption iteration. Executed on all priorities identified from
cross-primal and cross-spring review. Seven hotSpring glowplug hardening items
addressed. Ecosystem patterns from rhizoCrypt, loamSpine, wetSpring absorbed
into coralreef-core.

## Changes

### 1. deny.toml Enrichment
- `yanked` upgraded from `"warn"` to `"deny"` — blocks yanked crate versions.
- `wildcards` already `"deny"` — confirmed aligned.
- tarpc at 0.37 — confirmed aligned with ecosystem.
- No `once_cell` usage found — no `LazyLock` migration needed.

### 2. OrExit<T> Pattern (from wetSpring/rhizoCrypt)
- **New module**: `coralreef-core/src/or_exit.rs`
- Zero-panic validation for binary entry points.
- `Result::or_exit("context")` and `Option::or_exit("context")` extensions.
- Replaces `unwrap()`/`expect()` with `tracing::error!` + `process::exit(1)`.
- 2 unit tests.

### 3. IpcServiceError — Structured IPC Errors (from rhizoCrypt/loamSpine)
- **New module**: `coralreef-core/src/ipc/error.rs`
- `IpcPhase` enum: `Transport`, `Dispatch`, `Handler`, `Internal`.
- `IpcServiceError` with phase, message, optional error code.
- Phase-aware JSON-RPC error codes (-32000, -32601, -32603).
- `retryable()` method for caller retry decisions.
- Serde-serializable for wire transmission.
- 7 unit tests.
- **Migration**: Unix JSON-RPC dispatch now returns `IpcServiceError` instead
  of raw `String`. All 40+ tests updated.

### 4. coral-glowplug: JSON-RPC 2.0 Socket Protocol (hotSpring P1)
- **Rewritten**: `socket.rs` from custom `Request`/`Response` enums to proper
  JSON-RPC 2.0 newline-delimited protocol.
- Semantic method names: `device.list`, `device.get`, `device.swap`,
  `device.health`, `device.resurrect`, `health.check`, `health.liveness`,
  `daemon.status`, `daemon.shutdown`.
- Proper error codes: -32700 (parse), -32600 (invalid request), -32601 (method
  not found), -32602 (invalid params), -32603 (internal), -32000 (server).
- toadStool and hotSpring can now use standard JSON-RPC 2.0 clients.

### 5. coral-glowplug: Trait-Based GpuPersonality (hotSpring P3)
- **New module**: `personality.rs`
- `GpuPersonality` trait: `name()`, `provides_vfio()`, `drm_card()`,
  `supports_hbm2_training()`, `driver_module()`.
- Concrete implementations: `VfioPersonality`, `NouveauPersonality`,
  `AmdgpuPersonality`, `UnboundPersonality`.
- `PersonalityRegistry` for runtime personality discovery.
- `Personality` enum preserved for zero-allocation storage in `DeviceSlot`.
- 7 unit tests.

### 6. coral-glowplug: CAP_SYS_ADMIN (hotSpring P6)
- **Removed**: `sudo tee` fallback from `sysfs_write()`.
- Direct `std::fs::write()` with structured tracing on failure.
- Guidance: use systemd `AmbientCapabilities=CAP_SYS_ADMIN` or `setcap`.

### 7. coral-glowplug: DRM Consumer Fence Check (hotSpring P7)
- **New function**: `has_active_drm_consumers(bdf)`.
- Scans `/proc/*/fd` for symlinks to the device's DRM render nodes.
- Called before nouveau bind in `resurrect_hbm2()`.
- Waits 2s if consumers found, logs error if still active.

### 8. AMD Vega Metal Registers (amd_metal.rs)
- Evolved from TODO stubs to real MI50/GFX906 register layout.
- GRBM, SRBM, CP, SDMA0/SDMA1, RLC, MMHUB domain offsets.
- PowerDomains: GFX, SYS, RLC with enable registers.
- MemoryRegions: HBM2_FB (16 GB, 4 partitions), GART, L2_CACHE.
- Engines: GFX (compute), SDMA0 (copy), SDMA1 (copy).
- 8 register domains with offset ranges.
- Warmup sequence: GRBM/SRBM status verification.

### 9. Dual-Format Capability Parsing
- Discovery module now accepts both flat strings and nested objects
  for `provides` field in capability.list responses.
- `CapabilityRef` custom deserializer: `"gpu.dispatch"` OR
  `{"id": "gpu.dispatch", "version": "0.1.0"}`.
- Addresses neuralSpring S156 ecosystem standardization gap.
- 3 new tests.

## Test Impact

| Metric | Before | After |
|--------|--------|-------|
| Total passing | 2157 | 2185 |
| New tests | — | +28 |
| Failed | 0 | 0 |
| Ignored | 89 | 90 |

## Files Modified

### New Files
- `crates/coralreef-core/src/or_exit.rs`
- `crates/coralreef-core/src/ipc/error.rs`
- `crates/coral-glowplug/src/personality.rs`

### Modified Files
- `deny.toml` — yanked: deny
- `README.md` — iteration 52, test counts
- `STATUS.md` — iteration 52, test counts
- `WHATS_NEXT.md` — iteration 52
- `crates/coralreef-core/src/lib.rs` — or_exit module
- `crates/coralreef-core/src/ipc/mod.rs` — error module
- `crates/coralreef-core/src/ipc/unix_jsonrpc.rs` — IpcServiceError dispatch
- `crates/coralreef-core/src/ipc/tests_unix.rs` — error type updates
- `crates/coralreef-core/src/ipc/tests_unix_edge.rs` — error type updates
- `crates/coralreef-core/src/discovery.rs` — dual-format CapabilityRef
- `crates/coral-glowplug/src/main.rs` — personality module
- `crates/coral-glowplug/src/device.rs` — personality import, sysfs_write, DRM fence
- `crates/coral-glowplug/src/socket.rs` — JSON-RPC 2.0 protocol
- `crates/coral-driver/src/vfio/amd_metal.rs` — GFX906 registers

## hotSpring Request Status

| # | Request | Status |
|---|---------|--------|
| P1 | JSON-RPC 2.0 socket protocol | **DONE** |
| P2 | SCM_RIGHTS fd passing | Deferred (requires Unix crate changes) |
| P3 | Trait-based GpuPersonality | **DONE** |
| P4 | AMD Vega metal implementation | **DONE** (registers filled) |
| P5 | GP_PUT DMA read fix | Deferred (requires hardware testing) |
| P6 | CAP_SYS_ADMIN capability | **DONE** (sudo removed) |
| P7 | DRM consumer fence check | **DONE** |

## Remaining Blockers

- SCM_RIGHTS fd passing (P2) requires tokio Unix socket ancillary data support.
- GP_PUT DMA read fix (P5) needs VFIO hardware for verification.
- Coverage at ~58% — target 90% requires more unit tests for codegen paths.
