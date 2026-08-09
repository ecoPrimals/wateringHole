# ecoPrimals Ecosystem Blurb — Wave 157a EVOLUTIONARY STREAMLINING

**Date**: Aug 9, 2026 8:22AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **FLEET UNBLOCKED. EVOLUTIONARY STREAMLINING UNDERWAY.** P0 fixed (songBird 24 MB). Vine-bat operational. Gossip resolve live (`2fae9144`, 1,987 caps). **Lean by evolution**: songBird 9 transport crates converging behind shared `Transport` trait (any comms, lightweight). petalTongue doom-core moving to `ludoSpring` (game rendering belongs in a spring). toadStool `core` 272K splitting naturally via S371 WASM. No feature-gating — code moves to its right home.

---

## EXECUTION SUMMARY — sporeGate overwatch (this session)

### DEPOT REBUILD — Critical Path CLEARED
- **Cascaded from Forgejo**: all 16 primals + wateringHole pulled, zero drift
- **swarmVine Phase 2 pulled**: `7532c2b` (epidemic sweep loop + cross-gate TCP :7800 + tiered peer discovery)
- **5 primals rebuilt to musl**:
  - **biomeOS** v4.57.0 (21 MB) — dispatch reorder `44c40191`, routing `6f60cccf`, riboCipher auto-detect `1ff5859c`
  - **songBird** v0.2.1 (24 MB) — swarmVine seam `6b580cf0` + seam fix `af0d8fa8`
  - **cellMembrane** (17 MB) — transport unification `f5033f2`, `#[cfg(unix)]` 7→3
  - **swarmVine** Phase 2 (2.5 MB) — epidemic spread loop, cross-gate TCP listener, tiered peer discovery
  - **petalTongue** (rebuilt) — `/api/content/federation` endpoint `84e6e48`
- **Golgi pushed**: 19/19 musl binaries + BLAKE3SUMS synced

### NUCLEUS REDEPLOY — 15/15 ALIVE
- **biomeOS FD exhaustion**: fixed with `LimitNOFILE=65536` in systemd unit (also neural-api)
- **All 15 services alive**

### songBird Seam Fix — Socket Discovery + Gate Identity
- **Root cause 1**: `discover_swarmvine_socket()` looked in wrong paths — swarmVine runs at `/run/membrane/swarmvine-*.sock`
- **Root cause 2**: Gate identity from `GATE_ID`/`HOSTNAME` — neither set in systemd
- **Fix** (`af0d8fa8`): Globs `/run/membrane/swarmvine-*.sock`, falls back to `MEMBRANE_GATE_NAME`
- **Proof**: `gossip.inject` fires, swarmVine ingests `capability.advertise:sporeGate:{primal}` into tower gossip table

### petalTongue Data Braids Federation
- **New endpoint** (`84e6e48`): `/api/content/federation` — combines local CAS stats + swarmVine data-topic gossip
- **Transport**: Tower Atomic (no SSH for cross-gate content discovery)
- **Auto-populates**: when loamSpine/sweetGrass inject `cas.have`/`braid.head` gossip entries

### BLAKE3 Depot Integrity
- **BLAKE3SUMS regenerated**: 18/18 primal binaries hashed with b3sum, pushed to golgi

### Prior this session (eastGate overwatch)
- **swarmVine Phase 2 wired** — epidemic sweep, TCP :7800, peer discovery
- **songBird seam** (`6b580cf0`) — `ipc.register` → swarmVine `gossip.inject`
- **biomeOS riboCipher TOML loading fix** (`d1f555e7`) — startup path fixed, 430 entries
- **skunkBat vine-bat loop** (`e602e09`) — 8-check gossip pre-accept validation, 672 tests
- **biomeOS riboCipher auto-detect** (`1ff5859c`) — sweetGrass/rhizoCrypt auto-route
- **cellMembrane transport unification** (`f5033f2`) — `#[cfg(unix)]` 7→3
- **N2-N5 verified** — 90/91 (sweetGrass FIXED). toadStool TARPC only remaining
- **swarmVine v0.1.0 budded** — primal #16
- **6/6 gates redeployed**
- **Inner Membrane Phase 1 DONE** — songBird mesh gap fixed

---

## GATE STATUS — 6/6 COMPLETE

