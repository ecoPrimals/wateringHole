# ecoPrimals Ecosystem Blurb — Primal Infrastructure Frontloaded

**Date**: Aug 3, 2026 AM | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. 11 gates ONLINE. PRIMAL WORK FRONTLOADED — barraCuda subgroup fix unmerged, inter-gate content.get E2E untested, G31 batch provenance pending, G18 squirrel dispatch unwired. Springs-to-NUCLEUS mesh COMPLETE (cell graphs v2.0.0, deploy graphs v2.0.0). Gauge group mismatch (SU(3) code / SU(2) paper) blocks arXiv. 362 GB / 38 datasets / 17 domains.**

---

## PRIMALS THAT NEED WORK

Infrastructure that must land before springs can run distributed science at production quality.

### P0 — Blocks Active Science

| # | Primal | What | Unblocks | Size |
|---|--------|------|----------|------|
| 1 | **barraCuda** | Merge subgroup reduction shader fix (`sum_reduce_subgroup_f64.wgsl` entry point `fn main()` → `fn sum_reduce_f64()`). GPU scalar readbacks return **0.0** on SM100+ devices. Verified on biomeGate but **not merged upstream**. | hotSpring QCD production on biomeGate, G32 cross-vendor, all GPU springs on newer GPUs | **S** |
| 2 | **barraCuda** | GPU PRNG pipeline: composed shader duplicate-definition bug (all-zero output), 9.5% kinetic energy deficit from polyfill `log_f64`/`sqrt_f64`/`cos_f64`. `cpu_mom` workaround deployed. | Full GPU HMC path, throughput claims, G32 validation | **L** |
| 3 | **barraCuda** (paper) | Gauge group relabeling — code is **SU(3)** throughout (`Su3Matrix`, `Re Tr/3`, `β/3`). Paper says SU(2). ⟨P⟩≈0.15 is correct SU(3) at β=2.3. Paper, site pages, audit trail must be corrected. | G9 arXiv submission, sporePrint credibility | **M** |

### P1 — Spring Mesh & Data Access

| # | Primal | What | Unblocks | Size |
|---|--------|------|----------|------|
| 4 | **nestGate + songBird + biomeOS** | Live inter-gate `content.get` E2E validation. Cell graphs say "WIRED" but no live roundtrip tested. Need: mesh connectivity check, 1 GB roundtrip >800 MB/s on 10G, provenance chain intact across gate boundary. | All data-remote springs (hotSpring, neuralSpring, wetSpring dispatch, healthSpring, lithoSpore) | **M** |
| 5 | **nestGate** | Production-scale CAS federation. `content.get`/`content.put`/`content.replicate` implemented. Need sustained cross-gate replication validation, streaming for neuralSpring's 293 GB structural biology datasets. | neuralSpring (PDB/mmCIF/UniRef), healthSpring (ChEMBL/COSMIC) | **M** |
| 6 | **squirrel + biomeOS** | G18 agent dispatch → springs. squirrel has `signal.plan`, `provider.register`, `SpringToolDiscovery`, neuralAPI socket discovery. Need: end-to-end spring invocation through biomeOS signal graphs, not just direct primal RPC. | G18, tideGlass agent workflows, cross-spring orchestration | **L** |
| 7 | **sweetGrass + loamSpine + rhizoCrypt** | G31 batch provenance pipeline. Each primal has batch RPC individually. Need: coordinated cross-primal batch ops for 10× faster bulk ingestion (38 datasets, PDB 220K structures). Current: ~30 ms/object. | G31, westGate PDB ingest, tideGlass data prep, G7 federation scale | **L** |

### P2 — GPU/Silicon & Deploy

| # | Primal | What | Unblocks | Size |
|---|--------|------|----------|------|
| 8 | **toadStool** | VFIO ember service (fd broker for GPU passthrough). K80 GK210 firmware empty (`/lib/firmware/nvidia/gk210/`). Exp 182/184/227/234 blocked. | G32 VFIO experiments, cross-vendor QCD, multi-GPU | **M** |
| 9 | **coralReef + toadStool** | 44-experiment revalidation matrix on biomeGate. Compute Trio IPC validation (all 3 as services, not standalone). | G32 silicon deism, G45 hardware diversity | **L** |
| 10 | **biomeOS** | Multi-gate deploy validation. 7/7 deploy graphs written, 10/10 cell graphs at v2.0.0. Need: actual deploy execution on assigned gates with provenance trio + Node Atomic where specified. | All 10 spring/garden gate boots | **M** |

### P3 — Hardening & Portability

