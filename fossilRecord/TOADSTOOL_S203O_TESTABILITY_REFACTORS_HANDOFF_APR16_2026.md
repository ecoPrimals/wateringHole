# ToadStool S203o: Testability Refactors + Stub Evolution Wave 2

**Date**: April 16, 2026
**Scope**: Separate I/O from logic, evolve monitoring/storage stubs, centralize constants wave 4
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy --workspace -- -D warnings` ✅

---

## Summary

Addresses the "mixing UI render and logic" anti-pattern across 5 major modules.
Functions that interleaved filesystem reads with computation have been split into
thin I/O wrappers + pure testable parsers. Monitoring stubs evolved to real host
queries. Storage fake-success eliminated.

---

## 1. Testability Refactors (I/O ↔ Logic Separation)

| Module | Pure Functions Extracted | Tests |
|--------|------------------------|-------|
| `layer_adaptation/detection.rs` | `parse_meminfo_kb`, `estimate_storage_bandwidth`, `parse_net_speed_mbps`, `mbps_to_bytes_per_sec` | 13 |
| `capabilities/gpu.rs` | `parse_nvidia_information`, `parse_drm_uevent`, `infer_gpu_model_from_ids` | 10 |
| `configurator/defaults.rs` | `parse_resolv_conf` | 4 |
| `hardware/storage.rs` | `parse_df_available`, `classify_rotational` | 8 |
| `os_layer/compat/linux.rs` | `parse_kernel_version` | 3 |

**Pattern**: Every function that previously read a file AND parsed it AND made decisions
now has the parsing in a pure `fn` that takes `&str` and returns structured data. Tests
feed fixture strings. I/O stays in thin async shells.

## 2. Monitoring Evolution

**Before**: `get_system_resources` returned hardcoded 10 GiB storage, 0% CPU, 0 GPU units.
`start_monitoring` was a no-op.

**After**:
- CPU: `toadstool_sysmon::cpu_usage()` → `load_average()` → `memory_usage_percent()` fallback chain
- Memory: `toadstool_sysmon::memory_info()` → `/proc` fallback
- Storage: `disk_usage()` for root FS → `rustix::fs::statvfs("/")` fallback
- GPU: stays 0 with `tracing::debug!` (discovery-dependent)
- `start_monitoring`: real workload ID registration in `HashSet`

## 3. Storage Status Fix

`StorageClient::store_artifact` RPC failure path now returns `StorageStatus::LocalOnly`
(new variant) instead of `StorageStatus::Success`. Callers can distinguish between
remotely-persisted and local-only artifacts.

## 4. Constants Wave 4

**New sysfs**: `CLASS_DRM`, `CLASS_AKIDA`, `CLASS_GPIO`, `FS_SELINUX_ENFORCE`
**New env**: `TOADSTOOL_PORT`, `REQUEST_TIMEOUT`, `DNS_RESOLVERS`, `BASE_DOMAIN`,
`ENV`, `DEBUG`, `LOG_LEVEL`, `DATA_DIR`, `CACHE_DIR`, `ENABLE_PRIMAL_CAPABILITIES`,
`PRIMAL_HEARTBEAT_INTERVAL`

5 files updated for sysfs, 5 files updated for env vars.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Mixed I/O+logic functions | ~17 identified | 5 refactored (highest impact) |
| Pure testable parsers | 0 | 12 new |
| Tests for pure parsers | 0 | +38 |
| Monitoring: real host data | No (hardcoded) | Yes (sysmon + statvfs) |
| Storage fake success | Yes | No (LocalOnly variant) |
| Raw sysfs paths centralized | +4 constants | +4 call sites |
| Raw env vars centralized | +11 constants | +5 call sites |

---

## Remaining Testability Targets

These modules still mix I/O and logic (from the audit):
- `server/src/pure_jsonrpc/handler/dispatch/submit.rs` — JSON param parsing + coral client I/O
- `cli/src/zero_config/discovery.rs` — subprocess + meminfo parsing + socket probing
- `auto_config/src/ecosystem/discoverer.rs` — env branching + HTTP probing
- `server/src/tarpc_server/executor.rs` — CPU sampling + workload processing
- `server/src/cross_gate/dispatcher.rs` — JSON-RPC request/response + TCP I/O
