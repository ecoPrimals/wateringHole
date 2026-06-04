# rhizoCrypt — Wave 76c: MeshEventListener + IPC Trigger Path

**Date**: Jun 4, 2026
**Version**: 0.14.1
**Gate**: strandGate
**FRAGO**: wave76-parity-sprint-provenance (continued)

## Summary

Designed and implemented the IPC trigger path for wiring bearDog w137
`auth.trust_issuer` events to rhizoCrypt DAG recording. New
`MeshEventListener` module scaffolds the inbound event path — the
inverse of the existing outbound `ProvenanceNotifier`.

## IPC Trigger Path

```
bearDog (auth.trust_issuer fires)
  → rhizoCrypt MeshEventListener (discovers via Capability::Signing)
  → MeshTrustEvent wire DTO deserialized
  → MeshTrustEvent::into_event_type() maps to EventType::TrustIssuerRegistered
  → DAG session append (internal API, no RPC loopback)
```

## Schema Additions

- `MeshEventListener` — lifecycle: discover → connect (startup) → record_event
- `MeshTrustEvent` — wire DTO with `MeshTrustEventKind` discriminator
- `MeshTrustEventKind` — 5 variants mapping 1:1 to `EventType` mesh domain
- `RhizoCrypt.mesh_listener` field, created in `new()`, connected in `start()`
- Re-exports from `lib.rs`: `MeshEventListener`, `MeshTrustEvent`, `MeshTrustEventKind`

## Deep Debt: Clippy Guard Migration

- Migrated 29 test files from `#![allow(clippy::unwrap_used)]` to `#![expect(clippy::unwrap_used, reason = "test code")]`
- Removed unfulfilled `#![expect]` guards (files using only `expect()`, not `unwrap()`)
- Added guards to `dehydration_wire.rs` and `integration/mocks.rs::capability_mock_tests`
- Zero unfulfilled-expect warnings with `cargo clippy --tests`

## Test Results

- **1,681 tests passing** (all features), 0 failures
- **0 clippy warnings** (including `--tests`)
- **184 `.rs` files**, ~55,408 lines
- **Max production file**: 693 lines (within 700L limit)
- **Zero unsafe**, zero TODO/FIXME

## Files Changed (rhizoCrypt)

- `crates/rhizo-crypt-core/src/types_ecosystem/mesh/mod.rs` (NEW)
- `crates/rhizo-crypt-core/src/types_ecosystem/mesh/types.rs` (NEW)
- `crates/rhizo-crypt-core/src/types_ecosystem/mesh/listener.rs` (NEW)
- `crates/rhizo-crypt-core/src/types_ecosystem/mod.rs`
- `crates/rhizo-crypt-core/src/rhizocrypt/mod.rs`
- `crates/rhizo-crypt-core/src/lib.rs`
- 29 test files (clippy guard migration)
- `CHANGELOG.md`, `README.md`, `CONTEXT.md`
- `sporeprint/validation-summary.md`, `docs/DEPLOYMENT_CHECKLIST.md`
- `specs/00_SPECIFICATIONS_INDEX.md`

## Next Steps (Upstream Gaps)

1. **bearDog w137**: Needs `auth.events.subscribe` or `ipc.watch` on signing
   endpoint for rhizoCrypt to auto-subscribe. Until then, events can be
   injected via `record_event()` from RPC handler layer.
2. **Songbird**: When bearDog advertises `crypto:events` capability,
   `SongbirdClient::populate_registry()` should map it.
3. **Mesh session provisioning**: Dedicated mesh-trust session auto-creation
   on first event (or config-driven `RHIZOCRYPT_MESH_SESSION_ID`).

## Integration Status

| Component | Status |
|-----------|--------|
| Event types (Wave 76) | Delivered, tested |
| Wire DTOs | Delivered, roundtrip tested |
| MeshEventListener scaffold | Delivered, 11 tests |
| bearDog IPC subscription | Waiting on bearDog w137 |
| Mesh session auto-provision | Designed, not implemented |
| Clippy guard consistency | Complete (zero unfulfilled) |