| # | Primal | What | Unblocks | Size |
|---|--------|------|----------|------|
| 11 | **cellMembrane** | Site-profile abstraction (decouple from `192.168.4.0/22` hardcoding). `/run/membrane` permission reset on restart (tmpfiles.d shipped but biomeOS resets to 0770). | G11 portability, gate restart, G29 DNS Phase 2 | **M** |
| 12 | **petalTongue** | G19 live rendering consumer pipeline — wire petalTongue to consume Node Atomic GPU output (hotSpring QCD viz, esotericWebb shaders). | G19, hotSpring visualization, esotericWebb game shaders | **M** |
| 13 | **mitoBeacon** (bearDog layer) | Validate all 13 primals pass `probe_ribocipher_acceptance()` on live NUCLEUS post-depot rebuild. | Secure inter-gate RPC, G35 agentic LAN | **S** |

---

## PRIMAL HEALTH DASHBOARD

| Primal | Tests | Version | Health | Gap |
|--------|-------|---------|--------|-----|
| **biomeOS** | 8,570+ | v4.56.0 | GREEN | Multi-gate deploy E2E |
| **toadStool** | 9,193+ | — | GREEN | VFIO ember service (G32) |
| **songBird** | 14,835+ | 0.2.x | GREEN | Inter-gate E2E validation |
| **nestGate** | 13,095+ | — | GREEN | Cross-gate CAS at scale |
| **squirrel** | 7,138 | 0.1.0 | GREEN | G18 spring dispatch wiring |
| **barraCuda** | 4,959 | 0.4.0 | **YELLOW** | Subgroup shader unmerged; PRNG path broken |
| **petalTongue** | 6,755 | 1.7.0 | GREEN | G19 live render consumer |
| **coralReef** | 3,553 | 0.2.0 | GREEN | G32 VFIO diesel experiments |
| **rhizoCrypt** | 1,900 | 0.14.17 | GREEN | G31 batch coordination |
| **loamSpine** | 1,740 | 0.9.16 | GREEN | G31 batch coordination |
| **sweetGrass** | 1,636 | 0.8.0 | GREEN | G31 batch coordination |
| **cellMembrane** | 1,281+ | — | GREEN | Portability abstraction |
| **mitoBeacon** | — | protocol | GLACIAL | G27 identity genetics |

**Total**: ~116,930 tests. 12/13 GREEN. 1 YELLOW (barraCuda — unmerged fix).

---

## RECOMMENDED EXECUTION ORDER

```
Week 1 — Critical path:
  1. barraCuda subgroup fix merge           [S, blocks GPU readback on new silicon]
  2. Inter-gate content.get E2E test        [M, unblocks all data-remote springs]
  3. Gauge group paper relabel SU(2)→SU(3)  [M, unblocks arXiv G9]

Week 2 — Spring activation:
  4. biomeOS multi-gate deploy validation   [M, unblocks spring boot on gates]
  5. G31 batch provenance pipeline          [L, unblocks bulk ingest at scale]
  6. squirrel G18 neuralAPI dispatch        [L, unblocks agent orchestration]

Week 3+ — Silicon & hardening:
  7. toadStool ember + K80 firmware         [M, unblocks G32 VFIO]
  8. coralReef 44-experiment matrix         [L, G32 silicon deism]
  9. GPU PRNG fix (barraCuda)               [L, production HMC path]
```

---

## WHAT JUST HAPPENED

| Event | Impact |
|-------|--------|
| **Springs assigned to NUCLEUS gates** | All 10 springs/gardens on 5 gates by hardware specialization. Cell graphs v2.0.0. Deploy graphs v2.0.0. |
| **Gauge group mismatch discovered** | Code audit: engine is SU(3), paper says SU(2). ⟨P⟩≈0.15 is correct SU(3). Cold lattice P=1.0. NOT a ×4 measurement bug. 6→5 rung ladder. |
| **sporePrint plaquette ×4 AAR** | Correctly identified discrepancy. Root cause: gauge group mismatch, not normalization. Diagnostic protocol Tests A-D valuable for confirmation. |
| **tideGlass Cargo workspace** | Rust workspace at `protists/tideGlass/` with RGES scaffold. `cargo check` passes. |
| **Inter-gate data access config** | `intergate_data_access.toml` documents spring→dataset access matrix. Pattern exists, live E2E untested. |
| **ecosystem_manifest.toml v3.3.0** | Spring-to-gate assignment table. Gate profiles expanded. |
| **48 glacial goals tracked** | subGen scan added G36–G52 (gen5 chain, silicon gates, publication, collaborators). |

---

## SPRING STATUS (context — primals must land first)

### Tier 1 — Active

