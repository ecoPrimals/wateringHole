# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155v/156d)
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
- [x] **squirrel 4,613 tests** (consolidated 34→1 binary) — 90.1% coverage, 0 unsafe, Wave 156d sovereignty cleanup + 27 deprecated aliases removed
- [x] **Provenance 7/7 COMPLETE** — E2E validated on westGate (5th consecutive pass) + blueGate (Windows)
- [x] **Sovereign CI LIVE** — push-to-deploy E2E verified for ALL 13 primals including biomeOS (coevolution).
- [x] **Coevolution contract COMPLETE (G21)** — biomeOS `composition.test_swap` + cellMembrane `validate_with_deps`. Mode gap FIXED (`652cf8a7`).
- [x] **94 files fossilized** across 7 checkpoints. Latest: `wave155v_absorbed/` (20 files — 15 handoffs + 5 AARs). Active AARs: 20. Active handoffs: 16.
- [x] **whitePaper convergence (G22)**: **COMPLETE** — biomeOS v4.56 single-process merge. Dual-protocol (riboCipher + JSON-RPC) in one process. Validated on westGate + sporeGate.
- [x] **Portability checkpoint (G17) — PROVEN.** southGate 22/22 PASS. NUCLEUS from public depot, own entropy, user-space paths, no WireGuard, no inherited identity. 20h stable, 32 sockets, 76MB RSS, 29,294 foreign peer rejections.
- [x] **DATA FEDERATION (westGate)** — **519 GB, 130 datasets, 9+ domains, ~260K+ files, CAS 5,800+**, 100% provenance. tideGlass 7/7 COMPLETE. AlphaFold v6 42/46 proteomes. 50+ public sources. `data_catalog.toml` v2.0.0 shipped. **Inter-gate experiment comms over 10G LAN ENABLED.**
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
- [x] **SPRINGS-TO-NUCLEUS MESH (Aug 2)** — All 10 springs/gardens assigned to gates by hardware specialization. Cell graphs v2.0.0 (content.get + provenance trio + gate metadata). tideGlass Cargo workspace LIVE. biomeOS deploy graphs v2.0.0. Inter-gate CAS data access config created. ecosystem_manifest v3.3.0 with spring_mesh assignments.
- [ ] **PLANNED SERVICE INTERRUPTION (Aug 2)** — ATT gateway + DS224+ moving to basement. steamGate + reefGate enrollment queued post-move.

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~135K+ primal tests validated this wave** (songBird 14,840, bearDog 14K, nestGate 13K, toadStool 9.2K, biomeOS 8,570, petalTongue 6,755, barraCuda 5,037, squirrel 4,613, coralReef 3,512, rhizoCrypt 1,900, loamSpine 1,740, sweetGrass 1,645, cellMembrane 1,281+, tideGlass 176, primalSpring 197, skunkBat, footPrint 628, esotericWebb V30)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **14,019** tests, crypto.sign SHIPPED, dual-socket fix, FAMILY_SEED precedence, 94 orphan files purged (**Wave 155m**)
- [x] songBird: **14,840+** tests, universal-ipc, ACME HTTP-01, TCP registration fix, **`mesh.connectivity_check` + `mesh.throughput` SHIPPED (20 mesh methods)** (**Wave 155p**)
- [x] nestGate: **13,095+** tests, CAS on ZFS verified, deep debt complete, zero unsafe
- [x] toadStool: **9,193+** tests, **S349**: JSON-RPC health endpoint, dead deps purged, stubs fail-closed, hardcoding consolidated (**Wave 155m**)
- [x] biomeOS: **8,570+** tests, **v4.56**: G22 convergence, spring deploy graph executor SHIPPED, deep debt audit CLEAN (zero debt all categories), 139.2 GiB recovered. (**Wave 155p**)
- [x] petalTongue: **6,755** tests, CAS storage discovery refactor, canonical `get_family_id()`, hardcoded primal names removed (**Wave 156b**)
- [x] barraCuda: **5,037** tests, RTX 3090 profiled, **P0 shader fixes SHIPPED**: subgroup entry point `main→sum_reduce_f64` FIXED, PRNG compose duplicate-definition FIXED, `diversity_f64.wgsl` self-recursion FIXED. (**Wave 155p**)
- [x] ~~**barraCuda YELLOW**~~ → **GREEN**: PRNG half-range fixed (xoshiro 52→53 bits). Statistical validation harness. -1,488 LOC (LazyLock→const, error helpers). `cpu_mom` remains production HMC path (Box-Muller transcendental polyfill, not PRNG).
- [x] coralReef: **3,553** tests on biomeGate revalidation, 463 `.expect()` purged, PTX modernized
- [x] cellMembrane: **1,281+** tests, **P2 platform detection FIXED** (`d7026d7`), `TargetArch` deprecated → `Platform::detect()`, `validate_with_deps()`, J19+J16+J13 killed, registry API hardened. (**Wave 155n**)
- [x] rhizoCrypt: 1,900 tests, BTSP→DAG bridge, cross-gate provenance
- [x] loamSpine: **1,739** tests, registry drift fixed, `--bind` alias
- [x] sweetGrass: **1,645** tests, G3 E2E validated, **G31 batch pipeline SHIPPED** + concurrent `batch_commit` + trailer pattern alignment. DH-0 clean. (**Wave 156b**)
- [x] squirrel: **4,613 tests** (consolidated from 7,243 — 34→1 binaries), 90.1% coverage, 0 unsafe, 0 clippy, **`signal.dispatch` WIRED (G18)**, **156b test perf 400s→16s**, build 9.5→4.1 GiB (**Wave 155p→156b**)
- [x] primalSpring: 197 scenarios, all PASS
- [x] skunkBat: 9 threat types, ConnectivityAnomaly, frame crypto, PUBLIC
- [x] **BTSP 13/13** — all primals shipped ClientHello
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: 6/6 seams DONE
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [ ] **Inter-gate content.get E2E — READY TO TEST**: songBird `mesh.connectivity_check` + `mesh.throughput` SHIPPED. biomeOS routing READY. Need **live operational test** on actual gates (not code — ops). Blocks all data-remote springs.
- [x] **G31 batch provenance — STRUCTURALLY COMPLETE**: `dag.event.append_batch` LIVE (200/batch). sweetGrass concurrent `batch_commit`. Per-file spine entries removed (canonical architecture — 122× improvement). Provenance loop CLOSED (bearDog sig in sweetGrass braid). Remaining: `spine.entry.batch` for edge cases, E2E trio validation on westGate.
- [x] **G18 squirrel → biomeOS integration — LIVE ON IRONGATE**: squirrel rebuilt from source, `signal.dispatch` operational with 9 primal providers. Cross-primal routing validated (squirrel → rhizoCrypt 1ms, squirrel → bearDog crypto). esotericWebb + footPrint infrastructure confirmed ready.
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
| ironGate | **NUCLEUS (13)** | Linux | 10.13.37.7 | **NUCLEUS (13)** | **DOWNSTREAM HOST.** G18 DISPATCH LIVE (9 providers). 12.7 TB CAS on `/mnt/nestgate`. songBird federation to westGate. i9-14900K, RTX 5070, 94 GB. esotericWebb + footPrint LIVE. |
| flockGate | **DOWN** | Linux | 10.13.37.6 | full | Rebooted, RustDesk locked out. esotericWebb → **ironGate** |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090. **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | **NUCLEUS v4.57+ (restart deferred)** | Linux | 10.13.37.10 | **NUCLEUS (13)** | GPU at 100% QCD. Config cache COMPLETE (9/10 16⁴ configs, 325 MB). Dual-GPU scan LAUNCHED. RTX 3090 + RX 6950 XT. |
| westGate | **NUCLEUS v4.57** | Linux | 10.13.37.11 | **NUCLEUS (13)** | **DATA NAS.** 14/14 HEALTHY. GPS data CONVERTED (11 JSON, 103 MB CAS). Convergence: 89 PARTIAL, 32 PRIMORDIAL, 0/153 fully braided. |
| blueGate | **NUCLEUS v4.57+** | Windows | 10.13.37.12 | **NUCLEUS (13)** | 14/14 HEALTHY. UniBin CLI migration documented. |
| biomeGate | **GPU CRANKSHAFT + FULLY AGENTIC** | Linux | 10.13.37.3 | compute | Threadripper 3970X, 128GB. 3 VFIO GPUs. coralReef 3,553 tests. 44-experiment matrix. **WG mesh LIVE, 8/10 peers, Forgejo SSH working.** G32 silicon deism. |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| southGate | **NUCLEUS v4.57+ — 13/13 RE-VALIDATED** | Linux | **NO WG** (deliberate) | **NUCLEUS (13)** | 5800X3D + RTX 4060 + 128GB + 5TB NVMe. **G17 PROVEN. G8 PROVEN.** Re-validated after 97h uptime. Tower 0.15ms avg, 19 Gbps. |
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
| **NUCLEUS** (13) | **ACHIEVED ×6 — ALL GATES v4.57+** | **sporeGate** (14/14, CI build authority), **ironGate** (10/10, cell boot), **westGate** (14/14, GPS converted), **strandGate** (staged, GPU 100%), **blueGate** (14/14, UniBin), **southGate** (13/13, re-validated) | 27 signal graphs. biomeOS v4.57+ in depot. **G22 COMPLETE.** |

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
| **Game engine / creative** | esotericWebb → petalTongue → coralReef (shaders, WebGL) | **ironGate** (downstream host) | V22 live (flockGate), 453 tests, scene binding, moving to ironGate cell boot |
| **AI agent orchestration** | squirrel (4,613 tests, 90.1% cov, G18 wired) → biomeOS neuralAPI → any primal | any NUCLEUS gate | Capability routing proven (835+ caps) |
| **Genomics pipeline** | wetSpring → toadStool → nestGate (16S rRNA, GPU) | strandGate (RTX 3090) | Pipeline validated, cold (needs data) |
| **NF drug reversal (Gonzales/Bin)** | tideGlass → Nest Atomic → Provenance Trio → petalTongue (GPS viz) | westGate | Specs shipped, 519 GB data ready, Phase 0 NEXT. Mid-term: Cell 2026 rebuild → NF screen → CTF NDU |
| **GIS data** | footPrint → nestGate → petalTongue | **ironGate** (downstream host) | Matures petalTongue G19 → reusable for tideGlass GPS viz |
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
| squirrel AI agent | YES (4,613 tests, 90.1% cov, G18 wired, 156b: 400s→16s) | biomeOS neuralAPI routing, user-facing agent |
| Nest Atomic CAS | YES (3,252 objects, ZFS) | Data ingestion pipelines (AlphaFold, NF) |
| Provenance Trio | YES (7/7 E2E) | Every workload gets provenance tracking |

