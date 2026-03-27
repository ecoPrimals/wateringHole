<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — Pedantic Clippy, Constants, UniBin Signals, Test Expansion

**Date**: March 14, 2026 (session 5)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Code quality hardening + constants centralization + signal handling + test expansion

---

## Summary

Full pedantic clippy + nursery pass (0 warnings). Centralized all magic
numbers to `constants.rs`. Smart-refactored oversized files. Implemented
UniBin-compliant exit codes and signal handling. Expanded test coverage
with E2E, chaos, and service tests. Hardened ecoBin `deny.toml` with
explicit C-dependency bans. Cleaned stale doc references.

1. **1092 tests passing** (was 1075) — +17 new tests across E2E, chaos,
   and service modules.

2. **90.83% line coverage** (llvm-cov) — slight shift from file
   refactoring; 92.31% region coverage.

3. **0 clippy warnings** (pedantic + nursery) — 45+ errors resolved:
   `significant_drop_tightening`, `doc_markdown`, `must_use_candidate`,
   `missing_errors_doc`.

4. **7 constants centralized** — `SLED_CACHE_SIZE_BYTES`,
   `SLED_FLUSH_INTERVAL_MS`, `DISCOVERY_QUERY_TIMEOUT`,
   `DISCOVERY_RESPONSE_BUFFER_SIZE`, `PROVENANCE_CONNECTION_TIMEOUT`,
   `PROVENANCE_RESPONSE_TIMEOUT`, `PROVENANCE_DEFAULT_MAX_RESULTS`.

5. **UniBin exit codes + signal handling** — `exit_codes` module (0/1/2/3/130),
   `ServiceError::exit_code()` mapping, `shutdown_signal()` for
   SIGTERM/SIGINT (Unix) and Ctrl+C (other), graceful server shutdown.

6. **Smart file refactoring** — `store_sled.rs` 949→552 lines (tests
   extracted), `store_redb_tests_advanced.rs` 994→846 lines (query tests
   extracted). All files well under 1000-line limit.

7. **ecoBin compliance hardened** — `deny.toml` now explicitly bans
   `openssl-sys`, `native-tls`, `aws-lc-sys`, `zstd-sys`, `lz4-sys`,
   `libsqlite3-sys`, `cryptoki-sys`. `ring` tolerated only via opt-in
   `http-clients` feature.

---

## Changes

### Clippy Pedantic + Nursery (45+ fixes)

| Category | Count | Examples |
|----------|-------|---------|
| `significant_drop_tightening` | 8 | Inlined `RwLock` acquisitions in test harness, chaos tests, rate limiter |
| `doc_markdown` | 20+ | Wrapped identifiers in backticks across all crates |
| `missing_errors_doc` | 12 | Added `# Errors` sections to all public Result-returning fns in RPC client |
| `must_use_candidate` | 2 | `JsonRpcServer::new()`, `RhizoCryptRpcServer::new()` |
| Other | 3 | Collapsed nested `if let`, removed unused imports, replaced `expect()` |

### Constants Centralized

| Constant | Value | Replaces |
|----------|-------|----------|
| `SLED_CACHE_SIZE_BYTES` | `64 * 1024 * 1024` | Inline `64 * 1024 * 1024` in store_sled |
| `SLED_FLUSH_INTERVAL_MS` | `1000` | Inline `1000` in store_sled |
| `DISCOVERY_QUERY_TIMEOUT` | `Duration::from_secs(5)` | Inline in registry |
| `DISCOVERY_RESPONSE_BUFFER_SIZE` | `32` | Inline in registry |
| `PROVENANCE_CONNECTION_TIMEOUT` | `Duration::from_secs(5)` | Inline in provenance client |
| `PROVENANCE_RESPONSE_TIMEOUT` | `Duration::from_secs(10)` | Inline in provenance client |
| `PROVENANCE_DEFAULT_MAX_RESULTS` | `1000` | Inline in provenance types |

### Smart File Refactoring

| File | Before | After | Extracted To |
|------|--------|-------|-------------|
| `store_sled.rs` | 949 | 552 | `store_sled_tests.rs` |
| `store_redb_tests_advanced.rs` | 994 | 846 | `store_redb_tests_query.rs` |

### UniBin Signal Handling

