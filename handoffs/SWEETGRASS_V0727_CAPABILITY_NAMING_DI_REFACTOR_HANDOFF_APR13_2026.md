# SweetGrass v0.7.27 — Capability-Based Naming, DI, Smart Refactor

**Date**: April 13, 2026
**Sprint**: Deep Debt Cleanup III — Hardcoding Elimination & Code Quality
**Status**: COMPLETE

---

## Problem

Post-NestGate/composition sprint audit revealed:
1. Primal marketing names hardcoded in production code (`call_beardog_at`, composition health variables)
2. `Box<dyn std::error::Error>` in composition probe — not `thiserror`-compliant
3. `uds/tests.rs` at 958 lines — approaching 1000-line limit
4. Config tests sharing `/tmp/` with fixed filenames — parallel test race risk
5. `std::env::var` in composition health — not DI-injectable

## Solution

### 1. Capability-Based Naming (Hardcoding Elimination)

- **`call_beardog_at` → `call_security_provider_at`**: Function name no longer encodes a specific primal identity. Any provider implementing the `crypto.*` capability domain is supported.
- **Composition health variables**: `beardog` → `security`, `songbird` → `discovery`, `toadstool` → `compute`, `nestgate` → `storage`, `rhizocrypt` → `provenance`, `loamspine` → `ledger`. All variables now match their capability domain, not marketing names.
- **Doc comments**: Updated to reference capability domains rather than primal names.

### 2. Typed Error Handling

Replaced `Box<dyn std::error::Error + Send + Sync>` in `probe_capability` with `std::io::Result`:
- Serde errors mapped through `std::io::Error::new(ErrorKind::InvalidData, ...)`
- No trait-object boxing in the hot path
- Timeout wrapper still returns `"degraded"` on any failure

### 3. DI Pattern for Composition Health

Extracted `probe_capability_with_reader` and `discover_capability_socket_with_reader`:
- Accept `&(impl Fn(&str) -> Option<String> + Sync)` for env var injection
- `Sync` bound required for safe use in async context (`clippy::future_not_send`)
- Production code uses `|key| std::env::var(key).ok()` at composition root
- Tests can inject mock readers without `temp_env` mutex contention

### 4. Smart Refactor: `uds/tests.rs` → 5 Submodules

958-line monolithic test file split by concern:
- `tests/resolution.rs` (115 lines) — DI-based socket path resolution
- `tests/symlink.rs` (111 lines) — Cleanup and capability symlink management
- `tests/guard.rs` (42 lines) — BTSP insecure guard validation
- `tests/roundtrip.rs` (504 lines) — UDS protocol, concurrent, shutdown, self-knowledge
- `tests/env.rs` (179 lines) — Env-reading wrapper coverage

Uses `#[path = "tests/..."]` directives for `rustfmt` compatibility with edition 2024.

### 5. Config Test Isolation

Migrated 5 tests from shared `std::env::temp_dir()` with fixed filenames:
- `sweetgrass_test_config.toml` → `tempfile::tempdir()/config.toml`
- `sweetgrass_test_env_override.toml` → isolated tempdir
- `sweetgrass_test_invalid.toml` → isolated tempdir
- `sweetgrass_test_xdg_config/` → isolated tempdir
- `sweetgrass_test_home_config/` → isolated tempdir

Added `tempfile` as dev-dependency to `sweet-grass-core`.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --all-features` | PASS |
| `cargo clippy --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo fmt --all -- --check` | PASS |
| `cargo deny check` | PASS |
| `cargo test --all-features` | PASS (1,427 tests) |
| Coverage (testable code) | 90.4% line / 92.2% region |

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Hardcoded primal names in prod | 3 sites | 0 |
| `Box<dyn Error>` in prod | 1 | 0 |
| Max test file size | 958 lines | 504 lines |
| Config test isolation | Shared `/tmp/` | Per-test `tempdir` |
| Composition health DI | Direct `std::env::var` | Injectable reader |
| Tests | 1,427 | 1,427 |

## Files Changed

- `crates/sweet-grass-service/src/btsp/server.rs` — rename `call_beardog_at`
- `crates/sweet-grass-service/src/handlers/jsonrpc/composition.rs` — typed errors, DI, domain naming
- `crates/sweet-grass-service/src/uds/tests.rs` → hub file + 5 submodules
- `crates/sweet-grass-core/src/config/tests.rs` — tempdir isolation
- `crates/sweet-grass-core/Cargo.toml` — `tempfile` dev-dep
- `CHANGELOG.md`, `README.md`, `CONTEXT.md`, `DEVELOPMENT.md`, `QUICK_COMMANDS.md` — metrics

## Remaining Known Debt (Low)

- `server/tests.rs` at 898 lines — next refactor candidate
- Postgres full-path coverage — needs Docker CI
- NestGate store integration tests — needs running NestGate primal
- Pre-existing flaky TCP tests — timing-sensitive `sleep(100ms)` patterns
- `sqlx` Postgres driver not explicitly banned in `deny.toml` (implicit FFI hole)
