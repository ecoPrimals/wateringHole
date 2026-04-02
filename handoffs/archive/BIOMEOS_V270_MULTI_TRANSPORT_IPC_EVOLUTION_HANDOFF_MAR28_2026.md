# biomeOS v2.70 — Multi-Transport IPC Evolution Handoff

**Date**: March 28, 2026
**From**: biomeOS evolution session
**Status**: All primalSpring P0+P1 gaps resolved

---

## Summary

The Neural Router has been evolved from Unix-socket-only to universal multi-transport IPC. This unblocks cross-gate routing (Pixel, Android), abstract socket support (Squirrel, Android SELinux bypass), and TCP endpoint registration for inter-NUCLEUS capability forwarding.

## primalSpring Gaps Resolved

| Priority | Gap | Resolution |
|----------|-----|------------|
| **P0** | `RegisteredCapability` stores `PathBuf` | Evolved to `TransportEndpoint` (Unix/abstract/TCP/HTTP) |
| **P0** | `forward_request` only uses `AtomicClient::unix()` | Now uses `AtomicClient::from_endpoint()` — routes any transport |
| **P0** | `check_primal_health` uses `Path::exists()` | Replaced with `AtomicClient`-based transport-aware probing |
| **P1** | `capability.register` is transport-naive | Handler parses transport strings (`@name`, `tcp://host:port`, `http://`, `/path.sock`) |
| **P1** | Health checks assume filesystem | Both `quick_health_check` and `check_endpoint_health` use `AtomicClient` |

## Architecture Changes

### Type Evolution

```
RegisteredCapability.socket_path: PathBuf  →  RegisteredCapability.endpoint: TransportEndpoint
DiscoveredPrimal.socket_path: PathBuf      →  DiscoveredPrimal.endpoint: TransportEndpoint
DiscoveredAtomic.primary_socket: PathBuf   →  DiscoveredAtomic.primary_endpoint: TransportEndpoint
```

### Transport Endpoint (now Serde-enabled)

`TransportEndpoint` in `biomeos-core` now derives `Serialize`/`Deserialize` with tagged JSON:

```json
{"transport": "UnixSocket", "address": {"path": "/run/user/1000/beardog.sock"}}
{"transport": "AbstractSocket", "address": {"name": "biomeos_squirrel_abc123"}}
{"transport": "TcpSocket", "address": {"host": "192.0.2.100", "port": 9001}}
{"transport": "HttpJsonRpc", "address": {"host": "songbird.local", "port": 8080}}
```

### Forward Request Evolution

```
forward_request(&PathBuf, method, params)         →  forward_request(&TransportEndpoint, method, params)
AtomicClient::unix(socket_path)                    →  AtomicClient::from_endpoint(endpoint.clone())
socket_path.file_stem() for metrics label          →  primal_label_for_endpoint() (handles all transports)
```

### Health Check Evolution

**Before**: `Path::exists()` + manual `UnixStream` connect + JSON-RPC write/read

**After**: `AtomicClient::from_endpoint(endpoint).call("health.check", {})` — works for all transports, no filesystem assumption.

### capability.register Handler

The JSON-RPC `capability.register` handler now parses the `socket` field as a transport string:
- `/path/to/socket.sock` → `TransportEndpoint::UnixSocket`
- `@abstract_name` → `TransportEndpoint::AbstractSocket`
- `tcp://host:port` or `host:port` → `TransportEndpoint::TcpSocket`
- `http://host:port` → `TransportEndpoint::HttpJsonRpc`

Fallback: if parsing fails, defaults to `UnixSocket` for backward compat.

### Convenience Method

`register_capability_unix()` wraps `PathBuf` into `TransportEndpoint::UnixSocket` for callers that only deal with Unix sockets (bootstrap, graph deployment, config registry, translation loader).

## Files Changed

### Core Types (biomeos-core)
- `socket_discovery/transport.rs` — Added `Serialize`/`Deserialize` to `TransportEndpoint`

### Neural Router (biomeos-atomic-deploy)
- `neural_router/types.rs` — `socket_path` → `endpoint`, `primary_socket` → `primary_endpoint`
- `neural_router/mod.rs` — `register_capability()` accepts `TransportEndpoint`, added `register_capability_unix()`
- `neural_router/forwarding.rs` — `forward_request()` accepts `&TransportEndpoint`, `should_use_tarpc()` transport-aware, added `primal_label_for_endpoint()`
- `neural_router/discovery.rs` — `check_primal_health()` → `check_endpoint_health()`, `quick_health_check()` transport-aware, all discovery methods use `TransportEndpoint`

### Callers Updated
- `bootstrap.rs` — `register_capability_unix()`
- `handlers/capability.rs` — Transport-aware registration, `primary_endpoint`, display strings
- `handlers/graph.rs` — Transport-aware forwarding and registration
- `handlers/topology.rs` — `endpoint.display_string()`
- `neural_api_server/proxy.rs` — `primary_endpoint`
- `neural_api_server/server_lifecycle.rs` — `register_capability_unix()`
- `neural_api_server/translation_loader.rs` — `register_capability_unix()`

### Tests Updated
- `neural_router_tests.rs` — All tests use `TransportEndpoint`
- `neural_router/forwarding.rs` tests — `unix_ep()` helper
- `neural_router/discovery.rs` tests — 3 new transport-variant tests
- `tests/neural_api_routing_tests.rs` — Integration tests updated

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 7,160 | 7,165 |
| Clippy warnings | 0 | 0 |
| cargo doc warnings | 0 | 0 |
| cargo deny | PASS | PASS |
| Transport support | Unix only | Unix + Abstract + TCP + HTTP |
| Health check transports | Unix only (Path::exists) | All (AtomicClient-based) |

## Remaining P2 Items (Future)

| Item | Notes |
|------|-------|
| `route.register` JSON-RPC | Higher-level cross-gate routing API (register gate + transport + capabilities) |
| ARM64 biomeOS binary | Pure Rust (0 C deps), straightforward cross-compile |
| biomeOS on gate2 | Validates cross-gate routing end-to-end |

## Cross-Gate Routing: Now Possible

With `TransportEndpoint` stored in the registry, a primal on another gate can register:

```json
{
  "jsonrpc": "2.0",
  "method": "capability.register",
  "params": {
    "capability": "crypto.sign",
    "primal": "beardog",
    "socket": "tcp://192.0.2.100:9001",
    "source": "cross-gate"
  }
}
```

The Neural Router will then `forward_request` to `AtomicClient::tcp("192.0.2.100", 9001)` transparently.
