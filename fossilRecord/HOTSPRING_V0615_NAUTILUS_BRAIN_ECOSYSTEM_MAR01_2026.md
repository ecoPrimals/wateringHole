# hotSpring v0.6.15: Nautilus Shell + Brain Architecture Handoff

**Date:** March 1, 2026
**From:** hotSpring (computational physics validation)
**To:** All primals, all springs, toadStool/barracuda team
**License:** AGPL-3.0-only
**Covers:** v0.6.14 → v0.6.15, Exp 024–029, bingoCube/nautilus crate

---

## Executive Summary

- **4-layer brain architecture** operational: RTX 3090 (motor), Titan V
  (pre-motor), CPU 256GB (cortex), AKD1000 NPU (cerebellum with 15 heads).
  All substrates run concurrently during production HMC.
- **Nautilus Shell** (`primalTools/bingoCube/nautilus`): evolutionary reservoir
  computing from bingo boards. 5.3% LOO generalization error on QCD data.
  540× cost reduction via quenched→dynamical transfer. 26 tests, 3 examples.
- **First NPU-steered dynamical production** (Exp 029): NPU controls beta
  selection order, Titan V pre-thermalizes, CPU runs Anderson 3D proxies.
- **Concept edge detection**: LOO error spikes identify physical phase
  boundaries where predictions fail — maps the edge of knowledge.
- **NVK dual-GPU deadlock fix**: serialize `wgpu::Device` creation on main
  thread, then move devices to worker threads.

---

## Part 1: Brain Architecture (v0.6.15)

### What Changed

The production binary (`production_dynamical_mixed`) evolved from a serial
GPU-then-NPU loop into a concurrent brain with 4 layers:

| Layer | Substrate | Role | Status |
|-------|-----------|------|--------|
| Motor | RTX 3090 | CG/HMC solve (primary physics) | Production |
| Pre-motor | Titan V (NVK) | Quenched pre-thermalization for next β | Production |
| Cortex | CPU (TR 3970X, 256GB) | Anderson 3D proxy, ESN retrain | Production |
| Cerebellum | AKD1000 NPU | 15-head steering, anomaly detection | Production |

### Why This Matters for Other Springs

Any spring doing expensive iterative computation (CG solvers, eigensolvers,
optimization loops) can benefit from the same architecture:

1. **NPU as always-on monitor**: 30 mW inference while GPU computes.
   Detects anomalies without blocking the primary compute.
2. **Second GPU as pre-processor**: Pre-thermalize, pre-compute, or run
   cheap physics proxies concurrently with the primary workload.
3. **CPU cortex**: 256 GB RAM for deep analysis that doesn't fit on GPU.
   Anderson eigendecomposition, ESN retraining, post-analysis.

### NVK Dual-GPU Pattern

```
// Create BOTH devices on main thread (avoids NVK deadlock)
let (device_3090, queue_3090) = create_device(adapter_3090);
let (device_titan, queue_titan) = create_device(adapter_titan);
// Then move to worker threads
thread::scope(|s| {
    s.spawn(|| use_device(device_titan, queue_titan));
    // main thread uses device_3090
});
```

**toadStool action:** Absorb this pattern into `MultiDevicePool`.

---

## Part 2: Nautilus Shell (bingoCube/nautilus)

### What It Is

Evolutionary reservoir computing using BingoCube bingo boards as structured
random projections. Each board is a 5×5 grid of integers with column-range
constraints (col 1: 1–15, col 2: 16–30, etc.). A population of boards
forms the reservoir. Evolution replaces temporal recurrence — the
evolutionary history IS the memory.

### Validated Results

| Metric | Value |
|--------|-------|
| LOO CG error | 5.3% (16 boards, 20 generations) |
| Quenched→dynamical transfer | 4.4% LOO, **540× cost reduction** |
| Concept edge detection | 25.7% error at β=6.131 (phase boundary) |
| Crate | 7 modules, 26 tests, 3 examples |
| Shell serialization | JSON, ~37 KB |

### Crate Structure

```
bingocube-nautilus/
├── src/
│   ├── response.rs      # Board → ResponseVector via BLAKE3
│   ├── population.rs    # Ensemble, fitness (Pearson correlation)
│   ├── evolution.rs     # Selection, crossover, mutation (column-range)
│   ├── readout.rs       # Ridge regression, Cholesky solver
│   ├── shell.rs         # NautilusShell: history, transfer, merge
│   ├── constraints.rs   # DriftMonitor (N_e·s), EdgeSeeder
│   └── brain.rs         # NautilusBrain: integration API
└── examples/
    ├── shell_lifecycle.rs         # Within + between instance demo
    ├── live_qcd_prediction.rs     # Real QCD data training + LOO
    └── quenched_to_dynamical.rs   # Transfer learning demo
```

