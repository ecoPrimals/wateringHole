# ecoPrimals Ecosystem Blurb — Wave 155i

**Date**: Jul 29, 2026 07:50 EDT | **Wave**: 155i | **From**: eastGate overwatch
**Posture**: **NEST ATOMIC PIPELINE WIRING. loamSpine registry drift fixed. biomeOS `nest.ingest_dataset` signal graph shipped. sweetGrass G3 wiring handoff issued. AlphaFold ~1TB ingestion pipeline designed: northGate → westGate CAS with full Provenance Trio backtracking. Tower health validation target. P0: glibc depot target still open.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

**Posture**: Nest Atomic pipeline wiring begins. Deep evolution wave (155f-h)
landed — 9 primals shipped. Now pivoting from Tower Atomic validation to Nest
Atomic stand-up on westGate. loamSpine registry drift fixed (`certificate.verify`
discoverable). biomeOS `nest.ingest_dataset` signal graph created. sweetGrass G3
wiring handoff issued to close the Provenance Trio triangle. First data target:
~1TB AlphaFold protein structures from northGate.

**P0 OPEN**: musl genomeBins cannot `dlopen` glibc Vulkan ICD — compute primals
(barraCuda, coralReef, toadStool) need `x86_64-unknown-linux-gnu` depot target
for GPU workloads. sporeGate build team action.

**Gate-Team Assignments**:

| Gate | Teams / Primals | Status |
|------|-----------------|--------|
| **eastGate** | Overwatch, primalSpring, biomeOS | Code hub. Coordination. |
| **westGate** | petalTongue, squirrel, nestGate, Provenance Trio | **Tower LIVE. Code teams delivered.** |
| **strandGate** | toadStool, barraCuda, coralReef | **Tower LIVE. Compute Trio deployed.** |

**Sequencing**:
1. **DONE**: westGate Tower Atomic + code team audits + execution
2. **DONE**: strandGate sync + Tower Atomic + Compute Trio deployment
3. **DONE**: loamSpine registry drift fixed (certificate.verify/lifecycle/history)
4. **DONE**: biomeOS `nest.ingest_dataset` signal graph created
5. **NOW**: sweetGrass G3 wiring — `braid.commit` → loamSpine (handoff issued)
6. **NOW**: Tower health validation on westGate + strandGate
7. **NOW**: P0 glibc depot target for GPU primals
8. **NOW**: westGate ZFS pool creation (5×14TB) → Nest Atomic CAS
9. **NEXT**: northGate Tower assessment → cross-gate AlphaFold federation
10. **NEXT**: E2E Nest Atomic validation (small PDB test)
11. **NEXT**: Bulk AlphaFold ingestion (~1TB) through Nest Atomic pipeline

| Metric | Value |
|--------|-------|
| Signal graphs | **27** (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| Primal tests | **~70K+** (toadStool 23K, songBird 14K+, nestGate 13K, bearDog 12K, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K) |
| Jelly strings | **7/8 resolved** (J6 CLOSED, J7 low, J8 code shipped) |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 × 3 musl targets) — glibc target NEEDED |
| Gates ONLINE | **8** + strandGate Tower LIVE |
| Threat categories | **9** (skunkBat ConnectivityAnomaly) |

---

## WHAT CODE TEAMS SHIPPED (Wave 155f-h)

| Team | Latest Evolution | Key Commits |
|------|------------------|-------------|
| **songBird** | ACME HTTP-01 challenge responder, deep debt (fake metrics→errors), tower roundtrip tests | `305f5bee`, `0d6c0f55`, `c0096a17` |
| **cellMembrane** | **J6 CLOSED**: `gate.configure`/`gate.apply`. **J8 shipped**: SSH cert lifecycle via step-ca. 1,219 tests | `c66a56e`, `b13105b` |
| **barraCuda** | GPU SIGSEGV fix (`GPU_TEST_GUARD`), BTSP env races, ESN device crash, dead code removal (-1,200L). 4,957 tests | `042f1493` |
| **coralReef** | 10 compile errors fixed, 18/18 JSON-RPC dispatch complete, BTSP Phase 3 encrypted transport. 3,527 tests | `3d969f8` |
| **loamSpine** | BTSP handshake dedup: `verify_and_negotiate()` + `AsyncErrorSender`. 1,739 tests | `1ced08d` |
| **nestGate** | P0/P1 audit sweep: test compilation fixed, live CLI health probes, FHS path centralization, ZFS tier migration. 12,973 tests | `3ca3e1bc` |
| **petalTongue** | Topology → runtime `ecosystem_manifest.toml` loading. `main.rs` 727→199L split. Geometry module. 6,605 tests | `d60e67d` |
| **squirrel** | Capability purification: `beardog`→`security_provider`, local crypto→delegation, adapter IPC wired. 763 tests | `acbe09e3` |
| **toadStool** | S344: `deny.toml` expanded (Pure Rust Crypto), overstep reduction, socket centralization. 23,332 tests | `04fcb96e3` |

---

## GLACIAL GOALS — SEQUENCED

