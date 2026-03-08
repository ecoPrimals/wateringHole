# coralReef ↔ barraCuda: Precision Architecture — Who Owns What

**Date**: March 8, 2026
**Primals**: coralReef (compiler), barraCuda (math dispatch)
**Subject**: Three-tier precision model ownership and evolution path

---

## The Three Tiers

| Tier | Mantissa | Implementation | Throughput (RTX 3090) | When to Use |
|------|----------|---------------|----------------------|-------------|
| **f32** | 24 bits | Native f32 cores | ~29,770 GFLOPS | Visualization, inference, tolerant workloads |
| **df64** | ~48 bits | Pair of f32 (Dekker/Knuth) | ~7,000–10,000 GFLOPS | Science that needs >f32 but not full f64 |
| **f64** | 52 bits | Native f64 hardware | ~556 GFLOPS (consumer) / ~7,800 GFLOPS (Titan V) | Gold-standard reference, HPC hardware |

df64 is the "fp48" sweet spot: 12–18x faster than native f64 on consumer GPUs,
while delivering ~14 digits of precision (vs f32's ~7 and f64's ~16).

---

## Current Ownership

```
barraCuda                        coralReef
─────────                        ─────────
Owns: WHAT math to compute       Owns: HOW to compile to hardware
Owns: WHICH precision tier       Owns: f64 transcendental lowering
Generates: 3 WGSL variants       Compiles: whatever WGSL it receives
  - f32 shader                     - f32 → native f32 ops (done)
  - f64 shader                     - f64 → DFMA + polynomial lower (done)
  - df64 shader (preamble)         - df64 → ???
```

~~The gap: coralReef cannot compile df64 shaders.~~ **RESOLVED** (Iteration 13):
coralReef now has a built-in df64 preamble (`df64_preamble.wgsl`) that is
auto-prepended when source uses `Df64`/`df64_*`. 4 of 5 df64 tests pass
(gelu, sdpa_scores, softmax, layer_norm). sigmoid_f64 blocked by RA SSA tracking.

---

## The Right Boundary

**barraCuda owns precision STRATEGY** — it decides which tier based on:
- Scientific accuracy requirements (does this kernel need >7 digits?)
- Target hardware capabilities (`has_fast_fp64()`)
- User-specified precision policy

**coralReef owns precision IMPLEMENTATION** — it knows how to lower each tier
to the fastest possible hardware path:
- f32 → native (already done)
- f64 → native DFMA + transcendental polynomial lowering (already done)
- df64 → **coralReef should own this lowering** (not yet done)

---

## Evolution Path

### Phase 1 ~~(Near-term)~~ DONE — Preamble Concatenation

**Completed March 8, 2026 (Iteration 13).**

coralReef has a built-in `df64_preamble.wgsl` with Dekker/Knuth pair arithmetic.
The `prepare_wgsl()` function auto-prepends it when source uses `Df64`/`df64_*`
or `Fp64Strategy::DoubleFloat` is selected. Also strips `enable f64;` directives.

**What was added:**
- `Fp64Strategy` enum (`Native`, `DoubleFloat`, `F32Only`) in `CompileOptions`
- `prepare_wgsl()` — auto-detects df64 usage, prepends preamble, strips `enable f64;`
- `df64_preamble.wgsl` — struct, constructors, arithmetic, transcendentals (all f32)

**What this unblocked:** 5 df64 test fixtures pass (4 of original 5 + kl_divergence).

### Phase 2 (Medium-term): IR-Level df64 Lowering

coralReef learns to lower f64 IR ops to df64 pair arithmetic at the IR level.
barraCuda generates ONE f64 shader. coralReef's pipeline decides how to implement
it based on `Fp64Strategy`:

```
  Fp64Strategy::Native       → existing lower_f64/ (DFMA/polynomial)
  Fp64Strategy::DoubleFloat  → new lower_f64_to_df64/ (Dekker/Knuth pairs)
  Fp64Strategy::F32Only      → truncate to f32 (lossy, for visualization)
```

**What to add to coralReef:**
- `Fp64Strategy` enum in `CompileOptions` (replaces boolean `fp64_software`)
- `lower_f64_to_df64.rs` pass: transforms `OpDAdd` → df64 pair add, etc.
- Algorithms: Dekker multiplication, Knuth two-sum, error-free transformation
- Each df64 op expands to 5–15 f32 instructions in IR

