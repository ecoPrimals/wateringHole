# biomeOS v2.65 — Deep Debt Execution + Zero-Copy + Hardcode Evolution

**Date**: March 22, 2026
**From**: biomeOS deep debt execution session
**Version**: 2.65
**Previous**: v2.64 (Flaky Test Hardening + Coverage Push + serde_yml Migration)

---

## Session Summary

Continuation of v2.63/v2.64 deep audit. Executed on all audit recommendations: refactored untestable binaries into library modules, evolved hardcoded primal names to canonical constants, applied zero-copy patterns to hot paths, fixed all CWD/env race conditions in tests, and raised CI coverage threshold to 90%.

---

## Changes Made

### 1. Architectural Refactoring

| Component | Before | After |
|-----------|--------|-------|
| `tower.rs` | 895 lines, 0% coverage, monolithic binary | Thin CLI wrapper + `tower_orchestration.rs` library (20+ tests) |
| `verify-lineage.rs` | Hardcoded USB paths (`/media/$USER/spore*`) | `discover_spore_mounts()` — env `BIOMEOS_SPORE_PATHS` or dynamic scan |
| `nucleus.rs` JWT generation | Hand-rolled `base64_encode` + `/dev/urandom` | `base64` crate + `rand::thread_rng().fill_bytes()` (CSPRNG) |

### 2. Zero-Copy Evolution

- `ExecutionContext.env`: `HashMap<String, String>` → `Arc<HashMap<String, String>>` — eliminates deep clone per `tokio::spawn` in graph executor
- Full IPC/forwarding audit: `JsonRpcRequest` params clones are inherent to `serde_json::Value` ownership; raw-byte forwarding deferred as architectural change

### 3. Hardcoded Name Evolution (6 files)

All inline `"beardog"`, `"songbird"` string literals in production code replaced with `primal_names::BEARDOG`, `primal_names::SONGBIRD` constants from `biomeos-types`. `manifest.rs` `from_nucleus()` evolved from hardcoded two-binary match to dynamic discovery of all binaries.

### 4. Flaky Test Fixes (6 tests fixed, 1 restored)

- 4 tests: removed `set_current_dir` (process-global) — tests already set `BIOMEOS_PLASMID_BIN_DIR` in `ExecutionContext`
- 2 tests: added `#[serial_test::serial]` for `HOME` env var mutation
- 1 test un-ignored: `test_primal_start_capability_mode_default` (CWD race eliminated)

### 5. CI Threshold

Coverage enforcement raised from 85% to 90% in `ci.yml`.

---

## Quality Gates (All Passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-features -D warnings` | PASS (0 warnings) |
| `cargo test --workspace --all-features` | PASS (7,124 tests, 0 failures) |
| `cargo doc --workspace --no-deps` | PASS |
| Coverage | 90.35% region / 91.20% function / 90.41% line |

---

## Ecosystem Absorption Opportunities

None this session. All changes internal.

---

## Next Session Priorities

1. **DEPRECATED markers**: 6 production files with `DEPRECATED` comments — evolve or remove (state.rs HTTP bridge, deploy.rs graph path, health.rs graph check, beardog_client.rs HTTP arms, discovery.rs, primal_impls.rs legacy aliases)
2. **CI placeholder**: `ci.yml` Job 10 "version consistency" is a placeholder
3. **Shell script evolution**: Consider `cargo xtask` for remaining shell scripts
4. **Profiling-guided zero-copy**: Identify actual hot allocation sites via `perf`/`dhat` before further `Arc`/`Bytes` wrapping
