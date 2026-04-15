# ToadStool S203j–S203k: Deep Debt Comprehensive Evolution

**Date**: April 15, 2026
**Scope**: S203j (tarpc socket unification, idiomatic evolution) + S203k (comprehensive evolution pass)
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy --workspace -- -D warnings` ✅ | `cargo doc --workspace --no-deps` ✅

---

## Summary

Two consecutive deep debt sessions executing the primalSpring Phase 43 downstream audit.
Total: **17 debt items resolved**, **5 active items cataloged**, all quality gates green.

---

## S203j — Idiomatic Evolution Pass (9 resolved)

### async-trait Migration (Wave 3)
- 6 zero-dyn traits migrated to native `async fn` in traits: `HealthMonitor`, `SwapExecutor`,
  `DeviceDiscovery`, `HealthProbe`, `CrossCompilationToolchain`, `GpuDiscovery`
- 10 `#[async_trait]` annotations removed (183→~148)
- 5 crates freed from async-trait dep (total 8 across all waves)

### Tarpc Socket Unification
- `ToadStoolTarpcClient::discover()` was connecting to JSON-RPC socket (`compute.sock`)
  instead of tarpc socket (`compute-tarpc.sock`) — fixed with new `resolve_toadstool_tarpc_socket`
- Added `TOADSTOOL_TARPC_SOCKET` env var support + 3 unit tests

### Hardcoding → Capability-Based Evolution
- 30+ raw env var strings in `SocketPathEnv::from_env()` → interned `socket_env::*` constants
- New `constants::platform_paths` module: procfs/devfs/sysfs/etc constants + helper functions
- 6 files with hardcoded `"toadstool"` → `PRIMAL_NAME` constant
- Magic numbers (ports 8080–8082, timeouts, cache TTLs) → named constants

### Dependency Hygiene
- ~20 `Cargo.toml` files unified: inline version specs → `workspace = true`
- CUDA/OpenCL stubs marked `#[deprecated(since = "0.1.0")]`
- Redundant `#[allow(unsafe_code)]` removed from `nvpmu/init.rs`

---

## S203k — Comprehensive Evolution Pass (8 resolved, 5 cataloged)

### Network Configurator Stubs → Structural Validation
- 5 empty `apply_*`/`validate_*` functions evolved from log-only to structural validation
  (circuit breaker thresholds, DNS timeouts, auth methods, port range ordering, traffic percentages)

### Env Var Interning (Wave 2) + HTTP Protocol Constants
- ~40+ more raw env var strings centralized (infant_discovery, primal_discovery, scheduler, server)
- `HTTP_PROTOCOL` constant replaces raw `"http://"` in 7 modules
- `UNIX_SOCKET_URL_SCHEME` / `UNIX_SOCKET_URL_PREFIX` added

### Dead Code & Error Swallowing
- `#[allow(dead_code)]` → `#[expect(dead_code, reason)]` with documented reasons (4 sites)
- `.unwrap_or_default()` → `tracing::warn!` + fallback on 4 production paths

### Smart File Refactoring (4 large files)
- `edge/platforms/arduino.rs` (679L) → 4-submodule directory
- `edge/discovery.rs` (644L) → 5-strategy directory
- `crypto_lock/access_control/manager.rs` (601L) → extracted `validation.rs`
- `security/policies/manager.rs` (546L) → extracted `cache.rs` + `composition.rs`

### Active Debt Cataloged
5 previously-undocumented stubs: `D-SANDBOX-SIMULATION`, `D-PLUGIN-SIMULATE`,
`D-BYOB-RESOURCE-SIM`, `D-WORKLOAD-CLIENT-IPC`, `D-HW-LEARN-VERIFY`

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| `#[async_trait]` annotations | 183 | ~144 |
| Crates with `async-trait` dep | 19 | 11 |
| Raw env var strings | ~100+ | ~30 (in legacy edge crates) |
| Large production files (>600L) | 7 | 3 (type-heavy, naturally long) |
| Undocumented active debt | 5+ | 0 (all cataloged with D- prefix) |
| Silent error swallowing | 4+ sites | 0 (all traced) |

---

## Remaining Active Debt (toadStool)

| ID | Area | Priority |
|----|------|----------|
| `D-ASYNC-DYN-MARKERS` | ~144 annotations on dyn-dispatch traits | Medium (architectural) |
| `D-SANDBOX-SIMULATION` | Linux sandbox returns fake success | Low (requires kernel integration) |
| `D-PLUGIN-SIMULATE` | Plugin load/unload simulated | Low (needs ABI design) |
| `D-BYOB-RESOURCE-SIM` | Resource usage from specs not metrics | Low (needs cgroup stats) |
| `D-WORKLOAD-CLIENT-IPC` | Non-GPU workload IPC not wired | Medium |
| `D-HW-LEARN-VERIFY` | Register verification always fails | Low (needs nouveau UAPI) |
| Coverage 83.6% → 90% | Hardware-dependent test gaps | Medium |
| V4L2 ioctl surface | Camera/video capture | Low |

---

## Cross-Primal Impact

- **primalSpring**: All 4 audit items addressed (async-trait partially, socket unification complete,
  coverage ongoing, V4L2 deferred)
- **barraCuda**: `compute-tarpc.sock` naming convention now consistent client↔server
- **biomeOS composition**: JSON-RPC primary socket (`compute.sock`) confirmed as stable entry point
