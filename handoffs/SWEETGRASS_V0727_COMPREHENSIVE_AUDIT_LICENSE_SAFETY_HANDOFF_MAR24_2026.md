<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — Comprehensive Audit: Debt Resolution, License Alignment, Safety Hardening

**Date**: March 24, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,132 tests, 90.24% line coverage, all checks green

**Supersedes**: `SWEETGRASS_V0727_DEEP_DEBT_COORDINATED_SHUTDOWN_ZERO_COPY_HANDOFF_MAR24_2026.md` (archived)

---

## Summary

Full-spectrum audit of sweetGrass codebase against wateringHole standards
(STANDARDS_AND_EXPECTATIONS, PRIMAL_IPC_PROTOCOL, SEMANTIC_METHOD_NAMING,
ECOBIN_ARCHITECTURE, UNIBIN_ARCHITECTURE, SCYBORG_PROVENANCE_TRIO_GUIDANCE)
followed by execution of all actionable findings.

1. **Centralized `DEFAULT_SOURCE_PRIMAL`** — duplicate constant in compression
   and factory crates replaced with single definition in `sweet-grass-core::identity`

2. **Safe timestamp conversions** — 8 `timestamp() as u64` lossy casts evolved
   to `u64::try_from().unwrap_or(0)` in signer/testing.rs and listener/tests.rs

3. **`#![forbid(unsafe_code)]` on fuzz targets** — all 3 fuzz targets
   (fuzz_attribution, fuzz_braid_deserialize, fuzz_query_filter) now forbid unsafe

4. **License alignment** — LICENSE preamble evolved from `AGPL-3.0-or-later` to
   `AGPL-3.0-only` matching all 138 SPDX headers and Cargo.toml declarations

5. **Configurable resilience** — `RetryPolicy::from_env()` with
   `SWEETGRASS_RETRY_MAX`, `SWEETGRASS_RETRY_INITIAL_MS`, `SWEETGRASS_RETRY_MAX_MS`
   env vars; testable `from_env_with()` constructor pattern

6. **CONTEXT.md corrected** — all 27 JSON-RPC method names aligned with actual
   dispatch table (fixed `braid.get_by_hash`, `braid.delete`, `anchoring.anchor`,
   `anchoring.verify`, `attribution.calculate_rewards`, `provenance.export_provo`)

7. **Documentation sweep** — README metrics (1,132 tests, 138 files, 40,328 LOC,
   90.24% coverage, 829 max file), CHANGELOG duplicate [0.7.22] merged,
   showcase script version string updated, .cargo/config.toml documented

---

## Code Changes

| File | Change |
|------|--------|
| `sweet-grass-core/src/lib.rs` | Added `identity::DEFAULT_SOURCE_PRIMAL` constant |
| `sweet-grass-compression/src/engine/mod.rs` | Removed duplicate constant, use centralized |
| `sweet-grass-factory/src/factory/mod.rs` | Removed duplicate constant, use centralized |
| `sweet-grass-integration/src/signer/testing.rs` | Safe timestamp casts (2 sites) |
| `sweet-grass-integration/src/listener/tests.rs` | Safe timestamp casts (6 sites), removed `cast_sign_loss` suppression |
| `sweet-grass-integration/src/resilience.rs` | `RetryPolicy::from_env()` + `from_env_with()` + 4 new tests |
| `fuzz/fuzz_targets/fuzz_attribution.rs` | `#![forbid(unsafe_code)]` |
| `fuzz/fuzz_targets/fuzz_braid_deserialize.rs` | `#![forbid(unsafe_code)]` |
| `fuzz/fuzz_targets/fuzz_query_filter.rs` | `#![forbid(unsafe_code)]` |
| `LICENSE` | Preamble: `AGPL-3.0-or-later` → `AGPL-3.0-only` |
| `CONTEXT.md` | Corrected 27 JSON-RPC method names, updated metrics |
| `README.md` | Updated metrics, license reference |
| `CHANGELOG.md` | Merged duplicate [0.7.22], added [Unreleased] audit section |
| `DEVELOPMENT.md` | Updated test count and coverage |
| `QUICK_COMMANDS.md` | Updated test count |
| `showcase/00_START_HERE.md` | Updated test count |
| `showcase/.../demo-anchor-live.sh` | Version 0.7.0 → 0.7.27, test count |
| `.cargo/config.toml` | Documented user-specific target-dir |

---

## Audited — No Action Needed

These areas passed the audit with no changes required:

- **JSON-RPC 2.0 + tarpc first**: 27 semantic methods, batch + notification support, MCP tools
- **UniBin compliant**: `sweetgrass server|status|capabilities|socket` subcommands
- **ecoBin compliant**: zero C deps in production, cross-compilation ready, `cargo-deny` enforced
- **Primal sovereignty**: zero compile-time coupling to other primals, runtime discovery only
- **Mocks isolated**: all behind `#[cfg(any(test, feature = "test"))]`
- **File sizes**: all under 829 lines (limit 1,000)
- **Semantic naming**: `{domain}.{operation}` per wateringHole v2.1
- **Zero-copy**: `Arc<str>` on all hot-path strings, `Cow<'static, str>` in signatures
- **Store defaults**: architectural constants, not hardcoded values
- **Test URLs**: isolated to test modules
- **`async_trait`**: retained for `dyn` dispatch compatibility at current MSRV

---

## Deferred

| Item | Reason |
|------|--------|
| `async_trait` removal | Blocked on stable `dyn Trait` with async fn (MSRV 1.87) |
| Per-crate coverage push (integration, store-redb, store-sled) | Workspace 90.24% achieved; individual crate push for future session |
| GitHub Actions `actions/cache@v3` → v4, `codecov-action@v3` → v4 | Low priority, no functional impact |
| StorageResultExt abstraction | Needs profiling to justify |
| Tokio feature slimming | Per-crate audit needed |

---

## Cross-Ecosystem Signals

| Pattern | Source | Status in sweetGrass |
|---------|--------|---------------------|
| `RetryPolicy::from_env()` | Configurable resilience | ✅ Adopted |
| `#![forbid(unsafe_code)]` on fuzz targets | Safety hardening | ✅ Adopted |
| `u64::try_from()` safe casts | Modern Rust idiom | ✅ Adopted |
| AGPL-3.0-only (not or-later) | scyBorg license standard | ✅ Aligned |
| Centralized identity constants | DRY principle | ✅ Adopted |
| `.cargo/config.toml` documentation | Developer onboarding | ✅ Documented |

---

## Verification

```
cargo fmt:      PASS (0 diffs)
cargo clippy:   PASS (0 warnings, pedantic + nursery, -D warnings)
cargo doc:      PASS (0 warnings)
cargo test:     1,132 passed, 0 failed
cargo llvm-cov: 90.24% line coverage
unsafe blocks:  0 (#![forbid(unsafe_code)] all crates + fuzz targets)
TODOs/FIXMEs:   0 in .rs source
SPDX headers:   138/138 .rs files
```
