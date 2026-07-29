# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155i)
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
- [x] **17+ new handoff docs** delivered this wave (code teams + AARs + Nest Atomic + composition broker)
- [ ] waterFall graph partially wired — full composition pending Provenance Trio
- [ ] Context braids not yet replacing blurb paste — graduation path documented
- [x] `freshness.toml` updated to Wave 155h with 38 HEAD SHAs
- [x] **Nest Atomic LIVE on westGate** — 8 services, Provenance Trio CLOSED, ZFS online
- [x] sweetGrass G3 wiring COMPLETE (v0.8.0)
- [x] westGate ZFS 25.4TB + 2TB L2ARC online, all 5 storage tiers operational
- [x] P0 glibc depot FIXED (cellMembrane). P1 WG DNS FIXED.
- [ ] biomeOS composition broker handoff issued — BTSP session propagation needed
- [ ] 3 enrolling gates have no published heads in `heads/*.toml`

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] ~~P0: glibc depot target~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals
- [x] 43/43 repos Forgejo-first
- [x] **~72K+ `#[test]` attrs** in primals (toadStool 23K, songBird 14K+, nestGate 13K, bearDog 12K, biomeOS 8.5K, petalTongue 6.6K, barraCuda 5K, coralReef 3.5K, sweetGrass 1.6K, loamSpine 1.3K, cellMembrane 1.2K)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] nestGate vendor elimination COMPLETE (Wave 150u)
- [x] Production `.unwrap()` — 0 in critical-path primals
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: 11,993 tests, FIDO2 hardware, beacon proximity, HSM agnostic
- [x] songBird: 14,835+ tests, `mesh.gate_enroll`, universal-ipc, J3+J4+J5, `tower.health` facade, **ACME HTTP-01 Phase 1**
- [x] nestGate: **12,973** tests, **P0/P1 audit resolved**, live CLI health, FHS centralized, ZFS tier migration
- [x] toadStool: **23,332** tests, **S344**: deny.toml expanded, overstep reduced, socket centralized
- [x] rhizoCrypt: 1,456 tests, BTSP→DAG bridge, cross-gate provenance chain
- [x] loamSpine: **1,739** tests, **BTSP handshake dedup**: `verify_and_negotiate()` + `AsyncErrorSender`. **155i**: registry drift fixed — `certificate.verify/lifecycle/history` discoverable
- [x] sweetGrass: **1,625** tests, **v0.8.0**, **G3 wiring COMPLETE** — `LedgerClient`, `braid.commit` → loamSpine, ledger proof. Provenance Trio CLOSED
- [x] petalTongue: **6,605** tests, **topology→runtime manifest**, main.rs split, geometry module
- [x] squirrel: **763** tests, **capability purification**: beardog→security_provider, adapter IPC
- [x] barraCuda: **4,957** tests, **SIGSEGV fixed** (GPU_TEST_GUARD), BTSP env races, dead code (-1,200L)
- [x] coralReef: **3,527** tests, **18/18 JSON-RPC dispatch**, BTSP Phase 3 encrypted transport
- [x] primalSpring: 197 scenarios, all PASS, calibrated for 13-gate mesh
- [x] skunkBat: spawn-rate anomaly detection, `ConnectivityAnomaly` (9th threat), frame crypto, PUBLIC
- [x] **BTSP 13/13** — all primals shipped ClientHello
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: 6/6 seams DONE
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [x] **cellMembrane**: **1,223** tests, **J6 CLOSED**, **J8 code shipped**, **P0 glibc FIXED**, **P1 WG DNS FIXED**
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)
- [ ] nestGate: ghost methods `content.repo.*`/`content.mirror.*` — implement or remove (P2)

## 3. Hardware / Physical Topology

