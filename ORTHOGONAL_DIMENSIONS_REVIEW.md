# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 157a)
- [x] Gate heads published (`heads/*.toml`) — golgiBody auto-publishing active
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] **ECOSYSTEM_BLURB.md** is the universal handoff (Tracks A+B converged)
- [x] **70+ handoff docs + AARs** delivered Wave 155b–n. 10 AARs + 2 handoffs fossilized this wave.
- [x] **ZERO P0 (all 3 resolved + DEPLOYED Wave 157e):** ~~P0-A bearDog~~ DEPLOYED FLEET-WIDE (westGate: `crypto.sign_ed25519` signs in 0.4ms). ~~P0-B nestGate~~ DEPLOYED (westGate: `content.ingest` 5 files/6.3ms, Rust-native). ~~P0-C biomeOS FD~~ DEPLOYED (westGate: 13→15 FDs after 7 calls). All 6 gates on 157e depot. 16 primals self-audited — zero phantom methods.
- [x] **NUCLEUS ACHIEVED on 6 gates** — westGate, strandGate, blueGate, sporeGate, southGate, **ironGate**. All 6 v4.57+ G68-converged. Gate validation AARs fossilized.
- [x] **Depot UNIFIED + PRUNED + PEPTI LAYER (Wave 157e)** — Canonical path `/opt/ecoPrimals/plasmidBin/primals`. Auto-prune on every harvest. Disk health guard (80% warn, 90% block). **G69 Phase 3 CAS archival wired** (`archive_superseded_binary()` sign→spine→braid→CAS). G69 Depot Lineage spec published. blueGate → golgi push SOLVED. graftGate registered. Forgejo GC timer. golgi at 74% disk. **All 6 gates deployed Wave 157e.**
- [x] **biomeOS v4.56 SHIPPED** — G22 convergence steps 1+2: unified namespace, 244 caps, 47 deps removed.
- [x] **westGate ZFS rebuilt** — mirror → raidz1, 25.4 → 50.7 TB usable. AlphaFold DB fits.
- [x] **Golgi post-receive hook FIXED** (3 bugs: dispatcher, case, category). Sovereign CI E2E verified.
- [x] **cellMembrane 1,281+ tests** — MEMBRANE_*, crypto dedup, J16+J13+J19 killed, registry API hardened.
- [x] **squirrel -48,672 lines** (Waves 156e→156z deep cleanup). 3 orphan crates excised, 157 functions de-asynced, PluginV2 dead code eliminated, PrimalType + EcosystemPrimalType fossils deleted, config crate removed. 313 files changed. 0 unsafe, 0 clippy.
- [x] **Provenance 7/7 COMPLETE** — E2E validated on westGate (5th consecutive pass) + blueGate (Windows). **Braid pen test 86/87 PASS (Wave 157e)** — first-ever E2E provenance chain verification. **~~P1: `braid.verify` missing~~ → SHIPPED (sweetGrass, Wave 157g)** — method #48, capability-registered. **~~P2: braid.verify behavioral tests~~ → CLOSED (sweetGrass `a6cc287`, Wave 157i)** — 5 behavioral tests: unsigned braids, format validation, crypto-down permissive, not-found, attribution metadata.
- [x] **Sovereign CI LIVE** — push-to-deploy E2E verified for ALL 13 primals including biomeOS (coevolution).
- [x] **Wave 157e MESH DEPLOYED** — ALL 6 NUCLEUS gates on 157e depot. **Wave 157i**: G72 Pandemic: **11/11 teams Tier 1 COMPLETE** (~155+ crates shed fleet-wide). Gossip **3→7/16 primals LIVE** (barraCuda **22/22** full spec, wetSpring **4/4**, nestGate 11 CAS sites wired). **P2 braid.verify CLOSED** (sweetGrass behavioral tests). toadStool tokio 118→65 (45%). **graftGate Tower Atomic RUNNING on macOS** — 4th platform proven (G11). hotSpring pseudoSpore E2E pipeline shipped. bearDog +41 dead deps removed. petalTongue telemetry excised + runtime discovery. nestGate S147/S148 (1,666 tests).
- [x] **Overwatch retooled (Wave 157g)** — gate-agnostic temporal script (`overwatch-temporal.sh`) sweeps all 4 Forgejo orgs via HTTPS API, compares 43 repos against local HEAD, outputs human/JSON. No SSH needed. Overwatch position formally separated from primalSpring team: overwatch = coordination/blurb/review (floats to any gate); primalSpring = code + deployment (eastGate-resident). Phase B impulse-driven overwatch adoption accelerated.
- [x] **Coevolution contract COMPLETE (G21)** — biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED (`652cf8a7`).
- [x] **151 files fossilized** across 10 checkpoints. Latest: `wave156d_data_flow_activation/` (8 files). Active handoffs: 7 (BLURB + 6 active refs). **1,472 total fossil records.**
- [x] **whitePaper convergence (G22)**: **COMPLETE** — biomeOS v4.56 single-process merge. Dual-protocol (riboCipher + JSON-RPC) in one process. Validated on westGate + sporeGate.
- [x] **Portability checkpoint (G17) — PROVEN.** southGate 22/22 PASS. NUCLEUS from public depot, own entropy, user-space paths, no WireGuard, no inherited identity. 20h stable, 32 sockets, 76MB RSS, 29,294 foreign peer rejections.
- [x] **DATA FEDERATION (westGate)** — **3.21 TB, 153 datasets, 17+ domains, 2.5 TB CAS federated**, 100% provenance. tideGlass 7/7 COMPLETE. AlphaFold v6 42/46 proteomes. 50+ public sources. `data_catalog.toml` v2.0.0 shipped. **NG-05 CLOSED — CAS federation live, 26 capabilities registered.** Inter-gate via Tower Atomic LAN.
- [x] **Peptidoglycan DNS G29 COMPLETE** — 3-way redundancy: sporeGate dnsmasq (primary) + blueGate dnsproxy H2 secondary (LIVE) + golgi mesh DNS. Confirmed by sporeGate infrastructure verification.
- [x] **strandGate v4.56 DEPLOYED** — Carry-forward resolved. G22 confirmed. GPU QCD: 38-58× speedup, 5,500 traj/hr. hotSpring composition validated on live NUCLEUS.
- [x] **sporePrint DEMONSTRATION ERA** — 334→190 pages. pseudoSpore LIVE at primals.eco/pseudospore/. Hype cleaned (20 files). Tests: 116,930. First arXiv draft scaffolded.
- [x] **arXiv Rung 1 REFRAMED** — "Toward Vendor-Agnostic Lattice QCD on Consumer GPUs: SU(2) HMC with DF64 WebGPU/WGSL and Cryptographic Provenance." AI review absorbed. Scope ladder, plaquette normalization eq, precision matrix added. LaTeX updated. 6-rung research program defined. Experiment queue ACTIVE (β-scan, HMC diagnostics, increased stats).
- [x] **westGate persistence HARDENED** — ZFS auto-import, 13/13 NUCLEUS units enabled, boot dependency chain, daily snapshots, monthly scrub. 9/9 boot check PASS.
- [x] **hotSpring** — 627+ tests, 0 clippy. **pseudoSpore E2E pipeline SHIPPED** (pure Rust: `arxiv_production_campaign` → `arxiv_analysis` → `pseudospore_manifest` → `pseudospore_bundle` → `pseudospore_sign` (bearDog Ed25519) → `pseudospore_register` (westGate CAS + ironGate NFT)). 10 gossip events defined (scaffold — not yet hooked). 32⁴ thermalization fix (dt 0.01→0.005, warmup 500→1500). Rung 1 science COMPLETE — all physics validated. (**Wave 157i**)
- [x] **publications/ directory** — Auditable data transfer point for papers + pseudoSpore. Lattice QCD data centralized with full audit trail.
- [x] **golgi auto-publish fix** — THREE compounding bugs fixed: (1) worktree ownership mismatch (`git:git` vs `root:root`), (2) missing `--force` flag on `zola build`, (3) SSH config pointing at wrong golgi IP. sporePrint now deploys correctly to both inner and outer membrane.
- [x] **ironGate ONLINE** — Dev loop validated. Tower Atomic deployed (bearDog 10.6 MB + songBird 16.7 MB + skunkBat 2.6 MB). Forgejo SSH + HTTPS + depot all verified. 42 repos synced. Mesh: golgi 38ms, sporeGate 77ms, eastGate 78ms. **Ready for esotericWebb (G20).**
- [x] **P2 RESOLVED: GPU PRNG polyfill bias** — Root cause: WGSL transcendental polyfills (`log_f64`, `sqrt_f64`, `cos_f64`) in Box-Muller momentum shader produced wrong variance. Three-path comparison proves GPU MD pipeline is correct (bit-exact 4e-17). `cpu_mom` workaround deployed — CPU generates momenta, GPU does all MD at full speed. Section 3.2 UNBLOCKED. Finding strengthens the paper (validation methodology).
- [x] **SPRINGS-TO-NUCLEUS MESH (Aug 2)** — All 10 springs/gardens assigned to gates by hardware specialization. Cell graphs v2.0.0 (content.get + provenance trio + gate metadata). tideGlass Cargo workspace LIVE. biomeOS deploy graphs v2.0.0. Inter-gate CAS data access config created. ecosystem_manifest v3.3.0 with spring_mesh assignments.
- [x] ~~PLANNED SERVICE INTERRUPTION (Aug 2)~~ — **COMPLETE.** ATT gateway + DS224+ moved. reefGate enrollment queued. steamGate queued.

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~150K+ primal tests validated this wave** (songBird 14,840, bearDog 14,019, nestGate 1,630, **toadStool 8,447** (S379 post-gating), biomeOS 8,700+, squirrel ~5K, petalTongue 6,615, **barraCuda 5,054**, **coralReef 3,963+**, rhizoCrypt 1,900+, loamSpine 1,752+, **sweetGrass 1,684**, cellMembrane 1,349+, **tideGlass 220+**, primalSpring 197+, skunkBat 672, sourDough 518+, footPrint 708, esotericWebb V33 (484+), swarmVine 134+, bingoCube 31)
- [x] Zero TODO/FIXME/HACK in project code — **16/16 primals clean** (swarmVine budded Wave 157a)
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **14,019** tests. P0-A IN DEPOT. **Wave 157d**: `RiboCipherHandler` (16th handler kind) — `decode_mito_tag`, `encode_mito_signal`, `protocol_name`, `list_protocols` as JSON-RPC. Auto-announced via `primal.announce`. Unblocks biomeOS riboCipher Tier 2 cross-gate protocol detection. (**Wave 157d**)
- [x] songBird: **14,840+** tests. **Wave 157d**: Transport convergence (`TransportRegistry`, graceful shutdown, dyn-compatible trait). Gossip excised → swarmVine. PID fix. **RIBOCIPHER TIER 2 CHAIN CLOSED**: `dispatch_ribocipher_rpc()` replaces `dispatch_federation_rpc()` — federation port `:7700` routes mito-framed (`0xED`) connections through full `IpcServiceHandler` instead of stub. Health/capabilities intrinsics fast-path, all other methods via shared handler. bearDog encodes → biomeOS sends → songBird accepts. 7 new tests. (**Wave 157d**)
- [x] nestGate: **1,666** tests (94 IPC methods, 21 capability domains), dual-path CAS + Neural API wiring. **P0-B RESOLVED + IN DEPOT**. `content.stat` shipped. **G72 Tier 1 DONE**: jsonrpsee removed (1,864 LOC, -10 crates), crossbeam umbrella→channel, dead bincode removal. **S146 deep debt**: fake success paths eliminated (Azure/GCS/S3 → `not_implemented`), idiomatic Rust pass. **S147/S148**: nestgate-nas crate dropped, steam feature removed, shared state consolidation, gossip hooks at 11 CAS sites with 6 event types. (**Wave 157i S146-S148**)
- [x] toadStool: **8,447** tests (post-S379 count — feature gating removed vestigial test surface). S375 NUCLEUS manifest. S376 Tokio blast radius. **S377 manifest CONVERGED** (5→2 BiomeManifest structs). **S378 Tokio vestigial segmentation round 2: 118→65 files (45% reduction).** Dead features excised: `plugin-loading` (C FFI dlopen), `vulkano`, core `wgpu`, `wasm-runtime`. **S379 G72 Tier 1 COMPLETE**: 7 dead deps removed (http-body-util, criterion, uuid, env_logger, test-log, tempfile, vulkano), 6 promoted to workspace (bytemuck, zeroize, wasmi, blake3, anyhow, mdns-sd). `tokio::fs` eliminated (28 files → `std::fs`). tokio trimmed to 6 workspace features. **~73 GiB reclaimed** (S377-S379). **38/48 WASM** (79%) — wiring improved (ExecSpec::Wasm, infer_runtime_type), count flat. **G72 EXEMPLAR.** (**Wave 157i S379**)
- [x] biomeOS: **8,700+** tests (578 Neural API). P0-C IN DEPOT. **Wave 157d**: generic capability dispatch executor (`capability_call` handler routes any dotted capability through Neural API, `graph_foreach` for iterative sub-graph execution). **P1 FD exhaustion SELF-HEALING** (`raise_fd_limit()` at startup — soft NOFILE → 65536, cross-platform, no systemd dependency). Client-side riboCipher Tier 2 (`ConnectionPool::send_mito_jsonrpc` — `[0xED, 0x01]` + 32-byte mito-tag on fresh connections, graceful Tier 1 fallback). G69 depot lineage graph templates (`depot_lineage.toml`, `depot_lineage_batch.toml` with `graph_foreach`). (**Wave 157d**)
- [x] petalTongue: **6,755** tests. **Wave 157d G19**: `/ws/scene` WebSocket + `webgl_bridge` compilation (`DoomFrame`/`SceneGraph` → `WebGlScene` vertex/index buffers ready for GPU upload → broadcast channel). `raise_fd_limit()` self-healing (mirrors biomeOS pattern). `DEFAULT_LOOPBACK_HOST` centralized. Browser clients receive fully compiled buffers. esotericWebb + footPrint ready. (**Wave 157d**)
- [x] barraCuda: **5,054** tests. Silicon Fold absorbed. **Full gossip enmeshment — 22/22 events wired across runtime paths** (compute, tower, shader, dispatch, quota, OOM, precision — recovered, precision-degraded, systemic-error final 3 wired). G72 dep audit clean. **CONTEXT.md: 26 method domains.** Node Atomic Trio wiring, zero-panic (17 `.expect()` → `?`/Result). (**Wave 157i**)
- [x] ~~**barraCuda YELLOW**~~ → **GREEN**: PRNG half-range fixed (xoshiro 52→53 bits). Statistical validation harness. -1,488 LOC (LazyLock→const, error helpers). `cpu_mom` remains production HMC path (Box-Muller transcendental polyfill, not PRNG).
- [x] coralReef: **3,963+** tests. GEMM Phase 2 SHIPPED. **G72 Tier 1 DONE**: optional dep gating (futures/tokio-util behind `tarpc-transport`, tokio/process→dev-deps). `#[allow]→#[expect]` Rust 2024 idiom evolution. Health dispatch wired. 46 orphaned BTSP tests recovered. Proactive file splits + EVOLUTION assessment filed. (**Wave 157i**)
- [x] cellMembrane: **1,349+** tests. G69 Phase 1+2+3 COMPLETE. **G72 Tier 1 DONE**: tokio rt-multi-thread→dev-deps, time/macros removed. Socket name dedup (3→1 canonical). NUCLEUS install lifecycle extracted from harvest.rs. Deep debt sweep: error handling + health module extraction + constant consolidation. Cargo update (blake3, thiserror, aho-corasick, cc). (**Wave 157i**)
- [x] rhizoCrypt: **1,900+** tests. **G72 Tier 1 DONE**: wiremock removed (0 usage), **-46 crates (14.6% lockfile reduction)**. hashbrown dedup resolved (0.14+0.17→0.14). Deep debt sweep: vertex builder extracted, handlers standardized, test file split. (**Wave 157i**)
- [x] loamSpine: **1,752+** tests. **G72 Tier 1 DONE**: url crate + ICU chain excised (-7 crates), chacha20poly1305 0.10→0.11. RustCrypto unified. Deep debt: test file refactoring + comprehensive audit. Doc hygiene + cargo clean. (**Wave 157i**)
- [x] sweetGrass: **1,684** tests. **G72 Tier 1 DONE**: tokio `["full"]`→7 explicit features, dead bincode/chrono removed. **P2 braid.verify behavioral tests CLOSED** (5 tests: unsigned braids, format validation, crypto-down permissive, not-found, attribution metadata). Batch + verify extracted into focused submodules. DH-0 (debt horizon zero). (**Wave 157i**)
- [x] squirrel: **C8 DONE — -67,090 lines** total (Waves 156e→157c). 257K→190K lines, 16→12 crates, 4,090 tests. G66 transport abstraction. G65 protocol negotiation origin. 0 unsafe, 0 clippy. **`signal.dispatch` WIRED (G18).** (**Wave 157c**)
- [ ] primalSpring: **1,263 tests, 197 scenarios, 95 experiments.** **Wave 157g: ROLE SPLIT** — eastGate-resident code + deployment team (separated from overwatch). **biome.yaml consumption DONE**: composition module, `biome-eastgate.yaml` (14 primals, 3 compositions), `nucleus_launcher --biome`, exp122 37/37 PASS. `spine.list` routing gap CLOSED. **Next**: multi-composition orchestration + **G72 dep pandemic assist** (profile archaic patterns across primals for targeted excision). (**Wave 157g**)
- [x] skunkBat: 9 threat types, ConnectivityAnomaly, frame crypto, PUBLIC. **`metadata.analyze` shipped** (`e602e09`): 8-check gossip pre-accept validation for vine-bat loop. 672 tests.
- [x] **swarmVine — 134 tests (Wave 157d)**. **Windows port DONE** (`1759b2a`): 4 UDS call sites → G66 transport abstraction, tarpc `#[cfg(unix)]`/`#[cfg(not(unix))]` gating, `tcp` feature enabled. **Deep debt** (`d963d47`): IPv6 bracketed loopback bypass fix, `/tmp/biomeos/` hardcoded paths → `platform_paths::runtime_socket_dir()`, hostname dedup, nonce lock contention eliminated. **Phase 4** (`1322d98`): `gossip.subscribe` with tokio broadcast channel, `BloomFilter` for CAS have-set membership (FNV-1a, zero deps), `ComputeCapacity` scheduling hints, `DepotManifest` + `DepotManifestEntry` for binary distribution gossip. Gossip.rs refactored (941→755 LOC). (**Wave 157d**)
- [x] **BTSP 15/15 → 16/16** — all primals shipped ClientHello (swarmVine inherits from sourDough scaffold)
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: 6/6 seams DONE
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [x] **G64 Cephalization — COMPLETE (Wave 156q)**: C2 dual-socket 15/15, tarpc convergent evolution.
- [x] **G65 Protocol Negotiation — COMPLETE (Wave 156q)**: Single-socket dual-protocol, 15/15 primals. squirrel origin, sourDough reference.
- [x] **G66 Transport Abstraction — COMPLETE (Wave 157a)**: Silicon-agnostic IPC. TransportEndpoint/TransportStream/connect_transport. sourDough reference. **15/15 pass Windows cross-arch.** petalTongue `9a5ed02`, skunkBat `7ef22f3`, squirrel `234fa514` completed the set.
- [x] **C8 squirrel excision — DONE (Wave 157b)**: -67,090 lines, 236 files, 16→12 crates.
- [x] **westGate jelly string elimination (Wave 156v)**: Python braiding pipeline → primal-native RPCs. 4-30x speedup. Neural API would have prevented this.
- [x] **hotSpring ↔ primal deduplication (Wave 157a)**: Audit complete. barraCuda needs to absorb `HardwareCalibration::probe()` + `PrecisionEval` (1,090 LOC). toadStool already replaces `low_level/` and `fleet_*`. 4 systems to push upstream, 6 already wired.
- [ ] **Inter-gate content.get E2E — READY TO TEST**: songBird `mesh.connectivity_check` + `mesh.throughput` SHIPPED. biomeOS routing READY. Need **live operational test** on actual gates (not code — ops). Blocks all data-remote springs.
- [x] **G18 squirrel → biomeOS integration — LIVE ON IRONGATE**: squirrel rebuilt from source, `signal.dispatch` operational with 9 primal providers. Cross-primal routing validated (squirrel → rhizoCrypt 1ms, squirrel → bearDog crypto). esotericWebb + footPrint infrastructure confirmed ready. **NEXT**: wire footPrint agent panel (WebSocket → petal → squirrel).
- [x] **CODE OWNERSHIP DISCIPLINE ESTABLISHED**: Primary teams: sporeGate (provenance trio), biomeGate (Node Atomics), eastGate (Tower+agent), overwatch (orchestration+discovery). All 4 groups at 100% G65 + G66.
- [x] **Cross-arch 15/15 CLEAR (Wave 156z)**: petalTongue `9a5ed02` (TransportListener Phase 2), skunkBat `7ef22f3` (#[cfg(unix)] guards), squirrel `234fa514` (157d compliance). All pass `cargo check --target x86_64-pc-windows-gnu`.
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Physical Topology

- [x] Mixed 10G + 1G topology LIVE — 10G AOC backbone between houses, MikroTik CRS310 + Omada SX3008F
- [x] sporeGate on R45 → MikroTik — plasma membrane router (NAT/DHCP/DNS/nftables)
- [x] eastGate on MikroTik LAN — code hub, 10G SFP+ direct, **64 GB DDR5** (upgraded from 32 GB, Wave 157a)
- [x] northGate enrolled (Windows 11, RTX 5090, 2.5G ethernet)
- [x] westGate ONLINE — AMD Ryzen 7 5700X / 64GB DDR4 / 2TB NVMe / **ZFS raidz1 50.7TB usable (rebuilt from mirrors) + 2TB L2ARC SSD**
- [x] ironGate HDD — 14TB + 1TB + 1TB + ~2TB, enclave experiment planned
- [x] blueGate + swiftGate: Windows, house2, 10G backbone proven
- [x] grapheneGate: Android, Tower LIVE (bearDog + songBird + skunkBat)
- [x] 10G AOC trunk CRS310↔Omada proven (blueGate reaches relay via backbone)
- [x] **TOPOLOGY_MAP.toml** has full physical layout with cytoplasm zone model
- [ ] **steamGate** (Steam Deck) — NEXT cross-platform gate. SteamOS (Arch, glibc). User-space deploy.
- [x] **graftGate** (M4 Mac Mini) — **BOOTSTRAP COMPLETE (Aug 11).** First `aarch64-apple-darwin` target. **12/15 primals compiled** (80% first-build success): bearDog 6.3M, songBird 17M, skunkBat 2.6M, nestGate 6.7M, rhizoCrypt 5.8M, loamSpine 3.8M, sweetGrass 10M, barraCuda 2.2M, coralReef 6.6M, biomeOS 16M, swarmVine 2.0M, sourDough 2.8M. 3 darwin failures: toadStool (`silicon_registry_status` in `#[cfg(target_os = "linux")]` impl block), squirrel (Linux-only linker flags in `.cargo/config.toml`), petalTongue (`rustix::process::Signal` API differences). bearDog needed local ios.rs import fix. 41/42 repos cloned (sporePrint needs SSH). WG IP **10.13.37.13** assigned, pubkey registered. Rust 1.97.1. Remaining: golgiBody WG peer add, SSH key in Forgejo, depot push, NUCLEUS lifecycle (launchd).
- [ ] **iosGate** (iPhone XS) — GLACIAL. ecoPrimal user ready. Needs graftGate + Apple Dev Program. First tethered to graftGate for network; future: sovereign iOS gate.
- [ ] fieldGate OFFLINE (dead CMOS)
- [x] **biomeGate GPU CRANKSHAFT LIVE** — Threadripper 3970X, 128GB. 3 GPUs on VFIO: RTX 5060 (host/wgpu) + Titan V (GV100 SM70) + K80 (GK210×2 SM37, **unretired**). toadStool + hotSpring built. coralReef **3,553 tests PASS**. 44-experiment revalidation matrix staged. Exp 231 (K80 cross-gen quench) first-ever hardware run queued.
- [ ] Complete port→gate mapping (CRS310 + Omada + TL-SG605S-M2)
- [ ] Document Flint H1 + Flint 2 + Omada WiFi bridge configs

### Gate Fleet — Status Matrix

| Gate | Status | Platform | Mesh IP | Composition | Role |
|------|--------|----------|---------|-------------|------|
| golgiBody | ONLINE | Linux | 10.13.37.1 | thin-relay | Sole depot, enrollment, Forgejo, Drawbridge |
| sporeGate | ONLINE | Linux | 10.13.37.2 | full | Topology owner, fallback builder, depot, cascade hub, **peptidoglycan anchor H1** |
| eastGate | ONLINE | Linux | 10.13.37.5 | full | Code hub, overwatch. i9-12900K, **64 GB DDR5**, Z790-P WIFI |
| ironGate | **NUCLEUS (13)** | Linux | 10.13.37.7 | **NUCLEUS (13)** | **DOWNSTREAM HOST.** G18 DISPATCH LIVE (9 providers). 12.7 TB CAS. 170 caps. **Socket discovery FIXED** (songbird-register.sh 11 primals). TCP 7800 listening. i9-14900K, RTX 5070, 94 GB. esotericWebb V32 + footPrint LIVE. |
| flockGate | **DOWN** | Linux | 10.13.37.6 | full | Rebooted, RustDesk locked out. esotericWebb → **ironGate** |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090. **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). |
| grapheneGate | ONLINE | Android | 10.13.37.7 (mobile) | tower | Beacon seed, mobile Tower (Android — no IP collision with ironGate, different interface) |
| strandGate | **157e DEPLOYED — 7/7** | Linux | 10.13.37.10 | **NUCLEUS** | **SILICON FOLD + PHASE 1 CLEAR.** Campaign 22/45. GEMM PASS. RTX 3090 + RX 6950 XT + AKD1000. |
| westGate | **157e DEPLOYED — 14/14** | Linux | 10.13.37.11 | **NUCLEUS (14)** | **DATA NAS. 9+ JELLY ELIMINATED** (fleet-wide). Rust-native pipeline. Signed commits. Pen test 86/87. |
| blueGate | **157e DEPLOYED — 13/13** | Windows | 10.13.37.12 | **NUCLEUS (13)** | **PRIMARY BUILDER.** `:9800` validated. golgi SSH+SCP. barraCuda -23% binary. |
| biomeGate | **GPU CRANKSHAFT + FULLY AGENTIC** | Linux | 10.13.37.3 | compute | Threadripper 3970X, 128GB. 3 VFIO GPUs. coralReef 3,553 tests. 44-experiment matrix. **WG mesh LIVE, 8/10 peers, Forgejo SSH working.** G32 silicon deism. |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| **reefGate** | **QUEUED** | Linux | — | nest | DDR3 NUC + DS224+ NFS. Enrollment queued post basement move (G44). |
| southGate | **157e DEPLOYED — 13/13** | Linux | **NO WG** (deliberate) | **NUCLEUS (13)** | **CANARY PASS.** 17,595 conn/s, 0.057ms. No regression. RTX 4060. ~~P2 process leak~~ RESOLVED (coralReef RAII guards). |
| **steamGate** | **NEXT** | SteamOS | — | tower (3) | Steam Deck. Portable compute. gnu bins in depot. |
| **graftGate** | **TOWER BUILT** | macOS | 10.13.37.13 | tower (3) | **M4 Mac Mini.** First `aarch64-apple-darwin`. **12/15 primals compiled** (80% first-build). 41/42 repos cloned. WG keys generated. 3 darwin failures logged (toadStool, squirrel, petalTongue). |
| **iosGate** | **GLACIAL** | iOS | — | tower (3) | iPhone XS. ecoPrimal user. After graftGate + Apple Dev. |

