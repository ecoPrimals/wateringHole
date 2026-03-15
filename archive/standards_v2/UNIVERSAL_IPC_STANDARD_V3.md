# Universal IPC Standard v3.0 - Ecosystem Evolution

**Status**: PROPOSED STANDARD  
**Version**: 3.0.0  
**Date**: February 3, 2026  
**Authority**: wateringHole (ecoPrimals Core Standards)  
**Catalyst**: Real-world deployment friction on Pixel 8a (Android) + cross-device coordination

---

## Executive Summary

This standard defines **behavioral requirements** for platform-agnostic IPC that all primals implement **independently**. Each primal evolves toward these standards autonomously.

**The Problem**: Inconsistent transport selection across primals  
**The Solution**: Clear standards that each primal implements in their own codebase

---

## Core Principle: Primal Autonomy

> **"Primals are autonomous organisms that communicate via PROTOCOLS, not by embedding each other's code."**

### What This Standard IS

- ✅ **Behavioral specification** - defines WHAT primals must do
- ✅ **Protocol definition** - JSON-RPC 2.0, transport negotiation
- ✅ **Reference patterns** - example code to copy/adapt
- ✅ **Compliance criteria** - how to verify conformance

### What This Standard IS NOT

- ❌ **Shared library/crate** - NO cross-primal dependencies
- ❌ **Mandated implementation** - primals choose HOW to implement
- ❌ **Code embedding** - each primal owns their IPC code

### Why No Shared Crate?

```
❌ WRONG: Shared dependency creates coupling
┌─────────────────────────────────────────────┐
│  primal-ipc (shared crate)                  │
│  ├── BearDog depends                        │
│  ├── Songbird depends                       │
│  └── All primals depend                     │
│                                             │
│  Problem: One change affects ALL primals    │
│  Problem: Version conflicts                 │
│  Problem: Violates autonomy principle       │
└─────────────────────────────────────────────┘

✅ RIGHT: Each primal implements standard independently
┌─────────────────────────────────────────────┐
│  STANDARD (this document)                   │
│  ├── BearDog implements (own code)          │
│  ├── Songbird implements (own code)         │
│  └── Each primal implements (own code)      │
│                                             │
│  Benefit: True autonomy                     │
│  Benefit: Independent evolution             │
│  Benefit: No version coupling               │
└─────────────────────────────────────────────┘
```

---

## Evolution History

| Version | Date | Focus | Coverage |
|---------|------|-------|----------|
| **v1.0** | Jan 19, 2026 | Unix socket + JSON-RPC | Linux/macOS only |
| **v2.0** | Jan 30, 2026 | Platform-agnostic (conceptual) | All platforms (spec only) |
| **v3.0** | Feb 3, 2026 | **Unified implementation + dual protocol** | All platforms + JSON-RPC + tarpc |

---

## Core Architecture

### Transport Layer (v3.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL IPC LAYER                          │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ JSON-RPC │   │  tarpc   │   │  Custom  │   │  Future  │   │
│  │  2.0     │   │ (async)  │   │ Protocol │   │ Protocol │   │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   │
│       │              │              │              │          │
│  ┌────┴──────────────┴──────────────┴──────────────┴────┐    │
│  │              PROTOCOL ABSTRACTION LAYER              │    │
│  │            (transport-agnostic framing)              │    │
│  └────┬──────────────┬──────────────┬──────────────┬────┘    │
│       │              │              │              │          │
│  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐   │
│  │ Unix    │    │ Abstract│    │  TCP    │    │ Named   │   │
│  │ Socket  │    │ Socket  │    │         │    │ Pipe    │   │
│  │(Linux)  │    │(Android)│    │(Univ.)  │    │(Windows)│   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Transport Abstraction

```rust
/// Platform-agnostic transport endpoint
#[derive(Debug, Clone, PartialEq)]
pub enum TransportEndpoint {
    /// Filesystem Unix socket (Linux, macOS, BSD)
    UnixSocket { path: PathBuf },
    
    /// Abstract Unix socket (Android, Linux)
    /// Name automatically prefixed with null byte
    AbstractSocket { name: String },
    
    /// TCP socket (Universal fallback)
    Tcp { host: String, port: u16 },
    
    /// Windows named pipe
    #[cfg(windows)]
    NamedPipe { name: String },
    
    /// iOS XPC service
    #[cfg(target_os = "ios")]
    Xpc { service: String },
    
    /// In-process channel (WASM, embedded)
    #[cfg(target_family = "wasm")]
    InProcess { channel_id: String },
}

impl TransportEndpoint {
    /// Check if this is a "native" transport (fastest for platform)
    pub fn is_native(&self) -> bool;
    
    /// Display for logging/debugging
    pub fn display(&self) -> String;
    
    /// Create endpoint for primal on current platform
    pub fn for_primal(primal_name: &str) -> Result<Self>;
}
```

