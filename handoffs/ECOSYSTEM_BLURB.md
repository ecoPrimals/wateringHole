# ecoPrimals Ecosystem Blurb — Wave 155i

**Date**: Jul 29, 2026 11:45 EDT | **Wave**: 155i | **From**: eastGate overwatch
**Posture**: **COMPOSITION BROKER SHIPPED. BOTH P0s RESOLVED. biomeOS v4.45: riboCipher framing + BTSP session propagation in signal graph executor — composition broker pattern operational. 8 primals deep debt wave. CAS on ZFS verified (3,119 objects). RTX 3090 GPU profiled (FP64 ~104T). Nest Atomic E2E signal graphs UNBLOCKED. AlphaFold ingestion pipeline READY.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Posture**: Composition broker SHIPPED. biomeOS v4.45 delivered riboCipher
framing (`[0xEC, 0x01]` prefix on all CLI/core IPC) AND BTSP session propagation
in signal graph executor — the composition broker pattern is now operational.
8 primals shipped simultaneous deep debt sweeps. westGate Nest Atomic: 8 services,
3,119 CAS objects on ZFS, Provenance Trio 6/7 live. strandGate Compute Trio
rebuilt from glibc source, RTX 3090 profiled (FP64 ~104 TFLOPS). sporeGate depot
fully refreshed (19 binaries, health 5/11→9/11). E2E signal graphs (`nest.ingest_dataset`,
`nest.store`) are NOW UNBLOCKED for live validation.

**P0s RESOLVED**: ~~biomeOS BTSP session propagation~~ SHIPPED (`48cf9c33`).
~~biomeOS riboCipher transport~~ SHIPPED (`48cf9c33`). 35 composition broker
E2E tests validate nest topology, BTSP routing, and riboCipher framing.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Status |
|------|-----------------|--------|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. |
| **westGate** | petalTongue, squirrel, nestGate, Provenance Trio | **NEST ATOMIC LIVE. 8 services, 3,119 CAS objects, ZFS 25.4TB.** |
| **strandGate** | toadStool, barraCuda, coralReef | **Tower+Compute LIVE. RTX 3090 profiled. 5 primals, 17 sockets.** |
| **sporeGate** | golgiBody depot, cellMembrane ops | **Depot refreshed. 9/11 health. 19 binaries current.** |
| **blueGate** | **NEXT TARGET** — Windows. Full atomic stack proof. | **Tower → Nest → Node Atomic. Sub-builder. Inner membrane topo owner H2.** |
| **northGate** | AlphaFold data (~1TB). Daily driver — DO NOT RISK. | Windows. Data source only. |

**Sequencing**:
1. **DONE**: westGate Tower Atomic + code team audits + execution
2. **DONE**: strandGate sync + Tower Atomic + Compute Trio deployment
3. **DONE**: loamSpine registry drift fixed (certificate.verify/lifecycle/history)
4. **DONE**: biomeOS `nest.ingest_dataset` signal graph created
5. **DONE**: sweetGrass G3 wiring COMPLETE (v0.8.0, E2E validated, 1,636 tests)
6. **DONE**: westGate ZFS pool ONLINE (25.4TB, CAS verified, 3,119 objects)
7. **DONE**: westGate Nest Atomic multi-composition deployed (8 services, 1,704 capabilities)
8. **DONE**: P0 glibc depot FIXED. P1 WG DNS FIXED. P1 membrane depot REBUILT (J6).
9. **DONE**: Deep debt wave — nestGate 13K+, toadStool S346, cellMembrane fail-closed, barraCuda deprecation sweep, coralReef .expect() purge
10. **DONE**: strandGate Compute Trio rebuilt from glibc source, RTX 3090 GPU profiled
11. **DONE**: sporeGate depot refresh — 19 binaries, BLAKE3 verified, health 5/11→9/11
12. **DONE**: biomeOS BTSP session propagation in signal graph executor — SHIPPED (v4.45, `48cf9c33`)
13. **DONE**: biomeOS riboCipher transport fix in CLI paths — SHIPPED (v4.45, `48cf9c33`)
14. **NOW**: blueGate Tower Atomic deployment (Windows — G1 proof, inner membrane topo owner H2)
15. **NOW**: blueGate sub-builder enrollment under sporeGate (accelerate depot binary production)
16. **NOW**: bearDog `crypto.sign_ed25519` implementation (blocks Provenance 7/7)
17. **NOW**: sweetGrass + biomeOS depot binary refresh on sporeGate
18. **NEXT**: blueGate Nest Atomic (after Tower stable — biomeOS full composition broker role)
19. **NEXT**: blueGate Node Atomic (after Nest stable)
20. **NEXT**: swiftGate Tower Atomic deployment (Windows, second Windows proof)
21. **NEXT**: AlphaFold bulk ingestion (~1TB) from northGate through Nest Atomic pipeline
22. **NOTE**: northGate is daily driver — data source ONLY, do not deploy or risk breaking

