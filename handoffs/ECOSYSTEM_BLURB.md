# ecoPrimals Ecosystem Blurb — Wave 155i

**Date**: Jul 29, 2026 09:15 EDT | **Wave**: 155i | **From**: eastGate overwatch
**Posture**: **NEST ATOMIC LIVE ON WESTGATE. Provenance Trio CLOSED (sweetGrass G3 wired). westGate 8-service multi-composition deployed, 1,704 capabilities auto-discovered, 6 PDBs in CAS, ZFS 25.4TB + 2TB L2ARC online, all 5 storage tiers operational. P0 glibc depot FIXED (cellMembrane). P1 WG DNS FIXED. NEW P0: biomeOS needs BTSP session propagation in signal graph executor for composition broker pattern.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Posture**: Nest Atomic LIVE on westGate — first multi-composition deployment.
8 services deployed (Tower + Nest Atomic). biomeOS auto-discovered 1,704
capabilities. sweetGrass G3 wiring COMPLETE (v0.8.0) — Provenance Trio triangle
CLOSED. ZFS pool online (25.4TB mirrors + 2TB SSD L2ARC). All 5 storage tiers
operational. cellMembrane FIXED P0 glibc depot target + P1 WG DNS. songBird mesh
refactor shipped. 6 PDB protein structures stored in CAS with dedup verified.

**NEW P0**: biomeOS Neural API needs BTSP session propagation in signal graph
executor — inter-composition boundary broke when Nest primals require BTSP auth.
The Neural API must be the composition broker (handoff issued).

**PRIOR P0 CLOSED**: glibc depot target — cellMembrane `targets_for_primal()`
now auto-appends gnu for GPU primals unconditionally.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Status |
|------|-----------------|--------|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. |
| **westGate** | petalTongue, squirrel, nestGate, Provenance Trio | **NEST ATOMIC LIVE. 8 services, 1,704 capabilities, ZFS 25.4TB + L2ARC.** |
| **strandGate** | toadStool, barraCuda, coralReef | **Tower LIVE. Compute Trio deployed.** |

**Sequencing**:
1. **DONE**: westGate Tower Atomic + code team audits + execution
2. **DONE**: strandGate sync + Tower Atomic + Compute Trio deployment
3. **DONE**: loamSpine registry drift fixed (certificate.verify/lifecycle/history)
4. **DONE**: biomeOS `nest.ingest_dataset` signal graph created
5. **DONE**: sweetGrass G3 wiring COMPLETE (v0.8.0) — Provenance Trio CLOSED
6. **DONE**: westGate ZFS pool ONLINE (25.4TB + 2TB L2ARC, all 5 tiers)
7. **DONE**: westGate Nest Atomic multi-composition deployed (8 services, 1,704 capabilities)
8. **DONE**: P0 glibc depot target FIXED (cellMembrane). P1 WG DNS FIXED.
9. **NOW**: biomeOS BTSP session propagation in signal graph executor (NEW P0)
10. **NOW**: biomeOS riboCipher transport fix in CLI paths (NEW P0)
11. **NOW**: Rebuild membrane depot binary (gate.configure/gate.apply)
12. **NEXT**: E2E Nest Atomic signal graph validation (with BTSP working)
13. **NEXT**: AlphaFold bulk ingestion (~1TB) through Nest Atomic pipeline

| Metric | Value |
|--------|-------|
| Signal graphs | **27** (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| Primal tests | **~72K+** (toadStool 23K, songBird 14K+, nestGate 13K, bearDog 12K, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.3K, cellMembrane 1.2K) |
| Jelly strings | **7/8 resolved** (J6 CLOSED, J7 low, J8 code shipped) |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 musl targets) + glibc auto-add for GPU primals SHIPPED |
| Gates ONLINE | **8** + strandGate Tower LIVE |
| Threat categories | **9** (skunkBat ConnectivityAnomaly) |

---

## WHAT CODE TEAMS SHIPPED (Wave 155f-i)

| Team | Latest Evolution | Key Commits |
|------|------------------|-------------|
| **sweetGrass** | **G3 wiring COMPLETE**: `LedgerClient`, `braid.commit` → loamSpine, ledger proof. v0.8.0, 1,625 tests | `666dea5` |
| **cellMembrane** | **P0 glibc FIXED**: `targets_for_primal()` auto-appends gnu. **P1 WG DNS FIXED**: `DNS=` in wg-quick. 1,223 tests | `8d9bb58` |
| **songBird** | Mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L | `59f7ef75` |
| **loamSpine** | Registry drift fixed: `certificate.verify/lifecycle/history` discoverable. 1,285 tests | `d79231a` |
| **biomeOS** | `nest.ingest_dataset` signal graph (5-node pipeline). 27 total signal graphs | `e843b9ca` |
| **barraCuda** | GPU SIGSEGV fix (`GPU_TEST_GUARD`), BTSP env races, dead code (-1,200L). 4,957 tests | `042f1493` |
| **coralReef** | 18/18 JSON-RPC dispatch, BTSP Phase 3 encrypted transport. 3,527 tests | `3d969f8` |
| **nestGate** | P0/P1 closed, live CLI, FHS centralized, ZFS tier migration. 12,973 tests | `3ca3e1bc` |
| **petalTongue** | Topology → runtime manifest, main.rs split, geometry module. 6,605 tests | `d60e67d` |
| **squirrel** | Capability purification: beardog→security_provider, adapter IPC. 763 tests | `acbe09e3` |
| **toadStool** | S344 deny.toml, overstep reduction, socket centralization. 23,332 tests | `04fcb96e3` |

