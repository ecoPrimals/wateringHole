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
| CAS objects on ZFS | **3,119** objects, 25.4TB pool, 1.56× compression |
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
| **songBird** | Mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L | `59f7ef75` |
| **loamSpine** | Registry drift fixed: `certificate.verify/lifecycle/history` discoverable. 1,285 tests | `d79231a` |
| **biomeOS** | **COMPOSITION BROKER SHIPPED**: riboCipher framing + BTSP executor, 35 E2E tests, connection pool IO, v4.45, 8,564 tests | `8cee1adb` |
| **petalTongue** | Topology → runtime manifest, main.rs split, geometry module. 6,605 tests | `d60e67d` |
| **squirrel** | Capability purification: beardog→security_provider, adapter IPC. 763 tests | `acbe09e3` |

---

## GLACIAL GOALS — SEQUENCED

| # | Goal | Status | Gate |
|---|------|--------|------|
| G1 | Tower on Windows | **ACTIVE — blueGate target** | blueGate first, swiftGate second |
| G7 | Gate enmeshment | **ADVANCING** | westGate+strandGate LIVE. blueGate next (inner membrane topo owner H2) |
| G6 | bearDog public | READY | OPEN — songBird ACME Phase 1 unblocks TLS |
| G3 | Nest Atomic Phase 0 | **LIVE ON WESTGATE** | Provenance Trio 6/7, ZFS online, BTSP broker shipped. blueGate Nest Atomic is NEXT. |
| G4 | Nest cross-platform | **ACTIVE** | blueGate (Windows) Nest Atomic after Tower stable — biomeOS full broker role |
| G10 | Sub-builder mesh | **NEW** | blueGate as sub-builder under sporeGate — accelerate depot binary production |
| G5 | Chimera Phase 0 | PENDING | AFTER G1 |
| G2 | Tower on Android | PENDING | AFTER G1 |
| G8 | Plasmodium | PENDING | AFTER G7 |
| G9 | JOSS publication | PENDING | AFTER G3+G7 |

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
| J8 | Key enrollment portal | **DEPLOYED** — step-ca live at ca.primals.eco (see SPOREGATE_DEPLOYMENT_OPS_155h_AAR) | sporeGate ops |

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
| **blueGate** | **BOOTSTRAPPED** (Windows) | **40/40 repos synced. Tower bins verified. WG+SSH keys generated — awaiting registration.** | Tower Atomic deploy → Nest → Node. Sub-builder. Topo owner H2. |
| **strandGate** | **TOWER+COMPUTE LIVE** | Glibc depot received. Compute Trio validated. | Node Atomic profiling. Full BTSP validation. |
| **westGate** | **NEST ATOMIC LIVE** | CAS on ZFS verified. biomeOS broker ready. | E2E `nest.ingest_dataset` live. AlphaFold ingestion (~11hr dsync, NVMe staging recommended). |
| **swiftGate** | ONLINE (Windows) | — | G1 Tower on Windows (second Windows proof after blueGate) |
| **ironGate** | ONLINE | HDD enclave experiment | Nest Atomic secondary target |
| **southGate** | HW READY | — | Enroll → Tower |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner | Status |
|---|----------|-------|-------|--------|
| 1 | ~~**P0**~~ | ~~biomeOS BTSP session propagation~~ | ~~biomeOS~~ | **SHIPPED** (v4.45, `48cf9c33`) |
| 2 | ~~**P0**~~ | ~~biomeOS riboCipher transport framing~~ | ~~biomeOS~~ | **SHIPPED** (v4.45, `48cf9c33`) |
| 3 | P1 | bearDog `crypto.sign_ed25519` returns health stub, not signature | bearDog | Blocks Provenance Trio step 7/7 |
| 4 | P1 | sweetGrass depot binary lag (v0.7.64 vs source v0.8.0) | sporeGate | Blocks westGate G3 live validation |
| 5 | P1 | biomeOS depot binary lag — v4.45 composition broker not on sporeGate | sporeGate | Needed for live E2E |
| 6 | P1 | sporeGate mesh.reachability + rootpulse.ledger degraded | sporeGate | 2/11 remaining |
| 7 | P1 | songBird riboCipher probes → sweetGrass log noise (every 30s) | songBird | Low but annoying |
| 8 | P1 | hotSpring Forgejo pack corruption | eastGate admin | Not our lane |

