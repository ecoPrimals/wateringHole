# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155n)
- [x] Gate heads published (`heads/*.toml`) — golgiBody auto-publishing active
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] **ECOSYSTEM_BLURB.md** is the universal handoff (Tracks A+B converged)
- [x] **70+ handoff docs + AARs** delivered Wave 155b–n. 10 AARs + 2 handoffs fossilized this wave.
- [x] **ZERO P0 / ZERO P1 / ZERO P2.** All P1s GATE VALIDATED. P2 platform detection FIXED (`d7026d7`).
- [x] **NUCLEUS ACHIEVED on 5 gates** — westGate, strandGate, blueGate, sporeGate, **southGate (VALIDATION GATE 22/22 PASS)**. Gate validation AARs fossilized.
- [x] **Depot 46 binaries CURRENT** (16 musl + 15 gnu + 15 windows). biomeOS v4.56 + cellMembrane latest. BLAKE3 verified.
- [x] **biomeOS v4.56 SHIPPED** — G22 convergence steps 1+2: unified namespace, 244 caps, 47 deps removed.
- [x] **westGate ZFS rebuilt** — mirror → raidz1, 25.4 → 50.7 TB usable. AlphaFold DB fits.
- [x] **Golgi post-receive hook FIXED** (3 bugs: dispatcher, case, category). Sovereign CI E2E verified.
- [x] **cellMembrane 1,281+ tests** — MEMBRANE_*, crypto dedup, J16+J13+J19 killed, registry API hardened.
- [x] **squirrel 7,138 tests** — 90.1% coverage, 0 unsafe, universal-constants extraction
- [x] **Provenance 7/7 COMPLETE** — E2E validated on westGate (5th consecutive pass) + blueGate (Windows)
- [x] **Sovereign CI LIVE** — push-to-deploy E2E verified for ALL 13 primals including biomeOS (coevolution).
- [x] **Coevolution contract COMPLETE (G21)** — biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED (`652cf8a7`).
- [x] **42 files fossilized** across 3 checkpoints: `wave155n_checkpoint/` (25), `wave155n_gate_validated/` (2), `wave155n_springs_entry/` (17 — AARs + stale docs + impulses + context braids). Zero active AARs. Zero stale impulses.
- [x] **whitePaper convergence (G22)**: **COMPLETE** — biomeOS v4.56 single-process merge. Dual-protocol (riboCipher + JSON-RPC) in one process. Validated on westGate + sporeGate.
- [x] **Portability checkpoint (G17) — PROVEN.** southGate 22/22 PASS. NUCLEUS from public depot, own entropy, user-space paths, no WireGuard, no inherited identity. 20h stable, 32 sockets, 76MB RSS, 29,294 foreign peer rejections.
- [x] **DATA FEDERATION (westGate)** — **362 GB, 38 datasets, 17 domains, ~260K files, CAS 5,800+**, 100% provenance. tideGlass 7/7 COMPLETE. COSMIC v104, BRENDA, CHARMM36, PTB-XL, PubChem BioAssay, NCBI Taxonomy acquired. `data_catalog.toml` v2.0.0 shipped. **Inter-gate experiment comms over 10G LAN ENABLED.**
- [x] **Peptidoglycan DNS G29 COMPLETE** — 3-way redundancy: sporeGate dnsmasq (primary) + blueGate dnsproxy H2 secondary (LIVE) + golgi mesh DNS. Confirmed by sporeGate infrastructure verification.
- [x] **strandGate v4.56 DEPLOYED** — Carry-forward resolved. G22 confirmed. GPU QCD: 38-58× speedup, 5,500 traj/hr. hotSpring composition validated on live NUCLEUS.
- [x] **sporePrint DEMONSTRATION ERA** — 334→190 pages. pseudoSpore LIVE at primals.eco/pseudospore/. Hype cleaned (20 files). Tests: 116,930. First arXiv draft scaffolded.
- [x] **arXiv Rung 1 REFRAMED** — "Toward Vendor-Agnostic Lattice QCD on Consumer GPUs: SU(2) HMC with DF64 WebGPU/WGSL and Cryptographic Provenance." AI review absorbed. Scope ladder, plaquette normalization eq, precision matrix added. LaTeX updated. 6-rung research program defined. Experiment queue ACTIVE (β-scan, HMC diagnostics, increased stats).
- [x] **westGate persistence HARDENED** — ZFS auto-import, 13/13 NUCLEUS units enabled, boot dependency chain, daily snapshots, monthly scrub. 9/9 boot check PASS.
- [x] **hotSpring v0.6.32** — Deep debt clear. 627 tests, 0 clippy. thiserror migration. Files refactored.
- [x] **publications/ directory** — Auditable data transfer point for papers + pseudoSpore. Lattice QCD data centralized with full audit trail.
- [x] **golgi auto-publish fix** — THREE compounding bugs fixed: (1) worktree ownership mismatch (`git:git` vs `root:root`), (2) missing `--force` flag on `zola build`, (3) SSH config pointing at wrong golgi IP. sporePrint now deploys correctly to both inner and outer membrane.
- [x] **ironGate ONLINE** — Dev loop validated. Tower Atomic deployed (bearDog 10.6 MB + songBird 16.7 MB + skunkBat 2.6 MB). Forgejo SSH + HTTPS + depot all verified. 42 repos synced. Mesh: golgi 38ms, sporeGate 77ms, eastGate 78ms. **Ready for esotericWebb (G20).**
- [x] **P2 RESOLVED: GPU PRNG polyfill bias** — Root cause: WGSL transcendental polyfills (`log_f64`, `sqrt_f64`, `cos_f64`) in Box-Muller momentum shader produced wrong variance. Three-path comparison proves GPU MD pipeline is correct (bit-exact 4e-17). `cpu_mom` workaround deployed — CPU generates momenta, GPU does all MD at full speed. Section 3.2 UNBLOCKED. Finding strengthens the paper (validation methodology).
- [ ] **PLANNED SERVICE INTERRUPTION (Aug 2)** — ATT gateway + DS224+ moving to basement. steamGate + reefGate enrollment queued post-move.

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~63K+ primal tests validated this wave** (bearDog 14K, songBird 14.8K, nestGate 13K, toadStool 9.2K, biomeOS 8.6K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.7K, rhizoCrypt 1.9K, cellMembrane 1.2K+, squirrel 763, skunkBat, primalSpring 197)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **14,019** tests, crypto.sign SHIPPED, dual-socket fix, FAMILY_SEED precedence, 94 orphan files purged (**Wave 155m**)
- [x] songBird: 14,835+ tests, universal-ipc, ACME HTTP-01, TCP registration fix
- [x] nestGate: **13,095+** tests, CAS on ZFS verified, deep debt complete, zero unsafe
- [x] toadStool: **9,193+** tests, **S349**: JSON-RPC health endpoint, dead deps purged, stubs fail-closed, hardcoding consolidated (**Wave 155m**)
- [x] biomeOS: **8,570** tests, **v4.56**: G22 convergence steps 1+2 (unified namespace, 244 caps, 47 deps removed), dual-protocol health ping, socket ownership guard, `composition.test_swap`. (**Wave 155n**)
- [x] petalTongue: **6,605** tests, modern idiom evolution pass, debris audit (**Wave 155n**)
- [x] barraCuda: **4,957** tests, RTX 3090 profiled
- [x] coralReef: **3,527** tests, 463 `.expect()` purged, PTX modernized
- [x] cellMembrane: **1,281+** tests, **P2 platform detection FIXED** (`d7026d7`), `TargetArch` deprecated → `Platform::detect()`, `validate_with_deps()`, J19+J16+J13 killed, registry API hardened. (**Wave 155n**)
- [x] rhizoCrypt: 1,900 tests, BTSP→DAG bridge, cross-gate provenance
- [x] loamSpine: **1,739** tests, registry drift fixed, `--bind` alias
- [x] sweetGrass: **1,636** tests, G3 E2E validated, UUID fix
- [x] squirrel: **7,138** tests, 90.1% coverage, 0 unsafe, 0 clippy, universal-constants extraction, Cargo.lock purge (**Wave 155n**)
- [x] primalSpring: 197 scenarios, all PASS
- [x] skunkBat: 9 threat types, ConnectivityAnomaly, frame crypto, PUBLIC
- [x] **BTSP 13/13** — all primals shipped ClientHello
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: 6/6 seams DONE
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Physical Topology

