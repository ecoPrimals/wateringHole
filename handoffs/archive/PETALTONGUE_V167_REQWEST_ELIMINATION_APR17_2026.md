# petalTongue v1.6.7 — reqwest Elimination / Songbird TLS Delegation

**Date**: April 17, 2026
**Primal**: petalTongue
**Sprint**: Stadial blocker resolution
**Commit**: `a32bf60` on `main`

## Summary

`reqwest` runtime dependency fully eliminated from petalTongue. Replaced with
thin `LocalHttpClient` in `petal-tongue-ipc` built on `hyper` + `hyper-util`
(already transitive from `axum` — zero new crate additions to the lockfile).

The entire TLS transitive chain is gone from `Cargo.lock`:
- `reqwest` — removed
- `hyper-rustls` — removed
- `rustls` — removed
- `rustls-webpki` — removed
- `ring` — removed (was phantom lockfile entry, now fully gone)

petalTongue no longer owns any TLS stack. External HTTPS is delegated to
Songbird via tower atomic IPC (design ready, implementation pending Songbird
relay protocol).

## What Changed

### New: `LocalHttpClient` (`petal-tongue-ipc/src/http_client.rs`)

Thin HTTP client wrapping `hyper-util::client::legacy::Client`:
- `get(url)` / `get_with_headers(url, headers)` — GET requests
- `post_json(url, body)` / `post_json_with_headers(url, body, headers)` — JSON POST
- `post_raw(url, body, content_type)` — raw byte POST
- `get_stream(url, headers)` — streaming GET (SSE support)
- `HttpResponse` with `.status()`, `.is_success()`, `.json()`, `.text()`, `.bytes()`
- Configurable timeouts, connection pooling
- `http_get(url)` convenience function

### 6 Crates Migrated (13 code sites)

| Crate | Files Changed | What |
|-------|--------------|------|
| `petal-tongue-api` | `biomeos_client.rs`, `biomeos_error.rs` | BiomeOS HTTP client + error type |
| `petal-tongue-core` | `error.rs` | `BiomeOSApi(reqwest::Error)` → `BiomeOSApi(String)` |
| `petal-tongue-discovery` | `mdns_provider/mod.rs`, `errors.rs`, `retry.rs` | mDNS HTTP queries, error types, doctests |
| `petal-tongue-entropy` | `stream.rs`, `error.rs` | Entropy POST streaming |
| `petal-tongue-ui` | `sse.rs`, `state.rs`, `connect.rs`, `https_client.rs`, `universal_discovery.rs` | SSE consumer, entropy window, protocol selection, HTTP fallback, universal discovery |
| `petal-tongue-adapters` | `Cargo.toml` | Dead `reqwest` dep removed (never used in code) |

### Workspace Dependencies

Added to workspace `Cargo.toml`:
- `hyper = { version = "1", features = ["client", "http1"] }`
- `hyper-util = { version = "0.1", features = ["client-legacy", "http1", "tokio"] }`
- `http-body-util = "0.1"`
- `http = "1"`

All four were already in `Cargo.lock` as transitive deps of `axum`.
Declaring them as workspace deps adds zero new crates.

## Verification

- `cargo tree -i reqwest` → "did not match any packages"
- `grep -c reqwest Cargo.lock` → 0
- `grep -c ring Cargo.lock` → 0
- `grep -c rustls Cargo.lock` → 0
- `cargo check --workspace` — clean
- `cargo clippy --workspace --all-targets` — clean (zero new warnings)
- `cargo test --workspace` — 6,010+ passing, 0 failures

## Stadial Gate Status

| Gate Criterion | Status |
|----------------|--------|
| `async-trait` eliminated | Done (Sprint 8) |
| `ring` in Cargo.lock | **Eliminated** |
| `reqwest` runtime dep | **Eliminated** |
| `~18 dyn` usages | Done (Sprint 8) |
| `cargo deny` passes | Yes |

All stadial blockers for petalTongue are resolved.

## Architecture Note

`LocalHttpClient` is designed as a Songbird-ready abstraction. When Songbird
exposes an HTTP relay method over JSON-RPC (e.g. `http.request`), the client
internals can be swapped from direct hyper to IPC dispatch without changing any
call sites. The `HttpClientError` type is already protocol-agnostic.
