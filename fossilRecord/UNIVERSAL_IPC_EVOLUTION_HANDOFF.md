# Universal IPC Evolution - Implementation Handoff

**Date**: February 3, 2026  
**Status**: READY FOR IMPLEMENTATION  
**Priority**: High (Enables cross-device NUCLEUS)  
**Catalyst**: Pixel 8a deployment + cross-device AI coordination

---

## Summary

This handoff describes the **behavioral standards** for platform-agnostic IPC that each primal implements **independently in their own codebase**.

**Key Principle**: Primals enact their own evolution toward standards. NO shared crates.

---

## Core Philosophy

### Primal Autonomy

> "Primals are autonomous organisms that communicate via PROTOCOLS, not by embedding each other's code."

**What This Means**:
- ✅ Each primal owns their IPC implementation
- ✅ Standards define WHAT (behavior, protocol)
- ✅ Primals decide HOW (their own code)
- ❌ NO shared `primal-ipc` crate
- ❌ NO cross-primal dependencies

---

## Current State

### Problem: Duplicated IPC Code

| Primal | IPC Implementation | Lines | Platform Support |
|--------|-------------------|-------|------------------|
| **BearDog** | `beardog-tunnel/platform/*` | ~800 | Unix, Abstract, TCP |
| **Songbird** | `songbird-universal-ipc/*` | ~1200 | Unix, Abstract, TCP, WASM |
| **Toadstool** | Custom | ~300 | Unix only |
| **NestGate** | Custom | ~200 | Unix only |
| **Squirrel** | Custom | ~400 | Unix only |

**Total**: ~2900 lines of duplicated/similar IPC code

### Real-World Failure (Feb 3, 2026)

```
Pixel 8a (GrapheneOS):
  BearDog --socket /data/local/tmp/biomeos/sockets/beardog.sock
  Error: Failed to bind Unix socket: /data/local/tmp/biomeos/sockets/beardog.sock
  
Root Cause: SELinux blocks filesystem Unix sockets
Solution: Abstract sockets (@biomeos_beardog) or TCP fallback
Problem: BearDog binary lacks --listen flag for TCP
```

**Learning**: Each primal re-implements transport selection differently, leading to inconsistent platform support.

---

## Target State

### Solution: Each Primal Implements Standard

Each primal evolves their own IPC code to meet the standard:

```
BearDog:
  └── crates/beardog-tunnel/src/platform/   # THEIR code

Songbird:
  └── crates/songbird-universal-ipc/        # THEIR code

Other Primals:
  └── src/ipc/ or crates/primal-ipc/        # THEIR code
```

**NO shared crate. Each primal owns their implementation.**

### Benefits (of Standards Without Shared Code)

1. **True autonomy** - primals evolve independently
2. **No version coupling** - update when YOU are ready
3. **Owned code** - understand and debug your own IPC
4. **Resilient** - bug in BearDog doesn't affect Songbird
5. **Protocol alignment** - same behavior through spec, not dependency

---

## Implementation Plan (Each Primal Evolves Independently)

### Phase 1: Audit Current State (Each Team)

Each primal team audits their current IPC implementation:

**BearDog Team**:
```bash
# Already has excellent support
ls phase1/beardog/crates/beardog-tunnel/src/platform/
# unix.rs, android.rs, tcp_ipc/, etc.
```

**Songbird Team**:
```bash
# Already has comprehensive support
ls phase1/songbird/crates/songbird-universal-ipc/src/platform/
# unix.rs, android.rs, fallback.rs, etc.
```

**Other Primal Teams**:
```bash
# Audit what you have, plan what you need
grep -r "UnixListener\|TcpListener" your-primal/src/
```

---

### Phase 2: Evolve Each Primal's IPC (Each Team)

**BearDog Evolution Tasks**:
1. ✅ Unix sockets (implemented)
2. ✅ Abstract sockets (implemented)
3. ✅ TCP IPC (implemented)
4. ⏳ Ensure all transports bind on startup
5. ⏳ Test on Pixel 8a (Android)

**Songbird Evolution Tasks**:
1. ✅ All transports (implemented)
2. ✅ Multi-transport discovery (implemented)
3. ⏳ Protocol negotiation for tarpc (future)

**Other Primals Evolution Tasks**:
1. Copy reference patterns from `UNIVERSAL_IPC_STANDARD_V3.md`
2. Implement in YOUR codebase (not a dependency)
3. Test on target platforms

---

### Phase 3: Cross-Primal Testing (Coordination)

Each primal tests interoperability:

```bash
# BearDog team starts their server
./beardog server

# Songbird team connects via standard protocol
echo '{"jsonrpc":"2.0","method":"health","id":1}' | nc -U /path/to/beardog.sock

# Same protocol works regardless of implementation details
```

**Key Point**: Interoperability through PROTOCOL, not shared code.

---

### Phase 4: Protocol Evolution (Future)

When tarpc is desired:

1. **Update the STANDARD** (this document)
2. **Each primal implements tarpc** in their own codebase
3. **Protocol negotiation** allows gradual adoption
4. **NO shared tarpc crate** - each primal owns their implementation

---

## Code References

### BearDog Platform Implementation (to extract)

