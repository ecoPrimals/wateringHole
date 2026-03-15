# barraCuda v0.3.5 — Deep Debt Evolution & Precision Tiers Specification Handoff

**Date**: March 11, 2026
**From**: barraCuda
**To**: All springs, toadStool, coralReef

---

## Summary

barraCuda v0.3.5 completes two major milestones:

1. **Deep Debt Evolution Sprint** — resolves all remaining concrete debt identified
   in the comprehensive audit (magic numbers, lossy casts, formatting, license clarity).
2. **Precision Tiers Specification** — defines the full 15-tier precision ladder from
   Binary (1-bit) to DF128 (~104-bit mantissa), with WGSL pseudocode, reference test
   sources, and a 7-phase implementation roadmap.

All quality gates pass: `cargo fmt --check`, `cargo clippy -- -D warnings`,
`cargo doc --workspace --no-deps`. Zero unsafe, zero TODO, zero clippy warnings.

---

## Deep Debt Evolution Sprint

### Formatting fix
- Restored missing trailing newline in `spectral/mod.rs` — `cargo fmt --check` now
  passes clean.

### Magic number extraction
| Location | Before | After |
|----------|--------|-------|
| `dispatch/benchmark/operations.rs` | Inline `100`, `1`, `50.0`, `100.0`, `20.0`, `10.0`, `30.0` | Named constants: `SIMULATED_DISPATCH_OVERHEAD_US`, `SPEEDUP_MATMUL`, etc. |
| `esn_v2/model.rs` | Hardcoded `learning_rate = 0.01`, `.clamp(50, 1000)` | New `ESNConfig` fields: `sgd_learning_rate`, `sgd_min_iterations`, `sgd_max_iterations` with defaults |
| `staging/unidirectional.rs` | `Duration::from_secs(1)` | `DEFAULT_THROTTLE_WINDOW_SECS` constant |
| `benchmarks/mod.rs` | `Duration::from_secs(5)` | `DEFAULT_MIN_BENCH_DURATION_SECS` constant |

### Safe cast evolution
- Added `u32_from_u64()` and `u32_from_usize()` helpers in `error.rs`.
- Evolved all 4 `degree as u32` casts in RPC paths (`rpc.rs`, `ipc/methods.rs`) from
  silent truncation to `u32::try_from()` with proper error responses.
- External input (`degree: u64`) now fails gracefully instead of silently wrapping.

### License clarity
- Added copyright preamble to `LICENSE` file confirming AGPL-3.0-only intent.
- Fixed README.md references from "AGPL-3.0-or-later" to "AGPL-3.0-only".

### Documentation refresh
- Updated stale counts across root docs:
  - WGSL shaders: `716+` / `791` → `803` everywhere
  - Integration tests: `24` / `31` → `42` test files
  - Total tests: `3,100+` / `3,249` / `3,348` → `3,900+`
- Added `specs/PRECISION_TIERS_SPECIFICATION.md` to README tree and docs table.

---

## Precision Tiers Specification

Full specification at `specs/PRECISION_TIERS_SPECIFICATION.md` (967 lines).

### 15 Tiers (high to low)

| Tier | Mantissa | Implementation |
|------|----------|----------------|
| DF128 | ~104-bit | Dekker double-double on f64 base |
| QF128 | ~96-bit | Bailey quad-double on f32 base (consumer GPU compatible) |
| F64Precise | 52-bit | Native f64 with FMA fusion disabled |
| FP64 | 52-bit | Native IEEE 754 f64 |
| DF64 | ~48-bit | Dekker double-double on f32 base (existing) |
| TF32 | 10-bit | NVIDIA TensorFloat (informational) |
| FP32 | 23-bit | Native IEEE 754 f32 (existing baseline) |
| FP16 | 10-bit | IEEE 754 half-precision (SHADER_F16 native or emulated) |
| BF16 | 7-bit | Google Brain float (u32 bit manipulation) |
| FP8 E4M3 | 3-bit | Open Float Point (emulated via u32) |
| FP8 E5M2 | 2-bit | Open Float Point (emulated via u32) |
| INT8 Q8_0 | — | 32-element blocks, f16 scale (existing) |
| INT4 Q4_0 | — | 32-element blocks, f16 scale (existing) |
| INT2/Ternary | — | {−1, 0, +1} ternary packing |
| Binary | — | 1-bit XNOR + popcount |

### Implementation Roadmap (7 phases)
1. FP16 (SHADER_F16 detection + emulated fallback)
2. BF16 (ML training support)
3. DF128 (port df64_core.wgsl to f64 base + MPFR reference tables)
4. QF128 (Bailey quad-double, universal consumer GPU support)
5. FP8 (E4M3/E5M2 for inference)
6. INT2/Binary (extreme quantization)
7. K-quant (Q2_K–Q6_K super-block formats, GGML parity)

### Integration Points
- Extends `Precision` enum (shaders), `PrecisionTier` enum (device), `DType`, `QuantType`
- Extends `op_preamble` system for per-tier shader injection
- Extends `PrecisionBrain` for automatic tier routing
- Reference tests: MPFR, `half` crate, GGML, IEEE 754 test vectors

---

## Current State

| Metric | Value |
|--------|-------|
| Version | 0.3.5 |
| WGSL shaders | 803 |
| Rust source files | 1,060+ |
| Total tests | 3,900+ |
| Integration test files | 42 |
| Clippy warnings | 0 |
| Unsafe blocks | 0 |
| TODO/FIXME in code | 0 |
| License | AGPL-3.0-only |
| Grade | A+ |

---

## What's Next

- **Precision Phase 1**: FP16 SHADER_F16 detection and emulated fallback
- **Precision Phase 3**: DF128 (Dekker on f64 base, ~104-bit mantissa)
- **Test coverage**: Evolve CI `--fail-under` from 80 to 90%
- **Sovereign pipeline**: CoralReefDevice P0 blocker resolution
- **Multi-GPU**: Multi-adapter dispatch and load balancing
