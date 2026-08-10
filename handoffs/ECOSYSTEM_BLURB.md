# ecoPrimals Ecosystem Blurb — Wave 157e MESH DEPLOY IN PROGRESS

**Date**: Aug 10, 2026 11:30AM | **Wave**: 157e | **From**: overwatch (eastGate)
**Posture**: **DEPLOYING.** Phase 1 CLEAR (strandGate AAR). westGate Phase 2 deployed (14/14, 3/7 jelly strings eliminated, first signed spine commits). sporeGate pepti layer established (depot unified, 7 jelly strings excised, G69 Phase 3 CAS archival wired). Braid pen test 86/87 pass — provenance chain verified E2E. **Remaining: blueGate, southGate, ironGate Phase 2 deploy. eastGate overwatch validation.**

---

## DEPLOYMENT STATUS

### Phase 1 — CLEAR

| Gate | Status | Evidence |
|------|--------|----------|
| **sporeGate** | **DEPLOYED + EVOLVED** | Depot rebuilt Aug 10 13:41 UTC. Pepti-layer doctrine established. 7 jelly strings excised. G69 Phase 3 CAS archival wired. Depot unified at `/opt/ecoPrimals/plasmidBin/primals`. golgi at 74% disk (was 87%). 852 tests pass. |
| **strandGate** | **PHASE 1 CLEAR** | [AAR](handoffs/STRANDGATE_WAVE157E_PHASE1_AAR_AUG10_2026.md): 7/7 services alive. coralReef GEMM Phase 2 PASS. 2 GPUs detected. riboCipher Tier 2 active. 1 non-blocking divergence: toadStool depot binary predates S374 silicon registry. Production campaign 22/45 (ETA ~6h). |
| **eastGate** | **PENDING** | primalSpring to pull depot and validate. Overwatch temporal review complete. |

### Phase 2 — IN PROGRESS

| Gate | Status | Evidence |
|------|--------|----------|
| **westGate** | **DEPLOYED** | [AAR](aars/WESTGATE_WAVE157E_DEPLOY_AAR_AUG10_2026.md): 14/14 alive. All 3 P0s resolved in field. Pipeline Rust-native. 3/7 jelly strings eliminated. First signed spine commits. FD count stable (13→15 after 7 calls). `content.ingest` 5 files/6.3ms. [Braid pen test](aars/WESTGATE_BRAID_PENTEST_AAR_AUG10_2026.md): 86/87 pass. |
| **blueGate** | **PENDING** | Pull from golgi. Validate `builder.serve :9800`. |
| **southGate** | **PENDING** | Pull from golgi. Validate Tower Atomic baseline. |
| **ironGate** | **PENDING** | Pull from golgi. Cross-gate replication confirmed from westGate pen test (Level 7 PASS). |

---

## KEY EVOLUTION THIS CASCADE

### 1. westGate Deploy — 3/7 Jelly Strings Eliminated

| Jelly String | Status |
|-------------|--------|
| ~~Directory walk + hash (Python)~~ | **ELIMINATED** — nestGate `content.ingest` (Rust-native) |
| ~~CAS storage (Python base64)~~ | **ELIMINATED** — ingest does it in Rust |
| ~~Unsigned spine commits~~ | **ELIMINATED** — bearDog Ed25519 signing LIVE |
| ~~biomeOS routing bypass~~ | **MOSTLY ELIMINATED** — `capability.call` at 1.3ms |
| Chunk coordination (file locks) | ACTIVE — needs biomeOS task graph |
| NVMe staging (Python rsync) | ACTIVE — needs tier-aware ingest |
| Prov chain orchestration (5 RPCs) | ACTIVE — needs biomeOS graph |

### 2. sporeGate Pepti Layer — Depot Architecture Hardened

- Depot path unified: `/opt/ecoPrimals/plasmidBin/primals` (Caddy serves direct)
- `depot.prune` auto-cleans non-registry binaries on every harvest
- Disk health guard: warns 80%, blocks 90%
- G69 Phase 3: `archive_superseded_binary()` in harvest pipeline (sign→spine→braid→CAS)
- darwinGate (M4 Mac Mini) registered as sub-builder
- Forgejo weekly GC timer installed
- 7 legacy patterns excised (SSH transport, freshness unify, broken prov scripts, depot-push script)

### 3. Braid Pen Test — Provenance Chain Verified

86/87 pass across 8 progressive levels. First-ever E2E verification:
- Merkle proofs verify correctly (multi-vertex trees)
- Ed25519 signatures reject tampered payloads
- CAS content-addressing makes corruption-by-overwrite impossible
- Braids survive CAS deletion (braid as insurance thesis validated)
- ChaCha20-Poly1305 encrypted CAS works E2E
- Sharded recovery works (4-shard split, per-shard encryption, partial loss detection)
- Cross-gate federation works (`content.replicate` to ironGate)
- Discovery manifest: 131 datasets, 100 braids, 2 spines indexed

**P1 discovered**: `braid.verify` does not exist in sweetGrass — verification is manual, not atomic.

### 4. strandGate Production Campaign

22/45 configs complete. Physics quality excellent:
- Volume convergence visible: 16⁴→24⁴ (correct direction)
- β-dependence clean and monotonic
- Errors decrease with volume (√V scaling)
- All values consistent with Bali et al. literature
- ETA ~6h remaining (32⁴ configs dominant)

### 5. strandGate Pipeline Needs AAR

