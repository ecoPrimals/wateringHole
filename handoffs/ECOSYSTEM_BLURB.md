# ecoPrimals Ecosystem Blurb — Wave 158+ Operational (Sep 27, 2026)

**Date**: Sep 27, 2026 08:27 | **Wave**: 158+ | **From**: overwatch (eastGate)
**Posture**: **OPERATIONAL.** eastGate + golgiBody + sporeGate ONLINE. northGate ENROLLING. **4 LIVE SITES**: sporeprint.primals.eco (403 URLs), detroit.primals.eco (127 URLs), gorilla.primals.eco (20 URLs), guerillagorilla.primals.eco (alias). **All sitemaps 200.** GSC detroit: 97 pages discovered, Success. **Windows depot 14/17** (3 stale — team fixes pending). **nucleus-deploy Windows FIXED** (commit `58f6296`). **cellMembrane UDS→TCP DONE** (item #2 closed). **Three-tier dispersal PROVEN** (sporePrint → guerillaGorilla → detroit). **Sitemap P0 RESOLVED.** Milk-V Jupiter 2 ARRIVED (RISC-V RVA23). **3× Pi 500 ACQUIRED** (aarch64-linux, keyboard-integrated). **8 architecture families.** HARDWARE.md written — full fleet inventory. October: mesh rewake + House 2 power rebalance. Networking: House 2 all-10G MikroTik, 10G fiber to House 1 (eastGate), House 1 local 1G RJ45.

---

## What Changed (Wave 158 — Sep 26-27)

### guerillaGorilla LAUNCHED (gorilla.primals.eco)
- **20-page methodology site** — fEAR, preSCENT, STRIDe, amicusContra, pursuit predation, cross-protection, dispersal pattern
- **Three-tier dispersal proven**: sporePrint (catalogue) → guerillaGorilla (methodology) → detroit (case study)
- **Two aliases**: gorilla.primals.eco (primary) + guerillagorilla.primals.eco
- **Repos**: git.primals.eco/protoKarya/guerillaGorilla + github.com/protoKarya
- **scyBorg triple licensed** (AGPL-3.0 + ORC + CC-BY-SA 4.0)

### Sitemap P0 RESOLVED
- `content/sitemap/` → `content/site-map/` unblocked Zola sitemap.xml generation
- golgiBody build permissions fixed (public/ root→git)
- **All 3 sitemaps returning 200**: sporeprint (403 URLs), detroit (127 URLs), gorilla (20 URLs)

### cellMembrane UDS→TCP Fallback DONE
- Commit `f99583c` — 1,384 tests pass, cross-compiled 3 arches, membrane.exe BLAKE3 verified
- Windows health probes now use TCP fallback — no more false DEGRADED
- **Item #2 CLOSED** — strike from remaining infrastructure

### Windows Depot: 13/17 CURRENT (was 0/13 STALE)
- sporeGate rebuilt 13 `.exe` binaries from current source on golgiBody
- 12 leaked musl ELF binaries cleaned from Windows depot
- primalSpring IPC fully `#[cfg(unix)]` gated (`24f71cb7`)
- **4 primals still blocked**: toadStool (34 files), petalTongue (1 file), sweetGrass (1 field), sourDough (11 errors)

### northGate Concepts (Sep 27)
- **amicusContra** named — guerillaGorilla's outward projection function (downward/lateral/upward)
- **The Machine** — philosophy doc drafted (atlasHugged → detroit, `draft: true`)
- **Dispersal site concept** — wildcard subdomain evolution target (`*.primals.eco`)
- **Detroit dynasty expansion** — 12 new pages, 35+ actors, Stallworth/Kilpatrick dynasties
- **OSINT scrape** — BCF 990s (12yr data), Banks church conviction (Feb 2026), ghost employees

### rustChip Standalone (Sep 11)
- 367 tests pass, 0 fail. API docs decoupled from ecoPrimals internals
- BrainChip will link from their README — pending clean standalone experience
- `test_device_open` fixed (was panicking without hardware)

---

## Gate Status (Wave 158+)

| Gate | Composition | Location | Status |
|------|-------------|----------|--------|
| **eastGate** | Full NUCLEUS + overwatch | House 2 | ✅ ONLINE. Wave 158 cascade. |
| **golgiBody** | Caddy + Forgejo + Zola + cascade | Cloud (DO) | ✅ ONLINE. Cascade autonomous. 4 sites serving. |
| **sporeGate** | Foreman + depot + cascade hub | House 1 | ✅ ONLINE. Windows depot 13/17. Refocused on core duties. |
| **northGate** | Tower Atomic (target) | House 1 | 🔄 ENROLLING. Windows 11, RTX 5090. Pushing to Forgejo. |
| **biomeGate** | Tower 4/4 + Node Atomic | House 1 | ⏸️ OFFLINE. Power on needed. |
| **graftGate** | FULL NUCLEUS (Darwin) | House 1 | ⏸️ OFFLINE. Power on needed. sourDough Windows fix (11 errors). |
| **Jupiter 2** | NEW (RISC-V RVA23) | House 1 | 🆕 ARRIVED. Bring-up pending. 7th arch family. |
| **3× Pi 500** | Tower Atomic (target) | House 1 | 🆕 ACQUIRED. aarch64-linux. 15/15 depot ready. Mesh gossip / site hosts. |
| **NUC bench** | Tower Atomic (target) | House 1 | 🆕 DDR3 NUCs — sub-builders, site hosts, mesh nodes. |
| **ironGate** | Full NUCLEUS + 14TB CAS | House 2 | ⏸️ OFFLINE. Power rebalance next week. petalTongue fix (1 file). |
| **strandGate** | Full NUCLEUS + dual EPYC | House 2 | ⏸️ OFFLINE. Power rebalance next week. toadStool fix (34 files). 45 QCD configs banked. |
| **westGate** | Full NUCLEUS + 50.7TB ZFS | House 2 | ⏸️ OFFLINE. Power rebalance next week. sweetGrass fix (1 field). |
| **blueGate** | ENMESHED (Windows) | House 2 | ⏸️ OFFLINE. Rack move incomplete. |
| **southGate** | NUCLEUS + canary | House 2 | ⏸️ OFFLINE. Power rebalance next week. |

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

## Depot Status (Sep 27)

| Target | Binaries | Status |
|--------|----------|--------|
| `x86_64-unknown-linux-musl` | **18/18** | ✅ CURRENT |
| `aarch64-unknown-linux-musl` | **15/15** | ✅ CURRENT (ironGate) |
| `aarch64-apple-darwin` | **16/16** | ✅ CURRENT (graftGate) |
| `x86_64-unknown-linux-gnu` | **14/14** | ✅ CURRENT |
| `x86_64-pc-windows-gnu` | **14/17 FRESH** | 🔄 3 blocked on team unix fixes |

### Windows depot: 3 blocked on team fixes (was 4 — nucleus-deploy FIXED)

| Primal | Owner | Issue | Scope |
|--------|-------|-------|-------|
| **toadStool** | strandGate | 34 files with `tokio::net::UnixListener/UnixStream` | Large |
| **petalTongue** | ironGate | 34+ unix call sites across IPC server, transport, discovery, signal, display backends | Large (has `platform_substrate.rs` — needs expansion) |
| **sweetGrass** | westGate | `AppState.crypto` is `#[cfg(unix)]` but `braid_verify.rs:164` refs unconditionally | Small |
| **sourDough** | graftGate | 11 errors (not audited) | Unknown |

**Fix pattern** (proven in primalSpring `24f71cb7`): `cargo check --target x86_64-pc-windows-gnu` → gate with `#[cfg(unix)]` + `#[cfg(not(unix))]` fallback → push → sporeGate rebuilds `.exe`.

---

## Teams

| Gate | Code Teams | Role |
|------|-----------|------|
| eastGate | biomeOS, squirrel, projectNUCLEUS, primalSpring + overwatch | Orchestration + sovereignty |
| ironGate | bearDog, songBird, skunkBat, swarmVine, bingoCube, petalTongue, esotericWebb, footPrint, tideGlass + springs | Primal workhorse |
| strandGate | toadStool, barraCuda, coralReef, hotSpring, rustChip | Compute trio + HPC + science |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, wetSpring | Provenance trio + data CAS |
| sporeGate | cellMembrane, lithoSpore, plasmidBin ops | Topology + depot + cascade |
| graftGate | sourDough | Darwin builder |

**Meta-Primals:**

| Name | Role | Status |
|------|------|--------|
| **bonsai-bt** | DECIDE layer (behavior trees) | Phase 0 — ingesting |
| **guerillaGorilla** | ACCOUNTABILITY layer (methodology) | ACTIVE — gorilla.primals.eco LIVE |

### guerillaGorilla Capabilities

| Capability | Role |
|------------|------|
| **fEAR** | HOW WE HEAR — evidence intake, OSINT, signal detection |
| **preSCENT** | HOW WE SMELL — pattern recognition, network mapping |
| **STRIDe** | HOW WE MOVE — filing, publication, strategic action |
| **Pursuit Predation** | WHY IT WORKS — endurance vs sprint evasion |
| **Cross-Protection** | HOW WE SURVIVE — multiple surfaces, legal shields |
| **amicusContra** | HOW WE PROJECT — downward (stabilize) / lateral (cross-protect) / upward (force reproducibility) |

---

## Team Assignments — Wave 158+

| # | Track | Team/Gate | Status |
|---|-------|-----------|--------|
| 1 | **northGate enrollment** | northGate + eastGate | 🔄 WG mesh via golgi relay. Interim: Forgejo push. Target: vine-bat zero-SSH. |
| 2 | ~~**cellMembrane UDS→TCP**~~ | ~~sporeGate~~ | ✅ **DONE** (`f99583c`) |
| 3 | ~~**sporeGate rewake**~~ | ~~house 1~~ | ✅ **DONE** — Windows depot rebuilt, cascade autonomous |
| 4 | **detroit content evolution** | publicRecord team (sporeGate parallel IDE) | 🔄 Dynasty expansion, FOIA responses, OSINT loading |
| 5 | **guerillaGorilla formalization** | northGate + overwatch | 🔄 amicusContra, dispersal site, The Machine draft |
| 6 | **Windows depot: 3 team fixes** | strandGate, ironGate, westGate, graftGate | ⏸️ When gates come online. petalTongue reclassified: Large (34+ sites). |
| 7 | **nucleus-deploy Windows fix** | eastGate (projectNUCLEUS) | ✅ **DONE** (`58f6296`) — 2 call sites gated, 0 warnings unix+windows+riscv |
| 8 | **Milk-V Jupiter 2 bring-up** | eastGate (overwatch) | 🔄 PREP DONE — `riscv64gc-{gnu,musl}` targets installed. Awaiting physical boot. |
| 9 | **NUC bench composition** | house 1 | ⏸️ Tower Atomic on DDR3 NUCs |
| 10 | **House 2 power rebalance** | physical (next week) | ⏸️ ironGate, strandGate, westGate, southGate, blueGate |
| 11 | **sporePrint: register gorilla.primals.eco** | sporePrint team | Catalogue entity_registry + sources.toml |
| 12 | **swarmVine + skunkBat: vine-bat hardening** | ironGate (when online) | Zero-SSH enrollment target |

---

## CONVERGENCE RULE

> **Operational + Dispersal + Mesh Expansion + guerillaGorilla.**
> eastGate + golgiBody + sporeGate ONLINE. northGate ENROLLING.
> 4 LIVE SITES. All sitemaps 200. GSC Success. Sitemap P0 RESOLVED.
> guerillaGorilla LAUNCHED — amicusContra named. Three-tier dispersal PROVEN.
> Windows depot 14/17 (3 team fixes pending). nucleus-deploy FIXED. cellMembrane UDS→TCP DONE.
> Dispersal pattern + wildcard subdomain evolution spec'd.
> rustChip standalone (367 tests). Milk-V Jupiter 2 arrived (RISC-V RVA23).
> October: House 2 power rebalance, full mesh rewake, northGate enrollment,
> Jupiter 2 bring-up, Windows team fixes when gates online.
> *"Beside the small. Against unaccountable power. For the record."*

---

**See also**: [`infra/wateringHole/HARDWARE.md`](../HARDWARE.md) — full fleet inventory (16+ gates, 8 ISAs, networking topology, acquisition wishlist).

*Wave 158+ operational. 3 gates + golgiBody ONLINE. 4 live sites, all sitemaps 200. guerillaGorilla launched (gorilla.primals.eco). Three-tier dispersal proven. Windows depot 14/17 (nucleus-deploy FIXED). cellMembrane UDS→TCP done. 3× Pi 500 acquired. HARDWARE.md written. northGate enrolling. RISC-V targets installed. 8 arch families. October: mesh rewake, House 2 power, team fixes, Jupiter 2.*
