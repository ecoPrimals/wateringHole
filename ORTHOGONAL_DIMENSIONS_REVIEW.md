# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155j)
- [x] Gate heads published (`heads/*.toml`) — golgiBody auto-publishing active
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] 43/43 repos synced with Forgejo
- [x] **ECOSYSTEM_BLURB.md** is the universal handoff (Tracks A+B converged)
- [x] Fossilized: 42+ docs across `fossilRecord/wave150x_*` and `wave151a_completion/`
- [x] **waterFall** publish cascade defined — git → impulse → DAG → braid → anchor → relay
- [x] Impulse/Potential, Context Braid, Ecosystem Communication standards active
- [x] NeuralBridge in membrane-shadow routes with try-primal-first semantics
- [x] whitePaper gen/ review COMPLETE (Wave 151c)
- [x] JOSS publication strategy defined
- [x] GLOSSARY.md refreshed (Wave 155b)
- [x] cellMembrane + plasmidBin cascaded to Forgejo
- [x] **30+ handoff docs + AARs** delivered Wave 155f–i (code teams, gate AARs, Nest Atomic, composition broker, deep debt sweeps, Windows deployment)
- [ ] waterFall graph partially wired — full composition pending Provenance Trio
- [ ] Context braids not yet replacing blurb paste — graduation path documented
- [x] `freshness.toml` updated to Wave 155h with 38 HEAD SHAs
- [x] **Nest Atomic LIVE on westGate** — 8 services, Provenance Trio 6/7 live, ZFS online
- [x] sweetGrass G3 E2E validated (v0.8.0, 1,636 tests, mock loamSpine UDS)
- [x] westGate CAS on ZFS verified — 3,216 objects, 25.3TB pool, 1.50× compression, ARC 99.98% hit
- [x] P0 glibc depot FIXED. P1 WG DNS FIXED. P1 membrane depot REBUILT (J6).
- [x] **Deep debt wave**: 8 primals shipped simultaneous sweeps (nestGate, toadStool, cellMembrane, barraCuda, coralReef, sweetGrass, skunkBat, nestGate)
- [x] sporeGate depot refresh: Linux 19/19 binaries, BLAKE3 verified, health 5/11→9/11
- [x] strandGate Compute Trio rebuilt from glibc source, RTX 3090 profiled
- [x] ~~biomeOS composition broker~~ — **SHIPPED** (v4.45): riboCipher framing + BTSP executor, 35 E2E tests, 8,564 tests total
- [x] **blueGate Tower G1 COMPLETE** — 3/3 primals on Windows (source build, 3m 56s)
- [x] **blueGate Nest Atomic VALIDATED** — 10/10 primals on Windows, 107.6 MB, TCP-only
- [x] **westGate composition broker LIVE** — biomeOS v4.45 deployed, 704 capabilities, COORDINATED mode, E2E routing proven
- [x] songBird 3 follow-up Windows compile fixes shipped (`d9bda555`)
- [x] cellMembrane 45+ magic numbers centralized to `constants.rs` (1,221 tests)
- [x] strandGate **Node Atomic VALIDATED** — 450 methods, 746 pipelines/sec, sub-ms GPU dispatch
- [x] barraCuda RTX 3090 + RX 6950 XT dual-GPU validated — FHE bit-perfect, cdist 65× SciPy
- [x] toadStool S346 deep evolution + deployment docs (9,193+ tests, doctor CLI fixed)
- [x] **strandGate NUCLEUS ACHIEVED** — first full NUCLEUS (8/9 healthy, 1,742 caps, 674 IPC methods, sub-ms GPU)
- [x] **blueGate 13/13 on Windows** — infrastructure proof, 147 MB, 2+ hours stable
- [x] sporeGate Windows depot rebuilt — **11/14 fresh** (3 blocked on code-team platform gates)
- [x] sweetGrass braid_id→UUID mismatch FIXED (`4b5167b`)
- [x] cellMembrane boot_order enforcement SHIPPED (b7707ee) — systemd `After=` deps from `CompositionSpec`
- [x] loamSpine `--bind` alias for biomeOS CLI standardization
- [x] rhizoCrypt cross-compile hygiene — 4 targets, zero warnings, `--bind` alias
- [x] coralReef Windows cross-compilation — zero errors/warnings on `x86_64-pc-windows-gnu`
- [x] barraCuda `MultiDevicePool` wired into primal startup (`device.pool` IPC method)
- [x] sporeGate DNS/DHCP topology fixes (dnsmasq, DHCP DNS option, `sporegate.primals.local`)
- [ ] 2 enrolling gates have no published heads in `heads/*.toml`
- [ ] **Windows depot 3/14 stale** — bearDog, toadStool, coralReef need platform gating fixes
- [ ] **Windows CI gate** — `cargo check --target x86_64-pc-windows-gnu` not yet in CI
- [ ] **biomeOS composition lifecycle** — boot_order shipped but biomeOS doesn't consume it yet
- [ ] **DNS manifest/generator gap** — topology drifts from manifest (sporeGate AAR)

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
- [x] bearDog: 11,993 tests, FIDO2 hardware, beacon proximity, HSM agnostic
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
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)
- [ ] bearDog `crypto.sign_ed25519` returns health stub — blocks Provenance Trio 7/7 live on westGate

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
| westGate | **BROKER LIVE** | Linux | 10.13.37.11 | nest (8) | biomeOS v4.45 COORDINATED, 704 caps, 3,216 CAS objects. **Add Compute Trio → second NUCLEUS.** |
| blueGate | **13/13 WINDOWS** | Windows | 10.13.37.12 | **NUCLEUS infra** | **13/13 primals, 147 MB, TCP-only, 2+ hours stable. Awaiting biomeOS orchestration. STANDBY.** |
| swiftGate | HW READY | Windows | enrolling | tower (3) | Second Windows proof (after blueGate) |
| southGate | HW READY | Linux | enrolling | full (13) | House2 sovereign site |

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
| **Nest Atomic** (7+Tower) | LIVE | westGate (ZFS+CAS), blueGate (Windows) | Signal graphs: 9. Capability routing: YES. Graph execution: P1 (riboCipher). |
| **Node Atomic** (3+Tower) | VALIDATED | strandGate (746 pipelines/sec, sub-ms GPU) | Signal graphs: 3. |
| **NUCLEUS** (13) | **ACHIEVED** | **strandGate** (8/9, 1,742 caps, 674 methods), **blueGate** (13/13, infra proof) | 27 signal graphs. Lifecycle: NOT YET (manual startup). |

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

