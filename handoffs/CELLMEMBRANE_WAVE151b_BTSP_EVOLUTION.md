# cellMembrane Wave 151b — BTSP ClientHello Evolution

**Date**: 2026-07-26 | **Wave**: 151b | **Author**: cellMembrane team (sporeGate)
**Trigger**: Sub-wave 151b — all primals evolve to BTSP standard before Nest Atomic

---

## Summary

cellMembrane now implements the BTSP `ClientHello` 4-step handshake for all
bearDog UDS communication, matching the songBird reference implementation.

## Architecture

New module: `btsp_client.rs` (sync + async handshake variants)

**Handshake protocol:**
1. Client → `ClientHello { protocol: "btsp", version: 1, client_ephemeral_pub }`
2. Server → `ServerHello { challenge, session_id }`
3. Client → `ChallengeResponse { session_id, hmac: HMAC-SHA256(BTSP_KEY, challenge) }`
4. Server → `HandshakeComplete { cipher, session_id }`

**Key derivation:** `HKDF-SHA256(FAMILY_SEED, "ribocipher-v1", "btsp-challenge")`
— distinct from riboCipher mito key (`"mito-signal"` info param).

## Changed Files

| File | Change |
|------|--------|
| `btsp_client.rs` | **NEW** — 11 tests, sync + async handshake, key derivation, HMAC |
| `plasmid/signing.rs` | BTSP handshake before `crypto.sign_ed25519`, fallback to plain |
| `impulse/primal.rs` | BTSP for bearDog sockets, riboCipher for others, `is_beardog_socket()` |
| `jsonrpc.rs` | `call_btsp()` — async BTSP-aware JSON-RPC variant |
| `tower/timer.rs` | bearDog probe uses `probe_socket_btsp()` instead of `probe_socket()` |
| `lib.rs` | Register `btsp_client` module |

## Health Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,167 (was 1,156) |
| Clippy warnings | 0 |
| Files >800L | 0 |

## For Upstream Primal Teams

cellMembrane BTSP status: **DONE**. Reference the songBird implementation
(`btsp_client.rs` in songBird) or cellMembrane's `btsp_client.rs` for the
handshake pattern. Key requirements:
- `FAMILY_SEED` env var must be available at runtime
- Signal prefix `[0xEC, 0x03]` before handshake
- HMAC-SHA256 with HKDF-derived key (not raw FAMILY_SEED)
