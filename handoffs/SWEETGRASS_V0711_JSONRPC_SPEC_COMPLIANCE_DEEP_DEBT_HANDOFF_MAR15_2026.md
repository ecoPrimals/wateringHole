# SweetGrass v0.7.11 — JSON-RPC 2.0 Spec Compliance + Deep Debt + Coverage Push

**Date**: March 15, 2026
**From**: v0.7.10 → v0.7.11
**Status**: Complete — all checks pass
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0710_TYPED_ERRORS_LINT_HARDENING_HANDOFF_MAR15_2026.md`

---

## Summary

Full JSON-RPC 2.0 specification compliance: batch requests (Section 6) and
notifications (Section 4.1). Hardcoded magic strings extracted to named identity
constants. Property-based testing with proptest. Significant coverage push across
health, memory store, and capability handlers. Smart test refactoring to maintain
the 1000-line-per-file limit.

---

## JSON-RPC 2.0 Batch Request Support (Spec Section 6)

`handle_jsonrpc` now accepts both single JSON objects and JSON arrays:

```rust
// Before: Only single requests
pub async fn handle_jsonrpc(State(store): ..., body: String) -> impl IntoResponse

// After: Single, batch, and notification-aware
pub async fn handle_jsonrpc(State(store): ..., body: String) -> Response
```

Batch semantics:
- Array of requests → array of responses (only non-notification results included)
- Empty array → `Invalid Request` error (`-32600`)
- All-notification batch → `204 No Content`
- Mixed batch → array of responses for non-notifications only

**Inter-primal pattern**: All primals implementing JSON-RPC 2.0 should support
batch requests per Section 6. Parse the top-level JSON value first to determine
single vs. batch, then delegate to `process_single` for each element.

---

## JSON-RPC 2.0 Notification Support (Spec Section 4.1)

A notification is a request without an `id` field. The server MUST NOT reply.

```rust
fn process_single(raw: &serde_json::Value, store: &...) -> Option<JsonRpcResponse>
```

The `Option` return type encodes the spec: `None` = notification (no response).

Critically, `id: null` is NOT a notification — it is a valid request with a null ID.
Detection uses raw JSON inspection before deserialization:

```rust
let is_notification = raw.as_object().is_some_and(|obj| !obj.contains_key("id"));
```

**Inter-primal pattern**: Never use `Option<Value>` deserialization to detect
notifications — `serde_json` cannot distinguish missing `id` from `id: null`.
Inspect the raw JSON object for key presence.

---

## Hardcoded Constants Extracted

All magic strings extracted to `sweet_grass_core::identity`:

| Constant | Value | Was hardcoded in |
|----------|-------|------------------|
| `UNKNOWN_AGENT_DID` | `"did:key:unknown"` | `contribution.rs` |
| `MIME_MERKLE_ROOT` | `"application/x-merkle-root"` | `contribution.rs` |
| `MIME_OCTET_STREAM` | `"application/octet-stream"` | `contribution.rs` |
| `DEFAULT_STORAGE_BACKEND` | `"memory"` | `factory/mod.rs` |

Store crates also gained `DEFAULT_DB_PATH` constants:

| Crate | Constant | Value |
|-------|----------|-------|
| `sweet-grass-store-redb` | `DEFAULT_DB_PATH` | `"./sweetgrass_redb"` |
| `sweet-grass-store-sled` | `DEFAULT_DB_PATH` | `"./sweetgrass_sled"` |

**Inter-primal pattern**: Never hardcode DID fallbacks, MIME types, or storage
paths inline. Define named constants in a central identity/config module.

---

## Property-Based Testing (proptest)

6 proptest strategies added to `sweet-grass-core/src/braid/tests.rs`:

| Strategy | Property |
|----------|----------|
| `BraidId` roundtrip | `BraidId::new(s).as_ref() == s` for any non-empty string |
| `ContentHash` roundtrip | `ContentHash::new(s).as_ref() == s` for any non-empty string |
| `Did` roundtrip | `Did::new(s).as_ref() == s` for any non-empty string |
| Hex encode/decode | `hex_decode_strict(hex_encode(bytes)) == bytes` for any byte vector |
| Braid builder invariants | All built braids have non-empty `id`, `hash`, `attributed_to` |
| Arc clone equality | `Arc<str>`-based clones compare equal across all ID types |

**Inter-primal pattern**: Use proptest for all newtype wrappers around `Arc<str>` or
`String` to verify roundtrip invariants. Add to `[dev-dependencies]` as `proptest = "1"`.

---

## Coverage Push

### Health handler (8 new tests)
- `CountFailingStore` error scenarios (store returns error)
- `PrimalStatus` edge cases (`Degraded`, `Unknown`)
- Integration status propagation
- `determine_status` logic

### MemoryStore (18 new tests)
- `put_batch` / `get_batch` (2+ items, single item, mixed existing)
- Query edge cases (empty store, large offset, limit=0)
- Error paths (delete nonexistent, get nonexistent)
- Index consistency after updates and deletes
- Activity and entity creation/retrieval

### capability.list (4 new tests)
- Expected domain names present
- Method count matches registered handlers
- Grouping by domain produces expected structure
- All domains return non-empty method lists

---

## Smart Test Refactoring

`jsonrpc/tests.rs` exceeded 1000 LOC (1053). Rather than naive splitting:

| File | Before | After | Content |
|------|--------|-------|---------|
| `tests.rs` | 1053 | 768 | Domain-specific handler tests (braid, contribution, provenance, query) |
| `tests_protocol.rs` | — | 302 | Protocol-level tests (batch, notification, capability, entrypoint) |

The split follows the architectural boundary between protocol compliance and domain logic.

---

## JsonRpcResponse Evolution

```rust
// Before
pub struct JsonRpcResponse {
    pub jsonrpc: &'static str,
    // ...
}