### Why This Matters for Other Springs

- **wetSpring**: Anderson spectral statistics as Nautilus Shell input
  features. Board populations can evolve to predict QS transitions.
- **neuralSpring**: Nautilus Shell is a drop-in alternative to ESN for
  feed-forward hardware. No temporal feedback required.
- **airSpring**: Board evolution for ET₀ prediction from weather streams.
  Edge seeding detects microclimatic anomalies.
- **All springs**: Drift monitor implements the N_e·s boundary from the
  constrained evolution thesis — detects when evolutionary selection is
  failing due to insufficient population diversity.

### AKD1000 Mapping

Column-range constraint (integers 1–75) maps directly to int4 weights
(values 0–15 with column offset). The feed-forward architecture requires
no on-chip recurrence. A population of 16 boards = 16×25 = 400 int4
weights = 200 bytes. The AKD1000 can hold thousands of populations
simultaneously.

**toadStool action:** Wire `bingocube-nautilus` as a workspace dependency.
Map `Population::project()` to `akida-models` int4 inference pipeline.

---

## Part 3: ESN + NPU Evolution

### Current State (15 Heads)

| Head Group | Heads | Function |
|-----------|-------|----------|
| Pre-GPU | 4 | β screening, CG estimation, phase classification, quenched length |
| During-GPU | 5 | CG monitoring, reject prediction, plaquette tracking, therm detector, stepping |
| Post-GPU | 3 | CG cost, observable regression, anomaly detection |
| Proxy | 3 | Anderson CG prediction, spectral features, phase proxy |

### Cross-Run Learning

ESN weights persist across runs via JSON serialization. Exp 029 bootstraps
from Exp 024 (17 β points) + Exp 028 (8 β points) = 25 combined data
points. Each run enriches the next.

### Concept Edge Detection

When overlapping head groups disagree on a prediction, the disagreement
signal marks a **concept edge** — a region where the physics changes
qualitatively and predictions fail. These are the most scientifically
interesting regions and should be investigated, not avoided.

**wetSpring action:** Concept edges in Anderson spectral statistics may
correspond to QS phase transitions. The disagreement map could identify
novel microbial community states.

---

## Part 4: Action Items

### toadStool / barracuda Team

1. Absorb `NautilusBrain` API into `ai.*` JSON-RPC namespace
2. Wire `bingoCube-nautilus` as workspace dependency
3. Integrate drift monitor into `MultiDevicePool` scheduler
4. Absorb NVK dual-GPU serialization pattern into `MultiDevicePool`
5. Map board populations to AKD1000 int4 via `akida-models`

### wetSpring

1. Review concept edge detection for QS applications
2. Consider Nautilus Shell for Anderson spectral prediction (alternative to ESN)
3. Share Anderson localization features with hotSpring brain cortex

### neuralSpring

1. Evaluate Nautilus Shell as feed-forward ESN replacement for streaming
2. Drift monitor integration for training stability detection

### All Springs

1. Brain architecture pattern (4-layer concurrent) applicable to any
   multi-substrate workload
2. Cross-run learning via weight serialization now validated in production

---

## Files

| File | Location | Purpose |
|------|----------|---------|
| Brain arch spec | `hotSpring/specs/BIOMEGATE_BRAIN_ARCHITECTURE.md` | Full 4-layer specification |
| Nautilus crate | `primalTools/bingoCube/nautilus/` | Evolutionary reservoir computing |
| Exp 029 doc | `hotSpring/experiments/029_NPU_STEERING_PRODUCTION.md` | NPU-steered production run |
| Local handoff | `hotSpring/wateringHole/handoffs/HOTSPRING_NAUTILUS_BRAIN_TOADSTOOL_HANDOFF_MAR01_2026.md` | Detailed toadStool absorption guide |
| Thesis §3.4.6 | `whitePaper/gen3/thesis/03_theoretical_framework.md` | Nautilus Shell as constrained evolution evidence |
| baseCamp Paper 11 | `whitePaper/gen3/baseCamp/11_bingocube_nautilus_shell.md` | Full technical paper |
