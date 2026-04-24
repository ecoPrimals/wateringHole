# Songbird v0.2.1 — Wave 167: BTSP Relay Silent-Fail Fix

**Date**: April 15, 2026
**From**: Songbird team
**For**: primalSpring (Phase 45c validation), BearDog, ecosystem
**Wave**: 167
**Supersedes**: Wave 165 handoff (archived)

---

## Summary

Fixed three bugs causing the BTSP relay to silent-fail (primalSpring
reports "server closed connection (no ServerHello)"):

1. **family_seed encoding**: `resolve_family_seed_b64()` was base64-encoding
   the hex seed. BearDog expects the raw hex string per SOURDOUGH standard.
   Replaced with `resolve_family_seed()` — just `trim()` and pass through.

2. **Missing env fallbacks**: Only checked `FAMILY_SEED`. Added
   `BEARDOG_FAMILY_SEED` and `BIOMEOS_FAMILY_SEED` fallbacks (matching
   SOURDOUGH_BTSP_RELAY_PATTERN).

3. **Silent connection drops**: When seed resolution or `btsp.session.create`
   failed, error propagated via `?` without writing an error frame. Both
   `perform_server_handshake_ndjson` and `perform_server_handshake` now send
   `{"error":"handshake_failed","reason":"..."}` for ALL failure modes.
   Additionally, `handle_connection` and `handle_connection_with_peek` write
   a belt-and-suspenders error frame in their Err branches.

## Files Changed

| File | Change |
|------|--------|
| `crates/songbird-orchestrator/src/ipc/btsp.rs` | `resolve_family_seed_b64()` → `resolve_family_seed()` (raw hex, 3 env vars); error frames in both NDJSON + binary handshake paths |
| `crates/songbird-orchestrator/src/bin_interface/server.rs` | Error frame in `handle_connection` Err branch |
| `crates/songbird-orchestrator/src/ipc/pure_rust_server/server/connection.rs` | Error frame in `handle_connection_with_peek` Err branch |
| `crates/songbird-http-client/src/security_rpc_client/btsp.rs` | `btsp_session_create` param renamed `family_seed_b64` → `family_seed`, doc updated |

## Verification

All 7,387 lib tests pass, 0 clippy warnings (`-D warnings`), `cargo fmt` clean.

**To verify BTSP relay with primalSpring:**
```bash
RUST_LOG=songbird_orchestrator::ipc=debug \
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/songbird-${FAMILY_ID}.sock
```

Expected: JSON line with `server_ephemeral_pub`, `challenge`, `version`, `session_id`.
If error: JSON line with `error` and `reason` (no longer zero bytes).

## BTSP Convergence Status

With this fix, Songbird should progress from "partial" to "converged" in the
SOURDOUGH relay table. The full 4-step handshake (create → ServerHello →
ChallengeResponse → verify → HandshakeComplete) is now wired with correct
wire format and error handling matching the SOURDOUGH pattern.

## Reference

- `SOURDOUGH_BTSP_RELAY_PATTERN.md` — extracted relay standard
- `BTSP_WIRE_CONVERGENCE_APR24_2026.md` — updated Songbird entry
