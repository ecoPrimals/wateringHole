# ecoPrimals Ecosystem Blurb — Wave 155b

**Date**: Jul 27, 2026 | **Wave**: 155b | **From**: eastGate overwatch
**Posture**: **genomeBin CONVERGENCE — tracks converged, glacial goals set, all teams unified.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are" and "Your Team" sections. Everything else is reference.

---

## WHERE WE ARE

The ecosystem is **consolidated**. Tower Atomic, BTSP 13/13, autonomous enrollment,
and depot convergence are all **fossilized** (10 dimensions, F1-F10). Tracks A
(evolution) and B (fleet convergence) are now **converged** — the next work is
proving the stack works cross-platform while evolving the data layer.

| Metric | Value |
|--------|-------|
| Primal tests | **75,199** |
| Scenarios | 197, all PASS |
| BTSP | **13/13** |
| genomeBin Tier 1 | **5 targets** (Linux x86+ARM, Windows, Android, ARM IoT) |
| Depot | golgiBody sole depot — all genomeBins via Caddy TLS |
| Gates ONLINE | **7** (spore, east, iron, flock, golgi, graphene, north) |
| Gates HW READY | **5** (strand, west, blue[Win], swift[Win], south) |
| Fossilized | **10 dimensions** |
| Active dimensions | **9** (incl. new Dim 8: genomeBin / cross-platform) |

---

## GLACIAL GOALS

Gates are on, wired, and running. The validation target is the software
abstraction, not the hardware:

| # | Goal | What It Proves | Owner |
|---|------|---------------|-------|
| G1 | Tower Atomic on Windows | OS abstraction (IPC, service mgmt, paths) | songBird + cellMembrane |
| G2 | Tower Atomic on Android | Mobile trust boundary | bearDog + songBird |
| G3 | Nest Atomic Phase 0 | Cross-platform content-addressed storage | nestGate + provenance trio |
| G4 | Nest Atomic cross-platform | Agnostic data systems (ZFS, NTFS, ext4) | nestGate + cellMembrane |
| G5 | Chimera Phase 0 | `libtower.so` shared library extraction | bearDog + songBird |
| G6 | bearDog public flip | crates.io sovereignty | bearDog |
| G7 | Gate enmeshment (5 gates) | postPrimordial deployment pipeline | cellMembrane + all |
| G8 | Plasmodium | Multi-gate bonded compute | biomeOS |
| G9 | JOSS publication | Gonzales NF live system paper | projectFoundation |

---

## CODE TEAMS — PRIMAL STATUS + NEXT WORK

### Tower Atomic (bearDog + songBird + skunkBat)

The OS abstraction layer. Every gate runs Tower. Windows + Android proof is
the active frontier.

| Primal | Version | Tests | Status | Next Work |
|--------|---------|-------|--------|-----------|
| **bearDog** | 0.9.0 | 11,993 | SHIPPED | G5: Chimera extraction (`beardog-core` crate). G6: public flip (final audit). FIDO2 + beacon + HSM agnostic all done. |
| **songBird** | 0.2.1 | 10,335 | SHIPPED | G1: Windows named pipe IPC validation. `universal-ipc` has the code — needs live testing on blueGate. `mesh.gate_enroll` live on golgiBody. |
| **skunkBat** | 0.2.18 | — | PUBLIC | Stable. Spawn-rate anomaly detection, cipher floor. No active work unless regression. |

**Code context**: songBird's `universal-ipc` module already handles UDS (Linux),
named pipes (Windows), abstract sockets (Android), XPC (iOS), TCP (fallback).
The `Platform::detect()` in cellMembrane's `arch.rs` gives `TargetOs × CpuArch × LinkModel`.
These are the two pieces that make G1 work — the code exists, it needs live validation.

### Provenance Trio (rhizoCrypt + loamSpine + sweetGrass)

The memory layer. Nest Atomic depends on these three plus nestGate.

| Primal | Version | Status | Next Work |
|--------|---------|--------|-----------|
| **rhizoCrypt** | 0.14.17 | Stable | G3: Wire BTSP into DAG operations. Cross-repo provenance for multi-gate. |
| **loamSpine** | 0.9.16 | Stable | G3: Loam Certificate minting validation via primalSpring. |
| **sweetGrass** | 0.7.63 | Stable | G3: Attribution braids for cross-gate provenance chains. |

### Compute Triangle (toadStool + barraCuda + coralReef)

Hardware-aware compute. Relevant for strandGate (HPC) and GPU workloads.

