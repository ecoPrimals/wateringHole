# ecoPrimals Ecosystem Blurb — Wave 157e DEPLOY ACROSS MESH

**Date**: Aug 10, 2026 8:35AM | **Wave**: 157e | **From**: overwatch (eastGate)
**Posture**: **DEPLOY.** Wave 157d closed with zero P0, zero stragglers, all blurbed primals responded. Depot payload is the largest single-wave evolution: riboCipher Tier 2 chain, Node Atomic trio, GEMM Phase 2, Tokio deep debt, WebGL bridge, G69 Phase 2, FD self-healing, swarmVine Phase 4+Windows. **All code is in tree. Depot rebuild → phased deploy → mesh convergence.**

---

## DEPLOYMENT PLAN

### Phase 1 — Divergence Examination (primalSpring: eastGate + sporeGate + strandGate)

| Gate | Action | Why first |
|------|--------|-----------|
| **eastGate** | primalSpring pulls depot, redeploys all 16 primals. Overwatch validates service health (`biomeOS status`, Neural API `capability.resolve` sweep, `songBird peers`). | Hardware owner, overwatch seat. Full test before fleet. |
| **sporeGate** | Depot rebuild from HEAD (all 16 primals, 4 arches). Push to golgi. Self-deploy. Validate `cellMembrane harvest`, provenance braiding, `depot.lineage`. | Sole depot authority. Must rebuild before anyone else can pull. |
| **strandGate** | Pull from golgi post-rebuild. Validate silicon-specific paths: `coralReef` GEMM Phase 2, `barraCuda` IPC routing, `toadStool` silicon registry discovery (`compute.silicon.registry`). | GPU estate — silicon fold validation requires strandGate hardware. |

**Divergence checks at Phase 1 gates:**
- `biomeOS capability.resolve <cap>` for all 13,910+ registered capabilities — zero timeouts
- `songBird` Tier 2: `0xED` riboCipher framing accepted on `:7700` — decode + dispatch
- `bearDog` `crypto.sign_ed25519` responds (not health stub)
- `nestGate` `content.ingest` + `content.stat` respond
- `cellMembrane` `depot.prune` + `depot.lineage` respond
- `toadStool` `compute.silicon.registry` returns populated `SiliconRegistry`
- `swarmVine` gossip table shows cross-gate peers
- All primals report `status: alive` on health socket

### Phase 2 — Fleet Deploy (if Phase 1 clear)

| Gate | Action | Notes |
|------|--------|-------|
| **blueGate** | Pull from golgi. Redeploy. Validate Windows build authority still functional (`builder.serve :9800`). | Primary builder — must stay healthy. |
| **southGate** | Pull from golgi. Redeploy. Validate Tower Atomic (0.058ms baseline). | Validation gate — performance regression canary. |
| **ironGate** | Pull from golgi. Redeploy. Validate `esotericWebb` cell, 12.7 TB CAS, G18 surfaces. | Downstream host — heaviest data load. |
| **westGate** | Pull from golgi. Redeploy. Validate provenance braiding (990K+ files), CAS federation, Tower Atomic mesh access. | Data NAS — largest braid corpus. |

### Phase 3 — Regroup + Next Goals

Once mesh is converged on post-157d depot, primals pivot to next evolutionary phase.

---

## WAVE 157d PAYLOAD (what's deploying)

