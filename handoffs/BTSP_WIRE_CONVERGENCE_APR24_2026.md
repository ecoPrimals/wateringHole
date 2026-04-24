# BTSP Wire Convergence — April 24, 2026 (Updated)

**From:** primalSpring Phase 45c validation
**For:** All primal teams
**Status:** 167/171 guidestone, 7/13 BTSP authenticated → target 13/13

## Current State

After two rounds of upstream evolution, **7 of 13** NUCLEUS capabilities
authenticate via BTSP. The remaining 4 represent wire-format mismatches
in the BearDog relay path, not missing implementations. All 4 teams have
shipped fixes — the gap is narrowing through natural convergence.

### BTSP Scoreboard

| Capability | Primal | BTSP | Notes |
|---|---|---|---|
| security | BearDog | **PASS** | Direct connection (no relay) |
| discovery | Songbird | FAIL | Silent-fail relay (Wave 165 shipped, residual issue) |
| compute | ToadStool | FAIL | ServerHello works, full handshake incomplete |
| tensor | barraCuda | **PASS** | Sprint 44h: single BearDog connection + raw family_seed |
| shader | coralReef | **PASS** | Reference implementation |
| storage | NestGate | FAIL | Error frames work (Session 45c), relay verification fails |
| ai | Squirrel | **PASS** | Converged |
| dag | rhizoCrypt | **PASS** | Converged |
| commit | sweetGrass | **PASS** | Converged |
| provenance | rhizoCrypt | **PASS** | Converged |
| visualization | petalTongue | **PASS** | Converged |
| ledger | loamSpine | **PASS** | Converged |
| attribution | sweetGrass | **PASS** | Converged |

### What Converged (9 of 13)

These primals complete the full 4-step handshake through BearDog relay:

- **coralReef** — Reference implementation. Earliest correct relay.
- **Squirrel** — JSON-line BTSP relay, fast fallback.
- **rhizoCrypt** — Full BTSP with key derivation.
- **sweetGrass** — `session_id` in ServerHello, clean relay.
- **loamSpine** — `status:ok` added to HandshakeComplete (Phase 45c).
- **petalTongue** — BearDog field alignment (Phase 45c).
- **BearDog** — Direct (no relay needed).

### What's Still Converging (4 of 13)

These primals send valid ServerHello but the full handshake doesn't
complete through BearDog. Each team has shipped fixes addressing the
originally diagnosed issue — the residual failure is in the relay
verification step.

**Songbird** (Wave 168): Two root causes fixed: (1) `SecurityRpcClient::new()`
defaulted to Neural API mode, wrapping `btsp.session.create` in `capability.call`
— BearDog returned "Method not found". Changed to `new_direct()` since the
crypto socket IS the BearDog socket. (2) `resolve_family_seed()` now base64-
encodes the raw env string — BearDog base64-decodes `family_seed` internally.
Previous: W167 error frames + env fallbacks, W164 chunked reads, W162
`stream.shutdown()` removal.

**ToadStool** (Session 177): Fixed `verified` bool check (was `status`
string). Sends valid ServerHello with challenge. Full handshake
fails intermittently during BearDog relay verification.

**barraCuda** (Sprint 44h): **CONVERGED.** Two root causes fixed: (1) per-call
BearDog connections replaced with single persistent connection for both
session.create and session.verify (BearDog associates session state with
the socket). (2) `resolve_family_seed_b64()` was hex-decoding then base64-
encoding the FAMILY_SEED — BearDog expects raw string. Replaced with
`resolve_family_seed_raw()`. Sprint 44g (flush fix) was also necessary.

**NestGate** (Session 45c): Fixed `family_seed_ref` → actual `family_seed`,
added mode-aware error frames. Sends valid ServerHello, then returns
"connection closed before complete line" during verification step.

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
accept `session_id`. The `family_seed` parameter is the raw hex string
from the `FAMILY_SEED` environment variable — NOT base64-encoded bytes.

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

3. **family_seed from env as raw string.** Read `FAMILY_SEED` env var,
   pass it to BearDog as-is. Do NOT hex-decode or base64-encode it.
   BearDog handles the encoding internally.

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
