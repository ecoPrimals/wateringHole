# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

**Fossilization**: Dimensions that are fully complete with no open items graduate
to the FOSSILIZED section. They are not re-checked unless a regression signal
appears. This keeps the active review focused on evolving concerns.

---

# ACTIVE DIMENSIONS

## 1. Temporal / Coordination

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 155a)
- [x] Gate heads published (`heads/*.toml`) — eastGate, sporeGate, flockGate, ironGate, golgiBody
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses: 0 (26+ fossilized)
- [x] ecosystem_manifest.toml version current (v3.1.0)
- [x] 43/43 repos synced with Forgejo
- [x] Active handoffs: 1 (postPrimordial 5-gate enrollment)
- [x] Fossilized: 42+ docs across `fossilRecord/wave150x_*` and `wave151a_completion/`
- [x] **waterFall** publish cascade defined — git → impulse → DAG → braid → anchor → relay
- [x] **Impulse/Potential** standard active (Wave 63+)
- [x] **Context Braid** standard active (Wave 63+)
- [x] **Ecosystem Communication** standard active (Wave 68+)
- [x] NeuralBridge in membrane-shadow routes with try-primal-first semantics
- [x] Glacial correction (150x): git merge divergence documented as rootPulse evidence
- [x] **whitePaper gen/ review COMPLETE** (Wave 151c) — gen0-gen5, waterFall, RootPulse, subGen assessed
- [x] **JOSS publication strategy** defined — Gonzales NF pipeline as live system paper
- [x] **Autonomous enrollment blurb** — ECOSYSTEM_BLURB.md updated with gate-enroll.sh workflow + trust tiers
- [ ] GLOSSARY.md stale (Wave 138b) — needs refresh to 155a terms
- [ ] waterFall graph partially wired — full composition pending Provenance Trio
- [ ] Context braids not yet replacing blurb paste — graduation path documented
- [ ] `freshness.toml` stale at Wave 137 — needs cascade publish to 155a
- [ ] 5 enrolling gates have no published heads in `heads/*.toml`

## 2. Ecological (Primal Health)

- [x] All primals compile — all 4 depot architectures
- [x] Zero P0/P1 blockers in any primal
- [x] 43/43 repos Forgejo-first
- [x] **75,199 `#[test]` attrs in primals alone** — ecosystem-wide 100K+
- [x] Zero TODO/FIXME/HACK in project code — 15/15 primals clean (re-verified Wave 155a)
- [x] nestGate vendor elimination COMPLETE (Wave 150u)
- [x] Production `.unwrap()` — 0 in nestGate, loamSpine, toadStool, esotericWebb, cellMembrane, songBird
- [x] `unsafe` scoped to GPU primals, science FFI, and crypto
- [x] Format drift RESOLVED — all repos clean
- [x] bearDog: Wave 155a, **11,993 tests**, FIDO2 hardware + enrollment attestation, beacon proximity proof, iOS Secure Enclave, HSM agnostic, BTSP defense-in-depth
- [x] songBird: **10,335 tests**, `mesh.gate_enroll` endpoint shipped, crypto delegation **6/6 COMPLETE**, dynamic IP pool allocation
- [x] skunkBat: spawn-rate anomaly detection, cipher floor policy, now PUBLIC
- [x] cellMembrane: Phase 7 wired (gate.enroll → mesh.enroll via HMAC proof), builder identity, multi-target harvest, staleness alarm
- [x] **nestGate: BTSP ClientHello SHIPPED** — 9,617 tests, 7-step outbound handshake, Nest Atomic P1 blocker RESOLVED
- [x] **petalTongue: BTSP ClientHello SHIPPED** — 5,812 tests, outbound connections wired
- [x] **toadStool**: 17,614 tests — largest primal test surface
- [x] primalSpring: **197 scenarios**, all PASS
- [x] Tower debt: 36 → **1** (grapheneGate HSM only)
- [x] `enrollment-replay` RESOLVED
- [x] songBird crypto delegation to bearDog: **6/6 seams DONE** (JWT, checkpoint, auth)
- [x] **BTSP 13/13** — all primals shipped ClientHello (Wave 151d)
- [x] **Cargo.toml metadata** — homepage + documentation standardized across all primals
- [ ] **1 known debt finding**: grapheneGate-readiness (HSM not on eastGate)
- [ ] Chimera Phase 0: library extraction (UNBLOCKED — crypto delegation done)

## 3. Hardware / Topology

