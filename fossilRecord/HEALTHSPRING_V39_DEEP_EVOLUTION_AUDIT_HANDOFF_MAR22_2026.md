# healthSpring V39 Handoff — Deep Evolution Audit

**Date:** 2026-03-22
**From:** healthSpring V39 (deep evolution audit session)
**To:** barraCuda team, toadStool team, ecosystem
**License:** AGPL-3.0-or-later
**Supersedes:** HEALTHSPRING_V39_TOXICOLOGY_SIMULATION_HORMESIS_HANDOFF_MAR19_2026.md

---

## Executive Summary

Full eight-point evolution audit of healthSpring covering debt/gap analysis,
code quality, validation fidelity, barraCuda dependency health, evolution
readiness, test coverage, ecosystem compliance, and this handoff.

Fixed 5 clippy warnings (similar_names, suboptimal_flops, cast_lossless,
unwrap_used in test), migrated last `#[allow()]` to `#[expect()]`, split
`toxicology.rs` (1061 lines) into `toxicology/mod.rs` + `toxicology/hormesis.rs`
(564 + 508 lines), added 5 missing IPC capability advertisements
(toxicology + simulation), created CONTEXT.md per PUBLIC_SURFACE_STANDARD,
and fixed experiments/README.md version drift.

**Post-audit state:** 809 tests, 0 failures, 0 clippy warnings (pedantic +
nursery), 0 unsafe code, 0 TODO/FIXME in source, 0 `#[allow()]`, 0 files
over 1000 lines, 0 PII, CONTEXT.md present.

---

## What Changed

### Clippy Fixes (5 errors → 0)

| File | Issue | Fix |
|------|-------|-----|
| `toxicology.rs:720` | `suboptimal_flops` | `0.1 * 1.0 + 0.2 * 2.0` → `0.1f64.mul_add(1.0, 0.2 * 2.0)` |
| `toxicology.rs:928` | `similar_names` (`ic50_0`/`ic50_20`) | Renamed to `ic50_naive`/`ic50_adapted` |
| `toxicology.rs:949` | `similar_names` (`cost_0`/`cost_50`) | Renamed to `cost_naive`/`cost_adapted` |
| `simulation.rs:494` | `cast_lossless` | `\|i\| i as f64` → `f64::from` |
| `ipc/transport.rs:197` | `unwrap_used` in test | `.unwrap()` → `.unwrap_or("")` |

### `#[allow()]` → `#[expect()]` Migration

| File | Old | New |
|------|-----|-----|
| `data/fetch.rs:238` | `#[cfg_attr(not(feature = "nestgate"), allow(unused_variables))]` | `#[cfg_attr(not(feature = "nestgate"), expect(unused_variables, reason = "..."))]` |

### Module Split: `toxicology.rs` (1061 lines → 2 files)

| File | Lines | Content |
|------|-------|---------|
| `toxicology/mod.rs` | 564 | Core toxicology: burden, IPR, clearance, landscape, disorder |
| `toxicology/hormesis.rs` | 508 | Biphasic dose-response, mithridatism, immune calibration, ecological hormesis |

Public API unchanged — `pub mod hormesis; pub use hormesis::*;` preserves all exports.

### Missing Capability Advertisements (5 added)

The dispatch REGISTRY routed these methods but `ALL_CAPABILITIES` did not
advertise them to biomeOS:

| Method | Domain |
|--------|--------|
| `science.toxicology.biphasic_dose_response` | toxicology |
| `science.toxicology.toxicity_landscape` | toxicology |
| `science.toxicology.hormetic_optimum` | toxicology |
| `science.simulation.mechanistic_fitness` | simulation |
| `science.simulation.ecosystem_simulate` | simulation |

### CONTEXT.md Created

New file at repo root per PUBLIC_SURFACE_STANDARD.md Layer 3. 80 lines covering:
what it is, role in ecosystem, technical facts, key capabilities, boundaries,
related repos, evolution path, design philosophy.

### Documentation Drift Fixed

- `experiments/README.md`: V38/79 experiments/719 tests → V39/83 experiments/809 tests

---

## Quality Metrics

