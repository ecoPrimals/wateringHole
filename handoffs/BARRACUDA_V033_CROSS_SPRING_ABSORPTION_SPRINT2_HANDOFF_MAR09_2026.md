# barraCuda V0.3.3 — Cross-Spring Absorption Sprint 2 Handoff

**Date**: 2026-03-09
**Author**: barraCuda evolution agent
**Scope**: P0 absorptions from healthSpring, neuralSpring; public API consolidation

---

## What Changed

### 1. Tridiagonal QL Eigensolver (`special::tridiagonal_ql`)

**Source**: healthSpring `microbiome.rs` (V13)

- `tridiagonal_ql(diagonal, sub_diagonal) → (eigenvalues, eigenvectors)` — general-purpose
  symmetric tridiagonal eigensolver using QL algorithm with Wilkinson shifts
- `anderson_diagonalize(disorder, t_hop)` — convenience for Anderson tight-binding models
- **Bug fix**: Fixed off-by-one in EISPACK sub-diagonal convention from source code.
  The original healthSpring code placed sub-diagonal in e[0..n-2] but the QL shift
  convention expects e[1..n-1]. Incorrect for n=2 and general non-uniform sub-diagonals.
- 6 unit tests: empty, single, 2×2, Anderson 3-site, diagonal, orthogonality

**Impact for springs**:
- healthSpring/wetSpring can now call `barracuda::special::anderson_diagonalize()` for
  Anderson localization instead of maintaining their own QL code
- Any Lanczos → tridiag → QL pipeline can use this

### 2. LCG PRNG Module (`rng`)

**Source**: healthSpring `rng.rs` (V13)

- `LCG_MULTIPLIER: u64` — Knuth TAOCP Vol 2 constant (6364136223846793005)
- `lcg_step(state) → u64` — single LCG advance
- `state_to_f64(state) → f64` — extract uniform [0,1) from upper 31 bits
- `uniform_f64_sequence(seed, n) → Vec<f64>` — generate n values from seed
- CPU-only; complements existing GPU xoshiro128** (`ops::prng_xoshiro_wgsl`)
- 6 unit tests

**Impact for springs**:
- healthSpring, neuralSpring, wetSpring, airSpring can all import `barracuda::rng::lcg_step`
  instead of hardcoding `6_364_136_223_846_793_005_u64`
- healthSpring's `biosignal.rs` can replace inline `.wrapping_mul(LCG_MULTIPLIER)` calls
  with `lcg_step()`

### 3. Public Activations API (`activations`)

**Source**: Consolidation of duplicate implementations across springs

- Scalar: `sigmoid`, `relu`, `gelu`, `swish`, `mish`, `softplus`, `leaky_relu`
- Batch: `sigmoid_batch`, `relu_batch`, `gelu_batch`, `swish_batch`
- All f64 precision, numerically stable (sigmoid uses conditional exp)
- 8 unit tests

**Impact for springs**:
- `use barracuda::activations::{sigmoid, relu, gelu}` replaces 7+ duplicate implementations
- neuralSpring S134 specifically requested this API

### 4. Wright-Fisher Population Genetics (`ops::wright_fisher_f32`)

**Source**: neuralSpring `metalForge/shaders/wright_fisher_step.wgsl` (Papers 024/025)

- `WrightFisherF32::simulate_generation(freq_in, selection, prng_state) → freq_out`
- Xoshiro128** PRNG per-thread, binomial drift via sequential sampling
- `seed_xoshiro_state(base_seed, n)` — SplitMix32 seeding utility
- New WGSL shader: `shaders/science/wright_fisher_step_f32.wgsl`
- 6 tests: 3 CPU (seed length/nonzero/deterministic), 3 GPU (neutral drift, strong
  selection increases frequency, fixation after 500 generations at N=10)

**Impact for springs**:
- neuralSpring can offload Wright-Fisher to barraCuda GPU instead of maintaining metalForge shader
- Pangenome selection and meta-population dynamics Papers 024/025 can use this directly

### 5. xoshiro128ss.wgsl — Not Absorbed (Already Covered)

barraCuda already has `ops::prng_xoshiro_wgsl` with equivalent xoshiro128** GPU PRNG
supporting both f32 and f64 output modes. No duplicate absorption needed.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check` | ✅ |
| `cargo clippy --all-targets --all-features -D warnings` | ✅ |
| `cargo fmt --check` | ✅ |
| New unit tests (23 CPU + 3 GPU) | ✅ All pass |
| Existing test suite | ✅ No regressions |

---

## New Public API Surface

```rust
// Eigensolver
barracuda::special::tridiagonal_ql(diagonal, sub_diagonal) -> (Vec<f64>, Vec<f64>)
barracuda::special::anderson_diagonalize(disorder, t_hop) -> (Vec<f64>, Vec<f64>)

// PRNG
barracuda::rng::LCG_MULTIPLIER
barracuda::rng::lcg_step(state) -> u64
barracuda::rng::state_to_f64(state) -> f64
barracuda::rng::uniform_f64_sequence(seed, n) -> Vec<f64>

// Activations
barracuda::activations::{sigmoid, relu, gelu, swish, mish, softplus, leaky_relu}
barracuda::activations::{sigmoid_batch, relu_batch, gelu_batch, swish_batch}

// Population genetics
barracuda::ops::WrightFisherF32::new(device, config) -> Result<Self>
barracuda::ops::WrightFisherF32::simulate_generation(freq_in, selection, prng_state) -> Result<Vec<f32>>
barracuda::ops::seed_xoshiro_state(base_seed, n) -> Vec<u32>
```

---

## Remaining P1/P2 Absorption Opportunities

| Item | Source | Priority |
|------|--------|----------|
| `logsumexp_reduce.wgsl` | neuralSpring | P1 |
| `rk45_adaptive.wgsl` improvements | neuralSpring | P1 |
| ET₀ GPU ops (ISSUE-008) | airSpring | P1 |
| `BatchReconcileGpu` | wetSpring | P2 |
| Visualization `push_replace` | healthSpring | P2 |
| PBPK tissue profiles | healthSpring | P2 |
