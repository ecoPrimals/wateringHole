# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155b)
- [x] Gate heads published (`heads/*.toml`) — eastGate, sporeGate, flockGate, ironGate, golgiBody
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] 43/43 repos synced with Forgejo
- [x] Active handoffs: Track A (evolution), Track B (fleet convergence), sporeGate build mesh
- [x] Fossilized: 42+ docs across `fossilRecord/wave150x_*` and `wave151a_completion/`
- [x] **waterFall** publish cascade defined — git → impulse → DAG → braid → anchor → relay
- [x] **Impulse/Potential** standard active (Wave 63+)
- [x] **Context Braid** standard active (Wave 63+)
- [x] **Ecosystem Communication** standard active (Wave 68+)
- [x] NeuralBridge in membrane-shadow routes with try-primal-first semantics
- [x] Glacial correction (150x): git merge divergence documented as rootPulse evidence
- [x] **whitePaper gen/ review COMPLETE** (Wave 151c)
- [x] **JOSS publication strategy** defined — Gonzales NF pipeline as live system paper
- [x] **Autonomous enrollment blurb** — ECOSYSTEM_BLURB.md updated with genomeBin convergence posture
- [x] cellMembrane cascaded to Forgejo (Wave 155b)
- [x] plasmidBin cascaded to Forgejo (Wave 155b)
- [ ] GLOSSARY.md stale (Wave 138b) — needs refresh to 155b terms
- [ ] waterFall graph partially wired — full composition pending Provenance Trio
- [ ] Context braids not yet replacing blurb paste — graduation path documented
- [ ] `freshness.toml` stale at Wave 137 — needs cascade publish to 155b
- [ ] 5 enrolling gates have no published heads in `heads/*.toml`

## 2. Ecological (Primal Health)

- [x] All primals compile — 5 Tier 1 genomeBin architectures
- [x] Zero P0/P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] **75,199 `#[test]` attrs in primals alone** — ecosystem-wide 100K+
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] nestGate vendor elimination COMPLETE (Wave 150u)
- [x] Production `.unwrap()` — 0 in nestGate, loamSpine, toadStool, esotericWebb, cellMembrane, songBird
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: **11,993 tests**, FIDO2 hardware, enrollment attestation, beacon proximity, HSM agnostic
- [x] songBird: **10,335 tests**, `mesh.gate_enroll`, universal-ipc (UDS/pipes/abstract/XPC/TCP)
- [x] skunkBat: spawn-rate anomaly detection, cipher floor policy, PUBLIC
- [x] cellMembrane: Phase 7 enrollment, builder identity, checksum verify fix (plain+struct format)
- [x] **nestGate: BTSP ClientHello SHIPPED** — 9,617 tests
- [x] **petalTongue: BTSP ClientHello SHIPPED** — 5,812 tests
- [x] **toadStool**: 17,614 tests — largest primal test surface
- [x] primalSpring: **197 scenarios**, all PASS
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] songBird crypto delegation to bearDog: **6/6 seams DONE**
- [x] **BTSP 13/13** — all primals shipped ClientHello
- [x] Compositions fixed: `compute` and `nest` include Tower Atomic base primals
- [x] Checksum verify handles both plain-string and struct TOML formats
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Topology

- [x] Mixed 10G + 1G topology LIVE — 10G backbone between houses, 1G MikroTik for LAN
- [x] sporeGate on R45 → MikroTik — intra-membrane coordinator, HPC, build authority
- [x] eastGate on MikroTik LAN — code hub, LAN peer at 192.168.4.244 (0.17ms RTT)
- [x] 7-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate, northGate, grapheneGate)
- [x] northGate enrolled (Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] Tower Atomic shadow ACTIVE on 3 gates — 700+ shadow samples
- [x] LAN peering: **Tower 353x LAN** (0.45ms vs 158ms WG overlay)
- [x] **Autonomous enrollment SHIPPED** — `mesh.gate_enroll` + `gate-enroll.sh` + `gate-enroll.ps1`
- [x] **Dynamic IP pool allocation** — .20-.254 range
- [x] **Forgejo SSH key auto-registration** — REST API via enrollment endpoint
- [x] **Family seed delivery** — encrypted to enrollee WG pubkey via bearDog
- [x] **Trust tiers** — FIDO2/SoloKey (kin) > grapheneGate beacon (sibling) > token (extended)
- [x] **Self-registration pattern** — gates declare name + composition, manifest entries transitional
- [x] westGate ONLINE — 5x14TB HDD (70TB raw ZFS cold pool)
- [x] ironGate HDD — 14TB + 1TB + 1TB + ~2TB, enclave experiment planned
- [x] blueGate + swiftGate identified as **Windows** deployments (`x86_64-pc-windows-gnu`)

### Gate Fleet — Status Matrix

