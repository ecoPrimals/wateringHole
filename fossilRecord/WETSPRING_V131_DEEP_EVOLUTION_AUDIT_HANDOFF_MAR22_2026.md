# wetSpring V131 Handoff — Deep Evolution Audit

**Date:** 2026-03-22
**From:** wetSpring V131 (deep audit session)
**To:** barraCuda team, toadStool team, ecosystem
**License:** AGPL-3.0-or-later
**Supersedes:** WETSPRING_V130_ANDERSON_HORMESIS_FRAMEWORK_HANDOFF_MAR19_2026.md

---

## Executive Summary

Full eight-point evolution audit of wetSpring covering debt/gap analysis, code
quality, validation fidelity, barraCuda dependency health, evolution readiness,
test coverage, ecosystem compliance, and this handoff. Fixed 6 clippy warnings,
eliminated 6 remaining magic tolerance literals, hardened the Validator framework
(0/0 = fail), created missing CONTEXT.md, and added a reason to the last
`#[expect(dead_code)]` without one.

**Post-audit state:** 1,500+ tests, 0 failures, 0 clippy warnings (pedantic +
nursery, all features), 0 unsafe code, 0 TODO/FIXME/HACK in source, 0 `#[allow]`,
0 files over 1000 lines, 0 PII (emails, home paths, credentials), 0 local WGSL.

---

## What Changed

### Clippy Fixes (6 warnings → 0)

| File | Issue | Fix |
|------|-------|-----|
| `bio/binding_landscape.rs:461` | `manual_range_contains` | `d >= -2.0 && d <= 2.0` → `(-2.0..=2.0).contains(&d)` |
| `bio/hormesis.rs:407` | `suboptimal_flops` | `2.0 * w_half + tol` → `2.0f64.mul_add(w_half, tol)` |
| `bio/hormesis.rs:421,425` | `suboptimal_flops` | `16.5 * factor` subtraction → `mul_add` |
| `bio/hormesis.rs:440` | `redundant_closure` | `\|i\| f64::from(i)` → `f64::from` |
| `bio/binding_landscape.rs:297` | `unfulfilled_lint_expectations` | Removed stale `#[expect(clippy::unwrap_used)]` from test module |

### Magic Tolerance Elimination (6 inline literals → 0)

| File | Old | New | Constant |
|------|-----|-----|----------|
| `validate_pure_gpu_streaming_v13.rs` | `1.0` | `tolerances::BIOGAS_KINETICS_ASYMPTOTIC` | Gompertz H(50) → P |
| `validate_anaerobic_afex_stover.rs` | `1.0` | `tolerances::BIOGAS_KINETICS_ASYMPTOTIC` | Untreated H(50) ≈ P |
| `validate_anaerobic_codigestion.rs` | `1.0` | `tolerances::BIOGAS_KINETICS_ASYMPTOTIC` | Gompertz H(∞) → P |
| `validate_biomeos_petaltongue_full.rs` | `0.01` | `tolerances::ASYMPTOTIC_LIMIT` | Shannon H' |
| `validate_biomeos_petaltongue_full.rs` | `0.01` | `tolerances::ODE_STEADY_STATE` | ODE final B |
| `benchmark_python_vs_rust_v5.rs` | `0.01` | `tolerances::ASYMPTOTIC_LIMIT` | B(200) ≈ B_max |

### Validator Framework Hardening

- `print_result(name, 0, 0)` now returns `false` (FAIL) instead of `true`
- Prevents silent pass-through when data is missing or no checks execute
- Test updated: `print_result_zero_total_is_failure` asserts the new behavior

### `#[expect(dead_code)]` Reason Added

- `benchmark_python_vs_rust_v5.rs` `ParityBench` struct: added reason string

### CONTEXT.md Created

- New file at repo root per PUBLIC_SURFACE_STANDARD.md Layer 3
- 75 lines covering: what it is, role, technical facts, capabilities, boundaries,
  related repos, evolution path, design philosophy

---

## Quality Metrics

| Metric | Value |
|--------|-------|
| **Tests** | 1,500 passed, 0 failed, 1 ignored |
| **Validation checks** | 5,700+ across 354 binaries |
| **Clippy warnings** | 0 (pedantic + nursery, all features) |
| **`cargo fmt`** | Clean |
| **`cargo doc`** | Building (354 binary targets; zero warnings expected) |
| **Unsafe code** | 0 (`#![forbid(unsafe_code)]` on all crate roots) |
| **`#[allow()]`** | 0 (all overrides use `#[expect(reason)]`) |
| **TODO/FIXME/HACK** | 0 in `.rs` source |
| **Files > 1000 lines** | 0 (max: 939 lines) |
| **`.unwrap()` in library code** | 0 (crate-level `#![deny(clippy::unwrap_used)]`) |
| **PII** | 0 emails, 0 home paths, 0 credentials in source |
| **Local WGSL** | 0 (full lean achieved) |
| **Inline magic tolerances** | 0 (all use `tolerances::` named constants) |

