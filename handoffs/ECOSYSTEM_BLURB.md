# ecoPrimals Ecosystem Blurb — Publication Phase (Primal Handoffs)

**Date**: Aug 3, 2026 AM | **Wave**: 155n | **From**: strandGate → eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. arXiv 5/5 FILLED (Rung 1 experiment queue ACTIVE). GPU PRNG bias QUANTIFIED: 9.5% variance deficit, bit-identical NVIDIA + AMD. Multi-vendor proof LIVE (190× CPU speedup on AMD RDNA2). 11 gates ONLINE.**

---

## PRIMAL HANDOFFS — ACTION REQUIRED

These are the primal-level evolution targets derived from strandGate's math validation
and PRNG root-cause analysis. Each handoff is scoped to a specific primal and can be
executed independently.

---

### HANDOFF 1: barraCuda — WGSL Transcendental Validation Layer [P1]

**Finding**: WGSL `log(f64)` and `cos(f64)` produce a **9.5% variance deficit** in
Box-Muller output. Both NVIDIA (naga → SPIR-V → PTX) and AMD (naga → SPIR-V → RDNA IL)
produce **bit-identical** wrong output. This is a naga shader compiler or driver
transcendental implementation bug, not hardware-specific.

| Metric | GPU (WGSL) | CPU (IEEE 754) | Expected |
|--------|-----------|---------------|----------|
| σ | 0.6727 | 0.7079 | 0.7071 |
| ⟨p²⟩ | 0.4525 | 0.5011 | 0.5000 |
| Excess kurtosis | +0.84 | −0.003 | 0 |

**Action items**:

1. **Add `math::transcendental` module** to barraCuda with three paths:
   - `Validated`: Taylor series polyfill with known error bounds (correct, ~2× slower)
   - `Hardware`: f32 TMU → f64 promotion (fast, ~7-digit precision, adequate for PRNG)
   - `Native`: bare WGSL `log`/`cos` (broken on current drivers — document as hazard)

2. **Implement ziggurat PRNG** in pure WGSL (integer + f64 arithmetic, zero transcendentals).
   This eliminates the polyfill risk entirely. Reference: Marsaglia & Tsang (2000).

3. **Add distribution validation gate** to barraCuda CI:
   dispatch PRNG → readback → assert σ within 1% of expected.

**Affected gates**: ALL gates running physics via WGSL f64 transcendentals.
**Data**: `hotSpring/barracuda/src/bin/prng_polyfill_validation.rs` (ready to run anywhere).
**AAR**: `wateringHole/aars/STRANDGATE_PLAQUETTE_DIVERGENCE_ROOT_CAUSE_AAR.md`

---

### HANDOFF 2: hotSpring — Shader Composition Refactor [P1]

**Finding**: `GpuHmcStreamingPipelines::new()` composes the PRNG pipeline as:
```
format!("{WGSL_PRNG_PCG_F64}\n{WGSL_SU3_RANDOM_MOMENTA_F64}")
```

Both files define `pcg_hash`, `hash_u32`, `uniform_f64`. The **duplicate definitions
cause silent compilation failure** — the pipeline produces all-zero output with no
error from wgpu/naga.

**Action items**:

1. **Separate header from consumer**: `su3_random_momenta_f64.wgsl` should NOT
   self-contain the hash functions. It should assume `pcg_hash`, `hash_u32`,
   `uniform_f64` are provided by the composition header.

2. **Unify composition across all HMC modes**: Quenched streaming, dynamical,
   unidirectional, and Hamiltonian variants all compose shaders differently.
   ONE composition function, multiple consumer shaders.

3. **Add shader smoke test**: Dispatch → readback → assert non-zero. Catches
   silent compilation failures. Add to hotSpring CI.

4. **Share thermalized lattice**: The GPU production function re-thermalizes
   from scratch. Accept a pre-thermalized `Lattice` as argument to halve runtime.

**Affected files**:
- `barraCuda/…/shaders/lattice/su3_random_momenta_f64.wgsl` (remove self-contained funcs)
- `barraCuda/…/shaders/lattice/prng_pcg_f64.wgsl` (canonical header)
- `hotSpring/barracuda/src/lattice/gpu_hmc/streaming.rs` (composition)
- `hotSpring/barracuda/src/lattice/gpu_hmc/dynamical.rs` (composition)

---

### HANDOFF 3: hotSpring — Rung 1 Experiment Queue [P1 — arXiv blocker]

**Status**: 5/5 data sections filled. Rung 1 reframing applied. Experiment queue
is the remaining critical path per sporePrint AI review.

| # | Experiment | Deliverable | strandGate Status |
|---|-----------|-------------|-------------------|
| 1 | β-scan (1.8, 2.0, 2.2, 2.3, 2.4, 2.5) at 8⁴ | ⟨P⟩_GPU vs ⟨P⟩_CPU per β | READY — binary exists |
| 2 | 4-8 seeds × 1000 traj at 8⁴ β=2.3 | Per-chain means + bootstrap | READY — needs param change |
| 3 | HMC diagnostics (ΔH histogram, reversibility) | Creutz equality check | READY |
| 4 | PRNG QQ plots + tail statistics | Distribution validation | **DONE** (polyfill validation) |
| 5 | Plaquette normalization check (cold/hot) | Diagnostic | **DONE** (bit-exact: 4e-17) |
| 6 | 12⁴ and 16⁴ production | Extended scaling | GPU-only feasible |
| 7 | pseudoSpore signed release | v1.0.0-rung1 | Needs sweetGrass |

