# biomeOS v3.44 — `--bind` Flag Standardization (PG-55)

**Date**: May 6, 2026
**Author**: biomeOS agent
**Triggered by**: primalSpring projectNUCLEUS Phase 2a Security Audit — PG-55

---

## Summary

All TCP bind paths in biomeOS now accept `--bind <host>` to override the
default `0.0.0.0` (all-interfaces) binding. This resolves PG-55 for biomeOS,
which was flagged as HIGH across 6 primals during the Phase 2a penetration
testing audit.

## Changes

### `biomeos-types` (shared constants)
- New `tcp_bind_addr_with_host(Option<&str>, u16) -> SocketAddr` helper.
  Parses IP address, full `host:port` string, or falls back to `0.0.0.0:port`.
- 5 new tests (None/localhost/IPv6/full-addr/invalid-fallback).

### `biomeos-atomic-deploy` (Neural API server)
- `NeuralApiServer`: new `bind_address: Option<String>` field.
- `with_bind_address(addr)` builder method.
- `server_lifecycle.rs`: TCP listener uses `tcp_bind_addr_with_host()`.
- `neural-api-server` standalone binary: `--bind <host>` CLI arg.

### `biomeos` UniBin CLI
- `biomeos neural-api --bind <host>`: new flag, threads through to
  `NeuralApiServer::with_bind_address()`.
- `biomeos api --bind <host>`: new flag for the API server TCP path.
- Nucleus mode passes `None` (preserves existing default behavior).

### `biomeos-api` (API crate)
- `serve_tcp()` signature updated: `bind_host: Option<&str>` parameter.
  Uses `tcp_bind_addr_with_host()` instead of hardcoded `production_tcp_bind_addr()`.

## Usage

```bash
# Localhost only (recommended for single-machine deployment)
biomeos neural-api --port 9800 --bind 127.0.0.1

# All interfaces (default, explicit)
biomeos neural-api --port 9800 --bind 0.0.0.0

# API server localhost
biomeos api --port 3000 --bind 127.0.0.1
```

## Verification

- `cargo clippy --workspace -- -D warnings`: 0 warnings.
- `cargo fmt --check`: clean.
- `cargo test --workspace --lib`: 6,841 tests, 0 failures.
- No unsafe code, no TODO/FIXME markers.

## Remaining PG-55 Work (other primals)

Per primalSpring audit, 5 other primals still need `--bind`:
Songbird (HTTP), ToadStool, skunkBat, sweetGrass (main TCP), petalTongue.
Each primal team resolves independently. UniBin v1.1 `--bind <host:port>`
proposed as the cross-primal standard.