| System | What shipped |
|--------|-------------|
| **riboCipher Tier 2** | CHAIN CLOSED: bearDog encodes → biomeOS sends `[0xED,0x01]` → songBird accepts on `:7700` with full dispatch. |
| **Node Atomic trio** | FULLY WIRED: barraCuda IPC client (`compiler_prefers_coral()` + `CoralCompiler::compile_gemm()`), toadStool silicon registry (coralReef IPC query), coralReef GEMM Phase 2. |
| **toadStool S374** | Silicon registry, self-audit (126 methods), Tokio deep debt (26/48 WASM), types extracted to `toadstool-core`. |
| **songBird** | Transport convergence (`CanonicalTransport`), gossip excised to swarmVine, PID fix, riboCipher `:7700` acceptance. |
| **biomeOS** | Generic capability dispatch, `raise_fd_limit()` self-healing, Tier 2 client pool, G69 depot lineage templates. |
| **swarmVine** | Phase 4 (subscriptions, bloom filters, compute+depot types) + Windows port. 134 tests. |
| **petalTongue** | `/ws/scene` WebSocket, WebGL compilation bridge, FD self-healing. G19 browser surface foundation. |
| **cellMembrane** | G69 Phase 2: ProvenanceEntry enrichment, HarvestResult consolidation, validate_lineage hardening. |
| **barraCuda** | Zero-panic refactor, deep debt (DF64, CachedPipeline), Silicon Fold absorption. 5,031 tests. |
| **coralReef** | GEMM Phase 2 (shared-memory tiling), deep debt splits (PLop3, SM80 hazard). 3,814 tests. |
| **bearDog** | `RiboCipherHandler` for Tier 2 encode/decode. Health guard + -32601 for non-health. |

---

## NEXT GOALS (post-deploy regroup)

### Immediate — Unlocked by this deploy

| Goal | Owner | Description |
|------|-------|-------------|
| **Spine commit signing** | bearDog + loamSpine | `bearDog` `crypto.sign_ed25519` now in depot. Wire `loamSpine` → signed commits fleet-wide. |
| **G69 Phase 3: CAS archival** | cellMembrane | **WIRED** — `archive_superseded_binary()` in harvest pipeline. `depot_lineage` graph executes sign→spine→braid→CAS. Best-effort, never blocks builds. |
| **`native_braid.py` elimination** | cellMembrane | Last major jelly string. Rust replacement unblocked by G69 Phase 2. |
| **WASM push (26→48)** | toadStool | Tokio deep debt cleared path. 22 remaining crates need tokio feature-gate or sync alternatives. |
| **WebGL pipeline for esotericWebb** | petalTongue + esotericWebb | `/ws/scene` foundation ready. Wire G19 browser surfaces. |
| **squirrel agent panel** | squirrel + footPrint | WebSocket → petalTongue → squirrel live wiring. |

### Near-term — Next wave focus

| Goal | Owner | Description |
|------|-------|-------------|
| **shader.compile.wgsl** | barraCuda → coralReef | General shader compilation via IPC (beyond GEMM). |
| **PrecisionBrain routing** | barraCuda | Complete Fp64→F16 silicon-aware dispatch. |
| **PTX SM120 / Blackwell** | coralReef | Next-gen NVIDIA target. |
| **Vertex/Fragment shaders** | coralReef | 8-12 week effort, graphics pipeline completion. |
| **ludoSpring extraction** | petalTongue | `doom-core` → new spring for game/visualization engine. |
| **Inner Membrane Phase 4** | biomeOS + songBird | Pure primal communication — eliminate remaining WireGuard/SSH dependency. |

### Glacial — Ongoing

| Goal | Status |
|------|--------|
| arXiv 41/42 | `validate.sh` + reviewer send remaining |
| aarch64-musl depot | 13/19, no ARM64 gates active |
| southGate mesh enrollment | LAN discovery pending |
| darwinGate (M4 Mac Mini) | Hardware arriving — manifest registered, pending `gate.bootstrap` |
| steamGate | Future platform gate |

---

## GATE STATUS — 6/6 NUCLEUS

| Gate | Status | Deploy order |
|------|--------|-------------|
| **sporeGate** | **15/15 ALIVE** | **PHASE 1** — rebuild depot first, then self-deploy |
| **eastGate** | overwatch | **PHASE 1** — pull + validate after sporeGate rebuild |
| **strandGate** | **13/13 ALIVE** | **PHASE 1** — silicon validation (GPU estate) |
| **blueGate** | **13/13 ALIVE** | **PHASE 2** — builder health validation |
| **southGate** | **13/13 ALIVE** | **PHASE 2** — performance canary |
| **ironGate** | **13/13 ALIVE** | **PHASE 2** — downstream + CAS validation |
| **westGate** | **13/13 ALIVE** | **PHASE 2** — data NAS + braid validation |

---

## PEPTI-LAYER DOCTRINE — golgiBody Architecture

