# ecoPrimals Ecosystem Blurb — Wave 155g

**Date**: Jul 28, 2026 13:30 EDT | **Wave**: 155g | **From**: eastGate overwatch
**Posture**: **GATE DEPLOYMENT VALIDATED. westGate Tower Atomic LIVE (70 min from dead checkout). strandGate synced (42 repos converged). Startup blurb proven: HTTPS public pull, shallow roots handled, hardware divergences documented. Nest Atomic after Tower stable.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Status**: Gate deployment pipeline PROVEN. westGate went from 3-month-stale
dead checkout to Tower Atomic LIVE in 70 minutes using the startup blurb.
strandGate synced 42 repos with zero conflicts. Both gates filed detailed AARs.

**Key learnings from deployment**:
- HTTPS public pull unblocks fresh gates — no SSH key needed for initial sync
- GitHub→Forgejo "shallow roots" — all old GitHub clones need fresh Forgejo clone
- westGate hardware was wrong in all docs (AMD Ryzen 7 5700X, not i7-4771; 64GB RAM; 2TB NVMe; HDDs raw/no ZFS)
- songBird startup race: `nucleus_launcher.sh` must export `BEARDOG_SOCKET` before starting songBird
- Legacy federation probes on :7700 confirm peptidoglycan layer is active

northGate and ironGate still have RustDesk remote issues — peptidoglycan work
continues.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Why |
|------|-----------------|-----|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. Signal graph validation. |
| **westGate** | petalTongue, squirrel, nestGate (Nest Atomic testbed) | Clean HDD array → tiered storage profiling. Nest + data primals. |
| **strandGate** | toadStool, barraCuda, coralReef (compute trio) | Dual EPYC + RTX 3090 → GPU compute workloads. |

### Storage Tiering Model (westGate)

westGate's actual hardware (corrected from AAR):

```
TIER 0 — AMD Ryzen 7 5700X L3 (32MB)      ← AVAILABLE (Zen 3 unified cache)
TIER 1 — 64GB DDR4 RAM (tmpfs/ramdisk)    ← AVAILABLE
TIER 2 — Samsung 970 EVO Plus 2TB NVMe    ← AVAILABLE (1.1TB free, root FS)
TIER 3 — (absent — no SATA SSD)           ← NOT AVAILABLE
TIER 4 — 5×14TB HDD (OOS14000G)           ← RAW/UNMOUNTED (needs ZFS pool)
```

This lets nestGate's CAS profile real read/write latencies across all tiers.
The Nest Atomic signal graphs (`nest.store`, `nest.retrieve`, `nest.verify`)
can be validated against actual hardware variance — not simulated.

**Sequencing**:
1. **DONE**: westGate Tower Atomic deployed + verified (70 min, Wave 155f)
2. **DONE**: strandGate synced (42 repos, zero conflicts)
3. **NOW**: westGate code team spin-up (petalTongue, squirrel, Provenance Trio)
4. **NOW**: strandGate Tower Atomic → Compute Trio deployment
5. **NOW**: K-derm hardening continues (northGate/ironGate RustDesk, DNS)
6. **NEXT**: westGate ZFS pool creation → Nest Atomic tiered storage validation
7. **NEXT**: strandGate Node Atomic validation (node.compute on RTX 3090)

| Metric | Value |
|--------|-------|
| Signal graphs | **26** (Tower 8, Nest 8, Node 3, Meta 5, Braid 2) |
| Primal test attributes | **~56K** |
| Jelly strings | **6/7 resolved** |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 targets) |
| Gates ONLINE | **8** (westGate Tower LIVE. northGate + ironGate RustDesk degraded) |
| Threat categories | **9** (skunkBat ConnectivityAnomaly) |

---

## WHAT CODE TEAMS SHIPPED (cumulative Wave 155b-e)

| Team | Latest Evolution | Key Commits |
|------|------------------|-------------|
| **songBird** | `tower.health` + `tower.mesh_status` facade. J3+J4+J5 cascade automation. Named pipe IPC | `f2dacd62`, `d4bffbbd` |
| **cellMembrane** | J1+J2 CLOSED. J6 `ServiceSpec` foundation. 1,194 tests | `fc7c4d9`, `8a71345` |
| **skunkBat** | `ConnectivityAnomaly` 9th threat type. 182 new tests | `8d6a0de` |
| **sweetGrass** | G3: `CertificateRef` structured type on braids | `28092a8` |
| **loamSpine** | Entry extraction, schema V2, `certificate.history` RPC | `b03ab3d` |
| **rhizoCrypt** | SSOT sweep, 1,900 tests, method_gate consolidated | `904b17b`, `60f4e2a` |
| **biomeOS** | neuralAPI: 7 signal graphs, 19 translations, platform_native | `a2fb6716`, `ef42a287` |
| **nestGate** | BTSP peer wiring, NTFS CAS safety | `219cca42`, `a6e9e10e` |
| **toadStool** | S343: wgpu system queries + dispatch | `b1d3cfa1b` |
| **coralReef** | IPC merge resolution | `8ebd97d` |
| **primalSpring** | 56+ tower shadow benchmarks | `1b731803` |