### gen5 Dual-Science Pipeline

Two mid-term science tracks drive ecosystem evolution. Both consume the same primals, but exercise different capabilities. The support structures (footPrint, esotericWebb on ironGate) mature petalTongue (G19), which then serves both tracks.

**Track A — NF Drug Repurposing (Gonzales/Bin Chen)**
tideGlass rebuilds Cell 2026 GPS platform → NF drug reversal screen → CTF NDU grant.

- [x] **Step 1**: Provenance 7/7 — **DONE**
- [x] **Step 2**: westGate data federation — **519 GB, 7/7 modules data-ready**
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
- [ ] **Step 4**: arXiv Rung 1 submission — relabel SU(2)→SU(3), β-scan, HMC diagnostics. **NEXT.**
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

**ACTIVE (27 goals — in progress or unblocked):**

| ID | Goal | Status | Next Step |
|----|------|--------|-----------|
| G7 | Science data ingestion | **519 GB on ZFS** — 130 datasets, 9+ domains, 50+ sources. tideGlass 7/7 COMPLETE. AlphaFold v6 42/46 proteomes. Full 5-step provenance on every byte. | AlphaFold 23TB eventual. SRA FASTQ ~220 GB pipeline next. |
| G9 | arXiv publication (Murillo/Chuna QCD) | **16⁴ DUAL-GPU DATA COMPLETE.** β=6.0: +0.01% vs published. β=6.2: -0.04%. Cross-vendor 6 ppm (RTX 3090 vs RX 6950 XT). AMD 9.4x faster at 16⁴. 42-item reviewer rubric shipped. Reviewers: Murillo, Chuna, Bazavov. | Address 12 MUST-fix rubric items → LaTeX → reviewer send → arXiv submit. |
| G11 | Any chip + drive = mesh gate | ACTIVE | biomeGate + ironGate proved. steamGate NEXT. |
| G14 | sporePrint live science refresh | ACTIVE | pseudoSpore LIVE. Auto-publish FIXED. |
| G15 | tideGlass Phase 0 (NF archaeology) | **UNBLOCKED** | ChEMBL+PDB in CAS. Spin up tideGlass on westGate. |
| G18 | squirrel → biomeOS agent orchestration | ACTIVE | Springs+gardens: wire neuralAPI dispatch. |
| G19 | petalTongue + Node Atomics live rendering | ACTIVE | hotSpring QCD viz + esotericWebb. |
| G20 | esotericWebb game engine on NUCLEUS | **ACTIVE on ironGate** | **V30** — cell graph validation + batch prov. NUCLEUS substrate live. RTX 5070 ready. |
| G30 | westGate data federation root | **519 GB / 130 datasets / 9+ domains.** tideGlass 7/7. CAS 5,800+. 50+ sources. AlphaFold v6 running. | biomeOS-native `data:want` cascade to replace `bulk_ingest.py`. |
| G31 | Batch RPC for provenance pipeline | **STRUCTURALLY COMPLETE.** `dag.event.append_batch` LIVE (200/batch). sweetGrass concurrent `batch_commit`. Per-file spine entries removed (canonical architecture). | `spine.entry.batch` for edge cases. E2E trio validation on westGate. |
| G32 | Silicon deism vendor cracking | **NEW — biomeGate** | 3-GPU bench (RTX 5060 + Tesla + Titan V). coralReef diesel engine. hotSpring cross-vendor validation. |
| G34 | Outer membrane egress masking | **SPEC** | Flint as boundary router. Single opaque tunnel to golgi. ATT box sees nothing. |
| G35 | Fully agentic LAN | **7/8 DONE** (biomeGate joined mesh). | northGate + flockGate blocked (physical access). `membrane remote.enroll` proposed. |
| G36 | tideGlass Phase 1 — GPS reproduction (Gonzales/Bin Chen) | **ACTIVE** (specs shipped, G15 done) | RGES r=0.52, RCL SNR >1.5×, GPS4Drug R² within 5%. Cargo workspace LIVE. Specs: ARCHITECTURE, MODULE_SPECS, DATA_ACCESS, PHASE_0_CHECKLIST, VISUALIZATION. Mid-term deliverable: **sovereign rebuild of Cell 2026 GPS platform.** |
| G37 | NF Reversal Screen (Gonzales NF collaboration) | **ACTIVE** | RGES vs LINCS, ZINC compound screening, MEK inhibitors (selumetinib) in top-100. NF Data Portal ingested (658 files). Depends G36. |
| G38 | NF PseudoSpore artifact | **ACTIVE** | Self-verifying USB: data + code + provenance. `./validate` runs 7 tideGlass modules. **First gen5 science deliverable.** |
| G39 | CTF NDU grant ($125K) | **ACTIVE** | Preliminary data package for Children's Tumor Foundation NDU. Depends G36+G37. |
| G43 | steamGate — immutable OS handheld | **ACTIVE** | Steam Deck OLED. User-space musl deploy on read-only SteamOS. G17 pattern. |
| G44 | reefGate — paired intelligence/storage | **ACTIVE** | DDR3 NUC + Synology DS224+ NFS. G23 fractional replication target. |
| G45 | Lattice QCD Rungs 2–6 (Murillo/Chuna program) | **ACTIVE** (Rung 2 next) | SU(3) → quenched → dynamical → (2+1)-flavor → finite-T. Mid-term: **vendor-agnostic QCD on consumer GPUs** — barraCuda DF64, coralReef WGSL shaders, petalTongue QCD visualization. Each rung is publishable. |

