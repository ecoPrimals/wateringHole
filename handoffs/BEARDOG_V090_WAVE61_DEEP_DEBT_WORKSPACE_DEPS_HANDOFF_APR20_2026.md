<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 61: Deep Debt — Workspace Dep Normalization + Cross-Arch Fix

**Date**: April 20, 2026
**Primal**: BearDog (Security / Crypto)
**Wave**: 61
**Type**: Dependency normalization, cross-platform compilation fix, deep debt survey

---

## Changes

### Cross-Arch Compilation Fix (primalSpring Audit)

Resolved macOS/iOS/Windows/WASM compilation errors reported by primalSpring:

- **E0596** (`discovery_engine.rs`) — Platform-specific HSM implementations moved inline into `vec![]` with `#[cfg]` attrs.
- **E0053** (`ios.rs`, `windows.rs`, `wasm.rs`) — `PlatformSocket::bind` return type corrected from `io::Result<UnixListener>` to `io::Result<Box<PlatformListenerBackend>>`.
- Added `pub(super)` constructor on `UnixPlatformListener` for cross-module macOS path.

### Workspace Dependency Normalization (9 crates, 40+ pins)

Normalized explicit version pins to `{ workspace = true }` across:

| Crate | Deps Normalized |
|-------|----------------|
| beardog-discovery | tokio, serde, serde_json, toml, anyhow, tracing, chrono, tempfile, tokio-test, tracing-subscriber |
| beardog-workflows | parking_lot, hex, hmac, sha2, base64, tokio-test |
| beardog-capabilities | tokio, serde, serde_json, parking_lot, uuid, chrono, tracing, zeroize, tokio-test |
| beardog-traits | serde_json, uuid, serde, chrono, tokio |
| beardog-utils | tracing, parking_lot, tokio, serde, chrono, pbkdf2, hmac, hkdf, hex, futures, serial_test |
| beardog-tower-atomic | tokio, serde, serde_json, tracing, tokio-test, tracing-subscriber, tempfile |
| beardog-production | hkdf |
| beardog-monitoring | serial_test (version drift 3.2.0 → workspace 3.0) |
| beardog-types | semver |

### Deep Debt Survey Results

Comprehensive audit found:

- **Zero production files >800 LOC** (10 files >800 are all test-only)
- **Zero unsafe code** in production
- **Zero TODO/FIXME/HACK** markers
- **Zero commented-out code**
- **Zero hardcoded peer primal names** (only `biomeOS` platform name in log messages)
- **Production stubs reviewed** — `unix_socket_placeholder_addr` (sentinel SocketAddr for UDS) and `compliance_simulation_flag` (dry-run feature) are legitimate implementations
- **`Box<dyn PlatformStream>`** kept — I/O trait object with PrefixedStream wrapping makes enum dispatch impractical
- **`Pin<Box<dyn Future>>`** in consolidated_registry — legitimate type erasure for open-ended provider traits

---

## Quality Gates

- 14,786+ tests, 0 failures
- Zero clippy warnings (`-D warnings`)
- Zero rustfmt diffs
- Zero rustdoc warnings
- All production files <800 LOC

---

## Remaining `#[allow()]` Inventory

| Category | Count | Reason |
|----------|-------|--------|
| `deprecated` (re-exports) | ~7 | `#[expect]` unfulfillable on deprecated re-exports (rustc limitation) |
| `async_fn_in_trait` | 2 | Lint unfulfilled in Rust 1.93 — stays as `#[allow]` |
| `unreachable_patterns` | 2 | Conditional compilation — lint only fires when features disabled |
| `dead_code` (beardog-cli) | ~15 | CLI handler scaffolding for upcoming features |
| `clippy::wildcard_imports` | 2 | Monitoring glob re-exports (documented) |
| `ambiguous_glob_reexports` | 1 | Monitoring module re-exports (documented) |
| `clippy::upper_case_acronyms` | 1 | HSM acronym in config type |
| `unused_imports` (beardog-cli) | ~5 | Platform-conditional imports |

All remaining `#[allow()]` instances have documented `reason` strings and are either unfulfillable with `#[expect()]` or conditionally compiled.
