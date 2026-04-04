# hotSpring GPU RHMC + Silicon Science Handoff

**Date:** March 27, 2026
**From:** hotSpring (Strandgate)
**Experiments:** 096-103 (Silicon Characterization → GPU RHMC → Gradient Flow → Self-Tuning)
**License:** AGPL-3.0-only

---

## Summary

hotSpring has completed the full dynamical QCD science ladder on consumer GPU hardware:
quenched SU(3) → gradient flow → LSCFRK integrators → Nf=4 infrastructure → Chuna 44/44 →
Nf=2 → Nf=2+1 → self-tuning RHMC. This handoff documents what was built, what was learned,
and what each team should absorb.

---

## For barraCuda Team

### GPU RHMC Infrastructure
- `RationalApproximation`: Zolotarev optimal rational approximation via zeta recurrence
- `multi_shift_cg_solve`: Multi-shift CG for rational approximation (all poles solved simultaneously)
- `RhmcFermionConfig` / `RhmcConfig`: 2-sector configuration (light + strange quarks)
- `heatbath_approx`, `action_approx`, `force_approx`: Separate approximations for each RHMC phase
- `det_power`: Fractional power for staggered fermion rooting (1/8 for Nf=2, etc.)

### Self-Tuning Calibrator
- `RhmcCalibrator`: Eliminates all hand-tuned magic numbers
- GPU power iteration for spectral range (lambda_max from D†D, lambda_min from m²)
- Acceptance-driven step adaptation (dt, n_md auto-tuned)
- Consistency-monitored pole count (rational approximation quality from physics observable feedback)
- Only needs physics inputs: Nf, mass, beta, lattice dimensions

### GPU Gradient Flow
- `gpu_flow.rs`: 5 integrators (Euler, RK2/Heun, W6/Luscher, W7/Chuna LSCFRK3, CK4/LSCFRK4)
- LSCFRK coefficients derived from first principles via `const fn derive_lscfrk3(c2, c3)`
- 2N-storage scheme (memory-efficient for large lattices)
- Reuses HMC shader infrastructure (staples, gauge force)
- CK4 stability: 6 orders of magnitude better than W6/W7 at large epsilon

### Absorption Targets
- All RHMC GPU shaders (rational force, multi-shift CG kernels)
- `production_rhmc_flow.rs` as a reference for combining RHMC + flow
- `production_rhmc_scan.rs` for beta-scan workflows
- Self-tuning calibrator pattern for other simulation domains

---

## For toadStool Team

### Silicon Characterization Data (Exp 096-100)
- **RTX 3090 personality**: TMU compositor (1.89x throughput for table lookup), strong shader core
- **RX 6950 XT personality**: Cache/precision champion (AMD DF64 38% faster than NVIDIA, Infinity Cache advantage)
- **Titan V**: Genuine 1:2 fp64:fp32 via NVK, but limited by 12GB HBM2
- 4-phase pipeline: budget → saturation → QCD kernel → composition
- Hardware personality data for `PrecisionBrain` routing evolution

### Precision Routing Discovery
- Mathematical precision requirement should determine silicon unit, not programmer choice
- TMU viable for table-lookup physics (DSF interpolation, special functions)
- ROP viable for atomic accumulation (histogram, reduction)
- L2 cache as working-set amplifier for iterative solvers

### `PrecisionBrain` Evolution Opportunities
- Per-GPU personality profiles from silicon characterization
- Tolerance-based routing: operation → precision requirement → optimal silicon unit
- Fleet-aware scheduling: route DF64-heavy work to AMD, TMU-heavy to NVIDIA

---

## For coralReef Team

### Sovereign SASS for QCD
- RHMC kernels are compute-intensive (multi-shift CG, rational force) — ideal for tensor core acceleration
- Gradient flow kernels are memory-bandwidth-bound (SU(3) matrix operations) — benefit from L2 optimization
- `production_rhmc_flow.rs` demonstrates the full GPU→CPU readback→flow pipeline

### Multi-GPU Dispatch
- `HOTSPRING_GPU_ADAPTER` env var with substring matching (e.g., "3090", "6950")
- `discover_primary_and_secondary_adapters()` auto-discovers by memory/capability
- Dual-GPU validation pattern: same physics on different vendors confirms correctness
- `GpuF64::from_adapter_name()` for explicit adapter selection

---

## For primalSpring Team

### Self-Tuning Pattern
The RHMC calibrator eliminates magic numbers through three mechanisms:
1. **Spectral probe**: GPU power iteration finds lambda_max of D†D; m² gives lambda_min
2. **Acceptance feedback**: dt and n_md adjusted based on Metropolis acceptance rate
3. **Consistency check**: Rational approximation quality monitored via physics observables

This pattern generalizes to any simulation with tunable parameters and measurable quality metrics.

### Cross-Spring Evolution
- 85 WGSL shaders across hotSpring physics domains
- Silicon characterization data feeds into all springs via toadStool
- Hardware personality discovery is spring-agnostic

---

## What We Learned

### Hardware Personalities
- Consumer GPUs are NOT generic compute — each has a distinct personality
- AMD RDNA2 excels at DF64 (38% faster than NVIDIA Ampere) due to wider FP32 ALUs and Infinity Cache
- NVIDIA Ampere excels at TMU-based computation (1.89x throughput)
- The "best GPU for physics" depends on the mathematical operation

### Thermalization Bottleneck
- Small lattices (4^4, 8^4) require very short RHMC trajectories for reasonable acceptance
- Short trajectories = slow thermalization = unreliable equilibrium
- 16^4+ is the minimum for publishable dynamical QCD results
- Adaptive RHMC calibrator partially mitigates this by optimizing trajectory parameters

### CK4 Integrator Stability
- CK4 (LSCFRK4) is 6 orders of magnitude more stable than W6/W7 at large step sizes
- Enables larger epsilon in gradient flow → fewer steps → faster production
- Critical for scaling to 32^4+ lattices where flow step count dominates wall time

### Scaling Path to MILC-Scale
- Current: 8^4 dynamical, 16^4 quenched
- Target: 32^4 → 64^4 (competitive with MILC Nf=2+1+1)
- Strategy: GPU RHMC + multi-GPU (coralReef) + HBM2 fleet (Titan V) + full silicon routing
- Advantage over MILC: cost efficiency ($0.30 vs $M), silicon utilization measurement, portable sovereign stack

---

## Files Referenced

| File | Purpose |
|------|---------|
| `barracuda/src/lattice/gpu_flow.rs` | GPU gradient flow (5 integrators, LSCFRK) |
| `barracuda/src/lattice/gpu_hmc/` | GPU HMC infrastructure |
| `barracuda/src/bin/production_rhmc_flow.rs` | RHMC + gradient flow production binary |
| `barracuda/src/bin/production_rhmc_scan.rs` | RHMC beta-scan production binary |
| `whitePaper/baseCamp/silicon_characterization_at_scale.md` | Silicon characterization strategy |
| `whitePaper/baseCamp/chuna_gradient_flow.md` | Chuna Paper 43 reproduction + extensions |
| `whitePaper/baseCamp/murillo_lattice_qcd.md` | Full lattice QCD science ladder |
| `whitePaper/baseCamp/self_tuning_rhmc.md` | Self-tuning calibrator documentation |
| `experiments/096-100` | Silicon characterization experiments |
| `experiments/101_GPU_RHMC_PRODUCTION.md` | GPU RHMC results |
| `experiments/102_GRADIENT_FLOW_AT_VOLUME.md` | Flow convergence data |
| `experiments/103_RHMC_GRADIENT_FLOW.md` | RHMC + flow on dynamical configs |
