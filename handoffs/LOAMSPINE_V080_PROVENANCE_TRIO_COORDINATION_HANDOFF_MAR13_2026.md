# LoamSpine v0.8.0 — Provenance Trio Coordination Handoff

**Date**: March 13, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.0
**Focus**: Cross-primal coordination with rhizoCrypt + sweetGrass

---

## Summary

LoamSpine now accepts commits from both provenance trio primals via their native wire formats:

- **rhizoCrypt** → `permanent-storage.commitSession` (JSON-RPC compat layer, auto-spine creation)
- **sweetGrass** → `braid.commit` (native JSON-RPC, attribution anchoring with inclusion proofs)

This completes the permanence side of the trio coordination. All flows are tested end-to-end with 10 provenance trio integration tests.

---

## What Changed

### permanent-storage.* Compatibility Layer

rhizoCrypt's `LoamSpineHttpClient` calls `permanent-storage.commitSession` with its own request format (hex-encoded merkle root, `RpcDehydrationSummary` subset, optional committer DID). LoamSpine now translates this wire format to native types internally:

| rhizoCrypt sends | loamSpine translates to |
|---|---|
| `session_id: String` (UUID) | `session_id: Uuid` |
| `merkle_root: String` (hex 64 chars) | `session_hash: [u8; 32]` |
| `summary.vertex_count: u64` | `vertex_count: u64` |
| `committer_did: Option<String>` | `committer: Did` |
| *(no spine_id)* | Auto-resolved via `ensure_spine()` |

Additional compat methods:
- `permanent-storage.verifyCommit` — verify an entry exists by spine_id + hex entry_hash
- `permanent-storage.getCommit` — retrieve an entry by spine_id + hex entry_hash
- `permanent-storage.healthCheck` — always returns `true` when service is running

### Auto-Spine Resolution

When rhizoCrypt commits via the compat layer without a `spine_id`, loamSpine auto-creates (or reuses) a permanence spine for that committer DID. This is idempotent — same DID always maps to the same spine.

### Braid Anchoring

sweetGrass's `braid.commit` was already wired but is now validated with integration tests including:
- Braid entry type verification (`EntryType::BraidCommit`)
- Inclusion proof generation and verification
- Full trio flow (session commit + braid anchor on same spine)

---

## Test Coverage

| Test | Flow |
|---|---|
| `dehydration_flow_native_session_commit` | rhizoCrypt → loamSpine (native API) |
| `dehydration_flow_permanent_storage_compat` | rhizoCrypt → loamSpine (compat wire format) |
| `dehydration_flow_compat_auto_creates_spine` | Auto-spine creation + idempotency |
| `dehydration_flow_compat_invalid_hex_rejected` | Error: bad merkle root hex |
| `dehydration_flow_compat_invalid_session_id_rejected` | Error: bad session UUID |
| `braid_anchoring_flow` | sweetGrass → loamSpine (braid commit + entry verify) |
| `braid_anchoring_with_proof` | sweetGrass → loamSpine + inclusion proof |
| `full_provenance_trio_flow` | rhizoCrypt + sweetGrass → loamSpine (both on same spine, both provable) |
| `provenance_trio_via_compat_layer` | Full trio via compat layer + braid on auto-created spine |
| `permanent_storage_health_check` | Compat health endpoint |

---

## Metrics

| Metric | Before | After |
|---|---|---|
| Tests | 510+ | 549 |
| Provenance trio tests | 0 | 10 |
| JSON-RPC methods | 18 | 22 (+4 compat) |
| Clippy warnings | 0 | 0 |
| Unsafe code | 0 | 0 |

---

## Type Translation Notes for rhizoCrypt + sweetGrass

### rhizoCrypt → loamSpine

| Type | rhizoCrypt | loamSpine |
|---|---|---|
| Session ID | `String` (UUID text) | `uuid::Uuid` |
| Content Hash | `String` (hex) | `[u8; 32]` (Blake3) |
| DID | `String` | `Did(String)` |
| Spine ID | Not sent in initial commit | Auto-resolved per committer |

### sweetGrass → loamSpine

| Type | sweetGrass | loamSpine |
|---|---|---|
| Braid ID | `BraidId(Arc<str>)` (URN) | `uuid::Uuid` |
| Content Hash | `String` ("sha256:...") | `[u8; 32]` (Blake3) |
| DID | `Did(Arc<str>)` | `Did(String)` |

These translations happen at the client side (sweetGrass/rhizoCrypt are responsible for converting their types to loamSpine's wire format).

---

## Remaining Coordination Gaps

1. **rhizoCrypt → `permanent-storage.commitSession` method name alignment**: rhizoCrypt currently calls `permanent-storage.commitSession`. LoamSpine now accepts both this and `session.commit`. When rhizoCrypt upgrades, it can switch to `session.commit` and drop the compat prefix.

2. **sweetGrass BraidId → UUID**: sweetGrass uses URN-format BraidId (`urn:braid:uuid:...`). The client needs to extract the UUID portion when calling loamSpine's `braid.commit`. This is a sweetGrass-side concern.

3. **Neural API pathway learning**: The `neuralAPI` whitepaper describes adaptive orchestration that could learn optimal dehydration-to-permanence routes. This is not yet implemented in biomeOS.

4. **RootPulse niche activation**: biomeOS has the `rootpulse-niche.yaml` manifest but the commit DAG graph executor is not yet wired for live use.

---

## Inter-Primal Notes

- **biomeOS**: Can begin wiring the dehydration flow as a NUCLEUS atomic (rhizoCrypt `session.dehydrate` → loamSpine `session.commit`). The `permanent-storage.*` compat layer means existing rhizoCrypt code works as-is.
- **ludoSpring**: Game sessions that flow through rhizoCrypt can now be permanently committed to loamSpine with attribution braids from sweetGrass. The full game → dehydration → permanence → attribution pipeline is now testable.
- **rhizoCrypt**: No changes needed to call loamSpine. Existing `LoamSpineHttpClient` calling `permanent-storage.commitSession` will work. Future: migrate to `session.commit` for cleaner naming.
- **sweetGrass**: Needs to implement `BraidId → Uuid` extraction and `ContentHash → [u8; 32]` conversion in its loamSpine anchoring client. The `AnchoringClient` trait already has the right shape.

---

**Handoff by**: LoamSpine deep audit + provenance trio coordination session
