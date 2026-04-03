# toadStool S171 — Ember Absorption + Unsafe Evolution + Deep Debt

**Date**: April 1, 2026
**Session**: S171
**Primal**: toadStool (Universal Hardware)
**Quality**: `cargo check --workspace` clean, `cargo test` all passing, 0 clippy warnings

---

## Summary

S171 executes three major evolutions:

1. **Unsafe containment** — Created `toadstool-hw-safe` as the single unsafe zone for hardware primitives, migrated 4+ crates to use it
2. **Ember absorption** — toadStool now owns device lifecycle natively (no coral-ember dependency)
3. **Deep debt completion** — distributed crate fully documented, hardcoding evolved, glowPlug/ember subsystem scaffolded

---

## New Crates

### `toadstool-hw-safe` (crates/core/hw-safe)
Single unsafe containment zone for hardware primitives:
- `SafeMmapRegion` — RAII mmap/munmap wrapper, `map_shared_rw`/`map_shared_ro`
- `VolatileMmio` — bounds-checked `read_u32`/`write_u32` over MMIO regions
- `AlignedAlloc` — RAII aligned heap allocation (replaces manual `std::alloc`)

### `toadstool-glowplug` (crates/core/glowplug)
Hardware-agnostic device lifecycle interface:
- `DeviceId` — PCI BDF, USB Path, SysfsPath, DevNode, Serial, Platform
- `DevicePersonality` + `PersonalityRegistry` — driver modes and management
- `DeviceSlot` — managed device with personality, health, journal
- `FirmwareInterface` — abstraction for Falcon, UEFI/BIOS, NPU microcode
- `HealthProbe`, `DeviceDiscovery`, `SwapOrchestrator`
- Re-exports `toadstool-ember` as `ember` subsystem

### `toadstool-ember` (crates/core/ember)
Hardware-agnostic device holder (subsystem inside glowPlug):
- `ResourceHandle` trait — exclusive hardware access (VFIO fds, USB claims)
- `MetadataStore` — opaque per-device key/value persistence
- `HeldResource` — pairs ResourceHandle with metadata and lifecycle tracking
- `LendReceipt` — lending and reclaiming held resources
- `SwapJournal` — immutable lifecycle event log

---

## Unsafe Evolution

### Migrations to hw-safe
| Source | File | Change |
|--------|------|--------|
| akida-driver | `backends/mmap.rs` | `MmapRegion` → `SafeMmapRegion` delegate. Zero unsafe in mmap.rs. |
| nvpmu | `bar0.rs` | `Bar0Access` → `SafeMmapRegion` + `VolatileMmio`. Zero hand-rolled volatile. |
| runtime/gpu | `backends/cpu.rs` | `CpuAllocation` now holds `AlignedAlloc`. Zero unsafe. |
| runtime/gpu | `memory/pinned.rs` | `PinnedMemory` → `AlignedAlloc`. Zero unsafe. |

### SAFETY documentation
Added `// SAFETY:` comments to all remaining `output_from_ptr` ioctl implementations:
- `nvpmu/dma.rs`, `nvpmu/vfio.rs`
- `akida-driver/vfio/ioctl.rs`, `akida-driver/mmio.rs`
- `hw-learn/nouveau_drm.rs`

### Unsafe surface reduction
- Before S171: ~70+ unsafe operations across 17 files in 6 crates
- After S171: ~26 irreducible unsafe operations, all wrapped in safe APIs via `hw-safe`
- GPU FFI reclassified as firmware boundary (FECS/GPCCS/PMU are read-only observations)

---

## Ember Absorption (coral-ember → toadStool-native)

### GpuFirmwareProxy → GpuFirmwareAccess
- **Before**: Proxied FECS/GPCCS/PMU queries to coral-ember via JSON-RPC over Unix socket
- **After**: Direct BAR0 register reads via `nvpmu::Bar0Access` (backed by `SafeMmapRegion`)
- Defined Falcon register map: FECS `0x409000`, GPCCS `0x41A000`, PMU `0x10A000`
- CPUCTL at `+0x100`, PC at `+0x104`, halted bit `0x10`
- File: `crates/runtime/gpu/src/glowplug/firmware.rs`

### glowplug_client.rs → toadStool-native service
- **Before**: Discovered `coral-ember-default.sock` via `CORALREEF_EMBER_*` env vars, used `UnixJsonRpcClient`
- **After**: PCI sysfs enumeration (`/sys/bus/pci/devices/*/class`), `driver_override` + rebind for personality swaps
- Methods are synchronous (no async IPC needed for local sysfs operations)
- File: `crates/server/src/glowplug_client.rs`

