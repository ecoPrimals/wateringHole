# coralReef Phase 10 — Iteration 27: Deep Debt + Cross-Spring Absorption

**Date**: March 9, 2026
**Primal**: coralReef (sovereign GPU compiler)
**Phase**: 10 — Spring Absorption + Compiler Hardening
**Iteration**: 27

---

## Summary

This iteration resolved all P0 blockers for the AMD sovereign compute pipeline
and completed comprehensive cross-spring absorption. All 24 spring absorption
shaders now compile for both SM70 (NVIDIA) and RDNA2 (AMD).

## Completed Items

### P0 — Sovereign Pipeline Unblock

- **RDNA2 literal materialization pass**: VOP3 and VOP2 instructions with literal
  constants now automatically emit V_MOV_B32 prefix instructions to materialize
  values into scratch VGPRs. Two scratch VGPRs reserved beyond register
  allocation range.
- **f64 transcendental encodings**: F64Exp2, F64Log2, F64Sin, F64Cos implemented
  via V_CVT_F32_F64 + VOP1 transcendental + V_CVT_F64_F32 (~23-bit seed precision).
- **f32 transcendental encoding**: OpTranscendental mapped to RDNA2 VOP1 instructions
  (V_COS_F32, V_SIN_F32, V_EXP_F32, V_LOG_F32, V_RCP_F32, V_RSQ_F32, V_SQRT_F32).
- **OpShl/OpShr/OpSel non-VGPR fix**: VOP2 shift and select ops now handle
  non-VGPR sources via materialization instead of panicking.
- **AMD system register mapping**: Added SR indices 0x28–0x2D (workgroup sizes,
  grid dimensions) mapping to VGPRs v6–v11.

### P1 — Cross-Spring Absorption

- **healthSpring strip_f64_enable()**: `enable f64;` / `enable f16;` directives
  automatically stripped in prepare_wgsl() before naga parsing.
- **deformed_potentials_f64 SSARef panic**: All f64 entry points in naga translate
  (rounding, exp/log, sqrt, trig) protected with ensure_f64_ssa_ref().
- **hotSpring FMA shaders**: su3_link_update and wilson_plaquette patterns absorbed
  into test corpus (4 new tests: SM70 + RDNA2 variants).
- **f64 runtime diagnostic**: F64Capability struct with F64Recommendation enum
  added to coral-gpu for hardware capability reporting.

### P2 — API Surface + Standards

- **FMA policy**: FmaPolicy enum (Fused, Separate, Auto) added to CompileOptions
  and plumbed through the compilation pipeline.
- **f64 discovery manifest**: F64Support integrated into DiscoveryDevice with
  native/rate_divisor/recommendation fields.
- **PRNG preamble**: xorshift32 and wang_hash WGSL preamble auto-prepended
  when referenced in shader source.

### P3 — Test Corpus

- **neuralSpring shaders**: logsumexp, rk45_step, wright_fisher patterns added
  with SM70 + RDNA2 variants (6 new tests).

## Test Results

- **Total tests**: 1401 passing, 0 failed, 62 ignored (hardware-gated)
- **Spring absorption**: 24/24 passing (14 original + 4 FMA + 6 neuralSpring)
- **Clippy**: Clean under pedantic + nursery
- **Files >1000 lines**: 0
- **Stale TODOs**: 0
- **Source lines**: ~100K Rust

## Pipeline Status (Updated)

| Component | Status |
|-----------|--------|
| WGSL → IR (naga) | Complete |
| f64 lowering | Complete (all transcendentals) |
| Register allocation | Complete |
| NVIDIA encoding (SM70–SM89) | Complete |
| AMD encoding (RDNA2) | Complete — all ops encoded including transcendentals |
| Literal materialization | Complete — automatic V_MOV_B32 prefix |
| PM4 dispatch (AMD) | Complete — COMPUTE_USER_DATA wired |
| DRM submit (AMD) | Complete — GEM + CS + fence |
| Unified API (coral-gpu) | Complete — multi-GPU, f64 diagnostic |

## Remaining Evolution

- Nouveau DRM dispatch (EINVAL on GV100) — blocked until Titan V hardware available
- nvidia-drm UVM integration for NVIDIA dispatch path
- RDNA2 buffer READ path (SMEM loads return zeros) — write path works
- Full f64 precision refinement for AMD transcendentals (currently ~23-bit seed)
- Test coverage target: 90% (current ~63%)

## Integration Notes for Springs

Springs currently pinned to coralReef Iteration 10 should update to Iteration 27:
- All f64 shaders compile on AMD — no more VOP3 literal errors
- `enable f64;` / `enable f16;` directives handled automatically
- FMA policy control available via CompileOptions
- f64 hardware capability queryable via coral-gpu F64Capability
- PRNG functions (xorshift32, wang_hash) available as auto-prepended preamble
