# rhizoCrypt v0.14.0-dev — S38 Deep Debt + Module Refactor Handoff

**Date**: April 13, 2026
**Session**: 38
**Focus**: Deep debt cleanup, module refactoring, doc evolution, re-export narrowing

---

## Changes

### 1. JSON-RPC Handler Domain Extraction

`handler.rs` (583 lines monolith) refactored into `handler/` module tree:

| Module | Responsibility | Lines |
|--------|---------------|-------|
| `mod.rs` | `HandlerError`, `handle_request` dispatch, module wiring | 102 |
| `params.rs` | Shared JSON parameter extraction helpers | 127 |
| `vertex.rs` | Vertex, frontier, genesis, query, children dispatch | 81 |
| `slice.rs` | Slice checkout and lifecycle dispatch | 78 |
| `events.rs` | Event append and batch dispatch | 71 |
| `session.rs` | Session CRUD dispatch | 60 |
| `merkle.rs` | Merkle root, proof, verify dispatch | 54 |
| `capabilities.rs` | Capability list and identity dispatch | 49 |
| `tools.rs` | MCP-style tool list and invocation dispatch | 48 |
| `dehydration.rs` | Dehydration trigger and status dispatch | 30 |
| `health.rs` | Health, readiness, metrics dispatch | 24 |

### 2. Metrics Module Extraction

`metrics.rs` (530 lines) split into cohesive modules:

| Module | Responsibility | Lines |
|--------|---------------|-------|
| `metrics.rs` | `MetricsCollector`, `RpcMethod`, `ErrorType`, `SharedMetrics`, `RequestTimer` | 319 |
| `histogram.rs` | `Histogram`, `HistogramSnapshot`, `LATENCY_BUCKETS` | 117 |
| `prometheus.rs` | `export_prometheus`, `ALL_METHODS`, `ALL_ERROR_TYPES` | 113 |

### 3. Re-export Narrowing

- Removed `pub use rhizo_crypt_core;` and `pub use rhizo_crypt_rpc;` from `rhizocrypt-service` — nobody used the broad crate re-exports

### 4. Hardcoded Primal Name Evolution

Production doc comments evolved from vendor-specific to capability-generic:
- `provenance/client.rs`: Generic provider language
- `niche.rs`: "ecosystem attribution patterns" replaces "sweetGrass"
- `config.rs`: Same pattern
- `safe_env/mod.rs`: `examplePeer`/`exampleSigner` replace primal names in doc examples
- `dehydration_wire.rs`: Generic provider language
- `integration/mod.rs`: "peer services" replaces "sibling primals"

### 5. Clone Reduction

- `register_with_discovery` now takes `&str` instead of `String` (avoids allocation at call site)
- Audit confirmed remaining `.clone()` calls are Arc-wrapped (cheap ref count) or architecturally required (DashMap, DTOs)

---

## Code Health

| Check | Result |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy -D warnings` | 0 warnings (all features, all targets) |
| `cargo doc -D warnings` | Clean |
| `cargo test --all-features` | 1,510 passing, 0 failures |
| SPDX headers | All 160 `.rs` files |
| Unsafe blocks | 0 |
| Max file size | 664 lines (production), limit 1000 |

## Remaining Debt Assessment

### Already Clean
- No `todo!()`, `unimplemented!()`, or `unreachable!()` macros
- No `TODO`/`FIXME`/`HACK` comment markers
- No `unsafe` blocks anywhere
- No `unwrap()`/`expect()` in non-test production code
- Mocks properly gated behind `#[cfg(any(test, feature = "test-utils"))]`
- Metrics cast suppressions well-documented and justified (guarded by predicates)

### Tracked Low-Priority Items
- `loamspine_http.rs` (664 lines): JSON-RPC wire types could extract, but file is cohesive
- Remaining 500+ line production files are domain-cohesive (store, event, rhizocrypt, niche)
- `Box<dyn ProtocolAdapter>` intentional type erasure for runtime adapter selection
- `constants.rs` (516 lines) contains centralized configuration — structure is intentional
