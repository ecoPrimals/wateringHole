# ecoPrimals Ecosystem Blurb — Remaining Work Focus

**Date**: Aug 5, 2026 LATE | **Wave**: 156g | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. 14/26 DEBT ITEMS CLEARED. DEPOT REBUILT (26 binaries, blueGate sub-builder 15/15 Windows). nestgate.io 10/12 sections (health.liveness S8 SHIPPED, 11/13 alive). toadStool absorbs Akida driver (7,755 lines). ALL 15 PRIMALS at HEAD. 15/15 GREEN. ~140K+ tests. No code blockers — remaining work is ops + integration.**

---

## LATEST ARRIVALS (since 156f)

| Event | Source | Impact |
|-------|--------|--------|
| **DEPOT REBUILT** | sporeGate | 15/15 musl + 15/15 Windows = **26 binaries** pushed to golgi. blueGate sub-builder dispatched in parallel. 6 divergences documented (UDS protocol fragmentation, socket paths). All resolved except DIV-4 (coralReef tarpc architecture) and DIV-5 (toadStool socket deploy). |
| **petalTongue S8 CLEARED** | overwatch | `health.liveness` per primal via UDS. 13 primals queried concurrently with BTSP framing. 11/13 alive (coralReef=tarpc, toadStool=perms). **nestgate.io 10/12 sections.** |
| **toadStool Akida absorption** | biomeGate | rustChip neuromorphic driver: 9 new modules (VFIO, PUF, sentinel, SRAM, tenancy, glowplug, hybrid ESN, software backend). `Box<dyn NpuBackend>` trait objects. `akida-chip` shared silicon model. 171 tests. **Note**: `infra/rustChip` is biomeGate-local (not yet on Forgejo). |

---

## REMAINING WORK — 12 ITEMS

All code-level blockers (S1–S8, B1–B2, O1/O3/O4/O8, S4–S5) are **cleared**. What remains is ops deployments, feature integration, and science pipeline work. Organized by unlock sequence.

### Tier 1 — Next Unlocks (ops deployments)

| # | Item | Owner | Gate | Unblocks |
|---|------|-------|------|----------|
| **E2** | **squirrel systemd on ironGate** — create `squirrel.service`, deploy to `/run/user/1000/biomeos/squirrel.sock`. petal-bridge already routes `agent.*` → squirrel UDS. | eastGate | ironGate | **Agent panel LIVE on footprint.primals.eco** |
| **D1** | **tideGlass cell boot on westGate** — `biomeos nucleus attach --cell tideglass_cell.toml`. GPS data ready (11 JSON, 103 MB CAS). PetalTongueClient ready. | overwatch | westGate | **Track A science starts** |
| **O5** | **nestGate TCP on westGate** — set `NESTGATE_JSONRPC_TCP=1` or `--port 8080`. Register `content` capability with songBird. Code already shipped. | overwatch | westGate | **Inter-gate CAS federation** |

### Tier 2 — Integration Work (code + ops)

| # | Item | Owner | Primal | Unblocks |
|---|------|-------|--------|----------|
| **O7** | **Inter-gate `content.get` E2E** — first live test: ironGate pulls CAS object from westGate. songBird probes + nestGate `content.fetch` ready. | overwatch | songBird + nestGate | All data-remote springs |
| **O6** | **petalTongue scene passthrough** — accept tideGlass declarative viz format. If `SceneGraph` doesn't match, add passthrough mode. | overwatch | petalTongue | GPS + QCD viz pipeline |
| **E3** | **esotericWebb HEAD method** — GET=200, HEAD=502. HTTP handler missing HEAD support (NG-06). | eastGate | esotericWebb | `webb.primals.eco` health checks |
| **E1** | **bearDog Neural API routing stub** — register capability with Neural API so nestgate.io shows bearDog in routing table (NG-04). | eastGate | bearDog | nestgate.io 11/12 |
| **S9** | **Neural API symlink pattern** — document as canonical, replicate on all NUCLEUS gates. Currently sporeGate workaround. | overwatch | biomeOS (ops) | Gate deploys |

### Tier 3 — Feature Work (P3, not blocking)

| # | Item | Owner | Primal | Notes |
|---|------|-------|--------|-------|
| **B3** | **coralReef SU(N≥4) shader generalization** — WGSL hardcoded for 3×3. Not blocking Rung 1 (CPU measurement suffices). | biomeGate | coralReef | Blocks GPU-accelerated higher-N (G45 Rung 2+) |
| **O2** | **nestGate `content.fetch`** — download URL → CAS in one RPC. May already be shipped (Session 133). Verify. | overwatch | nestGate | Data pipeline convenience |

### Tier 4 — Ongoing / Monitoring

