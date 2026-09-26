# ecoPrimals Ecosystem Blurb — Wave 158 Rewake + Legal Primal + Mesh Expansion

**Date**: Sep 26, 2026 08:48 | **Wave**: 158 | **From**: overwatch (eastGate)
**Posture**: **REWAKE.** eastGate + golgiBody ONLINE. LAN gates OFFLINE (rewaking). northGate ENROLLING (Windows 11, RTX 5090). detroit.primals.eco LIVE (128 pages, BLAKE3 braided). primals.eco LIVE (Zola fixed). **Dispersal pattern PROVEN** (primal-as-site). **litho-core** extracted (6 modules). golgiBody cascade AUTONOMOUS (recovered from 3-week crash-loop). Milk-V Jupiter 2 (RISC-V RVA23) ARRIVED. **rustChip standalone** cleaned (367 tests, BrainChip README link pending). October rewake in progress.

---

## What Changed This Session (overwatch — Aug 16)

### bonsai-bt Forked + First Contact

**Source**: github.com/Sollimann/bonsai (MIT, v0.13.0, 207 commits, ~790 stars)
**Fork**: git.primals.eco/ecoPrimals/bonsai-bt (full mirror — all branches + tags)

Decision: Fork and evolve into a new ecoPrimals meta-primal — the DECIDE layer between squirrel REASON and biomeOS ROUTE. One-human project (Kristoffer Rakstad Solberg, Norway) with NASA Lunabotics production use.

Code audit: **0 unsafe**, 3,197 LOC core, 76 tests pass, 0 TODO/FIXME, 0 default deps.

**Exp125 LIVE** (primalSpring `08068ed4`): 5 behavior trees against NUCLEUS:
- **Tree 1**: Reactive health check (Sequence over capability domains) — PASS
- **Tree 2**: Compute fallback (Select — first-success-wins) — PASS
- **Tree 3**: Provenance pipeline (hash→store→DAG→sign chain) — PASS
- **Tree 4**: Serialization round-trip (550B JSON, BLAKE3 hashable, equality preserved) — PASS
- **Tree 5**: Memoryless reactive policy (re-evaluate conditions each tick) — PASS

23/24 checks pass (1 expected: no live NUCLEUS sockets in overwatch session).
`EcoAction` enum references Neural API domains, never primal names. Trees are content-addressable ecosystem artifacts.

Architecture: `squirrel → REASON | [name] → DECIDE | biomeOS → ROUTE | primals → ACT | sweetGrass → WITNESS | PathwayLearner → ADAPT`

5-phase ingestion: Phase 0 (code review + scyBorg license) → Phase 1 (sourDough scaffold) → Phase 2 (EcoAction, EcoBlackboard, provenance) → Phase 3 (Neural API behavior.*, tree.*) → Phase 4-5 (protocol + meta-primal integration)

### translate.js Evaluated — External Semantic Validator

**Assessment**: Do NOT fork. Use as-is for **Validation Class V: External Semantic** — can independently developed software correctly consume petalTongue's semantic output? Evidence package: freeze semantic contract → hash → integrate → publish failures.

### Fossilization Sweep

10 files fossilized to `fossilRecord/wave157k_enmeshment/`:
- biomeGate bootstrap AAR + sovereign dispatch session AAR (absorbed)
- eastGate enmeshment cascade AAR (all items CLOSED/DORMANT)
- nestGate content.put gap AAR + rootPulse overstep AAR (resolved)
- rhizoCrypt + sweetGrass deep debt AARs (shipped)
- swarmVine interstadial AAR (all items CLOSED)
- westGate enmeshment AAR + provenance trio AAR (absorbed)

**Total: 227 files fossilized** across 20 wave directories. **1,513 total records.** 11 active handoffs remain.

Full assessments: `whitePaper/subGen/contacts/BONSAI_BT_BEHAVIOR_TREE_EVALUATION.md`, `BONSAI_INGESTION_PLAN.md`, `TRANSLATE_JS_EXTERNAL_SEMANTIC_VALIDATION.md`

### Cascade Absorption (incoming AARs — Aug 16)

