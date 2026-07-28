# ecoPrimals Ecosystem Blurb — Wave 155d

**Date**: Jul 28, 2026 09:50 EDT | **Wave**: 155d | **From**: eastGate overwatch
**Posture**: **RECOVERY + ACCELERATION — peptidoglycan failure diagnosed + fixed, 6 primals shipped evolution, Nest Atomic G3 convergence underway.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Incident**: Two cascading NAT rate-limit collapses on golgiBody took down
all house1 RustDesk access. Root cause: per-IP UDP+TCP rate limits assumed
one-client-per-IP but 3 NATted gates shared one WAN IP. sporeGate diagnosed,
golgiBody fixed. Full AAR in `aars/OUTER_MEMBRANE_TOPOLOGY_FAILURE_155b_AAR.md`.

**Architecture evolution**: The incident revealed a **peptidoglycan layer** —
the physical/network topology fabric between outer membrane (RustDesk/human
access) and inner membrane (primals/WireGuard mesh). Three-layer model now
documented. RUSTDESK_MEMBRANE iptables chain created. dnsmasq sovereign DNS
restored on sporeGate.

**Code teams shipped hard during recovery**. songBird tackled J3+J4+J5 (cascade
automation). rhizoCrypt shipped cross-gate provenance. loamSpine deepened G3
verification. toadStool extended GPU pipeline. Provenance Trio G3 convergence
AAR documents the gap closure path.

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

## GLACIAL GOALS — UPDATED STATUS

| # | Goal | Status | What Landed |
|---|------|--------|-------------|
| G1 | Tower on Windows | **IN PROGRESS** | songBird named pipes + J3/J4/J5 cascade automation. cellMembrane InitSystem. toadStool wgpu. biomeOS platform_native. |
| G2 | Tower on Android | PENDING | — |
| G3 | Nest Atomic Phase 0 | **CONVERGING** | rhizoCrypt cross-gate provenance chain. loamSpine verification path + delegated minting. sweetGrass READY. Convergence AAR documents 4 gaps + 8 action items. |
| G4 | Nest cross-platform | **IN PROGRESS** | nestGate NTFS CAS safety. biomeOS socket templates. |
| G5 | Chimera Phase 0 | PENDING (blocked on G1 proof) | — |
| G6 | bearDog public | READY (final audit) | — |
| G7 | Gate enmeshment | **IN PROGRESS** | Depot live. Enrollment endpoint live. Peptidoglycan hardened. 10 RustDesk peers. |
| G8 | Plasmodium | PENDING (blocked on G7) | — |
| G9 | JOSS publication | PENDING | — |

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

### Tower Atomic

| Primal | Version | Next Work |
|--------|---------|-----------|
| **bearDog** | 0.9.0 | G5: `beardog-core` extraction. G6: public flip audit. |
| **songBird** | 0.2.1 | **J3/J4/J5 SHIPPED.** G1: live named-pipe test. Route self-config live validation. |
| **skunkBat** | 0.2.18 | Deps updated. Stable. |

### Provenance Trio + Nest Atomic

| Primal | Version | Next Work |
|--------|---------|-----------|
| **nestGate** | 0.5.0 | **G3: Wire `connect_with_btsp` into CAS call sites.** G4: NTFS safety live test. |
| **rhizoCrypt** | 0.14.17 | **G3: Wire `loamSpine.certificate.verify` from DAG auth.** Cross-gate provenance chain validation. |
| **loamSpine** | 0.9.16 | **G3: `MintingAuthority` validation in `mint_certificate`.** Wire discovery callers. |
| **sweetGrass** | 0.7.63 | **G3: Add `CertificateId` to braid attestation.** All upstream APIs ready — sweetGrass is the closer. |

### Compute Triangle

| Primal | Version | Next Work |
|--------|---------|-----------|
| **toadStool** | 0.2.0 | S343 shipped — wgpu in system queries + dispatch. Windows WMI enrichment next. |
| **barraCuda** | 0.4.0 | Stable. |
| **coralReef** | 0.2.0 | Stable. IPC aligned. |

### Data + Orchestration

