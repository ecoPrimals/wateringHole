# ecoPrimals Ecosystem Blurb — Wave 152a

**Date**: Jul 26, 2026 20:45 EDT | **Wave**: 152a | **From**: eastGate overwatch
**Posture**: **GATE FLEET ONLINE. 5 gates (strand, west, blue, swift, south) back online via RustDesk — postPrimordial enrollment beginning. bearDog Wave 152-154 evolution pushed (FIDO2, iosGate, HSM agnostic). All gates to Forgejo-first, agentic catch-up from golgiBody.**

---

## WHERE WE ARE

Waves 150-151 (Tower Atomic + BTSP sub-wave) are **fossilized**.
bearDog has continued evolving on flockGate through Wave 154.
5 previously-offline gates are **back online** and ready for postPrimordial enrollment.

| Metric | Value |
|--------|-------|
| Tower vs WireGuard | 353x LAN, 1.7x WAN |
| Scenarios | 197, all PASS |
| Known debt | **2** (grapheneGate provenance stale in git) |
| BTSP primals | **13/13** |
| Depot | 28 binaries × 2 arch (x86_64 + aarch64-musl) |
| Gates online | **spore, east, iron, flock, golgi, graphene, north** + **5 rejoining** |
| Gates rejoining | **strand, west, blue, swift, south** (Wave 109-114, ~40 waves behind) |

---

## THIS CASCADE — WHAT SHIPPED

### bearDog Wave 152-154 Evolution (flockGate → pushed)

Three major waves landed since last blurb (`0cd6279ef`):

**Wave 152-153 — FIDO2 Hardware Integration + Deep Debt Sweep** (`b8b3e9136`)
- FIDO2 hardware authenticator support wired
- Deep debt sweep across the full crate

**Wave 153c/154 — iosGate Deployment + HSM Agnostic Evolution** (`0cd6279ef`)
- **iOS Secure Enclave** wired to real Security.framework (P-256 ECDSA)
- iOS IPC evolved from XPC stubs to Unix domain sockets in sandbox
- HSM layer audit: eliminated production stubs, fixed module tree
- **3,333 lines of orphaned/corrupted debris deleted** (unwired modules, broken extractions, dead stubs)
- iosGate device registered, IPA build pipeline automated
- Zero TODOs, zero warnings, clean cargo check
- 112 files changed, 3,745 insertions, 5,173 deletions

### Gate Fleet Return — 5 Gates Back Online

**strand, west, blue, swift, south** all back online via RustDesk remote access.
strandGate agent status report (representative of the fleet):

- **Local repos**: Wave 109-114 (Jun 11-16), all clean, no uncommitted changes
- **Remotes broken**: WireGuard mesh not up, GitHub SSH misconfigured
- **USB BEA6-BBCE**: Staged today with 13/13 primals (Wave 142b binaries)
- **Delta**: ~40 waves behind current (109 → 152a)
- **Pre-cellMembrane**: gates predate SEO agentification and BTSP sub-wave

**Enrollment strategy**: postPrimordial — Forgejo-first, agentic catch-up from golgiBody.

---

## AGENT BOOTSTRAP — Autonomous Gate Enrollment

**Gate enrollment is now autonomous.** New or out-of-date gates self-enroll
by contacting golgiBody's `mesh.gate_enroll` endpoint. No human-in-the-loop
required (physical trust token provides proof of authorization).

### Autonomous Enrollment (preferred)

Run the enrollment client on the new gate:

```bash
# With a pre-shared enrollment token:
./infra/plasmidBin/enroll/gate-enroll.sh --hub primals.eco --token <token>

# With a FIDO2 SoloKey (strongest tier — auto-enrolls as Kin):
./infra/plasmidBin/enroll/gate-enroll.sh --hub primals.eco --fido2 <credential-id>

# With grapheneGate beacon proximity (medium tier — auto-enrolls as Sibling):
./infra/plasmidBin/enroll/gate-enroll.sh --hub primals.eco --beacon <beacon-id>
```

The enrollment client handles everything: WG keypair generation, SSH key
generation, contacting the enrollment endpoint, WireGuard configuration,
Forgejo SSH setup, and family seed delivery.

### What the Enrollment Endpoint Does (golgiBody)

The `mesh.gate_enroll` JSON-RPC method on songBird orchestrates:

1. **Verify physical proof** — FIDO2 attestation, beacon proximity, or token
2. **Allocate mesh IP** — from the dynamic pool (`.20`–`.254`), checking `wg show wg0`
3. **Register WG peer** — `wg set wg0 peer` on the hub
4. **Register SSH key** — Forgejo API (`FORGEJO_API_TOKEN`)
5. **Deliver family seed** — encrypted to enrollee's WG public key via bearDog
6. **Genetic enrollment** — BTSP-verified `mesh.enroll` with HMAC proof

### Trust Tiers (K-Derm Membrane Model)

| Proof Type | Trust Tier | Auto-Enroll |
|------------|-----------|-------------|
| FIDO2/SoloKey attestation | **Kin** (tier 1) | Yes |
| grapheneGate beacon proximity | **Sibling** (tier 2) | Yes |
| Pre-shared enrollment token | **Extended** (tier 3-4) | Yes |
| No physical proof | **Rejected** | No |

### For Gates Already In-Progress (5-gate fleet)

Gates that already have WG keys (south, strand, west) can call the enrollment
endpoint retroactively — it will allocate their IP, register them, and deliver
the family seed. Gates without keys (blue, swift) generate keys as part of the
enrollment script.

### Fallback: Manual Bootstrap (last resort)

If the enrollment endpoint is unreachable, see `infra/plasmidBin/enroll/RELAY_MANUAL.md`
for the manual WireGuard + Forgejo + RustDesk relay configuration.

