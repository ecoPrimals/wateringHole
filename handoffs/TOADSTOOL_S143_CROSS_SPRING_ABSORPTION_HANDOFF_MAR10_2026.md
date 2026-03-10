# toadStool S143 — Cross-Spring Absorption Handoff

**Date**: March 10, 2026
**From**: toadStool S143
**To**: barraCuda, hotSpring, all springs
**License**: AGPL-3.0-only
**Covers**: S142 → S143 — Cross-spring absorption sprint: NVVM poisoning defense, workload routing, brain interrupt pattern, deep debt elimination

---

## Executive Summary

toadStool S143 absorbed critical findings from all six springs and the wateringHole:

1. **NVVM device poisoning defense** (from hotSpring v0.6.25) — `HardwareCalibration` with driver-aware precision tier safety, `DeviceHealthStatus`, and `best_tier()` routing
2. **Workload size routing thresholds** (from healthSpring V14.1 / neuralSpring S139 / hotSpring v0.6.25) — `WorkloadRouter` with 10 GPU crossover thresholds validated by Kokkos parity benchmarks
3. **Brain interrupt pattern** (from hotSpring biomeGate Brain Architecture) — `AttentionState` escalation/de-escalation, `WorkloadAnomaly` detection, `InterruptAction` corrective responses
4. **Deep debt elimination** — hardcoded primal names, 4 GiB memory assumption, `/etc` paths, `/run/user/1000`, pre-existing test failure

---

## Part 1: NVVM Poisoning Defense

### New module: `crates/runtime/universal/src/backends/nvvm_safety.rs`

Absorbed from hotSpring v0.6.25 `hardware_calibration.rs` + `precision_brain.rs`.

| Type | Purpose |
|------|---------|
| `NvvmPoisoningRisk` | None / TranscendentalOnly / Unknown |
| `PrecisionTier` | F32 / F64 / F64Precise / Df64 |
| `TierCapability` | Per-tier compile/dispatch/transcendental safety |
| `HardwareCalibration` | Driver-aware calibration from `GpuAdapterInfo` |
| `DeviceHealthStatus` | Healthy / PoisonSuspected / Poisoned |

### Driver Classification

| Driver | Poisoning Risk | Transcendentals |
|--------|:---:|:---:|
| NVK (Mesa) | None | Safe at all tiers |
| AMD (radv) | None | Safe at all tiers |
| NVIDIA proprietary | TranscendentalOnly | Unsafe at F64Precise + DF64 |
| Unknown | Unknown | Assumed unsafe |

### Usage

```rust
use toadstool_runtime_universal::backends::nvvm_safety::*;

let cal = HardwareCalibration::from_adapter_info(&adapter_info);
if cal.is_tier_safe(PrecisionTier::Df64, true) {
    // Safe to compile DF64 shader with transcendentals
} else {
    // Fall back to F64 or F32
    let tier = cal.best_tier(true, true);
}
```

### Action for barraCuda

`compile_full_df64_pipeline()` should call `HardwareCalibration::is_tier_safe()` before compiling shaders with f64 transcendentals on NVIDIA proprietary.

---

## Part 2: Workload Routing Thresholds

### New module: `crates/runtime/orchestration/src/workload_routing.rs`

| Pattern | GPU Crossover N | Provenance |
|---------|:-:|---|
| Reduction | 10,000 | healthSpring V14.1 `kokkos_reduction` |
| Scatter | 50,000 | healthSpring V14.1 `kokkos_scatter` |
| MonteCarlo | 100,000 | healthSpring V14.1 `kokkos_monte_carlo` |
| OdeBatch | 5,000 | healthSpring V14.1 `kokkos_ode_batch` |
| NlmeIteration | 100 | healthSpring V14.1 `kokkos_nlme_iteration` |
| MatMul | 256 | neuralSpring S139 `bench_kokkos_parity` |
| Fft | 4,096 | neuralSpring S139 |
| SpMV | 1,000 | hotSpring v0.6.25 spectral |
| ElementWise | 100,000 | neuralSpring S139 |
| SmithWaterman | 1,000 | neuralSpring S139 BLAST pipeline |

### Action for springs

Springs can use `WorkloadRouter::route(pattern, problem_size)` to get CPU/GPU substrate target. Custom thresholds can override defaults from runtime calibration.

---

## Part 3: Brain Interrupt Pattern

### New module: `crates/runtime/orchestration/src/workload_health.rs`

Absorbed from hotSpring `specs/BIOMEGATE_BRAIN_ARCHITECTURE.md`.

| Type | Variants |
|------|---------|
| `AttentionState` | Green / Yellow / Red |
| `WorkloadAnomaly` | Stalled, Diverging, SlowerThanExpected, ThroughputCollapse, DeviceDegraded, MemoryPressure, DeadlineExceeded |
| `InterruptAction` | NoAction, IncreaseMonitoring, DecreaseMonitoring, KillWorkload, RestartWorkload, MigrateSubstrate, Preempt |

Streak-based escalation: consecutive anomalies escalate Green→Yellow→Red. Consecutive healthy intervals de-escalate (except Red, which requires explicit reset).

---

## Part 4: Deep Debt Elimination

| Issue | Fix |
|-------|-----|
| `"Shader Compile (coralReef)"` label | Removed primal name → `"Shader Compile"` |
| `"GPU Dispatch (barraCuda)"` label | Removed primal name → `"GPU Dispatch"` |
| 4 GiB memory assumption (3 sites) | Runtime-discovered via `toadstool_sysmon::memory_info()` |
| `/etc/toadstool/policies` | Platform-aware via `PlatformPaths::config_dir()` |
| `/run/user/1000` (8 showcase demos) | UID-detected from `/proc/self/status` |
| `deploy_graph_status_structure` test | Fixed: validates structure, not live sockets |
| `SubstrateCapabilities` | Added `memory_capacity_bytes` + `memory_bandwidth_bps` |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --workspace` | PASS |
| `cargo clippy --workspace` | 0 warnings |
| `cargo fmt --check` | 0 diffs |
| Server tests | 545/545 |
| Orchestration tests | 49/49 (21 new) |
| NVVM safety tests | 14/14 (new) |
| Workload routing tests | 8/8 (new) |
| Workload health tests | 13/13 (new) |

---

## Spring Sync Status

toadStool S143 reviewed all springs against the current state:

| Spring | Version | Pin | Gap |
|--------|---------|-----|-----|
| hotSpring | v0.6.25 | S138 | Springs 5 sessions behind (S138→S143) |
| groundSpring | V99 | S130+ | 13 sessions behind |
| neuralSpring | S139 | S130+ | 13 sessions behind |
| wetSpring | V105 | S130+ | 13 sessions behind |
| airSpring | v0.7.5 | S130+ | 13 sessions behind |
| healthSpring | V14.1 | S130+ | 13 sessions behind |

Springs should update their toadStool pin to benefit from: GPU sysmon telemetry (S142), PCIe P2P transport (S142), multi-tenant orchestrator (S142), NVVM safety (S143), workload routing (S143), brain interrupts (S143).