### Path to NUCLEUS

- [ ] **biomeOS graph executor riboCipher fix** — one-line (`send_ribocipher_jsonrpc_request()`). Blocks orchestrated graph execution across compositions.
- [ ] **biomeOS socket unification** — `biomeos/` vs `membrane/` split causes symlink workarounds
- [ ] **biomeOS socket evaporation** — Neural API restart wipes capabilities, sockets disappear
- [ ] **biomeOS full composition lifecycle** — startup ordering, health gating, composition transitions (Tower→Nest→Node→NUCLEUS) managed by biomeOS, not shell scripts
- [ ] **bearDog `crypto.sign_ed25519`** — real signing (blocks Provenance Trio 7/7, blocks Nest Atomic full E2E)
- [x] ~~**Node Atomic live**~~ — strandGate VALIDATED (746 pipelines/sec)
- [x] ~~**NUCLEUS live on one gate**~~ — **strandGate ACHIEVED** (8/9, 1,742 caps, manual startup). blueGate 13/13 infra proof.
- [ ] **NUCLEUS lifecycle** — biomeOS auto-startup via boot_order + health gates (cellMembrane shipped boot_order, biomeOS must consume)
- [ ] **Chimera Phase 0**: shared library extraction (`libtower.so`) — UNBLOCKED, deferred
- [ ] sporePrint primal pipeline: replace Zola
- [ ] 6 springs pending `validation.json`
- [ ] **Primal CLI flag standardization** — inconsistent bind flags across Nest primals (--bind vs --host vs --bind-address vs --http-port)

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
- [x] ~~Windows genomeBins stale~~ — **11/14 fresh** (sporeGate rebuilt Wave 155j). 3 blocked on code-team platform gates.
- [x] ~~**songBird Windows platform gate (P0)**~~ — **FIXED + IN DEPOT** (`d9bda555`, 21.3 MB)
- [ ] **3 Windows binaries blocked**: beardog.exe (UnixStream), toadstool.exe (GPU module), coralreef.exe (unix_jsonrpc)
- [ ] **No Windows CI gate** — `cargo check --target x86_64-pc-windows-gnu` would catch platform gates
- [ ] macOS genomeBins — check-pass only, no linker for cross-build from Linux
- [ ] `target`/`bind_mode` field removal — primals auto-detect, depot negotiates
- [ ] systemd abstraction for Windows Service / launchd paths (cellMembrane `InitSystem` foundation shipped)

## ~~9. Documentation / Fossil Record~~ → **FOSSILIZED as F11** (Wave 155h)

ALL ITEMS RESOLVED. Moved to Fossilized section below.

## ~~10. Jelly Strings — Deployment Automation~~ → **FOSSILIZED as F13** (Wave 155i)

Manual deployment loops → primal-native automation: **ACHIEVED**. Moved to Fossilized section below.

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

**Active**: 8 dimensions (1–5, 7–8, 11)
**Fossilized**: 13 dimensions (F1–F13)
**Summary**: Wave 155j — **NUCLEUS ACHIEVED** on strandGate (first gate: 8/9 healthy,
1,742 caps, 674 IPC methods, sub-ms GPU). blueGate 13/13 on Windows (147 MB, infra proof).
Windows depot 11/14 fresh. sweetGrass P2 UUID fixed. cellMembrane boot_order shipped.
**Remaining**: biomeOS composition lifecycle (consume boot_order, riboCipher graph executor,
socket fixes), bearDog `crypto.sign_ed25519` (Provenance 7/7), 3 Windows platform gates
(bearDog, toadStool, coralReef), DNS manifest generators. 7 teams STANDBY, 5 ACTIVE.
8 active dimensions, 13 fossilized. ~63K+ tests. 10 gates.

---

*Last used*: Wave 155i (Jul 29, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 155i (F13 — Jelly Strings)
