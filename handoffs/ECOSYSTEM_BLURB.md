# ecoPrimals Ecosystem Blurb — Wave 157k Interstadial (K-Derm Topology Checkpoint)

**Date**: Aug 13, 2026 11:30 | **Wave**: 157k | **From**: overwatch (eastGate)
**Posture**: 11 gates ONLINE (biomeGate DOWN — wipe + reinstall pending). **0/0/0.** ALL stadial code tracks CLOSED. ALL 3 sub-builders ENMESHED (ironGate + blueGate + graftGate via TCP/riboCipher :9800). SSH RETIRED for sub-builder dispatch. Primal code teams DORMANT. Inner membrane: NUCLEUS dogfooded on all gates. Peptidoglycan: nestgate.io Phase 2+3 LIVE. Outer membrane: external sovereignty only.

---

## What Changed Since Last Blurb

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

### biomeGate — REIMAGED → BOOTSTRAP PENDING

- Fresh Ubuntu 24.04 installed. Cursor + RustDesk installed.
- Previous failure: GlowPlug VFIO persistence broke boot (diesel engine lesson)
- **Next**: gate spin-up blurb → connectivity → sync → Tower → NUCLEUS
- **Then**: runtime-only VFIO for RTX 5060 first, Titan V + K80 after validation
- AAR filed: `BIOMEGATE_RECOVERY_AAR_AUG13_2026.md`

### Silicon Exploration Assignments — NEW

Cross-product mapping of every fixed-function silicon unit (GPU/NPU/CPU) × gate × spring. Documents exploration priorities per gate. Canonical reference: `handoffs/SILICON_EXPLORATION_ASSIGNMENTS.md`.

---

## Remaining Work

### Immediate (Pre-biomeGate Return)

| # | Item | Owner | Priority |
|---|------|-------|----------|
| 1 | D12/D13 upstream merge to biomeOS | eastGate (biomeOS team) | P1 |
| 2 | cellMembrane UDS→TCP fallback for health probes (Windows) | sporeGate (cellMembrane) | P2 |
| 3 | swarmVine `mesh.relay` `topic` param alignment | ironGate (swarmVine/songBird) | P2 |
| 4 | blueGate depot rebuild via autonomous dispatch | sporeGate foreman | P2 |
| 5 | `rust-toolchain.toml` GNU target for Windows | ironGate (songBird) | P2 |
| 6 | southGate SSH key enrollment | sporeGate ops | P3 |
| 7 | southGate LAN IP correction in manifest | overwatch | **DONE** (.149→.148) |

### biomeGate Fresh Deploy (Post-Reinstall)

| Step | Action |
|------|--------|
| 1 | Fresh Ubuntu 24.04 install with SSH enabled |
| 2 | Set `multi-user.target` default (no display manager) |
| 3 | Pre-enroll eastGate SSH key in `/root/.ssh/authorized_keys` |
| 4 | Register `lan_ip` in ecosystem manifest |
| 5 | Pull from depot, deploy Tower Atomic, start biomeOS |
| 6 | Verify mesh + gossip + NUCLEUS composition |
| 7 | Redesign GlowPlug: runtime-only VFIO, no boot persistence |
| 8 | Validate on RTX 5060 only before re-adding Titan V / K80 |

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

## Active Code Teams — ALL DORMANT

| Team | Track | Status |
|------|-------|--------|
| ~~**eastGate — biomeOS**~~ | ~~`deploy.result` gossip~~ | **DONE** (`f80e5f2a`). Dormant. |
| ~~**eastGate — primalSpring**~~ | ~~Wire `FleetDeployHealth`~~ | **DONE** (`d15ab028`, v0.9.50). Dormant. |
| ~~**sporeGate — cellMembrane**~~ | ~~`native_braid.py` → Rust~~ | **RETIRED** by westGate (`membrane content.braid`). |
| ~~**westGate — nestGate**~~ | ~~nestgate.io Phase 3~~ | **LIVE.** `/cas/{hash}` + provenance routes. |
| **strandGate — barraCuda** | Silicon saturation gaps | Science-track, not stadial. 6 gaps exposed. |

