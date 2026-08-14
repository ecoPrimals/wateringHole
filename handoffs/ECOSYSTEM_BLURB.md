# ecoPrimals Ecosystem Blurb — Wave 157k Pipeline + Provenance Convergence

**Date**: Aug 14, 2026 10:55 | **Wave**: 157k | **From**: sporeGate (foreman)
**Posture**: **12 gates ONLINE.** **0/0/0.** Cascade absorbed: swarmVine mesh.relay topic fix LANDED (`31e3e0a`, blocker #3 CLOSED), barraCuda DF64 shader compile (`4a3679f0`), coralReef WGSL-to-SPIR-V (`9c64cfa`). Rebuilding stale primals. Pipeline divergence RESOLVED. rootPulse trio graphs LIVE. westGate provenance trio 14/14 PASS. Depot: x86_64 13/13 CURRENT + 2 rebuilding from new commits.

---

## What Changed (sporeGate ops — Aug 14 10:36–10:55)

### Cascade from Forgejo + Rebuild

Pulled all 16 repos from golgiBody Forgejo. New commits absorbed:

| Primal | Commit | Change | Team |
|--------|--------|--------|------|
| **swarmVine** | `31e3e0a` | `mesh.relay` topic field fix — **blocker #3 CLOSED** | ironGate |
| **barraCuda** | `4a3679f0` | DF64 sovereign shader compilation via coralReef SPIR-V | strandGate |
| **coralReef** | `9c64cfa` | WGSL-to-SPIR-V DF64-safe emission endpoint | strandGate |

Rebuilt primals: barraCuda (9010KB, VERIFIED), coralReef (9329KB, VERIFIED). membrane + songbird rebuilding (picks up swarmVine topic fix + pipeline convergence code).

---

## What Changed (sporeGate ops — Aug 14 08:14–09:00)

### Pipeline Divergence Fix (P1 — RESOLVED)

Root cause: `serde(flatten)` collision between `ProvenanceFile` and `ProvenanceEntry` on shared `target`/`builder` field names. Per-entry `target` deserialized as `None`, making the harvest blind to architecture mismatches. The aarch64 build wrote provenance with correct commits, so the x86_64 harvest said "current" for everything — but x86_64 binaries were 2+ days stale.

Fixes:
1. **Two-pass TOML parse** — `load_provenance` parses raw `toml::Value`, deserializes each section individually, bypassing the flatten collision
2. **Target-aware drift detection** — `has_upstream_changes` checks `entry.target` vs `detect_target_triple()`
3. **rootPulse trio wiring** — drift queries `rootpulse_harvest` via neuralAPI first, flat file as fallback
4. **Binary PATH fix** — `~/.local/bin/membrane` was 11 days stale, shadowing `/usr/local/bin`
5. **Full x86_64 rebuild** — 13/13 primals rebuilt, 28 binaries pushed to depot

### rootPulse Graph Definitions (neuralAPI)

Three graphs created and discoverable:
- `rootpulse_commit` — cascade HEAD + harvest batch recording
- `rootpulse_harvest` — per-target build provenance (canonical drift authority)
- `rootpulse_diff` — sovereignty verification

Primal step handler implementations needed to fully activate; trio query degrades gracefully to flat file.

### westGate — Provenance Trio Experiments (14/14 PASS)

Built and executed 14-experiment validation suite via `membrane experiment.*` (Rust-native, Neural API composition). Validates the full provenance trust model lifecycle:

- **Estate**: 2,630 braids (100% verified), 1,421 DAG sessions / 390,984 vertices, 2 spines (1,386 commits), 6.57 TB on 63.7 TB ZFS
- **Experiments**: tamper detection, braid determinism, negative provenance, estate audit (100/100 verified), attribution, W3C PROV-O + RO-Crate export, DataCite, DAG lifecycle, spine permanence, crypto round-trips, ZFS storage, cross-primal composition, NUCLEUS census
- **Cross-industry exports**: `alphafold_provenance_statement.txt`, `alphafold_provenance_table.tsv`, `cell_ontology_ro-crate-metadata.json`, `cell_ontology_datacite.json`
- **primalSpring exp124**: New validation experiment codified in primalSpring
- **Routing gaps found**: sweetGrass auto-announce (depot binary needs rebuild), bearDog AEAD not surfaced in Neural API, rhizoCrypt dehydration method not routed, content.put not in nestGate translation
- **Glue retirement**: `native_braid.py` formally deprecated → `membrane experiment.*` + `membrane content.braid`
- AAR: `WESTGATE_PROVENANCE_TRIO_EXPERIMENTS_AAR_AUG14_2026.md`

---

## Previous Changes

### blueGate — ENMESHED (3 builds SUCCEEDED)

- **songBird** (`b8c22577`) — deep-debt sweep, P2 #6 fix, GNU toolchain workaround
- **swarmVine** (`0e4cb75`) — **FIRST EVER WINDOWS BUILD.** `#[cfg(unix)]` gating on UDS imports
- **membrane** (`c1b9de1`) — enmeshment TCP fallback + content.braid, builder.serve with riboCipher
- builder.serve ALIVE on `:9800` — LAN (.212) + WireGuard (.12) reachable
- NUCLEUS 13/13 (process-verified, UDS health probes show false DEGRADED on Windows)
- Depot 0/13 current — all stale vs source HEAD, awaiting sporeGate autonomous dispatch

### graftGate — builder.serve LIVE + D12 FIXED + Depot 16/16

- builder.serve on `:9800` with launchd plist (boot persistence), riboCipher compatible
- **D12 FIXED**: swarmVine NUCLEUS launch broken by wrong subcommand + wrong socket dir
- **D13 NEW**: `build_primal_command_with()` env var `${VAR}` inline expansion missing
- Depot corrected to **16/16 darwin** (was blurbed as 5/15 — stale data)
- 11/13 NUCLEUS processes ACTIVE (skunkBat/toadstool incubating)
- **Upstream merge needed**: D12/D13 patches to biomeOS on eastGate

### southGate — Cascade Complete + neuralSpring Fix

- **mesh.relay FIXED** in new songBird binary (was `"unknown JSON-RPC method"`)
- Remaining: swarmVine doesn't include `topic` field in mesh.relay params — ironGate fix
- neuralSpring GPU parity fix pushed (`4fa0c4c`) — 71/80 validation checks pass
- skunkBat fork storm (437 processes) cleaned — fresh restart eliminated spawn leak
- **SSH ready** for enrollment (port 22 open, key generated, LAN IP confirmed `.148`)
- 3 gossip peers outbound, 4 LAN mesh peers

### biomeGate — ONLINE + REGISTERED (Team Intermittent)

- **Reimaged** Ubuntu 24.04.3 (kernel 7.0.0-28). Tower 4/4 + Node Atomic trio. Ember fleet 4/4 GPUs.
- **WG peer + SSH key REGISTERED** via sporeGate. Mesh connected.
- **3 toadStool bugs fixed**: `.zst` firmware decompression, D3hot BAR0 wake, PRI fault false positives
- **Sovereign dispatch**: Cold boot blocked at HBM2 wall → warm handoff required for Volta. K80 unsigned falcons most tractable.
- **Team intermittent** — science-track pacing, resting between sessions
- **Next**: full NUCLEUS composition, nouveau warm handoff (Exp R6), K80 firmware extraction

### Silicon Exploration Assignments — NEW

Cross-product mapping of every fixed-function silicon unit (GPU/NPU/CPU) × gate × spring. Documents exploration priorities per gate. Canonical reference: `handoffs/SILICON_EXPLORATION_ASSIGNMENTS.md`.

---

## Remaining Work

### Remaining Infrastructure

| # | Item | Owner | Priority |
|---|------|-------|----------|
| 1 | D12/D13 upstream merge to biomeOS | eastGate (biomeOS team) | P1 |
| 2 | cellMembrane UDS→TCP fallback for health probes (Windows) | sporeGate (cellMembrane) | P2 |
| 3 | swarmVine `mesh.relay` `topic` param alignment | ironGate (swarmVine/songBird) | P2 |
| 4 | blueGate depot rebuild via autonomous dispatch | sporeGate foreman | P2 |
| 5 | `rust-toolchain.toml` GNU target for Windows | ironGate (songBird) | P2 |
| 6 | southGate SSH key enrollment | sporeGate ops | P3 |
| 7 | biomeGate full NUCLEUS composition | biomeGate (when active) | P3 |
| 10 | rootPulse trio step handler activation | nestGate, rhizoCrypt, bearDog, sweetGrass | P2 |
| 11 | Neural API translation registry audit (AEAD, dehydration, content.put) | westGate + ironGate | P2 |
| 12 | sweetGrass auto-announce in depot binary | sporeGate (depot rebuild) | P2 |
| ~~8~~ | ~~biomeGate WG + SSH registration~~ | ~~overwatch~~ | **DONE** (via sporeGate) |
| ~~9~~ | ~~southGate LAN IP correction~~ | ~~overwatch~~ | **DONE** (.149→.148) |

### biomeGate Deploy Status (COMPLETE through Tower + Node)

| Step | Action | Status |
|------|--------|--------|
| 1 | Fresh Ubuntu 24.04 install | **DONE** (kernel 7.0.0-28) |
| 2 | RustDesk + Cursor installed | **DONE** (ID: 1695902872) |
| 3 | Tower Atomic 4/4 from depot | **DONE** (bearDog, songBird, skunkBat, swarmVine) |
| 4 | Node Atomic trio source-built | **DONE** (toadStool+barraCuda GNU, coralReef depot) |
| 5 | 41/42 repos cloned | **DONE** (sporePrint needs SSH key on Forgejo) |
| 6 | WireGuard UP + registered | **DONE** — peer registered via sporeGate |
| 7 | Runtime VFIO (diesel engine lesson) | **DONE** — zero `/etc/modprobe.d/`, 4/4 GPUs alive |
| 8 | Sovereign dispatch experiments R1-R5 | **DONE** — HBM2 wall confirmed, 3 bugs fixed |
| 9 | biomeOS + full NUCLEUS composition | **NEXT** — after WG peer registration |
| 10 | Nouveau warm handoff (Exp R6) | **NEXT** — sovereign dispatch Tier 2 path |

### NanoWire SSH Retirement (Ongoing)

Tier 1 **RETIRED** (sub-builder dispatch). `builder.serve` pattern = graduation template.

| Tier | Scope | Status |
|------|-------|--------|
| 1 | Sub-builder CI dispatch | **RETIRED** (3/3 builders enmeshed) |
| 2 | gate.pull/check/info, plasmid.trigger, service.* | NEXT |
| 3 | Depot push + CAS archival | After Tier 2 |
| 4-7 | Caddy, enrollment, relay, git transport | Future |

Full checklist: `specs/NANOWIRE_RETIREMENT_CHECKLIST.md`

---

## Active Code Teams

| Team | Track | Status |
|------|-------|--------|
| **sporeGate — cellMembrane** | Pipeline divergence fix + rootPulse trio | **SHIPPED** (`3f9fa14`). Target-aware drift, two-pass parse, rootPulse graph wiring. |
| **westGate — cellMembrane** | Provenance trio experiments (14/14) | **SHIPPED**. `membrane experiment.*` suite + primalSpring exp124. |
| ~~**eastGate — biomeOS**~~ | ~~`deploy.result` gossip~~ | **DONE** (`f80e5f2a`). Dormant. |
| ~~**eastGate — primalSpring**~~ | ~~Wire `FleetDeployHealth`~~ | **DONE** (`d15ab028`, v0.9.50). Dormant. |
| ~~**westGate — nestGate**~~ | ~~nestgate.io Phase 3~~ | **LIVE.** `/cas/{hash}` + provenance routes. |
| **strandGate — barraCuda** | Silicon saturation gaps | Science-track, not stadial. 6 gaps exposed. |

Primal code teams are in **science/ops mode** — no new features, validation and infrastructure work only.

---

## Downstream Patterns — Active + Future

| Track | Description | Owner | Status |
|-------|-------------|-------|--------|
| **Sovereign dispatch** | Nouveau warm handoff (Exp R6) → K80 firmware extraction → shader dispatch on VFIO GPUs | biomeGate (intermittent) | ACTIVE |
| **SSH → Tower Atomic graduation** | Extend `builder.serve` for `depot.*`, `service.*`, `gate.*` capabilities. NanoWire Tiers 2-7. | sporeGate | NEXT |
| **Graph visualization** | biomeOS 79 TOML graphs → petalTongue GraphEngine → nestgate.io `/viz/graphs/`. Spec filed. | ironGate + eastGate | SPEC FILED |
| **arXiv submission** | Murillo/Chuna QCD preprint 41/42. Wire live site + reviewer send. | strandGate | ACTIVE |
| **Science pipeline E2E (G71)** | GPU data → pseudoSpore → NFT → reviewer. Full chain. | strandGate → ironGate → sporePrint | ACTIVE |
| **Silicon exploration matrix** | Gate × spring × unit cross-product. AARs per gate. | all compute gates | REFERENCE |
| **tideGlass cell boot** | Cell 2026 GPS rebuild on westGate. CAS federation now live. | westGate | QUEUED |
| **sporePrint refresh (G14)** | Gate status, pseudoSpore, K-Derm architecture page, data catalog. | sporeGate (sporePrint) | ASSIGNED |
| **whitePaper subgen** | THRESHOLDS_CROSSED, ENMESHMENT_CROSSING, TOPOLOGY_CONCEPT_TO_REALITY. | overwatch (followup) | PLANNED |
| **Provenance trio activation** | rootPulse step handlers → trio becomes canonical drift authority. Replaces flat provenance.toml. | westGate (nestGate, rhizoCrypt) | NEW |
| **`experiment.all` in gate spinup** | Run 14-experiment suite as post-deployment validation battery. Add to spinup playbooks. | westGate recommendation | NEW |
| **westGate hardware upgrades** | M.2 NVMe (CAS hot tier) + RAM 128GB (ARC expansion). Hardware on hand. | westGate | READY |

---

## Depot Status

| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **13/13 REBUILT** | Rebuilt Aug 14 (pipeline fix). 28 binaries pushed to depot. |
| `aarch64-unknown-linux-musl` | **15/15 REBUILT** | ironGate sub-builder, CAS replicated |
| `aarch64-apple-darwin` | **16/16 CURRENT** | graftGate — corrected from stale 5/15 blurb |
| `x86_64-pc-windows-gnu` | **0/13 STALE** | blueGate enmeshed — awaiting sporeGate autonomous dispatch |

---

## Code Team Ownership (Canonical)

| Gate | Code Teams | Role |
|------|-----------|------|
| eastGate | biomeOS, squirrel, projectNUCLEUS, primalSpring + overwatch | Orchestration + sovereignty |
| ironGate | bearDog, songBird, skunkBat, swarmVine, bingoCube, petalTongue, esotericWebb, footPrint, tideGlass + springs | Primal workhorse, 14TB NFT braid + CAS |
| strandGate | toadStool, barraCuda, coralReef, hotSpring, rustChip, helixVision, initioChem | Compute trio + batch HPC + science |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, wetSpring, projectFOUNDATION | Provenance trio + data CAS (50.7TB) |
| sporeGate | cellMembrane, lithoSpore, plasmidBin ops | Topology + depot + cascade |
| graftGate | sourDough | Darwin builder (FULL NUCLEUS) |
| southGate | neuralSpring | Validation canary |
| blueGate | — | Windows builder (ENMESHED) |
| biomeGate | hotSpring (sovereign dispatch) | ONLINE — Tower 4/4, Node Atomic, ember fleet 4/4, sovereign dispatch research |

---

## Architecture Reference

**NUCLEUS** = Tower + Nest + Node + biomeOS + petalTongue + squirrel + cellMembrane

| Atomic | Primals | Role |
|--------|---------|------|
| **Tower** | bearDog + songBird + skunkBat + swarmVine | Shared electron cloud: crypto, routing, defense, gossip |
| **Nest** | Tower + nestGate + rhizoCrypt + loamSpine + sweetGrass | Data identity: CAS + DAG + spine + braids |
| **Node** | Tower + toadStool + barraCuda + coralReef | Compute: dispatch + GPU + shaders |

---

## K-Derm Membrane Topology

The ecosystem operates as a diderm cell envelope with three distinct layers, each mapped to a DNS domain and a trust model:

```
Internet (extracellular)
    │
    ▼ [Cloudflare TLS, pull-only]
golgiBody-ext ──── OUTER MEMBRANE (primals.eco)
    │               Zola static site, sporePrint, publications
    │               Bond type: ionic/weak (external consumers)
    │ [GitHub trailing mirror]
    │
golgiBody ──────── PERIPLASM (Forgejo + depot + Caddy TLS)
    │               Push receiver (cis face), sole depot server
    │               Bond type: covalent/metallic
    │               Routes: primals.eco + nestgate.io + primal.eco
    │
    ▼ [WireGuard mesh, inner membrane]
┌── CYTOPLASM ──── INNER MEMBRANE (primal.eco)
│   │               NUCLEUS dogfooded. All IPC via UDS + songBird mesh.
│   │               All gates: kderm_role = cytoplasm
│   │
│   ├── sporeGate (foreman, cascade hub, depot authority)
│   │   └── dispatches to sub-builders via TCP/riboCipher :9800
│   │       ├── ironGate  (x86_64-musl workhorse, systemd)
│   │       ├── blueGate  (x86_64-windows, scheduled task)
│   │       └── graftGate (aarch64-darwin, launchd)
│   │
│   ├── eastGate (overwatch, biomeOS, primalSpring)
│   ├── ironGate (primal workhorse, 14TB CAS, RTX 5070 Ti)
│   ├── strandGate (compute trio, dual EPYC, RTX 3090)
│   ├── westGate (data CAS, 50.7TB ZFS, provenance trio)
│   ├── southGate (validation canary, RTX 4060)
│   └── biomeGate (GPU lab — ONLINE, Tower+Node, ember fleet 4/4)
│
└── PEPTIDOGLYCAN ── nestgate.io (primal-served data surface)
                    Served by petalTongue on sporeGate via mesh
                    Phase 2 LIVE: /depot/, /provenance/
                    Phase 3 LIVE: /cas/{hash}, /cas/{hash}/provenance
                    Federation: songBird content.locate across all gates
                    Sovereign Knot DNS + DNSSEC (no Cloudflare)
```

### Design Principles

- **Inner membrane = NUCLEUS dogfooded.** Every gate runs NUCLEUS via biomeOS Neural API. All inter-gate communication uses Tower Atomic mesh (songBird + swarmVine gossip + riboCipher). No external dependencies.
- **Peptidoglycan = primal-served.** nestgate.io is served by petalTongue (a primal), not a static site generator. Data integrity is proven by primals (nestGate CAS + sweetGrass braids + songBird federation). This is where we dogfood the data stack.
- **Outer membrane = external sovereignty only.** primals.eco uses Cloudflare DNS and Caddy TLS — external tools for external-facing content. No NUCLEUS runtime dependency. Pull-only. WireGuard and Cloudflare live here, not on inner membrane.
- **golgiBody = periplasm relay.** The sole VPS bridges inner and outer. Forgejo (push receiver), depot (binary distribution), Caddy (TLS termination for all 3 domains). Bond degradation: covalent (gate→golgi) → ionic (golgi→golgi-ext) → weak (golgi-ext→GitHub).

### Builder Dispatch Flow

```
overwatch (eastGate)
    │ blurb + cascade signal
    ▼
sporeGate (foreman)
    │ cascade timer (15min) or manual trigger
    │ reads ecosystem_manifest.toml for builder_host/builder_port
    ▼
call_tcp(riboCipher :9800) ─── JSON-RPC plasmid.harvest
    │
    ├── ironGate:9800  (systemd membrane-builder.service)
    │   └── x86_64-musl + aarch64-musl cross-compile
    │
    ├── blueGate:9800  (Windows scheduled task)
    │   └── x86_64-pc-windows-gnu
    │
    └── graftGate:9800 (launchd plist)
        └── aarch64-apple-darwin

    All builders: riboCipher [0xEC, 0x01] frame detection
    → JSON-RPC dispatch (health, plasmid.staleness, plasmid.harvest)
    → Results pushed to golgiBody depot via SCP (Tier 3 retirement: TCP relay)
```

---

## Team Assignments — Downstream Tracks

| # | Track | Team/Gate | Assignment |
|---|-------|-----------|------------|
| 1 | **D12/D13 biomeOS merge** | eastGate (biomeOS) | Merge swarmVine launch profile + `${VAR}` expansion from graftGate D12/D13. Minimal: TOML profile + `if !subcommand.is_empty()` guard + `${VAR}` while-let loop in `build_primal_command_with()`. |
| 2 | **cellMembrane UDS→TCP fallback** | sporeGate (cellMembrane) | Windows health probes (`primals.alive`, `sovereignty.s4_auth`) use UDS → false DEGRADED. Add TCP fallback using `builder.serve` pattern. |
| 3 | **swarmVine mesh.relay topic param** | ironGate (swarmVine + songBird) | swarmVine calls `mesh.relay` without `topic` field. songBird returns `"Missing required field: topic"`. Parameter format alignment. |
| 4 | **blueGate depot rebuild** | sporeGate (foreman) | Dispatch autonomous rebuild via `call_tcp(192.168.4.212:9800, plasmid.harvest)`. 0/13 current → rebuild all. |
| 5 | **rust-toolchain.toml GNU target** | ironGate (songBird) | Add `x86_64-pc-windows-gnu` as Windows target or `.cargo/config.toml` override. blueGate uses GNU toolchain, not MSVC. |
| 6 | **Graph visualization architecture** | ironGate (petalTongue) + eastGate (biomeOS) | Document `graph.export` capability: biomeOS 79 TOML graphs → petalTongue `GraphEngine` (force-directed/hierarchical layout) → SVG/DOT on nestgate.io `/viz/graphs/`. Spec filed: `specs/GRAPH_VISUALIZATION_SPEC.md`. |
| 7 | **sporePrint content refresh** | sporeGate (sporePrint) | Update gate-status page, pseudoSpore landing, data catalog stats, architecture K-Derm page (add nestgate.io, golgiBody-ext split, three-domain model). |
| 8 | **whitePaper subgen update** | overwatch (eastGate, followup) | Update `THRESHOLDS_CROSSED.md` (enmeshment, 6th OS, silicon exploration). Draft `ENMESHMENT_CROSSING.md` subgen. Update `TOPOLOGY_CONCEPT_TO_REALITY.md`. |
| 9 | **southGate SSH enrollment** | sporeGate ops | Port 22 open, key generated. Authorize in sporeGate SSH config. LAN IP confirmed `.148`. |

---

## Fossilization This Round

14 files fossilized to `fossilRecord/wave157k_interstadial/` this wave:
- 5 gate AARs (blueGate, strandGate, graftGate×2, grapheneGate) — absorbed into ortho
- 4 stale handoffs (BLUEGATE_DEPOT_PUSH_GUIDE, TEAM_WORK_VECTORS, SPOREPRINT_BLURB, TEAM_STARTUP_BLURB_TEMPLATE) — superseded
- `BIOMEGATE_RECOVERY_AAR_AUG13_2026.md` — recovery attempt absorbed, wipe completed
- `CELLMEMBRANE_WAVE157K_DEEP_DEBT_SWEEP_AUG13_2026.md` — code work done (`d6a56b3`)
- `NESTGATE_S150_DEEP_DEBT_SWEEP_AUG13_2026.md` — code work done, absorbed
- `DEPLOYMENT_SIGNALING_EVOLUTION_SPEC.md` — implemented (deploy.result Phases 1+2 DONE)
- `SWEETGRASS_CONVERGENCE_BACKPRESSURE_DESIGN.md` — implemented

Total: **217 files fossilized** across 19 wave directories. **1,494+ total records.**

---

## CONVERGENCE RULE

> **Pipeline + provenance convergence.** 12 gates ONLINE. 0/0/0.
> Pipeline divergence RESOLVED (serde flatten, target-aware drift, rootPulse trio).
> Depot REBUILT 13/13 x86_64. Cascade autonomous.
> Provenance trio validated: 14/14 experiments, 2,630 braids verified,
> cross-industry export (PROV-O, RO-Crate, DataCite) operational.
> 4 routing gaps documented for upstream teams.
> Next: rootPulse step handler activation, translation registry audit,
> blueGate depot rebuild, sovereign dispatch, arXiv.

---

*Wave 157k deep interstadial. 12 gates ONLINE. 0/0/0. Pipeline divergence RESOLVED (serde flatten + target-aware drift + rootPulse trio). Depot REBUILT 13/13 x86_64, 28 pushed. westGate provenance trio: 14/14 experiments PASS, 2,630 braids verified, cross-industry export live. 4 routing gaps documented. rootPulse graphs in neuralAPI. biomeGate registered + intermittent. K-Derm unified. 217 fossilized. Remaining: D12/D13 merge, rootPulse step handlers, translation registry audit, blueGate depot. Downstream: sovereign dispatch, arXiv, science E2E, graph viz.*
