# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155k)
- [x] Gate heads published (`heads/*.toml`) — golgiBody auto-publishing active
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] **ECOSYSTEM_BLURB.md** is the universal handoff (Tracks A+B converged)
- [x] **54 handoff docs + AARs** delivered Wave 155b–k
- [x] **ALL P0s RESOLVED. ALL P1s RESOLVED.** 12 teams STANDBY.
- [x] **NUCLEUS ACHIEVED** — strandGate (8/9, 1,742 caps), blueGate (13/13 Windows infra)
- [x] **Depot 14/14 REBUILT** by sporeGate (Jul 30) — 33 binaries, 5 targets, BLAKE3 verified
- [x] **biomeOS v4.47 NUCLEUS orchestrator DEPLOYED** on sporeGate — composition lifecycle, socket unification, capability persistence
- [x] **bearDog crypto.sign_ed25519 SHIPPED** (`3739e7078`) + Windows platform gating (`d6b1003bb`)
- [x] **Provenance 7/7 UNBLOCKED** — pending live validation
- [x] **Cross-platform expansion**: steamGate (Steam Deck) NEXT, darwinGate + iosGate GLACIAL
- [x] **Pipeline automation J9–J13** identified and handed off to sporeGate/cellMembrane
- [x] D10 (Jelly Strings) REOPENED for J9–J13
- [ ] waterFall graph partially wired — full composition pending Provenance Trio live validation
- [ ] Context braids not yet replacing blurb paste — graduation path documented
- [ ] 2 enrolling gates have no published heads in `heads/*.toml`
- [ ] **Windows CI gate** — `cargo check --target x86_64-pc-windows-gnu` not yet in CI

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~63K+ primal tests validated this wave** (nestGate 13K+, toadStool 9.2K+, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.7K, cellMembrane 1.2K)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] nestGate vendor elimination COMPLETE (Wave 150u)
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **14,019** tests, FIDO2 hardware, beacon proximity, HSM agnostic, **crypto.sign_ed25519 SHIPPED**, Windows platform gating SHIPPED
- [x] songBird: 14,835+ tests, `mesh.gate_enroll`, universal-ipc, J3+J4+J5, `tower.health` facade, **ACME HTTP-01 Phase 1**
- [x] nestGate: **13,095+** tests, CAS on ZFS verified (3,119 objects), deep debt complete, zero unsafe, zero panics, ghost methods removed, CLI evolved
- [x] toadStool: **9,193+** tests, **S346**: security fail-closed (macOS/Windows sandbox), unsafe containment (hw-safe crate), 75 doc warnings fixed, doctor CLI bug fix
- [x] rhizoCrypt: 1,456 tests, BTSP→DAG bridge, cross-gate provenance chain
- [x] loamSpine: **1,739** tests, **BTSP handshake dedup**: `verify_and_negotiate()` + `AsyncErrorSender`. **155i**: registry drift fixed — `certificate.verify/lifecycle/history` discoverable
- [x] sweetGrass: **1,636** tests, **v0.8.0**, **G3 E2E validated** — `LedgerClient`, mock loamSpine UDS, 11 E2E ledger tests. Provenance Trio CLOSED in source, 6/7 live on westGate
- [x] petalTongue: **6,605** tests, **topology→runtime manifest**, main.rs split, geometry module
- [x] squirrel: **763** tests, **capability purification**: beardog→security_provider, adapter IPC
- [x] barraCuda: **4,957** tests, **RTX 3090 profiled** (FP64 ~104 TFLOPS, DF64 framing corrected), deep debt sweep (10 batch funcs deprecated to shader path, self-knowledge, `ShaderValidationBackend::SovereignCpu`)
- [x] coralReef: **3,527** tests, **deep debt**: 463 `.expect()` eliminated, PTX macro modernization (-363L net), capability-based env keys
- [x] primalSpring: 197 scenarios, all PASS, calibrated for 13-gate mesh
- [x] skunkBat: spawn-rate anomaly detection, `ConnectivityAnomaly` (9th threat), frame crypto, PUBLIC
- [x] **BTSP 13/13** — all primals shipped ClientHello
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: 6/6 seams DONE
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [x] **cellMembrane**: **1,221** tests, **deep debt**: sandbox fail-closed, registry-driven tower status (no hardcoded names), 5 dedup extractions (-135 net lines)
- [x] ~~nestGate: ghost methods `content.repo.*`/`content.mirror.*`~~ — **REMOVED** (capability_registry cleaned)
- [x] ~~bearDog `crypto.sign_ed25519` returns health stub~~ — **SHIPPED** (`3739e7078`) — Provenance 7/7 UNBLOCKED
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Physical Topology

