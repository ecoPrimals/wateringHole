# sporePrint Blurb — Rung 1 Validation + Data Braids v2

**Date**: Aug 2, 2026 PM | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: arXiv reframed to "Toward Vendor-Agnostic Lattice QCD" (Rung 1 of 6). Experiment queue ACTIVE — β-scan, HMC diagnostics, increased stats must complete before submission. Data Braids updated: 356 GB / 32 datasets / 14 domains. LaTeX updated with Rung 1 corrections.

---

## WHAT JUST HAPPENED

| Event | Status |
|-------|--------|
| **arXiv Rung 1 reframing** | AI review was right: SU(2), not QCD. Paper retitled, scope ladder added, precision matrix added, 16⁴ overclaims removed, limitations reframed. |
| **LaTeX updated** | Title, abstract, Section 1.2 (scope ladder), plaquette normalization eq (Section 2.1), precision matrix (Section 2.2), experiment queue table (Section 4.4), conclusion reframed. |
| **Experiment queue created** | 7 experiments for hotSpring: β-scan, increased statistics, HMC diagnostics, PRNG isolation, plaquette normalization, larger volumes, pseudoSpore freeze. |
| **6-rung ladder defined** | SU(2) → SU(3) → quenched QCD → dynamical fermions → (2+1)-flavor → hot QCD. Each rung gets its own preprint. |
| **Data Braids v2** | Updated catalog to 356 GB / 32 datasets / 14 domains. 16 site pages (4 new domain pages). westGate tideGlass 7/7 COMPLETE. |
| **Phase 1-3** | COMPLETE: nav triage, pseudoSpore section, dashboards, hype cleanup, `/data/` section. |

---

## CRITICAL PATH: Rung 1 arXiv Submission

```
Experiment queue (strandGate/hotSpring)
    ↓  β-scan, HMC diagnostics, increased stats, PRNG QQ plots
sporePrint integrates data into paper tables
    ↓  update LaTeX with experiment results
Final hype compliance review
    ↓
arXiv hep-lat submission (cross-list cs.DC)
    ↓
Update site with arXiv ID + pseudoSpore v1.0.0-rung1
```

### What sporePrint is Waiting For

| Experiment | From | Priority | What sporePrint Does With It |
|-----------|------|----------|------------------------------|
| β-scan (1.8–2.5) | hotSpring/strandGate | MUST | New table in Section 3 — validates engine across coupling range |
| 4-8 seeds × 1000 traj | hotSpring/strandGate | MUST | Replace N_eff=30 with bootstrap errors |
| HMC diagnostics | hotSpring/strandGate | MUST | New ΔH histogram figure, Creutz equality number |
| PRNG QQ plots | hotSpring/strandGate | MUST | Quantify GPU polyfill defect rigorously |
| 12⁴ / 16⁴ production | hotSpring/strandGate | Should | Extend scaling table or restrict claims |

### What sporePrint Can Do Now (while waiting)

- Final hype compliance pass on current LaTeX
- WCAG 2.2 AAA accessibility audit
- Begin Rung 2 paper scaffold (SU(3) pure gauge) when barraCuda starts
- Regenerate site pages as experiment data arrives
- Populate pseudoSpore bundles with westGate data

---

## DATA BRAIDS — `/data/` (v2)

356 GB across 32 datasets in 14 science domains. All with full Provenance Trio provenance on westGate.

**New datasets since v1**: UniProt TrEMBL (148 GB), PDB70 (27 GB), BindingDB (583 MB), NF Data Portal (666 MB), GEO SOFT cancer (3 GB), TCGA Xena (449 MB), MONDO (103 MB), Reactome (96 MB), RefSeq GRCh38 (981 MB), NCBI Gene (7 GB).

**New domain pages**: Cancer Genomics, Disease Ontology, Genomic Reference, plus updates to Structural Biology, Drug Discovery, Gene Expression.

**tideGlass 7/7 COMPLETE** — all base data modules have data on ZFS with provenance.

---

## REMAINING WORK

| Task | Owner | Priority |
|------|-------|----------|
| **Rung 1 experiment queue completion** | hotSpring (strandGate) | **CRITICAL** — blocks arXiv |
| **Integrate experiment data into LaTeX** | sporePrint | **HIGH** — after experiments |
| Bundle data population | westGate | HIGH |
| Bundle upload to depot | sporePrint + lithoSpore | HIGH |
| pseudoSpore v1.0.0-rung1 signed release | Node Atomic | MEDIUM |
| Live dashboards → petalTongue (G19) | petalTongue | MEDIUM |
| Rung 2 paper scaffold | sporePrint | LOW (after Rung 1 submits) |
| WCAG 2.2 AAA | sporePrint | LOW |

---

## KEY INSIGHT

The AI review pattern holds for the third time: **the code is real, the comparisons are hype.** The engineering (plaquette values, precision, multi-vendor, provenance) all checked out. The framing (calling it "lattice QCD," claiming 16⁴ production) was the problem. Fix: name what you proved, not what you plan to prove. Rung 1 is SU(2) execution and arithmetic validation. That's a strong preprint on its own merits.

---

*Rung 1 reframed. LaTeX updated. Experiment queue is the critical path — sporePrint waits for hotSpring data, then integrates and submits. Data Braids doubled to 356 GB / 32 datasets. The 6-rung lattice QCD ladder gives the research program structure. Each rung gets its own paper.*
