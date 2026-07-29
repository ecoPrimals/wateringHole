# ecoPrimals Ecosystem Blurb — Wave 155i

**Date**: Jul 29, 2026 17:30 EDT | **Wave**: 155i | **From**: eastGate overwatch
**Posture**: **blueGate NEST 10/10 ON WINDOWS — first multi-composition Windows deployment. westGate composition broker LIVE (704 capabilities, E2E routing). strandGate Node Atomic VALIDATED (746 pipelines/sec). songBird 3 follow-up Windows compile fixes shipped (`d9bda555`). NEW P1: Windows depot stale (14 .exe from 07/16) — Linux depot current. bearDog crypto.sign_ed25519 blocks Provenance 7/7.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Posture**: blueGate achieved Tower G1 (3/3) AND Nest Atomic (10/10) on Windows —
first multi-composition deployment on a non-Linux gate. westGate composition broker
LIVE: biomeOS v4.45 deployed from depot, 704 capabilities registered (was 163),
COORDINATED mode, E2E capability routing proven (`content.put`, `storage.put`).
strandGate Node Atomic validated: 450 methods, 746 pipelines/sec, sub-ms GPU.
songBird shipped 3 follow-up Windows compile fixes (`d9bda555`).

**Key divergence**: Windows depot stale — all 14 `.exe` from 07/16, pre-P0-fix.
blueGate built from source (3m 56s). Linux depot is current (19/19). Windows
cross-compilation target not in sporeGate pipeline. Also: no Windows CI gate —
compile errors slip through. songBird `d9bda555` fixes NOT in any depot yet.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Status |
|------|-----------------|--------|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. |
| **westGate** | petalTongue, squirrel, nestGate, Provenance Trio | **NEST ATOMIC LIVE. Composition broker LIVE. 704 caps. 3,216 CAS objects. 20 sockets.** |
| **strandGate** | toadStool, barraCuda, coralReef | **NODE ATOMIC VALIDATED. 450 methods. 746 pipelines/sec. Sub-ms GPU.** |
| **sporeGate** | golgiBody depot, cellMembrane ops | **Linux depot current (19/19). Windows depot STALE.** |
| **blueGate** | Windows. Full atomic stack proof. | **TOWER G1 DONE. NEST 10/10. Node Atomic NEXT. Sub-builder. Topo H2.** |
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
14. **DONE**: songBird P0 Windows platform gate FIXED (`8c0adc8d`)
15. **DONE**: sporeGate deep-debt depot rebuild — 19/19 binaries current (songBird, biomeOS, sweetGrass all refreshed)
16. **DONE**: strandGate Node Atomic VALIDATED — 450 methods, 746 pipelines/sec, sub-ms GPU
17. **DONE**: cellMembrane 45+ magic numbers centralized
18. **DONE**: blueGate Tower G1 COMPLETE (3/3 on Windows — source build, 3m 56s)
19. **DONE**: blueGate Nest Atomic VALIDATED (10/10 primals, 107.6 MB, TCP transport)
20. **DONE**: songBird 3 follow-up Windows compile fixes (`d9bda555`)
21. **DONE**: westGate composition broker LIVE (biomeOS v4.45, 704 caps, COORDINATED, E2E routing)
22. **DONE**: westGate CAS 3,216 objects, Provenance Trio 6/7 re-confirmed
23. **NOW**: Windows depot rebuild — 14 `.exe` from 07/16, need `d9bda555` + all Wave 155i
24. **NOW**: Windows CI gate — `cargo check --target x86_64-pc-windows-gnu` on Linux CI
25. **NOW**: bearDog `crypto.sign_ed25519` implementation (blocks Provenance 7/7)
26. **NOW**: biomeOS graph executor riboCipher fix (one-line: `send_ribocipher_jsonrpc_request()`)
27. **NEXT**: blueGate Node Atomic (toadStool + barraCuda + coralReef)
28. **NEXT**: blueGate sub-builder enrollment under sporeGate
29. **NEXT**: swiftGate Tower Atomic deployment (Windows, second proof)
30. **NEXT**: AlphaFold bulk ingestion (~1TB) from northGate through Nest Atomic pipeline
31. **NOTE**: northGate is daily driver — data source ONLY, do not deploy

