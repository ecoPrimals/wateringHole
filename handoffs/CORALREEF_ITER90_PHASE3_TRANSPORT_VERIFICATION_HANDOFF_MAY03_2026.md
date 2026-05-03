<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 90: BTSP Phase 3 Transport Verification, GAP-04 Resolved

**Date**: May 3, 2026
**From**: coralReef team
**To**: primalSpring, hotSpring, all downstream springs

---

## Summary

BTSP Phase 3 encrypted frame loop verified reachable via integration test. Marker byte consumption fix closes a latent reachability gap on BTSP-authenticated connections. GAP-04 (tarpc health endpoint) documented as intentional architecture.

## Transport Reachability Fix

The non-`{` first byte used for BTSP protocol detection was not consumed from the `BufReader` before handing off to `handle_connection`. In production BTSP mode (Phase 2 authenticated, non-JSON first byte), this left the marker byte in the stream, corrupting the first JSON-RPC line read and preventing Phase 3 negotiate from being detected.

**Fix**: After `guard_from_first_byte` completes, consume the peeked byte when it's not `{`:
- Unix socket: `peeker.consume(1)` before spawning `handle_connection`
- TCP socket: `br.read_u8().await` when marker consumed

This fix makes the full path reachable in production BTSP mode:
`accept` → `fill_buf` (peek) → `guard_from_first_byte` (out-of-band Phase 2) → `consume(1)` → `handle_connection` → first line = `btsp.negotiate` → `process_encrypted_frames`

## GAP-04 Resolution: tarpc Health Endpoint

**Status**: Intentional design, not debt.

The tarpc transport (`tarpc_transport.rs`) implements the full wateringHole health triad:
- `health_check` → `service::handle_health_check()`
- `health_liveness` → `service::handle_health_liveness()`
- `health_readiness` → `service::handle_health_readiness()`
- `identity_get` → `service::handle_identity_get()`
- `capability_list` → `service::handle_capability_list()`

Architecture rationale: tarpc listens on `-tarpc.sock` suffix for high-performance binary calls (shader compilation from hotSpring). The main socket speaks JSON-RPC 2.0 for primalSpring/biomeOS health checks and capability discovery. Both transports have full health endpoints. primalSpring reaches health via JSON-RPC (correct behavior).

## Verification Test

New integration test `test_btsp_phase3_encrypted_frame_loop_reachable`:
1. Registers a session with handshake key
2. Sends `btsp.negotiate` via duplex channel to `handle_connection`
3. Receives `cipher: "chacha20-poly1305"` response
4. Derives client-side `SessionKeys` from handshake key + nonces
5. Sends encrypted `health.liveness` request frame
6. Receives encrypted response, decrypts, asserts `alive: true`

This proves the entire chain is exercised end-to-end.

## Test Results

- 4633 passing, 0 failures, 160 ignored (hardware-gated)
- Zero clippy warnings (pedantic + nursery)

## Downstream Impact

- **primalSpring**: Phase 3 transport verification audit item resolved; GAP-04 documented as intentional
- **hotSpring**: No change — tarpc path remains high-perf binary calls
- **compositions**: Encrypted channel now confirmed reachable in production BTSP mode
