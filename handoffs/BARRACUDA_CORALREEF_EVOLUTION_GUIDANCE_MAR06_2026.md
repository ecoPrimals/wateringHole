# barraCuda → coralReef Evolution Guidance

**Date**: 2026-03-06
**From**: barraCuda v0.3.3+
**To**: coralReef team
**License**: AGPL-3.0-only

---

## Context

barraCuda has completed spring absorption from hotSpring, groundSpring,
airSpring, wetSpring, and neuralSpring. The GPU test coordination harness
(`GpuTestGate`, `CoralProbe`, `gpu_section`) is operational. `Fp64Strategy`
now includes a `Sovereign` tier, and the `CoralCompiler` IPC client is
production-ready. This document describes what barraCuda needs from coralReef
to activate the sovereign pipeline end-to-end.

---

## 1. P0 — f64 Instruction Emission

**What**: groundSpring V85 discovered that coralReef-compiled binaries use
FMUL/FADD (f32 opcodes) instead of DMUL/DADD (f64 opcodes). The `f64_lower`
pass needs to emit double-precision instructions.

**Why it matters**: barraCuda's `Fp64Strategy::Sovereign` variant routes f64
shaders through coralReef when the naga/SPIR-V path fails (all f64
shared-memory reductions return zeros). Without correct f64 instruction
emission, the sovereign binaries produce f32-precision results despite being
compiled from f64 source.

**Verification**: barraCuda can validate this via the existing
`f64_computation_probe()` in `test_pool.rs` — dispatch
`f64(3.0) * f64(2.0) + f64(1.0)` through a coralReef-compiled binary and
verify the result is `7.0` to f64 precision.

---

## 2. P0 — coralDriver Compute Submission

**What**: The `coral-driver` crate has DRM ioctl scaffolding but needs
hardware-validated compute submission on real GPUs (RTX 3090, RX 6950 XT,
Titan V).

**Why it matters**: barraCuda has compiled native binaries cached in
`coral_compiler.rs` (`NATIVE_BINARY_CACHE`) but no dispatch path. The
sovereign pipeline is: `WGSL → coralReef IPC → native binary → cache →
coralDriver dispatch`. Without coralDriver, cached binaries are unused.

**Integration point**: barraCuda's `compile_shader_f64` will check the cache
first, and when coralDriver is available, submit the sovereign binary
directly instead of falling through to wgpu/naga:

```
Current:   WGSL → naga → SPIR-V → wgpu → driver
Sovereign: WGSL → coralReef → native binary → coralDriver → hardware
Fallback:  WGSL → DF64 rewrite → naga → SPIR-V → wgpu → driver
```

---

## 3. P1 — Uniform Buffer Bindings

**What**: coralReef does not yet support `var<uniform>` bindings in compute
shader prologues. barraCuda's `sum_reduce_f64.wgsl` uses a uniform for the
workgroup count parameter.

**Options**:
- **coralReef evolves**: Add uniform binding support in the compute prologue
  encoder. This is the preferred path — it maintains shader compatibility.
- **barraCuda adapts**: We can switch to a storage buffer for the parameter,
  but this reduces shader portability across the wgpu and sovereign paths.

**Recommendation**: coralReef should add uniform support. The binding layout
is straightforward: `@group(0) @binding(N) var<uniform> params: ParamsStruct`.

---

## 4. P1 — BAR.SYNC Encoding

**What**: `nvdisasm` reports undefined opex table value 0x10 for
`TABLES_opex_0` in barrier synchronisation instructions. The Volta SM70
barrier count field encoding differs from later architectures.

**Where to look**: Volta compute manuals, SASS ISA references. The
`BAR.SYNC` instruction uses a different encoding than Ada/Ampere for the
thread count predicate.

---

## 5. P2 — Loop Instruction Scheduling

**What**: Loop back-edges trigger `opt_instr_sched_prepass` assertion.
Unrolled shaders compile correctly, but loop-based reduction shaders (which
are more memory-efficient for large reductions) fail.

**Impact**: barraCuda's reduction pipeline currently uses unrolled shaders
through coralReef and loop-based shaders through wgpu/naga. Fixing loop
scheduling would allow all shader variants to go through the sovereign path.

---

## 6. IPC Contract — What barraCuda Provides

barraCuda's `CoralCompiler` client (`device/coral_compiler.rs`) uses:

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| Health | `compiler.health` | `()` | `HealthResponse` |
| Compile | `compiler.compile` | `CompileRequest` | `CompileResponse` |
| Archs | `compiler.supported_archs` | `()` | `Vec<String>` |

**Discovery**: barraCuda probes for coralReef via:
1. `BARRACUDA_SHADER_COMPILER_ADDR` / `BARRACUDA_SHADER_COMPILER_PORT` env
2. XDG runtime manifest: `$XDG_RUNTIME_DIR/ecoPrimals/coralReef*.json`
3. Default fallback: `127.0.0.1:9741`

**Caching**: Native binaries are cached by `(blake3_hash(shader_source), arch)`.
The cache persists for the process lifetime. Re-compilation is triggered only
on `CoralCompiler::reset()`.

**Test harness integration**: barraCuda's `CoralProbe` (`test_harness.rs`)
calls `probe_health()` once per process and caches the result. 3000+ tests
do not each make an IPC call. The `with_coral()` gate runs closures only
when coralReef is reachable.

---

## 7. Validation Corpus

barraCuda provides 700+ WGSL shaders across 5 springs as a validation corpus:
- 81 shaders from hotSpring (lattice QCD, MD, spectral)
- 6 shaders from airSpring (hydrology, agriculture)
- Cross-spring shaders from neuralSpring and groundSpring
- f64, DF64, f32, f16 precision tiers

The sovereign validation harness (`shaders/sovereign/validation_harness.rs`)
traverses all `.wgsl` files and runs them through naga parser → sovereign
optimizer → validator without GPU. coralReef should use these shaders for
regression testing.

---

## 8. AMD Backend Notes

barraCuda's `GpuDriverProfile` detects AMD RADV/ACO and routes to
appropriate workgroup sizes. If coralReef's AMD backend (RDNA2 GFX1030) is
hardware-validated, barraCuda can add a `CoralBackend::Amd` dispatch path
alongside the NVIDIA path. The IPC contract does not need to change — the
`arch` field in `CompileRequest` already supports any target string.

---

## 9. What barraCuda Has Already Done

| Item | Status |
|------|--------|
| `CoralCompiler` IPC client | Production |
| `probe_health()` public API | Production |
| `CoralProbe` in test harness | Production |
| `Fp64Strategy::Sovereign` variant | Production |
| Native binary cache (`NATIVE_BINARY_CACHE`) | Production |
| `arch_to_coral()` mapping (GpuArch → sm_xx) | Production |
| `with_coral()` test gate | Production |
| Tier 5 coralreef test tier in `test-tiered.sh` | Production |
| XDG runtime manifest discovery | Production |
| Graceful `try_current()` tokio guard | Production |

---

*barraCuda is ready for sovereign dispatch. The compile path works. The
cache works. The IPC works. The test harness probes and gates correctly.
What remains is coralReef fixing f64 instruction emission and hardening
coralDriver for real GPU submission.*