**GLACIAL (20 goals — future phases):**

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
| G53 | petalTongue maturation via downstream consumers | **ACTIVE** | footPrint (GIS/Leaflet) + esotericWebb (game/WebGL) on ironGate evolve petalTongue G19 live render → mature visualization becomes GPS viz for tideGlass NF (G37) + QCD viz for hotSpring (G45). **Conjugation architecture**: RustScript (`@protokarya/rustscript`) is the TypeScript conjugation layer, not scaffolding — 11 modules encoding Rust safety patterns (Result, Option, Owned, RefCell, Iter, Brand, Channel) for browser/TS-native targets. petalTongue owns render; RustScript conjugates safety across the language boundary. |
| G54 | Dual-science mid-term convergence | **ACTIVE** | **Track A (NF/GPS — Gonzales/Bin)**: tideGlass rebuilds Cell 2026 paper → NF drug repurposing → CTF NDU grant. **Track B (QCD — Murillo/Chuna)**: hotSpring arXiv Rung 1 → 6-rung lattice QCD program. Both tracks consume barraCuda (GPU math), petalTongue (viz), provenance trio (chains), nestGate (data). Infrastructure evolves toward both simultaneously. |
| G55 | Provenance batch RPCs (braids at machine speed) | **LARGELY RESOLVED** | `dag.event.append_batch` LIVE (200/batch, rhizoCrypt). Per-file spine entries REMOVED (canonical architecture alignment — 122× improvement). Trailer at 37.6/s sustained. Gap narrowed to 2× (vs 247× before). bearDog signature wired into sweetGrass braid — provenance loop CLOSED. Remaining: `spine.entry.batch` for future edge cases. |
| G56 | Neural API activation (capability routing everywhere) | **ACTIVE** | All consumers route through biomeOS Neural API (`neural-api-default.sock`) instead of direct primal sockets. footPrint, tideGlass, esotericWebb, all springs. Eliminates hardcoded socket paths. biomeOS routes `content.get`/`content.put`/`visualization.render` etc. via capability discovery. When primals evolve (e.g., nestGate adds `content.query`), consumers get it without rewiring. |
| G57 | nestgate.io data identity surface | **PHASE 1 LIVE (branded)** | **nestgate.io LIVE, branded, HTTP 200.** Dashboard renders but all sections "Loading..." — petalTongue on sporeGate cannot reach mesh data from public internet path. NEXT: SSR pre-render or WebSocket bridge from petalTongue to mesh sockets. Phase 2: depot+provenance browser. Phase 3: federated CAS. Phase 4: validation API. |
| G58 | Mixed provenance convergence | **ACTIVE** | Promote all westGate data from primordial/CAS-only to fully braided. `is_dataset_converged()` gate for springs. Revalidation running for priority + AlphaFold. All spring-critical data fully braided before Phase 4 boot. |
| G59 | Three-domain topology (k-derm website separation) | **DNS COMPLETE** | **ALL 3 LAYERS SEPARATED.** primals.eco LIVE (Cloudflare, 14 Caddy routes). nestgate.io LIVE (sovereign Knot DNS, petalTongue mesh). primal.eco SEALED (6 A records removed, dnsmasq-only). DNSSEC verified. Caddyfile version-controlled. Remaining: deploy dnsmasq config, wire nestgate.io content backend (4 DIVs), brand nestgate.io. |
| G60 | Federated CAS (nestgate.io cross-gate data surface) | **ACTIVE** | nestgate.io as federated CAS front door — hash requests resolve across mesh (westGate data, strandGate compute configs, ironGate consumer data). `content.locate` → songBird mesh broadcast → first-responder-serves. L1 cache on golgi for hot objects. Enables cross-gate data retrieval without knowing which gate holds data. Replication endpoint for reviewers. |
| G61 | Compute memoization via provenance trio | **ACTIVE** | strandGate thermalized lattice configs as CAS objects with provenance braids. 37 min CPU thermalization → instant on cache hit. Same BLAKE3→CAS→DAG→braid pattern as data acquisition. Cross-gate: biomeGate pulls configs for parity checks. Parallel pipeline: GPU produces while CPU thermalizes next β. NFT-style braids for both config and production results. |
| G62 | Nanowire → Primal Builder (mesh-routed builds) | **ACTIVE** | Phase 2a DONE: manifest-driven sub-builders (no recompile to add gates). Phase 2b SPEC: songBird mesh-routed `harvest.request`/`harvest.complete`. Foreman pattern: symmetric — any gate can request, any gate can build. Capability advertisement on startup. Parallel dispatch. biomeGate as second sub-builder (NW-05 pending). |
| G63 | BTSP local-trust (SO_PEERCRED for same-gate UDS) | **ACTIVE** | nestGate accepts same-gate callers without full BTSP X25519 handshake. Process-level auth via `SO_PEERCRED` — membrane group callers are trusted by filesystem perms. Unblocks footPrint CAS write, tideGlass CAS integration, all gardens/protists on same gate. Zero config, maximally primal-like. Proposed in footPrint Phase 2 deploy ready handoff. |
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