### Gate × Team × Deployment Matrix — Rationalized Code-Team Placement (Wave 157i)

Each gate has a hardware specialization. Code teams (Cursor IDE sessions) should be hosted
on the gate whose hardware matches their domain. This reduces eastGate overload and aligns
compute with capability. **Overwatch is gate-agnostic** — locally delegated to eastGate for
coordination but not bound to any single gate.

| Gate | Role | Intended Code Teams (Cursor sessions) |
|------|------|---------------------------------------|
| **eastGate** | Coordination hub, 64 GB DDR5, 10G | primalSpring, biomeOS, squirrel, songBird, overwatch coordination |
| **ironGate** | GPU compute + gardens, RTX 5070, i9-14900K | Compute trio (toadStool, barraCuda, coralReef), petalTongue, esotericWebb, footPrint |
| **westGate** | Data NAS, ZFS 50.7 TB, CAS federation | Provenance trio (rhizoCrypt, loamSpine, sweetGrass), nestGate, tideGlass, wetSpring |
| **strandGate** | Batch compute farm, dual EPYC, RTX 3090 | hotSpring batch campaigns (unattended). **No interactive code teams.** |
| **sporeGate** | Build + CI + depot, topology owner | cellMembrane ops only. **Lean — no primal code teams.** |
| **biomeGate** | Cross-vendor GPU lab, 3 VFIO GPUs | Node Atomic cross-vendor experiments (coralReef shader testing) |
| **blueGate** | Windows builder, Flint 2 bridge | Build-only sub-builder. **No code teams.** |
| **southGate** | Validation canary, RTX 4060, no WG | Validation only. neuralSpring if 128 GB needed. |
| **graftGate** | darwin builder, M4 Mac Mini | Apple/darwin builds, iosGate prep, sourDough cross-arch validation |

**Agent lifecycle**:
- **Tier 1 (Gate)**: Hardware overwatch agent — long-lived, rare restart. Gets universal `GATE_SPINUP_BLURB.md`.
- **Tier 2 (Code Team)**: Fresh agent per team — frequent restart. Gets user's K-NOME Blurb 1 (audit) + Blurb 2 (execute) from personal prompt bank on northGate.
- **Tier 3 (Ecosystem)**: Overwatch coordination. Gets `ECOSYSTEM_BLURB.md`.

Agent context is disposable and re-injectable. Persistent memory lives in Forgejo, wateringHole, specs, fossil records, and K-NOME documentation.

### Hardware Deployment Profile — Cross-Architecture Targeting (Wave 157i)

Profiles every deployment form factor the ecosystem can target — proven, imminent, and aspirational.

#### Tier A: Systems (Full OS, interactive or batch)

