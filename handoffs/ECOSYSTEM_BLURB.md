# ecoPrimals Ecosystem Blurb — Wave 157e MESH DEPLOYED

**Date**: Aug 10, 2026 11:45AM | **Wave**: 157e | **From**: overwatch (eastGate)
**Posture**: **DEPLOYED. ALL 6 GATES LIVE ON 157e DEPOT.** Phase 1 CLEAR (strandGate + sporeGate). Phase 2 COMPLETE (westGate 14/14, blueGate 13/13 + builder :9800, southGate 13/13 canary PASS, ironGate 13/13 + vine-bat). sporeGate pepti layer established. Braid pen test 86/87. First signed spine commits. 3/7 jelly strings eliminated. Performance canary: no regression (17,595 conn/s, 0.057ms). **Mesh converged. Ready for next goals.**

---

## DEPLOYMENT STATUS — ALL GATES DEPLOYED

| Gate | Status | Evidence |
|------|--------|----------|
| **sporeGate** | **DEPLOYED** | Depot rebuilt Aug 10 13:41 UTC. Pepti-layer established. 7 jelly strings excised. G69 Phase 3 CAS archival wired. 852 tests. golgi 74% disk. |
| **strandGate** | **DEPLOYED** | [AAR](handoffs/STRANDGATE_WAVE157E_PHASE1_AAR_AUG10_2026.md): 7/7 alive. GEMM Phase 2 PASS. riboCipher Tier 2 active. Production campaign 22/45. |
| **westGate** | **DEPLOYED** | [AAR](aars/WESTGATE_WAVE157E_DEPLOY_AAR_AUG10_2026.md): 14/14 alive. 3/7 jelly strings eliminated. First signed spine commits. FD stable. [Braid pen test](aars/WESTGATE_BRAID_PENTEST_AAR_AUG10_2026.md): 86/87. |
| **blueGate** | **DEPLOYED** | [AAR](aars/BLUEGATE_WAVE157E_PHASE2_DEPLOY_AAR.md): 13/13 alive. `builder.serve :9800` validated. golgi SSH authorized + SCP verified. `plasmid.harvest` operational. |
| **southGate** | **DEPLOYED** | [AAR](fossilRecord/wave157e_phase2_deploy/SOUTHGATE_PHASE2_PERFORMANCE_CANARY_AAR.md): 13/13 alive. **Canary PASS**: 17,595 conn/s, 0.057ms avg — no regression vs 157a. 28 capability sockets. barraCuda -23% binary size. |
| **ironGate** | **DEPLOYED** | [AAR](handoffs/IRONGATE_WAVE157E_PHASE2_DEPLOY_AAR.md): 13/13 alive. 166 capabilities. Dispatch 4ms. Vine-bat operational. westGate mesh peer confirmed. 84 MB RSS. |
| **eastGate** | overwatch | primalSpring to validate. Temporal review complete. |

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
| **toadStool CLI divergence** | toadStool + sporeGate | `up` now requires `<MANIFEST>`. ironGate disabled toadStool. Needs `biome.yaml` template or `toadstool run` adaptation. |
| **Process leak** | coralReef + skunkBat | ~36 orphans/hr on southGate (fork pattern). Needs child process reaping. |
| **biomeOS /health schema** | biomeOS | Returns empty string on blueGate. Should return structured JSON. |
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

## GATE STATUS — 6/6 NUCLEUS — ALL 157e DEPLOYED

| Gate | Services | Key capability |
|------|----------|---------------|
| **sporeGate** | **15/15 ALIVE** | Depot authority. Pepti layer. CAS archival. |
| **strandGate** | **7/7 ALIVE** | Silicon Fold. Production campaign 22/45. 2 GPUs. |
| **westGate** | **14/14 ALIVE** | Data NAS. Signed spine commits. 86/87 braid pen test. Pipeline Rust-native. |
| **blueGate** | **13/13 ALIVE** | Primary builder. `:9800` validated. golgi SSH. Windows native. |
| **southGate** | **13/13 ALIVE** | Performance canary. 17,595 conn/s. 0.057ms. No regression. |
| **ironGate** | **13/13 ALIVE** | Downstream host. 166 caps. Vine-bat. CAS 12.7 TB. |
| **eastGate** | overwatch | primalSpring validation pending. |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (all v4.57+ G68-converged) |
| Deploy progress | **6/6 gates deployed** + eastGate overwatch pending |
| P0 / P1 / P2 | **0 / 1 / 2** (P1: `braid.verify` missing. P2: petalTongue `--port`, coralReef/skunkBat process leak ~36/hr) |
| Golgi depot | **All-arch HEAD-only** unified at canonical path. Auto-prune. Disk-guarded (74%). |
| Build system | **Mesh-native** (blueGate primary, sporeGate fallback, eastGate tertiary, darwinGate enrolling) |
| Jelly strings | **3/7 eliminated** this wave (westGate deploy) |
| Braid pen test | **86/87 pass** — provenance chain E2E verified |
| Production campaign | **22/45** configs (strandGate QCD Rung 1) |
| Tests | **~148K+** across 16 primals |

---

*Wave 157e — MESH DEPLOYED. ALL 6 GATES LIVE. Performance canary PASS (17,595 conn/s, 0.057ms, no regression). 3/7 jelly strings eliminated. First signed spine commits. Braid pen test 86/87. Pepti-layer doctrine established. Production campaign 22/45. Mesh converged — ready for next goals. 16 primals. 0 P0. 1 P1 (braid.verify). ~148K+ tests.*