---

## GLACIAL GOALS — SEQUENCED

| # | Goal | Status | Gate |
|---|------|--------|------|
| G1 | Tower on Windows | **FRONTLOADED** | OPEN |
| G7 | Gate enmeshment | **FRONTLOADED** | OPEN — workload distribution validates pipeline |
| G6 | bearDog public | READY | OPEN |
| G3 | Nest Atomic Phase 0 | CONVERGING | **AFTER TOWER** — westGate tiered storage testbed |
| G4 | Nest cross-platform | IN PROGRESS | AFTER TOWER |
| G5 | Chimera Phase 0 | PENDING | AFTER G1 |
| G2 | Tower on Android | PENDING | AFTER G1 |
| G8 | Plasmodium | PENDING | AFTER G7 |
| G9 | JOSS publication | PENDING | AFTER G3+G7 |

---

## JELLY STRINGS — 6 OF 8 RESOLVED

| # | What | Status | Owner |
|---|------|--------|-------|
| J1 | Harvest | **CLOSED** — `--push` flag | cellMembrane |
| J2 | Depot push | **CLOSED** — `plasmid.push` + Rust depot_sync | cellMembrane |
| J3 | Service restart | **CLOSED** — `deploy.hot_swap` | songBird |
| J4 | Caddy config | **CLOSED** — route self-config | songBird |
| J5 | WG peer reg | **HARDENED** | songBird |
| J6 | systemd overrides | **FOUNDATION** — `ServiceSpec` renderers | cellMembrane |
| J7 | Legacy detection | OPEN (low priority) | cellMembrane |
| J8 | Key enrollment portal | **OPEN** — SSH keys exchanged via chat, needs portal | songBird + cellMembrane |

---

## CODE TEAMS — PRIMAL STATUS + GATE ASSIGNMENT

### eastGate — Overwatch + Orchestration

| Primal | Version | Role | Next Work |
|--------|---------|------|-----------|
| **biomeOS** | 0.1.0 | Signal graph orchestrator | **Live `tower.health` validation** on gates as teams deploy. |
| **primalSpring** | — | Scenario validation | Calibrate scenarios for distributed gate topology. |
| **bearDog** | 0.9.0 | Trust foundation | G6: public flip audit. G5: `beardog-core` extraction. |
| **songBird** | 0.2.1 | Discovery + IPC | `tower.health` facade shipped. Live validation on northGate. |
| **skunkBat** | 0.2.18 | Defense | `ConnectivityAnomaly` detection. Monitor gate migrations. |
| **cellMembrane** | — | Deployment fabric | J6 completion: `gate.configure` / `gate.apply`. |

### westGate — Nest Atomic + Data (DEPLOYING)

| Primal | Version | Role | Next Work |
|--------|---------|------|-----------|
| **petalTongue** | 1.7.0 | Visualization + WASM | Deploy to westGate. Validate genomeBin deployment cycle. |
| **squirrel** | 0.1.0 | AI + MCP | Deploy to westGate. Validate alongside petalTongue. |
| **nestGate** | 0.5.0 | Content-addressed storage | **Storage tiering validation.** Profile CAS across HDD/SSD/NVMe tiers. |
| **rhizoCrypt** | 0.14.17 | Lineage DAG | Deploy. G3 wiring with loamSpine after Tower stable. |
| **loamSpine** | 0.9.16 | Certificate ledger | Deploy. `MintingAuthority` validation on real Nest. |
| **sweetGrass** | 0.7.64 | Attribution braids | Deploy. `CertificateRef` integration with Provenance Trio. |

westGate Tower Atomic LIVE — Nest Atomic testbed with tiered storage:
- AMD Ryzen 7 5700X, 64GB DDR4, 2TB NVMe, 5×14TB HDD (raw)
- TIER 0-2 ready now. TIER 4 needs ZFS pool (human action). No SATA SSD.

### strandGate — Compute Trio (DEPLOYING)

| Primal | Version | Role | Next Work |
|--------|---------|------|-----------|
| **toadStool** | 0.2.0 | Compute dispatch | Deploy. Validate `node.compute` + `node.dispatch` on real GPU. |
| **barraCuda** | 0.4.0 | Tensor math | Deploy. RTX 3090 compute validation. |
| **coralReef** | 0.2.0 | Shader compilation | Deploy. WGSL → SPIR-V on real hardware. |

strandGate hardware: Dual EPYC + RTX 3090 — purpose-built for the compute trio.

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1 (peptidoglycan anchor: sporeGate)

