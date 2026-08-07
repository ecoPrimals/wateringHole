# coralReef Wave 157a — G68 Platform Substrate Deep Evolution

**Date**: 2026-08-07 | **Author**: coralReef code team (strandGate)
**Wave**: 157a | **From**: eastGate overwatch
**Gate**: strandGate

---

## SUMMARY

coralReef G68 deep evolution complete. 18 silicon deism sites identified and
evolved across ecosystem registration, BTSP discovery, provenance signing,
and security provider handshake. All IPC paths now use `TransportEndpoint` —
TCP works on non-Unix platforms when discovered. L1 links evolved (prior pass).
L2/L3: zero exposure.

## G68 EVOLUTION — coralReef

### L1: Links (done in prior pass)

| Function | Before | After |
|----------|--------|-------|
| `create_local_symlink()` | `Unsupported` on non-Unix | `symlink_file` on Windows, `Unsupported` only on exotic targets |

### IPC Deism → Transport-Agnostic (this pass)

| Module | Before (silicon deism) | After (G68) |
|--------|----------------------|-------------|
| `ecosystem/mod.rs` | `jsonrpc_bind_to_unix_path()` rejected TCP binds | `parse_bind_to_endpoint()` → `TransportEndpoint` (UDS or TCP) |
| `ecosystem/mod.rs` | `send_jsonrpc_line(&Path)` | `send_jsonrpc_line(&TransportEndpoint)` via `connect_transport()` |
| `ecosystem/mod.rs` | `heartbeat_loop(PathBuf)` | `heartbeat_loop(TransportEndpoint)` |
| `ecosystem/mod.rs` | Registration skipped on non-Unix | Registration attempts TCP when discovered |
| `btsp.rs` | `discover_by_capability() → PathBuf` | `discover_by_capability() → TransportEndpoint` |
| `btsp.rs` | `discover_security_socket() → PathBuf` | `discover_security_socket() → TransportEndpoint` |
| `btsp.rs` | `check_discovery_file_for_method()` UDS-only | Checks UDS → TCP → jsonrpc.bind fallback chain |
| `btsp.rs` | `security_rpc(&Path)` | `security_rpc(&TransportEndpoint)` |
| `btsp.rs` | `create_btsp_session(&Path)` | `create_btsp_session(&TransportEndpoint)` |
| `btsp_client.rs` | `handshake_on_stream_sync(&SyncTransportStream, &Path)` | `handshake_on_stream_sync(&SyncTransportStream, &TransportEndpoint)` |
| `btsp_client.rs` | `provider_rpc(&Path)` | `provider_rpc(&TransportEndpoint)` |
| `provenance.rs` | `CRYPTO_SIGN_SOCKET: OnceLock<Option<PathBuf>>` | `CRYPTO_SIGN_ENDPOINT: OnceLock<Option<TransportEndpoint>>` |
| `provenance.rs` | `try_sign()` via `connect_local_sync(path)` | `try_sign()` via `connect_transport_sync(endpoint)` |

### New API: `TransportEndpoint::from_bind_string()`

Canonical parser for ecosystem bind strings. Handles all formats:
- `unix:///path/to/socket.sock` → `TransportEndpoint::Uds`
- `/absolute/path.sock` → `TransportEndpoint::Uds`
- `tcp://host:port` → `TransportEndpoint::Tcp`
- `host:port` → `TransportEndpoint::Tcp`

Lives in `transport.rs` — accessible from both lib and bin targets.

### L2 (Permissions) / L3 (Device backends)

Zero exposure. coralReef is a pure compiler primal — no `PermissionsExt`,
no `set_mode`, no `rustix`/`libc` for device backends.

## G68 AUDIT SUMMARY

| Classification | Count | Notes |
|----------------|------:|-------|
| Same thing differently | 45 | G66 transport enums, async/sync delegation, Windows symlinks, signal handling |
| Silicon deism (was) | 18 | All evolved to `TransportEndpoint`-based transport-agnostic paths |
| Silicon deism (remaining) | 0 | All `#[cfg(unix)]` now confined to `transport.rs` (G66 substrate) |

Remaining `#[cfg(unix)]` in `transport.rs` is legitimate — that's where
platform gates belong per G66. Business logic never touches `#[cfg(unix)]`.

## PRE-EXISTING CLIPPY FIXES

- `protocol_negotiation.rs`: `items_after_statements` in 3 test functions
- `tolerances.rs`: `assertions_on_constants` in 12 test assertions

## CROSS-ARCH STATUS

- `cargo clippy --all-features --all-targets -- -D warnings` — zero warnings (Linux)
- `cargo clippy --target x86_64-pc-windows-gnu --all-features -- -D warnings` — zero warnings

## TEST STATUS

- All tests pass, 0 failures, 6 ignored (hardware-gated)
- Zero `unsafe` in production
- Zero clippy warnings on Linux + Windows

---

*coralReef Wave 157a. G68 deep evolution: 18 silicon deism sites evolved to
TransportEndpoint-based transport-agnostic paths. Ecosystem registration,
BTSP discovery, provenance signing all work on non-Unix via TCP when
discovered. Zero L2/L3 exposure. Cross-arch PASS.*