### Post-Enrollment Convergence

After enrollment, the gate agent should:

```bash
# Clone or pull all repos from Forgejo
for repo in primals/*/  springs/*/  infra/*/  gardens/*/; do
  (cd "$repo" && git fetch origin && git merge --ff-only origin/main) 2>&1
done

# Build from source
for primal in primals/*/; do
  (cd "$primal" && cargo build --release 2>&1 | tail -1)
done

# Validate
cd springs/primalSpring && cargo test --release
```

### Divergence Notes

**westGate** has mixed-wave repos from partial GitHub pulls before the SSH key
was revoked. Fast-forward from Forgejo HEAD should resolve most cases.

---

## WHAT'S DONE (FOSSILIZE)

| Item | Evidence |
|------|----------|
| Tower Atomic (Wave 150) | 353x LAN, 1.7x WAN, 197 scenarios, chimera unblocked |
| BTSP sub-wave (Wave 151b-d) | 13/13 primals shipped ClientHello |
| bearDog production hardening (151c-d) | Mock elimination, encrypt-at-rest, pen test 3 CRITICALs closed |
| bearDog FIDO2 + iosGate (152-154) | FIDO2 hardware, iOS Secure Enclave, HSM agnostic, 3,333L debris |
| whitePaper gen/ review | GEN_REVIEW_151c.md + JOSS_PUBLICATION.md |
| Cargo.toml metadata | All primals standardized |
| Depot convergence | 28 bins × 2 arch, provenance fresh |
| sporePrint SEO | Search doors + query routing shipped |

---

## REMAINING — FORWARD WORK

### P0 — PostPrimordial Gate Enrollment (5 gates)

Strategy: **autonomous enrollment** via `mesh.gate_enroll` endpoint on golgiBody.
Each gate runs `gate-enroll.sh` with a physical proof token → zero human intervention.

| # | Gate | Status | Enrollment Path |
|---|------|--------|-----------------|
| 1 | southGate | WG keyed | `gate-enroll.sh --token <token>` (retroactive) |
| 2 | strandGate | WG keyed | `gate-enroll.sh --token <token>` (retroactive) |
| 3 | westGate | WG keyed | `gate-enroll.sh --token <token>` (divergence: mixed-wave repos) |
| 4 | blueGate | Fresh | `gate-enroll.sh --token <token>` (full enrollment) |
| 5 | swiftGate | Fresh | `gate-enroll.sh --token <token>` (full enrollment) |

See **AGENT BOOTSTRAP** section above for the enrollment client and trust tier details.

### P1 — bearDog Public Flip

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | bearDog pen test (3 CRITICALs) | bearDog (flockGate) | **DONE** |
| 2 | bearDog production mock elimination | bearDog (flockGate) | **DONE** |
| 3 | bearDog FIDO2 + iosGate + HSM agnostic | bearDog (flockGate) | **DONE** |
| 4 | Flip bearDog repo to public | eastGate overwatch | **READY** (9/10) |

### P1 — Nest Atomic Phase 0

| # | Task | Owner |
|---|------|-------|
| 1 | Wire nestGate `connect_with_btsp` into priority call sites | nestGate (flockGate) |
| 2 | nestGate CAS integration testing | eastGate + flockGate |
| 3 | Nest Atomic Phase 0 validation | primalSpring (eastGate) |

### P1 — Enmeshment Use Cases

Once postPrimordial enrollment is complete, gates serve as compute:

| Gate | Role |
|------|------|
| strandGate | Heavy bioinformatics compute (128 threads, RTX 3090) — NF pipeline candidate |
| westGate | Cold storage archive (76TB ZFS) — NestGate CAS backend |
| blueGate | TBD — profile pending |
| swiftGate | TBD — profile pending |
| southGate | Full NUCLEUS deployment (house2) |

### P2 — Hardware

| # | Task | Owner |
|---|------|-------|
| 1 | grapheneGate Keystore2 binder IPC | bearDog (eastGate) |
| 2 | `aarch64-linux-android` depot target | sporeGate + eastGate |
| 3 | grapheneGate full NUCLEUS deploy | eastGate |

### Glacial Goals (projectFoundation/NUCLEUS)

| # | Task | Owner |
|---|------|-------|
| 1 | crates.io publishes (all public primals) | eastGate overwatch |
| 2 | JOSS paper — Gonzales NF live system | projectFoundation |
| 3 | CTF NDU grant alignment | projectFoundation |
| 4 | Show HN | projectFoundation |
| 5 | tideGlass Phase 0 (GPS rebuild) | projectFoundation |

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced, gen/ review COMPLETE |
| 2 | Ecological | GREEN — 197 scenarios, 2 debt, **13/13 BTSP** |
| 3 | Hardware | **AMBER → ADVANCING** — 5 gates rejoining, postPrimordial enrollment starting |
| 4 | Sovereignty | GREEN — BTSP 13/13, Tower EXCEEDS WG, depot fresh |
| 5 | Public Surface | GREEN — sporePrint SEO shipped |
| 6 | Compositions | GREEN — Nest Atomic Phase 0 UNBLOCKED |
| 7 | Documentation | GREEN — gen/ review, JOSS strategy, NF case study reconciled |
| 8 | Campus | GREEN |

---

*Wave 152a: GATE FLEET ONLINE. 5 gates (strand, west, blue, swift, south) back
online via RustDesk — postPrimordial enrollment beginning via Forgejo-first agentic
catch-up from golgiBody. bearDog Wave 152-154 evolution pushed (FIDO2 hardware,
iOS Secure Enclave, HSM agnostic, 3,333L debris cleaned, iosGate registered).
bearDog ready for public flip (9/10). 197 scenarios. 13/13 BTSP.*
