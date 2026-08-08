# ecoPrimals Ecosystem Blurb — Wave 157a NEURAL API DISPATCH FIXED + PROVENANCE TRIO PROVEN

**Date**: Aug 8, 2026 5:50PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **NEURAL API DISPATCH REORDER SHIPPED. 990K FILES BRAIDED INLINE. SWARMVINE WIRED.** biomeOS dispatch reorder (`44c40191`): translation registry before Tower relay — 15s timeout eliminated. Routing gaps fixed (`6f60cccf`): braid.* direct routes, riboCipher pool shipped. westGate proves provenance trio: 990,500 files braided inline (rsync→BLAKE3→CAS→DAG→spine→braid), 2,464 persistent sweetGrass braids, all 26 caps resolve. swarmVine epidemic spread + songBird seam wired. 17 COMPLETE / 21 ACTIVE / 26 GLACIAL (64 goals). N2-N5 verification next.

---

## EXECUTION SUMMARY — eastGate overwatch (this session)

### swarmVine Phase 2 — Epidemic Spread WIRED
- **Epidemic sweep loop** (`spread.rs`): 30s interval drain of forward queue → batch `gossip.spread` to all mesh peers via TCP + riboCipher (`0xEC 0x01`)
- **Cross-gate TCP listener**: `:7800` (configurable `--gossip-port`), reuses `server.rs` riboCipher connection handler
- **Tiered peer discovery**: `SWARMVINE_PEERS` environment variable (direct) + songBird `mesh.peers` UDS query (dynamic, extracts IP + assumes default gossip port)
- **CLI args**: `--spread-interval` (default 30s), `--gossip-port` (default 7800)
- **39/39 tests passing** (12 core + 21 server + 6 spread)
- **sourDough re-validated**: riboCipher FULL, Neural API FULL, G68

