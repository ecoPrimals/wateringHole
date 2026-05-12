# biomeOS v3.47 — Resource Envelope Enforcement (JH-2) + Composition Hot-Reload (JH-3)

**Date**: May 8, 2026
**Audit Items**: JH-2 (High), JH-3 (Medium)
**Status**: RESOLVED for biomeOS
**primalSpring Reference**: v0.9.25 Phase 60, BearDog JH-1 ionic tokens

---

## JH-2: Token-Carried Resource Envelope — RESOLVED

### What Changed

biomeOS now parses ionic token claims locally and enforces scope, expiry,
and resource envelope constraints at the MethodGate layer.

#### Ionic Token Claims Parsing

```
Token format: base64(header).base64(payload).base64(signature)
Payload: { iss, sub, scope, iat, exp, jti, resources? }
```

`IonicTokenClaims::parse(token)` decodes the payload segment and extracts:
- **scope** — glob patterns matching primalSpring standard
- **exp** — Unix epoch expiry
- **resources** — optional `ResourceEnvelope`

#### ResourceEnvelope

```rust
pub struct ResourceEnvelope {
    pub mem: Option<u64>,              // max bytes
    pub cpu: Option<f64>,              // max cores
    pub method_allowlist: Option<Vec<String>>,
}
```

#### Scope Matching

`scope_covers_method(scope, method)`:
- `"*"` matches everything
- `"prefix.*"` matches `prefix.anything` (dot-boundary)
- Exact string match otherwise

#### Enforcement in MethodGate::check()

In `Enforced` mode (`BIOMEOS_AUTH_MODE=enforced`):

1. No token → `-32001 PERMISSION_DENIED`
2. Expired token → `-32001`
3. Scope doesn't cover method → `-32001`
4. Method not in `method_allowlist` → `-32001`

In `Permissive` mode (default): all checks log warnings but allow.

#### Resource Checking API

`IonicTokenClaims` exposes:
- `resource_allowed(mem, cpu)` — checks request against envelope limits
- `method_in_allowlist(method)` — checks method against allowlist
- `is_expired()` — checks current time against `exp`

These are available for downstream enforcement (e.g., ToadStool's
`compute.dispatch.submit` can call `claims.resource_allowed()` before
allocating resources).

#### Bug Fix: _bearer_token Leak

Semantic-fallback routing (unknown `domain.operation` methods) previously
forwarded `_bearer_token` inside the `args` object to downstream primals.
Fixed: `_bearer_token` is now stripped before forwarding.

---

## JH-3: Composition Hot-Reload — RESOLVED

### New Method: `composition.reload`

```json
{
  "jsonrpc": "2.0",
  "method": "composition.reload",
  "params": {
    "name": "toadstool",
    "socket_path": "/run/user/1000/biomeos/toadstool-nucleus01.sock"
  },
  "id": 1
}
```

**Flow**:
1. Verify primal is registered in the composition
2. Graceful apoptosis of the existing instance
3. Brief drain pause (250ms) for in-flight requests
4. Re-register at the new socket (or same socket if not specified)
5. Health-check the restarted primal
6. Return `{ reloaded, name, socket_path, healthy }`

**Use case**: JupyterHub deployments can swap a single primal (e.g., after
a config change or binary update) without `systemctl restart` of the entire
NUCLEUS stack.

---

## Summary of JH Items

| Item | Severity | Status |
|------|----------|--------|
| JH-0 | Critical | **RESOLVED** (v3.46) — MethodGate wired |
| JH-2 | High | **RESOLVED** (v3.47) — Resource envelope enforcement |
| JH-3 | Medium | **RESOLVED** (v3.47) — composition.reload |

---

## Test Results

- 7,911 tests (0 failures, fully concurrent)
- `cargo clippy --all-targets`: 0 warnings
- `cargo fmt --check`: clean
