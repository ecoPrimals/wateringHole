<<<<<<< Updated upstream
# ecoPrimals Ecosystem Blurb — Wave 159 Rewake (Sep 28, 2026)

**Date**: Sep 28, 2026 10:45 | **Wave**: 159 | **From**: overwatch (eastGate)
**Posture**: **REWAKE.** eastGate + golgiBody + sporeGate ONLINE. northGate ENROLLING via primals-only (no SSH/nanowires). **4 LIVE SITES**: sporeprint.primals.eco (403 URLs), detroit.primals.eco (127 URLs), gorilla.primals.eco (20 URLs), guerillagorilla.primals.eco (alias). **All sitemaps 200.** GSC detroit: 97 pages discovered, Success. **Windows depot 16/16 PRIMALS** (all compile — up from 14/17). **nucleus-deploy Windows FIXED**. **cellMembrane UDS→TCP DONE**. **Three-tier dispersal PROVEN**. Milk-V Jupiter 2 ARRIVED (RISC-V RVA23). **3× Pi 500 ACQUIRED**. **8 architecture families.** House 2 power rebalance upcoming. Networking: House 2 all-10G MikroTik, 10G fiber to House 1 (eastGate), House 1 local 1G RJ45.

---

## What Changed (Wave 158–159 — Sep 26-28)

### Windows Cross-Compile: 16/16 PRIMALS ✅ (was 14/17)

All 16 primals now compile for `x86_64-pc-windows-gnu`. The remaining 3 blockers were fixed in one session:

| Primal | Fix | Commit | Pattern |
|--------|-----|--------|---------|
| **toadStool** | 4 files (byob_server, halo_dispatch, transport, sovereign) | `7f8f0ad08` | UDS + PCIe sysfs + sovereign CLI gating |
| **sweetGrass** | 1 file (braid_verify.rs) | `e546171` | crypto field `#[cfg(unix)]` |
| **sourDough** | 2 files (rpc_surface.rs, convergence.rs) | `f4d5160` | `#[cfg_attr(not(unix), allow(dead_code))]` on 9 items |
| **petalTongue** | 1 file (peptidoglycan.rs) | `7952cf32` | 1 `UnixStream` in CAS handler |

petalTongue was estimated "Large (34+ unix sites)" — turned out to be **1 function, 10 lines**. The `#[cfg(unix)]` + `#[cfg(not(unix))]` fallback pattern is now proven across every primal.

### guerillaGorilla LAUNCHED (gorilla.primals.eco)
- 20-page methodology site (fEAR, preSCENT, STRIDe, amicusContra, pursuit predation, cross-protection, dispersal pattern)
- Three-tier dispersal proven: sporePrint (catalogue) → guerillaGorilla (methodology) → detroit (case study)
- Registered in sporePrint sources.toml + entity registry (commit `854391c0`)

### northGate Bootstrap Strategy: Primals Only
- No SSH, no sovereign nanowires — pure primal mesh enrollment
- Pull binaries from golgiBody depot (`https://depot.primals.eco/primals/x86_64-pc-windows-gnu/`)
- Start Tower Atomic → songBird discovery → skunkBat enrollment → swarmVine gossip → mesh join
- sporeGate team managing depot sync + blurb delivery

### 26 Handoffs Fossilized
- All Wave 157k AARs (biomeGate K80/Kepler deep dive, strandGate science, westGate data, tideGlass Phase 0) moved to `fossilRecord/wave158_windows_rewake/`
- Handoffs reduced from 35 → 9 active documents

---

## Gate Status (Wave 159)

