# ecoPrimals Ecosystem Blurb — Wave 155e

**Date**: Jul 28, 2026 11:10 EDT | **Wave**: 155e | **From**: eastGate overwatch
**Posture**: **TOWER HARDENING ACCELERATING — J1+J2 CLOSED, 6/7 jelly strings resolved. songBird tower.health facade shipped. skunkBat k-derm detection live. sweetGrass CertificateRef shipped (G3 closer). Nest Atomic after Tower stable.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Priority**: Frontload **Tower Atomic hardening** on existing infrastructure.
The peptidoglycan failure proved that our connectivity fabric is fragile — we
need Tower stable on all online gates before layering Nest Atomic on top. Nest
Atomic work (G3 Provenance Trio wiring) occurs **after Tower is proven stable**.

**Sequencing**:
1. **NOW**: Harden k-derm layers (peptidoglycan DNS, outer membrane provisioning)
2. **NOW**: Tower Atomic live validation (tower.health on northGate, tower.enroll on enrolling gates)
3. **NOW**: Jelly string codification (J1 harvest, J2 push — unblock self-healing cascade)
4. **AFTER TOWER STABLE**: Nest Atomic Phase 1 wiring (G3 Provenance Trio IPC callers)
5. **AFTER TOWER STABLE**: Node Atomic live validation

**Incident recap**: Two NAT rate-limit collapses on golgiBody took down house1
RustDesk. sporeGate diagnosed, golgiBody fixed. Three-layer k-derm model
(outer membrane / peptidoglycan / inner membrane) now documented. Full AAR in
`aars/OUTER_MEMBRANE_TOPOLOGY_FAILURE_155b_AAR.md`.

| Metric | Value |
|--------|-------|
| Signal graphs | **26** (Tower 8, Nest 8, Node 3, Meta 5, Braid 2) |
| Primal test attributes | **~56K** (toadStool 22K, songBird 14K, nestGate 13K) |
| Jelly strings | **6/7 resolved** (J1-J5 CLOSED, J6 foundation, J7 low-pri) |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 targets) |
| Gates ONLINE | **7** + RustDesk restored |
| Threat categories | **9** (skunkBat `ConnectivityAnomaly` new) |
| cellMembrane tests | **1,194** |

---

## INCIDENT: PEPTIDOGLYCAN LAYER FAILURE

### What Happened
Two cascading rate-limit collapses on golgiBody:
1. **UDP** (Incident 1): 3 house1 gates behind 1 NAT IP hit 30/10s UDP limit → silent DROP → all RustDesk offline
2. **TCP** (Incident 2): Dead port 21114 (API, no listener) caused retry storms that poisoned the TCP rate counter → all TCP blocked

### What Fixed It
- **RUSTDESK_MEMBRANE** iptables chain: isolated from primal rules, NAT-aware limits (120 UDP/10s, 60 TCP/10s)
- **Port 21114 REJECT** with tcp-reset: stops retry storms immediately
- **dnsmasq** re-enabled on sporeGate: sovereign DNS chain restored
- **Duplicate hbbs/hbbr** processes killed on golgiBody

### Three-Layer Model Established

```
OUTER MEMBRANE — RustDesk/human access (relay.primals.eco)
PEPTIDOGLYCAN  — LAN/HPC topology fabric (NAT, DNS, switches, cabling)
INNER MEMBRANE — Primal IPC (WireGuard wg0 + songBird :7700 + BTSP)
```

---

## WHAT CODE TEAMS SHIPPED (cumulative Wave 155b-e)

