# NestGate v4.7.0-dev — Session 43l Handoff

**Date**: April 13, 2026
**Session**: 43l — Streaming storage parity: all 3 methods wired in both server paths
**Triggered by**: primalSpring downstream audit (claims 3 streaming methods "not yet wired")

---

## primalSpring Audit Triage

The audit claimed: "3 streaming storage methods declared in our graphs but not yet wired:
`storage.retrieve_range`, `storage.object.size`, `storage.namespaces.list`."

**This is mostly stale.** Triage:

| Method | Isomorphic Adapter (production) | Legacy `JsonRpcUnixServer` | Resolution |
|--------|-------------------------------|---------------------------|------------|
| `storage.retrieve_range` | **WIRED** (Session 43h) — handler + 5 tests | **WIRED** (Session 43h) — handler + 4 tests | Already fully resolved |
| `storage.object.size` | **WIRED** (Session 43h) — handler + 2 tests | **WIRED** (Session 43h) — handler + 3 tests | Already fully resolved |
| `storage.namespaces.list` | **WIRED** (Session 43h) — handler + 2 tests | **MISSING** — parity gap | **FIXED** (Session 43l) |

Production daemon (`nestgate-bin/commands/service.rs`) uses the **isomorphic IPC adapter**,
so all 3 methods were already available in production. The legacy `JsonRpcUnixServer` path
(still exported, used by integration tests and potentially downstream callers) was missing
only `storage.namespaces.list`.

### Items for primalSpring to update in PRIMAL_GAPS.md

Line 329 "Remaining" column should remove streaming storage reference. All 3 methods are
fully wired, tested, and dispatched:

```
| **NestGate** | ... | ... | Remaining: coverage 80→90%, 187 deprecated APIs (canonical-config migration markers) |
```

The streaming methods are NOT gaps — they are working and tested since Session 43h.

---

## What Was Fixed

### `storage.namespaces.list` — legacy server parity

- Added `storage_namespaces_list` handler in `unix_socket_server/storage_handlers.rs`
  (same logic as isomorphic adapter handler: enumerate subdirectories under
  `{base}/datasets/{family_id}/`, exclude underscore-prefixed internals, sort)
- Wired dispatch in `unix_socket_server/mod.rs` match arm
- Added 3 tests:
  - `namespaces_list_returns_dirs_only` — creates dirs, verifies `_blobs` filtered out
  - `namespaces_list_empty_for_missing_family` — graceful empty result
  - `namespaces_list_uses_state_family_id` — falls back to server state when params omitted

---

## Verification

- **Build**: `cargo check --workspace` PASS
- **Clippy**: `cargo clippy --workspace --all-targets --all-features -- -D warnings` PASS (0 warnings)
- **Tests**: 11,819 passing (+3), 0 failures, 451 ignored
- **Crosscheck**: `cargo test --test capability_registry_crosscheck` — 11/11 PASS

---

## Streaming Storage Method Summary

All 5 Session 43h streaming methods now wired in **both** server paths:

| Method | Description | Both paths |
|--------|-------------|-----------|
| `storage.store_blob` | Store binary blob (base64 over JSON-RPC) | YES |
| `storage.retrieve_blob` | Retrieve full blob | YES |
| `storage.retrieve_range` | Byte-range read (offset+length, 4 MiB chunks) | YES |
| `storage.object.size` | Blob metadata (total size) | YES |
| `storage.namespaces.list` | Enumerate namespaces under family | YES (Session 43l) |
