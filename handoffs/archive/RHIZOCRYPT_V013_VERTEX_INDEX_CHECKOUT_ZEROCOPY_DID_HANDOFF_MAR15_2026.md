<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Vertex Index, CheckoutSlice Evolution, Zero-Copy DID

**Date**: March 15, 2026 (session 8)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Performance optimization + API evolution + zero-copy + debt elimination
**Supersedes**: `RHIZOCRYPT_V013_SCYBORG_LICENSE_ZEROCOPY_AUDIT_HANDOFF_MAR15_2026.md`

---

## Summary

Executed on all remaining debt items from the session 7 handoff. Added an O(1)
vertex-to-session index eliminating the O(N) session scan in `verify_proof`.
Evolved `checkout_slice` from placeholder values to real LoamSpine parameters.
Migrated `Did` from `String` to `Arc<str>` for zero-cost cloning across the
entire DAG engine. Cleaned root docs, archived cross-project audit doc to
wateringHole fossil record, updated test count to 907. All quality gates green.

---

## Changes

### O(1) Vertex-to-Session Index

| Aspect | Detail |
|--------|--------|
| Field | `vertex_session_index: Arc<DashMap<VertexId, SessionId>>` on `RhizoCrypt` |
| Populated | `append_vertex()` — inserts vertex→session mapping after DAG store write |
| Cleaned | `discard_session()` — retains only non-matching entries; `stop()` — clears all |
| Public API | `session_for_vertex(VertexId) -> Option<SessionId>` |
| RPC impact | `verify_proof` now O(1) instead of O(N) session scan |

### CheckoutSlice API Evolution

| Before (placeholder) | After (real parameters) |
|----------------------|------------------------|
| `spine_index: u64` | `spine_id: String`, `entry_hash: String` (hex), `entry_index: u64` |
| `lender: Option<Did>` | `owner: Did` (required) |
| `borrower: Option<Did>` | `holder: Did` (required) |
| `SessionId::now()` placeholder | `session_id: SessionId` (required) |
| `VertexId::ZERO` placeholder | `checkout_vertex: VertexId` (required) |
| `[0u8; 32]` placeholder hash | Hex-decoded from `entry_hash` with validation |
| — | `certificate_id: Option<String>` (new, from spine) |

Updated in: tarpc service trait, RPC server impl, JSON-RPC handler, tarpc
client, 5 handler tests, client serialization test, integration test.

### Zero-Copy DID (`Did` → `Arc<str>`)

| Before | After |
|--------|-------|
| `Did(pub String)` | `Did(Arc<str>)` with `#[serde(transparent)]` |
| `Did::default()` allocates per call | `LazyLock` static — allocated once |
| `.clone()` copies full string | `.clone()` increments refcount (O(1)) |

Impact: every `Session`, `Slice`, `AgentSummary`, and `Attestation` clone is now
cheaper. DIDs propagate through RPC, dehydration, and provenance without heap
allocation on clone.

### Additional Improvements

| File | Change |
|------|--------|
| `signing.rs` | Fixed broken intra-doc link (`[sign]` → `[Self::sign]`) |
| `jsonrpc/handler.rs` | Removed unnecessary intermediate `result` variable |
| `rhizocrypt-service/lib.rs` | Capability-based error message replacing `"no songbird"` |
| `beardog_http.rs` | Extracted `DEFAULT_KEY_TYPE` const; `sign()` returns `bytes::Bytes` |
| `nestgate_http.rs` | Extracted `DEFAULT_CONTENT_TYPE` const; `retrieve()` returns `bytes::Bytes` |
| `config.rs` | Uses `constants::LOCALHOST` instead of hardcoded `"127.0.0.1"` |
| `rhizocrypt.rs` | Eliminated redundant `clone()` and double `id()` in `append_vertex` |

### Documentation & Cleanup

| Action | Detail |
|--------|--------|
| README.md | Test count 882+ → 907+ |
| CHANGELOG.md | Added session 8 entry |
| audit-hardcoded-primal-refs.md | Moved from `rhizoCrypt/docs/` to `wateringHole/handoffs/archive/` as fossil record |
| wateringHole handoff | This document |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --no-deps -D warnings` | Clean |
| `cargo test --workspace` | 907 pass, 0 fail |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| SPDX headers | All 105 `.rs` files |
| Max file size | All under 1000 lines |
| Production `unwrap()`/`expect()` | Zero (all in `#[cfg(test)]`) |
| Production `TODO`/`FIXME`/`HACK` | Zero |

---

## Files Modified (rhizoCrypt)

```
crates/rhizo-crypt-core/src/rhizocrypt.rs         # vertex_session_index, session_for_vertex
crates/rhizo-crypt-core/src/types.rs               # Did → Arc<str>
crates/rhizo-crypt-core/src/config.rs              # constants::LOCALHOST
crates/rhizo-crypt-core/src/clients/beardog_http.rs    # DEFAULT_KEY_TYPE, Bytes return
crates/rhizo-crypt-core/src/clients/nestgate_http.rs   # DEFAULT_CONTENT_TYPE, Bytes return
crates/rhizo-crypt-core/src/clients/capabilities/signing.rs  # doc link fix
crates/rhizo-crypt-rpc/src/service.rs              # verify_proof O(1), CheckoutSliceRequest
crates/rhizo-crypt-rpc/src/jsonrpc/handler.rs      # checkout dispatch, idiomatic return
crates/rhizo-crypt-rpc/src/jsonrpc/handler_tests.rs    # all checkout tests
crates/rhizo-crypt-rpc/src/client.rs               # test imports, checkout serialization
crates/rhizo-crypt-rpc/tests/rpc_integration.rs    # checkout integration test
crates/rhizocrypt-service/src/lib.rs               # capability-based error message
README.md
CHANGELOG.md
```

## Files Modified (wateringHole)

```
handoffs/RHIZOCRYPT_V013_VERTEX_INDEX_CHECKOUT_ZEROCOPY_DID_HANDOFF_MAR15_2026.md  # this
handoffs/archive/AUDIT_HARDCODED_PRIMAL_REFS_MAR14_2026.md  # fossil record from rhizoCrypt
```

---

## Remaining Debt (documented, not urgent)

1. `collect_attestations` returns empty `Vec` — needs BearDog signing integration for real attestation collection
2. 5 tarpc transitive advisories in cargo-deny — waiting on upstream fixes
3. `SmallVec` evaluation for store key allocation — performance optimization candidate
4. LMDB storage backend — `StorageBackend::Lmdb` returns startup error; redb and sled cover all needs

---

## Items Resolved from Previous Handoff

| Previous "Next Step" | Resolution |
|---------------------|------------|
| Update 11 stale showcase scripts from deprecated `Session::new` API | Confirmed clean — no `Session::new` usage found |
| Add vertex-to-session index for O(1) `verify_proof` lookup | Implemented: `vertex_session_index` DashMap |
| Push test count back above 900 | 907 tests passing |
| Evaluate `SmallVec` for store key allocation | Deferred — not a bottleneck |