| Gate | Status | RSS | Key evolution |
|------|--------|-----|---------------|
| **sporeGate** | **15/15 ALIVE** | — | **DEPOT REBUILT** (Aug 8), seam fix live, 1,958 caps, FD limit fixed |
| **blueGate** | 13/13 ALIVE | 264 MB | Windows 15/15, sub-builder ready |
| **southGate** | 13/13 ALIVE | 96 MB | 0.058ms Tower, SSH compliant |
| **ironGate** | 13/13 ALIVE | 41 MB | 2,058 capabilities, 42 repos clean |
| **strandGate** | 13/13 ALIVE | 127 MB | GPU Lanczos at machine epsilon, 75/87 thermalization cached |
| **westGate** | 13/13 ALIVE | — | NG-05 done, 26 caps registered, 2.5 TB CAS |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** (N-series 90/91, dispatch 4ms) |
| NUCLEUS gates | **6/6 redeployed** (sporeGate depot rebuilt) |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| Golgi depot | Musl **19/19** (rebuilt Aug 8 + BLAKE3SUMS), Windows **15/15** |
| Cascade | synced=16, zero drift, auto-push confirmed |
| SSH discipline | **ENFORCED** — all gates compliant |
| Trust surfaces | 3 routes + federation endpoint on nestgate.io |
| songBird mesh | **11 peers** across 7 gates |
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
| swarmVine budded | **DONE** — v0.1.0 epidemic gossip engine, primal #16 |
| swarmVine Phase 2 wired | **DONE** — epidemic sweep loop + cross-gate TCP :7800 + tiered peer discovery |
| songBird seam | **DONE** — `ipc.register` → swarmVine `gossip.inject` (`6b580cf0`) |
| biomeOS dispatch reorder | **DONE** — translation before Tower relay, 15s→1.3ms (`44c40191`) |
| biomeOS routing gaps | **DONE** — braid.* routes + timeout + composition socket (`6f60cccf`) |
| biomeOS riboCipher auto-detect | **DONE** — domain-level TOML flag, sweetGrass/rhizoCrypt auto-route (`1ff5859c`) |
| N2-N5 verification | **DONE** — 90/91 (sweetGrass FIXED by `d1f555e7`). toadStool TARPC only |
| riboCipher TOML loading bug | **DONE** — `d1f555e7` TOML-first (430 entries), domain-level check in direct fallback |
| skunkBat vine-bat loop | **DONE** — `metadata.analyze` 8-check gossip pre-accept (`e602e09`), 672 tests |
| cellMembrane transport unification | **DONE** — `#[cfg(unix)]` 7→3, TransportStream, 1,329 tests (`f5033f2`) |
| westGate inline braiding | **DONE** — 990,500 files braided, 2,464 sweetGrass braids persistent |
| Inner membrane Phase 1 | **DONE** — songBird mesh gap fixed, spec filed |
| **DEPOT REBUILD** | **DONE** — biomeOS, songBird, cellMembrane, swarmVine, petalTongue rebuilt to musl (Aug 8), golgi 19/19 |
| **biomeOS FD exhaustion** | **DONE** — LimitNOFILE=65536, 1,958 caps registered clean |
| **songBird seam fix** | **DONE** — socket discovery + MEMBRANE_GATE_NAME fallback (`af0d8fa8`), gossip.inject proven live |
| **nestgate.io data braids federation** | **DONE** — `/api/content/federation` endpoint, Tower Atomic transport (`84e6e48`) |
| **BLAKE3 depot integrity** | **DONE** — 18/18 hashed, BLAKE3SUMS pushed to golgi |
| **skunkBat PRIMAL_BIND_MODE** | **DONE** — accepts short forms tcp/uds/both (`a57ada5`) |

---

## REMAINING

### sporeGate/eastGate overwatch owns
- ~~DEPOT REBUILD~~ **DONE**
- ~~biomeOS FD exhaustion~~ **DONE**
- ~~nestgate.io data braids~~ **DONE**
- ~~coralReef BLAKE3 checksum~~ **DONE**
- ~~songBird seam fix~~ **DONE**
- **Fleet-wide gate redeploy** — golgi depot ready (19/19 + BLAKE3SUMS). Gates pull on their own harvest cycles.
- **southGate mesh enrollment** — not discoverable on LAN, deferred

### primalSpring owns (hardware cascade)
- eastGate temporal cascade to all gates
- NUCLEUS deployment lifecycle

