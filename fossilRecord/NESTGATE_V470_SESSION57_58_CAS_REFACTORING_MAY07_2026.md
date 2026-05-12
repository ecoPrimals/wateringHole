# NestGate v4.7.0-dev Sessions 57-58 Handoff

**Date**: May 7, 2026
**Sessions**: 57, 58
**Trigger**: projectNUCLEUS sovereignty testing gaps (NG-1 through NG-4), deep debt sweep

---

## Summary

Session 57 implemented content-addressed storage and versioned manifests (NG-1
through NG-4) from the projectNUCLEUS sovereignty testing audit. Session 58
executed a deep debt sweep: module splitting, test extraction, and constants
consolidation to bring all production files under 800 lines.

---

## Session 57: Content-Addressed Storage (NG-1 through NG-4)

### NG-1 (High): `content.put` / `content.get` — Content-Addressed Storage

New handler module `content_handlers.rs` implements:

- `content.put` — accepts raw content (or base64 binary), computes BLAKE3 hash,
  stores with hash-as-key under `_content/{family_id}/`, returns the hash.
  Deduplicates on repeat stores. Supports encryption via existing BTSP channel.
- `content.get` — retrieves content by BLAKE3 hash; returns raw value or
  base64-encoded binary with metadata.
- `content.exists` — lightweight existence check by hash.
- `content.list` — enumerates stored content hashes with optional `prefix` filter.

Storage layout: `_content/{family_id}/{blake3_hex}` with `.meta.json` sidecar
files for metadata (size, content type, timestamps).

### NG-2 (Medium): `content.publish` / `content.promote` — Collection Manifests

- `content.publish` — creates a versioned manifest mapping URL paths to content
  hashes. Validates referential integrity (all referenced hashes must exist).
  Stores under `_manifests/{family_id}/{collection}/{version}.json`.
- `content.resolve` — resolves a path within a collection version to its content
  hash, then returns the content.
- `content.promote` — sets an alias (e.g., `latest`) pointing to a specific
  version. Enables atomic deployments and rollback.
- `content.collections` — lists all collections and their available versions.

### NG-3 (Medium): Blob Store Visibility

- `storage.list_blobs` — enumerates blob store contents (invisible to `storage.list`).
- `storage.blob_exists` — lightweight existence check for blob keys.
- Parameter naming differences documented in `capability_registry.toml`
  (`storage.store_blob` uses `blob`, `storage.fetch_external` uses `cache_key`).

### NG-4 (Low): Streaming Protocol Documentation

`capability_registry.toml` expanded with full wire protocol documentation for
`storage.store_stream` / `storage.retrieve_stream`: chunking envelope, session
lifecycle, 4 MiB max chunk size, offset/total_size semantics.

### New IPC Routes

63 total UDS methods (up from 53). New methods:

| Method | Domain |
|--------|--------|
| `content.put` | Content-addressed storage |
| `content.get` | Content-addressed storage |
| `content.exists` | Content-addressed storage |
| `content.list` | Content-addressed storage |
| `content.publish` | Manifest management |
| `content.resolve` | Manifest management |
| `content.promote` | Manifest management |
| `content.collections` | Manifest management |
| `storage.list_blobs` | Blob store visibility |
| `storage.blob_exists` | Blob store visibility |

---

## Session 58: Deep Debt Sweep — Module Refactoring

### Test Extraction (>800L files)

- `storage_handlers.rs` 836L → 345L: inline `#[cfg(test)]` extracted to
  `tests/storage_handler_tests.rs`
- `content_handlers.rs` 806L → 510L: inline `#[cfg(test)]` extracted to
  `tests/content_handler_tests.rs`
- Shared test setup consolidated in `tests/common.rs`

### Module Split

- `unix_socket_server/mod.rs` 720L → 395L: connection lifecycle logic extracted
  to `connection.rs` (335L) — `handle_connection`, `json_rpc_loop`,
  `dispatch_or_reject_unauth`, `post_handshake_phase3_or_plaintext`

### Constants Consolidation

- `network_hardcoded::ports` now re-exports from `runtime_fallback_ports`,
  establishing a single source of truth for port definitions
- Legacy `BEARDOG_*` env vars remain as documented backward-compatibility
  fallbacks, correctly prioritized below canonical names

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero warnings)
  -- -D warnings
cargo test --workspace --lib     8,879 passing / 0 failures / 60 ignored
cargo test --workspace           12,353 passing / 0 failures
```

---

## Debt Posture Post-S58

- **Files > 800L**: zero production `.rs` files
- **Unsafe code**: zero (`#![forbid(unsafe_code)]` on all crate roots)
- **TODO/FIXME/HACK**: zero in production `.rs`
- **Mocks in production**: zero (all test doubles behind `#[cfg(test)]`)
- **Clippy warnings**: zero (pedantic + nursery, `-D warnings`)
- **Deprecated markers**: zero
- **C-FFI deps**: zero in production

---

## Downstream Impact

- **projectNUCLEUS unblocked**: `content.put`/`content.get` enable native
  content-addressed publishing without client-side BLAKE3 workaround
- **Manifest system**: `content.publish`/`content.promote` enable atomic
  deployments with rollback for sporePrint and other static content
- **Blob visibility**: `storage.list_blobs`/`storage.blob_exists` close the
  namespace opacity gap between KV and blob stores
- **Module health**: all production files under 800L, test surface cleanly
  separated for maintainability
