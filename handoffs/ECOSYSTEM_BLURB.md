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
| J8 | Key enrollment portal | **CODE SHIPPED** — step-ca lifecycle. Deployment pending on golgiBody | cellMembrane + songBird |

---

## CODE TEAMS — PRIMAL STATUS + GATE ASSIGNMENT

### eastGate — Overwatch + Orchestration

| Primal | Version | Role | Next Work |
|--------|---------|------|-----------|
| **biomeOS** | 0.1.0 | Signal graph orchestrator | `nest.ingest_dataset` shipped. Live `tower.health` validation on westGate + strandGate. |
| **primalSpring** | — | Scenario validation | Calibrate for distributed gate topology. |
| **bearDog** | 0.9.0 | Trust foundation | ACME Phase 2 client (songBird needs it). G6 audit. |
| **songBird** | 0.2.1 | Discovery + IPC | ACME shipped. bearDog Phase 2 blocked. Deep debt landed. |
| **skunkBat** | 0.2.18 | Defense | Monitor gate migrations. |
| **cellMembrane** | — | Deployment fabric | **J6 CLOSED.** J8 code shipped. **P0 glibc FIXED. P1 WG DNS FIXED.** step-ca on golgiBody pending. |

### westGate — Nest Atomic + Data (CODE TEAMS DELIVERED)

| Primal | Version | Tests | Latest |
|--------|---------|-------|--------|
| **petalTongue** | 1.7.0 | 6,605 | Topology architecture, runtime manifest, geometry split |
| **squirrel** | 0.1.0 | 763 | Capability purification, adapter IPC |
| **nestGate** | 0.5.0 | 12,973 | P0/P1 closed, live CLI, ZFS tier migration |
| **loamSpine** | 0.9.16 | 1,739 | BTSP handshake dedup. **155i**: registry drift fixed — `certificate.verify/lifecycle/history` discoverable |
| **rhizoCrypt** | 0.14.17 | 1,456 | (no new evolution this wave) |
| **sweetGrass** | **0.8.0** | **1,625** | **G3 wiring COMPLETE** — `LedgerClient`, `braid.commit` → loamSpine, ledger proof. Provenance Trio CLOSED |

westGate **NEST ATOMIC LIVE** — 8 services deployed, Provenance Trio CLOSED.
ZFS 25.4TB + 2TB L2ARC online. All 5 storage tiers operational. 6 PDBs in CAS. Next:
- **biomeOS BTSP composition broker** — signal graph executor needs BTSP propagation
- **E2E Nest Atomic signal graph validation** — with BTSP working end-to-end
- **AlphaFold bulk ingestion** → ~1TB from northGate through full pipeline

### strandGate — Compute Trio (DEPLOYED)

| Primal | Version | Tests | Latest |
|--------|---------|-------|--------|
| **toadStool** | 0.2.0 | 23,332 | S344 deny.toml, overstep reduction |
| **barraCuda** | 0.4.0 | 4,957 | SIGSEGV fix, BTSP env races, dead code (-1,200L) |
| **coralReef** | 0.2.0 | 3,527 | 18/18 dispatch, BTSP Phase 3 encrypted transport |

strandGate Tower LIVE + Compute Trio deployed. **P0 glibc RESOLVED** —
cellMembrane `targets_for_primal()` now auto-appends gnu for GPU primals.
Rebuild depot binaries on sporeGate to produce glibc genomeBins.

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1 (peptidoglycan anchor: sporeGate)

| Gate | Status | Teams | Next Work |
|------|--------|-------|-----------|
| **sporeGate** | ONLINE | Build authority | **P0**: Add glibc depot target for GPU primals. step-ca deploy. |
| **eastGate** | ONLINE | Overwatch | Coordinate. bearDog ACME Phase 2. |
| **northGate** | DEGRADED | — | Fix RustDesk. G1 Tower validation. |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | Teams | Next Work |
|------|--------|-------|-----------|
| **strandGate** | **TOWER+COMPUTE LIVE** | Compute trio | Await glibc depot. Profile RTX 3090. |
| **westGate** | **NEST ATOMIC LIVE** | Nest + data | biomeOS BTSP broker needed. E2E signal graph validation. AlphaFold ingestion. |
| **blueGate** | ONLINE (Windows) | — | Peptidoglycan anchor H2. G1 proof. |
| **ironGate** | DEGRADED (RustDesk) | — | Fix RustDesk. HDD enclave. |
| **swiftGate** | ONLINE (Windows) | — | Tower on Windows. |
| **southGate** | HW READY | — | Enroll → Tower → NUCLEUS. |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner |
|---|----------|-------|-------|
| 1 | **P0** | biomeOS BTSP session propagation in signal graph executor | biomeOS |
| 2 | **P0** | biomeOS riboCipher transport framing in CLI paths | biomeOS |
| 3 | P1 | Rebuild membrane depot binary with gate.configure/gate.apply | cellMembrane/sporeGate |
| 4 | P1 | Deploy step-ca on golgiBody (J8 deployment) | sporeGate ops |
| 5 | P1 | toadStool deployment model docs (no `server` subcommand) | toadStool |
| 6 | P1 | hotSpring Forgejo pack corruption | eastGate admin |
| 7 | P1 | nestGate ghost methods `content.repo.*`/`content.mirror.*` | nestGate |

