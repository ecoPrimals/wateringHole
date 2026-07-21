# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 150s)
- [x] Gate heads published (`heads/*.toml`)
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] Active handoffs: 5 (blurb, E2E standard, template, ABG guide, Lansing Scuffle blurb)
- [x] 8 fossilized handoffs, 14 fossilized AARs (canonical locations)
- [x] 43/43 repos synced with Forgejo (Jul 20 cascade)

## 2. Ecological (Primal Health)

- [x] All primals compile — all 4 depot architectures
- [x] Zero P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] 100,000+ `#[test]` attrs across ecosystem (Wave 150o audit)
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean (Wave 150q)
- [x] nestGate: 27 markers are ALL vendored upstream (`vendor/rustls-webpki` × 20, `vendor/rustls-rustcrypto` × 7)
- [x] Vendor root cause: `rustls-rustcrypto 0.0.2-alpha` pins webpki 0.102.x; need 0.103.12+ for RUSTSEC; ring stripped for Silicon Atheism
- [x] bingoCube (5), fossilRecord (3), rustChip (1) — minor, tracked (9 project TODOs total)
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] nestGate: deep unwrap audit complete (Session 121 — 0 prod unwrap)
- [ ] nestGate vendor elimination: un-vendor when upstream `rustls-rustcrypto` ships past `0.0.2-alpha` with webpki ≥ 0.103.12 and no `ring` dep
- [ ] Production `.unwrap()` hotspots — ecosystem-wide counts high (broader grep). Top: barraCuda (5,446), biomeOS (4,165), songBird (4,068), toadStool (3,657)

## 3. Hardware / Topology

- [x] 5-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] USB enrollment bundle staged for southGate (10.13.37.9)
- [x] gate-usb-bootstrap.sh + enroll/ bundle operational
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
- [x] DNSSEC on `primal.eco` + `nestgate.io`
- [x] DNSSEC on `primals.eco` — DS record at Porkbun (keyTag 2371, alg 13, SHA-256), AD=true validated Jul 21
- [x] **DNSSEC 3/3 domains complete** — all validated via Google DNS (AD=true)
- [x] Sovereignty Evolution Roadmap formalized in Diderm doc (Wave 150s)
- [x] Three-tier classification: Replace / Late-Stage / Firebreak
- [x] RustDesk confirmed AGPL-3.0 compliant — learn-from-leverage posture
- [x] JupyterHub repositioned: outer membrane interface only, compute = inner membrane primals
- [ ] **Phase 1: WireGuard → Tower Atomic** — Tower (bearDog + songBird + skunkBat) must meet/exceed WG performance. Parity benchmark needed.
- [ ] **Phase 1: Zola → primal sporePrint** — petalTongue rendering + nestGate CAS content + cellMembrane serving. WASM WebGL pipeline enables.
- [ ] **Phase 2: Forgejo → rootPulse** — sovereign version control over nestGate CAS + Provenance Trio. Late-stage, post-rootPulse.
- [ ] `primal.eco` inner membrane separation (P2)

## 5. Public Surface / Security

- [x] `sporeprint.primals.eco` — 200 (Jul 20)
- [x] `footprint.primals.eco` — 200 (Jul 20)
- [x] `live.primals.eco` — 200 (Jul 20)
- [x] `webb.primals.eco` — **200** (recovered — was 502 earlier Jul 20)
- [x] `lab.primals.eco` — 401 (auth expected)
- [x] `git.primals.eco` — 200 (Jul 20)
- [x] 6/6 surfaces healthy
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options)
- [x] fail2ban + rate limiting active
- [x] TLS auto-renewing (ACME)
- [ ] Lansing Scuffle public pages pending (sporePrint team blurb issued)

## 6. Compositions / Products

- [x] footPrint LIVE — 478 TS test cases, FULL NUCLEUS composition wired
- [x] esotericWebb LIVE — V22, 472 tests, scene binding fixed (recovered from 502)
- [x] lithoSpore ALL CLEAR — 235 tests, pseudoSpore pipeline matured (spore-status, populate-validation, promote-spore)
- [x] initioChem wired pseudospore-core as first external consumer
- [x] JupyterHub LIVE on ironGate — repositioned as outer membrane interface (ABG users), compute = inner membrane
- [x] pseudoSpore pipeline — 7 springs emitted
- [x] petalTongue WASM WebGL pipeline shipped (Wave 150r) — enables sporePrint primal replacement
- [ ] sporePrint primal pipeline: replace Zola with petalTongue + nestGate CAS + cellMembrane (Phase 1)
- [ ] 6 springs pending `validation.json`
- [ ] tideGlass — shelved (empty scaffold)
- [ ] projectFOUNDATION — not started

