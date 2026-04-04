# barraCuda v0.3.11 — Sprint 29: Deep Debt Cleanup & Shader-First Evolution

**Date**: 2026-04-04
**Primal**: barraCuda
**Version**: 0.3.11
**Session**: Sprint 29

---

## Summary

Comprehensive deep debt cleanup and evolution session targeting hardcoding, large file
refactoring, dependency hygiene, error handling, documentation accuracy, primal self-knowledge,
and lint suppression reduction. All changes verified against full quality gate suite.

---

## Changes

### Hardcoding → Capability-Based Constants

- **Workgroup size unification**: Magic `256` replaced with `WORKGROUP_SIZE_1D` constant
  from `device::capabilities` across 15+ files spanning shader dispatch, CPU executor,
  stats (jackknife), health (biosignal), numerical (gradient), ops (perlin_noise,
  population_pk, hill_dose_response, michaelis_menten_batch, scfa_batch, beat_classify,
  rop_force_accum). Single source of truth for workgroup sizing.
- **Namespace constants**: Hardcoded `"biomeos"` and `"ecoPrimals"` strings consolidated
  to shared named constants. `ECOSYSTEM_SOCKET_DIR` made `pub` in `barracuda-core` transport.
  `DEFAULT_ECOPRIMALS_DISCOVERY_DIR` created in `coral_compiler` and wired through
  `sovereign_device.rs`.

### Dependency Cleanup

- **`num-traits` removed**: Was declared in workspace `Cargo.toml` but never consumed by
  any crate. Removed entirely.
- **`tarpc` audit**: `rand` 0.8 and OpenTelemetry are mandatory upstream dependencies of
  tarpc 0.37 — cannot be disabled via features. Documented as known issue; `rand` 0.8/0.9
  duplication tracked for upstream resolution.

### Smart File Refactoring

- **`executor.rs`** (naga-exec): 1,097 → 932 lines. Vector operation helpers
  (`access_index_val`, `splat_value`, `swizzle_value`, component extractors) extracted
  to focused `vector_ops.rs` module (174 lines).
- **`eval.rs`** (naga-exec): 629 → 527 lines. Monolithic 264-line `eval_math` function
  decomposed into `math_f32`, `math_f64`, `math_u32`, `math_i32` dispatch functions +
  shared `require_arg` helper. `#[expect(clippy::too_many_lines)]` suppression eliminated.
- **`perlin_noise.rs`**: 7 identical `#[expect(cast_possible_truncation, cast_sign_loss)]`
  blocks consolidated into 2 helper functions (`perm_index`, `perm_index_f32`).

### Error Handling Evolution

- **`wgpu_backend.rs`**: `dispatch_compute_batch` `expect("len == 1 checked above")`
  evolved to safe `if let [_]` pattern-match + `Result` propagation. Production panic
  risk eliminated.
- **`guard.rs` / `pool.rs`**: Audited — their `expect()` calls in `Deref` impls are
  ownership invariants (encoder/buffer is `Some` from construction until `finish()`/
  `into_buffer()` consumes `self`). Documented as correct for typestate-like patterns.

### Documentation Accuracy

- **`nautilus/readout.rs`**: Misleading "no-op when GPU disabled" doc corrected to
  describe actual CPU ridge regression training path.
- **coral_compiler module**: All `coralReef` documentation evolved to describe
  capability-based discovery (`shader.compile`) rather than naming specific primals.
  `coralReef` mentioned only as reference implementation where history matters.

### Primal Self-Knowledge

- Production discovery logic verified: already uses capability-based lookups
  (`shader.compile` capability scan, not primal name matching). No code change needed.
- Documentation evolved from primal-name-centric to capability-centric language.

---

## Quality Gates

| Gate | Status | Detail |
|------|--------|--------|
| `cargo fmt` | Pass | All crates clean |
| `cargo clippy` (default) | Pass | Zero warnings, pedantic+nursery |
| `cargo clippy` (cpu-shader) | Pass | Zero warnings |
| `cargo test` (barracuda) | Pass | 3,815 lib tests, 0 failures |
| `cargo test` (naga-exec) | Pass | 16 tests, 0 failures |
| `cargo doc -D warnings` | Pass | naga-exec + barracuda |

---

## Files Changed

### New Files
- `crates/barracuda-naga-exec/src/vector_ops.rs` — Vector component access, splat, swizzle helpers (174 lines)

### Modified Files (key)
- `crates/barracuda-naga-exec/src/executor.rs` — Vector ops extracted (1,097→932 lines)
- `crates/barracuda-naga-exec/src/eval.rs` — `eval_math` decomposed (629→527 lines)
- `crates/barracuda-naga-exec/src/lib.rs` — `vector_ops` module registered
- `crates/barracuda/src/unified_hardware/shader_dispatch.rs` — `WORKGROUP_SIZE_1D` import
- `crates/barracuda/src/stats/jackknife.rs` — `WORKGROUP_SIZE_1D`
- `crates/barracuda/src/health/biosignal.rs` — `WORKGROUP_SIZE_1D`
- `crates/barracuda/src/numerical/gradient.rs` — `WORKGROUP_SIZE_1D`
- `crates/barracuda/src/cpu_executor/executor.rs` — `WORKGROUP_SIZE_1D`
- `crates/barracuda/src/ops/procedural/perlin_noise.rs` — `perm_index` helpers
- `crates/barracuda/src/ops/health/*.rs` — `WORKGROUP_SIZE_1D` (5 files)
- `crates/barracuda/src/ops/lattice/rop_force_accum.rs` — `WORKGROUP_SIZE_1D`
- `crates/barracuda/src/device/wgpu_backend.rs` — Safe `Result` pattern
- `crates/barracuda/src/nautilus/readout.rs` — Accurate doc
- `crates/barracuda/src/device/coral_compiler/*.rs` — Capability-based docs
- `crates/barracuda/src/device/sovereign_device.rs` — `DEFAULT_ECOPRIMALS_DISCOVERY_DIR`
- `crates/barracuda-core/src/ipc/transport.rs` — `pub` ECOSYSTEM_SOCKET_DIR
- `crates/barracuda-core/src/bin/barracuda.rs` — Shared constant
- `Cargo.toml` — `num-traits` removed

---

## Cross-Primal Impact

**None.** All changes are internal to barraCuda. No IPC protocol changes, no API changes,
no behavioral changes visible to consumers.

---

## Remaining Known Debt

- `tarpc` pulls duplicate `rand` 0.8 alongside direct `rand` 0.9 — upstream-blocked
- `executor.rs` `eval_expr` still ~196 lines — exhaustive naga `Expression` dispatch,
  splitting would obscure interpretation flow
- `guard.rs` / `pool.rs` `expect()` in `Deref` — correct by construction, not evolve-able
  without typestate complexity
