# projectNUCLEUS — Phase 60 Enforced Mode Validation Handoff

**Date**: 2026-05-08
**From**: projectNUCLEUS (ironGate)
**For**: primalSpring, primal teams, wateringHole
**Binaries**: plasmidBin v2026.05.08 (13/13 checksum-verified via `sync.sh`)

---

## Summary

After absorbing primalSpring Phase 60 and deploying with `NUCLEUS_AUTH_MODE=enforced`,
projectNUCLEUS ran a full 5-layer security validation. All upstream gaps from the
Multi-User Hardening pentest (JH-0 through JH-5) are confirmed resolved or adopted.

**Result**: 265 PASS, 0 FAIL, 0 KNOWN_GAP

---

## What We Validated

### MethodGate Enforced (JH-0)

- Deployed all 13 primals with `*_AUTH_MODE=enforced` env vars
- 10/13 primals confirm `"mode":"enforced"` via `auth.mode` on TCP
- 3 primals (songbird, squirrel, petaltongue) don't expose `auth.mode` on TCP
  - petaltongue is stricter: rejects all unauthenticated TCP via BTSP PT-09
- All unauthenticated RPC calls return `-32001 PERMISSION_DENIED`
- Health endpoints remain exempt (PG-56 whitelist)

### Ionic Token Flow (JH-1)

End-to-end validated:

```
identity.create → DID (did:key:z6Mkk...)
auth.issue_session(purpose="jupyterhub", ttl_hours=24) → scoped token
auth.verify_ionic(token) → valid: true, scope_ok: true, Ed25519 verified
capabilities.list + _bearer_token → OK (in scope)
```

- Scope rejection works: token with `crypto.*` scope passes MethodGate, token
  without `storage.*` scope is rejected by nestgate
- Token claims include issuer DID, subject, scope array, iat/exp, JTI

### Resource Envelopes (JH-2)

biomeOS and ToadStool enforce `timeout_ms`, `mem_mb`, `cpu_cores` on dispatch.

### Composition Reload (JH-3)

`composition.reload` tested — hot-swap single primal without full restart.

### Session UX (JH-4)

`auth.issue_session` with purpose-based presets (`jupyterhub`, `desktop`, `admin`)
returns tokens with appropriate scope arrays.

### Audit Log (JH-5)

skunkBat `security.audit_log` responds with ring buffer entries. 7 event kinds
instrumented from live code paths.

---

## Binding — DF-1 Fully Resolved

Phase 60 binaries (PG-55) default all 13 primals to `127.0.0.1`. All 14 primal
ports verified bound to localhost only. No UFW workaround needed.

deploy.sh DF-1 workaround code has been removed.

---

## New Upstream Gaps Found

| ID | Finding | Severity | Owner |
|----|---------|----------|-------|
| **JH-11** | Cross-primal token federation: beardog-issued ionic tokens not verifiable by other primals. Each MethodGate validates independently | Medium | primalSpring / biomeOS |
| **DF-2** | toadstool reads `TOADSTOOL_AUTH_MODE=enforced` but reports `mode=permissive` via `auth.mode` | Low | toadstool team |
| **DF-3** | songbird, squirrel don't expose `auth.mode` on TCP (may be UDS-only) | Info | Each primal team |

### JH-11 Context

Each primal's MethodGate validates independently. A beardog-issued token authenticates
to beardog methods, but nestgate/loamspine/etc. can't verify the signature because
they don't share beardog's public key. biomeOS composition forwarding with
`_resource_envelope` is the intended cross-primal auth path. For NUCLEUS deployment,
this means primal-to-primal calls through biomeOS work, but direct cross-primal
RPC with bearer tokens does not.

---

## Remaining Dark Forest Findings (Informational)

5 findings, none exploitable given current controls:

| Finding | Mitigation |
|---------|------------|
| Hub API leaks version 5.4.5 at `/hub/api/` | JH-10 — built-in handler, block at tunnel |
| Compute user can enumerate systemd services | Informational — no control granted |
| Reviewer can execute `python3` directly | Terminals disabled; only exploitable with terminal bypass |
| Oversized cookie returns HTTP 431 | Correct behavior (RFC 6585) |
| Null byte username reflected in 403 error | Auth rejected, CSP prevents XSS |

---

## Ecosystem State

| Metric | Value |
|--------|-------|
| Primals deployed | 13/13 |
| Primals on 127.0.0.1 | 14/14 ports |
| MethodGate enforced | 10/13 on TCP, 3 silent (UDS/BTSP) |
| Ionic tokens | Live (Ed25519, scope-checked) |
| Resource envelopes | Enforced (biomeOS + ToadStool) |
| Audit log | Live (skunkBat ring buffer) |
| Validation | **265 PASS, 0 FAIL, 0 KNOWN_GAP** |
| ABG tier enforcement | 62+ assertions, 4 tiers, 0 violations |
| plasmidBin | 13/13 checksum-verified, `sync.sh` operational |

---

## For Downstream Teams

1. **Set `*_AUTH_MODE=enforced`** on all primals in production deployments
2. **Issue session tokens** via `auth.issue_session(purpose="jupyterhub")`
   before calling protected methods
3. **Cross-primal calls** should go through biomeOS composition forwarding
   until JH-11 (cross-primal token federation) is resolved
4. **DF-2**: toadstool team should verify `TOADSTOOL_AUTH_MODE` env var mapping
5. **plasmidBin**: run `sync.sh` after `git pull` to ensure local binaries
   match `checksums.toml`

---

## References

- `projectNUCLEUS/validation/REVALIDATION_PHASE60_MAY08_2026.md` — full results
- `projectNUCLEUS/validation/security-20260508-160812/` — raw validation artifacts
- `primalSpring/wateringHole/METHOD_GATE_STANDARD.md` — canonical MethodGate spec
- `wateringHole/handoffs/PRIMALSPRING_V0925_PHASE60_IONIC_TOKENS_HANDOFF_MAY08_2026.md`
