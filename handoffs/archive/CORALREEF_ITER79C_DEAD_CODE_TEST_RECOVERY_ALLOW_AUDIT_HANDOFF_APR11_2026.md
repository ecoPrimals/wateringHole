# coralReef Iter 79c — Dead Code Cleanup, Test Recovery, #[allow] Audit

**Date**: April 11, 2026
**Primal**: coralReef
**Iteration**: 79c (follows 79b: CR-04/CR-05/libc canary)
**Matrix**: ECOSYSTEM_COMPLIANCE_MATRIX v2.7.0

---

## Executive Summary

Comprehensive deep debt audit across the entire coralReef codebase (804 `.rs` files,
12 workspace crates). Recovered 5 tests from orphaned dead code, audited all `#[allow]`
attributes in production code, and verified the codebase against every debt category:
mocks, hardcoding, unsafe code, Result types, file sizes, dependencies. All quality gates
green. 4,467 tests passing (+5 recovered).

---

## Part 1: What Changed

### Dead Code Recovery

Orphaned `uvm_compute_tests.rs` (275 lines) was discovered outside the module tree —
never compiled but containing 5 unique tests not duplicated in the active `uvm_compute/tests.rs`:

| Test | Coverage Added |
|------|---------------|
| `userd_gp_offsets_match_volta_ramuserd_layout` | Validates USERD GP_PUT/GP_GET offset constants (0x8C/0x88) |
| `gpu_gen_from_sm_boundary_values` | SM boundary testing (0, 74→76, 79→81, 99→101, 119→121, MAX) |
| `gpfifo_entry_masks_va_to_four_byte_alignment` | Misaligned VA masking to 4-byte boundary |
| `gpfifo_entry_max_length_truncates_to_field_width` | u32::MAX overflow truncation (22-bit field) |
| `gpfifo_entry_length_round_trip_all_bits` | Full round-trip encoding with max-width values |

Tests merged into active module, helper constants (`GPFIFO_VA_MASK`, `GPFIFO_LENGTH_SHIFT`,
`gpfifo_length_field_mask()`) added, orphan deleted.

### `#[allow]` Audit (All Production Code)

Audited every `#[allow(...)]` attribute across all 804 `.rs` files in 12 workspace crates.

| Category | Count | Action |
|----------|------:|--------|
| Conditional — cannot be `#[expect]` | 10 | Documented reasons: dead_code on enum variants (BTSP), unused_imports across lib/bin targets, wildcard_imports/enum_glob_use across lib/test targets |
| Missing `reason=` | 1 | Added: `gsp/knowledge/mod.rs` pub re-export `unused_imports` |
| Already correct `#[expect]` | ~30 | No change needed |

Key insight: Rust's `#[expect]` lint fails when the suppressed lint does NOT fire. Many
`#[allow]` attrs in coralReef suppress lints that fire conditionally (e.g., `dead_code` on
enum variants referenced only via `Debug`, `unused_imports` on items used from tests but not
lib). Converting these to `#[expect]` would break `cargo clippy --all-targets`.

### Comprehensive Audit Verification

| Category | Finding |
|----------|---------|
| Mocks in production | Zero — all `Mock*` types are `#[cfg(test)]`-gated |
| Hardcoded primal names | Zero — no other primal names in production code |
| Hardcoded ports | Zero — all default to `:0` or env-configurable |
| `Result<_, String>` in libraries | Zero — only in test helpers |
| `todo!()` / `unimplemented!()` | Zero |
| Unsafe outside coral-driver | Zero — `#![forbid(unsafe_code)]` on all other crate roots |
| Unsafe without SAFETY comment | Zero |
| Files > 1000 LOC | Zero — max production file 825 LOC |
| Dependencies with C FFI | Only optional `cudarc` (feature-gated); `libc` transitive-only |

---

## Part 2: Quality Gate

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS='-D warnings' cargo doc --all-features --no-deps` | PASS |
| `cargo test --workspace --all-features` | **4,467 passed** (+5), 0 failed, 153 ignored |
| `cargo deny check` | PASS (ecoBin v3 bans active) |
| All files <1000 lines | PASS |
| Zero TODO/FIXME/HACK in production | PASS |
| SPDX headers | PASS |

---

## Part 3: Compliance Matrix Update

| Tier | Status | Notes |
|------|--------|-------|
| T1 Build | A+ | All quality gates green; +5 tests recovered |
| T6 Responsibility | A+ | Zero orphaned/dead code; comprehensive audit verified |
| T8 Presentation | A+ | Root docs synchronized to Iter 79c; all test counts current |
| **Rollup** | **A+** | No tier regression |

---

## Part 4: Remaining Work

- **musl-static verification (T9)**: Cross-compile both x86_64 and aarch64
- **Coverage push**: Target 90% via `cargo llvm-cov`; hardware tests need local GPU
- **BTSP Phase 2 end-to-end**: Needs BearDog `btsp.session.create` service
- **Multi-shader batch API**: Documented as future; springs compose sequentially for now

---

## Files Changed (4 files, +70 / -278)

### Removed
- `crates/coral-driver/src/nv/uvm_compute_tests.rs` — orphaned test file (275 lines, never compiled)

### Modified
- `crates/coral-driver/src/nv/uvm_compute/tests.rs` — 5 tests merged from orphan + helper constants
- `crates/coral-driver/src/gsp/knowledge/mod.rs` — added `reason=` to `#[allow(unused_imports)]`
- `crates/coral-driver/src/vfio/channel/diagnostic/interpreter/probe/channel.rs` — documented `#[allow(missing_docs)]` conditional behavior