| Gate | Status | Platform | Mesh IP | Composition | Role |
|------|--------|----------|---------|-------------|------|
| golgiBody | ONLINE | Linux | 10.13.37.1 | thin-relay | Sole depot, enrollment, Forgejo, Drawbridge |
| sporeGate | ONLINE | Linux | 10.13.37.2 | full | Build authority, depot, cascade hub |
| eastGate | ONLINE | Linux | 10.13.37.5 | full | Code hub, overwatch |
| ironGate | ONLINE | Linux | 10.13.37.7 | full | GPU compute, 4x HDD enclave, JupyterHub |
| flockGate | ONLINE | Linux | 10.13.37.6 | full | Nest Atomic validation |
| northGate | ONLINE | Windows | 10.13.37.8 | full | RTX 5090, gaming/GPU |
| grapheneGate | ONLINE | Android | 10.13.37.7 | tower | Beacon seed, mobile Tower |
| strandGate | HW READY | Linux | enrolling | compute (7) | Dual EPYC, RTX 3090, bioinformatics |
| westGate | HW READY | Linux | enrolling | nest (7) | 70TB ZFS cold pool, NAS |
| blueGate | HW READY | Windows | enrolling | tower (3) | Distributed builder, media/gaming |
| swiftGate | HW READY | Windows | enrolling | full (13) | Hobby/consumer, house2 |
| southGate | HW READY | Linux | enrolling | full (13) | House2 sovereign site |

### Glacial Goals — Gate Enmeshment

Gates are on, wired, and running. Enmeshment is a glacial validation target requiring:

1. **Tower Atomic deployment** across all platforms (Linux + Windows + Android)
2. **Nest Atomic** for agnostic data systems (same OS abstraction as IPC)
3. **genomeBin depot** on golgiBody with all Tier 1 architectures
4. **Cross-platform validation** — Tower Atomic on Windows (blueGate, swiftGate) proves the abstraction

| Gate | Glacial Milestone | Blocker |
|------|------------------|---------|
| strandGate | Tower Atomic → compute workloads | Enrollment execution |
| westGate | Tower Atomic → Nest Atomic (ZFS CAS) | Enrollment execution |
| blueGate | Tower Atomic on Windows → build authority | Windows genomeBins in depot |
| swiftGate | Full NUCLEUS on Windows | Windows genomeBins in depot |
| southGate | Full NUCLEUS → second sovereign site | Enrollment execution |
| ironGate | HDD enclave model (LUKS per-disk) | Physical HDD installation |
| grapheneGate | Full NUCLEUS on Android | HSM + eastGate validation |

- [ ] fieldGate OFFLINE (dead CMOS)
- [ ] biomeGate OFFLINE (kernel recovery)

## 4. Sovereignty / Membranes

- [x] K-Derm three-layer model intact
- [x] Forgejo sovereign inner membrane operational (43/43 repos)
- [x] Push mirrors relay to GitHub on commit
- [x] gate.enroll: 7-phase, fully automated + Phase 7 mesh.enroll wired
- [x] Sovereign outer membrane operational (Caddy TLS)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] **DNSSEC 3/3 domains complete**
- [x] Sovereignty Evolution Roadmap formalized
- [x] RustDesk AGPL-3.0 compliant — learn-from-leverage posture
- [x] Sovereign depot auto-build pipeline DELIVERED (4 phases)
- [x] Crash-loop self-recovery LIVE — app breaker + systemd layers
- [x] Tower Atomic EXCEEDS WG (353x LAN, 1.7x WAN)
- [x] **6/6 exploration domains PROVEN LIVE**
- [x] **Genetic enrollment** — two-layer trust
- [x] **BTSP defense-in-depth** — `BEARDOG_UDS_REQUIRE_BTSP=1`
- [x] **Depot provenance** — builder=sporeGate, staleness alarm, multi-target
- [x] **Crypto delegation** — songBird → bearDog, chimera unblocked
- [x] **BTSP 13/13**
- [x] **Autonomous enrollment** — K-Derm inward escalation
- [x] **FIDO2 enrollment attestation** + **beacon proximity proof**
- [x] **golgiBody sole depot** — no local depots, all genomeBins served via Caddy TLS
- [ ] **Phase 2: Tower cutover** — shadow active, chimera design drafted
- [ ] **Phase 1: Zola → sporePrint primal pipeline** (crates.io a sub-goal of sovereignty)
- [ ] **Phase 2: Forgejo → rootPulse** — via Nest Atomic
- [ ] `primal.eco` inner membrane separation (P2)

## 5. Public Surface / Security

- [x] 6/6 surfaces healthy (sporeprint, footprint, live, webb, lab, git)
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options)
- [x] fail2ban + rate limiting active
- [x] TLS auto-renewing (ACME)
- [x] Tower pen test: 7 scenarios, all PASS, **0 remaining findings**
- [x] sporePrint transplant DONE + credibility audit
- [x] External claim convergence standard issued
- [ ] sporePrint ongoing: 5 impulses for maturity badges