// After — supports both Serialize and Deserialize
pub struct JsonRpcResponse {
    pub jsonrpc: std::borrow::Cow<'static, str>,
    // ...
}

const JSONRPC_VERSION: Cow<'static, str> = Cow::Borrowed("2.0");
```

`Cow::Borrowed("2.0")` is zero-allocation for serialization; `Cow` enables
deserialization without a custom deserializer.

---

## Files Modified

| Crate | Files | Changes |
|-------|-------|---------|
| `sweet-grass-core` | `lib.rs`, `braid/tests.rs` | `identity` constants, proptest strategies |
| `sweet-grass-service` | `handlers/jsonrpc/mod.rs` | Batch + notification + `process_single` extraction |
| `sweet-grass-service` | `handlers/jsonrpc/contribution.rs` | Magic strings → identity constants |
| `sweet-grass-service` | `handlers/jsonrpc/tests.rs` | Refactored, domain tests only |
| `sweet-grass-service` | `handlers/jsonrpc/tests_protocol.rs` | **New**: protocol-level tests |
| `sweet-grass-service` | `handlers/health.rs` | 8 new tests |
| `sweet-grass-service` | `uds.rs` | `process_single` integration |
| `sweet-grass-service` | `factory/mod.rs` | `DEFAULT_STORAGE_BACKEND` constant |
| `sweet-grass-store` | `memory/mod.rs` | 18 new tests |
| `sweet-grass-store-redb` | `lib.rs` | `DEFAULT_DB_PATH` constant |
| `sweet-grass-store-sled` | `lib.rs` | `DEFAULT_DB_PATH` constant |
| Workspace | `Cargo.toml` | Version 0.7.10 → 0.7.11 |

---

## Metrics

| Metric | v0.7.10 | v0.7.11 |
|--------|---------|---------|
| Tests | 847 | **892** |
| Source files | 111 | **112** (+tests_protocol.rs) |
| Largest file | 830L | **804L** |
| JSON-RPC batch support | No | **Yes** |
| JSON-RPC notification support | No | **Yes** |
| proptest strategies | 0 | **6** |
| Hardcoded magic strings | 5 | **0** |
| Unsafe code | 0 | 0 |
| Clippy warnings | 0 | 0 |

---

## Deferred

- **Zero-copy serde borrowing** — `Cow<'a, str>` in deserialization requires lifetime threading through store traits. Deferred to v0.8.0+.
- **tarpc batch/notification parity** — tarpc service trait doesn't have a notification concept. Deferred.
- **Showcase script modernization** — Many showcase scripts use obsolete CLI flags (`--port`, no `server` subcommand). Will be updated in a dedicated showcase refresh pass.

---

## Verification

```
cargo fmt --all -- --check         ✓
cargo check --workspace            ✓ (0 warnings)
cargo clippy --workspace --all-targets --all-features -- -D warnings  ✓ (0 warnings)
cargo test --workspace             ✓ (892 tests)
cargo doc --workspace --no-deps    ✓ (0 warnings)
cargo deny check                   ✓
```
