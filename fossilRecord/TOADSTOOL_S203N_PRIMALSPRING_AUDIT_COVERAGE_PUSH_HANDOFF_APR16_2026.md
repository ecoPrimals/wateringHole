# ToadStool S203n: primalSpring Audit Closure + Coverage Push

**Date**: April 16, 2026
**Scope**: Close primalSpring April 16 audit items (async-trait closure + coverage push)
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy --workspace -- -D warnings` ✅

---

## Summary

Addresses both remaining primalSpring April 16 audit items for toadStool:
1. `async-trait` dyn-ceiling formally closed
2. +129 tests across 15 previously-untested production modules

---

## 1. D-ASYNC-DYN-MARKERS — CLOSED

**Status**: Formally closed in DEBT.md as "dyn-ceiling reached, S203n".

All 158 remaining `#[async_trait]` annotations (113 production, 45 test) are on 32
genuinely `dyn`-dispatched traits with `NOTE(async-dyn)` markers. No further migration
planned. Further reduction would require trait splitting or enum dispatch — architectural
changes outside debt cleanup scope.

Closed per primalSpring April 16 downstream audit directive.

## 2. Coverage Push: +129 Tests

| Area | Module | Tests | What's Covered |
|------|--------|-------|----------------|
| **server** | `shader_dispatch.rs` | ~15 | Param parsing (base64/array), invalid params, VFIO path without shader client |
| **server** | `system_query.rs` | ~12 | Network bandwidth estimation, vendor mapping, threshold logic |
| **server** | `cross_gate/router.rs` | ~10 | Gate selection (VRAM, queue depth, model loaded), gate removal, remote check |
| **distributed** | `coordination/discovery/core.rs` | ~12 | Node registration validation, network capacity, optimal distribution |
| **distributed** | `coordination/discovery/registry.rs` | ~10 | Insert/update/remove, health staleness, node type filtering |
| **distributed** | `coordination/discovery/client.rs` | ~10 | Node data parsing, legacy type mapping, missing fields |
| **distributed** | `crypto_lock/validators.rs` | ~10 | Signature validation, delegation chain depth, revocation list |
| **CLI** | `configurator/security.rs` | ~12 | Security config validation (auth, PKI, isolation, audit) |
| **CLI** | `configurator/reliability.rs` | ~12 | Circuit breaker thresholds, health monitoring config |
| **CLI** | `configurator/traffic.rs` | ~10 | Canary/mirroring/splitting validation, load balancer algorithms |
| **integration** | `primals/manager.rs` | ~6 | Config defaults, startup order (with cycles), registration lifecycle |
| **integration** | `storage/artifacts.rs` | ~4 | Store/retrieve with unavailable RPC, error mapping |
| **WASM** | `component_model/registry.rs` | ~8 | Interface registration, instance creation/limits, stats |
| **WASM** | `component_model/core.rs` | ~8 | Config defaults, ComponentValue type matching, JSON round-trip |

All tests are inline `#[cfg(test)] mod tests` — no new files created.

---

## Metrics

| Metric | Before S203n | After S203n |
|--------|-------------|-------------|
| D-ASYNC-DYN-MARKERS | "Dyn-ceiling reached" | **CLOSED** |
| New tests | 0 | +129 |
| Untested production modules | ~18 high-impact | ~3 remaining (hardware-dependent) |
| Total workspace tests | 21,600+ | 21,700+ |

---

## Remaining Coverage Gaps

These modules remain undertested but are hardware-dependent or require live services:
- GPU execution paths (`runtime/gpu/src/engine/`) — requires GPU hardware
- V4L2 camera capture (`runtime/display/src/v4l2/`) — requires camera
- VFIO passthrough (`core/hw-safe/src/vfio_*`) — requires IOMMU-enabled hardware
- Container metrics (`runtime/container/src/engine.rs` `get_metrics()`) — needs cgroup/Docker