---

**Active**: 10 dimensions (1–5, 7–8, 10–12)
**Fossilized**: 13 dimensions (F1–F13)
**Summary**: Wave 155v/156d — **K-DERM SEPARATION COMPLETE + 13/13 GREEN.** All 3 DNS layers separated: primals.eco (Cloudflare, 14 Caddy routes), nestgate.io (sovereign Knot DNS, petalTongue mesh LIVE), primal.eco (SEALED — 6 A records removed, dnsmasq-only). DNSSEC verified (DS 2371/13/2). Caddyfile version-controlled from golgi. Provenance RESOLVED (122×). strandGate 12⁴ paper-ready. esotericWebb V30d. footPrint 628 tests. squirrel pushed (156d). G60-G63 added. 20 docs fossilized (94 total). ZERO P0/P1/P2. ~135K+ tests. **59 glacial goals** tracked (8 COMPLETE, **31 ACTIVE**, 20 GLACIAL/CONCEPT).

**Phase shift**: From "separate and spec" to **"wire and activate."** K-derm DNS separation DONE — all 3 layers have distinct DNS postures (Cloudflare / sovereign / sealed). Now: wire nestgate.io content backend (4 DIVs), deploy dnsmasq for inner membrane, Neural API everywhere, inter-gate content.get E2E, first spring boots. 12⁴ arXiv data is paper-ready. Springs can boot on braided data.

