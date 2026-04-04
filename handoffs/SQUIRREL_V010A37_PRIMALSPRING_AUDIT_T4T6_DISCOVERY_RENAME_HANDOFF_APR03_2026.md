<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.37 — primalSpring Audit T4/T6 Discovery Renames (2026-04-03)

## Summary

Address primalSpring audit findings: T4 Discovery (D → target B), T6 Responsibility
(C → target A). Renamed production primal-name coupling to capability-based domain
names. Removed dead workspace dependencies. T2 UniBin and T3 IPC verified already
compliant.

## primalSpring Audit Findings Addressed

| Tier | Finding | Action |
|------|---------|--------|
| T2 UniBin (C) | `--port` accepted but TCP not primary | Verified: `--port` wired to TCP JSON-RPC newline listener alongside UDS primary |
| T3 IPC (C) | TCP not used when UDS available, no domain symlink | Verified: SQ-01 dual bind (abstract + filesystem), `ai.sock` symlink created |
| T4 Discovery (D) | 1,789 primal-name refs / 215 files | Renamed production coupling (see below); residual refs are acceptable (enums, tests, serde, docs) |
| T6 Responsibility (C) | sled/sqlx/ed25519-dalek overstep | sled removed (dead dep); sqlx optional behind `persistence`; ed25519 behind `local-crypto` |

## Changes

### T6: Dead dependency cleanup

Removed 8 workspace deps with zero crate references:
`sled`, `redis`, `tungstenite`, `tracing-appender`, `rustls`, `rustls-pemfile`,
`wasmtime`, `wasmtime-wasi`.

### T4: Primal-name → capability-domain renames

**Security subsystem** (beardog → security_provider):
- `beardog_coordinator.rs` → `security_coordinator.rs`
- `BeardogSecurityCoordinator` → `SecurityCoordinator` (deprecated alias kept)
- `beardog_endpoint` → `security_endpoint` (config + serde alias)
- `enable_beardog_integration` → `enable_security_delegation`
- `authenticate_with_beardog` → `authenticate_with_security_provider`
- `SecurityProviderConfig::beardog()` → `::security_provider()`

**Compute subsystem** (toadstool → compute):
- `toadstool_endpoint` → `compute_endpoint` (config fields, env vars, defaults)
- `register_toadstool_service` → `register_compute_service`
- Env: `COMPUTE_ENDPOINT` primary, `TOADSTOOL_ENDPOINT` fallback

**Storage subsystem** (nestgate → storage):
- `nestgate_endpoint` → `storage_endpoint` (config fields, env vars)
- `register_nestgate_service` → `register_storage_service`
- Env: `STORAGE_ENDPOINT` primary, `NESTGATE_ENDPOINT` fallback

**Metrics** (primal modules → domain modules):
- `metric_names::toadstool` → `metric_names::compute`
- `metric_names::nestgate` → `metric_names::storage`
- `metric_names::beardog` → `metric_names::security_metrics`

### Backward compatibility

- All config fields have `#[serde(alias = "old_name")]`
- All env vars chain: new primary → old fallback
- Deprecated type alias `BeardogSecurityCoordinator = SecurityCoordinator`

## Verification

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (0 failures) |
| `cargo doc --no-deps` | PASS |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Primal-name ref counts (post-rename)

| Name | Refs | Files | Classification |
|------|------|-------|----------------|
| squirrel | 2,249 | 386 | Self-identity (acceptable) |
| beardog | 654 | 103 | Enum variants, primal_names, serde aliases, tests, provider integration |
| songbird | 303 | 88 | Enum variants, doc examples, test data, service mesh references |
| toadstool | 201 | 55 | Enum variants, doc examples, env fallbacks, test data |
| nestgate | 158 | 53 | Enum variants, doc examples, env fallbacks, test data |
| biomeos | 569 | 95 | Ecosystem integration (own domain) |

## Remaining acceptable debt

- `universal-patterns/security/providers/beardog.rs` — integration client that must
  know the security primal's protocol; acceptable coupling
- `PrimalType` enum variants, `primal_names` constants — canonical naming registry
- `niche.rs` `DEPENDENCIES` — legitimate self-knowledge of deploy graph
- Doc comments mentioning primals as examples — documentation