- [x] Mixed 10G + 1G topology LIVE — 10G AOC backbone between houses, MikroTik CRS310 + Omada SX3008F
- [x] sporeGate on R45 → MikroTik — plasma membrane router (NAT/DHCP/DNS/nftables)
- [x] eastGate on MikroTik LAN — code hub, 10G SFP+ direct
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
| eastGate | ONLINE | Linux | 10.13.37.5 | full | Code hub, overwatch |
| ironGate | **NUCLEUS (13)** | Linux | 10.13.37.7 | **NUCLEUS (13)** | 21/21 sockets HEALTHY. i9-14900K, RTX 5070 (Blackwell). esotericWebb (G20) + ProjectFOUNDATION + lithoSpore. 913 garden tests PASS. |
| flockGate | **DOWN** | Linux | 10.13.37.6 | full | Rebooted, RustDesk locked out. esotericWebb → **ironGate** |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090. **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | **NUCLEUS v4.55** | Linux | 10.13.37.10 | **NUCLEUS (13)** | **P1 GATE VALIDATED.** 12/12 HEALTHY, 1,017 methods, 13 procs. RTX 3090 p50=0.33ms. |
| westGate | **NUCLEUS v4.56** | Linux | 10.13.37.11 | **NUCLEUS (13)** | **G22 COMPLETE.** 835 caps. Prov 7/7. ZFS raidz1 50.7TB. **356 GB / 32 datasets. tideGlass 7/7 COMPLETE.** |
| blueGate | **NUCLEUS v4.56** | Windows | 10.13.37.12 | **NUCLEUS (13)** | biomeOS v4.56 deployed. Prov 7/7. membrane.exe LIVE. **P2 FIXED.** J12 LIVE E2E. |
| biomeGate | **GPU CRANKSHAFT + FULLY AGENTIC** | Linux | 10.13.37.3 | compute | Threadripper 3970X, 128GB. 3 VFIO GPUs. coralReef 3,553 tests. 44-experiment matrix. **WG mesh LIVE, 8/10 peers, Forgejo SSH working.** G32 silicon deism. |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| southGate | **NUCLEUS — VALIDATION GATE 22/22 PASS** | Linux | **NO WG** (deliberate) | **NUCLEUS (13)** | 5800X3D + RTX 4060 + 128GB + 5TB NVMe. **G17 PROVEN. G8 PROVEN.** 20h stable, 32 sockets, 76MB RSS. Own family (89df7a2d). |
| **steamGate** | **NEXT** | SteamOS | — | tower (3) | Steam Deck. Portable compute. gnu bins in depot. |
| **darwinGate** | **GLACIAL** | macOS | — | tower (3) | Mac Mini (acquire). apple-darwin builder. |
| **iosGate** | **GLACIAL** | iOS | — | tower (3) | iPhone. After darwinGate. Silicon deism. |