**94 files fossilized** across 7 checkpoints (`wave155v_absorbed/` = 20 files: 15 handoffs + 5 AARs). 20 active AARs, 16 active handoffs.
- **ironGate: PRIMARY DOWNSTREAM HOST.** NUCLEUS 26/27 HEALTHY. G19 PROVEN. esotericWebb V29. footPrint 563 tests. Phase 1 structurally ready. RTX 5070.
- westGate: **DATA NAS. 519 GB / 130 datasets.** Provenance divergence AAR. 3 provenance states converging. tideGlass 161 tests (CAS wired). airSpring 1,157. wetSpring 2,210.
- strandGate: **COMPUTE DEV.** Silicon deism VALIDATED (paper-ready). hotSpring arXiv production. neuralSpring V183 (1,518 tests).
- biomeGate: **GPU LAB.** 3 VFIO GPUs. G32 silicon deism.
- eastGate: **squirrel LOCAL** — 156b test perf 400s→16s, 4,613 tests.
- blueGate: **WINDOWS DEV.** ludoSpring. Sub-builder divergences 8/10 resolved.

**11 gates ONLINE** (6 NUCLEUS at v4.57+, 1 crankshaft + agentic, 4 other). **9 glacial goals COMPLETE** (G3, G4, G8, G10, G17, G21, G22, G29, G63).
**30 ACTIVE** (G7, G9, G11, G14, G15, G18, G19, G20, G30, G31, G32, G34, G35, G36, G37, G38, G39, G43, G44, G45, G53, G54, G55, G56, G57, G58, G59, **G60**, **G61**, **G62**).
**20 GLACIAL/CONCEPT** (future phases).
**59 total glacial goals** tracked.

