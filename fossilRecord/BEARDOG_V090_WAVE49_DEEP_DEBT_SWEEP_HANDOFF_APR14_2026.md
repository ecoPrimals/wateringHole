<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 49: Deep Debt Sweep Handoff

**Date**: April 14, 2026
**Commit**: `4660789d7`

## Summary

Workspace dependency unification, large file smart refactoring, and dead export cleanup.

## Changes

### 1. Workspace Dependency Alignment (5 crates)

| Crate | Dependencies Migrated |
|-------|----------------------|
| `beardog-config` | serde, toml, serde_json, serde_yaml, tracing, tokio, tempfile |
| `beardog-deploy` | tracing, tracing-subscriber, serde_json, clap, tokio, chrono, serde, tempfile |
| `beardog-core` | serde_json, tracing, hex, ed25519-dalek, x25519-dalek, sha2, sha3, toml, async-trait, zeroize, aes-gcm, chacha20poly1305, base64, p256, rsa, hkdf, tokio, serde, uuid, chrono, tokio-test, tracing-subscriber, tempfile, serial_test |
| `beardog-auth` | ed25519-dalek, sha3 |
| `beardog-node-registry` | serde_json (dev) |

### 2. Large File Smart Refactoring

| File | Before | After | Method |
|------|--------|-------|--------|
| `android_strongbox/core.rs` | 850 | 796 | Removed dead shadow `AndroidKeyParams` struct (34 lines); consolidated verbose `base_traits::` paths with `unified::` module alias |
| `cloud_discoverer.rs` | 826 | 790 | Hoisted 7× repeated capability type imports to module level (42 lines eliminated) |

### 3. Dead `pub use` Re-exports Removed

- `beardog-ipc::normalize_method` — zero external references
- `beardog-utils::{BufferPoolSafe, BufferPoolStats, MemoryPoolStats, SafeMemoryPool}` — zero external references via aliased names

### 4. Audited (No Change Needed)

- `#![allow(dead_code)]` in `infrastructure.rs` — documented reason valid (pub serde surface types; `#[expect]` would be unfulfilled)
- `#[allow(dead_code)]` in `beardog-cli` handlers — documented reason (`lib+bin` targets cause false `dead_code` lint)

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy -- -D warnings` | Clean |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | Clean |
| `cargo test --workspace` | 14,784 pass, 0 fail |

## Net Impact

- **+105 / −190 lines** across 11 files
- Version drift risk eliminated for 30+ dependencies
- Zero production files over 800 LOC (from 2)
- Zero unused root-level re-exports
