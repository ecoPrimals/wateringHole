# ecoPrimals Ecosystem Blurb — Wave 155b

**Date**: Jul 27, 2026 10:54 EDT | **Wave**: 155b | **From**: eastGate overwatch
**Posture**: **genomeBin CONVERGENCE. Silicon-deistic deployment: 5 Tier 1 target triples (Linux x86+ARM, Windows, Android, ARM IoT). Tower Atomic IS the OS abstraction layer. golgiBody sole depot. Self-enrollment pattern — gates declare name + composition, everything else intrinsic. Compositions fixed (compute/nest include Tower base). Windows gates (blueGate, swiftGate) + PowerShell enrollment. 13/13 BTSP. 197 scenarios.**

---

## WHERE WE ARE

Waves 150-151 (Tower Atomic + BTSP) **fossilized**. Wave 155a ships autonomous
gate enrollment across three primals (cellMembrane Phase 7, songBird mesh.gate_enroll,
bearDog FIDO2/beacon enrollment attestation). The enrollment system is code-complete
and Forgejo-pushed. Two parallel tracks now active.

| Metric | Value |
|--------|-------|
| Tower vs WireGuard | 353x LAN, 1.7x WAN |
| Scenarios | 197, all PASS |
| Known debt | **2** (grapheneGate provenance stale in git) |
| BTSP primals | **13/13** |
| Primal tests | **75,199** (#[test] in primals alone) |
| genomeBin Tier 1 | **5 targets**: x86_64-linux-musl, aarch64-linux-musl, x86_64-windows-gnu, aarch64-android, armv7-linux-musl |
| Depot | golgiBody sole depot — all genomeBins via Caddy TLS |
| Gates online | **7** (spore, east, iron, flock, golgi, graphene, north) |
| Gates enrolling | **5** (strand, west[Linux], blue[Win], swift[Win], south) |

---

## TWO PARALLEL TRACKS

### Track A: Evolution — Nest Atomic + bearDog Public

Continues the Wave 151 forward momentum. See `BLURB_TRACK_A_EVOLUTION.md`.

**Scope**: Nest Atomic Phase 0, bearDog public flip, Chimera Phase 0 extraction,
Tower cutover shadow analysis, crates.io publishing as sovereignty sub-goal.

### Track B: Fleet Convergence — 5-Gate Enrollment + NUCLEUS Validation

Gets hardware online and validates the postPrimordial deployment system.
See `BLURB_TRACK_B_FLEET_CONVERGENCE.md`.

**Scope**: Complete 5-gate autonomous enrollment, resolve divergences (westGate
mixed-wave repos), validate with benchScale + agentReagents NUCLEUS fleet.
All binaries from golgiBody depot. Tests the membrane and postPrimordial
deployment pipeline end-to-end.

---

## THIS CASCADE — WHAT SHIPPED (Wave 155a)

### Autonomous Gate Enrollment (cellMembrane + songBird + bearDog)

| Component | Change |
|-----------|--------|
| cellMembrane | Phase 7 wired — `gate.enroll` → `mesh.enroll` via HMAC-SHA256 proof |
| songBird | `mesh.gate_enroll` endpoint — 6-phase pipeline (proof → IP → WG → Forgejo → seed → genetic) |
| songBird | Dynamic IP pool allocation (.20-.254 from `wg show wg0 allowed-ips`) |
| bearDog | `fido2.attest_enrollment` + `fido2.verify_attestation` on trust roster |
| bearDog | `beacon.prove_proximity` + `beacon.verify_proximity` for grapheneGate BLE/NFC |
| plasmidBin | `gate-enroll.sh` — standalone client for zero-knowledge self-enrollment |

### Trust Tiers (K-Derm Membrane Model)

| Proof Type | Trust Tier | Auto-Enroll |
|------------|-----------|-------------|
| FIDO2/SoloKey attestation | **Kin** (tier 1) | Yes |
| grapheneGate beacon proximity | **Sibling** (tier 2) | Yes |
| Pre-shared enrollment token | **Extended** (tier 3-4) | Yes |
| No physical proof | **Rejected** | No |

---

## WHAT'S DONE (FOSSILIZE)

| Item | Evidence |
|------|----------|
| Tower Atomic (Wave 150) | 353x LAN, 1.7x WAN, 197 scenarios, chimera unblocked |
| BTSP sub-wave (Wave 151b-d) | 13/13 primals shipped ClientHello |
| bearDog FIDO2 + iosGate (152-154) | FIDO2 hardware, iOS Secure Enclave, HSM agnostic |
| Autonomous enrollment (Wave 155a) | mesh.gate_enroll + gate-enroll.sh + FIDO2/beacon attestation |
| whitePaper gen/ review | GEN_REVIEW_151c.md + JOSS_PUBLICATION.md |
| Depot convergence | 28 bins × 2 arch, provenance fresh |

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — Wave 155a, 43/43 synced |
| 2 | Ecological | GREEN — 75,199 tests, 2 debt, **13/13 BTSP** |
| 3 | Hardware | **AMBER → GREEN** — autonomous enrollment shipped, 5 gates ready |
| 4 | Sovereignty | GREEN — autonomous enrollment + FIDO2/beacon trust chain |
| 5 | Public Surface | GREEN — sporePrint SEO shipped |
| 6 | Compositions | GREEN — Nest Atomic Phase 0 UNBLOCKED, compute/nest include Tower base |
| 7 | Documentation | GREEN — enrollment documented, two parallel blurbs |
| 8 | Campus | GREEN |

---

*Wave 155b: genomeBin CONVERGENCE. Tower Atomic is the universal OS abstraction —
songBird universal-ipc already handles UDS (Linux), named pipes (Windows), abstract
sockets (Android), XPC (iOS), TCP (fallback). `bind_mode` and `target` are transitional
manifest fields — primals auto-detect via `Platform::detect()`. Five Tier 1 genomeBin
targets. golgiBody sole depot. Self-enrollment pattern live. cellMembrane pushed.
75,199 primal tests. 13/13 BTSP.*
