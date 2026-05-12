# Songbird v0.2.1 — Wave 168: BTSP Routing Bug + Seed Encoding Fix

**Date**: April 24, 2026
**From**: Songbird team
**For**: primalSpring (Phase 45c validation), BearDog, ecosystem
**Wave**: 168
**Supersedes**: Wave 167 handoff (archived)

---

## Summary

Two root causes fixed for guidestone error "Neural API error for
btsp.session.create: Method not found: capability.call":

### 1. SecurityRpcClient routing (the primary failure)

`SecurityRpcClient::new(crypto_socket)` in `app/core/mod.rs` delegated to
`new_neural_api()`, wrapping ALL calls in Neural API's `capability.call`
wrapper. BearDog doesn't understand `capability.call` and returned
"Method not found".

**Fix**: Changed to `SecurityRpcClient::new_direct(crypto_socket)` since
`crypto_socket` (discovered via `security_crypto_ipc_socket_from_env()`)
IS the BearDog socket. BTSP relay and all crypto operations now talk
directly to BearDog using actual method names via `semantic_to_actual()`.

### 2. family_seed encoding

`resolve_family_seed()` (Wave 167) passed the raw env string to BearDog.
BearDog's `btsp.session.create` base64-decodes the `family_seed` param
internally.

**Fix**: `resolve_family_seed()` now base64-encodes the trimmed raw env
string before returning. The SOURDOUGH doc's "do NOT base64-encode"
comment was incorrect for this parameter.

## Files Changed

| File | Change |
|------|--------|
| `crates/songbird-orchestrator/src/app/core/mod.rs` | `SecurityRpcClient::new()` → `new_direct()` |
| `crates/songbird-orchestrator/src/ipc/btsp.rs` | `resolve_family_seed()` base64-encodes raw env string |
| `crates/songbird-http-client/src/security_rpc_client/btsp.rs` | `btsp_session_create` doc updated for correct encoding |

## Verification

All 7,387 lib tests pass, 0 clippy warnings (`-D warnings`), `cargo fmt` clean.

**To verify BTSP relay:**
```bash
RUST_LOG=songbird_orchestrator::ipc=debug \
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/songbird-${FAMILY_ID}.sock
```

Expected: JSON line with `server_ephemeral_pub`, `challenge`, `version`, `session_id`.

Full validation: `primalspring_guidestone` should show `btsp:Tower:discovery: BTSP authenticated` — gets us to 10/13.

## Reference

- `SOURDOUGH_BTSP_RELAY_PATTERN.md` — relay pattern (note: family_seed encoding guidance is wrong)
- `BTSP_WIRE_CONVERGENCE_APR24_2026.md` — updated Songbird entry
