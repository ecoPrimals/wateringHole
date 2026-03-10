# ToadStool S140 — Deep Debt Evolution & Spring Absorption Sprint

**Date**: March 10, 2026
**Session**: S140
**Branch**: master
**QA**: `cargo fmt` ✓ | `cargo clippy -- -D warnings` ✓ | `cargo test --workspace` ✓

## Summary

S140 focused on deep debt evolution across the toadStool codebase:
eliminating hardcoded primal names, enriching streaming dispatch with
healthSpring's callback pattern, wiring barraCuda Sprint 2 APIs as
JSON-RPC methods, and smart-refactoring the largest production file.

## Changes

### Hardcoding Elimination (7 files)

All remaining production hardcoded primal names and paths evolved to
`interned_strings::primals::*` constants:

- `beardog_impl/adapters.rs`: `"beardog"` → `primals::BEARDOG`
- `unibin/format.rs`: `"toadstool.sock"` → `format!("{name}.sock")`
- `sandbox/types.rs`: `"toadstool"` → `primals::TOADSTOOL`
- `primal_capabilities.rs`: config dir + self-knowledge
- `display/ipc/platform.rs`: socket discovery path
- `cli/main.rs`: binary name fallback
- `zero_config/discovery.rs`: peer discovery name

### StreamingDispatchContext Enrichment

Absorbed healthSpring V13 `execute_streaming()` callback pattern:
- `StageProgress`: per-stage progress report
- `ProgressCallback`: `Box<dyn FnMut(&StageProgress) + Send>`
- `with_progress()`: builder for attaching progress callbacks
- `record_dispatch_with_progress()`: fires callback per stage
- 4 new unit tests

### barraCuda Sprint 2 API Awareness

3 new JSON-RPC methods:
- `science.activations.list`: 7 activation functions + batch variants
- `science.rng.capabilities`: CPU LCG + GPU xoshiro128** PRNG
- `science.special.functions`: 6 special math functions (eigensolver,
  plasma physics, pharmacology)

### Smart Refactoring

- `science.rs`: 1,139 → 828 LOC via extraction to `science_domains.rs`
  (ecology, discovery, deploy domain routing + `forward_to_primal`)

## What Other Primals Should Know

1. **New JSON-RPC methods available**:
   - `science.activations.list` — query available activation functions
   - `science.rng.capabilities` — query PRNG algorithms
   - `science.special.functions` — query special math functions
2. **Spring pins updated** to S140 in `SPRING_ABSORPTION_TRACKER.md`
3. **healthSpring V13** now tracked as a spring with pin status

## Dependencies

- No new crate dependencies
- No breaking API changes
- Existing JSON-RPC methods unchanged
