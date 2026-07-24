# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 150x)
- [x] Gate heads published (`heads/*.toml`)
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] Active handoffs: 6 (150w–150x era, post-fossilization)
- [x] Active AARs: 6 (150w)
- [x] 3 analysis docs (150w–150x: data analysis, composition map, chimera design)
- [x] 43/43 repos synced with Forgejo
- [x] Fossilized: 24 in `fossilRecord/wave150x_cleanup/`, 21 in `aars/fossils/`
- [ ] GLOSSARY.md stale (Wave 138b) — needs refresh to 150x terms

## 2. Ecological (Primal Health)

- [x] All primals compile — all 4 depot architectures
- [x] Zero P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] 100,000+ `#[test]` attrs across ecosystem (Wave 150o audit)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean (Wave 150q)
- [x] nestGate vendor elimination COMPLETE (Wave 150u) — vendor/ removed
- [x] Production `.unwrap()` — 0 prod unwraps confirmed: nestGate, loamSpine, toadStool, esotericWebb, cellMembrane (150u)
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] songBird: 14,322+ tests, zero clippy warnings, zero unsafe (150x)
- [x] bearDog: enrollment replay protection shipped (150x)
- [x] skunkBat: spawn-rate anomaly detection shipped (150x)
- [x] cellMembrane: crash-loop breaker shipped (150x)
- [x] primalSpring: **196 scenarios**, all PASS, 30 known debt findings
- [ ] Production `.unwrap()` — remaining primals need `clippy::unwrap_used` audit

## 3. Hardware / Topology

- [x] Mixed 10G + 1G topology LIVE — 10G backbone between houses/large compute, 1G via MikroTik for LAN gates
- [x] sporeGate on R45 → MikroTik — intra-membrane coordinator, golgiBody WAN liaison
- [x] eastGate on MikroTik LAN — code hub, LAN peer at 192.168.4.244 (0.17ms RTT)
- [x] 5-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] USB enrollment bundle staged for southGate (10.13.37.9)
- [x] gate-usb-bootstrap.sh + enroll/ bundle operational
- [x] Tower Atomic shadow ACTIVE on 3 gates (sporeGate, flockGate, golgiBody)
- [x] LAN peering confirmed (sporeGate ↔ eastGate via MikroTik, 0.17ms)
- [ ] southGate pending USB enrollment (house2, full NUCLEUS)
- [ ] strandGate enrollment pending (dual EPYC 7452, 256GB, RTX 3090)
- [ ] westGate OFFLINE (cold storage, 76TB ZFS — not blocking)
- [ ] fieldGate OFFLINE (dead CMOS — hardware surgery)
- [ ] biomeGate OFFLINE (kernel recovery)
- [ ] New gates (friends/family) will use R45 topology — Tower must support

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
- [x] RustDesk confirmed AGPL-3.0 compliant — learn-from-leverage posture
- [x] JupyterHub repositioned: outer membrane interface only, compute = inner membrane primals
- [x] Sovereign depot auto-build pipeline DELIVERED (4 phases — Wave 150w)
- [x] Crash-loop breaker — cellMembrane self-recovery for systemd storms (Wave 150x)
- [x] Tower Atomic PHASE 1 PASS — exceeds WG on WAN throughput, LAN latency, jitter (150w)
- [x] Tower Atomic P1 Hardening FULLY SHIPPED (9/9 tasks — 150x)
- [ ] **Phase 2: Tower cutover** — shadow mode active, 30 stress/pen findings remaining, chimera design drafted
- [ ] **Phase 1: Zola → primal sporePrint** — petalTongue rendering + nestGate CAS content + cellMembrane serving
- [ ] **Phase 2: Forgejo → rootPulse** — late-stage, post-rootPulse maturity
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
- [x] Tower Atomic pen test scenarios (7) — attack surface mapped, 30 findings tracked
- [ ] Lansing Scuffle public pages pending (sporePrint team blurb issued)

## 6. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition wired
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured
- [x] initioChem wired pseudospore-core as first external consumer
- [x] JupyterHub LIVE on ironGate — outer membrane interface
- [x] pseudoSpore pipeline — 7 springs emitted
- [x] petalTongue WASM WebGL pipeline shipped (Wave 150r) + v1.7.0 deployed (150w)
- [x] Tower Atomic exploration: 1/6 domains PROVEN LIVE, 5/6 structural GREEN
- [ ] sporePrint primal pipeline: replace Zola with petalTongue + nestGate CAS (P2)
- [ ] 6 springs pending `validation.json`
- [ ] tideGlass — shelved (empty scaffold)
- [ ] projectFOUNDATION — not started

## 7. Documentation / Fossil Record

- [x] Blurb reflects current wave (150x)
- [x] Active handoffs: 6 (150w–150x)
- [x] Active AARs: 6 (150w)
- [x] Active analysis docs: 3 (150w–150x)
- [x] Active impulses: 0
- [x] wateringHole standards: 37 active in 4 directories + 4 root docs
- [x] Standards reorganized into foundations/ (9), protocols/ (10), operations/ (12), compositions/ (6) — Wave 150t
- [x] 8 standards fossilized to `fossilRecord/wave150s_standards/`
- [x] Team startup blurb template issued
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
- [ ] sporePrint public pages not yet created (consulting, companies, scuffle, thermal)
- [ ] Building tour / physical access not yet arranged

## 9. Tower Atomic Deep Analysis (NEW — Wave 150x)

- [x] Honest data assessment: latency PROVEN, jitter PROVEN, throughput UNRELIABLE (duration_ms: 0)
- [x] Composition cost map: 12 UDS seams, 4 hops per cross-gate call, IPC 3.5× network on LAN
- [x] 7 stress test scenarios: sustained throughput, concurrent dispatch, BTSP storm, failover, churn, UDS hop cost, shadow fidelity
- [x] 7 pen test scenarios: malformed RPC, enrollment replay, capability escalation, cipher downgrade, UDS spoof, mesh poison, relay abuse
- [x] biomeOS chimera design: 6 requirements, 4-phase migration, performance targets
- [x] All 4 teams converged: 1,838 lines shipped against findings (150x)
- [x] Known debt reduced 36 → 30 in first cascade
- [x] Benchmark harness fixed: `duration_us` + sustained streaming mode
- [x] UDS connection pool shipped (songBird)
- [x] Enrollment replay protection shipped (bearDog)
- [x] federation.broadcast handler shipped (songBird) — gap from composition map resolved
- [x] Crash-loop breaker shipped (cellMembrane) — self-recovery gap resolved
- [x] Spawn-rate anomaly detection shipped (skunkBat)
- [ ] 30 known debt findings across 10 stress/pen scenarios (teams evolving independently)
- [ ] Chimera Phase 0: library extraction (can begin now — pure refactoring)
- [ ] Sustained throughput validation (harness ready, can run on 1G LAN now)

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

---

**Active**: 9 dimensions (1–9)
**Fossilized**: 5 dimensions (F1–F5)
**Summary**: All fossilized dimensions GREEN. Active: 8 GREEN / 1 AMBER (hardware — offline gates).

---

*Last used*: Wave 150x (Jul 24, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