| Form Factor | Gate(s) | Hardware | Target Triple | Composition | Status |
|-------------|---------|----------|---------------|-------------|--------|
| Desktop/Tower | eastGate, ironGate, strandGate, biomeGate, southGate, flockGate | x86_64, 27-256 GB, optional GPU | `x86_64-unknown-linux-musl` | Full NUCLEUS | **PROVEN** |
| Windows Desktop | northGate, blueGate, swiftGate | x86_64, 62-96 GB | `x86_64-pc-windows-gnu` | Full NUCLEUS / tower-builder | **PROVEN** |
| NAS/Storage | westGate | Ryzen 7, 64 GB, ZFS 50.7 TB | `x86_64-unknown-linux-musl` | Nest Atomic | **PROVEN** |
| NUC/Mini PC | sporeGate | Ryzen 5 6600H NUC, 27 GB | `x86_64-unknown-linux-musl` | Full NUCLEUS | **PROVEN** |
| Mac Mini | graftGate | M4 Apple Silicon, 16 GB | `aarch64-apple-darwin` | Tower (12/15 compiled) | **ACTIVE** |
| **Keyboard Computer** | **piGate** | **Raspberry Pi 500/500+**, Cortex-A76 2.4GHz, 8/16 GB, Vulkan 1.3 | `aarch64-unknown-linux-gnu` | Tower → NUCLEUS | **PLANNED** ($180-190) |
| **RISC-V SBC** | **riscGate** | **Milk-V Jupiter 2**, SpacemiT K3 8-core RVA23, up to 32 GB LPDDR5, **60 TOPS NPU**, 10GbE SFP+ | `riscv64gc-unknown-linux-gnu` | Tower → expand | **ON ORDER** (~$300+) |
| Handheld | steamGate | Steam Deck OLED, Zen 2, RDNA2 Vulkan 1.3 | `x86_64-unknown-linux-gnu` | Tower + Node Atomic | **QUEUED** |
| Cloud VM | cloudGate | Oracle Ampere A1 free tier | `aarch64-unknown-linux-gnu` | Tower | **GLACIAL** |
| NUC + NFS pair | reefGate | DDR3 NUC + Synology DS224+ | `x86_64-unknown-linux-musl` | Nest | **QUEUED** |

#### Tier B: Mobile / Tethered

| Form Factor | Gate | Hardware | Target Triple | Status |
|-------------|------|----------|---------------|--------|
| Android phone | grapheneGate | Pixel 8a (GrapheneOS) | `aarch64-unknown-linux-musl` | **PROVEN** — Tower LIVE |
| iOS phone | iosGate | iPhone XS | `aarch64-apple-ios` | **GLACIAL** — needs graftGate + Dev Program |

#### Tier C: Accelerator Cards (resources on Tier A hosts)

| Type | Hardware | Host Gate | Primal Consumer | Status |
|------|----------|-----------|-----------------|--------|
| NVIDIA GPU | RTX 5090 | northGate | toadStool, barraCuda, coralReef | LIVE (do-not-deploy gate) |
| NVIDIA GPU | RTX 5070 Ti | ironGate | toadStool, barraCuda, coralReef | **LIVE** — CUDA, SHADER_F64 |
| NVIDIA GPU | RTX 3090 | strandGate | hotSpring QCD, barraCuda | **LIVE** — DF64, 5,500 traj/hr |
| NVIDIA GPU | RTX 5060 | biomeGate | coralReef wgpu host | **LIVE** |
| NVIDIA GPU | RTX 4060 | southGate | validation canary | **LIVE** |
| NVIDIA VFIO | Titan V (GV100 SM70) | biomeGate | toadStool ember | **LIVE** — multi-gen validation |
| NVIDIA VFIO | K80 (GK210×2 SM37) | biomeGate | toadStool ember | **LIVE** — cross-gen quench |
| AMD GPU | RX 6950 XT | strandGate | barraCuda, coralReef | **LIVE** — Infinity Cache advantage |
| NPU (PCIe) | BrainChip Akida AKD1000 | strandGate | toadStool, rustChip | **LIVE** — 20,545 Hz inference |
| **RISC-V NPU** | **SpacemiT A100** (60 TOPS) | **riscGate** (on-SoC) | toadStool, squirrel | **INCOMING** — INT4/INT8/FP16 |
| FPGA | None in fleet | — | toadStool stubs only | Not planned |

#### Tier D: Edge / IoT / Constrained

| Device | Target | RAM | Feasibility |
|--------|--------|-----|-------------|
| Pi Zero 2W | `armv7-unknown-linux-musleabihf` | 512 MB | bearDog-only beacon. Not a gate. |
| CanaKit Pi 3B+ (2018) | `armv7` / `aarch64` | 1 GB | Below resource floor. Not enrolling. |
| Synology DS224+ | Intel J4125 (DSM) | 2 GB | NFS storage only. No primals on DSM. |
| WASM edge | `wasm32-unknown-unknown` / `wasm32-wasip1` | N/A | 38/48 toadStool crates. Browser compute surface. |

#### Tier E: Exotic / Aspirational (type-check proven, no hardware)

| Target | Platform | Notes |
|--------|----------|-------|
| `powerpc64le-unknown-linux-gnu` | IBM POWER10 HPC | Type-check only |
| `s390x-unknown-linux-gnu` | IBM Z mainframe | Type-check only |
| `loongarch64-unknown-linux-gnu` | Loongson (Chinese sovereign) | Type-check only |
| `sparc64-unknown-linux-gnu` | Oracle SPARC | Type-check only |
| `i686-unknown-linux-gnu` | 32-bit x86 legacy | Type-check only |
| `x86_64-unknown-freebsd` | BSD family | Type-check only |
| `x86_64-unknown-illumos` | Solaris lineage (ZFS origin) | Type-check only |
| `x86_64-unknown-none` | Bare metal x86_64 | ecoPrimals-as-OS concept |
| `aarch64-unknown-none` | Bare metal ARM64 | ecoPrimals-as-OS concept |
| `riscv64gc-unknown-none-elf` | Bare metal RISC-V | ecoPrimals-as-OS concept |

#### ISA × OS Coverage Matrix

| ISA | Linux (musl) | Linux (gnu) | Windows | macOS | Android | iOS | WASM | Bare Metal |
|-----|-------------|-------------|---------|-------|---------|-----|------|------------|
| **x86_64** | PROVEN (6 gates) | PROVEN (GPU layer) | PROVEN (3 gates) | type-check | — | — | PROVEN (38/48) | type-check |
| **aarch64** | PROVEN (grapheneGate) | PLANNED (piGate) | type-check | PROVEN 12/15 (graftGate) | PROVEN (grapheneGate) | GLACIAL (iosGate) | — | type-check |
| **riscv64** | — | ON ORDER (riscGate) | — | — | — | — | — | type-check |
| **armv7** | depot exists | type-check | — | — | — | — | — | — |

#### Deployment Scenario Matrix

| Scenario | Hardware | Composition | Network | Key Proof |
|----------|----------|-------------|---------|-----------|
| Classroom demo | Pi 500 + HDMI monitor | Tower or NUCLEUS | WiFi → drawbridge → golgiBody | $200 live mesh node for students |
| Conference booth | Pi 500 + portable monitor | NUCLEUS | Phone tether or venue WiFi | Sovereign OS on a keyboard |
| Edge AI | Jupiter 2 | Tower + toadStool + squirrel | 10GbE SFP+ or WiFi 6 | 60 TOPS RISC-V inference |
| Portable compute | Steam Deck | Tower + Node Atomic | WiFi | GPU compute from a handheld |
| Home NAS | westGate / reefGate | Nest Atomic | GigE LAN | Provenance-tracked personal data |
| GPU farm | strandGate / biomeGate | Node Atomic / Compute | 10G backbone | QCD, shader validation, silicon deism |
| WAN proof | cloudGate (Oracle ARM) | Tower | WAN → drawbridge | Trust-boundary crossing, NAT traversal |
| Mobile anchor | grapheneGate (Pixel 8a) | Tower | USB tether / WiFi | Beacon seed, physical root of trust |
| Build farm | blueGate + graftGate + sporeGate | tower-builder | LAN mesh | Cross-platform depot: 3 OS families |

## 4. K-Derm Layers — Connectivity Fabric + Three-Domain Topology

Three-layer model identified by peptidoglycan failure incident (Wave 155d).
**Wave 155v**: formalized as **THREE-DOMAIN TOPOLOGY SPEC** (`specs/THREE_DOMAIN_TOPOLOGY_SPEC.md`) mapping each k-derm layer to a DNS domain: primals.eco (outer), nestgate.io (peptidoglycan), primal.eco (inner).
**Wave 155v/156d**: **K-DERM SEPARATION COMPLETE** — primal.eco 6 A records REMOVED from sovereign Knot DNS (inner membrane SEALED). nestgate.io LIVE on mesh (petalTongue v1.7.0). DNSSEC verified. Caddyfile synced from golgi (14 subdomain routes). dnsmasq config ready for inner membrane resolution. `KDERM_DNS_ACTIONS.md` documents remaining ops items.

```
┌─────────────────────────────────────────────────────────┐
│  OUTER MEMBRANE — Human access (RustDesk → relay)       │
│  Route: public internet → relay.primals.eco             │
│  Auth: server key + per-gate password                   │
│  Owner: golgiBody RUSTDESK_MEMBRANE chain               │
│  Failure: NAT rate-limit collapse (2 incidents, fixed)  │
├─────────────────────────────────────────────────────────┤
│  PEPTIDOGLYCAN — LAN/HPC topology fabric                │
│  Hardware: Flints, CRS310, Omada, 10G AOC trunk         │
│  Services: NAT (sporeGate), DHCP, DNS (dnsmasq→stubby)  │
│  Scope: 192.168.4.0/22 flat LAN, both houses            │
│  Anchors: sporeGate (H1) + blueGate (H2)               │
│  Failure: dead dnsmasq on sporeGate (fixed)             │
├─────────────────────────────────────────────────────────┤
│  INNER MEMBRANE — Primal communications                 │
│  Route: songBird :7700 LAN-first + WG fallback          │
│  Auth: capability IPC, TLS, BTSP (15/15), riboCipher    │
│  Owner: per-primal, coordinated by overwatch             │
│  Status: 10-gate mesh, Tower LIVE on 6+ gates, Nest LIVE │
│  Gossip: swarmVine (primal #16) — vine spreads, bat val │
│  Evolution: Phase 2 riboCipher, Phase 3 swarmVine gossip│
└─────────────────────────────────────────────────────────┘
```

### Outer Membrane

- [x] RustDesk relay operational — `relay.primals.eco` → golgiBody
- [x] **RUSTDESK_MEMBRANE iptables chain** — isolated from primal rules
- [x] NAT-aware rate limits: 120 UDP/10s, 60 TCP new/10s
- [x] Port 21114 REJECT with tcp-reset (prevents retry storm poisoning)
- [x] 10 RustDesk peers registered in hbbs DB
- [x] `https://relay.primals.eco` info page active (passphrase-gated bootstrap)
- [x] Cursor rule `.cursor/rules/outer-membrane-rustdesk.mdc` codifies separation
- [x] netfilter-persistent saves (both UDP + TCP fixes survive reboot)
- [ ] LOG before DROP in RUSTDESK_MEMBRANE (visibility for future incidents)
- [ ] House2 Linux gates need RustDesk provisioning (network path proven via blueGate)

### Peptidoglycan

- [x] sporeGate is plasma membrane router — NAT/DHCP/DNS/nftables for house1
- [x] **dnsmasq re-enabled** on sporeGate — sovereign DNS chain: dnsmasq → stubby → upstream
- [x] 10G AOC backbone CRS310↔Omada proven and healthy
- [x] Flat LAN 192.168.4.0/22 — both houses on same broadcast domain
- [x] Anchor model defined: sporeGate (H1) + blueGate (H2)
- [ ] **G29 — Peptidoglycan isomorphism**: DNS is a recurring SPOF. sporeGate dnsmasq dies → all LAN gates lose resolution. strandGate DNS dead (Aug 1). northGate 2-3s page delays (DNS timeout + fallback). Not fully isomorphic yet.
- [ ] DNS: verify dnsmasq on all Linux gates (sporeGate done, others PENDING)
- [ ] northGate DNS delay diagnosis (DNS timeout pattern — likely single-DNS DHCP + slow fallback)
- [ ] strandGate DNS dead (Aug 1, 2026) — systemd-resolved has no working upstream. sporeGate dnsmasq likely down again.
- [ ] Redundant DNS: DHCP should hand out 2+ DNS servers (sporeGate dnsmasq + 1.1.1.1 fallback)
- [ ] dnsmasq health monitor + auto-restart on sporeGate (systemd watchdog or cellMembrane health check)
- [ ] Port→gate mapping incomplete (need physical audit)
- [ ] WiFi bridge documentation (Flint H1 + Flint 2 configs)
- [ ] Standardized gate provisioning script (DNS + RustDesk + health checks)

### Inner Membrane

