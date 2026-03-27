# hotSpring → Ecosystem: Nautilus Shell Evolution + Adaptive Steering

**Date:** 2026-03-01
**From:** hotSpring v0.6.15
**To:** All springs (ecosystem-wide handoff)
**Scope:** Nautilus Shell self-regulation, AKD1000 readiness, Exp 030 adaptive steering

## What's New

### 1. Nautilus Shell Self-Regulation

The `bingocube-nautilus` crate now has a complete self-regulation loop wired
into `evolve_generation()`:

- **Drift Monitor**: tracks N_e · s each generation. When drift dominates
  selection, auto-applies `IncreaseSelection` (sharpen tournament/elitism)
  or `IncreasePop` (inject fresh random boards)
- **Edge Seeding**: detected concept edges (LOO cross-validation) drive
  directed mutagenesis — bottom 25% of boards replaced with edge-biased boards
- **Audit Trail**: each `GenerationRecord` records `ne_s` and `drift_action`

### 2. AKD1000 Int4 Weight Export

`shell.export_akd1000_weights()` quantizes readout weights to [-8, 7] (int4):
- Per-target dequantization scales and biases
- `predict_dequantized()` for software validation
- Quantization MSE = 0.004 on QCD-like data

### 3. Full Brain Rehearsal (Validated)

End-to-end example validating: drift-monitored evolution → concept edges →
edge-seeded re-evolution → AKD1000 export → save/restore (bit-perfect) →
instance transfer + merge → production reset.

### 4. Exp 030: Fixed Adaptive Steering

Exp 029's adaptive steering had a guard bug preventing NPU point insertion.
Fixed: NPU now inserts up to `--max-adaptive=12` points across the full
measured range. Bootstrapped from 29 data points (Exps 024+028+029).

## Cross-Spring Relevance

| Spring | What to absorb |
|--------|---------------|
| **wetSpring** | Drift monitor pattern for Anderson localization ESN; edge seeding for disorder boundary detection |
| **airSpring** | AKD1000 int4 export path for agricultural NPU models |
| **neuralSpring** | Evolutionary reservoir as alternative to backprop for surrogate learning |
| **groundSpring** | Concept edge detection (LOO CV) as uncertainty quantification tool |
| **toadStool** | Detailed absorption handoff in hotSpring/wateringHole/handoffs/ |

## Crate Coordinates

```
primalTools/bingoCube/nautilus/
  31 tests, 5 examples
  Key files: src/shell.rs, src/constraints.rs, src/evolution.rs, src/readout.rs
  Cargo.toml: bingocube-nautilus v0.1.0
```

## Validation

- 31 unit tests pass
- 5 examples run clean (including full_brain_rehearsal end-to-end)
- Blind Exp 029 prediction: 2.6% CG error (never trained on dynamical data)
- State persistence: bit-perfect prediction match after save/restore

## Addendum: NPU Parameter Controller (2026-03-01)

Exp 030 revealed NPU parameter suggestions were logged but not applied (dt=0.0032,
97.5% acceptance). Exp 031 closes the feedback loop: the NPU now controls dt/n_md
per-beta with mid-beta acceptance-driven adaptation. The ESN trains to target 70%
acceptance using actual dt_used. The brain architecture now has a complete
observe → predict → apply → retrain cycle.

See: `hotSpring/wateringHole/handoffs/HOTSPRING_V0615_NPU_PARAM_CONTROL_TOADSTOOL_HANDOFF_MAR01_2026.md`
