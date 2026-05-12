# Songbird v0.2.1 — Wave 153 BTSP NDJSON Wire-Format Alignment

**Date**: April 21, 2026
**From**: Songbird Wave 153
**For**: primalSpring (Phase 45b), all spring teams, BearDog team
**Resolves**: Phase 45b BTSP escalation — Songbird BTSP wire-format gap

---

## Problem

primalSpring sends BTSP `ClientHello` as JSON-line:
```json
{"protocol":"btsp","version":1,"client_ephemeral_pub":"..."}\n
```

Songbird's UDS accept path only had two modes:
1. First byte `{` → NDJSON JSON-RPC (no BTSP handshake)
2. First byte != `{` → length-prefixed binary BTSP

The JSON-line `ClientHello` starts with `{`, so it was routed to the NDJSON
handler, which tried to parse it as JSON-RPC (expects `"jsonrpc"`, `"method"`)
and returned a parse error. Connection failed.

## Fix

### First-line auto-detection (connection.rs)

When `FAMILY_ID` is set and first byte is `{`, Songbird now reads the **full
first line** and checks whether it contains `"protocol":"btsp"`:

| First line contains | Route |
|---------------------|-------|
| `"protocol":"btsp"` | BTSP NDJSON handshake → NDJSON JSON-RPC session |
| `"jsonrpc"` / `"method"` | Plain NDJSON JSON-RPC session |
| (non-`{` first byte) | Length-prefixed binary BTSP handshake |

### NDJSON BTSP handshake (btsp.rs)

New `perform_server_handshake_ndjson()` implements the same 4-step BTSP
handshake but with newline-delimited JSON framing:

1. `ClientHello` (pre-read from first line)
2. `ServerHello` (NDJSON)
3. `ChallengeResponse` (NDJSON)
4. `HandshakeComplete` (NDJSON)

Same BearDog crypto delegation (`btsp.session.create`, `btsp.session.verify`,
`btsp.negotiate`). After handshake, the connection continues with persistent
NDJSON JSON-RPC — same as cleartext sessions.

### Wire compatibility

The `ClientHello` struct now accepts optional `protocol` field
(`#[serde(default)]`). Both wire formats (length-prefix and JSON-line) work
with the same struct.

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace -- -D warnings` | Zero warnings |
| `cargo fmt --all --check` | Clean |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace --lib` | 7,388 passed, 0 failed, 22 ignored |

8 new tests added (discriminator, deserialization, NDJSON roundtrip).

---

## What Spring Teams Can Do Now

Once BearDog is accessible (live NUCLEUS), primalSpring's
`Transport::connect_btsp()` should successfully complete the 4-step BTSP
handshake with Songbird's UDS socket. The guidestone `btsp:Tower:discovery`
check should flip from FAIL to PASS.

---

**License**: AGPL-3.0-or-later