All primal code teams are **dormant**. Remaining work is infrastructure ops, upstream merges, and science campaigns.

---

## Downstream Patterns (After Stadial Closes)

| Track | Description | Owner |
|-------|-------------|-------|
| **biomeGate fresh deploy** | Validates complete Tower → NUCLEUS deployment on clean hardware. First test of diesel engine lessons. | overwatch + biomeGate |
| **SSH → Tower Atomic graduation** | Extend `builder.serve` for `depot.*`, `service.*`, `gate.*` capabilities. | sporeGate |
| **nestgate.io Phase 3** | `/cas/{hash}` via `content.locate` mesh query. Data Braids card. | westGate + golgiBody |
| **arXiv submission** | Murillo/Chuna QCD preprint 41/42. Wire live site + reviewer send. | strandGate |
| **Science pipeline E2E (G71)** | GPU data → pseudoSpore → NFT → reviewer. | strandGate → ironGate → sporePrint |
| **Silicon exploration matrix** | Gate × spring × unit cross-product. AARs per gate. | all compute gates |
| **tideGlass cell boot** | Cell 2026 GPS rebuild on westGate. CAS federation now live. | westGate |
| **sporePrint refresh (G14)** | pseudoSpore LIVE. QCD page + science artifacts. | ironGate |

---

## Depot Status

| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **15/15 CURRENT** | Pushed to 5 gates |
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
| biomeGate | — | REIMAGED (bootstrap pending — spin-up blurb issued) |

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
│   └── biomeGate (GPU lab — REIMAGED, bootstrap pending)
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

9 AARs/handoffs fossilized to `fossilRecord/wave157k_interstadial/` this wave:
- `BLUEGATE_WAVE157K_INTERSTADIAL_AAR.md` — absorbed into ortho + blurb
- `STRANDGATE_FULL_SILICON_SATURATION_AAR_157k.md` — absorbed into ortho
- `GRAFTGATE_WAVE157K_BUILDER_SERVE_AAR.md` — absorbed into ortho + nanowire
- `GRAFTGATE_WAVE157K_FULL_DARWIN_DEPOT_AAR.md` — superseded by builder.serve AAR
- `GRAPHENEGATE_FULL_NUCLEUS_DEPLOY_AAR_AUG13_2026.md` — absorbed into ortho
- `BLUEGATE_DEPOT_PUSH_GUIDE.md` — superseded by builder.serve enmeshment (SSH→TCP)
- `TEAM_WORK_VECTORS.md` — superseded by blurb team assignments
- `SPOREPRINT_BLURB.md` — acted upon, superseded by current blurb
- `TEAM_STARTUP_BLURB_TEMPLATE.md` — self-marked SUPERSEDED, replaced by 3-tier system

Total: **212 files fossilized** across 19 wave directories. **1,489+ total records.**

---

## CONVERGENCE RULE

> **K-Derm topology checkpoint.** Inner membrane = NUCLEUS dogfooded on all gates.
> Peptidoglycan = primal-served (nestgate.io Phase 2+3 LIVE via petalTongue).
> Outer membrane = external sovereignty only (Cloudflare, Caddy TLS, Zola static).
> All 3 sub-builders enmeshed via TCP/riboCipher. SSH RETIRED for dispatch.
> 9 team assignments issued. D12/D13 biomeOS merge is the only code action.
> biomeGate fresh deploy validates the full pipeline on clean hardware.
> Graph visualization, sporePrint refresh, and whitePaper subgen are downstream.

---

*Wave 157k interstadial — K-Derm topology checkpoint. 0/0/0. Inner membrane: NUCLEUS dogfooded, all gates cytoplasm. Peptidoglycan: nestgate.io Phase 2+3 LIVE. Outer: external sovereignty only. ALL 3 sub-builders ENMESHED. 9 team assignments issued. 9 AARs fossilized (212 total). Remaining: biomeGate fresh deploy, D12/D13 merge, UDS→TCP fallback, mesh.relay topic, graph viz spec. Downstream: arXiv, science E2E, whitePaper subgen, sporePrint refresh.*