| Metric | Value |
|--------|-------|
| **Tests** | 809 passed, 0 failed |
| **Clippy warnings** | 0 (pedantic + nursery, all targets) |
| **`cargo fmt`** | Clean |
| **`cargo doc`** | 0 warnings |
| **Unsafe code** | 0 (`#![forbid(unsafe_code)]` on all crate roots) |
| **`#[allow()]`** | 0 (all overrides use `#[expect(reason)]`) |
| **TODO/FIXME** | 0 in `.rs` source |
| **Files > 1000 lines** | 0 (max: 849 lines — provenance.rs) |
| **`.unwrap()` in library code** | 0 (crate-level `#![deny(clippy::unwrap_used)]`) |
| **PII** | 0 emails, 0 home paths, 0 credentials in source |
| **Line coverage** | ~79% (target: 90%; low areas: toadstool GPU paths, visualization streaming, WFDB annotations) |
| **IPC capabilities** | 64 (51 science + 13 infrastructure) + `mcp.tools.list` |

---

## barraCuda Primitive Consumption

- **Pin**: barraCuda v0.3.5, rev `a60819c3` (2026-03-14)
- **CPU-side**: `barracuda::stats` (hill, shannon, simpson, chao1, bray_curtis, mean), `barracuda::rng` (lcg), `barracuda::special` (anderson_diagonalize), `barracuda::health` (mm_auc, antibiotic_perturbation, scr_rate), `barracuda::numerical` (OdeSystem, BatchedOdeRK4)
- **GPU-side** (feature-gated): `barracuda::device::WgpuDevice`, `barracuda::ops` (HillFunctionF64, PopulationPkF64, DiversityFusionGpu, MichaelisMentenBatchGpu, ScfaBatchGpu, BeatClassifyGpu)
- **Local WGSL**: 6 shaders (hill, popPK, diversity, MM batch, SCFA batch, beat classify)
- **Not yet absorbed from barraCuda**: `ops::fft` (HRV power spectrum uses local `biosignal::fft::rfft`), `linalg::cholesky` (NLME uses local solver)

### What barraCuda Should Absorb

1. **`biphasic_dose_response`** — element-wise hormetic curve, ready for `batched_elementwise_f64.wgsl`
2. **`toxicity_ipr`** — IPR reduction, maps to `FusedMapReduceF64`
3. **`mechanistic_cell_fitness`** — compound of Hill ops, batch-parallel per pathway
4. **`ecosystem_simulate`** — ODE batch, similar to PBPK pattern
5. **`fft_radix2_f64`** — barraCuda has `ops::fft`; healthSpring should consume it instead of local impl

---

## Evolution Readiness

### Tier Assessment (from specs/EVOLUTION_MAP.md)

| Tier | Count | Description |
|------|-------|-------------|
| **A (Direct rewire)** | 10 modules | Hill, PopPK, Diversity, compound IC50, allometric, VAS time-course, feline PK, fibrosis, endocrine, species params |
| **B (Adapt/compose)** | 14 modules | Simpson (FusedMapReduce), AUC (parallel prefix), Anderson xi, PPG R-value, Bray-Curtis, FOCE, SAEM, VPC, toxicity IPR, burden, biphasic, ecosystem ODE, affinity landscape |
| **C (New shader)** | 4 modules | Pan-Tompkins (streaming/NPU), fuse_channels (toadStool pipeline), PBPK ODE, HRV FFT |

### Blocking Promotion

1. **NPU dispatch**: biosignal streaming (Pan-Tompkins, fuse_channels) needs Akida driver in toadStool
2. **ODE solver absorption**: PBPK still uses simple Euler; `OdeSystem` trait exists but PBPK not migrated
3. **FFT absorption**: local HRV FFT should migrate to `barracuda::ops::fft`
4. **NLME GPU**: FOCE per-subject gradient is embarrassingly parallel but no shader yet

---

## Audit Findings (Reference — No Fix Needed)

### Validation Fidelity

