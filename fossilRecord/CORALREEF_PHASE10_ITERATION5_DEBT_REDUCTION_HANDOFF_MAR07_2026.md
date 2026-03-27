# coralReef — Phase 10 Iteration 5: Debt Reduction Handoff

**Date**: March 7, 2026
**From**: coralReef
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, barraCuda, toadStool

---

## Summary

coralReef Phase 10 — Iteration 5 completes pointer expression tracking,
smart module refactoring, and a comprehensive debt audit. 14/27 cross-spring
shaders now compile to native SM70 SASS. 832 tests, 811 passing, zero failures.

## Metrics

| Metric | Iteration 3 | Iteration 5 | Delta |
|--------|-------------|-------------|-------|
| Total tests | 832 | 832 | — |
| Passing | 805 | 811 | **+6** |
| Ignored | 27 | 21 | **-6** |
| Corpus passing SM70 | 8 | **14** | **+6** |
| Clippy warnings | 0 | 0 | — |
| Largest file (prod) | 842 LOC | 408 LOC | **-434** |

## Compiler Features Added (Iterations 4 + 5)

| Feature | Shaders Unblocked |
|---------|-------------------|
| Binary Divide (f32/f64/int via rcp) | su3 advanced to reg alloc |
| Binary Modulo (f32/f64/int) | su3 advanced to reg alloc |
| ArrayLength (CBuf descriptor) | chi2_batch |
| Math::Pow (exp2(y*log2(x))) | rk4 advanced to ptr tracking |
| Math::Exp, Math::Log | infrastructure |
| Atomic statement (full set) | rdf_histogram |
| **Pointer expression tracking** | **rk4_parallel, yukawa_force_celllist** |

### Pointer Tracking Root Cause

`FunctionArgument` during inline expansion used `return Ok(...)` which
bypassed `expr_map.insert()`. All stores to global buffers from inlined
functions silently failed. Fixed by removing early returns — standard
control flow now ensures expr_map insertion.

## Cross-Spring Shader Corpus (14/27 compiling)

| Spring | Shaders | Passing | New This Iteration |
|--------|---------|---------|-------------------|
| hotSpring | 16 | 9 | chi2_batch, rdf_histogram |
| groundSpring | 2 | 2 | anderson_lyapunov_f64 |
| neuralSpring | 8 | 3 | rk4_parallel |
| airSpring | 1 | 0 | — |
| **Total** | **27** | **14** | **+6** |

### Remaining Blockers

| Blocker | Count | Shaders |
|---------|-------|---------|
| df64 preamble (multi-file) | 5 | gelu, layer_norm, softmax, sdpa_scores, sigmoid |
| External include | 2 | dielectric_mermin, bcs_bisection |
| Reg alloc SSA tracking | 1 | su3_gauge_force |
| Scheduler loop phi | 1 | wilson_plaquette |
| Encoder reg file | 1 | semf_batch |
| const_tracker | 1 | batched_hfb_hamiltonian |
| WGSL keyword | 1 | kl_divergence |
| naga f64 extension | 1 | local_elementwise |

## Debt Reduction

### Module Refactoring

| Module | Before | After |
|--------|--------|-------|
| `opt_instr_sched_prepass/mod.rs` | 842 LOC | 313 LOC (+ generate_order.rs 408 + net_live.rs 117) |

### Audit Results

- **unwrap()**: All 75 unwraps in ipc/mod.rs + naga_translate/mod.rs confirmed test-only
- **Unsafe**: coral-driver unsafe well-structured (RAII MappedRegion, documented safety)
- **Dependencies**: libc is only direct FFI dep (required for DRM)
- **Hardcoding**: No peer primal names in production code
- **Mocks**: No test mocks in production; coral-reef-stubs is deliberate replacement

## Compilation Benchmarks (SM70, debug build)

| Shader | Size | Time |
|--------|------|------|
| `axpy_f64` | 672 B | 49 ms |
| `chi2_batch_f64` | 992 B | 51 ms |
| `cg_kernels_f64` | 768 B | 53 ms |
| `kinetic_energy_f64` | 944 B | 56 ms |
| `berendsen_f64` | 1,152 B | 58 ms |
| `vv_half_kick_f64` | 1,984 B | 70 ms |
| `mean_reduce` | 528 B | 80 ms |
| `sum_reduce_f64` | 1,376 B | 161 ms |
| `rdf_histogram_f64` | 3,984 B | 196 ms |
| `anderson_lyapunov_f64` | 4,896 B | 271 ms |
| `anderson_lyapunov_f32` | 2,272 B | 279 ms |
| `stress_virial_f64` | 5,952 B | 437 ms |
| `yukawa_force_celllist_f64` | 12,272 B | 747 ms |
| `rk4_parallel` | 8,624 B | 1,527 ms |

---

*coralReef — sovereign Rust GPU compiler, 14/27 cross-spring shaders compiling, zero FFI.*
