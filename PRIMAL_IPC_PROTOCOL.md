# 🌍 Primal IPC Protocol Standard

**Status**: Official Ecosystem Standard  
**Version**: 2.0.0 (Platform-Agnostic Evolution)  
**v1.0**: January 19, 2026 (Unix-focused)  
**v2.0**: January 30, 2026 (Platform-agnostic)  
**Authority**: wateringHole (ecoPrimals Core Standards)

---

## 📢 **v2.0 UPDATE: Platform-Agnostic Transports** (January 30, 2026)

**Evolution**: From Unix-centric to universal platform support

**What Changed:**
- ✅ Multiple transport support (Unix, abstract, TCP, named pipes, XPC, etc.)
- ✅ Runtime transport discovery (automatic platform detection)
- ✅ Graceful fallback (prefer native, fall back to TCP)
- ✅ Zero platform assumptions (no hardcoded paths)

**Backward Compatibility**: v1.0 behavior (Unix sockets) is v2.0's preferred transport on Linux/macOS

See "Platform-Agnostic Transports (v2.0)" section below for details.

---

## 🎯 PURPOSE

Define a universal, platform-agnostic IPC protocol that enables autonomous primals to discover and communicate with each other **without embedding each other's code**.

---

## 🏛️ CORE PRINCIPLES

### **1. Primal Autonomy**

> "Primals are autonomous organisms that communicate via protocols,  
> NOT by embedding each other's code."

- ✅ Each primal implements the protocol independently
- ✅ No primal depends on another primal's library/crate
- ✅ Standard protocol enables interoperability
- ❌ Cross-embedding is prohibited

### **2. Platform Universality** (Updated v2.0)

> "Write once, run everywhere: Linux, Android, macOS, Windows, iOS, WASM, embedded."

**v1.0 Approach (Unix-focused):**
- ✅ Unix socket API via tokio
- ⚠️ Assumed Unix sockets available on all platforms
- ⚠️ Limited to Unix-like systems

**v2.0 Approach (Platform-agnostic):**
- ✅ Multiple transport support (Unix, abstract, TCP, named pipes, XPC, etc.)
- ✅ Runtime transport discovery (automatic platform detection)
- ✅ Graceful fallback (prefer native, fall back to TCP localhost)
- ✅ Zero platform assumptions (no `#[cfg(unix)]` or hardcoded paths)
- ✅ Universal: Works on Linux, Android, Windows, macOS, iOS, WASM, embedded

### **3. Capability-Based Discovery**

> "Find services by what they do, not by hardcoded names."

- ✅ Runtime discovery via registry (Songbird)
- ✅ Capability-based queries ("who has crypto?")
- ✅ Dynamic service resolution
- ❌ No hardcoded primal dependencies

---

## 📋 PROTOCOL SPECIFICATION

### **Transport Layer**

**Always**: `tokio::net::{UnixStream, UnixListener}`

```rust
use tokio::net::{UnixStream, UnixListener};

// Create socket (server)
let listener = UnixListener::bind("/primal/myname").await?;

// Connect to socket (client)
let stream = UnixStream::connect("/primal/othername").await?;
```

**Platform Handling**:
- **Unix** (Linux, macOS, BSD): Native Unix domain sockets
- **Windows**: Named pipes with Unix socket API (via tokio)
- **Other**: TCP localhost fallback (if needed)

**Key**: Application code NEVER changes! tokio handles platform!

---

### **Namespace Convention**

**Standard Path Format**: `/primal/{primal-name}`

**Examples**:
```
/primal/beardog    - BearDog crypto service
/primal/songbird   - Songbird network orchestration
/primal/squirrel   - Squirrel AI/MCP assistant
/primal/nestgate   - NestGate storage service
```

**Rules**:
- ✅ Always lowercase
- ✅ Always `/primal/` prefix
- ✅ Primal name only (no version, no UUID)
- ❌ No spaces or special characters

---

### **Message Format**

**Standard**: JSON-RPC 2.0

