# ecoPrimals Ecosystem Blurb — Wave 155b

**Date**: Jul 27, 2026 12:52 EDT | **Wave**: 155b | **From**: eastGate overwatch
**Posture**: **genomeBin CONVERGENCE — code teams evolved, jelly strings identified, cross-platform proof underway.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find "Your Team", act on your next work.

---

## WHERE WE ARE

Tracks A + B **converged**. 10 dimensions fossilized (F1-F10). Code teams
responded to the Wave 155b blurb with evolution across 7 primals + cellMembrane.
sporeGate AAR identifies 7 jelly strings in the deployment pipeline — the
harvest/push/deploy chain is still shell scripts. That's the evolution frontier.

| Metric | Value |
|--------|-------|
| Primal tests | **~78K** (rhizoCrypt +10, toadStool 9,232, loamSpine 1,732) |
| Scenarios | 197, all PASS (primalSpring calibrated for 13-gate mesh) |
| BTSP | **13/13** |
| genomeBin depot | **39 binaries** (13 primals × 3 targets) on golgiBody |
| Depot targets | x86_64-linux-musl + aarch64-linux-musl + **x86_64-windows-gnu** |
| Gates ONLINE | **7** |
| Gates HW READY | **5** |
| Tower shadow | 24 new benchmark samples today (3 gates × 4 paths × 2 modes) |

---

## WHAT TEAMS SHIPPED THIS WAVE

| Team | Evolution | Commit |
|------|-----------|--------|
| **songBird** | G1: First-class Windows named pipe IPC — `TransportEndpoint::NamedPipe` + `IpcStream::NamedPipe`. GateEnroll dispatch + drawbridge body-method fallback | `7e3517c8`, `c4c5d2d2` |
| **rhizoCrypt** | G3: BTSP→DAG auth bridge — `ConnectionOrigin::BtspAuthenticated`. Federate hardening — source gate provenance, signature verification. 1,893 tests (+10) | `d4972b0` |
| **nestGate** | G3: BTSP→CAS wiring + G4 cross-platform paths. Deep debt: capability probe, orphan cleanup, dep hygiene | `d0921a2b`, `9138068f` |
| **loamSpine** | G3: Full certificate lifecycle E2E with seal. 6 dead-code stubs realigned to Nest Atomic Phase 0. 1,732 tests | `d1b1594` |
| **toadStool** | S342: wgpu cross-platform GPU fallback (DX12/Vulkan/Metal). Doctor GPU check fix (Windows/macOS). SAFETY docs on MMIO ops. 9,232 tests | `64f661674` |
| **skunkBat** | Refactor: frame crypto extracted from negotiate.rs into frame.rs | `578136c` |
| **coralReef** | Test extraction: encoding.rs + op_misc modules separated | `40ea5b1` |
| **cellMembrane** | G1: `InitSystem` dispatch — systemd/launchd/windows-service/bare process manager. 513 insertions | `cbadae4` |
| **primalSpring** | Gate count calibrated for 13-gate mesh + sporePrint known debt fix | `05e72e46` |
| **sporeGate** | AAR: 39 binaries (3 targets) harvested + pushed to golgiBody. 7 jelly strings triaged (J1-J7) | deployment |

---

## GLACIAL GOALS — UPDATED STATUS

| # | Goal | Status | What Landed This Wave |
|---|------|--------|----------------------|
| G1 | Tower on Windows | **IN PROGRESS** | songBird named pipes shipped. cellMembrane InitSystem dispatch shipped. toadStool wgpu GPU fallback shipped. |
| G2 | Tower on Android | PENDING | — |
| G3 | Nest Atomic Phase 0 | **IN PROGRESS** | rhizoCrypt BTSP→DAG bridge. loamSpine lifecycle E2E. nestGate BTSP→CAS wiring. |
| G4 | Nest cross-platform | **IN PROGRESS** | nestGate cross-platform paths. rhizoCrypt federate hardening. |
| G5 | Chimera Phase 0 | PENDING (blocked on G1 proof) | — |
| G6 | bearDog public | READY (final audit) | — |
| G7 | Gate enmeshment | **IN PROGRESS** | 39 binaries on golgiBody depot. Enrollment endpoint live. |
| G8 | Plasmodium | PENDING (blocked on G7) | — |
| G9 | JOSS publication | PENDING | — |

