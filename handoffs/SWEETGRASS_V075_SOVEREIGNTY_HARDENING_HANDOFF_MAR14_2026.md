# SweetGrass v0.7.5 — Sovereignty Hardening + Coverage Push Handoff

**Date**: March 14, 2026
**From**: SweetGrass (v0.7.5)
**To**: All primal teams, biomeOS, Springs
**License**: AGPL-3.0-only
**Supersedes**: v0.7.4 handoff

---

## Summary

SweetGrass v0.7.5 is a **breaking JSON-RPC method rename** aligning all methods
to the `{domain}.{operation}` snake_case standard from
`SEMANTIC_METHOD_NAMING_STANDARD`. Discovery structs renamed for vendor-agnostic
sovereignty. UDS socket path and tarpc concurrency made configurable.
`#[allow]` attributes evolved to `#[expect(..., reason)]` with documented
rationale. 34 new tests bring region coverage to 91%.

---

## Breaking Changes

### JSON-RPC Method Renames (11 methods)

All methods now follow `{domain}.{operation}` snake_case per wateringHole standard.

| Old (v0.7.4) | New (v0.7.5) | Domain |
|---------------|--------------|--------|
| `braid.getByHash` | `braid.get_by_hash` | braid |
| `braid.getByContent` | `braid.get_by_content` | braid |
| `braid.getBatch` | `braid.get_batch` | braid |
| `provenance.exportProvo` | `provenance.export_provo` | provenance |
| `attribution.topContributors` | `attribution.top_contributors` | attribution |
| `compression.compressSession` | `compression.compress_session` | compression |
| `compression.createMetaBraid` | `compression.create_meta_braid` | compression |
| `contribution.recordSession` | `contribution.record_session` | contribution |
| `contribution.recordDehydration` | `contribution.record_dehydration` | contribution |
| `anchoring.anchorBraid` | `anchoring.anchor` | anchoring |
| `anchoring.verifyAnchor` | `anchoring.verify` | anchoring |

**Unchanged methods** (already compliant): `braid.create`, `braid.get`,
`braid.query`, `braid.delete`, `braid.commit`, `provenance.graph`,
`attribution.chain`, `contribution.record`, `anchoring.get_anchors`,
`health.check`.

### Complete Method Table (v0.7.5)

| Method | Handler |
|--------|---------|
| `braid.create` | Create a new braid |
| `braid.get` | Get braid by ID |
| `braid.get_by_hash` | Get braid by content hash |
| `braid.get_by_content` | Get braid by content match |
| `braid.get_batch` | Batch get by IDs |
| `braid.query` | Query braids with filters |
| `braid.delete` | Delete a braid |
| `braid.commit` | Commit braid to LoamSpine |
| `provenance.graph` | Get provenance graph |
| `provenance.export_provo` | Export W3C PROV-O JSON-LD |
| `attribution.chain` | Get attribution chain |
| `attribution.top_contributors` | Top N contributors |
| `compression.compress_session` | Compress a session |
| `compression.create_meta_braid` | Create meta-braid |
| `contribution.record` | Record a contribution |
| `contribution.record_session` | Record session contribution |
| `contribution.record_dehydration` | Record dehydration summary |
| `anchoring.anchor` | Anchor a braid |
| `anchoring.verify` | Verify anchor |
| `anchoring.get_anchors` | Get anchors for braid |
| `health.check` | Health check |

---

## Action Required by Consumers

### biomeOS

`capability_registry.toml` translations updated to new method names.
No graph changes needed — graphs use semantic capability names
(`provenance.create_braid`, etc.) that route through the registry.

### rhizoCrypt

`ProvenanceNotifier` updated: `contribution.record_session` and
`contribution.record_dehydration` (was camelCase).

### Springs (ludoSpring, wetSpring, airSpring, etc.)

Springs using `sweet-grass-core` as a Cargo dep for type definitions:
no changes needed (types unchanged). Springs calling sweetGrass via
biomeOS capability routing: no changes needed (registry handles translation).

### Direct JSON-RPC Callers

Any code sending raw JSON-RPC to sweetGrass must update method strings.

---

## Non-Breaking Changes

### Sovereignty Hardening

- `SongbirdDiscovery` renamed to `RegistryDiscovery` (vendor-agnostic)
- `SongbirdRpc` renamed to `RegistryRpc`
- UDS socket path resolved from `SelfKnowledge` / `PRIMAL_NAME` env
  (was hardcoded `PRIMAL_NAME` constant)
- tarpc `max_concurrent_requests` configurable via env `TARPC_MAX_CONCURRENT_REQUESTS`
  and builder (was hardcoded `100`)

### Idiomatic Rust

- 11 production `#[allow(...)]` evolved to `#[expect(..., reason = "...")]`
- 2 `value as u64` casts replaced with `u64::try_from(...).unwrap_or(0)`
- Mock factory docs clarify `#[cfg]` branching (compile-time isolation)

### Coverage

- 34 new tests (760 → 794)
- Region coverage: 91% (was 89%)
- Line coverage: 89% (postgres store and binary entry need Docker/e2e infra)

### Dependencies

- `cargo-deny` fully passing (dev-only advisory ignores for testcontainers chain)
- All production deps pure Rust (no C backends)

---

## Metrics

```
Version:        0.7.5
Tests:          794 passing
Region coverage: 91% (cargo llvm-cov)
Line coverage:  89%
Clippy:         0 warnings (pedantic + nursery)
Max file:       828 lines (limit: 1000)
TODOs:          0 in source
Unsafe:         0 (forbidden)
cargo deny:     advisories ok, bans ok, licenses ok, sources ok
```

---

## Coordination Status

| Integration | Status |
|-------------|--------|
| biomeOS capability_registry.toml | Updated to v0.7.5 methods |
| biomeOS rootpulse_commit.toml | Uses semantic capabilities (no changes needed) |
| rhizoCrypt ProvenanceNotifier | Updated to snake_case methods |
| ludoSpring exp052-066 | Uses sweet-grass-core types (no changes needed) |
| LoamSpine braid.commit | Unchanged (already compliant) |
| API spec (specs/API_SPECIFICATION.md) | Updated to v0.7.5 method table |
| PRIMAL_REGISTRY.md | Updated: v0.7.5, 794 tests, 91% coverage |
