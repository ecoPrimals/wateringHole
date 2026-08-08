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
- [x] **ZERO P0 / ZERO P1 / ZERO P2.** All P1s GATE VALIDATED. P2 platform detection FIXED (`d7026d7`).
- [x] **NUCLEUS ACHIEVED on 5 gates** — westGate, strandGate, blueGate, sporeGate, **southGate (VALIDATION GATE 22/22 PASS)**. Gate validation AARs fossilized.
- [x] **Depot v4.57+ SYNCED** — 52 builds (13 primals × 4 targets). **ALL 6 NUCLEUS GATES DEPLOYED.** golgi depot pushed. Harvest scheduler shipped (cellMembrane CI-EVO-01).
- [x] **biomeOS v4.56 SHIPPED** — G22 convergence steps 1+2: unified namespace, 244 caps, 47 deps removed.
- [x] **westGate ZFS rebuilt** — mirror → raidz1, 25.4 → 50.7 TB usable. AlphaFold DB fits.
- [x] **Golgi post-receive hook FIXED** (3 bugs: dispatcher, case, category). Sovereign CI E2E verified.
- [x] **cellMembrane 1,281+ tests** — MEMBRANE_*, crypto dedup, J16+J13+J19 killed, registry API hardened.
- [x] **squirrel -48,672 lines** (Waves 156e→156z deep cleanup). 3 orphan crates excised, 157 functions de-asynced, PluginV2 dead code eliminated, PrimalType + EcosystemPrimalType fossils deleted, config crate removed. 313 files changed. 0 unsafe, 0 clippy.
- [x] **Provenance 7/7 COMPLETE** — E2E validated on westGate (5th consecutive pass) + blueGate (Windows)
- [x] **Sovereign CI LIVE** — push-to-deploy E2E verified for ALL 13 primals including biomeOS (coevolution).
- [x] **Coevolution contract COMPLETE (G21)** — biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED (`652cf8a7`).
- [x] **151 files fossilized** across 10 checkpoints. Latest: `wave156d_data_flow_activation/` (8 files). Active handoffs: 7 (BLURB + 6 active refs). **1,472 total fossil records.**
- [x] **whitePaper convergence (G22)**: **COMPLETE** — biomeOS v4.56 single-process merge. Dual-protocol (riboCipher + JSON-RPC) in one process. Validated on westGate + sporeGate.
- [x] **Portability checkpoint (G17) — PROVEN.** southGate 22/22 PASS. NUCLEUS from public depot, own entropy, user-space paths, no WireGuard, no inherited identity. 20h stable, 32 sockets, 76MB RSS, 29,294 foreign peer rejections.
- [x] **DATA FEDERATION (westGate)** — **519 GB, 130 datasets, 9+ domains, ~260K+ files, CAS 5,800+**, 100% provenance. tideGlass 7/7 COMPLETE. AlphaFold v6 42/46 proteomes. 50+ public sources. `data_catalog.toml` v2.0.0 shipped. **Inter-gate experiment comms over 10G LAN ENABLED.**
- [x] **Peptidoglycan DNS G29 COMPLETE** — 3-way redundancy: sporeGate dnsmasq (primary) + blueGate dnsproxy H2 secondary (LIVE) + golgi mesh DNS. Confirmed by sporeGate infrastructure verification.
- [x] **strandGate v4.56 DEPLOYED** — Carry-forward resolved. G22 confirmed. GPU QCD: 38-58× speedup, 5,500 traj/hr. hotSpring composition validated on live NUCLEUS.
- [x] **sporePrint DEMONSTRATION ERA** — 334→190 pages. pseudoSpore LIVE at primals.eco/pseudospore/. Hype cleaned (20 files). Tests: 116,930. First arXiv draft scaffolded.
- [x] **arXiv Rung 1 REFRAMED** — "Toward Vendor-Agnostic Lattice QCD on Consumer GPUs: SU(2) HMC with DF64 WebGPU/WGSL and Cryptographic Provenance." AI review absorbed. Scope ladder, plaquette normalization eq, precision matrix added. LaTeX updated. 6-rung research program defined. Experiment queue ACTIVE (β-scan, HMC diagnostics, increased stats).
- [x] **westGate persistence HARDENED** — ZFS auto-import, 13/13 NUCLEUS units enabled, boot dependency chain, daily snapshots, monthly scrub. 9/9 boot check PASS.
- [x] **hotSpring v0.6.32** — Deep debt clear. 627 tests, 0 clippy. thiserror migration. Files refactored. **v0.6.32 deprecation cleanup**: 24K+ LOC fossilized (low_level MMIO, 15 experiment bins, 51 fossilized bins moved to archive). `fleet_client`/`fleet_ember` deprecated → toadStool. **Rung 1 science COMPLETE** — all physics validated, 3 remaining items are upstream (naga bug, sporePrint URLs).
- [x] **publications/ directory** — Auditable data transfer point for papers + pseudoSpore. Lattice QCD data centralized with full audit trail.
- [x] **golgi auto-publish fix** — THREE compounding bugs fixed: (1) worktree ownership mismatch (`git:git` vs `root:root`), (2) missing `--force` flag on `zola build`, (3) SSH config pointing at wrong golgi IP. sporePrint now deploys correctly to both inner and outer membrane.
- [x] **ironGate ONLINE** — Dev loop validated. Tower Atomic deployed (bearDog 10.6 MB + songBird 16.7 MB + skunkBat 2.6 MB). Forgejo SSH + HTTPS + depot all verified. 42 repos synced. Mesh: golgi 38ms, sporeGate 77ms, eastGate 78ms. **Ready for esotericWebb (G20).**
- [x] **P2 RESOLVED: GPU PRNG polyfill bias** — Root cause: WGSL transcendental polyfills (`log_f64`, `sqrt_f64`, `cos_f64`) in Box-Muller momentum shader produced wrong variance. Three-path comparison proves GPU MD pipeline is correct (bit-exact 4e-17). `cpu_mom` workaround deployed — CPU generates momenta, GPU does all MD at full speed. Section 3.2 UNBLOCKED. Finding strengthens the paper (validation methodology).
- [x] **SPRINGS-TO-NUCLEUS MESH (Aug 2)** — All 10 springs/gardens assigned to gates by hardware specialization. Cell graphs v2.0.0 (content.get + provenance trio + gate metadata). tideGlass Cargo workspace LIVE. biomeOS deploy graphs v2.0.0. Inter-gate CAS data access config created. ecosystem_manifest v3.3.0 with spring_mesh assignments.
- [ ] **PLANNED SERVICE INTERRUPTION (Aug 2)** — ATT gateway + DS224+ moving to basement. steamGate + reefGate enrollment queued post-move.

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~140K+ primal tests validated this wave** (songBird 14,840, bearDog 14,019, nestGate 1,630+, toadStool 9,193+, biomeOS 8,570+, squirrel ~5K (post-cleanup), petalTongue 6,615, barraCuda 4,959, coralReef 3,580, rhizoCrypt 1,791, loamSpine 1,752, sweetGrass 1,655, cellMembrane 1,281+, **tideGlass 220**, primalSpring 197, skunkBat 609, sourDough 518, **footPrint 708**, **esotericWebb V31c (484)**, bingoCube 31)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **14,019** tests, crypto.sign SHIPPED, dual-socket fix, FAMILY_SEED precedence, 94 orphan files purged (**Wave 155m**)
- [x] songBird: **14,840+** tests, universal-ipc, ACME HTTP-01, TCP registration fix, **`mesh.connectivity_check` + `mesh.throughput` SHIPPED (20 mesh methods)** (**Wave 155p**)
- [x] nestGate: **1,630+** tests (94 IPC methods, 21 capability domains), `content.ingest` + `dataset.convergence` + dual-path CAS + Neural API wiring (O1/O3/O4/O8 CLEARED)
- [x] toadStool: **9,193+** tests, **B1/B2: membrane socket perms FIXED** (dir 0o750, socket 0o660, cell boot unblocked on all gates) (**Wave 156e**). `akida-chip` absorbed from rustChip (`3f75aa5e7`). **G68-prod ACHIEVED (S363→S368)**: 24→0 production violations. `select_backend` gated, `akida device open` migrated, musl ioctl fixed (S366), Layer 2 internal gating (S368). **Long-tail**: extending platform abstraction to all deployment types as hw-safe owner of Node Atomic. (**Wave 157a**)
- [x] biomeOS: **8,700+** tests (578 Neural API), **v4.57+**: G67 forwarding fix + Stage 2 routing infra. riboCipher dual-lane pool, Bootstrap→Coordinated watcher, TOML capability translations. 59.3 GiB cargo clean. Cross-arch PASS. (**Wave 157a**)
- [x] petalTongue: **6,755** tests, CAS storage discovery refactor, canonical `get_family_id()`, hardcoded primal names removed (**Wave 156b**)
- [x] barraCuda: **4,959** tests, RTX 3090 profiled, C2 dual-socket shipped, GPU buffer alignment panic FIXED, 13 ignored tests promoted to active, 214 clippy warnings eliminated. (**Wave 156k**)
- [x] ~~**barraCuda YELLOW**~~ → **GREEN**: PRNG half-range fixed (xoshiro 52→53 bits). Statistical validation harness. -1,488 LOC (LazyLock→const, error helpers). `cpu_mom` remains production HMC path (Box-Muller transcendental polyfill, not PRNG).
- [x] coralReef: **3,580** tests, C2 dual-socket, SPIR-V extraction, binary ops + memory ops coverage. Deep debt clean. (**Wave 156k**)
- [x] cellMembrane: **1,327** tests, **P2 platform detection FIXED** (`d7026d7`), `TargetArch` deprecated → `Platform::detect()`, `validate_with_deps()`, J19+J16+J13 killed, registry API hardened. **Wave 157a platform abstraction**: 15 `#[cfg(unix)]` blocks eliminated across 6 files → 3 bind-point-only cfg gates. `sync_ipc.rs` centralizes IPC. BTSP handshake genericized to `impl Read + Write`. Process lifecycle in platform substrate. -150 LOC. (**Wave 157a**)
- [x] rhizoCrypt: 1,900 tests, BTSP→DAG bridge, cross-gate provenance
- [x] loamSpine: **1,752** tests, `spine.status` SHIPPED (53 JSON-RPC + **37 tarpc** methods, S6 CLEARED), **G64 tarpc-CONVERGED** (first primal with full domain parity), zero unsafe/unwrap/TODO
- [x] sweetGrass: **1,655** tests (47 methods + 11 aliases), `convergence.check` + `braid.list` SHIPPED (S1/S2/S3 CLEARED). LedgerClient refactor compiles clean. (**Wave 156f**)
- [x] squirrel: **C8 DONE — -67,090 lines** total (Waves 156e→157c). 257K→190K lines, 16→12 crates, 4,090 tests. G66 transport abstraction. G65 protocol negotiation origin. 0 unsafe, 0 clippy. **`signal.dispatch` WIRED (G18).** (**Wave 157c**)
- [x] primalSpring: **1,263 tests, 197 scenarios, 95 experiments.** Post-primordial reshape: `primordial-compat` feature-gated, 10 experiments migrated to NeuralBridge, `trio_ops/` shared utilities extracted, session-scoped provenance model. (**Wave 157a**)
- [x] skunkBat: 9 threat types, ConnectivityAnomaly, frame crypto, PUBLIC
- [x] **BTSP 13/13** → **15/15** — all primals shipped ClientHello
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
- [ ] **darwinGate** (Mac Mini) — GLACIAL. Needs HW acquisition. First apple-darwin target.
- [ ] **iosGate** (iPhone) — GLACIAL. Needs darwinGate + Apple Dev Program. Walled garden research.
- [ ] fieldGate OFFLINE (dead CMOS)
- [x] **biomeGate GPU CRANKSHAFT LIVE** — Threadripper 3970X, 128GB. 3 GPUs on VFIO: RTX 5060 (host/wgpu) + Titan V (GV100 SM70) + K80 (GK210×2 SM37, **unretired**). toadStool + hotSpring built. coralReef **3,553 tests PASS**. 44-experiment revalidation matrix staged. Exp 231 (K80 cross-gen quench) first-ever hardware run queued.
- [ ] Complete port→gate mapping (CRS310 + Omada + TL-SG605S-M2)
- [ ] Document Flint H1 + Flint 2 + Omada WiFi bridge configs

