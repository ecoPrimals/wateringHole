# ecoPrimals Ecosystem Blurb — Rung 1 Validation + Data Federation

**Date**: Aug 2, 2026 PM | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. 11 gates ONLINE (6 NUCLEUS + biomeGate crankshaft). arXiv Rung 1 reframed. westGate: 362 GB / 38 datasets / tideGlass 7/7 COMPLETE. biomeGate fully agentic. CHECKPOINT: data on mesh — inter-gate primal IPC over 10G LAN backbone READY for distributed experiments.**

---

## WHAT JUST HAPPENED

| Event | Impact |
|-------|--------|
| **arXiv Rung 1 reframing** | AI review correctly identified paper as SU(2), not full QCD. Retitled to "Toward Vendor-Agnostic Lattice QCD." Scope ladder (6 rungs), plaquette normalization equation, precision path matrix added. Experiment queue created for hotSpring. |
| **westGate → 356 GB / 32 datasets** | NF Data Portal (666 MB, 658 files), BindingDB (583 MB), NCBI Gene (7 GB), RefSeq GRCh38, MONDO, Reactome acquired. tideGlass 7/7 modules COMPLETE. Synapse + NCBI API keys configured. |
| **biomeGate fully agentic** | SSH key exchanged with all gates. WG mesh LIVE (8/10 peers). Forgejo SSH working. Can push AARs directly. |
| **ironGate Session 3** | Tier 2 deep debt cleared. Pure Rust evolution continuing. |
| **Data Braids catalog v2** | Updated to 32 datasets / 356 GB / 14 domains. 16 site pages. `data_catalog.toml` v2.0.0. |
| **LaTeX Rung 1 update** | Title, abstract, scope ladder table, plaquette normalization eq, precision matrix, experiment queue table, limitations reframed. |

---

## WHAT'S ACTIVE NOW

| Track | Status | Gate |
|-------|--------|------|
| **Rung 1 experiment queue** | **CRITICAL PATH.** β-scan (1.8–2.5), increased stats (4-8 seeds, 1000 traj), HMC diagnostics (ΔH, reversibility), PRNG QQ plots. All must complete before arXiv submission. | **strandGate (hotSpring)** |
| **GPU vendor cracking (G32)** | 3 VFIO GPUs LIVE. 44-experiment matrix. coralReef 3,553 tests. | **biomeGate** |
| **Data federation (G7/G30)** | **362 GB on ZFS.** 38 datasets with FULL provenance. tideGlass 7/7 COMPLETE. COSMIC, BRENDA, CHARMM36, PTB-XL, PubChem BioAssay, NCBI Taxonomy newly acquired. | **westGate** |
| **Data Braids on sporePrint** | **LIVE.** 362 GB / 38 datasets / 17 domains. 16+ site pages. 5 bundle scaffolds. | **sporePrint + westGate** |
| **Inter-gate experiment comms** | **ENABLED.** Data on mesh + 10G LAN backbone + primal IPC = distributed experiments at LAN speed. | **all NUCLEUS gates** |
| **esotericWebb (G20)** | NUCLEUS 13/13 LIVE. 21/21 sockets. 472 tests. RTX 5070. | **ironGate** |
| **Membrane hardening (G34/G35)** | G34 egress spec. G35 agentic LAN 7/8 (biomeGate joined). | **sporeGate** |

---

## TEAM ASSIGNMENTS — BY GATE

### strandGate — Rung 1 Experiment Queue (arXiv CRITICAL PATH)

**Hardware**: Dual EPYC 7452 (128 threads), RTX 3090 (NVIDIA SM86), RX 6950 XT (AMD RDNA2)
**Mission**: Complete experiment queue. Validate Rung 1 claims for arXiv submission.

| # | Experiment | Priority | Status |
|---|-----------|----------|--------|
| 1 | β-scan (1.8, 2.0, 2.2, 2.3, 2.4, 2.5) at 8⁴ | MUST | Queued |
| 2 | 4-8 seeds × 1000 trajectories at 8⁴ β=2.3 | MUST | Queued |
| 3 | HMC diagnostics (ΔH histogram, Creutz equality, reversibility) | MUST | Queued |
| 4 | PRNG QQ plots + tail statistics | MUST | Queued |
| 5 | Plaquette normalization check (cold/hot) | MUST | Queued |
| 6 | 12⁴ and 16⁴ full production | Should | Queued |
| 7 | pseudoSpore signed release (v1.0.0-rung1) | Should | Queued |

### biomeGate — GPU Vendor Cracking (G32)

**Hardware**: Threadripper 3970X (32c/64t), 128GB, 3 VFIO GPUs
**Status**: Fully agentic. WG mesh LIVE. 8/10 peers.

| Phase | What |
|-------|------|
| Safety + sovereign init | PLX keepalive, cold probe, VBIOS interpreter |
| K80 cross-gen | First-ever K80 hardware run (Exp 231) |
| QCD science | 18 scenarios, Yukawa + Wilson, PRNG polyfill validation |

