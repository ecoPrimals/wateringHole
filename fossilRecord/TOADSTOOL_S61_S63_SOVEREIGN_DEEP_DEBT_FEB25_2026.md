# ToadStool → Ecosystem Handoff: Sessions 61-63 (Sovereign Compiler + Deep Debt Evolution)

**Date**: February 25, 2026
**From**: ToadStool / BarraCUDA (ecoPrimals/phase1/toadStool)
**To**: All Springs + ecosystem primals
**ToadStool baseline**: Sessions 61-63 (Feb 25, 2026)

---

## Summary

Sessions 61-63 deliver two major thrusts: (1) the **Sovereign Compiler** — an end-to-end
Rust GPU compilation pipeline via naga-IR that bypasses WGSL text parsing at runtime, and
(2) **systematic deep debt resolution** across the barracuda codebase — dead code wired into
live paths, smart refactoring of large files, and API hygiene improvements.

### Key Numbers

| Metric | Before (S60) | After (S63) | Delta |
|--------|-------------|-------------|-------|
| WGSL shaders | 680+ | 687 | +7 (DF64 force variants) |
| Barracuda tests | 2,435 | 2,440 | +5 |
| Clippy warnings | 0 | 0 | — |
| `#[allow(dead_code)]` on WGSL constants | 25+ | 0 | eliminated |
| `coulomb_f64/mod.rs` lines | 610 | 369 | -39% |
| `morse_f64.rs` lines | 953 | 804 | -16% |

---

## Part 1: Sovereign Compiler (Session 61)

### What It Is

`SovereignCompiler` in `crates/barracuda/src/shaders/sovereign/` provides naga-IR level
optimization with SPIR-V output — the first step toward end-to-end Rust GPU compilation
(eliminating the WGSL text → naga parse → SPIR-V → driver pipeline at runtime).

### Pipeline

```
WGSL source → naga::front::wgsl::parse → naga IR
  → FMA fusion (Mul+Add → fma, ~1.3x)
  → Dead expression elimination (mark-sweep DCE)
  → naga::back::spv::write → SPIR-V binary
  → wgpu SPIRV_SHADER_PASSTHROUGH → GPU driver
```

### What Springs Should Know

- **No API changes required** — `compile_shader_f64()` automatically attempts the sovereign
  path and falls back to WGSL text when SPIR-V passthrough is unavailable.
- **FMA fusion is universal** — benefits all backends (NVIDIA, AMD, Intel), not just NAK.
- **`SPIRV_SHADER_PASSTHROUGH`** is now requested in all 5 device creation paths.
  If a driver doesn't support it, the feature request is silently ignored.

### Future Iterations (Not Yet Implemented)

- Register pressure estimation (naga expression arena live-range counting)
- Loop software pipelining at naga IR level
- Architecture-specific peephole optimization per `GpuArch`
- naga → NAK IR direct bridge (research — would bypass `spirv_to_nir` C boundary)

---

## Part 2: Deep Debt Evolution (Sessions 62-63)

### Dead Code → Live Code

| Item | What Changed | Impact |
|------|-------------|--------|
| `solve_gpu_parallel` (cyclic reduction) | Full O(log n) GPU implementation was complete but never called | Now dispatched for n ≥ 2048; serial path retained for smaller systems |
| `partial_maximin` (maximin LHS) | O(n) per-swap distance recompute was implemented but unused | Wired into CP optimization loop; was calling O(n²) `maximin_distance()` per swap |
| `erfc_deriv` (electrostatics) | Public function had `#[allow(dead_code)]` | Promoted to public API; re-exported from `electrostatics::mod.rs` |
| 25+ WGSL shader constants | `#[allow(dead_code)] const WGSL_*` across barracuda | All evolved to documented `pub const` with module-level re-exports |

### Smart Refactoring

