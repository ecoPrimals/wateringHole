# Wave 82c: Overwatch Shift — plasmidBin to cellMembrane, primalSpring Role Evolution

**Date**: 2026-06-06  
**Author**: eastGate overwatch  
**Type**: Ownership transfer + role evolution  
**Status**: Active  

---

## Context

primalSpring evolved as the ecosystem coordination hub because it was
first. It absorbed plasmidBin CI/CD, VPS deployment scripting, upstream
primal coordination, overwatch ops, and ecosystem-wide rollout — in
addition to its actual domain: validating how primals compose.

This conflation is technical debt at the organizational level. Every
other spring validates domain experiments:

| Spring | Domain | Experiments |
|--------|--------|-------------|
| hotSpring | Physics, Anderson disorder, dose-response | Shader validation, population PK |
| wetSpring | Biology, LTEE, ChEMBL, fermentation | Provenance chains, data fetch |
| neuralSpring | Neural networks, co-training, encoding | Model validation, SMILES |
| healthSpring | Epidemiology, scoring, enrichment | RGES, MATRIX, Hill curves |
| ludoSpring | Game science, flow theory, engagement | Session mechanics, narrative |
| airSpring | Atmospheric chemistry, photodissociation | Cross-section validation |
| groundSpring | Soil microbiome, community ecology | Population dynamics |
| **primalSpring** | **Primal coordination** | **Composition patterns, bonding, mesh** |

primalSpring should be doing what the last row says — experimenting with
how primals work together, discovering new composition patterns, testing
bonding models, validating mesh behaviors. Not managing deployment
pipelines, VPS binary refresh timers, and upstream team blurbs.

---

## Ownership Transfers

### 1. plasmidBin → cellMembrane (evolution) → projectNUCLEUS (deployment)

**What moves**: Full ownership of `infra/plasmidBin/` repository.

| Aspect | From | To |
|--------|------|----|
| Binary harvesting + checksums | primalSpring (eastGate ops) | cellMembrane |
| CI/CD (check-updates.yml, harvest.yml) | primalSpring (eastGate ops) | cellMembrane |
| `sources.toml` maintenance | primalSpring | cellMembrane |
| `deploy_membrane.sh` (check, refresh, self-refresh) | primalSpring | cellMembrane |
| VPS binary deployment | primalSpring (eastGate ops) | cellMembrane → peptidoglycan |
| Checksum verification (`checksums.toml`, `provenance.toml`) | primalSpring | cellMembrane |
| `plasmidbin` CLI binary evolution | primalSpring | cellMembrane |
| Long-term deployment consumption | — | projectNUCLEUS |

**What primalSpring retains**: primalSpring continues to *consume* plasmidBin
for experiment binary discovery (via `$ECOPRIMALS_PLASMID_BIN` or XDG paths).
It does not manage the depot.

### 2. VPS Deployment Ops → cellMembrane

| Aspect | From | To |
|--------|------|----|
| Systemd unit management | primalSpring (eastGate ops) | cellMembrane |
| Caddy endpoint wiring | primalSpring (eastGate ops) | cellMembrane |
| Firewall (ufw) management | primalSpring (eastGate ops) | cellMembrane |
| Peptidoglycan self-refresh timer | primalSpring (eastGate ops) | cellMembrane |
| VPS binary refresh cycle | primalSpring (eastGate ops) | cellMembrane |
| Cross-node socat bridges | primalSpring (eastGate ops) | cellMembrane |

### 3. Upstream Primal Blurbs + Coordination → wateringHole Overwatch

| Aspect | From | To |
|--------|------|----|
| Team blurb generation + distribution | primalSpring | wateringHole overwatch (any gate) |
| Ecosystem freshness tracking | primalSpring | wateringHole overwatch |
| FRAGO generation for primal teams | primalSpring | wateringHole overwatch |
| Handoff fossilization cycle | primalSpring | wateringHole overwatch |

---

## primalSpring New Role: Primal Experimentation Spring

primalSpring becomes the spring that *experiments with primals* — like
hotSpring experiments with physics and wetSpring experiments with biology.

**Core mission**: Validate and discover how primals compose, bond, mesh,
and produce emergent behavior. The experiments/ directory is the heart,
not the tools/ directory.

**What stays in primalSpring**:
- `ecoPrimal/` library crate — composition types, IPC client, bonding models
- `experiments/` — 93 experiments across 21 tracks
- `graphs/` — deploy graph TOMLs (compositions are the experiments)
- `validation/scenarios/` — 61 absorbed scenarios
- `certification/` — guideStone composition certification
- `docs/` — gap registry, wire contracts (primal-facing)
- `nucleus_launcher` — Rust binary for spawning compositions (experiment tool)

**What migrates out over time**:
- `tools/desktop_nucleus.sh` → projectNUCLEUS
- `tools/build_ecosystem_genomeBin.sh` → plasmidBin (cellMembrane)
- VPS-specific scripts → cellMembrane
- Upstream blurb/handoff coordination → wateringHole overwatch

---

## Remaining Non-Hardware Work (team-owned, not primalSpring)

### For primal teams (blurb to teams via wateringHole):

| Item | Owner | Priority |
|------|-------|----------|
| 6 primals missing `capability_registry.toml` | Each primal team | MEDIUM |
| songBird 73% coverage (vs 90% stadial) | southGate | MEDIUM |
| 3 VPS rolled-back binaries (toadstool/coralreef/squirrel) | cellMembrane (new) | P1 |
| skunkBat UDS binary rebuild | eastGate/skunkBat | P2 |
| squirrel/petaltongue health probe framing | eastGate/ironGate | P2 |

### For spring teams:

| Item | Owner | Priority |
|------|-------|----------|
| 3 springs missing `domain_profile.toml` | hotSpring, ludoSpring, neuralSpring | LOW |
| healthSpring Wave 82 pattern absorption | ironGate | P2 |

### For cellMembrane (new responsibilities):

| Item | Priority | Notes |
|------|----------|-------|
| Accept plasmidBin repo ownership | P0 | Review `sources.toml`, CI workflows |
| VPS binary refresh: rebuild 3 rolled-back primals | P1 | toadstool/coralreef/squirrel |
| Peptidoglycan self-refresh: evolve to auto-fetch | P1 | Binary store on VPS or GH Releases fetch |
| Deploy `mesh.init` on VPS | P1 | All 13 confirmed ALIVE, ready |

---

## Active FRAGOs — Reassignment

| FRAGO | Current Owner | New Owner |
|-------|---------------|-----------|
| westGate enrollment | eastGate ops | wateringHole overwatch (hardware-gated) |
| Transport evolution | eastGate + all | songBird team + biomeOS team |
| Peptidoglycan self-awareness | eastGate ops | cellMembrane |

---

*"The spring that watches everything watches nothing. The spring that
experiments with everything discovers something."*