**Method Naming**: See `SEMANTIC_METHOD_NAMING_STANDARD.md` for semantic namespace conventions (v2.0+)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "domain.operation",  // e.g., "crypto.encrypt", "http.get"
    "params": {
        "key": "value"
    },
    "id": 1
}
```

**Success Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "data": "value"
    },
    "id": 1
}
```

**Error Response**:
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32601,
        "message": "Method not found",
        "data": null
    },
    "id": 1
}
```

**Standard Error Codes**:
- `-32700`: Parse error
- `-32600`: Invalid request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

---

## 🔍 DISCOVERY PROTOCOL

### **Songbird as Discovery Service**

**Role**: Songbird maintains the service registry and answers discovery queries.

**NOT a library**: Primals communicate with Songbird via JSON-RPC, not by importing code.

### **Discovery Methods**

#### **1. Register Service**

**When**: Primal startup  
**To**: Songbird (`/primal/songbird`)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "ipc.register",
    "params": {
        "name": "beardog",
        "endpoint": "/primal/beardog",
        "capabilities": ["crypto", "btsp", "ed25519", "x25519"],
        "version": "2.7.0",
        "metadata": {
            "description": "Pure Rust cryptographic services"
        }
    },
    "id": 1
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "registered": true,
        "endpoint": "/primal/beardog"
    },
    "id": 1
}
```

#### **2. Resolve Service**

**When**: Need to find another primal  
**To**: Songbird (`/primal/songbird`)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "ipc.resolve",
    "params": {
        "primal": "beardog"
    },
    "id": 2
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "name": "beardog",
        "endpoint": "/primal/beardog",
        "capabilities": ["crypto", "btsp"],
        "version": "2.7.0",
        "available": true
    },
    "id": 2
}
```

#### **3. Find by Capability**

**When**: Need a service with specific capability  
**To**: Songbird (`/primal/songbird`)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "ipc.find_capability",
    "params": {
        "capability": "crypto"
    },
    "id": 3
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "services": [
            {
                "name": "beardog",
                "endpoint": "/primal/beardog",
                "capabilities": ["crypto", "btsp"],
                "version": "2.7.0"
            }
        ]
    },
    "id": 3
}
```

#### **4. List All Services**

**When**: System discovery, health checks  
**To**: Songbird (`/primal/songbird`)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "ipc.list",
    "params": {},
    "id": 4
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "services": [
            {
                "name": "beardog",
                "endpoint": "/primal/beardog",
                "capabilities": ["crypto", "btsp"],
                "available": true
            },
            {
                "name": "squirrel",
                "endpoint": "/primal/squirrel",
                "capabilities": ["ai", "mcp"],
                "available": true
            }
        ],
        "count": 2
    },
    "id": 4
}
```

#### **5. Heartbeat**

**When**: Periodic (every 30-60 seconds)  
**To**: Songbird (`/primal/songbird`)

**Request**:
```json
{
    "jsonrpc": "2.0",
    "method": "ipc.heartbeat",
    "params": {
        "name": "beardog"
    },
    "id": 5
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "acknowledged": true,
        "timestamp": "2026-01-19T20:00:00Z"
    },
    "id": 5
}
```

---

## 🔧 IMPLEMENTATION GUIDE

### **For Server (Listening Primal)**

```rust
use tokio::net::UnixListener;
use serde_json::json;

async fn start_server() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Create socket
    let listener = UnixListener::bind("/primal/myprimal").await?;
    println!("✅ Listening on /primal/myprimal");
    
    // 2. Register with Songbird
    register_with_songbird().await?;
    
    // 3. Accept connections
    loop {
        let (mut stream, _addr) = listener.accept().await?;
        
        tokio::spawn(async move {
            // Handle JSON-RPC requests
            handle_connection(stream).await;
        });
    }
}

