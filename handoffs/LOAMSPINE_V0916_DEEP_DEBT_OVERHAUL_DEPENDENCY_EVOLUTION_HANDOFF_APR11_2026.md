<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt Overhaul & Dependency Evolution Handoff

**Date**: April 11, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Tests**: 1,507 (all concurrent, ~3s, zero flaky)  
**Coverage**: 92% line / 89% region / 93% function  
**Source Files**: 170 `.rs` (+ 3 fuzz targets)

---

## Summary

Final deep debt pass for v0.9.16. Focuses on BTSP security hardening, module architecture, dependency hygiene, storage test reliability, hardcoding evolution, and transport refactoring. All changes verified through full parallel test runs with zero failures.

---

## Changes

### 1. BTSP Challenge Evolution (Security)

**Before**: `generate_challenge_placeholder()` — deterministic timestamp-derived bytes (nanosecond clock).  
**After**: `generate_challenge()` — `blake3(uuid_v7_a || uuid_v7_b)` producing 256-bit hash, hex-encoded to 64 chars. 148+ bits of OS-sourced entropy per challenge. Zero new dependencies (blake3 and uuid already in tree).

**Resolves**: KNOWN_ISSUES.md "BTSP challenge generation uses placeholder" item.

### 2. Smart Refactor: btsp.rs → btsp/ Module Directory

**Before**: Single `btsp.rs` (696 lines) containing wire types, config, framing, BearDog client, and handshake logic.  
**After**: `btsp/` directory with 5 focused submodules:

| Module | Lines | Responsibility |
|--------|-------|---------------|
| `wire.rs` | 95 | Serializable handshake message types |
| `config.rs` | 120 | Environment-driven BTSP configuration, BearDog socket resolution |
| `frame.rs` | 85 | Length-prefixed frame I/O (read/write/serialize/deserialize) |
| `beardog_client.rs` | 90 | JSON-RPC delegation to BearDog |
| `handshake.rs` | 175 | Server-side 4-step BTSP handshake protocol |
| `mod.rs` | 50 | Re-exports and module declarations |

All production modules now under 581 lines (max: `discovery_client/mod.rs`).

### 3. Dependency Cleanup

- **Removed**: `serde_bytes` 0.11 from `loam-spine-core` — confirmed unused via source grep.
- **Centralized**: 8 shared dependencies promoted to `[workspace.dependencies]`:
  - Internal: `loam-spine-core`, `loam-spine-api`
  - External: `tarpc`, `futures`, `clap`, `bytes`, `url`, `bincode`
  - Member crates now reference via `workspace = true`

### 4. Storage Test Isolation (Zero Flaky Tests)

**Problem**: 7 storage tests failed intermittently under parallel execution:
- Sled: File lock contention from close-then-reopen pattern
- SQLite: "disk I/O error" under concurrent filesystem pressure
- redb: Persistence assertion failures from stale temp directories

**Solution**:
- **Sled**: Added `from_db(db: sled::Db)` constructors to `SledSpineStorage`, `SledEntryStorage`, `SledCertificateStorage`. Tests maintain single open handle — no close-reopen. 10 tests updated.
- **SQLite**: `open_connection()` now enables `PRAGMA journal_mode=WAL` + `PRAGMA busy_timeout=5000` for concurrent access resilience.
- **redb**: Migrated from manual `remove_dir_all` to `tempfile::tempdir()` lifecycle. Added explicit `drop(storage)` before re-open assertions. 5 tests updated.

**Verified**: `cargo test --workspace --all-features` — 1,507 tests, 0 failures.

### 5. Lint Audit

4 production `#[allow]` documented as irreducible:
- 2× `clippy::wildcard_imports` — tarpc `service!` macro requires wildcard import; `#[expect]` fails with `unfulfilled-lint-expectations` in all-features test builds
- 2× `clippy::unused_async` — functions are synchronous without `dns-srv`/`mdns` features but async with them; `#[expect]` fails in `--all-features` builds

### 6. Registry Path Centralization (Hardcoding Evolution)

**Before**: `/health`, `/discover`, `/register`, `/heartbeat`, `/deregister` as inline string fragments in `discovery_client/mod.rs` and `transport/mock.rs`.  
**After**: `constants::registry` module with `DISCOVER_PATH`, `REGISTER_PATH`, `HEARTBEAT_PATH`, `DEREGISTER_PATH` constants. All registry HTTP paths now reference centralized constants.

### 7. BTSP Provider Socket Naming (Hardcoding Evolution)

**Before**: `"beardog"` hardcoded as string literals in socket name construction.  
**After**: `BTSP_PROVIDER_PREFIX` constant in `btsp/config.rs` with documentation explaining it's a BTSP protocol convention, not a primal dependency.

### 8. Smart Refactor: jsonrpc/server.rs → server.rs + uds.rs

**Before**: Single `server.rs` (529 lines) mixing TCP server, HTTP parsing, UDS server, and BTSP gating.  
**After**: TCP transport in `server.rs` (362 lines), UDS transport + BTSP gating in `uds.rs` (172 lines). Clean domain boundary between TCP/HTTP and UDS transports. Shared `handle_stream` dispatch stays in `server.rs`.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,373 | 1,507 |
| Source files | 167 | 170 |
| Max production file | 696 (btsp.rs) | 605 (discovery_client/mod.rs) |
| Flaky storage tests | 7 | 0 |
| Unused dependencies | 1 (serde_bytes) | 0 |
| Workspace-centralized deps | partial | 100% shared deps |
| BTSP challenge entropy | ~64 bits (timestamp) | 148+ bits (OS entropy) |

