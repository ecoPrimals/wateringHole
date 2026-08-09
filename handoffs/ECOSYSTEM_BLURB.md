# ecoPrimals Ecosystem Blurb — Wave 157a VINE-BAT LOOP OPERATIONAL

**Date**: Aug 8, 2026 9:55PM | **Wave**: 157a | **From**: sporeGate overwatch
**Posture**: **VINE-BAT LOOP OPERATIONAL. FULL PRE-ACCEPT CHAIN LIVE.** swarmVine now calls skunkBat `metadata.analyze` on every remote `gossip.spread` — deny/reject blocks, allow/warn passes (`df97b25`). biomeOS TOML fix (`d1f555e7`) and skunkBat vine-bat (`e602e09`) both deployed locally. 6 primals rebuilt (biomeOS, songBird, cellMembrane, swarmVine, petalTongue, skunkBat), golgi 19/19 + BLAKE3SUMS. sporeGate 15/15 ALIVE, 1,414 caps. **Vine spreads, bat validates.**

---

## EXECUTION SUMMARY — sporeGate overwatch (this session)

### VINE-BAT PRE-ACCEPT HOOK — `df97b25`
- **swarmVine `gossip.spread`** now calls skunkBat `metadata.analyze` before ingesting remote entries
- **Verdict semantics**: `deny`/`reject` → block entry, `allow`/`warn` → accept
- **Graceful degradation**: if skunkBat unreachable → entries pass through (vine spreads, bat validates when available)
- **Configurable**: `SWARMVINE_SKUNKBAT_SOCK` env var. Disabled in test builds via `cfg!(test)` gate
- **E2E proven**: good entries accepted (8/8 checks pass), malicious entries rejected (TTL > 255 → deny)
- **39 tests pass** (12 core + 27 server)
- Pushed to Forgejo `df97b25`

### biomeOS + skunkBat Local Deploy
- **biomeOS rebuilt** (21 MB) — now includes TOML loading fix `d1f555e7`: TOML-first path, 118 translations loaded
- **skunkBat rebuilt** (3.2 MB) — now includes `metadata.analyze` 8-check pre-accept (`e602e09`), deployed locally
- **swarmVine rebuilt** (2.5 MB) — includes vine-bat hook `df97b25`
- **All 3 redeployed** to NUCLEUS, 15/15 ALIVE
- **Golgi depot updated**: 19/19 + BLAKE3SUMS

### Prior sessions (sporeGate overwatch + eastGate)
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
| **sporeGate** | **15/15 ALIVE** | — | **VINE-BAT LIVE** (Aug 8), 1,414 caps, vine-bat pre-accept operational |
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
| Golgi depot | Musl **19/19** (rebuilt Aug 8 + BLAKE3SUMS, vine-bat hook), Windows **15/15** |
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

---

## REMAINING

### sporeGate/eastGate overwatch owns
- ~~DEPOT REBUILD~~ **DONE** (but see P0 below)
- ~~biomeOS FD exhaustion~~ **DONE** on sporeGate + ironGate (see P1 below)
- ~~nestgate.io data braids~~ **DONE**
- ~~coralReef BLAKE3 checksum~~ **DONE**
- ~~songBird seam fix~~ **DONE** in code (`af0d8fa8`) — **NOT in depot binary**

### P0: Depot songBird binary is PRE-SEAM (multiple gates report)
- **Problem**: golgi depot songBird is 19 MB (built from `6b580cf0`). The seam fix `af0d8fa8` (socket discovery + `MEMBRANE_GATE_NAME`) was pushed AFTER depot rebuild. Gates pulling from depot get a songBird where `gossip.inject` silently fails.
- **Evidence**: ironGate Session 15+16 flagged it. Local builds from source are 24 MB (correct). Depot is 19 MB (pre-fix).
- **Fix**: **sporeGate must rebuild songBird from `af0d8fa8`**, push to golgi, regenerate BLAKE3SUMS. Also rebuild skunkBat (`e602e09` vine-bat) + biomeOS (`993b97f7` gossip table + `d1f555e7` TOML fix) if not already in depot.
- **Workaround**: gates can build songBird from source (ironGate did this).

### P1: FD exhaustion on biomeOS + songBird (all gates)
- **Problem**: biomeOS default `LimitNOFILE=1024` overwhelmed during simultaneous primal announcement storm on restart. Causes capability registration failures and socket errors.
- **Fix**: Add `LimitNOFILE=65536` to biomeOS AND songBird systemd units on every gate.
- **Applied on**: sporeGate, ironGate. **NOT applied on**: westGate, strandGate, blueGate, southGate, eastGate.
- **Long-term**: toadStool Node Atomic systemd template should include `LimitNOFILE=65536` for all membrane services.

- **Fleet-wide gate redeploy** — BLOCKED on P0 songBird rebuild. Gates should not pull until golgi has corrected binary.
- **southGate mesh enrollment** — not discoverable on LAN, deferred

### primalSpring owns (hardware cascade)
- eastGate temporal cascade to all gates
- NUCLEUS deployment lifecycle

### swarmVine integration (all teams — Phase 3)
- ~~**songBird team**: Wire `ipc.register` → swarmVine `gossip.inject`~~ **DONE** (`6b580cf0`)
- ~~**songBird team**: Fix socket discovery + gate identity~~ **DONE** (`af0d8fa8`)
- ~~**skunkBat team**: Wire `metadata.analyze` pre-accept validator~~ **DONE** (`e602e09`) — vine-bat loop code-complete
- ~~**swarmVine**: Wire pre-accept hook into `gossip.spread`~~ **DONE** (`df97b25`) — vine-bat loop **OPERATIONAL**
- ~~**biomeOS team**: Wire `capability.resolve` → swarmVine gossip table~~ **DONE** (`993b97f7`) — `discovery_gossip.rs` + targeted mesh dispatch. Fallback: local → gossip → targeted → broadcast. 7 tests.
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

*Wave 157a VINE-BAT OPERATIONAL. Full chain live: `gossip.spread` → skunkBat `metadata.analyze` (8-check, deny/warn/allow) → swarmVine ingest → epidemic spread → cross-gate TCP. `df97b25` wires the pre-accept hook; `e602e09` + `af0d8fa8` + `84e6e48` complete the mesh integration stack. 6 primals rebuilt, golgi 19/19 + BLAKE3SUMS. sporeGate 15/15 ALIVE (4ms dispatch, 1,414 caps). N-series 90/91. 30 COMPLETE / 11 ACTIVE / 26 GLACIAL. 16 primals. arXiv 4/5 closed.*