**biomeGate** — 2 AARs landed:
- **DRM hot-add root cause**: Single root cause behind 3 session kills (nouveau DRM node + Xorg hot-add). Machine-checked preflight + live DRM watch in `toadstool-cylinder`.
- **Measurement truth**: 4 bugs fixed (D3hot reads as cold, Tier 2 without FECS, sleeping GPU as warm, catalyst PC range). `RegisterRead` enum replaces raw `u32` at 10 sites. **Titan V Tier 1 CONFIRMED** (23 engines, PRAMIN accessible, reproducible). FECS PRI fault blocks Tier 2. K80 blocked by missing GK210 chipset entry — software gap, path forward: map `0xf2` onto `gk110b`. `toadstool sovereign handoff|status|strategies` CLI shipped.

**eastGate** — Ingestion AAR:
- exp125 validated (23/24). Socket naming mismatch identified (biomeOS `biomeos-neural.sock` vs discovery `neural-api-{family}.sock`) — known gap, not blocking.
- **rootPulse 6/6 graphs REGISTERED** (`af1dc9d3`): commit, harvest, branch, merge, diff, federate. biomeOS 1,608 tests pass. `graph.list` exposes all. **Item #10 CLOSED.**

**northGate** — tideGlass Phase 0 external review (GitHub→Forgejo cascade):
- 10-week gap assessed. All infrastructure prerequisites COMPLETE. Revised estimate: **5-7 focused days** (was 1-2 weeks).
- Priority 1: start Phase 0 this week. Priority 2: arXiv reviewer send (parallel, 6-8h). Priority 3: Gonzales reactivation (gated on Phase 0).
- Collaborator contact decay risk: fall semester starts ~Aug 26. CTF NDU requires preliminary data.
- **"The pivot point is now."**

**strandGate** — AMD full silicon activation AAR update (10/10 COMPLETE, cross-validation confirmed).

### Cascade Absorption (incoming AARs — Aug 17)

**strandGate** — Science pipeline status + full session AAR:
- **45 production configs BANKED**: SU(3) pure gauge, 3β × 3V × 5 seeds (16⁴/24⁴/32⁴)
- **Cross-GPU validated**: AMD RX 6950 XT vs NVIDIA RTX 3090, **0.19% delta** at β=6.20 32⁴
- **Dark silicon 7/8 lit**: ROPs (790G scatter-adds/s), RT cores (45× NVIDIA advantage), rasterizer (433M query/s AMD), depth buffer, video encoder, mesh shaders. Tensor cores blocked (needs PTX)
- **Protocol mismatch identified**: 16⁴/24⁴ at dt=0.01 vs 32⁴ at dt=0.0025 → systematic bias, 32⁴ 13-29σ below literature
- **Resolution**: unified protocol run (all volumes dt=0.0025, n_md=40, 2000+ warmup)
- **Upstream needs P1**: barraCuda configurable warmup count, plaquette time-series export for autocorrelation
- Full session AAR fossilized (`wave157k_interstadial/`)

**biomeGate** — 3 AARs landed (K80 wedge hunt + vendor excision + sovereign ground truth):
- **K80 wedge hunt**: 4 bugs found (sentinel-as-data pattern), all fixed. PROM VBIOS decoded at `BAR0+0x300000` — first K80 VBIOS obtained without vendor code. Die survives cold bring-up ×4. **Sole K80 blocker**: VBIOS opcode coverage (interpreter decodes 24%, a misparse)
- **Vendor tool excision**: GPU detection now native sysfs/procfs. nvidia-smi saw 1 of 4 GPUs and invented a 5th. 216 test targets recovered that had silently stopped compiling. Real `RwLock` guard-across-await bug found. Floating `rust-toolchain.toml` drift exposed (stable→1.97.1, 542 fmt violations, 682 clippy warnings)
- **SOVEREIGN_GROUND_TRUTH.md**: "No shader has ever executed on the sovereign path on any NVIDIA GPU." All verified GPU compute runs through wgpu/Vulkan with vendor drivers present. Tier ladder: 0→1→2→3 formalized
- **6 ecosystem-wide gaps raised**: (1) pin toolchain; (2) `--no-run` CI gate; (3) `cfg(all())` grep; (4) vendor tooling in barraCuda/coralReef; (5) `runtime/edge` limbo; (6) NVIDIA VRAM native source

