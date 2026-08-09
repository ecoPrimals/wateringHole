# ecoPrimals Ecosystem Blurb — Wave 157b VERTEBRATE DEPOT REFRESH

**Date**: Aug 9, 2026 10:15AM | **Wave**: 157b | **From**: sporeGate overwatch
**Posture**: **VERTEBRATE DEPOT REBUILT. 14 PRIMALS EVOLVED. 13,910 CAPS.** 8 primals rebuilt to musl from vertebrate HEAD (songBird, swarmVine, petalTongue, nestGate, coralReef, loamSpine, sourDough, barraCuda). songBird seam fix for vertebrate socket layout (`42aba605`): swarmVine now at `/run/membrane/biomeos/`. Vine-bat loop operational. golgi 19/19 + BLAKE3SUMS. sporeGate 15/15 ALIVE. **Other gates build from golgi depot. blueGate Windows .exe pre-vertebrate.**

---

## EXECUTION SUMMARY — sporeGate overwatch (this session)

### VERTEBRATE DEPOT REFRESH — 8 Primals Rebuilt
- **Cascaded from Forgejo**: 14 of 16 primals had new vertebrate evolution commits (RPC self-audit, registry-dispatch parity)
- **Depot audit**: 6 already rebuilt by eastGate (skunkBat, bearDog, rhizoCrypt, sweetGrass, toadStool). 8 needed rebuild.
- **8 primals rebuilt to musl**:
  - **songBird** (24 MB) — vertebrate `33e9a8be` (CanonicalTransport + swarmVine delegation) + socket fix `42aba605`
  - **swarmVine** (2.5 MB) — vertebrate `2cd4964` (deep audit, async dispatch, riboCipher module)
  - **petalTongue** (29 MB) — vertebrate `87a2530` (RPC self-audit + doom-core decoupling + dep prune)
  - **nestGate** (9.1 MB) — vertebrate `4cafa535` (content.stat shipped, RPC self-audit, registry sync)
  - **coralReef** (7.6 MB) — vertebrate `e32a117` (programmatic registry-vs-dispatch integrity)
  - **loamSpine** (4.8 MB) — vertebrate `c3c6c0f` (self-audit + persist_tip abstraction)
  - **sourDough** (3.4 MB) — vertebrate `3e1b588` (RPC-surface audit tool + AAR handoff)
  - **barraCuda** (5.4 MB) — vertebrate `bcc6683a` (self-audit RPC + storage buffer 512→1GiB)
- **Golgi pushed**: 19/19 + BLAKE3SUMS

### songBird Seam Fix — Vertebrate Socket Layout (`42aba605`)
- **Problem**: Vertebrate evolution moved swarmVine socket from `/run/membrane/swarmvine-*.sock` to `/run/membrane/biomeos/swarmvine-*.sock`. songBird seam couldn't find it.
- **Fix**: `discover_swarmvine_socket()` now searches `/run/membrane/biomeos/` first, falls back to flat layout.
- **Verified**: `ipc.register` → songBird → `gossip.inject` → swarmVine gossip table. Seam live at new path.

### NUCLEUS Refresh — 15/15 ALIVE, 13,910 Caps
- All 8 rebuilt primals + songBird seam fix deployed to local NUCLEUS
- **13,910 capabilities** (up from 1,987) — vertebrate RPC self-audit expanded method surfaces
- **Vine-bat loop operational** at new socket path
- **11 mesh peers** online

### Prior sessions
- **5 primals rebuilt to musl** — biomeOS, songBird, cellMembrane, swarmVine, petalTongue. Golgi 19/19
- **songBird seam fix** (`af0d8fa8`) — socket discovery + `MEMBRANE_GATE_NAME`, gossip.inject proven live
- **petalTongue data braids federation** (`84e6e48`) — `/api/content/federation`, Tower Atomic transport
- **biomeOS FD exhaustion** — `LimitNOFILE=65536`, 1,958 caps registered clean
- **BLAKE3 depot integrity** — 19/19 hashed, pushed to golgi
- **swarmVine Phase 2** — epidemic sweep, TCP :7800, peer discovery (`7532c2b`)
- **songBird seam** (`6b580cf0`) — `ipc.register` → swarmVine `gossip.inject`
- **biomeOS TOML loading fix** (`d1f555e7`) — startup path fixed, 118 translations
- **skunkBat vine-bat** (`e602e09`) — 8-check gossip pre-accept, 672 tests
- **biomeOS riboCipher auto-detect** (`1ff5859c`) — sweetGrass/rhizoCrypt auto-route
- **cellMembrane transport unification** (`f5033f2`) — `#[cfg(unix)]` 7→3
- **N2-N5 verified** — 90/91 (sweetGrass FIXED). toadStool TARPC only
- **swarmVine v0.1.0 budded** — primal #16
- **6/6 gates redeployed**
- **Inner Membrane Phase 1 DONE** — songBird mesh gap fixed

---

## GATE STATUS — 6/6 COMPLETE

