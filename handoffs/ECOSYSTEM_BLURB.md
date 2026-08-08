# ecoPrimals Ecosystem Blurb — Wave 157a N2-N5 VERIFIED + DEPOT REBUILD IS THE GATE

**Date**: Aug 8, 2026 6:45PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **N2-N5 VERIFIED (87/91). RIBOCIPHER AUTO-DETECT SHIPPED. DEPOT REBUILD IS THE GATE.** primalSpring verified dispatch fix: 1.3ms mean (was 15s), 9/11 primals forward. biomeOS riboCipher auto-detect shipped (`1ff5859c`): sweetGrass/rhizoCrypt auto-route through riboCipher pool. cellMembrane transport unification: `#[cfg(unix)]` 7→3. **Critical path**: depot rebuild (current binary is Jul 15 pre-fix) → gate redeploy → fleet-wide Neural API activation. 17 COMPLETE / 21 ACTIVE / 26 GLACIAL (64 goals).

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

### primalSpring N2-N5 Verification — DISPATCH FIX PROVEN
- **exp118 (Graph Execution)**: **14/14** (was 6/12). graph.list, graph.execute, graph.status all work
- **exp119 (PathwayLearner)**: **12/12**. 919 exec/s throughput
- **exp120 (Self-Registration)**: **29/29**. 34 caps, 58 methods, 11/11 domains resolve
- **exp121 (riboCipher Auto-Detect)**: **32/36**. 9/11 primals forward. sweetGrass FAIL (riboCipher-only), toadStool FAIL (TARPC mismatch)
- **Dispatch latency**: 15,000ms → **1.3ms mean, 2.5ms max**
- **Acceptance test**: exp121 goes 32/36→36/36 once depot binary includes riboCipher auto-detect fix

### biomeOS riboCipher Auto-Detect — sweetGrass/rhizoCrypt Gap CLOSED
- **Commit `1ff5859c`**: domain-level `ribocipher: bool` in `capability_registry.toml`
- **TOML inheritance**: domain flag auto-propagates to all translations (entry-level override supported)
- **Affected domains**: `attribution` (sweetGrass: provenance.*, braid.*) + `ephemeral_workspace` (rhizoCrypt: dag.*)
- **Dispatch**: checks `trans.ribocipher` → auto-uses `forward_request_ribocipher()` for both initial + self-healing retry
- **Impact**: westGate 990K inline braiding can now route through Neural API without bypass

### cellMembrane Transport Unification
- **Commit `f5033f2`**: G66 TransportStream graduation, jsonrpc.rs `#[cfg(unix)]` 7→3
- **Shared helpers**: `rpc_over_stream()` + `notify_over_stream()` — UDS + TCP share one implementation
- **Dead code cleanup**: `CommitPayload`, `PushEvent.commits` `#[allow(dead_code)]` removed
- **Hardcode elimination**: `security.sock` → registry lookup, `webhook.sock` → `WEBHOOK_SOCKET_NAME` constant
- **1,329 tests**, zero regressions

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
| Primals | **16** (N2-N5 verified, dispatch 1.3ms) |
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
| biomeOS dispatch reorder | **DONE** — translation before Tower relay, 15s→1.3ms (`44c40191`) |
| biomeOS routing gaps | **DONE** — braid.* routes + 30s→15s timeout + composition socket (`6f60cccf`) |
| biomeOS riboCipher auto-detect | **DONE** — domain-level TOML flag, sweetGrass/rhizoCrypt auto-route (`1ff5859c`) |
| N2-N5 verification | **DONE** — 87/91 (exp118-121). 9/11 primals forward. sweetGrass needs redeploy, toadStool TARPC |
| cellMembrane transport unification | **DONE** — `#[cfg(unix)]` 7→3, TransportStream, 1,329 tests (`f5033f2`) |
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
- ~~**primalSpring**: N2-N5 verification~~ **DONE** (87/91). Remaining: toadStool TARPC shim (architecture decision)
- **sporeGate**: **DEPOT REBUILD** — current binary is Jul 15 pre-dispatch-fix. Must rebuild with `44c40191` + `6f60cccf` + `1ff5859c` for fleet-wide activation
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

*Wave 157a N2-N5 verified (87/91, 1.3ms dispatch). biomeOS riboCipher auto-detect shipped (`1ff5859c`). cellMembrane transport unification (7→3 cfg). Critical path: depot rebuild (Jul 15 binary) → gate redeploy → fleet-wide activation. swarmVine Phase 2 + songBird seam. 17 COMPLETE / 21 ACTIVE / 26 GLACIAL. 16 primals. arXiv 4/5 closed.*