### Concept Evolution: sporePrint → NUCLEUS-Served Live Data Surface (Aug 17)

sporePrint should evolve from a static Zola site into a **NUCLEUS-served live data surface** where the data and references are served by the underlying primal systems, and the semantic layer is exposed for translations.

**Architecture:**
```
NUCLEUS primals → cellMembrane (data pipeline) → petalTongue (semantic surface)
    ├── Live: gate status, test counts, provenance chains, spring results
    ├── Live: dataset catalog, CAS stats, depot versions
    ├── Static: philosophy, thesis, architecture docs (Zola templates)
    └── Semantic layer exposed for translate.js (Validation Class V)
```

**Why now**: petalTongue already serves nestgate.io with live primal data (Phase 2+3). The same pattern extends to primals.eco. This makes the site self-updating — when strandGate banks 45 QCD configs, the site reflects it. When a gate comes online, the status page shows it. No manual content updates needed for science data.

**Phasing**: Phase 0 (fix static site NOW). Phase 1 (live data endpoints via petalTongue). Phase 2 (cellMembrane data pipeline). Phase 3 (semantic layer for translate.js). Phase 4 (Google SEO).

---

## Gate Status Summary (Wave 158 — Rewake)

| Gate | Composition | Location | Status |
|------|-------------|----------|--------|
| **eastGate** | Full NUCLEUS + overwatch | House 2 | ✅ ONLINE. rustChip cleaned. Wave 158 cascade. |
| **golgiBody** | Caddy + Forgejo + Zola + cascade | Cloud (DO) | ✅ ONLINE. Cascade autonomous. detroit + primals.eco serving. |
| **northGate** | Tower Atomic (target) | House 1 | 🔄 ENROLLING. Windows 11, RTX 5090. Pushing to Forgejo. |
| **sporeGate** | Foreman + depot | House 1 | ⏸️ OFFLINE. Priority 1 rewake — cascade foreman. |
| **biomeGate** | Tower 4/4 + Node Atomic | House 1 | ⏸️ OFFLINE. Power on needed. |
| **graftGate** | FULL NUCLEUS (Darwin) | House 1 | ⏸️ OFFLINE. Power on needed. |
| **Jupiter 2** | NEW (RISC-V RVA23) | House 1 | 🆕 ARRIVED. Bring-up pending. 7th arch family. |
| **NUC bench** | Tower Atomic (target) | House 1 | 🆕 DDR3 NUCs — sub-builders, site hosts, mesh nodes. |
| **ironGate** | Full NUCLEUS + 14TB CAS | House 2 | ⏸️ OFFLINE. Power rebalance next week. |
| **strandGate** | Full NUCLEUS + dual EPYC | House 2 | ⏸️ OFFLINE. Power rebalance next week. 45 QCD configs banked. |
| **westGate** | Full NUCLEUS + 50.7TB ZFS | House 2 | ⏸️ OFFLINE. Power rebalance next week. |
| **blueGate** | ENMESHED (Windows) | House 2 | ⏸️ OFFLINE. Rack move incomplete. Depot 0/13 STALE. |
| **southGate** | NUCLEUS + canary | House 2 | ⏸️ OFFLINE. Power rebalance next week. |
| **grapheneGate** | Tower Atomic | Mobile | ADB deploy. |
| **iosGate** | BearDogApp | Mobile | 6th OS family. |
| **steamGate** | Tower Atomic | Mobile | Portable compute. |

---

## Remaining Infrastructure

