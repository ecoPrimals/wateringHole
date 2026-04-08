# ToadStool S192 — GAP-MATRIX-12: BTSP Insecure Guard

**Date**: April 8, 2026
**From**: ToadStool team
**To**: primalSpring / BearDog team / biomeOS
**Re**: GAP-MATRIX-12 resolution — `BIOMEOS_INSECURE` guard implementation

---

## Summary

- **GAP-MATRIX-12 RESOLVED**: `validate_insecure_guard()` implemented at server startup
- **Guard behavior**: Refuses start when `FAMILY_ID` (non-default) + `BIOMEOS_INSECURE=1` are both set
- **BTSP awareness**: Startup logging indicates security posture (production/dev mode)
- **11 new tests** covering all environment variable combinations

---

## What Was Implemented

### BTSP Insecure Guard (Phase 1 Compliance)

Per `BTSP_PROTOCOL_STANDARD.md` §Compliance Checklist:

| Environment | Behavior | Status |
|-------------|----------|--------|
| `FAMILY_ID` set (not "default") | Production — BTSP handshake expected | Logged at startup |
| `BIOMEOS_INSECURE=1`, no `FAMILY_ID` | Development — raw cleartext | Allowed |
| `FAMILY_ID` + `BIOMEOS_INSECURE=1` | **Error — refuse to start** | **Implemented** |
| Neither set | Default dev mode | Allowed |

### Changed Files

| File | Change |
|------|--------|
| `crates/core/common/src/primal_sockets/paths.rs` | +`validate_insecure_guard()`, +`is_btsp_required()` |
| `crates/core/common/src/primal_sockets/api.rs` | +`check_insecure_guard()` convenience wrapper |
| `crates/core/common/src/primal_sockets/env.rs` | +`biomeos_insecure` field on `SocketPathEnv` |
| `crates/core/common/src/primal_sockets/mod.rs` | Re-export new APIs |
| `crates/server/src/unibin/mod.rs` | Guard + BTSP awareness logging in `run_server_main()` |
| `crates/cli/src/daemon/server.rs` | Guard in `DaemonServer::start()` |
| Tests (2 files) | 11 new tests covering all env combos |

### Error Message Example

```
BTSP security conflict: FAMILY_ID="production-1" (production)
with BIOMEOS_INSECURE=1 (development). These are mutually exclusive.
Either unset BIOMEOS_INSECURE for production, or unset FAMILY_ID
for development. See BTSP_PROTOCOL_STANDARD.md §Compliance Checklist.
```

---

## Remaining BTSP Work (Phase 2+)

| Item | Status | Notes |
|------|--------|-------|
| Socket naming (`{primal}-{family_id}.sock`) | Already implemented | `socket_filename_for_family()` in unibin |
| `BIOMEOS_INSECURE` guard | **Done (S192)** | Blocks startup on conflict |
| BTSP handshake on connections | Pending Phase 2 | Blocked on BearDog `btsp.session.*` |
| X25519 ephemeral key exchange | Pending Phase 2 | Needs BearDog crypto primitives |
| Cipher negotiation | Pending Phase 2 | `BTSP_CHACHA20_POLY1305` default |
| Length-prefixed framing | Pending Phase 2 | 16 MiB max frame |

---

## References

- `BTSP_PROTOCOL_STANDARD.md` §Compliance Checklist
- `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §Socket Naming
- `GAP-MATRIX-12` in `NUCLEUS_VALIDATION_MATRIX.md`

---

AGPL-3.0-or-later — ecoPrimals sovereign community property
