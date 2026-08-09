# ecoPrimals Ecosystem Blurb — Wave 157d DEPOT UNIFIED + G69 LINEAGE SPEC

**Date**: Aug 9, 2026 5:10PM | **Wave**: 157d | **From**: sporeGate topology
**Posture**: **ZERO P0. DEPOT UNIFIED + PRUNED. G69 DEPOT LINEAGE SPEC PUBLISHED.** Depot cleaned (test/demo binaries pruned, 60 primals-only across 4 arches). G69 specification published: binary evolution tracked via provenance trio — same CAS/spine/braid pattern as data braids. Scope boundary enforced: topology owns depot pipeline + specs, primal teams own their internals. swarmVine Windows port handoff filed (not implemented by topology).

---

## WHAT'S SOLVED (infrastructure phase complete)

| System | Status | Evidence |
|--------|--------|----------|
| **All P0s** | **RESOLVED** | P0-A bearDog (`766951004`), P0-B nestGate (stale depot), P0-C biomeOS FD (`6a51638d`). Depot rebuild deploys. |
| **Build system** | **MESH-NATIVE** | blueGate `builder.serve :9800` — Tower Atomic dispatch, no SSH. 14/14 vertebrate built (23 min). Authorities: `[blueGate, sporeGate, eastGate]`. |
| **Depot** | **UNIFIED + PRUNED** | golgi: musl 19, windows-gnu 16, gnu 16, aarch64 13. BLAKE3SUMS all arches. 60 primal binaries (test/demo/bench pruned). G69 lineage spec published. 13,910 caps on sporeGate. |
| **Neural API** | **CALL PATH UNBLOCKED** | P0-C fixed. `capability.resolve` (7ms) + `capability.call` (1 pooled conn per forward). Both paths operational. |
| **G68 Platform** | **16/16 COMPLETE** | 205→0 production violations. 16/16 cross-arch. |
| **Gates** | **6/6 NUCLEUS** | All v4.57+ G68-converged. Vine-bat operational. 11 mesh peers. |
| **Cascade** | **ZERO DRIFT** | 15min auto-cascade, auto-push, auto-harvest. |
| **SSH discipline** | **ENFORCED** | Zero github remotes. K-Derm relay chain: gate → Forgejo → pepti → golgi-ext → GitHub. |

---

## NEXT EVOLUTION — WHAT EACH TEAM WORKS ON

### Primal evolution (vertebrate phase — lean by evolution)

