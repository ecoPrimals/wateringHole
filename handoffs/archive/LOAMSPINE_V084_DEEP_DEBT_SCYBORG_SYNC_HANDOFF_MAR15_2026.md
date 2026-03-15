<!-- SPDX-License-Identifier: AGPL-3.0-only -->

# LoamSpine v0.8.4 — Deep Debt, Scyborg License, Sync Protocol & Coverage

**Date**: March 15, 2026  
**From**: v0.8.3 → v0.8.4  
**Status**: Complete

---

## Summary

Deep debt evolution pass. Scyborg license schema implemented. SyncProtocol evolved from stub to real JSON-RPC/TCP sync engine. Protocol escalation (IpcProtocol negotiation). SQLite smart-refactored to modular directory. Zero-copy storage keys. CI cross-compilation for musl targets. 61 new tests with coverage boost to 86.47%.

---

## Changes

### Scyborg License Schema

- `SCYBORG_LICENSE_TYPE_URI`, `SCYBORG_LICENSE_SCHEMA_VERSION` constants
- `CertificateType::scyborg_license()` constructor, `is_scyborg_license()` predicate
- `CertificateMetadata::with_scyborg_license()` builder with `scyborg:spdx_expression`, `scyborg:content_category`, `scyborg:copyright_holder`, `scyborg:share_alike` metadata keys
- 5 tests covering schema, metadata, and full certificate creation

### Protocol Escalation

- `IpcProtocol` enum (`JsonRpc`, `Tarpc`) for protocol negotiation
- `resolve_primal_socket()` / `resolve_primal_tarpc_socket()` — socket path builders from primal/family ID
- `negotiate_protocol()` — prefers tarpc Unix socket (`.tarpc.sock`) if present, falls back to JSON-RPC (`.sock`)
- 5 tests for socket resolution and negotiation

### SyncProtocol Evolution

- `rpc_call()` — generic length-prefixed JSON-RPC over TCP
- `push_to_peer()` / `pull_from_peer()` — real network sync via `sync.push` / `sync.pull`
- `best_peer_endpoint()` — selects reachable peer by trying TCP connect
- Graceful fallback to local queueing on any network failure
- `connect_timeout` field on `SyncEngine`

### SQLite Smart Refactoring

- 990-line `sqlite.rs` → `sqlite/` directory:
  - `mod.rs` (104 lines): Module glue, re-exports, `SqliteStorage` struct
  - `common.rs` (38 lines): Shared helpers (`to_storage_err`, `lock_conn`, `flush_wal`, `count_rows`, `open_connection`)
  - `spine.rs` (155 lines): `SqliteSpineStorage`
  - `entry.rs` (185 lines): `SqliteEntryStorage`
  - `certificate.rs` (164 lines): `SqliteCertificateStorage`
  - `tests.rs` (293 lines): All SQLite tests
- Total: 939 lines (was 990)

### Zero-Copy Storage Keys

- `make_index_key` in redb and sled evolved from `Vec<u8>` heap allocation to `[u8; 24]` stack array
- Direct `copy_from_slice` into fixed buffer — no allocation, no drop

### CI Cross-Compilation

- New `cross-compile` job in `.github/workflows/ci.yml`
- `cross-rs/cross` for `x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`, `armv7-unknown-linux-musleabihf`
- Builds `loamspine-service` with default features per ecoBin musl requirement

### Test Coverage (+61 tests)

| Area | Tests Added | Coverage Before → After |
|------|-------------|-------------------------|
| Neural API (IPC) | 7+ | 57% → 88% |
| Transport (HTTP/RPC) | 10+ | 70% → 92% |
| Infant discovery | 10+ | 55% → 56.6% |
| Storage (redb) | 10+ | — |
| Storage (sled) | 10+ | — |
| Certificate (scyborg) | 5 | — |
| Network (protocol) | 5 | — |
| Sync | 4+ | — |

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --pedantic --nursery -D warnings` | PASS (0 errors) |
| `cargo doc --no-deps -D warnings` | PASS (0 warnings) |
| `cargo test --all-features` | PASS (870/870) |
| Max production file < 1000 | PASS (915 max) |
| `#![forbid(unsafe_code)]` | PASS |
| `cargo deny` | PASS |

---

## Metrics Delta

| Metric | v0.8.3 | v0.8.4 |
|--------|--------|--------|
| Tests | 809 | 870 |
| Line coverage | 84.52% | 86.47% |
| Max production file | 990 | 915 |
| Source files | 96 | 97 |
| Scyborg license | — | implemented |
| Protocol escalation | — | implemented |
| SyncProtocol | stub | real (JSON-RPC/TCP) |
| CI musl targets | — | x86_64, aarch64, armv7 |
| Storage key alloc | heap (`Vec<u8>`) | stack (`[u8; 24]`) |

---

## Ecosystem Impact

- **No breaking API changes** — all changes are additive or internal
- **Scyborg license** enables certificate-based licensing across ecosystem
- **Protocol escalation** allows primals to prefer tarpc when available
- **SyncProtocol** enables spine federation between peer instances
- **CI musl** validates ecoBin compliance with static linking
- **AGPL-3.0-only maintained** — SPDX headers on all 97 source files

---

## Remaining Gaps → v0.9.0

- Coverage: 86.47% → 90%+ (jsonrpc server loop 39%, main.rs 0%, DNS SRV/mDNS network paths)
- `storage/tests.rs` at 1122 lines — candidate for per-backend split
- Waypoint relending chain and expiry sweep
- Certificate provenance proof and escrow
- PrimalAdapter retry + circuit-breaker
- Showcase demos: ~10% complete (14+ scripts have inconsistent BINS_DIR paths)
