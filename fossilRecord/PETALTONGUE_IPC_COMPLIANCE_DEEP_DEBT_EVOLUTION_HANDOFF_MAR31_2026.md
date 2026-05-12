# petalTongue IPC Compliance + Deep Debt Evolution

**Date**: March 31, 2026
**Primal**: petalTongue (Universal User Interface)
**Phase**: IPC compliance evolution + deep debt resolution
**Triggered by**: IPC_COMPLIANCE_MATRIX v1.2 audit, PRIMAL_GAPS PT-01 through PT-07

---

## Summary

Comprehensive IPC compliance evolution and deep technical debt resolution for
petalTongue, addressing all HIGH-severity gaps from `IPC_COMPLIANCE_MATRIX.md`
v1.2, `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2,
`CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1, and
`PRIMALSPRING_COMPOSITION_GUIDANCE.md`.

---

## Changes by Category

### PT-01: Socket Path (Critical — was blocking composition)

**Before**: `$XDG_RUNTIME_DIR/petaltongue/petaltongue-nat0-default.sock`
**After**: `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`

- `socket_path.rs`: Rewrote `get_petaltongue_socket_path()` and `discover_primal_socket()` to use shared `biomeos/` directory
- Fallback: `/tmp/biomeos/petaltongue.sock`
- `PETALTONGUE_SOCKET` env override still takes priority
- Updated all consumer code: `client.rs`, `discovery_helpers.rs`, `primal_registration.rs`, `biomeos_jsonrpc_client.rs`, `server.rs`
- Updated `manifest.toml` socket_pattern
- Updated `ENV_VARS.md` documentation

### PT-02: TCP JSON-RPC via `--port` (High)

- Made `handle_connection` generic over `AsyncRead + AsyncWrite + Unpin` (was `UnixStream`-only)
- Added `tcp_port: Option<u16>` to `UnixSocketServer` with `with_tcp_port()` builder
- `start()` uses `tokio::select!` to accept on both UDS and TCP concurrently
- Wired `--port` flag through `Commands::Server { port }` → `server_mode::run()`
- Usage: `petaltongue server --port 9100`

### PT-03: SSE Push for Web Mode (High)

- Added `/api/events` SSE endpoint to axum router
- `DataService::subscribe()` broadcast → `BroadcastStream` → SSE frames
- Added `snapshot_sync()` for non-async stream contexts
- 15-second keepalive
- Added `tokio-stream` dependency with `sync` feature

### RPC Method Compliance (SEMANTIC_METHOD_NAMING_STANDARD v2.2)

- **New handler: `identity.get`** — returns primal identity per CAPABILITY_BASED_DISCOVERY_STANDARD
- **New handler: `lifecycle.status`** — returns lifecycle state per PRIMALSPRING_COMPOSITION_GUIDANCE
- **Health aliases**: `ping` → liveness, `health` → liveness, `status` → health.check, `check` → health.check
- **Capabilities alias**: `primal.capabilities` now routes alongside `capabilities.list` and `capability.list`
- **Response shape alignment**: `health.liveness` → `{"status": "alive", "alive": true}`, `health.readiness` → `{"status": "ready", ...}`
- **Dynamic transport**: `capabilities.list` transport field reflects actual TCP state

### motor_tx Wiring (Server Mode)

- Created `mpsc::channel` in `server_mode::run()`, passed to server via `with_motor_sender()`
- `spawn_blocking` drains receiver and logs at `debug` — prevents `motor.*` IPC methods from erroring without a display

### Manifest Cleanup

- Removed `lifecycle.register` from methods list (petalTongue calls this outbound, doesn't serve it)
- Updated `socket_pattern` to `${XDG_RUNTIME_DIR}/biomeos/petaltongue.sock`
- Changed `capability.list` to `capabilities.list` (canonical name)

### Clippy / Test Fixes

- Fixed 20+ clippy errors across 8 crates (midpoint, redundant clones, dead_code, format args, Default::default field assignment, etc.)
- Fixed `introspect_bound_data_empty_graph` test (headless now pre-populates graph)

### Deep Debt Resolution

- **Socket path migration**: All client-side socket construction moved to `biomeos/{primal}.sock` standard
- **Dead code cleanup**: Removed module-wide `#![allow(dead_code)]` from `cache.rs`, removed unused `DiscoveredProvider` alias
- **Primal name constants**: Replaced hardcoded string literals in `provenance_trio.rs` with `capability_names::primal_names::*`
- **Large file refactor**: Split `ui_components.rs` (901 lines) → directory module with 6 focused submodules
- **IPC crate docs**: Corrected protocol priority from "tarpc PRIMARY" to "JSON-RPC PRIMARY (listen), tarpc (outbound client)"

---

## IPC Compliance Matrix Status (After)

| Dimension | Before | After |
|-----------|--------|-------|
| Socket Path | **X** | **C** (`biomeos/petaltongue.sock`) |
| --port TCP | **X** | **C** (`server --port <N>`) |
| Wire Framing | P (UDS only) | **C** (UDS + TCP) |
| Health Names | ? | **C** (with aliases: ping, health, status, check) |
| identity.get | **X** | **C** |
| lifecycle.status | **X** | **C** |
| capabilities.list | P (alias only) | **C** (canonical + 2 aliases) |
| SSE/WS Push | **X** | **C** (`/api/events` SSE) |
| motor_tx server | **X** | **C** (channel drain) |
| Standalone | C | C |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo fmt --check --all` | PASS |
| `cargo test --workspace` | PASS (5,834+ tests, 0 failures) |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |
| `cargo llvm-cov --workspace --summary-only` | ~90% line coverage |
| All files < 1,000 LOC | PASS |
| SPDX headers | PASS (all 602 .rs files) |
| Zero unsafe code | PASS |
| Zero C dependencies | PASS |

---

## Ecosystem Impact

- **primalSpring**: petalTongue now passes composition gate probes (`health.*`, `capabilities.list`, `identity.get`, `lifecycle.status`)
- **sourDough**: Socket at `biomeos/petaltongue.sock` is discoverable by biomeOS socket scanning
- **Mobile substrates**: TCP JSON-RPC available via `--port` for cross-gate access
- **Web consumers**: SSE push eliminates polling for live topology updates
- **All primals**: `motor.*` IPC methods now succeed in server/web mode (no display required)

---

## Deferred (Future PRs)

- **EguiShapes variant**: `ModalityOutput::EguiShapes` for native egui shape consumption
- **aarch64 headless cross-compile**: `cargo-zigbuild` CI job for `aarch64-unknown-linux-musl`
- **Domain symlinks**: `$XDG_RUNTIME_DIR/biomeos/visualization → petaltongue.sock`
- **Zero-copy IPC**: `serde_json::to_writer` in connection handler
- **JSON-RPC batch requests**: Protocol completeness
- **Abstract Unix sockets**: `--abstract` flag for Android/SELinux (UniBin v1.2)

---

*5,834+ tests passing, 18 ignored, ~90% line coverage.
Zero clippy warnings. Zero fmt drift. Zero files over 1,000 LOC.
All pure Rust. Sovereignty is a runtime choice.*
