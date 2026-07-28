# ecoPrimals Ecosystem Blurb — Wave 155d

**Date**: Jul 28, 2026 10:10 EDT | **Wave**: 155d | **From**: eastGate overwatch
**Posture**: **TOWER ATOMIC HARDENING — frontloading infra stability + k-derm layers. Nest Atomic after Tower is stable on existing gates.**

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
| Primal test attributes | **~54K** (songBird 14K, toadStool 22K, nestGate 13K) |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 targets) |
| Gates ONLINE | **7** + RustDesk restored |
| RustDesk peers | **10** registered in hbbs DB |
| Forgejo | **ONLINE** (was down ~12h yesterday) |

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

## WHAT CODE TEAMS SHIPPED (cumulative Wave 155b-d)

| Team | Evolution | Commits |
|------|-----------|---------|
| **biomeOS** | neuralAPI: 7 new signal graphs, 19 atomic translations, platform_native transport | `a2fb6716`, `ef42a287` |
| **songBird** | **J3+J4+J5**: cascade automation — `deploy.hot_swap`, route self-config via `route.rs`, WG peer hardening. Named pipe IPC. GateEnroll dispatch | `d4bffbbd`, `7e3517c8`, `c4c5d2d2` |
| **rhizoCrypt** | **G3**: cross-gate provenance chain — `federate→sweetGrass` push + gateway witnesses. BTSP→DAG bridge | `ed81f19`, `d4972b0` |
| **nestGate** | G3: BTSP peer wiring. G4: NTFS CAS safety. Dep evolution + stub cleanup + fabricated fallback cleanup | `219cca42`, `a6e9e10e`, `d0921a2b`, `9138068f` |
| **loamSpine** | G3: semantic certificate checks + RPC surface + delegated minting builder. Deep debt — legacy manager, clone dedup, BTSP move semantics | `1eb6d09`, `29307d1`, `d1b1594` |
| **toadStool** | S343: wgpu into system queries + dispatch. S342: GPU fallback + doctor fix | `b1d3cfa1b`, `64f661674` |
| **sweetGrass** | G3 READY — cross-gate attribution types, BTSP ClientHello, PROV-O wiring all shipped. Waiting upstream trio | `fa253aa` |
| **skunkBat** | Cargo update (34 deps). Frame crypto extraction | `349ec9f`, `578136c` |
| **coralReef** | IPC merge resolution. Test extraction | `8ebd97d`, `40ea5b1` |
| **cellMembrane** | `InitSystem` dispatch (systemd/launchd/windows-service/bare) | `cbadae4` |
| **primalSpring** | 56 tower shadow benchmarks. Gate count calibrated | `1b731803`, `05e72e46` |
| **sporeGate** | Peptidoglycan incident response. RUSTDESK_MEMBRANE chain. 39 binaries. 7 jelly strings | deployment |

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

## JELLY STRINGS — UPDATED

| # | What | Status | Owner |
|---|------|--------|-------|
| J1 | Harvest is shell loops | OPEN | cellMembrane |
| J2 | Depot push is rsync | OPEN | cellMembrane |
| J3 | Service restart is manual | **SHIPPED** — `deploy.hot_swap` | songBird |
| J4 | Caddy config is manual | **SHIPPED** — route self-config via `route.rs` | songBird |
| J5 | WG peer reg is ssh+wg set | **HARDENED** — WG peer management evolution | songBird |
| J6 | systemd overrides manual | OPEN | cellMembrane |
| J7 | Legacy service detection | OPEN (low priority) | cellMembrane |

**songBird closed 3 of 7 jelly strings in one commit.** J1+J2 remain as the P0 path for cellMembrane.

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
| **songBird** | 0.2.1 | **J3/J4/J5 SHIPPED.** Live validation: named-pipe test on northGate, route self-config, `deploy.hot_swap` on house1 gates. |
| **skunkBat** | 0.2.18 | Deps updated. Stable. Tower audit trail for k-derm incident detection (see AAR skunkBat targets). |

### Compute Triangle (Tower infra support)

| Primal | Version | Next Work |
|--------|---------|-----------|
| **toadStool** | 0.2.0 | S343 shipped. Windows WMI enrichment for `node.discover_hardware`. |
| **barraCuda** | 0.4.0 | Stable. |
| **coralReef** | 0.2.0 | Stable. IPC aligned. |

### Provenance Trio + Nest Atomic (AFTER TOWER STABLE)

| Primal | Version | Next Work (deferred) |
|--------|---------|----------------------|
| **nestGate** | 0.5.0 | G3: Wire `connect_with_btsp` into CAS call sites. G4: NTFS safety live test. |
| **rhizoCrypt** | 0.14.17 | G3: Wire `loamSpine.certificate.verify` from DAG auth. Cross-gate provenance validation. |
| **loamSpine** | 0.9.16 | G3: `MintingAuthority` validation in `mint_certificate`. Wire discovery callers. |
| **sweetGrass** | 0.7.63 | G3: Add `CertificateId` to braid attestation. All upstream APIs ready — sweetGrass is the closer. |

### Data + Orchestration

| Primal | Version | Next Work |
|--------|---------|-----------|
| **biomeOS** | 0.1.0 | **Live signal graph validation**: `tower.health` + `tower.mesh_status` on online gates. |
| **squirrel** | 0.1.0 | Stable. |
| **petalTongue** | 1.7.0 | Stable. |

### cellMembrane (FRONTLOADED — jelly strings)

| Component | Next Work |
|-----------|-----------|
| **membrane-shadow** | **J1**: `plasmid.harvest` Rust command (P0). **J2**: `plasmid.push` (P1). J6: cross-platform service config. |

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
 │    └── J1 (harvest) → J2 (push) → self-healing cascade
 │
 ├── G6 (bearDog public) — independent, ready
 │
 └── biomeOS: live signal graph validation (tower.health, tower.mesh_status)

PHASE 2: NEST ATOMIC (AFTER TOWER STABLE)
 │
 ├── G3 (Nest Atomic Phase 0) — Provenance Trio IPC wiring
 │    ├── rhizoCrypt: wire certificate.verify from DAG
 │    ├── sweetGrass: CertificateId on braids
 │    ├── loamSpine: MintingAuthority validation
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

*Wave 155d. Priority reoriented: Tower Atomic hardening first, Nest Atomic after
stable. K-derm three-layer model documented (outer membrane / peptidoglycan /
inner membrane). Peptidoglycan failure diagnosed and fixed. songBird closed
J3+J4+J5 (cascade automation). G3 foundation is shipped but wiring deferred
until Tower is proven on existing gates. Next immediate: DNS hardening across
all gates, Tower Atomic live validation (tower.health, tower.enroll), house2
RustDesk provisioning, and J1+J2 harvest/push codification.*
