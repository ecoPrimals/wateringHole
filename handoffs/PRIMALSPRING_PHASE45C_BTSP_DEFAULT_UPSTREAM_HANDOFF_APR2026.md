# primalSpring Phase 45c — BTSP Default Everywhere: Upstream Primal Handoff

**From**: primalSpring v0.9.17 (Phase 45c)
**For**: All primal teams
**Date**: April 2026

---

## What Happened

primalSpring escalated its BTSP policy from "incremental tower-delegated" to
**BTSP expected on every capability, every tier**. guidestone now reports
cleartext as FAIL. We drove JSON-line BTSP auto-detection and full handshake
relay fixes into 5 upstream primals, resolving the majority of BTSP failures.

**Result**: 11/13 capabilities BTSP-authenticated (was 5/13).

---

## What We Fixed In Your Code (Pull These Changes)

### Common Pattern (All 5 Relay Primals)

Every relay primal (ToadStool, barraCuda, coralReef, NestGate, Squirrel) had
the same family of issues when primalSpring's JSON-line ClientHello arrived:

1. **JSON-line BTSP auto-detection**: The `0x7B` (`{`) first-byte path routed
   to plain JSON-RPC without checking for `"protocol":"btsp"`. Fixed by reading
   the full first line and checking for the BTSP protocol field before routing.

2. **`btsp.session.create` parameters**: Was sending `family_seed_ref` or
   missing `family_seed` entirely. BearDog requires the literal base64-encoded
   `FAMILY_SEED` value.

3. **BearDog field name alignment**:
   - `btsp.session.verify`: expects `session_token` (not `session_id`) and
     `response` (not `client_response`)
   - `btsp.session.create` returns `session_token` (not `session_id`) — use
     fallback parsing: `.get("session_id").or_else(|| .get("session_token"))`

4. **Challenge sourcing**: BearDog generates the challenge in `btsp.session.create`.
   Relay primals MUST use BearDog's challenge in ServerHello, not generate their own.
   Using a local challenge causes HMAC verification failure ("family verification rejected").

5. **Consistent framing**: If ClientHello arrived as JSON-line (newline-delimited),
   the entire handshake (ServerHello, ChallengeResponse, HandshakeComplete) must
   use JSON-line framing. Mixing binary length-prefixed with JSON-line fails.

### Per-Primal Changes

**ToadStool** (`crates/server/src/pure_jsonrpc/connection/unix.rs`, `crates/core/common/src/btsp/`):
- Added `line_looks_like_btsp_client_hello()` check in first-byte `{` path
- New `relay_json_line_handshake()` in `btsp/json_line.rs`
- New `load_family_seed_for_btsp()` in `btsp/family_seed.rs`

**barraCuda** (`crates/barracuda-core/src/ipc/btsp.rs`):
- `is_btsp_client_hello()` now detects `"protocol": "btsp"` in addition to `"type": "ClientHello"`
- `session_create_rpc()` sends base64-encoded `family_seed`
- `session_verify_rpc()` passes `client_ephemeral_pub` and `preferred_cipher` to BearDog

**coralReef** (`crates/coralreef-core/src/ipc/btsp.rs`, `unix_jsonrpc.rs`):
- New `relay_json_line_handshake()` with full 4-step relay
- `b64_encode()` helper (no external `base64` crate needed — reads `/dev/urandom`)
- `BtspSessionError` made `pub` for cross-module access
- `BIOMEOS_FAMILY_ID` must be set in launch environment (nucleus_launcher.sh updated)

**NestGate** (`crates/nestgate-rpc/src/rpc/btsp_server_handshake/mod.rs`, `btsp_client.rs`):
- `resolve_security_socket_path()` now checks env vars (`SECURITY_PROVIDER_SOCKET`,
  `CRYPTO_PROVIDER_SOCKET`, `SECURITY_SOCKET`) before family-scoped discovery
- `perform_handshake()` uses JSON-line framing when `client_hello_json_line` is present
- New `read_json_line()` / `write_json_line()` helpers

