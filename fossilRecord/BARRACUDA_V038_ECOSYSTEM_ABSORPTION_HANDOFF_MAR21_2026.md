# barraCuda v0.3.8 — Ecosystem Absorption & API Housekeeping

**Date**: 2026-03-21
**Sprint**: 18
**Version**: 0.3.8
**Scope**: Full pull + review of 8 springs + 10+ primals; API housekeeping; cross-spring feature audit

---

## Summary

Comprehensive ecosystem-wide pull and review across all springs (airSpring, groundSpring,
hotSpring, neuralSpring, wetSpring, healthSpring, ludoSpring, primalSpring) and all primals
(bearDog, nestGate, songBird, squirrel, toadStool, biomeOS, loamSpine, petalTongue,
rhizoCrypt, sweetGrass). Three new repositories cloned (healthSpring, ludoSpring,
primalSpring). All absorption opportunities evaluated, many confirmed already implemented.

## Changes

### Breaking (API)

- **`GpuDriverProfile` struct removed** — Deprecated since v0.3.6, all springs migrated to
  `DeviceCapabilities` in Sprint 14. Supporting enums (`DriverKind`, `CompilerKind`, `GpuArch`,
  `Fp64Rate`, `EigensolveStrategy`, `Fp64Strategy`, `PrecisionRoutingAdvice`, `Workaround`)
  remain. Migration: `GpuDriverProfile::from_device(dev)` → `DeviceCapabilities::from_device(dev)`.
- **`folding_df64` gated behind `domain-fold` feature** — Included in `domain-models` umbrella.
  No change needed if using default features.

### New API

- **`barracuda::cast`** module — Safe numeric cast helpers (`usize_as_u32`, `u64_as_u32`,
  `f64_as_f32_checked`, `f64_as_f32_lossy`, etc.) with `CastOverflow` and `PrecisionLoss`
  typed error variants in `BarracudaError`.
- **`ESN::wgpu_device()`** and **`MultiHeadEsn::wgpu_device()`** — Direct `&Arc<WgpuDevice>`
  access. neuralSpring can replace `reservoir.state().device().clone()` workaround.
- **`WGSL_GELU_F64`**, **`WGSL_SOFTMAX_SIMPLE_F64`**, **`WGSL_SOFTMAX_BASIC_F64`** —
  Public f64 shader constants for springs building custom `ComputeDispatch` pipelines.

### Quality

- **Tolerance stability contract** — Tightening tolerances is now a documented breaking change.
- **`cast_lossless` promoted to `warn`** — Zero violations found; codebase already clean.
- **3,618 tests pass**, zero clippy warnings, `cargo fmt` clean.

## Ecosystem Audit Results

Already implemented (no work needed):
- Pairwise Hamming/Jaccard distance → `ops/bio/pairwise_hamming.rs`, `pairwise_jaccard.rs`
- L2/cdist/pdist → `ops/cdist_wgsl.rs`, `ops/pdist.rs`
- Chi-squared → `special/chi_squared.rs`, `ops/fused_chi_squared_f64.rs`
- KL divergence → `ops/kl_divergence.rs`, `ops/fused_kl_divergence_f64.rs`
- xoshiro128ss GPU PRNG → `ops/prng_xoshiro_wgsl.rs`, `shaders/misc/xoshiro128ss_f64.wgsl`
- HMM backward/Viterbi → `ops/bio/hmm.rs` (full GPU implementation)

Deferred (awaiting spring input):
- Health ODE systems — `OdeSystem` trait + `ode_bio/` infrastructure ready; waiting for
  healthSpring to provide specific PK/PD model parameters
- hotSpring shader contributions — hotSpring focused on GPU vendor issues with coralReef;
  no new shaders to absorb this sprint

## Cross-Primal Pins

- toadStool: S163
- coralReef: Phase 10 Iter 62
- All springs synced to barraCuda v0.3.5+ / wgpu 28

## Quality Gates

- `cargo fmt --all --check` ✅
- `cargo clippy --all-targets` ✅ (zero warnings)
- `cargo test --lib -p barracuda` ✅ (3,618 pass, 0 fail)
- `cargo test -p barracuda-core` ✅
- `#![forbid(unsafe_code)]` ✅
- Zero production `unwrap()` ✅
