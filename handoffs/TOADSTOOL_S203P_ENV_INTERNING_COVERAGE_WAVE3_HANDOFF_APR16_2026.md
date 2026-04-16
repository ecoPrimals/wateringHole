# ToadStool S203p: Env Interning Complete + Coverage Wave 3

**Date**: April 16, 2026
**Scope**: Complete env var string interning, coverage for pure-logic modules
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy --workspace -- -D warnings` ✅

---

## Summary

Completes the env var interning initiative: all `TOADSTOOL_*` environment variable
string literals across the config subsystem now use centralized `socket_env::*`
constants. Plus +21 tests for 6 previously-untested pure-logic production modules.

---

## 1. Env Interning Complete

~55 new `socket_env` constants added across categories:

| Category | Count | Examples |
|----------|-------|---------|
| Resource limits | 4 | `MAX_CPU`, `MAX_MEMORY`, `EXECUTION_TIMEOUT` |
| Logging | 10 | `LOG_TO_FILE`, `LOG_FORMAT`, `LOG_ROTATION`, `LOG_MAX_SIZE` |
| Runtime (container/wasm/python) | 10 | `CONTAINER_RUNTIME`, `WASM_ENGINE`, `PYTHON_EXECUTABLE` |
| Security | 13 | `JWT_SECRET`, `ENCRYPTION_ALGORITHM`, `SANDBOX_TYPE` |
| Feature flags | 14 | `ENABLE_METRICS`, `ENABLE_FEDERATION`, `ENABLE_GRPC` |
| App config | 2 | `VERBOSE`, `WORKER_THREADS` |

6 env_overrides files fully converted. No raw `TOADSTOOL_*` strings remain in
the env_overrides subsystem.

## 2. Coverage Wave 3 (+21 tests)

| Module | Tests | What's Covered |
|--------|-------|----------------|
| `platform_paths/paths.rs` | 3 | XDG resolution, HOME fallback, temp-only fallback |
| `semantic_methods/mappings_core.rs` | 3 | Registration, lookup miss, duplicate handling |
| `resource_optimizer/cost.rs` | 5 | Benefit ranking, duration cap, resource savings |
| `resource_optimizer/allocation.rs` | 3 | Bottleneck detection, diamond parallelization, empty graph |
| `resource_estimator/estimator.rs` | 4 | Linear chain, diamond DAG, cycle detection, single node |
| `workload_routing/defaults.rs` | 3 | Crossover thresholds, pattern matching, WorkloadRouter default |

---

## Metrics

| Metric | Before S203p | After S203p |
|--------|-------------|-------------|
| Raw env var strings in env_overrides | ~55 | 0 |
| socket_env constants | ~30 | ~85 |
| New tests | 0 | +21 |
| Untested pure-logic modules | ~10 | ~4 remaining |

---

## Remaining

- CLI defaults.rs still has ~12 raw strings for non-TOADSTOOL names
  (Jaeger, Prometheus, CA/cert paths, sidecar image)
- ~5 untestable modules remain (heavy I/O: TCP/Unix connections, platform monitoring)
- Coverage target 83.6% → 90% (hardware-dependent gaps remain)
