# rhizoCrypt v0.14.0-dev — Session 37: UDS Unconditional + TCP Opt-in (LD-06)

**Date:** 2026-04-12
**Primal:** rhizoCrypt
**Context:** wetSpring exp094 audit — Provenance Trio UDS parity (LD-06)

---

## Summary

Evolved rhizoCrypt transport model to match loamSpine/sweetGrass: UDS is now
unconditional on Unix, TCP is opt-in via `--port` or env vars. Resolves the
blocking LD-06 gap where `dag` capability SKIPped in wetSpring exp094 due to
missing `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`.

## Transport Model (Before → After)

| Aspect | Before | After |
|--------|--------|-------|
| UDS | Opt-in (`--unix` flag) | **Unconditional** on Unix |
| TCP | Always started | **Opt-in** (`--port`, `RHIZOCRYPT_PORT`, `RHIZOCRYPT_JSONRPC_PORT`) |
| `rhizocrypt server` | TCP-only on 9400/9401 | UDS-only at `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock` |
| `rhizocrypt server --port 9400` | N/A | UDS + TCP |
| `--unix` flag | Enables UDS | Overrides UDS path (UDS always active) |

## Changes

### `main.rs`
- On Unix, always passes `Some("")` (default UDS path) to `run_server`,
  regardless of `--unix` flag presence. `--unix PATH` becomes a path override.
- Updated help text and module docs for UDS-first model.

### `lib.rs`
- Added `has_explicit_tcp_config()` — checks `RHIZOCRYPT_PORT`,
  `RHIZOCRYPT_RPC_PORT`, `RHIZOCRYPT_JSONRPC_PORT` env vars for TCP opt-in.
- `run_server_with_ready`: UDS starts first (unconditional on Unix), then TCP
  starts only when `port_override.is_some() || host_override.is_some() ||
  has_explicit_tcp_config()`.
- Extracted `serve_with_tcp()` to satisfy 100-line function limit.
- UDS-only path: waits on shutdown signal, signals UDS shutdown on exit.
- Backward-compat: test code can still pass `None` for unix_socket to skip UDS.

### Docs
- `README.md`: Updated quick start, IPC row, transport row, config table.
- `CONTEXT.md`: Added "UDS unconditional" and "TCP opt-in" IPC lines.
- `docs/ENV_VARS.md`: Marked port vars as "Opt-in TCP", updated UDS section
  to document unconditional behavior.

## Code Health

| Metric | Value |
|--------|-------|
| Tests | 1,510 passing (`--all-features`) |
| Clippy | 0 warnings (workspace-wide `-D warnings`) |
| Docs | 0 warnings (`-D warnings`) |
| Fmt | Clean |

## For Trio Partners (loamSpine, sweetGrass)

rhizoCrypt now matches the Provenance Trio transport standard:
- UDS unconditional at `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock` (or
  `rhizocrypt-{family_id}.sock` when `FAMILY_ID` is set)
- TCP opt-in via `--port` or env vars
- BTSP Phase 2 handshake on UDS when `FAMILY_ID` is set

The loamSpine "connection closes after first response" workaround should no
longer apply — `TCP_NODELAY` + `flush` hardening (S36) covers this.

## For wetSpring Validation

- **LD-06**: RESOLVED — `rhizocrypt.sock` now present in
  `$XDG_RUNTIME_DIR/biomeos/` on any `rhizocrypt server` invocation.
- `dag` capability should no longer SKIP in exp094.

## For primalSpring Gap Registry

- **LD-06 (UDS parity)**: RESOLVED
- **TRIO-IPC**: RESOLVED (S36 + S37 combined)