| Gate | Composition | Location | Status | Priority |
|------|-------------|----------|--------|----------|
| **eastGate** | Full NUCLEUS + overwatch | House 2 | ✅ ONLINE | — |
| **golgiBody** | Caddy + Forgejo + Zola + cascade | Cloud (DO) | ✅ ONLINE | — |
| **sporeGate** | Foreman + depot + cascade hub | House 1 | ✅ ONLINE | — |
| **northGate** | Tower Atomic (target) | House 1 | 🔄 ENROLLING | P1 — primal-only bootstrap |
| **3× Pi 500** | Tower Atomic (target) | House 1 | 🆕 ACQUIRED | P2 — always-on mesh infra |
| **Jupiter 2** | NEW (RISC-V RVA23) | House 1 | 🆕 ARRIVED | P2 — 7th arch bring-up |
| **biomeGate** | Tower + Node (TR 3970X, HBM2) | House 1 | ⏸️ OFFLINE | P3 — power on when ready |
| **graftGate** | NUCLEUS (Darwin, M4) | House 1 | ⏸️ OFFLINE | P3 — power on when ready |
| **NUC bench** | Tower Atomic (DDR3 NUCs) | House 1 | 🆕 Available | P3 — sub-builders |
| **ironGate** | NUCLEUS + 14TB CAS (i9-14900K) | House 2 | ⏸️ OFFLINE | P2 — House 2 rebalance |
| **strandGate** | NUCLEUS + EPYC (64C/128T) | House 2 | ⏸️ OFFLINE | P2 — House 2 rebalance |
| **westGate** | NUCLEUS + 50.7TB ZFS | House 2 | ⏸️ OFFLINE | P3 — House 2 rebalance |
| **southGate** | NUCLEUS + canary (5800X3D) | House 2 | ⏸️ OFFLINE | P3 — House 2 rebalance |
| **blueGate** | Windows builder | House 2 | ⏸️ OFFLINE | P3 — rack move |

---

## Live Sites

| Site | URLs | Sitemap | GSC |
|------|------|---------|-----|
| **sporeprint.primals.eco** | 403 | ✅ 200 | Verified, domain migration |
| **detroit.primals.eco** | 127 | ✅ 200 | 97 pages discovered, Success |
| **gorilla.primals.eco** | 20 | ✅ 200 | NEW |
| **guerillagorilla.primals.eco** | alias | ✅ 200 | alias of gorilla |
| **primals.eco** | — | — | 301 → sporeprint |

---

## Depot Status (Sep 28)

| Target | Binaries | Status |
|--------|----------|--------|
| `x86_64-unknown-linux-musl` | **18/18** | ✅ CURRENT |
| `aarch64-unknown-linux-musl` | **15/15** | ✅ CURRENT (ironGate built) |
| `aarch64-apple-darwin` | **16/16** | ✅ CURRENT (graftGate built) |
| `x86_64-unknown-linux-gnu` | **14/14** | ✅ CURRENT |
| `x86_64-pc-windows-gnu` | **16/16 COMPILE** | 🔄 Depot stale — needs rebuild + sync |

### Windows Depot Action Item

All 16 primals now *compile* for Windows. The golgiBody depot has stale `.exe` binaries (some from August). **sporeGate team** needs to:
1. `cargo build --release --target x86_64-pc-windows-gnu` for all 16 primals
2. Copy to `plasmidBin/primals/x86_64-pc-windows-gnu/`
3. `rsync` to golgiBody depot
4. Regenerate `checksums.toml` with BLAKE3
=======
# ecoPrimals Ecosystem Blurb — Wave 157k Interstadial (Post-Enmeshment)

**Date**: Aug 13, 2026 09:04 | **Wave**: 157k | **From**: sporeGate (foreman)
**Posture**: 11 gates ONLINE (biomeGate DOWN). **0/0/0.** Stadial item #1 CLOSED: blueGate + ironGate enmeshed into cascade via Tower Atomic TCP dispatch. **SSH deprecated for sub-builder dispatch (R-SUB in NanoWire checklist confirmed RETIRED).** CAS replication to ironGate 12TB WIRED. Gate hygiene composition-native. Build pipeline fully autonomous for musl + aarch64 targets. Windows target ready for first autonomous rebuild.

---

## What Changed (sporeGate ops — Aug 13 07:43–09:00)

### Sub-Builder Enmeshment (Stadial #1 CLOSED)

The foreman cascade can now auto-dispatch cross-architecture builds to ironGate and blueGate without SSH:

```
BEFORE:  sporeGate --SSH--> ironGate/blueGate "membrane plasmid.harvest ..."
NOW:     sporeGate --call_tcp(riboCipher)--> builder.serve :9800 → JSON-RPC plasmid.harvest
```

**Changes:**
- `SubBuilderEntry` gains `builder_host` / `builder_port` — direct TCP when mesh relay unavailable
- `resolve_builder_endpoint()` prefers TCP over MeshRelay (bridge until relay registration universal)
- `builder.serve` handles riboCipher `[0xEC, 0x01]` signal prefix (compatible with `call_tcp` framing)
- ironGate: `membrane-builder.service` (systemd, enabled, `:9800`, UFW opened for LAN)
- blueGate: rebuilt from `e8d4ffa`, WMI-detached process, scheduled task for reboot persistence
- Both verified end-to-end: `health` + `plasmid.staleness` via riboCipher-framed TCP from sporeGate

