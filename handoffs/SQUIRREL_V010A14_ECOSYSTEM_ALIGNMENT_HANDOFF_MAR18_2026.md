<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.14 — Ecosystem Alignment Handoff

**Date**: March 18, 2026
**Primal**: Squirrel (AI coordination)
**Domain**: `ai`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)

## Summary

Ecosystem alignment sprint: capability registry TOML sync test as a compile-time
invariant, `SpringToolDef` aligned with biomeOS `McpToolDefinition` V251 types,
`PRIMAL_DOMAIN` constant for cross-primal identity consistency, consumed
capabilities expanded to 29, cross-compile CI targets for aarch64-musl.

## Changes

### Added

- **Capability registry TOML sync test** — `niche::tests::capability_registry_toml_sync`
  uses `include_str!` to compile-time verify bidirectional consistency between
  `niche::CAPABILITIES` and `capability_registry.toml`
- **`identity::PRIMAL_DOMAIN`** — `"ai"` constant in `universal-constants::identity`
  matching `niche::DOMAIN`; cross-verified by `identity_primal_domain_matches_niche_domain` test
- **7 new consumed capabilities**:
  - `health.liveness`, `health.readiness` — probe peer primals before routing
  - `relay.authorize`, `relay.status` — BearDog relay coordination
  - `dag.event.append`, `dag.vertex.query` — rhizoCrypt DAG sessions
  - `anchoring.verify` — sweetGrass provenance verification
- **`build-ecobin-arm` / `build-ecobin-all`** justfile targets for `aarch64-unknown-linux-musl`

### Changed

- **`SpringToolDef`** — added optional `version` and `primal` fields for biomeOS
  `McpToolDefinition` V251 interop (backward-compatible via `#[serde(skip_serializing_if)]`)

## Quality Gate

| Metric | Value |
|--------|-------|
| Tests | 5,430 passing / 0 failures |
| Clippy | CLEAN (`pedantic + nursery + deny(warnings)`) |
| Formatting | `cargo fmt --check` passes |
| Unsafe | 0 in production |
| ecoBin | 14-crate C-dep ban list |
| Consumed capabilities | 29 |

## Patterns Worth Adopting

1. **TOML sync test** — Any primal with a `capability_registry.toml` should add
   an `include_str!` test verifying its niche `CAPABILITIES` array stays in sync.
2. **`PRIMAL_DOMAIN` in identity** — Ensures domain consistency across modules.
3. **`McpToolDefinition` alignment** — Springs returning `mcp.tools.list` should
   include `version` and `primal` fields for richer routing.

## Known Issues

1. `chaos_07_memory_pressure` flaky under parallel test load
2. Coverage at 71% — gap to 90% target
3. `adapter.rs` (974L) unwired legacy code

## Dependencies

| Primal | Capabilities Used | Required |
|--------|-------------------|----------|
| BearDog | `crypto.*`, `auth.*`, `secrets.*`, `relay.*` | Yes |
| Songbird | `discovery.*` | Yes |
| ToadStool | `compute.*` | No |
| NestGate | `storage.*`, `model.*` | No |
| rhizoCrypt | `dag.*` | No |
| sweetGrass | `anchoring.*`, `attribution.*` | No |
| Domain Springs | `mcp.tools.list`, `health.*` | No |
