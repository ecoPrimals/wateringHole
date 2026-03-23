# sweetGrass v0.7.22 Handoff — Sovereignty: Inline Wire Types

**Date**: March 17, 2026  
**From**: sweetGrass  
**To**: rhizoCrypt, loamSpine, primalSpring, biomeOS  
**Status**: Released

---

## Summary

sweetGrass v0.7.22 removes the `provenance-trio-types` shared crate dependency
entirely. Each primal now owns its own wire types. Communication between trio
partners is via JSON-RPC only — no compile-time coupling.

This resolves the issue raised by primalSpring on March 22, 2026 regarding
`cargo check` failures when `phase2/provenance-trio-types/` is absent.

---

## What Changed

### Removed
- `provenance-trio-types` from workspace `Cargo.toml`, `sweet-grass-core/Cargo.toml`, `sweet-grass-service/Cargo.toml`
- `WireDehydrationSummary` re-export and ~80 lines of `From` impls in `dehydration.rs`
- Intermediate wire-type deserialization step in `handle_record_dehydration`

### Added
- `PipelineRequest`, `PipelineResult`, `AgentContribution` structs inline in `contribution.rs`
- `provenance-trio-types` banned in `deny.toml` to prevent re-introduction
- `#[serde(default)]` on `SessionOperation.timestamp` and `Attestation.attested_at`

### Changed
- `handle_record_dehydration` now deserializes directly into `DehydrationSummary`
- Module docs in `dehydration.rs` reflect JSON-RPC wire contract, not shared crate

---

## Wire Compatibility

**No wire-level changes.** The JSON payloads accepted and produced by sweetGrass
are identical. Unknown fields from partner primals are silently ignored by serde.
Omitted optional fields default gracefully.

The `contribution.record_dehydration` method still accepts the same JSON schema
that rhizoCrypt produces. The `pipeline.attribute` method still returns the same
schema that biomeOS graphs consume.

---

## For primalSpring

sweetGrass no longer depends on `provenance-trio-types`. You can:
- Remove the shared crate from your build graphs
- Continue routing via `capability.call` as before
- sweetGrass, loamSpine, and rhizoCrypt communicate via JSON-RPC only

---

## For rhizoCrypt and loamSpine

If you also inline your types (recommended per sovereignty standard), the
`provenance-trio-types` crate can be archived. Each primal owns its own
serialization contract for the wire format.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,077 passing |
| Clippy | 0 warnings (pedantic + nursery) |
| Cross-primal deps | 0 |
| Unsafe blocks | 0 |
| Max file size | <600 LOC |
| deny.toml guards | gRPC, protobuf, openssl, ring, reqwest, provenance-trio-types |

---

## Registry Updates

- `PRIMAL_REGISTRY.md`: sweetGrass entry updated to v0.7.22
- `genomeBin/manifest.toml`: sweetGrass latest updated to 0.7.22