**Commits:**
- `e8d4ffa` cellMembrane — enmesh: TCP fallback + riboCipher signal handling
- `f8406bac6` wateringHole — manifest: builder_host/port for TCP dispatch

### SSH Deprecation Cross-Solve

This enmeshment **retires SSH for all sub-builder dispatch** (NanoWire checklist item R-SUB). The same TCP JSON-RPC pattern can now graduate the remaining SSH uses:

| SSH Use | Current | Tower Atomic Replacement | Status |
|---------|---------|--------------------------|--------|
| Sub-builder dispatch | `ssh gate "membrane plasmid.harvest"` | `call_tcp(builder_host:9800, plasmid.harvest)` | **RETIRED** |
| CAS archival | `ssh::scp_from(golgi, old_binary)` | `call_tcp` + binary relay RPC or HTTPS GET | Next |
| Depot push | `ssh::scp_to(golgi, new_binary)` | `call_tcp` + binary relay RPC or HTTPS PUT | Next |
| Gate pull/check | `ssh gate "membrane temporal.cascade"` | `cascade.notify` gossip (already live) | Parallel |
| Service ops | `ssh gate "systemctl ..."` | `service.*` capability RPC | Future |

The `builder.serve` pattern (TCP listener + riboCipher framing + JSON-RPC dispatch) is the template for all remaining SSH retirements. Each gate that runs `builder.serve` can be extended with additional capabilities (`depot.push`, `depot.pull`, `service.status`) on the same port.

---

## Remaining Stadial Work

| # | Item | Owner | Status |
|---|------|-------|--------|
| ~~1~~ | ~~Enmesh blueGate Windows builder into cascade~~ | ~~sporeGate~~ | **CLOSED.** TCP dispatch live, riboCipher compatible. |
| 2 | graftGate SSH key enrollment + builder.serve | physical | BLOCKED — M4 Mac Mini, physical access needed |
| 3 | southGate SSH key enrollment | overwatch | Port open, key not authorized |
| 4 | biomeGate SSH recovery | physical | GPU lab DOWN, eventual |
| 5 | westGate CAS enrollment | sporeGate | LAN IP not in topology — 50.7TB cold CAS target |
| 6 | **Graduate CAS archival from SSH to TCP relay** | sporeGate | NEW — use builder.serve pattern for `depot.cas_push` capability |
| 7 | **Graduate depot push from SSH to TCP relay** | sporeGate | NEW — use builder.serve pattern for `depot.receive` capability |

---

## Active Code Teams (4 tracks, rest dormant)

| Team | Track | Status |
|------|-------|--------|
| **eastGate — biomeOS** | `deploy.result` gossip emission via swarmVine | Last orchestration gap. primalSpring Phase 2 scaffolding ready to consume. |
| **eastGate — primalSpring** | Wire `FleetDeployHealth` into `nucleus_launcher` CLI | Integration once biomeOS Phase 1 lands. |
| **sporeGate — cellMembrane** | `native_braid.py` → Rust (1,259 LOC) | westGate/wateringHole scope, not cellMembrane repo. Coordination needed. |
| **westGate — nestGate** | nestgate.io Phase 3: `/cas/{hash}` via `content.locate` | `content.locate` mesh scope WIRED. Endpoint plumbing. |

All other primal code teams are **dormant** — code is stable, no evolution needed.
>>>>>>> Stashed changes

---

## Teams — Wave 159 Rewake

<<<<<<< Updated upstream
### Design Philosophy: Convergence over Assignment
=======
| Track | Description | Owner |
|-------|-------------|-------|
| **SSH → Tower Atomic graduation** | Extend `builder.serve` to handle `depot.*`, `service.*`, `gate.*` capabilities. Each graduated capability removes one SSH call site from the NanoWire checklist. | sporeGate |
| **nestgate.io Phase 3** | `/cas/{hash}` via `content.locate` mesh query. Data Braids card. | westGate + golgiBody |
| **arXiv submission** | Murillo/Chuna QCD preprint 41/42. Wire live site + reviewer send. | strandGate |
| **Science pipeline E2E (G71)** | GPU data → pseudoSpore → NFT → reviewer. | strandGate → ironGate → sporePrint |
| **tideGlass cell boot** | Cell 2026 GPS rebuild on westGate. CAS federation now live. | westGate |
| **sporePrint refresh (G14)** | pseudoSpore LIVE. QCD page + science artifacts. | ironGate |
>>>>>>> Stashed changes