- [x] Mixed 10G + 1G topology LIVE — 10G AOC backbone between houses, MikroTik CRS310 + Omada SX3008F
- [x] sporeGate on R45 → MikroTik — plasma membrane router (NAT/DHCP/DNS/nftables)
- [x] eastGate on MikroTik LAN — code hub, 10G SFP+ direct
- [x] northGate enrolled (Windows 11, RTX 5090, 2.5G ethernet)
- [x] westGate ONLINE — AMD Ryzen 7 5700X / 64GB DDR4 / 2TB NVMe / **ZFS 25.4TB mirrors + 2TB L2ARC SSD, all 5 storage tiers operational**
- [x] ironGate HDD — 14TB + 1TB + 1TB + ~2TB, enclave experiment planned
- [x] blueGate + swiftGate: Windows, house2, 10G backbone proven
- [x] grapheneGate: Android, Tower LIVE (bearDog + songBird + skunkBat)
- [x] 10G AOC trunk CRS310↔Omada proven (blueGate reaches relay via backbone)
- [x] **TOPOLOGY_MAP.toml** has full physical layout with cytoplasm zone model
- [ ] **steamGate** (Steam Deck) — NEXT cross-platform gate. SteamOS (Arch, glibc). User-space deploy.
- [ ] **darwinGate** (Mac Mini) — GLACIAL. Needs HW acquisition. First apple-darwin target.
- [ ] **iosGate** (iPhone) — GLACIAL. Needs darwinGate + Apple Dev Program. Walled garden research.
- [ ] fieldGate OFFLINE (dead CMOS)
- [ ] biomeGate OFFLINE (kernel recovery)
- [ ] Complete port→gate mapping (CRS310 + Omada + TL-SG605S-M2)
- [ ] Document Flint H1 + Flint 2 + Omada WiFi bridge configs

### Gate Fleet — Status Matrix

| Gate | Status | Platform | Mesh IP | Composition | Role |
|------|--------|----------|---------|-------------|------|
| golgiBody | ONLINE | Linux | 10.13.37.1 | thin-relay | Sole depot, enrollment, Forgejo, Drawbridge |
| sporeGate | ONLINE | Linux | 10.13.37.2 | full | Build authority, depot, cascade hub, **peptidoglycan anchor H1** |
| eastGate | ONLINE | Linux | 10.13.37.5 | full | Code hub, overwatch |
| ironGate | ONLINE | Linux | 10.13.37.7 | full | GPU compute, 4x HDD enclave, JupyterHub |
| flockGate | ONLINE | Linux | 10.13.37.6 | full | Nest Atomic validation (after Tower stable) |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090. **DAILY DRIVER — DO NOT DEPLOY.** AlphaFold data source (~1TB). |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | **NUCLEUS** | Linux | 10.13.37.10 | **NUCLEUS (13)** | **FIRST NUCLEUS.** 8/9 healthy, 1,742 caps, 674 IPC methods, RTX 3090 sub-ms GPU. STANDBY. |
| westGate | **BROKER LIVE** | Linux | 10.13.37.11 | nest (8) | **Deploy v4.47 + Compute Trio → second NUCLEUS.** 704 caps, 3,216 CAS. |
| blueGate | **13/13 WINDOWS** | Windows | 10.13.37.12 | **NUCLEUS infra** | Depot 14/14 fresh. Pull new bins → lifecycle-managed NUCLEUS. |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| southGate | HW READY | Linux | enrolling | full (13) | House2 sovereign site |
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
- [ ] DNS: verify dnsmasq on all Linux gates (sporeGate done, others PENDING)
- [ ] northGate DNS delay diagnosis (likely dead dnsmasq)
- [ ] Port→gate mapping incomplete (need physical audit)
- [ ] WiFi bridge documentation (Flint H1 + Flint 2 configs)
- [ ] Standardized gate provisioning script (DNS + RustDesk + health checks)

### Inner Membrane