```
phase1/beardog/crates/beardog-tunnel/src/platform/
├── mod.rs       # PlatformSocket trait, endpoint types (255 lines)
├── unix.rs      # Unix socket implementation (120 lines)
├── android.rs   # Abstract socket implementation (100 lines)
├── windows.rs   # Named pipe stub (50 lines)
├── ios.rs       # XPC stub (40 lines)
└── wasm.rs      # In-process stub (30 lines)

phase1/beardog/crates/beardog-tunnel/src/tcp_ipc/
├── mod.rs       # Module declaration
├── server.rs    # TCP IPC server (197 lines)
└── client.rs    # TCP IPC client (72 lines)
```

### Songbird Universal IPC (to extract)

```
phase1/songbird/crates/songbird-universal-ipc/src/
├── platform/
│   ├── mod.rs        # Platform detection, multi-transport (340 lines)
│   ├── unix.rs       # Unix implementation (180 lines)
│   ├── android.rs    # Abstract sockets (150 lines)
│   ├── fallback.rs   # TCP fallback (100 lines)
│   ├── windows.rs    # Named pipes (80 lines)
│   ├── ios.rs        # XPC (50 lines)
│   └── wasm.rs       # In-process (40 lines)
├── endpoint.rs       # NativeEndpoint enum
├── error.rs          # Error types
├── ipc.rs            # IPC client
└── service.rs        # Service abstraction
```

---

## Testing Strategy

### Unit Tests (in `primal-ipc`)

```rust
#[cfg(test)]
mod tests {
    #[tokio::test]
    async fn test_unix_socket_roundtrip() {
        let server = PrimalServer::start("test").await.unwrap();
        let client = PrimalClient::connect("test").await.unwrap();
        
        let response = client.call("echo", json!({"msg": "hello"})).await;
        assert_eq!(response["msg"], "hello");
    }
    
    #[tokio::test]
    async fn test_tcp_fallback() {
        let server = PrimalServer::builder("test")
            .with_transports(&[Transport::Tcp { port: 0 }])  // Random port
            .start()
            .await
            .unwrap();
        
        // Should connect via TCP
        let client = PrimalClient::connect("test").await.unwrap();
        assert!(client.transport_info().is_tcp());
    }
    
    #[tokio::test]
    #[cfg(target_os = "linux")]
    async fn test_abstract_socket() {
        let server = PrimalServer::builder("test")
            .with_transports(&[Transport::AbstractSocket { name: "@test".into() }])
            .start()
            .await
            .unwrap();
        
        let client = PrimalClient::connect("test").await.unwrap();
        assert!(client.transport_info().is_abstract());
    }
}
```

### Integration Tests (cross-primal)

```bash
# Test BearDog → Songbird communication
./beardog server &
./songbird server --beardog-socket /run/user/1000/biomeos/beardog.sock &

# Verify registration
echo '{"jsonrpc":"2.0","method":"ipc.list","id":1}' | nc -U /tmp/songbird.sock
# Should show beardog registered
```

### Platform Tests (CI matrix)

```yaml
# .github/workflows/ipc-tests.yml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        target: [x86_64-unknown-linux-musl, aarch64-unknown-linux-musl]
    
    steps:
      - uses: actions/checkout@v4
      - run: cargo test -p primal-ipc --all-features
```

---

## Evolution Timeline (Each Primal at Their Own Pace)

### Immediate (When Ready)

Each primal team:
- [ ] Audit current IPC implementation
- [ ] Identify missing transports
- [ ] Plan evolution toward standard

### Short-Term (1-2 Weeks)

BearDog:
- [ ] Ensure multi-transport server binds all available
- [ ] Test on Pixel 8a (Android)
- [ ] Document any issues for standard update

Songbird:
- [ ] Already compliant - validate against standard
- [ ] Document reference patterns for other primals

### Medium-Term (2-4 Weeks)

Other Primals (Toadstool, NestGate, Squirrel):
- [ ] Implement multi-transport support
- [ ] Use reference patterns from standard
- [ ] Test cross-device

### Future (When Beneficial)

- [ ] tarpc protocol support (each primal implements)
- [ ] Protocol negotiation standard update
- [ ] New platform support (Windows, iOS)

---

## Success Metrics

| Metric | Before | Target |
|--------|--------|--------|
| **Primal autonomy** | Varies | 100% (no cross-embedding) |
| **Android support** | BearDog ✅, Songbird ✅, Others ❌ | All primals |
| **Transport fallback** | Manual selection | Automatic (Tier 1 → Tier 2) |
| **Protocol compliance** | Mostly compliant | 100% JSON-RPC 2.0 |
| **Cross-device** | Partial | Full (via TCP fallback) |

**Note**: Lines of code is NOT a metric. Each primal owning ~500-1000 lines of IPC code is HEALTHY autonomy, not wasteful duplication.

---

## Related Documents

- `wateringHole/UNIVERSAL_IPC_STANDARD_V3.md` - Full specification
- `wateringHole/PRIMAL_IPC_PROTOCOL.md` - Discovery protocol
- `wateringHole/ECOBIN_ARCHITECTURE_STANDARD.md` - ecoBin compliance
- `biomeOS/docs/sessions/feb03-2026/NUCLEUS_VALIDATION_FEB03_2026.md` - Deployment findings

---

## Contact

**Standard Owner**: wateringHole Core Team  
**Implementation Lead**: TBD (first primal to migrate)  
**Review**: All primal teams

---

**Created**: February 3, 2026  
**Status**: READY FOR IMPLEMENTATION  
**Priority**: HIGH

---

🦀🔗✨ **Unified IPC = Universal Deployment** ✨🔗🦀
