<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine v0.8.2 — Pure Rust Evolution (redb, pure JSON-RPC, ureq)

**Date**: March 14, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.2 (in-place evolution, no version bump)
**Type**: Dependency evolution, ecoBin compliance, pure Rust sovereignty

---

## Summary

Eliminated all C/C++/assembly dependencies from LoamSpine's default feature set.
Three major dependency evolutions: (1) `sled` demoted to optional, `redb` installed
as default pure-Rust embedded database; (2) `jsonrpsee` fully removed, replaced with
hand-rolled pure JSON-RPC 2.0 server; (3) `reqwest` replaced with `ureq` for HTTP
discovery. `ring` is now explicitly banned in `deny.toml`. All quality gates green:
739 tests, 0 clippy/doc warnings, ecoBin compliant.

---

## What Changed

### redb Default Storage Backend
- New `RedbStorage` (pure Rust embedded DB) with `RedbSpineStorage`,
  `RedbEntryStorage`, `RedbCertificateStorage` implementations
- Pattern follows rhizoCrypt's established redb usage
- `redb-storage` is now the default feature
- `sled` demoted to optional `sled-storage` feature (still compiles, still tested)
- `primal-capabilities.toml` and advertisement metadata updated

### jsonrpsee → Pure JSON-RPC 2.0
- `jsonrpsee` crate completely removed from `loam-spine-api/Cargo.toml`
- Hand-rolled JSON-RPC 2.0 server using `tokio::net::TcpListener`
- Handles both raw newline-delimited JSON and HTTP POST
- `macro_rules! rpc` dispatcher avoids async lifetime complications
- Custom `ServerHandle` with `stop()`/`stopped()` for graceful shutdown
- All tests rewritten against `LoamSpineJsonRpc::handle_request` directly

### reqwest → ureq
- `reqwest` removed (transitive `ring` dependency)
- `ureq` added with `default-features = false` (pure Rust, no TLS, no ring)
- Blocking `ureq` calls wrapped in `tokio::task::spawn_blocking`
- HTTPS routes through BearDog/Songbird TLS stack (not ureq)

### ring Banned
- `deny.toml` updated: `ring` crate explicitly denied
- Zero C/assembly dependencies in default feature set
- Full ecoBin compliance achieved

### Documentation Sweep
- `README.md`: test count, storage backends, badges
- `STATUS.md`: pure JSON-RPC, redb default, v0.8.2+ section
- `WHATS_NEXT.md`: completed items for redb/jsonrpc/ureq evolution
- `primal-capabilities.toml`: storage_backend → redb
- `deny.toml`: ring banned, jsonrpsee comment removed
- All 7 specs updated (ARCHITECTURE, PURE_RUST_RPC, API_SPECIFICATION,
  LOAMSPINE_SPECIFICATION, STORAGE_BACKENDS, SERVICE_LIFECYCLE, INDEX)
- All showcase docs updated (version, dates, storage references)
- discovery_client advertisement metadata: sled → redb

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 744 | 739 (-5 stale integration stubs removed) |
| Source files | 92+ | 93+ (+1 redb.rs) |
| Max file size | 422 | 422 |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe code | 0 | 0 |
| C deps (default) | 0 (but ring transitive) | 0 (ring eliminated) |
| ecoBin | partial (ring via jsonrpsee/reqwest) | **compliant** |

---

## Inter-Primal Notes

### biomeOS
- NeuralAPI integration unchanged. 19 capabilities registered at startup.
- `MetricsCollector` already uses redb — no changes needed.

### rhizoCrypt
- `permanent-storage.*` compat layer unchanged.
- rhizoCrypt established the redb pattern that LoamSpine now follows.

### sweetGrass
- `braid.commit` unchanged.
- sweetGrass also migrated to redb (v0.7.4+).

### BearDog / Songbird
- HTTPS discovery routes through BearDog/Songbird TLS stack.
- ureq handles plain HTTP only; no in-primal TLS needed.

---

## Dependency Evolution Map

| Removed | Replaced With | Reason |
|---------|---------------|--------|
| `jsonrpsee` | hand-rolled pure JSON-RPC | `ring` transitive dep (C/asm) |
| `reqwest` | `ureq` (no default features) | `ring` transitive dep (C/asm) |
| `sled` (default) | `redb` (default) | `libc` dep; redb is pure Rust |
| `ring` (transitive) | — (banned in deny.toml) | C/assembly, violates ecoBin |

---

## Known Remaining Items

1. **Sled/SQLite CertificateStorage**: Only in-memory and redb impls exist.
2. **Waypoint relending**: `SliceTerms.allow_relend` defined but not implemented.
3. **SyncProtocol**: Federation stub, intentional — future phase.
4. **Showcase demos**: ~10% complete.
5. **Test count delta**: 5 tests removed during migration (stale jsonrpsee/reqwest stubs).

---

## Files Changed

Key files (not exhaustive):
- `crates/loam-spine-core/Cargo.toml` (sled optional, redb default, ureq replaces reqwest)
- `crates/loam-spine-core/src/storage/redb.rs` (new — full redb storage backend)
- `crates/loam-spine-core/src/storage/mod.rs` (feature gates, StorageBackend::Redb default)
- `crates/loam-spine-core/src/transport/http.rs` (rewritten — ureq replacing reqwest)
- `crates/loam-spine-core/src/transport/mod.rs` (doc updates)
- `crates/loam-spine-core/src/discovery_client/mod.rs` (sled → redb metadata)
- `crates/loam-spine-api/Cargo.toml` (jsonrpsee removed)
- `crates/loam-spine-api/src/jsonrpc/mod.rs` (rewritten — pure JSON-RPC server)
- `crates/loam-spine-api/src/jsonrpc/tests.rs` (rewritten against handle_request)
- `crates/loam-spine-api/src/lib.rs` (new re-exports)
- `crates/loam-spine-api/tests/provenance_trio.rs` (updated for pure JSON-RPC)
- `bin/loamspine-service/main.rs` (mut handle for ServerHandle)
- `README.md`, `STATUS.md`, `WHATS_NEXT.md`, `CHANGELOG.md`
- `primal-capabilities.toml`, `deny.toml`
- `specs/` (7 files updated)
- `showcase/` (12+ files updated)