- `exit_codes` module: `SUCCESS=0`, `GENERAL_ERROR=1`, `CONFIG_ERROR=2`, `NETWORK_ERROR=3`, `INTERRUPTED=130`
- `ServiceError::exit_code()`: Config/AddrParse→2, Rpc/Discovery→3, other→1
- `shutdown_signal()`: `tokio::signal` for SIGTERM+SIGINT (Unix) / Ctrl+C (other)
- `run_server()`: `tokio::select!` with `tokio::pin!` for graceful shutdown
- `main()`: Exits with mapped exit code on error

### ecoBin deny.toml

Added explicit `deny` entries for 7 C-backed crates. `ring` skip rule
documented as opt-in only via `http-clients` feature, pending
`rustls-rustcrypto` stabilization.

### Test Expansion (+17)

| Test File | Count | Tests |
|-----------|-------|-------|
| `e2e/merkle_operations.rs` | 4 | Root determinism, proof gen/verify, root changes on append, branching DAGs |
| `e2e/slice_workflows.rs` | 5 | Checkout copy/loan, resolution, isolation, mode validation |
| `chaos/resource_exhaustion.rs` | 4 | Max sessions boundary, large payloads, rapid create/destroy, many vertices |
| `service_integration.rs` | 3 | Exit code constants, error mapping, signal safety |
| `binary_integration.rs` | 1 | Invalid address exit code |

### Documentation Cleanup

- Removed broken reference to `docs/VERIFICATION_CHECKLIST.md` from `ENV_VARS.md` and specs
- Fixed broken reference to `00_SHOWCASE_INDEX.md` → `00_START_HERE.md` in showcase
- Fixed stale date (2025→2026) in `docs/audit-hardcoded-primal-refs.md`
- `CHANGELOG.md`: Session 5 entry

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean (0 warnings) |
| `cargo test --workspace --all-features` | 1092 pass, 0 fail |
| `cargo test --doc --workspace --all-features` | 30 pass, 0 ignored |
| `cargo llvm-cov --all-features` | 90.83% lines, 92.31% regions |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| SPDX headers | All `.rs` files |
| Max file size | All under 1000 lines (max 858) |
| Production TODOs | 0 |
| Production unwrap/expect | 0 |

---

## Remaining Work

1. **Coverage headroom** — 90.83% achieved; remaining gaps:
   - `store_redb.rs` (67%) — internal DB error paths require fault injection
   - `handler.rs` (86%) — some JSON-RPC edge cases
   - `provenance/client.rs` (84%) — mock-only coverage paths

2. **Legacy env var fallbacks** — `BEARDOG_ADDRESS`, `NESTGATE_ADDRESS`,
   `LOAMSPINE_ADDRESS` still supported with deprecation warnings in
   `capability.rs`. Good practice for migration; remove in v1.0.

3. **CI coverage gate** — `cargo-llvm-cov` should be installed in CI
   workflow with 90% enforcement.

4. **Showcase cleanup** — `01-inter-primal-live/05-complete-workflows/`
   README references scripts that don't exist. `GAPS_DISCOVERED.md` and
   `EXECUTIVE_SUMMARY_FINAL.md` are expected outputs from showcase runs,
   not pre-existing — references are design-intentional.

---

## Dependency Status

Default build (redb, no http-clients) is 100% Pure Rust (ecoBin compliant).
C deps (`ring` via rustls) are properly gated behind the optional
`http-clients` feature with `deny.toml` enforcement. Seven additional
C-backed crates explicitly banned.

---

## Handoff Context

Previous sessions:
- Session 1 (Mar 12): wateringHole standards, UniBin, capability discovery
- Session 2 (Mar 13): Deep debt, 862 tests, cargo-deny, service lib extraction
- Session 3 (Mar 14): 90% coverage, platform-agnostic transport, doctor subcommand
- Session 4 (Mar 14): Sovereignty, doc tests, capability-based errors, 91% coverage
- Session 5 (Mar 14): This session — pedantic clippy, constants, UniBin signals, 1092 tests

Supersedes: `RHIZOCRYPT_V013_SOVEREIGNTY_DOCTESTS_CLEANUP_HANDOFF_MAR14_2026.md`
(archived to `handoffs/archive/`).

The codebase is fully clean under pedantic + nursery clippy, has centralized
constants, proper signal handling, and 1092 tests at 90.83% coverage.
Next evolution targets: CI coverage gate, fault-injection testing for
store_redb error paths, and legacy env var removal in v1.0.