### swarmVine integration (all teams — Phase 3)
- ~~**songBird team**: Wire `ipc.register` → swarmVine `gossip.inject`~~ **DONE** (`6b580cf0`)
- ~~**songBird team**: Fix socket discovery + gate identity~~ **DONE** (`af0d8fa8`)
- ~~**skunkBat team**: Wire `metadata.analyze` pre-accept validator~~ **DONE** (`e602e09`) — vine-bat loop code-complete
- **biomeOS team**: Wire `capability.resolve` → swarmVine gossip table (cross-gate capability discovery)
- **nestGate/loamSpine**: Inject data gossip entries (`cas.have`, `braid.head`) into swarmVine
- **toadStool/coralReef**: Inject compute gossip entries (`compute.capacity`, `build.queue`)
- **All gates**: Deploy swarmVine to NUCLEUS (binary in depot, ready)

### Binary audit — evolutionary streamlining (eastGate overwatch Aug 9)

**Philosophy**: Lean by evolution, not by excision. No feature-gating within primals. Code moves to its right home — a different primal, a spring, or a composition. Repeated patterns converge through abstraction.

| Primal | Binary | Deps | Crates | Lines | Evolution Path |
|--------|--------|------|--------|-------|----------------|
| **petalTongue** | **33.8 MB** | **656** | 19 | 209K | **doom-core → ludoSpring.** Game rendering belongs in a spring. Already optional. 656 deps need convergence. |
| **songBird** | **23.8 MB** | 646 | **31** | **470K** | **Transport abstraction.** 9 transport crates roll their own connect/send/recv. Shared `Transport` trait collapses boilerplate. songBird stays lightweight, any comms. |
| **biomeOS** | **20.4 MB** | 377 | 26 | 302K | Reasonable for routing substrate. |
| **toadStool** | **12.4 MB** | 627 | 14 | **708K** | **S371 natural split.** `core` 272K extracting to WASM-capable crates (24/48 done). |
| **bearDog** | **8.3 MB** | 556 | **31** | 498K | Already lean. `types`/`tunnel` may share crypto patterns with cellMembrane. |
| swarmVine | **2.5 MB** | 113 | 2 | 4K | **Baseline** — single-domain primal. |

### Other teams own
- **sporePrint**: ~~SU(2)→SU(N) relabel~~ **DONE**. QCD download pages, LaTeX preprint
- ~~**primalSpring**: N2-N5 verification~~ **DONE** (90/91). Remaining: toadStool TARPC shim
- **toadStool**: S371 WASM refactor — `core` 272K splitting naturally as compute kernels extract. 24/48 crates done.
- **songBird**: Transport trait convergence — 9 crates share connect/send/recv patterns. Abstract, don't gate.
- **petalTongue**: Move `doom-core` to **ludoSpring**. Converge 656 deps through workspace inheritance.
- **bearDog**: Review `types`/`tunnel` for shared abstractions with cellMembrane transport layer.
- **cellMembrane**: `native_braid.py` → Rust
- **projectNUCLEUS**: workloads/ → spring repos, specs → wateringHole
- **All primals**: Self-register capabilities with songBird on startup
- ~~**skunkBat**: `PRIMAL_BIND_MODE` env var~~ **DONE** (`a57ada5`)
- **petalTongue**: `--port` in server mode (P4, Windows)

### arXiv blockers (41/42) — 4/5 closed
1. ~~pseudoSpore bundle~~ **DONE** (lithoSpore)
2. ~~SU(2)→SU(N) relabel~~ **DONE** (sporePrint `3e037fe`)
3. ~~`/pseudospore/` route~~ **DONE** (petalTongue)
4. `validate.sh` — bundle-specific BLAKE3 + DAG + Ed25519 verification + freeze/sign v1.0.0-rung1
5. Reviewer send (Murillo, Chuna, Bazavov)

---

*Wave 157a EVOLUTIONARY STREAMLINING. P0 fixed. Fleet unblocked. Lean by evolution: songBird 9 transports → shared Transport trait (any comms, lightweight). petalTongue doom-core → ludoSpring. toadStool core 272K → S371 natural WASM split. No feature-gating — code moves to right home. Baseline: swarmVine 2.5 MB / skunkBat 3.2 MB / sourDough 3.3 MB. Full mesh chain live. sporeGate 15/15 ALIVE. N-series 90/91. 16 primals.*
