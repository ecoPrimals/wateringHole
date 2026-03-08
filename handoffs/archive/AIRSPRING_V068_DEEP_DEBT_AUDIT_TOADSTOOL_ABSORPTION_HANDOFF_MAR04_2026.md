<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# airSpring V0.6.8 Deep Debt Audit — ToadStool/barraCuda Absorption Handoff

**Date**: March 4, 2026
**From**: airSpring V0.6.8 (ecology/agriculture validation Spring)
**To**: ToadStool S93+ / barraCuda 0.3.1+ / All Springs
**License**: AGPL-3.0-or-later

---

## Executive Summary

airSpring completed deep debt audit round 2 on March 4, 2026. This handoff
documents patterns, learnings, and absorption candidates for the barraCuda/ToadStool
team and sibling Springs.

- 1132/1132 workspace tests (846 lib + 286 integration), 62 forge, 86 binaries
- Zero clippy pedantic+nursery warnings, zero unsafe, zero mocks in production
- Sovereignty hardened: `domain_use` replaces `airspring_use`, agnostic debug labels
- Dependency gated: `ureq`/`ring` behind `standalone-http` feature for pure Rust builds
- 3 large files refactored into focused modules (preserving public API)
- Fallible constructors (`try_new`) for data providers
- Zero-copy CSV parser optimization

---

## 1. Absorption Candidates for barraCuda

### 1.1 Six Local WGSL Shaders (Pending f64 Promotion)

Six f32 shaders in `local_elementwise.wgsl` validated (Exp 075) and ready for
absorption into `batched_elementwise_f64` as ops 14-19:

| Proposed Op | Domain | Precision | Status |
|:-----------:|--------|-----------|--------|
| 14 | SCS-CN Runoff | f32 → **f64** | Validated, pure arithmetic |
| 15 | Stewart Yield | f32 → **f64** | Validated, pure arithmetic |
| 16 | Makkink ET₀ | f32 → **f64** | Validated, needs `sat_vp` helpers |
| 17 | Turc ET₀ | f32 → **f64** | Validated, humidity branch |
| 18 | Hamon PET | f32 → **f64** | Validated, needs `daylight_hr` |
| 19 | Blaney-Criddle PET | f32 → **f64** | Validated, needs `daylight_hr` |

All helper functions already exist in ToadStool (see V053 handoff for mapping).

### 1.2 Domain Tolerances

50 named tolerance constants in airSpring's `tolerances.rs` may inform barraCuda's
cross-domain tolerance library. Notable strictness vs barraCuda defaults:

- `ET0_REFERENCE`: abs=0.01, rel=1e-3 (FAO-56 worked examples)
- `WATER_BALANCE_MASS`: abs=0.01, rel=1e-6 (mass conservation)
- `BIO_DIVERSITY_SHANNON`: abs=1e-8, rel=1e-8 (exact formula)

### 1.3 `BatchedStatefulF64` Water Balance Pattern

The seasonal pipeline chains state across GPU dispatches without per-day CPU readback.
This pattern (`state_in → compute → state_out → swap`) is the key to multi-field
performance (6.8M field-days/s).

---

## 2. Cross-Spring Patterns (For All Springs)

### 2.1 Feature-Gating C Dependencies

Any dependency pulling C/asm code (e.g., `ureq` → `ring`) should be feature-gated:

```toml
[features]
standalone-http = ["dep:ureq"]
```

`discover_transport()` returns `Option<_>` so callers handle the "no transport"
case. Springs using Songbird TLS get a pure Rust build path.

### 2.2 Sovereignty Sweep Checklist

Primal names should not appear in:
- [ ] Struct field names (use `domain_*` instead of `{primal}_*`)
- [ ] GPU debug labels (use generic names: `local_elementwise` not `airspring_local_elementwise`)
- [ ] Log messages (use capability names: `compute.dispatch` not `toadstool`)
- [ ] Environment variable names (use `BARRACUDA_*` not `AIRSPRING_BARRACUDA_*`)

### 2.3 Fallible Constructor Pattern

```rust
pub fn try_new() -> Result<Self, Error> {
    let transport = discover_transport()
        .ok_or_else(|| Error::NoTransport("no HTTP transport available"))?;
    Ok(Self { transport })
}

pub fn new() -> Self {
    Self::try_new().expect("HTTP transport required")
}
```

### 2.4 Large-File Refactoring Pattern

Convert `file.rs` → `file/mod.rs` + submodules. Re-export public types from `mod.rs`.
Public API unchanged. Update `Cargo.toml` binary paths if refactoring binaries.

---

## 3. barraCuda Primitive Consumption (March 4 Snapshot)

airSpring consumes 25+ primitives across 7 barraCuda domains:

| Domain | Count | Key Primitives |
|--------|:-----:|----------------|
| Device | 4 | `WgpuDevice`, `Fp64Strategy`, `GpuDriverProfile`, `F64BuiltinCapabilities` |
| Ops | 8 | `BatchedElementwiseF64` (14 ops), `KrigingF64`, `FusedMapReduceF64`, `MovingWindowStats`, `DiversityFusionGpu` |
| Optimize | 4 | `brent`, `BrentGpu`, `nelder_mead`, `multi_start_nelder_mead` |
| Stats | 15+ | `pearson`, `rmse`, `bootstrap_ci`, `BootstrapMeanGpu`, `JackknifeMeanGpu`, `norm_ppf`, `fit_*`, `shannon`, `simpson` |
| PDE | 4 | `CrankNicolsonConfig`, `HeatEquation1D`, `richards`, `RichardsGpu` |
| Linalg | 1 | `ridge_regression` |
| Validation | 5 | `ValidationHarness`, `exit_no_gpu`, `gpu_required`, `check`, `Tolerance` |

No duplicate math in production code. Test utilities have intentionally different
conventions (documented).

---

## 4. Evolution State

- **28 Tier A** gaps fully integrated (ops 0-13, uncertainty stack, BrentGpu, RichardsGpu)
- **4 Tier B** partially wired (BFGS, tridiagonal, RK45, seasonal pipeline GPU)
- **1 Tier C** data client (HTTP/JSON, now feature-gated)
- **6 GPU-local** ops validated (f32, pending f64 absorption)
- ToadStool S93 synced, barraCuda 0.3.1 standalone

---

## 5. Quality Gates

| Gate | Result |
|------|--------|
| Tests | 1132 workspace + 62 forge, 0 failures |
| Clippy | 0 warnings (pedantic + nursery) |
| Fmt | 0 diffs |
| Doc | 0 warnings |
| Unsafe | 0 (both crates `#![forbid(unsafe_code)]`) |
| File size | All < 1000 LOC |
| Sovereignty | 0 hardcoded primal names in production |
| Mocks | 0 in production (isolated to test/feature) |
| C dependencies | Feature-gated (`ureq`/`ring` behind `standalone-http`) |
| License | AGPL-3.0-or-later (cargo-deny clean) |
