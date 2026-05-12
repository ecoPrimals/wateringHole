# biomeOS v3.44 — `--bind` Flag Standardization (PG-55)

**Date**: May 6, 2026
**Author**: biomeOS agent
**Triggered by**: primalSpring projectNUCLEUS Phase 2a Security Audit — PG-55

---

## Summary

All TCP bind paths in biomeOS now accept `--bind <host>` to override the
default bind address. Default changed to `127.0.0.1` (localhost-only).
This resolves PG-55 for biomeOS, which was flagged as HIGH across 6 primals
during the Phase 2a penetration testing audit.

## Changes

### `biomeos-types` (shared constants)
- New `tcp_bind_addr_with_host(Option<&str>, u16) -> SocketAddr` helper.
  Parses IP address, full `host:port` string, or falls back to `127.0.0.1:port`.
- `default_tcp_bind_addr(port)` returns `127.0.0.1:port`.
- 6 new tests (None/localhost/IPv6/full-addr/invalid-fallback/default-localhost).

### `biomeos-atomic-deploy` (Neural API server)
- `NeuralApiServer`: new `bind_address: Option<String>` field.
- `with_bind_address(addr)` builder method.
- `server_lifecycle.rs`: TCP listener uses `tcp_bind_addr_with_host()`.
- `neural-api-server` standalone binary: `--bind <host>` CLI arg.

### `biomeos` UniBin CLI
- `biomeos neural-api --bind <host>`: new flag, threads through to
  `NeuralApiServer::with_bind_address()`.
- `biomeos api --bind <host>`: new flag for the API server TCP path.
- `biomeos nucleus --bind <host>`: forwards `--bind` to embedded Neural API.

### `biomeos-api` (API crate)
- `serve_tcp()` signature updated: `bind_host: Option<&str>` parameter.
  Uses `tcp_bind_addr_with_host()` instead of hardcoded `production_tcp_bind_addr()`.

## Usage

```bash
# Localhost only (default — secure by default)
biomeos neural-api --port 9800

# All interfaces (explicit opt-in)
biomeos neural-api --port 9800 --bind 0.0.0.0

# API server localhost
biomeos api --port 3000 --bind 127.0.0.1

# Nucleus mode forwards --bind to Neural API
biomeos nucleus --port 9800 --bind 127.0.0.1
```

## Verification

- `cargo clippy --workspace -- -D warnings`: 0 warnings.
- `cargo fmt --check`: clean.
- `cargo test --workspace --lib`: 6,842 tests, 0 failures.
- No unsafe code, no TODO/FIXME markers.

## PG-55 Status — ALL RESOLVED (May 6, 2026)

All 13 primals now have bind control defaulting to `127.0.0.1`.
Songbird, ToadStool, skunkBat, petalTongue shipped `--bind`.
sweetGrass defaults bare `--port` to localhost. biomeOS nucleus forwards `--bind`.
