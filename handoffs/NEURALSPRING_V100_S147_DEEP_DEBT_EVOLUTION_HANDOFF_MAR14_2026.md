# neuralSpring V100 S147 → barraCuda / toadStool: Deep Debt Execution + BarraCUDA Evolution

**Date:** March 14, 2026
**From:** neuralSpring S147 (1115 lib tests, 73 forge tests, 260 binaries, 0 clippy)
**To:** barraCuda, toadStool teams
**Scope:** Deep debt elimination, barracuda evolution, tolerance centralization, provenance completeness
**Supersedes:** V99 S146 Industry GPU Parity Handoff (Mar 12, 2026)
**License:** AGPL-3.0-or-later

---

## Executive Summary

- **Zero inline magic numbers** in production library code — all 13 sites across 8 files centralized to `tolerances::` named constants with doc justifications
- **Zero duplicate math** — `digester_anderson::shannon_diversity` rewired to `barracuda::stats::shannon_from_frequencies`
- **6 provenance records added** for composition experiments (Exp 096–100 + Paper 027)
- **Capability-based discovery** — hardcoded primal names in IPC discovery evolved to `config::` constants
- **All quality gates pass**: fmt, clippy pedantic (0 warnings), 1115/1115 lib tests, 0 doc warnings

---

## For BarraCUDA: Absorption Candidates

### Tolerance Registry Pattern

neuralSpring's `tolerances/mod.rs` (80+ named constants, each with doc justification) is mature enough to extract into a shared `barracuda::tolerances` crate:

| Constant | Value | Cross-Spring Use |
|----------|-------|-----------------|
| `LOG_ZERO_GUARD` | `1e-30` | Shannon, Boltzmann, Dirichlet normalization |
| `EXACT_F64` | `1e-12` | IPR thresholds, denominator guards |
| `NUMERICAL_DISTINCTNESS` | `1e-15` | Level spacing, interpolation guards |
| `CROSS_LANGUAGE` | `1e-6` | Python↔Rust parity |

### Validation Patterns

| Pattern | Location | Absorption Value |
|---------|----------|-----------------|
| `ValidationHarness` (check_abs/check_rel/exit) | `src/validation/mod.rs` | All springs duplicate this |
| `BaselineProvenance` struct | `src/provenance/mod.rs` | Cross-spring provenance |
| `hotSpring` pattern (hardcoded expected, pass/fail, exit 0/1) | All `validate_*` binaries | Standardize |

### Upstream Requests (Carried Forward from V99)

| Request | Priority | Impact |
|---------|----------|--------|
| Softmax pipeline caching | P0 | 24× improvement (170µs → <20µs) |
| Dedicated RFFT WGSL shader | P0 | 700× improvement |
| Fused MHA kernel | P1 | 30× improvement |
| `ops::logsumexp` in HMM | P1 | Eliminate manual implementation |

---

## BarraCUDA Usage: 219 files, 45+ submodules, 80+ functions

neuralSpring exercises BarraCUDA more broadly than any other spring: stats, linalg, ops (bio, fused, reduction), dispatch, esn_v2, nautilus, nn, tensor, device, spectral, shaders. Zero duplicate math remaining.

---

## Code Health After Deep Debt

| Metric | Before (S146) | After (S147) |
|--------|--------------|--------------|
| Inline magic numbers | 13 sites in 8 files | 0 |
| Duplicate math functions | 1 (shannon_diversity) | 0 |
| Missing provenance records | 6 experiments | 0 |
| Hardcoded primal names | 2 sites | 0 |
| Clippy warnings | 0 | 0 |
| Library tests | 1115 | 1115 |