### LIVE SITE ASSESSMENT (Aug 4 PM)

| Site | URL | HTTP | Functional? | Primary Issue |
|------|-----|------|-------------|---------------|
| **sporePrint** | `sporeprint.primals.eco` | 200 | **YES** | Zola static — renders well, claims verifiable, science content accurate |
| **footPrint** | `footprint.primals.eco` | 200 | **PARTIAL** | Map UI loads but initializes empty. Agent not connected (`agentConnected:false`). CAS has 3 objects + 1 project (real GIS). Tiles blocked by dual CSP headers (Express + Caddy both emit). Need: auto-load default project, squirrel connect, single CSP source. |
| **nestgate.io** | `nestgate.io` | 200 | **PARTIAL** | Branded dashboard loads but ALL sections "Loading..." — JS fetches mesh data from endpoints unreachable on public path. Need: SSR pre-render, or WebSocket bridge from petalTongue to live mesh sockets. |
| **esotericWebb** | `webb.primals.eco` | **502** | **NO** | CRPG engine is IPC-only (Rust + cell graph). No HTTP server or browser client. petalTongue WebGL render pipeline required for browser game. 502 = Caddy has no backend to proxy to. |

**MID-TERM SCIENCE TRACKS**:
- **Track A (NF/GPS)**: G15→G36→G37→G38→G39. Gonzales/Bin Chen. tideGlass rebuilds Cell 2026 → NF reversal screen → CTF NDU $125K.
- **Track B (QCD)**: G9→G45. Murillo/Chuna. arXiv Rung 1 → 6-rung lattice QCD on consumer GPUs.
- **Support convergence (G53)**: footPrint + esotericWebb on ironGate → petalTongue G19 → GPS viz (Track A) + QCD viz (Track B).

