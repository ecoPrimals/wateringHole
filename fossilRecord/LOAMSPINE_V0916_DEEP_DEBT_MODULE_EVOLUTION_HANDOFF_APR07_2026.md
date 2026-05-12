<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt Module Evolution

**Date**: April 7, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Type**: Deep Debt Evolution  

---

## Summary

Smart-refactored 6 large files into domain-focused module directories, migrated SQLite storage to `StorageResultExt`, extracted parse helpers, removed hardcoded vendor names, documented undocumented modules, and pushed 18 new tests across discovery cache, certificate loan paths, and tarpc server delegation.

---

## Changes

### 1. Smart module refactoring (6 files)

Files were split by **domain semantics**, not arbitrary line count. Each new directory has a `mod.rs` entry point that re-exports the public API unchanged.

| Original file | Crate | Lines | New directory modules |
|---|---|---|---|
| `types.rs` | loam-spine-api | 819 | `types/mod.rs`, `anchor.rs`, `certificate.rs`, `permanent_storage.rs`, `tests.rs` |
| `error.rs` | loam-spine-core | 777 | `error/mod.rs`, `ipc.rs`, `dispatch.rs`, `storage_ext.rs`, `tests.rs` |
| `neural_api.rs` | loam-spine-core | 735 | `neural_api/mod.rs`, `socket.rs`, `mcp.rs`, `tests.rs` |
| `infant_discovery/mod.rs` | loam-spine-core | — | Extracted `cache.rs` (`DiscoveryCache` struct) |
| `constants/network.rs` | loam-spine-core | — | Extracted `env_resolution.rs` (env-reading facades) |
| `sync/mod.rs` | loam-spine-core | — | Extracted `streaming.rs` (NDJSON progress) |

**Source files**: 136 → **148** (+12 new module files). All under 1000 lines.

### 2. SQLite `StorageResultExt` migration

The standalone `to_storage_err` function in `sqlite/common.rs` was removed. All 3 SQLite modules migrated:

- `sqlite/entry.rs` — `.storage_err()` / `.storage_ctx("entry insert")`
- `sqlite/certificate.rs` — `.storage_err()` / `.storage_ctx("certificate upsert")`
- `sqlite/spine.rs` — `.storage_err()` / `.storage_ctx("spine create")`
- `sqlite/common.rs` — `flush_wal()` and `count_rows()` updated

Consistent with the redb/sled `StorageResultExt` migration completed earlier.

### 3. Parse helper extraction (`integration_ops.rs`)

Duplicated UUID and hex parsing logic across 6 call sites extracted to:

```rust
fn parse_uuid(s: &str, field: &str) -> ApiResult<uuid::Uuid>
fn parse_content_hash(hex_str: &str, field: &str) -> ApiResult<ContentHash>
fn bytes_to_hex(bytes: &[u8; 32]) -> String
```

### 4. Hardcoding removal (`niche.rs`)

External dependency description changed from vendor-specific "Songbird/Consul/etcd for primal discovery" to generic "service registry (mDNS / DNS-SRV / etcd) for primal discovery (env vars as fallback)".

### 5. Deploy graph alignment

`graphs/loamspine_deploy.toml`:
- Version: 0.9.15 → **0.9.16**
- STATUS comment: `V0.9.15 (March 2026)` → `V0.9.16 (April 2026)`
- Added `anchor.publish`, `anchor.verify` to registered capabilities
- Updated description to mention public chain anchoring

### 6. Documentation

- `sqlite/common.rs`: Doc comments added to all 5 functions (`flush_wal`, `count_rows`, `check_table_exists`, `get_connection`, `ensure_tables`)
- `types/mod.rs`: `serde_opt_bytes` module and its `serialize`/`deserialize` functions documented

### 7. Coverage push (18 new tests)

| Domain | Tests | Description |
|---|---|---|
| `DiscoveryCache` | 8 | `new_is_empty`, `insert_and_get`, `get_fresh_missing_key`, `get_fresh_empty_vec`, `get_fresh_all_stale`, `clear`, `all_returns_snapshot`, `is_fresh` |
| `certificate_loan` expired paths | 5 | `auto_return_disabled`, `no_expiry`, `expired_success`, `chain_unwind`, `nonexistent_cert` |
| tarpc server | 5 | `config_default`, `config_clone_debug`, `custom_config`, `commit_session_via_rpc`, `commit_braid_via_rpc`, `get_certificate_not_found` |

### 8. Dependency audit

Verified `cc` crate does not appear in default build graph (`cargo tree -e normal` clean). Only enters via optional `sqlite` feature gate through `libsqlite3-sys`.

---

## Verification

```
cargo fmt --check          # clean
cargo clippy --all-targets # 0 warnings
cargo test                 # 1,298 tests, 0 failures
```

---

## Metrics

| Metric | Before | After |
|---|---|---|
| Tests | 1,280 | 1,298 |
| Source files | 136 | 148 |
| Clippy warnings | 0 | 0 |
| Max file size | 899 | ~900 |
| `to_storage_err` calls in SQLite | ~12 | 0 |
| Hardcoded vendor names in niche | 1 | 0 |
| Deploy graph version | 0.9.15 | 0.9.16 |

---

## Root docs updated

- `CHANGELOG.md` — Deep debt module evolution section added to 0.9.16
- `WHATS_NEXT.md` — New section, date bumped to April 7
- `STATUS.md` — Test count (1,298), file count (148), date bumped to April 7

---

## Impact

- **No API changes** — All public types, methods, and wire formats are unchanged
- **No behavioral changes** — Pure structural refactoring + coverage + docs
- **No dependency changes** — No new crates added or removed
- **Downstream**: None required. This is internal code organization only.

---

## Remaining debt (out of scope)

- **plasmidBin musl harvest**: Binary built in-repo; not yet harvested to `infra/plasmidBin/checksums.toml`
- **genomeBin version**: `wateringHole/genomeBin/manifest.toml` still shows `0.9.5` for loamSpine
- **`commit.session` naming**: Metadata still uses old form in `consumed_capabilities` — cosmetic only
