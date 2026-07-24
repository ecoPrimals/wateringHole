# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 150x)
- [x] Gate heads published (`heads/*.toml`)
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] 43/43 repos synced with Forgejo
- [x] Active handoffs: 7 (150w–150x), Active AARs: 4 (150w–150x), Active analysis: 3
- [x] Fossilized: 24 in `fossilRecord/wave150x_cleanup/`, 26 in `aars/fossils/`
- [x] **waterFall** publish cascade defined (`graphs/waterfall_publish.toml`) — git → impulse → DAG → braid → anchor → relay
- [x] **Impulse/Potential** standard active (Wave 63+) — TOML FRAGOs, auto-discovered via cascade
- [x] **Context Braid** standard active (Wave 63+) — structured developer state, TTL auto-decay
- [x] **Ecosystem Communication** standard active (Wave 68+) — three-artifact model (handoffs/FRAGOs/blurbs)
- [x] NeuralBridge in membrane-shadow routes with try-primal-first semantics
- [x] Glacial correction (150x): git merge divergence documented as rootPulse evidence
- [ ] GLOSSARY.md stale (Wave 138b) — needs refresh to 150x terms
- [ ] waterFall graph partially wired — full primal composition pending Provenance Trio maturity
- [ ] Context braids not yet replacing blurb paste in practice — graduation path documented

## 2. Ecological (Primal Health)

- [x] All primals compile — all 4 depot architectures
- [x] Zero P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] 100,000+ `#[test]` attrs across ecosystem (Wave 150o audit)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean (Wave 150q)
- [x] nestGate vendor elimination COMPLETE (Wave 150u) — vendor/ removed
- [x] Production `.unwrap()` — 0 prod unwraps confirmed: nestGate, loamSpine, toadStool, esotericWebb, cellMembrane
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: 13,937 tests, enrollment replay protection, UDS connection cap (150x)
- [x] songBird: 14,322+ tests, UDS connection pool, federation.broadcast, sustained benchmark (150x)
- [x] skunkBat: spawn-rate anomaly detection (150x)
- [x] cellMembrane: crash-loop breaker + systemd hardening — `Restart=always` eliminated ecosystem-wide (150x)
- [x] primalSpring: **196 scenarios**, all PASS
- [ ] **30 known debt findings** across 10 stress/pen scenarios — teams evolve independently
- [ ] Production `.unwrap()` — remaining primals need `clippy::unwrap_used` audit
- [ ] Chimera Phase 0: library extraction (pure refactoring, can begin now)

## 3. Hardware / Topology

- [x] Mixed 10G + 1G topology LIVE and DONE — 10G backbone between houses, 1G MikroTik for LAN
- [x] sporeGate on R45 → MikroTik — intra-membrane coordinator, HPC interface, build authority
- [x] eastGate on MikroTik LAN — code hub, LAN peer at 192.168.4.244 (0.17ms RTT)
- [x] 5-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] Tower Atomic shadow ACTIVE on 3 gates (sporeGate, flockGate, golgiBody)
- [x] LAN peering confirmed (sporeGate ↔ eastGate, 0.17ms ICMP, 0.72ms Tower)
- [x] USB enrollment bundle staged (gate-usb-bootstrap.sh + enroll/)
- [x] New gates (friends/family) will use R45 — Tower handles mixed 1G/10G routing
- [ ] southGate pending USB enrollment (house2, full NUCLEUS)
- [ ] strandGate enrollment pending (dual EPYC 7452, 256GB, RTX 3090)
- [ ] westGate OFFLINE (cold storage, 76TB ZFS — not blocking)
- [ ] fieldGate OFFLINE (dead CMOS — hardware surgery)
- [ ] biomeGate OFFLINE (kernel recovery)

## 4. Sovereignty / Membranes

- [x] K-Derm three-layer model intact
- [x] Forgejo sovereign inner membrane operational (43/43 repos)
- [x] Push mirrors relay to GitHub on commit
- [x] gate.enroll: 7-phase, fully automated
- [x] Sovereign outer membrane operational (Caddy TLS)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] **DNSSEC 3/3 domains complete** (`primal.eco`, `nestgate.io`, `primals.eco`)
- [x] Sovereignty Evolution Roadmap formalized in Diderm doc (Wave 150s)
- [x] Three-tier classification: Replace / Late-Stage / Firebreak
- [x] RustDesk AGPL-3.0 compliant — learn-from-leverage posture
- [x] Sovereign depot auto-build pipeline DELIVERED (4 phases — Wave 150w)
- [x] Crash-loop self-recovery LIVE — application (breaker) + systemd (StartLimitBurst) layers
- [x] Tower Atomic PHASE 1 PASS — EXCEEDS WG (1.56x LAN throughput, 1.11x WAN)
- [x] Tower P1 Hardening FULLY SHIPPED (9/9 tasks — 150x)
- [x] **6/6 exploration domains PROVEN LIVE** (capability routing, multi-stack, large data, secure compute, distributed, edge/SFF)
- [ ] **Phase 2: Tower cutover** — shadow active, 30 findings remaining, chimera design drafted
- [ ] **Phase 1: Zola → sporePrint primal pipeline** — petalTongue + nestGate CAS + cellMembrane
- [ ] **Phase 2: Forgejo → rootPulse** — DAG + linear + attribution over nestGate CAS + Provenance Trio
- [ ] `primal.eco` inner membrane separation (P2)

## 5. Public Surface / Security

