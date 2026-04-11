# sweetGrass v0.7.27 — SG-02 Socket Flag, TCP Opt-in, BTSP Mock BearDog

**Date**: April 11, 2026
**Primal**: sweetGrass v0.7.27
**Commit**: 045774e
**Trigger**: Provenance Trio audit response — primalSpring portability debt audit

---

## Summary

Resolves remaining sweetGrass debt items from the primalSpring portability
audit. Four categories: SG-02 socket flag, Tower Atomic TCP opt-in, BTSP
DI refactor with mock BearDog tests, and Postgres error-path coverage.

---

## Changes

### SG-02: `--socket` CLI Flag (RESOLVED)

`Commands::Server` now accepts `--socket <PATH>` (env: `SWEETGRASS_SOCKET`)
for explicit UDS path override. Plumbed to `start_uds_listener_at()` and
`cleanup_socket_at()`. When omitted, falls back to the standard 4-tier
resolution: `SWEETGRASS_SOCKET` env → `BIOMEOS_SOCKET_DIR` →
`XDG_RUNTIME_DIR/biomeos/` → `$TMPDIR/sweetgrass.sock`.

biomeOS already resolves sweetGrass via plain `{primal}.sock` fallback
(BM-08), but `--socket` enables per-invocation override for testing,
containers, and multi-instance deployments.

### Tower Atomic TCP Opt-in

`--port` changed from `u16` (default `0`, always-on) to `Option<u16>`.
TCP JSON-RPC now only starts when `--port` is explicitly provided.
Omit `--port` for UDS-only mode (default). This aligns sweetGrass with
rhizoCrypt and loamSpine: all three primals in the Provenance Trio are
now UDS-first, TCP opt-in.

### BTSP `perform_server_handshake_with` (DI Refactor)

Extracted `call_beardog_at(socket_path, method, params)` from the
hardcoded `call_beardog` wrapper. Internal functions (`receive_hello_and_create_session`,
`exchange_challenge`) now accept `security_socket: &Path`.

New public API: `perform_server_handshake_with(stream, security_socket)` —
DI-friendly variant that avoids `set_var` (which is `unsafe` in edition 2024
and blocked by `#![forbid(unsafe_code)]`).

**4 integration tests** in `btsp_mock_beardog.rs`:
- Full handshake with mock BearDog (create → hello → challenge → negotiate)
- Verify-rejection (BearDog returns `"verified": false`)
- Provider-unreachable (nonexistent socket)
- `HandshakeComplete` serde roundtrip

### Postgres Error-Path Coverage

- `connect_refused_returns_connection_error` — exercises `connect()` against
  unreachable Postgres (port 59999), verifying `PostgresError::Connection`
- `connect_url_refused_returns_connection_error` — same via `connect_url()`
- `config_is_configured_empty` / `config_is_configured_set` — boundary tests
- `validated_filter_empty` / `validated_filter_with_hash` / `validated_filter_overflow_timestamp`
- `PostgresStore` now derives `Debug` (was `Clone`-only)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,245 | 1,315 |
| Clippy | 0 warnings | 0 warnings |
| Fmt | PASS | PASS |
| `cargo deny` | CLEAN | CLEAN |
| TCP default | always-on (port 0) | opt-in (omit = UDS-only) |
| `--socket` flag | MISSING (SG-02 open) | RESOLVED |

---

## Ecosystem Impact

### For Springs (wetSpring, ludoSpring, healthSpring)
- sweetGrass default mode is now UDS-only — springs connecting via UDS are
  unaffected; springs expecting TCP must pass `--port` when starting sweetGrass
- `--socket` enables per-container socket path override

### For Compliance Matrix
- **SG-02** can be marked **RESOLVED** (was prematurely marked in previous handoff)
- **TCP opt-in** now matches rhizoCrypt/loamSpine — Tower Atomic aligned
- BTSP coverage significantly expanded with mock BearDog integration

### For Trio Partners (rhizoCrypt, loamSpine)
- Pattern: DI-friendly `_with` variant for BTSP handshake (avoids `unsafe set_var`)
  is recommended for adoption by rhizoCrypt and loamSpine

---

## Remaining Known Gaps

| Gap | Status | Notes |
|-----|--------|-------|
| Postgres CI coverage | Deferred | Needs Docker Postgres in CI |
| BTSP Phase 3 (encrypted framing) | Not started | Ecosystem-wide — waiting on BearDog |
| musl-static binary | Not tested locally | In plasmidBin (8.9M glibc) |