- **`ValidationHarness`**: all 83 experiments use hotSpring pattern (PASS/FAIL per check, exit 0/1)
- **`PROVENANCE_REGISTRY`**: all entries have script, commit, date, command filled
- **Baseline JSON linkage uneven**: exp010 is strong (embeds JSON + provenance); exp001, exp097, exp098, exp099 validate behaviorally but do not embed/compare Python JSON in the binary
- **`cross_validate.py` coverage gap**: covers Tracks 1–8 but not Track 9 experiments (exp097, exp098, exp099, exp111); banner says "Python ↔ Rust" but actually validates Python self-consistency

### Test Coverage Gaps (79% → 90% target)

Low-coverage modules pulling down the aggregate:

| Module | Coverage | Reason |
|--------|----------|--------|
| `toadstool/pipeline/gpu.rs` | 0% | Feature-gated GPU path, no GPU in CI |
| `toadstool/pipeline/workload.rs` | 0% | GPU-only workload routing |
| `toadstool/pipeline/mod.rs` | 29% | CPU+GPU paths; GPU half untested |
| `toadstool/stage/exec.rs` | 36% | GPU execution paths |
| `visualization/stream.rs` | 58% | SSE streaming requires live server |
| `wfdb/annotations.rs` | 59% | Needs PhysioNet test fixtures |
| `visualization/nodes/biosignal.rs` | 74% | Branch coverage on optional channels |
| `visualization/ipc_push/client.rs` | 75% | Unix socket IPC requires mock server |

### I/O Parsers (Streaming Assessment)

- **WFDB Format 212/16**: streaming decoder via `BufReader`, single reusable line buffer
- **No FASTQ/mzML/MS2 in healthSpring** (those are wetSpring domain)
- All file-based I/O uses `BufReader` or `include_str!` for embedded baselines

### Semantic Method Naming

Fully compliant with wateringHole `SEMANTIC_METHOD_NAMING_STANDARD.md`:
`{domain}.{operation}[.{variant}]` pattern. All capabilities use `science.{subdomain}.{operation}`,
`provenance.{operation}`, `lifecycle.{operation}`, `capability.{operation}`, etc.

### License

`AGPL-3.0-or-later` in Cargo.toml, SPDX headers on all source files.

---

## Patterns Worth Absorbing Upstream

1. **`toxicology/hormesis.rs` module split** — clean domain separation: core toxicology
   (burden, IPR, clearance) vs hormesis (biphasic, mithridatism, immune calibration).
   Other springs with growing modules should follow this pattern at the 800-line mark.

2. **Dispatch REGISTRY → `ALL_CAPABILITIES` drift** — if the dispatch registry grows
   independently of the capability advertisement list, methods become routable but
   invisible to biomeOS. Consider deriving `ALL_CAPABILITIES` from the REGISTRY
   instead of maintaining two lists.

3. **`OrExit` trait** — zero-panic error handling for validation binaries. Already in
   use across all 83 experiments. Candidate for extraction to barraCuda validation.

4. **CONTEXT.md compliance** — healthSpring now has CONTEXT.md per PUBLIC_SURFACE_STANDARD
   Layer 3. All springs should follow.

---

## Open Items for Next Session

1. **Coverage push to 90%** — toadstool GPU paths need `#[cfg(not(feature = "gpu"))]`
   CPU-fallback test paths or mock GPU context; `visualization/stream.rs` needs
   in-process SSE test; `wfdb/annotations.rs` needs PhysioNet fixture download
2. **Baseline JSON embedding** — wire exp097/098/099/111 to `include_str!` their
   baseline JSON with provenance check (exp010 pattern)
3. **`cross_validate.py` Track 9 coverage** — add exp097, exp098, exp099, exp111
   baseline checks; fix banner text ("Python ↔ Rust" vs actual behavior)
4. **FFT absorption** — migrate `biosignal::fft::rfft` to `barracuda::ops::fft`
5. **README capability count** — root README claims 85 capabilities; actual is 65
   (51 science + 13 infra + `mcp.tools.list`). Reconcile or document what the
   difference represents
6. **`PROVENANCE_REGISTRY` `checks` field** — most entries have `checks: 0` even
   for scripts producing rich baselines; populate for audit value
7. **NLME GPU promotion** — FOCE per-subject gradient parallelization is the
   NONMEM bottleneck; request `BatchedGradientGpu` from barraCuda