- [x] Mixed 10G + 1G topology LIVE — 10G backbone between houses, 1G MikroTik for LAN
- [x] sporeGate on R45 → MikroTik — intra-membrane coordinator, HPC, build authority
- [x] eastGate on MikroTik LAN — code hub, LAN peer at 192.168.4.244 (0.17ms RTT)
- [x] 7-gate WireGuard mesh LIVE (golgi, sporeGate, eastGate, flockGate, ironGate, northGate, grapheneGate)
- [x] northGate enrolled (10.13.37.8, Windows 11, RTX 5090, WireGuard active)
- [x] grapheneGate Tower LIVE (bearDog + songBird + skunkBat)
- [x] Tower Atomic shadow ACTIVE on 3 gates — 700+ shadow samples
- [x] LAN peering: **Tower 353x LAN** (0.45ms vs 158ms WG overlay)
- [x] **Depot: 28 binaries × 2 architectures** (x86_64 + aarch64), all fresh Jul 25
- [x] aarch64 cross-compile working — zero source changes, zero build failures
- [x] **5 gates back online** via RustDesk (strand, west, blue, swift, south) — Wave 109-114, ~40 waves behind
- [x] **Autonomous enrollment SHIPPED** — `mesh.gate_enroll` endpoint on golgiBody + `gate-enroll.sh` client
- [x] **Dynamic IP pool allocation** — .20-.254 range, scanned from `wg show wg0 allowed-ips`
- [x] **Forgejo SSH key auto-registration** — REST API via enrollment endpoint
- [x] **Family seed delivery** — encrypted to enrollee WG pubkey via bearDog
- [x] **Trust tiers** — FIDO2/SoloKey (kin) > grapheneGate beacon (sibling) > token (extended)

### Gate Fleet — Enrollment & Use-Case Matrix

| Gate | Status | Mesh IP | Role / Capacity | golgiBody Update Path |
|------|--------|---------|-----------------|----------------------|
| golgiBody | ONLINE | 10.13.37.1 | Hub, enrollment authority, Forgejo, Drawbridge | Self (publisher) |
| sporeGate | ONLINE | 10.13.37.2 | HPC build, depot authority, intra-membrane coord | WG mesh → Forgejo pull |
| eastGate | ONLINE | 10.13.37.3 | Code hub, overwatch, LAN peer | WG mesh → Forgejo pull |
| ironGate | ONLINE | 10.13.37.5 | JupyterHub, outer membrane, springs host | WG mesh → Forgejo pull |
| flockGate | ONLINE | 10.13.37.6 | Nest Atomic Phase 0 validation | WG mesh → Forgejo pull |
| northGate | ONLINE | 10.13.37.8 | Windows 11, RTX 5090, GPU compute | WG mesh → Forgejo pull |
| grapheneGate | ONLINE | 10.13.37.7 | Android, Tower LIVE, beacon seed source | WG mesh → Forgejo pull |
| strandGate | ENROLLING | .20-.254 | Dual EPYC 7452, 256GB, RTX 3090 — bioinformatics compute. Tower Atomic workhouse. RJ45→Omada + RJ45→Flint2 | `gate-enroll.sh --compose compute` → mesh → Forgejo |
| westGate | ENROLLING | .20-.254 | 76TB ZFS NAS — NestGate CAS backend, outer membrane exposed for WAN. Omada 10G | `gate-enroll.sh --compose nest` → mesh → Forgejo |
| blueGate | ENROLLING | .20-.254 | Distributed builder (sporeGate foreman), media/gaming, Tower Atomic workhouse. Flint2 2.5G | `gate-enroll.sh --compose tower` → mesh → Forgejo |
| swiftGate | ENROLLING | .20-.254 | Hobby/consumer (like northGate), full NUCLEUS, gaming/desktop. Flint2 2.5G | `gate-enroll.sh --compose full` → mesh → Forgejo |
| southGate | ENROLLING | .20-.254 | House2 full NUCLEUS — second sovereign site. Omada 10G | `gate-enroll.sh --compose full` → mesh → Forgejo |

### Post-Enrollment Convergence Path

Once a gate completes `gate-enroll.sh`, it has WG mesh + Forgejo SSH + family seed. Convergence:
1. `git clone git@forgejo:eco/<repo>.git` for all 43+ repos via mesh
2. `cargo build --release` per primal using depot or source
3. Run `springs/primalSpring` to validate local build
4. Publish head to `wateringHole/heads/<gate>.toml`
5. Gate online — receives wave updates via temporal cascade from golgiBody

### Remaining Hardware Items

