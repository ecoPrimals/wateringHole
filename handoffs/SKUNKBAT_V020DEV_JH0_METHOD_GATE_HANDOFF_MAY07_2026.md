# skunkBat v0.2.0-dev — JH-0 MethodGate Adoption

**Date**: May 7, 2026
**Scope**: JH-0 pre-dispatch capability gate + JH-5 design documentation
**Build**: 356 tests passing, clippy clean, 45 source files (max 725 LOC)

---

## JH-0: MethodGate Pre-Dispatch Authorization (RESOLVED)

Adopted the ecosystem-standard `MethodGate` pattern from primalSpring v0.9.25.

### Architecture

```
incoming RPC → validate JSON-RPC → MethodGate::check() → dispatch()
                                        ↓
                              Public: always pass
                              Protected + token: pass
                              Protected + no token + Permissive: warn + pass
                              Protected + no token + Enforced: -32001 REJECT
```

### Method Classification

| Level | Methods |
|-------|---------|
| Public | `health.*`, `identity.get`, `capabilities.list`, `capability.list`, `lifecycle.*`, `auth.check`, `auth.mode`, `auth.peer_info` |
| Protected | `security.scan`, `security.detect`, `security.respond`, `security.metrics` |

### New Auth Methods

- `auth.check` — returns `{authenticated, mode}`
- `auth.mode` — returns `{mode: "permissive"|"enforced"}`
- `auth.peer_info` — returns `{origin, has_token}`

### Configuration

- `SKUNKBAT_AUTH_MODE=enforced` — reject unauthenticated protected calls
- Default: `permissive` (log + allow for backward compatibility)
- Error: `-32001 PERMISSION_DENIED` with `{method}` in data

### CallerContext

Connection origin tracked per-connection:
- **Unix** — local UDS (trusted)
- **Loopback** — TCP 127.0.0.1/::1
- **Remote** — TCP from non-loopback address

**Files**: `crates/skunk-bat-server/src/ipc/method_gate.rs` (new, 226 LOC)

---

## JH-5: Security Audit Ingestion (DESIGN DOCUMENTED)

The gate emits structured `tracing::warn!` events with fields:
- `method` — the protected method called
- `origin` — connection origin enum
- `caller_uid` / `caller_pid` — future: SO_PEERCRED

These events are the primary signal for JH-5 heterogeneous log consumption.
Full implementation (systemd journal ingestion, BTSP tunnel log parsing,
rhizoCrypt DAG feeding, sweetGrass provenance braids) is deferred pending
ionic token infrastructure (JH-1 → JH-4 from BearDog).

---

## Ecosystem Implications

- primalSpring can mark JH-0 adoption as COMPLETE for skunkBat
- JH-5 is design-documented, implementation deferred (depends on JH-1/JH-4)
- No breaking changes — default mode is permissive
- `auth.*` methods now advertised in `capabilities.list`
- Gate emits ecosystem-standard error code `-32001 PERMISSION_DENIED`
