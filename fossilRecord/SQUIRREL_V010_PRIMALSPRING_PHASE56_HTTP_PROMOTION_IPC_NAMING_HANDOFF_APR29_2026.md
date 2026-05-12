# Squirrel v0.1.0 — primalSpring Phase 56 Audit Resolution

**Date**: April 29, 2026 (session AP)
**Primal**: Squirrel (AI coordination)
**Source**: primalSpring v0.9.24 (Phase 56) — Desktop NUCLEUS local debt + upstream absorption targets

## Two Gaps Resolved

### GAP-03 (P0): HTTP URL Auto-Promotion in `inference.register_provider`

**Problem**: When a provider sends `"socket": "http://localhost:11434"` (using the `socket` field rather than `endpoint`), the value was stored as a UDS filesystem path. This created a broken provider — `Path::exists` on an HTTP URL returns false, and all routing attempts fail. neuralSpring registers Ollama this way because it predates the `endpoint` field.

**Root cause**: Session AN (Phase 55) added the `endpoint` field and HTTP transport support, but assumed callers would use the new field. In practice, callers send HTTP URLs in the pre-existing `socket` field.

**Solution**: `handlers_inference.rs` now auto-detects HTTP scheme (`http://`, `https://`) in the `socket` param and promotes it to `endpoint`:

```rust
let (socket, endpoint) = match (&raw_socket, &raw_endpoint) {
    (Some(s), None) if is_http(s) => (None, Some(s.clone())),
    _ => (raw_socket, raw_endpoint),
};
```

- Logged as `info!` with `"Auto-promoting HTTP URL from 'socket' to 'endpoint'"`.
- Backward compatible: explicit `endpoint` field still works; UDS `socket` paths unaffected.
- New test: `register_http_endpoint_provider` validates HTTP endpoint registration and model listing through `list_providers_detailed`.

**Files**: `handlers_inference.rs`, `router_tests.rs`

### GAP-06 (P2): Canonical `ipc.*` Method Naming

**Problem**: Squirrel used `discovery.register`, `discovery.heartbeat`, and `discovery.find_provider` as RPC method names when communicating with the discovery service. The canonical biomeOS IPC protocol uses the `ipc.*` namespace.

**Solution**: Evolved all three method names:

| Before | After |
|---|---|
| `discovery.register` | `ipc.register` |
| `discovery.heartbeat` | `ipc.heartbeat` |
| `discovery.find_provider` | `ipc.find_provider` |

- All doc comments, log messages, and wire JSON updated.
- Discovery service tests pass (they validate response behavior, not method names).

**Files**: `discovery_service.rs`, `discovery.rs`

## Quality Gates

- `cargo fmt`: PASS
- `cargo clippy -D warnings`: PASS (0 warnings)
- `cargo test`: **7,181 passing** / 0 failures
- `cargo deny check`: `advisories ok, bans ok, licenses ok, sources ok`

## Upstream Context

The Phase 56 audit documents the broader goal of evolving bash symlinks (13 capability-aliased `.sock` files) into Neural API's `CapabilityTranslationRegistry`. Squirrel's side is now clean: IPC registration uses canonical method names and HTTP providers work regardless of which field carries the URL. The remaining work is in biomeOS Neural API (either `capability.resolve` RPC or automatic symlink creation during `NucleusMode` startup).
