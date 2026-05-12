# petalTongue v1.6.7 — BTSP JSON-Line Handshake Relay

**Date**: April 23, 2026
**From**: petalTongue team
**Ref**: primalSpring Phase 45c — BTSP Default Everywhere upstream debt

## Summary

Resolves the last BTSP upstream debt for petalTongue. primalSpring's
guidestone previously reported `visualization` as FAIL because petalTongue
closed connections on JSON-line ClientHello. Now fully functional with
both length-prefixed and JSON-line BTSP framing.

## Problem

primalSpring sends ClientHello as a JSON line:
```json
{"protocol":"btsp","version":1,"client_ephemeral_pub":"<base64>"}
```

petalTongue's accept loop correctly classified this as BTSP (via
`is_btsp_json_announcement`), but then routed to `perform_server_handshake`
which uses **length-prefixed** framing (`read_frame` = u32 + body).
The JSON line bytes `{"pr` were misinterpreted as a u32 length, causing
immediate handshake failure.

Additionally, the BearDog provider calls had 4 field name misalignments:
1. `family_seed_ref: "env:FAMILY_SEED"` instead of actual base64 seed
2. Local `rand_u128()` challenge instead of BearDog's challenge
3. `session_id` instead of `session_token` in verify call
4. `client_response` instead of `response` in verify call

## Solution

### New: `btsp/json_line.rs`

Full 4-step JSON-line BTSP handshake relay following the upstream pattern
(same as ToadStool, barraCuda, coralReef, NestGate, Squirrel):

| Step | Action | Framing |
|------|--------|---------|
| 1 | Read ClientHello | JSON line (`\n`-terminated) |
| 2 | Call BearDog `btsp.session.create` | JSON-RPC over UDS |
| 3 | Send ServerHello | JSON line |
| 4 | Read ChallengeResponse | JSON line |
| 5 | Call BearDog `btsp.session.verify` | JSON-RPC over UDS |
| 6 | Send HandshakeComplete | JSON line |

### Changed: Accept Loop Routing

Three-way classification in both `handle_uds_with_btsp` and `handle_tcp_with_btsp`:

| First byte | Buffer content | Route |
|------------|---------------|-------|
| Not `{` | — | `perform_server_handshake` (length-prefixed) |
| `{` | Contains `"protocol"` | `relay_json_line_handshake` (JSON-line) |
| `{` | No `"protocol"` | Plain JSON-RPC (no handshake) |

### Changed: BearDog Field Alignment

| Method | Field | Before | After |
|--------|-------|--------|-------|
| `btsp.session.create` | params | `family_seed_ref: "env:FAMILY_SEED"` | `family_seed: "<actual base64>"` |
| `btsp.session.create` | challenge | Local `rand_u128()` | BearDog's returned challenge |
| `btsp.session.create` | response key | `session_id` only | `session_token` with `session_id` fallback |
| `btsp.session.verify` | params | `session_id`, `client_response` | `session_token`, `response` |
| HandshakeComplete | status | `"complete"` | `"ok"` |

### Changed: Provider Socket Cascade

```
BTSP_PROVIDER_SOCKET > BEARDOG_SOCKET > SECURITY_PROVIDER_SOCKET >
CRYPTO_PROVIDER_SOCKET > SECURITY_SOCKET >
$BIOMEOS_SOCKET_DIR/{provider}-{family}.sock
```

### New: `load_family_seed()`

`BtspHandshakeConfig::load_family_seed()` resolves `BEARDOG_FAMILY_SEED` > `FAMILY_SEED`
for passing actual seed value to BearDog (not a reference string).

## Files Changed

| File | Action |
|------|--------|
| `crates/petal-tongue-ipc/src/btsp/json_line.rs` | **Created** — JSON-line handshake relay |
| `crates/petal-tongue-ipc/src/btsp/mod.rs` | **Modified** — added `mod json_line`, re-exports |
| `crates/petal-tongue-ipc/src/btsp/server.rs` | **Modified** — field name alignment, BearDog challenge, family_seed |
| `crates/petal-tongue-ipc/src/btsp/types.rs` | **Modified** — env cascade, `load_family_seed()` |
| `crates/petal-tongue-ipc/src/unix_socket_server.rs` | **Modified** — three-way routing to JSON-line/length-prefixed/plain |
| `crates/petal-tongue-ipc/src/btsp/tests.rs` | **Modified** — 9 new tests |

## Verification

- `cargo clippy --workspace --all-targets --all-features` — 0 warnings
- `cargo test --workspace --all-features` — all passing
- `cargo check --target x86_64-apple-darwin` — macOS cross-check clean
- 21 BTSP-specific tests passing (12 existing + 9 new)

## For primalSpring

The `visualization` capability should now pass guidestone BTSP validation.
petalTongue supports both framing modes:
- **JSON-line**: For primalSpring guidestone and composition validation
- **Length-prefixed**: For direct BTSP clients using binary framing

Both paths delegate to BearDog for session create/verify with aligned field names.
