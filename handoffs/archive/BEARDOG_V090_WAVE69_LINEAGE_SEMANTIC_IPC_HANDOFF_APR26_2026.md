<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 69: Lineage Semantic IPC Methods

> April 26, 2026

## Summary

Resolved primalSpring audit "Ionic Contract Signing + Lineage" (April 26, 2026). Added `lineage.list`, `lineage.verify`, and `lineage.get` semantic IPC methods for verifiable lineage queries. Confirmed `crypto.sign_contract` was already fully wired through `IonicBondHandler`.

## Changes

### New IPC methods (CryptoHandler → genetic route)

| Method | Wire format | Backing |
|--------|------------|---------|
| `lineage.list` | `→ {} ← { chains: [LineageChainSummary], count }` | `BirdSongManager::list_lineage_chains()` |
| `lineage.verify` | Same params as `genetic.verify_lineage` | Delegates to `handle_verify_lineage` (Blake3 simple + chain Merkle) |
| `lineage.get` | `→ { chain_id } ← LineageChain \| { error: "chain_not_found" }` | `BirdSongManager::get_lineage_chain()` |

### New types

- `LineageChainSummary` — `beardog-genetics::birdsong::lineage_chain` — summary struct for chain listing (chain_id, root_node_id, node_count, generation, created_at)

### `crypto.sign_contract` — confirmed wired

Already routed via `IonicBondHandler` with full lifecycle (propose → accept → seal). Registered in capabilities with cost metrics. No changes needed.

## Files modified

| File | Change |
|------|--------|
| `crates/beardog-genetics/src/birdsong/lineage_chain.rs` | Added `LineageChainSummary`, `list_chains()` |
| `crates/beardog-genetics/src/birdsong/manager.rs` | Added `list_lineage_chains()` |
| `crates/beardog-genetics/src/birdsong/mod.rs` | Export `LineageChainSummary` |
| `crates/beardog-tunnel/.../crypto_handler/genetic.rs` | Added `lineage.list`, `lineage.verify`, `lineage.get` routes + 3 tests |
| `crates/beardog-tunnel/.../crypto_handler/method_list.rs` | Registered 3 methods (96 → 99) |
| `crates/beardog-tunnel/.../handlers/capabilities.rs` | Added `lineage` capability block + cost metrics |
| `crates/beardog-tunnel/.../handlers/crypto_handler_tests.rs` | Updated method count 96 → 99 |
| `CHANGELOG.md`, `STATUS.md` | Updated |

## Quality

- **Clippy**: 0 warnings (pedantic + nursery)
- **Format**: clean
- **Tests**: 3 new (lineage_list_returns_empty_chains, lineage_verify_delegates_to_genetic, lineage_get_missing_chain) — all pass
- **Method count**: 99 CryptoHandler methods + 9 IonicBondHandler methods

## Downstream impact

- **skunkBat**: `lineage.list` + `lineage.verify` now available for thymic selection
- **primalSpring**: Both audit items resolved — `crypto.sign_contract` confirmed, lineage methods implemented
- **Multi-gate federation**: `lineage.get` enables full chain retrieval for cross-tower verification
