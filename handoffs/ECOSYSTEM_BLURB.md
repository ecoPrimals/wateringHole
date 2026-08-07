# ecoPrimals Ecosystem Blurb — Cross-Arch + Neural API

**Date**: Aug 7, 2026 7:49AM | **Wave**: 156x | **From**: eastGate overwatch
**Posture**: **CROSS-ARCH FIRST, THEN NEURAL API LIVE.** coralReef + toadStool fixed cross-arch (3 remain: petalTongue, skunkBat, squirrel). biomeOS Neural API must go fully live for Tower atomics + composition tasks. westGate AAR absorbed: jelly string elimination + 343 GB data federation. strandGate + westGate atomic learnings feed composition patterns.

---

## CROSS-ARCH — 3 PRIMALS REMAIN

coralReef (`bdc6dbb`) and toadStool (`23d4f0a`) shipped cross-arch fixes. **12/15 now pass Windows.**

| Primal | Owner | Status | Remaining violations |
|--------|-------|--------|---------------------|
| ~~coralReef~~ | ~~biomeGate~~ | **FIXED** (`bdc6dbb`) | Zero cfg(unix) in production code |
| ~~toadStool~~ | ~~biomeGate~~ | **FIXED** (`23d4f0a`) | Transport-agnostic helpers to dispatch.rs, G65 modules gated |
| **petalTongue** | overwatch | FAILING | Test modules: `jsonrpc_integration_tests.rs`, `jsonrpc_provider/tests.rs` — wrap with `#[cfg(unix)]` |
| **skunkBat** | eastGate | FAILING | Prod: `rpc.rs` UnixStream, `tarpc_uds.rs` unix listen. Tests: 7 tarpc UDS tests |
| **squirrel** | eastGate | FAILING | `security.rs` PermissionsExt, `capability_jwt.rs` UnixListener, JWT integration tests |

**Pre-push standard**: `cargo check --target x86_64-pc-windows-gnu`

---

## NEURAL API — ACTIVATE FOR TOWER ATOMICS

biomeOS Neural API is fully built (456 tests) but not yet live as the primary routing layer. It needs to be the driver for all primal composition.

### What exists

| Component | Status | Lines | Tests |
|-----------|--------|-------|-------|
| `neural-api-server` binary | Built, not deployed as primary | 30+ | — |
| `neural_router/` | Capability routing, discovery, forwarding, perceptron, weights | ~3K+ | 150+ |
| `neural_api_server/` | Connection handling, BTSP negotiation, G65 protocol negotiation, route table, enrichment, agents | ~3K+ | 200+ |
| `neural_executor/` | Graph execution, dispatch, rollback, node impls | ~2K+ | 100+ |
| `neural_graph/` | TOML graph parsing, cross-gate support | ~1K+ | 30+ |
| `neural-api-client` + sync | Client libraries for consumers | ~800 | 40+ |

### What it does

- **Capability discovery**: Scans primal sockets, calls `capabilities.list`, builds registry
- **Routing**: `discover_capability("dag.session.create")` → resolves to rhizoCrypt socket
- **Composite atomics**: Tower (bearDog + songBird + skunkBat), Node (toadStool + barraCuda + coralReef), provenance trio
- **Forwarding**: Routes JSON-RPC calls to the right primal, with tarpc elevation
- **Graph execution**: TOML deploy graphs define composition, Neural API orchestrates

### What needs to happen

| # | Task | Owner | Impact |
|---|------|-------|--------|
| **N1** | Deploy `neural-api-server` as systemd service on sporeGate NUCLEUS | overwatch | Neural API LIVE on first gate |
| **N2** | Wire Tower atomic composition through Neural API routing | overwatch | bearDog + songBird + skunkBat routed via capability, not hardcoded sockets |
| **N3** | Wire Node atomic composition (toadStool + barraCuda + coralReef) | biomeGate | GPU/compute routed via capability |
| **N4** | Wire provenance trio (rhizoCrypt + loamSpine + sweetGrass) | sporeGate | Data braiding routed via capability |
| **N5** | squirrel agent routing through Neural API | eastGate | Agent panel uses capability discovery, not socket paths |
| **N6** | Deploy Neural API on westGate + strandGate | per-gate | Composition patterns proven on production gates |

### Learnings from strandGate + westGate

strandGate and westGate have been running atomic compositions directly (socket paths, manual wiring). Their learnings:

- **westGate jelly string elimination**: Python braiding pipeline was bypassing all primal-native RPCs. 4-30x slower, 3.8 GB RAM for sorted file lists, no cross-tier dedup. Replaced with `native_braid.py` calling `content.ingest` + `dag.pipeline.ingest` directly. **Neural API routing would have prevented this** — consumers call capabilities, not sockets, so the right Rust code path is always used.

- **strandGate compute memoization**: hotSpring → coralReef → barraCuda composition for QCD. Currently wired manually per gate config. Neural API makes this portable — same graph definition works on any gate with the right primals.

- **westGate multi-tier CAS**: nestGate warm/cold/legacy tiering. Currently one-gate. Neural API + songBird enables cross-gate CAS federation (G60) through capability routing.

---

## SEQUENCE

1. **3 code teams fix cross-arch** (petalTongue, skunkBat, squirrel)
2. **All 15 pass `cargo check --target x86_64-pc-windows-gnu`**
3. **Neural API activation** (N1-N6, parallel with depot rebuild)
4. **Depot rebuild** — musl 16/16 + Windows 15/15
5. **Single clean deploy** — all gates
6. **Springs + downstream** on composition foundation

---

## ABSORBED THIS CASCADE

| Source | What | Key detail |
|--------|------|-----------|
| coralReef `bdc6dbb` | G66 full confinement | Zero cfg(unix) in production. Cross-arch passes. |
| toadStool `23d4f0a` | Cross-arch compliance | Transport-agnostic dispatch extracted. G65 modules gated. |
| westGate AAR | Jelly string elimination | Python braiding → primal-native. 4-30x speedup. |
| westGate AAR | Data federation at 343 GB | 22 datasets, 257K+ files, Batches 1+2 complete |
| whitePaper | DF64 precision folding theory | MILC interop roadmap + β=5.9 anomaly resolved |

---

## BACKGROUND

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | 343 GB federation. AlphaFold tiering. native_braid deployed. | Running |
| **strandGate** | SU(N) grid. arXiv 40/42. Observable battery 69/69. | Running |
| **whitePaper** | petalTongue-native figures. DF64 theory. Reviewer critique response. | Evolving |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| G64 + G65 + G66 | **COMPLETE** |
| Cross-arch (Windows) | **12/15 pass** — 3 remain (petalTongue, skunkBat, squirrel) |
| Neural API | **456 tests, not yet deployed as primary routing** |
| Musl depot | **16/16 on golgi** |
| sporeGate health | **12/13 alive** |
| westGate data | **343 GB, 22 datasets, 257K+ files** |
| Primal tests | **~140,000+** |
| arXiv | **40/42 (95%)** |

---

*Wave 156x — **CROSS-ARCH + NEURAL API.** coralReef + toadStool fixed (12/15 Windows). 3 remain: petalTongue, skunkBat, squirrel. Neural API activation planned (N1-N6) — 456 tests, full capability routing, composite atomics, graph execution. westGate jelly string elimination absorbed. strandGate + westGate atomic learnings feed composition patterns. Fix cross-arch → activate Neural API → rebuild depot → deploy everywhere. 14 COMPLETE / 25 ACTIVE / 23 GLACIAL. 62 goals. 15/15 GREEN.*
