# Gate Deployment Standard

**Status:** OPERATIONAL
**Last updated:** 2026-05-28 (Wave 60)

## Overview

A gate is an independent eukaryotic cell in the ecoPrimals organism.
Each gate runs its own NUCLEUS composition, validates science through
its assigned spring(s), and syncs evolution through the VPS periplasm.

## Gate Anatomy

```
┌─ Gate ──────────────────────────────────────────────┐
│                                                      │
│  cytoplasm: NUCLEUS (primals on UDS)                │
│  ├── Tower atomic (beardog, songbird, skunkbat)     │
│  ├── Node atomic  (+ toadstool, barracuda, coralreef)│
│  ├── Nest atomic  (+ nestgate, rhizocrypt, loamspine,│
│  │                   sweetgrass)                     │
│  └── Meta-tier    (+ biomeos, squirrel, petaltongue) │
│                                                      │
│  spring niche: domain validation                     │
│  plasma membrane: firewall + authentication          │
│                                                      │
└──────────────┬───────────────────────────────────────┘
               │
         Songbird :7700 (federation)
               │
         VPS periplasm (Forgejo + Caddy + DNS)
```

## Gate Registry

| Gate | NUCLEUS | Primary Spring | Hardware |
|------|---------|---------------|----------|
| eastGate | 13/13 (reference) | primalSpring | Coordination |
| ironGate | 13/13 | healthSpring + ludoSpring | Clinical |
| southGate | 13/13 | wetSpring + neuralSpring | Pattern |
| biomeGate | 9/13 → 13/13 | hotSpring | GPU compute |
| strandGate | pending | hotSpring (science) + ABG | 64-core science |

## Deployment Phases

### Phase 1: Tower (minimum viable gate)
```bash
plasmidBin/deploy_gate.sh --composition tower --gate $GATE_NAME
```
Deploys bearDog + Songbird + skunkBat. The gate can authenticate,
discover peers, and detect threats.

### Phase 2: Node (compute-capable)
```bash
plasmidBin/deploy_gate.sh --composition node --gate $GATE_NAME
```
Adds toadStool + barraCuda + coralReef. The gate can dispatch and
execute compute workloads.

### Phase 3: Nest (storage + provenance)
```bash
plasmidBin/deploy_gate.sh --composition nest --gate $GATE_NAME
```
Adds nestGate + rhizoCrypt + loamSpine + sweetGrass. The gate can
persist data with provenance tracking.

### Phase 4: Full NUCLEUS + Meta
```bash
plasmidBin/deploy_gate.sh --composition full --gate $GATE_NAME
```
Adds biomeOS + squirrel + petalTongue. Full 13/13 composition.

## Spring Niche Deployment

After NUCLEUS is live, deploy the spring niche:

```bash
plasmidBin/deploy_gate.sh --niche hotspring --gate biomeGate
```

Spring niches define which primals are composed for domain validation.
See `plasmidBin/manifest.toml` `[niches]` for composition details.

## Health Validation

```bash
# Check primal health
songbird doctor --format json

# Validate spring composition
primalspring validate --spring hotSpring --live

# Full gate health check
plasmidBin/validate-primal-proof.sh --gate $GATE_NAME
```

## Forgejo Sync

Each gate syncs through the VPS periplasm:

```bash
# Pull from Forgejo
cascade-pull.sh --gate auto --source forgejo

# Push evolution
git push forgejo main
```

## Standards

- **Binary source:** `plasmidBin/` via `fetch.sh` or GitHub Releases
- **Profiles:** `plasmidBin/profiles/{tower,node,nest,nucleus,full}.toml`
- **Niches:** `plasmidBin/manifest.toml` `[niches]`
- **Health:** Songbird `:7700` federation + `doctor` command
- **Sync:** Forgejo at `git.primals.eco:2222` (SSH)