---

## JELLY STRINGS — DEPLOYMENT EVOLUTION PRIORITY

From sporeGate AAR. These block the transition from "operator runs shell
loops" to "gates self-heal via cascade":

| # | What | Impact | Owner | Priority |
|---|------|--------|-------|----------|
| J1 | Harvest is shell loops | Blocks distributed building | cellMembrane | **P0** |
| J2 | Depot push is rsync | No integrity verify, no atomic swap | cellMembrane | **P1** |
| J3 | Service restart is manual | Blocks cascade-driven deployment | cellMembrane + songBird | **P1** |
| J4 | Caddy config is manual | Blocks self-configuring routes | songBird | **P2** |
| J5 | WG peer reg is ssh+wg set | Already coded, needs live test | songBird | **P2** |
| J6 | systemd overrides manual | Blocks cross-platform service config | cellMembrane | **P2** |
| J7 | Legacy service detection | One-time, low recurrence | cellMembrane | **P3** |

**Convergence path**: J1 (Rust harvest command) → J2 (Rust depot push) → J3 (auto hot-swap) → self-healing cascade.

---

## CODE TEAMS — PRIMAL STATUS + NEXT WORK

### Tower Atomic

| Primal | Version | Tests | This Wave | Next Work |
|--------|---------|-------|-----------|-----------|
| **bearDog** | 0.9.0 | 11,993 | — | G5: `beardog-core` crate extraction. G6: public flip audit. |
| **songBird** | 0.2.1 | 10,335 | Named pipe IPC, GateEnroll dispatch | G1: Live test named pipes on blueGate/northGate. J4: native TLS (replace Caddy). J5: live enrollment validation. |
| **skunkBat** | 0.2.18 | — | Frame crypto extraction | Stable. No active work. |

### Provenance Trio + Nest Atomic

| Primal | Version | Tests | This Wave | Next Work |
|--------|---------|-------|-----------|-----------|
| **nestGate** | 0.5.0 | 9,617 | BTSP→CAS wiring, cross-platform paths, dep hygiene | G3: Wire `connect_with_btsp` into priority CAS call sites. G4: Windows path handling (NTFS vs ext4). |
| **rhizoCrypt** | 0.14.17 | 1,893 | BTSP→DAG bridge, federate hardening | G3: Cross-gate provenance chain with loamSpine+sweetGrass. |
| **loamSpine** | 0.9.16 | 1,732 | Lifecycle E2E with seal, dead-code alignment | G3: MintingAuthority validation path. Coordinate with primalSpring for scenarios. |
| **sweetGrass** | 0.7.63 | — | — | G3: Attribution braids for cross-gate provenance chains. Wire with rhizoCrypt federate. |

### Compute Triangle

| Primal | Version | Tests | This Wave | Next Work |
|--------|---------|-------|-----------|-----------|
| **toadStool** | 0.2.0 | 9,232 | wgpu GPU fallback, doctor fix, SAFETY docs | Windows-native enrichment: WMI `Win32_VideoController`, DXGI adapter enum. |
| **barraCuda** | 0.4.0 | — | — | Stable. |
| **coralReef** | 0.2.0 | — | Test extraction | Stable. Windows Vulkan path if needed. |

### Data + Orchestration

| Primal | Version | Tests | Next Work |
|--------|---------|-------|-----------|
| **biomeOS** | 0.1.0 | — | G8: Plasmodium multi-gate bonding (after G7). |
| **squirrel** | 0.1.0 | — | Stable. Evolves with NUCLEUS. |
| **petalTongue** | 1.7.0 | 5,812 | Stable. |

### cellMembrane

| Component | This Wave | Next Work |
|-----------|-----------|-----------|
| **membrane-shadow** | `InitSystem` dispatch (systemd/launchd/windows-service/bare) | **J1**: `plasmid.harvest` Rust command. **J2**: `plasmid.push` Rust command. **J3**: `deploy.hot-swap`. Gate service config from profile TOML. |

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1

| Gate | Status | Next Work |
|------|--------|-----------|
| **sporeGate** | ONLINE. 39 binaries × 3 targets harvested | J1: codify harvest loop into `membrane plasmid.harvest`. Foreman for blueGate. |
| **eastGate** | ONLINE. Overwatch | Coordination. bearDog public flip. Cargo.toml metadata cascade (8 primals done). |
| **northGate** | ONLINE. Windows, WG mesh | G1 validation: test songBird named pipe IPC live. Test Tower Atomic services on Windows. |