### Protocol Abstraction (NEW in v3.0)

```rust
/// Protocol-agnostic message framing
pub trait PrimalProtocol: Send + Sync {
    /// Protocol identifier (for negotiation)
    fn protocol_id(&self) -> &'static str;
    
    /// Encode request to bytes
    fn encode_request(&self, method: &str, params: Value, id: RequestId) -> Vec<u8>;
    
    /// Decode response from bytes
    fn decode_response(&self, bytes: &[u8]) -> Result<Response>;
    
    /// Encode notification (no response expected)
    fn encode_notification(&self, method: &str, params: Value) -> Vec<u8>;
}

/// Built-in protocol implementations
pub struct JsonRpcProtocol;    // JSON-RPC 2.0 (current standard)
pub struct TarpcProtocol;      // tarpc binary (high-performance)
pub struct MessagePackProtocol; // MessagePack (compact binary)
```

---

## Reference Implementation Patterns

Each primal implements these patterns **in their own codebase**. This is reference code to copy/adapt, NOT a shared dependency.

### Recommended File Structure (within each primal)

```
your-primal/
├── crates/
│   └── your-primal-ipc/     # OR inline in main crate
│       └── src/
│           ├── transport/
│           │   ├── mod.rs       # Platform detection
│           │   ├── unix.rs      # Unix sockets
│           │   ├── abstract.rs  # Android abstract sockets
│           │   └── tcp.rs       # TCP fallback
│           ├── endpoint.rs      # TransportEndpoint enum
│           └── server.rs        # IPC server
```

### Reference Dependencies (copy to your Cargo.toml)

```toml
# Each primal adds these to their OWN Cargo.toml
# This is NOT a shared crate!

[dependencies]
tokio = { version = "1", features = ["net", "io-util", "sync", "rt"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
async-trait = "0.1"
tracing = "0.1"

# Optional for tarpc (high-performance)
# tarpc = { version = "0.34", optional = true }
# bincode = { version = "1.3", optional = true }
```

---

## Public API

### Server API

```rust
use primal_ipc::{PrimalServer, ServerConfig};

// Simple: Start with automatic transport discovery
let server = PrimalServer::start("beardog").await?;

// With config: Explicit transport preferences
let server = PrimalServer::builder("beardog")
    .with_protocol(Protocol::JsonRpc)
    .prefer_transport(Transport::UnixSocket)
    .fallback_transport(Transport::Tcp { port: 9900 })
    .with_family_id("ecosystem_alpha")
    .start()
    .await?;

// Accept connections (any transport)
loop {
    let (conn, transport_info) = server.accept().await?;
    tracing::info!("Connection via {}", transport_info.display());
    tokio::spawn(handle_connection(conn));
}
```

### Client API

```rust
use primal_ipc::{PrimalClient, ConnectOptions};

// Simple: Discover and connect
let client = PrimalClient::connect("beardog").await?;

// With options: Explicit preferences
let client = PrimalClient::builder()
    .primal("beardog")
    .protocol(Protocol::JsonRpc)
    .timeout(Duration::from_secs(5))
    .with_discovery_hints(&["unix:///run/user/1000/biomeos/beardog.sock"])
    .connect()
    .await?;

// Make RPC call
let response = client.call("crypto.sign", json!({
    "data": "hello",
    "algorithm": "ed25519"
})).await?;
```

### Registration API (Songbird Integration)

```rust
use primal_ipc::registry::{ServiceRegistry, ServiceInfo};

// Register with Songbird (or local registry)
let registry = ServiceRegistry::connect().await?;

registry.register(ServiceInfo {
    name: "beardog".into(),
    endpoints: server.endpoints(),  // All bound transports
    capabilities: vec!["crypto", "security", "genetics"],
    version: "0.9.0".into(),
    family_id: Some("ecosystem_alpha".into()),
}).await?;

// Discovery
let crypto_services = registry.find_by_capability("crypto").await?;
```

