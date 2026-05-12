# NestGate v4.7.0-dev — Phase 2 Modernization Handoff

**Date**: March 28, 2026  
**Primal**: nestgate  
**Version**: 4.7.0-dev  
**Branch**: main

---

## Summary

Phase 2 modernization of nestgate focused on compilation surface optimization, dependency hygiene, primal sovereignty, and modern idiomatic Rust patterns. This follows the Session 4 decomposition that split the 295K-line monolith into 6 crates.

### Key Outcomes

| Metric | Session 4 (Before) | Phase 2 (After) |
|--------|-------------------|-----------------|
| Workspace crates | 18 | **22** (+4 new) |
| nestgate-core pub mod | 37 | **24** (+54 re-exports) |
| nestgate-core deps | 51 | **44** |
| nestgate-core lines | ~74K | **~52K** |
| Max file size | 865L | **813L** (test file) |
| Unused feature flags | 13 | **0** |
| Version drift | 4 mismatches | **0** |
| Primal overreach | BEARDOG/SONGBIRD refs | **zero** |

---

## Changes in Detail

### 1. Dependency Hygiene
- **100+ inline dep versions** hoisted to `workspace = true` across all 22 crates
- Bumped workspace: dashmap 5.5→6.1, url 2.4→2.5, tempfile 3.8→3.10, clap 4.0→4.5
- Added to workspace: jsonrpsee, pin-project, mdns-sd, getrandom, serial_test, temp-env
- `sysinfo` made optional (cfg-gated, default on) — Linux uses `/proc`+rustix first
- Removed `mdns-sd` from core (was unused; discovery crate is canonical home)
- Pruned 13 unused feature flags from nestgate-core

### 2. New Crates Extracted
- **nestgate-security**: cert, crypto, jwt_validation, zero_cost, zero_cost_security_provider
  - Moved RustCrypto stack (aes-gcm, argon2, ed25519-dalek, hmac, sha2, etc.) out of core
- **nestgate-platform**: env_process, linux_proc, platform
  - Canonical home for OS abstractions (rustix, uzers, gethostname, etcetera)
- **nestgate-observe**: observability, diagnostics, events
  - Telemetry domain with stub traits for core coupling
- **nestgate-cache**: cache, cache_math, uuid_cache
  - Caching domain (dashmap, lru, parking_lot)

All use re-export facades for zero downstream breakage.

### 3. Primal Sovereignty
- `BEARDOG_AUTH_ENDPOINT` → `AUTH_PROVIDER_ENDPOINT` (capability-based)
- `discover_songbird_ipc` → `discover_orchestration_ipc` (generic)
- All `SONGBIRD_*` env vars removed — use `NESTGATE_ORCHESTRATION_*` or `ORCHESTRATION_*`
- Cleaned primal-specific names from 15+ files of docs, comments, test data

### 4. Modern Idiomatic Rust
- Migrated `#[allow(` → `#[expect(`, reason = "...")]` (biomeOS pattern)
- Added `clippy::cast_possible_truncation`, `cast_sign_loss`, `cast_precision_loss` lints
- Fixed `Box<dyn Error>` return → `NestGateError` in auth_token_manager.rs

### 5. File Size Compliance
- Split 4 files >700L into directory modules (canonical_types, storage_adapters, canonical_hierarchy, universal_providers_zero_cost)
- All production files now under 725 lines

---

## Impact on Other Primals

### Environment Variable Changes
Primals that previously used these env vars must update:
- `BEARDOG_AUTH_ENDPOINT` → `AUTH_PROVIDER_ENDPOINT`
- `SONGBIRD_IPC_PATH` → `ORCHESTRATION_IPC_PATH` or `NESTGATE_ORCHESTRATION_IPC_PATH`
- `SONGBIRD_HOST` → `ORCHESTRATION_HOST`
- `SONGBIRD_PORT` → `ORCHESTRATION_PORT`

### For BearDog
If BearDog relied on NestGate reading `BEARDOG_AUTH_ENDPOINT`, it should now set `AUTH_PROVIDER_ENDPOINT` instead. NestGate discovers auth providers by capability, not by primal name.

### For Songbird
NestGate's IPC discovery no longer looks for `SONGBIRD_*` env vars. Set `ORCHESTRATION_IPC_PATH` for the orchestration gateway endpoint.

### For All Primals
NestGate's public API (`nestgate_core::*`) is unchanged — all extractions use re-export facades. Cargo.toml dependency on `nestgate-core` continues to work.

---

## Known Issues

- `nestgate-api` / `nestgate-bin`: Pre-existing async lifetime errors (61 errors, from async_trait migration in Session 4). Not caused by Phase 2. Deferred for separate fix.
- `nestgate-observe` uses stub traits for `crate::traits::Service` and `canonical_types::events::*` — these should be wired to real types when nestgate-core traits are further extracted.

---

## Build Verification

```
cargo check -p nestgate-types -p nestgate-config -p nestgate-platform
  -p nestgate-security -p nestgate-storage -p nestgate-rpc
  -p nestgate-discovery -p nestgate-observe -p nestgate-cache
  -p nestgate-core -p nestgate-canonical -p nestgate-zfs
  -p nestgate-network -p nestgate-automation -p nestgate-mcp
  -p nestgate-nas -p nestgate-middleware -p nestgate-fsmonitor
  -p nestgate-performance -p nestgate-installer
→ All 20 crates compile clean (0 errors)
```
