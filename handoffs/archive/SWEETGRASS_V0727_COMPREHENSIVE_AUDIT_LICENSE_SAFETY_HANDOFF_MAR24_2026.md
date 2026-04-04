<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — Comprehensive Audit: Debt Resolution, CLI Extraction, Safety Hardening

**Date**: March 24, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,147 tests, 90.54% region coverage, all checks green

**Supersedes**: `SWEETGRASS_V0727_DEEP_DEBT_COORDINATED_SHUTDOWN_ZERO_COPY_HANDOFF_MAR24_2026.md` (archived)

---

## Summary

Two-phase audit and deep execution session against wateringHole standards
(STANDARDS_AND_EXPECTATIONS, PRIMAL_IPC_PROTOCOL, SEMANTIC_METHOD_NAMING,
ECOBIN_ARCHITECTURE, UNIBIN_ARCHITECTURE, SCYBORG_PROVENANCE_TRIO_GUIDANCE).

**Phase 1 — Audit + Constants + Safety:**
Centralized identity constants, safe timestamp casts, fuzz target hardening,
LICENSE alignment to AGPL-3.0-only, configurable resilience, CONTEXT.md correction.

**Phase 2 — Execution + CLI Extraction + Coverage:**
Extracted testable CLI module from binary entry point, expanded anchor integration
tests, aligned fuzz edition to 2024, refactored `run_server` for clippy compliance,
added persistent AI guidance rules.

---

## Code Changes

| File | Change |
|------|--------|
| `sweet-grass-service/src/cli.rs` | **NEW**: Extracted CLI logic (capabilities report, address parsing, health check) + 7 tests |
| `sweet-grass-service/src/lib.rs` | Added `pub mod cli` + re-exports |
| `sweet-grass-service/src/bin/service.rs` | Refactored to delegate to `cli` module; `serve_all` helper extracted from `run_server` |
| `sweet-grass-integration/src/anchor/tests.rs` | 7 new tests: discovery, reconnect, multi-ops, serialization roundtrips |
| `sweet-grass-core/src/lib.rs` | Added `identity::DEFAULT_SOURCE_PRIMAL` constant |
| `sweet-grass-compression/src/engine/mod.rs` | Removed duplicate constant, use centralized |
| `sweet-grass-factory/src/factory/mod.rs` | Removed duplicate constant, use centralized |
| `sweet-grass-integration/src/signer/testing.rs` | Safe timestamp casts (2 sites) |
| `sweet-grass-integration/src/listener/tests.rs` | Safe timestamp casts (6 sites), removed `cast_sign_loss` suppression |
| `sweet-grass-integration/src/resilience.rs` | `RetryPolicy::from_env()` + `from_env_with()` + 4 new tests |
| `fuzz/Cargo.toml` | `edition = "2021"` → `edition = "2024"` |
| `fuzz/fuzz_targets/*.rs` | `#![forbid(unsafe_code)]` on all 3 targets |
| `LICENSE` | Preamble: `AGPL-3.0-or-later` → `AGPL-3.0-only` |
| `docker-compose.yml` | Removed deprecated `version: '3.8'` key |
| `.cursor/rules/ecosystem-standards.mdc` | **NEW**: Persistent AI guidance for ecosystem standards |
| `.cursor/rules/rust-patterns.mdc` | **NEW**: Persistent AI guidance for Rust patterns |
| `CONTEXT.md` | Corrected 27 JSON-RPC method names, updated metrics |
| `README.md` | Updated metrics: 1,147 tests, 139 files, 40,851 LOC, 90.54% coverage |
| `CHANGELOG.md` | Updated [Unreleased] with both phases |
| `ROADMAP.md` | Added latest items, updated coverage numbers |
| `DEVELOPMENT.md` | Updated metrics, last-updated date |
| `QUICK_COMMANDS.md` | Updated test count |

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
- **`async_trait`**: retained for `dyn` dispatch compatibility at current MSRV

---

## Deferred

| Item | Reason |
|------|--------|
| `async_trait` removal | Blocked on stable `dyn Trait` with async fn (MSRV 1.87) |
| Zero-copy Phase 3 remaining (`Cow<str>` in factory APIs, `Arc<Braid>` in queries) | Low priority — hot-path clones already eliminated |
| tarpc mock server for `tarpc_client.rs` (8% coverage) | Complex mock infrastructure needed |
| store-redb/store-sled per-crate coverage push (70-75% → 90%) | Workspace 90.54% achieved; individual crate push for future session |
| GitHub Actions cache/codecov version bumps | Low priority, no functional impact |

---

## Cross-Ecosystem Signals

| Pattern | Source | Status in sweetGrass |
|---------|--------|---------------------|
| `RetryPolicy::from_env()` | Configurable resilience | Adopted |
| `#![forbid(unsafe_code)]` on fuzz targets | Safety hardening | Adopted |
| `u64::try_from()` safe casts | Modern Rust idiom | Adopted |
| AGPL-3.0-only (not or-later) | scyBorg license standard | Aligned |
| Centralized identity constants | DRY principle | Adopted |
| CLI extraction to library module | Testability pattern | Adopted |
| `.cursor/rules/` AI guidance | Development velocity | Adopted |
| `edition = "2024"` on fuzz targets | Workspace consistency | Aligned |

---

## Verification

```
cargo fmt:      PASS (0 diffs)
cargo clippy:   PASS (0 warnings, pedantic + nursery, -D warnings)
cargo doc:      PASS (0 warnings)
cargo test:     1,147 passed, 0 failed
cargo llvm-cov: 90.54% region coverage
unsafe blocks:  0 (#![forbid(unsafe_code)] all crates + fuzz targets)
TODOs/FIXMEs:   0 in .rs source
SPDX headers:   139/139 .rs files
Max file:       829 lines (limit 1,000)
```