| # | Item | Gate | Status |
|---|------|------|--------|
| **D3** | **Convoy completion** — 11M+ files at 217/s on NVMe. Post-convoy: rsync hot→cold. | westGate | Running (~14h ETA) |
| **D4** | **SU(N) thermalization** — 87-config grid on 64 EPYC threads (~2wk). Monitor + measure as configs land. | strandGate | Running |

---

## CEPHALIZATION — G64: tarpc CONVERGENT EVOLUTION

The ecosystem is dual-protocol by design: JSON-RPC is the discovery/bootstrap layer, tarpc is the performance composition layer. Like biological cephalization — organisms developing centralized coordination — all primals converge to a common tarpc composition pattern while evolving through their own code independently. Bats, birds, and insects all fly, but each evolved flight on their own terms.

### Inter-Membrane Transport Layers

| Layer | Protocol | Scope | Speed | When |
|-------|----------|-------|-------|------|
| **Intra-gate** | tarpc UDS (binary) | Primals on same NUCLEUS | sub-ms, zero serde | Phase 1 (NOW — 5 primals ready) |
| **Cross-gate bootstrap** | JSON-RPC over songBird mesh | Gate-to-gate discovery | ~1-5ms | Current (LIVE) |
| **Cross-gate elevated** | tarpc over songBird relay | Gate-to-gate composition | sub-ms binary | Phase 2 (after version convergence) |
| **Browser/diagnostic** | JSON-RPC / REST | Dashboards, health, tools | ~10ms | Permanent (conjugation layer) |

### Current tarpc Readiness

| State | Primals | Count |
|-------|---------|-------|
| **tarpc-default** (server + client, default feature) | coralReef, barraCuda, toadStool, nestGate, squirrel | 5 |
| **tarpc-wired** (service definitions, optional) | songBird, sweetGrass, loamSpine, rhizoCrypt, petalTongue, biomeOS | 6 |
| **tarpc dep only** (not yet serving) | bearDog, skunkBat, sourDough, bingoCube | 4 |

### Convergence Blockers

1. **tarpc version split**: songBird + petalTongue on **0.34**, all others on **0.37**. bincode 1.3→2.x compatibility blocks upgrade.
2. **UDS protocol fragmentation**: 6 divergences documented (DIV-1→6). Some primals use BTSP framing, some don't. songBird uses plain JSON on UDS.
3. **Port-agnostic routing**: Tower Atomic currently assigns ports. Cephalization eliminates this — songBird discovers and routes by capability, not port.

### Performance Thesis

westGate convoy achieves 217 files/s with JSON-RPC IPC (~5ms/file primal time). tarpc binary framing eliminates the JSON serde roundtrip entirely. For intra-gate composition (same UDS, same machine), this could push primal-to-primal calls below 100µs — **potentially 50x improvement** for high-frequency composition patterns like provenance braiding, CAS operations, and GPU dispatch chains.

---

## DEPOT STATUS

All 15 primals compile clean at HEAD. Pushed to Forgejo. **Depot REBUILT** — 26 binaries on golgi. blueGate sub-builder proven (15/15 Windows).

| Primal | HEAD | Key Change |
|--------|------|------------|
| sweetGrass | `4a6ec48` | convergence.check + braid.list (S1–S3) |
| nestGate | `cbeb328` | content.ingest + dataset.convergence + Neural API (O1/O3/O4/O8) |
| loamSpine | `ede1b65` | spine.status (S6) |
| toadStool | `da284da` | socket perms (B1/B2) + Akida driver absorption |
| petalTongue | `783aaac` | mesh.peers (S7) + health.liveness (S8) |
| coralReef | `e5ff9a8` | VOP3 split, WGSL optimization (6 commits) |
| squirrel | `d752462` | deep debt sweep 156e→156j |
| rhizoCrypt | `c0abe75` | S4/S5 verified pre-shipped, clean audit |

**Remaining 7 primals** (songBird, bearDog, biomeOS, barraCuda, cellMembrane, skunkBat, sourDough, bingoCube) — no functional changes this cascade, already at depot-current HEAD.

**rustChip dependency**: toadStool workspace now references `../../infra/rustChip/crates/akida-chip`. This repo is biomeGate-local (not yet on Forgejo). Does not affect genomebin depot builds (neuromorphic crates are workspace-only, not in the UniBin target). **Action**: biomeGate team should push rustChip to Forgejo when ready.

---

## GATE FLEET STATUS

