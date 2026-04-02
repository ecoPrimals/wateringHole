# biomeOS v2.76 — Deep Debt: Engine Refactor + Convention-Based Socket Env

**Date**: March 28, 2026
**Version**: v2.76
**Tests**: 7,202 passing, 0 failures, 0 Clippy warnings

## Summary

Deep debt evolution focused on smart refactoring, convention-based socket environment variables, and unused dependency cleanup. No new features — pure codebase quality improvement.

## Changes

### 1. Smart Refactor: socket_discovery/engine.rs (916 → 423 + 497 lines)

**Before**: Single 916-line file mixing public API orchestration, transport probes, filesystem discovery, manifest parsing, socket registry queries, and cache operations.

**After**: Split by concern into:
- `engine.rs` (423 lines): Public API (`discover_primal`, `discover_capability`, `discover_with_fallback`), struct definition, constructors, cache, helpers
- `engine_probes.rs` (497 lines): Transport probe implementations — environment hints, XDG/tmp filesystem discovery, capability sockets, manifest discovery, socket registry, abstract socket probes, TCP fallback, and connection verification

### 2. Convention-Based Socket Env Keys

**Before**: Hardcoded per-primal env var strings:
```rust
.env("BEARDOG_SOCKET", &security_socket)
.env("TOADSTOOL_SOCKET", socket_path.as_os_str())
.env("SQUIRREL_SOCKET", socket_path.as_os_str())
```

**After**: Convention-derived via `socket_env_key()`:
```rust
let self_socket_key = socket_env_key(config.name);
cmd.env(&self_socket_key, socket_path.as_os_str());
// ...
cmd.env(socket_env_key(BEARDOG), &security_socket);
```

Files evolved: `nucleus.rs`, `trust.rs`, `http_client.rs`, `beardog.rs`

### 3. Unused Workspace Dependencies Removed

Removed from `[workspace.dependencies]`:
- `rfd` (v0.14) — native file dialog, pulls C dependencies, no member crate referenced it
- `image` (v0.24) — image processing, no member crate referenced it

### 4. test-utils Documentation

`biomeos-test-utils` `#![allow(clippy::expect_used, clippy::unwrap_used)]` now has a documented reason. `#![expect]` not applicable because the non-test production surface has zero unwrap/expect calls — all `.unwrap()` calls live inside `#[cfg(test)]` blocks with their own `#[expect]`.

## Audit Summary

The comprehensive deep debt audit found:
- **Zero** `#[allow]` in production code (all migrated to `#[expect]` in prior versions)
- **Zero** `unsafe` code in production (only in test-utils `env_helpers.rs` — necessary for `set_var`, already has `#[expect]`)
- **Zero** `todo!()` / `panic!()` / `unimplemented!()` in production
- **Zero** `TODO` / `FIXME` / `HACK` markers in production code
- **Zero** mock implementations in production code (all isolated to test)
- **Zero** `.unwrap()` in production runtime paths (all in test code)

## Files Changed

| File | Change |
|------|--------|
| `crates/biomeos-core/src/socket_discovery/engine.rs` | Slimmed from 916 to 423 lines |
| `crates/biomeos-core/src/socket_discovery/engine_probes.rs` | **NEW** — 497 lines extracted |
| `crates/biomeos-core/src/socket_discovery/mod.rs` | Added `mod engine_probes` |
| `crates/biomeos/src/modes/nucleus.rs` | Convention-based `socket_env_key()` |
| `crates/biomeos-api/src/handlers/trust.rs` | `socket_env_key("beardog")` |
| `crates/biomeos-atomic-deploy/src/http_client.rs` | `socket_env_key(SONGBIRD)` |
| `crates/biomeos-federation/src/subfederation/beardog.rs` | `socket_env_key("beardog")` |
| `crates/biomeos-test-utils/src/lib.rs` | Documented `#![allow]` reason |
| `Cargo.toml` | Removed `rfd`, `image` workspace deps |
| Root docs (6 files) | Version bump v2.75→v2.76 |
| `CHANGELOG.md` | New v2.76 entry |