| Primal | Version | Next Work |
|--------|---------|-----------|
| **biomeOS** | 0.1.0 | Signal graph executor validation on live gate. G8: Plasmodium (after G7). |
| **squirrel** | 0.1.0 | Stable. |
| **petalTongue** | 1.7.0 | **Recovery target** — petal layer failure mentioned. Check status. |

### cellMembrane

| Component | Next Work |
|-----------|-----------|
| **membrane-shadow** | **J1**: `plasmid.harvest` Rust command (P0). **J2**: `plasmid.push`. J6: service config from profile. |

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1

| Gate | Status | Next Work |
|------|--------|-----------|
| **sporeGate** | ONLINE. Incident responder. dnsmasq restored | Peptidoglycan anchor. DNS health on all gates. J1 harvest codification. |
| **eastGate** | ONLINE. Overwatch | Coordination. ECOSYSTEM_BLURB cascade. G3 convergence tracking. |
| **northGate** | ONLINE. Windows, WG mesh | DNS diagnosis (likely dead dnsmasq). G1 live validation. |

### House 2

| Gate | Status | Next Work |
|------|--------|-----------|
| **ironGate** | ONLINE. 4x HDD | HDD enclave. `node.discover_hardware` validation. |
| **strandGate** | HW READY | RustDesk provisioning (via blueGate). Enroll → Tower → compute. |
| **westGate** | HW READY (5x14TB) | RustDesk provisioning. Enroll → **Nest Atomic** → ZFS CAS. G3 validation. |
| **blueGate** | ONLINE (Windows). 10G backbone proven | **Peptidoglycan anchor house2.** RustDesk provisioning for house2 Linux gates. G1 proof. |
| **swiftGate** | ONLINE (Windows) | Enroll → NUCLEUS on Windows. |
| **southGate** | HW READY | RustDesk provisioning. Enroll → NUCLEUS → sovereign site. |

### Remote / Mobile

| Gate | Status | Next Work |
|------|--------|-----------|
| **golgiBody** | ONLINE. RUSTDESK_MEMBRANE hardened | Serve depot. LOG before DROP. |
| **flockGate** | ONLINE | G3: Nest Atomic Phase 0 validation. |
| **grapheneGate** | ONLINE | G2 (after G1 proven). |

---

## CROSS-CUTTING DEPENDENCIES

```
PEPTIDOGLYCAN HARDENED (RUSTDESK_MEMBRANE, DNS, 3-layer model)
 │
 ├── biomeOS neuralAPI (DELIVERED — 26 signals, 19 translations)
 │    │
 │    ├── G7 (gate enmeshment) — tower.enroll live, 10 RustDesk peers
 │    │    ├── G1 (Tower on Windows) — J3/J4/J5 SHIPPED by songBird
 │    │    │    ├── blueGate G1 proof (named pipes live)
 │    │    │    └── northGate DNS fix → live validation
 │    │    ├── G3 (Nest Atomic Phase 0) — CONVERGING
 │    │    │    ├── rhizoCrypt: wire certificate.verify from DAG
 │    │    │    ├── sweetGrass: CertificateId on braids
 │    │    │    ├── loamSpine: MintingAuthority validation
 │    │    │    └── flockGate + westGate validation
 │    │    └── J1 (harvest) → J2 (push) → self-healing cascade
 │    │
 │    ├── G5 (Chimera) ← G1 proven
 │    ├── G6 (bearDog public) ← independent (ready)
 │    ├── G8 (Plasmodium) ← G7 complete
 │    └── G9 (JOSS) ← G3 + G7 complete
 │
 └── Peptidoglycan P0: DNS all gates → P1: RustDesk house2 → resume enrollment
```

---

*Wave 155d. Peptidoglycan layer failure diagnosed and fixed — three-layer model
(outer membrane / peptidoglycan / inner membrane) now documented. songBird
closed J3+J4+J5 in one commit (cascade automation surface). G3 converging —
rhizoCrypt cross-gate provenance shipped, sweetGrass READY, 4 gaps identified
with clear owners. Forgejo restored. 5 pending commits pushed. Next: DNS
hardening across all gates, house2 RustDesk provisioning, and G3 Phase 1 wiring.*
