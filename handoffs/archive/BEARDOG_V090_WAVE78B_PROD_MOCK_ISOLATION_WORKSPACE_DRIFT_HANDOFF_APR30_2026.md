<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 78b Handoff: Production Mock Isolation, Workspace Drift & Dead Feature

**Date**: April 30, 2026
**From**: BearDog Team
**To**: ecoPrimals ecosystem — informational, no consumer action required

---

## Summary

Internal code hygiene pass. Zero behavior changes, zero new RPC methods, zero API surface changes.

## Changes

### Production Mocks Gated Behind `#[cfg(test)]`

`ipc_server.rs` contained test-only types compiled into the production library:
- `IpcTestHandler`, `IpcFailingRegisterHandler`, `IpcFailingEventHandler`, `IpcFailingCapabilityHandler`
- `IpcHandlerBackend` enum dispatch
- `IpcServer` struct (legacy server; production uses `UnixSocketIpcServer`)

These included `unreachable!()` panic paths that shipped in release binaries. All moved
into a `#[cfg(test)] mod test_fixtures` submodule — zero test regression (19/19 pass).

### Workspace Dependency Drift (10 deps centralized)

| Dependency | Crates affected |
|-----------|-----------------|
| `crossbeam` | beardog-types, beardog-utils |
| `dashmap` | beardog-utils |
| `http` | beardog-core |
| `url` | beardog-discovery |
| `walkdir` | beardog-deploy |
| `dotenvy` | beardog-config |
| `dirs` | beardog-config |
| `tokio-stream` | beardog-security |
| `getrandom` | beardog-types |

All converted from explicit version pins to `{ workspace = true }`.

### Dead Feature Removed

`android_native = []` in `beardog-tunnel/Cargo.toml` — declared and emitted by `build.rs`
on Android targets but never checked via `cfg(feature)` in any Rust source.

### Deprecation Form Normalized

`#[deprecated = "msg"]` (legacy string form) in `primal_types/io.rs` converted to
structured `#[deprecated(since = "0.9.0", note = "Use CapabilityBasedEcosystem instead")]`.

## CI Status

- `cargo fmt --check` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo deny check` — 4/4 PASS (advisories, bans, licenses, sources)
- `cargo check --workspace` — clean
- ipc_server tests: 19/19 pass