[Upstream needs](handoffs/STRANDGATE_E2E_PIPELINE_NEEDS_AUG10_2026.md) for first complete science pipeline:
- **ironGate**: NFT registration endpoint, `/pseudospore/<hash>` route, verification page
- **sporePrint**: QCD Rung 1 page, download route, LaTeX→web
- **petalTongue**: data visualization capability, WebGL lattice scene
- **pepti/golgi**: `validate.sh` → Rust binary, pseudospore_manifest depot binary

---

## NEXT GOALS (post-deploy regroup)

### Immediate — In progress or unblocked

| Goal | Owner | Status |
|------|-------|--------|
| **Spine commit signing** | bearDog + loamSpine | **LIVE on westGate** — first signed commits in ecosystem history |
| **G69 Phase 3: CAS archival** | sporeGate | **WIRED** — `archive_superseded_binary()` in harvest pipeline |
| **`native_braid.py` evolution** | westGate + cellMembrane | **3/7 eliminated** — remaining 4 need biomeOS graph or nestGate tier awareness |
| **`braid.verify`** | sweetGrass | **NEW P1** — verification must become atomic (discovered in pen test) |
| **toadStool S374 depot binary** | sporeGate | Non-blocking — next rebuild from HEAD includes silicon registry |
| **Production campaign completion** | strandGate | 22/45 → 45/45 (~6h remaining) |

### Near-term — Next wave focus

| Goal | Owner | Description |
|------|-------|-------------|
| **Science pipeline E2E** | strandGate + ironGate + sporePrint | NFT registration, pseudoSpore bundles, QCD page |
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC |
| **PrecisionBrain routing** | barraCuda | Fp64→F16 silicon-aware dispatch |
| **WASM push (26→48)** | toadStool | Tokio deep debt cleared path |
| **WebGL pipeline** | petalTongue + esotericWebb | G19 browser surfaces |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring |
| **Inner Membrane Phase 4** | biomeOS + songBird | Pure primal communication |

### Glacial

| Goal | Status |
|------|--------|
| arXiv 41/42 | Campaign 22/45. `validate.sh` → Rust binary. Reviewer send. |
| aarch64-musl depot | 13/19, no ARM64 gates active |
| southGate mesh enrollment | LAN discovery pending |
| darwinGate (M4 Mac Mini) | Manifest registered, pending `gate.bootstrap` |
| steamGate | Future platform gate |
| Remaining 4 jelly strings | Need biomeOS graph executor or nestGate tier awareness |

---

## PEPTI-LAYER DOCTRINE — golgiBody Architecture

**golgiBody is the peptidoglycan layer** — a thin relay and deployment hub for ALL platforms. It holds exactly ONE binary per (primal, arch) — the latest verified phenotype (HEAD). The genotype history lives in CAS.

### Sub-Builder Fleet

| Target | Sub-builder | Status |
|--------|-------------|--------|
| `x86_64-unknown-linux-musl` | sporeGate (fallback) | **LIVE** |
| `x86_64-unknown-linux-gnu` | sporeGate | **LIVE** |
| `x86_64-pc-windows-gnu` | blueGate | **LIVE** |
| `aarch64-unknown-linux-musl` | eastGate (cross) | **PARTIAL** |
| `aarch64-apple-darwin` | darwinGate (M4 Mac Mini) | **ENROLLING** |
| `aarch64-linux-android` | sporeGate (NDK cross) | **STALE** |

---

## GATE STATUS — 6/6 NUCLEUS

| Gate | Status | Deploy phase |
|------|--------|-------------|
| **sporeGate** | **15/15 ALIVE** | **PHASE 1 DONE** — depot rebuilt, pepti layer established |
| **strandGate** | **13/13 ALIVE** | **PHASE 1 CLEAR** — silicon validated, campaign running |
| **eastGate** | overwatch | **PHASE 1 PENDING** — primalSpring to validate |
| **westGate** | **14/14 ALIVE** | **PHASE 2 DONE** — 3/7 jelly strings eliminated, signed commits |
| **blueGate** | **13/13 ALIVE** | **PHASE 2 PENDING** — builder health validation |
| **southGate** | **13/13 ALIVE** | **PHASE 2 PENDING** — performance canary |
| **ironGate** | **13/13 ALIVE** | **PHASE 2 PENDING** — cross-gate replication confirmed |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (all v4.57+ G68-converged) |
| Deploy progress | **3/7 gates deployed** (sporeGate, strandGate, westGate) |
| P0 / P1 / P2 | **0 / 1 / 1** (P1: `braid.verify` missing. P2: petalTongue `--port`) |
| Golgi depot | **All-arch HEAD-only** unified at canonical path. Auto-prune. Disk-guarded (74%). |
| Build system | **Mesh-native** (blueGate primary, sporeGate fallback, eastGate tertiary, darwinGate enrolling) |
| Jelly strings | **3/7 eliminated** this wave (westGate deploy) |
| Braid pen test | **86/87 pass** — provenance chain E2E verified |
| Production campaign | **22/45** configs (strandGate QCD Rung 1) |
| Tests | **~148K+** across 16 primals |

---

*Wave 157e — MESH DEPLOY IN PROGRESS. Phase 1 CLEAR (strandGate + sporeGate). Phase 2: westGate DEPLOYED (3/7 jelly strings eliminated, first signed commits). blueGate, southGate, ironGate pending. Braid pen test 86/87 — provenance chain verified. sporeGate pepti layer established. strandGate production campaign 22/45. 16 primals. 0 P0. 1 P1 (braid.verify). ~148K+ tests.*