**golgiBody is the peptidoglycan layer** — a thin relay and deployment hub for ALL platforms. It holds exactly ONE binary per (primal, arch) — the latest verified phenotype (HEAD). The genotype history lives in CAS.

### Invariants

1. **HEAD-only depot**: golgi stores the *latest generation* per (primal, arch). Superseded binaries are archived to CAS before overwrite.
2. **Never compiles**: golgi has no build toolchain. Sub-builders push HEAD to golgi; golgi only serves and relays.
3. **All-arch deployment hub**: musl, gnu, windows, darwin/ARM64, android, future RISC-V — every platform has a slot in `plasmidBin/primals/{arch}/`.
4. **Disk-guarded**: Pre-push disk health check warns at 80%, blocks at 90%. Auto-prune removes non-registry binaries on every harvest.
5. **Forgejo relay**: Holds relay copies of ecosystem repos. Weekly GC timer compacts objects. Shallow clone depth.

### Sub-Builder Fleet

| Target | Sub-builder | Status |
|--------|-------------|--------|
| `x86_64-unknown-linux-musl` | sporeGate (fallback) | **LIVE** |
| `x86_64-unknown-linux-gnu` | sporeGate | **LIVE** |
| `x86_64-pc-windows-gnu` | blueGate | **LIVE** |
| `aarch64-unknown-linux-musl` | eastGate (cross) | **PARTIAL** |
| `aarch64-apple-darwin` | darwinGate (M4 Mac Mini) | **ENROLLING** |
| `aarch64-linux-android` | sporeGate (NDK cross) | **STALE** |

### Binary Evolution (G69 Phase 3)

Superseded binaries follow the provenance trio pattern:
- **BLAKE3** content hash = CAS identity
- **loamSpine** = per-(primal,arch) linear commit history (Merkle chain)
- **sweetGrass** = attribution braids (builder, wave, commit delta)
- **nestGate/ironGate** = CAS storage (12.7TB on ironGate)
- Same pattern westGate uses for 990K+ data braids

### Gate Role Clarity

- **golgiBody** — Pepti relay. All-arch HEAD-only depot. Caddy TLS. Forgejo relay. Stays thin.
- **sporeGate** — Topology owner. Cascade timer. Prune authority. Foreman for sub-builder fleet. Fallback musl/gnu builder.
- **blueGate** — Primary builder. Windows-gnu native. `builder.serve :9800` on mesh.
- **darwinGate** — Apple builder. `aarch64-apple-darwin` native. `builder.serve` on mesh.
- **eastGate** — Overwatch. Tertiary builder. aarch64-musl cross-compile. primalSpring validation.
- **ironGate** — Binary CAS archive. Every binary ever built, keyed by BLAKE3. 12.7TB. G69 Phase 3 target.
- **westGate** — Data CAS. 990K+ braided files. 50.7TB ZFS. CAS federation endpoint.

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (all v4.57+ G68-converged) |
| P0 / P1 / P2 | **0 / 0 / 1** (P2: petalTongue `--port`) |
| Golgi depot | **All-arch HEAD-only**: musl 19, windows-gnu 25, gnu 14, aarch64 14. G69 lineage. Auto-prune. Disk-guarded. |
| Build system | **Mesh-native** (blueGate primary, sporeGate fallback, eastGate tertiary, darwinGate enrolling) |
| Depot path | **Unified** at `/opt/ecoPrimals/plasmidBin/primals` — Caddy serves direct, no symlinks |
| songBird mesh | **11 peers** across 7 gates |
| Caps registered | **13,910+** |
| Tests | **~148K+** across 16 primals |

---

*Wave 157e — DEPLOY ACROSS MESH. Phase 1: primalSpring (eastGate + sporeGate + strandGate) examines divergence. Phase 2: fleet-wide (blueGate, southGate, ironGate, westGate). Phase 3: regroup for next goals. Payload: riboCipher Tier 2, Node Atomic trio, GEMM Phase 2, toadStool S374, songBird vertebrate, swarmVine Phase 4, WebGL bridge, G69 Phase 2. 16 primals. 0 P0. ~148K+ tests.*
