# coralReef — Phase 10 Iteration 35 Handoff

**Date**: March 11, 2026
**Commit**: `1dfbaff` (pushed to `origin/main`)
**Tests**: 1616 passing, 0 failed, 55 ignored

---

## Summary

Three evolution tracks completed:

1. **FirmwareInventory + compute_viable()** — Absorbs the `hw-learn` pattern from the toadStool handoff. Structured firmware probe for 6 subsystems (ACR, GR, SEC2, NVDEC, PMU, GSP) per GPU chip. `compute_viable()` reports whether nouveau compute dispatch can succeed: requires GR firmware + either PMU (Volta/Turing) or GSP (Ampere+). `compute_blockers()` returns human-readable list of missing components.

2. **drm_ioctl_typed elimination** — All 7 legacy `drm_ioctl_typed` call sites migrated to `drm_ioctl_named` with operation-specific names (`nouveau_channel_alloc`, `nouveau_channel_free`, `nouveau_gem_new`, `nouveau_gem_info`, `nouveau_gem_pushbuf`, `nouveau_gem_cpu_prep`, `diag_channel_alloc`). Dead `drm_ioctl_typed` function removed. Every DRM ioctl failure now reports which operation failed.

3. **Unsafe reduction** — 29 → 24 unsafe blocks. All confined to `coral-driver` kernel ABI boundary. 8 of 9 crates enforce `#[deny(unsafe_code)]`.

---

## Files Changed

| File | Change |
|------|--------|
| `crates/coral-driver/src/nv/identity.rs` | `FwStatus`, `FirmwareInventory`, `firmware_inventory()`, `compute_viable()`, `compute_blockers()` + 4 tests |
| `crates/coral-driver/src/nv/ioctl/diag.rs` | Re-exports `FirmwareInventory`, `FwStatus`, `firmware_inventory`; migrated `drm_ioctl_typed` → `drm_ioctl_named` |
| `crates/coral-driver/src/nv/ioctl/mod.rs` | Re-exports new types; 6 ioctl calls migrated to `drm_ioctl_named` |
| `crates/coral-driver/src/drm.rs` | Dead `drm_ioctl_typed` function removed |
| `EVOLUTION.md` | Updated to Iteration 35 |
| `STATUS.md` | Updated to Iteration 35 |
| `WHATS_NEXT.md` | Updated to Iteration 35 |

---

## For hotSpring

- `FirmwareInventory` confirms Titan V GV100 PMU firmware is **missing** — this is why `CHANNEL_ALLOC` returns EINVAL even after the Exp 057 ABI fixes
- Use `coral_driver::nv::ioctl::firmware_inventory("gv100")` to probe before attempting dispatch
- `compute_viable()` returns `false` for GV100 (missing PMU, no GSP fallback on Volta)

## For toadStool

- The `hw-learn` observe→distill→apply pattern is now partially absorbed as `FirmwareInventory`
- Next step: wire `compute_viable()` into `shader.compile.capabilities` IPC response (Iter 36)
- Enables capability-based routing: if `!compute_viable()`, route to nvidia-drm render node

## For barraCuda

- `drm_ioctl_named` error messages now include operation names — facilitates multi-GPU dispatch debugging
- `FirmwareInventory` available for per-GPU dispatch viability checking before attempting kernel channel allocation

---

## Iteration 36 Candidates

- Wire `FirmwareInventory` into `shader.compile.capabilities` IPC response
- Probe-at-startup caching for firmware inventory (avoid repeated sysfs reads)
- Automatic dispatch fallback: skip nouveau channel alloc when PMU missing → report `Dispatch::Unavailable`
- Evolve showcase `ecosystem_socket()` to use discovery manifest
