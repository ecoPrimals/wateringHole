# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 151a)
- [x] Gate heads published (`heads/*.toml`)
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] 43/43 repos synced with Forgejo
- [x] Active handoffs: 4, Active AARs: 1, Active analysis: 1
- [x] Fossilized: 42 docs across `fossilRecord/wave150x_*` and `wave151a_completion/`
- [x] **waterFall** publish cascade defined — git → impulse → DAG → braid → anchor → relay
- [x] **Impulse/Potential** standard active (Wave 63+)
- [x] **Context Braid** standard active (Wave 63+)
- [x] **Ecosystem Communication** standard active (Wave 68+)
- [x] NeuralBridge in membrane-shadow routes with try-primal-first semantics
- [x] Glacial correction (150x): git merge divergence documented as rootPulse evidence
- [ ] GLOSSARY.md stale (Wave 138b) — needs refresh to 151a terms
- [ ] waterFall graph partially wired — full composition pending Provenance Trio
- [ ] Context braids not yet replacing blurb paste — graduation path documented

## 2. Ecological (Primal Health)

- [x] All primals compile — all 4 depot architectures
- [x] Zero P0/P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] 100,000+ `#[test]` attrs across ecosystem
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean
- [x] nestGate vendor elimination COMPLETE (Wave 150u)
- [x] Production `.unwrap()` — 0 in nestGate, loamSpine, toadStool, esotericWebb, cellMembrane, songBird
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: 13,973+ tests, genetic enrollment, cipher floor, blake3, BTSP defense-in-depth, enrollment decomposition (7 modules)
- [x] songBird: 14,332+ tests, crypto delegation **6/6 COMPLETE**, retry, health, socket watch, IPC pool, challenge-verify, revocation
- [x] skunkBat: spawn-rate anomaly detection, cipher floor policy, now PUBLIC
- [x] cellMembrane: 1,156 tests, builder identity, multi-target harvest, staleness alarm, crash-loop breaker
- [x] primalSpring: **197 scenarios**, all PASS
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] `enrollment-replay` RESOLVED
- [x] songBird crypto delegation to bearDog: **6/6 seams DONE** (JWT, checkpoint, auth)
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Topology

- [x] Mixed 10G + 1G topology LIVE — 10G backbone between houses, 1G MikroTik for LAN
- [x] sporeGate on R45 → MikroTik — intra-membrane coordinator, HPC, build authority
- [x] eastGate on MikroTik LAN — code hub, LAN peer at 192.168.4.244 (0.17ms RTT)
- [x] 5-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] Tower Atomic shadow ACTIVE on 3 gates — 700+ shadow samples
- [x] LAN peering: **Tower 353x LAN** (0.45ms vs 158ms WG overlay)
- [x] USB enrollment bundle staged (gate-usb-bootstrap.sh + enroll/)
- [x] **Depot: 28 binaries × 2 architectures** (x86_64 + aarch64), all fresh Jul 25
- [x] aarch64 cross-compile working — zero source changes, zero build failures
- [ ] southGate pending USB enrollment (house2, full NUCLEUS)
- [ ] strandGate enrollment pending (dual EPYC 7452, 256GB, RTX 3090)
- [ ] grapheneGate → standalone Android platform (P1, eastGate validates HSM then full NUCLEUS deploy)
- [ ] westGate OFFLINE (cold storage, 76TB ZFS)
- [ ] fieldGate OFFLINE (dead CMOS)
- [ ] biomeGate OFFLINE (kernel recovery)

## 4. Sovereignty / Membranes

