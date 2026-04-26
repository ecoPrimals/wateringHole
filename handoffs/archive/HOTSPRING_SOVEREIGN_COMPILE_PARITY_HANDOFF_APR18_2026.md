# hotSpring: Sovereign Compile Parity Handoff

**Date:** April 18, 2026  
**Spring:** hotSpring v0.6.32  
**Primals:** coralReef (coral-reef, coral-gpu, coral-driver), barraCuda  
**License:** AGPL-3.0-or-later

---

## Milestone

Full HMC pipeline (10 QCD shaders) compiles from WGSL to native SASS on three
NVIDIA GPU generations via coralReef's sovereign compiler:

| Target | SM | GPU | Result |
|--------|---:|-----|--------|
| Kepler | 35 | Tesla K80 (GK210) | 10/10 PASS |
| Volta | 70 | Titan V (GV100) | 10/10 PASS |
| Blackwell | 120 | RTX 5060 (GB206) | 10/10 PASS |

Vendor dispatch validated on RTX 5060 via wgpu/Vulkan — Wilson plaquette and
sum reduction dispatch correctly. `validate_pure_gauge --features sovereign-dispatch`
reports **16/16 checks pass**.

---

## coralReef Changes (for upstream absorption)

### 1. f64 Transcendental Lowering Fix (`coral-reef`)

**Files:** `codegen/lower_f64/mod.rs`, `codegen/lower_f64/poly/exp2.rs`, `codegen/lower_f64/poly/trig.rs`

`lower_f64_function()` had an early return (`if !is_amd && sm.sm() < 70 { return; }`)
that skipped f64 transcendental lowering for NVIDIA GPUs below SM70. Since MUFU is
f32-only on ALL NVIDIA generations, this left `OpF64Rcp`/`OpF64Exp2` in the IR and
panicked the SM32 encoder.

Fix:
- Removed the SM < 70 guard
- Added `emit_iadd(out, alloc, pred, a, b, sm)` — IAdd2 for SM32, IAdd3 for SM70+
- Added `emit_shl_imm(out, alloc, pred, src, shift_bits, sm)` — OpShl for SM32, OpShf for SM70+
- Updated `exp2.rs` and `trig.rs` to use these helpers

All 1,314 coral-reef unit tests pass.

### 2. Modified Immediate Fallback (`coral-reef`)

**File:** `codegen/ir/src.rs`

`as_imm_not_i20()` and `as_imm_not_f20()` asserted `is_unmodified()` on `Imm32` sources.
Copy propagation could attach source modifiers (fneg/fabs) to immediates, triggering a panic.
Changed to return `None` when modifiers are present, allowing the encoder to fall back to
register-based encoding.

### 3. QMD v5.0 for Blackwell (`coral-driver`)

**File:** `nv/qmd.rs`

Blackwell (SM120+) uses a 384-byte (96-word) QMD layout vs 256-byte for pre-Hopper.
`build_qmd_v50()` and `build_qmd_for_sm()` dispatch SM >= 100 to v5.0. PCI device ID
range extended to 0x2B00..=0x2DFF for GB206.

---

## HMC Pipeline Shaders Validated

| Shader | Domain |
|--------|--------|
| wilson_plaquette_f64 | Gauge action observable |
| sum_reduce_f64 | Lattice-wide reduction |
| cg_compute_alpha_f64 | CG solver step size |
| su3_gauge_force_f64 | Gauge force for HMC |
| metropolis_f64 | Accept/reject |
| dirac_staggered_f64 | Staggered Dirac operator |
| staggered_fermion_force_f64 | Fermion force |
| fermion_action_sum_f64 | Fermion action |
| hamiltonian_assembly_f64 | Hamiltonian computation |
| cg_kernels_f64 | CG solver operations |

---

## Remaining Blockers

| ID | Description | Severity |
|----|-------------|----------|
| GAP-HS-031 | NOP GPFIFO timeout on RTX 5060 — compile works, dispatch blocked (USERD/channel setup) | Medium |
| GAP-HS-030 | GV100 WPR not used by closed driver (Volta predates GSP) — approach pivot needed | Critical |
| GAP-HS-031-K80 | K80 VFIO EBUSY (kernel iommufd cdev leak on AMD IOMMU) | Medium |

---

## Cross-Spring Relevance

- **primalSpring**: `GpuGeneration` enum pattern (Kepler/CpuRm/GspRm) useful for any primal
  that routes by GPU architecture
- **toadStool**: Ember absorption path — sovereign init and compile validation infra
  ready for migration
- **neuralSpring**: Sovereign compile works; once dispatch is fixed, ML/inference shaders
  can use the same pipeline
- **biomeOS**: `capability_registry.toml` `shader.compile.wgsl` capability now validated
  for cross-generation SASS output

---

## Experiment Journals

- **Exp 173**: VM reagent WPR capture (Volta WPR finding)
- **Exp 174**: K80 Kepler sovereign boot progress
- **Exp 175**: RTX 5060 shared compute (GPFIFO timeout, QMD v5.0)
- **Exp 176**: QCD parity benchmark (full HMC pipeline, f64 fix, 16/16 validate_pure_gauge)