## 4. K-Derm Layers — Connectivity Fabric (NEW — extracted from incidents + sovereignty)

Three-layer model identified by peptidoglycan failure incident (Wave 155d):

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
| **Silicon deism** | **PROVEN on 3 platforms** | Linux (musl+gnu), Windows (windows-gnu), Android (aarch64). SteamOS NEXT, darwin/iOS GLACIAL. |
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
- [x] **DNSSEC 3/3 domains complete**
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
- [ ] `primal.eco` inner membrane separation (P2)

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
| **NUCLEUS** (13) | **ACHIEVED ×4 — GATE VALIDATED** | **westGate** (835 caps, Prov 7/7, ZFS 50.7TB), **strandGate** (1,017 methods, 1 proc/primal), **blueGate** (Windows, Prov 7/7, P2 FIXED), **sporeGate** (11/11, CI) | 27 signal graphs. biomeOS v4.56 in depot. **G22 COMPLETE.** |

### What's proven

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
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
- [ ] **No Windows CI gate** — `cargo check --target x86_64-pc-windows-gnu` not yet in CI
- [ ] **macOS genomeBins** — can't cross-compile from Linux. Needs darwinGate (Mac Mini) to self-build.
- [ ] **SteamOS validation** — gnu depot bins may work as-is on Steam Deck (user-space deploy)
- [ ] `target`/`bind_mode` field removal — primals auto-detect, depot negotiates
- [ ] systemd abstraction for launchd paths (cellMembrane `InitSystem` foundation shipped, darwin untested)