## 7. Documentation / Fossil Record

- [x] Blurb reflects current wave (150s)
- [x] Active handoffs: 5 (all current and actionable)
- [x] Active AARs: 0 (all fossilized)
- [x] Active impulses: 0
- [x] wateringHole standards stable (~49 documents)
- [x] Team startup blurb template issued
- [x] Lansing Scuffle blurb issued for sporePrint team
- [x] AARs in canonical `aars/fossils/` (housekeeping complete Wave 150o)

## 8. Campus / Physical Infrastructure (NEW — Wave 150p)

- [x] Lansing Scuffle vision documented (10 docs, 120K+ in whitePaper/lansingScuffle/)
- [x] Property profile: 1305 S Cedar St, 464K SF, 8 MW, 600-ton HVAC
- [x] Economics model: 5 revenue stages, SBA 504 math, AGPL consulting
- [x] K-Derm zone mapping applied to building floors
- [x] Thermal sovereignty loop designed (solar → compute → heat → water → gardens)
- [x] footPrint GeoJSON location added (John Bean Building)
- [x] sporePrint team blurb issued (4 new pages + 4 updates)
- [ ] sporePrint public pages not yet created (consulting, companies, scuffle, thermal)
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
- No regression through Waves 137b–150p
- GLACIAL_SHIFT_READINESS.md in fossilRecord
- *Remaining*: SHOW_HN readiness rubric is a strategic planning item, not a glacial concern

## F2. Content-Addressed Convergence (fossilized Wave 150p, completed Wave 143b)

ALL 6 LAYERS COMPLETE. The architectural pattern is fully solved and
formalized in whitePaper/gen5/foundations/.

- L1: Git repos — tree hashes in freshness.toml
- L2: Depot binaries — BLAKE3 diff in depot_sync
- L3: Heads metadata — TreeParity for auto-publish
- L4: Impulses — content-hash deduplication
- L5: rhizoCrypt SessionTreeHash — SHIPPED
- L6: Cascade divergence — tree-parity before policy dispatch
- Pattern documented in whitePaper
- *Remaining*: primalSpring scenario (validation exercise, not a gap)

## F3. Silicon Atheism (fossilized Wave 150p, completed Wave 145a)

Phase 1 (cross-compile) and Phase 2 (transport abstraction) COMPLETE.
14/14 primals on all 4 depot architectures. Transport trait-based everywhere.

- Phase 1: 14/14 primals cross-compile (Wave 142a)
- Phase 2: 14/14 transport abstraction (Wave 145a)
- Device discovery: toadStool glowplug Vulkan
- Platform lifecycle: petalTongue trait
- lithoSpore: zero C/asm in pipeline
- *Evolving edges* (tracked in Dim 2, not blocking):
  - Credential store trait (bearDog + squirrel) — partially done
  - Health monitoring trait — P2
  - `primal-transport` crate publication — P2

## F4. Depot / Build Pipeline (fossilized Wave 150p, completed Wave 150n)

Fully operational. All items cleared. No open issues.

- Depot authority: sporeGate + eastGate
- 59+ binaries, BLAKE3 + Ed25519 signed
- 4 architectures: x86_64-musl, aarch64-musl, android, windows
- `require-signed` enforced system-wide
- SIGN-VERIFY-ON-FETCH operational
- `plasmid.harvest` → `plasmid.fetch` end-to-end
- `depot_sync --push` operational
- nestgate depot path fixed (Wave 150n)
- USB staging with --enroll flag operational

## F5. Cascade Pipeline / Convergence (fossilized Wave 150p, completed Wave 150k)

43/43 repos converged on Forgejo-first. Push mirrors relay to GitHub.
No cyclic divergence. WaterFall sync pattern formalized.

- 43/43 repos Forgejo-first (Wave 150k)
- Push mirrors: sync_on_commit (Wave 150j)
- No cyclic divergence (tree hashes since Wave 138c)
- `membrane temporal.cascade` operational
- gate.enroll automates Forgejo-first setup
- *Evolving edge*: songBird BTSP → gate.enroll integration (P1 — tracked in Dim 4)

---

**Active**: 8 dimensions (1–8)
**Fossilized**: 5 dimensions (F1–F5)
**Summary**: All fossilized dimensions GREEN. Active: 7 GREEN / 1 AMBER (hardware).

---

*Last used*: Wave 150s (Jul 21, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
