<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Public Chain Anchor Handoff

**Date**: April 6, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Closes**: Gap 4 from `WETSPRING_SCIENCE_NUCLEUS_GAPS_HANDOFF_APR06_2026.md`

---

## Summary

LoamSpine now supports **public chain anchoring** — recording receipts from
external append-only ledgers (blockchains, data commons, federated spines)
to enable external verification of provenance braids.

Key design decision: LoamSpine **only records the receipt**. The actual chain
submission is performed by a capability-discovered `"chain-anchor"` primal.
This follows the ecoPrimals philosophy of self-knowledge only.

---

## What Was Implemented

### 1. New Entry Type: `PublicChainAnchor`

Added to `EntryType` enum in `crates/loam-spine-core/src/entry/mod.rs`:

- `anchor_target: AnchorTarget` — which external system was used
- `state_hash: ContentHash` — Blake3 hash of the spine's tip at anchor time
- `tx_ref: String` — transaction hash or proof reference on external system
- `block_height: u64` — block height or sequence number (0 if N/A)
- `anchor_timestamp: Timestamp` — when the anchor was confirmed

### 2. `AnchorTarget` Enum (chain-agnostic)

```
Bitcoin | Ethereum | FederatedSpine { peer_id } | DataCommons { commons_id } | Other { name }
```

`#[non_exhaustive]` for forward compatibility.

### 3. Service Methods

In `crates/loam-spine-core/src/service/anchor.rs`:

- `anchor_to_public_chain(spine_id, anchor_target, tx_ref, block_height, anchor_timestamp)` → `AnchorReceipt`
- `verify_anchor(spine_id, anchor_entry_hash?)` → `AnchorVerification`

### 4. JSON-RPC + tarpc Methods

- `anchor.publish` — Record a public chain anchor on a spine
- `anchor.verify` — Verify a spine's state against a recorded anchor

Both wired through `crates/loam-spine-api/src/jsonrpc/mod.rs` (dispatch),
`crates/loam-spine-api/src/service/anchor_ops.rs` (RPC service layer),
`crates/loam-spine-api/src/tarpc_server.rs` (tarpc implementation),
and `crates/loam-spine-api/src/rpc.rs` (tarpc trait).

### 5. Capability Advertisement

- **Provided**: `"public-anchoring"` added to `capabilities::identifiers::loamspine`
- **Consumed**: `"chain-anchor"` added to `capabilities::identifiers::external`
- Updated: `ADVERTISED` set, `LoamSpineCapability::PublicAnchoring` variant, niche self-knowledge, neural API CAPABILITIES, MCP tools, cost estimates

### 6. Spec Updated

`specs/LOAMSPINE_SPECIFICATION.md` Section 2.5 updated from "Optional" to "Implemented".

---

## What Is NOT Included (Deferred)

| Item | Owner | Notes |
|------|-------|-------|
| Chain submitter primal | TBD | Separate `"chain-anchor"` primal for BTC/ETH/etc. |
| Automatic periodic anchoring | loamSpine | Future background task (like `ExpirySweeper`) |
| Radiating attribution calculator | sunCloud + sweetGrass | Gap 7 from same handoff |
| Cross-spring data exchange | RootPulse | Gap 3 from same handoff |

---

## wetSpring Linkage

wetSpring's Tier 3 `verify_url` can now link to loamSpine's `anchor.verify`
JSON-RPC method. The flow:

1. A `"chain-anchor"` primal submits a spine state hash to an external ledger
2. It returns `tx_ref` and `block_height` to the caller
3. Caller (or chain-anchor primal) calls `anchor.publish` on loamSpine
4. wetSpring's `verify_url` points to `anchor.verify` for external parties

---

## Tests

10 new tests covering:

- Entry serde roundtrip (`PublicChainAnchor`)
- Domain classification (`"anchor"`)
- Waypoint exclusion (not allowed in waypoint spines)
- Service method roundtrip (publish + verify)
- Verify latest anchor resolution
- Missing spine error
- Non-anchor entry error
- `AnchorTarget` serde roundtrip (all 5 variants)
- JSON-RPC dispatch: `anchor.publish`
- JSON-RPC dispatch: `anchor.verify` (latest)

**Total tests**: 1,280 (was 1,270)

---

## Verification

```
cargo fmt --all -- --check     # PASS
cargo clippy --workspace -- -D warnings   # PASS (0 warnings)
cargo test --workspace         # PASS (1,280 tests, 0 failures)
cargo doc --workspace --no-deps           # PASS (0 warnings)
```
