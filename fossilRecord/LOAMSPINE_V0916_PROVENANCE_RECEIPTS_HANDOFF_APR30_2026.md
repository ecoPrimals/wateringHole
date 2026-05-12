# loamSpine v0.9.16 — Self-Contained Provenance Receipts

**Date**: April 30, 2026
**From**: loamSpine v0.9.16
**Responding to**: primalSpring Phase 56c — "Provenance chain for guideStone receipts"

---

## What Changed

### Self-Contained Provenance Receipts (IMPLEMENTED)

`CommitSessionResponse` is now a complete provenance receipt. Downstream
consumers (guideStone, composition scripts) can trace DAG-to-ledger
computation provenance from the response alone without follow-up entry fetches.

**Fields added** (alongside existing `spine_id`, `commit_hash`, `index`, `committed_at`):

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `Uuid` | Session that was committed |
| `merkle_root` | `ContentHash` | Merkle root of the session DAG |
| `vertex_count` | `u64` | Number of vertices in the session |
| `committer` | `Did` | DID of the committer |
| `tower_signature` | `Option<String>` | Base64 Ed25519 signature (when `BEARDOG_SOCKET` is set) |

**Verification pattern**: Given a `CommitSessionResponse`, a downstream
consumer can:
1. Verify the entry exists at `(spine_id, commit_hash, index)`
2. Verify the DAG binding: `session_id` + `merkle_root` match the committed entry
3. Verify the signature: strip `tower_signature`/`tower_signature_alg` from
   entry metadata, recompute canonical bytes, verify against `tower_signature`

### Provenance Chain Extended

`get_provenance_chain(content_hash)` now matches `SessionCommit` entries on
`merkle_root` with relationship `"committed-from"`. Previously only `DataAnchor`
and `BraidCommit` entries were matched. The three relationships are:

- `"anchored-by"` — `DataAnchor` entry references this content hash
- `"attributed-to"` — `BraidCommit` entry references this content hash
- `"committed-from"` — `SessionCommit` entry has this merkle root

### Deep Debt Audit (CLEAN)

10-dimension audit performed same session:

| Dimension | Result |
|-----------|--------|
| TODOs/FIXMEs/HACKs | None |
| Unsafe | `#![forbid(unsafe_code)]` all crates |
| Mocks in production | None (properly gated) |
| println/dbg! in prod | None |
| unwrap/expect in prod | None |
| Large files (>800L) | None (max 783L) |
| `#[allow]` | 4, all justified with reasons |
| Hardcoded primal names | **Fixed** — 2 `"biomeos"` literals → `BIOMEOS_SOCKET_DIR` constant |
| cargo deny/clippy/fmt | All clean |
| External native deps | None (blake3 pure, ring/openssl banned) |

---

## Correction to Phase 56c

The Phase 56c blurb states:

> "loamSpine — Provenance chain for guideStone receipts: DAG signing can't
> trace computation provenance yet."

**Correction**: `CommitSessionResponse` is now a self-contained provenance
receipt with session binding + Tower signature. `get_provenance_chain()`
matches `SessionCommit` entries. This gap is **resolved**.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,509 (all concurrent, zero flaky) |
| Max .rs file | 783L (test), 605L (production) |
| Clippy | Clean (pedantic + nursery) |
| cargo deny | Clean |
| Unsafe | Forbidden |

---

*Ref: `LOAMSPINE_V0916_TOWER_SIGNING_DEEP_DEBT_HANDOFF_APR28_2026.md` for Tower signing context*
