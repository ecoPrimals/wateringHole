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
| **toadStool** | WASM + cross-arch | S371: 24/48 crates WASM-capable (50% kernel). Natural `core` 272K split continuing. Extends platform abstraction as Node Atomic hw-safe owner. |
| **swarmVine** | Data + compute gossip | **Windows port P2** — handoff filed (`SWARMVINE_WINDOWS_PORT_HANDOFF.md`): 4 UDS call sites need transport abstraction, tarpc needs `#[cfg(unix)]` gating. Phase 3 integration: data gossip + compute gossip. |
| **biomeOS** | Neural API production | P0-C fix in code, needs depot rebuild. Next: provenance graph templates, `capability.call` fleet-wide deployment, Phase 2 riboCipher Tier 2 evolution. |
| **bearDog** | Crypto surface | P0-A code-fixed. Depot rebuild unblocks spine commit signing on westGate. Next: `decode_mito_tag` as Neural API capability for riboCipher Tier 2. |
| **cellMembrane** | Membrane evolution | G69 Depot Lineage: `depot.prune` (Phase 1), lineage metadata (Phase 2), CAS archival (Phase 3). `native_braid.py` → Rust. Convergent pattern with data braids. |
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
| **strandGate** | Compute + silicon | SU(4+) thermalization (12 configs remaining). DF64 precision experiments. NPU metalforge phase classification. |
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
| **strandGate** | **13/13 ALIVE** | AMD DF64 > NVIDIA (24.1 vs 18.1 TFLOPS). ROP 7.4x. NPU <2W. 75/87 therm. |
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
| Tests | **~142K+** across 16 primals |

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

*Wave 157d — Depot unified + pruned (60 primal binaries, 4 arches). G69 Depot Lineage spec published: binary evolution via provenance trio (same CAS/spine/braid pattern as data braids). Scope boundary enforced: topology owns depot pipeline + specs, primal teams own internals. swarmVine Windows port handoff filed. 16 primals. 0 P0. ~142K+ tests.*