| Primal | Version | Tests | Next Work |
|--------|---------|-------|-----------|
| **toadStool** | 0.2.0 | 17,614 | Cross-platform hardware discovery (Windows GPU probing). |
| **barraCuda** | 0.4.0 | — | Stable. 712+ WGSL f64 shaders. No active work. |
| **coralReef** | 0.2.0 | — | Stable. Shader compilation. Windows Vulkan path. |

### Data + Orchestration

| Primal | Version | Tests | Next Work |
|--------|---------|-------|-----------|
| **nestGate** | 0.5.0 | 9,617 | G3: BTSP ClientHello integration (shipped but needs wiring into CAS call sites). G4: cross-platform CAS (Windows paths, NTFS considerations). ZFS CAS backend for westGate. |
| **biomeOS** | 0.1.0 | — | G8: Plasmodium multi-gate bonding. Deploy graph execution cross-platform. |
| **squirrel** | 0.1.0 | — | AI coordination layer. Stable, evolves with NUCLEUS. |
| **petalTongue** | 1.7.0 | 5,812 | Stable. WASM/WebGL shipped. BTSP ClientHello shipped. |
| **sourDough** | 0.4.0 | — | Scaffolding tool. Stable. |
| **bingoCube** | 0.1.1 | — | Crypto commitment tool. Stable. |

### cellMembrane (gardens/)

| Component | Version | Next Work |
|-----------|---------|-----------|
| **membrane-shadow** | 0.1.0 | `nucleus.rs` needs Windows Service + launchd + init paths (currently systemd-only). Checksum verify fix shipped. gate.bootstrap cross-platform. |
| **cellmembrane-types** | 0.1.0 | `GateProfile` target/bind_mode fields transitional — primals auto-detect. |

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1

| Gate | Platform | Composition | Current State | Next Work |
|------|----------|-------------|---------------|-----------|
| **sporeGate** | Linux | full | ONLINE. Build authority, cascade hub | Harvest Windows genomeBins (`--target x86_64-pc-windows-gnu`). Push to golgiBody depot. Foreman for blueGate builder. |
| **eastGate** | Linux | full | ONLINE. Code hub, overwatch | Coordination. Track validation across gate teams. bearDog public flip. |
| **northGate** | Windows | full | ONLINE. RTX 5090, WG mesh | G1 validation target — Tower Atomic on Windows already running via WG. Can validate songBird named pipe IPC. |

### House 2 (641 Samantha) — Omada + Flint2

| Gate | Platform | Composition | Current State | Next Work |
|------|----------|-------------|---------------|-----------|
| **ironGate** | Linux | full | ONLINE. 4x HDD (14TB+1TB+1TB+~2TB) | HDD enclave model: LUKS per-disk encrypted compartments. JupyterHub live. GPU compute. Data systems experimentation. |
| **strandGate** | Linux | compute (7) | HW READY. Dual EPYC 7452, 256GB, RTX 3090 | Enroll → Tower Atomic → GPU/HPC workloads. Bioinformatics compute workhouse. NF pipeline target. |
| **westGate** | Linux | nest (7) | HW READY. 5x14TB HDD (70TB raw) | Enroll → Tower Atomic → NestGate CAS. ZFS cold pool for ecosystem archive + NAS. |
| **blueGate** | Windows | tower (3) | HW READY. Flint2 2.5G | Enroll (`gate-enroll.ps1`) → Tower on Windows → distributed builder under sporeGate foreman. Media/gaming. G1 proof. |
| **swiftGate** | Windows | full (13) | HW READY. Flint2 2.5G | Enroll (`gate-enroll.ps1`) → Full NUCLEUS on Windows. Hobby/consumer — house2 northGate equivalent. |
| **southGate** | Linux | full (13) | HW READY. Omada 10G | Enroll → Full NUCLEUS → second sovereign site. Hub candidate. |

### Remote / Mobile

| Gate | Platform | Status | Next Work |
|------|----------|--------|-----------|
| **golgiBody** | Linux (VPS) | ONLINE | Sole depot. Enrollment endpoint live. Serve Windows genomeBins once sporeGate harvests. |
| **flockGate** | Linux | ONLINE | Nest Atomic Phase 0 validation. nestGate BTSP wiring. |
| **grapheneGate** | Android | ONLINE | G2: Tower → full NUCLEUS on Android. HSM validation from eastGate first. |

### Offline

| Gate | Issue |
|------|-------|
| fieldGate | Dead CMOS |
| biomeGate | Kernel recovery |

---

## ENROLLMENT PIPELINE (for HW READY gates)

Every HW READY gate follows the same path:

