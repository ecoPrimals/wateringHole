# petalTongue v1.6.6 — PG-55 `--bind` Flag Handoff

**Date**: May 6, 2026
**Scope**: PG-55 LOW — `--bind host:port` for `server` and `live` modes
**Status**: RESOLVED

## Problem

petalTongue's TCP listener bound to `0.0.0.0:<port>` with no override when
`--port` was specified. While lowest risk (serves UI), ecosystem consistency
requires a `--bind` flag matching Squirrel SQ-04 and coralReef patterns.

## Fix

### CLI Layer (`src/main.rs`)

- Added `--bind <IP>` flag to both `Commands::Server` and `Commands::Live`.
- Added `PETALTONGUE_IPC_HOST` env var (via `#[arg(env)]`).
- New `parse_ipc_bind_host()` helper: parses IP, falls back to `127.0.0.1`.
- Secure default: `127.0.0.1` (localhost only). Docker/network: `--bind 0.0.0.0`.

### IPC Layer (`crates/petal-tongue-ipc/src/unix_socket_server.rs`)

- Added `tcp_bind_host: std::net::IpAddr` field to `UnixSocketServer`.
- New `with_tcp_bind_host()` builder method.
- `start()` now binds `SocketAddr::new(self.tcp_bind_host, port)` instead of
  hardcoded `([0, 0, 0, 0], port)`.

### Discovery Registration (`crates/petal-tongue-ipc/src/primal_registration.rs`)

- Renamed `with_tcp_port(port)` to `with_tcp_endpoint(host, port)`.
- Songbird `ipc.register` payload now carries the actual bind host
  (e.g., `"tcp": "127.0.0.1:9900"` or `"tcp": "0.0.0.0:9900"`).

### Server/Live Mode Wiring

- `server_mode::run()` and `live_mode::run_on_main_thread()` accept
  `tcp_bind_host: IpAddr` and pass it through to `UnixSocketServer`.

## Tests

- `test_cli_parse_server_with_bind` — verifies `--bind 0.0.0.0` parsing
- `test_parse_ipc_bind_host_defaults_to_localhost` — secure default
- `test_parse_ipc_bind_host_accepts_wildcard` — `0.0.0.0` → `UNSPECIFIED`
- `test_parse_ipc_bind_host_accepts_ipv6` — `::1` → IPv6 localhost
- `test_parse_ipc_bind_host_invalid_falls_back_to_localhost` — graceful fallback
- All 196 existing tests pass (188 unit + 8 e2e).

## Ecosystem Parity

| Primal | `--bind` | Env Var | Default |
|--------|----------|---------|---------|
| Squirrel | `--bind` | `SQUIRREL_BIND` / `SQUIRREL_IPC_HOST` | `127.0.0.1` |
| coralReef | `--bind` | `CORALREEF_IPC_HOST` | `127.0.0.1` |
| petalTongue | `--bind` | `PETALTONGUE_IPC_HOST` | `127.0.0.1` |

## Usage

```bash
# Localhost only (default, secure)
petaltongue server --port 9900

# Docker / network-facing
petaltongue server --port 9900 --bind 0.0.0.0

# Via environment
PETALTONGUE_IPC_HOST=0.0.0.0 petaltongue server --port 9900
```

## Verification

```bash
cargo check --all-features                          # clean
cargo clippy --all-features --workspace -D warnings  # 0 warnings
cargo fmt --check                                    # pass
cargo test --all-features                            # 196 pass
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps       # clean
```