- [x] Mixed 10G + 1G topology LIVE — 10G AOC backbone between houses, MikroTik CRS310 + Omada SX3008F
- [x] sporeGate on R45 → MikroTik — plasma membrane router (NAT/DHCP/DNS/nftables)
- [x] eastGate on MikroTik LAN — code hub, 10G SFP+ direct
- [x] northGate enrolled (Windows 11, RTX 5090, 2.5G ethernet)
- [x] westGate ONLINE — AMD Ryzen 7 5700X / 64GB DDR4 / 2TB NVMe / 5×14TB HDD raw (NOT i7-4771, NOT ZFS pooled)
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
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090, G1 validation target |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | **TOWER+COMPUTE LIVE** | Linux | 10.13.37.10 | compute (7) | Dual EPYC 7452, RTX 3090, GPU verified, P0 glibc needed |
| westGate | **TOWER LIVE** | Linux | 10.13.37.11 | nest (7) | AMD Ryzen 7 5700X, 64GB, 2TB NVMe, 5×14TB raw |
| blueGate | HW READY | Windows | enrolling | tower (3) | Distributed builder, **peptidoglycan anchor H2** |
| swiftGate | HW READY | Windows | enrolling | full (13) | Hobby/consumer, house2 |
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
│  Status: 9-gate mesh, Tower Atomic LIVE on 5+ gates      │
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

- [x] **9-gate WireGuard mesh** — golgi, sporeGate, eastGate, flockGate, ironGate, northGate, grapheneGate, westGate, strandGate
- [x] Tower Atomic shadow active — westGate + strandGate LIVE
- [x] LAN peering: Tower 353x LAN (0.45ms vs 158ms WG overlay)
- [x] songBird universal-ipc: UDS/named pipes/abstract sockets/TCP
- [x] BTSP defense-in-depth: 13/13 primals
- [x] **biomeOS neuralAPI**: **27** signal graphs, 19 atomic translations, platform_native transport. **1,704 capabilities auto-discovered on westGate.**
- [x] **songBird ACME HTTP-01** challenge responder shipped — Phase 1 TLS elimination
- [x] songBird mesh refactor: enrollment crypto + mesh helpers extracted, all files <800L
- [ ] **biomeOS BTSP session propagation** — signal graph executor needs BTSP handshakes when dispatching to primals that require auth (P0, handoff issued)
- [ ] **biomeOS riboCipher transport** — CLI tools lack `[0xEC, 0x01]` framing (P0)
- [ ] Only 2 WG peers active in practice (enrollment pending for house2 gates)
- [ ] WireGuard DNS catch-all in wg0 template hijacks all resolution (strandGate AAR)

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
- [ ] Phase 2: Forgejo → rootPulse — via Nest Atomic (AFTER Tower stable)
- [ ] `primal.eco` inner membrane separation (P2)

## 6. Public Surface / Security

- [x] 6/6 surfaces healthy (sporeprint, footprint, live, webb, lab, git)
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options)
- [x] fail2ban + rate limiting active
- [x] TLS auto-renewing (ACME)
- [x] Tower pen test: 7 scenarios, all PASS, 0 remaining findings
- [x] sporePrint transplant DONE + credibility audit
- [x] External claim convergence standard issued
- [ ] sporePrint ongoing: 5 impulses for maturity badges

## 7. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] petalTongue WASM WebGL pipeline shipped + v1.7.0 deployed
- [x] Tower Atomic: 6/6 exploration domains PROVEN, chimera Phase 0 unblocked
- [x] songBird crypto delegation 6/6 COMPLETE — composition model validated
- [x] Composition profiles fixed: `compute` = Tower + node, `nest` = Tower + provenance trio
- [x] `tower-builder` profile created for distributed build mesh nodes
- [x] **biomeOS neuralAPI**: Tower (8), Node (3), Nest (**9**) signal graphs with semantic dispatch. **1,704 capabilities auto-discovered on westGate.**
- [ ] **biomeOS composition broker** — needs BTSP session propagation for multi-composition deployments (P0)
- [ ] **Chimera Phase 0**: shared library extraction (`libtower.so`) — UNBLOCKED
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
- [x] coralReef 18/18 JSON-RPC dispatch complete (10 compile errors fixed, BTSP Phase 3)
- [x] ~~P0 glibc~~ — **FIXED** (cellMembrane `8d9bb58`): `targets_for_primal()` auto-appends gnu for GPU primals. Depot rebuild needed on sporeGate.
- [ ] J8: Key enrollment portal — code shipped, deployment pending
- [x] Pure Rust across all primals — zero C deps on critical path
- [x] toadStool wgpu cross-platform GPU (DX12/Vulkan/Metal)
- [x] biomeOS platform_native transport on all 27 signal graphs
- [x] biomeOS cross-platform socket templates (named pipes + TCP fallback)
- [ ] Windows genomeBins not yet in golgiBody depot (cross-compile needed)
- [ ] macOS genomeBins — check-pass only, no linker for cross-build from Linux
- [ ] `target`/`bind_mode` field removal — primals auto-detect, depot negotiates
- [ ] systemd abstraction for Windows Service / launchd paths (cellMembrane `InitSystem` foundation shipped)

