<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 61 Handoff

**Date**: March 21, 2026
**Primal**: coralReef
**Phase**: 10 — Spring Absorption + Compiler Hardening
**Iteration**: 61

---

## Summary

Dependency injection architecture session: four crates gained testable surfaces
through trait abstraction, library/binary splits, and pure-parsing extraction.
coral-ember split into lib + thin binary. coral-glowplug gained `SysfsOps` trait
for mock-based device management testing. coral-gpu gained `GpuContext::from_parts`
+ session-local compile cache. coral-driver gained pure parsing functions for
firmware, PCI, VBIOS, and devinit scripts. Coverage rose from 65.8% to 67.6% line
(+244 tests: 3062 → 3306, 0 failures). Six crates now exceed 90% target. Remaining
stale primal name references evolved to capability-based descriptions.

---

## Changes

### 1. coral-ember Library/Binary Split

- `src/lib.rs` — New crate root with `#![forbid(unsafe_code)]`, `#![warn(missing_docs)]`
- `src/main.rs` — Thin entry: `coral_ember::run()` + `exit(code)`
- Library exports: `parse_glowplug_config`, `find_config`, `ember_socket_path`,
  `handle_client`, `handle_swap_device`, `verify_drm_isolation_with_paths`,
  `detect_lifecycle`, `HeldDevice`, config types
- `Cargo.toml` gains `[lib]` section alongside `[[bin]]`
- Integration tests in `tests/`: config paths, IPC dispatch, swap, vendor lifecycle

### 2. coral-glowplug `SysfsOps` Trait

- `SysfsOps` trait (`sysfs_ops.rs`): `read_pci_ids`, `read_iommu_group`,
  `read_current_driver`, `read_power_state`, `read_link_width`, `find_drm_card`,
  `has_active_drm_consumers`, `sysfs_write`, `bind_iommu_group_to_vfio`
- `RealSysfs` — zero-sized production impl delegating to `crate::sysfs`
- `MockSysfs` — `#[cfg(test)]` with `HashMap` fields + `Mutex<Vec>` write recording
- `DeviceSlot<S: SysfsOps = RealSysfs>` — backward-compatible generic
- `activate()`, `swap()`, `release()`, `check_health()` route through `self.sysfs`

### 3. coral-gpu `GpuContext::from_parts`

- `GpuContext::from_parts(target, device, options)` — bypasses DRM/VFIO probing
- `compile_wgsl_cached(&mut self, wgsl)` — session-local map keyed by `hash_wgsl`
- `compile_options(&self)` — read-only access to `CompileOptions`
- `open_driver` / `open_driver_at_path` — now `pub(crate)` for error path testing

### 4. coral-driver Parsing Extraction

- GSP: `parse_u32_pairs_from_bytes`, `GrFirmwareBlobs::from_legacy_bytes`,
  `parse_net_img_bytes` — firmware parsing on `&[u8]` without file I/O
- PCI: `parse_pci_bdf`, `pci_class_base`, `parse_pci_sysfs_hex_id`,
  `parse_pci_resource_line`, `parse_sysfs_pcie_speed/width/power_state`
- VBIOS: `validate_vbios` pub(crate), `BitTable::parse` testable
- Devinit: `scan_init_script_writes` with crafted byte sequences
- Memory: `pramin_window_layout` extracted from `PraminRegion::new`

### 5. Primal Name Evolution

Remaining hardcoded primal names evolved to capability-based descriptions:
- `Songbird proxy` → `Delegated TLS` (primal-rpc-client docs)
- `BearDog crypto delegation` → `ecosystem crypto delegation`
- `hotSpring Exp 051` → `Ecosystem Exp-051` (coral-driver ioctl)
- `hotSpring P3 request` → `ecosystem P3 review` (personality.rs)
- `groundSpring` → `numerical validation service` (tolerances, tol, lower_f64)
- `healthSpring` → `ecosystem health monitoring` (tolerances.rs)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests passing | 3062 | 3306 |
| Tests failed | 0 | 0 |
| Tests ignored | 102 | 108 |
| Line coverage | 65.8% | 67.6% |
| Crates above 90% | 5 | 6 |

### Per-Crate Coverage

| Crate | Coverage | Notes |
|-------|----------|-------|
| coralreef-core | 95.9% | Above target |
| primal-rpc-client | 98.4% | Above target |
| coral-reef-stubs | 95.2% | Above target |
| coral-reef-bitview | 91.3% | Above target |
| coral-reef-isa | 100.0% | Above target |
| amd-isa-gen | 91.3% | Above target |
| nak-ir-proc | 88.6% | Near target |
| coral-reef | 78.6% | Remaining: emit.rs, spiller.rs, ISA encoders |
| coral-gpu | 65.8% | Hardware-gated DRM/VFIO paths |
| coral-ember | 65.2% | run() daemon loop needs VFIO |
| coral-glowplug | 62.3% | BAR/MMIO/VFIO behind MappedBar/VfioHolder |
| coral-driver | 29.9% | ~70% is raw ioctl/MMIO — needs hardware CI |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | ✅ PASS |
| `cargo clippy --all-features -- -D warnings` | ✅ PASS (0 warnings) |
| `cargo test --all-features` | ✅ PASS (3306 pass, 0 fail, 108 ignored) |
| `cargo doc --all-features --no-deps` | ✅ PASS (0 warnings) |
| All files < 1000 LOC | ✅ PASS |

---

## Architecture Decisions

### Why trait-based DI over `#[cfg(test)]` mocks?

Trait-based DI (`SysfsOps`, `ComputeDevice`) is preferred because:
- Tests exercise real production code paths, not `#[cfg(test)]` alternates
- The abstraction boundary is explicit and documented
- Generic defaults (`DeviceSlot<S = RealSysfs>`) maintain backward compatibility
- Mock injection catches integration bugs that `#[cfg(test)]` stubs hide

### Why lib/binary split for coral-ember?

Binary-only crates cannot be imported by integration tests (`tests/`). Splitting
into lib + thin main enables:
- Integration tests importing `coral_ember::handle_client` etc.
- Downstream crates (if ever needed) importing ember types
- Better code organization: daemon logic is library, startup is binary

---

## Cross-Primal Notes

- **No API breaks** — all public surfaces are additive
- **No new primal references** — zero hardcoded primal names in production code
- **Capability-based discovery** unchanged — `shader.compile.*`, `health.*` methods
- **IPC protocol** unchanged — JSON-RPC 2.0 + tarpc, same method names

---

## Next Steps (Iter 62+)

| Task | Priority | Detail |
|------|----------|--------|
| coral-reef emit.rs/spiller.rs coverage | P1 | Builder-level unit tests, fix lop2.and encoding gap |
| MappedBar/VfioHolder DI traits | P2 | Unlock coral-glowplug/ember health/resurrect testing |
| Hardware CI | P2 | VFIO Titan V for coral-driver coverage |
| coral-driver unsafe reduction | P3 | Continue mmap/munmap → safe wrapper evolution |
| tarpc OpenTelemetry upstream | P3 | Track mio#1735 and tarpc unconditional otel |
