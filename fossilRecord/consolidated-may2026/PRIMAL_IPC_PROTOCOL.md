# Primal IPC Protocol Standard

**Status**: Ecosystem Standard
**Version**: 3.1.0
**Authority**: wateringHole (ecoPrimals Core Standards)

**Version History**:
- v1.0 (Jan 19, 2026): Unix socket + JSON-RPC 2.0
- v2.0 (Jan 30, 2026): Platform-agnostic transport concept
- v3.0 (Feb 3, 2026): Unified transport + dual protocol + tarpc. Consolidated from `PRIMAL_IPC_PROTOCOL.md` v2.0 and `UNIVERSAL_IPC_STANDARD_V3.md` v3.0.
- v3.1 (Mar 25, 2026): Wire framing, standalone startup, `--port` convention. Driven by esotericWebb first live composition with plasmidBin primals.

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

### Wire Framing (v3.1)

The canonical wire framing for inter-primal JSON-RPC is **newline-delimited**:
one JSON-RPC object per line, terminated by `\n` (ASCII 0x0A).

```
{"jsonrpc":"2.0","method":"health.liveness","id":1}\n
{"jsonrpc":"2.0","result":{"status":"alive"},"id":1}\n
```

Primals MUST accept this framing on at least one transport (UDS or TCP).
This is the format that orchestrators, springs, and inter-primal clients use
on raw byte streams (`UnixStream`, `TcpStream`).

**HTTP-wrapped JSON-RPC** (e.g. `POST /jsonrpc` with Axum or jsonrpsee) is
acceptable for external APIs, dashboards, and human-facing tooling. However,
HTTP MUST NOT be the only JSON-RPC surface. Every primal MUST provide a
newline-delimited endpoint for composition.

| Surface | Framing | Required | Audience |
|---------|---------|----------|----------|
| Inter-primal IPC | Newline-delimited over UDS/TCP | **MUST** | Primals, springs, orchestrators |
| External API | HTTP POST JSON-RPC | MAY | Dashboards, CLI tools, browsers |
| High-performance | tarpc (binary) | MAY | Rust-to-Rust hot paths |

**Why this matters:** esotericWebb's `PrimalClient` sends raw newline JSON-RPC
over `TcpStream` and `UnixStream`. Primals that only accept HTTP-wrapped
JSON-RPC (e.g. behind Axum) are unreachable by the standard client. The same
applies to any orchestrator or spring using the standard raw-stream pattern.

**Reference implementation:** esotericWebb `webb/src/ipc/client.rs` demonstrates
the canonical client. The server side is a `BufReader` loop reading lines from
an accepted stream connection.

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
$XDG_RUNTIME_DIR/biomeos/<primal>.sock
```

When running family-scoped (multiple families on one host):
```
$XDG_RUNTIME_DIR/biomeos/<primal>-${FAMILY_ID}.sock
```

For springs in niche deployment:
```
$XDG_RUNTIME_DIR/biomeos/<spring>.sock
```

**Filesystem sockets are REQUIRED on Linux.** Abstract namespace sockets
(`@primal`) are acceptable as Tier 1 on Android but MUST NOT be the only
socket on Linux — they are invisible to `readdir()` and break filesystem-based
discovery. Primals using abstract sockets MUST also bind a filesystem socket.

**Capability-domain symlinks (v3.1):** Primals SHOULD create a symlink named
after their capability domain alongside the primal-named socket:

```
$XDG_RUNTIME_DIR/biomeos/ai.sock -> squirrel.sock
$XDG_RUNTIME_DIR/biomeos/dag.sock -> rhizocrypt.sock
```

This enables capability-based filesystem discovery (Tier 3 in
`CAPABILITY_BASED_DISCOVERY_STANDARD.md`) without requiring Songbird or
Neural API to be running.

**Custom directories are non-conformant.** Sockets MUST live in the biomeos
directory, not in primal-specific directories (e.g., `/run/user/1000/petaltongue/`
is non-conformant; use `/run/user/1000/biomeos/petaltongue.sock` instead).

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

### Standalone Startup (v3.1)

Primals MUST start successfully when no other primals are running and no
identity environment variables are set. This is **standalone mode** — the
primal operates in isolation with degraded capability.

Primals MUST NOT hard-fail on missing `FAMILY_ID`, `NODE_ID`, or discovery
endpoints. When identity is absent, default to `standalone` or `default`.
When Songbird or Neural API are unreachable, log a warning and continue.

This enables:
- Local development without a full ecosystem
- Spring-driven composition where primals start before discovery is available
- Incremental bringup of deploy graphs
- Testing individual primals in isolation

---

## Compliance Checklist

**Autonomy (critical)**:
- [ ] ZERO imports from other primals
- [ ] Implements IPC in own codebase

**Protocol (v3.1)**:
- [ ] JSON-RPC 2.0 supported (required)
- [ ] Newline-delimited framing on at least one transport (UDS or TCP)
- [ ] Method naming follows `SEMANTIC_METHOD_NAMING_STANDARD.md`
- [ ] `health.liveness`, `health.readiness`, `health.check` respond correctly

**Transport (v3.1)**:
- [ ] Filesystem socket in `$XDG_RUNTIME_DIR/biomeos/<primal>.sock`
- [ ] Capability-domain symlink created (e.g., `ai.sock -> squirrel.sock`)
- [ ] No abstract-namespace-only sockets on Linux
- [ ] `server --port <PORT>` binds TCP JSON-RPC (newline-delimited)
- [ ] Runtime transport discovery
- [ ] No hardcoded socket paths

**Startup (v3.1)**:
- [ ] Starts in standalone mode without `FAMILY_ID` / `NODE_ID`
- [ ] Degrades gracefully when Songbird / Neural API are unreachable
- [ ] `server --port <PORT>` accepted by UniBin `server` subcommand

**Discovery**:
- [ ] Registers with Songbird on startup (when available)
- [ ] Declares capabilities in registration
- [ ] Periodic heartbeat (when registry is available)

**Testing**:
- [ ] Tested on Linux (Unix sockets)
- [ ] Tested with raw newline JSON-RPC client (not just HTTP)

See `IPC_COMPLIANCE_MATRIX.md` for per-primal status.

---

## Related Standards

- `SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming (`domain.verb`)
- `UNIBIN_ARCHITECTURE_STANDARD.md` — Binary structure and `--port` convention
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Universal portability
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — Capability-domain sockets and discovery tiers
- `IPC_COMPLIANCE_MATRIX.md` — Per-primal interop status
- `SPRING_INTEROP_LESSONS.md` — Learnings from spring composition
- `birdsong/BIRDSONG_PROTOCOL.md` — Encrypted UDP discovery
- `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` — Spring niche IPC requirements
