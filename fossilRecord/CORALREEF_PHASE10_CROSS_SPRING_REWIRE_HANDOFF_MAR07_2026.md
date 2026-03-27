# coralReef — Phase 10 Cross-Spring Rewire Handoff

**Date**: March 7, 2026
**From**: coralReef
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, barraCuda, toadStool

---

## Summary

coralReef Phase 10 — Spring Absorption + Compiler Hardening — cross-spring
rewire complete. 27 WGSL shaders imported from all 5 ecosystem springs.
832 tests passing, zero failures.

## Metrics

| Metric | Value |
|--------|-------|
| Total tests | 832 |
| Failures | 0 |
| Ignored (tracked) | 27 |
| WGSL corpus shaders | 27 (from 5 springs) |
| Corpus passing SM70 | 8 |
| Clippy warnings | 0 |
| Unsafe blocks | 0 |
| Files > 1000 LOC | 0 (max 590, down from 918) |

## Cross-Spring Shader Corpus

| Spring | Shaders Imported | Passing | Domain |
|--------|-----------------|---------|--------|
| hotSpring | 16 | 6 | Lattice QCD, MD, nuclear physics |
| groundSpring | 2 | 1 | Condensed matter (Anderson localization) |
| neuralSpring | 8 | 2 | ML attention (coralForge), ODE solver, statistics |
| airSpring | 1 | 0 | Hydrology domain ops |
| **Total** | **27** | **8** | |

### Cross-Spring Evolution Notes

These shaders demonstrate how patterns flow across springs:

1. **hotSpring precision → neuralSpring coralForge**: FMA control, Kahan
   summation patterns from hotSpring's lattice QCD precision work were
   adopted by neuralSpring's `gelu_f64`, `layer_norm_f64`, `softmax_f64`
   for df64 core streaming attention primitives.

2. **neuralSpring statistics → wetSpring + groundSpring**: `kl_divergence_f64`
   originated in neuralSpring for information-theoretic validation, then was
   absorbed by wetSpring for cross-entropy metrics and referenced by
   groundSpring for Anderson model fitness scoring.

3. **hotSpring MD → wetSpring**: `stress_virial_f64` (off-diagonal stress
   tensor) from hotSpring MD simulations is used by wetSpring for mechanical
   property validation in bio-material pipelines.

4. **groundSpring → neuralSpring**: `anderson_lyapunov` (condensed matter
   disorder model) is referenced by neuralSpring for disorder sweep
   validation in metalForge experiments.

5. **hotSpring precision → all springs**: Cancellation-safe BCS v² formula
   (`bcs_bisection_f64`) and stable W(z) asymptotic (`dielectric_mermin_f64`)
   establish numerical safety patterns referenced by wetSpring gap analysis.

## Compilation Benchmarks (SM70, debug build)

| Shader | Size | Time | Notes |
|--------|------|------|-------|
| `axpy_f64` | 672 B | 55 ms | Lattice QCD basic |
| `kinetic_energy_f64` | 944 B | 52 ms | MD reduction |
| `berendsen_f64` | 1,152 B | 55 ms | MD thermostat, sqrt, uniform |
| `cg_kernels_f64` | 768 B | 60 ms | CG with shared memory, barriers |
| `vv_half_kick_f64` | 1,984 B | 63 ms | MD velocity-Verlet |
| `mean_reduce` | 528 B | 78 ms | f32 single-workgroup |
| `sum_reduce_f64` | 1,376 B | 147 ms | f64 shared memory barriers |
| `anderson_lyapunov_f32` | 2,272 B | 213 ms | Loops, PRNG, uniform struct |

## IPC Contract Status

coralReef IPC matches barraCuda expectations:

| Method | Protocol | Status |
|--------|----------|--------|
| `compiler.compile` | JSON-RPC + tarpc | Implemented |
| `compiler.compile_wgsl` | JSON-RPC + tarpc | Implemented |
| `compiler.health` | JSON-RPC + tarpc | Implemented |
| `compiler.supported_archs` | JSON-RPC | Implemented |

### toadStool Integration Notes

toadStool uses `shader.compile.*` namespace — coralReef uses `compiler.*`.
toadStool should proxy its `shader.compile.wgsl` → `compiler.compile_wgsl`
and `shader.compile.spirv` → `compiler.compile`. coralReef's tarpc service
is at the method names above; toadStool's proxy layer handles the mapping.

## Remaining Blockers

| Blocker | Priority | Impact |
|---------|----------|--------|
| `Expression::As` (type cast) | **P1** | Unlocks 14/19 ignored shaders |
| coralDriver hardware dispatch | **P1** | Blocks all springs for sovereign execution |
| Scheduler loop-carried phi | P2 | 2 shaders (SU(3), Wilson plaquette) |
| `Math::Pow` function | P2 | 1 shader (rk4_parallel) |
| Atomic operations | P2 | 1 shader (rdf_histogram) |

## Smart Refactoring Completed

| File | Before | After | Method |
|------|--------|-------|--------|
| `ir/mod.rs` | 918 LOC | 262 LOC | Extracted `src.rs` (427), `fold.rs` (115), `pred.rs` (135) |
| `ipc.rs` | 853 LOC | 590 LOC | Split into `ipc/{mod,jsonrpc,tarpc_transport}.rs` |

---

*coralReef — sovereign Rust GPU compiler, zero FFI, zero vendor lock-in.*
