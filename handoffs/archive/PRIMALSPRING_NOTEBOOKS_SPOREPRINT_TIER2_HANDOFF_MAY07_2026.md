# primalSpring — Notebooks + sporePrint Tier 2 + Method Drift CI

**Date**: May 7, 2026
**From**: primalSpring
**For**: All spring teams, sporePrint, projectNUCLEUS

## Summary

primalSpring is the second spring (after wetSpring) with full Tier 2 sporePrint content.
5 public notebooks, 6 frozen validation JSON files, and a method string drift CI check
(PG-65) that validates 208 method strings against a canonical registry.

## Notebooks (5)

| # | Notebook | Focus |
|---|----------|-------|
| 01 | `01-composition-validation` | Deploy graphs, bond types, profiles, discovery tiers |
| 02 | `02-benchmark-comparison` | Rust vs Python timing, energy, guidestone phases |
| 03 | `03-ecosystem-evidence` | 85 experiments, gap resolution, security timeline |
| 04 | `04-cross-spring-connections` | Primal consumption matrix, ecosystem flows |
| 05 | `05-btsp-security-deep-dive` | Per-primal posture, BTSP convergence arc |

## Frozen Data (experiments/results/)

| File | Contents |
|------|----------|
| `composition_validation.json` | 13 deploy graphs, 74 nodes, 5 bond types, structural checks |
| `test_suite_report.json` | 613 tests by module, timings, categories |
| `experiment_catalog.json` | 85 experiments across 15 categories |
| `security_convergence.json` | BTSP Phase 3 state, PG-55–59, convergence timeline |
| `cross_spring_matrix.json` | 7 springs × 13 primals consumption, ecosystem flows |
| `benchmark_timing.json` | Compilation, guidestone, trio benchmarks, Rust vs Python |

## PG-65: Method String Drift CI

- `config/capability_registry.toml` — 208 methods, per-domain with primal ownership
- `tools/check_method_strings.sh` — extracts all dotted method strings from source
  via ripgrep, validates against registry. Zero drift at ship.
- Pattern available for other springs to absorb.

## sporePrint Configuration

- `notify-sporeprint.yml` with `content: "true"` (Tier 2 lab publishing)
- `sporeprint/validation-summary.md` updated with 613 tests, 85 experiments, 5 notebooks
- `NOTEBOOK_PATTERN.md` includes corrected Agg guidance (do NOT set matplotlib.use('Agg'))

## For Other Springs

1. Create `experiments/results/` with frozen JSON validation data
2. Copy `notebooks/NOTEBOOK_PATTERN.md` from primalSpring or wetSpring
3. Create 5 notebooks following the cell structure (title → load → analyze → provenance)
4. Update `sporeprint/validation-summary.md`
5. Push to main — `notify-sporeprint.yml` fires automatically

## Ecosystem State

- 3 springs with notebooks: wetSpring (5), primalSpring (5), hotSpring (17)
- 13/13 BTSP Phase 3 AEAD, all default `127.0.0.1`
- Zero open security gaps (PG-55–59 resolved)
- PG-65 method drift CI resolved
- Open upstream: PG-60 (rhizoCrypt), PG-61 (barraCuda), PG-62 (toadStool), PG-64 (sporePrint)