| File | Before | After | Technique |
|------|--------|-------|-----------|
| `coulomb_f64/mod.rs` | 610 lines | 369 lines | Extracted `CoulombBuffers` struct, `read_f64_via_staging()`, `map_staging_to_vec()` — eliminated complete GPU pipeline duplication between forces-only and forces+energy paths |
| `morse_f64.rs` | 953 lines | 804 lines | Extracted `MorseBuffers` struct and `reduce_bond_forces()` function — shared across `compute_gpu` and `compute_gpu_with_energy` |

### API Hygiene

| Change | Detail |
|--------|--------|
| `WebGPUAdapter::mock_data` | `String` placeholder → `_private: ()` (zero heap allocation when webgpu feature disabled) |
| `instant` crate | Removed from neurobench-runner (unused; code already on `std::time::Instant`) |
| `GriffinLim` | `n_iter` dead_code annotation removed (field IS used in GPU params); `n_fft`/`hop_length` documented as reserved |
| `fhe_key_switch.rs` | Dead `U64_EMU_PREAMBLE` constant removed |
| OS compat stubs | `can_handle()` checks `cfg!(target_os)`; `execute_with_compatibility()` returns `SystemError::NotSupported` on wrong platform |
| Discovery fallbacks | Table-driven `default_fallbacks()`, early-exit when not dev mode |

---

## Part 3: What Springs Should Absorb / Act On

### For All Springs

1. **No action needed on sovereign compiler** — it's transparent. Your existing barracuda
   imports work identically. FMA fusion is automatically applied.

2. **New public API**: `barracuda::ops::md::electrostatics::erfc_deriv` is now exported.
   If any spring needs the derivative of erfc for force calculations, it's available.

3. **Maximin LHS is faster** — if any spring uses `barracuda::sample::maximin_lhs()`,
   the optimization loop is now O(n) per swap instead of O(n²). No API change.

4. **Cyclic reduction auto-parallel** — `CyclicReductionF64::solve()` now dispatches to
   O(log n) GPU parallel for n ≥ 2048. No API change needed.

### For groundSpring

- **V6 handoff items remain unchanged** — the 3 priority absorption targets (batched_multinomial,
  rawr_weighted_mean, mc_et0_propagate) and PRNG alignment are still pending.
- **`spectral::anderson` re-export issue** (V6 lesson #1) not yet addressed — still private
  submodule with re-exports at `spectral::*`.

### For wetSpring

- **All 31 ToadStool primitives consumed remain stable** — no breaking API changes.
- **Track 3 drug repurposing** workstream unaffected.

### For neuralSpring

- **All 11 rewired functions remain stable** — no breaking API changes.
- **`GpuDriverProfile`** continues to work identically.

### For hotSpring

- **NAK Titan V validation** still BLOCKED on hardware access.
- **Sovereign compiler FMA fusion** now addresses NAK Deficiency 4 at the IR level for all
  backends — same benefit on NVIDIA, AMD, Intel.

---

## Part 4: Quality Gates

| Gate | Status |
|------|--------|
| `cargo build --workspace` | PASS |
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy -p barracuda --lib` | 0 warnings |
| `cargo test -p barracuda --lib` | 2,440 pass (4 known W-003 cascade, 12 ignored) |
| File size limit | All production files under 1000 lines |
| Dead code | Zero `#[allow(dead_code)]` on WGSL constants |
| Production mocks | Zero (TpuBackend::Mock behind feature gate) |

---

## Part 5: Active Debt (Carried Forward)

| ID | Description | Status |
|----|-------------|--------|
| W-001 | f64 transcendental polyfills (28 functions via pure WGSL) | Active — architecturally solved |
| W-003 | NAK Titan V hardware validation | BLOCKED — requires Titan V hardware |
| D-S46-001 | Conv2D/Pool stride/padding/channels | Carried |
| D-S18-002 | cubecl transitive `dirs-sys` | Low — needs upstream PR |
| P1 | DF64 extended transcendentals (asin, acos, atan, sinh, cosh, gamma, erf) | Upcoming |
| P2 | Architecture-specific polynomial selection per silicon family | Deferred until profiling |

---

*ToadStool S61-63 handoff complete. Sovereign compiler operational, deep debt systematically resolved. All springs: no breaking changes, no action required.*
