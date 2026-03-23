<!--
SPDX-License-Identifier: CC-BY-SA-4.0
https://creativecommons.org/licenses/by-sa/4.0/
-->

# healthSpring V42 → toadStool / barraCuda Absorption Handoff

**Date**: 2026-03-23
**From**: healthSpring V42
**To**: toadStool team, barraCuda team, coralReef team
**Pins**: barraCuda v0.3.7, toadStool S163+, coralReef Phase 10+
**Supersedes**: V41 toadStool/barraCuda Evolution Handoff

## Executive Summary
healthSpring V42 completes the deep debt resolution sprint. All 6 barraCuda GPU ops are live and validated. 3 API drift errors fixed (simulate rename, ScfaParams type bridge, hardware_hint field). ODE codegen wired. 863 tests passing with zero clippy warnings. This handoff documents what barraCuda/toadStool should absorb from healthSpring V42.

## API Drift Fixed in V42

These indicate areas where healthSpring was behind barraCuda's API evolution:

1. **MichaelisMentenBatchGpu**: `.compute()` renamed to `.simulate()` upstream. healthSpring updated. Signature also refactored from 8 individual params to `&MmBatchConfig`.

2. **ScfaParams type**: `crate::microbiome::ScfaParams` and `barracuda::health::microbiome::ScfaParams` are structurally identical but different types. healthSpring now bridges explicitly. Consider: should barraCuda re-export or provide a From impl?

3. **DispatchDescriptor.hardware_hint**: New field `HardwareHint` added by barraCuda. healthSpring defaults to `HardwareHint::Compute`. Sovereign dispatch path now compiles.

## What barraCuda Should Absorb

### New Primitive Requests (unchanged from V41, re-prioritized)

1. **BatchedGradientGpu** (P0) — FOCE per-subject gradient. Each subject independent → embarrassingly parallel.

2. **HormesisSweepGpu** (P1) — Biphasic dose-response batched over dose vectors. toxicology::biphasic_dose_response is element-wise.

3. **CausalChainBatchGpu** (P2) — Multi-pathway Hill product with damage accumulation.

### ODE Systems Ready for Upstream Absorption

3 OdeSystem trait implementations in healthSpring gpu/ode_systems.rs:
- MichaelisMentenOde — capacity-limited PK elimination
- OralOneCompartmentOde — first-order absorption + elimination  
- TwoCompartmentOde — bi-exponential distribution + elimination

These generate valid WGSL via BatchedOdeRK4::generate_shader(). Candidate for barracuda::health::ode module.

### WGSL Shaders Ready for Upstream Review

6 WGSL shaders in ecoPrimal/shaders/health/:
- hill_dose_response_f64.wgsl (already absorbed as barracuda::ops::hill_f64)
- population_pk_f64.wgsl (already absorbed as barracuda::ops::population_pk_f64)
- diversity_f64.wgsl (already absorbed as barracuda::ops::bio::diversity_fusion)
- michaelis_menten_batch_f64.wgsl (absorbed as barracuda::ops::health::michaelis_menten_batch)
- scfa_batch_f64.wgsl (absorbed as barracuda::ops::health::scfa_batch)
- beat_classify_batch_f64.wgsl (absorbed as barracuda::ops::health::beat_classify)

All 6 are absorbed. healthSpring local copies exist only for validation parity testing. No new shader candidates from V42.

### Patterns for toadStool to Absorb

| Pattern | healthSpring File | Relevance |
|---------|------------------|-----------|
| ValidationSink trait | validation.rs | Composable validation output for pipeline stages |
| normalize_method() | ipc/rpc.rs | Strip legacy prefixes before routing |
| OnceLock GPU probe | gpu/mod.rs | Thread-safe cached GPU availability check |
| check_abs_or_rel() | validation.rs | Smart tolerance auto-selection |
| exit_skipped (exit 2) | validation.rs | GPU-absent CI distinction |
| Workspace [lints] | Cargo.toml | Single-source lint governance |

### Cross-Spring Science Opportunities

From the V42 cross-ecosystem review:

| Source Spring | Pattern | healthSpring Application |
|--------------|---------|--------------------------|
| groundSpring V120 | measurement.gillespie / measurement.bistable | Stochastic QS simulation |
| wetSpring V132 | Session provenance DAGs | Reproducibility chains |
| neuralSpring V120 | TensorSession adoption | Fused multi-op GPU |
| airSpring 0.10.0 | Platform-agnostic Transport (Unix+TCP) | Already adopted in V41 |
| ludoSpring V29 | llvm-cov floor + consent-gated medical | ZK medical model scaffolding |

## barraCuda Consumption Summary (v0.3.7)

6 GPU ops (all live), ~25 CPU primitives consumed. No new primitives consumed in V42.

Available but NOT consumed:
- KimuraGpu (population genetics)
- JackknifeGpu (NLME diagnostics) 
- DeviceCapabilities (replaces deprecated GpuDriverProfile)
- tensor.create / tensor.matmul (future NLME matrix ops)

## Quality Snapshot

| Metric | V42 |
|--------|-----|
| Tests | 863 |
| Clippy | 0 errors, 0 warnings |
| cargo deny | PASS |
| cargo doc | 0 warnings |
| Unsafe | 0 |
| barraCuda pin | v0.3.7 |
| GPU ops live | 6/6 |
| ODE codegen ops | 1 (MM batch) |

## Reproduction
```bash
cd healthSpring
cargo test --workspace              # 863 tests, 0 failures
cargo clippy --workspace --all-targets --all-features -- -D warnings  # 0 errors
cargo fmt --check --all             # 0 diffs  
cargo deny check                    # advisories ok, bans ok, licenses ok
cargo doc --workspace --no-deps     # 0 warnings
```

---
*Part of ecoPrimals — sovereign computing for science.*