| Team | Latest Evolution | Key Commits |
|------|------------------|-------------|
| **songBird** | **`tower.health` + `tower.mesh_status` facade** for biomeOS signal graphs. J3+J4+J5 cascade automation. Named pipe IPC | `f2dacd62`, `d4bffbbd` |
| **cellMembrane** | **J1+J2 CLOSED**: `plasmid.harvest --push`, `plasmid.push` first-class command, Rust depot_sync refactor. **J6 foundation**: `ServiceSpec` cross-platform model (systemd+launchd renderers). 6 deep debt fixes. 1,194 tests | `fc7c4d9`, `8a71345` |
| **skunkBat** | **`ConnectivityAnomaly`** — 9th threat category for k-derm incident detection. `platform.rs` module. 182 new tests | `8d6a0de` |
| **sweetGrass** | **G3: `CertificateRef`** structured type on braids. Backward-compat wire format. Version → 0.7.64 | `28092a8` |
| **loamSpine** | Entry module extraction (`entry/types.rs`). Schema evolution `V2`. `certificate.history` RPC. 935 insertions | `b03ab3d` |
| **rhizoCrypt** | SSOT sweep — 1,900 tests aligned. `method_gate_tests` consolidated. Cargo update | `904b17b`, `60f4e2a` |
| **biomeOS** | neuralAPI: 7 signal graphs, 19 atomic translations, platform_native transport | `a2fb6716`, `ef42a287` |
| **nestGate** | G3: BTSP peer wiring. G4: NTFS CAS safety. Dep + stub cleanup | `219cca42`, `a6e9e10e` |
| **toadStool** | S343: wgpu into system queries + dispatch | `b1d3cfa1b` |
| **coralReef** | IPC merge resolution | `8ebd97d` |
| **primalSpring** | 56+ tower shadow benchmarks | `1b731803` |
| **sporeGate** | Peptidoglycan incident response. RUSTDESK_MEMBRANE. 39 binaries | deployment |

---

## GLACIAL GOALS — SEQUENCED

**Gate**: Tower Atomic hardening gates open. Nest Atomic gates open after Tower stable.

| # | Goal | Status | Gate | What Landed |
|---|------|--------|------|-------------|
| G1 | Tower on Windows | **FRONTLOADED** | OPEN | songBird named pipes + J3/J4/J5. cellMembrane InitSystem. toadStool wgpu. biomeOS platform_native. |
| G7 | Gate enmeshment | **FRONTLOADED** | OPEN | Depot live. Enrollment live. Peptidoglycan hardened. 10 RustDesk peers. |
| G6 | bearDog public | READY | OPEN | Final audit. Independent of other goals. |
| G3 | Nest Atomic Phase 0 | CONVERGING | **AFTER TOWER** | Foundation shipped (rhizoCrypt, loamSpine, sweetGrass). IPC wiring waits. |
| G4 | Nest cross-platform | IN PROGRESS | **AFTER TOWER** | nestGate NTFS safety shipped. Full validation after Tower on Windows proven. |
| G5 | Chimera Phase 0 | PENDING | AFTER G1 | Blocked on G1 proof. |
| G2 | Tower on Android | PENDING | AFTER G1 | — |
| G8 | Plasmodium | PENDING | AFTER G7 | — |
| G9 | JOSS publication | PENDING | AFTER G3+G7 | — |

---

## G3 CONVERGENCE — PROVENANCE TRIO STATUS

From `PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md`:

### What's Working
- Individual APIs mature, tested, non-overlapping concerns
- BTSP universal (13/13) — auth layer solved
- IPC contract alignment — `Serialize`/`Deserialize` on wire types
- Discovery helpers tested and G3-labeled in loamSpine

### Convergence Gaps

| # | Gap | Owner | Requires |
|---|-----|-------|----------|
| 1 | Cross-primal certificate provenance | rhizoCrypt | loamSpine `certificate.verify` (shipped) |
| 2 | Attribution braid ↔ certificate linkage | sweetGrass + loamSpine | `CertificateId` on braids |
| 3 | MintingAuthority delegation validation | loamSpine | rhizoCrypt trust anchor, sweetGrass attestation |
| 4 | Cross-gate provenance chain | All three + cellMembrane | End-to-end integration |

### Phase Path
```
Phase 0 (NOW): each primal evolves independently
Phase 1 (Wire): IPC callers between primals
Phase 2 (Cross-gate): verification over mesh relay
Phase 3 (rootPulse): biomeOS orchestrates as unified data layer
```

---

## JELLY STRINGS — 6 OF 7 RESOLVED

| # | What | Status | Owner |
|---|------|--------|-------|
| J1 | Harvest is shell loops | **CLOSED** — was already Rust, added `--push` | cellMembrane |
| J2 | Depot push is rsync | **CLOSED** — `plasmid.push` + Rust depot_sync refactor | cellMembrane |
| J3 | Service restart is manual | **CLOSED** — `deploy.hot_swap` | songBird |
| J4 | Caddy config is manual | **CLOSED** — route self-config via `route.rs` | songBird |
| J5 | WG peer reg is ssh+wg set | **HARDENED** — WG peer management | songBird |
| J6 | systemd overrides manual | **FOUNDATION** — `ServiceSpec` model + renderers shipped | cellMembrane |
| J7 | Legacy service detection | OPEN (low priority) | cellMembrane |

