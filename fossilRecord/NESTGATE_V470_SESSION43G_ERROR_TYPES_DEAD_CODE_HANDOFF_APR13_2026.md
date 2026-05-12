# NestGate v4.7.0-dev — Session 43g Handoff

**Date**: April 13, 2026  
**Primal**: NestGate (storage)  
**Session**: 43g — Error types & dead code evolution  
**Status**: GREEN — all checks pass  

---

## Changes

### Box<dyn Error> evolved to typed errors
5 production function signatures replaced `Box<dyn std::error::Error>` with `NestGateError` / `Result<T>`:
- `WebSocketManager::broadcast_event` (nestgate-api/rest/websocket.rs)
- `collect_real_storage_pools` (nestgate-api/handlers/storage/probes.rs)
- `get_directory_usage` (nestgate-api/handlers/storage/probes.rs)
- `collect_real_zfs_snapshots` (nestgate-api/handlers/storage/probes.rs)
- `create_storage_backend` (nestgate-api/rest/handlers/zfs/helpers.rs)
- `calculate_real_zfs_cache_hit_ratio` (nestgate-api/rest/handlers/monitoring/prometheus.rs)
- Config error `source: Box<dyn Error + Send + Sync>` retained (standard thiserror pattern).

### Zero-caller deprecated constants deleted (46 lines)
- `ports.rs`: PROMETHEUS, METRICS_PROMETHEUS, HEALTH_DEFAULT, METRICS_ALT, STORAGE_DISCOVERY_DEFAULT
- `runtime_fallback_ports.rs`: ORCHESTRATOR
- Deprecated count: 210 → 193

### Root documentation corrected
- README.md: deprecated count 202→193, test count 11,794→11,805, file size 500→750, clippy command aligned, duplicate dead-code bullet consolidated, dates updated
- STATUS.md: verification dates updated to 2026-04-13, session tag updated
- CONTEXT.md: edition field clarified (2021 shim noted), clippy command aligned

### Debris cleaned
- Empty directories removed: `nestgate-zfs/data/`, `nestgate-zfs/config/`

### Audits completed (no action required)
- **Dependency audit**: `inotify-sys`, `linux-raw-sys` confirmed transitive (rustix/notify); `libfuzzer-sys` fuzz-only. Zero C-FFI in production.
- **`#[async_trait]` audit**: Zero live usage — already on native async fn in traits.
- **TODO/FIXME scan**: Zero markers in production code.
- **Archive/backup scan**: Zero stale files (.bak, .old, .orig, .swp).
- **Build artifacts outside target/**: None.

---

## Verification

```
Build:    cargo check --workspace --all-features --all-targets — PASS
Clippy:   cargo clippy --workspace --all-targets --all-features -- -D warnings — PASS
Format:   cargo fmt --all --check — PASS
Docs:     cargo doc --workspace --no-deps — PASS (zero warnings)
Tests:    11,805 passing, 0 failures, 451 ignored
Coverage: ~81.7% line (llvm-cov)
```

---

## Remaining work (tracked, not blocking)

| Item | Priority | Notes |
|------|----------|-------|
| Coverage → 90% | P2 | Currently 81.7%; wateringHole 80% met |
| 193 deprecated APIs | P2 | Canonical config migration; all callers use `#[expect(deprecated)]` |
| `linux-raw-sys` dual versions | P3 | rustix 0.38 vs 1.x; align when tempfile upgrades |
| BTSP Phase 3 (key exchange) | P3 | Depends on BearDog crypto capability maturity |

---

## Ecosystem status

- **NestGate → primalSpring**: No blockers. NG-08 (ring elimination) confirmed RESOLVED.
- **NestGate → BearDog**: Crypto delegation operational; BTSP Phase 2 handshake wired.
- **NestGate → biomeOS**: capability IPC functional; no outstanding issues.
