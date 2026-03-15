# Primal IPC Protocol Standard

**Status**: Ecosystem Standard
**Version**: 3.0.0
**Authority**: wateringHole (ecoPrimals Core Standards)

**Version History**:
- v1.0 (Jan 19, 2026): Unix socket + JSON-RPC 2.0
- v2.0 (Jan 30, 2026): Platform-agnostic transport concept
- v3.0 (Feb 3, 2026): Unified transport + dual protocol + tarpc. Consolidated from `PRIMAL_IPC_PROTOCOL.md` v2.0 and `UNIVERSAL_IPC_STANDARD_V3.md` v3.0.

---

## Core Principle

> Primals are autonomous organisms that communicate via PROTOCOLS,
> not by embedding each other's code.

- Each primal implements IPC independently in its own codebase
- No shared IPC crate — duplication is healthy independence
- Standard protocol enables interoperability without coupling
- Primals adopt standard updates at their own pace

---

## Protocol Specification

### Message Format: JSON-RPC 2.0

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "domain.operation",
    "params": { "key": "value" },
    "id": 1
}
```

**Success Response**:
```json
{
    "jsonrpc": "2.0",
    "result": { "data": "value" },
    "id": 1
}
```

**Error Response**:
```json
{
    "jsonrpc": "2.0",
    "error": { "code": -32601, "message": "Method not found", "data": null },
    "id": 1
}
```

**Standard Error Codes**: -32700 (parse), -32600 (invalid request), -32601 (method not found), -32602 (invalid params), -32603 (internal).

**Method naming**: See `SEMANTIC_METHOD_NAMING_STANDARD.md` for `domain.verb` conventions.

### Dual Protocol Support (v3.0)

| Protocol | Strengths | Use Case |
|----------|-----------|----------|
| **JSON-RPC 2.0** | Human-readable, debuggable, universal | External APIs, cross-language, required |
| **tarpc** | High-performance, type-safe, Rust-native | Internal primal-to-primal, optional |

Primals MUST support JSON-RPC 2.0. tarpc is optional for high-performance paths.
Protocol negotiation occurs on connection — peers exchange supported protocols
and select the best mutual option.

---

## Transport Layer

### Tier System

```
Tier 1 (Native — fastest for platform):
├── Unix Sockets       (Linux, macOS, BSD)
├── Abstract Sockets   (Android, Linux)
├── Named Pipes        (Windows)
└── XPC                (iOS, macOS)

Tier 2 (Universal — always works):
└── TCP Localhost      (all platforms)

Tier 3 (Specialized):
├── In-Process         (WASM, embedded)
└── Shared Memory      (high-performance, requires setup)
```

Primals discover the best transport at runtime. Prefer Tier 1 (native), fall
back to Tier 2 (TCP). No hardcoded socket paths.

### Socket Path Convention

```
$XDG_RUNTIME_DIR/biomeos/<primal>-${FAMILY_ID}.sock
```

For springs in niche deployment:
```
$XDG_RUNTIME_DIR/biomeos/<spring>-${FAMILY_ID}.sock
```

### Platform Support Matrix

| Platform | Transport | Status |
|----------|-----------|--------|
| Linux (x86_64) | Unix Socket | Production |
| Linux (aarch64) | Unix Socket | Production |
| Android | Abstract Socket | Production |
| macOS | Unix Socket | Production |
| Windows | Named Pipe / TCP | Planned |
| iOS | XPC | Documented |
| WASM | In-Process | Documented |

---

## Discovery Protocol

### Songbird as Registry

Songbird maintains the service registry. Primals communicate with Songbird via
JSON-RPC — never by importing Songbird code.

### Registration (on startup)

```json
{
    "jsonrpc": "2.0",
    "method": "ipc.register",
    "params": {
        "name": "beardog",
        "endpoint": "/primal/beardog",
        "capabilities": ["crypto", "btsp", "ed25519", "x25519"],
        "version": "2.7.0"
    },
    "id": 1
}
```

### Find by Capability

```json
{
    "jsonrpc": "2.0",
    "method": "ipc.find_capability",
    "params": { "capability": "crypto" },
    "id": 2
}
```

Returns all primals providing that capability with their endpoints.

### Other Discovery Methods

| Method | Purpose |
|--------|---------|
| `ipc.register` | Register primal + capabilities |
| `ipc.resolve` | Find primal by name |
| `ipc.find_capability` | Find primals by capability |
| `ipc.list` | List all registered primals |
| `ipc.heartbeat` | Periodic presence signal (every 30-60s) |

### biomeOS Neural API Integration

When biomeOS is running, primals also register via `lifecycle.register` with
the Neural API. biomeOS provides higher-order routing beyond Songbird's
capability-based discovery.

---

## Implementation Pattern

Each primal implements IPC in its own codebase. This is reference code to
copy and adapt — NOT a shared dependency.

### Recommended File Structure

```
your-primal/
└── src/
    ├── ipc/
    │   ├── mod.rs          # Transport selection
    │   ├── server.rs       # JSON-RPC server
    │   └── client.rs       # Client for calling other primals
    └── dispatch.rs         # Method routing
```

### Server Pattern

```rust
// Start IPC server with runtime transport discovery
let endpoint = TransportEndpoint::for_primal("myprimal")?;
let listener = bind_transport(&endpoint).await?;

// Register with Songbird
register_with_songbird("myprimal", &endpoint, &capabilities).await?;

// Accept connections
loop {
    let (stream, _) = listener.accept().await?;
    tokio::spawn(handle_json_rpc(stream));
}
```

### Client Pattern

```rust
// Discover and connect (capability-based)
let crypto_endpoint = find_by_capability("crypto").await?;
let stream = connect_transport(&crypto_endpoint).await?;

// Call method
let response = json_rpc_call(&stream, "crypto.sign", json!({
    "data": "hello",
    "algorithm": "ed25519"
})).await?;
```

### Key Implementation Rules

- ZERO imports from other primals
- ZERO shared IPC crates
- Uses `tokio` for async I/O (ecosystem standard runtime)
- Runtime transport discovery (not compile-time only)
- Graceful fallback (Tier 1 → Tier 2)
- ~500-1000 lines of IPC code per primal — this is healthy independence

---

## Compliance Checklist

**Autonomy (critical)**:
- [ ] ZERO imports from other primals
- [ ] Implements IPC in own codebase

**Protocol**:
- [ ] JSON-RPC 2.0 supported (required)
- [ ] Method naming follows `SEMANTIC_METHOD_NAMING_STANDARD.md`

**Transport**:
- [ ] Multi-transport binding (native + fallback)
- [ ] Runtime transport discovery
- [ ] No hardcoded socket paths

**Discovery**:
- [ ] Registers with Songbird on startup
- [ ] Declares capabilities in registration
- [ ] Periodic heartbeat

**Testing**:
- [ ] Tested on Linux (Unix sockets)

---

## Related Standards

- `SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming (`domain.verb`)
- `UNIBIN_ARCHITECTURE_STANDARD.md` — Binary structure
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Universal portability
- `birdsong/BIRDSONG_PROTOCOL.md` — Encrypted UDP discovery
- `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` — Spring niche IPC requirements