### songBird Seam — `ipc.register` → swarmVine `gossip.inject`
- **Commit `6b580cf0`**: When any primal registers capabilities via `ipc.register`, songBird now fires a `gossip.inject` to the local swarmVine instance
- **Fire-and-forget**: both paths run in parallel (songBird announce + swarmVine gossip). If swarmVine not deployed, silently skipped
- **Gate identity**: resolved from `GATE_ID` or `HOSTNAME` env (matches swarmVine's own pattern)
- **Gossip key format**: `capability.advertise:{gate}:{primal}` under `tower` topic
- **songBird tests**: 53 tests, zero regressions

### biomeOS Neural API — Dispatch Reorder + Routing Gaps SHIPPED
- **Dispatch reorder** (`44c40191`): translation registry checked before Tower relay. Eliminates 15s timeout for all registered capabilities. New order: signal graph → translation → Tower relay → direct.
- **Routing gaps** (`6f60cccf`): braid.* direct routes to sweetGrass (6 methods). convergence.* to primalSpring. Router timeout: 30s→15s (was using eviction interval). composition.test_swap socket → membrane dir (fixes PrivateTmp Permission denied).
- **riboCipher pool** shipped: dual lane (plain + riboCipher). `send_ribocipher_jsonrpc()` for G68 primals.
- **Bootstrap→Coordinated auto-transition**: background probe loop, no manual intervention needed.
- **TOML-driven capability translations**: `capability_registry.toml` loaded at runtime, compiled defaults are cold-start fallback only.

### westGate Provenance Trio — 990,500 Files Braided Inline
- **Inline braiding proven**: rsync phase → `native_braid.py --incremental` → BLAKE3 → CAS → DAG batch → spine commit → braid. No data lands without provenance.
- **990,500 files** braided (324 AlphaFold + 989,423 structures + 753 SRA FASTQ), 240 Merkle roots, 24,336 dedup hits
- **sweetGrass**: 2,464 braids in persistent store (survives restart — only persistent provenance anchor)
- **riboCipher enforcement**: G68 sweetGrass + rhizoCrypt reject plain JSON-RPC. 2-byte `[0xEC 0x01]` prefix mandatory.
- **songBird capability resolution**: all 26 capabilities across 5 provenance primals resolve correctly
- **Gap identified**: biomeOS `capability.call` needs riboCipher-aware dispatch for sweetGrass/rhizoCrypt (pool exists but auto-detect not wired)

### Prior this session
- **swarmVine v0.1.0 budded** — sourDough scaffold, 3 gossip domains, 33/33 tests, depot + golgi
- **6/6 gates redeployed** — all confirmed
- **Inner Membrane Phase 1 DONE** — songBird mesh gap fixed

---

## GATE STATUS — 6/6 COMPLETE

| Gate | Status | RSS | Key evolution |
|------|--------|-----|---------------|
| **sporeGate** | 13/13 ALIVE | — | S370 depot, cascade auto-push, zero drift |
| **blueGate** | 13/13 ALIVE | 264 MB | Windows 15/15, sub-builder ready |
| **southGate** | 13/13 ALIVE | 96 MB | 0.058ms Tower, SSH compliant |
| **ironGate** | 13/13 ALIVE | 41 MB | 2,058 capabilities, 42 repos clean |
| **strandGate** | 13/13 ALIVE | 127 MB | GPU Lanczos at machine epsilon, 75/87 thermalization cached, NPU VFIO-bound |
| **westGate** | 13/13 ALIVE | — | NG-05 done, 26 caps registered, 2.5 TB CAS |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** (swarmVine Phase 2 wired + songBird seam) |
| NUCLEUS gates | **6/6 redeployed** |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| Golgi depot | Musl **18/18** (swarmVine added), Windows **15/15** |
| Cascade | synced=15, zero drift, auto-push confirmed |
| SSH discipline | **ENFORCED** — all gates compliant |
| Trust surfaces | 3 routes live on nestgate.io |
| Primal drift | **zero** |
| Ownership | primalSpring → hardware cascade, overwatch → orchestration |

---

## WHAT'S CLOSED (cumulative)

| Gap | Status |
|-----|--------|
| Gate redeploy 6/6 | **DONE** |
| NG-05 westGate CAS federation | **DONE** — 26 caps, 2.5 TB |
| strandGate depot access + NUCLEUS | **DONE** — SSH + Forgejo + 14 services |
| `plasmid.fetch --source forgejo` | **DONE** — cellMembrane `55fdff3` |
| nestgate.io trust surfaces | **DONE** — 3 routes live |
| Cascade golgi auto-push | **DONE** — confirmed in logs |
| SSH discipline all gates | **DONE** — zero github remotes |
| QCD pseudoSpore bundle | **DONE** — lithoSpore v1.0.0-rung1 |
| toadStool S370 depot | **DONE** — rebuilt + pushed |
| swarmVine budded | **DONE** — v0.1.0 epidemic gossip engine, primal #16, depot + golgi |
| swarmVine Phase 2 wired | **DONE** — epidemic sweep loop + cross-gate TCP :7800 + tiered peer discovery |
| songBird seam | **DONE** — `ipc.register` → swarmVine `gossip.inject` (`6b580cf0`) |
| biomeOS dispatch reorder | **DONE** — translation before Tower relay, 15s timeout eliminated (`44c40191`) |
| biomeOS routing gaps | **DONE** — braid.* routes + 30s→15s timeout + composition socket (`6f60cccf`) |
| biomeOS riboCipher pool | **DONE** — dual lane dispatch, `send_ribocipher_jsonrpc()` |
| westGate inline braiding | **DONE** — 990,500 files braided, 2,464 sweetGrass braids persistent |
| Inner membrane Phase 1 | **DONE** — songBird mesh gap fixed, spec filed |

---

## REMAINING

### sporeGate/eastGate overwatch owns
- ~~westGate mesh connectivity~~ **DONE** — `SONGBIRD_LOCAL_PEERS` seeding, westGate now in songBird mesh (LAN, reachable)
- ~~strandGate mesh isolation~~ **DONE** — 1 peer → 5 peers via LAN seeding
- ~~Inner membrane spec~~ **DONE** — `INNER_MEMBRANE_PURE_PRIMALS_SPEC.md` filed
- **nestgate.io data braids vs westGate CAS** — now UNBLOCKED (westGate in mesh). Wire via Tower Atomic, not SSH.
- **southGate mesh enrollment** — not discoverable on LAN, deferred
- **coralReef BLAKE3 checksum** stale on golgi depot — regenerate after next rebuild

### primalSpring owns (hardware cascade)
- eastGate temporal cascade to all gates
- NUCLEUS deployment lifecycle

### swarmVine integration (all teams — Phase 3)
- ~~**songBird team**: Wire `ipc.register` → swarmVine `gossip.inject` seam~~ **DONE** (`6b580cf0`)
- **skunkBat team**: Wire `metadata.analyze` as pre-accept validator for gossip entries (vine-bat loop)
- **biomeOS team**: Wire `capability.resolve` → swarmVine gossip table (cross-gate capability discovery without broadcast)
- **nestGate/loamSpine**: Inject data gossip entries (`cas.have`, `braid.head`) into swarmVine on content changes
- **toadStool/coralReef**: Inject compute gossip entries (`compute.capacity`, `build.queue`) on resource changes
- **All gates**: Deploy swarmVine to NUCLEUS (binary in depot, epidemic spread + TCP listener ready)

### Other teams own
- **sporePrint**: ~~SU(2)→SU(N) relabel~~ **DONE**. QCD download pages, LaTeX preprint
- **primalSpring**: Neural API N2-N5 verification (dispatch reorder unblocks). riboCipher-aware dispatch auto-detect for sweetGrass/rhizoCrypt
- **toadStool**: Long-tail cross-arch + WASM compute (S371: 24/48 crates, 50% kernel)
- **cellMembrane**: `native_braid.py` → Rust
- **projectNUCLEUS**: workloads/ → spring repos, specs → wateringHole
- **All primals**: Self-register capabilities with songBird on startup (upstream from westGate pattern)
- **skunkBat**: `PRIMAL_BIND_MODE` env var (P3, Windows)
- **petalTongue**: `--port` in server mode (P4, Windows)

### arXiv blockers (41/42) — 4/5 closed
1. ~~pseudoSpore bundle~~ **DONE** (lithoSpore)
2. ~~SU(2)→SU(N) relabel~~ **DONE** (sporePrint `3e037fe`)
3. ~~`/pseudospore/` route~~ **DONE** (petalTongue)
4. `validate.sh` — bundle-specific BLAKE3 + DAG + Ed25519 verification + freeze/sign v1.0.0-rung1
5. Reviewer send (Murillo, Chuna, Bazavov)

---

*Wave 157a Neural API dispatch reorder + provenance trio proven. biomeOS: dispatch reorder (translation before Tower relay), routing gaps (braid.* routes, 30s→15s timeout), riboCipher pool (dual lane). westGate: 990,500 files braided inline, 2,464 sweetGrass braids persistent, 26 caps resolve. swarmVine Phase 2 wired + songBird seam LIVE. G34→GLACIAL. 17 COMPLETE / 21 ACTIVE / 26 GLACIAL. 16 primals. arXiv 4/5 closed.*