- [x] **10-gate WireGuard mesh** — golgi, sporeGate, eastGate, flockGate, ironGate, northGate, grapheneGate, westGate, strandGate, **blueGate** (peer #9)
- [x] Tower Atomic LIVE on 6+ gates — westGate, strandGate, grapheneGate, eastGate, sporeGate, blueGate (Windows)
- [x] LAN peering: Tower 353x LAN (0.45ms vs 158ms WG overlay)
- [x] songBird universal-ipc: UDS/named pipes/abstract sockets/TCP
- [x] BTSP defense-in-depth: **16/16** primals (swarmVine from sourDough scaffold)
- [x] **biomeOS neuralAPI**: **27** signal graphs, **v4.57+**: Stage 2 routing infra shipped (578 Neural API tests). G22 convergence (unified namespace, 244 caps). westGate 26 caps registered. `capability.resolve` working. Deploy sequence evolving to register-gossip-verify-in-mesh. **swarmVine gossip integration NEXT** — `capability.resolve` will query swarmVine gossip table for cross-gate routing. (8,700+ tests)
- [x] **songBird ACME HTTP-01** challenge responder shipped — Phase 1 TLS elimination
- [x] songBird mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L
- [x] sporeGate depot fully refreshed: health **11/11 HEALTHY**, **49 binaries** (18 musl + 16 gnu + 15 windows), BLAKE3 verified. swarmVine binary added.
- [x] **Sovereign CI LIVE** — push-to-deploy E2E verified. **Golgi hook FIXED** (3 bugs: dispatcher, case, category).
- [x] ~~WireGuard DNS catch-all~~ — **FIXED** (cellMembrane `8d9bb58`)
- [x] ~~Socket ownership P2~~ — **FIXED** (biomeOS `0e45262f` + v4.54 socket ownership guard)
- [x] ~~rootpulse.ledger~~ — **FIXED** (cellMembrane `0cfcce5`: advisory OK)
- [x] ~~**P2: Sandbox false positive**~~ — **FIXED** (coevolution: cellMembrane `validate_with_deps()` → biomeOS `composition.test_swap`). Depot now serves v4.55.
- [ ] `/run/membrane` permission reset — biomeOS resets dir to 0770 at runtime (P3)

## 5. Sovereignty / Trust — postPrimordial Alignment Check

### Sovereignty Principles — Status

| Principle | Status | Evidence |
|-----------|--------|----------|
| **No external dependencies** | **ALIGNED + G72 TIER 1 COMPLETE** | Pure-Rust TLS. Zero C deps on critical path. **G72 Tier 1 DONE (11/11 teams)**: ~155+ crates shed, tokio surfaces trimmed/gated, dead deps excised (jsonrpsee, wiremock, vulkano, url+ICU, bearDog +41 deps, petalTongue telemetry). **Tier 2 QUEUED**: HTTP client consolidation (reqwest/ureq/hyper → songBird/capability.call), axum 0.7→0.8, wgpu 22→28. |
| **Single source of truth** | **ALIGNED** | Forgejo (golgiBody) is sole canonical remote. GitHub is push-mirror only. |
| **Sole depot** | **ALIGNED** | All genomeBins from `depot.primals.eco`. Sovereign CI auto-publishes. |
| **Portable mesh** | **VALIDATING** | NUCLEUS proven on 4 gates. **southGate = validation gate**: deliberately off WireGuard, deploys from public depot, own genetic lineage, bonding/encryption validation across trust boundary. Proves portability for external deployments. |
| **Silicon deism** | **G66 COMPLETE — PROVEN on 4 platforms** | Linux (musl+gnu), Windows (windows-gnu 12/15), Android (aarch64), **macOS (aarch64-apple-darwin — 12/15 compiled, 80% first-build)**. G66 transport abstraction 15/15. 3 darwin failures logged for code-team resolution. SteamOS NEXT. iosGate GLACIAL. |
| **Zero telemetry** | **ALIGNED** | No telemetry, no analytics, no cloud lock-in across all primals. |
| **AGPL-3.0** | **ALIGNED** | All primals, gardens, springs. scyBorg triple-license framework defined. |
| **Pure Rust crypto** | **ALIGNED** | bearDog Ed25519 signing, BTSP 16/16, riboCipher transport. swarmVine inherits full crypto from sourDough scaffold. |
| **Self-healing** | **ALIGNED + GATE VALIDATED** | biomeOS v4.55: dual-protocol health ping, PID-aware kill-before-spawn, socket ownership guard. westGate: 0% socket loss. strandGate: 1 proc/primal. |

### Interstitial Goals — Alignment

| Goal | Status | Notes |
|------|--------|-------|
| **Reconstitutable from cold** | **VALIDATING (southGate)** | Depot has all binaries, Forgejo has all source. southGate is testing: deploy from public depot, own keys, no WireGuard, no `/etc/environment` inheritance. If NUCLEUS launches clean, reconstitution is proven. |
| **Move to new HPC mesh** | **VALIDATING (southGate)** | southGate = "friend's LAN pool" archetype. Deliberately off WireGuard. If it can bond, accept encrypted work, and return signed results across a trust boundary, the system is portable to any network. |
| **Shut down and restart** | **PARTIAL** | biomeOS `nucleus start` works. But `/run/membrane` is tmpfs, socket permissions reset, no systemd tmpfiles.d. Each gate restart requires manual fixup. |
| **No convenience coupling** | **RISK** | sporeGate's `/etc/environment` with `RUSTUP_HOME`, `CARGO_HOME`, `ECOPRIMALS_ROOT` is gate-specific. SSH key aliases (`golgi`) are in user-specific configs. These are jelly strings. |

- [x] K-Derm three-layer model intact (peptidoglycan documented)
- [x] Forgejo sovereign inner membrane operational (43/43 repos)
- [x] Push mirrors relay to GitHub on commit
- [x] Sovereign outer membrane operational (Caddy TLS)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] **DNSSEC 3/3 domains complete** — primals.eco DS 2371/13/2 chain VERIFIED (Porkbun → .eco TLD → Cloudflare KSK). nestgate.io + primal.eco signed by sovereign Knot DNS (ECDSA P-256, auto re-sign).
- [x] RustDesk AGPL-3.0 compliant — learn-from-leverage posture
- [x] **Sovereign CI LIVE** — push-to-deploy, depot auto-built, BLAKE3 verified
- [x] Crash-loop self-recovery LIVE — app breaker + systemd layers
- [x] Tower Atomic EXCEEDS WG (353x LAN, 1.7x WAN)
- [x] 6/6 exploration domains PROVEN LIVE
- [x] Genetic enrollment — two-layer trust
- [x] BTSP defense-in-depth (16/16)
- [x] Depot provenance — builder=sporeGate, staleness alarm, multi-target
- [x] Crypto delegation — songBird → bearDog, chimera unblocked
- [x] golgiBody sole depot — no local depots, all genomeBins via Caddy TLS
- [x] **cellMembrane reqwest purged** — sovereign HTTP client, pure-Rust TLS
- [x] **Provenance 7/7** — full E2E signed chain, portable across Linux + Windows
- [ ] **PORTABILITY**: cellMembrane site-profile abstraction (decouple from 192.168.4.0/22)
- [ ] **PORTABILITY**: WireGuard endpoint auto-discovery (no hardcoded IPs in peer config)
- [ ] **PORTABILITY**: Depot mirror/relocate (golgiBody is single point of failure)
- [ ] **PORTABILITY**: `pseudoSpore pack/unpack` — reconstitute gate from seed file
- [ ] Phase 2: Tower cutover — shadow active, chimera design drafted
- [ ] Phase 1: Zola → sporePrint primal pipeline (crates.io a sub-goal)
- [ ] Phase 2: Forgejo → rootPulse — via Nest Atomic
- [x] `primal.eco` inner membrane separation — **COMPLETE.** 6 A records removed from Knot DNS. Zero public records. dnsmasq config ready for LAN resolution. Inner membrane SEALED.

## ~~6. Public Surface / Security~~ → **FOSSILIZED as F12** (Wave 155i)

ALL SECURITY ITEMS RESOLVED. sporePrint impulses are an ongoing publishing cadence, not a security concern — tracked under D11 (Campus). Moved to Fossilized section below.

## 7. Compositions / Products — NUCLEUS Convergence

### Atomic Composition Status

```
NUCLEUS = Tower Atomic + Nest Atomic + Node Atomic + biomeOS orchestration
        = bearDog + songBird + skunkBat           (Tower — security + discovery + defense)
        + nestGate + rhizoCrypt + loamSpine + sweetGrass  (Nest — storage + provenance)
        + toadStool + barraCuda + coralReef        (Node — compute + GPU + shaders)
        + biomeOS                                  (orchestrator — all 13)
        + swarmVine                                (cross-layer gossip — vine spreads, bat validates)
        + petalTongue + squirrel                   (agent + rendering surface)
```

| Composition | Status | Gates Proven | biomeOS Orchestrated? |
|-------------|--------|--------------|----------------------|
| **Tower Atomic** (3) | LIVE | 6 gates (incl. Windows, Android) | Signal graphs: 8. Direct IPC: YES. |
| **Nest Atomic** (7+Tower) | LIVE | westGate (ZFS+CAS), blueGate (Windows) | Signal graphs: 9. Graph execution: **FIXED** (v4.47 riboCipher). |
| **Node Atomic** (3+Tower) | VALIDATED | strandGate (746 pipelines/sec, sub-ms GPU) | Signal graphs: 3. |
| **NUCLEUS** (13+3) | **ACHIEVED ×6 — ALL GATES v4.57+ G68-CONVERGED. ZERO P0. NEURAL API CALL PATH UNBLOCKED. 16 PRIMALS. 13,910 CAPS.** | **sporeGate** (15/15), **ironGate** (13/13), **westGate** (13/13, NG-05 done), **strandGate** (13/13), **blueGate** (13/13), **southGate** (13/13) | 27 signal graphs. **All P0s resolved. Mesh-native build dispatch. Deploy evolves: pull → restart → register → gossip-announce → verify-in-mesh.** |

### What's proven

- [x] footPrint LIVE — **708 TS tests, Phase 2 DEPLOYED on ironGate.** CAS E2E. golgi Caddy routing DONE.
- [x] esotericWebb LIVE — **V32, 484+ tests, CELL LIVE on ironGate (13/13 ALIVE).** G68 redeployed. 28 caps, `nest.store` signal decomposition.
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] petalTongue WASM WebGL pipeline shipped + v1.7.0 deployed
- [x] Tower Atomic: 6/6 exploration domains PROVEN, chimera Phase 0 unblocked
- [x] songBird crypto delegation 6/6 COMPLETE — composition model validated
- [x] Composition profiles fixed: `compute` = Tower + node, `nest` = Tower + provenance trio
- [x] `tower-builder` profile created for distributed build mesh nodes
- [x] ~~**biomeOS composition broker**~~ — **SHIPPED** (v4.45): riboCipher framing + BTSP executor + 35 E2E tests
- [x] **biomeOS capability routing E2E**: `content.put` → nestGate, `storage.put` → nestGate, signal graph dispatch routing works
- [x] **westGate COORDINATED mode**: 704 capabilities, 390 translations, 70 signal graphs loaded
- [x] **blueGate Nest 10/10 on Windows** — first multi-composition non-Linux deployment
- [x] **Springs-to-NUCLEUS mesh** — 10 springs/gardens assigned to 5 gates. Cell graphs v2.0.0 with content.get/content.put. biomeOS deploy graphs v2.0.0. tideGlass Cargo workspace created. Inter-gate CAS data access documented.
- [x] **ironGate DOWNSTREAM HOST (Aug 3, G68 redeployed Aug 8)** — esotericWebb V32 (CELL LIVE, 13/13 ALIVE) + footPrint 708 tests (Phase 2 deploy ready). NUCLEUS 13/13. RTX 5070. G19 PROVEN. riboCipher transport validated. BTSP local-trust (G63) is remaining CAS blocker.
- [x] **Wave 155v/156d BROAD EVOLUTION ABSORBED (Aug 4)** — Provenance divergence RESOLVED (122×). Three-domain topology spec'd. 12⁴ paper-ready. Federated CAS + compute memoization spec'd. Nanowire→Primal Builder Phase 2a DONE. squirrel pushed (156d sovereignty). ~135K+ tests. 20 docs fossilized (94 total).

### Path to NUCLEUS — ALL CODE SHIPPED

- [x] ~~**biomeOS graph executor riboCipher fix**~~ — **SHIPPED** (v4.47 `bd202674`)
- [x] ~~**biomeOS socket unification**~~ — **SHIPPED** (unified to `membrane/`, 22 graph TOMLs)
- [x] ~~**biomeOS socket evaporation**~~ — **SHIPPED** (capability persistence to disk)
- [x] ~~**biomeOS full composition lifecycle**~~ — **SHIPPED** (`composition.start` RPC + boot_order integration)
- [x] ~~**bearDog `crypto.sign_ed25519`**~~ — **SHIPPED** (`3739e7078`) — Provenance 7/7 UNBLOCKED
- [x] ~~**Node Atomic live**~~ — strandGate VALIDATED (746 pipelines/sec)
- [x] ~~**NUCLEUS live on one gate**~~ — strandGate + blueGate + sporeGate (v4.47 deployed)
- [x] ~~**NUCLEUS lifecycle**~~ — **SHIPPED** (biomeOS `composition.start` + cellMembrane boot_order)
- [x] ~~**Primal CLI flag standardization**~~ — **SHIPPED** (`specs/PRIMAL_BIND_FLAGS_STANDARD.md`)

### Remaining (deployment + glacial)

- [x] ~~Provenance 7/7 live validation~~ — **COMPLETE** on westGate (Linux/ZFS) + blueGate (Windows)
- [x] ~~westGate NUCLEUS~~ — **DONE** (13/13, 654 caps, 29 sockets, Prov 7/7)
- [x] ~~blueGate lifecycle NUCLEUS~~ — **DONE** (14/14 depot, Prov 7/7 on Windows). **Wave 157c: PRIMARY BUILD AUTHORITY** — 14/14 vertebrate built (23 min), `builder.serve :9800` mesh-native dispatch (Tower Atomic, no SSH). Build authorities: `[blueGate, sporeGate, eastGate]`. 7/14 match depot size within 1%. Logged D1-D4 (songBird PID P2, skunkBat bind-mode, binary size parity P3, petalTongue port P4).
- [x] ~~strandGate redeploy~~ — **v4.55 depot deploy, P1 GATE VALIDATED**: 12/12 HEALTHY, 1,017 methods, 13 procs (1 each).
- [x] ~~**Coevolution (G21)**~~ — **COMPLETE**: biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED. Depot rebuilt.
- [ ] **Cross-platform gates** — steamGate (NEXT, UNBLOCKED), graftGate (GLACIAL), iosGate (GLACIAL)
- [ ] **Chimera Phase 0**: shared library extraction (`libtower.so`) — UNBLOCKED, deferred
- [ ] sporePrint primal pipeline: replace Zola
- [ ] 6 springs pending `validation.json`

## 8. genomeBin / Cross-Platform Deployment

- [x] **5 Tier 1 genomeBin targets**: x86_64-linux-musl, aarch64-linux-musl, x86_64-windows-gnu, aarch64-android, armv7-linux-musl
- [x] **8 Tier 3 PROVEN** exotic architectures
- [x] songBird universal-ipc: UDS/named pipes/abstract sockets/XPC/TCP
- [x] cellMembrane `Platform`: `TargetOs × CpuArch × LinkModel` with `detect()` at compile time
- [x] cellMembrane `InitSystem` dispatch: systemd/launchd/windows-service/bare
- [x] golgiBody sole depot — all genomeBins via `https://depot.primals.eco`
- [x] `bind_mode` and `target` marked transitional in GateProfile
- [x] PowerShell enrollment for Windows gates (`gate-enroll.ps1`)
- [x] Self-registration — gates declare name + composition
- [x] **Startup blurb PROVEN** — westGate: dead checkout → Tower LIVE in 70 min
- [x] HTTPS public pull — zero-auth initial sync for fresh gates
- [x] Shallow roots pattern documented — GitHub clones need fresh Forgejo clone
- [x] `nucleus_launcher.sh` BEARDOG_SOCKET race fixed (westGate I5)
- [x] **strandGate Compute Trio deployed** — Tower + barraCuda + coralReef LIVE
- [x] barraCuda GPU verified on RTX 3090 (source build, SHADER_F64 enabled)
- [x] coralReef 18/18 JSON-RPC dispatch complete, 463 `.expect()` purged, PTX modernized
- [x] ~~P0 glibc~~ — **FIXED**. Depot rebuilt on sporeGate — 16 musl + 3 glibc, BLAKE3 19/19 verified
- [x] J8: Key enrollment portal — **DEPLOYED** (step-ca live at ca.primals.eco)
- [x] Pure Rust across all primals — zero C deps on critical path
- [x] toadStool wgpu cross-platform GPU (DX12/Vulkan/Metal)
- [x] biomeOS platform_native transport on all 27 signal graphs
- [x] biomeOS cross-platform socket templates (named pipes + TCP fallback)
- [x] ~~Windows genomeBins stale~~ — **15/15 REBUILT** (sporeGate Jul 30). membrane.exe NEW. ALL platform gates fixed.
- [x] ~~**songBird Windows platform gate (P0)**~~ — **FIXED + IN DEPOT** (`d9bda555`)
- [x] ~~toadstool.exe~~ **FIXED**. ~~coralreef.exe~~ **FIXED**. ~~beardog.exe~~ **FIXED**. ~~membrane.exe~~ **FIXED** (`4ccbab1`)
- [x] **Depot: 49+ binaries across 5 target directories** (18 musl, 16 gnu, 15 windows-gnu, + aarch64-musl, aarch64-android dirs). swarmVine v0.1.0 (2.4 MB musl) added.
- [x] **Windows cross-arch 15/15 PASS** — `cargo check --target x86_64-pc-windows-gnu` mandated as pre-push. All 15 primals pass (Wave 156z). Not yet in CI automation.
- [ ] **macOS genomeBins** — can't cross-compile from Linux. **graftGate: 12/15 compiled** (Aug 11). First `aarch64-apple-darwin` binaries built. 3 failures need code-team fixes (toadStool cfg gate, squirrel linker flags, petalTongue rustix API). Depot target directory + push remaining. cellMembrane `InitSystem::Launchd` path to be validated.
- [ ] **SteamOS validation** — gnu depot bins may work as-is on Steam Deck (user-space deploy)
- [ ] `target`/`bind_mode` field removal — primals auto-detect, depot negotiates
- [ ] systemd abstraction for launchd paths (cellMembrane `InitSystem` foundation shipped, darwin untested)

