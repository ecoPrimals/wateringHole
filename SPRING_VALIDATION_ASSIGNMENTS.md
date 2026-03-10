# Spring Validation Assignments — Live Physics Pipeline

**Purpose**: Assign each spring a specific validation responsibility for barraCuda's
compute dispatch pipeline. barraCuda tests the dispatch; springs validate with
live physics, biology, and domain computation.
**Last Updated**: March 10, 2026
**barraCuda**: v0.3.4 (AGPL-3.0-only, 3,500+ tests, 0 clippy, 0 unsafe, NVVM poisoning guarded)

---

## Principle

> barraCuda validates that the dispatch pipeline works.
> Springs validate that the dispatch pipeline produces correct science.

barraCuda's test suite covers shader compilation, buffer management, tensor
operations, and dispatch correctness. What it cannot test is whether
multi-step scientific workflows produce physically meaningful results under
real-world conditions. That responsibility belongs to the springs.

```
barraCuda (math primal)
  │  validates: dispatch, precision, shader compilation, buffer lifecycle
  │
  ├── hotSpring (physics)
  │     validates: f64 precision under cancellation, conservation laws, spectral convergence
  │
  ├── wetSpring (metagenomics)
  │     validates: statistical stability, bio-diversity indices, ODE integration accuracy
  │
  ├── airSpring (agriculture/hydro)
  │     validates: PDE solver stability, seasonal pipeline chaining, GPU/CPU parity
  │
  ├── groundSpring (condensed matter)
  │     validates: noise resilience, Anderson localization, tolerance system correctness
  │
  ├── neuralSpring (ML/agents)
  │     validates: training convergence, attention numerics, evolutionary stability
  │
  └── healthSpring (PK/PD)
        validates: dose-response curves, population Monte Carlo, eigensolve accuracy
```

---

## Validation Matrix

Each cell describes what the spring validates against barraCuda primitives.

| Spring | barraCuda Module | Validation Target | Success Criteria | Frequency |
|--------|-----------------|-------------------|------------------|-----------|
| **hotSpring** | `ops::md::forces` | Yukawa/Coulomb/Morse force accuracy | Energy conservation ≤ 10⁻⁶ drift per 1000 steps | Per release |
| **hotSpring** | `linalg::sparse` | CG solver convergence on lattice systems | Residual ≤ 10⁻¹² in ≤ 500 iterations | Per release |
| **hotSpring** | `shaders::sovereign::df64_rewrite` | DF64 precision under subtraction | ULP error ≤ 4 vs CPU f64 reference | Per release |
| **hotSpring** | `special::plasma_dispersion` | W(z) near cancellation points | Relative error ≤ 1% at z·Z(z) ≈ -1 | Per release |
| **wetSpring** | `ops::bio::*` | Kmer histogram, taxonomy, UniFrac, ANI | Match Python baselines within tolerance tier 8 | Per release |
| **wetSpring** | `numerical::rk45` | Adaptive ODE trajectory accuracy | Endpoint error ≤ configured `atol`/`rtol` | Per release |
| **wetSpring** | `stats::welford` | Parallel Welford numerical stability | Match sequential to ≤ 10⁻¹⁰ relative error | Per release |
| **airSpring** | `pde::richards_gpu` | Richards equation steady-state | Converge within physical bounds, mass conservation | Per release |
| **airSpring** | `ops` (seasonal pipeline) | ET₀ → Kc → WB → Yield chain | End-to-end parity ≤ 0.04% vs CPU | Per release |
| **airSpring** | `stats::correlation` | Fused Pearson on real-world data | r² match NIST reference datasets | Per release |
| **groundSpring** | `spectral::anderson` | Anderson localization length | Match analytic 1D result within 5% | Per release |
| **groundSpring** | `numerical::tolerance` | 13-tier tolerance sweep | All tiers produce monotonic refinement | Per release |
| **groundSpring** | `stats::*` (delegated) | 11 delegated statistical functions | RMSE ≤ tolerance tier 6 vs exact | Per release |
| **neuralSpring** | `nn::lstm_reservoir` | LSTM training convergence | Loss decreasing over 10 epochs | Per release |
| **neuralSpring** | `ops::attention` | Multi-head attention numerics | Softmax sum-to-one ≤ 10⁻⁶ | Per release |
| **neuralSpring** | `ops::wright_fisher_f32` | Allele frequency drift | Distribution matches Wright-Fisher expectation | Per release |
| **healthSpring** | `ops::hill_f64` | Hill dose-response Emax | EC50 recovery within 1% of known | Per release |
| **healthSpring** | `ops::population_pk_f64` | Population PK Monte Carlo | Parameter distribution matches published | Per release |
| **healthSpring** | `special::tridiagonal_ql` | Eigensolve on real PK covariance matrices | Eigenvalues match LAPACK reference | Per release |

---

## Spring-Specific Assignment Details

### hotSpring — Precision & Conservation Validator

**Owner**: Computational physics team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate that f64 and DF64 arithmetic produce
physically correct results under the most demanding numerical conditions.

**Assigned validations**:

1. **Force conservation**: Run 1000-step MD with Yukawa potential.
   Verify total energy drift ≤ 10⁻⁶. Uses `ops::md::forces::yukawa_f64`.
