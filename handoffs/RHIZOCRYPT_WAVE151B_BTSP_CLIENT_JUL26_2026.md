# rhizoCrypt Wave 151b — BTSP Client-Side Handshake

**Date**: Jul 26, 2026 | **Commit**: `e832b94` | **Wave**: 151b

## Summary

rhizoCrypt now implements the consumer-side BTSP `ClientHello` 4-step
handshake for outbound UDS connections to bearDog and other BTSP-strict
peers. When `BEARDOG_UDS_REQUIRE_BTSP=1` is set, all outbound UDS
connections automatically use NDJSON framing with BTSP authentication
instead of HTTP-over-UDS.

## What Changed

| Component | Change |
|-----------|--------|
| `btsp_client.rs` (new) | 4-step BTSP handshake: `ClientHello` → `ServerHello` → `ChallengeResponse` → `HandshakeComplete` |
| `btsp_uds.rs` (new) | `BtspUnixAdapter`: NDJSON JSON-RPC over BTSP-authenticated UDS |
| `AdapterFactory` | Auto-selects `BtspUnixAdapter` when BTSP strict mode is detected |
| `transport.rs` | `send_jsonrpc_request` performs fail-closed BTSP handshake on Unix streams |

## BTSP Status: DONE

rhizoCrypt's BTSP status is now **DONE** per the Wave 151b standard:

- Client-side `ClientHello` handshake implemented
- HMAC-SHA256 challenge-response matches bearDog expectations
- Family seed resolution: `RHIZOCRYPT_FAMILY_SEED` → `FAMILY_SEED` → `BEARDOG_FAMILY_SEED`
- Strict mode detection via `BEARDOG_UDS_REQUIRE_BTSP=1` or `BTSP_STRICT_MODE=1`

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,886 (+8) |
| Source files | 225 `.rs` |
| Lines | ~61,967 |
| Coverage | 93.83% |
| Clippy | 0 warnings |
| cargo deny | CLEAN |

## Env Vars Added

| Variable | Purpose |
|----------|---------|
| `BEARDOG_UDS_REQUIRE_BTSP` | Activate client-side BTSP handshake (`1`) |
| `BTSP_STRICT_MODE` | Alias for above |
| `BEARDOG_FAMILY_SEED` | Fallback family seed for client handshake |