## 13. Vertebrate Evolution — Internal Structure via Abstraction (Wave 157a)

**Phase shift**: Cephalization (G64) gave the ecosystem a nervous system — Neural API, biomeOS routing, Tower mesh. Now primals develop **internal skeletal structure**: shared abstractions across crates, domain delegation to the right primal/spring, self-audit for cross-focus that belongs elsewhere. **Vertebrates vs invertebrates** — the primals that evolved first carry early patterns (repeated connect/send/recv, game engines in viz primals, monolithic cores). The newer primals (swarmVine, skunkBat) are already vertebrate — clean, single-domain, minimal deps.

**Philosophy**: Lean by evolution, not excision. No feature-gating. Code moves to its right home. Patterns converge through shared traits. westGate's 7-session retrospective revealed 6 Python jelly strings that exist because primal API surfaces diverged from assumptions — the vertebrate fix is primal self-audit: each team verifies their actual API surface matches what others expect.

| Primal | Binary | Deps | Crates | Lines | Evolution Path |
|--------|--------|------|--------|-------|----------------|
| petalTongue | **33.8 MB** | **656** | 19 | 209K | **doom-core → ludoSpring** (game rendering belongs in a spring). 656 deps need workspace convergence. |
| songBird | **23.8 MB** | 646 | **31** | **470K** | ~~Transport trait~~ DONE. ~~Gossip excision~~ DONE. ~~PID~~ FIXED. ~~riboCipher :7700~~ DONE. **Vertebrate evolution COMPLETE.** |
| biomeOS | **20.4 MB** | 377 | 26 | 302K | P0-C IN DEPOT. Generic capability dispatch. FD self-healing. riboCipher Tier 2 client pool. G69 depot lineage templates. |
| toadStool | **12.4 MB** | 627 | 14 | **708K** | **`core` 272K → natural S371 WASM split.** 24/48 done. |
| bearDog | **8.3 MB** | 556 | **31** | 498K | ~~P0-A~~ **FIXED + IN DEPOT**. Spine signing unblocked. |
| nestGate | **8.5 MB** | 424 | — | — | ~~P0-B~~ RESOLVED. `content.ingest` shipped S136, stale depot was root cause. `content.stat` shipped. Rebuilt. |
| swarmVine | **2.5 MB** | 113 | 2 | 4K | **Vertebrate baseline** — Windows port DONE, Phase 4 shipped, 134 tests. |
| skunkBat | **3.2 MB** | 156 | 4 | 24K | Vertebrate. |
| sourDough | **3.3 MB** | 212 | 3 | 23K | Vertebrate. |

**Evolutionary action items — primals self-audit:**
- [x] **songBird**: ~~(1) Transport convergence~~ **SHIPPED** (`TransportRegistry` + boxed-closure adapter, graceful shutdown wired). ~~(2) Gossip excision~~ **SHIPPED** (`mesh.capabilities_announce`/`revoke` → swarmVine `gossip.forward` UDS). ~~(3) P2 PID~~ **FIXED** (`cleanup_legacy_pid_files()`).
- [ ] **petalTongue**: Move `doom-core` to **ludoSpring** (already optional `doom = ["dep:doom-core"]`). `/ws/scene` WebSocket SHIPPED (G19 foundation).
- [x] **bearDog**: ~~P0-A~~ **FIXED + IN DEPOT** — health guard deployed fleet-wide. Spine signing unblocked.
- [x] **nestGate**: ~~P0-B~~ RESOLVED — `content.ingest` shipped S136, `content.stat` shipped. Rebuilt + deployed.
- [x] **biomeOS**: ~~P0-C~~ **FIXED + IN DEPOT** (`6a51638d`) — `capability.call` operational fleet-wide.
- [ ] **toadStool**: S371 naturally splitting `core` 272K. Continue.
- [x] **All primals**: ~~Self-audit~~ **COMPLETE** — all 13+ primals verified RPC surface matches capability_registry.toml. bearDog, songBird, biomeOS, nestGate, loamSpine, rhizoCrypt, barraCuda, coralReef, cellMembrane, squirrel, skunkBat all self-audited. Zero phantom methods fleet-wide.
- [ ] **Dep convergence → G72 Dependency Pandemic — TIER 1 COMPLETE**: **11/11 teams responded. ~155+ crates shed fleet-wide.** rhizoCrypt: 316→270 (-14.6%). nestGate: 424→414 (-10) + S147/S148 crate surgery. loamSpine: 306→299 (-7). toadStool: 7 dead deps + 6 workspace-promoted. sweetGrass: bincode/chrono removed. coralReef: optional dep gating. cellMembrane: time/macros trimmed. tideGlass: tokio→current-thread. wetSpring: verified clean. **bearDog: +41 dead deps removed, tokio["full"] eliminated.** **petalTongue: telemetry crate removed, runtime discovery replaces 13 hardcoded peers.** **Tier 2 QUEUED.** See `specs/DEPENDENCY_PANDEMIC_SPEC.md`.
- [ ] **Depot**: Track binary sizes in `sizes.toml` for regression detection.

## ~~9. Documentation / Fossil Record~~ → **FOSSILIZED as F11** (Wave 155h)

ALL ITEMS RESOLVED. Moved to Fossilized section below.

## ~~10. Jelly Strings~~ → **FOSSILIZED as F14** (Wave 156h)

ALL ITEMS RESOLVED. J9–J19 (11/11 KILLED or LIVE E2E). J12 evolution (SSH → songBird IPC) is a G62 concern, not a jelly string. Moved to Fossilized section below.

## 12. gen5 — Full NUCLEUS as Live Platform (NEW)

gen4 is COMPLETE (4 NUCLEUS gates on v4.55, Provenance 7/7, Sovereign CI, coevolution).
gen5 is **NUCLEUS as a usable platform** — validated by strandGate Node Atomic landmark:
2,130 matmul/sec, cross-atomic provenance E2E (GPU→sign→verify→DAG→attribution→Merkle),
W3C PROV-O, AlphaFold 20-30 structures/day capacity. **gen5 thesis VALIDATED.**

### The Full NUCLEUS Stack — Graph of Sub-Graphs

NUCLEUS is not a flat list of primals — it is a **graph of composition sub-graphs**.
Each atomic composition is a sub-graph with internal dependency ordering. A primal
can appear in multiple future compositions. `biome.yaml` defines which sub-graphs
a gate runs. biomeOS graph executor starts/routes/orchestrates through compositions.

```
┌─────────────────────────────────────────────────────────┐
│  NUCLEUS = graph(Tower, Nest, Node, cross, surfaces)    │
│  biome.yaml = composition manifest (BYOB per gate)      │
│  biomeOS = graph executor (Hamiltonian — runs the graph)│
├─────────────────────────────────────────────────────────┤
│  ┌─── Tower Atomic sub-graph ───┐                       │
│  │ bearDog → songBird → skunkBat │  trust + mesh + def  │
│  └──────────────────────────────┘                       │
│  ┌─── Nest Atomic sub-graph ────┐                       │
│  │ nestGate → rhizoCrypt →       │  CAS + DAG +         │
│  │ loamSpine → sweetGrass        │  spine + braids      │
│  └──────────────────────────────┘                       │
│  ┌─── Node Atomic sub-graph ────┐                       │
│  │ toadStool → barraCuda →       │  dispatch + compute  │
│  │ coralReef                     │  + shaders           │
│  └──────────────────────────────┘                       │
│  ┌─── Cross-layer ──────────────┐                       │
│  │ swarmVine (gossip)            │  ant colony           │
│  └──────────────────────────────┘                       │
│  ┌─── Surfaces ─────────────────┐                       │
│  │ petalTongue (render/viz)      │  photon              │
│  │ squirrel (AI agent)           │  observer            │
│  └──────────────────────────────┘                       │
├─────────────────────────────────────────────────────────┤
│  primalSpring = experimental ground for compositions    │
│  Prototypes biome.yaml, validates sub-graph lifecycle,  │
│  leads future spring composition patterns               │
└─────────────────────────────────────────────────────────┘
```

### What NUCLEUS Enables — gen5 Workloads

| Workload | Stack | Gate(s) | Status |
|----------|-------|---------|--------|
| **Scientific visualization** | hotSpring → toadStool → petalTongue (QCD, molecular) | westGate, strandGate | Node Atomic validated, petalTongue WASM ready |
| **Game engine / creative** | esotericWebb → petalTongue → coralReef (shaders, WebGL) | **ironGate** (downstream host) | **V32, 484+ tests, CELL LIVE on ironGate (13/13).** G68 redeployed. 28 caps. Needs petalTongue WebGL pipeline (G19) for browser surface. |
| **AI agent orchestration** | squirrel (4,613 tests, 90.1% cov, G18 wired) → biomeOS neuralAPI → any primal | any NUCLEUS gate | Capability routing proven (835+ caps) |
| **Genomics pipeline** | wetSpring → toadStool → nestGate (16S rRNA, GPU) | strandGate (RTX 3090) | Pipeline validated, cold (needs data) |
| **NF drug reversal (Gonzales/Bin)** | tideGlass → Nest Atomic → Provenance Trio → petalTongue (GPS viz) | westGate | 214 tests, CAS + petal clients wired, GPS data CONVERTED, 2.5 TB CAS federated. Cell boot NEXT. Mid-term: Cell 2026 rebuild → NF screen → CTF NDU |
| **GIS data** | footPrint → nestGate → petalTongue | **ironGate** (downstream host) | Matures petalTongue G19 → reusable for tideGlass GPS viz |
| **Protein structure** | AlphaFold ~1TB → Nest Atomic CAS → provenance | westGate (ZFS 50.7TB) | Data on northGate, pipeline READY |
| **helixVision** | Genomics + AlphaFold + rendering | multi-gate | Orchestrator role. *(coralForge retired — helixVision is the canonical name.)* |
| **Cross-platform deploy** | cellMembrane → depot → any chip + drive | all gates | 35 binaries, 3 platforms proven |

### Platform Readiness — What's Wired vs What Needs Wiring

| Component | Proven? | What's Next |
|-----------|---------|-------------|
| biomeOS neuralAPI dispatch | **YES — 578 tests, Stage 2 infra shipped (riboCipher pool, auto-transition, TOML caps)** | **N2-N5 verification (primalSpring owns). Fleet-wide boot registration. Capability gossip (Phase 3).** |
| petalTongue WebGL/WASM | YES (6,605 tests, v1.7.0) | Live renders fed by Node Atomic GPU output |
| toadStool GPU dispatch | YES (746 pipes/sec, sub-ms) | petalTongue consumer pipeline |
| coralReef shaders | YES (WGSL/SPIR-V/PTX) | esotericWebb game shader pipeline |
| barraCuda tensor math | YES (FP64 104T, RTX 3090) | hotSpring QCD live computation |
| squirrel AI agent | YES (4,613 tests, 90.1% cov, G18 wired, 156b: 400s→16s) | biomeOS neuralAPI routing, user-facing agent |
| Nest Atomic CAS | YES (3,252 objects, ZFS) | Data ingestion pipelines (AlphaFold, NF) |
| Provenance Trio | YES (7/7 E2E) | Every workload gets provenance tracking |

### gen5 Dual-Science Pipeline

Two mid-term science tracks drive ecosystem evolution. Both consume the same primals, but exercise different capabilities. The support structures (footPrint, esotericWebb on ironGate) mature petalTongue (G19), which then serves both tracks.

**Track A — NF Drug Repurposing (Gonzales/Bin Chen)**
tideGlass rebuilds Cell 2026 GPS platform → NF drug reversal screen → CTF NDU grant.

- [x] **Step 1**: Provenance 7/7 — **DONE**
- [x] **Step 2**: westGate data federation — **3.21 TB / 153 datasets / 2.5 TB CAS federated, convoy COMPLETE (145/s). GPS data CONVERTED.**
- [x] **Step 3**: tideGlass specs shipped (ARCHITECTURE, MODULE_SPECS, DATA_ACCESS, PHASE_0_CHECKLIST, VISUALIZATION)
- [ ] **Step 4**: tideGlass Phase 0 — Zenodo inventory + RGES reproduction (Python). **NEXT.**
- [ ] **Step 5**: Phase 1 — reproduce all 7 modules against published claims
- [ ] **Step 6**: NF reversal screen (novel application)
- [ ] **Step 7**: NF pseudoSpore — **THE gen5 ARTIFACT** (G38)
- [ ] **Step 8**: CTF NDU grant application (G39)

**Track B — Lattice QCD on Consumer GPUs (Murillo/Chuna)**
hotSpring arXiv Rung 1 → 6-rung QCD program → vendor-agnostic physics.

- [x] **Step 1**: barraCuda DF64 GPU compute — **DONE** (FP64 104T on RTX 3090)
- [x] **Step 2**: hotSpring SU(3) pure gauge — **DONE** (5,500 traj/hr, plaquette validated)
- [x] **Step 3**: Gauge group resolved — **SU(3) confirmed**, paper relabel needed
- [ ] **Step 4**: arXiv Rung 1 submission — **PREPRINT 41/42.** NPU silicon continuum integrated (§2.9, §4.7). MILC Δ=3×10⁻⁹. β-scan receipt (7 β-values, 8⁴ SU(3)). Murillo claims audit done. **Wire live site → pseudoSpore → reviewer send.** |
- [ ] **Step 5**: Rung 2 — quenched fermions
- [ ] **Step 6-8**: Rungs 3-6 (dynamical → (2+1)-flavor → finite-T → cross-vendor)

**Support → Science convergence**: footPrint (GIS) + esotericWebb (CRPG) on ironGate mature petalTongue's live render pipeline (G19/G53). The same petalTongue then provides: GPS visualization for tideGlass NF screening (volcano plots, enrichment curves, MCTS traces) + QCD visualization for hotSpring (lattice configs, plaquette evolution, HMC trajectories). The downstream products are not just products — they are infrastructure maturation targets.

### sporePrint — Live Platform as Public Surface

sporePrint is subGen presented to the world. Design: **science first, infrastructure second**.
But the infrastructure IS the product — NUCLEUS running live workloads, not a static site.

Visitor flow: see live science → notice it runs on commodity HW → grab pseudoSpore → discover mesh.