---

## Hardcoding Evolution

| Item | Before | After |
|------|--------|-------|
| TCP bind address | `"0.0.0.0"` literal | `TOADSTOOL_BIND_ADDRESS` env var with `"0.0.0.0"` default |
| Gate ID | `HOSTNAME` only | `TOADSTOOL_GATE_ID` preferred, `HOSTNAME` fallback |
| Load balancer self | `LOCALHOST_IPV4` constant | `self_node_id()` method (env-driven) |
| Network configurator | 12+ inline magic numbers | Named constants + env overridable (`TOADSTOOL_SIDECAR_IMAGE`, `TOADSTOOL_AUDIT_LOG_PATH`) |

---

## Documentation

- **distributed crate**: All ~400 `missing_docs` warnings resolved. `#![allow(missing_docs)]` removed.
- Documented: `songbird_integration/types/` (12 files), `cloud/` (19 files), `beardog_integration/`, `security_provider/`, `primal_capabilities/`, `crypto_lock/`, `crypto_integration/`, `coordination_integration/`, and 7 more modules.

---

## Root Doc Updates

- `README.md` — S171 session stamps, project structure includes new crates, unsafe surface updated, glowPlug/ember narrative
- `CHANGELOG.md` — S170 + S171 sections added
- `DOCUMENTATION.md` — S171 current state, glowPlug/ember subsystem
- `NEXT_STEPS.md` — S171 header and latest summary
- `CONTEXT.md` — Compute Trio roles updated (barraCuda=math, toadStool=hardware, coralReef=compiler)
- `DEBT.md` — Active debt updated (D-IOCTL-TYPED, D-LOCKED-MEMORY), S171 resolved items
- `biome.yaml` — License fixed AGPL-3.0-or-later → AGPL-3.0-only
- `.envrc` — Removed stale PyO3 exports (pyo3 removed in S169)

---

## Files Changed

### New files
- `crates/core/hw-safe/` (entire crate: Cargo.toml, src/lib.rs, safe_mmap.rs, volatile_mmio.rs, aligned_alloc.rs)
- `crates/core/glowplug/` (entire crate: Cargo.toml, src/lib.rs, device_id.rs, personality.rs, device_slot.rs, firmware.rs, health.rs, discovery.rs, swap.rs)
- `crates/core/ember/` (entire crate: Cargo.toml, src/lib.rs, resource_handle.rs, metadata.rs, held_resource.rs, lend_reclaim.rs, journal.rs)
- `crates/runtime/gpu/src/glowplug/` (mod.rs, personality.rs, firmware.rs, discovery.rs)

### Modified files (significant)
- `crates/neuromorphic/akida-driver/src/backends/mmap.rs` — SafeMmapRegion migration
- `crates/core/nvpmu/src/bar0.rs` — SafeMmapRegion + VolatileMmio migration
- `crates/runtime/gpu/src/unified_memory/backend.rs` — CpuAllocation holds AlignedAlloc
- `crates/runtime/gpu/src/unified_memory/backends/cpu.rs` — AlignedAlloc migration
- `crates/runtime/gpu/src/memory/pinned.rs` — AlignedAlloc migration
- `crates/server/src/glowplug_client.rs` — coral-ember proxy → native service
- `crates/runtime/gpu/src/glowplug/firmware.rs` — GpuFirmwareProxy → GpuFirmwareAccess
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — sync ember handlers
- `crates/distributed/src/lib.rs` — missing_docs resolved
- ~50 files in distributed crate with new doc comments

---

## Remaining Debt (for next session)

| ID | Description | Priority |
|----|-------------|----------|
| D-COV | Test coverage → 90% (currently ~80%) | Medium |
| D-IOCTL-TYPED | VFIO ioctl dispatch → typed per-operation modules | Low |
| D-LOCKED-MEMORY | Compose AlignedAlloc + mlock into LockedMemory RAII type | Low |
| D-EMBEDDED-PROGRAMMER | Embedded ISP/ICSP programmer impls (placeholder errors) | Low |
| D-EMBEDDED-EMULATOR | MOS 6502 / Z80 emulator impls (placeholder errors) | Low |

---

*toadStool S171 — sovereign hardware, zero external dependency for device lifecycle.*
