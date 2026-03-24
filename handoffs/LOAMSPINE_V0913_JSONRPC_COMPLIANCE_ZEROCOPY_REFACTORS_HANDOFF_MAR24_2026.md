<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# LoamSpine v0.9.13 — JSON-RPC 2.0 Compliance, Zero-Copy & Smart Refactors

**Date**: March 24, 2026  
**From**: LoamSpine  
**To**: All Springs, All Primals, biomeOS  
**Status**: Complete, ready for push

---

## Summary

LoamSpine v0.9.13 executes on P1/P2 audit findings: strict JSON-RPC 2.0
spec compliance, zero-copy deserialization evolution, idiomatic API ergonomics,
and smart file refactoring to maintain headroom under the 1000-line limit.

1. **JSON-RPC 2.0 spec compliance** — `process_request` rewritten to validate
   `"jsonrpc": "2.0"` on every request (single and batch), suppress responses
   for notifications (missing/null `id`), and return correct error codes
   (`INVALID_REQUEST` for empty batch and version mismatch).

2. **Serialization safety** — All `unwrap_or_default()` on response
   serialization replaced with `serialize_response()` helper that logs via
   `tracing::error!` and returns a hard-coded JSON-RPC internal error fallback.

3. **Zero-copy Signature deserialization** — Custom `ByteBufferVisitor`
   eliminates `Vec<u8>` intermediary for binary formats (bincode/postcard)
   via `visit_byte_buf`. JSON path unchanged.

4. **Idiomatic API evolution** — `JsonRpcResponse::error()` and
   `TimeMarker::branch()`/`tag()` accept `impl Into<String>`, eliminating
   redundant `.to_string()` allocations at call sites.

5. **Smart file refactors** — `spine.rs` 854 → **438** lines,
   `waypoint.rs` 815 → **511** lines via test extraction to dedicated
   `*_tests.rs` / `*_proptests.rs` files. Production code cohesion preserved.

---

## Code Changes

| File | Change |
|------|--------|
| `crates/loam-spine-api/src/jsonrpc/mod.rs` | JSON-RPC 2.0 validation, notification suppression, `serialize_response()`, `impl Into<String>` |
| `crates/loam-spine-core/src/types.rs` | `ByteBufferVisitor` for zero-copy Signature deserialization |
| `crates/loam-spine-core/src/temporal/time_marker.rs` | `impl Into<String>` for `branch()`/`tag()` parameters |
| `crates/loam-spine-core/src/spine.rs` | Tests extracted to `spine_tests.rs` + `spine_proptests.rs` |
| `crates/loam-spine-core/src/waypoint.rs` | Tests extracted to `waypoint_tests.rs` |
| `crates/loam-spine-api/src/jsonrpc/tests.rs` | Updated empty batch test for `-32600` error code |

---

## Metrics

| Metric | v0.9.12 | v0.9.13 |
|--------|---------|---------|
| Tests | 1,312 | **1,312** |
| Clippy | 0 | 0 |
| Doc warnings | 0 | 0 |
| Max file | 954 | 954 |
| Source files | 124 | **130** (+6 test extractions) |
| Unsafe | 0 (`forbid`) | 0 (`forbid`) |

---

## What Other Primals Should Know

- **JSON-RPC 2.0 compliance is now strict**: Requests with invalid/missing
  `jsonrpc: "2.0"` return `INVALID_REQUEST` (-32600). Notifications (no `id`)
  receive no response. HTTP notifications return `204 No Content`.

- **`ByteBufferVisitor` pattern** for zero-copy serde deserialization is
  available for absorption. Binary codec paths avoid `Vec<u8>` intermediary.

- **`impl Into<String>` on constructors** is the idiomatic Rust pattern for
  APIs that accept both `&str` and `String` without forcing callers to allocate.

---

## Patterns Available for Absorption

| Pattern | Where | What |
|---------|-------|------|
| `serialize_response()` fallback | `jsonrpc/mod.rs` | Never silently drop serialization errors |
| `is_notification()` check | `jsonrpc/mod.rs` | Proper JSON-RPC 2.0 notification detection |
| `ByteBufferVisitor` | `types.rs` | Zero-copy serde visitor for `bytes::Bytes` |
| `impl Into<String>` on constructors | `time_marker.rs`, `jsonrpc/mod.rs` | Ergonomic API parameters |
| Test extraction via `#[path]` | `spine.rs`, `waypoint.rs` | Smart refactoring without losing cohesion |

---

## Verification

All checks pass:
- `cargo fmt --check` — clean
- `cargo clippy --all-targets --all-features -- -D warnings` — 0 warnings
- `cargo doc --no-deps` — 0 warnings
- `cargo test --all-features` — 1,312 tests passing
