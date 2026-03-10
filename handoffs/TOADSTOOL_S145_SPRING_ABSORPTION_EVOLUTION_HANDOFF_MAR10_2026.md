# ToadStool S145 — Spring Absorption & Evolution Execution Handoff

**Date**: March 10, 2026
**Session**: S145
**Author**: toadStool team
**Status**: All quality gates passing. 19,965 tests (0 failures, 101 skipped). Clippy pedantic clean. ~86% line coverage.

---

## Summary

S145 executed on all identified spring absorption items from the cross-spring review
(hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, healthSpring). Deep debt
evolution principles applied: modern idiomatic Rust, capability-based discovery, safe code,
no production mocks, no hardcoding.

---

## Absorptions Completed

### PrecisionBrain (from hotSpring v0.6.25)

**File**: `crates/runtime/universal/src/backends/nvvm_safety.rs`

- `PrecisionHint` enum: Critical, Moderate, ThroughputBound, LowPrecision
- `PrecisionBrain` struct with cached O(1) route table built from `HardwareCalibration`
- F64 throttle detection: when dispatch latency ratio > 8x, throughput workloads prefer DF64
- `dispatch_latency_ratio` field added to `TierCapability` for runtime calibration
- 8 new tests covering all routing paths

**Integration**: Springs call `PrecisionBrain::new(calibration, None)` after device init,
then `brain.route(PrecisionHint::Critical)` for O(1) tier selection.

### NvkZeroGuard (from airSpring v0.7.5)

**File**: `crates/runtime/universal/src/backends/nvvm_safety.rs`

- `ZeroGuardVerdict` enum: Valid, AllZeros, NanContaminated
- `nvk_zero_guard_check(&[f64])` — detects NVK Volta zero-output bug
- `nvk_zero_guard_check_f32(&[f32])` — f32 variant
- 8 new tests

**Integration**: After GPU shader dispatch, call `nvk_zero_guard_check(&output_buffer)`.
If `AllZeros`, fall back to CPU or DF64 path.

### 8 New WorkloadPatterns (neuralSpring S140 + healthSpring V14.1)

**File**: `crates/runtime/orchestration/src/workload_routing.rs`

| Pattern | Crossover N | Source |
|---------|-------------|--------|
| Pairwise | 500,000 | neuralSpring S140 pairwise_substrate bench |
| BatchFitness | 50,000 | neuralSpring S140 batch_fitness_substrate bench |
| HmmBatch | 5,000 | neuralSpring S140 hmm_substrate bench |
| SpatialPayoff | 4,000 | neuralSpring S140 spatial_substrate bench |
| Stochastic | 100,000 | neuralSpring S140 stochastic_substrate bench |
| PopulationPk | 100 | healthSpring V14.1 metalForge parallel_gpu_min |
| DoseResponse | 1,000 | healthSpring V14.1 metalForge sweep_gpu_min |
| DiversityIndex | 500 | healthSpring V14.1 metalForge reduce_gpu_min |

9 new routing tests + 1 completeness test.

### 5 New Capability Domains (ISSUE-001)

**File**: `crates/core/common/src/interned_strings.rs`

- `capabilities::BIOLOGY` — wetSpring (metagenomics, phylogenetics, mass spec)
- `capabilities::HEALTH` — healthSpring (PK/PD, NLME, biosignal)
- `capabilities::MEASUREMENT` — groundSpring (UQ, validation)
- `capabilities::OPTIMIZATION` — neuralSpring (ML, evolutionary computation)
- `capabilities::VISUALIZATION` — petalTongue (streaming pipeline)

### capability.call Format Standardization (ISSUE-003)

**File**: `crates/server/src/pure_jsonrpc/handler/science_domains.rs`

`deploy_capability_call` now supports two formats:
- Format A (flat): `{ "capability": "biology", "method": "phylo.infer", "params": {...} }`
- Format B (semantic): `{ "qualified_method": "biology.phylo.infer", "params": {...} }`

### Spring-as-Provider ProviderRegistry (ISSUE-007)

**File**: `crates/distributed/src/primal_capabilities/registry.rs`

- `ProviderRegistration` struct: capability, socket_path, methods, provider_name, version
- `ProviderRegistry`: register, deregister, resolve_socket (with filesystem fallback), prune_stale
- 8 new tests covering registration lifecycle and serde

### Hardcoding Evolution

- `ServerConfig::default()` port: bare `8080` → `toadstool_config::ports::get_port_with_env()`
- All other production `http://localhost:8080` references confirmed test-only

---

## Audit Findings

| Category | Finding |
|----------|---------|
| Production mocks | Zero — all mocks `#[cfg(test)]` or `test-mocks` feature |
| Unsafe code | Limited to GPU FFI + secure enclave; 36 crates have `#![deny(unsafe_code)]` |
| Files >1000 LOC | Zero — largest is ~981 lines |
| TODO/FIXME/HACK/XXX in code | Zero |
| External C FFI | Zero (ecoBin v3.0 compliant) |
| Hardcoded ports in production | Zero — all centralized via `toadstool_config::ports` |

---

## Spring Pin Status (S145)

| Spring | Pin |
|--------|-----|
| hotSpring | v0.6.25 → S145 |
| groundSpring | V100 → S145 |
| neuralSpring | V91/S140 → S145 |
| wetSpring | V99+ → S145 |
| airSpring | v0.7.5 → S145 |
| healthSpring | V14.1 → S145 |

---

## Action Items for Other Primals

### barraCuda
- Absorb `PrecisionBrain` for shader dispatch tier selection
- Absorb `NvkZeroGuard` for post-dispatch validation
- Wire new WorkloadPatterns into metalForge dispatch decisions

### Springs
- Register with toadStool using `ProviderRegistry` pattern (JSON-RPC `provider.register_capability`)
- Use `qualified_method` format B for capability calls
- Update spring pins to S145

### coralReef
- Test sovereign WGSL→native path as NVVM bypass (from hotSpring v0.6.25 handoff)
- Multi-device compile for topology-aware placement

---

## Files Changed

| File | Change |
|------|--------|
| `crates/runtime/universal/src/backends/nvvm_safety.rs` | +PrecisionBrain, +NvkZeroGuard, +TierCapability.dispatch_latency_ratio |
| `crates/runtime/universal/src/backends/mod.rs` | Export new types |
| `crates/runtime/orchestration/src/workload_routing.rs` | +8 WorkloadPattern variants, +8 thresholds, +10 tests |
| `crates/core/common/src/interned_strings.rs` | +5 capability domains |
| `crates/server/src/pure_jsonrpc/handler/science_domains.rs` | Format B qualified_method support |
| `crates/distributed/src/primal_capabilities/registry.rs` | +ProviderRegistry, +ProviderRegistration |
| `crates/distributed/src/primal_capabilities/mod.rs` | Export new types |
| `crates/server/src/config/mod.rs` | Port hardcoding → centralized config |
| `EVOLUTION_TRACKER.md` | S145 + S144 entries |
| `README.md` | Updated to S145 |
| `DEBT.md` | Coverage updated |
| `NEXT_STEPS.md` | Updated to S145 |
| `SPRING_ABSORPTION_TRACKER.md` | Updated to S145, spring pins refreshed |