**Sequencing**:
1. Phase 1 (NOW): sporePrint content refresh to Wave 155m reality
2. Phase 2: Live workload surfaces (QCD viz, game engine, GIS, genomics)
3. Phase 3: PseudoSpore grab pattern (NF as first downloadable artifact)
4. Phase 4: projectFOUNDATION auto-feeds from provenance

### Glacial Goals — Post-Threshold Checkpoint (Aug 1, 2026)

**COMPLETE (17 goals — proven on live hardware):**

| ID | Goal | Evidence |
|----|------|----------|
| G3 | Provenance Trio 7/7 | 8th consecutive pass. First real data (PDB+ChEMBL) at 100% provenance. |
| G4 | NUCLEUS on multiple gates | **×6**: westGate, strandGate, blueGate, sporeGate, southGate, **ironGate** (21/21 HEALTHY). |
| G8 | Plasmodium (multi-gate bonding) | southGate 22/22 PASS. BTSP trust without WireGuard. 29,294 foreign rejections. |
| G10 | Sub-builder mesh | J12 LIVE E2E. **Wave 157c: MESH-NATIVE** — `builder.serve :9800` Tower Atomic dispatch (no SSH). blueGate primary build authority. |
| G17 | Portability — reconstitute from cold | southGate: public depot + own entropy + user-space + no WG = 20h NUCLEUS. |
| G21 | biomeOS-cellMembrane coevolution | composition.test_swap + validate_with_deps. |
| G22 | biomeOS API convergence | Single-process dual-protocol. Validated on 3 gates. |
| G29 | Peptidoglycan isomorphism | 3-way DNS: sporeGate + blueGate H2 + golgi mesh. |
| G31 | Batch RPC for provenance pipeline | RESOLVED — superseded by G55 convoy (217/s, 460x). `dag.event.append_batch` LIVE. |
| G55 | Provenance batch RPCs (braids at machine speed) | RESOLVED — 700x. 217/s NVMe, 265/s inline, 4-tier storage. |
| G59 | Three-domain topology (k-derm website separation) | DNS COMPLETE. All 3 layers separated. primal.eco SEALED. nestgate.io LIVE. DNSSEC verified. |
| G64 | Cephalization — tarpc convergent evolution | C2 15/15, G65 15/15, C8 done (-67K lines). All primals dual-protocol. Graduated Wave 156q. |
| G65 | Protocol Negotiation — single-socket dual-protocol | 15/15 primals. squirrel origin, sourDough reference. Spec: `specs/PROTOCOL_NEGOTIATION_SPEC.md`. Graduated Wave 156q. |
| G66 | Transport Abstraction — silicon-agnostic IPC | 15/15 modules shipped. 15/15 Windows cross-arch PASS. sourDough reference. Spec: `specs/TRANSPORT_ABSTRACTION_SPEC.md`. Graduated Wave 157a. |
| **G68** | **Platform Substrate Abstraction** | **16/16 prod-clean, 16/16 cross-arch. 205→0 production violations.** sourDough scanner v2. toadStool S363→S368 (24→0). cellMembrane 15 cfg→3. Graduated Wave 157a. |

**ACTIVE (22 goals — in progress or unblocked):**

*Ecosystem checkpoint (Wave 157a): G68 fossilized (17th COMPLETE). G7+G30, G15+G36, G56+G67 merged (duplicate scopes). G49+G50 reclassified GLACIAL. Deploy infrastructure solved — frontloading primal evolution. Neural API becoming required system.*

| ID | Goal | Status | Next Step |
|----|------|--------|-----------|
| G7/G30 | westGate data federation & ingestion | **3.3 TB on ZFS — 153 datasets, 989K+ files braided inline.** Convoy COMPLETE (145/s, 460x). AlphaFold v6 42/46 proteomes. **7-session retrospective filed**. **All 3 P0s RESOLVED**: ~~P0-A bearDog~~ CODE FIXED, ~~P0-B nestGate~~ RESOLVED (stale depot), ~~P0-C biomeOS FD~~ FIXED (`6a51638d`). Pipeline API fixed. | `native_braid.py` → Rust. Depot rebuild deploys P0-A+C fixes fleet-wide. Spine commit signing unblocked once depot is current. *(Merged G7+G30.)* |
| G9 | arXiv publication (Murillo/Chuna QCD) | **PREPRINT 41/42.** NPU silicon continuum integrated (§2.9, §4.7 rewritten, §7, Appendix A). SU(N) N=2→8, 69 cached configs. β-scan receipt: 7 β-values on 8⁴ (β=2.0→6.5), plaquettes match literature. MILC bidirectional Δ⟨P⟩=3×10⁻⁹. NPU ESN: 100% accuracy (11 features, MCC=1.0). Murillo claims audit complete. | Wire live site (pseudoSpore artifact, `validate.sh`, reviewer JupyterHub). Then reviewer send. |
| G11 | Any chip + drive = mesh gate | ACTIVE | biomeGate + ironGate proved. steamGate NEXT. |
| G14 | sporePrint live science refresh | ACTIVE | pseudoSpore LIVE. Auto-publish FIXED. |
| G18 | squirrel → biomeOS agent orchestration | **LIVE on ironGate** | 9 providers, cross-primal dispatch validated (Session 10). Wire footPrint agent panel next. |
| G19 | petalTongue + Node Atomics live rendering | ACTIVE | hotSpring QCD viz + esotericWebb. |
| G20 | esotericWebb game engine on NUCLEUS | **CELL LIVE — G68 REDEPLOYED** | **V32** — 484+ tests, 28 caps, 13/13 ALIVE on ironGate. `nest.store` signal decomposition validated. Needs petalTongue WebGL pipeline (G19) for browser surface. |
| G32 | Silicon deism vendor cracking | **NEW — biomeGate** | 3-GPU bench (RTX 5060 + Tesla + Titan V). coralReef diesel engine. hotSpring cross-vendor validation. |
| G35 | Fully agentic LAN | **7/8 DONE** (biomeGate joined mesh). | northGate + flockGate blocked (physical access). `membrane remote.enroll` proposed. |
| G15/G36 | tideGlass NF archaeology & GPS reproduction | **ACTIVE** (214 tests, CAS wired, 5 viz scenes) | GPS data CONVERTED (11 JSON, 103 MB CAS). `content.query` WIRED. PetalTongueClient coded. 17 IPC methods. Cell boot on westGate NEXT (CAS federation now live). Mid-term: **sovereign rebuild of Cell 2026 GPS platform.** *(Merged G15+G36 — same tideGlass track, phased.)* |
| G37 | NF Reversal Screen (Gonzales NF collaboration) | **ACTIVE** | RGES vs LINCS, ZINC compound screening, MEK inhibitors (selumetinib) in top-100. NF Data Portal ingested (658 files). Depends G36. |
| G38 | NF PseudoSpore artifact | **ACTIVE** | Self-verifying USB: data + code + provenance. `./validate` runs 7 tideGlass modules. **First gen5 science deliverable.** |
| G39 | CTF NDU grant ($125K) | **ACTIVE** | Preliminary data package for Children's Tumor Foundation NDU. Depends G36+G37. |
| G43 | steamGate — immutable OS handheld | **ACTIVE** | Steam Deck OLED. User-space musl deploy on read-only SteamOS. G17 pattern. |
| G44 | reefGate — paired intelligence/storage | **ACTIVE** | DDR3 NUC + Synology DS224+ NFS. G23 fractional replication target. |
| G45 | Lattice QCD Rungs 2–6 (Murillo/Chuna program) | **ACTIVE — SU(N) GENERALIZED** | GaugeGroup trait covers N=2,3,4,5,6,8. Rung 1 reframed from SU(3)-only to full SU(N) ladder. 87-config thermalization grid running on 64 EPYC threads (~2wk). `arxiv_measure_battery` ready. 30 finite-T configs for deconfinement T_c/√σ analysis. SU(N>=4) GPU shaders need generalization (WGSL hardcoded for 3x3). |

**GLACIAL (24 goals — future phases):**

| ID | Goal | Status | Dependency |
|----|------|--------|------------|
| G6 | bearDog public (crates.io) | GLACIAL | crates.io publishing |
| **G12** | **graftGate (M4 Mac Mini)** | **ACTIVE — TOWER RUNNING** | M4 arrived Aug 10. **Tower Atomic built + running Aug 11** — 4th platform proven (G11). iPhone XS tethering. First `aarch64-apple-darwin`. Remaining: full mesh enrollment, WireGuard, depot push, NUCLEUS lifecycle (launchd). cellMembrane `InitSystem::Launchd` validation. Unblocks G13 (iosGate). |
| G13 | iosGate (iPhone) | GLACIAL | graftGate + Dev Program |
| G16 | pseudoSpore grab pattern on web | GLACIAL | After NF data + tideGlass |
| G23 | nestGate CAS fractional replication | GLACIAL | Data redundancy schema exists |
| G24 | Sovereign Identity Garden | CONCEPT | Gate-first (cameras/sensors), phone later |
| G25 | bearDog StrongBox/Secure Enclave | GLACIAL | Gate-connected first, phone later |
| G26 | sweetGrass zero-knowledge attestations | GLACIAL | Prove encrypted data properties |
| G27 | mitoBeacon identity genetics | GLACIAL | Person-level cryptographic DNA |
| G28 | Cross-platform sovereign identity | GLACIAL | Depends on G12 + G13 |
| G34 | Outer membrane egress masking | GLACIAL | Flint as boundary router. Single opaque tunnel to golgi. ATT box sees nothing. Spec exists, no implementation. |
| G40 | cloudGate — WAN enrollment validation | GLACIAL | Oracle ARM VM, NAT traversal, trust-boundary crossing |
| G41 | piGate — resource-constrained ARM proof | GLACIAL | RPi 5, ~$125 edge gate |
| G42 | riscGate — RISC-V third ISA | GLACIAL | StarFive VisionFive 2, open-ISA |
| G46 | Show HN public launch | GLACIAL | 28-item rubric. Blocked until NF pseudoSpore + sporePrint |
| G47 | projectFOUNDATION auto-feed | CONCEPT | Provenance-driven knowledge layer, thread lineage |
| G48 | projectNUCLEUS product packaging | CONCEPT | NUCLEUS product + pseudoSpore delivery pipeline |
| G49 | lab.primals.eco periplasmic JupyterHub | GLACIAL | Reviewer-access interactive compute on ironGate |
| G50 | initioChem pseudoSpore (ABG track) | GLACIAL | Whole-cell expression artifact |
| G51 | Inkfish/Valve marine collaboration | CONCEPT | Marine genomics, coral holobiont science |
| G52 | blueFish PFAS QC (Jones track) | GLACIAL | EPA 1633A open PFAS QC |
| G53 | petalTongue maturation via downstream consumers | **ACTIVELY WIRING** | **footPrint**: `petal-bridge.ts` dual-socket WS↔UDS relay (agent→squirrel, viz→petal) WIRED. Auto-load. CSP dedup. **tideGlass**: `PetalTongueClient` ACTIVATED (dead_code removed, `is_viz_method()` gate, fire-and-forget forwarding). **nestgate.io**: 20 primals discovered, 8/12 dashboard sections, Tower Atomic architecture view. **Conjugation**: RustScript (`@protokarya/rustscript`) is the TS conjugation layer — 11 modules. |
| G54 | Dual-science mid-term convergence | **ACTIVE** | **Track A (NF/GPS — Gonzales/Bin)**: tideGlass rebuilds Cell 2026 paper → NF drug repurposing → CTF NDU grant. **Track B (QCD — Murillo/Chuna)**: hotSpring arXiv Rung 1 → 6-rung lattice QCD program. Both tracks consume barraCuda (GPU math), petalTongue (viz), provenance trio (chains), nestGate (data). Infrastructure evolves toward both simultaneously. |
| ~~G56/G67~~ | ~~**Neural API activation & Stage 2 routing**~~ | **FOSSILIZED as F15** | N-series 90/91. All P0s deployed fleet-wide. `capability.call` operational. **Evolution continues as G70 (composition graph executor).** |
| **G70** | **Neural API as composition graph executor** | **ACTIVE — POST-PANDEMIC ENMESHMENT** | **NUCLEUS is a graph of sub-graphs.** **Wave 157i enmeshment**: (1-9 from 157g all CLOSED). (10) **G72 Tier 1 COMPLETE** (9/9 teams, ~114 crates shed). (11) **Gossip injection 3→6/16 LIVE** (barraCuda 19 events, esotericWebb 2, lithoSpore synced; wetSpring 2/4 partial; hotSpring scaffold). (12) **P2 braid.verify CLOSED** (sweetGrass behavioral tests). (13) **projectNUCLEUS `nucleus-deploy verify --manifest`** — 29/29 PASS on ironGate (schema, membership, composition kinds, cycle detection, federation). (14) **hotSpring pseudoSpore E2E pipeline** shipped (compute→manifest→bundle→sign→register — pure Rust). **Remaining**: depot rebuild (new gossip binaries), songBird MeshRelay (blueGate + southGate blocked), sourDough live checks (`convergence`+`rpc-surface`), hotSpring gossip wiring (10 events scaffold), multi-composition orchestration, primalSpring modernization, graftGate bootstrap + enrollment. |
| G57 | nestgate.io data identity surface | **PHASE 2 — 10/12 sections + trust surface routes** | `/api/content/stats` (live CAS from rhizoCrypt), `/pseudospore/` (5 bundles), `/api/pseudospore/bundles` — all LIVE. mesh.peers WIRED. 20 primals discovered. **NG-05 CLOSED** (westGate CAS federation). Data Braids card can now query westGate TCP. Remaining: wire Data Braids card against westGate `192.168.4.149:8080`. |
| G58 | Mixed provenance convergence | **ACTIVE** | Promote all westGate data from primordial/CAS-only to fully braided. `is_dataset_converged()` gate for springs. Revalidation running for priority + AlphaFold. All spring-critical data fully braided before Phase 4 boot. |
| G60 | Federated CAS (nestgate.io cross-gate data surface) | **ACTIVE — FEDERATION ENDPOINT SHIPPED** | **petalTongue `/api/content/federation`** (`84e6e48`): combines local rhizoCrypt CAS stats with swarmVine data-topic gossip entries. Mesh-wide content availability via Tower Atomic transport (no SSH). As gates inject `cas.have` + `braid.head` entries, they appear automatically. **biomeOS gossip integration** (`993b97f7`): `capability.resolve` → swarmVine gossip table → targeted mesh dispatch. L1 cache on golgi for hot objects still needed. |
| G61 | Compute memoization via provenance trio | **ACTIVE** | strandGate thermalized lattice configs as CAS objects with provenance braids. 37 min CPU thermalization → instant on cache hit. Same BLAKE3→CAS→DAG→braid pattern as data acquisition. Cross-gate: biomeGate pulls configs for parity checks. Parallel pipeline: GPU produces while CPU thermalizes next β. NFT-style braids for both config and production results. |
| ~~G62~~ | ~~Nanowire → Primal Builder (mesh-routed builds)~~ | **FOSSILIZED as F16** | Phase 2a+2b DONE. Mesh-native dispatch + depot push LIVE. blueGate primary builder. **Remaining** (glacial): biomeGate 2nd sub-builder, `compute.capacity` gossip. |
| G63 | BTSP local-trust (SO_PEERCRED for same-gate UDS) | **ACTIVE** | nestGate accepts same-gate callers without full BTSP X25519 handshake. Process-level auth via `SO_PEERCRED` — membrane group callers are trusted by filesystem perms. Unblocks footPrint CAS write, tideGlass CAS integration, all gardens/protists on same gate. Zero config, maximally primal-like. Proposed in footPrint Phase 2 deploy ready handoff. |
| **G71** | **Science pipeline E2E** (strandGate → ironGate → sporePrint) | **ACTIVE** | First complete science artifact: GPU data → pseudoSpore → NFT → reviewer. Needs: ironGate NFT endpoint, sporePrint QCD page, petalTongue data viz, `validate.sh` → Rust. strandGate campaign 22/45. |
| **G72** | **Dependency Pandemic — Stadial Shift** | **TIER 1 COMPLETE (11/11)** | **Biological pandemic evolution — Tier 1 DONE.** 11/11 teams responded: toadStool (EXEMPLAR — tokio 118→65, 7 dead deps, plugin-loading/vulkano excised, ~73 GiB reclaimed), rhizoCrypt (-46 crates, 14.6%), nestGate (jsonrpsee -1,864 LOC, -10 crates, S147/S148 crate surgery), loamSpine (url+ICU -7 crates), sweetGrass (tokio trimmed, bincode/chrono removed), coralReef (optional dep gating), cellMembrane (rt-multi-thread→dev-deps), tideGlass (rt→current-thread), wetSpring (verified clean), **bearDog (+41 dead deps removed, tokio["full"] eliminated)**, **petalTongue (telemetry crate removed, runtime discovery replaces 13 hardcoded peers)**. **~155+ crates shed fleet-wide.** **Tier 2 QUEUED**: HTTP → songBird/capability.call (nestGate ureq first), axum 0.7→0.8 (5 projects), wgpu 22→28 (toadStool), YAML unification, tokio::sync→std::sync audit. **Tier 3**: sourDough dep validator, archaic pattern excision. See `specs/DEPENDENCY_PANDEMIC_SPEC.md`. |
| — | Chimera Phase 0 (shared library) | GLACIAL | Deferred |
| — | Zola → sporePrint primal pipeline | GLACIAL | Replace static site gen |

