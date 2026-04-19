# BearDog v0.9.0 — Wave 59 Handoff

**Date**: April 20, 2026
**Trigger**: Deep debt execution — enum dispatch, workspace deps, test refactoring
**Commit**: `ae23b8c55`

## What Changed

### 1. Box<dyn> → Enum Dispatch

Two production `Box<dyn>` patterns replaced with zero-allocation enum dispatch:

- **`ProtocolHandlerBackend`** (beardog-core): replaces `Box<dyn ProtocolHandler>` in universal discovery service. 2 variants: `Minimal`, `Mdns` (feature-gated).
- **`IpcStream`** (beardog-ipc): replaces `Box<dyn AsyncStream>` in `connect_beardog()`. 2 variants: `Unix(UnixStream)`, `Tcp(TcpStream)`. Implements `AsyncRead + AsyncWrite` via direct delegation.

Remaining `Box<dyn PlatformStream>` is intentionally kept — I/O trait object overhead is negligible vs socket latency, and `PrefixedStream` recursive wrapping makes enum dispatch impractical.

### 2. Workspace Dependency Normalization

- `beardog-hid`: `libc = "0.2"` → `{ workspace = true }`
- `beardog-adapters`: 12 explicit version pins → workspace refs (serde_json, tracing, sha2, ed25519-dalek, blake3, hex, serde, tokio, chrono, uuid, semver, crossterm)
- `beardog-genetics`: 8 explicit version pins → workspace refs (serde_json, hex, ed25519-dalek, blake3, hkdf, chacha20poly1305, parking_lot, crossterm)
- `semver` and `crossterm` added to `[workspace.dependencies]`

### 3. #[allow()] → #[expect()] Migration

7 production `#[allow()]` attributes migrated to `#[expect()]` with explicit reason strings:
- 6× `async_fn_in_trait` on trait definitions across beardog-tunnel, beardog-core, beardog-types
- 1× `clippy::cast_precision_loss` for memory-size f64 cast

### 4. Test File Refactoring

- **`fault_injection/mod.rs`** (966 → 546 LOC): Split into `config_fault_tests.rs`, `crypto_fault_tests.rs`, `ipc_fault_tests.rs`, `state_fault_tests.rs` + `framework_tests` inline module
- **`graph_security_integration_tests.rs`** (881 LOC): Split into `helpers.rs` + `core_rpc_tests.rs` + `peer_scenario_tests.rs`

### 5. Dependency Audit

- `blake3` `pure` feature confirmed active; `cc` only a build-dep, not compiled
- `lazy_static` in lockfile is transitive from `rsa` → `num-bigint-dig` (upstream issue)
- Zero `unsafe` blocks in production code; `#![forbid(unsafe_code)]` workspace-wide

## Quality Gate

| Check | Status |
|-------|--------|
| `cargo fmt` | Clean |
| `cargo clippy --workspace -D warnings` | 0 warnings |
| `cargo test --workspace` | 14,786 passing, 0 failures |
| `cargo deny check` | All 4 checks pass |
