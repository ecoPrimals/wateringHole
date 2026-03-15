# barraCuda v0.3.3 — Plasma Physics Absorption + Deep Debt Evolution

**Date**: March 8, 2026
**Scope**: hotSpring Chuna P43-45 shader absorption, cross-spring review, deep debt resolution
**Quality gates**: fmt clean, clippy zero warnings, 3,097/3,097 tests pass (13 ignored)

---

## Plasma Physics Absorption (hotSpring v0.6.23)

4 WGSL shaders absorbed from hotSpring's Chuna Papers 43-45 into `shaders/science/plasma/`:

| Shader | Lines | Domain | Source |
|--------|-------|--------|--------|
| `dielectric_mermin_f64.wgsl` | 194 | Mermin ε(k,ω) with plasma dispersion W(z) | Chuna P44 |
| `dielectric_multicomponent_f64.wgsl` | 161 | Multi-species Mermin dielectric | Chuna P44 |
| `bgk_relaxation_f64.wgsl` | 77 | BGK relaxation (two-pass: moments + relax) | Chuna P45 |
| `euler_hll_f64.wgsl` | 136 | 1D Euler with HLL Riemann solver | Chuna P45 |

New `PlasmaPhysics` variant added to `ShaderCategory` enum. 4 provenance records added to the cross-spring registry.

Total WGSL shaders: 712 → 716.

---

## Cross-Spring Review Findings

### neuralSpring coralForge shaders — ALREADY ABSORBED

All 18 neuralSpring metalForge shaders (15 Evoformer df64 + head_split + head_concat + swarm_nn_scores) are already present in barraCuda:
- `attention/`: triangle_mul_outgoing/incoming, triangle_attention, sdpa_scores, attention_apply, ipa_scores, msa_row/col_attention_scores, outer_product_mean
- `activation/`: gelu_f64, sigmoid_df64, softmax_f64
- `norm/`: layer_norm_f64
- `tensor/`: head_split_f64, head_concat_f64
- `misc/`: backbone_update_f64
- `bio/`: swarm_nn_scores_f64

### Spring status summary

| Spring | Version | barraCuda pin | Local WGSL | Status |
|--------|---------|---------------|------------|--------|
| wetSpring | V99 | `a898dee` | 0 (fully lean) | 166/166 |
| airSpring | v0.7.5 | `a898dee` | 0 (fully lean) | 865 tests |
| groundSpring | V100 | `a898dee` | 2 (reference only) | 936 tests |
| neuralSpring | S132 | `a898dee` | 41 (all absorbed upstream) | 218/218 |
| hotSpring | v0.6.23 | `cdd748d` | 84 (4 now absorbed) | Chuna 41/41 |

---

## Deep Debt Resolution

### Codebase Health (scan results)

| Category | Count |
|----------|-------|
| Unsafe blocks | **0** (`#![deny(unsafe_code)]`) |
| Mocks in production | **0** |
| TODO/FIXME/HACK in code | **0** |
| Production `unwrap()` in hot paths | **0** |

### Changes made

1. **Magic numbers → `eps::SAFE_DIV`**: `cosine_similarity_f64.rs` (`1e-14`) and `correlation_f64_wgsl.rs` (`1e-15`) now use `crate::tolerances::eps::SAFE_DIV`.
2. **Stale template debris**: Deleted `shaders/templates/elementwise_add.wgsl.template` (leftover from the `{{SCALAR}}` system). Empty `templates/` directory removed.
3. **Clone optimization**: `solver_state.rs` Nelder-Mead shrinkage extracts clone to local variable for clarity.

### Dependency analysis

- `half` crate retained: used for f16 weight format parsing in `shaders/quantized.rs` (GPTQ/GGUF model weights). Not related to removed `Precision::F16`.
- All other dependencies are appropriate and have no pure-Rust alternatives that would be beneficial.
- `blake3` already uses `pure` feature (no C/SIMD).

### Large files (>500 lines)

5 files over 500 lines, all within acceptable bounds:
- `precision_tests.rs` (622) — test file
- `pipeline_cache.rs` (612) — complex caching logic, well-structured
- `provenance/registry.rs` (580 → ~620 with 4 new records) — data registry
- `driver_profile/mod.rs` (567) — hardware detection, already decomposed
- `ode_generic.rs` (556) — ODE engine, well-structured

No refactoring needed — all are well-organized within their domains.

---

## API Migration Note

All springs are pinned to barraCuda `a898dee` (pre-lean-out). When they sync to HEAD:
- **hotSpring**: `compile_shader_universal(Precision::Df64)` → `compile_shader_df64()`
- **neuralSpring**: `compile_shader_universal(source, precision, None)` → `compile_shader_f64/df64()`
- **wetSpring/airSpring**: Doc-only references, no compile errors
