# biomeOS v3.44 — `--bind` Flag + Localhost Default (PG-55 FULL)

**Date**: May 6, 2026
**Author**: biomeOS agent
**Triggered by**: primalSpring projectNUCLEUS Phase 2a Security Audit — PG-55

---

## Summary

All TCP bind paths in biomeOS now accept `--bind <host>` and **default to
`127.0.0.1` (localhost-only)** instead of `0.0.0.0`. Nucleus mode now
forwards `--bind` to the embedded Neural API server. This fully resolves
PG-55 for biomeOS — both the audit items:

1. Default changed from `0.0.0.0` to `127.0.0.1`
2. Nucleus mode forwards `--bind`

## Changes

### `biomeos-types` (shared constants)
- New `default_tcp_bind_addr(port)` returns `127.0.0.1:port`.
- `tcp_bind_addr_with_host(None, port)` now falls back to localhost, not `0.0.0.0`.
- `production_tcp_bind_addr()` retained for explicit all-interfaces use.
- 6 tests (default-localhost, explicit-localhost, all-interfaces, IPv6, full-addr, invalid).

### `biomeos-atomic-deploy` (Neural API server)
- `NeuralApiServer`: new `bind_address: Option<String>` field.
- `with_bind_address(addr)` builder method.
- `server_lifecycle.rs`: TCP listener uses `tcp_bind_addr_with_host()`.
- `neural-api-server` standalone binary: `--bind <host>` CLI arg.

### `biomeos` UniBin CLI
- `biomeos neural-api --bind <host>`: new flag.
- `biomeos api --bind <host>`: new flag for the API server TCP path.
- `biomeos nucleus --bind <host>`: **new flag**, forwarded to the embedded
  Neural API server (previously hardcoded to `None`).

### `biomeos-api` (API crate)
- `serve_tcp()` signature updated: `bind_host: Option<&str>` parameter.

## Usage

```bash
# Default: localhost only (no flag needed)
biomeos neural-api --port 9800
biomeos nucleus --node-id n1 --port 9800

# Explicit all-interfaces (opt-in)
biomeos neural-api --port 9800 --bind 0.0.0.0
biomeos nucleus --node-id n1 --port 9800 --bind 0.0.0.0

# API server (same pattern)
biomeos api --port 3000
biomeos api --port 3000 --bind 0.0.0.0
```

## Verification

- `cargo clippy --workspace -- -D warnings`: 0 warnings.
- `cargo fmt --check`: clean.
- `cargo test --workspace --lib`: 6,842 tests, 0 failures.
- No unsafe code, no TODO/FIXME markers.

## PG-55 Status (cross-primal)

biomeOS is now fully clean. Per latest primalSpring audit, remaining LOW
items are skunkBat (default `0.0.0.0`) and sweetGrass (no `--bind` flag).
All other primals are clean.
