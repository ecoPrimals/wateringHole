# ecoPrimals Ecosystem Blurb — Wave 143a

**Date**: Jul 16, 2026 09:35 EDT | **Wave**: 143a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. SILICON ATHEISM PHASE 2 IN MOTION.**

**This cascade**: Teams responded to Phase 2 FRAGO. **Windows 14/14 COMPLETE —
59 depot binaries** (confirmed). songBird shipped `IpcStream` platform
abstraction. petalTongue shipped Phase 2 metrics trait + Android paths + WS
bridge. skunkBat adopted `TransportEndpoint`. toadStool S332-S333: glowplug
Vulkan backend + 9,232 tests. coralReef: 3,650 tests. Deep debt across 8
primals. Manifest fixes (bind_mode/mobility enums). **RustDesk connectivity
transient to ironGate + flockGate**. 38/39 synced (wateringHole diverge resolved).

---

## Per-Primal Remaining Work

### petalTongue

| Work | Priority | Status |
|------|----------|--------|
| `petal-tongue-platform` — Phase 2 reference pattern | — | **SHIPPED** (`1af1a98`) |
| Phase 2: metrics trait + Android paths + WS bridge | — | **SHIPPED** (`470d7b5`) |
| Phase 2: `MeshTopologySource` abstraction + deep debt | — | **SHIPPED** (`337e1d0`) |
| footPrint composition: wire `WS_PATH` → agent bridge | P2 | TODO |

### toadStool

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 gating (`target_os = "linux"`) | — | **DONE** (S329) |
| glowplug `WgpuGpuDiscovery` Vulkan backend | P1 | **DONE** (S332) |
| glowplug `PortableSwapExecutor` compute backend | P1 | **DONE** (S332) |
| ember `PortableResourceHandle` GPU handle abstraction | P2 | **DONE** (S332) |
| Structural debt: 7 files refactored, primal name cleanup | — | **DONE** (S333) |
| Deep debt: S329-S333 (clone elim, borrowed deser, test extraction, +57 tests) | — | **DONE** |

### bearDog

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 IPC gating + libc removal | — | **DONE** (`5d4258d`) |
| HSM provider → Android Keystore backend | P2 | NEW |
| HSM provider → Windows DPAPI backend | P2 | NEW |
| Deep debt: BTreeMap batch 4, test extraction wave 2 | — | **DONE** |

### squirrel

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 Windows harvest unblock | — | **DONE** (`110c9939`) |
| Credential store → Android Keystore backend | P2 | NEW |
| Credential store → Windows Credential Manager backend | P2 | NEW |
| Transport: raw UDS → `TransportEndpoint` trait | P2 | Phase 2 |

### sourDough

| Work | Priority | Status |
|------|----------|--------|
| Android platform parity (Os::Android + LibC::Bionic) | — | **DONE** (`6115e4a`) |
| All 3 cross-targets green, 490 tests | — | **DONE** |
| Full genomeBin standard | — | **COMPLETE** |

### songBird

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 reference implementation | — | **DONE** |
| `IpcStream` platform abstraction (Phase 2 transport) | — | **SHIPPED** (`12099d84`) |
| `drawbridge_auth` extraction | — | **SHIPPED** (`12099d84`) |
| footPrint drawbridge wiring (`PROXY_PATH`) | P2 | TODO |
| tideGlass drawbridge bonds (LINCS, GEO, ChEMBL, NF) | P2 | TODO |

### nestGate

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch (Session 109) | — | **DONE** |
| Sessions 112-113: production mocks, visibility, String::from R7 | — | **DONE** (`9cfc2b07`) |
| footPrint CAS wiring (`PROJECTS_PATH`) | P2 | TODO |

### cellMembrane

| Work | Priority | Status |
|------|----------|--------|
| `portable-atomic` | — | **SHIPPED** (`f4da0ae`) |
| CAC impulse dedup (Layer 4) | — | **SHIPPED** (`f4da0ae`) |
| sporePrint health check | — | **SHIPPED** (`f4da0ae`) |
| CAC: TreeParity for heads auto-publish | P1 | FRAGO issued |
| CAC: Tree-parity before cascade policy | P1 | FRAGO issued |
| Caddy blocks for footPrint + tideGlass | P2 | TODO |

### rhizoCrypt

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch | — | **DONE** |
| SSOT sweep (dates, line count, coverage alignment) | — | **DONE** (`35a58bd`) |
| CAC: `SessionTreeHash` primitive | P2 | FRAGO issued |
| Transport: raw UDS → `TransportEndpoint` trait | P2 | Phase 2 |