async fn register_with_songbird() -> Result<(), Box<dyn std::error::Error>> {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    
    // Connect to Songbird
    let mut stream = tokio::net::UnixStream::connect("/primal/songbird").await?;
    
    // Send registration
    let request = json!({
        "jsonrpc": "2.0",
        "method": "ipc.register",
        "params": {
            "name": "myprimal",
            "endpoint": "/primal/myprimal",
            "capabilities": ["capability1", "capability2"],
            "version": "1.0.0"
        },
        "id": 1
    });
    
    let request_bytes = serde_json::to_vec(&request)?;
    stream.write_all(&request_bytes).await?;
    stream.write_all(b"\n").await?;  // Message delimiter
    
    // Read response
    let mut buf = vec![0u8; 4096];
    let n = stream.read(&mut buf).await?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    
    println!("✅ Registered: {:?}", response);
    
    Ok(())
}
```

### **For Client (Connecting Primal)**

```rust
use tokio::net::UnixStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use serde_json::json;

async fn call_service(
    primal: &str,
    method: &str,
    params: serde_json::Value
) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    // 1. Resolve primal via Songbird (optional, can cache)
    let endpoint = resolve_primal(primal).await?;
    
    // 2. Connect directly to target primal
    let mut stream = UnixStream::connect(&endpoint).await?;
    
    // 3. Send JSON-RPC request
    let request = json!({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    });
    
    let request_bytes = serde_json::to_vec(&request)?;
    stream.write_all(&request_bytes).await?;
    stream.write_all(b"\n").await?;
    
    // 4. Read response
    let mut buf = vec![0u8; 8192];
    let n = stream.read(&mut buf).await?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    
    // 5. Extract result
    if let Some(result) = response.get("result") {
        Ok(result.clone())
    } else if let Some(error) = response.get("error") {
        Err(format!("RPC Error: {:?}", error).into())
    } else {
        Err("Invalid response".into())
    }
}

async fn resolve_primal(name: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut stream = UnixStream::connect("/primal/songbird").await?;
    
    let request = json!({
        "jsonrpc": "2.0",
        "method": "ipc.resolve",
        "params": { "primal": name },
        "id": 1
    });
    
    let request_bytes = serde_json::to_vec(&request)?;
    stream.write_all(&request_bytes).await?;
    stream.write_all(b"\n").await?;
    
    let mut buf = vec![0u8; 4096];
    let n = stream.read(&mut buf).await?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    
    let endpoint = response["result"]["endpoint"]
        .as_str()
        .ok_or("No endpoint in response")?;
    
    Ok(endpoint.to_string())
}
```

---

## 📊 COMPLETE EXAMPLE: Squirrel → BearDog

### **Scenario**: Squirrel needs to sign data with BearDog

```rust
// In Squirrel (autonomous, no BearDog import!):

use tokio::net::UnixStream;
use serde_json::json;

async fn sign_data(data: &str) -> Result<String, Box<dyn std::error::Error>> {
    // 1. Find crypto service (capability-based!)
    let crypto_service = find_by_capability("crypto").await?;
    
    // 2. Connect directly
    let mut stream = UnixStream::connect(&crypto_service).await?;
    
    // 3. Call sign method (BearDog's API)
    let request = json!({
        "jsonrpc": "2.0",
        "method": "crypto.sign",
        "params": {
            "data": data,
            "algorithm": "ed25519"
        },
        "id": 1
    });
    
    // Send request
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    let request_bytes = serde_json::to_vec(&request)?;
    stream.write_all(&request_bytes).await?;
    stream.write_all(b"\n").await?;
    
    // Read response
    let mut buf = vec![0u8; 8192];
    let n = stream.read(&mut buf).await?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    
    // Extract signature
    let signature = response["result"]["signature"]
        .as_str()
        .ok_or("No signature in response")?;
    
    Ok(signature.to_string())
}

