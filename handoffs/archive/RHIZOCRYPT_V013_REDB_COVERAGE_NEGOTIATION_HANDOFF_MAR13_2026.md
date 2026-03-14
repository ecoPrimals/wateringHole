<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — redb Default, 90% Coverage, Method Negotiation Handoff

**Date**: March 13, 2026
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Pure Rust evolution + coverage + client negotiation

---

## Summary

Four major evolutions completed:

1. **redb default storage** — Switched from `sled` (libc dep) to `redb` (100% Pure Rust)
   as the default storage backend. ecoBin fully compliant. Sled remains as optional feature.

2. **90% test coverage** — Expanded from 80.6% to 90.02% line coverage (llvm-cov).
   114 new tests across 14 modules. 600 total tests passing.

3. **Client method negotiation** — LoamSpine HTTP client dynamically negotiates
   native (`commit.session`) vs compatibility (`permanent-storage.commitSession`)
   method names. Cached via AtomicU8.

4. **Discovery registry evolution** — Live Songbird queries via HTTP/1.1 over TCP
   with `discovery.resolve` JSON-RPC, response parsing, capability conversion,
   and result caching.

---

## Changes

### Storage

| Item | Detail |
|------|--------|
| Default backend | `redb` (was `sled`) |
| Feature flag | `default = ["redb"]` |
| Sled status | Optional via `--features sled` |
| ecoBin | Fully compliant — zero C dependencies in default build |
| Tests | 26 redb-specific tests (CRUD, DAG, persistence, concurrency) |

### Coverage

| Metric | Before | After |
|--------|--------|-------|
| Line coverage | 80.60% | 90.02% |
| Total tests | 486 | 600 |
| Modules at 90%+ | 12 | 25 |

Key module improvements:

- `rpc/client.rs`: 0% → 81% (tarpc client serialization + error paths)
- `event.rs`: 68% → 100% (all EventType/SessionOutcome variants)
- `rhizocrypt.rs`: 80% → 92% (session ops, vertex ops, dehydration, slices)
- `rpc/jsonrpc/mod.rs`: 20% → 77% (Axum endpoint integration tests)
- `store_redb.rs`: 62% → 79% (diamond DAG, persistence, children index)

### Method Negotiation (LoamSpine Client)

- `call_negotiated()` tries native method name first
- On `-32601` (method not found), falls back to compatibility name
- Outcome cached in `AtomicU8` (Unknown → Native / Compat)
- `resolve_method()` returns cached preference for subsequent calls
- New `methods::native` and `methods::compat` constant modules

### Discovery

- `DiscoveryRegistry::discover()` performs live HTTP/1.1 TCP queries to Songbird
- `query_discovery_source()` sends `discovery.resolve` JSON-RPC request
- `parse_capability()` converts string names to `Capability` enum variants
- Results cached in `DashMap` for subsequent lookups

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-targets --features redb -- -D warnings` | Clean |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --features redb --lib` | 600 pass, 0 fail |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| Line coverage (llvm-cov) | 90.02% |
| Max file size | Under 1000 lines |

---

## Files Changed

### New Files
- `crates/rhizo-crypt-core/src/store_redb.rs` — redb DagStore implementation
- `crates/rhizo-crypt-core/src/discovery/` — Refactored discovery modules
- `crates/rhizo-crypt-rpc/src/jsonrpc/` — Refactored JSON-RPC modules
- `crates/rhizo-crypt-core/src/clients/adapters/unix_socket.rs` — Unix socket adapter
- `crates/rhizo-crypt-core/src/clients/songbird/{config,connection,discovery}.rs`

### Modified Files
- `Cargo.toml` — Added `redb = "2.4"` workspace dependency
- `crates/rhizo-crypt-core/Cargo.toml` — `default = ["redb"]`, redb feature gate
- `crates/rhizo-crypt-core/src/lib.rs` — Register and re-export store_redb
- `crates/rhizo-crypt-core/src/clients/loamspine_http.rs` — Method negotiation
- `crates/rhizo-crypt-core/src/discovery/registry.rs` — Live Songbird queries
- `crates/rhizo-crypt-rpc/src/jsonrpc/handler.rs` — 12 handler tests
- 14 additional files with expanded test coverage

---

## Known Issues

- Binary integration tests (`rhizocrypt-service/tests/binary_integration.rs`)
  fail when `CARGO_TARGET_DIR` is set to an external path. Pre-existing
  infrastructure issue, not related to current changes.

---

## Next Steps

- Wire redb backend into the service binary's `start()` method for persistent mode
- Evolve Songbird client from scaffolded to live TCP connection mode
- Expand property-based testing (proptest) for DAG operations
- Integrate sweetGrass provenance trait for RootPulse coordination