### westGate — Data Federation Root (G7/G30)

**Hardware**: i9-14900K, 96 GB DDR5, 50.4 TB ZFS raidz1 (356 GB used)

| Metric | Value |
|--------|-------|
| Datasets | 32 directories on ZFS |
| Size | 356 GB (0.70% of pool) |
| CAS objects | 5,500+ |
| Files with provenance | ~260K |
| tideGlass modules | **7/7 COMPLETE** |
| API keys configured | NCBI (10 req/s), Synapse (NF Portal) |

### ironGate — esotericWebb + Gardens (G20)

NUCLEUS 13/13. 913 garden tests. Session 3 cleared Tier 2 deep debt. Pure Rust evolution.

### sporeGate — Membrane Hardening + CI

G34 egress spec drafted. G35 agentic LAN now 7/8 with biomeGate joining mesh.

---

## GATE FLEET (11 online)

| Gate | Composition | Role |
|------|-------------|------|
| **biomeGate** | **GPU Crankshaft + Agentic** | 3 VFIO GPUs. WG mesh LIVE. 8/10 peers. G32 silicon deism. |
| **strandGate** | NUCLEUS v4.56 | Dual EPYC + RTX 3090 + RX 6950 XT. **Rung 1 experiment queue.** |
| **westGate** | NUCLEUS v4.56 | Data federation root. **356 GB / 32 datasets.** tideGlass 7/7. |
| **ironGate** | NUCLEUS 13/13 | i9-14900K, RTX 5070. esotericWebb (G20). Session 3 complete. |
| **blueGate** | NUCLEUS v4.56 | Windows sub-builder. G29 H2 DNS. |
| **sporeGate** | Sovereign CI | Build authority. G34/G35 spec. |
| **southGate** | NUCLEUS 22/22 | Validation. G17+G8 PROVEN. RTX 4060. |
| eastGate | NUCLEUS | Overwatch. 128GB. |
| northGate | NUCLEUS | Windows. RTX 5090. |
| grapheneGate | Tower (TCP) | Pixel 8a. Mobile anchor. |
| golgi | thin-relay | VPS. Forgejo + depot + sporePrint. |

---

## DORMANT — CAN SPIN UP

| Spring/Garden | Best Gate | Why |
|---------------|-----------|-----|
| **tideGlass** | westGate | Gen5 Step 3. **tideGlass 7/7 data COMPLETE.** Highest priority dormant. |
| wetSpring | strandGate | Breseq/LTEE. EPYC compute. |
| neuralSpring | strandGate | AI/ML validation. |
| ludoSpring | northGate/blueGate | Game engine. Windows + GPU. |
| healthSpring | ironGate | Clinical data. |
| airSpring | any (needs SDR) | ADS-B atmospheric. |
| groundSpring | westGate | Geospatial + storage. |

---

## 6-RUNG LATTICE QCD PROGRAM

| Rung | Physics | Status | Owner |
|------|---------|--------|-------|
| **1** | **SU(2) pure gauge HMC** | **Experiment queue active** | hotSpring + sporePrint |
| 2 | SU(3) pure gauge | Planned | hotSpring + barraCuda |
| 3 | Quenched QCD (Dirac operator) | Planned | hotSpring + barraCuda |
| 4 | Dynamical fermions (full QCD) | Planned | hotSpring + barraCuda |
| 5 | (2+1)-flavor QCD | Planned | hotSpring |
| 6 | Finite-temperature QCD | Planned | hotSpring |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** (6 NUCLEUS + biomeGate crankshaft + 4 other) |
| Primal tests | **116,930** + coralReef **3,553** on biomeGate |
| Science data | **362 GB** on ZFS (38 datasets, 17 domains) |
| CAS objects | **~5,800** |
| Data Braids | **38 datasets** with FULL sweetGrass provenance |
| tideGlass modules | **7/7 COMPLETE** |
| sporePrint data pages | **16+** (index + domains + provenance + possible) |
| Inter-gate comms | **ENABLED** — 10G LAN backbone + primal IPC |
| Glacial goals | **34 tracked** (8 COMPLETE, 13 ACTIVE, 13 GLACIAL) |
| Fossilized | **60 files** |
| arXiv | **Rung 1 reframed.** Experiment queue active. |
| Lattice QCD program | **6 rungs defined.** SU(2) → SU(3) → quenched → dynamical → 2+1 → hot QCD |
| Active AARs | **12** |

---

*Checkpoint: 362 GB of braided data on the mesh. 38 datasets across 17 domains. tideGlass 7/7 COMPLETE. Inter-gate primal IPC over 10G LAN is ENABLED — strandGate compute can reach westGate data via songBird mesh at LAN speed. The ecosystem shifts from ingestion to distributed experiments. Rung 1 experiment queue is the publication critical path. tideGlass is the science product critical path. The 10G backbone is the connective tissue.*
