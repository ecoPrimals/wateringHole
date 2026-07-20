# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

---

## 1. Temporal

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 150o)
- [x] Gate heads published (`heads/*.toml`) — all active gates have recent timestamps
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses triaged — 0 active, 26+ fossilized
- [x] No stale diverge impulses older than 2 waves
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] Active handoffs minimal: 4 (blurb, E2E standard, template, ABG guide)
- [x] 8 fossilized handoffs in `handoffs/fossils/`
- [x] 14 fossilized AARs in `aars/fossils/` (6 moved from handoffs/fossils/ Wave 150o)

## 2. Ecological (Primal Health)

- [x] All primals compile (`cargo check` / `cargo test` green) — all 4 depot arch
- [x] Zero P1 blockers in any primal
- [x] All primal repos converged across remotes (43/43 Forgejo-first)
- [x] Transport injection adopted across all non-exempt primals
- [x] Neural API methods shipped by all primal teams
- [x] Test counts stable and increasing (100,000+ `#[test]` attrs — Wave 150o audit)
- [x] Phase 2 abstraction COMPLETE 14/14 — transport layer fully abstracted
- [x] Silicon Atheism Phase 2 transport 14/14 COMPLETE
- [x] CAC 6/6 COMPLETE
- [x] Glacial Shift 8/8 ALL CLEAR
- [x] Dimensional review sweep COMPLETE — 43 repos scored (Wave 150o)
- [x] GAP-036 socket naming closed ecosystem-wide
- [x] GAP-038 stale UDS cleanup closed ecosystem-wide
- [x] Zero debt markers in 39/43 repos (0 TODO/FIXME/HACK)
- [ ] TODO/FIXME markers: nestGate (27), bingoCube (5), fossilRecord (3), rustChip (1)
- [x] Format drift RESOLVED (biomeOS, petalTongue, squirrel — all clean, Wave 150k)
- [x] Forgejo-first remote swap COMPLETE — 43/43 repos origin=Forgejo (Wave 150k)
- [x] `unsafe` scoped to GPU primals (barraCuda 326, toadStool 384), science (wetSpring 389), crypto (bingoCube 146, petalTongue 353)

## 3. Hardware / Topology

- [x] `ecosystem_manifest.toml` reflects current physical state
- [x] 5-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] All 5 active WG peers have handshakes within 2 minutes (Jul 20)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] USB enrollment bundle staged for southGate (10.13.37.9)
- [x] gate-usb-bootstrap.sh + enroll/ bundle + stage_usb.sh --enroll
- [ ] esotericWebb process down on flockGate (webb.primals.eco 502)
- [ ] westGate OFFLINE (cold storage, 76TB ZFS — not blocking)
- [ ] fieldGate OFFLINE (dead CMOS — hardware surgery needed)
- [ ] strandGate enrollment pending (dual EPYC 7452, 256GB, RTX 3090)
- [ ] biomeGate OFFLINE (kernel recovery)
- [ ] southGate pending USB enrollment

## 4. Sovereignty / Membranes

- [x] K-Derm three-layer model intact (cytoplasm → periplasm → outer membrane)
- [x] Forgejo sovereign inner membrane operational (git.primals.eco:2222)
- [x] Forgejo-first remote standard COMPLETE — 43/43 repos origin=Forgejo
- [x] gate.enroll automates membrane-correct enrollment (7-phase, fully automated)
- [x] Sovereign outer membrane operational (Caddy TLS, bearDog ACME)
- [x] Inner membrane zero-commercial (primal.eco data path)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [x] DNSSEC enabled on sovereign domains — `primal.eco` + `nestgate.io`
- [ ] DNSSEC on `primals.eco` — not enabled (P2, enable via Cloudflare)
- [ ] primal.eco inner membrane separation (P2)

## 5. Depot / Build Pipeline

- [x] Depot authority operational (sporeGate + eastGate — build authorities)
- [x] ecoBins built as musl-static stripped (post-primordial standard)
- [x] 59+ depot binaries, BLAKE3 + Ed25519 signed, VPS depot serving
- [x] `require-signed` enforced system-wide
- [x] SIGN-VERIFY-ON-FETCH operational in cellMembrane
- [x] All 4 depot architectures: x86_64-musl(16) + aarch64-musl(16) + android(13) + windows(14)
- [x] Depot layout consistent across depot authority and relay mirrors
- [x] `plasmid.harvest` → `plasmid.fetch` pipeline tested end-to-end
- [x] `depot_sync --push` operational (builder → VPS)
- [x] lithoSpore ring dependency dropped — zero C/asm in ecoBin pipeline
- [x] nestgate binary path fixed in plasmidBin depot (Wave 150n)

