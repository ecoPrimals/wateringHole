# Cross-Spring Handoff: DF64-Compute NAK Pipeline — Sovereign Solution Required

**Date**: March 5, 2026
**From**: hotSpring
**To**: barraCuda, toadStool
**Type**: HANDOFF — Deep Debt Resolution
**Priority**: P1 (blocks consumer GPU competitive benchmarks)

---

## Summary

hotSpring's `compile_df64_compute_shader()` (a local reimplementation of DF64
rewriting) **fails pipeline validation on NVK/NAK** for all Yukawa force
shaders. The RTX 3090 produces zero forces, zero energy — silent physics
failure that passes validation harnesses (0% drift on 0.0 values).

**Root cause**: hotSpring bypasses barraCuda's proper shader compilation
pipeline and uses its own naga-guided f64→DF64 rewrite, which produces
invalid SPIR-V/WGSL that NAK rejects.

**Immediate fix applied**: Disabled `use_df64_compute` for NVK. All NVK
shaders now route through barraCuda's `compile_shader_f64()` polyfill
pipeline (native f64 + exp/log/sin/cos polyfills). This is **correct but
slow** (1/64 f64 rate on consumer Ampere/Ada GPUs).

**What's needed**: barraCuda's `compile_shader_universal(Precision::Df64)`
pipeline working on NVK for the Yukawa force kernel. This would give consumer
GPUs 10–30× speedup by using FP32 cores at 1:1 rate instead of FP64 at 1:64.

---

## The Debt

hotSpring has its own `compile_df64_compute_shader()` in `barracuda/src/gpu/mod.rs`
(lines 730–816) that duplicates what barraCuda's `compile_shader_universal(Df64)`
does, but incorrectly:

### hotSpring's broken path (DISABLED)

```
WGSL (f64) → strip enable f64 → expand compound assignments → replace abs()
→ replace polyfill transcendentals → naga-guided infix rewrite (f64 ops → DF64 bridge)
→ inject DF64 core/transcendental libraries → compile_shader()
```

**Failure mode**: NAK rejects the resulting shader module at pipeline creation.
The naga rewrite produces WGSL that parses but generates invalid SPIR-V when
compiled through naga→NAK. The `df64_gt`, `df64_lt` bridge functions and
compound assignment expansions produce incorrect naga IR spans.

### barraCuda's proper path (SHOULD BE USED)

```
compile_shader_universal(source, Precision::Df64, label)
  → Layer 1: rewrite_f64_infix_full() (naga-guided, robust)
  → Layer 2: downcast_f64_to_df64() (text-based fallback)
  → compile_shader_df64() (prepends df64_core + df64_transcendentals)
  → sovereign SPIR-V or WGSL fallback
```

barraCuda's two-layer approach is more robust: naga-guided rewrite first,
with text-based downcast as fallback. hotSpring only has the naga path with
no fallback.

---

## Current State

### What works (after today's fix)

| GPU | Path | Performance | Precision | Status |
|-----|------|-------------|-----------|--------|
| Titan V (NVK) | Native f64 | Fast (1:2 rate) | 52-bit | ✅ Working |
| RTX 3090 (NVK) | Native f64 + polyfills | Slow (1:64 rate) | 52-bit | ✅ Working |
| RTX 3090 (NVK) | DF64-compute | Fast (1:1 FP32) | 48-bit | ❌ Pipeline fails |

### Validation evidence

RTX 3090 with native f64 polyfill path (today's run):
```
[pipeline:RTX 3090 (NVK GA102)] yukawa_force_f64: pipeline valid (21.13ms)
Equilibration: 171.27s (5000 steps, 34.25ms/step)
Production step 14999: E=2295.555 (stable to 0.01 over 15K steps)
```

RTX 3090 with DF64-compute path (before fix):
```
[pipeline:RTX 3090 (NVK GA102)] yukawa_force_f64: *** PIPELINE ERROR: Validation Error
ShaderModule with 'yukawa_force_f64' label is invalid
→ All subsequent steps: KE=0, PE=0, E=0 (silent failure)
```

---

## Action Items for barraCuda

### P1: Enable compile_shader_universal(Df64) for hotSpring Yukawa shaders

1. **Test case**: `barracuda/src/md/shaders/yukawa_force_f64.wgsl` on NVK
   - Contains: `sqrt()`, `exp()`, `round()` on f64 values
   - Contains: `for` loop with `continue`, compound `+=`/`-=`
   - 4 storage buffers: positions, forces, pe_buf, params (all `array<f64>`)

2. **Reproduce**: Run `sarkas_gpu --full` on NVK with `use_df64_compute = true`
   in `gpu/mod.rs` line 264. Pipeline creation fails for `yukawa_force_f64`.

3. **Expected fix**: Ensure `compile_shader_universal(source, Precision::Df64, label)`
   produces a valid pipeline for this shader on NVK. The two-layer approach
   should handle it — if naga rewrite fails, text-based downcast should work.

4. **Bonus**: If the DF64 pipeline validates, measure steps/s for the Yukawa
   force kernel at N=2000. Expected: 300–900 steps/s (vs 29 steps/s native f64).
   This is the headline number for faculty review.

### P2: hotSpring should use compile_shader_universal instead of local DF64 code

Once the barraCuda Df64 pipeline works on NVK:

1. Replace `compile_df64_compute_shader()` in `gpu/mod.rs` with a call to
   `self.wgpu_device.compile_shader_universal(source, Precision::Df64, label)`
2. Remove the local naga rewrite code (lines 730–816)
3. Remove `expand_compound_assignments()`, `split_top_level_semicolons()`,
   `try_expand_compound()` — these are debt from the manual rewrite approach
4. Remove `use_df64_compute` field from `GpuF64` struct

### P3: Add Yukawa force to barraCuda's NVK CI/test matrix

The Yukawa force shader is a good stress test for DF64 because it has:
- Mixed f64 builtins (sqrt, exp, round)
- Conditional branches inside loops
- Compound assignments (+=, -=)
- 4-buffer binding layout

---

## Test Shaders for barraCuda NAK Validation

Priority order (simplest to most complex):

1. `yukawa_force_f64.wgsl` — single kernel, all-pairs, PBC
2. `yukawa_force_celllist_f64.wgsl` — cell-list variant (more complex indexing)
3. `yukawa_force_celllist_v2_f64.wgsl` — indirect cell-list (most complex)
4. Lattice QCD: `cg_kernels_f64.wgsl` — CG solver (multiple entry points)

---

## Files Changed in hotSpring

- `barracuda/src/gpu/mod.rs`: Disabled `use_df64_compute` for NVK
  (set `needs_df64 = false` unconditionally, was `is_nvk && !high_f64_throughput`)
- No changes to barraCuda crate

---

## Performance Target

| Path | Steps/s (N=2000) | Precision | FP units used |
|------|-------------------|-----------|---------------|
| Native f64 (current) | ~29 | 52-bit mantissa | FP64 at 1/64 rate |
| DF64 (target) | ~300–900 | 48-bit mantissa | FP32 at 1/1 rate |
| Kokkos-CUDA (reference) | TBD (needs proprietary driver) | 64-bit | CUDA cores |

The DF64 path is the competitive path for consumer GPUs. On datacenter GPUs
(Titan V, V100, A100), native f64 at 1:2 rate is already fast enough.

---

*Math is universal. Precision is silicon. The sovereign compiler decides.*
