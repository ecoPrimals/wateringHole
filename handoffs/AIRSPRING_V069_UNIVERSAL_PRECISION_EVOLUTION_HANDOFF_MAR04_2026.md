# airSpring V0.6.9 — Universal Precision Evolution Handoff

**Date**: March 4, 2026  
**Spring**: airSpring (ecology/agriculture validation)  
**Session**: Cross-Spring Evolution + Universal Precision Promotion  
**Dependencies**: BarraCuda 0.3.1 (standalone), ToadStool (dispatch only)

---

## Summary

Promoted airSpring's 6 local GPU shaders from fixed f32 to **f64-canonical universal
precision** via BarraCuda's `compile_shader_universal()` architecture. This is the
flagship evolution: "math is universal, precision is silicon."

### What Changed

| Component | Before (V0.6.8) | After (V0.6.9) |
|-----------|-----------------|-----------------|
| Shader source | `local_elementwise.wgsl` (f32) | `local_elementwise_f64.wgsl` (f64 canonical) |
| Compilation | `create_shader_module` (direct) | `compile_shader_universal` (BarraCuda) |
| Precision | Fixed f32 | Auto: F32 on consumer, F64 on pro GPUs |
| Buffer handling | f64→f32→GPU→f32→f64 | Precision-aware (f64 native or f32 downcast) |
| Test tolerances | Fixed ~1e-3 | Precision-adaptive (1e-10 for F64, 1e-3 for F32) |
| Provenance | Undocumented | Cross-spring provenance in shader headers |

### Files Modified (~15 files)

**New files:**
- `src/shaders/local_elementwise_f64.wgsl` — f64 canonical shader (6 ops)
- `src/bin/validate_cross_spring_evolution.rs` — Exp 078 benchmark binary

**Evolved files:**
- `src/gpu/local_dispatch.rs` — precision-aware compilation + dispatch
- `src/gpu/evolution_gaps.rs` — Tier A entries updated
- `src/gpu/mod.rs` — module table updated
- `src/gpu/runoff.rs` — doc-comments updated
- `src/gpu/yield_response.rs` — doc-comments updated
- `src/gpu/simple_et0.rs` — doc-comments updated
- `src/shaders/local_elementwise.wgsl` — marked as LEGACY

---

## Cross-Spring Shader Provenance

The universal precision architecture was evolved across all Springs:

| Component | Origin Spring | Session | What It Enables |
|-----------|---------------|---------|-----------------|
| `math_f64.wgsl` (exp, log, pow, sin) | hotSpring | S54 | Full f64 precision for all shaders |
| `df64_core.wgsl` + transcendentals | hotSpring | S58-S71 | ~48-bit on consumer GPUs |
| `compile_shader_universal` | neuralSpring | S68 | One source → any precision |
| `Fp64Strategy` / `GpuDriverProfile` | hotSpring | S58 | Auto precision per hardware |
| `batched_elementwise_f64.wgsl` | airSpring+wetSpring | S42-S79 | 14 domain ops at f64 |
| `diversity_fusion_f64.wgsl` | wetSpring | S70 | Shannon+Simpson GPU |
| `mc_et0_propagate_f64.wgsl` | groundSpring | S64 | MC uncertainty GPU kernel |
| `brent_f64.wgsl` | neuralSpring | S83 | Root-finding (VG inverse) |
| `local_elementwise_f64.wgsl` | airSpring | V0.6.9 | 6 agri ops, f64 canonical |

---

## Architecture

```
f64 canonical WGSL source (math is universal)
       │
       ▼
compile_shader_universal(source, precision, label)
       │
 ┌─────┼─────┐
 F64   F32   Df64
 │     │     │
 Titan RTX   Arc
 V     4070  A770
```

**Key design decision**: `LocalElementwise::new()` defaults to `Precision::F32` because:
1. Agricultural science (FAO-56) only needs ~6 significant digits; f32 gives ~7
2. f64 compute shaders are unreliable on some GPUs that advertise `SHADER_F64`
   but produce zeros (discovered during this session via diagnostic testing)
3. The f64 canonical source provides code clarity and future-proofing
4. `with_precision(device, Precision::F64)` available for verified pro GPUs

**WGSL directive note**: The `enable f64;` directive in `local_elementwise_f64.wgsl`
must be stripped before passing to `compile_shader_universal` for non-F64 paths,
because `downcast_f64_to_f32` doesn't strip WGSL directives. The F64 compilation
path (`compile_shader_f64`) handles this internally.

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt` | PASS |
| `cargo clippy --all-targets --all-features -- -W pedantic -W nursery -D warnings` | 0 warnings |
| `cargo test --lib` | **852 passed**, 0 failed |
| `cargo test --tests` | **1133 passed**, 0 failed |
| `cargo doc --no-deps` | PASS |

---

## Discovery: f64 Compute Shader Reliability

During diagnostic testing, we discovered that this GPU (`has_f64_shaders: true`)
produces all-zero output from f64 compute shaders — both via `compile_shader_f64`
and raw `create_shader_module` with `enable f64;`. The f32 downcast path works
perfectly. This confirms the value of BarraCuda's universal precision architecture:
write f64-canonical, compile to whatever the hardware actually supports.

This finding should be reported upstream to BarraCuda for the probe cache to
account for (similar to groundSpring V37's NVK discovery).

---

## Next Steps

1. **BarraCuda ops 14-19**: Absorb the 6 local ops into `batched_elementwise_f64`
   for cross-Spring reuse (wetSpring could use SCS-CN, neuralSpring could use ET₀)
2. **Df64 path**: Wire `Precision::Df64` for consumer GPUs that benefit from
   ~48-bit mantissa (beyond what the f32 path provides)
3. **Report f64 compute shader issue**: Upstream to BarraCuda probe cache
4. **Wire `BatchedNelderMeadGpu`**: GPU-resident isotherm fitting
5. **Wire `BatchedStatefulF64`**: GPU-resident water balance (eliminates per-day readback)