---

## barraCuda Primitive Consumption

- **150+ primitives** consumed from barraCuda v0.3.5
- **0 local WGSL** shaders (full Write→Absorb→Lean cycle complete)
- **45 GPU modules** across both crates
- **Key primitives:** `FusedMapReduceF64`, `BrayCurtisF64`, `BatchedEighGpu`,
  `GemmF64`, `FelsensteinGpu`, `SmithWatermanGpu`, `TreeInferenceGpu`,
  `BatchedOdeRK4`, `HmmBatchForwardF64`, `Dada2EStepGpu`
- **No duplicate math** — all GPU compute routes through barraCuda

### Evolution Readiness Summary

| Tier | Count | Description |
|------|-------|-------------|
| **A (Lean)** | 22 modules | Direct upstream primitive, no local WGSL |
| **B (Compose)** | 11 modules | Multiple primitives, minor wiring |
| **C (Write)** | 0 modules | Tier C is empty — full lean achieved |

### Blocking Items

1. `reconciliation_gpu` — CPU passthrough; needs `BatchReconcileGpu` for true GPU
2. `ComputeDispatch` migration — P3, medium effort
3. DF64 GEMM adoption — P3, low effort
4. `BandwidthTier` wiring in metalForge — P3, low effort

---

## Patterns Worth Absorbing Upstream

1. **Validator 0/0 = FAIL** — prevents silent pass-through. All springs using
   `wetspring_barracuda::validation::Validator` now get this safety net.
   Consider propagating to barraCuda's own validation framework.

2. **`BIOGAS_KINETICS_ASYMPTOTIC`** tolerance constant (1.0 mL/g VS) — now covers
   all Gompertz growth model validation checks. Springs doing kinetics modeling
   should reference this instead of inline `1.0`.

3. **`OrExit` trait** — zero-panic error handling for validation binaries.
   Replaces `.expect()` / `.unwrap()` with clean stderr + `process::exit(1)`.
   Candidate for extraction to barraCuda validation module.

4. **CONTEXT.md template compliance** — wetSpring now has a CONTEXT.md following
   PUBLIC_SURFACE_STANDARD Layer 3. Other springs should follow.

---

## Audit Findings (No Fix Needed)

### License Field

Cargo.toml says `AGPL-3.0-or-later`. STANDARDS_AND_EXPECTATIONS says
`AGPL-3.0-only`. The LICENSE file contains AGPL-3.0 text. The `-or-later`
suffix is intentional per the SPDX identifier chosen at project inception.
Verify alignment with `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` if changing.

### I/O Parsers (Streaming Assessment)

All core parsers stream from disk (BufReader-based):
- **FASTQ:** Zero-copy path via `for_each_record` (borrowed slices into reused buffers)
- **mzML:** Streaming XML pull parser with reusable decode buffers
- **MS2:** Streaming with single reusable line buffer
- **JCAMP/mzXML/Nanopore:** All streaming iterators
- **BIOM:** Parses from BufReader but loads full table (matrix domain requirement)

### Test Coverage (Four Types Present)

1. **Unit tests:** 170+ modules with `#[cfg(test)]`, 1,500+ individual tests
2. **Integration tests:** `tests/io_roundtrip.rs`, `tests/bio_integration.rs`,
   `tests/determinism.rs`, `tests/ipc_roundtrip.rs`
3. **Validation binaries:** 354 binaries with PASS/FAIL, exit 0/1/2 pattern
4. **Determinism tests:** `determinism_diversity`, `determinism_ode`,
   `determinism_special_functions`, `determinism_encoding_roundtrip`,
   `determinism_fastq_parsing`, `determinism_anderson_spectral`

### Provenance Quality

- **Strong:** `validate_features`, `validate_diversity`, `validate_peaks`,
  `validate_barracuda_cpu_v27` — full table with commit, script, date, command
- **Thin:** `validate_cross_primal_pipeline_v98` — only date and command
- Recommend standardizing all validators to the full provenance table format

---

## Open Items for Next Session

1. **Provenance standardization** — audit all 354 binaries for provenance table
   completeness; template the full `{commit, script, date, command, hardware}` tuple
2. **`cargo-llvm-cov`** — run line coverage measurement; target 90% on library code
3. **License field alignment** — resolve `AGPL-3.0-or-later` vs `AGPL-3.0-only`
   per SCYBORG_PROVENANCE_TRIO_GUIDANCE.md
4. **`cargo doc --all-features`** — verify zero doc warnings (build was in progress
   at audit completion; 354 binary targets make this slow)
5. **`reconciliation_gpu`** → request `BatchReconcileGpu` from barraCuda
6. **`ComputeDispatch` migration** — P3 priority, migrate GPU ops from manual BGL
