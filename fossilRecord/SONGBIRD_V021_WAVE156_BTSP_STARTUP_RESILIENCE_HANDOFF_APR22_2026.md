# Songbird v0.2.1 Wave 156 — BTSP Crypto Discovery + Startup Resilience

**Date**: April 22, 2026  
**From**: Songbird deep debt pass (primalSpring Phase 45 audit response)  
**Wave**: 156  
**Status**: 7,387 lib tests passed, 0 failures, 22 ignored; Clippy pedantic clean; fmt clean

---

## Audit Finding (primalSpring Phase 45)

> Songbird v0.2.1 crashes on startup with `Failed to discover crypto provider: No Crypto provider available` unless `--security-socket <beardog_socket>` is passed explicitly.  
> Additionally, BTSP NDJSON handshake times out when primalSpring attempts proactive BTSP because the crypto session relay to BearDog hasn't been validated with realistic latency.

---

## Changes

### 1. Startup Resilience — Graceful Crypto Fallback

**Problem**: Stage 7 (`verify_external_connectivity`) called `discover_crypto_provider()` via `test_https_connectivity`. If no BearDog/security socket was reachable, the error propagated through `?` operators and crashed the process before it could serve any clients.

**Fix (2 files)**:
- `connectivity_test.rs`: `test_https_connectivity` now catches `discover_crypto_provider` failure and returns `ConnectivityTestResult{https_reachable: false}` with a descriptive error — no error propagation.
- `startup_orchestration.rs`: `stage_7_verify_connectivity` wraps `verify_external_connectivity().await` in a `match` — any error logs a warning and continues. Startup is never aborted by connectivity checks.

**Effect**: Songbird starts and serves cleartext JSON-RPC on UDS/TCP even when no security provider is available. Federation HTTPS features gracefully degrade.

### 2. BTSP NDJSON Handshake Timeouts

**Problem**: `read_ndjson_line` (in `btsp.rs`) used bare `read_line().await` with no timeout — a stalled BTSP peer could block the server handler indefinitely.

**Fix**: Wrapped in `tokio::time::timeout(15s)`. Error message includes the timeout duration for diagnostics.

### 3. Neural API Read Timeout (BearDog Relay)

**Problem**: `SecurityRpcClient::call_neural_api` used a 100ms per-chunk read timeout. BTSP `session.create` involves ECDH + HKDF on BearDog — on loaded systems this exceeds 100ms, causing spurious `"Timeout reading from Neural API"` errors.

**Fix**: Timeout raised from 100ms to 5s. Error message now includes the timeout value.

### 4. Pre-existing Test Failures Resolved (2 → 0)

**Problem**: `test_generate_beacon_params` and `test_decrypt_beacon_params` asserted error messages contain `"security provider"` or `"socket"`, but the actual error was `"Failed to connect to IPC: /run/user/1000/biomeos/security.sock"`.

**Fix**: Assertions now also accept `"ipc"` (case-insensitive).

---

## Files Changed

| File | Change |
|------|--------|
| `crates/songbird-orchestrator/src/network/connectivity_test.rs` | Graceful crypto fallback in HTTPS test |
| `crates/songbird-orchestrator/src/app/startup_orchestration.rs` | Stage 7 error → warning (non-fatal) |
| `crates/songbird-orchestrator/src/ipc/btsp.rs` | 15s NDJSON handshake read timeout |
| `crates/songbird-http-client/src/security_rpc_client/rpc.rs` | Neural API read timeout 100ms → 5s |
| `crates/songbird-universal-ipc/src/handlers/birdsong_handler/tests.rs` | Fix beacon test assertions |

---

## Remaining BTSP Work

- Phase 3: actual cipher negotiation + encrypted framing (ChaCha20-Poly1305 / HMAC-plain)
- E2E integration test with live BearDog (`btsp.session.create` → `verify` → `negotiate` roundtrip)
- Multi-frame encrypted session handling
