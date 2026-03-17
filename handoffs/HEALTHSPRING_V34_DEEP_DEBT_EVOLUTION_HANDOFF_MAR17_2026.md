# healthSpring V34 — Deep Debt Evolution Handoff

**Date**: March 17, 2026
**From**: healthSpring V34
**To**: barraCuda, toadStool, coralReef, petalTongue, Squirrel, biomeOS, sibling springs
**License**: AGPL-3.0-or-later

---

## Executive Summary

- healthSpring V34 completes a deep debt evolution pass across the full codebase
- **Zero clippy warnings** under `pedantic + nursery + all` with `-D warnings`
- **634 unit tests passing**, zero failures
- **14 experiments migrated** from manual counters to `ValidationHarness`
- **4 large files refactored** into single-responsibility modules (all files < 500 LOC)
- **Canonical `PRIMAL_NAME`** — single source of truth, zero hardcoded strings
- **Capability-based discovery** added for coralReef (shader) and Squirrel (model)
- **Provenance** added to `microbiome_transfer.rs` gut parameter set

## What Changed in V34

### 1. Canonical Primal Identity

`PRIMAL_NAME`, `PRIMAL_DOMAIN`, and `QS_GENE_MATRIX_FILE` are now `pub const` in `lib.rs`. All 12+ usages of hardcoded `"healthspring"` across visualization nodes, IPC socket, capabilities, and scenario builders now reference the canonical constant. Primal code has self-knowledge only — no other primal names are hardcoded.

**Files changed**: `lib.rs`, `ipc/socket.rs`, `bin/healthspring_primal/capabilities.rs`, `visualization/nodes/{mod,biosignal,microbiome,endocrine,pkpd}.rs`, `visualization/mod.rs`, `visualization/scenarios/mod.rs`, `data/storage.rs`

### 2. Smart File Refactoring

| Original File | LOC | Split Into | Max LOC |
|---------------|-----|-----------|---------|
| `toadstool/pipeline.rs` | 767 | `pipeline/{mod,gpu,workload,tests}.rs` | 403 |
| `toadstool/stage.rs` | 587 | `stage/{mod,exec,tests}.rs` | 283 |
| `bin/healthspring_primal/server.rs` | 571 | `server/{mod,signal,connection,routing,registration}.rs` | 230 |
| `pkpd/diagnostics.rs` | 531 | `diagnostics/{mod,cwres,vpc,gof}.rs` | 291 |

All public APIs preserved via re-exports. Zero test regressions.

### 3. ValidationHarness Migration

14 experiments (exp001–006, exp010–013, exp020–023) migrated from manual `passed`/`failed` counters to `ValidationHarness`. Each now uses `check_abs`, `check_rel`, `check_bool`, `check_exact`, `check_lower`, `check_upper` and `exit()`. The hotSpring pattern is now consistent across all validation binaries.

### 4. Capability-Based Discovery (coralReef + Squirrel)

Two new discovery functions in `ipc/socket.rs`:
- `discover_shader_compiler()` — probes for `shader.*` capabilities (coralReef)
- `discover_inference_primal()` — probes for `model.*` capabilities (Squirrel)

Both follow the three-tier resolution pattern: env override → named primal scan → capability probe. No hardcoded primal names.

New capabilities registered in `ALL_CAPABILITIES`:
- `compute.shader_compile`
- `model.inference_route`

### 5. Provenance for Gut Parameters

`VALIDATED_GUT_PROVENANCE` added to `microbiome_transfer.rs` — 5 `AnalyticalProvenance` records linking each `GutAndersonParams` entry to its source experiment (exp010, exp012, exp013, exp105).

### 6. Clippy Clean

Fixed `option_if_let_else` in exp084 and exp060. Removed stale `#[expect(clippy::too_many_lines)]` from shortened experiments. Added `#[cfg_attr(not(feature = "gpu"), expect(...))]` for feature-conditional lints in metalForge. Full workspace passes `clippy::all + pedantic + nursery` with zero warnings.

## barraCuda Consumption Inventory

healthSpring uses the following barraCuda modules:
- `barracuda::stats` — Shannon, Simpson, Chao1, Pielou, Bray-Curtis
- `barracuda::special` — tridiagonal QL, Anderson diagonalize
- `barracuda::rng` — LCG step, multiplier
- `barracuda::ops` — HillFunctionF64, PopulationPkF64, DiversityFusionGpu
- `barracuda::numerical` — OdeSystem trait (Michaelis-Menten, compartmental PK)

### Absorption Candidates (healthSpring → barraCuda)

| Local Module | Target barraCuda Location | Status |
|-------------|--------------------------|--------|
| `michaelis_menten_batch_f64.wgsl` | `barracuda::ops::bio::MichaelisMentenBatch` | Tier B |
| `scfa_batch_f64.wgsl` | `barracuda::ops::bio::ScfaBatch` | Tier B |
| `beat_classify_batch_f64.wgsl` | `barracuda::ops::bio::BeatClassifyBatch` | Tier B |
| `biosignal/fft.rs` | `barracuda::spectral::fft` | Tier C |

## toadStool / metalForge Consumption

- `healthspring-toadstool` wraps pipeline execution (CPU/GPU/auto)
- `healthspring-forge` provides `PrecisionRouting`, `Workload`, `Substrate`
- Pipeline refactored: `gpu.rs` handles result conversion, `workload.rs` handles metalForge routing

## coralReef Integration Plan

Current: `strip_f64_enable()` WGSL preprocessor workaround for f64 support.
Target: Direct `shader.compile.*` IPC to coralReef for sovereign WGSL → SPIR-V → native.
Discovery function `discover_shader_compiler()` is wired and ready.

## Squirrel Integration Plan

New `discover_inference_primal()` ready for `model.*` capability routing.
Use case: route patient assessment scenarios through Squirrel for ML-augmented risk scoring.

## Remaining Debt

| Priority | Item | Tracking |
|----------|------|----------|
| Medium | `TensorSession` migration from local `execute_fused()` | specs/EVOLUTION_MAP.md |
| Medium | Property-based testing (`proptest`) for WFDB/QS parsers | — |
| Low | `deny.toml` `multiple-versions = "deny"` | stabilize dep tree first |
| Low | Niche YAML version alignment (`0.26.0` → crate `0.1.0`) | — |
| Low | QS matrix `from_str` → `from_reader` for streaming | L2 |

## Verification

```
cargo test --workspace --lib  → 634 passed, 0 failed
cargo clippy --workspace --all-targets -D warnings -D clippy::{all,pedantic,nursery}  → 0 errors
cargo fmt --all -- --check  → 0 diffs
```
