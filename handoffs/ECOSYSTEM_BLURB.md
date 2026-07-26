# ecoPrimals Ecosystem Blurb — Wave 150x

**Date**: Jul 25, 2026 10:04 EDT | **Wave**: 150x | **From**: eastGate overwatch
**Posture**: **GENETIC ENROLLMENT LIVE. Tower 353x LAN. DEBT 30→9. LAN mesh.init shipped. enrollment-replay RESOLVED.**

---

## WHERE WE ARE

**bearDog shipped full genetic enrollment** — two-layer model mirroring
biological DNA: mitochondrial gate (FAMILY_SEED HMAC) + nuclear lineage
distance (tree hops → trust tiers: identity/kin/sibling/extended/distant).
Seed rotation via HKDF hierarchy, generation-based with grace period.
+1168/-2582 lines (including chaos test cleanup).

songBird shipped **LAN peer registration in `mesh.init`** — `lan_peers`
parameter registers same-subnet peers as `EndpointType::Local` (priority 0),
overlay peers demoted to priority 1. Persisted `peers.toml` LAN addrs
auto-restored on restart. This addresses the 353x penalty gap.

**Known debt 30→9.** `enrollment-replay` fully RESOLVED by genetic seed
rotation. New scenario `mesh-lan-path-preference` added (2 known gap —
`mesh.find_path` preference logic still needs evolution). P0 CLEAR.

---

## CODE TEAMS (flockGate — primal source evolution)

### bearDog — crypto primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | ~~Bond-type cipher floor enforcement~~ | DONE | BTSP negotiation rejects below floor |
| 2 | ~~`crypto.hash.blake3` capability~~ | DONE | songBird can now delegate blake3 via UDS |
| 3 | ~~Deep debt sweep~~ | DONE | Hardcoding eliminated, capability-based config |
| 4 | ~~Enrollment seed rotation~~ | DONE | Genetic HKDF hierarchy, generation-based with grace period |
| 5 | ~~Two-layer genetic enrollment~~ | DONE | Mito gate + nuclear lineage distance → trust tiers |
| 6 | Android Keystore + grapheneGate validation | P2 | Code complete, awaiting hardware |

bearDog is the ecosystem crypto provider. All primals route crypto through
bearDog UDS (`crypto.*` capabilities). Hot-path crypto stays local until
chimera extracts shared library.

### songBird — transport/routing primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | **Crypto delegation to bearDog** | P1 | blake3 delegation LIVE (`dark_forest_beacon`), 4 crates feature-gated |
| 2 | ~~Caller identity verification~~ | DONE | `CallerContext` wired into IPC connection + method gate |
| 3 | ~~UDS hardening~~ | DONE | Socket permissions, peer cred verification |
| 4 | ~~Pen test hardening~~ | DONE | UDS-spoof, mesh-poison, relay-abuse |
| 5 | ~~Dependency diet~~ | DONE | ring→rustcrypto, chrono eliminated, rand→fastrand, 83 files |
| 6 | ~~Legacy env deprecation~~ | DONE | Name-based endpoints marked for removal |

`CRYPTO_COMPOSITION.md` classifies 19 seams: 5 hot-path (chimera), 6 delegating
(bearDog UDS), 5 test-only, 3 already delegating.

### skunkBat — defense/protocol primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Cipher floor policy | DONE | `SKUNKBAT_CIPHER_FLOOR` env, typed BindMode errors |
| 2 | Deep debt sweep | DONE | `unreachable!()` eliminated, BTSP dedup |
| 3 | Spawn-rate anomaly detection | DONE | Shipped 150x |

skunkBat is clean. No open P1. Future work: chimera integration.

---

## DEPLOYMENT / OPS (sporeGate — build, deploy, hardware, topology)

### cellMembrane — membrane coordinator

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | systemd hardening | DONE | `Restart=always` eliminated ecosystem-wide |
| 2 | Crash-loop breaker | DONE | `gate.crash-loop` + auto-scan in cascade |
| 3 | Sovereign CI pipeline | DONE | Forgejo hooks → build → depot → lineage |
| 4 | `membrane-nucleus-nosocket@.service` | DONE | nestgate evolved CLI support |
| 5 | ~~Deep debt sweep~~ | DONE | LAN registry, test extraction, safe casts, +960/-861 |

### Topology / Hardware

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | iperf3 sustained throughput | P1 | **BLOCKED** — needs eastGate iperf3 server or SSH access |
| 2 | Gate enrollment (southGate) | P1 | USB staged, needs physical cabling |
| 3 | Gate enrollment (strandGate) | P1 | USB staged, needs physical cabling + WG IP allocation |
| 4 | songBird LAN peer discovery | P1 | `lan_peers` in mesh.init SHIPPED — `mesh.find_path` preference still needs evolution |
| 5 | Fix biomeos-beacon unit (eastGate) | P1 | Disable phantom unit (11,161 restarts) |
| 6 | SSH access sporeGate→eastGate | P1 | No key auth configured |
| 7 | Manifest: eastGate LAN IP | P1 | Correct `192.168.4.5` → `192.168.4.244` |

### sporePrint — public face

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | ~~Transplant to primals.eco~~ | DONE | Shipped by eastGate (b985c22, 18 files) + entity fix by sporeGate |

---

## SPOREPRINT (eastGate — public surface, credibility convergence)