The Wave 157k team assignments (ironGate = primal workhorse, strandGate = compute trio, etc.) assumed 11+ gates online simultaneously. That world is paused. For the rewake:

- **eastGate** is the only development authority. All code ships from here.
- **sporeGate** is the operational authority. Cascade, depot, build pipeline.
- **golgiBody** is the relay. Forgejo, Caddy, depot serving, WireGuard hub.
- **Gate teams** are deployment validators, not code owners. When a gate comes online, its team pulls, builds, validates, and reports. They don't push code — they push AARs.

<<<<<<< Updated upstream
### Active Teams
=======
| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **15/15 CURRENT** | Pushed to 5 gates |
| `aarch64-unknown-linux-musl` | **15/15 REBUILT** | ironGate sub-builder, CAS replicated |
| `aarch64-apple-darwin` | **5/15 refreshed** | graftGate, blocked on SSH for remaining 10 |
| `x86_64-pc-windows-gnu` | **STALE → READY** | blueGate builder enmeshed — first autonomous rebuild on next cascade |
>>>>>>> Stashed changes

| Team | Authority | Primals | Role |
|------|-----------|---------|------|
| **overwatch** (eastGate) | Code + orchestration | All 16 | Primary development, cross-compile, architecture decisions |
| **sporeGate ops** | Build + deploy | cellMembrane, lithoSpore | Cascade timers, depot sync, Forgejo hooks, site builds |
| **publicRecord** (sporeGate parallel IDE) | Content | detroit-build, guerillaGorilla | Evidence pipeline, OSINT loading, site content |
| **northGate** (House 1) | Deployment validator | Tower Atomic consumer | Primal-only mesh enrollment, OSINT loading |

### Gate Teams (Activate on Rewake)

<<<<<<< Updated upstream
When a gate powers on, its team activates with a focused mission:
=======
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
| biomeGate | — | DOWN (GPU lab) |
>>>>>>> Stashed changes

| Gate | Team Mission | First Task |
|------|-------------|------------|
| **biomeGate** | HBM2 + NPU validation | hotSpring resume, Titan V + MI50 toadStool dispatch |
| **graftGate** | Darwin depot refresh | `cargo build --release` all 16 primals on M4 |
| **ironGate** | Primal workhorse + aarch64 builder | Full NUCLEUS validate, aarch64 depot rebuild |
| **strandGate** | HPC + science compute | hotSpring QCD production (45 configs banked), toadStool + barraCuda workloads |
| **westGate** | Data + provenance root | ZFS health check, nestGate CAS validation, 50.7TB archive |
| **southGate** | NUCLEUS canary | Full deployment validation, regression suite |
| **blueGate** | Windows native builder | Replace cross-compile with native Windows builds |

### Primal Ownership (Code Authority = eastGate)

All 16 primals are developed on eastGate. Gate teams validate deployments and report findings.

| Atomic | Primals | Gate Affinity (validation) |
|--------|---------|--------------------------|
| **Tower** | bearDog, songBird, skunkBat | Every gate runs Tower. Universal. |
| **Nest** | nestGate, rhizoCrypt, loamSpine, sweetGrass | westGate (storage root), ironGate (CAS validation) |
| **Compute** | toadStool, barraCuda, coralReef | strandGate (HPC), biomeGate (HBM2/NPU) |
| **Orchestrator** | biomeOS | eastGate (primary), southGate (canary) |
| **Surface** | petalTongue | ironGate (viz), sporeGate (peptidoglycan depot) |
| **Gossip** | swarmVine | Universal — every gate, every mesh |
| **Tools** | squirrel, sourDough, bingoCube | eastGate (development only) |

### Meta-Primals

<<<<<<< Updated upstream
| Name | Role | Status |
|------|------|--------|
| **guerillaGorilla** | ACCOUNTABILITY layer (methodology) | ACTIVE — gorilla.primals.eco LIVE |
| **bonsai-bt** | DECIDE layer (behavior trees) | Phase 0 — forked, 23/24 passing |

---

## Team Assignments — Wave 159 (Reset)