## ~~9. Documentation / Fossil Record~~ → **FOSSILIZED as F11** (Wave 155h)

ALL ITEMS RESOLVED. Moved to Fossilized section below.

## 10. Jelly Strings — Deployment Automation (**REOPENED** Wave 155k)

J1–J8 fossilized as F13 (Wave 155i). New jelly strings identified in the depot
publish pipeline — every manual `plasmid.harvest` and `temporal.cascade` is a
jelly string to kill.

**Jelly strings (Wave 155k → 155m)**:

- [x] ~~**J9**: Cascade trigger~~ — **KILLED** (golgi post-receive hook → SSH → sporeGate `sovereign.ci.trigger`)
- [x] ~~**J10**: Build trigger~~ — **KILLED** (`MEMBRANE_BUILD_AUTHORITY=1`, drift pipeline active)
- [x] ~~**J11**: Multi-target build~~ — **KILLED** (`targets_for_primal()` reads manifest, auto musl+gnu)
- [x] ~~**J12**: Sub-builder dispatch~~ — **LIVE E2E** (SSH jelly-string-first). sporeGate foreman dispatch WIRED + blueGate local build PROVEN. SSH key enrolled. Evolution: SSH → songBird IPC (primal-native, deprecate SSH like WireGuard)
- [x] ~~**J13**: Depot freshness probe~~ — **KILLED** (cellMembrane `0d39075`: `plasmid.staleness --publish` mesh broadcast)

**Operational jelly strings (from sporeGate AAR)**:

- [x] ~~**J14**: Socket ownership~~ — **KILLED** (biomeOS `0e45262f`: bind now `0666` for multi-user IPC)
- [x] ~~**J15**: checksums.toml~~ — **KILLED** (cellMembrane `0cfcce5`: `finalize_depot()` full disk scan)
- [x] ~~**J16**: cellMembrane self-CI~~ — **KILLED** (cellMembrane `0d39075`: `sources.toml` garden self-enrollment)
- [x] ~~**J17**: `/run/membrane` tmpfiles.d~~ — **KILLED** (cellMembrane `0cfcce5`: `membrane.conf` shipped)
- [x] ~~**J18**: `/etc/environment` gate coupling~~ — **CODE SHIPPED** (`882ad09`): `env_or()` migration + gate-name identity bridge. Gate validation pending.
- [x] ~~**J19**: biomeOS sandbox bypass~~ — **KILLED** (cellMembrane `00c6800`: `validate_with_deps()` → biomeOS `composition.test_swap`)

**Pipeline status**: Forgejo push → cascade → diff → build → checksum → depot push → verify. **11/11 KILLED or LIVE E2E (J9–J19).** J12 is SSH jelly-string-first; evolution path → songBird IPC.

**Owner**: sporeGate + blueGate (J12 sub-builder) + cellMembrane (J18 portability)

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
| **Game engine / creative** | esotericWebb → petalTongue → coralReef (shaders, WebGL) | flockGate | V22 live, 472 tests, scene binding |
| **AI agent orchestration** | squirrel (7,138 tests, 90.1% cov) → biomeOS neuralAPI → any primal | any NUCLEUS gate | Capability routing proven (835+ caps) |
| **Genomics pipeline** | wetSpring → toadStool → nestGate (16S rRNA, GPU) | strandGate (RTX 3090) | Pipeline validated, cold (needs data) |
| **NF drug reversal** | tideGlass → Nest Atomic → Provenance Trio | westGate | Steps 1-2 DONE, Phase 0 NEXT |
| **GIS data** | footPrint → nestGate → petalTongue | flockGate | Running (primals.eco/footprint/) |
| **Protein structure** | AlphaFold ~1TB → Nest Atomic CAS → provenance | westGate (ZFS 25.4TB) | Data on northGate, pipeline READY |
| **helixVision** | Genomics + AlphaFold + rendering | multi-gate | Orchestrator role, absorbed coralForge |
| **Cross-platform deploy** | cellMembrane → depot → any chip + drive | all gates | 35 binaries, 3 platforms proven |

