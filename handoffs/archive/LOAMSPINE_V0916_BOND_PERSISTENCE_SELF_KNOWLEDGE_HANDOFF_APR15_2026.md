<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Bond Persistence & Self-Knowledge Evolution

**Date**: April 15, 2026
**Primal**: loamSpine
**Version**: 0.9.16
**Previous handoff**: `LOAMSPINE_V0916_DEEP_DEBT_EVOLUTION_PASS2_HANDOFF_APR12_2026.md` (archived)

---

## Summary

Two passes of deep debt evolution focused on (1) implementing the bond ledger persistence wire contract from primalSpring's provenance trio audit, and (2) evolving all production code to strict self-knowledge-only compliance — no hardcoded primal names in production code or docs.

---

## Pass 1: Bond Ledger Persistence

Implements the `bonding.ledger.*` wire contract from `STORAGE_WIRE_CONTRACT.md` for ionic bond state persistence.

### New JSON-RPC Methods (3)

| Method | Description |
|--------|-------------|
| `bonding.ledger.store` | Store ionic bond record (append-only spine + in-memory index) |
| `bonding.ledger.retrieve` | Retrieve bond by ID (O(1) via HashMap) |
| `bonding.ledger.list` | List all stored bond IDs |

### Implementation

- **`BondLedgerRecord` entry type**: New `EntryType` variant in `entry/mod.rs` with `bond_id` + opaque `serde_json::Value` data
- **`bond-ledger` capability**: Added to `LoamSpineCapability` with `append_only: true` semantics
- **Dedicated bond spine**: Lazily created on first `store`, with in-memory `HashMap<bond_id, data>` index for O(1) retrieval
- **Full RPC stack**: `loam-spine-core` service → `loam-spine-api` types → tarpc trait → JSON-RPC dispatch → integration tests
- **NeuralAPI + MCP**: Bond ledger methods advertised in capability list, cost estimates, and MCP tool discovery
- **Niche self-knowledge**: `"bonding"` domain, 3 methods, semantic mappings, cost estimates all registered

### Tests Added

- 7 unit tests in `service/bond_ledger.rs`
- 9 JSON-RPC integration tests in `jsonrpc/tests_bond_ledger.rs`
- Covers: store, retrieve, list, overwrite, realistic ionic bond data, error handling

---

## Pass 2: Self-Knowledge Evolution

### BTSP Provider Decoupling (Code-Level)

- `DEFAULT_BTSP_PROVIDER_PREFIX`: `"beardog"` → `"btsp-provider"` (protocol-based naming)
- `BEARDOG_SOCKET` env fallback: **removed** — only `BTSP_PROVIDER_SOCKET` honored
- All 31 BTSP tests updated to match new naming
- Mock function `handle_mock_beardog_connection` → `handle_mock_btsp_provider`

### Production Doc/Comment Scrub (~50 references)

Hardcoded primal names replaced with capability-generic language across 25+ files:

| Old Pattern | New Pattern |
|-------------|-------------|
| `BearDog` | "crypto capability primal", "BTSP provider", "signing primal" |
| `rhizoCrypt` | "ephemeral DAG primal", "ecosystem convention" |
| `sweetGrass` | "attribution primal" |
| `NestGate` | "content-addressed storage" |
| `barraCuda` / `ToadStool` / `songbird` | "ecosystem convention/pattern" |

Affected modules: `entry`, `capabilities`, `trio_types`, `temporal` (2), `sync`, `streaming`, `error` (3), `traits`, `discovery`, `certificate`, `waypoint`, `niche`, `jsonrpc` (2), `permanent_storage`, `integration_ops`, `rpc.rs`, `uds.rs`, `main.rs`, `Cargo.toml` (2)

### API Evolution

- `bond_ledger_store`: `String` → `impl Into<String>` for `bond_id`
- `DiscoveryCache::insert`: `String` → `impl Into<String>` for capability key

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | **1,434** (all concurrent, ~3s, zero flaky) |
| Source files | **186** `.rs` (+ 3 fuzz targets) |
| JSON-RPC methods | **37** |
| Coverage | ~90.9% line / ~89% branch / ~92.9% region |
| Clippy | 0 warnings (pedantic + nursery) |
| `cargo doc` | 0 warnings |
| Unsafe | 0 (`#![forbid(unsafe_code)]`) |
| Max file size | 783 lines (test file); all production < 605 |
| SPDX headers | All 186 source files |
| Capability Wire Standard | **Full L3** |

---

## Gates (All Green)

```
cargo fmt --all -- --check     ✓
cargo clippy --all-targets     ✓ (0 warnings)
cargo doc --no-deps            ✓ (0 warnings)
cargo test --workspace         ✓ (1,434 passed, 0 failed)
cargo deny check               ✓
```

---

## Remaining Known Debt

| Area | Status |
|------|--------|
| `BTSP_NULL` cipher only | Phase 3 — awaiting BTSP provider session key propagation |
| PostgreSQL / RocksDB backends | v1.0.0 target |
| `rusqlite` C dep | Feature-gated, not default (`redb` default is pure Rust) |
| `bincode` v1 RUSTSEC | Migration to v2 is storage format breaking change |

---

## Self-Knowledge Compliance

**Zero hardcoded primal names in production code.** Remaining references in `#[cfg(test)]` blocks (5 in `manifest.rs` test data) are appropriate for test fixtures exercising the manifest parser.

The `primal_names.rs` module enforces the policy:

> LoamSpine follows the self-knowledge only philosophy: it knows its own
> identity and discovers other primals at runtime via capability-based
> discovery. No other primal names are hardcoded here.

---

*Previous handoffs archived in `handoffs/archive/LOAMSPINE_V0916_*`*
