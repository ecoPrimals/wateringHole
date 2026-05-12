# Songbird v0.2.1 Wave 148 — PG-21 Resolution: Persistent NDJSON Sessions

**Date**: April 20, 2026
**Version**: v0.2.1-wave148
**Trigger**: primalSpring v0.9.16 downstream audit — PG-21 "HTTP framing on UDS"

---

## Summary

The orchestrator's `UnixSocketServer` NDJSON handler (`connection.rs`) was
**single-shot**: it processed one JSON-RPC request/response, then broke out of
the read loop and closed the connection. When downstream springs kept the
connection open for multi-step validation (e.g. `health.liveness` →
`capabilities.list`), the second request hit a closed pipe, which
primalSpring classified as `is_protocol_error()` → SKIP.

The BTSP length-prefixed handler had the same single-shot behavior.

## Root Cause

The PG-21 report described "HTTP framing on UDS". Investigation confirmed
Songbird does **not** serve HTTP on UDS — all UDS paths use raw NDJSON or
BTSP binary framing; HTTP/Axum is TCP-only (`app/http_server.rs`). The
symptom was a closed connection after one exchange, which looked like a
protocol mismatch to the spring's NDJSON client.

The `bin_interface/server.rs` handler (persistent loop) was correct, but the
orchestrator's `UnixSocketServer` in `pure_rust_server/server/connection.rs`
(the path used in NUCLEUS deployments) had an unconditional `break` at line
465 after writing the first response.

## Changes

| File | Change |
|------|--------|
| `connection.rs` | `handle_ndjson_session`: removed unconditional `break` after response — now loops until client EOF |
| `connection.rs` | `handle_btsp_frame` → `handle_btsp_frames`: persistent frame loop after handshake |
| `connection.rs` | Parse errors in both NDJSON and BTSP send error response + `continue` (was `break`) |

## Verification

- `cargo check --workspace` — PASS
- `cargo clippy --workspace -- -D warnings` — PASS (0 warnings)
- `cargo fmt --all --check` — PASS
- `cargo test --workspace --lib` — **7,377 passed**, 0 failed

## Downstream Impact

Springs (hotSpring, healthSpring, wetSpring, ludoSpring, neuralSpring) that
previously saw `is_protocol_error()` → SKIP on Songbird's UDS socket should
now see persistent connections with full multi-request sessions. No spring-side
changes required — their existing NDJSON clients already handle persistent
connections correctly.

## Protocol Documentation

| Transport | Protocol | Handler |
|-----------|----------|---------|
| UDS (orchestrator) | NDJSON or BTSP (first-byte peek: `{` → NDJSON) | `connection.rs` |
| UDS (bin_interface) | NDJSON | `bin_interface/server.rs` |
| UDS (http_gateway) | NDJSON | `http_gateway/unix_listener.rs` |
| UDS (universal IPC) | NDJSON | `tower_atomic/server.rs` |
| TCP (HTTP API) | HTTP/1.1 + Axum (`/jsonrpc` POST) | `app/http_server.rs` |
| TCP (IPC) | NDJSON | `bin_interface/server.rs` |
