# toadStool S172 — Deep Debt Evolution Plan (6 Phases)

**Date**: April 2, 2026
**Session**: S172
**Primal**: toadStool (Universal Hardware)
**Quality**: `cargo check --workspace` clean, `cargo test --workspace` all passing (21,500+ tests, 0 failures), 0 clippy warnings

---

## Summary

S172 executes a comprehensive 6-phase deep debt evolution plan:

1. **Production stubs → real implementations** — 6 distributed stubs evolved, feature gating, typed errors
2. **Hardcoding → capability-based** — `CapabilityDomain` enum, sysfs discovery, port evolution
3. **Unsafe evolution** — `LockedMemory` RAII type, typed ioctl wrappers, BYOB health loop wired
4. **Smart refactoring** — 3 large files decomposed into coherent submodules
5. **memmap2 migration** — hand-rolled mmap replaced, 4 unsafe blocks eliminated
6. **Coverage expansion** — +55 tests across hw_learn and transport handlers

---

## Phase 1: Production Stubs → Real Implementations

### distributed/ stubs evolved
| Stub | Evolution |
|------|-----------|
| `validate_delegation_proof` | Real cryptographic proof validation in crypto_lock |
| `CachedResult` | TTL-based cache with `is_valid()` check |
| `CloudCostTracker` | Real cost tracking with `record_cost` and `total_cost` |
| `CloudPerformanceTracker` | Real latency tracking with `record_latency` and `average_latency` |
| `update_node_health` | Real songbird registry node health update |
| `UniversalJobProcessor` | Added `new()` constructor (was `Default` only) |

### Feature gating and error typing
- `TRpcTransport::send_message` gated behind `#[cfg(feature = "tarpc-transport")]`
- CUDA "not implemented" evolved to typed `ToadStoolError::runtime` with operation name and alternative suggestions

---

## Phase 2: Hardcoding → Capability-Based

### CapabilityDomain enum
Created `CapabilityDomain` in `toadstool_common::interned_strings`:
- 7 variants: `Security`, `Coordination`, `Storage`, `Compute`, `Routing`, `Intelligence`, `Monitoring`
- `from_label()` resolves legacy primal names (`beardog` → Security, `songbird` → Coordination, `squirrel` → Routing, etc.)
- Replaced ~30 hardcoded primal name sites across `capability_helpers.rs`, `paths.rs`, `ecosystem/types.rs`

### Sysfs path discovery
- Routed `/dev/dri/card0` and PCI BDF paths through `toadstool_sysmon::gpu::discover_gpus()` and `GpuDevice::card_path()`
- Created `toadstool_sysmon::system::hostname()` to replace direct `/etc/hostname` reads
- Migrated legacy fallback ports to `resolve_env_port()` helper

---

## Phase 3: Unsafe Evolution

### LockedMemory RAII type (hw-safe)
- Composes `AlignedAlloc` + `rustix::mm::mlock`/`munlock`
- RAII: `mlock` on creation, `munlock` on `Drop`
- `Send + Sync` safe, page-aligned convenience constructor
- 5 tests covering creation, Drop, alignment, zero-size edge case

### Typed ioctl wrappers (nvpmu)
- Replaced generic `DmaIoctl<OP, T>` dispatch in `nvpmu/vfio.rs` with typed helper functions:
  - `vfio_get_api_version()`
  - `vfio_group_get_status()`
  - `vfio_device_get_bar0_info()`
- Stronger compile-time safety for VFIO operations

### BYOB health monitoring
- Wired `monitor_deployment_health` into a background `tokio::spawn` task
- Added `health_handles: Arc<RwLock<HashMap<Uuid, JoinHandle<()>>>>` to `ByobComputeExecutor`
- `deploy_biome` spawns health monitor; `stop_deployment` aborts it

### Embedded placeholder evolution
- Evolved macros with clearer feature gating (`embedded-placeholder-impls` vs `embedded-hw`)

---

## Phase 4: Smart Refactoring (3 files)

| Source | Extraction | Purpose |
|--------|-----------|---------|
| `cli/daemon/jsonrpc_server.rs` | `routes.rs` | Route handler functions extracted |
| `core/toadstool/runtime.rs` | `runtime/engine_registry.rs` | Engine management extracted |
| `core/toadstool/byob/byob_impl/mod.rs` | `deployment_lifecycle.rs` | Deployment lifecycle functions |

All production files remain under 400 lines.

---

## Phase 5: memmap2 Migration

### hw-safe/safe_mmap.rs
- Replaced hand-rolled `rustix::mm::mmap`/`munmap` with `memmap2::MmapRaw`
- **4 unsafe blocks eliminated**:
  1. `mmap` syscall in `map_shared_rw`
  2. `mmap` syscall in `map_shared_ro`
  3. Manual `munmap` in `Drop` implementation
  4. `unsafe impl Send + Sync` (memmap2 handles this)
- Only 1 irreducible unsafe remains: `VolatileMmio::new` (raw pointer creation from mmap base)
- Removed unused `map_with_flags`/`map_file`; `MmapFailed` source → `std::io::Error`
- Unsafe surface: ~26 → ~22 irreducible operations

---

## Phase 6: Coverage Expansion

### hw_learn handlers (0% → 80%+)
Tests added to 5 handler files:
- `apply.rs` — recipe application, dry-run mode, missing/invalid parameters
- `observe_distill.rs` — observation recording, knowledge distillation, empty observations
- `share_recipe.rs` — recipe import, store, load, list, missing params
- `status.rs` — GPU status query, empty GPUs, invalid params
- `telemetry.rs` — GPU telemetry reporting, missing GPU ID

Test isolation via `handler_with_temp_store()` helper using `tempfile::TempDir`.

### transport handler (2% → comprehensive)
18 new tests:
- `TransportHandler` constructor, `transport_discover`, `transport_list`
- `transport_route` (error + success with `LoopbackTransport`)
- `transport_open` (error + success paths)
- `transport_stream` (error + happy path streaming)
- `transport_status` (empty, unknown stream, happy path)

### Regression fix
- Fixed `ServiceType::from_capability("routing")` → `Compute` mapping (squirrel/routing regression)

---

## Active Debt (for next session)

| ID | Description | Priority |
|----|-------------|----------|
| D-COV | Test coverage → 90% (currently ~80%, 21,500+ tests) | Medium |
| D-EMBEDDED-PROGRAMMER | Embedded ISP/ICSP programmer impls (placeholder errors) | Low |
| D-EMBEDDED-EMULATOR | MOS 6502 / Z80 emulator impls (placeholder errors) | Low |

---

*toadStool S172 — deep debt evolution, 4 fewer unsafe blocks, capability-domain architecture.*
