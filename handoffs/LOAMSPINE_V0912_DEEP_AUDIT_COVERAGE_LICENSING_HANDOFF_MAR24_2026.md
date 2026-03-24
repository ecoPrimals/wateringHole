<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# LoamSpine v0.9.12 — Deep Audit Execution, Coverage Push & scyBorg Licensing

**Date**: March 24, 2026  
**From**: LoamSpine  
**To**: All Springs, All Primals, biomeOS  
**Status**: Complete, ready for push

---

## Summary

LoamSpine v0.9.12 executes on all findings from a comprehensive deep audit,
evolving unsafe policy, pushing coverage past the 90% line threshold, completing
scyBorg triple license compliance, and smart-refactoring the main specification.

1. **`#![forbid(unsafe_code)]` workspace-wide** — Evolved from `deny` to `forbid`
   in both workspace-level `Cargo.toml` lints and the `loam-spine-core` crate
   attribute. Zero unsafe code in the entire codebase including tests.

2. **Coverage 89.59% → 90.02% line** — 29 new tests targeting uncovered error
   paths and edge cases across all storage backends (redb, sled, sqlite), core
   types, trio types, waypoint, streaming, and transport modules.

3. **scyBorg triple license complete** — Added `LICENSE-ORC` (game mechanics)
   and `LICENSE-CC-BY-SA` (creative/documentation) alongside the existing
   `LICENSE` (AGPL-3.0-or-later). All three layers of the scyBorg provenance
   trio license are now explicitly declared.

4. **Spec smart-refactor** — `LOAMSPINE_SPECIFICATION.md` reduced from 1,521 to
   1,089 lines by deduplicating the data model section (430 lines of struct
   definitions replaced with summary + cross-reference to `DATA_MODEL.md`) and
   Appendix A (certificate lifecycle replaced with cross-reference to
   `CERTIFICATE_LAYER.md`).

5. **Clippy all-targets clean** — Fixed 8 errors in `sqlite/tests.rs`: 2 unused
   variables renamed with underscore prefix, 6 redundant closures replaced with
   `PoisonError::into_inner` method reference.

---

## Code Changes

| File | Change |
|------|--------|
| `Cargo.toml` | `unsafe_code = "deny"` → `unsafe_code = "forbid"` in workspace lints |
| `crates/loam-spine-core/src/lib.rs` | `#![deny(unsafe_code)]` → `#![forbid(unsafe_code)]` |
| `crates/loam-spine-core/src/storage/sqlite/tests.rs` | 8 clippy fixes + 7 new tests (temporary, flush, nonexistent) |
| `crates/loam-spine-core/src/storage/redb_tests_coverage.rs` | 2 new tests (corrupt entry, short index key) |
| `crates/loam-spine-core/src/storage/sled_tests.rs` | 4 new tests (corrupt bincode, cross-spine iteration) |
| `crates/loam-spine-core/src/types.rs` | 4 new tests (Did::from, Signature::default, Timestamp::Display, ByteBuffer) |
| `crates/loam-spine-core/src/trio_types.rs` | 3 new tests (default weight, as_str accessors) |
| `crates/loam-spine-core/src/waypoint.rs` | 3 new tests (RelendingChain, DepartureReason, SliceOperationType) |
| `crates/loam-spine-core/src/streaming.rs` | 1 new test (empty line skipping) |
| `crates/loam-spine-core/src/transport/mod.rs` | 1 new test (from_bytes zero-copy) |
| `crates/loam-spine-core/src/transport/mock.rs` | 1 new test (SuccessTransport::new) |
| `LICENSE-ORC` | New: ORC license for game mechanics |
| `LICENSE-CC-BY-SA` | New: CC-BY-SA-4.0 for creative/documentation |
| `specs/LOAMSPINE_SPECIFICATION.md` | Smart-refactored 1,521 → 1,089 lines |

---

## Metrics

| Metric | v0.9.11 | v0.9.12 |
|--------|---------|---------|
| Tests | 1,283 | **1,312** (+29) |
| Line coverage | 89.59% | **90.02%** |
| Region coverage | 91.54% | **91.99%** |
| Function coverage | 85.94% | **86.30%** |
| Unsafe code | 0 (`deny`) | 0 (`**forbid**`) |
| Max file | 878 | 954 |
| Source files | 124 | 124 |
| License files | 1 (AGPL) | **3** (AGPL + ORC + CC-BY-SA) |
| Clippy | 0 | 0 |
| Doc warnings | 0 | 0 |

---

## What Other Primals Should Know

- **`#![forbid(unsafe_code)]`** is now enforced at workspace level. Any
  dependency or future change attempting unsafe code will fail to compile.
  This is the strongest possible Rust safety guarantee.

- **scyBorg triple license** is now fully materialized with three license
  files. Other primals following the scyBorg model should ensure they have
  all three files: `LICENSE` (AGPL-3.0), `LICENSE-ORC`, `LICENSE-CC-BY-SA`.

- **Coverage methodology**: Used `cargo llvm-cov --show-missing-lines` to
  identify exact uncovered branches, then wrote targeted tests. This is more
  effective than bulk test generation.

---

## Patterns Available for Absorption

| Pattern | Where | What |
|---------|-------|------|
| `forbid(unsafe_code)` workspace lint | `Cargo.toml` | Strongest safety guarantee at workspace level |
| Targeted coverage via `--show-missing-lines` | Test files | Efficient coverage improvement methodology |
| Spec deduplication via cross-reference | `specs/LOAMSPINE_SPECIFICATION.md` | Keep specs DRY by referencing domain-specific docs |
| `PoisonError::into_inner` method reference | `sqlite/tests.rs` | Clippy-clean mutex poison handling |

---

## Verification

All checks pass:
- `cargo fmt --check` — clean
- `cargo clippy --all-targets --all-features -- -D warnings` — 0 warnings
- `RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps` — 0 warnings
- `cargo test --all-features` — 1,312 tests passing
- `cargo llvm-cov` — 90.02% line / 91.99% region / 86.30% function