### Gate Fleet — Status Matrix

| Gate | Status | Platform | Mesh IP | Composition | Role |
|------|--------|----------|---------|-------------|------|
| golgiBody | ONLINE | Linux | 10.13.37.1 | thin-relay | Sole depot, enrollment, Forgejo, Drawbridge |
| sporeGate | ONLINE | Linux | 10.13.37.2 | full | Build authority, depot, cascade hub, **peptidoglycan anchor H1** |
| eastGate | ONLINE | Linux | 10.13.37.5 | full | Code hub, overwatch. i9-12900K, **64 GB DDR5**, Z790-P WIFI |
| ironGate | **NUCLEUS (13)** | Linux | 10.13.37.7 | **NUCLEUS (13)** | **DOWNSTREAM HOST.** G18 DISPATCH LIVE (9 providers). 12.7 TB CAS on `/mnt/nestgate`. songBird federation to westGate. i9-14900K, RTX 5070, 94 GB. esotericWebb + footPrint LIVE. |
| flockGate | **DOWN** | Linux | 10.13.37.6 | full | Rebooted, RustDesk locked out. esotericWebb → **ironGate** |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090. **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | **NUCLEUS v4.57+ (restart deferred)** | Linux | 10.13.37.10 | **NUCLEUS (13)** | GPU at 100% QCD. Config cache COMPLETE (9/10 16⁴ configs, 325 MB). Dual-GPU scan LAUNCHED. RTX 3090 + RX 6950 XT. |
| westGate | **NUCLEUS v4.57** | Linux | 10.13.37.11 | **NUCLEUS (13)** | **DATA NAS.** 14/14 HEALTHY. 3.21 TB / 153 datasets / **452 GB CAS**. Convoy 145/s (460x). GPS data CONVERTED. 0/153 fully braided — convoy ACTIVE. |
| blueGate | **NUCLEUS v4.57+** | Windows | 10.13.37.12 | **NUCLEUS (13)** | 14/14 HEALTHY. **Primary builder** (15 Windows). UniBin CLI migration documented. |
| biomeGate | **GPU CRANKSHAFT + FULLY AGENTIC** | Linux | 10.13.37.3 | compute | Threadripper 3970X, 128GB. 3 VFIO GPUs. coralReef 3,553 tests. 44-experiment matrix. **WG mesh LIVE, 8/10 peers, Forgejo SSH working.** G32 silicon deism. |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| southGate | **G68 REDEPLOYED — 13/13 ALIVE** | Linux | **NO WG** (deliberate) | **NUCLEUS (13)** | 5800X3D + RTX 4060 + 128GB + 5TB NVMe. **G17 PROVEN. G8 PROVEN.** G68 redeploy: 96 MB RSS, 0.058ms Tower (2.6x faster). SSH discipline: 33 repos cleaned. |
| **steamGate** | **NEXT** | SteamOS | — | tower (3) | Steam Deck. Portable compute. gnu bins in depot. |
| **darwinGate** | **GLACIAL** | macOS | — | tower (3) | Mac Mini (acquire). apple-darwin builder. |
| **iosGate** | **GLACIAL** | iOS | — | tower (3) | iPhone. After darwinGate. Silicon deism. |

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
│  Route: WireGuard wg0 (10.13.37.x) + songBird :7700    │
│  Auth: capability IPC, TLS, BTSP (13/13)                │
│  Owner: per-primal, coordinated by overwatch             │
│  Status: 9-gate mesh, Tower LIVE on 5+ gates, Nest LIVE  │
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
- [x] BTSP defense-in-depth: 13/13 primals
- [x] **biomeOS neuralAPI**: **27** signal graphs, **v4.56**: G22 convergence (unified namespace, 244 caps), dual-protocol health ping, socket ownership guard, `composition.test_swap`. (8,570 tests)
- [x] **songBird ACME HTTP-01** challenge responder shipped — Phase 1 TLS elimination
- [x] songBird mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L
- [x] sporeGate depot fully refreshed: health **11/11 HEALTHY**, **46 binaries** (16 musl + 15 gnu + 15 windows), BLAKE3 verified
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
| **No external dependencies** | **ALIGNED** | cellMembrane purged reqwest → sovereign HTTP/1.1 client. Pure-Rust TLS. Zero C deps on critical path. |
| **Single source of truth** | **ALIGNED** | Forgejo (golgiBody) is sole canonical remote. GitHub is push-mirror only. |
| **Sole depot** | **ALIGNED** | All genomeBins from `depot.primals.eco`. Sovereign CI auto-publishes. |
| **Portable mesh** | **VALIDATING** | NUCLEUS proven on 4 gates. **southGate = validation gate**: deliberately off WireGuard, deploys from public depot, own genetic lineage, bonding/encryption validation across trust boundary. Proves portability for external deployments. |
| **Silicon deism** | **G66 COMPLETE — PROVEN on 3 platforms** | Linux (musl+gnu), Windows (windows-gnu 12/15), Android (aarch64). G66 transport abstraction 15/15. SteamOS NEXT, darwin/iOS GLACIAL. |
| **Zero telemetry** | **ALIGNED** | No telemetry, no analytics, no cloud lock-in across all primals. |
| **AGPL-3.0** | **ALIGNED** | All primals, gardens, springs. scyBorg triple-license framework defined. |
| **Pure Rust crypto** | **ALIGNED** | bearDog Ed25519 signing, BTSP 13/13, riboCipher transport. |
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
- [x] BTSP defense-in-depth (13/13)
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
```

| Composition | Status | Gates Proven | biomeOS Orchestrated? |
|-------------|--------|--------------|----------------------|
| **Tower Atomic** (3) | LIVE | 6 gates (incl. Windows, Android) | Signal graphs: 8. Direct IPC: YES. |
| **Nest Atomic** (7+Tower) | LIVE | westGate (ZFS+CAS), blueGate (Windows) | Signal graphs: 9. Graph execution: **FIXED** (v4.47 riboCipher). |
| **Node Atomic** (3+Tower) | VALIDATED | strandGate (746 pipelines/sec, sub-ms GPU) | Signal graphs: 3. |
| **NUCLEUS** (13) | **ACHIEVED ×6 — ALL GATES v4.57+. G64+G65+G66 COMPLETE. STAGE 2 INFRA SHIPPED.** | **sporeGate** (12/13, depot), **ironGate** (NUCLEUS), **westGate** (14/14), **strandGate** (GPU 100%), **blueGate** (14/14), **southGate** (13/13) | 27 signal graphs. **G56/G67: Stage 2 routing infra shipped (578 tests). Depot rebuild → deploy → springs.** |

### What's proven

- [x] footPrint LIVE — **708 TS tests, Phase 2 DEPLOYED on ironGate.** CAS E2E. golgi Caddy routing DONE.
- [x] esotericWebb LIVE — **V31b, 484 tests, CELL BOOT SUCCEEDED on ironGate.** 28 caps, `nest.store` signal decomposition.
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
- [x] **ironGate DOWNSTREAM HOST (Aug 3)** — esotericWebb V30 + footPrint 628 tests (Phase 2 deploy ready). NUCLEUS 13/13. RTX 5070. G19 PROVEN. riboCipher transport validated. BTSP local-trust (G63) is remaining CAS blocker.
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
- [x] ~~blueGate lifecycle NUCLEUS~~ — **DONE** (14/14 depot, Prov 7/7 on Windows)
- [x] ~~strandGate redeploy~~ — **v4.55 depot deploy, P1 GATE VALIDATED**: 12/12 HEALTHY, 1,017 methods, 13 procs (1 each).
- [x] ~~**Coevolution (G21)**~~ — **COMPLETE**: biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED. Depot rebuilt.
- [ ] **Cross-platform gates** — steamGate (NEXT, UNBLOCKED), darwinGate (GLACIAL), iosGate (GLACIAL)
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
- [x] **Depot: 46 binaries across 5 target directories** (16 musl, 15 gnu, 15 windows-gnu, + aarch64-musl, aarch64-android dirs)
- [x] **Windows cross-arch 15/15 PASS** — `cargo check --target x86_64-pc-windows-gnu` mandated as pre-push. All 15 primals pass (Wave 156z). Not yet in CI automation.
- [ ] **macOS genomeBins** — can't cross-compile from Linux. Needs darwinGate (Mac Mini) to self-build.
- [ ] **SteamOS validation** — gnu depot bins may work as-is on Steam Deck (user-space deploy)
- [ ] `target`/`bind_mode` field removal — primals auto-detect, depot negotiates
- [ ] systemd abstraction for launchd paths (cellMembrane `InitSystem` foundation shipped, darwin untested)

## ~~9. Documentation / Fossil Record~~ → **FOSSILIZED as F11** (Wave 155h)

ALL ITEMS RESOLVED. Moved to Fossilized section below.

## ~~10. Jelly Strings~~ → **FOSSILIZED as F14** (Wave 156h)

ALL ITEMS RESOLVED. J9–J19 (11/11 KILLED or LIVE E2E). J12 evolution (SSH → songBird IPC) is a G62 concern, not a jelly string. Moved to Fossilized section below.

## 12. gen5 — Full NUCLEUS as Live Platform (NEW)

gen4 is COMPLETE (4 NUCLEUS gates on v4.55, Provenance 7/7, Sovereign CI, coevolution).
gen5 is **NUCLEUS as a usable platform** — validated by strandGate Node Atomic landmark:
2,130 matmul/sec, cross-atomic provenance E2E (GPU→sign→verify→DAG→attribution→Merkle),
W3C PROV-O, AlphaFold 20-30 structures/day capacity. **gen5 thesis VALIDATED.**

### The Full NUCLEUS Stack

```
┌─────────────────────────────────────────────────────────┐
│  squirrel — AI agent frontend                           │
│  MCP integration, capability discovery, natural         │
│  language → biomeOS neuralAPI semantic dispatch          │
├─────────────────────────────────────────────────────────┤
│  biomeOS — orchestration backend                        │
│  27 signal graphs, 654+ capabilities, composition       │
│  lifecycle, semantic dispatch (tower.*, nest.*, node.*) │
├─────────────────────────────────────────────────────────┤
│  petalTongue — rendering + visualization                │
│  WebGL/WASM pipeline, real-time viz, game rendering     │
│  Works WITH Node Atomics for GPU-accelerated output     │
├─────────────────────────────────────────────────────────┤
│  Node Atomics — GPU compute + shaders                   │
│  toadStool (dispatch) + barraCuda (tensor math) +       │
│  coralReef (shaders/WGSL/SPIR-V) = QCD to videogames   │
├─────────────────────────────────────────────────────────┤
│  Nest Atomics — storage + provenance                    │
│  nestGate (CAS) + Provenance Trio (7/7 COMPLETE)        │
│  Every object has lineage, every computation has proof   │
├─────────────────────────────────────────────────────────┤
│  Tower Atomics — trust + discovery + defense             │
│  bearDog + songBird + skunkBat = foundation layer       │
└─────────────────────────────────────────────────────────┘
```

### What NUCLEUS Enables — gen5 Workloads

| Workload | Stack | Gate(s) | Status |
|----------|-------|---------|--------|
| **Scientific visualization** | hotSpring → toadStool → petalTongue (QCD, molecular) | westGate, strandGate | Node Atomic validated, petalTongue WASM ready |
| **Game engine / creative** | esotericWebb → petalTongue → coralReef (shaders, WebGL) | **ironGate** (downstream host) | **V31b, 484 tests, CELL BOOT SUCCEEDED on ironGate.** 28 caps, 8/9 primals. Needs petalTongue WebGL pipeline (G19) for browser surface. |
| **AI agent orchestration** | squirrel (4,613 tests, 90.1% cov, G18 wired) → biomeOS neuralAPI → any primal | any NUCLEUS gate | Capability routing proven (835+ caps) |
| **Genomics pipeline** | wetSpring → toadStool → nestGate (16S rRNA, GPU) | strandGate (RTX 3090) | Pipeline validated, cold (needs data) |
| **NF drug reversal (Gonzales/Bin)** | tideGlass → Nest Atomic → Provenance Trio → petalTongue (GPS viz) | westGate | 214 tests, CAS + petal clients wired, GPS data CONVERTED, 452 GB CAS. Cell boot NEXT. Mid-term: Cell 2026 rebuild → NF screen → CTF NDU |
| **GIS data** | footPrint → nestGate → petalTongue | **ironGate** (downstream host) | Matures petalTongue G19 → reusable for tideGlass GPS viz |
| **Protein structure** | AlphaFold ~1TB → Nest Atomic CAS → provenance | westGate (ZFS 25.4TB) | Data on northGate, pipeline READY |
| **helixVision** | Genomics + AlphaFold + rendering | multi-gate | Orchestrator role, absorbed coralForge |
| **Cross-platform deploy** | cellMembrane → depot → any chip + drive | all gates | 35 binaries, 3 platforms proven |

### Platform Readiness — What's Wired vs What Needs Wiring

| Component | Proven? | What's Next |
|-----------|---------|-------------|
| biomeOS neuralAPI dispatch | **YES — 578 tests, Stage 2 infra shipped (riboCipher pool, auto-transition, TOML caps)** | **N2-N5 verification → depot rebuild → deploy.** |
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
- [x] **Step 2**: westGate data federation — **3.21 TB / 153 datasets / 452 GB CAS, convoy at 145/s. GPS data CONVERTED.**
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

**COMPLETE (16 goals — proven on live hardware):**

| ID | Goal | Evidence |
|----|------|----------|
| G3 | Provenance Trio 7/7 | 8th consecutive pass. First real data (PDB+ChEMBL) at 100% provenance. |
| G4 | NUCLEUS on multiple gates | **×6**: westGate, strandGate, blueGate, sporeGate, southGate, **ironGate** (21/21 HEALTHY). |
| G8 | Plasmodium (multi-gate bonding) | southGate 22/22 PASS. BTSP trust without WireGuard. 29,294 foreign rejections. |
| G10 | Sub-builder mesh | J12 LIVE E2E. sporeGate → blueGate → BLAKE3 verified. |
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

**ACTIVE (25 goals — in progress or unblocked):**

*G66+G68 graduated to COMPLETE (Wave 157a). G67 added (Wave 156z). G56/G67 Stage 2 infra shipped. Triad Phase A LIVE on sporeGate. All primal teams CLEAR. Gate redeploy NEXT.*

| ID | Goal | Status | Next Step |
|----|------|--------|-----------|
| G7 | Science data ingestion | **3.21 TB on ZFS — 153 datasets, 17+ domains, 452 GB CAS pool.** Convoy at 145/s (460x). 7.9M files remaining (~15h ETA). AlphaFold v6 42/46 proteomes. GPS data CONVERTED (11 JSON, 103 MB). | Convoy completion → bulk convergence. AlphaFold 23TB eventual. |
| G9 | arXiv publication (Murillo/Chuna QCD) | **PREPRINT 41/42.** NPU silicon continuum integrated (§2.9, §4.7 rewritten, §7, Appendix A). SU(N) N=2→8, 69 cached configs. β-scan receipt: 7 β-values on 8⁴ (β=2.0→6.5), plaquettes match literature. MILC bidirectional Δ⟨P⟩=3×10⁻⁹. NPU ESN: 100% accuracy (11 features, MCC=1.0). Murillo claims audit complete. | Wire live site (pseudoSpore artifact, `validate.sh`, reviewer JupyterHub). Then reviewer send. |
| G11 | Any chip + drive = mesh gate | ACTIVE | biomeGate + ironGate proved. steamGate NEXT. |
| G14 | sporePrint live science refresh | ACTIVE | pseudoSpore LIVE. Auto-publish FIXED. |
| G15 | tideGlass Phase 0 (NF archaeology) | **INFRASTRUCTURE READY** | 214 tests. 17 IPC methods. CAS client + `content.query` wired. 5 viz scenes. **Needs cell boot on westGate.** |
| G18 | squirrel → biomeOS agent orchestration | **LIVE on ironGate** | 9 providers, cross-primal dispatch validated (Session 10). Wire footPrint agent panel next. |
| G19 | petalTongue + Node Atomics live rendering | ACTIVE | hotSpring QCD viz + esotericWebb. |
| G20 | esotericWebb game engine on NUCLEUS | **CELL BOOT SUCCEEDED** | **V31b** — 484 tests, 28 caps, 8/9 primals live on ironGate. `nest.store` signal decomposition validated. Needs petalTongue WebGL pipeline (G19) for browser surface. |
| G30 | westGate data federation root | **3.21 TB / 153 datasets / 17+ domains / 452 GB CAS.** Convoy 145/s. GPS data converted. | Federation unblock (TCP + songBird). `data:want` cascade. |
| G32 | Silicon deism vendor cracking | **NEW — biomeGate** | 3-GPU bench (RTX 5060 + Tesla + Titan V). coralReef diesel engine. hotSpring cross-vendor validation. |
| G34 | Outer membrane egress masking | **SPEC** | Flint as boundary router. Single opaque tunnel to golgi. ATT box sees nothing. |
| G35 | Fully agentic LAN | **7/8 DONE** (biomeGate joined mesh). | northGate + flockGate blocked (physical access). `membrane remote.enroll` proposed. |
| G36 | tideGlass Phase 1 — GPS reproduction (Gonzales/Bin Chen) | **ACTIVE** (214 tests, CAS wired, 5 viz scenes) | GPS data CONVERTED (11 JSON, 103 MB CAS). `content.query` WIRED. PetalTongueClient coded (dead_code). Cell boot on westGate NEXT. Mid-term: **sovereign rebuild of Cell 2026 GPS platform.** |
| G37 | NF Reversal Screen (Gonzales NF collaboration) | **ACTIVE** | RGES vs LINCS, ZINC compound screening, MEK inhibitors (selumetinib) in top-100. NF Data Portal ingested (658 files). Depends G36. |
| G38 | NF PseudoSpore artifact | **ACTIVE** | Self-verifying USB: data + code + provenance. `./validate` runs 7 tideGlass modules. **First gen5 science deliverable.** |
| G39 | CTF NDU grant ($125K) | **ACTIVE** | Preliminary data package for Children's Tumor Foundation NDU. Depends G36+G37. |
| G43 | steamGate — immutable OS handheld | **ACTIVE** | Steam Deck OLED. User-space musl deploy on read-only SteamOS. G17 pattern. |
| G44 | reefGate — paired intelligence/storage | **ACTIVE** | DDR3 NUC + Synology DS224+ NFS. G23 fractional replication target. |
| G45 | Lattice QCD Rungs 2–6 (Murillo/Chuna program) | **ACTIVE — SU(N) GENERALIZED** | GaugeGroup trait covers N=2,3,4,5,6,8. Rung 1 reframed from SU(3)-only to full SU(N) ladder. 87-config thermalization grid running on 64 EPYC threads (~2wk). `arxiv_measure_battery` ready. 30 finite-T configs for deconfinement T_c/√σ analysis. SU(N>=4) GPU shaders need generalization (WGSL hardcoded for 3x3). |

**GLACIAL (23 goals — future phases):**

| ID | Goal | Status | Dependency |
|----|------|--------|------------|
| G6 | bearDog public (crates.io) | GLACIAL | crates.io publishing |
| G12 | darwinGate (Mac Mini) | GLACIAL | HW acquisition → iOS + Sovereign Identity |
| G13 | iosGate (iPhone) | GLACIAL | darwinGate + Dev Program |
| G16 | pseudoSpore grab pattern on web | GLACIAL | After NF data + tideGlass |
| G23 | nestGate CAS fractional replication | GLACIAL | Data redundancy schema exists |
| G24 | Sovereign Identity Garden | CONCEPT | Gate-first (cameras/sensors), phone later |
| G25 | bearDog StrongBox/Secure Enclave | GLACIAL | Gate-connected first, phone later |
| G26 | sweetGrass zero-knowledge attestations | GLACIAL | Prove encrypted data properties |
| G27 | mitoBeacon identity genetics | GLACIAL | Person-level cryptographic DNA |
| G28 | Cross-platform sovereign identity | GLACIAL | Depends on G12 + G13 |
| G40 | cloudGate — WAN enrollment validation | GLACIAL | Oracle ARM VM, NAT traversal, trust-boundary crossing |
| G41 | piGate — resource-constrained ARM proof | GLACIAL | RPi 5, ~$125 edge gate |
| G42 | riscGate — RISC-V third ISA | GLACIAL | StarFive VisionFive 2, open-ISA |
| G46 | Show HN public launch | GLACIAL | 28-item rubric. Blocked until NF pseudoSpore + sporePrint |
| G47 | projectFOUNDATION auto-feed | CONCEPT | Provenance-driven knowledge layer, thread lineage |
| G48 | projectNUCLEUS product packaging | CONCEPT | NUCLEUS product + pseudoSpore delivery pipeline |
| G49 | lab.primals.eco periplasmic JupyterHub | ACTIVE | Reviewer-access interactive compute on ironGate |
| G50 | initioChem pseudoSpore (ABG track) | ACTIVE | Whole-cell expression artifact |
| G51 | Inkfish/Valve marine collaboration | CONCEPT | Marine genomics, coral holobiont science |
| G52 | blueFish PFAS QC (Jones track) | GLACIAL | EPA 1633A open PFAS QC |
| G53 | petalTongue maturation via downstream consumers | **ACTIVELY WIRING** | **footPrint**: `petal-bridge.ts` dual-socket WS↔UDS relay (agent→squirrel, viz→petal) WIRED. Auto-load. CSP dedup. **tideGlass**: `PetalTongueClient` ACTIVATED (dead_code removed, `is_viz_method()` gate, fire-and-forget forwarding). **nestgate.io**: 20 primals discovered, 8/12 dashboard sections, Tower Atomic architecture view. **Conjugation**: RustScript (`@protokarya/rustscript`) is the TS conjugation layer — 11 modules. |
| G54 | Dual-science mid-term convergence | **ACTIVE** | **Track A (NF/GPS — Gonzales/Bin)**: tideGlass rebuilds Cell 2026 paper → NF drug repurposing → CTF NDU grant. **Track B (QCD — Murillo/Chuna)**: hotSpring arXiv Rung 1 → 6-rung lattice QCD program. Both tracks consume barraCuda (GPU math), petalTongue (viz), provenance trio (chains), nestGate (data). Infrastructure evolves toward both simultaneously. |
| G56 | **Neural API activation (capability routing everywhere)** | **ACTIVE — STAGE 2 DEPLOYED ON 6 GATES** | biomeOS 4.57.0 deployed on all 6 NUCLEUS gates. 578 tests. westGate: 26 capabilities registered with songBird (`capability.resolve` working). Primal self-registration is the next evolution — currently manual `ipc.register` scripts. **N2-N5 verification → primalSpring owns.** |
| G67 | **Neural API forwarding fix + Stage 2 transition** | **ACTIVE — DEPLOYED ON 6 GATES** | Stage 2 infra deployed across all NUCLEUS gates. westGate NG-05 DONE (nestGate TCP + songBird capability registration). `capability.resolve("content.get")` → nestGate working. **Remaining: N2-N5 verification, primal self-registration on startup.** |
| G57 | nestgate.io data identity surface | **PHASE 2 — 10/12 sections + trust surface routes** | `/api/content/stats` (live CAS from rhizoCrypt), `/pseudospore/` (5 bundles), `/api/pseudospore/bundles` — all LIVE. mesh.peers WIRED. 20 primals discovered. **NG-05 CLOSED** (westGate CAS federation). Data Braids card can now query westGate TCP. Remaining: wire Data Braids card against westGate `192.168.4.149:8080`. |
| G58 | Mixed provenance convergence | **ACTIVE** | Promote all westGate data from primordial/CAS-only to fully braided. `is_dataset_converged()` gate for springs. Revalidation running for priority + AlphaFold. All spring-critical data fully braided before Phase 4 boot. |
| G60 | Federated CAS (nestgate.io cross-gate data surface) | **ACTIVE** | nestgate.io as federated CAS front door — hash requests resolve across mesh (westGate data, strandGate compute configs, ironGate consumer data). `content.locate` → songBird mesh broadcast → first-responder-serves. L1 cache on golgi for hot objects. Enables cross-gate data retrieval without knowing which gate holds data. Replication endpoint for reviewers. |
| G61 | Compute memoization via provenance trio | **ACTIVE** | strandGate thermalized lattice configs as CAS objects with provenance braids. 37 min CPU thermalization → instant on cache hit. Same BLAKE3→CAS→DAG→braid pattern as data acquisition. Cross-gate: biomeGate pulls configs for parity checks. Parallel pipeline: GPU produces while CPU thermalizes next β. NFT-style braids for both config and production results. |
| G62 | Nanowire → Primal Builder (mesh-routed builds) | **ACTIVE** | Phase 2a DONE: manifest-driven sub-builders (no recompile to add gates). Phase 2b SPEC: songBird mesh-routed `harvest.request`/`harvest.complete`. Foreman pattern: symmetric — any gate can request, any gate can build. Capability advertisement on startup. Parallel dispatch. biomeGate as second sub-builder (NW-05 pending). |
| G63 | BTSP local-trust (SO_PEERCRED for same-gate UDS) | **ACTIVE** | nestGate accepts same-gate callers without full BTSP X25519 handshake. Process-level auth via `SO_PEERCRED` — membrane group callers are trusted by filesystem perms. Unblocks footPrint CAS write, tideGlass CAS integration, all gardens/protists on same gate. Zero config, maximally primal-like. Proposed in footPrint Phase 2 deploy ready handoff. |
| **G68** | **Platform Substrate Abstraction — beyond cfg(unix)** | **COMPLETE — 16/16 PROD-CLEAN, 16/16 CROSS-ARCH** | sourDough scanner v2 (prod/test split, 3 compliance levels). **8/16 G68 compliant** (sourDough, nestGate, petalTongue, bingoCube, loamSpine, barraCuda, cellMembrane, + 1). **8/16 G68-prod** (squirrel, bearDog, songBird, rhizoCrypt, skunkBat, sweetGrass, coralReef, biomeOS, toadStool — test-only assertions). **ZERO production violations.** 205→0 across Wave 157a. toadStool S363→S368 (24→0). cellMembrane 15 cfg blocks eliminated (1,327 tests). 16/16 Windows cross-arch PASS. **G68 CONVERGED — ready for fossilization after gate redeploy validation.** |
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
- coralForge retired — vestigial name, now helixVision
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

---

**Active**: 9 dimensions (1–5, 7–8, 11–12)
**Fossilized**: 14 dimensions (F1–F14)
**Summary**: Wave 157a — **6/6 GATES REDEPLOYED. NG-05 CLOSED. TRUST SURFACES LIVE.** 16/16 prod-clean. 16/16 cross-arch. 205→0 violations. 6/6 NUCLEUS gates running G68-converged biomeOS 4.57.0. westGate NG-05 complete (26 capabilities registered, CAS 2.5 TB federated). cellMembrane `plasmid.fetch --source forgejo` FIXED. lithoSpore QCD pseudoSpore bundle PACKAGED. toadStool S370: WASM compute (15 crates on wasm32). SSH discipline enforced ecosystem-wide. **ZERO P0/P1. ~140K+ tests.**

**Phase shift**: **"Neural API self-registration + arXiv trust surface + springs."** Gates deployed. NG-05 closed. Sovereign deploy path (Forgejo plasmid.fetch) fixed. Next: (1) primal self-registration — primals announce capabilities to songBird on startup (westGate manual pattern → primal-native), (2) arXiv trust surface — `validate.sh`, sporePrint SU(N) relabel, freeze/sign v1.0.0-rung1, reviewer send, (3) springs activation — tideGlass cell boot on westGate (CAS federation now live), hotSpring QCD viz, esotericWebb, (4) projectNUCLEUS Phase 2 handoffs (workloads/specs → spring repos + wateringHole).

**151 files fossilized** across 11 checkpoints (1,472 total records). Active handoffs: 7.
- **ironGate: DOWNSTREAM SURFACE.** NF GPS + ABG + MILC targets. Novel ferment transcript CAS depot. G18 LIVE. 12.7 TB CAS. RTX 5070.
- westGate: **DATA BRAIDS DEPOT.** 343 GB federated, 519 GB total. Convoy COMPLETE. Jelly strings eliminated. Federation: Neural API routing NEXT.
- strandGate: **COMPUTE.** SU(N) thermalization. Dual-GPU. Config cache memoization. Compute memoization patterns ready for Neural API.
- **sporeGate: CI + MEMBRANE.** Depot 17/17 musl. nestgate.io 10/12. Neural API deploy N1 target.
- biomeGate: **GPU LAB + CRANKSHAFT.** 3 VFIO GPUs. toadStool Akida. coralReef cross-arch FIXED.
- eastGate: **OVERWATCH + CODE TEAMS.** 64 GB DDR5. squirrel 4,090 tests (C8 done, -67K lines). primalSpring (N2-N5) + biomeOS (routing infra) code teams activated.
- blueGate: **WINDOWS + PRIMARY BUILDER.** 15/15 Windows builds. Sub-builder proven. v4.57+ SYNCED.
- southGate: **VALIDATION.** Re-validated (13/13, Tower 0.15ms, 19 Gbps).

**11 gates ONLINE** (6 NUCLEUS at v4.57+, 1 crankshaft + agentic, 4 other). **16 glacial goals COMPLETE** (G3, G4, G8, G10, G17, G21, G22, G29, G31, G55, G59, G64, G65, G66, **G68**).
**25 ACTIVE** (G7, G9, G11, G14, G15, G18, G19, G20, G30, G32, G34, G35, G36, G37, G38, G39, G43, G44, G45, G53, G54, **G56**, G57, G58, G60, G61, G62, **G67**).
**23 GLACIAL/CONCEPT** (future phases).
**65 total glacial goals** tracked.

**DEBT CLEARING + NEURAL API ACTIVATION** — current phase:

**CLEARED (all primals G64+G65+G66 code-shipped):**
- ~~S1–S7, O1–O8, B1+B2~~ — ALL RESOLVED (see above)
- ~~C2 dual-socket 15/15~~ — DONE
- ~~G65 protocol negotiation 15/15~~ — DONE
- ~~G66 transport modules 15/15~~ — DONE
- ~~C8 squirrel excision -67K lines~~ — DONE
- ~~coralReef + toadStool cross-arch~~ — FIXED

**CROSS-ARCH CLEARED (Wave 156z→157a):**
- ~~petalTongue~~ — `9a5ed02` TransportListener Phase 2 gating
- ~~skunkBat~~ — `7ef22f3` #[cfg(unix)] guards on tarpc + IPC tests
- ~~squirrel~~ — `234fa514` Wave 157d cross-arch compliance
- ~~toadStool~~ — S363 `select_backend` gated + `akida device open` migration
- **16/16 repos pass `cargo check --target x86_64-pc-windows-gnu`** (15 primals + cellMembrane)

**NEURAL API ACTIVATION (G56+G67 — STAGE 2 INFRA SHIPPED):**
- ~~**N1**: Fix forwarding path~~ — **DONE** (`ffed2c5b`)
- ~~**Stage 2 infra**: riboCipher pool, Bootstrap→Coordinated, TOML caps~~ — **SHIPPED** (biomeOS code team, 578 tests)
- ~~**primalSpring post-primordial**: NeuralBridge migration, primordial-compat gating~~ — **SHIPPED** (1,263 tests, 197 scenarios)
- **N2**: Verify on eastGate — `capability.call` routes to bearDog — **NEXT**
- **N3**: Tower Atomic routing
- **N4**: Provenance Trio routing
- **N5**: squirrel agent routing
- **N6**: Deploy Neural API on westGate + strandGate (post depot rebuild)

**REMAINING — TARGETED WAVES FROM HERE:**
- ~~**G68 convergence**~~: **16/16 prod-clean, 16/16 cross-arch. COMPLETE.** 205→0 production violations. toadStool S363→S368 (24→0). cellMembrane 15 cfg blocks eliminated (1,327 tests).
- ~~**Phase A**~~: **DONE** — cascade timer LIVE on sporeGate (15m systemd, G68 membrane, zero drift).
- ~~**Depot rebuild + deploy**~~: **DONE** — 4 passes, Musl 17/17, Windows 15/15. 13/13 ALIVE on sporeGate.
- ~~**Gate redeploy**~~: **6/6 NUCLEUS GATES DONE** — sporeGate (13/13), blueGate (13/13 Windows), southGate (13/13, 96MB), ironGate (13/13, 41MB), strandGate (11/13, 127MB), westGate (13/13 + NG-05 federation).
- **Neural API evolution**: primalSpring guides compositional evolution. westGate shipped songBird capability registration (26 caps). Next: primal self-registration on startup, N2-N5 verification.
- **toadStool long-tail**: Extending platform abstraction to all deployment types (Node Atomic hw-safe owner). Cross-arch for every backend.
- **cellMembrane long-tail**: `native_braid.py` → Rust (last Python in active pipeline). NM hook naming unification.
- **Springs**: tideGlass cell boot, hotSpring viz, esotericWebb browser surface.
- **arXiv**: wire live site + pseudoSpore + reviewer send.
- **Wave cadence**: targeted primal waves. No more ecosystem-wide convergence days.
- **G68 COMPLETE. GATE REDEPLOY NEXT. PRIMALSPRING NEURAL API EVOLUTION CONTINUES.**

### LIVE SITE ASSESSMENT (Aug 5 PM)

| Site | URL | HTTP | Functional? | Primary Issue |
|------|-----|------|-------------|---------------|
| **sporePrint** | `sporeprint.primals.eco` | 200 | **YES** | Zola static — renders well, claims verifiable, science content accurate |
| **footPrint** | `footprint.primals.eco` | 200 | **YES (auto-loads)** | `petal-bridge.ts` wired (dual-socket WS↔UDS). `autoLoadDefaultProject()` → map loads on first visit. `SKIP_CSP=1` deduplicates headers. **Remaining**: squirrel UDS socket for agent panel. |
| **nestgate.io** | `nestgate.io` | 200 | **YES (9/12 sections)** | Neural API bridge LIVE — **20 primals discovered.** Tower Atomic layers, routing table, namespace chart, data braids, **gate mesh table** (mesh.peers WIRED via songBird UDS). **Remaining**: health liveness (NG-03), bearDog routing stub (NG-04), CAS content browse. |
| **esotericWebb** | `webb.primals.eco` | GET 200 / HEAD 502 | **PARTIAL** | HTML served (11,768 B). HEAD method missing in handler (NG-06). Needs petalTongue WebGL pipeline (G19) for live game surface. |

**MID-TERM SCIENCE TRACKS**:
- **Track A (NF/GPS)**: G15→G36→G37→G38→G39. Gonzales/Bin Chen. tideGlass rebuilds Cell 2026 → NF reversal screen → CTF NDU $125K.
- **Track B (QCD)**: G9→G45. Murillo/Chuna. arXiv Rung 1 → 6-rung lattice QCD on consumer GPUs.
- **Support convergence (G53)**: footPrint + esotericWebb on ironGate → petalTongue G19 → GPS viz (Track A) + QCD viz (Track B).

**Gauge group resolved in code** (G9): SU(3) labels disambiguated in barraCuda/hotSpring. Paper/site relabel still needed (sporePrint scope). arXiv UNBLOCKED.

**Open items — prioritized by data pipeline + springs readiness:**
- ~~**G55: Batch RPCs for provenance**~~ — **RESOLVED (460x)**. Convoy at 145/s. Primals never the bottleneck.
- ~~**G59: Three-domain topology**~~ — **DNS SEPARATION COMPLETE.** All 3 layers separated. primal.eco SEALED (6 A records removed). nestgate.io LIVE on mesh. DNSSEC verified. Remaining: deploy dnsmasq, wire content backend, brand nestgate.io.
- **G56: Neural API activation** — route footPrint, tideGlass, esotericWebb, all springs through `neural-api-default.sock`. Eliminate hardcoded socket paths. biomeOS signal graphs already wired for data federation.
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

*Last used*: Wave 157a — 6/6 NUCLEUS gates redeployed. NG-05 CLOSED (westGate CAS federation, 26 capabilities). cellMembrane plasmid.fetch forgejo FIXED. lithoSpore QCD pseudoSpore PACKAGED. toadStool S370 WASM compute. SSH discipline enforced ecosystem-wide. Trust surfaces live. 16 COMPLETE, 25 ACTIVE, 23 GLACIAL. 65 goals. ~140K+ tests. (Aug 8, 2026 9:50AM)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 157a — G66+G68 graduated to COMPLETE (16th glacial goal). G68: 205→0 production violations across 16 repos. hotSpring 24K LOC fossilized. Stage 2 infra shipped (G56/G67). arXiv 41/42 (NPU silicon continuum). (151+ total across 12 checkpoints, 1,472+ total records)
*Latest reopen*: Wave 155k (D10 — Jelly Strings J9–J13, extended to J14–J19 in 155n)
