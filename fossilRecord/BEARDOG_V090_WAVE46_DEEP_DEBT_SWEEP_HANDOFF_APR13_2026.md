<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 46: Deep Debt Sweep Handoff

**Date**: April 13, 2026
**Author**: bearDog team (automated)
**Commit**: (see bearDog repo HEAD)

---

## Summary

Wave 46 addresses accumulated technical debt identified by comprehensive audit:
dead Cargo features, dependency version drift, production wildcard imports, and
large production files (>800 LOC).

## Changes

### Dead Cargo Features Removed (6)

| Crate | Feature | Reason |
|-------|---------|--------|
| beardog-ipc | `json-rpc` | Zero `cfg(feature)` gates in source |
| beardog-discovery | `service-registry` | Zero `cfg(feature)` gates in source |
| beardog-tunnel | `pixel8_optimizations` | Zero `cfg(feature)` gates in source |
| beardog-tunnel | `strongbox_hardware` | Zero `cfg(feature)` gates in source |
| beardog-integration | `mock-upa` | Zero `cfg(feature)` gates in source |
| beardog-cli | `pure-rust` | Enabled `adb_client` + `nusb` — both unused in source |

### Unused Optional Dependencies Removed (2)

- `adb_client` 0.8 (beardog-cli) — gated behind dead `pure-rust` feature
- `nusb` 0.1 (beardog-cli) — gated behind dead `pure-rust` feature

### Production Wildcard Import Eliminated

- `crates/beardog-tunnel/src/tunnel/hsm/ios_secure_enclave/capability.rs`:
  `use super::types::*` → explicit `{BiometricFeature, BiometricPolicy, IOSVersion, SecureEnclaveCapability, SecureEnclaveDevice}`

### Dependency Version Drift Fixed

| Crate | Dependency | Was | Now |
|-------|-----------|-----|-----|
| beardog-integration | thiserror | "1.0" | workspace (2.0) |
| beardog-hid | tokio | "1.43" | workspace (1.35) |
| beardog-client | tokio | "1.43" | workspace (1.35) |
| beardog-integration | tokio | "1.35" (explicit) | workspace = true |
| beardog-hid | tracing | "0.1" | workspace = true |
| beardog-hid | async-trait | "0.1" | workspace = true |
| beardog-client | serde, serde_json, anyhow, thiserror, tracing, chrono, tempfile | explicit versions | workspace = true |
| beardog-integration | serde, serde_json, async-trait, futures, tracing, tracing-subscriber, chrono | explicit versions | workspace = true |

### Large File Refactoring (Test Extraction)

| File | Before | After | Extracted To |
|------|--------|-------|-------------|
| `beardog-ipc/src/registry_client.rs` | 827 | 427 | `registry_client_inline_tests.rs` |
| `beardog-monitoring/src/monitoring/service.rs` | 822 | 552 | `service_tests.rs` |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | 14,784 passed, 0 failed |

## Upstream Impact

None — internal debt cleanup only. No wire protocol, API, or behavioral changes.