## 11. Campus / Physical Infrastructure

- [x] Lansing Scuffle vision documented (10 docs, 120K+ in whitePaper/lansingScuffle/)
- [x] Property profile: 1305 S Cedar St, 464K SF, 8 MW, 600-ton HVAC
- [x] Economics model: 5 revenue stages, SBA 504 math, AGPL consulting
- [x] K-Derm zone mapping applied to building floors
- [x] Thermal sovereignty loop designed
- [x] footPrint GeoJSON location added
- [x] sporePrint transplant + credibility audit DONE
- [ ] sporePrint ongoing: 5 impulses for maturity badges (migrated from D6)
- [ ] Building tour / physical access not yet arranged

---

# FOSSILIZED DIMENSIONS

*Fully complete. Not re-checked unless regression signal appears.*

## F1. Glacial Shift (fossilized Wave 150p, completed Wave 137b)

8/8 criteria cleared. No regression through 14+ waves.

## F2. Content-Addressed Convergence (fossilized Wave 150p, completed Wave 143b)

ALL 6 LAYERS COMPLETE. Architectural pattern fully solved.

## F3. Silicon Atheism (fossilized Wave 150p, completed Wave 145a)

Phase 1 (cross-compile) and Phase 2 (transport) COMPLETE.
14/14 primals on all 4 depot architectures. Evolved into Dimension 8 (genomeBin).

## F4. Depot / Build Pipeline (fossilized Wave 150p, completed Wave 150n)

59+ binaries, BLAKE3 + Ed25519 signed, 4 architectures, `require-signed` enforced.
Sovereign CI hooks deployed to 29 repos on golgiBody.

## F5. Cascade Pipeline / Convergence (fossilized Wave 150p, completed Wave 150k)

43/43 repos converged on Forgejo-first. Push mirrors relay to GitHub.

## F6. Tower Atomic Deep Analysis (fossilized Wave 150x, completed Wave 150x)

4-team convergence sprint. Analysis docs and composition map fossilized.

## F7. sporePrint Transplant (fossilized Wave 150x, completed Wave 150x)

Transplant shipped, credibility audit landed. External claim convergence established.

## F8. Tower Atomic Completion + Depot Convergence (fossilized Wave 151a)

Tower Atomic sprint (150v–151a) fully resolved. All P0/P1 items closed.
Tower debt: 36 → 1 (grapheneGate HSM only).

## F9. BTSP Sub-Wave + Publication Strategy (fossilized Wave 151d)

BTSP sub-wave (151b–151d) fully resolved. All 13 primals shipped ClientHello.
Publication strategy: whitePaper gen/ review COMPLETE, JOSS defined.

## F10. Autonomous Gate Enrollment (fossilized Wave 155b)

Zero-operator postPrimordial enrollment fully shipped:

- songBird `mesh.gate_enroll`: 6-phase pipeline
- bearDog FIDO2 enrollment attestation + beacon proximity proof
- cellMembrane Phase 7: gate.enroll → mesh.enroll
- Dynamic IP pool, K-Derm inward escalation, trust tiers
- `gate-enroll.sh` (Linux) + `gate-enroll.ps1` (Windows)
- golgiBody drawbridge: Caddy TLS → `/enroll/*` → songBird
- Self-registration: gates declare name + composition

## F11. Documentation / Fossil Record (fossilized Wave 155h)


All documentation infrastructure complete and current:

- ECOSYSTEM_BLURB.md universal handoff (Tracks A+B converged)
- PRIMAL_REGISTRY.md refreshed — merge conflicts resolved, 15-primal posture
- freshness.toml updated to Wave 155h (38 HEAD SHAs)
- 12 standards wave tags reviewed and bumped (Wave 63–139 → 155h)
- Team startup blurb template issued and validated (westGate + strandGate)
- GLOSSARY.md refreshed (Wave 155b)
- gate-enroll.sh + gate-enroll.ps1 documented
- whitePaper gen/ review COMPLETE
- 42+ docs fossilized in fossilRecord/
- coralForge retired — **DEAD** (empty repo, 0 commits). Canonical successor: helixVision (gardens/). All active references converged.
- Peptidoglycan + Provenance Trio AARs filed
- 17+ handoff docs from Wave 155f–i (code teams + AARs + Nest Atomic)

## F12. Public Surface / Security (fossilized Wave 155i)

All security infrastructure complete and operational:

- 6/6 surfaces healthy (sporeprint, footprint, live, webb, lab, git)
- Security headers deployed (HSTS, CSP, X-Frame-Options)
- fail2ban + rate limiting active
- TLS auto-renewing (ACME)
- Tower pen test: 7 scenarios, all PASS, 0 remaining findings
- sporePrint transplant DONE + credibility audit
- External claim convergence standard issued
- sporePrint impulses (ongoing cadence) tracked under D11 Campus

## F13. Jelly Strings — Deployment Automation (fossilized Wave 155i)

Manual deployment shell loops → primal-native Rust automation: **ACHIEVED**.

- J1–J6: ALL CLOSED (harvest, depot push, service restart, Caddy config, WG peer reg, systemd overrides)
- J7: Legacy detection — one-time P3, deprioritized (does not block any deployment)
- J8: Key enrollment portal — DEPLOYED (step-ca live at ca.primals.eco)

7/8 code-complete + deployed. All deployment automation that was manual is now
primal-native. J7 is a one-time cleanup task that does not affect the dimension's
completeness.

## F14. Jelly Strings — Sovereign CI Pipeline (fossilized Wave 156h)

J9–J19 (11/11 KILLED or LIVE E2E). Full sovereign CI pipeline operational:
Forgejo push → cascade → diff → build → checksum → depot push → verify.

- J9–J13: Cascade/build/depot triggers — ALL KILLED
- J12: Sub-builder dispatch — LIVE E2E (SSH-first, songBird IPC evolution → G62)
- J14–J19: Socket ownership, checksums, self-CI, tmpfiles, env coupling, sandbox — ALL KILLED

sporeGate + blueGate sub-builder + cellMembrane portability. SSH → songBird
evolution tracked under G62 (Nanowire → Primal Builder).

## F15. Neural API Activation + Debt Clearing (fossilized Wave 157g)

Neural API activation (G56/G67) COMPLETE — 90/91 verified, deployed fleet-wide:
- N1–N6 all SHIPPED and VERIFIED
- exp118 14/14, exp119 12/12, exp120 29/29, exp121 35/36
- `capability.call` operational: 1.3ms westGate, 4ms ironGate
- riboCipher Tier 2 CLOSED, auto-detect SHIPPED
- All P0s (bearDog, nestGate, biomeOS) resolved + deployed
- 1 remaining: toadStool tarpc protocol mismatch (architecture decision, not P1)

Debt clearing COMPLETE:
- S1–S7, O1–O8, B1+B2 ALL RESOLVED
- C2 dual-socket 15/15
- G64 cephalization, G65 protocol negotiation, G66 transport abstraction — all 15/15
- C8 squirrel excision -67K lines
- Cross-arch 16/16 PASS (`cargo check --target x86_64-pc-windows-gnu`)

**Evolution continues as G70 (Neural API as composition graph executor).**

## F16. Nanowire → Primal Builder (fossilized Wave 157g)

Mesh-native build dispatch fully operational:
- blueGate `builder.serve :9800` Tower Atomic (no SSH)
- Build authorities: `[blueGate, sporeGate, eastGate]`
- Depot push SOLVED (blueGate → golgi SSH key authorized)
- swarmVine `DepotManifest` gossip type shipped
- Remaining glacial: biomeGate as 2nd sub-builder, `compute.capacity` gossip integration

---

**Active**: 10 dimensions (1–5, 7–8, 11–13)
**Fossilized**: 16 dimensions (F1–F16)
**Summary**: Wave 157i POST-PANDEMIC ENMESHMENT. G72 Tier 1: **11/11 teams complete, ~155+ crates shed fleet-wide.** toadStool tokio 118→65 (45%). bearDog +41 deps. petalTongue telemetry excised. Gossip 3→7/16 LIVE (barraCuda **22/22** full spec, wetSpring **4/4**, nestGate 11 CAS sites). P2 braid.verify CLOSED → **0/0/1** (petalTongue port only). **graftGate Tower Atomic RUNNING on macOS — 4th platform proven (G11).** nestGate S147/S148 (1,666 tests). hotSpring pseudoSpore E2E pipeline shipped. Three-tier blurb system formalized. Gate×Team matrix rationalized. **16 primals. 0 P0. 0 P1. 1 P2. ~150K+ tests.**

**Phase shift**: **"Interstadial selects for lean primals."** The pandemic response was immediate and universal — all 11 addressed teams shed vestigial dependencies within a single wave. The interstadial is demonstrably underway: Tier 1 complete (11/11, ~155+ crates), Tier 2 queued (HTTP→songBird, axum→0.8, wgpu→28). graftGate proves the 4th platform (macOS, `aarch64-apple-darwin`) — Tower Atomic runs with minimal edits, validating G68/G66/ecoBin standard. The gossip mesh thickens: 7/16 primals inject runtime events, barraCuda reaches full 22/22 spec coverage, wetSpring completes 4/4, nestGate wires 11 CAS sites. hotSpring ships the first complete science artifact pipeline (pure Rust, zero Python). The composition layer solidifies: NUCLEUS manifest verification (29/29), biome.yaml consumption proven, graph executor prototyped. Gate×Team deployment matrix rationalized — code teams aligned to hardware specialization. Three-tier blurb system formalized (gate spin-up → K-NOME code prompts → ecosystem cascade). The **next pressure**: Tier 2 consolidation + graftGate full enrollment + remaining gossip wiring + songBird MeshRelay.

**151+ files fossilized** across 14 checkpoints (1,570+ total records). Active handoffs: 8 (GATE_SPINUP_BLURB.md added, 2 templates superseded).
- **ironGate: DOWNSTREAM SURFACE.** **REDEPLOYED** (depot v4.57.0, dispatch 13-17ms). esotericWebb V32 CELL LIVE. NF GPS + ABG + MILC targets. G18 LIVE. 12.7 TB CAS. RTX 5070.
- westGate: **DATA BRAIDS DEPOT + FULL RETROSPECTIVE.** 3.3 TB / 989K files braided / 153 datasets / 2.5 TB CAS. Vine-bat operational, 14/14 services. **7-session AAR filed**: chunked spine braiding, middle-out parallel, convergence tiering (88%→12% NVMe), inline atomic ingress. **3 P0s documented**: bearDog sign stub, nestGate API mismatch, biomeOS FD leak. Pipeline API fixed (`content.ingest→content.put`). Jelly string inventory mapped.
- strandGate: **COMPUTE + SILICON FOLD COMPLETE.** **13/13 ALIVE.** **15/15 silicon units accessible and measured** (only tensor cores driver-blocked → coralReef SASS). **AMD 20x faster root cause**: Infinity Cache (128 MB) keeps 12⁴-16⁴ working sets cache-resident; NVIDIA L2 (6 MB) causes VRAM thrash. **F16 1.32x free speedup on AMD** (native packed f16 vs NVIDIA widening). **RT Cores operational** (NVIDIA 22x advantage for BVH). **250-2500x MILC** for stencil ops. Cross-GPU pipeline 0.16% overhead. IC cliff confirmed at 128 MB. Tiling: 16⁴ = hardware-natural tile size. Upstream: barraCuda absorbs `RiverScheduler`, `TileDecomposer`, `VideoCodec`, buffer negotiation. toadStool absorbs `silicon_capability_registry`. AMD buffer limit fix (`i32::MAX`). **Video encoding: 61:1 NVENC compression** (236 MB config → 3.85 MB). 75/87 thermalization cached.
- **sporeGate: TOPOLOGY OWNER + FALLBACK BUILDER.** **DEPOT UNIFIED + PRUNED (Wave 157d)** — 60 primal binaries, 4 arches, BLAKE3SUMS all. **G69 Depot Lineage spec published.** All P0 fixes IN DEPOT. Build authorities: `[blueGate, sporeGate, eastGate]` — mesh-native dispatch (no SSH). blueGate → golgi push SOLVED (SSH key authorized). **15/15 ALIVE**, 13,910 caps. Vine-bat operational. songBird mesh 11 peers.
- biomeGate: **GPU LAB + CRANKSHAFT.** 3 VFIO GPUs. toadStool Akida. coralReef cross-arch FIXED.
- eastGate: **OVERWATCH + CODE TEAMS.** 64 GB DDR5. squirrel 4,090 tests (C8 done, -67K lines). toadStool S371 (24/48 WASM). primalSpring owns hardware cascade + Neural API evolution. biomeOS routing infra activated. cellMembrane service decomposition shipped. **swarmVine + songBird teams local** — epidemic spread + seam wired from eastGate.
- blueGate: **WINDOWS + PRIMARY BUILDER.** 14/14 vertebrate built (23 min). `builder.serve :9800` mesh-native dispatch (Tower Atomic, no SSH). Build authorities: `[blueGate, sporeGate, eastGate]`. ~~D1 PID~~ FIXED. ~~D2 bind-mode~~ resolved. D3 binary size parity P3. ~~D4 petalTongue port~~ P4 open. golgi push SOLVED (SSH key authorized).
- southGate: **VALIDATION.** Re-validated (13/13, Tower 0.15ms, 19 Gbps).