**Resolved this wave**: ~~P0 glibc depot~~ FIXED. ~~P1 WG DNS~~ FIXED. ~~P1 ZFS pool~~ ONLINE.

---

## HANDOFFS (newest first)

| File | Status |
|------|--------|
| `BIOMEOS_TOWER_ATOMIC_COMPOSITION_BROKER_WAVE155i.md` | **biomeOS BTSP composition broker (NEW P0)** |
| `SWEETGRASS_G3_WIRING_COMPLETE_WAVE155i.md` | **sweetGrass G3 COMPLETE — Provenance Trio CLOSED** |
| `CELLMEMBRANE_WAVE155i_GLIBC_DEPOT_WG_DNS.md` | **P0 glibc FIXED + P1 WG DNS FIXED** |
| `TOWER_ATOMIC_VALIDATION_WAVE155i.md` | Tower health validation — all gates |
| `NEST_ATOMIC_ALPHAFOLD_WAVE155i.md` | Nest Atomic pipeline + AlphaFold ingestion plan |
| `SWEETGRASS_NEST_ATOMIC_G3_WIRING_WAVE155i.md` | sweetGrass G3 wiring handoff (completed) |
| `SQUIRREL_WESTGATE_CODE_TEAM_AUDIT_WAVE155g.md` | Audit: 763 tests, clean |
| `PETALTONGUE_WESTGATE_EVOLUTION_WAVE155g.md` | Topology architecture evolution |
| `PETALTONGUE_WESTGATE_CODE_TEAM_AUDIT_WAVE155g.md` | Audit: 6,558 tests |
| `NESTGATE_WESTGATE_CODE_TEAM_EXECUTION_WAVE155g.md` | P0/P1 resolved |
| `NESTGATE_WESTGATE_CODE_TEAM_AUDIT_WAVE155g.md` | Audit: 12,973 tests |
| `CORALREEF_WAVE155f_STRANDGATE_EXECUTION_JUL28_2026.md` | 18/18 dispatch, all P0 fixed |
| `CORALREEF_WAVE155f_STRANDGATE_AUDIT_JUL28_2026.md` | 10 compile errors found |
| `BARRACUDA_WAVE155f_STRANDGATE_DEEP_DEBT_JUL28_2026.md` | SIGSEGV + env races |
| `CELLMEMBRANE_WAVE155f_J8_KEY_PORTAL.md` | step-ca SSH cert lifecycle |
| `CELLMEMBRANE_WAVE155f_J6_COMPLETION.md` | gate.configure/gate.apply |
| `SPOREGATE_J8_STEP_CA_DEPLOYMENT.md` | step-ca deployment guide |

AARs:
- `WESTGATE_NEST_ATOMIC_MULTICOMP_155i_AAR.md` — **First multi-composition deployment. 8 services, 1,704 capabilities. BTSP boundary gap identified.**
- `WESTGATE_ZFS_POOL_CREATION_155i_AAR.md` — **ZFS 25.4TB + L2ARC online, all 5 tiers**
- `SPOREGATE_DEPLOYMENT_OPS_155h_AAR.md` — P0 glibc + step-ca + depot + firewall
- `STRANDGATE_COMPUTE_TRIO_DEPLOYMENT_155f_AAR.md` — Tower + Compute deployed
- `WESTGATE_TOWER_ATOMIC_DEPLOYMENT_155f_AAR.md` — Tower LIVE in 70 min
- `WESTGATE_ENROLLMENT_WAVE155f_AAR.md` — Hardware corrected

---

*Wave 155i. Nest Atomic LIVE on westGate — first multi-composition (8 services).
biomeOS auto-discovered 1,704 capabilities. Provenance Trio CLOSED (sweetGrass G3
wired, v0.8.0). ZFS 25.4TB + 2TB L2ARC online, all 5 storage tiers operational.
6 PDB protein structures in CAS. P0 glibc FIXED (cellMembrane). P1 WG DNS FIXED.
songBird mesh refactor. NEW P0: biomeOS BTSP session propagation in signal graph
executor — composition broker pattern needed for inter-primal trust. 27 signal
graphs. ~72K+ tests. AlphaFold ~1TB ingestion pipeline ready after BTSP broker.*
