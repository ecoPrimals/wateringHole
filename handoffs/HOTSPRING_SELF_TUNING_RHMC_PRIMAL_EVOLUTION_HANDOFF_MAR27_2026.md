# hotSpring — Self-Tuning RHMC: Primal Evolution Handoff

**Date:** 2026-03-27
**From:** hotSpring → barraCuda, toadStool, coralReef, primalSpring, ALL springs
**Status:** Self-tuning RHMC calibrator complete (Phases 1-4). NPU bridge pending.
**Experiments:** Exp 101 (GPU RHMC production), Exp 102 (gradient flow at volume), Exp 103 (self-tuning calibrator)
**Modules:** `rhmc_calibrator.rs`, `spectral_probe.rs`, `tolerances/lattice.rs`
**License:** AGPL-3.0-only

---

## What Happened

hotSpring evolved the GPU RHMC infrastructure from hand-tuned fixed parameters
to a self-tuning calibrator that discovers all simulation parameters from physics
measurements. Every parameter is either derived from theory, measured from the
gauge field via GPU power iteration, adapted from acceptance rate feedback, or
validated against heatbath-action consistency. Zero hand-tuned magic numbers.

This is the culmination of Exp 099 (RHMC infrastructure) → Exp 101 (production
Nf=2 and Nf=2+1) → Exp 102 (gradient flow at volume) → Exp 103 (self-tuning).

### Key results

- **SpectralProbe**: GPU power iteration for λ_max(D†D), analytical m² bound for
  λ_min. Replaces hardcoded [0.01, 64.0] with measured spectral range.
- **RhmcCalibrator**: Acceptance-driven dt/n_md adaptation, consistency-driven
  pole count, force/Metropolis CG tolerance split. Produces fully configured
  `RhmcConfig` from `(Nf, mass, β, dims)`.
- **12 named tolerance constants** in `tolerances/lattice.rs`, each with physics
  justification in doc comments.
- **`--adaptive` flag** on `production_rhmc_scan` binary for zero-config runs.

---

## For barraCuda

### Absorb: Self-tuning pattern as a general primal capability

The `RhmcCalibrator` pattern — measure, adapt, validate, repeat — is the same
feedback loop that any scientific simulation needs. barraCuda should consider
promoting the pattern to a general-purpose `SimulationCalibrator` trait:

```rust
pub trait SimulationCalibrator {
    type Config;
    type Result;
    fn produce_config(&self) -> Self::Config;
    fn observe(&mut self, result: &Self::Result);
    fn needs_recalibration(&self) -> bool;
}
```

This would allow other springs (wetSpring MD, healthSpring PK/PD) to use the
same self-tuning infrastructure with domain-specific physics validators.

### Absorb: Spectral probing as a dispatch operation

`SpectralProbe` (GPU power iteration + Dirac dispatch) should become a barraCuda
dispatch op: `lattice.spectral.probe(operator, n_iter)`. The power iteration
pattern is generic — it works for any linear operator, not just D†D.

### Evolve: Tolerance system

The 12 new RHMC constants in `tolerances/lattice.rs` follow the existing naming
convention (`RHMC_*` prefix). The tolerance system is growing organically — 
consider whether a `ToleranceSet` or per-domain tolerance group would help
organize the 50+ constants that now live in this module.

---

## For toadStool

### Absorb: Calibrator as a brain-compatible module

The `RhmcCalibrator` state (dt, n_md, n_poles, spectral range, acceptance
history) is exactly the kind of data that the toadStool brain should track.
New surface endpoints:

- `compute.rhmc.calibrate` — trigger spectral probe, return SpectralInfo
- `compute.rhmc.produce_config` — get current RhmcConfig from calibrator
- `compute.rhmc.observe` — feed trajectory result to calibrator
- `compute.rhmc.status` — dt, n_md, poles, acceptance rate, mean |ΔH|

### Evolve: Multi-GPU calibrator aggregation

