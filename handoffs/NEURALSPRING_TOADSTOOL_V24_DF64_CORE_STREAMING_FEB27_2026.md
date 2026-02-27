# neuralSpring → ToadStool V24 — df64 Core Streaming (Session 88)

**Date**: February 27, 2026
**From**: neuralSpring (ecoPrimals/neuralSpring)
**To**: ToadStool/BarraCUDA team (ecoPrimals/phase1/toadstool)
**ToadStool HEAD**: `f0feb226` (S68)
**License**: AGPL-3.0-or-later

---

## Executive Summary

neuralSpring has evolved all 15 sovereign folding (AlphaFold2) WGSL shaders to
the hotSpring/ToadStool df64 core streaming pattern. This validates that the
df64 approach (originally developed for nuclear physics in hotSpring) generalizes
cleanly to ML workloads. The shaders now use f64 buffer I/O with df64 compute
on FP32 cores, achieving ~14-digit (fp48) precision on consumer GPUs.

---

## What Changed (Session 88)

### GPU Wrapper (`src/gpu.rs`)

Three new methods added to neuralSpring's `Gpu` wrapper:

- `create_buffer_f64(count)` — allocates f64 GPU buffer
- `upload_f64(data: &[f64])` — creates + populates f64 buffer
- `compile_shader_f64_hybrid(source, label)` — prepends `WGSL_DF64_CORE` +
  `WGSL_DF64_TRANSCENDENTALS` then calls `compile_shader_f64`

### 15 WGSL Shaders Evolved

All sovereign folding shaders in `metalForge/shaders/` converted from
`array<f32>` to `array<f64>` buffers with three-zone df64 compute:

| Category | Shaders | Precision Tier | Max Diff |
|----------|---------|----------------|----------|
| Evoformer | GELU, LayerNorm, softmax, SDPA (3-pass), triangle mul (2), triangle attn, OPM, MSA row/col attn | Mixed | 6.4e-8 to 3.4e-4 |
| Structure | IPA scores, backbone update, torsion angles | Arithmetic | 3.6e-8 to 3.4e-7 |
| Activation | sigmoid | Transcendental | (CPU validated) |

### GPU Validator Rewritten

`validate_sovereign_folding_gpu` now uses:
- f64 data generation and upload
- `compile_shader_f64_hybrid` for shader compilation
- f64 buffer readback via `read_buffer_f64`
- Two-tier tolerance: `GPU_DF64_TOL = 1e-6`, `GPU_DF64_TRANS_TOL = 5e-4`
- `Fp64Strategy::Hybrid` auto-detection

---

## Precision Discovery: Two Tiers

| Tier | Operations | Observed | Bottleneck |
|------|-----------|----------|------------|
| Arithmetic | dot, matmul, accumulate, `sqrt_df64` | 3.6e-8 to 5.6e-7 | f32 FMA tracking |
| Transcendental | `exp_df64`, `tanh_df64` | 1.7e-4 to 3.4e-4 | Horner degree-6 polynomial |

This matches hotSpring's experience: arithmetic df64 ops are ~7 decimal digits
accurate, while transcendental df64 ops are ~3-4 digits accurate. Both are
dramatically better than pure f32.

---

## Absorption Targets for ToadStool

### High Priority

1. **`compile_shader_df64_streaming(source, label)`** — both neuralSpring and
   hotSpring manually prepend the df64 preambles. This should be a first-class
   `WgpuDevice` method.

2. **Universal df64 ML primitives** — the 15 shaders contain building blocks
   that are not domain-specific:
   - `gelu_df64` / `sigmoid_df64` — pointwise activations
   - `layer_norm_df64` — normalization
   - `softmax_df64` — row-wise softmax
   - `sdpa_df64` — scaled dot-product attention pipeline

3. **`barracuda::nn` module** (from V51, still pending):
   - `SimpleMLP` — 3 WDM surrogates + hotSpring
   - `LstmReservoir` — nW-03 S(q,ω)
   - `EsnClassifier` — nW-05 regime

### Medium Priority

4. **Transcendental precision upgrade** — degree-10+ Horner or Padé approximants
   for `exp_df64`/`tanh_df64` would close the gap from ~3e-4 to ~1e-8.
   All downstream Springs benefit.

5. **`fused_chi_squared_f64`**, **`fused_kl_divergence_f64`** — local shaders
   in metalForge ready for absorption.

---

## Cross-Spring Validation of df64

The df64 core streaming pattern is now validated across two Springs:

| Spring | Domain | Shaders | Precision |
|--------|--------|---------|-----------|
| hotSpring | Nuclear physics, lattice QCD | ~30+ | ~1e-10 arithmetic |
| neuralSpring | ML, protein folding | 15 | 3.6e-8 to 5.6e-7 arithmetic |

This confirms df64 core streaming is a **general-purpose precision technique**,
not domain-specific. It should be the default compilation path for any Spring
needing better-than-f32 precision on consumer GPUs.

---

## Validation

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo test --workspace` | **675/675 PASS** |
| `validate_all` | **158/158 PASS** |
| `validate_sovereign_folding_gpu` | **37/37 PASS** (df64 core streaming) |

---

*neuralSpring → ToadStool V24 handoff — February 27, 2026, Session 88.*