---

## Transport Selection Strategy

### Priority Order (Tier System)

```
Tier 1 (Native - Fastest):
├── Unix Sockets       (Linux, macOS, BSD)
├── Abstract Sockets   (Android, Linux)
├── Named Pipes        (Windows)
└── XPC                (iOS, macOS)

Tier 2 (Universal - Always Works):
└── TCP Localhost      (All platforms)

Tier 3 (Specialized):
├── In-Process         (WASM, embedded)
└── Shared Memory      (High-performance, requires setup)
```

### Runtime Discovery

```rust
/// Discover best transport for current platform
pub async fn discover_transports(primal: &str) -> Vec<(Transport, Priority)> {
    let mut transports = vec![];
    
    // Try native transports first
    #[cfg(target_os = "android")]
    if let Ok(t) = try_abstract_socket(primal) {
        transports.push((t, Priority::Native));
    }
    
    #[cfg(all(unix, not(target_os = "android")))]
    if let Ok(t) = try_unix_socket(primal) {
        transports.push((t, Priority::Native));
    }
    
    #[cfg(windows)]
    if let Ok(t) = try_named_pipe(primal) {
        transports.push((t, Priority::Native));
    }
    
    // TCP always available as fallback
    if let Ok(t) = try_tcp_localhost(primal).await {
        transports.push((t, Priority::Fallback));
    }
    
    transports
}
```

---

## JSON-RPC + tarpc Interoperability

### Why Both Protocols?

| Protocol | Strengths | Use Case |
|----------|-----------|----------|
| **JSON-RPC** | Human-readable, debuggable, universal | External APIs, cross-language |
| **tarpc** | High-performance, type-safe, Rust-native | Internal primal-to-primal |

### Protocol Negotiation

```rust
// On connection, negotiate protocol
pub async fn negotiate_protocol(
    stream: &mut impl AsyncReadWrite
) -> Result<Box<dyn PrimalProtocol>> {
    // Send supported protocols
    let supported = [JSONRPC_ID, TARPC_ID, MSGPACK_ID];
    stream.write_all(&encode_supported(&supported)).await?;
    
    // Receive peer's supported protocols
    let peer_supported = decode_supported(&stream.read_negotiation().await?)?;
    
    // Select best mutual protocol
    select_best_protocol(&supported, &peer_supported)
}
```

### Transparent Switching

```rust
// Client doesn't care about protocol
let client = PrimalClient::connect("beardog").await?;

// Automatically uses best available protocol
// (tarpc if both support it, JSON-RPC otherwise)
let result = client.call("crypto.sign", params).await?;
```

---

## Evolution Path (Each Primal Implements Independently)

### Phase 1: Audit Current Transport Support

Each primal team audits their current IPC:

```bash
# Check what transports your primal supports
grep -r "UnixListener\|TcpListener\|AbstractSocket" src/
```

### Phase 2: Implement Missing Transports

Each primal adds transports following the reference patterns:

```rust
// In YOUR primal's codebase (not a shared crate!)

/// Transport selection - implement in your primal
pub async fn select_transport(primal: &str) -> Result<Transport> {
    // 1. Try platform-native (fastest)
    #[cfg(target_os = "android")]
    if let Ok(t) = try_abstract_socket(primal) {
        return Ok(t);
    }
    
    #[cfg(all(unix, not(target_os = "android")))]
    if let Ok(t) = try_unix_socket(primal) {
        return Ok(t);
    }
    
    // 2. Fall back to TCP (universal)
    try_tcp_localhost(primal).await
}
```

### Phase 3: Test on All Target Platforms

```bash
# Each primal tests their OWN implementation
cargo test --target x86_64-unknown-linux-musl
cargo test --target aarch64-unknown-linux-musl
# Test on actual Android device
adb push target/aarch64-unknown-linux-musl/release/your-primal /data/local/tmp/
```

### Example: BearDog Evolution

BearDog already has good transport support in `beardog-tunnel/src/platform/`. Evolution path:

1. ✅ Unix sockets (already implemented)
2. ✅ Abstract sockets (already implemented)
3. ✅ TCP IPC (already implemented)
4. ⏳ Ensure multi-transport server binds all available