async fn find_by_capability(cap: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut stream = UnixStream::connect("/primal/songbird").await?;
    
    let request = json!({
        "jsonrpc": "2.0",
        "method": "ipc.find_capability",
        "params": { "capability": cap },
        "id": 1
    });
    
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    stream.write_all(&serde_json::to_vec(&request)?).await?;
    stream.write_all(b"\n").await?;
    
    let mut buf = vec![0u8; 4096];
    let n = stream.read(&mut buf).await?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    
    let endpoint = response["result"]["services"][0]["endpoint"]
        .as_str()
        .ok_or("No service found")?;
    
    Ok(endpoint.to_string())
}
```

**Key Points**:
- ✅ Squirrel has ZERO BearDog imports
- ✅ Squirrel has ZERO Songbird imports
- ✅ Only tokio (ecosystem standard runtime)
- ✅ Uses standard protocol (JSON-RPC)
- ✅ Capability-based discovery (finds "crypto", not "beardog")
- ✅ Direct peer-to-peer communication

---

## 🌟 BENEFITS

### **1. Primal Autonomy** ✅

```
Each primal:
  - Implements protocol independently
  - Zero code dependencies on other primals
  - Can evolve without coordination
  - TRUE autonomous organism
```

### **2. Platform Universality** ✅

```
Application code:
  - ALWAYS uses UnixStream
  - ZERO #[cfg] conditionals
  - Works on Linux, macOS, Windows, RISC-V
  - tokio handles platform differences
```

### **3. Capability-Based Discovery** ✅

```
Runtime discovery:
  - Find by "what they do" not "who they are"
  - No hardcoded dependencies
  - Dynamic service resolution
  - Resilient architecture
```

### **4. Performance** ✅

```
Direct communication:
  - Peer-to-peer after discovery
  - Zero proxy overhead
  - Native socket performance
  - Minimal latency
```

---

## 📋 COMPLIANCE CHECKLIST

### **For Primal to be IPC-Compliant**

- [ ] **Transport**: Uses `tokio::net::UnixStream` exclusively
- [ ] **Namespace**: Binds to `/primal/{name}`
- [ ] **Format**: Uses JSON-RPC 2.0
- [ ] **Registration**: Registers with Songbird on startup
- [ ] **Discovery**: Resolves services via Songbird
- [ ] **Capabilities**: Declares capabilities in registration
- [ ] **Heartbeat**: Sends periodic heartbeat to Songbird
- [ ] **Autonomy**: ZERO imports from other primals
- [ ] **Platform**: ZERO `#[cfg(unix)]` or `#[cfg(windows)]`

---

## 🔄 VERSION HISTORY

### **v1.0.0** (January 19, 2026)

- Initial standard release
- JSON-RPC 2.0 protocol
- Unix socket transport
- Songbird discovery service
- Capability-based queries
- Standard namespace (`/primal/*`)

---

## 📚 REFERENCES

### **Related Standards**

- JSON-RPC 2.0 Specification: https://www.jsonrpc.org/specification
- Unix Domain Sockets: POSIX.1-2008
- tokio Documentation: https://docs.rs/tokio/

### **ecoPrimals Standards**

- `UNIBIN_ARCHITECTURE_STANDARD.md`
- `ECOBIN_ARCHITECTURE_STANDARD.md`
- `GENOMEBIN_ARCHITECTURE_STANDARD.md`
- `TOWER_ATOMIC_ARCHITECTURE.md` (BearDog)

### **Implementation Examples**

- BearDog: Tower Atomic (JSON-RPC over Unix sockets)
- Songbird: Universal IPC service
- Squirrel: AI delegation via protocol

---

## 🎯 SUMMARY

**Primal IPC Protocol v1.0** enables:

- ✅ **Autonomous primals** (no cross-embedding)
- ✅ **Universal deployment** (all platforms)
- ✅ **Dynamic discovery** (capability-based)
- ✅ **Direct communication** (peer-to-peer)
- ✅ **Standard protocol** (JSON-RPC 2.0)
- ✅ **TRUE PRIMAL architecture** (runtime discovery only)

**Core Pattern**:
```
1. Register with Songbird (declare capabilities)
2. Discover via Songbird (find by capability)
3. Connect directly (peer-to-peer Unix socket)
4. Communicate via JSON-RPC 2.0
```

---

**Standard**: `PRIMAL_IPC_PROTOCOL.md`  
**Version**: 1.0.0  
**Authority**: wateringHole  
**Status**: Official Ecosystem Standard

🌍🦀✨ **Universal communication through protocol, not embedding!** ✨🦀🌍