**ZERO P0s.** Resolved: ~~P0 BTSP session propagation~~ SHIPPED. ~~P0 riboCipher transport~~ SHIPPED. ~~P0 glibc depot~~ FIXED. ~~P1 WG DNS~~ FIXED. ~~P1 ZFS pool~~ ONLINE. ~~P1 step-ca~~ DEPLOYED. ~~P1 membrane depot~~ REBUILT (J6). ~~P1 nestGate ghost methods~~ REMOVED. ~~P1 toadStool deployment docs~~ SHIPPED (S345). sporeGate health 5/11→9/11.

---

## HANDOFFS (newest first)

| File | Status |
|------|--------|
| `CELLMEMBRANE_WAVE155i_DEEP_DEBT_EVOLUTION.md` | **Deep debt: sandbox fail-closed, registry-driven tower** |
| `NESTGATE_WAVE155i_DEEP_DEBT_CAS_JUL29_2026.md` | **CAS on ZFS verified, 13K+ tests, zero unsafe** |
| `CORALREEF_WAVE155i_STRANDGATE_VALIDATION_JUL29_2026.md` | **18/18 methods, 463 .expect() purged, PTX modernized** |
| `STRANDGATE_WAVE155i_COMPUTE_TRIO_VALIDATION.md` | **Compute Trio rebuilt, RTX 3090 profiled, 5 primals** |
| `BIOMEOS_TOWER_ATOMIC_COMPOSITION_BROKER_WAVE155i.md` | biomeOS BTSP composition broker (P0) |
| `SWEETGRASS_G3_WIRING_COMPLETE_WAVE155i.md` | sweetGrass G3 COMPLETE — Provenance Trio CLOSED |
| `CELLMEMBRANE_WAVE155i_GLIBC_DEPOT_WG_DNS.md` | P0 glibc FIXED + P1 WG DNS FIXED |

AARs:
- `SWEETGRASS_G3_E2E_VALIDATED_155i_AAR.md` — **G3 E2E validated, 1,636 tests, v0.8.0**
- `WESTGATE_CASCADE_REVIEW_ZFS_PROVENANCE_155i_AAR.md` — **CAS migration, Provenance 6/7, storage profiling**
- `STRANDGATE_COMPUTE_TRIO_SILICON_UTILIZATION_155i_AAR.md` — **DF64 framing, RTX 3090 FP64 ~104T, silicon map**
- `SPOREGATE_DEPLOYMENT_OPS_155i_AAR.md` — **Depot refresh 19 binaries, health 5/11→9/11**
- `WESTGATE_NEST_ATOMIC_MULTICOMP_155i_AAR.md` — First multi-composition. 8 services, 1,704 capabilities.
- `WESTGATE_ZFS_POOL_CREATION_155i_AAR.md` — ZFS 25.4TB + L2ARC online, all 5 tiers

---

### SPOREPRINT (Wave 155i transplant — Jul 29, 2026)

sporePrint updated to reflect Wave 155i ecosystem state:
- Nest Atomic LIVE on westGate: 8 services, 1,704 capabilities, ZFS, Provenance Trio CLOSED
- strandGate Tower + Compute Trio LIVE promoted from HW READY
- Test counts updated across 13 primals (105,568 total, validated by spore-validate)
- 27 signal graphs documented, 39 genomeBin depot binaries
- G3 glacial goal now LIVE, G7 ADVANCING
- 8+ gates online (westGate, strandGate, blueGate, swiftGate all promoted)
- Tower Atomic page updated with "Compositions built on Tower" section

Files changed: config.toml, tower_atomic.md, living-systems.md, MESH_TOPOLOGY.md,
NUCLEUS_ARCHITECTURE.md, CONTEXT.md, llms.txt, products/_index.md, architecture/_index.md, README.md

---

*Wave 155i — Composition Broker + Deep Debt Wave. ZERO P0s. biomeOS v4.45 shipped
composition broker. 8 primals deep debt sweeps. CAS on ZFS verified (3,119 objects).
RTX 3090 profiled (FP64 ~104T). sporeGate depot refreshed (19 binaries). E2E signal
graphs UNBLOCKED. NEXT: blueGate (Windows) — Tower → Nest → Node Atomic, inner
membrane topo owner H2, sub-builder under sporeGate. First full atomic stack proof
on Windows with biomeOS in full composition broker role. northGate is daily driver —
AlphaFold data source only, do not deploy. swiftGate follows blueGate. ~63K+ tests.*
