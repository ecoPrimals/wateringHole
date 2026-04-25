# BTSP Wire Convergence — April 24, 2026 (CONVERGED)

**From:** primalSpring Phase 45c validation
**For:** All primal teams
**Status:** **171/171 guidestone ALL PASS, 13/13 BTSP authenticated — CONVERGED**

## Current State

**Full NUCLEUS BTSP convergence achieved.** All 13 capabilities authenticate
via BTSP. Every primal implements the 4-step handshake protocol through
BearDog relay (or direct connection for BearDog itself). This represents
the completion of the Phase 45c BTSP-default-everywhere goal.

### BTSP Scoreboard (Final)

| Capability | Primal | BTSP | Resolution |
|---|---|---|---|
| security | BearDog | **PASS** | Direct connection (no relay) |
| discovery | Songbird | **PASS** | Wave 169: `SecurityRpcClient::new_direct()` |
| compute | ToadStool | **PASS** | Post-handshake connection persistence |
| tensor | barraCuda | **PASS** | `writer.flush()` instead of `shutdown()` |
| shader | coralReef | **PASS** | Reference implementation |
| storage | NestGate | **PASS** | `family_seed` base64, mode-aware error frames |
| ai | Squirrel | **PASS** | JSON-line BTSP relay |
| dag | rhizoCrypt | **PASS** | First-byte auto-detect, key derivation |
| commit | sweetGrass | **PASS** | Three-way multiplexing |
| provenance | rhizoCrypt | **PASS** | BTSP liveness passthrough |
| visualization | petalTongue | **PASS** | BearDog field alignment |
| ledger | loamSpine | **PASS** | `btsp.negotiate` non-fatal fallback |
| attribution | sweetGrass | **PASS** | `session_id` in ServerHello |

### Convergence Timeline

- **Phase 45c start**: 5/13 BTSP authenticated
- **Round 1** (coralReef, Squirrel, rhizoCrypt, sweetGrass, BearDog): 7/13 → reference implementations
- **Round 2** (loamSpine, petalTongue): 9/13 → `status:ok` in HandshakeComplete, BearDog field alignment
- **Round 3** (Songbird Wave 169, ToadStool, barraCuda, NestGate): **13/13** → final wire-format fixes

### Key Fixes in Final Round

**Songbird** (Wave 169): Root cause was `SecurityRpcClient::new()` defaulting
to Neural API mode — `btsp.session.create` was routed through `capability.call`
which BearDog rejects. Fix: `SecurityRpcClient::new_direct()` at two call sites
in `bin_interface/server.rs`.

**ToadStool**: Post-handshake connection was being dropped instead of kept alive
for subsequent NDJSON RPC traffic. Fix: restructured control flow in
`jsonrpc_server.rs` and `pure_jsonrpc/connection/unix.rs` to maintain connection.

**loamSpine**: BearDog does not implement `btsp.negotiate` — loamSpine was treating
"Method not found" as fatal and silently dropping the connection. Fix: non-fatal
fallback to client's `preferred_cipher` in `handshake.rs`.

**NestGate** (Session 45c): `family_seed` base64 encoding aligned with BearDog wire
contract. Mode-aware error frames ensure JSON-line errors for JSON-line clients.

## BearDog Wire Contract (ground truth)

### `btsp.session.create`

**Request:**
```json
{"jsonrpc":"2.0","method":"btsp.session.create","params":{"family_seed":"<hex-string>"},"id":1}
```

**Response:**
```json
{"jsonrpc":"2.0","result":{"challenge":"<base64>","server_ephemeral_pub":"<base64>","session_token":"<uuid>"},"id":1}
```

Note: `session_token` is the canonical field name. Some versions also
accept `session_id`. The `family_seed` parameter must be the
**base64-encoded** raw hex string from the `FAMILY_SEED` environment
variable: `BASE64.encode(env_var.trim().as_bytes())`. BearDog
base64-decodes this to recover the hex bytes, then derives the
handshake key from those bytes.

### `btsp.session.verify`

**Request:**
```json
{"jsonrpc":"2.0","method":"btsp.session.verify","params":{"session_token":"<uuid>","response":"<base64>","client_ephemeral_pub":"<base64>","preferred_cipher":"null"},"id":2}
```

**Response (success):**
```json
{"jsonrpc":"2.0","result":{"verified":true,"session_id":"<uuid>","cipher":"null"},"id":2}
```

Key: `verified` is a **bool**, not a string. There is no `status` field.

## Pattern to Converge On

The working primals share a common relay pattern. See
`SOURDOUGH_BTSP_RELAY_PATTERN.md` for the extracted standard.

**Key properties of a working relay:**

1. **First-line auto-detect**: Peek first byte of incoming connection.
   `0x7B` (`{`) → read full line → check for `"protocol":"btsp"` →
   route to handshake path. Otherwise → plain JSON-RPC.

2. **BearDog relay is a function call, not a new connection per step.**
   Connect to BearDog socket once, call `btsp.session.create`, read
   response, call `btsp.session.verify`, read response. Do NOT
   `shutdown()` or `close()` between calls.

3. **family_seed: base64-encode the raw env string.** Read `FAMILY_SEED`
   env var, `trim()` whitespace, then **base64-encode the raw bytes**
   (`BASE64.encode(raw.as_bytes())`). BearDog base64-decodes this
   parameter to recover the hex string bytes for HKDF. All passing
   primals (Squirrel, coralReef, sweetGrass, rhizoCrypt) do this.
   Sending the raw hex without base64 causes HMAC mismatch.

4. **JSON-aware socket reads.** BearDog keeps sockets open for multiple
   requests. Use chunked reads that break on complete JSON — never
   `read_to_end()` (hangs forever) or `stream.shutdown()` (kills the
   connection).

5. **Error frames match client framing.** If the client sent JSON-line,
   errors must be JSON-line. If length-prefixed, errors must be
   length-prefixed. Silent drops are never acceptable.

## Verification

Each primal's BTSP relay should pass this socat test (NUCLEUS running):

```bash
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/${PRIMAL}-${FAMILY_ID}.sock
```

**Expected**: JSON line with `challenge`, `server_ephemeral_pub`, `version`.
If empty → auto-detect not triggering. If error frame → BearDog relay failing.

Full validation: `primalspring_guidestone` reports `BTSP authenticated` for
the capability.

## Reference Implementations

| Implementation | Path | Status |
|---|---|---|
| coralReef relay | `crates/coralreef-core/src/ipc/btsp.rs` | Reference (earliest correct) |
| sweetGrass relay | `crates/sweetgrass-ipc/src/btsp/` | Clean, includes session_id |
| squirrel relay | `crates/squirrel-core/src/btsp/` | Converged |
| primalSpring client | `ecoPrimal/src/ipc/btsp_handshake.rs` | Client-side reference |
| BearDog API | `btsp.session.create`, `btsp.session.verify` | Ground truth |

## Evolution Philosophy

These primals are evolving toward convergence — not being dictated to.
Each team identified and fixed their specific wire issues independently.
The converged pattern (documented in `SOURDOUGH_BTSP_RELAY_PATTERN.md`)
is extracted from what works, not prescribed in advance. Future primals
(sourDough) will absorb this pattern as starter culture.
