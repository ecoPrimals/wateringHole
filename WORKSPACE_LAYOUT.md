# Canonical Workspace Layout

**Version:** 1.0.0
**Date:** March 25, 2026
**Status:** Active
**Authority:** wateringHole (ecoPrimals Core Standards)

This document defines the canonical directory structure for the ecoPrimals
workspace on any development machine. The layout eliminates the historical
`phase1/` and `phase2/` directories and organizes repos by role.

Run `bootstrap.sh` (in this directory) to set up or migrate a machine.

---

## Directory Structure

```
ecoPrimals/                     # workspace root
  primals/                      # all primals, flat
    barraCuda/                  #   math engine (816 WGSL shaders)
    bearDog/                    #   cryptography
    biomeOS/                    #   Neural API orchestrator
    bingoCube/                  #   human-verifiable commitment
    coralReef/                  #   sovereign shader compiler
    loamSpine/                  #   immutable lineage tracker
    nestGate/                   #   sovereign storage
    petalTongue/                #   visualization
    rhizoCrypt/                 #   content-addressed DAG
    skunkBat/                   #   defensive network security
    songBird/                   #   network orchestration
    sourDough/                  #   project scaffolding
    squirrel/                   #   AI coordination
    sweetGrass/                 #   attribution protocol
    toadStool/                  #   sovereign compute hardware
  springs/                      # science validation
    airSpring/                  #   precision agriculture
    groundSpring/               #   measurement noise
    healthSpring/               #   PK/PD, microbiome, biosignal
    hotSpring/                  #   computational physics
    ludoSpring/                 #   game science, HCI, PCG
    neuralSpring/               #   ML primitives, spectral
    primalSpring/               #   composition validation
    wetSpring/                  #   metagenomics, analytical chemistry
  gardens/                      # usable systems (creative surface)
    blueFish/                   #   data pipeline for PIs
    esotericWebb/               #   cross-evolution CRPG
  infra/                        # ecosystem support
    plasmidBin/                 #   binary distribution
    sporePrint/                 #   public verification portal
    wateringHole/               #   standards and handoffs
    whitePaper/                 #   gen0-gen4 papers
  sort-after/                   # unclear placement, revisit later
    agentReagents/
    benchScale/
    ionChannel/
    rustChip/
```

---

## GitHub Org Mapping

There is no monorepo. Each primal, spring, and garden is a standalone repository
under its respective GitHub organization — like independent organisms in an
ecosystem. This aligns with the gen3 whitePaper principle: primals are sovereign
entities that discover each other at runtime, never at compile time.

| Local Directory | GitHub Org | Role |
|----------------|------------|------|
| `primals/` | ecoPrimals | Sovereign infrastructure primals |
| `springs/` | syntheticChemistry | Science validation springs |
| `gardens/` | sporeGarden | Usable systems (creative surface) |
| `infra/` | ecoPrimals | Ecosystem support (wateringHole, plasmidBin, etc.) |
| `sort-after/` | mixed (syntheticChemistry mostly) | Temporary parking |

### Organizations

| Org | Purpose | Visibility |
|-----|---------|------------|
| **ecoPrimals** | Primals + ecosystem infrastructure | Mix: public infra, private primals |
| **syntheticChemistry** | Springs (science validation) + lab tools | Public springs, private lab tools |
| **sporeGarden** | Gardens (creative surface, usable systems) | Public |

### Full Repo Inventory

#### primals/ (ecoPrimals org)

| Repo | GitHub | Visibility |
|------|--------|------------|
| barraCuda | ecoPrimals/barraCuda | public |
| bearDog | ecoPrimals/bearDog | private |
| biomeOS | ecoPrimals/biomeOS | private |
| bingoCube | ecoPrimals/bingoCube | private |
| coralReef | ecoPrimals/coralReef | public |
| loamSpine | ecoPrimals/loamSpine | private |
| nestGate | ecoPrimals/nestGate | private |
| petalTongue | ecoPrimals/petalTongue | private |
| rhizoCrypt | ecoPrimals/rhizoCrypt | private |
| skunkBat | ecoPrimals/skunkBat | private |
| songBird | ecoPrimals/songBird | private |
| sourDough | ecoPrimals/sourDough | private |
| squirrel | ecoPrimals/squirrel | public |
| sweetGrass | ecoPrimals/sweetGrass | private |
| toadStool | ecoPrimals/toadStool | public |

#### springs/ (syntheticChemistry org)

| Repo | GitHub | Visibility |
|------|--------|------------|
| airSpring | syntheticChemistry/airSpring | public |
| groundSpring | syntheticChemistry/groundSpring | public |
| healthSpring | syntheticChemistry/healthSpring | public |
| hotSpring | syntheticChemistry/hotSpring | public |
| ludoSpring | syntheticChemistry/ludoSpring | public |
| neuralSpring | syntheticChemistry/neuralSpring | public |
| primalSpring | syntheticChemistry/primalSpring | public |
| wetSpring | syntheticChemistry/wetSpring | public |

#### gardens/ (sporeGarden org)

| Repo | GitHub | Visibility |
|------|--------|------------|
| esotericWebb | sporeGarden/esotericWebb | public |
| blueFish | syntheticChemistry/blueFish (pending transfer to sporeGarden) | public |

#### infra/ (ecoPrimals org)

| Repo | GitHub | Visibility | Notes |
|------|--------|------------|-------|
| wateringHole | ecoPrimals/wateringHole | public | Ecosystem standards, handoffs, leverage guides |
| whitePaper | ecoPrimals/whitePaper | private | gen0–gen4 papers |
| plasmidBin | ecoPrimals/plasmidBin | public | Consumer-facing binary distribution surface |
| sporePrint | ecoPrimals/sporePrint | public | Public verification portal |