### biomeOS

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch | — | **DONE** (`16b25557`) |
| Neural API transport → trait-based dispatch | P2 | Phase 2 (TCP fallback exists) |

### skunkBat

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch | — | **DONE** |
| Phase 2: `TransportEndpoint` adoption | — | **SHIPPED** (`6ae036a`) |
| Deep debt: `#[allow]` → `#[expect]`, dead fields, named constants | — | **DONE** (`022bf76`) |

### coralReef

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch | — | **DONE** |
| Deep debt: error handling, de-hardcoding, deduplication | — | **DONE** (`d51bab4`) |
| 3,650 tests (Wave 145 docs) | — | **DONE** |
| Transport: raw UDS → `TransportEndpoint` trait | P2 | Phase 2 |

### barraCuda / loamSpine / sweetGrass

| Work | Priority | Status |
|------|----------|--------|
| Phase 1 cross-arch | — | **DONE** (all) |
| barraCuda: dead feature removal, safe u32 casts, visibility | — | **DONE** (`75c1c880`) |
| loamSpine: async fs hygiene, base64 migration, clone reduction | — | **DONE** (`3cc9ceb`) |
| sweetGrass: v0.7.62, deny.toml cleanup | — | **DONE** (`6344fdb`) |
| Transport: raw UDS → `TransportEndpoint` trait | P2 | Phase 2 |

### sporePrint

| Work | Priority | Status |
|------|----------|--------|
| Rebuild on golgi (P0 — root 404) | **P0** | DIVERGENCE |

### primalSpring

| Work | Priority | Status |
|------|----------|--------|
| `full-cross-compile` scenario (all primals, all arch) | P1 | FRAGO issued |
| `depot-architecture-coverage` scenario | P2 | TODO |
| `footprint-drawbridge-live` scenario (E2E) | P2 | TODO |

---

## sporeGate Hardware Team

| Work | Priority | Status |
|------|----------|--------|
| Windows 14/14 harvest | — | **COMPLETE** (59 depot binaries) |
| northGate mesh enrollment (songbird.exe) | P1 | TODO |
| footPrint server composition deploy | P2 | TODO |

---

## Standing State

### Depot

```
59 depot binaries — Windows 14/14 COMPLETE. bearDog UDS fix on sporeGate.
  x86_64-linux-musl     14   FRESH
  aarch64-linux-musl    14   FRESH
  aarch64-android       14   FRESH
  x86_64-windows-gnu    14   FRESH (Wave 142b harvest)
  BLAKE3 + Ed25519 signed. VPS depot serving.

Exotic validated (songBird): riscv64gc powerpc64le powerpc64 s390x sparc64 arm32 armv7 i686
```

### Topology Issues

| Issue | Status |
|-------|--------|
| RustDesk transient connectivity to ironGate | ACTIVE — intermittent |
| RustDesk transient connectivity to flockGate | ACTIVE — intermittent |
| sporePrint rebuild on golgi (P0 — root 404) | DIVERGENCE |

### Infrastructure Hygiene

| Item | Status |
|------|--------|
| GLACIAL_SHIFT_READINESS.md update (stale 139c) | TODO |
| DNSSEC on primals.eco | TODO |
| primal.eco inner membrane separation | TODO |
| ecosystem_manifest bind_mode/mobility fix | **FIXED** (this cascade) |

### Gate Status

```
eastGate     — PRIMARY. Cascade authority. 38/39 synced.
northGate    — Windows mesh target. RTX 5090. ~1TB AlphaFold.
sporeGate    — NUCLEUS. 13-target build authority. 59 depot bins. Windows 14/14.
golgiBody    — Outer membrane. footprint/ + live. Root 404 (sporePrint).
westGate     — OFFLINE. ZFS cold storage.
ironGate     — ABG/NF compute. JupyterHub. RustDesk transient.
flockGate    — WAN covalent. 16 bonds. RustDesk transient.
grapheneGate — StrongBox target. 14/14 Android ecobins.
```

---

*Wave 143a: Phase 2 FRAGO response — 3 primals shipping abstractions (songBird IpcStream,
petalTongue metrics+Android+WS, skunkBat TransportEndpoint). Windows 14/14 COMPLETE (59
depot bins). toadStool S332-S333 glowplug Vulkan + 9,232 tests. coralReef 3,650 tests.
Deep debt across 8 primals. Manifest fixes. RustDesk transient to ironGate+flockGate.
38/39 synced.*