| # | Item | Owner | Priority |
|---|------|-------|----------|
| 2 | cellMembrane UDS→TCP fallback (Windows health probes) | sporeGate (cellMembrane) | P2 |
| 4 | blueGate depot rebuild via autonomous dispatch | sporeGate foreman | P2 |
| 5 | `rust-toolchain.toml` GNU target for Windows | ironGate (songBird) | P2 |
| 6 | southGate SSH key enrollment | sporeGate ops | P3 |
| 7 | biomeGate full NUCLEUS composition | biomeGate (when active) | P3 |
| ~~10~~ | ~~rootPulse graph execution via biomeOS~~ | ~~eastGate (biomeOS)~~ | **DONE** (`af1dc9d3`, 6/6 graphs registered) |
| 11 | bearDog AEAD Neural API surfacing (last translation gap) | ironGate (bearDog) | P2 |
| 12 | sweetGrass auto-announce in depot binary | sporeGate (depot rebuild) | P2 |
| 15 | AlphaFold ingress Phase B+C completion | westGate | ACTIVE |
| 16 | tideGlass Phase 0 (gen5 sole bottleneck) | westGate | QUEUED |
| 17 | barraCuda: configurable warmup count in GpuHmcConfig | strandGate (barraCuda) | **P1** |
| 18 | barraCuda: plaquette time-series export for autocorrelation | strandGate (barraCuda) | **P1** |
| 19 | Ecosystem: pin `rust-toolchain.toml` versions (biomeGate finding) | all primals | P2 |
| 20 | Ecosystem: `cargo test --workspace --no-run` CI gate | sporeGate (CI) | P2 |
| 21 | Ecosystem: grep for `cfg(all())` vacuous-true (biomeGate finding) | all primals | P2 |

---

## Active Code Teams

| Team | Track | Status |
|------|-------|--------|
| **eastGate — primalSpring** | exp125 bonsai-bt integration | **ACTIVE** (parallel IDE). Testing behavior trees against live NUCLEUS. |
| **westGate — cellMembrane** | AlphaFold ingress pipeline | **ACTIVE**. Phase B running (10M+ files). |
| **strandGate — hotSpring** | SU(3) production campaigns | **45 CONFIGS BANKED.** Protocol correction run NEXT. NVIDIA β=5.90 still running. |
| **strandGate — barraCuda + coralReef** | DF64 sovereign shaders | **SHIPPED** (`4a3679f0` + `9c64cfa`). **Upstream P1s**: configurable warmup, plaquette time-series. |
| **biomeGate — toadStool** | Vendor tool excision + K80 sovereign | **SHIPPED** (10 commits). sysfs GPU detection. 216 tests recovered. 12 non-compiling targets remain. |
| **sporeGate — cellMembrane** | Cascade ops | **SHIPPED** (`3f9fa14`). Autonomous. |
| **westGate — rhizoCrypt** | rootPulse handlers | **SHIPPED** (`fa35ed3`). 1,858 tests. DORMANT. |
| **westGate — sweetGrass** | rootPulse handlers | **SHIPPED** (`f31e1bc`). 1,746 tests. DORMANT. |
| **ironGate — swarmVine** | gossip.relay topic fix | **CLOSED** (`31e3e0a`). DORMANT. |
| **eastGate — biomeOS** | D12/D13 + content.put | **ALL DONE**. DORMANT. |

---

## Downstream Patterns

| Track | Owner | Status |
|-------|-------|--------|
| **bonsai-bt meta-primal** | eastGate (overwatch → assigned) | **PHASE 0 — INGESTING** |
| **External semantic validation (translate.js)** | sporeGate (sporePrint/petalTongue) | ASSESSED |
| **Sovereign dispatch** | biomeGate (intermittent) | ACTIVE |
| **SSH → Tower Atomic graduation** (NanoWire Tiers 2-7) | sporeGate | NEXT |
| **Graph visualization** | ironGate (petalTongue) + eastGate (biomeOS) | SPEC FILED |
| **arXiv submission** | strandGate | ACTIVE |
| **Science pipeline E2E (G71)** | strandGate → ironGate → sporePrint | ACTIVE |
| **rootPulse graph execution** | eastGate (biomeOS) | REFRAMED |
| **AlphaFold Neural API ingress** | westGate | ACTIVE |
| **Gen5 critical path** | westGate | QUEUED |
| **sporePrint: Zola fix → NUCLEUS live surface (G14, D14)** | sporeGate (sporePrint + petalTongue + cellMembrane) | **CRITICAL — website NOT OPERABLE. Concept evolved: static → live data surface** |
| **whitePaper subgen** | overwatch (followup) | PLANNED |
| **westGate hardware upgrades** | westGate | READY |

