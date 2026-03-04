# wetSpring → toadStool / barracuda — V61 Barracuda Evolution + Absorption Handoff

**Date:** February 27, 2026
**From:** wetSpring
**To:** toadStool / barracuda core team
**Covers:** V61 barracuda evolution review + absorption candidates + field genomics learnings
**ToadStool Pin:** S68 (`f0feb226`)
**License:** AGPL-3.0-only

---

## Executive Summary

- **79 ToadStool primitives** consumed (barracuda always-on, zero fallback code)
- **0 local WGSL** shaders (fully lean — all 8 original bio shaders absorbed)
- **0 local derivative/regression** math (delegated to upstream)
- **1 passthrough** remaining (`reconciliation_gpu` — needs `BatchReconcileGpu`)
- **3 absorption candidates** ready: ESN reservoir, NPU inference bridge, validator pattern
- **`io::nanopore`** module operational (V61) — new streaming I/O pattern for field genomics
- **39/39 three-tier** paper controls confirmed (CPU + GPU + metalForge, all open data)

---

## Absorption Candidates (Ready Now)

### 1. `bio::esn` → `barracuda::ml::esn`

Echo State Network reservoir computing — used by 4+ Springs (wetSpring NPU,
hotSpring precision, neuralSpring ML, airSpring IoT). Generic reservoir pattern:
sparse reservoir generation → Cholesky ridge readout → single-step inference.

**API surface:**
- `EsnConfig` (reservoir_size, spectral_radius, input_scaling, leak_rate, ridge_alpha)
- `Esn::new(config)` → sparse reservoir with controlled spectral radius
- `Esn::train(inputs, targets)` → Cholesky ridge regression readout
- `Esn::infer(input)` → reservoir update + readout
- `w_in()`, `w_res()`, `w_out()`, `w_out_mut()`, `config()` — raw weight access

**Validation:** 896 lib tests, Exp114/194/196c.

### 2. NPU Inference Bridge → `barracuda::npu`

Standard int8 inference via DMA to AKD1000:
- `npu_infer_i8(device, input_i8) → output_i8`
- `load_reservoir_weights(device, weights_f64) → SRAM`
- `load_readout_weights(device, weights_f64) → mutation`
- `npu_batch_infer(device, batch_i8) → NpuBatchResult`
- `quantize_community_profile_int8(profile_f64) → profile_i8`

**Validation:** 60 checks on real AKD1000 (Exp193-195), 13 quantization (Exp196c).

### 3. Validator Harness Pattern

hotSpring and wetSpring converged on same pattern: named tolerances, provenance
headers, `check(name, got, expected, tol)` with human-readable output.
Upstream `ValidationHarness` exists; pattern should be standardized.

---

## Three-Tier Paper Controls

| Track | Papers | CPU | GPU | metalForge | All Open Data |
|-------|:------:|:---:|:---:|:----------:|:------------:|
| Track 1 (Ecology) | 10 | 10/10 | 10/10 | 10/10 | Yes |
| Track 1b (Phylogenetics) | 5 | 5/5 | 5/5 | 5/5 | Yes |
| Track 1c (Metagenomics) | 6 | 6/6 | 6/6 | 6/6 | Yes |
| Track 2 (PFAS/LC-MS) | 4 | 4/4 | 4/4 | 4/4 | Yes |
| Track 3 (Drug repurposing) | 5 | 5/5 | 5/5 | 5/5 | Yes |
| Track 4 (Soil QS) | 9 | 9/9 | 9/9 | 9/9 | Yes |
| **Total** | **39** | **39/39** | **39/39** | **39/39** | **Yes** |

Data sources: NCBI SRA, Zenodo, EPA, MBL, MG-RAST, Figshare, OSF, MassBank,
repoDB, published model equations, published soil metrics.

---

## Key Learnings for ToadStool Evolution

1. **Int8 quantization preserves classification** — affine quantization loses
   magnitude precision but preserves ordering. Consider `barracuda::quantize`
   module for standardized int8/int4 quantization.

2. **Streaming I/O is mandatory for field** — iterator-based parsing with
   reusable buffers (not whole-file deserialization). Pattern: `XyzIter::open(path)`
   yields `Result<XyzRecord>` lazily.

3. **Named tolerances prevent drift** — 92 constants with scientific justification
   eliminated all ad-hoc magic numbers. Cross-spring standard recommended.

4. **Power-budget-aware routing** — metalForge should consider power as a
   first-class dispatch constraint alongside latency and accuracy for field
   deployment (10 mW NPU vs 60W GPU vs 5W CPU).

5. **Write → Absorb → Lean cycle accelerates** — early absorptions took weeks,
   later ones took hours. ToadStool's `generate_shader()` and `Precision` enum
   made absorption nearly mechanical.

---

## Supersedes

- `WETSPRING_TOADSTOOL_V27_EVOLUTION_FEB24_2026.md` (archived)

## Full Details

See `wetSpring/wateringHole/handoffs/WETSPRING_TOADSTOOL_V61_NANOPORE_FIELD_GENOMICS_HANDOFF_FEB27_2026.md`
for the comprehensive handoff with hardware matrix, barracuda module inventory,
and detailed absorption API specifications.