| Gate | NUCLEUS | Role | Key Status |
|------|---------|------|------------|
| **sporeGate** | 14/14 v4.57+ | CI / membrane | **DEPOT REBUILT** (26 bins). nestgate.io 10/12. Knot DNS. |
| **ironGate** | 10/10 v4.57+ | Downstream host | G18 LIVE. 12.7 TB CAS. footPrint LIVE. **Needs: squirrel deploy (E2)** |
| **westGate** | 14/14 v4.57 | Data NAS | 3.21 TB / 452 GB CAS. Convoy running. **Needs: nestGate TCP (O5), tideGlass cell boot (D1)** |
| **strandGate** | v4.57+ (deferred) | Compute | SU(N) 87-config grid running. Dual-GPU scan. |
| **blueGate** | 14/14 v4.57+ | Windows dev | **Sub-builder PROVEN** (15/15 Windows). ludoSpring waiting. |
| **southGate** | 13/13 v4.57+ | Validation | Re-validated. G17+G8 proven. |
| **biomeGate** | Source-built | GPU lab | Akida driver. rustChip local. 3 VFIO GPUs. |
| **golgi** | Thin relay | VPS | footprint.primals.eco routing. |

---

## DUAL-SCIENCE STATUS

### Track A: NF Drug Repurposing (Gonzales / Bin Chen)

| Component | Status | Next |
|-----------|--------|------|
| **tideGlass** | 220 tests. PetalTongueClient ACTIVATED. GPS data CONVERTED. | **D1: cell boot on westGate** → Chen 2017 benchmark |
| **footPrint** | PHASE 2 LIVE. 708 tests. petal-bridge wired. | **E2: squirrel deploy** → agent panel |
| **westGate data** | 3.21 TB. 452 GB CAS. 4-tier storage. Convoy running. | Convoy completion → bulk convergence |
| **nestGate** | 94 methods, 21 domains. Neural API wired. | **O5: TCP on westGate** → federation |
| **Provenance trio** | 7/7. 700x improvement (217/s NVMe). | Convoy running. Post-convoy: rsync hot→cold |

### Track B: Lattice QCD on Consumer GPUs (Murillo / Chuna)

| Component | Status | Next |
|-----------|--------|------|
| **strandGate** | SU(N) generalized (N=2→8). 87-config grid RUNNING. 16⁴ confirmed (6 ppm). | SU(N) data tables. 32⁴ target. |
| **hotSpring** | 652 lib tests. Config cache LIVE. | SU(2) thermalizing. SU(3)→SU(8) queued. |
| **arXiv preprint** | 42-item reviewer rubric. Murillo/Chuna/Bazavov panel. | Address 12 MUST-fix → LaTeX → send |

---

## LIVE SITES

| Site | URL | Sections | Remaining |
|------|-----|----------|-----------|
| **sporePrint** | `sporeprint.primals.eco` | LIVE | — |
| **footPrint** | `footprint.primals.eco` | LIVE (auto-loads) | squirrel UDS socket (E2) |
| **nestgate.io** | `nestgate.io` | **10/12** (health.liveness S8 just shipped) | bearDog routing stub (E1), CAS content browse |
| **esotericWebb** | `webb.primals.eco` | GET 200 / HEAD 502 | HEAD method (E3), petalTongue WebGL (G19) |

---

## K-DERM — FULLY OPERATIONAL

| Layer | Domain | Status |
|-------|--------|--------|
| Outer | `primals.eco` | LIVE — Cloudflare wildcard, 14 Caddy routes |
| Peptidoglycan | `nestgate.io` | LIVE — 20 primals, 10/12 sections, sovereign Knot DNS + DNSSEC |
| Inner | `primal.eco` | LIVE — dnsmasq, all 11 gates resolving, zero public records |

---

## CODE OWNERSHIP

| Primary Gate | Primals |
|-------------|---------|
| **sporeGate** | sweetGrass, loamSpine, rhizoCrypt |
| **biomeGate** | toadStool, barraCuda, coralReef |
| **eastGate** | bearDog, skunkBat, squirrel, sourDough, bingoCube |
| **overwatch** | biomeOS, songBird, nestGate, petalTongue, cellMembrane |

---

*Wave 156g — **Remaining Work Focus.** 14/26 debt items cleared (entire sporeGate + biomeGate backlogs DONE, nestGate upstream gaps CLOSED, nestgate.io 10/12 sections). 12 items remain: 3 ops deployments (E2 squirrel, D1 tideGlass boot, O5 nestGate TCP), 5 integration tasks (O7 inter-gate E2E, O6 scene passthrough, E3 HEAD fix, E1 bearDog stub, S9 symlink docs), 2 feature work (B3 SU(N) shaders, O2 content.fetch verify), 2 ongoing (D3 convoy, D4 thermalization). No code blockers — all remaining work is ops or integration.*

*toadStool absorbs Akida neuromorphic driver (7,755 lines, `Box<dyn NpuBackend>` trait objects, VFIO subsystem). rustChip needs Forgejo publication.*

*All 15 primals at HEAD. Depot REBUILT (26 binaries, blueGate sub-builder proven). ~140K+ tests, 15/15 GREEN.*
