# barraCuda v0.3.4 — Cross-Spring Absorption Sprint 3 Handoff

**Date**: March 9, 2026
**From**: barraCuda v0.3.3 → v0.3.4
**To**: All springs, toadStool, coralReef
**License**: AGPL-3.0-or-later
**Springs reviewed**: hotSpring v0.6.24, groundSpring V99, neuralSpring S135, wetSpring V102, airSpring v0.7.5, healthSpring V13, toadStool S139

---

## Summary

Sprint 3 addressed all new absorption requests from the latest spring handoffs.
Three new API conveniences, one discovery alignment, one composite spectral
primitive, and confirmed five capabilities were already present.

---

## New Public API Surface

### `Rk45Result::variable_trajectory(var_idx)` → `Vec<f64>`
Extracts the trajectory of a single ODE variable across all recorded time steps.
Replaces the manual `y_history[step][var_idx]` indexing pattern used by 5+ ODE
scenario builders in wetSpring V102. Also added `n_vars()`. 2 tests.

**For springs**: Replace:
```rust
let traj: Vec<f64> = result.y_history.iter().map(|step| step[var_idx]).collect();
```
With:
```rust
let traj = result.variable_trajectory(var_idx);
```

### `spectral::analyze_weight_matrix(matrix, n, gamma)` → `WeightMatrixAnalysis`
Composite primitive combining:
- `eigh_f64` eigenvalue decomposition
- Spectral bandwidth, condition number, phase classification (Marchenko-Pastur)
- Mean inverse participation ratio (IPR)
- Level spacing ratio ⟨r⟩
- Spectral entropy

Single call for neural network weight matrix diagnostics. 4 tests.

**For neuralSpring**: Replace local `WeightSpectralResult` computation with:
```rust
let analysis = barracuda::spectral::analyze_weight_matrix(&weights, n, 1.0)?;
```

### `histogram_u32_to_f64(counts: &[u32])` → `Vec<f64>`
Conversion for GPU k-mer histogram readback. Spectrum/visualization channels
require `Vec<f64>`; GPU histograms produce `Vec<u32>`. 2 tests.

---

## Discovery Evolution

### toadStool S139 Dual-Scan Alignment
`discover_from_file()` now scans both:
1. `$XDG_RUNTIME_DIR/ecoPrimals/` (flat — toadStool S139 compat write)
2. `$XDG_RUNTIME_DIR/ecoPrimals/discovery/` (canonical path)

This aligns with toadStool S139's dual-write discovery pattern, ensuring
barraCuda can discover primals regardless of which path they announce on.

---

## Confirmed Existing Coverage (No Absorption Needed)

| Capability | Requested By | Status |
|-----------|-------------|--------|
| `regularized_gamma_q(a, x)` | airSpring v0.7.5 | Already in `special::gamma` |
| `CorrelationResult::r_squared()` | airSpring v0.7.5 | Already in `ops::correlation_f64_wgsl` |
| ET0 GPU: Thornthwaite (op=11) | airSpring v0.7.5 / ISSUE-008 | Already in `batched_elementwise_f64.wgsl` |
| ET0 GPU: Makkink (op=14) | airSpring v0.7.5 / ISSUE-008 | Already in `batched_elementwise_f64.wgsl` |
| ET0 GPU: Turc (op=15) | airSpring v0.7.5 / ISSUE-008 | Already in `batched_elementwise_f64.wgsl` |
| ET0 GPU: Hamon (op=16) | airSpring v0.7.5 / ISSUE-008 | Already in `batched_elementwise_f64.wgsl` |

---

## Quality Gates

```
cargo check:            PASS
cargo clippy:           PASS (zero warnings)
cargo fmt --check:      PASS (zero diffs)
cargo test (targeted):  8/8 new tests PASS
```

## Remaining Open Items

### P2 — Pending
- RHMC multi-shift CG solver (hotSpring)
- Adaptive HMC dt from acceptance rate (hotSpring)
- `ComputeBackend` trait (P3)
- `ComputeDispatch` tarpc for NUCLEUS (P3)
- `BandwidthTier` in device profile (P3)
- `domain-genomics` feature extraction (P3)
- Phylogenetic placement GPU op (wetSpring V102)

### ISSUE-006 — Open
GPU-side `special_f64.wgsl` primitives that avoid cancellation by design.
CPU-side `plasma_dispersion_w_stable()` already absorbed. GPU shader evolution
pending (requires per-operation FMA policy from coralReef).

### ISSUE-008 — Resolved
All 4 ET0 methods (Thornthwaite, Makkink, Turc, Hamon) confirmed present as
GPU shaders via `BatchedElementwise` op codes 11, 14, 15, 16. airSpring can
close this issue.

---

## File Changes

- `crates/barracuda/src/numerical/rk45.rs` — added `impl Rk45Result` with `variable_trajectory()` and `n_vars()`
- `crates/barracuda/src/numerical/rk45_tests.rs` — 2 new tests
- `crates/barracuda/src/spectral/stats.rs` — added `WeightMatrixAnalysis`, `analyze_weight_matrix()`, helper functions, 4 new tests
- `crates/barracuda/src/spectral/mod.rs` — re-exports for `WeightMatrixAnalysis`, `analyze_weight_matrix`
- `crates/barracuda/src/ops/bio/kmer_histogram.rs` — added `histogram_u32_to_f64()`, 2 new tests
- `crates/barracuda/src/ops/bio/mod.rs` — re-export `histogram_u32_to_f64`
- `crates/barracuda/src/device/coral_compiler/discovery.rs` — dual-scan discovery paths
- Root docs: `SPRING_ABSORPTION.md`, `WHATS_NEXT.md`, `STATUS.md`, `specs/REMAINING_WORK.md`
