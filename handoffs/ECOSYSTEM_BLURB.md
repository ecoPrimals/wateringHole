# ecoPrimals Ecosystem Blurb — Wave 142a

**Date**: Jul 16, 2026 07:30 EDT | **Wave**: 142a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. FULL genomeBin STANDARD ACHIEVED.**

**This cascade**: All 14 primals now compile for all 4 depot architectures.
petalTongue full Windows workspace cross-compile. squirrel Windows harvest
unblocked. sourDough Android platform parity (Os::Android + LibC::Bionic, 490
tests). toadStool S329 `#[cfg(target_os = "linux")]` gating confirmed to exclude
both Windows AND Android — full genomeBin ready. bearDog libc removal. Deep
debt across 5 primals. 39/39 repos synced.

---

## P0: primals.eco Root 404

sporePrint root site returning 404 on `primals.eco`. `footprint/` and
`live.primals.eco` both 200. Needs rebuild/rsync on golgi.

| Owner | Action |
|-------|--------|
| sporePrint team / golgi operator | Rebuild sporePrint and rsync `public/` to golgi |

---

## Evolution Goals — Next Waves

### Goal 1: Silicon Atheism — FULL genomeBin STANDARD (P0 — HARVEST READY)

**All 14 primals compile for all 4 depot architectures. sporeGate re-harvest pending.**

| Work | Owner | Priority | Status |
|------|-------|----------|--------|
| Full 14-primal re-harvest (all 4 arch) | sporeGate | **P0** | **READY** — all blockers resolved |
| Windows harvest | sporeGate | P0 | **14/14 READY** (was 11/14 — petalTongue, squirrel, bearDog resolved) |
| Android harvest | sporeGate | P0 | **14/14 READY** (was 11/14 — sourDough, toadStool resolved) |
| petalTongue Android cdylib target | petalTongue | P2 | Pending (NDK integration — not a compile blocker) |
| `portable-atomic` (PPC32 + consoles) | cellMembrane | P1 | **SHIPPED** (`f4da0ae`) |
| `full-cross-compile` primalSpring scenario | primalSpring | P1 | FRAGO issued |
| Cross-platform E2E test | primalSpring | P2 | NEW |

**Expected**: 56 depot binaries (14 × 4 arch) — up from 55.
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

### Depot (55 binaries → 56 expected after re-harvest)

```
Depot (4 arch, 55 bins — Wave 141b harvest, re-harvest pending):
  x86_64-linux-musl     14   READY (all primals)
  aarch64-linux-musl    14   READY (all primals)
  aarch64-android       14   READY (sourDough+toadStool resolved — re-harvest pending)
  x86_64-windows-gnu    14   READY (petalTongue+squirrel+bearDog resolved — re-harvest pending)
  BLAKE3 + Ed25519 signed. VPS depot serving.

  Current depot: 55 bins (11 Win + 11 Android). After re-harvest: 56 (14×4).

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
                55 depot + 8 exotic. Re-harvest pending (56 expected).
golgiBody    — Outer membrane. footprint/ + live. serving (200). Root 404 (sporePrint).
westGate     — OFFLINE. ZFS cold storage.
ironGate     — ABG/NF compute. JupyterHub.
flockGate    — WAN covalent. 16 bonds.
grapheneGate — StrongBox target. 14/14 Android ecobins (re-harvest pending).
```

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
```
DONE    55 signed ecobins, 4 architectures, 8 exotic validated
DONE    OS Atheism Phases 1-2 (types + transport)
DONE    Per-primal cross-arch adoption: 14/14 COMPLETE
DONE    All 14 primals compile for all 4 depot architectures (full genomeBin standard)
NOW     sporeGate full re-harvest (14×4 = 56 binaries expected)
NOW     Exotic expansion (RISC-V, ARMv7 depot candidates)
NOW     portable-atomic for PPC32 (consoles, embedded)
NOW     northGate mesh enrollment
GOAL    User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm → Sovereign Membrane Parity
```
DONE    Identity web + cascade convergence + depot alignment
DONE    CAC pattern formalized (3/6 layers solved)
NOW     CAC layers 4-6 (heads, rhizoCrypt, cascade)
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

*Wave 142a: FULL genomeBin STANDARD. All 14 primals compile for all 4 depot architectures.
Windows: 14/14 ready (petalTongue full workspace, squirrel unblocked, bearDog libc removed).
Android: 14/14 ready (sourDough Os::Android+LibC::Bionic 490 tests, toadStool target_os="linux"
gating confirmed). sporeGate re-harvest: 56 binaries expected (14×4). Deep debt across 5
primals this cascade. 39/39 synced.*
