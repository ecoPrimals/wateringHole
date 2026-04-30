# NestGate v4.7.0-dev Session 50 Handoff

**Date**: April 30, 2026
**Session**: 50
**Trigger**: primalSpring Phase 56c audit — streaming/fetch_external gaps

---

## Summary

Resolved three NestGate items from the Phase 56c stadial convergence audit:

1. **Streaming storage discovery gap** (the real blocker behind "springs can't stream big data back")
2. **`storage.fetch_external` dispatch gap** in semantic router and isomorphic adapter
3. **Protocol documentation** for downstream spring integration

---

## What Changed

### 1. Streaming Methods Now Discoverable

**Problem**: NestGate fully implements chunked streaming storage (`store_stream`, `store_stream_chunk`, `retrieve_stream`, `retrieve_stream_chunk`) with 4 MiB chunks, session management, and 1-hour TTL — but `capability_registry.toml` did not advertise these methods. Springs trusting only the registry concluded NestGate "can't stream."

**Fix**: Added all four streaming methods to `capability_registry.toml` methods list and added inline protocol documentation (chunk flow, sizes, TTL).

### 2. `storage.fetch_external` Wired Across All Transports

**Problem**: `storage.fetch_external` was implemented on the unix_socket_server dispatch path but:
- Not wired in the `SemanticRouter::call_method` — fell through to "unknown method"
- Not dispatched in the isomorphic unix adapter — advertised in `capabilities.list` but returned -32601

**Fix**:
- Added `storage.fetch_external` arm to `semantic_router/mod.rs` delegating to the existing `external_handlers::storage_fetch_external`
- Added `handle_storage_fetch_external` to `unix_adapter_handlers.rs` and wired it in the isomorphic adapter dispatch
- Made `external_handlers` module `pub(crate)` for cross-module access

### 3. Protocol Documentation

- `capability_registry.toml`: Inline streaming protocol description (4-step flow)
- `transport/README.md`: Full method inventory including streaming and fetch_external; emoji purged
- `QUICK_START_BIOMEOS.md`: Streaming upload/download examples with JSON-RPC request/response pairs; `storage.fetch_external` documented with cross-spring data pipeline use case
- `CAPABILITY_MAPPINGS.md`: Method list updated to include streaming methods

---

## Verification

```
cargo check --workspace              PASS
cargo clippy --workspace -- -D warnings   PASS (zero warnings)
cargo fmt --check                    PASS
cargo test --workspace --lib         8,841 passed, 0 failed, 60 ignored
```

---

## Cross-Spring Context

The Phase 56c audit cited "springs can't stream big data back" as medium priority. Investigation revealed:

- The streaming protocol is fully functional (two-phase: begin session, then loop chunks)
- `storage.retrieve` handles up to 64 MiB single-response; beyond that, streaming is required
- The blocker was **discovery**: springs querying `capability_registry.toml` or the semantic router could not find streaming methods
- With this fix, springs calling `capabilities.list` or reading the registry will see all streaming endpoints

**Cross-spring persistent storage IPC**: NestGate provides namespace isolation with a `shared` default namespace. Multiple springs in the same family share data by convention (same filesystem path). True cross-spring RPC routing is a biomeOS composition concern, not a NestGate concern.

---

## Files Modified

- `capability_registry.toml` — streaming methods + protocol docs
- `code/crates/nestgate-rpc/src/rpc/semantic_router/mod.rs` — fetch_external dispatch
- `code/crates/nestgate-rpc/src/rpc/semantic_router/storage.rs` — fetch_external handler
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/mod.rs` — external_handlers visibility
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/external_handlers.rs` — pub visibility
- `code/crates/nestgate-rpc/src/rpc/isomorphic_ipc/unix_adapter/mod.rs` — fetch_external arm
- `code/crates/nestgate-rpc/src/rpc/isomorphic_ipc/unix_adapter/unix_adapter_handlers.rs` — handler
- `code/crates/nestgate-api/src/transport/README.md` — full rewrite (emoji purge + streaming docs)
- `docs/integration/biomeos/QUICK_START_BIOMEOS.md` — streaming + fetch_external examples
- `CAPABILITY_MAPPINGS.md` — method list update
- Root docs (STATUS.md, README.md, etc.) — Session 50, April 30, 2026
