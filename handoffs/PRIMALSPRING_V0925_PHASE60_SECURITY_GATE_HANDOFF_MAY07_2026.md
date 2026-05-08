# primalSpring v0.9.25 — Phase 60 Security Gate Handoff (May 7, 2026)

**From**: primalSpring  
**For**: All primal teams, spring teams, projectNUCLEUS  
**Severity**: Critical (JH-0)  
**Status**: primalSpring reference implementation COMPLETE, ecosystem adoption PENDING

---

## What Changed

primalSpring now ships a **pre-dispatch capability authorization gate** on its
JSON-RPC dispatcher, addressing **JH-0 (Critical)** from the projectNUCLEUS
multi-user hardening pentest. This is the reference implementation that all
primals should adopt.

## The Problem (JH-0)

Every primal's JSON-RPC dispatcher previously accepted unauthenticated calls
from any localhost process. In multi-user compositions (JupyterHub, shared
ironGate), any process could call any method — including destructive ones like
`storage.delete` or `compute.dispatch.submit`.

## The Solution: Method Gate Pattern

### Architecture

```
Connection → CallerContext → MethodGate::check → dispatch_request
                                    │
                              ┌─────┴─────┐
                              │ Public     │ Protected
                              │ → allow    │ → check token
                              └────────────┘
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `MethodAccessLevel` | `Public` (health, identity, capabilities) / `Protected` (everything else) |
| `CallerContext` | Bearer token, peer credentials (SO_PEERCRED), connection origin |
| `MethodGate` | Configurable gate: `Permissive` (log, allow) / `Enforced` (reject -32001) |
| `classify_method()` | Determines access level from method string |

### Error Codes (server-defined range)

| Code | Name | When |
|------|------|------|
| `-32001` | `PERMISSION_DENIED` | Token missing or insufficient scope |
| `-32000` | `UNAUTHORIZED` | Identity could not be established |
| `-32002` | `NOT_READY` | Primal still initializing |

### Public Method Whitelist (exempt from token check)

- `health.*` — liveness and readiness probes
- `identity.get` — primal self-identification
- `capabilities.list` / `capability.list` — capability advertisement
- `lifecycle.status` — running/stopped status
- `auth.check` / `auth.mode` / `auth.peer_info` — gate introspection

### New `auth.*` Methods

| Method | Returns |
|--------|---------|
| `auth.check` | `{ authenticated: bool, enforcement: "permissive"/"enforced" }` |
| `auth.mode` | `{ mode: "permissive"/"enforced" }` |
| `auth.peer_info` | `{ origin: "Unix"/"Loopback"/"Remote", peer: { uid, pid } }` |

### Enforcement Modes

- **Permissive** (default): logs violations but allows all calls. Backward-compatible.
- **Enforced**: rejects unauthenticated calls to protected methods with `-32001`.
- Controlled via `PRIMALSPRING_AUTH_MODE` env var (or primal-specific equivalent).

## What Primals Need To Do

1. **Add error codes** (`-32001`, `-32000`) to your protocol types
2. **Create a method gate module** — classify methods, extract caller context
3. **Wire into your dispatcher** — gate check before dispatch
4. **Register `auth.*` methods** in your capabilities
5. Start in **Permissive** mode — flip to Enforced when ready

Full implementation guide: `primalSpring/wateringHole/METHOD_GATE_STANDARD.md`

## What Also Shipped

- **SeedConfig + OnceLock** replaces `unsafe { env::set_var }` — zero unsafe blocks remaining
- **`PermissionDenied` error variant** in `IpcError` with `is_permission_denied()` query
- **Guidestone Layer 1.6** — validates method gate wiring via live IPC
- **`tools/check_method_gate.sh`** — CI advisory tool
- **369 registered capability methods** (was 366; +3 `auth.*`)
- **666 tests** (618 passed + 48 ignored)
- **PT-09, PT-13** — petalTongue resolved (BTSP Phase 2, NestGate CAS backend)

## Adoption Path

1. **primalSpring** ✅ — reference implementation, permissive default
2. **BearDog** — add `auth.issue_ionic` / `auth.verify_ionic` for token issuance (JH-1)
3. **All primals** — adopt gate pattern, start permissive
4. **Compositions** — flip to enforced per-composition when all primals have the gate
5. **Step 2b** — BTSP auth inside the encrypted tunnel, replacing PAM

## References

- `primalSpring/wateringHole/METHOD_GATE_STANDARD.md` — full ecosystem standard
- `primalSpring/ecoPrimal/src/ipc/method_gate.rs` — reference implementation
- `primalSpring/ecoPrimal/src/bin/primalspring_primal/server.rs` — wiring example
- `infra/wateringHole/handoffs/PROJECTNUCLEUS_MULTIUSER_HARDENING_HANDOFF_MAY07_2026.md` — pentest evidence