**6/7 resolved.** `plasmid.harvest --all --local --push` is now a single command
for the full harvest→push cycle. J6 has the `ServiceSpec` cross-platform model
(systemd + launchd renderers). J7 is low priority / one-time.

---

## PEPTIDOGLYCAN — HARDENING PRIORITIES

From the incident AAR, sequenced:

| Priority | Item | Owner | Status |
|----------|------|-------|--------|
| P0 | DNS: verify dnsmasq on all Linux gates | sporeGate | sporeGate DONE, others PENDING |
| P1 | Provision RustDesk on house2 Linux gates | blueGate | network proven, clients needed |
| P1 | Complete port→gate mapping in TOPOLOGY_MAP | overwatch | partial |
| P2 | LOG before DROP in RUSTDESK_MEMBRANE | golgiBody | OPEN |
| P2 | northGate DNS diagnosis | northGate | OPEN |
| P3 | Standardized gate provisioning script | wateringHole | future |

---

## CODE TEAMS — PRIMAL STATUS + NEXT WORK

### Tower Atomic (FRONTLOADED — hardening now)

| Primal | Version | Next Work |
|--------|---------|-----------|
| **bearDog** | 0.9.0 | **G6: public flip audit.** G5: `beardog-core` extraction for Chimera. |
| **songBird** | 0.2.1 | **`tower.health` + `tower.mesh_status` facades SHIPPED.** Live validation on northGate (named pipes) + house1 gates (`deploy.hot_swap`). |
| **skunkBat** | 0.2.18 | **`ConnectivityAnomaly` SHIPPED** — 9th threat category. K-derm incident pattern detection live. 182 new tests. |

### Compute Triangle (Tower infra support)

| Primal | Version | Next Work |
|--------|---------|-----------|
| **toadStool** | 0.2.0 | S343 shipped. Windows WMI enrichment for `node.discover_hardware`. |
| **barraCuda** | 0.4.0 | Stable. |
| **coralReef** | 0.2.0 | Stable. IPC aligned. |

### Provenance Trio + Nest Atomic (AFTER TOWER STABLE)

| Primal | Version | Status | Next Work (deferred) |
|--------|---------|--------|----------------------|
| **nestGate** | 0.5.0 | G3+G4 foundation shipped | Wire `connect_with_btsp` into CAS call sites. NTFS safety live test. |
| **rhizoCrypt** | 0.14.17 | SSOT aligned, 1,900 tests | Wire `loamSpine.certificate.verify` from DAG auth. |
| **loamSpine** | 0.9.16 | Entry extracted, `certificate.history` RPC | `MintingAuthority` validation. Wire discovery callers. |
| **sweetGrass** | 0.7.64 | **`CertificateRef` SHIPPED** | G3 closer — structured certificate references on braids. Ready for Provenance Trio wiring. |

### Data + Orchestration

| Primal | Version | Next Work |
|--------|---------|-----------|
| **biomeOS** | 0.1.0 | **Live signal graph validation**: songBird now responds to `tower.health` — test on live gate. |
| **squirrel** | 0.1.0 | Stable. |
| **petalTongue** | 1.7.0 | Stable. |

### cellMembrane (FRONTLOADED — jelly strings)

| Component | Status | Next Work |
|-----------|--------|-----------|
| **membrane-shadow** | **J1+J2 CLOSED. J6 foundation shipped.** 1,194 tests | J6 completion: `gate.configure` / `gate.apply` declarative drop-in generation. |

---

## GATE TEAMS — STATUS + NEXT WORK

**Focus**: K-derm hardening + Tower Atomic validation on existing gates first.

### House 1 (peptidoglycan anchor: sporeGate)

