# NestGate v4.7.0 — Session 44a: BTSP JSON-Line Framing + Security Socket Discovery

**Date:** April 2026
**Primal:** NestGate
**Ref:** primalSpring Phase 45c audit — BTSP JSON-line relay fixes

## Summary

Implemented the BTSP changes requested by primalSpring Phase 45c. The
original uncommitted changes were lost, so these were re-implemented from
the audit description and evolved to be clippy-clean and fully tested.

## Changes

### 1. Security Socket Discovery (`btsp_client.rs`)

`resolve_security_socket_path()` expanded from 2-var lookup + hardcoded
default to a 6-tier resolution:

| Priority | Source |
|----------|--------|
| 1 | `SECURITY_PROVIDER_SOCKET` env |
| 2 | `CRYPTO_PROVIDER_SOCKET` env |
| 3 | `SECURITY_SOCKET` env |
| 4 | `SECURITY_ENDPOINT` (if local filesystem path) |
| 5 | `$XDG_RUNTIME_DIR/biomeos/{security,beardog,crypto}.sock` |
| 6 | `/run/capability/security.sock` (default) |

Empty env vars are skipped. XDG discovery scans for known socket names
in order. This removes the hardcoded-only fallback path and enables
BearDog discovery in a live NUCLEUS without manual configuration.

### 2. JSON-Line Framing (`btsp_server_handshake/mod.rs`)

- Added `read_json_line()` / `write_json_line()` helpers for
  newline-delimited JSON framing.
- `perform_handshake()` auto-detects framing by peeking the first byte:
  `{` → JSON-line mode; otherwise → length-prefixed (4-byte BE header).
- Server responds in the same framing mode the client used.

### 3. Field Alignment

- `ChallengeResponse` now accepts optional `session_token` field from
  BearDog-style clients.
- `btsp.negotiate` includes `session_token` when present.
- Challenge value is extracted from BearDog's `btsp.session.create`
  response when the provider returns one (overriding our generated
  challenge).

### 4. Server Wiring (`isomorphic_ipc/server.rs`)

Updated connection disambiguation: when BTSP is required and first byte
is `{`, peeks the buffer for `"jsonrpc"` / `"method"` fields to
distinguish plain JSON-RPC (biomeOS composition) from JSON-line BTSP
ClientHello. Previous logic assumed all `{`-prefixed traffic was plain
JSON-RPC.

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 8,816 (lib), +9 new |
| Clippy own-code warnings | 0 |
| Files changed | 4 |
| Lines added | 367 |
| Lines removed | 63 |

## Verification

- `cargo check --workspace` ✓
- `cargo fmt --all` ✓
- `cargo clippy` (pedantic + nursery) — 0 own-code warnings ✓
- `cargo test --workspace --lib` — 8,816 passed, 0 failed ✓

## Remaining (from prior audit)

1. **Coverage 84.12% → 90%** target
2. **Vendored `rustls-rustcrypto`** — track upstream for de-vendoring
3. **`isomorphic_ipc/server.rs`** at 847 lines — candidate for
   refactoring below 800L threshold
