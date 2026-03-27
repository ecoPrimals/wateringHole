# biomeOS v2.64 — Flaky Test Hardening + Coverage Push + serde_yml Migration

**Date**: March 22, 2026
**From**: biomeOS deep evolution session
**Version**: 2.64
**Previous**: v2.63 (Deep Audit + Idiomatic Rust Evolution)

---

## Session Summary

Continuation of the v2.63 deep audit session. Focused on test reliability, coverage threshold, deprecated dependency elimination, and documentation alignment.

---

## Changes Made

### 1. Flaky Test Fixes (3 tests)

| Test | Root Cause | Fix |
|------|-----------|-----|
| `nucleation::test_xdg_runtime_strategy` | Env var mutation without serialization | `#[serial_test::serial]` + `TestEnvGuard` RAII |
| `nucleation::test_xdg_runtime_fallback_to_tmp` | Same | Same |
| `capability_registry_tests2::test_registry_socket_heartbeat_unknown_primal` | ReadySender dropped under llvm-cov instrumentation overhead | `tokio::time::timeout` wrapper on `ready_rx.wait()` |
| `capability_handlers::test_primal_start_capability_family_id_from_params` | CWD race with parallel tests under llvm-cov | `#[serial_test::serial]` |

### 2. Method Name Test Alignment (6 tests)

Previous session renamed RPC dispatch methods to `domain.verb` format but missed 6 test assertions in `device_management_server/mod.rs`:

- `get_primals_extended` → `primal.list`
- `get_niche_templates` → `niche.list_templates`
- `validate_niche` → `niche.validate` (2 tests)
- `deploy_niche` → `niche.deploy` (2 tests)

### 3. Songbird Error Message Fix

Restored meaningful default: `unwrap_or_default()` → `unwrap_or("Unknown error")` with cleaner `if let Some(err)` pattern. Empty error messages are not user-friendly.

### 4. Coverage Push (19 new tests)

| File | Tests Added | Coverage Impact |
|------|-------------|----------------|
| `nucleus_tests4.rs` | 14 | `detect_ecosystem`, `generate_jwt_secret`, `base64_encode`, `format_nucleus_summary`, `NucleusMode`, `wait_for_socket` |
| `cli.rs` | 4 | `ContextTip::to_colored_string` all 3 variants |
| `realtime_tests.rs` | 1 | WebSocket success path with local echo server |

### 5. serde_yaml → serde_yml Migration

Eliminated deprecated `serde_yaml = "0.9"` across workspace:
- Workspace `[dependencies]`: `serde_yaml = { package = "serde_yml", version = "0.0.12" }`
- `biomeos-cli/Cargo.toml`: same
- Now consistent with `biomeos-types`, `biomeos-boot`, `biomeos-manifest`, `biomeos-deploy` (already migrated)

### 6. Clippy Fix

`implicit_clone` lint in `songbird.rs`: `pattern.to_string()` → `(*pattern).clone()`

---

## Quality Gates (All Passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-features -D warnings` | PASS (0 warnings) |
| `cargo test --workspace --all-features` | PASS (~5,060+ tests, 0 failures) |
| `cargo doc --workspace --no-deps` | PASS |
| `cargo deny check` | PASS (advisories, bans, licenses, sources OK) |
| `cargo llvm-cov` | 90.26% region / 91.14% function / 89.99% line |

---

## Documentation Updated

- `README.md`: v2.64, updated test count and function coverage
- `CURRENT_STATUS.md`: v2.64, session summary in header, function coverage updated
- `CHANGELOG.md`: Full v2.64 entry
- `DOCUMENTATION.md`: Date updated, archive path reconciled
- `specs/README.md`: Date updated, archive path reconciled
- `wateringHole/README.md`: biomeOS row updated to v2.64 with current metrics

---

## Known Issues (Pre-existing, Not Introduced)

1. **`nucleation::test_xdg_runtime_strategy`** now fixed with `#[serial]`
2. **Pre-existing `#[ignore]` tests** (~83): CWD-sensitive tests that need `--test-threads=1`
3. **`biomeos-types` doc warning**: broken intra-doc link for `helpers::capabilities_for_primal` (pre-existing)

---

## Ecosystem Absorption Opportunities

None identified this session. All changes were internal hardening.

---

## Next Session Priorities

1. **Line coverage to 90.00%+**: Currently 89.99% — 11 lines from threshold. Target `nucleus.rs` `run()` orchestration path or `provider.rs` registry success paths.
2. **CI placeholder**: `ci.yml` Job 10 "version consistency" is a placeholder — wire up actual checks.
3. **Shell script evolution**: Consider `cargo xtask` for `scripts/build_primals_for_testing.sh` and `scripts/test_provenance_trio_e2e.sh`.
4. **DEPRECATED markers**: Review 6 production files with `DEPRECATED` comments (state.rs, deploy.rs, health.rs, beardog_client.rs, discovery.rs, primal_impls.rs) — evolve or remove.
