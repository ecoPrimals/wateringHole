# NestGate v4.7.0-dev — Session 43h Handoff

**Date**: April 13, 2026  
**Primal**: NestGate (storage)  
**Session**: 43h — Streaming storage & cross-spring namespace isolation  
**Status**: GREEN — all checks pass  

---

## primalSpring Upstream Gaps Resolved

### 1. Large/streaming tensor retrieval (medium)

**Problem**: `storage.retrieve` returns the full value as inline JSON, blocking IPC for multi-MB payloads.

**Resolution**: The isomorphic IPC adapter now supports the full large-object method set:

| Method | Description |
|--------|-------------|
| `storage.store_blob` | Store binary data (base64 encoded) |
| `storage.retrieve_blob` | Retrieve full blob as base64 |
| `storage.retrieve_range` | Chunked byte-range read (4 MiB max per call, base64) |
| `storage.object.size` | Get size/existence without reading content |

**Streaming pattern for callers**:
1. `storage.object.size` to learn total bytes
2. N calls to `storage.retrieve_range` with `{offset, length}` to read chunks
3. Reassemble on the caller side

This matches the pattern already documented in the deprecated Unix server and validated in the new test suite (chunked reassembly test).

### 2. Cross-spring persistent storage IPC (medium)

**Problem**: No namespace isolation — all springs share one flat keyspace.

**Resolution**: Caller-isolated namespaces with explicit cross-spring access.

**Directory layout**:
```
{base}/datasets/{family_id}/{namespace}/{key}.json   (JSON values)
{base}/datasets/{family_id}/{namespace}/_blobs/{key}  (binary blobs)
```

**Namespace model**:
- `family_id` resolved from env (`NESTGATE_FAMILY_ID` / `FAMILY_ID` / `BIOMEOS_FAMILY_ID`), default `"default"`
- `namespace` parameter on all `storage.*` methods, default `"shared"`
- `"shared"` namespace readable/writable by all springs in the family (cross-spring meeting point)
- Spring-specific namespaces (e.g. `"wetspring"`) are private — other springs must pass explicit `namespace` to access
- `storage.namespaces.list` enumerates available namespaces

**Wire format** (backward compatible):
```json
{"method": "storage.store", "params": {"key": "data", "value": {...}}}
{"method": "storage.store", "params": {"key": "data", "value": {...}, "namespace": "wetspring"}}
{"method": "storage.retrieve", "params": {"key": "data", "namespace": "shared"}}
```

Omitting `namespace` defaults to `"shared"` — existing callers work unchanged.

---

## Verification

```
Build:    cargo check --workspace --all-features --all-targets — PASS
Clippy:   cargo clippy --workspace --all-targets --all-features -- -D warnings — PASS
Format:   cargo fmt --all --check — PASS
Docs:     cargo doc --workspace --no-deps — PASS (zero warnings)
Tests:    11,816 passing, 0 failures, 451 ignored (+11 new tests)
```

---

## New methods added to isomorphic IPC

- `storage.store_blob`
- `storage.retrieve_blob`
- `storage.retrieve_range`
- `storage.object.size`
- `storage.namespaces.list`

All registered in `capability_registry.toml` and advertised via `capabilities.list`.

---

## Impact on other primals

- **wetSpring / neuralSpring**: Can now use `storage.retrieve_range` for large PDE grids and training checkpoints
- **healthSpring / wetSpring**: Can use `namespace` parameter for cross-spring data sharing via `"shared"` namespace, or isolated storage via their own namespace
- **All springs**: Backward compatible — existing callers that omit `namespace` get `"shared"` (same as previous flat behavior)

---

## Follow-up: Session 43i — Final Sovereignty Cleanup

Removed the last 3 hardcoded primal names from production `.rs` files:
- `model_cache_handlers.rs`: "BearDog" and "Songbird" in `consumed_capabilities` JSON reason strings replaced with capability-generic wording
- `atomic/mod.rs`: "primalSpring" in doc header replaced with neutral "Audit Compliance Note"

**Result**: Zero primal names in production Rust code. Zero TODO/FIXME/HACK markers. Zero stale debris.
