# NestGate v4.7.0-dev — Ring Elimination, Capability Symlink, Smart Refactoring & Doc Cleanup

**Date**: March 31, 2026  
**Primal**: nestgate (storage & permanence)  
**Session type**: Deep debt execution — ring elimination, filesystem-backed IPC, capability symlink, smart refactoring, doc modernization  
**Supersedes**: NESTGATE_V470_ANCESTRAL_OVERSTEP_DEEP_DEBT_EVOLUTION_HANDOFF_MAR31_2026.md (corrects ring/test-count/workspace inaccuracies)

---

## What Was Done

### CRITICAL: ring/rustls/reqwest Eliminated from Dependency Tree

The `nestgate-installer` crate pulled `reqwest` → `rustls` → `ring` (C/ASM crypto), violating ecoBin. BearDog solved the same issue for songBird's TLS protocol using pure-Rust crypto primitives. Since the installer runs before the ecosystem is available, it cannot delegate TLS to bearDog IPC.

**Solution**: Replaced `reqwest` + `rustls` with `std::process::Command` calling the system `curl` binary. The OS handles TLS. This eliminates ring, rustls, reqwest, hyper-rustls, and all transitive C/ASM dependencies.

- `nestgate-installer/src/download.rs`: Rewritten with `curl_json()` and `curl_download()` helpers
- `nestgate-installer/Cargo.toml`: `reqwest` and `rustls` deps removed
- `Cargo.lock`: Verified ring/rustls/reqwest/hyper-rustls all absent
- `println!` → `tracing::info!` for installation progress

### NG-01 Resolved: Filesystem-Backed IPC Storage

`unix_adapter.rs` used an in-memory `HashMap` for storage — data lost on restart. Now backed by filesystem under `get_storage_base_path()/datasets/`.

- Path-traversal sanitization on all key inputs
- New routes: `data.store`, `data.retrieve`, `nat.store_traversal_info`, `nat.retrieve_traversal_info`, `beacon.store/retrieve/list/delete`
- Health: `health.liveness`, `health.readiness` (checks storage backend availability)
- `capabilities.list` returns full method inventory with version

### storage.sock Capability Symlink

Per `CAPABILITY_BASED_DISCOVERY_STANDARD`, other primals discover NestGate's storage by looking for `storage.sock` in `$XDG_RUNTIME_DIR`.

- `install_storage_capability_symlink()`: Creates `storage.sock` → `nestgate.sock` symlink
- `remove_storage_capability_symlink()`: Cleanup on shutdown
- `StorageCapabilitySymlinkGuard`: RAII guard pattern — symlink removed on drop
- Integrated into Unix socket server bind and isomorphic IPC server startup

### Smart Refactoring (3 large files decomposed)

| File | Before | After |
|------|--------|-------|
| `health.rs` | 785L monolith | `health/` package: mod.rs + types.rs + reporting.rs + monitoring.rs + tests.rs |
| `cache/types.rs` | 858L monolith | `cache/types/` package: mod.rs + tier.rs + policy.rs + stats.rs + entry.rs + tests.rs |
| `pool/manager.rs` | 832L monolith | `pool/` package: manager.rs + discovery.rs + status.rs + operations.rs |

### Capability-Based Naming Evolution

- `BearDogClient` → `SecurityProviderClient` (with `#[deprecated]` alias for compat)
- `BearDogRequest/Response` → `SecurityProviderRequest/Response`
- `NESTGATE_BEARDOG_URL` → `NESTGATE_CAPABILITY_SECURITY_ENDPOINT` (legacy as fallback with `tracing::warn!`)
- All doc comments updated to refer to "security capability provider"

### Production Stub Evolution

| Stub | Before | After |
|------|--------|-------|
| `validate_certificate` | Silent `Ok(true)` | `Err(not_implemented)` — delegation to security provider |
| `generate_self_signed` | Static PEM string | `Err(not_implemented)` — delegation to security provider |
| `get_recommendations` | `Ok(vec![])` | `Err(not_implemented)` with actionable message |
| `migrate_dataset_to_tier` | `Ok(())` no-op | `Err(not_implemented)` — callers log warn and continue |
| `ServiceAction::Logs` | `println!` | `Err(not_implemented)` pointing to `journalctl` |

### Hardcoding Elimination

