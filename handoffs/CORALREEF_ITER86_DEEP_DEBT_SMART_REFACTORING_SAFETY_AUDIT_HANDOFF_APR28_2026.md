# coralReef Iteration 86 — Deep Debt: Smart File Refactoring + Safety Audit

**Date**: April 28, 2026
**From**: coralReef (Iteration 86)

---

## What Changed

### Smart File Refactoring (>800L → Cohesive Modules)

| File | Before | After | Extracted To |
|------|--------|-------|-------------|
| `sm20/tex.rs` | 854L | 341L | `tex_tests.rs` (517L) |
| `amd-isa-gen/main.rs` | 826L | 112L | `main_tests.rs` (715L) |
| `tests_unix_edge.rs` | 935L | 517L | `tests_unix_dispatch.rs` (443L) |

All production `.rs` files now under 800L. Remaining >800L files are generated code,
dense hardware data tables, test files, or examples — all under the 1000L hard limit.

### Safety Audit

- Added missing `// SAFETY:` comment on `coral_kmod.rs` `alloc_gpu_buffer` zeroed struct
- Removed unused `AsyncReadExt` import from `tests_chaos.rs`
- Verified all ~80+ `unsafe` blocks in `coral-driver` have SAFETY comments
- Verified all 5 other crates enforce `#![forbid(unsafe_code)]`

### Full Codebase Audit

| Category | Status |
|----------|--------|
| Unsafe code | All confined to `coral-driver` with SAFETY comments |
| External deps | No C/C++ in production (transitive `libc` via mio only) |
| Hardcoded paths | All have env var overrides |
| Hardcoded primal names | Only in doc comments and `biomeos` namespace |
| Production mocks | None — all test-isolated |
| TODO/FIXME/HACK | Zero in committed `.rs` |
| Commented-out code | None |
| `.unwrap()` in library code | None (test-only) |

---

## Verification

- 4,701 tests passing, 0 failed
- Zero clippy warnings (`clippy::pedantic` + `clippy::nursery`)
- Zero new dependencies
