# SPDX-License-Identifier: AGPL-3.0-only

# wetSpring V100 → barraCuda/toadStool/petalTongue Handoff

**Date:** 2026-03-09
**From:** wetSpring V100 (1,074 lib tests + 203 forge tests, zero clippy warnings)
**To:** barraCuda team (math primitives), toadStool team (hardware dispatch), petalTongue team (visualization)
**License:** AGPL-3.0-only

---

## Executive Summary

wetSpring V100 integrates petalTongue visualization, validates CPU/GPU math
parity for visualization domains, evolves local code for upstream absorption
readiness, and validates mixed hardware dispatch with bandwidth-aware routing.
Six new experiments (327–332) add 173 validation checks. Total: 1,277 tests,
332 experiments, 311 binaries, 8,982+ checks. Full regression green.

---

## 1. petalTongue Visualization Integration (Exp327, Exp329, Exp330)

### Architecture

wetSpring follows the healthSpring pattern: schema-driven types in
`barracuda/src/visualization/`, IPC push over Unix domain sockets, no direct
petalTongue crate dependency.

```
EcologyScenario (schema)
  ├── ScenarioNode { id, label, kind, channels: Vec<DataChannel> }
  ├── ScenarioEdge { source, target, label }
  └── DataChannel { name, channel_type, unit, data: Vec<f64>, labels }
         └── channel_type: TimeSeries | Distribution | Bar | Gauge | Heatmap | Scatter
```

### Modules Created

| Module | Location | Purpose |
|--------|----------|---------|
| `visualization/types.rs` | barracuda | DataChannel, EcologyScenario, ScenarioNode/Edge |
| `visualization/scenarios/*.rs` | barracuda | 5 builders: diversity, kmd, pcoa, ode, ordination |
| `visualization/ipc.rs` | barracuda | PetalTonguePushClient (JSON-RPC 2.0 over UDS) |
| `forge/visualization/mod.rs` | metalForge | inventory_scenario, dispatch_scenario, nucleus_scenario |

### Validation

- **Exp327** (45/45): Schema serialization, all 5 builders, IPC parameter shapes
- **Exp329** (19/19): metalForge hardware inventory, workload dispatch, NUCLEUS topology
- **Exp330** (34/34): Full chain: biomeOS → NUCLEUS → science → petalTongue → metalForge overlay

---

## 2. CPU vs GPU Pure Math Parity (Exp328)

Validates that GPU-accelerated scientific functions produce results within
tolerance of CPU implementations for all domains exercised by visualization.

| Domain | Functions | Tolerance |
|--------|-----------|-----------|
| Diversity | shannon, simpson, observed_features, pielou_evenness | GPU_VS_CPU_F64 |
| Bray-Curtis | bray_curtis_condensed_gpu | GPU_VS_CPU_F64 |
| PCoA | pcoa eigendecomposition | GPU_VS_CPU_F64 |
| KMD | kendrick_mass_defect | GPU_VS_CPU_F64 |
| ODE | qs_biofilm integrate | GPU_VS_CPU_F64 |

**27/27 PASS.** All GPU results within 1e-10 of CPU.

---

## 3. Local Evolution for Upstream Absorption (Exp331)

### FitResult API Migration

`pangenome::fit_heaps_law` migrated from `r.params[0]` to `r.slope()`:

```rust
// Before (V99)
barracuda::stats::fit_linear(&ln_g, &ln_n).map(|r| r.params[0])

// After (V100)
barracuda::stats::fit_linear(&ln_g, &ln_n).and_then(|r| r.slope())
```

### HmmModel Discoverability

```rust
#[doc(alias = "HMM")]
#[doc(alias = "HiddenMarkovModel")]
pub struct HmmModel { ... }
```

### NMF Bio Re-export

```rust
// bio/mod.rs — V100
pub use barracuda::linalg::nmf;
```

### Quality Test Extraction

`quality/mod.rs` (547 LOC) → `quality/mod.rs` (308 LOC) + `quality_tests.rs` (239 LOC).
Uses `#[cfg(test)] #[path = "quality_tests.rs"] mod tests;` pattern from V93+.

**24/24 PASS.**

---

## 4. Mixed Hardware Dispatch Evolution (Exp332)

### Bandwidth-Aware Workload Routing

Four workloads now carry representative `data_bytes` for `route_bandwidth_aware`:

| Workload | data_bytes | Rationale |
|----------|-----------|-----------|
| kmer_histogram | 10 MB | Per k-mer batch |
| smith_waterman | 50 MB | Pairwise alignment batches |
| pcoa | 8 MB | 1000×1000 f64 distance matrix |
| dada2 | 100 MB | DADA2 E-step matrices |

### Routing Verification

| Scenario | Expected | Actual |
|----------|----------|--------|
| 64 B data | GPU (compute > transfer) | GPU |
| 100 MB data | CPU (transfer dominates) | CPU (BandwidthFallback) |
| No data_bytes | GPU (standard routing) | GPU |
| GPU-preferred + 500 MB | GPU (preference overrides) | GPU |
| 8-bit quant | NPU | NPU |
| SimdVector | CPU | CPU |
| PCIe 4.0 x16, 1 MB | 38 µs transfer | 38.29 µs |

**24/24 PASS.**

---

## 5. Quality Gates

| Gate | Status |
|------|--------|
| `cargo check` (CPU) | PASS |
| `cargo check --features gpu` | PASS |
| `cargo check --features json` | PASS |
| `cargo test -p wetspring-barracuda --features json` | 1,074 passed, 0 failed |
| `cargo test -p wetspring-forge` | 203 passed, 0 failed |
| `cargo clippy --all-targets --features json -- -D warnings` | ZERO warnings |
| `cargo fmt --check` | PASS |
| `cargo doc --no-deps --features json` | PASS (0 warnings) |

---

## 6. Recommendations

### For barraCuda Team
1. **FitResult `.slope()`/`.intercept()` adoption** — wetSpring V100 demonstrates
   the cleaner API. Consider deprecating direct `.params[0]` access.
2. **NMF re-export pattern** — `barracuda::linalg::nmf` works but bio-domain callers
   expect it at `barracuda::bio::nmf` or similar. Consider domain-level re-exports.

### For toadStool Team
1. **BandwidthTier** in workload metadata — wetSpring now wires `data_bytes` into
   `BioWorkload`. toadStool's `capability_call` routing should consume this for
   batched dispatch decisions.
2. **ComputeDispatch migration** (P3) — 6 modules use it; remaining modules use
   barraCuda primitives that manage their own pipelines.

### For petalTongue Team
1. **Schema adoption** — wetSpring's `DataChannel` / `EcologyScenario` types are
   ready for upstream integration. The 6 channel types (TimeSeries, Distribution,
   Bar, Gauge, Heatmap, Scatter) cover all current bio visualization needs.
2. **IPC contract** — `push_render` method over JSON-RPC 2.0 Unix domain socket.
   Schema version "1.0", domain "ecology".

---

## 7. Chain Position

```
V97 (wgpu 28 rewire) → V98 (upstream rewire) → V98+ (cross-spring)
  → V99 (biomeOS/NUCLEUS) → V100 (petalTongue + evolution + mixed HW)
```

---

*This handoff is unidirectional: wetSpring → barraCuda/toadStool/petalTongue. No response expected.*