On a multi-GPU fleet, each device runs trajectories independently. The
calibrator should aggregate observations from all devices, converging
faster on optimal parameters. This is a natural extension of the existing
`ResourceOrchestrator` + `PcieTransport` infrastructure.

### Evolve: Hardware-aware initial heuristics

The calibrator currently uses volume-scaled initial dt. On HBM2 cards
(Titan V, MI50) with faster CG solves, the initial dt can be more
aggressive. toadStool's `GpuCapabilities` should inform the calibrator's
starting point.

---

## For coralReef

### No direct absorption needed

The self-tuning calibrator operates at the simulation layer above shader
dispatch. However, the spectral probe's power iteration pattern (repeated
Dirac dispatch + dot product) would benefit from coralReef's kernel fusion:
fusing the D†D application with the normalization step would eliminate one
readback per iteration.

---

## For primalSpring

### Pattern: Physics-validated parameter discovery

The self-tuning RHMC demonstrates a general primal pattern:

1. Classify every parameter (mathematical / discovered / adapted / validated / learned)
2. Never hand-tune what can be measured
3. Use physics observables as the sole validator
4. Degrade gracefully without NPU (NPU accelerates but is not required)
5. Store all thresholds as named, documented constants

This pattern applies to any spring's simulation: wetSpring (MD step sizes,
thermostat coupling), healthSpring (PK/PD integration tolerances),
airSpring (sensor calibration intervals), groundSpring (soil model parameters).

### NPU integration roadmap

The calibrator's `NpuBridge` (Phase 5) connects to existing NPU heads:
- `A2_ANDERSON_LAMBDA_MIN` → spectral minimum prediction
- `ANOMALY_DETECT` → configuration safety flags
- `CG_ESTIMATE` → iteration count prediction
- `PARAM_SUGGEST` → direct dt/n_md suggestions

These heads are already defined in `barracuda/src/md/reservoir/heads.rs`.
The ESN training infrastructure from Exp 020-029 provides the training
pipeline. The missing piece is the feedback loop from calibrator observations
to ESN training data, which the `NpuBridge` will provide.

---

## For ALL springs

### The self-tuning principle

hotSpring has demonstrated that hand-tuning simulation parameters is
non-reproducible work. The calibrator replaces it with a reproducible
algorithm: measure the physics, adapt the parameters, validate the results.

Any spring that currently requires human-tuned parameters should evolve
toward the same pattern. The infrastructure (tolerance constants, feedback
loops, spectral probes) is in barraCuda and available to all consumers.

### Experiment log

Full details in `hotSpring/experiments/103_SELF_TUNING_RHMC_CALIBRATOR.md`.
baseCamp briefing in `hotSpring/whitePaper/baseCamp/self_tuning_rhmc.md`.

---

## Files Changed (hotSpring)

| File | Change |
|------|--------|
| `barracuda/src/lattice/gpu_hmc/spectral_probe.rs` | **NEW** — SpectralInfo + GPU power iteration |
| `barracuda/src/lattice/gpu_hmc/rhmc_calibrator.rs` | **NEW** — RhmcCalibrator orchestrator |
| `barracuda/src/lattice/gpu_hmc/gpu_rhmc.rs` | Extended GpuRhmcResult, pub(super) dirac_dispatch |
| `barracuda/src/lattice/gpu_hmc/mod.rs` | Re-exports for new modules |
| `barracuda/src/lattice/rhmc.rs` | `RhmcConfig::calibrated_nf2()` constructor |
| `barracuda/src/tolerances/lattice.rs` | 12 new RHMC self-tuning constants |
| `barracuda/src/tolerances/mod.rs` | Re-exports for new constants |
| `barracuda/src/bin/production_rhmc_scan.rs` | `--adaptive` flag + calibrator integration |
| `experiments/103_SELF_TUNING_RHMC_CALIBRATOR.md` | Experiment journal |
| `whitePaper/baseCamp/self_tuning_rhmc.md` | baseCamp briefing |
