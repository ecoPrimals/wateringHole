<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 50: Evolution Pass Handoff

**Date**: April 15, 2026
**Commit**: `d8a56cf83` (pre-push)

## Summary

Hardcoded ecosystem namespace evolved to capability-based discovery, 3 large production files smart-refactored, 3 orphaned files from prior refactoring passes wired into module tree, full codebase audit for unsafe code / production mocks / dead markers.

## Changes

### 1. Hardcoded Namespace → Configurable Discovery

| File | Change |
|------|--------|
| `beardog-tower-atomic/src/discovery.rs` | 4× hardcoded `"biomeos"` → `resolve_biomeos_ipc_subdir_from_optional()` from `beardog-types`. Added `ipc_namespace: Option<String>` to `DiscoverSocketEnv` (reads `BIOMEOS_IPC_NAMESPACE` env). |
| `beardog-core/src/socket_config.rs` | `.join("biomeos")` → `.join(BIOMEOS_RUNTIME_SOCKET_SUBDIR)` shared constant. |

### 2. Large File Smart Refactoring

| File | Before | After | Method |
|------|--------|-------|--------|
| `tunnel/hsm/types/android.rs` | 802 | 588 | Deduplicated 220 lines of transport traits/stubs; wired orphaned `android_transports.rs` as sibling module with `pub use` re-exports |
| `tunnel/hsm/providers/ios.rs` | 864 | 286 | Replaced 580 lines inline `mod tests` with `#[path = "ios_tests.rs"]` (external file was identical but orphaned) |
| `universal_hsm_discovery/discovery/mobile_discoverer.rs` | 806 | 471 | Extracted 5 repetitive capability builders (353 lines) to `mobile_hsm_capabilities.rs` with shared `no_api_support()` / `no_advanced_features()` / `no_human_entropy()` helpers |

### 3. Orphaned Files Wired

| File | Status |
|------|--------|
| `android_transports.rs` | Was dead (not in `mod.rs`); now `pub mod android_transports` in types |
| `ios_tests.rs` | Was dead (not referenced); now `#[path = "ios_tests.rs"]` from `ios.rs` |
| `mobile_hsm_capabilities.rs` | New extraction target; `pub mod mobile_hsm_capabilities` in discovery |

### 4. Codebase Audit Findings

| Category | Finding |
|----------|---------|
| `unsafe` blocks | 0 |
| Production mocks | 0 (all 287 mock/stub refs behind `#[cfg(test)]`) |
| TODO/FIXME/HACK markers | 0 |
| `.bak`/`.old`/`.tmp` debris | 0 |
| `serde_yaml` (deprecated) | Pure Rust via `unsafe-libyaml`; 4 files to migrate when fork stabilizes |
| `ring` (C/asm) | Only behind optional `dns-sd` feature; not in default build |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | Clean |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace` | 14,784 pass, 0 fail (1 pre-existing flaky: `key_export_roundtrip` HOME env race) |

## Net Impact

- **+540 / −920 lines** across 10 files (net −380)
- Zero production files over 800 LOC (from 3)
- Zero hardcoded ecosystem namespace strings in production discovery paths
- 3 orphaned files from prior refactoring passes now compiled

## Blocked Items (Cross-Primal)

| Item | Reason |
|------|--------|
| Bond persistence | Requires NestGate/loamSpine ledger coordination |
| HSM/Titan M2 `tee_*` path | Requires hardware access for Pixel cross-arch |
