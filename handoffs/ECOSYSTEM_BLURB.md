# ecoPrimals Ecosystem Blurb — Wave 155f

**Date**: Jul 28, 2026 11:55 EDT | **Wave**: 155f | **From**: eastGate overwatch
**Posture**: **GATE WORKLOAD DISTRIBUTION — teams moving to dedicated gates. Tower hardening validated through live deployment. Storage tiering model on westGate. Nest Atomic after Tower stable.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Priority shift**: We're distributing code teams across gates. This serves two
purposes: (1) put workloads on the hardware that matches them, and (2) validate
the deployment pipeline (enrollment, Tower Atomic, genomeBins, cascade) by
actually moving work and observing divergences and failure patterns.

northGate and ironGate still have RustDesk remote issues — peptidoglycan work
continues. westGate is back online with a clean HDD array and becomes the
Nest Atomic testbed with tiered storage profiling.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Why |
|------|-----------------|-----|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. Signal graph validation. |
| **westGate** | petalTongue, squirrel, nestGate (Nest Atomic testbed) | Clean HDD array → tiered storage profiling. Nest + data primals. |
| **strandGate** | toadStool, barraCuda, coralReef (compute trio) | Dual EPYC + RTX 3090 → GPU compute workloads. |

### Storage Tiering Model (westGate)

westGate's 5x14TB HDD array plus additional drives (2.5" SSD can be added)
creates a real-world tiered storage testbed for Nest Atomic:

```
TIER 0 — AMD L3/L1 cache (if AMD CPU)     ← compute-adjacent, nanosecond
TIER 1 — RAM (tmpfs / ramdisk)             ← volatile, microsecond
TIER 2 — NVMe                              ← fast persistent, sub-millisecond
TIER 3 — 2.5" SSD (SATA)                   ← mid persistent, millisecond
TIER 4 — HDD (5x14TB array)               ← cold/bulk, multi-millisecond
```

This lets nestGate's CAS profile real read/write latencies across all tiers.
The Nest Atomic signal graphs (`nest.store`, `nest.retrieve`, `nest.verify`)
can be validated against actual hardware variance — not simulated.

**Sequencing**:
1. **NOW**: Distribute teams to gates (deployment validation)
2. **NOW**: Tower Atomic on each gate (tower.health, tower.enroll)
3. **NOW**: K-derm hardening continues (northGate/ironGate RustDesk, DNS)
4. **THEN**: westGate storage tiering + Nest Atomic validation
5. **THEN**: strandGate compute trio validation (node.compute, node.dispatch)

| Metric | Value |
|--------|-------|
| Signal graphs | **26** (Tower 8, Nest 8, Node 3, Meta 5, Braid 2) |
| Primal test attributes | **~56K** |
| Jelly strings | **6/7 resolved** |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 targets) |
| Gates ONLINE | **7** (northGate + ironGate RustDesk degraded) |
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

## JELLY STRINGS — 6 OF 7 RESOLVED

| # | What | Status | Owner |
|---|------|--------|-------|
| J1 | Harvest | **CLOSED** — `--push` flag | cellMembrane |
| J2 | Depot push | **CLOSED** — `plasmid.push` + Rust depot_sync | cellMembrane |
| J3 | Service restart | **CLOSED** — `deploy.hot_swap` | songBird |
| J4 | Caddy config | **CLOSED** — route self-config | songBird |
| J5 | WG peer reg | **HARDENED** | songBird |
| J6 | systemd overrides | **FOUNDATION** — `ServiceSpec` renderers | cellMembrane |
| J7 | Legacy detection | OPEN (low priority) | cellMembrane |

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

westGate becomes the Nest Atomic testbed with tiered storage:
- 5x14TB HDD array (TIER 4 — cold/bulk CAS)
- 2.5" SSD available (TIER 3 — mid persistent)
- NVMe if present (TIER 2 — fast persistent)
- RAM cache (TIER 1 — volatile fast path)
- AMD cache hierarchy if AMD CPU (TIER 0 — compute-adjacent)

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
| **strandGate** | HW READY | **Compute trio** | Enroll → Tower → deploy toadStool+barraCuda+coralReef. Node Atomic validation. |
| **westGate** | HW READY (5x14TB) | **Nest + data primals** | Enroll → Tower → deploy petal+squirrel+Provenance Trio. Storage tiering. |
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
 ├── GATE DEPLOYMENTS (validates pipeline)
 │    ├── westGate: enroll → Tower → deploy petalTongue + squirrel + Provenance Trio
 │    ├── strandGate: enroll → Tower → deploy compute trio (toadStool, barraCuda, coralReef)
 │    └── Observe divergences + failure patterns → harden deployment pipeline
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
| `CELLMEMBRANE_WAVE155d_JELLY_STRING_CODIFICATION.md` | J1+J2 closed, J6 foundation |
| `LOAMSPINE_WAVE155D_STRUCTURAL_EXTRACTION_SCHEMA_EVOLUTION_JUL28_2026.md` | Entry extraction, schema V2 |
| `SWEETGRASS_WAVE155b_G3_READINESS_JUL27_2026.md` | CertificateRef shipped |
| `BLURB_SPOREGATE_BUILD_MESH.md` | Build mesh topology |

AARs: `OUTER_MEMBRANE_TOPOLOGY_FAILURE_155b_AAR.md` | `PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md` | `SPOREGATE_DEPLOYMENT_EVOLUTION_155b_AAR.md`

---

*Wave 155f. Teams distributing to dedicated gates: eastGate (overwatch +
orchestration), westGate (Nest + data primals with tiered storage testbed),
strandGate (compute trio on dual EPYC + RTX 3090). The migrations themselves
validate the deployment pipeline — enrollment, Tower Atomic bootstrap, genomeBin
fetch, cascade. Storage tiering model defined (cache → RAM → NVMe → SSD → HDD)
for real Nest Atomic profiling. northGate + ironGate RustDesk still degraded —
peptidoglycan work continues. 6/7 jelly strings resolved. Tower hardening
through live gate deployment is the current posture.*