## 6. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] pseudoSpore pipeline — 7 springs emitted
- [x] petalTongue WASM WebGL pipeline shipped + v1.7.0 deployed
- [x] Tower Atomic: 6/6 exploration domains PROVEN, chimera Phase 0 unblocked
- [x] songBird crypto delegation 6/6 COMPLETE — composition model validated
- [x] Composition profiles fixed: `compute` = Tower + node primals, `nest` = Tower + provenance trio
- [x] `tower-builder` profile created for distributed build mesh nodes
- [ ] **Chimera Phase 0**: shared library extraction (`libtower.so`) — UNBLOCKED
- [ ] sporePrint primal pipeline: replace Zola
- [ ] 6 springs pending `validation.json`

## 7. Documentation / Fossil Record

- [x] Blurb reflects current wave (155b) — genomeBin convergence posture
- [x] Active handoffs: 3 (Track A evolution, Track B fleet, sporeGate build mesh)
- [x] Active impulses: 0
- [x] wateringHole standards: 37 active in 4 directories
- [x] **42+ docs fossilized** across `wave150x_*` and `wave151a_completion/`
- [x] Team startup blurb template issued
- [x] **whitePaper GEN_REVIEW_151c.md** — full generational arc assessment
- [x] **gate-enroll.sh + gate-enroll.ps1** documented
- [ ] GLOSSARY.md needs refresh (Wave 138b → 155b terms)
- [ ] PRIMAL_REGISTRY.md needs refresh (Wave 109 → current 15-primal posture)
- [ ] 18 standards with stale wave tags (headers need bump)

## 8. genomeBin / Cross-Platform Deployment (NEW — extracted from Hardware + Ecological)

- [x] **5 Tier 1 genomeBin targets**: x86_64-linux-musl, aarch64-linux-musl, x86_64-windows-gnu, aarch64-android, armv7-linux-musl
- [x] **8 Tier 3 PROVEN** exotic architectures (Wave 140a AAR — RISC-V, PPC64, s390x, SPARC64, i686, ARM32)
- [x] **songBird universal-ipc**: UDS (Linux), named pipes (Windows), abstract sockets (Android), XPC (iOS), TCP (fallback)
- [x] **cellMembrane `Platform`**: `TargetOs × CpuArch × LinkModel` decomposition with `detect()` at compile time
- [x] **golgiBody sole depot** — all genomeBins served via `https://depot.primals.eco`
- [x] **`bind_mode` and `target` marked transitional** in GateProfile — primals auto-detect
- [x] **PowerShell enrollment** for Windows gates (`gate-enroll.ps1`)
- [x] **Self-registration** — gates declare name + composition, no manifest pre-definition needed
- [x] `deploy_gate.sh` supports `--build-authority` flag
- [x] Pure Rust across all primals — zero C deps on critical path enables all targets
- [ ] **Windows genomeBins** not yet in golgiBody depot — sporeGate needs to cross-compile
- [ ] **macOS genomeBins** — check-pass only, no linker for cross-build from Linux
- [ ] **`target` field removal** — primals auto-detect, depot negotiates by platform
- [ ] **`bind_mode` field removal** — songBird universal-ipc auto-selects transport
- [ ] **Nest Atomic cross-platform data** — NestGate CAS must be OS-agnostic (same as IPC)
- [ ] **systemd abstraction** — cellMembrane `nucleus.rs` needs Windows Service / launchd / init paths
- [ ] **WASM target** — check-pass, no deployed gate yet

## 9. Campus / Physical Infrastructure

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

- songBird `mesh.gate_enroll`: 6-phase pipeline (proof → IP → WG → Forgejo → seed → genetic)
- bearDog FIDO2 enrollment attestation + beacon proximity proof
- cellMembrane Phase 7: gate.enroll → mesh.enroll via HMAC proof
- Dynamic IP pool allocation (.20-.254)
- K-Derm inward escalation: extracellular → cytoplasm via physical proof
- `gate-enroll.sh` (Linux) + `gate-enroll.ps1` (Windows) — self-enrollment clients
- Trust tiers: FIDO2/SoloKey (kin) > beacon proximity (sibling) > token (extended)
- golgiBody drawbridge: Caddy TLS → `/enroll/*` → songBird
- Self-registration: gates declare name + composition, no pre-definition needed

---

**Active**: 9 dimensions (1–9)
**Fossilized**: 10 dimensions (F1–F10)
**Summary**: All fossilized GREEN. Active: 8 GREEN / 1 NEW (genomeBin — cross-platform deployment evolution).
Glacial: gate enmeshment (Tower + Nest Atomic across Linux/Windows/Android).

---

*Last used*: Wave 155b (Jul 27, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 155b (F10 — Autonomous Gate Enrollment)
