<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.16 — Deep Debt Resolution & Compliance Audit Handoff

**Date**: March 22, 2026
**Primal**: Squirrel (AI coordination)
**Domain**: `ai`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)

## Summary

Comprehensive audit and deep debt resolution sprint. Zero Clippy warnings under
full pedantic/nursery lint set. Dependency evolution: removed unmaintained/unsound
crates (`serde_yml`, `yaml-rust`, `config`). All cargo-deny checks passing.
Production stubs evolved to complete implementations. Smart file refactoring —
all files under 1,000 lines. Test suite expanded from 5,440 to 5,574. Coverage
improved from 69.95% to 71.05% lines.

## Changes

### Dependency Evolution

- **`serde_yml` → `serde_yaml_ng` v0.10** — `serde_yml` was flagged unmaintained
  and unsound; migrated all Cargo.tomls and source files to maintained fork
- **Removed `config` v0.13** — unused direct dependency in ai-tools; also removes
  transitive `yaml-rust` (unmaintained)
- **Removed `yaml-rust` v0.4** — unused direct dependency in rule-system
- **Pinned 22 wildcard internal deps** — all `path = "…"` now carry explicit version
- **cargo-deny fully passing** — `advisories ok, bans ok, licenses ok, sources ok`
- **`deny.toml` documented exceptions** — `cc@1` (build-time only via pprof/wasmtime/sqlx-sqlite),
  `bincode` advisory (tarpc transitive, RUSTSEC-2025-0141), `linked-hash-map` advisory
  (yaml-rust transitive, RUSTSEC-2026-0002)

### Clippy Pedantic/Nursery Compliance

- Zero warnings on `cargo clippy --all-features -- -D warnings`
- Added `#[must_use]` on 11+ return-value functions
- Added `# Errors` doc sections on 123+ `Result`-returning public functions
- Removed workspace-level `must_use_candidate = "allow"` and `missing_errors_doc = "allow"`
- All 22 crates use `#[cfg_attr(test, allow(clippy::unwrap_used, clippy::expect_used))]`
  instead of blanket `#![allow]`

### Smart File Refactoring

All files now under 1,000 lines (max: 985 — `rate_limiter.rs`):

| File | Before | After |
|------|--------|-------|
| `ipc_client.rs` | 999 lines | 6 modules (types, discovery, connection, messaging, tests, mod) |
| `types.rs` (config) | 972 lines | 4 files (definitions, defaults, impls, mod) |
| `traits.rs` (ecosystem-api) | 960 lines | 6 files (primal, mesh, discovery, ai, config, tests) |
| `adapter.rs` (MCP) | 974 lines | 3 files (core, tests, mod) |
| `monitoring.rs` | 1,384 lines | 953 + 431 (tests extracted to `monitoring_tests.rs`) |

### Production Stub Evolution

- **`PlaceholderPlugin` → `NoOpPlugin`** — null-object pattern with `create_noop_plugin()`
- **`SystemPlaceholderPlugin` → `DefaultPlugin`** — proper lifecycle logging
- **Federation hardcoded strings → `CapabilityUnavailable`** — new `CoreError` variant
  maps to HTTP 503 with structured capability ID and hint
- **AI vendor clients → `IpcRoutedVendorClient`** — delegates through ecosystem IPC
  via `NeuralHttpClient` rather than direct HTTP

### Hardcoding Evolution

- Ports and IPs evolved to `DiscoveredEndpoint` pattern with env-var discovery chain
- Primal code only has self-knowledge; discovers peers via capabilities at runtime
- `CapabilityIdentifier` replaces deprecated `EcosystemPrimalType` enum

## Quality Gate

| Metric | Value |
|--------|-------|
| Tests | 5,574 passing / 0 failures |
| Line coverage | 71.05% (up from 69.95%) |
| Clippy | CLEAN (`pedantic + nursery + deny(warnings)`, zero errors) |
| cargo-deny | All 4 checks passing (advisories, bans, licenses, sources) |
| cargo doc | Zero warnings (`--all-features --no-deps`) |
| Formatting | `cargo fmt --check` passes |
| Unsafe | 0 in production (`#![forbid(unsafe_code)]` in all 22 crates) |
| Files >1000L | 0 (max: 985) |
| `.rs` files | 1,287 |
| SPDX headers | 100% (1,287/1,287) |

## Impact on Other Primals

### For All Primals

- The `serde_yml` → `serde_yaml_ng` migration pattern is recommended for any primal
  still using `serde_yml`. The crate is unmaintained and has known unsoundness.
- The `#[cfg_attr(test, allow(clippy::unwrap_used))]` pattern (instead of blanket
  `#![allow]`) is the recommended approach for test exemptions.

### For primalSpring

No changes to exposed capabilities or consumed capabilities from alpha.15. The
recommendation from that handoff still stands: update Squirrel node `health_method`
from `"ai.health"` to `"health.liveness"` in `primalspring_deploy.toml`.

### For Songbird/BearDog

No protocol changes. Squirrel's IPC client refactoring is internal — the public
API surface is unchanged.

## Remaining Debt

1. **Coverage gap** — 71% → 90% target requires focused test expansion in:
   ai-tools (11%), config (26%), universal-patterns (34%), ecosystem-api (29%)
2. **Performance optimizer stubs** — `batch_processor` and `optimizer` in
   `core/plugins/src/performance_optimizer/` deferred to Phase 2
3. **`chaos_07_memory_pressure`** — flaky under parallel test load

## Patterns Worth Adopting

1. **cargo-deny with documented exceptions** — `skip` rules with `reason` fields
   for build-time-only transitive deps, rather than banning outright
2. **Smart file refactoring** — split by semantic boundaries (types, discovery,
   connection, messaging) not arbitrary line counts
3. **Null-object pattern** — `NoOpPlugin` with `create_noop_plugin()` factory for
   clean plugin system fallbacks
4. **`CapabilityUnavailable` error variant** — structured 503 with capability ID
   and hint, rather than "not yet implemented" strings

## Dependencies

| Primal | Capabilities Used | Required |
|--------|-------------------|----------|
| BearDog | `crypto.*`, `auth.*`, `secrets.*`, `relay.*` | Yes |
| Songbird | `discovery.*` | Yes |
| ToadStool | `compute.*` | No |
| NestGate | `storage.*`, `model.*` | No |
| primalSpring | `coordination.*`, `composition.*` | No |
| petalTongue | `visualization.*`, `interaction.*` | No |
| rhizoCrypt | `dag.*` | No |
| sweetGrass | `anchoring.*`, `attribution.*` | No |
| Domain Springs | `mcp.tools.list`, `health.*` | No |