## ~~9. Documentation / Fossil Record~~ → **FOSSILIZED as F11** (Wave 155h)

ALL ITEMS RESOLVED. Moved to Fossilized section below.

## 10. Jelly Strings — Deployment Automation (NEW — extracted from sporeGate AAR)

From sporeGate deployment AAR. These block "operator runs shell loops" →
"gates self-heal via cascade":

- [x] **J1: Harvest** — CLOSED. Was already Rust. `--push` flag added (`8a71345`)
- [x] **J2: Depot push** — CLOSED. `plasmid.push` first-class + Rust depot_sync (`8a71345`)
- [x] **J3: Service restart** — CLOSED. songBird `deploy.hot_swap` (`d4bffbbd`)
- [x] **J4: Caddy config** — CLOSED. songBird route self-config via `route.rs` (`d4bffbbd`)
- [x] **J5: WG peer reg** — HARDENED. songBird WG peer management (`d4bffbbd`)
- [x] **J6: systemd overrides** — **CLOSED**. `gate.configure` + `gate.apply` shipped (`c66a56e`). Init system dispatch: systemd/launchd/bare.
- [ ] **J7: Legacy service detection** — OPEN. One-time, low priority (cellMembrane P3)
- [x] **J8: Key enrollment portal** — **CODE SHIPPED**. step-ca SSH cert lifecycle in cellMembrane (`b13105b`). enroll phase 8 (`ssh_cert`). Non-fatal if CA not deployed. **Deployment pending** — sporeGate needs step-ca on golgiBody.

7/8 resolved. J6 CLOSED (gate.configure/apply). J8 code shipped (step-ca lifecycle),
deployment pending. **Near-fossilization**: only J7 (legacy detection, P3) remains.
Once step-ca is deployed on golgiBody, J8 graduates from "code shipped" to "CLOSED".

## 11. Campus / Physical Infrastructure

- [x] Lansing Scuffle vision documented (10 docs, 120K+ in whitePaper/lansingScuffle/)
- [x] Property profile: 1305 S Cedar St, 464K SF, 8 MW, 600-ton HVAC
- [x] Economics model: 5 revenue stages, SBA 504 math, AGPL consulting
- [x] K-Derm zone mapping applied to building floors
- [x] Thermal sovereignty loop designed
- [x] footPrint GeoJSON location added
- [x] sporePrint transplant + credibility audit DONE
- [ ] sporePrint ongoing: 5 impulses
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
- 11+ new handoff docs from Wave 155f–h code teams

---

**Active**: 10 dimensions (1–8, 10–11)
**Fossilized**: 11 dimensions (F1–F11)
**Summary**: Orthogonal review at Wave 155i. Nest Atomic LIVE on westGate — first
multi-composition (8 services, 1,704 capabilities auto-discovered). Provenance Trio
CLOSED (sweetGrass G3 v0.8.0). ZFS 25.4TB + L2ARC online, all 5 tiers. P0 glibc
FIXED. P1 WG DNS FIXED. NEW P0: biomeOS needs BTSP session propagation in signal
graph executor for composition broker pattern. 27 signal graphs. ~72K+ tests.

---

*Last used*: Wave 155i (Jul 29, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 155h (F11 — Documentation / Fossil Record)