## 6. Website / Public Surface / Security

- [x] `sporeprint.primals.eco` returning 200 (266ms — Jul 20)
- [x] `footprint.primals.eco` returning 200 (332ms — Jul 20)
- [x] `live.primals.eco` returning 200 (463ms — Jul 20)
- [x] `lab.primals.eco` returning 401 (257ms — auth expected, Jul 20)
- [x] `git.primals.eco` returning 200 (291ms — Jul 20)
- [ ] `webb.primals.eco` returning 502 (300ms — esotericWebb process down, Jul 20)
- [x] Subdomain standard formalized: `prefix.primals.eco` REQUIRED
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options, X-Content-Type)
- [x] fail2ban active on SSH endpoints
- [x] Rate limiting configured
- [x] TLS certificates auto-renewing (ACME / Let's Encrypt)
- [x] sporePrint `live` maturity level shipped

## 7. Glacial Shift

- [x] All 8 glacial criteria assessed — ALL CLEAR (since Wave 137b)
- [x] No regression on previously cleared criteria
- [ ] SHOW_HN readiness rubric updated

## 8. Compositions / Products / Live Services

- [x] footPrint LIVE at `footprint.primals.eco` — 478 TS test cases, responsive
- [ ] esotericWebb process down on flockGate — 502 (needs restart)
- [x] lithoSpore ALL CLEAR — USB round-trip validated, 229 tests
- [x] pseudoSpore pipeline — 7 springs emitted (6 pending validation.json)
- [ ] tideGlass — shelved (empty scaffold)
- [x] Drawbridge weak bond registrations current
- [x] protoKarya projects registered in manifest (footPrint + tideGlass)
- [x] JupyterHub LIVE on ironGate (lab.primals.eco)
- [ ] projectFOUNDATION — not started

## 9. Documentation / Fossil Record

- [x] Blurb reflects current wave scope and status (Wave 150o)
- [x] Stale handoffs fossilized (8 in handoffs/fossils/)
- [x] AARs in canonical location (14 in aars/fossils/ — 6 moved Wave 150o)
- [x] Active handoffs minimal: 4 (blurb, E2E standard, template, ABG guide)
- [x] Active AARs: 0 (all fossilized)
- [x] Active impulses: 0
- [x] Team startup blurb template created
- [x] wateringHole standards stable (~49 standards documents)
- [x] Orthogonal Dimensions Review checklist current (this file)

## 10. Cascade Pipeline / Convergence

- [x] `membrane temporal.cascade` runs without hanging
- [x] All repo remotes converged — 43/43 Forgejo-first (Wave 150k)
- [x] No cyclic divergence in freshness records (tree hashes since Wave 138c)
- [x] Forgejo push mirrors operational (43/43 repos, sync_on_commit)
- [x] WaterFall sync pattern formalized (Forgejo-first K-Derm relay chain)
- [x] gate.enroll automates Forgejo-first remote setup for new gates
- [ ] songBird BTSP → gate.enroll integration (P1 — last enrollment primitive)

## 11. Content-Addressed Convergence (CAC — ALL 6 LAYERS COMPLETE)

- [x] L1: Git repos — tree hashes in freshness.toml
- [x] L2: Depot binaries — BLAKE3 diff in depot_sync --push
- [x] L3: Heads metadata — TreeParity for auto-publish
- [x] L4: Impulses — content-hash deduplication
- [x] L5: rhizoCrypt — SessionTreeHash primitive SHIPPED
- [x] L6: Cascade divergence — tree-parity before policy dispatch
- [x] Pattern formalized in whitePaper/gen5/foundations/
- [ ] primalSpring: content-addressed-convergence scenario (FRAGO issued)

## 12. Architecture / OS Parity (Silicon Atheism)

### Phase 1: Cross-Compile (COMPLETE — Wave 142a)
- [x] 14/14 primals compile for all 4 depot architectures

### Phase 2: Abstraction Over Gating (COMPLETE — Wave 145a, 14/14 Transport)
- [x] Transport: all 14 primals ship trait-based transport abstraction
- [x] Device discovery: toadStool glowplug Vulkan backend
- [x] Platform lifecycle: petalTongue `PlatformLifecycle` trait
- [ ] Credential store: trait-based (bearDog authority + squirrel cache) — partially done
- [ ] Health monitoring: trait-based (not procfs-hardcoded) — P2
- [ ] Subsystem convergence: `primal-transport` crate publication — P2

---

*Last used*: Wave 150o (Jul 20, 2026)
*Created*: Wave 139a