### Example: Songbird Evolution

Songbird has excellent support in `songbird-universal-ipc/`. Evolution path:

1. ✅ All transports implemented
2. ✅ Multi-transport discovery
3. ⏳ Ensure protocol negotiation support

### Example: Other Primals

Primals with minimal IPC should evolve their code:

1. Copy reference patterns from this standard
2. Implement in your own crate
3. Test on target platforms
4. NO dependency on other primals

---

## Platform Support Matrix

| Platform | Transport | Status | Notes |
|----------|-----------|--------|-------|
| **Linux (x86_64)** | Unix Socket | ✅ Ready | Primary target |
| **Linux (aarch64)** | Unix Socket | ✅ Ready | Raspberry Pi, etc. |
| **Android** | Abstract Socket | ✅ Ready | GrapheneOS tested |
| **Android** | TCP (fallback) | ✅ Ready | SELinux workaround |
| **macOS (Intel)** | Unix Socket | ✅ Ready | |
| **macOS (M-series)** | Unix Socket | ✅ Ready | |
| **Windows** | Named Pipe | ⏳ Planned | Pure Rust (tokio-pipe) |
| **Windows** | TCP (fallback) | ✅ Ready | |
| **iOS** | XPC | 📝 Documented | Awaiting Pure Rust bindings |
| **WASM** | In-Process | 📝 Documented | No true IPC |

---

## Compliance Checklist

### For Primal to be IPC v3.0 Compliant

**Autonomy (CRITICAL)**:
- [ ] **ZERO imports from other primals** - Implements IPC in own codebase
- [ ] **ZERO shared IPC crates** - No cross-primal dependencies

**Transport Support**:
- [ ] Supports multi-transport binding (native + fallback)
- [ ] Implements graceful fallback (Tier 1 → Tier 2)
- [ ] Zero hardcoded socket paths
- [ ] Runtime transport discovery (not compile-time only)

**Protocol Support**:
- [ ] JSON-RPC 2.0 (required)
- [ ] Protocol negotiation supported (optional tarpc)

**Discovery**:
- [ ] Registers with Songbird on startup
- [ ] Declares capabilities in registration
- [ ] Heartbeat for presence

**Platform Testing**:
- [ ] Tested on Linux (Unix sockets)
- [ ] Tested on Android (abstract sockets or TCP fallback)
- [ ] Cross-device communication verified

---

## Benefits of Standards (Without Shared Code)

### 1. True Primal Autonomy

**With Shared Crate**: All primals coupled to one crate's release cycle  
**With Standards**: Each primal evolves independently at their own pace

### 2. Consistent Behavior Through Protocol

**Problem**: BearDog and Songbird have slightly different transport selection  
**Solution**: Same PROTOCOL (JSON-RPC 2.0), same BEHAVIOR specification, independent CODE

### 3. Reference Patterns Enable Learning

**Problem**: Each primal starts from scratch  
**Solution**: Copy reference patterns, adapt to your needs, own your code

### 4. Protocol Evolution Without Coupling

**With Shared Crate**: Protocol change = version bump = all primals update  
**With Standards**: Protocol spec evolves, primals adopt when ready

### 5. Resilient Architecture

**With Shared Crate**: Bug in shared code affects ALL primals  
**With Standards**: Bug in BearDog's IPC only affects BearDog

### 6. Why "Duplication" is Acceptable

```
Each primal has ~500-1000 lines of IPC code
  → This is NOT wasteful duplication
  → This is HEALTHY independence
  → Each primal owns and understands their IPC
  → No hidden coupling through shared dependencies
```

---

## Related Standards

- `PRIMAL_IPC_PROTOCOL.md` v2.0 - Discovery protocol (JSON-RPC methods)
- `ECOBIN_ARCHITECTURE_STANDARD.md` v2.0 - ecoBin compliance
- `SEMANTIC_METHOD_NAMING_STANDARD.md` - Method naming conventions
- `UNIBIN_ARCHITECTURE_STANDARD.md` - Binary structure

---

**Standard**: Universal IPC Standard v3.0  
**Version**: 3.0.0 (February 3, 2026)  
**Authority**: wateringHole  
**Status**: PROPOSED STANDARD

---

🦀🌍✨ **One Crate, All Platforms, All Protocols!** ✨🌍🦀
