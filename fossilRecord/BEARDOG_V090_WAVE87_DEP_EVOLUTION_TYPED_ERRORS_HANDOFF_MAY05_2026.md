# BearDog v0.9.0 — Wave 87 Handoff

**Date**: May 5, 2026
**Status**: Committed and pushed
**Branch**: main

---

## Summary

Wave 87 executes deep dependency evolution and begins the `Result<_, String>`
→ typed error migration in `beardog-config`.

## Changes

### 1. Dependency Evolution: crossterm 0.27 → 0.29

- Eliminates `mio` version duplication (0.8 + 1.0 → unified 1.x)
- crossterm 0.29 uses `mio ^1.0`, aligning with tokio's reactor
- Zero API breakage — our usage (event, terminal, cursor, style) is stable

### 2. Deep Dependency Audit Results

| Category | Finding | Action |
|----------|---------|--------|
| `syn` transitive | Build-time only (proc macros) | Not actionable — standard for derive-heavy Rust |
| `tokio` features | All features used across workspace | `full` justified; no trim possible |
| `rand` 0.8 / 0.9 | From `rsa` + `tungstenite` upstream | Awaiting upstream upgrades |
| `thiserror` 1 / 2 | From `x509-parser` / `asn1-rs` upstream | Awaiting upstream upgrades |
| `getrandom` 0.2/0.3/0.4 | Multi-source | Minimal runtime cost; monitoring |
| `hashbrown` 0.14/0.17 | `dashmap` vs `toml_edit` | Accept until ecosystem converges |
| `socket2` 0.5/0.6 | `mdns-sd` vs `tokio` | Bump mdns-sd when compatible |
| Large files (>800 LOC) | 0 in crates/ | Clean |
| Unsafe code | 0 blocks | All crates `#![forbid(unsafe_code)]` |
| async-trait | Eliminated | Gone from Cargo.lock |
| Production mocks | 0 | All properly `#[cfg(test)]` gated |
| Hardcoded primal names | 0 | Clean |
| TODO/FIXME/HACK/XXX | 0 | Clean |
| `todo!()` / `unimplemented!()` | 0 | Clean |

### 3. Typed Error Migration: beardog-config (5 sites → 0 String errors)

Migrated all `Result<(), String>` validators to `ConfigResult<()>`:

| File | Before | After |
|------|--------|-------|
| `network_ports.rs` | `Result<(), String>` | `ConfigResult<()>` with `InvalidValue` / `PortConflict` |
| `network_addresses.rs` | `Result<(), String>` | `ConfigResult<()>` with `InvalidValue` |
| `network_hosts.rs` | `Result<(), String>` | `ConfigResult<()>` with `InvalidValue` |
| `timeouts_new/validation.rs` | `Result<(), String>` | `ConfigResult<()>` with `InvalidValue` + `range_check()` DRY helper |
| `timeouts_new/core.rs` | `Result<(), String>` (delegate) | `ConfigResult<()>` |

Removed `map_err(ConfigError::Validation)` wrappers in `network.rs` and `lib.rs`.

### 4. Remaining Result<_, String> Inventory

| Crate | Count | Notes |
|-------|-------|-------|
| `beardog-tunnel` | 183 | IPC handlers, crypto, ionic bond — largest migration target |
| `beardog-types` | 30 | Mostly `validate()` helpers |
| `beardog-core` | 1 | `socket_config.rs` |
| `beardog-auth` | 1 | `OnceLock` internals |
| **beardog-config** | **0** | **Fully migrated this wave** |

## CI Status

- `cargo fmt`: clean
- `cargo clippy --workspace`: 0 warnings (library targets)
- `cargo test --workspace`: 0 failures

---

_Handoff from bearDog Wave 87 — May 5, 2026_