---

## Depot Status

| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **13/13 CURRENT** | Rebuilt Aug 14. |
| `aarch64-unknown-linux-musl` | **15/15 CURRENT** | ironGate sub-builder. |
| `aarch64-apple-darwin` | **16/16 CURRENT** | graftGate. |
| `x86_64-pc-windows-gnu` | **0/13 STALE** | Awaiting autonomous dispatch. |

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
| biomeGate | hotSpring (sovereign dispatch) | ONLINE — Tower 4/4, Node Atomic, ember fleet 4/4 |

**New Primal (ingesting):**

| Repo | Source | Role | Status |
|------|--------|------|--------|
| **bonsai-bt** | Fork of github.com/Sollimann/bonsai | DECIDE layer meta-primal | Phase 0 (Forgejo mirror, exp125 first contact) |

---

## Architecture Reference

**NUCLEUS** = Tower + Nest + Node + biomeOS + petalTongue + squirrel + cellMembrane

| Atomic | Primals | Role |
|--------|---------|------|
| **Tower** | bearDog + songBird + skunkBat + swarmVine | Shared electron cloud: crypto, routing, defense, gossip |
| **Nest** | Tower + nestGate + rhizoCrypt + loamSpine + sweetGrass | Data identity: CAS + DAG + spine + braids |
| **Node** | Tower + toadStool + barraCuda + coralReef | Compute: dispatch + GPU + shaders |

**DECIDE layer** (ingesting): bonsai-bt behavior trees as execution policy between squirrel reasoning and biomeOS routing. Trees are serializable, content-addressable artifacts. `Behavior<EcoAction>` is generic over Neural API signals.

---

## K-Derm Membrane Topology

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

---

## NanoWire SSH Retirement

| Tier | Scope | Status |
|------|-------|--------|
| 1 | Sub-builder CI dispatch | **RETIRED** (3/3 builders enmeshed) |
| 2 | gate.pull/check/info, plasmid.trigger, service.* | NEXT |
| 3 | Depot push + CAS archival | After Tier 2 |
| 4-7 | Caddy, enrollment, relay, git transport | Future |

---

## Physical Topology — Rewake Plan

**House 1** (northGate location — online this week):
| Gate | Hardware | Status | Rewake |
|------|----------|--------|--------|
| **northGate** | Ryzen 9 9950X3D, RTX 5090, 96GB DDR5 | ENROLLING | Tower Atomic → full primal enrollment. Interim: Forgejo push. |
| **biomeGate** | GPU lab (Titan V, K80, multi-GPU) | OFFLINE | Power on, Tower 4/4 + Node should resume. |
| **sporeGate** | Foreman + depot + cascade hub | OFFLINE | **PRIORITY 1** — cascade foreman, depot authority, detroit braiding. |
| **graftGate** | Mac (Darwin builder) | OFFLINE | Power on, FULL NUCLEUS should resume. |
| **Milk-V Jupiter 2** | RISC-V RVA23, full vector | NEW | Bring-up — first `riscv64gc-unknown-linux-musl` target. 7th arch family. |
| **NUC bench** (DDR3 units) | Intel NUCs, low-power | NEW | Sub-builders, site hosts, mesh expansion nodes. Tower Atomic candidates. |

**House 2** (needs power rebalance — next week):
| Gate | Hardware | Status | Rewake |
|------|----------|--------|--------|
| **eastGate** | Ryzen, AKD1000, overwatch | ✅ ONLINE | Running now. |
| **ironGate** | i9-14900K, RTX 5070 Ti, 14TB | OFFLINE | Power rebalance needed. |
| **strandGate** | Dual EPYC, RTX 3090, QCD batch | OFFLINE | Power rebalance needed. |
| **westGate** | 50.7TB ZFS, provenance trio | OFFLINE | Power rebalance needed. |
| **blueGate** | Windows builder | OFFLINE | Rack move incomplete. |
| **southGate** | Validation canary, RTX 4060 | OFFLINE | Power rebalance needed. |