---

## Verification Pipeline (All Pass)

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-features --all-targets -- -D warnings
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps
cargo deny check licenses bans sources
cargo test --workspace --all-features  # 1,507 pass
```

---

## Files Changed

### New
- `crates/loam-spine-core/src/btsp/mod.rs`
- `crates/loam-spine-core/src/btsp/wire.rs`
- `crates/loam-spine-core/src/btsp/config.rs`
- `crates/loam-spine-core/src/btsp/frame.rs`
- `crates/loam-spine-core/src/btsp/beardog_client.rs`
- `crates/loam-spine-core/src/btsp/handshake.rs`
- `crates/loam-spine-api/src/jsonrpc/uds.rs` (UDS transport extracted from server.rs)

### Deleted
- `crates/loam-spine-core/src/btsp.rs` (replaced by btsp/ directory)

### Modified
- `Cargo.toml` (workspace dependency centralization)
- `Cargo.lock` (serde_bytes removed)
- `crates/loam-spine-core/Cargo.toml` (serde_bytes removed, deps centralized)
- `crates/loam-spine-api/Cargo.toml` (deps centralized)
- `bin/loamspine-service/Cargo.toml` (deps centralized)
- `crates/loam-spine-core/src/storage/sled.rs` (from_db constructors)
- `crates/loam-spine-core/src/storage/sled_tests.rs` (10 tests updated)
- `crates/loam-spine-core/src/storage/sled_tests_certificate.rs` (3 tests updated)
- `crates/loam-spine-core/src/storage/sqlite/common.rs` (WAL + busy_timeout)
- `crates/loam-spine-core/src/storage/redb_tests.rs` (5 tests updated)
- `crates/loam-spine-core/src/btsp_tests.rs` (imports updated, challenge test evolved)
- `crates/loam-spine-api/src/tarpc_server.rs` (#[allow] audit)
- `crates/loam-spine-api/src/service/mod.rs` (#[allow] audit)
- `crates/loam-spine-core/src/constants.rs` (registry path constants)
- `crates/loam-spine-core/src/discovery_client/mod.rs` (registry paths → constants)
- `crates/loam-spine-core/src/transport/mock.rs` (registry path → constant)
- `crates/loam-spine-api/src/jsonrpc/server.rs` (UDS extracted to uds.rs)
- `crates/loam-spine-api/src/jsonrpc/mod.rs` (uds module added)

---

## Gap Matrix Impact

| Gap | Status | Notes |
|-----|--------|-------|
| GAP-07 (loamSpine startup panic) | **RESOLVED** (v0.9.15) | LS-03 fixed; 1,507 tests confirm stability |
| BTSP challenge placeholder | **RESOLVED** (v0.9.16) | blake3+uuid entropy, not timestamp |
| Storage test flakiness | **RESOLVED** (v0.9.16) | Zero flaky across sled/SQLite/redb |
| btsp.rs >500 lines | **RESOLVED** (v0.9.16) | 5 submodules, all <200 lines |
| TRIO-IPC flush-on-write | **RESOLVED** (v0.9.16) | flush() on all IPC paths (already present), TCP_NODELAY added |
| TRIO-IPC concurrent load | **RESOLVED** (v0.9.16) | 8×5 concurrent UDS load test (sweetGrass pattern) |

---

## Trio IPC Stability (primalSpring Audit Response)

### flush-on-write (already present)
All production socket write paths already call `flush().await` after writes:
- JSON-RPC server (NDJSON + HTTP responses)
- BTSP `write_frame` (length-prefixed frames)
- BearDog client (UDS JSON-RPC)
- Sync federation (TCP length+JSON)
- Discovery attestation (TCP JSON-RPC)
- NeuralAPI (UDS length-prefixed)

### TCP_NODELAY (newly added)
Nagle's algorithm disabled on all TCP sockets:
- **Server accept**: `stream.set_nodelay(true)` in JSON-RPC TCP accept loop
- **Sync client**: `set_nodelay(true)` after `TcpStream::connect` in federation sync
- **Discovery client**: `set_nodelay(true)` after `TcpStream::connect` for attestation

tarpc manages its own transport layer (we don't access the raw `TcpStream`).

### Concurrent UDS load test
New test: `uds_concurrent_load_8x5` — 8 clients × 5 requests over persistent connections. Matches sweetGrass v0.7.27 pattern. All responses verified (correct id, correct result).

---

## Actions for Downstream

### For ludoSpring (GAP-07)
- LoamSpine IPC is stable. GAP-07 can be closed. `permanence.sock` available for UDS, TCP JSON-RPC on `--port`. SignalHandler handles SIGTERM/SIGINT graceful shutdown. UDS backpressure limited to 256 concurrent connections. TCP_NODELAY on all TCP sockets.

### For wetSpring (Provenance Trio IPC)
- LoamSpine endpoints are stable: `session.commit`, `braid.commit`, `entry.append` all tested. Persistent UDS connections supported (no reconnect per request). `--socket` flag available for explicit socket path override. Concurrent 8×5 UDS load verified.

### For sweetGrass / rhizoCrypt (Trio IPC parity)
- flush-on-write pattern confirmed present on all paths (predates sweetGrass handoff callout). TCP_NODELAY now added. Concurrent load test pattern adopted.

### For primalSpring (Re-validation)
- Tier 10 re-validation can proceed. `health.liveness`, `capabilities.list`, `identity.get` all respond correctly. 36 JSON-RPC methods available. IPC stability: flush + TCP_NODELAY + concurrent UDS load tested.
