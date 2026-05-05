# rustChip v0.1.0 — Science Showcase + Glowplug Handoff

**Date:** April 30, 2026
**From:** infra team (rustChip)
**To:** primal teams, spring teams, sporePrint, NUCLEUS composition
**Repo:** [syntheticChemistry/rustChip](https://github.com/syntheticChemistry/rustChip)
**Location:** `infra/rustChip` in the ecoPrimals workspace

---

## Summary

This handoff covers three major additions to rustChip since the 0.1.0 release:

1. **glowplug absorption** — VFIO device lifecycle management (bind, warm boot,
   health check, teardown) absorbed from coralReef's ember/glowplug. rustChip
   now manages its own AKD1000 hardware lifecycle without external orchestrator
   or kernel module.

2. **HW/SW backend separation** — `VfioBackend` [HW] and `SoftwareBackend` [SW]
   are explicitly labeled and never conflated. `BackendSelection` enum and
   `select_backend()` provide the composition entry point for external systems.

3. **Science showcase** — 4 narrative explorations + 5 standalone demo binaries
   reproducing peer-reviewed NPU science claims without external data.

4. **scyBorg licensing** — AGPL-3.0-or-later (code) + ORC (game mechanics) +
   CC-BY-SA 4.0 (creative/docs). Lineage principle: code absorbed from
   ecoPrimals retains full scyBorg license even within the BrainChip symbiotic
   exception boundary.

---

## For hotSpring Team

- **`science_lattice_esn`** reproduces the Hybrid ESN pattern for Lattice QCD
  thermalization steering. This is a standalone proof of the claim from Exp 022:
  sub-millisecond NPU decisions within a simulation loop. Run with
  `cargo run --bin science_lattice_esn` — no external data needed.

- **`WHY_NPU.md`** (`whitePaper/explorations/`) grounds all physics measurements
  in the hardware evidence. It articulates why 54 µs NPU inference matters for
  HMC accept/reject gating and how the hybrid ESN architecture splits compute
  at the natural tanh/FC boundary.

- **`SPRINGS_ON_SILICON.md`** maps the Hybrid ESN pattern across physics
  domains. The pattern table shows how the same ESN reservoir + NPU readout
  architecture applies to thermalization detection, phase classification,
  transport prediction, and Anderson regime identification.

- **`science_precision_ladder`** demonstrates f64 → f32 → int8 → int4
  degradation across science domains. Relevant to hotSpring's tolerance
  budgeting for physics observables.

### What hotSpring should absorb

The ESN reservoir + NPU readout split is the key architectural pattern. When
composing for NUCLEUS, hotSpring's ESN modules should expose a trait-compatible
interface with rustChip's `HybridEsn` — allowing the same reservoir weights to
run on either the hotSpring full-precision path or the rustChip NPU fast path.

---

## For wetSpring Team

- **`science_bloom_sentinel`** reproduces the Streaming Sentinel pattern for
  harmful algal bloom detection. Generates synthetic sensor data (chlorophyll,
  phycocyanin, turbidity, dissolved oxygen), runs continuous NPU classification,
  and reports detection latency. Maps to wetSpring's HAB monitoring work.

- **`science_spectral_triage`** reproduces the Microsecond Gatekeeper pattern
  for LC-MS spectral peak triage. Shows how NPU can reject 90%+ background
  peaks in microseconds, passing only interesting spectra to the full analysis
  pipeline. Maps to wetSpring's metabolomics/proteomics work.

- **Precision Discipline** — the `science_precision_ladder` demo shows how int8
  is sufficient for biology classification tasks while int4 requires careful
  calibration. Relevant for wetSpring's deployment of edge classifiers.

### What wetSpring should absorb

The streaming sentinel pattern (continuous inference on sensor data with alert
thresholds) is directly applicable to any wetSpring monitoring workload. The
key insight: reset ESN state between independent samples for classification
tasks; maintain state only for truly sequential/temporal tasks.

---

## For airSpring Team

- **`science_crop_classifier`** reproduces the Online Adaptation pattern for
  seasonal crop stress classification. Simulates concept drift across growing
  seasons and demonstrates (1+1)-ES weight evolution on NPU SRAM at runtime.
  This is the proof that NPU weights can adapt to distribution shift without
  model retraining or redeployment.

### What airSpring should absorb

The (1+1)-ES online adaptation pattern: a single parent weight vector produces
one mutant per generation; the fitter survivor continues. At 136 gen/sec on
AKD1000 SRAM, this enables field-deployed classifiers to track seasonal drift
autonomously. airSpring's crop monitoring systems should expose a fitness
function interface compatible with `NpuEvolver::evolve()`.

---

## For toadStool Team

- **glowplug is now self-contained in rustChip.** The VFIO lifecycle no longer
  depends on coralReef at runtime. `akida-driver::glowplug` handles bind, warm
  boot, health check, and teardown. The `NpuBackend` trait is stable for
  integration.

- **`BackendSelection` enum** and `select_backend()` are the composition entry
  points. toadStool's dispatch layer can call `select_backend(Auto, ...)` to
  get either `VfioBackend` [HW] or `SoftwareBackend` [SW] based on hardware
  availability.

- **No runtime dependency on coralReef.** The absorbed glowplug code is
  derivative but self-contained. toadStool can depend on `akida-driver` without
  pulling in coralReef.

### What toadStool should absorb

The `NpuBackend` trait with `verify_load()`, `mutate_weights()`, `read_sram()`
extensions is the stable interface. toadStool's `NpuBackendDispatch` enum can
wrap rustChip's backends directly. The `BackendSelection` pattern maps to
toadStool's `select_backend(Auto, ...)` three-tier fallback.

---

## For NUCLEUS Composition

rustChip's `NpuBackend` trait maps to the `capability.register` pattern:

```
capability.register { name: "npu.inference", provider: "rustChip", ... }
capability.register { name: "npu.parse",     provider: "rustChip", ... }
capability.register { name: "npu.convert",   provider: "rustChip", ... }
capability.register { name: "npu.evolve",    provider: "rustChip", ... }
capability.register { name: "npu.warmboot",  provider: "rustChip", ... }
```

- **Sovereign boot** provides warm cycle without external orchestrator — useful
  for NUCLEUS health monitoring and automatic recovery.
- **Science demos** validate NPU claims for sporePrint pages (Nature Preserve,
  Page 27). Each demo is a standalone reproducibility artifact.
- **HW/SW paths are explicit** — NUCLEUS can route to NPU hardware when
  available and fall back to CPU simulation transparently.

---

## For biomeOS / neuralAPI

- **`BackendSelection` enum** and **`select_backend()`** are the composition
  entry points. biomeOS can register rustChip as an NPU capability provider.
- **HW/SW paths are explicit and never conflated.** When biomeOS dispatches
  to NPU, it gets hardware inference; when hardware is unavailable, it gets
  deterministic software simulation.
- **No JSON-RPC server yet** — rustChip is a library + CLI. Integration is
  via library dependency or subprocess invocation. If biomeOS orchestration
  needs a service, a thin JSON-RPC wrapper around `NpuBackend` is the
  recommended next step (following coralReef's UDS JSON-RPC pattern).

---

## Key Files

| Path | What it is |
|------|-----------|
| `crates/akida-driver/src/glowplug.rs` | Sovereign VFIO lifecycle |
| `crates/akida-driver/src/backend.rs` | `NpuBackend` trait + `BackendSelection` |
| `crates/akida-driver/src/backends/software.rs` | `SoftwareBackend` [SW] |
| `crates/akida-driver/src/vfio/mod.rs` | `VfioBackend` [HW] |
| `crates/akida-bench/src/bin/science_*.rs` | 5 science demo binaries |
| `whitePaper/explorations/WHY_NPU.md` | Foundational neuromorphic argument |
| `whitePaper/explorations/SPRINGS_ON_SILICON.md` | 5 patterns × 3 domains |
| `whitePaper/explorations/NPU_FRONTIERS.md` | 10 creative frontiers |
| `whitePaper/explorations/NPU_ON_GPU_DIE.md` | NPU on GPU die analysis |
| `baseCamp/systems/sovereign_boot.md` | Glowplug system documentation |
| `specs/EVOLUTION.md` | Full evolution history |
| `LEVERAGE.md` | Standalone + integrated usage guide |

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 367 |
| Zoo models | 28 |
| Science demo binaries | 5 |
| Narrative explorations | 8 |
| Experiments | 6 |
| Crates | 5 |
| NPs confirmed (Exp 006) | 80 |
| SRAM confirmed (Exp 006) | 10 MB |

---

## Next Steps for rustChip Team

This handoff enables a fresh IDE team to pick up rustChip evolution:

1. **IRQ-based inference completion** — replace polling with `VFIO_DEVICE_SET_IRQS`
2. **Scatter-gather DMA** — large payload support
3. **Reservoir research patterns** — port ensemble and state extraction from toadStool
4. **AKD1500 support** — device ID exists; needs BAR verification
5. **Phase E** — Rust `akida_pcie` kernel module via Linux kernel Rust bindings