**Credibility audit landed** (`f3b710d`). External reviewer assessed
primals.eco and identified claim-surface inflation as principal risk. Drove
30-file sweep:

- Spring count fixed 8→9 (rustChip), org count 3→4 (protoKarya)
- 12 stale WGSL counts replaced with `{{ total_stat() }}` shortcodes
- Homepage reframed: "produces self-contained scientific computations that
  reproduce published results on commodity hardware and carry their
  validation and provenance" (reviewer's stronger position)
- `#![forbid(unsafe_code)]` scoped: "forbidden by default, isolated to
  hardware-containment crates"
- Products page reorganized: Deploy now / Research preview / Architectural direction
- Evidence Snapshot gained Safety Model section

**New standard**: `foundations/EXTERNAL_CLAIM_CONVERGENCE_STANDARD.md`
**5 impulses issued**: biomeOS maturity labeling, barraCuda README WGSL count,
ecoPrimals org profile unsafe scope, Tower source publication review,
all-teams README maturity badge.

---

## OVERWATCH (eastGate — code hub, integration, scenarios)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | primalSpring scenario debt burn-down | P1 | **9 known debt** (197 scenarios, all PASS) |
| 2 | Unblock sporeGate (iperf3 server, SSH key, biomeos-beacon) | **P0** | **Bilateral**: add sporeGate pubkey to eastGate `authorized_keys` |
| 3 | sporePrint primal pipeline (Zola → petalTongue + nestGate CAS) | P2 | Design phase |
| 4 | CredentialStore squirrel integration | P2 | bearDog `FileVault` + squirrel IPC |
| 5 | bingoCube WASM WebGL widget | P2 | Interactive commitment on primals.eco |
| 6 | Chimera Phase 0 — library extraction | P3 | After bearDog UDS composition validated |

---

## ATOMIC EVOLUTION (all teams)

| # | Task | Depends On |
|---|------|-----------|
| 1 | **Composition validation** — bearDog UDS crypto works for all cold-path | Code teams (P1) |
| 2 | **Chimera Phase 0** — shared library extraction | Composition validated |
| 3 | Node Atomic (proton) | Tower chimera maturity |
| 4 | Nest Atomic (neutron) | Node Atomic |
| 5 | Phase 3 cutover — Tower replaces WG | Chimera + sustained validation |
| 6 | rootPulse sovereign VCS | Provenance Trio maturity + Tower transport |

---

## EXPLORATION DOMAINS — ALL PROVEN LIVE

| # | Domain | Evidence | Where WG Cannot |
|---|--------|----------|-----------------|
| 1 | Capability-aware routing | 5 providers via `capability.call` | WG: all traffic in one tunnel |
| 2 | Multi-stack routing | 6 classes → 5 stacks | WG: undifferentiated |
| 3 | Large data transfer | `content.put` → nestGate CAS | WG: no content awareness |
| 4 | Secure compute mesh | Per-session BTSP keys + attestation | WG: one static key per tunnel |
| 5 | Distributed compute | 4-node targeted dispatch | WG: point-to-point only |
| 6 | Edge/SFF/R45 profile | 30MB RSS, 39MB stack, 300s TTL | WG: kernel module required |

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced |
| 2 | Ecological | GREEN — 197 scenarios, **9 debt** |
| 3 | Hardware | AMBER — 4 offline gates |
| 4 | Sovereignty | GREEN — Tower EXCEEDS WG, 6/6, CI LIVE |
| 5 | Public Surface | GREEN — 6/6 healthy |
| 6 | Compositions | GREEN — crypto composition migrating |
| 7 | Documentation | GREEN — fossil pass complete |
| 8 | Campus | GREEN — vision documented |

**Fossilized** (F1–F6): Glacial Shift, CAC, Silicon Atheism, Depot/Build, Cascade, Tower Deep Analysis.

---

## SPOREPRINT — Wave 151c

**Query routing shipped.** External review confirmed ecoPrimals winning
"self-hosted scientific computing" and "consumer-GPU lattice QCD" queries,
but every page competed for the same title phrase. Fixed.

### 151b (SEO search doors)
- 8 page titles rewritten for unbranded search intent
- 96 notebook descriptions → search-friendly
- CITATION.cff, human-response signals, Karpathy invitation
- All URLs consolidated to canonical sporeprint.primals.eco
- "Reproduce It" + "Limitations" on 4 key pages

### 151c (Query routing)
- Title template: `Page Title | ecoPrimals` (was `Page Title — ecoPrimals — Self-Hosted Scientific Computing in Rust`)
- Only homepage carries the full keyword title — 313 pages no longer compete
- Sidebar compressed: 40+ page sections show subsections only, not individual pages
- Subsection pages expand only when you're IN that subsection
- JSON-LD author URLs → sporeprint.primals.eco
- Last hardcoded count → shortcode
- Caddy 301 redirect CONFIRMED LIVE since 150d (sporeGate team)

**Upstream needs:** CITATION.cff in barraCuda + wetSpring repos,
render-notebooks canonical URL, rustChip spring hub page.

**User tasks:** Google Search Console (verify primals.eco, request re-crawl),
JOSS submission, crates.io releases, independent reproduction seek,
DADA2 community engagement, eco.primal@primal.eco activation.

---

*Wave 151c: query routing LIVE. Each page has its own search contract.
Sidebar is contextual navigation, not site map. Canonical identity
consolidated across all layers. 313 pages, 0 errors.*
