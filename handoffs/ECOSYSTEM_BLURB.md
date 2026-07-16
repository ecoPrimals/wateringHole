# ecoPrimals Ecosystem Blurb — Wave 141b

**Date**: Jul 15, 2026 16:50 EDT | **Wave**: 141b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. SILICON ATHEISM CONVERGENCE ACCELERATING.**

**This cascade**: sporeGate executed Windows + Android re-harvest.
**55 depot binaries** across 4 architectures (up from 45). Windows: 11/14.
Android: 11/14. cellMembrane delivered CAC impulse dedup + portable-atomic
+ sporePrint health check (P0 detection). footPrint `@protokarya/rustscript`
npm package finalized. 39/39 repos synced.

---

## P0: primals.eco Root 404

sporePrint root site returning 404 on `primals.eco`. `footprint/` and
`live.primals.eco` both 200. Likely needs rebuild/rsync on golgi.

| Owner | Action |
|-------|--------|
| sporePrint team / golgi operator | Rebuild sporePrint and rsync `public/` to golgi |
| cellMembrane team | Add `sporePrint` health check to cascade post-sync |

---

## Evolution Goals — Next Waves

### Goal 1: Silicon Atheism Convergence (P1 — PARALLEL SUBTASK, ACCELERATING)

**Adoption: 14/14 COMPLETE. Harvest: 55 binaries (11 Windows, 11 Android).**

| Work | Owner | Priority | Status |
|------|-------|----------|--------|
| Windows harvest | sporeGate | P0 | **11/14 DONE** — bearDog, squirrel, petalTongue pending |
| Android harvest | sporeGate | P1 | **11/14 DONE** — petalTongue, toadStool, sourDough pending |
| `portable-atomic` (PPC32 + consoles) | cellMembrane | P1 | **SHIPPED** (`f4da0ae`) |
| CAC impulse dedup | cellMembrane | P1 | **SHIPPED** (`f4da0ae`) — Layer 4 solved |
| sporePrint health check (P0 detection) | cellMembrane | P1 | **SHIPPED** (`f4da0ae`) |
| Remaining 3 Windows primals (UDS abstraction) | bearDog, squirrel, petalTongue | P1 | TODO |
| `full-cross-compile` primalSpring scenario | primalSpring | P1 | FRAGO issued |
| Cross-platform E2E test | primalSpring | P2 | NEW |

**Per-primal handoff**: `CROSS_ARCH_PER_PRIMAL_HANDOFFS.md`

### Goal 2: Content-Addressed Convergence (P1–P2)

**Score: 3/6 layers solved.**

| Layer | Fix | Priority | Status |
|-------|-----|----------|--------|
| Git repos (tree hashes) | freshness.toml `HEAD^{tree}` | — | **SOLVED** |
| Depot binaries (BLAKE3) | depot_sync checksums | — | **SOLVED** |
| Impulse dedup | Content-hash before creation | — | **SOLVED** (`f4da0ae`) |
| Heads auto-publish | TreeParity before agentic dispatch | P1 | FRAGO issued |
| rhizoCrypt DAG | SessionTreeHash primitive | P2 | FRAGO issued |
| Cascade divergence | Tree-parity before policy | P1 | FRAGO issued |

**Handoffs**: `CAC_CELLMEMBRANE_HANDOFF.md`, `CAC_RHIZOCRYPT_HANDOFF.md`

### Goal 3: footPrint Full Composition (Track 3)

| Step | Owner | Status |
|------|-------|--------|
| Wire `PROXY_PATH` → songBird drawbridge | songBird + footPrint | TODO |
| Wire `PROJECTS_PATH` → nestGate CAS | nestGate + footPrint | TODO |
| Wire `WS_PATH` → agent bridge | petalTongue | TODO |
| Deploy composition on sporeGate | sporeGate hardware | TODO |
| Caddy block + drawbridge routes | cellMembrane | TODO |
| `footprint-drawbridge-live` scenario (E2E) | primalSpring | TODO |
| RustScript → `@protoKarya/rustscript` | footPrint | TODO |

**Handoff**: `FOOTPRINT_SERVER_DEPLOY_HANDOFF_139a.md`

### Goal 4: tideGlass Phase 0

| Step | Owner | Status |
|------|-------|--------|
| Clone into `protists/tideGlass` | overwatch | TODO |
| Reproduce GPS paper figures vs Python baseline | Gonzales | TODO |
| Caddy block at `tideglass.primals.eco` | cellMembrane | TODO |
| Drawbridge bonds (LINCS, GEO, ChEMBL, NF Portal) | songBird | TODO |

---

## Standing State

