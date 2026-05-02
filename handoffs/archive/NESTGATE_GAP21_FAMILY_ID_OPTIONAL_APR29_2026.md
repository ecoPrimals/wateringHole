# NestGate GAP-21 Resolution — `family_id` Optional in Storage Wire Schema

**Date**: April 29, 2026  
**From**: NestGate team  
**To**: primalSpring, downstream compositions  
**Ref**: primalSpring Phase 56 `LIVE_DEPLOYMENT_GAP_REPORT_PHASE56.md`

---

## Issue

GAP-21: `storage.store` and all `storage.*` methods require `family_id` parameter
or return error. Not documented in wire schema. Downstream springs added `family_id`
to all calls as a workaround.

## Resolution

**`family_id` is now explicitly documented as optional** when connecting to a
family-scoped socket (`nestgate-{family}.sock`). The server defaults to its own
`NESTGATE_FAMILY_ID` / `FAMILY_ID` from the environment.

### Behavior

1. If `family_id` is present in params: used as-is (explicit always wins)
2. If omitted: server's socket-scoped family from env (`NESTGATE_FAMILY_ID` > `FAMILY_ID` > `"standalone"`)
3. If both are absent: error with message `"family_id required — set NESTGATE_FAMILY_ID or pass family_id in params"`

In NUCLEUS compositions, case 2 is the norm. `desktop_nucleus.sh` exports
`FAMILY_ID=desktop-nucleus`, so NestGate's `SocketConfig` picks it up automatically.
Springs should **not** need to pass `family_id` in every request.

### What changed

| File | Change |
|------|--------|
| `storage_handlers.rs` `resolve_family_id` | Debug log when falling back to server default |
| `storage_stream.rs` `resolve_family_id` | Aligned with same logging pattern |
| `storage_handlers.rs` `storage_namespaces_list` | Now uses shared `resolve_family_id` (was inline fallback) |
| `capability_registry.toml` | Documents `family_id` as optional with env fallback |
| `QUICK_START_BIOMEOS.md` | Documents params for `storage.store` / `storage.retrieve` |
| `transport/README.md` | Notes `family_id` optional in socat example |
| New test | `store_retrieve_without_family_id_uses_server_default` — full CRUD cycle |

### For primalSpring

You can now remove the `family_id` parameter from all NestGate storage calls in
experiments (exp094, exp101, exp105, exp106). The server default handles it.
Keeping `family_id` in params is harmless (explicit override still works).

### Codebase health

- Tests: 8,841 passing, 0 failures, 60 ignored
- Clippy: ZERO warnings (`-D warnings`)
- Format: CLEAN

---

## Verification

```bash
# Connect to a family-scoped socket and omit family_id:
echo '{"jsonrpc":"2.0","method":"storage.store","params":{"key":"test","value":"hello"},"id":1}' | \
  socat - UNIX-CONNECT:/run/user/$(id -u)/nestgate-desktop-nucleus.sock

# Expected: {"jsonrpc":"2.0","result":{"status":"stored","key":"test","family_id":"desktop-nucleus"},"id":1}
```