| # | Goal | Status | Gate |
|---|------|--------|------|
| G1 | Tower on Windows | **FRONTLOADED** | OPEN |
| G7 | Gate enmeshment | **ADVANCING** | westGate+strandGate Tower LIVE |
| G6 | bearDog public | READY | OPEN — songBird ACME Phase 1 unblocks TLS |
| G3 | Nest Atomic Phase 0 | **WIRING** | loamSpine registry fixed, signal graph created, sweetGrass G3 handoff issued, ZFS pool pending |
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
| **cellMembrane** | — | Deployment fabric | **J6 CLOSED.** J8 code shipped. step-ca deployment on golgiBody. |

### westGate — Nest Atomic + Data (CODE TEAMS DELIVERED)

| Primal | Version | Tests | Latest |
|--------|---------|-------|--------|
| **petalTongue** | 1.7.0 | 6,605 | Topology architecture, runtime manifest, geometry split |
| **squirrel** | 0.1.0 | 763 | Capability purification, adapter IPC |
| **nestGate** | 0.5.0 | 12,973 | P0/P1 closed, live CLI, ZFS tier migration |
| **loamSpine** | 0.9.16 | 1,739 | BTSP handshake dedup. **155i**: registry drift fixed — `certificate.verify/lifecycle/history` discoverable |
| **rhizoCrypt** | 0.14.17 | 1,456 | (no new evolution this wave) |
| **sweetGrass** | 0.7.64 | 1,676 | **G3 wiring handoff issued** — `braid.commit` → loamSpine, `anchoring.verify` ledger proof |

westGate Tower LIVE. Code teams have delivered audits + execution. Next:
- **sweetGrass G3 wiring** — close Provenance Trio triangle (handoff issued)
- **ZFS pool creation** (human) → Nest Atomic tiered CAS storage
- **E2E Nest Atomic validation** → small PDB ingestion test
- **AlphaFold bulk ingestion** → ~1TB from northGate through full pipeline

### strandGate — Compute Trio (DEPLOYED)

| Primal | Version | Tests | Latest |
|--------|---------|-------|--------|
| **toadStool** | 0.2.0 | 23,332 | S344 deny.toml, overstep reduction |
| **barraCuda** | 0.4.0 | 4,957 | SIGSEGV fix, BTSP env races, dead code (-1,200L) |
| **coralReef** | 0.2.0 | 3,527 | 18/18 dispatch, BTSP Phase 3 encrypted transport |

strandGate Tower LIVE + Compute Trio deployed. **P0 blocker**: musl genomeBins
can't `dlopen` glibc Vulkan ICD — source build works, depot binary doesn't.
Need `x86_64-unknown-linux-gnu` glibc target in depot pipeline.

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
| **westGate** | **TOWER LIVE** | Nest + data | ZFS pool → Nest Atomic. G3 wiring. |
| **blueGate** | ONLINE (Windows) | — | Peptidoglycan anchor H2. G1 proof. |
| **ironGate** | DEGRADED (RustDesk) | — | Fix RustDesk. HDD enclave. |
| **swiftGate** | ONLINE (Windows) | — | Tower on Windows. |
| **southGate** | HW READY | — | Enroll → Tower → NUCLEUS. |

---

## OPEN P0/P1 ROLLUP

| # | Priority | Issue | Owner |
|---|----------|-------|-------|
| 1 | **P0** | glibc depot target for compute primals (musl can't dlopen Vulkan) | sporeGate build |
| 2 | P1 | Deploy step-ca on golgiBody (J8 deployment) | sporeGate ops |
| 3 | P1 | toadStool deployment model docs (no `server` subcommand) | toadStool |
| 4 | P1 | hotSpring Forgejo pack corruption | eastGate admin |
| 5 | P1 | westGate ZFS pool creation (5×14TB) | westGate human |
| 6 | P1 | nestGate ghost methods `content.repo.*`/`content.mirror.*` | nestGate |
| 7 | P1 | WireGuard DNS catch-all in wg0 template | cellMembrane |

---

## HANDOFFS (newest first)

| File | Status |
|------|--------|
| `NEST_ATOMIC_ALPHAFOLD_WAVE155i.md` | **Nest Atomic pipeline + AlphaFold ingestion plan** |
| `SWEETGRASS_NEST_ATOMIC_G3_WIRING_WAVE155i.md` | **sweetGrass G3 wiring handoff** |
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
- `STRANDGATE_COMPUTE_TRIO_DEPLOYMENT_155f_AAR.md` — Tower + Compute deployed, P0 musl/glibc
- `WESTGATE_TOWER_ATOMIC_DEPLOYMENT_155f_AAR.md` — Tower LIVE in 70 min
- `WESTGATE_ENROLLMENT_WAVE155f_AAR.md` — Hardware corrected

---

*Wave 155i. Nest Atomic pipeline wiring begins. loamSpine registry drift fixed
(certificate.verify/lifecycle/history now discoverable). biomeOS nest.ingest_dataset
signal graph created (5-node pipeline: session → CAS → DAG → dehydrate → provenance).
sweetGrass G3 wiring handoff issued to close Provenance Trio triangle. AlphaFold
~1TB ingestion pipeline designed: northGate → westGate CAS with full backtracking.
Tower health validation queued for westGate + strandGate. westGate ZFS pool pending.
P0 glibc depot target still open. 27 signal graphs. ~70K+ tests.*