| Gate | Status | Teams | Next Work |
|------|--------|-------|-----------|
| **sporeGate** | ONLINE. Anchor H1 | Build authority | DNS health all gates. Harvest + push to depot. Foreman. |
| **eastGate** | ONLINE. Overwatch | biomeOS, primalSpring, Tower stack | Coordinate gate deployments. `tower.health` live test. |
| **northGate** | DEGRADED (RustDesk) | — | **Fix RustDesk.** Fix DNS. G1 Tower validation (named pipes). |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | Teams | Next Work |
|------|--------|-------|-----------|
| **blueGate** | ONLINE (Windows) | — | Peptidoglycan anchor H2. RustDesk provisioning for H2 Linux. G1 proof. |
| **ironGate** | DEGRADED (RustDesk) | — | **Fix RustDesk.** Tower validation. HDD enclave later. |
| **strandGate** | SYNCED (42 repos) | **Compute trio** | Tower Atomic → deploy toadStool+barraCuda+coralReef. Node Atomic validation. |
| **westGate** | **TOWER LIVE** | **Nest + data primals** | Code team spin-up. ZFS pool creation → Nest Atomic tiered storage. |
| **swiftGate** | ONLINE (Windows) | — | Tower on Windows → full NUCLEUS. |
| **southGate** | HW READY | — | Enroll → Tower → full NUCLEUS → sovereign site. |

### Remote / Mobile

| Gate | Status | Next Work |
|------|--------|-----------|
| **golgiBody** | ONLINE | Serve depot. LOG before DROP. |
| **flockGate** | ONLINE | Tower validation. Nest validation after Tower stable. |
| **grapheneGate** | ONLINE | G2 (Tower on Android) after G1 proven. |

---

## CROSS-CUTTING DEPENDENCIES — SEQUENCED

```
PHASE 1: TOWER + GATE WORKLOAD DISTRIBUTION (NOW)
 │
 ├── GATE DEPLOYMENTS (pipeline VALIDATED)
 │    ├── westGate: ✅ Tower LIVE → code team spin-up → Nest Atomic
 │    ├── strandGate: ✅ synced → Tower Atomic → compute trio (toadStool, barraCuda, coralReef)
 │    └── AARs filed: startup blurb hardened, hardware profiles corrected
 │
 ├── K-DERM LAYERS
 │    ├── northGate + ironGate: fix RustDesk issues
 │    ├── Peptidoglycan: DNS all gates → port mapping
 │    └── Inner membrane: Tower validation on all online gates
 │
 ├── G7 (gate enmeshment) — tower.enroll on enrolling gates
 │    └── J1+J2 CLOSED → J6 foundation → self-healing cascade
 │
 ├── G6 (bearDog public) — independent, ready
 └── biomeOS + songBird: tower.health → live signal graph validation

PHASE 2: NEST ATOMIC + COMPUTE (AFTER TOWER STABLE)
 │
 ├── westGate: storage tiering validation (HDD/SSD/NVMe/RAM/cache)
 │    ├── nest.store → nest.retrieve → nest.verify across tiers
 │    └── G3 Provenance Trio wiring (rhizoCrypt ↔ loamSpine ↔ sweetGrass)
 │
 ├── strandGate: Node Atomic validation
 │    └── node.compute → node.dispatch on RTX 3090
 │
 ├── G4 (Nest cross-platform)
 └── G5 (Chimera) ← G1 proven

PHASE 3: FULL NUCLEUS
 │
 ├── G8 (Plasmodium) ← G7 complete
 └── G9 (JOSS) ← G3 + G7 complete
```

---

## HANDOFFS

| File | Status |
|------|--------|
| `WESTGATE_OVERWATCH_SYNC_WAVE155f.md` | **NEW** — 41 repos synced, hardware divergences |
| `STRANDGATE_OVERWATCH_SYNC_WAVE155f.md` | **NEW** — 42 repos synced, shallow roots documented |
| `CELLMEMBRANE_WAVE155d_JELLY_STRING_CODIFICATION.md` | J1+J2 closed, J6 foundation |
| `LOAMSPINE_WAVE155D_STRUCTURAL_EXTRACTION_SCHEMA_EVOLUTION_JUL28_2026.md` | Entry extraction, schema V2 |
| `SWEETGRASS_WAVE155b_G3_READINESS_JUL27_2026.md` | CertificateRef shipped |
| `BLURB_SPOREGATE_BUILD_MESH.md` | Build mesh topology |

AARs:
- `WESTGATE_ENROLLMENT_WAVE155f_AAR.md` — **NEW** — hardware profile corrected, 6 divergences
- `WESTGATE_TOWER_ATOMIC_DEPLOYMENT_155f_AAR.md` — **NEW** — Tower LIVE in 70 min, 8 issues (5 resolved)
- `OUTER_MEMBRANE_TOPOLOGY_FAILURE_155b_AAR.md` | `PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md` | `SPOREGATE_DEPLOYMENT_EVOLUTION_155b_AAR.md`

---

*Wave 155g. Deployment pipeline PROVEN. westGate: dead checkout → Tower Atomic
LIVE in 70 minutes (AMD Ryzen 7 5700X / 64GB / 2TB NVMe / 5×14TB raw HDD).
strandGate: 42 repos synced, zero conflicts, compute trio ready. Startup blurb
hardened with HTTPS fallback, shallow roots handling, symlink guards. 8 gates
online (westGate promoted). J8 opened (key enrollment portal). Next: westGate
code team spin-up, strandGate Tower Atomic, ZFS pool creation for Nest Atomic.
northGate + ironGate RustDesk degraded. 6/8 jelly strings resolved.*