**Gauge group resolved in code** (G9): SU(3) labels disambiguated in barraCuda/hotSpring. Paper/site relabel still needed (sporePrint scope). arXiv UNBLOCKED.

**Open items — prioritized by data pipeline + springs readiness:**
- **G55: Batch RPCs for provenance** — `dag.event.append_batch` already LIVE (200/batch). Per-file spine entries REMOVED (canonical architecture). Gap narrowed to 2× (37.6/s vs 74/s). Remaining: `spine.entry.batch` for edge cases.
- ~~**G59: Three-domain topology**~~ — **DNS SEPARATION COMPLETE.** All 3 layers separated. primal.eco SEALED (6 A records removed). nestgate.io LIVE on mesh. DNSSEC verified. Remaining: deploy dnsmasq, wire content backend, brand nestgate.io.
- **G56: Neural API activation** — route footPrint, tideGlass, esotericWebb, all springs through `neural-api-default.sock`. Eliminate hardcoded socket paths. biomeOS signal graphs already wired for data federation.
- **G57: nestgate.io** — **PHASE 1 LIVE** (petalTongue mesh). 4 DIVs: content backend, discovery service, port conflict, branding. Phase 2: depot+provenance browser. Phase 3: federated CAS API.
- **G58: Mixed provenance convergence** — promote primordial → braided for all spring-critical data. `is_dataset_converged()` gate. Revalidation running.
- **nestGate canonical client crate** — 6 tideGlass CAS divergences (DIV-1→6). groundSpring + airSpring have stale CAS clients. One crate for all.
- ~~**biomeOS cell attachment CLI**~~ — **SHIPPED** (`biomeos nucleus attach`, v4.57).
- **toadStool ExecStart fix** — BLOCKING 9/9 membrane composition.
- **membrane socket permissions** — root:root → group-writable for `biomeos`.
- **footPrint live refinement** — dual CSP headers (Express + Caddy), no auto-load, squirrel not connected.
- **esotericWebb web surface** — 502 from `webb.primals.eco`. Needs petalTongue WebGL pipeline or standalone HTTP serve mode.
- **nestgate.io mesh bridge** — dashboard "Loading..." from public. Needs SSR pre-render or WebSocket relay.
- ~~arXiv plaquette ×4 normalization~~ — **RESOLVED** (gauge group mismatch SU(2)→SU(3). 12⁴ data paper-ready. Rung 1 UNBLOCKED).
- ~~squirrel → biomeOS G18 integration~~ — **LIVE on ironGate** (Session 10). 9 providers, cross-primal dispatch validated.
- Inter-gate content.get live test (songBird probes + nestGate content.fetch ready)
- petalTongue WebGPU/wgpu evolution (G53 maturation) — conjugation layer (RustScript) established, petalTongue render pipeline is the remaining gap
- ~~barraCuda PRNG validation~~ — **FIXED** (YELLOW→GREEN, statistical validation harness)
- ~~BTSP transport signal documentation~~ — SHIPPED

---

*Last used*: Wave 156d — G18 signal dispatch LIVE (ironGate, 9 providers). ironGate 12.7 TB CAS + songBird federation. Convoy 145/s (460x). 16⁴ dual-GPU data COMPLETE (6 ppm, +0.01%). tideGlass 214 tests. Reviewer rubric 42 items. (Aug 5, 2026 AM)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 156d — 25 files to `wave156d_depot_sync_complete/` (139 total across 9 checkpoints)
*Latest reopen*: Wave 155k (D10 — Jelly Strings J9–J13, extended to J14–J19 in 155n)