| Metric | Value |
|--------|-------|
| Signal graphs | **27** (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| Primal tests | **~63K+** (nestGate 13K+, toadStool 9.2K+, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.3K, cellMembrane 1.2K) |
| Jelly strings | **7/8 resolved** (J6 CLOSED, J7 low, J8 deployed) |
| BTSP | **13/13** |
| Linux depot | **19/19 current** (16 musl + 3 glibc). BLAKE3 19/19 verified |
| Windows depot | **14 `.exe` STALE** (07/16 — pre-P0-fix, pre-Wave-155i) |
| Gates ONLINE | **9** — blueGate Nest 10/10, strandGate Node Atomic, westGate Broker LIVE |
| Threat categories | **9** (skunkBat ConnectivityAnomaly) |
| CAS objects on ZFS | **3,216** objects, 25.3TB pool, 1.50x compression, ARC 99.98% hit |
| westGate capabilities | **704** registered (was 163), 390 translations, 70 signal graphs |
| GPU validation | RTX 3090 FP32 96T / FP64 104T / DF64 92T + RX 6950 XT dual-GPU — strandGate |
| blueGate Windows | **10 primals running, 107.6 MB, TCP-only transport** |

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
| **songBird** | **P0 FIXED + 3 follow-up Windows compile fixes**: TCP fallback, enrollment_crypto UDS→TCP, import path fix, cfg-gating. Deep debt: 2 test monoliths split (1,018L+998L→10 modules). | `d9bda555` |
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
| **sporeGate** | **9/11 HEALTHY** | Linux depot 19/19 current. **Windows depot STALE (07/16).** | Windows cross-build pipeline. Sub-builder integration. |
| **eastGate** | ONLINE | songBird `d9bda555`. cellMembrane magic numbers. Overwatch cascade. | Windows CI gate. bearDog crypto. |
| **northGate** | ONLINE (Windows) | **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). | Data staging to westGate/blueGate once Nest Atomic validated on target |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | NOW | NEXT |
|------|--------|-----|------|
| **blueGate** | **NEST 10/10** (Windows) | **G1 DONE. Nest DONE. 10 primals, 107.6 MB, TCP-only.** Built from source. | Node Atomic. Sub-builder enrollment. |
| **strandGate** | **NODE ATOMIC VALIDATED** | **450 methods, 746 pipelines/sec, sub-ms GPU.** barraCuda 4,957 tests, toadStool 9,193+. | Full BTSP. glibc depot refresh. |
| **westGate** | **BROKER LIVE** | **biomeOS v4.45 deployed. 704 caps. COORDINATED. 3,216 CAS objects. 20 sockets.** | Graph executor riboCipher fix. AlphaFold ingestion. |
| **swiftGate** | ONLINE (Windows) | — | G1 Tower on Windows (second Windows proof after blueGate) |
| **ironGate** | ONLINE | HDD enclave experiment | Nest Atomic secondary target |
| **southGate** | HW READY | — | Enroll → Tower |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner | Status |
|---|----------|-------|-------|--------|
| 1 | **P1** | **Windows depot stale** — 14 `.exe` from 07/16 (pre-P0-fix). `d9bda555` not in any depot. | sporeGate | **OPEN** — blocks depot-path Windows deployments |
| 2 | **P1** | **No Windows CI gate** — compile errors slip through | eastGate/CI | **OPEN** — `cargo check --target x86_64-pc-windows-gnu` |
| 3 | **P1** | bearDog `crypto.sign_ed25519` returns health stub | bearDog | Blocks Provenance Trio 7/7 |
| 4 | **P1** | biomeOS graph executor sends raw JSON-RPC (no riboCipher prefix) | biomeOS | One-line fix: `send_ribocipher_jsonrpc_request()` |
| 5 | P1 | sporeGate mesh.reachability + rootpulse.ledger | sporeGate | 2/11 degraded |
| 6 | P2 | songBird `services: 0` — bearDog/skunkBat not registered via TCP | songBird | blueGate AAR |
| 7 | P2 | songBird PID file Unix paths on Windows (`C:\var\run\songbird\`) | songBird | blueGate AAR |
| 8 | P2 | sweetGrass braid_id→UUID mismatch | sweetGrass | westGate AAR |
| 9 | P2 | biomeOS socket `biomeos/` vs `membrane/` split | biomeOS | westGate AAR |
| 10 | P2 | biomeOS socket evaporation on Neural API restart | biomeOS | westGate AAR |
| 11 | P2 | Nest primal CLI flag divergence (--bind vs --host vs --bind-address) | Multi | blueGate Nest AAR |
| 12 | P2 | hotSpring Forgejo pack corruption | eastGate admin | Low |

**ZERO P0s.** blueGate proved Tower+Nest on Windows via source build. Windows depot pipeline and CI are the new systemic P1s.

---

*Wave 155i — blueGate NEST 10/10 on Windows (historic first). Tower G1 achieved via
source build after 3 follow-up compile fixes (`d9bda555`). westGate composition broker
LIVE: biomeOS v4.45, 704 capabilities, COORDINATED mode, E2E routing proven. strandGate
Node Atomic: 450 methods, 746 pipelines/sec. ZERO P0s. New P1s: Windows depot stale
(14 .exe from 07/16), no Windows CI gate. bearDog crypto.sign blocks Provenance 7/7.
~63K+ tests. 27 signal graphs. 9 gates online.*
