# Songbird v0.2.1 — Wave 120: SB-03 Sled → NestGate Storage Migration

**Date**: April 7, 2026
**Primal**: songBird
**Previous**: Wave 119 (archived)
**Trigger**: primalSpring downstream audit — SB-03 sled overstep (storage belongs to NestGate)

---

## Summary

Resolved the SB-03 storage overstep: Songbird no longer needs to embed sled for persistence. New `NestGateStorage` and `NestGateOnionStorage` backends delegate to the `storage.*` capability provider (NestGate) via JSON-RPC at runtime. In-memory fallback when no provider is available. `sled-storage` feature deprecated in both affected crates.

## Audit Finding (primalSpring)

> SB-03: sled default-on in orchestrator/sovereign-onion. Feature-gated but default-enabled. Should migrate to NestGate storage API when available.

**Correction**: sled was already feature-gated and NOT default-enabled (non-default `sled-storage` feature). But the overstep principle is valid — storage belongs to NestGate per the Primal Responsibility Matrix.

## Changes

### New: NestGate Storage Backends

- **`songbird-orchestrator/src/storage_nestgate/`**: `NestGateStorage` implements both `ConsentStorageBackend` and `TaskStorageBackend` via `storage.*` JSON-RPC over Unix socket. Key namespacing: `songbird/consent/`, `songbird/task/`, `songbird/checkpoint/`.

- **`songbird-sovereign-onion/src/storage_nestgate.rs`**: `NestGateOnionStorage` implements `OnionStorageBackend` via direct JSON-RPC (avoids circular dependency with `songbird-universal-ipc`).

- **`songbird-universal-ipc`**: Added `TowerAtomicClient::connect_unix_path()` for direct socket connections.

### Capability Discovery Wiring

- `ConsentManager::with_storage()`: NestGate discovery first → sled (if feature) → in-memory
- `TaskLifecycleManager::new()`: same NestGate-first flow
- `OnionService::new_via_security_provider()`: NestGate first → sled/in-memory

### Deprecation

- `sled-storage` feature marked deprecated in both `Cargo.toml` files
- Doc comments on backend traits updated to point to NestGate as production path
- `REMAINING_WORK.md` SB-03 section updated from "Blocked" to "Resolved"

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,764 | 12,772 |
| sled dependency status | optional, non-default | deprecated, optional, non-default |
| NestGate storage backends | 0 | 2 (`NestGateStorage`, `NestGateOnionStorage`) |
| Storage overstep | present (sled embedded) | resolved (capability delegation) |

## Verification

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,772 passed, 0 failed
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok

## Remaining

- NestGate must expose live `storage.*` IPC endpoints for end-to-end validation
- Connection pooling for `NestGateStorage` (currently opens per-call)
- See `REMAINING_WORK.md` for full status