| Metric | Value |
|--------|-------|
| Signal graphs | **27** (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| Primal tests | **~55K+** (nestGate 13K+, toadStool 9.2K+, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.3K, cellMembrane 1.2K) |
| Jelly strings | **7/8 resolved** (J6 CLOSED, J7 low, J8 deployed) |
| BTSP | **13/13** |
| genomeBin depot | **19 binaries refreshed** (16 musl + 3 glibc). BLAKE3 checksums 19/19 verified |
| Gates ONLINE | **8** + strandGate Tower+Compute LIVE, westGate Nest Atomic LIVE |
| Threat categories | **9** (skunkBat ConnectivityAnomaly) |
| CAS objects on ZFS | **3,119** objects, 25.4TB pool, 1.56x compression |
| GPU validation | RTX 3090 FP32 96T / FP64 104T / DF64 92T — strandGate |
| sporeGate health | **9/11** OK (was 5/11) |

---

## WHAT CODE TEAMS SHIPPED (Wave 155i — deep debt + validation wave)

| Team | Latest Evolution | Key Commits |
|------|------------------|-------------|
| **sweetGrass** | **G3 E2E validated**: 11 E2E ledger tests added, mock loamSpine UDS server. 1,636 tests, v0.8.0 | `ab887e8` |
| **cellMembrane** | **Deep debt**: sandbox fail-closed, registry-driven tower status (no hardcoded names), 5 dedup extractions. -135 net lines. 1,221 tests | `54d0865` |
| **nestGate** | **CAS on ZFS verified**: 3,119 objects on 25.4TB pool. CLI evolved (probe bypasses JWT), file renames, ghost methods removed. **13,095+ tests**, zero unsafe, zero panics | `6b6d4849` |
| **barraCuda** | **RTX 3090 profiled**: FP64 ~104 TFLOPS, DF64 framing corrected, 10 batch funcs deprecated to shader path. Deep debt sweep. 4,957 tests | `34603689` |
| **coralReef** | **Deep debt**: 463 `.expect()` eliminated, PTX macro modernization (-363L net), capability-based env. 3,527 tests | `c6ab001` |
| **toadStool** | **S346**: security fail-closed (macOS/Windows sandbox), unsafe containment (hw-safe crate), 75 doc warnings fixed. Doctor CLI bug fix. 9,193+ tests | `b9ded4280` |
| **skunkBat** | Cargo update: tokio-macros 2.7.1→2.7.2 | `b0df971` |
| **songBird** | **P0 FIXED**: Windows platform gate → TCP fallback. Deep debt: 2 test monoliths split (1,018L+998L→10 modules). Zero files >800L. | `8c0adc8d` |
| **loamSpine** | Registry drift fixed: `certificate.verify/lifecycle/history` discoverable. 1,285 tests | `d79231a` |
| **biomeOS** | **COMPOSITION BROKER SHIPPED**: riboCipher framing + BTSP executor, 35 E2E tests, connection pool IO, v4.45, 8,564 tests | `8cee1adb` |
| **petalTongue** | Topology → runtime manifest, main.rs split, geometry module. 6,605 tests | `d60e67d` |
| **squirrel** | Capability purification: beardog→security_provider, adapter IPC. 763 tests | `acbe09e3` |

---

## JELLY STRINGS — 7 OF 8 RESOLVED

| # | What | Status | Owner |
|---|------|--------|-------|
| J1 | Harvest | **CLOSED** — `--push` flag | cellMembrane |
| J2 | Depot push | **CLOSED** — `plasmid.push` + Rust depot_sync | cellMembrane |
| J3 | Service restart | **CLOSED** — `deploy.hot_swap` | songBird |
| J4 | Caddy config | **CLOSED** — route self-config | songBird |
| J5 | WG peer reg | **HARDENED** | songBird |
| J6 | systemd overrides | **CLOSED** — `gate.configure` + `gate.apply` | cellMembrane |
| J7 | Legacy detection | OPEN (low priority) | cellMembrane |
| J8 | Key enrollment portal | **DEPLOYED** — step-ca live at ca.primals.eco | sporeGate ops |

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1 (peptidoglycan anchor: sporeGate)

| Gate | Status | NOW | NEXT |
|------|--------|-----|------|
| **sporeGate** | **9/11 HEALTHY** | Depot refresh DONE. Resolve remaining 2 degraded. Prepare blueGate sub-builder enrollment. | blueGate builder integration. biomeOS+sweetGrass depot rebuild. |
| **eastGate** | ONLINE | biomeOS composition broker SHIPPED (v4.45). Overwatch cascade. | Coordinate blueGate Tower deployment |
| **northGate** | ONLINE (Windows) | **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). | Data staging to westGate/blueGate once Nest Atomic validated on target |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | NOW | NEXT |
|------|--------|-----|------|
| **blueGate** | **TOWER 2/3** (Windows) | **Mesh LIVE (3 peers). bearDog+skunkBat HEALTHY. songBird fix SHIPPED — awaiting depot rebuild.** | Depot pull → full Tower → Nest → Node. Sub-builder. Topo owner H2. |
| **strandGate** | **TOWER+COMPUTE LIVE** | Glibc depot received. Compute Trio validated. | Node Atomic profiling. Full BTSP validation. |
| **westGate** | **NEST ATOMIC LIVE** | CAS on ZFS verified. biomeOS broker ready. | E2E nest.ingest_dataset live. AlphaFold ingestion. |
| **swiftGate** | ONLINE (Windows) | — | G1 Tower on Windows (second Windows proof after blueGate) |
| **ironGate** | ONLINE | HDD enclave experiment | Nest Atomic secondary target |
| **southGate** | HW READY | — | Enroll → Tower |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner | Status |
|---|----------|-------|-------|--------|
| 1 | P1 | songBird Windows fix awaiting depot rebuild | sporeGate | **Our lane** |
| 2 | P1 | bearDog crypto.sign_ed25519 returns health stub | bearDog | Code team |
| 3 | P1 | sweetGrass depot binary lag (v0.7.64 vs v0.8.0) | sporeGate | **Our lane** |
| 4 | P1 | biomeOS depot binary lag (v4.45 not on sporeGate) | sporeGate | **Our lane** |
| 5 | P1 | sporeGate mesh.reachability + rootpulse.ledger | sporeGate | Code team items |
| 6 | P1 | songBird riboCipher probe noise (every 30s) | songBird | Code team |
| 7 | P1 | hotSpring Forgejo pack corruption | eastGate admin | Not our lane |

**ZERO P0s.** All prior P0s resolved.

---

*Wave 155i — Composition Broker + Deep Debt Wave. ZERO P0s. biomeOS v4.45 shipped
composition broker. 8 primals deep debt sweeps. CAS on ZFS verified (3,119 objects).
RTX 3090 profiled (FP64 ~104T). sporeGate depot refreshed (19 binaries). E2E signal
graphs UNBLOCKED. NEXT: blueGate (Windows) — Tower → Nest → Node Atomic, inner
membrane topo owner H2, sub-builder under sporeGate.*