**11 gates ONLINE** (6 NUCLEUS 157e-deployed, 1 crankshaft + agentic, 4 other). graftGate M4 ARRIVED (12th gate imminent). **17 glacial goals COMPLETE** (G3, G4, G8, G10, G17, G21, G22, G29, G31, G55, G59, G64, G65, G66, **G68**, **G56/G67** (F15), **G62** (F16)).
**21 ACTIVE** (G7/G30, G9, G11, **G12**, G14, G15/G36, G18, G19, G20, G32, G35, G37, G38, G39, G43, G44, G45, G53, G54, G57, G58, G60, G61, G63, **G70**, **G71**, **G72**).
**24 GLACIAL/CONCEPT**.
**67+ total glacial goals** tracked.
**ZERO P0. ZERO P1. 1 P2.** G72 Tier 1 complete (11/11, ~155+ crates). Gossip 7/16 (barraCuda 22/22). graftGate Tower RUNNING. nestGate S147/S148. Three-tier blurb system. Gate×Team matrix. **NEXT PHASE: G72 Tier 2 (HTTP consolidation + axum + wgpu) + graftGate full enrollment + songBird MeshRelay + remaining gossip wiring.**

~~**DEBT CLEARING + NEURAL API ACTIVATION**~~ — **FOSSILIZED as F15 + F16 (Wave 157g).**
All debt items resolved. Neural API 90/91 verified, deployed fleet-wide. Cross-arch 16/16 PASS. See F15 + F16 below.

**REMAINING — TARGETED WAVES FROM HERE:**
- ~~**G68 convergence**~~: **16/16 prod-clean, 16/16 cross-arch. COMPLETE.** 205→0 production violations. toadStool S363→S368 (24→0). cellMembrane 15 cfg blocks eliminated (1,327 tests).
- ~~**Phase A**~~: **DONE** — cascade timer LIVE on sporeGate (15m systemd, G68 membrane, zero drift).
- ~~**Depot rebuild + deploy**~~: **DONE** — **sporeGate rebuilt Aug 8**: biomeOS v4.57.0 + songBird + cellMembrane + swarmVine, golgi 18/18 musl. sporeGate **15/15 ALIVE** (1,958 caps, 4ms dispatch, 11 mesh peers). FD exhaustion fixed.
- ~~**Gate redeploy**~~: **ALL 6 GATES DEPLOYED on 157e depot (Wave 157e).** Phase 1 CLEAR (strandGate + sporeGate). Phase 2 COMPLETE (westGate + blueGate + southGate + ironGate). Performance canary PASS. **FOSSILIZED.**
- ~~**Neural API evolution**~~: **ALL PHASES CODE-COMPLETE. DEPLOYED FLEET-WIDE.** riboCipher Tier 2 CLOSED. All P0s deployed. `capability.call` operational (1.3ms westGate, 4ms ironGate). **NEXT PHASE: Neural API as primary composition interface** — all consumers route through `capability.call`, graph executor for multi-step workflows, gossip-based cross-gate discovery.
- **toadStool long-tail → G72 Exemplar**: S377 manifest CONVERGED. S378 Tokio 118→65 files (45% reduction, round 2). S379 G72 Tier 1 COMPLETE: 7 dead deps removed, 6 promoted to workspace, `tokio::fs` eliminated (28 files→`std::fs`), plugin-loading/vulkano/core-wgpu excised, ~73 GiB reclaimed across S377-S379. Pattern: feature-gate vestigial behind `legacy-*`. ~65 files of real async remain (irreducible: server, IPC, daemon). **38/48 WASM** (79%) — wiring improved (ExecSpec::Wasm, infer_runtime_type), count flat.
- ~~**cellMembrane long-tail**~~: **G69 Phase 1+2+3 COMPLETE (Wave 157g).** 1,353 tests. 0 clippy. 13-commit evolution + sourDough CI wiring (`2430a0b`: 4 static validators in golgi post-receive across 15 primal repos, advisory). **Remaining**: `native_braid.py` → Rust (last major jelly: 1,259 LOC Python). `convergence`+`rpc-surface` live validators not yet wired.
- **Springs**: tideGlass cell boot, hotSpring viz, esotericWebb browser surface.
- **arXiv**: strandGate production campaign 22/45 (~6h remaining). Wire live site + pseudoSpore + reviewer send.
- **Wave cadence**: targeted primal waves. No more ecosystem-wide convergence days.
- ~~**G68 COMPLETE. DEPLOY COMPLETE.**~~ **FOSSILIZED.** Deploy infrastructure + mesh convergence solved.
- **NEW: Neural API escalation** — biomeOS becomes THE interface. `capability.call` as standard routing for all consumers. Graph executor for complex workflows. Neural API registry as single source of truth. Pepti layer + data federation + Neural API = three-pillar architecture.
- **G72 Dependency Pandemic — Tier 1 COMPLETE (11/11)**: ~155+ crates shed fleet-wide. toadStool tokio 118→65 (45%), rhizoCrypt -46 crates (14.6%), nestGate jsonrpsee -1,864 LOC + S147/S148, loamSpine url+ICU -7, bearDog +41 dead deps removed, petalTongue telemetry excised. All primals verified clean or trimmed. **Tier 2 QUEUED**: HTTP→songBird (nestGate ureq first), axum 0.7→0.8 (5 projects), wgpu 22→28 (toadStool), YAML unification, tokio::sync→std::sync audit. **Tier 3**: sourDough dep validator, archaic pattern excision. See `specs/DEPENDENCY_PANDEMIC_SPEC.md`.

### ECOSYSTEM CHECKPOINT — DEPLOY SOLVED, PRIMAL EVOLUTION FRONTLOADED (Aug 8)

**Old patterns cleared:**
- ~~Gate-local `cargo build`~~ → golgi depot pull (~30s)
- ~~Manual golgi depot sync~~ → cascade auto-push (zero drift)
- ~~GitHub deploy keys / `github` remotes~~ → Forgejo-first, K-Derm relay
- ~~Manual capability registration~~ → `mesh.register` at boot (cellMembrane shipped)
- ~~WG+SSH for inner membrane RPC~~ → songBird LAN-first mesh (Phase 1 DONE)

**New patterns enforced:**
- Deploy lifecycle: `pull → restart → register → gossip-announce → verify-in-mesh`
- Sovereign fetch: `plasmid.fetch --source forgejo` (all gates)
- LAN-first: `SONGBIRD_LOCAL_PEERS` seeds cross-house peers
- Gossip-first: swarmVine epidemic gossip for capability/data/compute (replaces songBird broadcast for capability discovery)
- Cascade: 15min timer, auto-harvest, auto-push, zero drift
- Dep pandemic (G72): external deps shed as compositions close gaps — HTTP→songBird, tokio surface minimized, version splits unified

**Inner membrane evolution roadmap:**
- **Phase 1 DONE**: songBird mesh connectivity (westGate + strandGate seeded)
- **Phase 2 COMPLETE — CHAIN CLOSED**: riboCipher Tier 2 (`0xED` mito-obfuscated cross-gate transport)
  - bearDog: ~~`decode_mito_tag`~~ **SHIPPED** (`RiboCipherHandler` — 16th handler kind, 4 methods, auto-announced)
  - biomeOS: ~~client pool~~ **SHIPPED** (`ConnectionPool::send_mito_jsonrpc` — `[0xED, 0x01]` + mito-tag, Tier 1 fallback)
  - songBird: ~~accept `0xED` on :7700~~ **SHIPPED** — `dispatch_ribocipher_rpc()` replaces stub, full `IpcServiceHandler` dispatch on mito-framed connections
  - skunkBat: evolve from REJECT to delegate-and-route (P2, future)
- **Phase 3 ACTIVE → Phase 4 SHIPPED**: Capability + data + compute federation via swarmVine (primal #16)
  - **swarmVine**: epidemic gossip engine. **134 tests.** Windows port DONE. **Phase 4 shipped**: `gossip.subscribe` (broadcast channel), `BloomFilter` (CAS have-set), `ComputeCapacity` scheduling hints, `DepotManifest` for binary distribution gossip. Deep debt clean (zero hardcoded paths, IPv6 fix, nonce contention eliminated).
  - **songBird seam LIVE** (`6b580cf0`): `ipc.register` fires `gossip.inject` to local swarmVine. Fire-and-forget — both paths (songBird announce + swarmVine gossip) run in parallel.
  - **skunkBat `metadata.analyze` SHIPPED** (`e602e09`): 8-check gossip pre-accept validation (topic validity, key format, origin identity, TTL bounds, payload size, freshness, lifetime, quarantine). Returns allow/warn/block verdict. 672 tests (+16). **Vine-bat loop enabled.**
  - **biomeOS gossip table SHIPPED** (`993b97f7`): `capability.resolve` → swarmVine `gossip.query` → targeted mesh dispatch. Fallback chain: local discovery → gossip hints → targeted → broadcast. 7 new tests. `discovery_gossip.rs` + `mesh.rs` targeted dispatch.
  - nestGate/loamSpine: inject `cas.have` + `braid.head` data gossip entries (loamSpine 4 events LIVE via `gossip.inject` UDS)
  - **barraCuda 22/22 events FULLY WIRED** (compute, tower, shader, dispatch, quota, OOM, precision — recovered, precision-degraded, systemic-error final 3 wired). **FULL SPEC COVERAGE.**
  - **esotericWebb 2 session lifecycle events LIVE** (V33 gossip mesh enmeshment).
  - **wetSpring 4/4 LIVE** (all events hooked).
  - **nestGate gossip hooks at 11 CAS sites**, 6 event types (S147/S148).
  - hotSpring: 10 gossip events defined (scaffold — not yet hooked at call sites).
  - **Cross-gate gossip LIVE**: westGate → sporeGate, eastGate, strandGate within 30s. 4-gate mesh confirmed. ironGate listening, not yet peered. blueGate + southGate blocked (need MeshRelay).
- **Phase 4 FUTURE**: WG deprecation for inner membrane (keeps outer membrane + human ops)

**MID-TERM SCIENCE TRACKS**:
- **Track A (NF/GPS)**: G15→G36→G37→G38→G39. Gonzales/Bin Chen. tideGlass rebuilds Cell 2026 → NF reversal screen → CTF NDU $125K.
- **Track B (QCD)**: G9→G45. Murillo/Chuna. arXiv Rung 1 → 6-rung lattice QCD on consumer GPUs.
- **Support convergence (G53)**: footPrint + esotericWebb on ironGate → petalTongue G19 → GPS viz (Track A) + QCD viz (Track B).

**Gauge group resolved in code** (G9): SU(3) labels disambiguated in barraCuda/hotSpring. Paper/site relabel still needed (sporePrint scope). arXiv UNBLOCKED.

**Open items — prioritized by data pipeline + springs readiness:**
- ~~**G55: Batch RPCs for provenance**~~ — **RESOLVED (460x)**. Convoy at 145/s. Primals never the bottleneck.
- ~~**G59: Three-domain topology**~~ — **DNS SEPARATION COMPLETE.** All 3 layers separated. primal.eco SEALED. nestgate.io LIVE on mesh. DNSSEC verified. Trust surfaces live (3 routes). ~~Remaining: deploy dnsmasq, wire content backend, brand nestgate.io.~~ Content backend wired. dnsmasq ops tracked under D4 peptidoglycan.
- ~~**G56: Neural API activation**~~ — **FOSSILIZED as F15.** All routing operational. Evolution continues as G70.
- **G57: nestgate.io** — **PHASE 1 LIVE** (petalTongue mesh). 4 DIVs: content backend, discovery service, port conflict, branding. Phase 2: depot+provenance browser. Phase 3: federated CAS API.
- **G58: Mixed provenance convergence** — promote primordial → braided for all spring-critical data. `is_dataset_converged()` gate. Revalidation running.
- ~~**nestGate canonical client crate (O8)**~~ — **RESOLVED.** Reframed as Neural API wiring — consumers use `capability.call("content", "get", ...)` through coordinator. No primal-specific crate needed. 5 domains, 6 federation methods, MeshRelay transport wired.
- ~~**biomeOS cell attachment CLI**~~ — **SHIPPED** (`biomeos nucleus attach`, v4.57).
- ~~**toadStool ExecStart fix + socket perms (B1+B2)**~~ — **FIXED.** Dir 0o750 (group-traversable), socket 0o660 (group-connectable). Cell boot unblocked on all gates.
- ~~**footPrint CSP + auto-load**~~ — **RESOLVED.** `petal-bridge.ts` wired. `SKIP_CSP=1`. `autoLoadDefaultProject()`. Remaining: squirrel UDS socket on ironGate.
- **esotericWebb HEAD method (E3)** — GET 200 / HEAD 502. HTTP handler missing HEAD support (NG-06). petalTongue WebGL pipeline still needed for live game surface.
- ~~**nestgate.io mesh bridge + mesh.peers (S7)**~~ — **PHASE 2 LIVE.** Neural API bridge discovers 20 primals, **9/12 sections** functional. mesh.peers WIRED (songBird UDS). Remaining: health liveness per primal (S8/NG-03), bearDog routing stub (NG-04).
- **squirrel deploy on ironGate (E2)** — petal-bridge routes `agent.*` → squirrel UDS but squirrel process needs to be running. Deploy as systemd service with `squirrel.sock` at canonical path.
- ~~**nestGate dual-path CAS (O4)**~~ — **SHIPPED.** `NESTGATE_WARM_PATHS` + `NESTGATE_COLD_PATHS` for 2-tier. 7 CAS handlers updated. Backward-compatible.
- ~~arXiv plaquette ×4 normalization~~ — **RESOLVED** (gauge group mismatch SU(2)→SU(3). 12⁴ data paper-ready. Rung 1 UNBLOCKED).
- ~~squirrel → biomeOS G18 integration~~ — **LIVE on ironGate** (Session 10). 9 providers, cross-primal dispatch validated.
- Inter-gate content.get live test (songBird probes + nestGate content.fetch ready)
- petalTongue WebGPU/wgpu evolution (G53 maturation) — conjugation layer (RustScript) established, petalTongue render pipeline is the remaining gap
- ~~barraCuda PRNG validation~~ — **FIXED** (YELLOW→GREEN, statistical validation harness)
- ~~BTSP transport signal documentation~~ — SHIPPED

---

*Last used*: Wave 157i POST-PANDEMIC ENMESHMENT. G72 Tier 1: 11/11 teams complete, ~155+ crates shed. Gossip 7/16 LIVE (barraCuda 22/22, wetSpring 4/4, nestGate 11 CAS sites). graftGate Tower Atomic RUNNING on macOS — 4th platform (G11). nestGate S147/S148 (1,666 tests). Three-tier blurb system formalized. Gate×Team matrix rationalized. 10 ACTIVE dims, 16 FOSSILIZED. 17 goals COMPLETE, 21 ACTIVE, 24 GLACIAL. 16 primals. 0 P0. 0 P1. 1 P2. ~150K+ tests. (Aug 11, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 157g — F15 + F16. (170+ total across 16 checkpoints, 1,590+ total records)
*Latest checkpoint*: Wave 157i — G72 Tier 1 COMPLETE (11/11), graftGate Tower macOS (G11 4th platform), old startup template superseded, three-tier blurb system formalized.
*Latest reopen*: Wave 155k (D10 — Jelly Strings J9–J13, extended to J14–J19 in 155n)
