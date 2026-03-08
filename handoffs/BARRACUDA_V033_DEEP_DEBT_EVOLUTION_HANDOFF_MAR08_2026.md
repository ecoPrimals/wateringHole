# barraCuda v0.3.3 — Deep Debt Evolution Sprint Handoff

**Date**: March 8, 2026
**From**: barraCuda
**To**: All Springs, toadStool, coralReef

---

## Summary

This sprint resolves the P0 f64 shared-memory routing gap across all reduce
ops, extracts hardcoded primal identity to a single constant, and evolves
`SpringDomain` from a hardcoded enum to a runtime-extensible capability type.

## Changes

### P0: Fp64Strategy Routing — All f64 Reduce Ops

**Problem**: `SumReduceF64` and `VarianceReduceF64` correctly routed through
`shader_for_device()` to select DF64 shaders on Hybrid hardware (Ada Lovelace
RTX 4070, NVK). Four reduce ops and `ReduceScalarPipeline` did NOT, producing
zeros on Hybrid GPUs when using `var<workgroup>` f64.

**Fixed ops**:
- `ProdReduceF64` — product and log-product reduction
- `NormReduceF64` — L1, L2, Linf, Frobenius, p-norm reduction
- `FusedMapReduceF64` — configurable map+reduce (Shannon, Simpson, etc.)
- `ReduceScalarPipeline` — two-pass scalar pipeline (also fixed `compile_shader` bypass)

**New shaders**:
- `shaders/reduce/prod_reduce_df64.wgsl`
- `shaders/reduce/norm_reduce_df64.wgsl`
- `shaders/reduce/fused_map_reduce_df64.wgsl`

All use `shared_hi`/`shared_lo` f32-pair workgroup memory with `df64_add`/`df64_mul`.

### P1: PRIMAL_NAME Constant

`const PRIMAL_NAME: &str = "barraCuda"` in `barracuda-core/src/lib.rs` replaces
5 scattered string literals across `bin/barracuda.rs`, `rpc.rs`, `lib.rs`,
`ipc/methods.rs`. Self-knowledge in one definition.

### P2: SpringDomain Capability Evolution

`SpringDomain` evolved from a hardcoded 6-variant enum to
`struct SpringDomain(pub &'static str)`. barraCuda no longer embeds
compile-time knowledge of other primals in its type system. Associated
constants (`HOT_SPRING`, `WET_SPRING`, etc.) preserve ergonomics.

New domains are runtime-extensible: `SpringDomain("myNewDomain")`.

## Impact on Springs

- **All springs using f64 reduce ops**: Product, norm, and fused-map-reduce
  operations now correctly produce non-zero results on Hybrid hardware.
- **Springs referencing `SpringDomain`**: Update `SpringDomain::HotSpring` to
  `SpringDomain::HOT_SPRING` (associated constants instead of enum variants).

## Validation

- Zero warnings across full workspace
- 268+ tests passed (provenance, reduce ops, barracuda-core, broader ops, integration)
- Zero failures

## Pin

barraCuda HEAD at time of handoff (commit pending).