### Platform Readiness — What's Wired vs What Needs Wiring

| Component | Proven? | What's Next |
|-----------|---------|-------------|
| biomeOS neuralAPI dispatch | YES (654 caps, 27 graphs) | squirrel → neuralAPI agent integration |
| petalTongue WebGL/WASM | YES (6,605 tests, v1.7.0) | Live renders fed by Node Atomic GPU output |
| toadStool GPU dispatch | YES (746 pipes/sec, sub-ms) | petalTongue consumer pipeline |
| coralReef shaders | YES (WGSL/SPIR-V/PTX) | esotericWebb game shader pipeline |
| barraCuda tensor math | YES (FP64 104T, RTX 3090) | hotSpring QCD live computation |
| squirrel AI agent | YES (7,138 tests, 90.1% cov, MCP) | biomeOS neuralAPI routing, user-facing agent |
| Nest Atomic CAS | YES (3,252 objects, ZFS) | Data ingestion pipelines (AlphaFold, NF) |
| Provenance Trio | YES (7/7 E2E) | Every workload gets provenance tracking |

### gen5 Science Pipeline (one track through the platform)

- [x] **Step 1**: bearDog `crypto.sign_ed25519` — **DONE**
- [x] **Step 2**: Provenance 7/7 — **DONE**
- [ ] **Step 3**: tideGlass Phase 0 — archaeology. **NEXT.**
- [ ] **Step 4-6**: Reproduce → NF ingestion → reversal screen
- [ ] **Step 7**: One NF pseudoSpore — **THE gen5 ARTIFACT.**
- [ ] **Step 8**: JOSS paper + CTF NDU

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

**COMPLETE (8 goals — proven on live hardware):**

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

**ACTIVE (13 goals — in progress or unblocked):**

| ID | Goal | Status | Next Step |
|----|------|--------|-----------|
| G7 | Science data ingestion | **362 GB on ZFS** — 38 datasets, 17 domains, ~260K files. tideGlass 7/7 COMPLETE. COSMIC v104 + BRENDA + CHARMM36 + PTB-XL acquired. | Inter-gate experiment comms ENABLED. AlphaFold 23TB eventual. |
| G9 | arXiv + JOSS publication | **Rung 1 REFRAMED.** "Toward Vendor-Agnostic Lattice QCD." Experiment queue ACTIVE (β-scan, HMC diagnostics, increased stats). | hotSpring completes queue → sporePrint submits. |
| G11 | Any chip + drive = mesh gate | ACTIVE | biomeGate + ironGate proved. steamGate NEXT. |
| G14 | sporePrint live science refresh | ACTIVE | pseudoSpore LIVE. Auto-publish FIXED. |
| G15 | tideGlass Phase 0 (NF archaeology) | **UNBLOCKED** | ChEMBL+PDB in CAS. Spin up tideGlass on westGate. |
| G18 | squirrel → biomeOS agent orchestration | ACTIVE | Springs+gardens: wire neuralAPI dispatch. |
| G19 | petalTongue + Node Atomics live rendering | ACTIVE | hotSpring QCD viz + esotericWebb. |
| G20 | esotericWebb game engine on NUCLEUS | **ACTIVE on ironGate** | 472 tests PASS. NUCLEUS substrate live. RTX 5070 ready. |
| G30 | westGate data federation root | **362 GB / 38 datasets / 17 domains.** tideGlass 7/7 COMPLETE. CAS 5,800+. NCBI + Synapse API keys live. COSMIC v104 + BRENDA kinetics acquired. | Inter-gate experiment comms via 10G LAN ENABLED. |
| G31 | Batch RPC for provenance pipeline | ACTIVE | loamSpine/bearDog/sweetGrass batch ops → 10× faster ingestion. |
| G32 | Silicon deism vendor cracking | **NEW — biomeGate** | 3-GPU bench (RTX 5060 + Tesla + Titan V). coralReef diesel engine. hotSpring cross-vendor validation. |
| G34 | Outer membrane egress masking | **SPEC** | Flint as boundary router. Single opaque tunnel to golgi. ATT box sees nothing. |
| G35 | Fully agentic LAN | **7/8 DONE** (biomeGate joined mesh). | northGate + flockGate blocked (physical access). `membrane remote.enroll` proposed. |