| Gate | Status | Next Work |
|------|--------|-----------|
| **sporeGate** | ONLINE. Peptidoglycan anchor H1 | **DNS health all H1 gates.** J1 harvest codification. Tower Atomic validation. |
| **eastGate** | ONLINE. Overwatch | Coordination. biomeOS `tower.health` live test. bearDog public audit. |
| **northGate** | ONLINE. Windows, WG mesh | **Fix DNS (dnsmasq).** G1 Tower validation: `tower.health` via named pipes. |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | Next Work |
|------|--------|-----------|
| **blueGate** | ONLINE (Windows). 10G backbone | **Peptidoglycan anchor H2.** Provision RustDesk on H2 Linux gates. G1 Tower on Windows proof. |
| **ironGate** | ONLINE. 4x HDD | Tower Atomic validation. HDD enclave after Tower stable. |
| **strandGate** | HW READY | Provision RustDesk (via blueGate) → enroll → Tower → compute. |
| **westGate** | HW READY (5x14TB) | Provision RustDesk → enroll → Tower. Nest Atomic + ZFS CAS **after Tower stable**. |
| **swiftGate** | ONLINE (Windows) | Tower on Windows → full NUCLEUS after proven. |
| **southGate** | HW READY | Provision RustDesk → enroll → Tower → full NUCLEUS. |

### Remote / Mobile

| Gate | Status | Next Work |
|------|--------|-----------|
| **golgiBody** | ONLINE. RUSTDESK_MEMBRANE hardened | Serve depot. LOG before DROP. |
| **flockGate** | ONLINE | Tower validation. Nest Atomic validation **after Tower stable**. |
| **grapheneGate** | ONLINE | Tower stable first. G2 (Tower on Android) after G1 proven. |

---

## CROSS-CUTTING DEPENDENCIES — SEQUENCED

```
PHASE 1: TOWER ATOMIC HARDENING (NOW)
 │
 ├── K-DERM LAYERS
 │    ├── Peptidoglycan: DNS all gates → port mapping → provisioning script
 │    ├── Outer membrane: RustDesk house2 Linux gates → LOG before DROP
 │    └── Inner membrane: Tower validation on all online gates
 │
 ├── G7 (gate enmeshment) — tower.enroll on enrolling gates
 │    ├── G1 (Tower on Windows) — J3/J4/J5 SHIPPED
 │    │    ├── northGate: fix DNS → tower.health via named pipes
 │    │    └── blueGate: G1 proof → distributed builder
 │    └── J1+J2 CLOSED → J6 foundation → self-healing cascade
 │
 ├── G6 (bearDog public) — independent, ready
 │
 ├── skunkBat: ConnectivityAnomaly k-derm detection LIVE
 │
 └── biomeOS + songBird: tower.health facade → live signal graph test

PHASE 2: NEST ATOMIC (AFTER TOWER STABLE)
 │
 ├── G3 (Nest Atomic Phase 0) — Provenance Trio IPC wiring
 │    ├── rhizoCrypt: wire certificate.verify from DAG
 │    ├── sweetGrass: CertificateRef SHIPPED → wire into cross-gate braids
 │    ├── loamSpine: certificate.history RPC + MintingAuthority validation
 │    └── flockGate + westGate validation
 │
 ├── G4 (Nest cross-platform) — NTFS CAS validation
 └── G5 (Chimera) ← G1 proven

PHASE 3: FULL NUCLEUS
 │
 ├── G8 (Plasmodium) ← G7 complete
 └── G9 (JOSS) ← G3 + G7 complete
```

---

---

## HANDOFFS

| File | Status |
|------|--------|
| `CELLMEMBRANE_WAVE155d_JELLY_STRING_CODIFICATION.md` | **NEW** — J1+J2 closed, J6 foundation |
| `LOAMSPINE_WAVE155D_STRUCTURAL_EXTRACTION_SCHEMA_EVOLUTION_JUL28_2026.md` | **NEW** — entry extraction, schema V2 |
| `SWEETGRASS_WAVE155b_G3_READINESS_JUL27_2026.md` | UPDATED — CertificateRef shipped |
| `BLURB_SPOREGATE_BUILD_MESH.md` | CURRENT |

AARs: `OUTER_MEMBRANE_TOPOLOGY_FAILURE_155b_AAR.md` | `PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md` | `SPOREGATE_DEPLOYMENT_EVOLUTION_155b_AAR.md`

---

*Wave 155e. Tower hardening accelerating. 6/7 jelly strings resolved — J1+J2
CLOSED by cellMembrane (`plasmid.harvest --push` single command), J6 ServiceSpec
foundation shipped. songBird `tower.health` facade ready for biomeOS signal graph
live validation. skunkBat `ConnectivityAnomaly` 9th threat type for k-derm
detection. sweetGrass `CertificateRef` shipped (G3 closer ready for Phase 2).
loamSpine `certificate.history` RPC + entry extraction. rhizoCrypt SSOT aligned.
Next: Tower live validation on gates, DNS hardening, house2 RustDesk provisioning.*
