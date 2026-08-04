# tideGlass Wave 156b — Full Rust Rebuild + Deep Debt Resolution

**Date**: Aug 3–4, 2026
**Gate**: westGate (Data NAS)
**Wave**: 156b
**Primal**: tideGlass
**Repo**: `protoKarya/tideGlass`

---

## Summary

Full Rust rebuild of tideGlass from Phase 0 doc scaffold to Phase 4
production-ready UniBin. Seven science modules implemented as library crates
composing into a single `tideglass` binary with UDS JSON-RPC 2.0 server.
176 tests, zero clippy warnings, zero TODOs. G56 Neural API routing
(`neural-api-default.sock`) with direct fallback. Provenance convergence gate
for mixed-state data on westGate. CAS wiring live with graceful degradation.
All 21 transitive dependencies verified pure Rust. Documentation fully
reconciled. Ready for westGate cell boot.

## Crate Architecture

| Crate | Purpose |
|-------|---------|
| `tideglass-core` | `PRIMAL_NAME`, `count_as_f64`, Arc\<str\> newtypes, KS enrichment, permutation p-values, IPC types, CAS types, capability discovery, error handling |
| `tideglass-rges` | RGES pipeline: enrichment → BH-FDR correction → compound ranking |
| `tideglass-rcl` | Representative cell line selection via signal-to-noise ratio |
| `tideglass-gps4drug` | Structure-to-expression prediction (linear regression from molecular features) |
| `tideglass-screen` | Compound library + Lipinski Rule of Five + structural alert filtering |
| `tideglass-molsearch` | Monte Carlo Tree Search molecular optimization (UCB1, 5 action types) |
| `tideglass-octad` | Benchmark evaluation: AUC, precision/recall, F1, concordance correlation |
| `tideglass-nf` | NF1 tissue-weighted reversal scoring with compartment geometry |
| `tideglass-bin` | UniBin: UDS JSON-RPC server, dispatch router, CAS client, health triad, CLI |

## IPC Methods (11 implemented)

| Method | Module |
|--------|--------|
| `capabilities.list` | core/bin |
| `health.liveness` | bin |
| `health.check` | bin (reports CAS routing + convergence) |
| `health.readiness` | bin (reports CAS routing + convergence) |
| `science.rges_screen` | rges |
| `science.rcl_select` | rcl |
| `science.gps4drug_predict` | gps4drug |
| `science.compound_screen` | screen |
| `science.mcts_optimize` | molsearch |
| `science.octad_benchmark` | octad |
| `science.nf_score` | nf |

## CAS Integration

- Neural API routing: `NEURAL_API_SOCKET` → `neural-api-default.sock` → `neural-api.sock` → direct fallback
- `CasClient` over UDS: `content.get`, `content.exists`, `content.list`, `content.put`
- `load_from_cas()` on server startup with graceful degradation
- `store_pipeline_result()` for provenance write-back
- `is_dataset_converged()` gate for mixed provenance states
- 6 divergences documented (DIV-1→6) in CAS AAR handoff

## Deep Debt Completed

### Identity & Constants
- `PRIMAL_NAME` centralized in `tideglass-core` — single source of truth
- `count_as_f64()` replaces 17 scattered `#[allow(clippy::cast_precision_loss)]`
- Zero hardcoded gate names, port numbers, or primal socket paths

### Code Quality
- `#![forbid(unsafe_code)]` on all 9 crates
- `clippy::pedantic` + `clippy::nursery` — zero warnings
- Zero `.unwrap()` in production code
- Zero TODO/FIXME/HACK markers
- All string IDs use `Arc<str>` newtypes (zero-copy)
- `thiserror` for all error types

### Dependencies
- 6 direct: serde, serde_json, thiserror, rand, tokio, base64
- 21 total transitive — all pure Rust, no C FFI
- `cargo deny` clean: advisories, bans, licenses, sources

### Documentation
- All root docs reconciled: README, CONTEXT, CHANGELOG, CONTRIBUTING, SECURITY
- All specs reconciled: ARCHITECTURE, MODULE_SPECS, DATA_ACCESS, VISUALIZATION
- Repo URL corrected to `protoKarya/tideGlass` across all files
- `scope.toml` pending comments cleaned to `awaiting` format
- `validation/README.md` updated with current test count

## Metrics

| Metric | Value |
|--------|-------|
| Rust source files | 32 |
| Total LOC | ~7,000 |
| Largest file | dispatch.rs (611 lines, 270L code + 340L tests) |
| External deps | 6 direct, 21 transitive |
| Test count | 176 |
| Clippy warnings | 0 |
| Unsafe code | forbidden |

## Phase 4 Blockers (Not tideGlass)

1. **biomeOS cell boot on westGate** — first cell composition deploy
2. **GPS NumPy/pickle → JSON** — data team conversion task
3. **Chen 2017 benchmark** — RGES correlation target r >= 0.52 (needs converted data)
4. **Provenance write chain** — rhizoCrypt → loamSpine → sweetGrass (needs NUCLEUS primals)

## Upstream Review Requests

- **overwatch**: Audit 176-test UniBin for deployment readiness
- **nestGate team**: Canonical Rust CAS client crate for ecosystem (DIV-5)
- **biomeOS**: Review `tideglass_cell.toml` for live cell boot
- **westGate data team**: GPS NumPy/pickle → JSON conversion priority