**plasmidBin dual structure**: The public `ecoPrimals/plasmidBin` repo is the
consumer-facing distribution surface (per-primal directories with `metadata.toml`,
`fetch.sh`, `harvest.sh`). The local `infra/plasmidBin/` directory in the
development workspace contains operational tooling (`deploy_gate.sh`,
`start_primal.sh`, `doctor.sh`, `ports.env`, actual binaries). Consumers clone
the public repo; operators use the local infra tooling. Binary artifacts live in
GitHub Releases on the public repo, not in git.

#### sort-after/ (syntheticChemistry — lab tools, in stasis or gifted)

| Repo | GitHub | Visibility | Status | Purpose |
|------|--------|------------|--------|---------|
| agentReagents | syntheticChemistry/agentReagents | private | Stasis | VM image builder (YAML manifests, cloud-init). Built for local rustdesk testing when Cosmic broke passthrough. Future: syntheticChemistry lab validation tool. |
| benchScale | syntheticChemistry/benchScale | private | Stasis | VM provisioner (libvirt, CloudInit). Built alongside agentReagents for the same rustdesk testing. Future: syntheticChemistry substrate validation tool. |
| ionChannel | syntheticChemistry/ionChannel | private | Evolving | Secure connection channel. Started as K-NOME test project solving rustdesk/Cosmic passthrough. May evolve into a gated secure Linux connection point for primals, or remain a science tool for validating other systems. |
| rustChip | syntheticChemistry/rustChip | public | Active (gift) | NPU/Akida characterization toolkit. Extracted from toadStool's metalForge subsystem, evolves via hotSpring experiments. Public gift to Akida — gives them hardware access without primal dependency. |

---

## Cross-Repo Path Conventions

Springs and gardens reference primals via relative paths in `Cargo.toml`.
After the layout migration, the canonical relative paths are:

### From a spring root (`springs/{spring}/Cargo.toml`)

```toml
barracuda = { path = "../../primals/barraCuda/crates/barracuda" }
neural-api-client-sync = { path = "../../primals/biomeOS/crates/neural-api-client-sync" }
```

### From a spring subcrate (`springs/{spring}/barracuda/Cargo.toml`)

```toml
barracuda = { path = "../../../primals/barraCuda/crates/barracuda" }
```

### From a deeper nested crate (`springs/{spring}/metalForge/forge/Cargo.toml`)

```toml
barracuda = { path = "../../../../primals/barraCuda/crates/barracuda" }
```

### From a garden (`gardens/{project}/Cargo.toml`)

Same depth as springs — `../../primals/barraCuda/crates/barracuda`.

### Migration: old paths to new

| Old (from ecoSprings/{spring}/) | New (from springs/{spring}/) |
|---------------------------------|------------------------------|
| `../barraCuda/crates/barracuda` | `../../primals/barraCuda/crates/barracuda` |
| `../../barraCuda/crates/barracuda` (from subcrate) | `../../../primals/barraCuda/crates/barracuda` |
| `../phase2/biomeOS/crates/neural-api-client-sync` | `../../primals/biomeOS/crates/neural-api-client-sync` |

The `bootstrap.sh` script prints warnings for Cargo.toml files that contain
relative path dependencies needing updates, but does not modify them
automatically.

---

## Migration from Historical Layout

The historical layout used `phase1/`, `phase2/`, and `ecoSprings/` directories.
Some machines may also have primals at the top level. The `bootstrap.sh` script
handles all known variants:

| Historical Location | New Location |
|---------------------|-------------|
| `phase1/beardog/` | `primals/bearDog/` |
| `phase1/nestgate/` | `primals/nestGate/` |
| `phase1/songbird/` | `primals/songBird/` |
| `phase1/squirrel/` | `primals/squirrel/` |
| `phase1/toadstool/` | `primals/toadStool/` |
| `phase2/biomeOS/` | `primals/biomeOS/` |
| `phase2/loamSpine/` | `primals/loamSpine/` |
| `phase2/rhizoCrypt/` | `primals/rhizoCrypt/` |
| `phase2/sweetGrass/` | `primals/sweetGrass/` |
| `barraCuda/` (top-level) | `primals/barraCuda/` |
| `coralReef/` (top-level) | `primals/coralReef/` |
| `petalTongue/` (top-level) | `primals/petalTongue/` |
| `ecoSprings/{spring}/` | `springs/{spring}/` |
| `ecoSprings/esotericWebb/` | `gardens/esotericWebb/` |
| `wateringHole/` (top-level) | `infra/wateringHole/` |
| `whitePaper/` (top-level) | `infra/whitePaper/` |
| `plasmidBin/` (top-level) | `infra/plasmidBin/` |

Note: `phase1/` used lowercase directory names (e.g., `beardog` not `bearDog`).
The script preserves the actual directory name — git tracks the remote, not the
local folder name.

---

## Pending Org Transfers

- **blueFish**: currently in syntheticChemistry, should transfer to sporeGarden.
  Run `gh repo transfer syntheticChemistry/blueFish sporeGarden` when ready.
- **coralForge** (syntheticChemistry): will be renamed and moved to sporeGarden
  as a DNA/AI tool. Not included in the layout until renamed.

---

## Related Standards

- `PRIMAL_REGISTRY.md` — authoritative catalog of every primal
- `SPRING_CATALOG.md` (in whitePaper/gen3/) — spring inventory
- `PRIMAL_IPC_PROTOCOL.md` — IPC standards for inter-primal communication
- `IPC_COMPLIANCE_MATRIX.md` — per-primal interop status
