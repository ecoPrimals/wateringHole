# Squirrel v0.10 — Deep Debt: Env Evolution, Orphan Removal, Cross-Arch Fix (April 20, 2026)

## Changes

### 1. Cross-Arch `uname()` Fix (primalSpring PG audit)

`rustix::system::uname()` is infallible in rustix 1.x (returns `Uname`), but
code used `if let Ok(u) = uname()` from the 0.38.x API. Gated behind
`#[cfg(all(unix, not(target_os = "linux")))]` so it never compiled on Linux —
only broke macOS/Android targets.

**Verified clean on**: `aarch64-apple-darwin`, `x86_64-apple-darwin`,
`aarch64-linux-android`.

### 2. Orphaned File Removal

`ecosystem-api/src/client.rs`, `client_types.rs`, `client_mock.rs` (802 lines
total) were **never mounted** in `lib.rs`. They referenced `reqwest` (removed in
stadial gate) and would not compile even if mounted. Deleted as dead code.

### 3. Env Var Evolution to Capability-First

| Constant | Old Value | New Value |
|----------|-----------|-----------|
| `HEARTBEAT_INTERVAL` | `SONGBIRD_HEARTBEAT_INTERVAL` | `SERVICE_MESH_HEARTBEAT_INTERVAL` |
| `INITIAL_DELAY` | `SONGBIRD_INITIAL_DELAY_MS` | `SERVICE_MESH_INITIAL_DELAY_MS` |
| `BIOMEOS_REGISTRATION_URL` | `BIOMEOS_REGISTRATION_URL` | `ECOSYSTEM_REGISTRATION_URL` |
| `BIOMEOS_HEALTH_URL` | `BIOMEOS_HEALTH_URL` | `ECOSYSTEM_HEALTH_URL` |
| `BIOMEOS_METRICS_URL` | `BIOMEOS_METRICS_URL` | `ECOSYSTEM_METRICS_URL` |

Legacy env var names (`SONGBIRD_*`, `BIOMEOS_*`) remain as fallbacks in the
config resolution chains — no breaking change for existing deployments.

### 4. EcosystemEndpoints Refactor

`EcosystemEndpoints::default()` refactored from ~90 lines of repetitive
per-endpoint `BIOMEOS_*` resolution to ~25 lines via extracted
`resolve_ecosystem_endpoint()` helper. Now checks `ECOSYSTEM_*` before
`BIOMEOS_*` for each endpoint.

### 5. `get_biomeos_endpoints()` Capability-First

Added `ECOSYSTEM_ENDPOINT`/`ECOSYSTEM_PORT` > `BIOMEOS_ENDPOINT`/`BIOMEOS_PORT`
chains in `primal_provider/core/mod.rs`.

### 6. Comprehensive Audit Findings

| Category | Result |
|----------|--------|
| Actual `unsafe` blocks | **0** (all hits are doc comments) |
| `TODO`/`FIXME`/`HACK`/`todo!`/`unimplemented!` | **0** |
| `#[allow()]` in production | **1** (justified: trait method in `providers/types.rs`) |
| Production mocks | **0** (all behind `#[cfg(test)]` or test features) |
| Production files >800L | **0** |
| Hardcoded primal name string literals | **0** in `Class C` — all remaining are backward-compat aliases (Class A), enum variants (Class E), or doc comments (Class D) |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 |
| Coverage | 90.1% |
| `.rs` files | ~1,032 (down from ~1,035) |
| Lines | ~335k (down from ~336k) |
| Production files >800L | 0 |
| `cargo clippy -- -D warnings` | 0 warnings |
| `cargo fmt -- --check` | clean |
