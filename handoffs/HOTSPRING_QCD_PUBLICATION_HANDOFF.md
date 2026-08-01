# Handoff: hotSpring QCD → arXiv Publication

**Date**: Aug 1, 2026 | **Wave**: post-155n
**From**: sporePrint team | **To**: hotSpring team (strandGate)
**Pattern**: `wateringHole/protocols/PUBLICATION_PIPELINE_STANDARD.md`

---

## TL;DR

sporePrint has scaffolded an arXiv paper draft and pseudoSpore site page for the
SU(2) lattice QCD results on consumer GPU. **The structure, benchmarks, and
framing are done.** The hotSpring team needs to fill 5 data sections marked
`[TODO]` in the draft. When those are filled, the paper is ready for submission.

This is the first ecoPrimals publication under ORCID 0009-0004-2141-0321.

---

## What's Already Done (sporePrint owns)

| Deliverable | Location | Status |
|-------------|----------|--------|
| arXiv draft (structure) | `whitePaper/subGen/LATTICE_QCD_CONSUMER_GPU_ARXIV.md` | DONE |
| pseudoSpore site page | `sporeprint.primals.eco/pseudospore/hotspring-qcd-su2/` | LIVE |
| Verification guide | `sporeprint.primals.eco/pseudospore/verify/` | LIVE |
| Data catalog page | `sporeprint.primals.eco/pseudospore/` | LIVE |
| GPU compute page | `sporeprint.primals.eco/lab/gpu-compute-live/` | LIVE |
| Publication pipeline standard | `wateringHole/protocols/PUBLICATION_PIPELINE_STANDARD.md` | DONE |

---

## What hotSpring Needs to Deliver

### 1. Plaquette Measurements (Section 3.2)

**What**: Average plaquette ⟨P⟩ values at specified β for each lattice volume.

**Format** — fill this table:

```markdown
| Lattice | β   | ⟨P⟩ (DF64 GPU) | ⟨P⟩ (f64 CPU) | |Δ| / σ | Trajectories | Thermalization |
|---------|-----|-----------------|----------------|---------|--------------|----------------|
| 8^4     | 2.3 |                 |                |         |              |                |
| 16^4    | 2.3 |                 |                |         |              |                |
```

**Why**: Standard validation in every lattice paper. Reviewers will check ⟨P⟩
against known Wilson action results. The GPU vs CPU comparison proves DF64
precision is sufficient for physics observables.

**How to produce**: Run production HMC at β=2.3, measure plaquette after
thermalization, compute mean + standard error. Compare DF64 GPU values
against f64 CPU reference values computed on the same configurations.

---

### 2. DF64 vs f64 Precision Comparison (Section 3.3)

**What**: ULP (Unit in Last Place) analysis comparing DF64 arithmetic against
native f64 reference on the same inputs.

**Format** — fill this table:

```markdown
| Operation        | Max |Δ| (ULP) | Mean |Δ| (ULP) | Digits Agreement |
|------------------|----------------|----------------|------------------|
| Addition         |                |                |                  |
| Multiplication   |                |                |                  |
| Division         |                |                |                  |
| SU(2) multiply   |                |                |                  |
| Plaquette accum  |                |                |                  |
```

**Why**: Establishes the precision floor. Reviewers need to know exactly how
many digits DF64 preserves for each operation class.

**How to produce**: Run the same sequence of operations in DF64 (GPU) and
native f64 (CPU). Compare bit-for-bit. Report max and mean ULP deviation.

---

### 3. Autocorrelation Analysis (Section 3.5)

**What**: Integrated autocorrelation time τ_int for the plaquette observable
at each lattice volume.

**Format** — fill this table:

```markdown
| Lattice | β   | τ_int (plaquette) | Effective independent configs | Method |
|---------|-----|-------------------|------------------------------|--------|
| 8^4     | 2.3 |                   |                              |        |
| 16^4    | 2.3 |                   |                              |        |
```

**Why**: Autocorrelation determines how many trajectories are needed for
independent measurements. Critical for error bar validity.

**How to produce**: Standard Γ-method or binning analysis on plaquette
time series. Madras-Sokal or Wolff windowing algorithm.

---

### 4. Multi-Vendor Benchmarks (Section 3.4)

**What**: Same lattice scaling benchmarks on non-NVIDIA GPUs.

**Format** — fill this table:

```markdown
| GPU           | Architecture | VRAM  | GPU ms/traj (8^4) | GPU ms/traj (16^4) |
|---------------|-------------|-------|--------------------|--------------------|
| RTX 3090      | SM86        | 24 GB | 25.8 (done)        | 625.9 (done)       |
| RTX 4060      | SM89        | 8 GB  |                    |                    |
| RTX 5090      | SM100       | 32 GB |                    |                    |
| RX 6950 XT    | RDNA2       | 16 GB |                    |                    |
```

**Why**: The paper's key claim is vendor neutrality. At minimum one AMD
result is needed. Intel Arc would strengthen the argument but is optional.

**Owner**: This may require Node Atomic team coordination if AMD hardware
is on a different gate. RTX 4060/5090 results can come from any gate with
those GPUs.

---

### 5. Thermalization Figure (Optional but Strong)

**What**: Plot of plaquette value vs trajectory number showing convergence
from hot start to equilibrium.

**Format**: SVG or high-res PNG. X-axis: trajectory number. Y-axis: ⟨P⟩.
Show thermalization region and production region with a vertical line.

**Why**: Visual proof of correct HMC behavior. Reviewers expect this.

---

## How to Fill the Draft

1. Open `whitePaper/subGen/LATTICE_QCD_CONSUMER_GPU_ARXIV.md`
2. Search for `[TODO]` — there are 5 markers
3. Replace `[pending]` cells with measured values
4. Remove the `[TODO]` marker line when the section is complete
5. Commit to whitePaper main and push to Forgejo
6. File a completion AAR in `wateringHole/aars/`

**Do not change the structure.** The sections, headings, and table columns
are already formatted for the target venue. Just fill the data cells.

---

## Hype Cleanup Reminders

These rules apply to every number in the paper:

- **GPU vs CPU speedup**: Always specify "same hardware, same algorithm"
- **DF64 precision**: Say "~14 significant digits" not "f64 precision"
- **No theoretical TFLOPS**: Use measured trajectories/hour
- **Accept rates**: Report actual measured rates, not theoretical
- **Error bars**: Standard error of the mean, not standard deviation

---

## Publication Path

```
hotSpring fills [TODO] sections
    ↓
sporePrint reviews for hype compliance
    ↓
Convert markdown → LaTeX (standard REVTeX4-2 template)
    ↓
Submit to arXiv hep-lat (cross-list cs.DC)
    ↓
sporePrint updates site page with arXiv ID
    ↓
JOSS submission (software paper) after arXiv acceptance
```

**Target venues**:
- **arXiv hep-lat** — primary (lattice QCD audience)
- **cs.DC** — cross-list (distributed computing / GPU methodology)
- **JOSS** — secondary (software paper for the barraCuda + coralReef stack)
- **Computer Physics Communications** — stretch (if reviewers want journal)

---

## Contact

sporePrint team monitors this handoff. When hotSpring data is ready,
push to whitePaper and file AAR. sporePrint will review within 24 hours
and prepare the LaTeX conversion.

---

*First publication for ecoPrimals ORCID. The scaffold is ready.
The engineering is proven. The physics data completes the paper.*
