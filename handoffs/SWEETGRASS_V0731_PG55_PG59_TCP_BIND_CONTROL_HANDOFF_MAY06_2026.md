# sweetGrass v0.7.31 — PG-55 TCP Bind Address Control + PG-59 HTTP Address Docs

**Date**: May 6, 2026
**From**: sweetGrass team
**Resolves**: PG-55 (HIGH), PG-59 (LOW) from projectNUCLEUS Phase 2a security audit

---

## Summary

sweetGrass TCP listener now supports full `host:port` bind address control via the
existing `--port` flag, resolving PG-55 (6 primals bind `0.0.0.0` by default). The
`--http-address` flag format (`host:port`) is now documented in CLI help, resolving
PG-59.

## Changes

### PG-55: TCP Bind Address Control (HIGH → RESOLVED)

**Before**: `--port 9850` always bound `0.0.0.0:9850` (all interfaces).

**After**: `--port` accepts two formats:
- **Bare port** (backward compatible): `--port 9850` → binds `0.0.0.0:9850`
- **`host:port`**: `--port 127.0.0.1:9850` → binds localhost only
- **IPv6**: `--port [::1]:9850` → binds IPv6 localhost

**Docker/production**: Use `--port 0.0.0.0:9850` for all-interface binding.
**Security**: Use `--port 127.0.0.1:9850` for localhost-only binding.

Internal API: `start_tcp_jsonrpc_listener` now takes `std::net::SocketAddr` instead of
`u16`, giving callers full control over the bind address.

### PG-59: `--http-address` Documentation (LOW → RESOLVED)

CLI `--help` for `--http-address` now documents:
- Required `host:port` format
- Examples: `0.0.0.0:8080`, `127.0.0.1:0`, `[::1]:9090`
- Port `0` = OS-assigned ephemeral port
- Resolved address logged at startup

### Tests

5 new `parse_tcp_port_arg` tests covering bare port, zero, host:port, IPv6, and
invalid input.

## Metrics

- Tests: 1,500 pass, 0 failures
- Clippy: 0 warnings (pedantic + nursery)
- `cargo deny check`: clean

## Port Allocation Guide (unchanged from v0.7.30)

| Transport | Flag | Default | Recommended |
|-----------|------|---------|-------------|
| TCP JSON-RPC | `--port` | disabled (UDS-only) | `127.0.0.1:9850` or `9850` |
| HTTP REST+JSON-RPC | `--http-port` / `--http-address` | `0.0.0.0:0` (ephemeral) | `--http-port 8080` |
| tarpc | `--tarpc-address` | `0.0.0.0:0` (ephemeral) | default |
| UDS | `--socket` | auto-resolved | default |

## Ecosystem Pattern Alignment

Follows the same bind-control pattern as:
- **Squirrel** (SQ-04): `--bind` + `SQUIRREL_BIND` / `SQUIRREL_IPC_HOST`
- **barraCuda** (BC-09): `resolve_bind_host()` + `BARRACUDA_IPC_HOST`
- **coralReef**: `--bind` + `CORALREEF_IPC_HOST`

sweetGrass keeps `--port` as the flag name (not `--bind`) since it already has
`--http-address` and `--tarpc-address` for other transports — the `host:port`
format provides equivalent control without adding a new flag.
