# hotSpring Interstadial Sprint — Handoff (May 11, 2026)

**From:** hotSpring (syntheticChemistry/hotSpring)
**To:** primalSpring coordination, upstream primal teams, sibling springs, projectNUCLEUS, foundation, lithoSpore

---

## Summary

hotSpring completed the interstadial sprint targets from the river delta
evolution guidance. All three priorities addressed. hotSpring is now the
**3rd spring qualifying for the Tier 4 IPC-first exit gate** (with
groundSpring and healthSpring).

**Current metrics:** 576 lib tests (default / IPC-first) / 1,025 lib
tests (barracuda-local), zero clippy warnings, 189 experiments, 7
validation scenarios, 7 deploy graphs, guideStone L6 CERTIFIED.

---

## What changed

### Priority 1: Tier 4 IPC-First Defaults — DONE

`barracuda/Cargo.toml` `default` changed from `["barracuda-local"]` to `[]`.
Bare `cargo build` now produces an IPC-only binary with no barracuda
library linkage. Local compute is opt-in via `--features barracuda-local`.

- 576 tests pass in default (IPC-first) mode
- 1,025 tests pass with `--features barracuda-local`
- hotSpring qualifies for Pillar 5 Tier 4 exit gate

### Priority 2: metalForge/forge Decoupling — DONE

`metalForge/forge/Cargo.toml` barracuda dependency made `optional = true`
behind `barracuda-local` feature. `bridge` module conditionally compiled
with `#[cfg(feature = "barracuda-local")]`. Both default and barracuda-local
builds compile and pass clippy.

### Priority 3: LTEE B2 Anderson — STARTED (Tier 1)

Created `notebooks/papers/13-ltee-anderson-fitness.ipynb` — Python Tier 1
baseline for Wiser et al. 2013. Maps LTEE fitness increments to Anderson
disorder potential, applies level spacing ratio diagnostics (⟨r⟩), sliding
window localization analysis, 12-population variance.

- Expected values JSON produced for lithoSpore module 7 (anderson)
- Exp 189 added to EXPERIMENT_INDEX
- B2 marked STARTED in PAPER_REVIEW_QUEUE
- B9 (DFE ↔ RMT) annotated as depending on B2

### Deep Debt Cleanup

- **`#[allow]` → `#[expect(reason)]`** across 9 modules (production + test)
- **Magic numbers → named constants:** `MD_REPORT_CADENCE` (5 MD modules),
  `DYNAMICAL_CG_MAX_ITER` referenced in 10 config defaults
- **NPU discovery:** `$NPU_DEVICE_DIRS` env override for device node paths
- **2 clippy warnings resolved:** `suspicious_arithmetic_impl` (complex div),
  `unnecessary_wraps` (bisect fallback)

---

## For upstream primal teams

### barraCuda
- hotSpring now uses `barracuda` as `optional = true` in both `barracuda/`
  and `metalForge/forge/`. The `dep:barracuda` syntax + `barracuda-local`
  feature gate is the canonical pattern. Other springs should follow.
- `DYNAMICAL_CG_MAX_ITER` is defined in hotSpring's `tolerances/lattice.rs`
  but the same constant should live in barraCuda upstream for cross-spring
  sharing.

### toadStool
- metalForge/forge `probe_gpus()` uses `wgpu` directly (not via barracuda)
  for GPU enumeration. When toadStool absorbs NPU substrate support,
  `probe_npus()` and the `$NPU_DEVICE_DIRS` env cascade should migrate
  upstream.

### nestGate — HIGH PRIORITY UPSTREAM
- Still not live for data chains. LTEE B2 expected values JSON has no
  BLAKE3 content hash. Foundation Thread 2 source anchors have empty
  `blake3` and `retrieved` fields. Next evolution round requires live
  nestGate for end-to-end provenance.

### squirrel
- JH-0 method gate shipped (pulled in this sprint). hotSpring's
  `squirrel_client.rs` is ready for `method.gate` calls when the
  ecosystem wires the gate validation loop.

---

## For sibling springs

### Tier 4 IPC-First Pattern

The ecosystem needs 4+ springs with `default = []` (no barracuda linkage).
Current qualifying: groundSpring, healthSpring, **hotSpring** (new).
Need 1 more from: wetSpring, neuralSpring, airSpring.

Pattern reference:
```toml
[features]
default = []
barracuda-local = ["dep:barracuda"]
```

Key steps:
1. Make barracuda `optional = true` in `[dependencies]`
2. Flip `default` from `["barracuda-local"]` (or similar) to `[]`
3. Gate all barracuda-importing code behind `#[cfg(feature = "barracuda-local")]`
4. Gate barracuda-dependent tests similarly
5. Verify: `cargo test --lib` (IPC-only subset) + `cargo test --lib --features barracuda-local` (full)

### metalForge/forge Decoupling

If your spring has a `metalForge/forge` or similar hardware discovery crate
with a hard barracuda path dep, make it optional too. Pattern:
```toml
barracuda = { path = "...", optional = true }
[features]
barracuda-local = ["dep:barracuda"]
```
Gate the bridge/device-creation module behind the feature.

### LTEE B2 Anderson Pattern

For springs with LTEE assignments: the notebook pattern in
`notebooks/papers/13-ltee-anderson-fitness.ipynb` shows how to create a
Tier 1 Python baseline that maps physics infrastructure (spectral theory,
level statistics) to biological data. Each spring's existing physics
primitives can be reused — the gap is the biological data mapping and
expected values JSON for lithoSpore.

---

## For lithoSpore

- **Module 7 (anderson):** hotSpring Exp 189 produces
  `experiments/results/ltee/ltee_b2_anderson_expected.json` with:
  - Wiser power-law model parameters (α, β from Table S2)
  - Anderson diagnostics (full trajectory ⟨r⟩, population mean/std,
    effective disorder W, sliding window early/late ⟨r⟩)
  - 5 validation checks (power-law no plateau, diminishing returns,
    ⟨r⟩ between GOE/Poisson, population variance, 12 replicates)
- **Tier 2 target:** `validate_ltee_anderson` Rust scenario using
  `barracuda::spectral` — not yet implemented.

---

## For projectNUCLEUS

- No new workload TOMLs needed from this sprint. Existing
  `hotspring-md-validation.toml` (sarkas-yukawa-md) is current.
- LTEE B2 is Tier 1 only (notebook) — no NUCLEUS workload until Tier 2.

---

## Remaining hotSpring items (not blocking ecosystem)

| Item | Severity | Owner |
|------|----------|-------|
| LTEE B2 Tier 2 (Rust scenario) | Future | L3 |
| LTEE B9 (DFE ↔ RMT) Tier 1 | Future (depends on B2) | L3 |
| nestGate BLAKE3 for foundation sources | Blocked | L1 (nestGate) |
| TensorSession migration (deprecated GPU HMC) | Low | L3 + barraCuda |
| Paper queue Tier 4 (WDM papers 32-42) | Future | L3 |
| Sovereign GPU barriers (Titan V, K80) | Low | L3 + coralReef |