| # | Track | Owner | Status |
|---|-------|-------|--------|
| 1 | **northGate primal-only bootstrap** | sporeGate + northGate | 🔄 Depot sync, blurb delivery, primal enrollment |
| 2 | **Windows depot rebuild (16/16)** | sporeGate | 🔄 All compile — needs `cargo build --release` + depot sync |
| 3 | **House 2 power rebalance** | physical (overwatch) | ⏸️ ironGate, strandGate, westGate, southGate, blueGate |
| 4 | **Pi 500 cluster bring-up** | House 1 | ⏸️ 3× aarch64, 15/15 depot ready, Tower Atomic target |
| 5 | **Jupiter 2 bring-up** | eastGate | ⏸️ RISC-V RVA23, 7th arch, targets installed |
| 6 | **biomeGate + graftGate power on** | physical (House 1) | ⏸️ When ready |
| 7 | **detroit content evolution** | publicRecord team | 🔄 Dynasty expansion, FOIA responses, OSINT loading |
| 8 | **cellMembrane cascade.notify** | sporeGate (cellMembrane team) | ⏸️ NanoWire Tier 2 unlock (spec'd in CELLMEMBRANE_WAVE159_CASCADE_NOTIFY) |
| 9 | **arXiv Rung 1 send** | eastGate | ⏸️ When strandGate wakes |
| 10 | **NUC bench Tower Atomic** | House 1 | ⏸️ DDR3 NUCs — mesh expansion |

---

## Key Specs (Active)

| Spec | Path | Status |
|------|------|--------|
| Dispersal Pattern | `specs/DISPERSAL_PATTERN.md` | PROVEN (3 sites, litho-core substrate) |
| Composition Contract | `specs/COMPOSITION_CONTRACT.md` | Stable |
| Transport Abstraction | `specs/TRANSPORT_ABSTRACTION_SPEC.md` | Stable |
| NanoWire Retirement | `specs/NANOWIRE_RETIREMENT_CHECKLIST.md` | Tier 1 DONE, Tier 2 in progress |
| Outer Membrane Topology | `specs/OUTER_MEMBRANE_TOPOLOGY.md` | Current |
| Cascade Timer | `specs/WATERFALL_CASCADE_TIMER_SPEC.md` | LIVE on sporeGate |

---

## CONVERGENCE RULE

> **Rewake + Mesh Expansion + Primal-Only Bootstrap.**
> eastGate + golgiBody + sporeGate ONLINE. northGate ENROLLING (primals only — no SSH).
> 4 LIVE SITES. All sitemaps 200. GSC Success.
> **Windows 16/16 primals compile** (depot rebuild pending).
> guerillaGorilla LAUNCHED. Three-tier dispersal PROVEN.
> nucleus-deploy FIXED. cellMembrane UDS→TCP DONE.
> 3× Pi 500 acquired. Jupiter 2 arrived. 8 arch families.
> 26 handoffs fossilized — clean slate for rewake.
> Teams reset: eastGate = code authority, sporeGate = ops authority, gate teams = validators.
> October: House 2 power rebalance, northGate primal bootstrap, Pi 500 + Jupiter 2 bring-up.
> *"Beside the small. Against unaccountable power. For the record."*

---

**See also**: [`infra/wateringHole/HARDWARE.md`](../HARDWARE.md) — full fleet inventory (16+ gates, 8 ISAs, networking topology, acquisition wishlist).

*Wave 159 rewake. 3 gates + golgiBody ONLINE. 4 live sites, all sitemaps 200. Windows 16/16 primals compile (depot rebuild pending). guerillaGorilla launched. Three-tier dispersal proven. 26 handoffs fossilized. Teams reset for rewake — eastGate code authority, sporeGate ops authority, gate teams validate. 3× Pi 500 + Jupiter 2 new hardware. northGate enrolling via primals only. October: House 2 power, mesh expansion, 7th arch bring-up.*
=======
## CONVERGENCE RULE

> **Stadial #1 CLOSED.** Sub-builder dispatch is Tower Atomic TCP — SSH RETIRED for this path.
> The `builder.serve` pattern (TCP + riboCipher + JSON-RPC) is the template for graduating
> ALL remaining SSH uses. Each capability added to `builder.serve` removes one SSH call site.
> Overwatch: notify blueGate their builder is enmeshed and Windows depot will auto-rebuild
> on next cascade. graftGate needs SSH key enrollment for Darwin builder.serve deployment.

---

*Wave 157k interstadial post-enmeshment. 0/0/0. Stadial #1 CLOSED. Sub-builder dispatch: SSH → Tower Atomic TCP (RETIRED). blueGate + ironGate enmeshed. CAS replication wired. builder.serve is the template for all SSH retirement. Next: graduate CAS archival + depot push from SSH to TCP relay. Downstream: deploy.result gossip, nestgate.io Phase 3, arXiv, science E2E.*
>>>>>>> Stashed changes