**GLACIAL (13 goals — future phases):**

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
| — | Chimera Phase 0 (shared library) | GLACIAL | Deferred |
| — | Zola → sporePrint primal pipeline | GLACIAL | Replace static site gen |
| — | 6 springs pending validation.json | GLACIAL | Springs+gardens phase |

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

---

**Active**: 10 dimensions (1–5, 7–8, 10–12)
**Fossilized**: 13 dimensions (F1–F13)
**Summary**: Wave 155n RUNG 1 VALIDATION + DATA FEDERATION — **ZERO P0/P1/P2. arXiv reframed to "Toward Vendor-Agnostic Lattice QCD" (Rung 1 of 6). Experiment queue ACTIVE. 356 GB / 32 datasets / 14 domains. tideGlass 7/7 COMPLETE. biomeGate fully agentic. 116,930 tests.**

**Phase shift**: From "AMD benchmarks as last blocker" to **"experiment queue as critical path."** AI review correctly reframed SU(2) result. sporePrint demonstration era live. Data Braids doubled (172 GB → 356 GB). biomeGate joined mesh (7/8 agentic).

**60 files fossilized** across 5 checkpoints. 12 active AARs, 5 active handoffs.
- **biomeGate: FULLY AGENTIC.** WG mesh LIVE (8/10 peers). 3 VFIO GPUs. coralReef 3,553 tests. 44-experiment matrix.
- westGate: **356 GB / 32 datasets.** tideGlass 7/7 COMPLETE. NCBI + Synapse API keys live. CAS 5,500+.
- strandGate: **Rung 1 experiment queue ACTIVE.** β-scan, HMC diagnostics, increased stats. Dual EPYC + RTX 3090 + RX 6950 XT.
- ironGate: **Session 3 complete.** Tier 2 deep debt cleared. Pure Rust evolution.
- sporePrint: **Data Braids v2.** 16 site pages. LaTeX updated with Rung 1 reframing.
- blueGate: **v4.56.** G29 H2 DNS secondary LIVE.
- sporeGate: **v4.56.** G29 3-way DNS COMPLETE.
- southGate: **NUCLEUS 22/22 PASS.** Validation gate.

**11 gates ONLINE** (6 NUCLEUS, 1 crankshaft + agentic, 4 other). **8 glacial goals COMPLETE** (G3, G4, G8, G10, G17, G21, G22, G29).
**13 ACTIVE** (G7, G9, G11, G14, G15, G18, G19, G20, G30, G31, **G32**, **G34**, **G35**).
**13 GLACIAL** (future phases).
**34 total glacial goals** tracked.

**Rung 1 experiment queue ACTIVE.** 6-rung lattice QCD ladder defined. SU(2) → SU(3) → quenched → dynamical → (2+1) → hot QCD.
**Silicon deism vendor cracking ACTIVE.** biomeGate: 3-GPU VFIO bench. strandGate: CPU + NVIDIA + AMD validation.
**Data federation: 362 GB.** tideGlass 7/7 COMPLETE. 38 braided datasets across 17 domains. Inter-gate experiment comms ENABLED via 10G LAN.

**Open items:**
- Rung 1 experiment queue (β-scan, HMC diagnostics, increased statistics) — blocks arXiv submission
- G32: coralReef diesel engine — biomeGate 3-GPU vendor solve
- G34: Outer membrane egress masking — Flint boundary router spec ready
- G35: Fully agentic LAN — 7/8 gates SSH'd, flockGate blocked
- Bundle data population (westGate → pseudoSpore bundles)
- tideGlass spin-up — 7/7 data COMPLETE, highest priority dormant

---

*Last used*: Wave 155n silicon deism + publication (Aug 2, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 155n springs-entry (58 files across 5 checkpoints)
*Latest reopen*: Wave 155k (D10 — Jelly Strings J9–J13, extended to J14–J19 in 155n)