| Gate | Status | RSS | Key evolution |
|------|--------|-----|---------------|
| **sporeGate** | **15/15 ALIVE** | — | **VERTEBRATE LIVE** (Aug 9), 13,910 caps, vine-bat + gossip resolve operational |
| **blueGate** | 13/13 ALIVE | 264 MB | Windows 15/15, sub-builder ready |
| **southGate** | 13/13 ALIVE | 96 MB | 0.058ms Tower, SSH compliant |
| **ironGate** | 13/13 ALIVE | 41 MB | 2,058 capabilities, 42 repos clean |
| **strandGate** | 13/13 ALIVE | 127 MB | GPU Lanczos at machine epsilon, 75/87 thermalization cached |
| **westGate** | 13/13 ALIVE | — | NG-05 done, 26 caps registered, 2.5 TB CAS |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** (vertebrate evolution: RPC self-audit, registry-dispatch parity) |
| NUCLEUS gates | **6/6 redeployed** (sporeGate vertebrate live) |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| Golgi depot | Musl **19/19** (vertebrate Aug 9 + BLAKE3SUMS), Windows **15/15** (pre-vertebrate, blueGate rebuild needed) |
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
| **Vine-bat pre-accept hook** | **DONE** — swarmVine `gossip.spread` calls skunkBat `metadata.analyze` (`df97b25`), deny blocks, allow/warn passes. 39 tests. E2E proven |
| **biomeOS TOML deploy** | **DONE** — `d1f555e7` deployed locally, 118 translations loaded |
| **skunkBat vine-bat deploy** | **DONE** — `e602e09` deployed locally, 8-check pre-accept live |
| **P0 songBird depot** | **DONE** — rebuilt 24 MB with seam fix `af0d8fa8`, pushed to golgi. Was 19 MB pre-seam |
| **biomeOS gossip resolve** | **DONE** — `capability.resolve` → swarmVine gossip table (`993b97f7`), targeted mesh dispatch. 1,987 caps |
| **biomeOS provenance translations** | **DONE** — `2fae9144` raw translations (content.stat, spine.list, dag.*, braid.verify). <100ms routing |
| **Vertebrate depot refresh** | **DONE** — 8 primals rebuilt from vertebrate HEAD, golgi 19/19. 13,910 caps on sporeGate |
| **songBird vertebrate socket fix** | **DONE** — `42aba605` discovers swarmVine at `/run/membrane/biomeos/` (vertebrate layout) |

---

## REMAINING

### sporeGate/eastGate overwatch owns
- ~~DEPOT REBUILD~~ **DONE**
- ~~biomeOS FD exhaustion~~ **DONE** on sporeGate (see P1 below for other gates)
- ~~nestgate.io data braids~~ **DONE**
- ~~coralReef BLAKE3 checksum~~ **DONE**
- ~~songBird seam fix~~ **DONE** — code (`af0d8fa8`) AND depot binary (24 MB) both correct
- ~~P0 songBird depot~~ **DONE** — rebuilt, pushed to golgi
- ~~biomeOS gossip resolve~~ **DONE** — `993b97f7` + `2fae9144` deployed
- **Fleet-wide gate redeploy** — golgi musl depot CURRENT (vertebrate). Gates pull on harvest cycles.
- **P1: FD exhaustion on remaining gates** — `LimitNOFILE=65536` applied on sporeGate + ironGate. NOT applied on: westGate, strandGate, blueGate, southGate, eastGate.
- **Windows .exe depot** — blueGate (J12 sub-builder) needs to rebuild 15 .exe from vertebrate HEAD. Current .exe are Aug 7-8 (pre-vertebrate).
- **aarch64-musl depot** — 13/19 binaries, partially stale. No ARM64 gates active, low priority.
- **southGate mesh enrollment** — not discoverable on LAN, deferred

### primalSpring owns (hardware cascade)
- eastGate temporal cascade to all gates
- NUCLEUS deployment lifecycle

### swarmVine integration (all teams — Phase 3)
- ~~**songBird team**: Wire `ipc.register` → swarmVine `gossip.inject`~~ **DONE** (`6b580cf0`)
- ~~**songBird team**: Fix socket discovery + gate identity~~ **DONE** (`af0d8fa8`)
- ~~**skunkBat team**: Wire `metadata.analyze` pre-accept validator~~ **DONE** (`e602e09`) — vine-bat loop code-complete
- ~~**swarmVine**: Wire pre-accept hook into `gossip.spread`~~ **DONE** (`df97b25`) — vine-bat loop **OPERATIONAL**
- ~~**biomeOS team**: Wire `capability.resolve` → swarmVine gossip table~~ **DONE** (`993b97f7`) — local → gossip → targeted → broadcast fallback chain
- **nestGate/loamSpine**: Inject data gossip entries (`cas.have`, `braid.head`) into swarmVine
- **toadStool/coralReef**: Inject compute gossip entries (`compute.capacity`, `build.queue`)
- **All gates**: Deploy swarmVine to NUCLEUS (binary in depot, ready)

### Other teams own
- **sporePrint**: ~~SU(2)→SU(N) relabel~~ **DONE**. QCD download pages, LaTeX preprint
- ~~**primalSpring**: N2-N5 verification~~ **DONE** (90/91). Remaining: toadStool TARPC shim
- **toadStool**: Long-tail cross-arch + WASM compute (S371: 24/48 crates, 50% kernel)
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

*Wave 157b VERTEBRATE DEPOT REBUILT. 14 primals evolved (RPC self-audit, registry parity). 8 rebuilt to musl, golgi 19/19 + BLAKE3SUMS. songBird seam fixed for vertebrate socket layout (`42aba605`). sporeGate 15/15 ALIVE, 13,910 caps. Vine-bat loop operational. Mesh integration chain complete. Windows .exe depot pre-vertebrate (blueGate sub-builder needed). 35 COMPLETE / 9 ACTIVE / 26 GLACIAL. 16 primals. arXiv 4/5 closed.*
