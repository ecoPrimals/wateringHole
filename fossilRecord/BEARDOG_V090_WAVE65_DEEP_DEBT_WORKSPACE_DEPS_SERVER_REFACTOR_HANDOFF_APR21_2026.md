# BearDog v0.9.0 — Wave 65: Deep Debt — Workspace Dep Normalization, server.rs Smart Refactor

**Date:** April 21, 2026
**Primal:** BearDog v0.9.0
**Wave:** 65
**Commit:** `9ccbc32f1`
**Type:** Deep Debt / Refactoring

---

## Summary

Wave 65 continues the deep debt pass with two structural improvements:
workspace dependency normalization for the final 6 explicit version pins,
and a smart refactor of the largest production file (`server.rs`).

## Changes

### 1. Workspace Dependency Normalization

6 explicit version pins across 6 crate `Cargo.toml` files migrated to
`{ workspace = true }`, with versions centralized in root `Cargo.toml`:

| Dependency | Crates | Before | After |
|-----------|--------|--------|-------|
| `mdns-sd` | beardog-adapters, beardog-capabilities, beardog-core, beardog-discovery | `version = "0.11"` | `workspace = true` |
| `validator` | beardog-config | `version = "0.20", features = ["derive"]` | `workspace = true` |
| `tokio-serde` | beardog-tunnel | `version = "0.9", features = ["json"]` | `workspace = true` |

All crates now use workspace deps exclusively — zero explicit version pins remain.

### 2. server.rs Smart Refactor

`crates/beardog-tunnel/src/unix_socket_ipc/server.rs` exceeded the 800 LOC
guideline (834 LOC). Extracted 5 protocol-specific connection handlers by
domain concern:

| Method | Purpose |
|--------|---------|
| `handle_jsonrpc_universal` | JSON-RPC over any stream |
| `handle_http_universal` | HTTP request handling |
| `handle_btsp_jsonline_connection` | JSON-line BTSP handshake orchestration |
| `handle_jsonrpc_ndjson_loop` | Plain NDJSON JSON-RPC (post-handshake, null cipher) |
| `handle_jsonrpc_btsp` | Encrypted BTSP frame handler |

**Result:** `server.rs` 834 → 619 LOC, `connection_handlers.rs` 231 LOC.
Inter-module visibility via `pub(super)`.

### 3. Mock Isolation Verification

`hsm_provider_mocks.rs` confirmed correctly gated with `#[cfg(test)]` at
module declaration (line 26 of parent `mod.rs`). Corrected false positive
from prior survey.

## Quality

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (0 warnings) |
| `cargo deny check` | PASS (4/4) |
| `cargo test --workspace` | 14,921+ tests, 0 failures (1 known flaky pre-existing) |

## Files Changed

- `Cargo.toml` (root) — added 3 workspace deps
- `crates/beardog-adapters/Cargo.toml` — mdns-sd workspace
- `crates/beardog-capabilities/Cargo.toml` — mdns-sd workspace
- `crates/beardog-core/Cargo.toml` — mdns-sd workspace
- `crates/beardog-discovery/Cargo.toml` — mdns-sd workspace
- `crates/beardog-config/Cargo.toml` — validator workspace
- `crates/beardog-tunnel/Cargo.toml` — tokio-serde workspace
- `crates/beardog-tunnel/src/unix_socket_ipc/server.rs` — reduced to 619 LOC
- `crates/beardog-tunnel/src/unix_socket_ipc/connection_handlers.rs` — NEW (231 LOC)
- `crates/beardog-tunnel/src/unix_socket_ipc/mod.rs` — added `mod connection_handlers`