| Spring | Gate | Data Gate | Mission | Blocked By |
|--------|------|-----------|---------|------------|
| **hotSpring** | strandGate | westGate | SU(3) pure gauge HMC, experiment queue | barraCuda subgroup fix (#1), paper relabel (#3) |
| **tideGlass** | westGate | westGate (local) | RGES drug repurposing | biomeOS deploy validation (#10), G31 batch ingest (#7) |
| **wetSpring** | westGate | westGate (local) | Metagenomics, breseq/LTEE | squirrel dispatch (#6), compute dispatch to strandGate (#4) |

### Tier 2 — Spin Up Next

| Spring | Gate | Data Gate | Blocked By |
|--------|------|-----------|------------|
| healthSpring | ironGate | westGate | Inter-gate content.get (#4), nestGate CAS scale (#5) |
| neuralSpring | strandGate | westGate | Inter-gate content.get (#4), nestGate streaming (#5) — 293 GB |
| lithoSpore | ironGate | westGate | Inter-gate content.get (#4) |

### Tier 3 — When Ready

| Spring | Gate | Blocked By |
|--------|------|------------|
| groundSpring | westGate | biomeOS deploy (#10) |
| airSpring | westGate | biomeOS deploy (#10) |
| ludoSpring | blueGate | biomeOS deploy (#10) |
| esotericWebb | ironGate | petalTongue live render (#12) |

---

## LATTICE QCD PROGRAM (LADDER COLLAPSED)

Code is **SU(3)** throughout. Paper says SU(2). Ladder collapses from 6 rungs to 5.

| Rung | Physics | Status | Owner |
|------|---------|--------|-------|
| **1** | **SU(3) pure gauge HMC** | **This is what the code does.** Experiment queue active. | hotSpring + barraCuda |
| 2 | Quenched QCD (Dirac operator) | Planned | hotSpring + barraCuda |
| 3 | Dynamical fermions (full QCD) | Planned | hotSpring + barraCuda |
| 4 | (2+1)-flavor QCD | Planned | hotSpring |
| 5 | Finite-temperature QCD | Planned | hotSpring |

---

## GATE FLEET (11 online)

| Gate | Composition | Role |
|------|-------------|------|
| **biomeGate** | GPU Crankshaft + Agentic | 3 VFIO GPUs. WG mesh LIVE. 8/10 peers. G32 silicon deism. |
| **strandGate** | NUCLEUS v4.56 | Dual EPYC + RTX 3090 + RX 6950 XT. hotSpring + neuralSpring. |
| **westGate** | NUCLEUS v4.56 | Data federation root. 362 GB / 38 datasets / 17 domains. tideGlass + wetSpring. |
| **ironGate** | NUCLEUS 13/13 | i9-14900K, RTX 5070. healthSpring + lithoSpore + esotericWebb. |
| **blueGate** | NUCLEUS v4.56 | Windows sub-builder. ludoSpring. G29 H2 DNS. |
| **sporeGate** | Sovereign CI | Build authority. G34/G35 spec. |
| **southGate** | NUCLEUS 22/22 | Validation. G17+G8 PROVEN. RTX 4060. |
| eastGate | NUCLEUS | Overwatch. 128GB. |
| northGate | NUCLEUS | Windows. RTX 5090. |
| grapheneGate | Tower (TCP) | Pixel 8a. Mobile anchor. |
| golgi | thin-relay | VPS. Forgejo + depot + sporePrint. |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** (6 NUCLEUS + biomeGate crankshaft + 4 other) |
| Primal tests | **116,930** (12 GREEN, 1 YELLOW) |
| Primal needing fix | **barraCuda** — subgroup shader unmerged, PRNG path broken |
| Springs assigned | **10** across **5 gates** |
| Cell/deploy graphs | **10/10** cell v2.0.0, **7/7** deploy v2.0.0 |
| Science data | **362 GB** on ZFS (38 datasets, 17 domains, ~5,800 CAS objects) |
| Inter-gate data access | Config WIRED, live E2E **UNTESTED** |
| Glacial goals | **48 tracked** (8 COMPLETE, 20 ACTIVE, 20 GLACIAL/CONCEPT) |
| arXiv | **BLOCKED** — gauge group mismatch (SU(3) code, SU(2) paper) |
| ecosystem_manifest.toml | **v3.3.0** |

---

*Primals are the substrate. 116,930 tests, 12/13 GREEN. The infrastructure is proven — NUCLEUS runs on 6 gates, provenance trio is 7/7, mesh connects 11 nodes. What's missing is the wiring between proven primals and assigned springs: barraCuda's subgroup fix blocks GPU readback on new silicon. Inter-gate content.get is configured but untested end-to-end. squirrel can discover springs but can't dispatch through biomeOS signal graphs yet. The provenance trio works per-object but not in coordinated batch. Fix these primal gaps and springs can boot inside NUCLEUS compositions and start running distributed science across the 10G LAN backbone.*