- [x] **10-gate WireGuard mesh** — golgi, sporeGate, eastGate, flockGate, ironGate, northGate, grapheneGate, westGate, strandGate, **blueGate** (peer #9)
- [x] Tower Atomic LIVE on 6+ gates — westGate, strandGate, grapheneGate, eastGate, sporeGate, blueGate (Windows)
- [x] LAN peering: Tower 353x LAN (0.45ms vs 158ms WG overlay)
- [x] songBird universal-ipc: UDS/named pipes/abstract sockets/TCP
- [x] BTSP defense-in-depth: 13/13 primals
- [x] **biomeOS neuralAPI**: **27** signal graphs, **composition broker LIVE** (riboCipher + BTSP), 8,564 tests, **704 capabilities on westGate in COORDINATED mode**, E2E routing proven
- [x] **songBird ACME HTTP-01** challenge responder shipped — Phase 1 TLS elimination
- [x] songBird mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L
- [x] sporeGate depot fully refreshed: health 5/11→9/11, 19 binaries, glibc compute trio shipped
- [x] ~~**biomeOS BTSP session propagation**~~ — **SHIPPED** (`48cf9c33`): `send_jsonrpc_async` is BTSP-aware, family-scoped socket trigger handshake
- [x] ~~**biomeOS riboCipher transport**~~ — **SHIPPED** (`48cf9c33`): CLI + core IPC prepend `[0xEC, 0x01]` clear-tier signal
- [ ] songBird probes without riboCipher → sweetGrass log noise every 30s (P1)
- [ ] sporeGate mesh.reachability + rootpulse.ledger still degraded (2/11)
- [ ] Only 2 WG peers active in practice (enrollment pending for house2 gates)
- [x] ~~WireGuard DNS catch-all~~ — **FIXED** (cellMembrane `8d9bb58`): `WgConfig.dns` field + `DNS=` in wg-quick output

## 5. Sovereignty / Trust

- [x] K-Derm three-layer model intact (and now with peptidoglycan documented)
- [x] Forgejo sovereign inner membrane operational (43/43 repos)
- [x] Push mirrors relay to GitHub on commit
- [x] Sovereign outer membrane operational (Caddy TLS)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] **DNSSEC 3/3 domains complete**
- [x] RustDesk AGPL-3.0 compliant — learn-from-leverage posture
- [x] Sovereign depot auto-build pipeline DELIVERED (4 phases)
- [x] Crash-loop self-recovery LIVE — app breaker + systemd layers
- [x] Tower Atomic EXCEEDS WG (353x LAN, 1.7x WAN)
- [x] 6/6 exploration domains PROVEN LIVE
- [x] Genetic enrollment — two-layer trust
- [x] BTSP defense-in-depth
- [x] Depot provenance — builder=sporeGate, staleness alarm, multi-target
- [x] Crypto delegation — songBird → bearDog, chimera unblocked
- [x] golgiBody sole depot — no local depots, all genomeBins via Caddy TLS
- [ ] Phase 2: Tower cutover — shadow active, chimera design drafted
- [ ] Phase 1: Zola → sporePrint primal pipeline (crates.io a sub-goal)
- [ ] Phase 2: Forgejo → rootPulse — via Nest Atomic (**Nest LIVE on westGate — unblocked after BTSP broker**)
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
| **NUCLEUS** (13) | **ACHIEVED** | **strandGate** (8/9, 1,742 caps), **blueGate** (13/13 infra), **sporeGate** (v4.47 deployed) | 27 signal graphs. Lifecycle: **SHIPPED** (composition.start, boot_order). |

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

- [ ] **Provenance 7/7 live validation** — sweetGrass + loamSpine + bearDog crypto.sign E2E on a running gate
- [ ] **westGate NUCLEUS** — deploy biomeOS v4.47 + Compute Trio → second lifecycle-managed NUCLEUS
- [ ] **blueGate lifecycle NUCLEUS** — pull fresh depot bins → biomeOS-orchestrated startup
- [ ] **Cross-platform gates** — steamGate (NEXT), darwinGate (GLACIAL), iosGate (GLACIAL)
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
- [x] ~~Windows genomeBins stale~~ — **14/14 REBUILT** (sporeGate Jul 30). ALL platform gates fixed.
- [x] ~~**songBird Windows platform gate (P0)**~~ — **FIXED + IN DEPOT** (`d9bda555`)
- [x] ~~toadstool.exe blocked~~ — **FIXED** (S347 `2df71399b`). ~~coralreef.exe blocked~~ — **FIXED** (`edcd696`). ~~beardog.exe blocked~~ — **FIXED** (`d6b1003bb`)
- [x] **Depot: 33 binaries across 5 target directories** (musl, gnu, windows-gnu, aarch64-musl, aarch64-android)
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

**New jelly strings (Wave 155k)**:

- [ ] **J9**: Cascade trigger — Forgejo webhook → auto `temporal.cascade` (cellMembrane `webhook/pipeline.rs`)
- [ ] **J10**: Build trigger — post-cascade diff detection → auto `plasmid.harvest --primal <changed> --push`
- [ ] **J11**: Multi-target build — manifest-driven target selection (read gate compositions, build all needed arches)
- [ ] **J12**: Sub-builder dispatch — sporeGate dispatches Windows builds to blueGate via songBird IPC
- [ ] **J13**: Depot freshness probe — continuous SHA comparison (heads/*.toml vs depot provenance) + mesh alert on drift

**Pipeline target**: Forgejo push → cascade → diff → build → checksum → depot push → verify. Zero human.

**Owner**: cellMembrane (J9, J10, J13) + sporeGate (J11, J12) + blueGate (J12 sub-builder)
**Handoff**: `SPOREGATE_DEPOT_REBUILD_NUCLEUS_PIPELINE_WAVE155k.md`

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

**Active**: 9 dimensions (1–5, 7–8, 10–11)
**Fossilized**: 13 dimensions (F1–F13)
**Summary**: Wave 155k — **ALL CODE SHIPPED. ZERO P0/P1s.** Depot 14/14 REBUILT.
biomeOS v4.47 NUCLEUS orchestrator + bearDog crypto.sign DEPLOYED on sporeGate.
Provenance 7/7 UNBLOCKED. 12 teams STANDBY. D7 (Compositions) has no blocking code items —
all remaining work is deployment + validation. Cross-platform expansion: steamGate NEXT,
darwinGate + iosGate GLACIAL (silicon deism obligations). D10 REOPENED for J9–J13 pipeline
automation. 9 active dimensions, 13 fossilized. ~63K+ tests. 10+ gates (3 new planned).

---

*Last used*: Wave 155k (Jul 30, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 155i (F13 — Jelly Strings J1–J8)
*Latest reopen*: Wave 155k (D10 — Jelly Strings J9–J13)
