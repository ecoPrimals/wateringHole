# petalTongue v1.6.7 — `live` Mode + BTSP Wire-Format Fix

**Date**: April 21, 2026
**From**: petalTongue team
**Ref**: primalSpring Phase 45b audit

## Summary

Two changes that unblock interactive desktop NUCLEUS deployment:

1. **`petaltongue live` subcommand** — merges `ui` (egui/eframe) and `server` (UDS JSON-RPC IPC) into a single process
2. **BTSP wire-format detection fix** — correctly classifies `{"protocol":"btsp",...}` as BTSP announcement instead of invalid JSON-RPC

## `petaltongue live` Mode

### Architecture

```
domain logic ──► visualization.render.scene ──► egui window
     ▲                                              │
     └◄────── interaction.poll ◄── user input ◄─────┘
```

- IPC server (`UnixSocketServer`) runs as a background `tokio::spawn` task
- egui window runs on main thread via `tokio::task::spawn_blocking`
- Connected via shared state:
  - `Arc<RwLock<VisualizationState>>` — scene data
  - `Arc<RwLock<SensorStreamRegistry>>` — sensor streams
  - `Arc<RwLock<InteractionSubscriberRegistry>>` — user input events
  - `UnboundedSender<CallbackDispatch>` — PT-06 push delivery

### CLI

```bash
petaltongue live
petaltongue live --socket /run/user/1000/biomeos/petaltongue-myfamily.sock
petaltongue live --port 9090
petaltongue live --scenario scenario.json --no-audio
```

### Files

| File | Action |
|------|--------|
| `src/live_mode.rs` | **Created** — combines server + UI with shared state |
| `src/main.rs` | **Modified** — `Commands::Live` variant, dispatch, `mod live_mode` |

## BTSP Wire-Format Detection Fix

### Problem

primalSpring sends `{"protocol":"btsp","version":"1.0",...}` as a JSON-line announcement.
Previous first-byte peek logic classified all `{`-starting messages as JSON-RPC, causing
deserialization failures (no `jsonrpc`/`method`/`id` fields).

### Fix

Three-way classification via `is_btsp_json_announcement()`:

| First byte | Peek content | Classification |
|------------|-------------|----------------|
| Not `{` | — | BTSP length-prefixed framing |
| `{` | Contains `"protocol"` | BTSP JSON-line announcement → handshake |
| `{` | No `"protocol"` | Plain JSON-RPC (unchanged) |

Applied to both `handle_uds_with_btsp` and `handle_tcp_with_btsp`. TCP peek buffer
increased from 1 to 64 bytes. UDS already uses `BufReader::fill_buf()` which returns
all available bytes.

### Files

| File | Action |
|------|--------|
| `crates/petal-tongue-ipc/src/unix_socket_server.rs` | **Modified** — new `is_btsp_json_announcement()`, enhanced peek in both handlers |
| `crates/petal-tongue-ipc/src/unix_socket_server_tests.rs` | **Modified** — 5 new tests for wire-format classification |

## Verification

- `cargo clippy --workspace --all-targets --all-features` — 0 new warnings
- `cargo test --workspace --all-features` — all passing
- `cargo check --target x86_64-apple-darwin` — macOS cross-check clean
- 5 new unit tests for BTSP peek classification (all pass)
