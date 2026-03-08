# coralReef: df64 Preamble + Fp64Strategy — Phase 1 Complete

**Date**: March 8, 2026  
**Primal**: coralReef (compiler)  
**Depends on**: barraCuda (precision strategy), all consumer springs  
**Status**: Phase 1 implemented, 5 df64 tests passing  

---

## What Changed

### 1. `Fp64Strategy` Enum (replaces boolean)

`CompileOptions` now has a three-tier `fp64_strategy` field:

```rust
pub enum Fp64Strategy {
    Native,      // Hardware f64 + software transcendental lowering (default)
    DoubleFloat, // Lower to df64 f32-pair arithmetic (~48 bits)
    F32Only,     // Truncate to f32 (lossy, visualization only)
}
```

The old `fp64_software: bool` field still exists for backward compatibility.

### 2. Auto-Prepend df64 Preamble

When `Fp64Strategy::DoubleFloat` is selected **or** when the WGSL source uses
`Df64` / `df64_*` functions, coralReef automatically prepends its built-in
df64 preamble before naga parsing. Zero caller overhead.

### 3. `enable f64;` Directive Stripping

WGSL `enable f64;` directives are automatically stripped — naga handles f64
natively. Shaders written with `enable f64;` (like airSpring's hydrology ops)
compile without modification.

### 4. Built-in df64 Preamble

`crates/coral-reef/src/df64_preamble.wgsl` provides:

| Category | Functions |
|----------|-----------|
| **Struct** | `Df64 { hi: f32, lo: f32 }` |
| **Constructors** | `df64_zero`, `df64_from_f32`, `df64_from_f64`, `df64_to_f64` |
| **Core** | `two_sum` (Knuth), `fast_two_sum`, `two_prod` (Dekker via FMA) |
| **Arithmetic** | `df64_add`, `df64_sub`, `df64_mul`, `df64_div`, `df64_neg` |
| **Transcendentals** | `exp_df64`, `sqrt_df64`, `tanh_df64` |

All operations use f32 hardware only — works on every GPU.

---

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| `corpus_gelu_f64` | **PASS** | df64 GELU activation, preamble auto-prepended |
| `corpus_layer_norm_f64` | **PASS** | df64 layer normalization |
| `corpus_softmax_f64` | **PASS** | df64 softmax (pass 2 of 3-pass SDPA) |
| `corpus_sdpa_scores_f64` | **PASS** | df64 QK^T/sqrt(d_k) (pass 1 of 3-pass SDPA) |
| `corpus_kl_divergence_f64` | **PASS** | Fixed `shared` → `wg_scratch` (WGSL reserved keyword) |
| `corpus_sigmoid_f64` | **PASS** | Fixed Iteration 20 — SSA dominance repair via `fix_entry_live_in` |
| `corpus_local_elementwise_f64` | IGNORED | Math::Acos not yet implemented |

**Totals**: 991 tests — 960 passing, 31 ignored, 0 failed

---

## How barraCuda Should Use This

### Immediate (Today)

Send df64 WGSL to coralReef as before — it just works:

```json
{
  "method": "shader.compile.wgsl",
  "params": {
    "source": "// df64 shader using Df64, df64_add, etc.\n...",
    "arch": "sm86"
  }
}
```

coralReef detects `Df64` / `df64_*` usage and auto-prepends the preamble.

### Preferred (Going Forward)

Specify the strategy explicitly:

```json
{
  "method": "shader.compile.wgsl",
  "params": {
    "source": "...",
    "arch": "sm86",
    "fp64_strategy": "double_float"
  }
}
```

### What barraCuda No Longer Needs To Do

- **No need to inline df64_core.wgsl** — coralReef has it built-in
- **No need to manage preamble concatenation** — automatic
- **No need to maintain transcendental implementations** — coralReef owns them

---

## How Springs Should Wire (Titan V / RTX 3090)

### For df64 shaders (GELU, softmax, layer_norm, SDPA scores)

```rust
use coral_reef::{compile_wgsl, CompileOptions, GpuTarget, NvArch, Fp64Strategy};

let binary = compile_wgsl(df64_wgsl_source, &CompileOptions {
    target: GpuTarget::Nvidia(NvArch::Sm70),  // Titan V
    fp64_strategy: Fp64Strategy::DoubleFloat,
    ..Default::default()
})?;
```

The Fp64Strategy hint is optional — if the source uses df64 types, the preamble
is prepended regardless. But explicit is better.

### For native f64 shaders (BCS, Mermin, VACF)

```rust
let binary = compile_wgsl(f64_wgsl_source, &CompileOptions {
    target: GpuTarget::Nvidia(NvArch::Sm70),
    fp64_strategy: Fp64Strategy::Native,
    ..Default::default()
})?;
```

---

## Remaining Gaps (Phase 2 Territory)

| Gap | Impact | Fix |
|-----|--------|-----|
| ~~`sigmoid_f64` RA failure~~ | ~~Branched exp_df64~~ | **Fixed Iteration 20** — SSA dominance repair |
| ~~`switch` statement~~ | ~~`local_elementwise_f64`~~ | **Fixed Iteration 14** — Statement::Switch lowering |
| IR-level df64 lowering | barraCuda still needs 2 shader variants | `lower_f64_to_df64.rs` pass |
| Adaptive precision | Auto-select tier per-operation | Numerical analysis in compiler |

---

## Architecture Summary

```
barraCuda                          coralReef
─────────                          ─────────
Writes math (WGSL)         →       Compiles math to GPU binary
Chooses precision tier     →       Implements precision tier
Sends Fp64Strategy hint    →       Owns df64 preamble + lowering
                                   Owns `enable f64;` handling
                                   Owns transcendental polynomials
```

**Principle**: barraCuda writes the math. coralReef compiles the math.
The precision tier is the interface between them.
