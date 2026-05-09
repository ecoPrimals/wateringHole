# coralReef Iteration 93 — hotSpring Merge Hardening + Coverage Expansion

**Date**: May 7, 2026
**Tests**: 4704 passing, 0 failures, 181 ignored (hardware-gated)
**Clippy**: Zero warnings (pedantic + nursery)
**primalSpring Phase**: 60 (only item: transitive libc — no action needed)

---

## Summary

Iteration 93 hardened the codebase after a large hotSpring merge (63 files, +4,403 lines) that introduced new GPU device open paths with hardcoded device paths, undocumented unsafe blocks, and untested hardware logic. All debt has been resolved.

---

## Changes

### Env-Overridable Paths (11 hotSpring regressions fixed)

hotSpring's new `open_userspace.rs`, `open_kmod.rs`, `compute_trait.rs`, and `channel_setup.rs` re-introduced hardcoded `/dev/nvidiactl` and `/dev/nvidia{N}` paths that bypass the existing `nv_ctl_path()` / `nv_gpu_path_prefix()` env-overridable functions from `uvm/constants.rs`.

All 11 instances now use the centralized functions, maintaining testability in container/namespace environments.

### SAFETY Comments (5 added)

hotSpring unsafe blocks in `open_kmod.rs` (4) and `open_userspace.rs` (2) were missing required `// SAFETY:` documentation. All now carry explanations of pointer validity and memory safety invariants.

### Coverage Expansion (10 new tests)

- **`pri.rs` (4 tests)**: Mock-based unit tests for PRI ring management using closure-based register access. Tests hub station parameter writes, privring timing mask correctness, and VBIOS ring init logic (dead hub detection, alive hub confirmation).
- **`pgob.rs` (6 tests)**: Data validation for the PGOB power step table (count, dword alignment, address range) and `PgobOutcome` struct behavior (clone, debug, field access).

### Full Audit Results

| Category | Status |
|----------|--------|
| `Result<_, String>` in production | **Zero** |
| Files over 1000L | **Zero** (all cohesive) |
| Unsafe without SAFETY | **Zero** |
| Mocks in production | **Zero** (all `#[cfg(test)]`) |
| External non-Rust deps | **Zero** (cudarc opt-in, libc upstream) |
| Hardcoded paths in production | **Zero** (kernel ABI paths inherent) |
| `.unwrap()` in library code | **Zero** |
| TODO/FIXME/HACK | **Zero** |

---

## primalSpring Phase 60 Status

Single item: **Transitive libc dependency** via `mio` (tokio's IO reactor). Resolves when upstream `mio` migrates to `rustix` (mio#1735). No action from coralReef.

---

## Architecture Notes

- hotSpring's sovereign GPU boot code (`kepler_cold.rs`, `pgob.rs`, `boot_sequence.rs`, `vbios_devinit.rs`) is pure hardware MMIO — untestable without physical Kepler GPUs. Tests are gated behind `#[ignore]`.
- The `ember_gate.rs` module from hotSpring has excellent mock-based tests (Unix socket simulation).
- PRI ring functions use closure-based register access (`r: &dyn Fn(u32) -> u32`, `w: &dyn Fn(u32, u32)`) enabling mock testing without hardware.

---

## Next Iteration Focus

- Coverage push toward 90% (coral-glowplug/coral-ember/coral-gpu largest gaps)
- PTX emitter completion for SM120/Blackwell
- UVM hardware validation (RTX 5060)
- `coral-gpu` sovereign path evolution