**What this unblocks:**
- barraCuda drops the 3-variant generation — just emits f64 WGSL
- coralReef handles precision routing internally
- df64 patterns can be optimized at IR level (CSE on error terms, register
  allocation across hi/lo pairs, dead error elimination)

**Effort:** Medium — ~500 lines of IR transforms, following the existing
`lower_f64/poly/` pattern.

### Phase 3 (Future): Adaptive Precision

coralReef's compiler analyzes each f64 operation and decides whether df64
precision is sufficient based on numerical analysis:
- Accumulations (sum reduction) → df64 is fine
- Divisions near zero → needs true f64
- Transcendentals → df64 polynomial good for most, but log near 1 needs f64

This is research-grade and depends on Phase 2 being solid.

---

## IPC Contract Evolution

### Current (Phase 1)

```json
{
  "method": "shader.compile.wgsl",
  "params": {
    "source": "<WGSL with df64 preamble inlined>",
    "arch": "sm86",
    "fp64_software": true
  }
}
```

barraCuda sends pre-baked df64 WGSL. coralReef compiles it as f32 struct ops.

### Target (Phase 2)

```json
{
  "method": "shader.compile.wgsl",
  "params": {
    "source": "<clean f64 WGSL — one version>",
    "arch": "sm86",
    "fp64_strategy": "double_float"
  }
}
```

barraCuda sends one f64 shader. coralReef handles the lowering.

---

## What barraCuda Should Do

1. **Keep generating df64 WGSL for now** (Phase 1 compatibility)
2. **Always also generate the clean f64 variant** (needed for Phase 2)
3. **Send `Fp64Strategy` hint in IPC** even if coralReef ignores it initially
4. **Do NOT inline coralReef internals** — barraCuda should not know about DFMA,
   Newton-Raphson, or polynomial coefficients. That's compiler territory.

## What coralReef Should Do

1. ~~**Phase 1 now:** Add preamble concatenation to unblock 5 tests~~ **DONE**
2. **Phase 2 next:** Implement `lower_f64_to_df64` IR pass
3. ~~**Evolve `CompileOptions`:** `fp64_software: bool` → `fp64_strategy: Fp64Strategy`~~ **DONE**
4. **Use `has_fast_fp64()`** to auto-select strategy when not specified:
   - Titan V / A100 → `Fp64Strategy::Native` (1:2 rate, true f64 is fast enough)
   - RTX 3090 / RX 6950 XT → `Fp64Strategy::DoubleFloat` (consumer cards need df64)
   - RX 7900 XTX → `Fp64Strategy::Native` (RDNA3 has decent f64)

---

## Key Principle

> **barraCuda writes the math. coralReef compiles the math.**
>
> barraCuda should never need to know about GPU ISA, register allocation,
> or instruction encoding. coralReef should never need to know about
> Bethe-Weizsacker mass formulas or GELU activation functions.
>
> The precision tier is the INTERFACE between them. barraCuda says
> "I need ~14 digits". coralReef figures out the fastest way to deliver that
> on the target hardware.

---

## df64 Algorithms for coralReef Phase 2

Reference implementations for the IR lowering pass:

### Two-Sum (Knuth)
```
fn two_sum(a: f32, b: f32) -> (f32, f32) {
    let s = a + b;
    let v = s - a;
    let err = (a - (s - v)) + (b - v);
    (s, err)
}
```
→ 6 f32 ops per df64 add

### Dekker Multiplication
```
fn two_prod(a: f32, b: f32) -> (f32, f32) {
    let p = a * b;
    let err = fma(a, b, -p);
    (p, err)
}
```
→ 2 f32 ops per df64 mul (with FMA)

### df64 Add
```
fn df64_add((ah, al): (f32, f32), (bh, bl): (f32, f32)) -> (f32, f32) {
    let (sh, sl) = two_sum(ah, bh);
    let sl = sl + al + bl;
    two_sum(sh, sl)  // renormalize
}
```
→ ~12 f32 ops

### df64 Mul
```
fn df64_mul((ah, al): (f32, f32), (bh, bl): (f32, f32)) -> (f32, f32) {
    let (ph, pl) = two_prod(ah, bh);
    let pl = pl + ah * bl + al * bh;
    two_sum(ph, pl)  // renormalize
}
```
→ ~8 f32 ops (with FMA)

These map directly to IR: `OpFAdd`, `OpFMul`, `OpFFma`, `OpFSub` — all of which
coralReef already encodes for both NVIDIA and AMD.