| Team | Domain | Next Work |
|------|--------|-----------|
| **songBird** | Transport convergence | `CanonicalTransport` trait shipped (`33e9a8be`). Converge remaining 9 transport crate impls behind the shared interface. Formally excise gossip methods to swarmVine. |
| **petalTongue** | Rendering focus | `doom-core` decoupled (`87a2530`). Extract to **ludoSpring** when spring is scaffolded. WebGL pipeline for esotericWebb browser surface (G19). Fix `--port` flag in server mode (P4, filed twice). |
| **toadStool** | WASM + cross-arch + silicon registry | S371: 24/48 crates WASM-capable. **Node Atomic AAR**: query coralReef `shader.compile.capabilities` for silicon registry. Absorb `silicon_capability_registry` from silicon fold. Dispatch descriptor wiring already consuming `shader_info`. |
| **swarmVine** | Data + compute gossip | **Windows port P2** — handoff filed (`SWARMVINE_WINDOWS_PORT_HANDOFF.md`): 4 UDS call sites need transport abstraction, tarpc needs `#[cfg(unix)]` gating. Phase 3 integration: data gossip + compute gossip. |
| **barraCuda** | GPU compute | **Silicon Fold ABSORBED** (`9222193c`): 5 new abstractions (NegotiatedLimits, SiliconRouter, TileDecomposer, RiverScheduler, VideoCodec). Buffer limit 512M→1G for 32⁴ lattices (`9f3856d7`). Self-audit clean. 5,025 tests. **Next**: wire `CoralReefDevice` → coralReef `shader.compile.wgsl` IPC. |
| **coralReef** | GPU compiler | **Node Atomic AAR filed**: 18/18 IPC methods LIVE. Compute Trio wire contract tested. `Fp64Strategy` precision routing delivered. Integer subgroup fix shipped (`2b433e9`). 3,702 tests. Remaining: GEMM tiling Phase 1 (2-3 weeks), vertex/fragment shaders (8-12 weeks). |
| **biomeOS** | Neural API production | P0-C fix **IN DEPOT** — `capability.call` fleet-wide operational. Next: provenance graph templates, Phase 2 riboCipher Tier 2 evolution. |
| **nestGate** | CAS surface | P0-B **IN DEPOT**. `content.stat` SHIPPED (`4cafa535`). Self-audit: `dataset.convergence` announce gap fixed. |
| **loamSpine** | Spine surface | Self-audit: 54/54 JSON-RPC + 37/37 tarpc verified (`c3c6c0f`). `persist_tip()` abstraction (18 call sites → 1 helper). Signing path ready for bearDog. |
| **rhizoCrypt** | DAG surface | Self-audit (`920ac8b`): `dag.session.tree_hash` undeclared → added. `lifecycle.status` phantom → removed. 40 methods. Zero phantoms. |
| **bearDog** | Crypto surface | P0-A **IN DEPOT**. Spine commit signing unblocked. Next: `decode_mito_tag` as Neural API capability for riboCipher Tier 2. |
| **cellMembrane** | Membrane evolution | G69 `depot.prune` **SHIPPED** (`1e9d32b`): registry-driven depot cleanup, `--dry-run`, BLAKE3SUMS regen. Deep debt (`18e5cdb`): 14 port hardcodes → constants, IP literals → constants, self-knowledge purged, zero clippy. 1,347 tests. Next: lineage metadata (Phase 2), `native_braid.py` → Rust. |
| **sourDough** | Primal factory | `rpc-surface` audit tool shipped (`aa1a2f8`). All primals should self-audit against `capability_registry.toml` using this tool. |
| **squirrel** | Agent surface | C8 done (-67K lines). G18 LIVE on ironGate (9 providers). Next: footPrint agent panel wiring (WebSocket → petal → squirrel). |

### Spring/garden evolution (science + product work)

| Team | Domain | Next Work |
|------|--------|-----------|
| **hotSpring** | QCD compute | arXiv Rung 1: 41/42 items done. Wire `validate.sh` + pseudoSpore + reviewer send. Rung 2 (quenched fermions) queued. |
| **tideGlass** | NF drug reversal | Phase 0: Zenodo inventory + RGES reproduction. Cell boot on westGate. GPS data converted. |
| **esotericWebb** | CRPG engine | V32 CELL LIVE on ironGate (484+ tests). Needs petalTongue WebGL pipeline (G19) for browser surface. |
| **footPrint** | GIS surface | Phase 2 on ironGate. `petal-bridge.ts` wired. Matures petalTongue G19. |
| **sporePrint** | Public surface | QCD download pages, LaTeX preprint, live science refresh. |

### Gate operations (deploy + hardware)

| Team | Domain | Next Work |
|------|--------|-----------|
| **sporeGate** | Topology owner | G69 Depot Lineage spec published. Depot relay + pruning operational. Scope: depot pipeline, manifests, gate enrollment, specs. Does NOT implement primal internals. |
| **blueGate** | Primary builder | golgi SSH key AUTHORIZED. Depot push live. BLAKE3SUMS generated. swarmVine Windows port handoff filed (primal team scope). |
| **strandGate** | Compute + silicon | **SILICON FOLD AAR**: 15/15 units accessible and measured. AMD 20x root cause found (IC vs L2 working set thrashing). F16 1.32x on AMD (free). RT Cores live (22x NVIDIA). 250-2500x MILC for stencil. Cross-GPU pipeline 0.16% overhead. Upstream: barraCuda absorbs `RiverScheduler`+`TileDecomposer`+`VideoCodec`+buffer negotiation. toadStool absorbs `silicon_capability_registry`. |
| **westGate** | Data NAS | `native_braid.py` → Rust. Spine commit signing once bearDog depot ships. |
| **primalSpring** | eastGate hardware | Owns temporal cascade to all gates. NUCLEUS deployment lifecycle. Neural API experimentation + evolution guidance. |