- [x] K-Derm three-layer model intact
- [x] Forgejo sovereign inner membrane operational (43/43 repos)
- [x] Push mirrors relay to GitHub on commit
- [x] gate.enroll: 7-phase, fully automated
- [x] Sovereign outer membrane operational (Caddy TLS)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] **DNSSEC 3/3 domains complete**
- [x] Sovereignty Evolution Roadmap formalized
- [x] RustDesk AGPL-3.0 compliant — learn-from-leverage posture
- [x] Sovereign depot auto-build pipeline DELIVERED (4 phases)
- [x] Crash-loop self-recovery LIVE — app breaker + systemd layers
- [x] Tower Atomic EXCEEDS WG (353x LAN, 1.7x WAN)
- [x] Tower P1 Hardening FULLY SHIPPED
- [x] **6/6 exploration domains PROVEN LIVE**
- [x] **Genetic enrollment** — two-layer trust (mito gate + nuclear lineage)
- [x] **BTSP defense-in-depth** — `BEARDOG_UDS_REQUIRE_BTSP=1` on local sockets
- [x] **Depot provenance** — builder=sporeGate, staleness alarm, multi-target
- [x] **Crypto delegation** — songBird delegates all crypto to bearDog, chimera unblocked
- [ ] **Phase 2: Tower cutover** — shadow active, chimera design drafted
- [ ] **Phase 1: Zola → sporePrint primal pipeline**
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
- [ ] sporePrint ongoing: 5 impulses for maturity badges, WGSL, unsafe scope

## 6. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] pseudoSpore pipeline — 7 springs emitted
- [x] petalTongue WASM WebGL pipeline shipped + v1.7.0 deployed
- [x] Tower Atomic: 6/6 exploration domains PROVEN, chimera Phase 0 unblocked
- [x] songBird crypto delegation 6/6 COMPLETE — composition model validated
- [ ] **Chimera Phase 0**: shared library extraction (`libtower.so`) — UNBLOCKED
- [ ] sporePrint primal pipeline: replace Zola
- [ ] 6 springs pending `validation.json`
- [ ] tideGlass — shelved

## 7. Documentation / Fossil Record

- [x] Blurb reflects current wave (151a)
- [x] Active handoffs: 4, Active AARs: 1, Active analysis: 1 (chimera design)
- [x] Active impulses: 0
- [x] wateringHole standards: 37 active in 4 directories
- [x] Standards reorganized: foundations/ (9), protocols/ (10), operations/ (12), compositions/ (6)
- [x] **42+ docs fossilized** across `wave150x_*` and `wave151a_completion/` (9 docs this pass)
- [x] Team startup blurb template issued
- [ ] GLOSSARY.md needs refresh (Wave 138b → 151a terms)
- [ ] PRIMAL_REGISTRY.md needs refresh (Wave 109 → current 15-primal posture)
- [ ] 18 standards with stale wave tags (headers need bump)

## 8. Campus / Physical Infrastructure

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
14/14 primals on all 4 depot architectures.

## F4. Depot / Build Pipeline (fossilized Wave 150p, completed Wave 150n)

59+ binaries, BLAKE3 + Ed25519 signed, 4 architectures, `require-signed` enforced.
Sovereign CI hooks deployed to 29 repos on golgiBody.

## F5. Cascade Pipeline / Convergence (fossilized Wave 150p, completed Wave 150k)

43/43 repos converged on Forgejo-first. Push mirrors relay to GitHub.

## F6. Tower Atomic Deep Analysis (fossilized Wave 150x, completed Wave 150x)

4-team convergence sprint. Analysis docs and composition map fossilized.
Chimera design remains active analysis (Dim 6). Known debt tracked in Dim 2.

## F7. sporePrint Transplant (fossilized Wave 150x, completed Wave 150x)

Transplant shipped (b985c22), credibility audit landed (f3b710d).
External claim convergence standard established.

## F8. Tower Atomic Completion + Depot Convergence (fossilized Wave 151a)

Tower Atomic sprint (150v–151a) fully resolved. All P0/P1 items closed:

- Tower debt: 36 → 1 (grapheneGate HSM only, hardware-gated)
- 7/7 final debt items: retry, health, socket watch, pool, BTSP strict, announce validation, revocation
- bearDog: enrollment decomposition (1,061L → 7 modules), BTSP defense-in-depth, dns_timeout fix
- songBird: crypto delegation 6/6 COMPLETE (JWT, checkpoint, auth), capability propagation
- Depot divergence P0 RESOLVED: 28 binaries × 2 arch, provenance fresh, builder=sporeGate
- cellMembrane: builder identity, multi-target harvest, staleness alarm
- 9 docs fossilized to `wave151a_completion/`

---

**Active**: 8 dimensions (1–8)
**Fossilized**: 8 dimensions (F1–F8)
**Summary**: All fossilized GREEN. Active: 7 GREEN / 1 AMBER (hardware — offline gates).

---

*Last used*: Wave 151a (Jul 25, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 151a (F8 — Tower Completion + Depot)
