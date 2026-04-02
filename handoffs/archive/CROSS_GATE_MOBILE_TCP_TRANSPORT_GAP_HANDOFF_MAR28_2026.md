# Cross-Gate Mobile TCP Transport Gap — Handoff

**Date**: March 28, 2026
**Source**: primalSpring Phase 18 — Live NUCLEUS + Cross-Gate Federation Validation
**Urgency**: High — blocks full mobile atomic deployment
**Affects**: BearDog, biomeOS, NestGate, Squirrel, Toadstool (all primals needing mobile IPC)

---

## Summary

During live cross-gate deployment validation (Eastgate x86_64 ↔ Pixel 8a aarch64 via ADB),
we confirmed that **GrapheneOS SELinux policy categorically blocks Unix socket (`sock_file`)
creation** from the `shell` execution context. This blocks all primals except Songbird
(which has `--listen` TCP fallback) from running on Android.

## SELinux Evidence

```
avc: denied { create } for name="beardog-pixel.sock"
  scontext=u:r:shell:s0
  tcontext=u:object_r:shell_data_file:s0
  tclass=sock_file permissive=0
```

This denial is absolute — it applies to all paths (`/data/local/tmp/`, `/tmp/`, any writable
filesystem). Abstract sockets may also be blocked (not tested on GrapheneOS specifically).

## Current Mobile IPC Status

| Primal | Mobile IPC | Status | Gap |
|--------|-----------|--------|-----|
| **Songbird** | `--listen 127.0.0.1:9901` | **WORKS** | None — TCP IPC mode exists |
| **BearDog** | Unix socket only | **BLOCKED** | Server hard-exits if socket bind fails |
| **biomeOS api** | Ignores `--port`, forces socket | **BLOCKED** | TCP mode "deprecated", not implemented |
| **biomeOS nucleus** | Waits for primal sockets | **BLOCKED** | No TCP transport awareness |
| **NestGate** | Unix socket only | **NOT TESTED** | Likely same issue |
| **Squirrel** | Abstract socket (`@squirrel`) | **NOT TESTED** | May work if abstract sockets allowed |
| **Toadstool** | CLI-only (no server) | N/A | No IPC needed |

## What Each Primal Team Needs

### BearDog (Critical)

Add `--listen <ADDR>` to `beardog server` for TCP-only JSON-RPC IPC. The TCP JSON-RPC
server already exists in `multi_transport.rs` (line 394, `TcpListener::bind(jsonrpc_addr)`).
The issue is that `server.rs` starts `UnixSocketIpcServer` first and hard-exits at line 196
if the socket doesn't bind within 5 seconds.

**Suggested approach**:
- Add `--listen <ADDR>` CLI flag to `ServerArgs`
- When `--listen` is provided, skip Unix socket creation and start the multi-transport TCP
  JSON-RPC server directly
- Use `BEARDOG_ENABLE_JSONRPC=true` and `BEARDOG_BIND_ADDR` environment variables as fallback
- The `MultiTransportConfig::from_env()` already supports these vars

**Reference**: Songbird's `--listen` implementation is the ecosystem pattern to follow.
Songbird detects `--listen` and uses TCP instead of Unix socket for inter-primal IPC.

### biomeOS (Critical)

1. **`api` mode**: Honor `--port` flag. Currently logs `"HTTP mode deprecated — using Unix
   socket only"` and forces socket bind. When `--port` is provided, bind HTTP/WebSocket on
   that port even if Unix socket fails.

2. **`nucleus` mode**: After spawning primals, check for TCP endpoints (not just socket
   files). Pass `--listen` to child primals on platforms where Unix sockets fail.

3. **`capability.call` gate routing**: The `call()` method in `handlers/capability.rs`
   (line 522) always uses `atomic.primary_endpoint` from `discover_capability()`. It ignores
   any `gate` parameter. For cross-gate federation, it needs to:
   - Check for `gate` in params
   - Look up the gate's endpoint in the capability registry
   - Forward to the gate-specific endpoint instead of primary

4. **`TransportEndpoint`**: Already supports TCP parsing (`tcp://host:port`) — this is correct.

### NestGate, Squirrel (Medium Priority)

Same pattern as BearDog: add `--listen <ADDR>` for TCP-only IPC when Unix sockets are
unavailable. Test on Android via ADB.

## Validated Cross-Gate Pattern

The working pattern for Eastgate ↔ Pixel federation:

```
Eastgate (x86_64):
  biomeOS neural-api (Unix socket) → orchestrates local primals
  BearDog (Unix socket) → crypto
  Songbird (Unix socket) → network
  NestGate (Unix socket) → storage
  Squirrel (abstract socket) → AI

Pixel (aarch64, via ADB):
  Songbird (TCP 127.0.0.1:9901) → network (SELinux: no sockets)
  ADB forward: Pixel:9901 → Eastgate:19901

Federation:
  biomeOS route.register:
    primal=songbird, gate=pixel8a, transport=tcp://127.0.0.1:19901
    capabilities=[network, discovery, http, mesh, birdsong]
```

## Validation Commands (Reproducible)

```bash
# Start Songbird on Pixel (TCP mode)
adb shell "FAMILY_ID=8ff3b864a4bc589a NODE_ID=pixel8a \
  SONGBIRD_DATA_DIR=/data/local/tmp/songbird-data \
  SONGBIRD_PID_DIR=/data/local/tmp/biomeos/pid \
  SONGBIRD_SECURITY_PROVIDER=none \
  nohup /data/local/tmp/biomeos/primals/songbird server \
  --port 9200 --listen 127.0.0.1:9901 > /data/local/tmp/songbird.log 2>&1 &"

# ADB port forward
adb forward tcp:19901 tcp:9901

# Health check from Eastgate
echo '{"jsonrpc":"2.0","method":"health","params":{},"id":1}' | nc -w 3 127.0.0.1 19901

# Register on biomeOS
echo '{"jsonrpc":"2.0","method":"route.register","params":{
  "primal":"songbird","gate":"pixel8a",
  "transport":"tcp://127.0.0.1:19901",
  "capabilities":["network","discovery","http","mesh","birdsong"]
},"id":1}' | nc -U /run/user/1000/biomeos/neural-api-8ff3b864a4bc589a.sock -w 5
```

---

**License**: AGPL-3.0-or-later
