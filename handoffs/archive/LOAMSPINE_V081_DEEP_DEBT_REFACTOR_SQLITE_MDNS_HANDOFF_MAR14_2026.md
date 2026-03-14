<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine v0.8.1 — Deep Debt, Refactoring, SQLite & mDNS Handoff

**Date**: March 14, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.0 → 0.8.1
**Type**: Deep debt audit, large file refactoring, new storage backend, mDNS evolution

---

## Summary

Comprehensive codebase audit against wateringHole standards followed by
multi-wave remediation. All quality gates green: 700 tests passing, 0 clippy
warnings (all targets, all features, `-D warnings`), zero unsafe, all files
under 1000 lines (max 810, down from 949). New SQLite storage backend
(feature-gated). mDNS stub evolved to real implementation. Three large files
refactored into module directories. Error types evolved from `Box<dyn Error>`
to typed enums. Zero-copy evolution begun with `Cow<'static, str>`.

---

## What Changed

### Error Type Evolution
- `bin/loamspine-service/main.rs`: `Box<dyn Error>` → `anyhow::Result<()>`
- `tarpc_server.rs`: `Box<dyn Error + Send + Sync>` → `ServerError`
- `jsonrpc/mod.rs`: Same — `Box<dyn Error + Send + Sync>` → `ServerError`
- New `ServerError` enum in `loam-spine-api/src/error.rs` with `Bind` and
  `Transport` variants

### Large File Refactoring
| Before | After (mod.rs + tests.rs) |
|--------|---------------------------|
| `entry.rs` (949 lines) | `entry/mod.rs` (464) + `entry/tests.rs` (488) |
| `discovery_client.rs` (912) | `discovery_client/mod.rs` (435) + `discovery_client/tests.rs` (478) |
| `infant_discovery.rs` (831) | `infant_discovery/mod.rs` (685) + `infant_discovery/tests.rs` (258) |

### SQLite Storage Backend (new)
- `crates/loam-spine-core/src/storage/sqlite.rs` (457 lines)
- `SqliteSpineStorage`, `SqliteEntryStorage`, `SqliteStorage`
- Feature-gated: `--features sqlite`
- Uses `rusqlite` with `bundled` (not ecoBin — documented)
- JSON serialization, proper schema with indexes
- Safe integer conversions (`i64::try_from`)

### Real mDNS Discovery
- Replaced `mdns_query_stub` with real `mdns` crate v3.0 integration
- `tokio::task::spawn_blocking` for async compatibility
- Parses SRV/A records from mDNS responses
- Added `futures-util` and `async-std` as optional deps for mdns feature

### Zero-Copy Evolution
- `bind_address()` → `Cow<'static, str>` (avoids allocation for static defaults)

### Documentation
- **STATUS.md** (new): Implementation status per spec area
- **WHATS_NEXT.md** (new): Roadmap (v0.9.0, v1.0.0, long-term)
- **CHANGELOG.md**: v0.8.1 entry added
- **KNOWN_ISSUES.md**: Updated to reflect resolved items
- **README.md**: Accurate source file count (88), max file size (810)
- Showcase scripts fixed: wrong example names, outdated metrics

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Version | 0.8.0 | 0.8.1 |
| Tests | 700 | 700 (maintained) |
| Source files | 80 | 88 (+8 from refactoring + sqlite) |
| Max file size | 949 | 810 |
| Clippy warnings | 0 | 0 |
| Unsafe code | 0 | 0 |
| C deps (default) | 0 | 0 |
| Storage backends | 2 (memory, sled) | 3 (+sqlite, feature-gated) |
| mDNS | stub | real implementation |
| Error types | Box<dyn Error> | typed (ServerError, anyhow) |
| SPDX headers | 84/84 | 88/88 |

---

## Inter-Primal Notes

### biomeOS
- NeuralAPI integration unchanged. 19 capabilities registered at startup.
- Socket path follows XDG standard.

### rhizoCrypt
- `permanent-storage.*` compat layer unchanged.
- `trio_types` bridge unchanged.

### sweetGrass
- `braid.commit` unchanged.

---

## Known Remaining Items

1. **Coverage**: 90%+ claimed but not re-measured with llvm-cov this session
   (build cache issue prevented instrumented builds). Should re-verify.
2. **Broader Cow adoption**: Only `bind_address()` evolved. Documented in
   WHATS_NEXT.md for v0.9.0.
3. **PostgreSQL/RocksDB**: Spec'd but not implemented. Deferred to v1.0.0.
4. **Showcase demos**: ~10% complete; scripts fixed but demos need real
   implementations.

---

## Files Changed

Key files (not exhaustive):
- `Cargo.toml` (workspace — unchanged)
- `bin/loamspine-service/Cargo.toml` (added anyhow)
- `bin/loamspine-service/main.rs` (anyhow, Cow)
- `crates/loam-spine-core/Cargo.toml` (rusqlite, futures-util, async-std)
- `crates/loam-spine-core/src/entry/` (new directory)
- `crates/loam-spine-core/src/discovery_client/` (new directory)
- `crates/loam-spine-core/src/infant_discovery/` (new directory)
- `crates/loam-spine-core/src/storage/sqlite.rs` (new)
- `crates/loam-spine-core/src/storage/mod.rs` (sqlite feature gate)
- `crates/loam-spine-core/src/constants/network.rs` (Cow)
- `crates/loam-spine-api/src/error.rs` (ServerError)
- `crates/loam-spine-api/src/tarpc_server.rs` (ServerError)
- `crates/loam-spine-api/src/jsonrpc/mod.rs` (ServerError)
- `crates/loam-spine-api/src/lib.rs` (re-export ServerError)
- `README.md`, `CHANGELOG.md`, `STATUS.md`, `WHATS_NEXT.md`
- `docs/planning/KNOWN_ISSUES.md`
- `showcase/` (5 files with fixed example names and metrics)