### Depot (45 binaries + 8 exotic validated)

```
Depot (4 arch, 55 bins — Wave 141b harvest):
  x86_64-linux-musl     16   FRESH
  aarch64-linux-musl    16   FRESH
  aarch64-android       11   FRESH (3 pending: petalTongue, toadStool, sourDough)
  x86_64-windows-gnu    11   FRESH (3 pending: bearDog, squirrel, petalTongue — UDS abstraction)
  BLAKE3 + Ed25519 signed. VPS depot serving.

Exotic validated (songBird, not yet in depot):
  riscv64gc  powerpc64le  powerpc64  s390x  sparc64  arm32  armv7  i686
  PPC32 blocked (portable-atomic FRAGO issued)
```

### Pipeline

| Component | Status |
|-----------|--------|
| `membrane` on sporeGate | CURRENT — Phase 2 shipped |
| `depot_sync --push` | OPERATIONAL |
| SSH sporeGate → golgi | CONNECTED |
| FRAGO impulse system | OPERATIONAL (2 active) |
| cellMembrane health | 1,074 tests, clippy clean, `#![forbid(unsafe_code)]` |

### Spring Mathematics

```
Infrastructure: 162 scenarios, 1,194 tests (5 protoKarya gaps identified)
Domain:         wetSpring 782, healthSpring 233, hotSpring 500+, neuralSpring 154
```

### Remaining Infrastructure Hygiene

| Item | Status |
|------|--------|
| sporePrint rebuild on golgi (P0 — 404) | DIVERGENCE |
| sporeGate head re-publish (stale Jul 6) | TODO |
| freshness.toml re-publish (stale Wave 137) | TODO |
| GLACIAL_SHIFT_READINESS.md update (stale 139c) | TODO |
| DNSSEC on primals.eco | TODO |
| primal.eco inner membrane separation | TODO |
| northGate mesh enrollment | TODO (songbird.exe ready) |

---

## Gate Status

```
eastGate     — PRIMARY. Cascade authority. 42 repos. 39/39 synced.
northGate    — Windows mesh target. songbird.exe in depot. RTX 5090. ~1TB AlphaFold.
sporeGate    — NUCLEUS. 13-target build authority. Phase 2 shipped.
                45 depot + 8 exotic. Head stale (Jul 6 — needs re-publish).
golgiBody    — Outer membrane. footprint/ + live. serving (200). Root 404 (sporePrint).
westGate     — OFFLINE. ZFS cold storage.
ironGate     — ABG/NF compute. JupyterHub.
flockGate    — WAN covalent. 16 bonds.
grapheneGate — StrongBox target. 12/14 Android ecobins.
```

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
```
DONE    45 signed ecobins, 4 architectures, 8 exotic validated
DONE    OS Atheism Phases 1-2 (types + transport)
DONE    Per-primal cross-arch adoption: 14/14 COMPLETE
NOW     sporeGate full Windows harvest (14 primals ready)
NOW     Multi-arch harvest (Android, RISC-V, ARMv7 depot candidates)
NOW     portable-atomic for PPC32 (consoles, embedded)
NOW     northGate mesh enrollment
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm → Sovereign Membrane Parity
```
DONE    Identity web + cascade convergence + depot alignment
DONE    CAC pattern formalized (2/6 layers solved)
NOW     CAC layers 3-6 (heads, impulses, rhizoCrypt, cascade)
NOW     sporePrint rebuild (P0)
NOW     DNSSEC + primal.eco separation
GOAL    Universal depot — same system for every gate and architecture.
```

### Track 3: Live Compositions → External Science Production ← PRIMARY
```
DONE    footPrint client LIVE + deep debt cleaned (98 tests)
DONE    Gonzales chart scenes (4) + petalTongue clippy clean (366 tests)
NOW     footPrint server composition on sporeGate
DONE    RustScript → @protokarya/rustscript npm package (47 files, 23.8 KB)
NOW     Live drawbridge E2E (USGS/FEMA → songBird → NestGate CAS)
NEXT    tideGlass Phase 0 (GPS paper reproduction)
NEXT    helixVision Phase C (GEMM → Evoformer)
GOAL    Pure Rust backend + sovereign compositions + external science.
```

---

*Wave 141b: 55 depot binaries (11 Windows, 11 Android — up from 45). 14/14 cross-arch
adopted. cellMembrane: CAC impulse dedup SHIPPED (3/6 layers solved), portable-atomic
SHIPPED, sporePrint health check SHIPPED. RustScript npm package finalized. 3 Windows
+ 3 Android primals pending UDS/platform fixes. 39/39 synced. 2 active FRAGOs.*