**Cloud** (always on):
| Gate | Hardware | Status |
|------|----------|--------|
| **golgiBody** | DigitalOcean VPS | ✅ ONLINE | Caddy, Forgejo, Zola, cascade, WG relay |

## Team Assignments — Wave 158

| # | Track | Team/Gate | Assignment |
|---|-------|-----------|------------|
| 1 | **northGate enrollment** | northGate + eastGate | WG mesh enrollment via golgi relay. Interim: push to Forgejo. Target: Tower Atomic → vine-bat zero-SSH. |
| 2 | **nucleus-deploy Windows fix** | eastGate (projectNUCLEUS) | 2 call sites: `deploy.rs` UDS + `below.rs` MetadataExt. lithoSpore `platform.rs` pattern. ~30 min. |
| 3 | **sporeGate rewake** | house 1 (physical) | Power on, verify cascade, depot harvest, detroit braiding pipeline. |
| 4 | **detroit → braid pipeline** | sporeGate + northGate | evidence.push → nestGate CAS → sweetGrass braid. Pipeline spec'd, needs sporeGate online. |
| 5 | **Milk-V Jupiter 2 bring-up** | eastGate (overwatch) | Boot, toolchain test, musl cross-compile probe. `riscv64gc-unknown-linux-musl` depot target. |
| 6 | **NUC bench composition** | house 1 | Tower Atomic on DDR3 NUCs — sub-builders, site hosts, mesh expansion. Light composition test. |
| 7 | **graftGate + biomeGate rewake** | house 1 (physical) | Power on, verify NUCLEUS/Tower compositions resume. |
| 8 | **House 2 power rebalance** | physical (next week) | ironGate, strandGate, westGate, southGate, blueGate. |
| 9 | **sporePrint: fix Zola → live surface → SEO** | sporeGate (when online) | Phase 0 DONE (Zola fixed). Phase 0.5: QCD data up. Phase 1+: live data endpoints. |
| 10 | **swarmVine + skunkBat evolution** | ironGate (when online) | vine-bat loop hardening. Target: zero-SSH gate enrollment via gossip + BTSP. |

---

## CONVERGENCE RULE

> **Rewake + Dispersal + Mesh Expansion.**
> eastGate + golgiBody ONLINE. LAN gates rewaking (Oct).
> northGate ENROLLING — first Windows gate with full primal enrollment target.
> detroit.primals.eco LIVE — legal primal pattern PROVEN (128 pages, 70+ edges, BLAKE3 braided).
> Dispersal pattern SPEC'D — any domain can produce a provenance-traced `.primals.eco` site.
> litho-core extracted — 6-module shared substrate (detroit → sporePrint convergence).
> golgiBody cascade AUTONOMOUS (3-week crash-loop → HEALTHY).
> primals.eco LIVE (Zola date fix, GSC resubmitted).
> rustChip STANDALONE (367 tests, API docs decoupled, BrainChip README link target).
> Milk-V Jupiter 2 ARRIVED (RISC-V RVA23, full vector — 7th architecture family).
> Near-term: vine-bat loop → zero-SSH enrollment. sovereign path: local boot → gossip → BTSP.
> nucleus-deploy Windows fix: 2 call sites (UDS + MetadataExt). lithoSpore platform.rs pattern.
> October: rewake LAN mesh, enroll northGate, blueGate + graftGate back online, Jupiter 2 bring-up.

---

*Wave 158 rewake. eastGate + golgiBody ONLINE. detroit.primals.eco LIVE (legal primal pattern). primals.eco LIVE. northGate enrolling (Windows 11, RTX 5090). Dispersal pattern proved + spec'd. litho-core extracted. golgiBody cascade autonomous. rustChip standalone cleaned. Milk-V Jupiter 2 arrived (RISC-V RVA23 — 7th arch family). Near-term: vine-bat zero-SSH enrollment, nucleus-deploy Windows fix (2 call sites), mesh rewake. October: LAN gates back, northGate full enrollment, blueGate + graftGate online, Jupiter 2 bring-up.*
