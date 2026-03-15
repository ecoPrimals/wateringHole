<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda v0.3.5 — Nursery Lints & Iterator Evolution Handoff

**Date**: March 12, 2026
**Primal**: barraCuda
**Version**: 0.3.5
**Type**: Deep debt evolution sprint 2

---

## Summary

Second deep debt sprint following the comprehensive audit. Focused on clippy
nursery lint promotion, eliminating `if_same_then_else` patterns, evolving
range loops to idiomatic iterators, and removing remaining hardcoded discovery
paths. 200 files changed, net code reduction. All quality gates green.

---

## Changes

### Nursery Lint Promotion (5 lints, 193 files auto-fixed)

- **`redundant_clone`** (warn): Removed unnecessary `.clone()` across workspace.
- **`imprecise_flops`** (warn): Evolved to `ln_1p()`, `to_radians()`, `hypot()`,
  `exp2()` for better numerical precision in scientific compute paths.
- **`unnecessary_struct_initialization`** (warn): Simplified struct construction.
- **`derive_partial_eq_without_eq`** (warn): Added `Eq` where `PartialEq` derived.
- **`suboptimal_flops`** (allow): Analyzed 643 `mul_add` sites. Kept as allow —
  `a*b + c` is the canonical mathematical form in scientific code.

### `if_same_then_else` (7 sites fixed, lint promoted to warn)

| File | Fix |
|------|-----|
| `ops/linalg/qr.rs` | Merged identical below-diagonal and small-value branches |
| `ops/spherical_harmonics_f64_wgsl.rs` | Merged `x > 0` and even-`l` branches |
| `ops/kldiv_loss.rs` (2 sites) | Removed redundant reduction-size branching |
| `optimize/diagnostics.rs` | Merged duplicate `Stagnant` convergence states |
| `shaders/precision/polyfill.rs` | Merged `enables.is_empty()` branches |
| `unified_hardware/cpu_executor.rs` | Removed redundant SSE4.1 detection |

### Iterator Evolution (`needless_range_loop` reduction)

| File | Before | After |
|------|--------|-------|
| `linalg/sparse/csr.rs` | `for i in 0..n { diag[i] = ... }` | `(0..n).map(\|i\| self.get(i,i)).collect()` |
| `device/capabilities/device_info.rs` | `for i in 0..16 { if path.exists() }` | `(0..16).any()` |
| `ops/fft/fft_1d.rs` | Push-loop twiddle gen | `(0..degree).map().unzip()` (f32 + f64) |

### Hardcoding Evolution

- 3 discovery file path constructions derived from `PRIMAL_NAMESPACE`.
- `zeros`/`ones` dispatch duplication eliminated via combined match arm.
- Doc comments updated to `{PRIMAL_NAMESPACE}` placeholder.

### Doc Cleanup

- Fixed stale integration test count (43 -> 42, matching actual filesystem).
- Updated REMAINING_WORK quality gate entry.
- Added sprint 2 achieved section to REMAINING_WORK.md.
- Added sprint 2 entry to WHATS_NEXT.md recently completed.
- Updated STATUS.md grade table and achievements.

---

## Lint Configuration (final state)

14 lints promoted from bulk-allow to warn:

**Pedantic (9)**: `needless_raw_string_hashes`, `redundant_closure_for_method_calls`,
`bool_to_int_with_if`, `cloned_instead_of_copied`, `map_unwrap_or`,
`no_effect_underscore_binding`, `format_push_string`, `explicit_iter_loop`,
`used_underscore_binding`.

**Nursery (4 warn + 1 allow)**: `redundant_clone`, `imprecise_flops`,
`unnecessary_struct_initialization`, `derive_partial_eq_without_eq` (warn);
`suboptimal_flops` (allow with rationale).

**Also promoted**: `if_same_then_else` (was allow, now warn).

**Remaining allow**: `needless_range_loop` (56 sites in multi-array scientific code).

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -- -D warnings` | Pass |
| `cargo doc --no-deps` | Pass (zero warnings) |
| `cargo deny check` | Pass |
| `cargo nextest --no-fail-fast` | 3,688 pass / 0 fail / 15 skip |

---

## Cross-Primal Impact

None. All changes are internal. No API changes.