- [ ] **5-gate fleet enrollment** — endpoint live on golgiBody (Wave 155a), scripts staged at `membrane.primals.eco/depot/enroll/`, execution via RustDesk pending
- [ ] strandGate: Tower Atomic workhouse — bearDog + songBird + skunkBat + compute workloads
- [ ] blueGate: Distributed builder under sporeGate foreman (Node Atomic pattern). Media/gaming services
- [ ] westGate: Nest composition — 76TB ZFS NAS, outer membrane, WAN mesh
- [ ] swiftGate: Full NUCLEUS hobby computer — gaming/desktop/family
- [ ] westGate: cold storage — NestGate CAS backend, 76TB ZFS for ecosystem archive
- [ ] blueGate: profile and role assignment pending
- [ ] swiftGate: profile and role assignment pending
- [ ] southGate: house2 full NUCLEUS — second sovereign site
- [ ] grapheneGate → standalone Android platform (P1, eastGate validates HSM then full NUCLEUS deploy)
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
- [x] Tower P1 Hardening FULLY SHIPPED
- [x] **6/6 exploration domains PROVEN LIVE**
- [x] **Genetic enrollment** — two-layer trust (mito gate + nuclear lineage)
- [x] **BTSP defense-in-depth** — `BEARDOG_UDS_REQUIRE_BTSP=1` on local sockets
- [x] **Depot provenance** — builder=sporeGate, staleness alarm, multi-target
- [x] **Crypto delegation** — songBird delegates all crypto to bearDog, chimera unblocked
- [x] **BTSP 13/13** — all primals enforce BTSP ClientHello on outbound connections
- [x] **Autonomous enrollment** — K-Derm inward escalation: extracellular → cytoplasm via physical proof
- [x] **FIDO2 enrollment attestation** — bearDog `fido2.attest_enrollment` + `verify_attestation` on trust roster
- [x] **Beacon proximity proof** — grapheneGate BLE/NFC seed exchange → enrollment proof chain
- [x] **Forgejo API auto-provisioning** — SSH key registration via `mesh.gate_enroll`
- [x] **Family seed encrypted delivery** — bearDog `crypto.encrypt` to enrollee WG pubkey
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

- [x] Blurb reflects current wave (155a) — autonomous enrollment documented
- [x] Active handoffs: 1 (postPrimordial 5-gate enrollment execution)
- [x] Active impulses: 0
- [x] wateringHole standards: 37 active in 4 directories
- [x] Standards reorganized: foundations/ (9), protocols/ (10), operations/ (12), compositions/ (6)
- [x] **42+ docs fossilized** across `wave150x_*` and `wave151a_completion/` (9 docs this pass)
- [x] Team startup blurb template issued
- [x] **whitePaper GEN_REVIEW_151c.md** — full generational arc assessment (gen0-gen5 + siblings)
- [x] **gen5/thesis/JOSS_PUBLICATION.md** — JOSS strategy for Gonzales NF live system
- [x] **gen5/README.md** — updated to Wave 151c, tideGlass added, JOSS track, status current
- [x] **gen5/products/NF_CASE_STUDY.md** — tideGlass Thread 0 reconciled, infrastructure section added
- [x] **gate-enroll.sh** documented — self-enrolling client + trust tier table in blurb
- [ ] GLOSSARY.md needs refresh (Wave 138b → 155a terms)
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

## F9. BTSP Sub-Wave + Publication Strategy (fossilized Wave 151d)

BTSP sub-wave (151b–151d) fully resolved. All 13 primals shipped ClientHello:

- **Wave 151b**: 9 primals shipped BTSP (songBird, barraCuda, coralReef, loamSpine, rhizoCrypt, skunkBat, sweetGrass, cellMembrane, toadStool)
- **Wave 151c**: squirrel + biomeOS shipped from eastGate. grapheneGate validated (10/13, HSM blocked). sporePrint SEO shipped. ironGate back online.
- **Wave 151d**: nestGate BTSP ClientHello (P1 Nest Atomic blocker RESOLVED — 1,630 tests, 7-step handshake). petalTongue BTSP ClientHello (6,589 tests, outbound wired).
- **Publication strategy**: whitePaper gen/ review COMPLETE. Gonzales NF pipeline defined as gen5 JOSS proof case. JOSS_PUBLICATION.md created. NF_CASE_STUDY.md reconciled with tideGlass. crates.io publishing deferred to sovereignty outer-membrane track.
- **Cargo.toml metadata**: homepage + documentation standardized across all primals.

---

**Active**: 8 dimensions (1–8)
**Fossilized**: 9 dimensions (F1–F9)
**Summary**: All fossilized GREEN. Active: 7 GREEN / 1 AMBER→GREEN (hardware — autonomous enrollment shipped, 5 gates ready for execution, 7 gates fully meshed).

---

*Last used*: Wave 155a (Jul 27, 2026)
*Created*: Wave 139a
*First fossilization*: Wave 150p
*Latest fossilization*: Wave 151d (F9 — BTSP Sub-Wave + Publication Strategy)
