<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.29 — Dependency Evolution & Discovery-First Hardcoding Removal

| Field | Value |
|-------|-------|
| **Date** | 2026-04-02 |
| **Primal** | Squirrel (AI Coordination) |
| **From** | Deep debt execution session (session B) |
| **Version** | 0.1.0-alpha.29 |
| **Status** | GREEN — 7,161 tests / 0 failures / 110 ignored / 85.3% coverage / zero clippy / zero rustdoc warnings |

---

## Summary

Second deep debt session on April 2. Focused on three axes: (1) supply chain reduction
via systematic unused dependency removal, (2) discovery-first evolution of all hardcoded
endpoints/ports/hosts, and (3) production mock isolation and smart refactoring.

## Changes Made

### Supply Chain Reduction (50+ dependencies removed)

Systematic audit using `cargo-machete` + manual source verification across 13 crates.
Conservative approach: feature-gated and optional deps preserved even if not directly
referenced in current source.

Key removals:
- **Build/perf tooling**: `iai`, `pprof`, `parking_lot`
- **Unused runtime**: `sled`, `redis`, `wasmtime`, `tower`, `tower-http`
- **Duplicate/superseded**: `bytes`, `dashmap`, `futures`, `glob`, `secrecy`, `env_logger`
- **Networking**: `url`, `rustls` (direct), `metrics-exporter-prometheus`
- **Serialization**: `bincode`, `tracing-subscriber`
- **Advisory resolution**: `lru` removed from `squirrel-rule-system` → resolves RUSTSEC-2026-0002

### Production Mock Isolation

- `MockAIClient` in `ai-tools/src/common/clients/mod.rs` gated behind `#[cfg(any(test, feature = "testing"))]`
- Re-export in `ai-tools/src/common/mod.rs` similarly gated
- `justfile` test recipe updated to `cargo test --workspace --all-features` for integration test access

### Discovery-First Hardcoding Removal

All hardcoded hosts, ports, and primal-specific URLs replaced with dynamic resolution:

| Location | Before | After |
|----------|--------|-------|
| `ecosystem_service.rs` | `http://localhost:{port}` | `get_host("SQUIRREL_HOST", DEFAULT_LOCALHOST)` + `build_http_url()` |
| `federation/service.rs` | Duplicated `NODE_IP` → `MCP_HOST` → `"localhost"` | Extracted `resolve_node_host()` helper + `build_http_url()` |
| `dashboard_integration.rs` | `http://localhost:{}/api/observability` | `get_host("WEB_UI_HOST", ...)` + `get_port("WEB_UI_PORT", 8080)` |
| `presets.rs` | `bind_address: "127.0.0.1"`, `port: 8080` | `get_bind_address()` + `get_service_port("http")` |
| `security_adapter.rs` | `https://beardog.ecosystem.local` | `get_host("SECURITY_SERVICE_ENDPOINT", "https://security.ecosystem.local")` |
| `orchestration_adapter.rs` | `https://songbird.ecosystem.local` | `get_host("ORCHESTRATION_SERVICE_ENDPOINT", ...)` |
| `storage_adapter.rs` | `https://nestgate.ecosystem.local` | `get_host("STORAGE_SERVICE_ENDPOINT", ...)` |
| `compute_adapter.rs` | `https://toadstool.ecosystem.local` | `get_host("COMPUTE_SERVICE_ENDPOINT", ...)` |
| `schemas.rs` | `songbird → toadstool → squirrel → nestgate` | `orchestration → compute → self → storage` |

### Port Unification

- `DEFAULT_MCP_PORT` conflict (8778 in config.rs vs 8444 in server) resolved to 8444
- Doc comments in `server/mod.rs` corrected to match

### Smart Refactoring

- `optimization.rs` (919 lines) → `optimization/` module directory:
  - `selector.rs` — `ProviderSelector`
  - `scorer.rs` — `ProviderScorer`
  - `utils.rs` — `OptimizationUtils`
  - `tests.rs` — all test code with `MockClient`
  - `mod.rs` — re-exports
- `compute_adapter.rs` — extracted `compute_service_endpoints()` helper to stay under clippy line limit

### deny.toml Cleanup

- Removed `RUSTSEC-2026-0002` advisory ignore (lru dependency fully removed)
- Removed unused license allowances: `AGPL-3.0-only`, `OpenSSL`, `Unicode-DFS-2016`

### Doc Example Evolution

- Replaced `todo!()` in `security/traits.rs` doc examples with illustrative `Err(SecurityError::...)` returns
- Replaced `unimplemented!()` in `universal/traits.rs` doc examples with generic comments

### Orphan Module Audit (documented, not yet cleaned)

Identified uncompiled module trees present on disk but not declared in parent `mod.rs`/`lib.rs`:
- `crates/core/mcp/src/enhanced/`, `server/`, `client/`, `biome_handler/`, `protocol/rpc_helpers.rs`
- `crates/tools/ai-tools/src/providers/`, `api/`
- `crates/main/src/testing/`, `enhanced/`

These are archive/evolutionary fossils — present for reference but not compiled. Future session
candidate for archival to `ecoPrimals/fossilRecord/`.

## Metrics

| Metric | Before (alpha.28) | After (alpha.29) |
|--------|--------------------|-------------------|
| Tests passing | 7,161 | 7,161 |
| Workspace deps (Cargo.lock entries) | ~higher | -1,644 lines in lockfile |
| Hardcoded localhost sites | 4+ | 0 |
| Hardcoded primal URLs | 8 | 0 |
| Mock code in production | MockAIClient exposed | Fully isolated |
| Port conflicts | 1 (8778 vs 8444) | 0 |
| deny.toml advisory ignores | 1 | 0 |
| Files >1000 lines | 0 | 0 |
| Clippy warnings | 0 | 0 |

## Quality Gates

```
cargo fmt --all -- --check         ✅ PASS
cargo clippy --all-features -- -D warnings  ✅ PASS (0 warnings)
cargo doc --all-features --no-deps ✅ PASS (0 warnings)
cargo test --workspace --all-features       ✅ PASS (7,161 / 0 / 110)
cargo deny check                   ✅ PASS (0 warnings)
```

## Remaining Work (Future Sessions)

- **Coverage lift** — 85.3% → 90% target. Low files: `plugins/security.rs` (56%), `rule-system/evaluator.rs` (71%), `rule-system/manager.rs` (69%)
- **110 ignored tests** — audit and either fix or document
- **Orphan module archival** — move uncompiled module trees to `ecoPrimals/fossilRecord/`
- **ecoBin v3 C elimination** — ring via sqlx/rustls needs `rustls-rustcrypto` migration
- **Clone audit** — ~1,500+ `.clone()` calls; review top-10 production files for unnecessary clones
- **SDK MCP operations** — placeholder implementations need real server I/O
