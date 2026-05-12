# ToadStool S176 — BTSP JSON-line Handshake Relay

**Date**: April 23, 2026
**Session**: S176
**Trigger**: primalSpring Phase 45c downstream audit — BTSP JSON-line relay fixes
**Ref**: `PRIMALSPRING_PHASE45C_BTSP_DEFAULT_UPSTREAM_HANDOFF_APR2026.md`

---

## What Changed

Implemented JSON-line BTSP auto-detection and 4-step handshake relay via BearDog IPC.
When primalSpring sends `{"protocol":"btsp","version":1,"client_ephemeral_pub":"..."}` as
a JSON line over a Unix socket, toadStool now detects this on the `0x7B` first-byte path
and relays to BearDog instead of returning a JSON-RPC parse error.

### New Modules

| File | Purpose |
|------|---------|
| `crates/core/common/src/btsp/json_line.rs` (368 lines) | `line_looks_like_btsp_client_hello()`, `relay_json_line_handshake()` (4-step BearDog IPC relay), `read_full_line_after_first_byte()`, `resolve_security_socket_path()` |
| `crates/core/common/src/btsp/family_seed.rs` (195 lines) | `load_family_seed_for_btsp()` — env→file cascade (FAMILY_SEED → BEARDOG_FAMILY_SEED → .family.seed), base64/hex/raw normalization |
| `crates/core/common/src/btsp/framing.rs` | `PrependByte<S>` extracted from unix.rs for reuse across connection handlers |

### Wiring (all 3 connection paths)

| File | Change |
|------|--------|
| `crates/server/src/pure_jsonrpc/connection/unix.rs` | `0x7B` path now reads full first line, checks `line_looks_like_btsp_client_hello()`, routes to `relay_json_line_handshake()` before JSON-RPC fallback |
| `crates/server/src/tarpc_server/connection.rs` | Same detection on plaintext first-byte path before tarpc handshake |
| `crates/cli/src/daemon/jsonrpc_server.rs` | Same detection on daemon BTSP socket |

### Wire Protocol (relay)

1. Client sends: `{"protocol":"btsp","version":1,"client_ephemeral_pub":"<b64>"}\n`
2. ToadStool calls BearDog: `btsp.session.create` with `{"family_seed":"<b64>"}`
3. ToadStool sends ServerHello: `{"version":1,"server_ephemeral_pub":"<from BD>","challenge":"<from BD>"}\n`
4. Client sends ChallengeResponse: `{"response":"<hmac>","preferred_cipher":"..."}\n`
5. ToadStool calls BearDog: `btsp.session.verify` with session_token, response, client_ephemeral_pub, preferred_cipher
6. ToadStool sends HandshakeComplete: `{"status":"ok","session_id":"...","cipher":"..."}\n`

### Security Socket Discovery

Env cascade: `SECURITY_PROVIDER_SOCKET` → `CRYPTO_PROVIDER_SOCKET` → `SECURITY_SOCKET` → capability-scoped fallback via `primal_sockets`.

---

## Verification

- `cargo check --workspace --exclude toadstool-runtime-edge` — clean
- `cargo clippy --workspace --exclude toadstool-runtime-edge -- -D warnings` — 0 warnings
- `cargo test --workspace --exclude toadstool-runtime-edge --lib` — 7,809 tests, 0 failures
- `cargo fmt --all --check` — 0 diffs

---

## Quality Gates

| Gate | Status |
|------|--------|
| Build | Clean |
| Clippy | 0 warnings |
| Tests | 7,809 lib-only, 0 failures |
| unsafe blocks | 49 (all in hw containment) |
| `#![forbid(unsafe_code)]` | 42 crates |
| Production TODOs | 0 |

---

## Ecosystem Impact

- **primalSpring Phase 45c**: toadStool JSON-line BTSP relay is now implemented. Guidestone should no longer report toadStool as BTSP FAIL for JSON-line ClientHello.
- **Existing binary BTSP**: Unchanged. The `0x7B` path is additive — binary length-prefixed BTSP (first byte < 0x09) continues to work as before.
- **BTSP Phase 3** (encrypted post-handshake channel): Still deferred ecosystem-wide. NULL cipher operational.