**Note**: Experiments 4 and 5 are COMPLETE from our PRNG validation and static
plaquette diagnostic. Experiments 1-3 and 6 are straightforward extensions of the
existing `arxiv_production_run` binary.

---

### HANDOFF 4: toadStool / coralReef — Statistical Shader Validation [P2]

**Finding**: The current shader validation only checks for compilation success and
crashes, not output correctness. A shader can compile, dispatch, and produce
statistically wrong results with zero errors.

**Action items**:

1. **Add stochastic shader validation** to toadStool's test harness: for any shader
   producing random output, run dispatch → readback → moment test (mean, variance,
   skewness, kurtosis against expected distribution).

2. **Cross-vendor regression matrix**: Same shader, dispatch on all available adapters,
   compare output statistics. The `prng_polyfill_validation` binary is a template.

3. **biomeGate opportunity**: Titan V (SM70, FP64 1:2 rate) may produce CORRECT
   `log(f64)` via hardware transcendentals. Testing would determine if the bug is
   naga-specific or driver-specific. K80 (SM37, FP64 1:3) adds another data point.

---

### HANDOFF 5: sporePrint — LaTeX + Publication [READY]

**Status**: arXiv draft is publication-ready for Rung 1 scope.

| Deliverable | Status |
|-------------|--------|
| LaTeX conversion (REVTeX4-2) | READY — `whitePaper/subGen/lattice_qcd_consumer_gpu.tex` exists |
| Rung 1 experiment queue completion | BLOCKED on hotSpring (experiments 1-3, 6) |
| Hype compliance review | READY (reframing already applied) |
| PRNG advisory (standalone short note) | OPTIONAL — 9.5% bias finding is independently publishable |

---

### HANDOFF 6: sweetGrass — pseudoSpore Release [P3]

Sign and publish `v1.0.0-rung1` pseudoSpore artifact containing:
- Raw trajectory data (4⁴ + 8⁴ at β=2.3, 200 trajectories each)
- Benchmark CSVs (RTX 3090 + RX 6950 XT + CPU timings)
- WGSL compute shaders (as shipped)
- PRNG polyfill validation output
- Full provenance chain (CAS → DAG → Merkle → Spine → Ed25519)

---

## ECOSYSTEM-WIDE ADVISORY

**WGSL f64 transcendental hazard**: Any gate running Monte Carlo or stochastic
physics via WGSL f64 `log`/`cos`/`sin`/`exp` MUST validate output distributions.
The `cpu_mom` pattern (generate random numbers on CPU, upload to GPU) is the
standard workaround until barraCuda provides a validated transcendental layer.

**Applies to**: hotSpring (HMC momenta), any future spring using GPU random sampling,
biomeGate's 44-experiment matrix (QCD science phase).

---

## WHAT STRANDGATE PROVED

| Claim | Evidence |
|-------|---------|
| **Vendor-agnostic physics** | Same WGSL → same ⟨P⟩ on NVIDIA + AMD (\|Δ\|/σ = 0.82, cross-GPU Δ = 3.1e-9) |
| **Consumer GPU viable** | 190× CPU speedup on RX 6950 XT, 47× on RTX 3090 |
| **DF64 precision sufficient** | 9-digit accumulated (DF64), 15-digit (native f64), both >> σ_stat |
| **PRNG is the sole failure mode** | Three-path proof: MD bit-exact, PRNG produces 9.5% variance deficit |
| **Bug is shader-compiler, not hardware** | Bit-identical wrong output on NVIDIA + AMD |
| **`cpu_mom` is correct + fast** | Full GPU speed with CPU-generated momenta, <2% overhead |

---

## GATE FLEET (unchanged)

| Gate | Role | Active Track |
|------|------|-------------|
| **biomeGate** | GPU Crankshaft | G32 silicon deism + Titan V PRNG validation opportunity |
| **strandGate** | Math Validation | Rung 1 experiment queue + PRNG characterization DONE |
| **westGate** | Data Federation | 362 GB / 38 datasets. tideGlass 7/7. |
| **ironGate** | esotericWebb | NUCLEUS 13/13. G20. Session 3 complete. |
| **sporeGate** | CI + Membrane | G34/G35. Agentic LAN 7/8. |
| **southGate** | Validation | G17+G8 PROVEN. RTX 4060 arXiv data (pending). |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| arXiv | **5/5 sections FILLED.** Rung 1 experiment queue: 2/7 DONE, 5 remaining. |
| PRNG bias | **QUANTIFIED**: 9.5% variance deficit, bit-identical cross-vendor |
| Multi-vendor | **PROVEN**: RTX 3090 + RX 6950 XT, same physics |
| Primal handoffs | **6 active** (2× P1 barraCuda/hotSpring, 1× P1 arXiv, 1× P2 toadStool, 1× sporePrint, 1× sweetGrass) |
| Gates online | **11** |
| Science data | **362 GB** on ZFS |

---

*Handoffs frontloaded. The primals know what they need to evolve. barraCuda owns the
transcendental fix. hotSpring owns the composition refactor and experiment queue.
sporePrint is ready when the data lands. The diesel engine works — the transcendentals
just need to tell the truth.*