2. **Lattice QCD CG convergence**: Solve 8⁴ lattice system with GPU CG.
   Verify residual convergence to machine epsilon. Uses `linalg::sparse::cg_gpu`.
3. **DF64 subtraction test**: Compute W(z) at 100 points near cancellation.
   Verify ULP error ≤ 4 against arbitrary-precision reference.
4. **GPU/CPU parity**: Run transport coefficient calculation on both.
   Verify agreement within DF64 tolerance.

---

### wetSpring — Statistical & ODE Validator

**Owner**: Metagenomics team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate biological statistics and ODE integrator
correctness across diverse datasets.

**Assigned validations**:

1. **Bio-diversity pipeline**: Run full Shannon/Simpson/UniFrac pipeline
   on NCBI reference datasets. Compare against published values.
2. **ODE integrator accuracy**: Integrate Lotka-Volterra with RK45.
   Verify conservation of Lotka-Volterra invariant.
3. **Parallel Welford stability**: Compute mean/variance of 10⁶ points
   split into 8 chunks. Verify merge matches sequential.
4. **Kmer histogram reproducibility**: Same input → same output across
   CPU and GPU paths.

---

### airSpring — PDE & Pipeline Validator

**Owner**: Agriculture/hydrology team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate PDE solvers and multi-stage GPU pipelines
against published agronomic benchmarks.

**Assigned validations**:

1. **Richards PDE stability**: Run 50-step infiltration simulation.
   Verify moisture profile within physical bounds [0, θ_s].
2. **Seasonal pipeline end-to-end**: ET₀ → dual Kc → water balance → yield.
   Verify GPU matches CPU within 0.04% over 365-day simulation.
3. **FAO-56 PM reference**: Compute ET₀ for 100 Michigan stations.
   Verify against Open-Meteo ERA5 baselines.
4. **GPU/NPU cross-dispatch**: Same computation on GPU and NPU.
   Verify results within tolerance tier 8.

---

### groundSpring — Noise & Tolerance Validator

**Owner**: Condensed matter team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate numerical robustness under adversarial
conditions and verify the tolerance system itself.

**Assigned validations**:

1. **Anderson localization**: Compute localization length for 1D/2D/3D
   disordered systems. Verify 1D matches analytic λ = 105.2 ± 2 at W=1.
2. **Tolerance monotonicity**: Sweep all 13 tolerance tiers on the same
   computation. Verify each tier is strictly tighter than the next.
3. **Noise injection**: Add controlled noise to inputs and verify
   barraCuda stats functions degrade gracefully (no NaN, no panic).
4. **Chi-squared universality**: Run chi-squared on 6 distribution types.
   Verify p-values match scipy.stats reference.

---

### neuralSpring — ML & Evolution Validator

**Owner**: ML/neuroevolution team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate neural network operations and evolutionary
algorithms produce convergent results.

**Assigned validations**:

1. **Attention numerics**: Run multi-head attention on random inputs.
   Verify softmax rows sum to 1.0 within 10⁻⁶.
2. **LSTM convergence**: Train 3-layer LSTM on sine wave prediction.
   Verify loss decreases monotonically over 10 epochs.
3. **Wright-Fisher drift**: Run 1000 populations for 500 generations.
   Verify fixation probability matches 2Ns theory.
4. **ESN spectral radius**: Verify reservoir eigenvalue decomposition
   produces spectral radius within 1% of configured value.

---

### healthSpring — Pharmacology Validator

**Owner**: Health/PK-PD team
**barraCuda pin**: v0.3.4
**Key responsibility**: Validate pharmacological models and eigensolvers
against published clinical and mathematical references.

**Assigned validations**:

1. **Hill dose-response**: Fit Hill curve to published Emax data.
   Verify EC50 recovery within 1% of known value.
2. **Population PK Monte Carlo**: Run 1000-subject simulation.
   Verify Cmax/AUC distribution matches published clinical trial.
3. **Tridiagonal QL eigensolve**: Solve 100×100 real symmetric matrix.
   Verify eigenvalues match LAPACK reference within 10⁻¹².
4. **Microbiome PCA**: Run PCA on OTU abundance matrix.
   Verify explained variance matches R/sklearn reference.

---

## Workflow

1. **barraCuda releases** v0.3.4 (or any version bump)
2. Each spring **pulls the new pin** and runs its assigned validations
3. Results are reported as **pass/fail with numerical evidence**
4. Failures trigger a **SPRING_EVOLUTION_ISSUES.md** entry
5. barraCuda absorbs any fix and springs re-validate

```
barraCuda release
      │
      ├── hotSpring: cargo test --release -- physics_validation
      ├── wetSpring: cargo test --release -- bio_validation
      ├── airSpring: cargo test --release -- pde_validation
      ├── groundSpring: cargo test --release -- tolerance_validation
      ├── neuralSpring: cargo test --release -- ml_validation
      └── healthSpring: cargo test --release -- pk_validation
              │
              ▼
      All pass → pin confirmed
      Any fail → SPRING_EVOLUTION_ISSUES.md → fix → re-validate
```

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-10 | Spring pins updated to v0.3.4; PCIe topology, VRAM quota, BGL builder added to matrix |
| 2026-03-10 | Initial spring validation assignments created |