### House 2

| Gate | Status | Next Work |
|------|--------|-----------|
| **ironGate** | ONLINE. 4x HDD | HDD enclave model (LUKS per-disk). JupyterHub live. |
| **strandGate** | HW READY | Enroll → Tower → compute workloads (bioinformatics, NF pipeline). |
| **westGate** | HW READY | Enroll → Tower → Nest Atomic → ZFS CAS cold pool. |
| **blueGate** | HW READY (Windows) | Enroll (`gate-enroll.ps1`) → Tower on Windows → distributed builder. G1 proof. |
| **swiftGate** | HW READY (Windows) | Enroll (`gate-enroll.ps1`) → Full NUCLEUS on Windows. |
| **southGate** | HW READY | Enroll → Full NUCLEUS → second sovereign site. |

### Remote / Mobile

| Gate | Status | Next Work |
|------|--------|-----------|
| **golgiBody** | ONLINE. 39 binaries in depot | Serve genomeBins. Enrollment endpoint live. |
| **flockGate** | ONLINE | G3: Nest Atomic Phase 0 validation (nestGate + provenance trio). |
| **grapheneGate** | ONLINE | G2: Tower → full NUCLEUS on Android (after G1 proven). |

---

## CROSS-CUTTING DEPENDENCIES

```
G7 (gate enmeshment) — 39 binaries on depot, enrollment live
 ├── G1 (Tower on Windows) — songBird pipes SHIPPED, cellMembrane InitSystem SHIPPED
 │    ├── blueGate + swiftGate enrollment
 │    └── northGate live validation
 ├── G3 (Nest Atomic Phase 0) — rhizoCrypt BTSP bridge SHIPPED, nestGate CAS wiring SHIPPED
 │    ├── loamSpine lifecycle E2E SHIPPED
 │    └── flockGate validation
 ├── G4 (Nest cross-platform) — nestGate paths SHIPPED
 │    └── westGate ZFS CAS
 └── J1 (harvest command) → J2 (depot push) → J3 (auto hot-swap) → self-healing cascade

G5 (Chimera) ← G1 proven
G6 (bearDog public) ← independent (ready)
G8 (Plasmodium) ← G7 complete
```

---

## REMAINING HANDOFFS (active in handoffs/)

| File | Scope | Status |
|------|-------|--------|
| `ECOSYSTEM_BLURB.md` | This document — universal handoff | CURRENT |
| `BLURB_TRACK_A_EVOLUTION.md` | Nest Atomic + Chimera scope reference | CONVERGED |
| `BLURB_TRACK_B_FLEET_CONVERGENCE.md` | Enrollment phases reference | CONVERGED |
| `BLURB_SPOREGATE_BUILD_MESH.md` | Build mesh + harvest topology | CURRENT |
| `LOAMSPINE_WAVE155B_G3_READINESS_JUL27_2026.md` | G3 readiness detail | NEW |
| `RHIZOCRYPT_WAVE155B_BTSP_DAG_BRIDGE_JUL27_2026.md` | BTSP→DAG bridge detail | NEW |
| `TOADSTOOL_S342_CROSS_PLATFORM_GPU_JUL27_2026.md` | Cross-platform GPU detail | NEW |
| `ABG_JUPYTERHUB_ACCESS_GUIDE.md` | Operational reference | STATIC |
| `LIVE_FRONTEND_E2E_TUTORIAL_STANDARD.md` | Operational standard | STATIC |
| `TEAM_STARTUP_BLURB_TEMPLATE.md` | Template | STATIC |

AAR in `aars/`:
| File | Scope |
|------|-------|
| `SPOREGATE_DEPLOYMENT_EVOLUTION_155b_AAR.md` | Jelly string triage + isomorphic target |

---

*Wave 155b. Code teams accelerated: G1 (Tower on Windows) has 3 shipped components,
G3 (Nest Atomic) has 3 shipped components, toadStool cross-platform GPU live.
sporeGate depot has 39 binaries across 3 targets. 7 jelly strings triaged —
J1 (Rust harvest) is the P0 that unblocks distributed building and cascade
automation. The system is at the inflection point: primitives exist, orchestration
needs codification.*