- [x] `sporeprint.primals.eco` — 200
- [x] `footprint.primals.eco` — 200
- [x] `live.primals.eco` — 200
- [x] `webb.primals.eco` — 200
- [x] `lab.primals.eco` — 401 (auth expected)
- [x] `git.primals.eco` — 200
- [x] 6/6 surfaces healthy
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options)
- [x] fail2ban + rate limiting active
- [x] TLS auto-renewing (ACME)
- [x] Tower pen test: 7 scenarios, attack surface mapped, 30 findings tracked
- [x] sporePrint transplant guidance issued (Wave 150x) — Tower Atomic, topology, sovereign CI
- [ ] sporePrint primals.eco update pending (team handed off)

## 6. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition wired
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] initioChem wired pseudospore-core as first external consumer
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] pseudoSpore pipeline — 7 springs emitted
- [x] petalTongue WASM WebGL pipeline shipped (150r) + v1.7.0 deployed (150w)
- [x] Tower Atomic: **6/6 exploration domains PROVEN LIVE** — exceeds WG structurally
- [ ] sporePrint primal pipeline: replace Zola (petalTongue + nestGate CAS + cellMembrane)
- [ ] 6 springs pending `validation.json`
- [ ] tideGlass — shelved (empty scaffold)
- [ ] projectFOUNDATION — not started

## 7. Documentation / Fossil Record

- [x] Blurb reflects current wave (150x) — glacial correction framing
- [x] Active handoffs: 7 (150w–150x)
- [x] Active AARs: 4 (150w–150x)
- [x] Active analysis docs: 3 (150w–150x)
- [x] Active impulses: 0
- [x] wateringHole standards: 37 active in 4 directories + 4 root docs
- [x] Standards reorganized: foundations/ (9), protocols/ (10), operations/ (12), compositions/ (6)
- [x] 8 standards fossilized to `fossilRecord/wave150s_standards/`
- [x] Team startup blurb template issued
- [x] Wave 150x fossil pass: 24 handoffs + 26 AARs archived
- [ ] GLOSSARY.md needs refresh (Wave 138b → 150x terms)
- [ ] PRIMAL_REGISTRY.md needs refresh (Wave 109 → current 15-primal posture)
- [ ] 18 standards with stale wave tags (evergreen content, headers need bump)

## 8. Campus / Physical Infrastructure (Wave 150p)

- [x] Lansing Scuffle vision documented (10 docs, 120K+ in whitePaper/lansingScuffle/)
- [x] Property profile: 1305 S Cedar St, 464K SF, 8 MW, 600-ton HVAC
- [x] Economics model: 5 revenue stages, SBA 504 math, AGPL consulting
- [x] K-Derm zone mapping applied to building floors
- [x] Thermal sovereignty loop designed (solar → compute → heat → water → gardens)
- [x] footPrint GeoJSON location added (John Bean Building)
- [x] sporePrint team blurb issued (4 new pages + 4 updates)
- [ ] sporePrint public pages pending (team handed off with transplant guidance)
- [ ] Building tour / physical access not yet arranged

---

# FOSSILIZED DIMENSIONS

*These dimensions are fully complete. No open items. Not re-checked unless
a regression signal appears. Each entry records the wave it was fossilized
and the key evidence of completion.*

## F1. Glacial Shift (fossilized Wave 150p, completed Wave 137b)

All 8 glacial criteria assessed — ALL CLEAR since Wave 137b. No regression
in 13+ waves. The ecosystem has proven it is not fragile.

- 8/8 criteria cleared
- No regression through Waves 137b–150x
- GLACIAL_SHIFT_READINESS.md in fossilRecord

## F2. Content-Addressed Convergence (fossilized Wave 150p, completed Wave 143b)

ALL 6 LAYERS COMPLETE. The architectural pattern is fully solved.

- L1–L6 complete, documented in whitePaper

## F3. Silicon Atheism (fossilized Wave 150p, completed Wave 145a)

Phase 1 (cross-compile) and Phase 2 (transport abstraction) COMPLETE.
14/14 primals on all 4 depot architectures.

## F4. Depot / Build Pipeline (fossilized Wave 150p, completed Wave 150n)

Fully operational. Sovereign auto-build pipeline (Wave 150w) extends this.

- 59+ binaries, BLAKE3 + Ed25519 signed
- 4 architectures, `require-signed` enforced
- Sovereign CI hooks deployed to 29 repos on golgiBody

## F5. Cascade Pipeline / Convergence (fossilized Wave 150p, completed Wave 150k)

43/43 repos converged on Forgejo-first. Push mirrors relay to GitHub.

## F6. Tower Atomic Deep Analysis (fossilized Wave 150x, completed Wave 150x)

4-team convergence sprint shipped all analysis and hardening tasks.
Remaining 30 debt findings tracked in Dim 2 (Ecological). Chimera evolution
tracked in Dim 4 (Sovereignty). This dimension captured the investigation;
the ongoing work lives in existing dimensions.

- Honest data assessment: latency/jitter PROVEN, throughput harness FIXED
- Composition cost map: 12 UDS seams, IPC 3.5× network on LAN
- 14 new stress/pen scenarios (196 total), all PASS
- biomeOS chimera design: 6 requirements, 4-phase migration
- All 4 teams converged: 1,838 lines across 57 files
- Known debt reduced 36 → 30
- bearDog: replay protection + UDS cap
- songBird: connection pool + federation.broadcast + sustained benchmark
- cellMembrane: crash-loop breaker + systemd hardening
- skunkBat: spawn-rate anomaly detection

---

**Active**: 8 dimensions (1–8)
**Fossilized**: 6 dimensions (F1–F6)
**Summary**: All fossilized dimensions GREEN. Active: 7 GREEN / 1 AMBER (hardware — offline gates).

---

*Last used*: Wave 150x (Jul 24, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 150x (F6 — Tower Atomic Deep Analysis)
