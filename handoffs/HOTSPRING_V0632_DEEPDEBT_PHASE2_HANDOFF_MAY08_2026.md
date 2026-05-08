# hotSpring v0.6.32 — Deep Debt Evolution Phase 2 Handoff

**Date:** May 8, 2026
**Spring:** hotSpring v0.6.32
**Test count:** 1002 lib tests (up from 993), 166 binaries, 128 WGSL shaders

---

## Summary

Comprehensive deep-debt resolution across 8 execution waves:

1. **Downstream audit** — Cloned `projectNUCLEUS` and `foundation` to
   `gardens/`, audited integration patterns, created `docs/DOWNSTREAM_PATTERNS.md`
2. **Smart refactoring** — 3 large files split into submodules (pseudofermion
   Hasenbusch, NPU handlers by concern, nuclear EOS display). single_beta.rs
   (953L) left intact — monolithic orchestration function, splitting would
   degrade readability.
3. **Unsafe evolution** — `exp070_register_dump.rs` mmap wrapped in
   `SafeBarMapping` struct with RAII `Drop` impl and bounds-checked accessors
4. **Hardcoding elimination** — toadstool socket resolution migrated to
   `niche::socket_dirs()`, deprecated primal_bridge accessors stripped of
   hardcoded name fallbacks, ember socket paths confirmed acceptable (already
   use FleetDiscovery)
5. **Test coverage** — 9 new unit tests (primal_bridge, receipt_signing),
   3 new integration tests (dielectric, spectral, lattice QCD)
6. **Benchmark gaps** — Nuclear EOS and spectral domains added to
   `validate_barracuda_cpu_gpu_parity` (8 domains total)
7. **Paper queue** — Paper 45 `kinetic_fluid_control.json` committed, frozen
   greenboard JSON created, Tier 4 binaries verified (`validate_fpeos` 18/19,
   `validate_atomec` 7/9)
8. **Documentation** — README, CHANGELOG, PRIMAL_GAPS, PAPER_REVIEW_QUEUE
   updated. This handoff written.

---

## New Gaps for Upstream

| ID | Description | Owner |
|----|-------------|-------|
| GAP-HS-046 | Average-atom SCF charge conservation (2/9 failures) | hotSpring physics |
| GAP-HS-047 | projectNUCLEUS workload binary name mismatch | projectNUCLEUS |

---

## Validation

```
cargo test --lib               # 1002 passed, 6 ignored
cargo test --test integration_dielectric   # 5 passed
cargo test --test integration_spectral     # 3 passed
cargo test --test integration_lattice      # 4 passed
cargo clippy --lib              # clean
validate_fpeos                  # 18/19 (advisory thermo consistency)
validate_atomec                 # 7/9 (charge conservation, density monotonicity)
```

---

## Files Changed

### New files
- `docs/DOWNSTREAM_PATTERNS.md`
- `barracuda/src/lattice/pseudofermion/hasenbusch.rs`
- `barracuda/src/production/npu_worker/handlers/{mod,precompute,thermalization,inference,proxy}.rs`
- `barracuda/src/nuclear_eos_helpers/display.rs`
- `barracuda/tests/integration_dielectric.rs`
- `barracuda/tests/integration_spectral.rs`
- `barracuda/tests/integration_lattice.rs`
- `experiments/results/papers/parity_greenboard_frozen_20260508.json`
- `experiments/results/papers/README.md`
- `control/kinetic_fluid/results/kinetic_fluid_control.json`

### Modified files
- `barracuda/src/bin/exp070_register_dump.rs` — SafeBarMapping wrapper
- `barracuda/src/bin/validate_barracuda_cpu_gpu_parity.rs` — +2 domains
- `barracuda/src/toadstool_report.rs` — socket resolution
- `barracuda/src/primal_bridge.rs` — deprecated fallback removal + tests
- `barracuda/src/receipt_signing.rs` — tests added
- `barracuda/src/lattice/pseudofermion/mod.rs` — Hasenbusch extraction
- `barracuda/src/nuclear_eos_helpers/mod.rs` — display extraction
- `README.md`, `CHANGELOG.md`, `docs/PRIMAL_GAPS.md`, `specs/PAPER_REVIEW_QUEUE.md`