---

## GATE STATUS — 6/6 NUCLEUS

| Gate | Status | Key evolution |
|------|--------|---------------|
| **sporeGate** | **15/15 ALIVE** | Topology owner, fallback builder. 13,910 caps. Vine-bat + gossip resolve operational. |
| **blueGate** | **13/13 ALIVE** | **PRIMARY BUILDER** — 14/14 vertebrate (23 min), mesh-native dispatch :9800. |
| **southGate** | **13/13 ALIVE** | Validation gate. 0.058ms Tower. G17 + G8 proven. |
| **ironGate** | **13/13 ALIVE** | Downstream host. G18 LIVE. esotericWebb V32 CELL. RTX 5070. 12.7 TB CAS. |
| **strandGate** | **13/13 ALIVE** | **SILICON FOLD + NODE ATOMIC AAR**: 15/15 units, AMD 20x (IC vs L2). coralReef 18/18 IPC live. Integer subgroup fix shipped. |
| **westGate** | **13/13 ALIVE** | Data NAS. 3.3 TB / 989K files braided. 2.5 TB CAS federated. |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** |
| NUCLEUS gates | **6/6** (all v4.57+ G68-converged) |
| P0 / P1 / P2 | **0 / 1 / 2** (P1: FD exhaustion on 5 gates. P2: songBird PID, petalTongue port) |
| Golgi depot | **4-arch unified + pruned**: musl 19, windows-gnu 16, gnu 16, aarch64 13. **BLAKE3SUMS all arches.** 60 primal binaries. G69 lineage spec published. |
| Build system | **Mesh-native** (blueGate primary, sporeGate fallback, eastGate tertiary) |
| Cascade | **Zero drift**, 15min auto-cascade |
| songBird mesh | **11 peers** across 7 gates |
| Caps registered | **13,910** (up from 1,987 pre-vertebrate) |
| Tests | **~145K+** across 16 primals (barraCuda 5,025, coralReef 3,702, cellMembrane 1,347 updated) |

---

## REMAINING BLOCKERS

### Immediate — RESOLVED
- ~~**biomeOS P0-C depot rebuild**~~ — **IN DEPOT** (0 stale primals). Deployed fleet-wide.
- ~~**bearDog P0-A depot rebuild**~~ — **IN DEPOT** (0 stale primals). Deployed fleet-wide.
- ~~**blueGate → golgi push**~~ — **SOLVED.** golgi SSH key authorized (both `id_ed25519` and `id_ed25519_ecoPrimal`). blueGate can `scp` directly or relay via sporeGate LAN→WAN. 66 Windows binaries now on golgi.

### P1 / P2 debt
- **P1: FD exhaustion** — `LimitNOFILE=65536` NOT applied on: westGate, strandGate, blueGate, southGate, eastGate.
- **P2: songBird PID management** — 3 path changes in 3 waves. No liveness check. No cleanup on exit. (blueGate D1)
- **P2: petalTongue `--port` in server mode** — filed twice, still ignored. (blueGate D4)
- **P2: swarmVine Windows port** — handoff filed (`SWARMVINE_WINDOWS_PORT_HANDOFF.md`). 4 call sites + tarpc gating. Primal team scope, not topology. (blueGate filed)
- **P3: Binary size parity** — 4/14 Windows builds oversized (barraCuda 4.4x from workspace bloat). (blueGate D3)

### Glacial
- **arXiv**: `validate.sh` + reviewer send. 41/42.
- **aarch64-musl depot**: 13/19, partially stale. No ARM64 gates active.
- **southGate mesh enrollment**: not discoverable on LAN.
- **steamGate + darwinGate**: future platform gates.

---

*Wave 157d — barraCuda Silicon Fold ABSORBED (5 device abstractions, buffer fix, 5,025 tests). Provenance trio self-audited clean (loamSpine 91/91 methods, nestGate content.stat shipped, rhizoCrypt 40/40 zero phantoms). coralReef 18/18 IPC + integer fix. cellMembrane G69 depot.prune SHIPPED. All vertebrate self-audits converging. 16 primals. 0 P0. ~145K+ tests.*