**Squirrel** (`crates/main/src/rpc/btsp_handshake/mod.rs`, `btsp_handshake_wire.rs`):
- `btsp_handshake_after_client_hello()` gains `json_line_mode: bool` parameter
- Conditional JSON-line framing for ServerHello/ChallengeResponse/HandshakeComplete
- New `write_json_line()` / `read_json_line_msg()` in wire module

---

## Remaining Upstream BTSP Debt

### petalTongue — No BTSP Server

**Behavior**: Closes connection immediately on receiving ClientHello.
**Fix path**: Add `PeekedStream` first-byte peek (like skunkBat's pattern).
If first byte is `{`, read full line, check for `"protocol":"btsp"`.
Route to a `relay_json_line_handshake()` function that calls BearDog
for session create/verify. Same pattern as the 5 primals above.

### loamSpine — Incomplete Handshake

**Behavior**: Initiates BTSP handshake (sends ServerHello) but does not send
the final HandshakeComplete message, causing primalSpring to timeout.
**Fix path**: Ensure the NDJSON handshake flow completes all 4 steps.
After `btsp.session.verify` succeeds, write `HandshakeComplete` as a JSON line.

---

## BTSP Wire Protocol Reference

primalSpring's ClientHello (JSON-line):
```json
{"protocol":"btsp","version":1,"client_ephemeral_pub":"<base64>"}
```

Expected server flow:
1. **Detect**: First byte `{`, full line contains `"protocol":"btsp"`
2. **Call BearDog**: `btsp.session.create` with `{"family_seed":"<base64>"}`
3. **Send ServerHello**: `{"version":1,"server_ephemeral_pub":"<from BD>","challenge":"<from BD>"}\n`
4. **Read ChallengeResponse**: `{"response":"<hmac>","preferred_cipher":"..."}\n`
5. **Call BearDog**: `btsp.session.verify` with `{"session_token":"...","response":"...","client_ephemeral_pub":"...","preferred_cipher":"..."}`
6. **Send HandshakeComplete**: `{"status":"ok","session_id":"...","cipher":"..."}\n`

---

## NUCLEUS Composition Patterns

The composition patterns discovered during this phase that are relevant to all primals:

### Family-Scoped Socket Discovery
All primals should support `{capability}-{family_id}.sock` naming. The nucleus
launcher creates symlinks: `security-nucleus01.sock` → `beardog-nucleus01.sock`,
`compute-nucleus01.sock` → `toadstool-nucleus01.sock`, etc. This enables multiple
NUCLEUS families on the same host.

### Environment Variable Cascade for Security Provider
Primals needing BearDog should check in order:
1. `SECURITY_PROVIDER_SOCKET` / `CRYPTO_PROVIDER_SOCKET` / `SECURITY_SOCKET`
2. Family-scoped: `$XDG_RUNTIME_DIR/biomeos/beardog-{family}.sock`
3. Family-scoped: `$XDG_RUNTIME_DIR/biomeos/crypto-{family}.sock`
4. Default hardcoded path

### Handshake Timeout Budget
Relay primals call BearDog during the handshake, adding a round-trip. primalSpring
uses a 15-second handshake timeout (vs 5s for normal IPC) to accommodate this.
Relay primals should also ensure their internal BearDog calls don't timeout
before the client gives up.

---

## Verification

After pulling these changes, verify BTSP works:

```bash
# Start a NUCLEUS
export FAMILY_ID="test-nucleus01"
export BEARDOG_FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p)"
./nucleus_launcher.sh --composition full start

# Test with socat (should get ServerHello, not JSON-RPC error)
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' | \
  socat - UNIX-CONNECT:/run/user/$UID/biomeos/{primal}-{family}.sock

# Run guidestone for full validation
cargo run --release --bin primalspring_guidestone
```

---

## Key References

- BTSP protocol: `infra/wateringHole/BTSP_PROTOCOL_STANDARD.md`
- Composition guidance: `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md`
- Gap registry: `primalSpring/docs/PRIMAL_GAPS.md`
- Changelog: `primalSpring/CHANGELOG.md` (Phase 45c entry)