---

## GLACIAL GOALS — SEQUENCED

| # | Goal | Status | Gate |
|---|------|--------|------|
| G1 | Tower on Windows | **FRONTLOADED** | OPEN |
| G7 | Gate enmeshment | **ADVANCING** | westGate+strandGate Tower LIVE |
| G6 | bearDog public | READY | OPEN — songBird ACME Phase 1 unblocks TLS |
| G3 | Nest Atomic Phase 0 | **LIVE ON WESTGATE** | Provenance Trio CLOSED, ZFS online, 8 services, 1,704 capabilities. BTSP broker needed. |
| G4 | Nest cross-platform | IN PROGRESS | AFTER TOWER |
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
| **sporeGate** | ONLINE | Rebuild depot with glibc target. step-ca deploy on golgiBody. | Glibc genomeBins for strandGate compute |
| **eastGate** | ONLINE | biomeOS BTSP broker evolution. bearDog ACME Phase 2. | Coordinate Nest Atomic validation fleet |
| **northGate** | ONLINE (Windows) | Tower assessment for AlphaFold federation | Stage ~1TB AlphaFold → westGate |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | NOW | NEXT |
|------|--------|-----|------|
| **strandGate** | **TOWER+COMPUTE LIVE** | Await glibc depot rebuild | RTX 3090 compute profiling. Node Atomic. |
| **westGate** | **NEST ATOMIC LIVE** | Await biomeOS BTSP broker | E2E signal graph → AlphaFold ingestion |
| **blueGate** | ONLINE (Windows) | Peptidoglycan anchor H2 | G1 Tower on Windows proof |
| **ironGate** | ONLINE | HDD enclave experiment | Nest Atomic secondary target |
| **swiftGate** | ONLINE (Windows) | — | G1 Tower on Windows |
| **southGate** | HW READY | — | Enroll → Tower |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner | sporeGate Note |
|---|----------|-------|-------|----------------|
| 1 | **P0** | biomeOS BTSP session propagation in signal graph executor | biomeOS | Code team |
| 2 | **P0** | biomeOS riboCipher transport framing in CLI paths | biomeOS | Code team |
| 3 | P1 | Rebuild membrane depot binary with gate.configure/gate.apply | cellMembrane/sporeGate | **Our lane** |
| 4 | ~~P1~~ | ~~Deploy step-ca on golgiBody (J8 deployment)~~ | ~~sporeGate ops~~ | **DONE (155h)** |
| 5 | P1 | toadStool deployment model docs (no `server` subcommand) | toadStool | Code team |
| 6 | P1 | hotSpring Forgejo pack corruption | eastGate admin | Not our lane |
| 7 | P1 | nestGate ghost methods `content.repo.*`/`content.mirror.*` | nestGate | Code team |

**Resolved this wave**: ~~P0 glibc depot~~ FIXED. ~~P1 WG DNS~~ FIXED. ~~P1 ZFS pool~~ ONLINE. ~~P1 step-ca~~ DEPLOYED (155h).

---

## HANDOFFS (newest first)

| File | Status |
|------|--------|
| `BIOMEOS_TOWER_ATOMIC_COMPOSITION_BROKER_WAVE155i.md` | **biomeOS BTSP composition broker (NEW P0)** |
| `SWEETGRASS_G3_WIRING_COMPLETE_WAVE155i.md` | **sweetGrass G3 COMPLETE — Provenance Trio CLOSED** |
| `CELLMEMBRANE_WAVE155i_GLIBC_DEPOT_WG_DNS.md` | **P0 glibc FIXED + P1 WG DNS FIXED** |
| `TOWER_ATOMIC_VALIDATION_WAVE155i.md` | Tower health validation — all gates |
| `NEST_ATOMIC_ALPHAFOLD_WAVE155i.md` | Nest Atomic pipeline + AlphaFold ingestion plan |

AARs:
- `WESTGATE_NEST_ATOMIC_MULTICOMP_155i_AAR.md` — **First multi-composition deployment. 8 services, 1,704 capabilities.**
- `WESTGATE_ZFS_POOL_CREATION_155i_AAR.md` — **ZFS 25.4TB + L2ARC online, all 5 tiers**
- `SPOREGATE_DEPLOYMENT_OPS_155h_AAR.md` — P0 glibc + step-ca + depot + firewall (RESOLVED)

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

*Wave 155i. Nest Atomic LIVE on westGate — first multi-composition (8 services).
biomeOS auto-discovered 1,704 capabilities. Provenance Trio CLOSED (sweetGrass G3
wired, v0.8.0). ZFS 25.4TB + 2TB L2ARC online, all 5 storage tiers operational.
6 PDB protein structures in CAS. P0 glibc FIXED (cellMembrane). P1 WG DNS FIXED.
songBird mesh refactor. NEW P0: biomeOS BTSP session propagation in signal graph
executor — composition broker pattern needed for inter-primal trust. 27 signal
graphs. ~72K+ tests. AlphaFold ~1TB ingestion pipeline ready after BTSP broker.*
