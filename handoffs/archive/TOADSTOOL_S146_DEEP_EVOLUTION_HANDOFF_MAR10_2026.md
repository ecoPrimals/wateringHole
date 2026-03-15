# ToadStool S146 — Deep Evolution Handoff

**Session**: S146 (March 10, 2026)
**From**: toadStool
**To**: All springs, barraCuda
**Tests**: 19,972 passed (0 failures, 101 skipped)
**Clippy**: Pedantic clean
**Spring Pins**: hotSpring v0.6.27, groundSpring V100, neuralSpring V96/S143, wetSpring V109, airSpring v0.7.5, healthSpring V19

---

## Changes in S146

### 1. nvvm_transcendental_risk in gpu.info (P0 — hotSpring v0.6.26 request)

The `gpu.info` JSON-RPC response now includes an `nvvm_safety` object with per-device:
- `nvvm_poisoning_risk` — driver-inferred risk classification
- `nvvm_transcendental_risk` — boolean, true if DF64/F64Precise transcendentals may poison
- `f64_transcendentals_safe` / `df64_transcendentals_safe` — safe-tier booleans
- `safe_tiers` — array of safe precision tiers (e.g. `["F32", "F64", "F64Precise", "DF64"]`)

**Impact on springs**: hotSpring and barraCuda can now query toadStool for NVVM safety classification instead of probing locally (which risks device poisoning).

### 2. PrecisionBrain wired into compile_wgsl_multi

`shader.compile.wgsl.multi` response now includes a `precision_advice` object with per-target-device:
- `safe_tiers` — which precision tiers to compile for
- `avoid_transcendentals` — whether DF64/F64Precise transcendentals should be avoided

This prevents compilation of dangerous shaders on proprietary NVIDIA drivers.

### 3. PcieTopologyGraph marked stable

`PcieTopologyGraph` now has:
- `#[non_exhaustive]` — fields may be added without breakage
- `PcieTopologyGraph::empty()` constructor for testing
- Doc annotation declaring stability as of S146

Springs may depend on `pair()`, `switch_neighbors()`, and `effective_bandwidth_bps()` without breakage risk.

### 4. SpringDomain expansion (wetSpring V109 convention)

10 new `SpringDomain` variants added:
- `Pharmacokinetics`, `Biosignal`, `Microbiome` (healthSpring)
- `Agriculture`, `Environmental` (airSpring)
- `Phylogenetics`, `MassSpectrometry` (wetSpring)
- `UncertaintyQuantification` (groundSpring)
- `EvolutionaryComputation`, `Optimization` (neuralSpring)

`SpringDomain::as_str()` returns SCREAMING_SNAKE_CASE per wetSpring V109 naming convention.

`HealthSpring` added to `Spring` enum with `Spring::ALL` including all 6 springs.

**Breaking change**: `provenance_json()` domain strings changed from PascalCase to SCREAMING_SNAKE_CASE. Any consumer parsing domain names should update.

### 5. gpu_memory_estimate_bytes + route_with_vram (healthSpring V19)

`WorkloadPattern::gpu_memory_estimate_bytes(problem_size)` returns conservative VRAM estimates:
- N×N patterns (Pairwise, SpatialPayoff): `8 * N²`
- FFT: `16 * N` (complex f64)
- Sparse (SpMV): `24 * N`
- Default: `8 * N`

`WorkloadRouter::route_with_vram()` falls back to CPU if estimated GPU memory exceeds available VRAM.

### 6. Cross-spring provenance expanded

Two new `CrossSpringFlow` entries for healthSpring:
- `PopulationPk/DoseResponse WorkloadPatterns` (from→ALL, Pharmacokinetics domain)
- `DiversityIndex WorkloadPattern` (from→wetSpring+neuralSpring, Biosignal domain)

---

## Action Items for Springs

| Spring | Action | Priority |
|--------|--------|----------|
| hotSpring | Use `gpu.info` `nvvm_safety` instead of local probing. Verify v0.6.27 compat. | P0 |
| barraCuda | Consume `precision_advice` from `shader.compile.wgsl.multi` response for per-device tier selection. | P1 |
| wetSpring | Confirm SCREAMING_SNAKE_CASE domain string compat. New SpringDomain variants available. | P1 |
| healthSpring | `MichaelisMentenBatch`, `ScfaBatch`, `BeatClassifyBatch` noted as StageOps — will add as WorkloadPatterns when thresholds validated. | P2 |
| neuralSpring | `ParallelEighDispatch` and `EnsembleDisagreement` pipeline graph noted — barraCuda-level. | P2 |
| All springs | `PcieTopologyGraph` is now stable. Topology-aware scheduling available via `route_multi_gpu()`. | INFO |

---

## Files Changed

| File | Change |
|------|--------|
| `crates/server/src/pure_jsonrpc/handler/core.rs` | gpu_info() now includes nvvm_safety |
| `crates/server/src/gpu_system.rs` | +query_nvvm_safety() function |
| `crates/server/src/pure_jsonrpc/handler/mod.rs` | compile_wgsl_multi enriched with precision_advice; +build_precision_advice() |
| `crates/core/sysmon/src/pcie_topology.rs` | PcieTopologyGraph #[non_exhaustive] + empty() constructor |
| `crates/core/toadstool/src/cross_spring_provenance.rs` | +10 SpringDomain variants, HealthSpring, as_str() SCREAMING_SNAKE_CASE, 2 new flows |
| `crates/runtime/orchestration/src/workload_routing.rs` | +gpu_memory_estimate_bytes(), +route_with_vram(), tests |
| Root docs | EVOLUTION_TRACKER, SPRING_ABSORPTION_TRACKER, README, DEBT, NEXT_STEPS updated |