- Port fallbacks 8084/9091 → `runtime_fallback_ports::HTTP` / `runtime_fallback_ports::METRICS`
- K8s API URL `127.0.0.1:8001` → required `KUBERNETES_SERVICE_HOST` env var
- Cache paths `/tmp/nestgate_hot_cache` → `resolve_cache_base()` (XDG/env/tmp fallback)
- `jwt_rustcrypto.rs` renamed to `jwt_claims.rs` (honest about content)

### Ancestral Overstep Shed

| Area | Action |
|------|--------|
| Crypto (nestgate-security) | Cert validation/generation return not_implemented; delegate to bearDog |
| Discovery (nestgate-discovery) | mDNS behind `mdns` feature gate; production via biomeOS/songBird |
| AI/MCP (nestgate-mcp) | Directory removed entirely |
| Network (nestgate-network) | Removed as dependency from nestgate-api, nestgate-bin, nestgate-nas |

### Dead Code & Quality

- Module-level `#![allow(dead_code)]` removed from 4 crates; narrowed to item-level with `reason = "..."` 
- Only 1 production module-level `#![allow(dead_code)]` remaining: `rest/rpc/manager.rs` (structural placeholder, documented)
- `#![forbid(unsafe_code)]` added to nestgate-observe and nestgate-env-process-shim (now all 22 crates)
- CPU metrics tests fixed for multi-core systems

### Doc Cleanup

- README.md, STATUS.md, CHANGELOG.md, START_HERE.md, QUICK_REFERENCE.md, DOCUMENTATION_INDEX.md all updated
- Corrected: test counts (8,376), workspace members (24), ring narrative (eliminated, not provider), file size limits, removed nestgate-mcp references, updated compliance tables

---

## Current Measured State

```
Build:       24/24 workspace members, 0 errors
Clippy:      ZERO warnings (cargo clippy --workspace --all-features --all-targets)
Format:      CLEAN (cargo fmt --check)
Tests:       8,376 lib tests passing, 0 failures
Docs:        ZERO warnings (cargo doc --workspace --no-deps)
Coverage:    80.95% line (llvm-cov) — not re-measured this session
Max file:    879 lines (metrics.rs)
TLS/crypto:  Delegated to bearDog IPC; installer uses system curl
             ring/rustls/reqwest: NOT in Cargo.lock
Discovery:   Env vars + songBird IPC (mDNS feature-gated)
MCP:         Removed from workspace (delegated to biomeOS capability.call)
IPC routes:  storage.*, data.*, nat.*, beacon.*, health.*, capabilities.* all wired
Symlink:     storage.sock → nestgate.sock (auto-managed lifecycle)
```

---

## External Dependency Audit

| Dependency | Type | Status |
|------------|------|--------|
| `ring` | C/asm crypto | **ELIMINATED** — installer uses system curl |
| `rustls` / `reqwest` | HTTP+TLS | **ELIMINATED** — installer uses system curl |
| `aws-lc-rs` / `openssl` / `native-tls` | — | NOT in dependency tree |
| `inotify-sys` | Linux FFI (via notify) | Required for filesystem monitoring |
| `libc` | System FFI (via tokio, uzers) | Unavoidable for system programming |
| `-sys` crates | — | Only `linux-raw-sys` (rustix ABI defs) + `inotify-sys` |

---

## Remaining Debt (Prioritized)

| Priority | Item | Status |
|----------|------|--------|
| P1 | Coverage to 90% (~9pp gap) | 80.95% — multi-session effort |
| P2 | Profile `.clone()` hotspots in RPC layer | Needs benchmark data |
| P3 | Multi-filesystem substrate testing (ZFS, btrfs, xfs, ext4) | Infra-dependent |
| P3 | Cross-gate replication (multi-node data orchestration) | Design phase |

---

## Corrections to Previous Handoff

The earlier Mar 31 handoff (`NESTGATE_V470_ANCESTRAL_OVERSTEP_*`) contained inaccuracies:
- Stated "ring provider" for TLS — ring is now **eliminated**
- Stated 25/25 workspace members — correct count is **24**
- Stated 8,384 tests — correct count is **8,376**
- Stated `data.*`/`nat.*` routes "pending" — they are now **wired**

---

## Artifacts

- **Handoff**: This file
- **README**: `primals/nestgate/README.md` (updated)
- **Status**: `primals/nestgate/STATUS.md` (updated)
- **Changelog**: `primals/nestgate/CHANGELOG.md` (Session 12 entry added)
- **Coverage**: `cargo llvm-cov --workspace --lib --summary-only`
- **Fossil record**: `wateringHole/fossilRecord/nestgate/`