1. **Enroll**: `gate-enroll.sh` (Linux) or `gate-enroll.ps1` (Windows) with hub + token
2. **Mesh**: WG peer registered, Forgejo SSH key created, family seed delivered
3. **Clone**: All 43+ repos from Forgejo over mesh
4. **Bootstrap**: `membrane gate.bootstrap <gate>` — fetches genomeBins from golgiBody for architecture
5. **Validate**: `primalSpring` scenarios pass
6. **Head**: Publish `wateringHole/heads/<gate>.toml`
7. **Online**: Gate receives wave updates via temporal cascade

Self-registration — gates declare name + composition. No manifest pre-definition.
golgiBody is the sole depot. No USB, no SCP, no local depots.

---

## WHAT'S FOSSILIZED (DON'T RE-CHECK)

| F# | What | Wave |
|----|------|------|
| F1 | Glacial Shift | 137b |
| F2 | Content-Addressed Convergence | 143b |
| F3 | Silicon Atheism → evolved into Dim 8 | 145a |
| F4 | Depot / Build Pipeline | 150n |
| F5 | Cascade Pipeline | 150k |
| F6 | Tower Atomic Deep Analysis | 150x |
| F7 | sporePrint Transplant | 150x |
| F8 | Tower Atomic Completion | 151a |
| F9 | BTSP + Publication Strategy | 151d |
| F10 | Autonomous Gate Enrollment | 155b |

10 handoffs from Wave 151b-152a in `fossilRecord/wave155b_btsp_enrollment/`.

---

## CROSS-CUTTING DEPENDENCIES

```
G7 (gate enmeshment)
 ├── G1 (Tower on Windows) ← songBird universal-ipc + cellMembrane nucleus.rs
 │    └── blueGate + swiftGate enrollment
 ├── G2 (Tower on Android) ← bearDog HSM + songBird
 │    └── grapheneGate full NUCLEUS
 ├── G3 (Nest Atomic Phase 0) ← nestGate + provenance trio
 │    └── flockGate validation
 ├── G4 (Nest cross-platform) ← nestGate + cellMembrane
 │    └── westGate ZFS CAS
 └── sporeGate Windows genomeBin harvest → golgiBody depot

G5 (Chimera) ← G1 proven (Tower composition validated cross-platform)
G6 (bearDog public) ← final audit (independent)
G8 (Plasmodium) ← G7 (multiple gates enmeshed)
G9 (JOSS) ← G3 + wetSpring (independent research track)
```

---

## REFERENCE FILES

| File | What |
|------|------|
| `wateringHole/ORTHOGONAL_DIMENSIONS_REVIEW.md` | Full 9-dimension + 10-fossil review |
| `wateringHole/GLOSSARY.md` | Terminology (refreshed Wave 155b) |
| `wateringHole/ecosystem_manifest.toml` | Gate profiles, compositions, build metadata |
| `wateringHole/TOPOLOGY_MAP.toml` | Network topology, latency matrix, affinity |
| `wateringHole/wave.toml` | Current wave coordination |
| `plasmidBin/manifest.toml` | genomeBin target matrix, primal registry |
| `plasmidBin/enroll/gate-enroll.sh` | Linux enrollment script |
| `plasmidBin/enroll/gate-enroll.ps1` | Windows enrollment script |
| `plasmidBin/profiles/tower-builder.toml` | Builder node profile |
| `cellMembrane/crates/membrane-shadow/src/gate/` | gate.enroll, gate.bootstrap, verify |
| `songBird/crates/songbird-universal-ipc/` | Cross-platform IPC layer |

---

## SPOREPRINT — Wave 155b

**Wave 155b transplant shipped.** 10 files, 154 insertions, 106 deletions.

- Entity registry updated: bearDog 11,993, songBird 10,335, nestGate 9,617,
  toadStool 17,614, petalTongue 5,812. Total 93,700 tests
- Tower Atomic: BTSP 13/13, genomeBin 5 targets, autonomous enrollment (F10),
  glacial goals G1/G2/G5 documented
- Gate mesh: 7 online + 5 HW ready gate table across tower_atomic, living-systems,
  MESH_TOPOLOGY
- Title templates specialized: `Page Title | ecoPrimals` (only homepage has full keywords)
- Sidebar compressed: 40+ page sections show subsections only
- Canonical host fully consolidated (Caddy 301 confirmed live 150d)

**Divergence**: Blurb says primal_tests=75,199 but individual counts only
updated for 5/15 primals. Entity sum is 82,124. Need `spore-validate refresh`.

---

*Wave 155b: 313 pages, 0 errors. Tracks converged. Ecosystem consolidated.
The frontier is cross-platform proof: Tower on Windows, Nest Atomic, Chimera.*
