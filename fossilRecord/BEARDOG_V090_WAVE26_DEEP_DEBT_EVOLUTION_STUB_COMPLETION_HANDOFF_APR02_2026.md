# BearDog v0.9.0 — Wave 26 Deep Debt Evolution + Stub Completion Handoff

**Date:** April 2, 2026
**Author:** AI pair (Claude) + eastgate
**Scope:** primalSpring audit remediation, deep debt cleanup, stub → implementation evolution, dependency alignment, dead code removal, root doc reconciliation

---

## Summary

Executed on all remaining deep debt cleanup and evolution gaps identified by
the primalSpring downstream audit. Stabilised flaky tests, evolved stubs to
real implementations, aligned workspace dependencies, wired orphaned modules,
cleaned dead code, removed debris, and updated all root documentation.

---

## Gate Status (April 2, 2026)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace -D warnings` | Pass (0 warnings) |
| `cargo build --workspace` | Pass |
| `cargo test --workspace` | **14,366 passed, 0 failed** |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

---

## primalSpring Audit Items — All Resolved

| Item | Before | After |
|------|--------|-------|
| Flaky `test_production_ready_thread_safe` | Assertion fail under concurrent `config::production_ready` | 35 tests `#[serial]` (shared `AtomicBool`) |
| `deny.toml` skip-list | 30 transitive version-skips | 15 (12 resolved splits removed) |
| AI tree scope (11.9K LOC) | Compiled unconditionally | Feature-gated behind `ai` Cargo feature |
| `beardog-integration` (2.6K LOC) | In workspace | Already excluded from workspace per responsibility matrix |

---

## Stub → Implementation Evolution

| Stub | Evolution |
|------|-----------|
| `handle_key_info` ("Coming soon!") | Real implementation: loads key metadata from `~/.beardog/keys/` via `key_store::load_key`; `_with_home` DI variant for tests |
| `client.rs` ("Command execution not yet implemented") | Real JSON-RPC 2.0 `dispatch_rpc()` over Unix socket with NDJSON framing |
| `universal_hsm/entropy/` (never compiled) | Wired into module tree; `collector.rs` and `live_feed_validator.rs` now compile and pass 15 tests |
| `collector_production_tests.rs` (referenced nonexistent `EntropyConfig`) | Rewritten to match current `EntropyCollector` API |

---

## Dependency Alignment

All root `Cargo.toml` dependencies now use `workspace = true`:

- `beardog-ipc` (was `path = "crates/beardog-ipc"`)
- `beardog-hid` (added to `[workspace.dependencies]`, was `path = "crates/beardog-hid"`)
- `serial_test` (was explicit `"3.2"`, now workspace)
- `beardog-adapters`, `beardog-capabilities`, `beardog-genetics` (were `path =`, now workspace)
- `tempfile` (was explicit `"3.8"`, now workspace)

---

## Dead Code Cleanup

| File | Change |
|------|--------|
| `quantum_discovery.rs` | Removed 3 unused `Arc<RwLock<…>>` fields + `RwLock` import |
| `api_endpoints.rs` | 3 test-only `BearDogCore` methods moved behind `#[cfg(test)]` |
| `key_revoke.rs` | Removed redundant `#[allow(dead_code)]` from `merge()` (it is used) |
| `live_feed_validator.rs` | Wired unused `min_hardware_entropy_ratio` field into validation logic |
| tarpc client/server docs | Hardcoded `127.0.0.1:9901` → capability-based discovery references |

---

## Debris Removed

- `audit.log` (159 KB) — build artifact
- `env.example` — duplicate of `.env.example`
- `crates/beardog-integration-tests/src/` — empty directory

---

## Known Remaining Debt (Low Priority)

| Item | Status | Notes |
|------|--------|-------|
| FIDO2/CTAP2 Phase 2 stubs | Documented | Returns proper errors, not fake data |
| iOS XPC transport | Documented | Returns `Unsupported` with TCP fallback guidance |
| `universal_hsm/providers/` (5 files) | On-disk, not compiled | API-drifted from current types; needs alignment before wiring |
| PKCS#11 provider fields (`library_path`, `slot_id`, `metadata`) | `#[allow(dead_code)]` | Reserved for Phase 2 session wiring; read in tests |
| `beardog-production` coverage (59%) | Tracked | Config management module; serial test constraint limits parallel coverage pushes |

---

## Files Changed

Workspace root:
- `Cargo.toml` — dependency alignment
- `STATUS.md` — updated to accurate current state
- `CHANGELOG.md` — Wave 26 entry added
- `audit.log` — deleted
- `env.example` — deleted (duplicate)

Crates:
- `beardog-cli/src/handlers/key.rs` — `handle_key_info` + `handle_key_info_with_home` implementations
- `beardog-tunnel/src/modes/client.rs` — JSON-RPC dispatch implementation
- `beardog-tunnel/src/universal_hsm/mod.rs` — wired entropy + traits modules
- `beardog-tunnel/src/universal_hsm/entropy/collector.rs` — idiomatic rewrite
- `beardog-tunnel/src/universal_hsm/entropy/live_feed_validator.rs` — idiomatic rewrite
- `beardog-tunnel/src/universal_hsm/entropy/collector_production_tests.rs` — API-aligned rewrite
- `beardog-core/src/ecosystem/quantum_discovery.rs` — dead fields removed
- `beardog-core/src/ecosystem/primal_interface/api_endpoints.rs` — test-only gating
- `beardog-core/src/lib.rs` — AI module test gating
- `beardog-ipc/src/tarpc_client.rs` — doc evolution
- `beardog-ipc/src/tarpc_server/server.rs` — doc evolution
- `beardog-tunnel/src/coverage_boost_wave10.rs` — test updated for new client behavior
- `src/main_coverage_extension.rs` — test updated for key_info error semantics

---

## Next Steps

1. Wire `universal_hsm/providers/` modules after aligning with current `BearDogError` API
2. Continue `beardog-production` coverage push (currently 59%)
3. Track `deny.toml` skip-list reduction as RustCrypto ecosystem aligns (15 → target 0)
4. Long-term: AI tree (11.9K LOC) relocation decision per NUCLEUS crypto boundary
