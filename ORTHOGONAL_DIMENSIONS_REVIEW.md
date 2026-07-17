# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

---

## 1. Temporal

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 147b)
- [x] Gate heads published (`heads/*.toml`) — all active gates have recent timestamps
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses triaged — 0 active, 26 fossilized
- [x] No stale diverge impulses older than 2 waves
- [x] ecosystem_manifest.toml version current (v3.1.0)

## 2. Ecological (Primal Health)

- [x] All primals compile (`cargo check` / `cargo test` green) — all 4 depot arch
- [x] Zero P1 blockers in any primal
- [x] All primal repos converged across remotes (all synced)
- [x] Transport injection adopted across all non-exempt primals
- [x] Neural API methods shipped by all primal teams
- [x] Test counts stable or increasing (~90,000+ ecosystem-wide)
- [x] Phase 2 abstraction COMPLETE 14/14 — transport layer fully abstracted
- [x] Silicon Atheism Phase 2 transport 14/14 COMPLETE
- [x] CAC 6/6 COMPLETE
- [x] Glacial Shift 8/8 ALL CLEAR

## 3. Hardware / Topology

- [x] `ecosystem_manifest.toml` reflects current physical state
- [x] 6-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate, northGate)
- [x] Gate roles match manifest `[topology]` section
- [x] Network backbone operational (CRS310 10G trunk, MikroTik, switches)
- [ ] RustDesk transient to ironGate + flockGate (intermittent — not blocking)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat, 15/15 depot bins)
- [ ] westGate OFFLINE (cold storage, 76TB ZFS — not blocking)
- [ ] fieldGate OFFLINE (dead CMOS — hardware surgery needed)
- [ ] strandGate enrollment pending (dual EPYC 7452, 256GB, RTX 3090)
- [ ] biomeGate OFFLINE (kernel recovery)

## 4. Sovereignty / Membranes

- [x] K-Derm three-layer model intact (cytoplasm → periplasm → outer membrane)
- [x] Forgejo sovereign inner membrane operational (git.primals.eco:2222)
- [x] Forgejo-first remote standard formalized (origin=Forgejo, github=GitHub)
- [x] gate.enroll automates membrane-correct enrollment (cellMembrane 467560d)
- [x] Sovereign outer membrane operational (Caddy TLS, bearDog ACME)
- [x] Inner membrane zero-commercial (primal.eco data path)
- [x] S1-S4 sovereignty shadows ALL GRADUATED
- [ ] DNSSEC enabled on sovereign domains (P2)
- [ ] primal.eco inner membrane separation (P2)

## 5. Depot / Build Pipeline

- [x] Depot authority operational (sporeGate + eastGate — build authorities)
- [x] ecoBins built as musl-static stripped (post-primordial standard)
- [x] 59 depot binaries, BLAKE3 + Ed25519 signed, VPS depot serving
- [x] `require-signed` enforced system-wide
- [x] SIGN-VERIFY-ON-FETCH operational in cellMembrane
- [x] All 4 depot architectures: x86_64-musl(16) + aarch64-musl(16) + android(13) + windows(14)
- [x] Depot layout consistent across depot authority and relay mirrors
- [x] `plasmid.harvest` → `plasmid.fetch` pipeline tested end-to-end
- [x] `depot_sync --push` operational (builder → VPS)
- [ ] Exotic architectures expanded as adoption completes (riscv64, armv7, s390x validated by songBird)

## 6. Website / Public Surface / Security

- [ ] `primals.eco` root — sporePrint rebuild needed (P0)
- [x] `primals.eco/footprint/` returning 200 (GIS composition LIVE)
- [x] `live.primals.eco` returning 200 (petalTongue TOPO-VIS)
- [x] `lab.primals.eco` returning 200 (JupyterHub on ironGate)
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options, X-Content-Type)
- [x] fail2ban active on SSH endpoints
- [x] Rate limiting configured
- [x] TLS certificates auto-renewing (ACME / Let's Encrypt)
- [x] No new CRITICAL exposures

## 7. Glacial Shift

- [x] All 8 glacial criteria assessed — ALL CLEAR (since Wave 137b)
- [x] No regression on previously cleared criteria
- [x] GLACIAL_SHIFT_READINESS.md trimmed and current
- [ ] SHOW_HN readiness rubric updated

## 8. Compositions / Products / External

- [x] footPrint LIVE at `primals.eco/footprint/` — client operational (174 tests)
- [ ] tideGlass — Phase 0 not started
- [x] Drawbridge weak bond registrations current (songBird 16 bonds)
- [x] protoKarya projects registered in manifest (footPrint + tideGlass)
- [x] Composition routing standard applied
- [ ] primalSpring `protokarya-wan-deploy` scenario (1/5 remaining)
- [ ] footPrint composition wiring: WS_PATH (petalTongue), PROXY_PATH (songBird)
- [x] JupyterHub LIVE on ironGate (lab.primals.eco)

## 9. Documentation / Fossil Record

- [x] Blurb reflects current wave scope and status (Wave 147b)
- [x] Stale handoffs fossilized (25+ handoffs in fossilRecord/)
- [x] Active handoffs minimal: 3 (blurb, ABG guide, protokarya gaps)
- [x] Active impulses: 0
- [x] Team startup blurb template created (TEAM_STARTUP_BLURB_TEMPLATE.md)
- [x] wateringHole standards stable (~30 standards documents)

## 10. Cascade Pipeline / Convergence

- [x] `membrane temporal.cascade` runs without hanging
- [x] All repo remotes converged (primalSpring divergence resolved Wave 147b)
- [x] No cyclic divergence in freshness records (tree hashes since Wave 138c)
- [x] Forgejo mirrors operational (bidirectional repos functional)
- [x] WaterFall sync pattern formalized (Forgejo-first K-Derm relay chain)
- [x] gate.enroll automates Forgejo-first remote setup for new gates

## 11. Content-Addressed Convergence (CAC — ALL 6 LAYERS COMPLETE)

- [x] L1: Git repos — tree hashes in freshness.toml (Wave 138c)
- [x] L2: Depot binaries — BLAKE3 diff in depot_sync --push (Wave 139e)
- [x] L3: Heads metadata — TreeParity for auto-publish (cellMembrane Wave 143b)
- [x] L4: Impulses — content-hash deduplication (cellMembrane f4da0ae, Wave 141b)
- [x] L5: rhizoCrypt — SessionTreeHash primitive SHIPPED (Wave 143b — ce3d534)
- [x] L6: Cascade divergence — tree-parity before policy dispatch (cellMembrane Wave 143b)
- [x] Pattern formalized in whitePaper/gen5/foundations/ (Wave 140a)
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

### Exotic Architectures (validated by songBird, not in depot yet)
- riscv64gc, powerpc64le, powerpc64, s390x, sparc64, arm32, armv7, i686

---

*Last used*: Wave 147b (Jul 17, 2026)
*Created*: Wave 139a
