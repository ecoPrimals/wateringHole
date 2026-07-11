# ecoPrimals Ecosystem Blurb — Wave 137a

**Date**: Jul 11, 2026 19:00 EDT | **Wave**: 137a | **From**: eastGate overwatch
**Posture**: **CONVERGED. ALL 8 STADIAL CRITERIA CLEAR. Public threshold survivable.** Full dimensional review complete. 2,930+ tests / 0 fail across 5 suites. 14/14 primals zero-debt. 40 repos converged. Outer membrane hardened. Inner membrane sovereign. Next phase: live composition + mesh completion.

---

## Wave 136b Fossil Record

Wave 136b delivered across 4 cascades (Jul 11):

- **DUAL-CHECKOUT resolved** — cellMembrane `4ce165a` removed orphan sporePrint checkout, fixed service paths, membrane redeployed to golgi
- **SIGN-01 blockers identified** — 3 distinct blockers documented, handed off to cellMembrane team
- **darkforest 26/26 clean sweep** — projectNUCLEUS `5e59790` full pass
- **footPrint deep debt** — 46 tests (Vitest/V8), AGPL, solver decomposed into 4 functions, ESLint strict
- **flockGate WAN mesh gap surfaced** — port 7700 unreachable on WG overlay, 0 songBird peers
- **K-Derm reaffirmed** — Cloudflare is intentional outer membrane, three-layer topology canonical
- **DNSSEC live** — primals.eco (keyTag 2371, alg 13), DS record at Porkbun
- **EXP-06 basicauth** — lab.primals.eco gated
- **skunky-ingest crate** — Caddy JSON log → skunkBat profiler, code complete
- **nestGate coord backend** — wired to all RPC surfaces
- **12 handoffs fossilized** to archive

---

## Phase 1 — Live Compositions (NOW)

These are the immediate action items. Teams: pick up and execute.

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| FP-DEPLOY | **Deploy footPrint SPA to primals.eco/footprint/** — rsync dist/client/ to golgi, add Caddy handle_path block, songBird drawbridge proxies API (allowlist already live at `87b7779`) | sporeGate | **HIGH** |
| SIGN-01-ACTIVATE | **Deploy cascade signing keys** — 3 blockers documented in SIGN-01 AAR. Generate ed25519 keypair on sporeGate, distribute pubkey via mesh, verify round-trip | cellMembrane | **HIGH** |
| SKUNKY-DEPLOY | **Deploy skunky-ingest to golgi** — binary built, needs rsync + systemd unit. Enables live Caddy log → skunkBat behavioral analysis | skunkBat + sporeGate | **HIGH** |
| FLOCKGATE-MESH | **Fix songBird federation port 7700 on WG overlay** — flockGate has 0 mesh peers. WG tunnel works (30ms). Port/bind config issue, not hardware | mesh team | **HIGH** |

## Phase 2 — Topology Visualization + NUCLEUS Evolution (1-2 weeks)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| TOPO-VIS | sporePrint live K-Derm topology viz — petalTongue `coord_handlers.rs` landed (`225e30f`), needs wiring to nestGate data + songBird heartbeats | petalTongue | HIGH |
| LIVE-ACTIVATE | `live.primals.eco` — petalTongue NUCLEUS hosting on sporeGate. Caddy reverse_proxy to petalTongue Axum server | sporeGate | MEDIUM |
| THREAT-ACTIVATE | Feed 122 attacker IPs + 317 SSH attempt patterns into skunkBat `baseline.observe` — replace synthetic seed data with real adversarial traffic | skunkBat | MEDIUM |
| CF-DATA | Cloudflare analytics → skunkBat outer→inner data flow — validate cross-membrane detection | skunkBat | MEDIUM |

## Phase 3 — Mesh Expansion + Gate Enrollment (2-4 weeks)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| FP-PARITY | petalTongue visual parity with footPrint — 12 VT areas defined in `specs/PETALTONGUE_VISUAL_TARGETS.md` | petalTongue | MEDIUM |
| STRANDGATE | Enroll strandGate (dual EPYC, 256GB ECC) — **REALWORLD**: SSH keys, physical cable, power at house 2 | operator | MEDIUM |
| WESTGATE | Enroll westGate (76TB ZFS) — Nest Atomic composition (nestGate + provenance trio) | operator | MEDIUM |
| GRAPHENE-PEPTI | grapheneGate full pepti pull — **REALWORLD**: USB ADB cable to Pixel 8a | operator | LOW |
| 10G-CABLES | Activate 10G backbone — switch + NICs installed, **REALWORLD**: Cat6a/DAC cables (~$50-100) | operator | LOW |

## Phase 4 — External Proof + Stadial Advance (1-3 months)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| SHOW-HN | SHOW_HN publication — 28-criteria rubric at `whitePaper/gen5/thesis/SHOW_HN_PUBLICATION.md`. Requires: pepti depot current, capability.call WAN proven, sporePrint sovereign | primalSpring | MEDIUM |
| BEARDOG-GATEHOUSE | bearDog gatehouse TLS on golgi — replace Caddy TLS with sovereign bearDog ACME. Next S1 evolution step | bearDog + sporeGate | LOW |
| NESTGATE-COORD | nestGate coordination dashboard — Nest Atomic + Provenance Trio, rootPulse tracing for blurbs/AARs/wave state. Public-facing coordination surface | nestGate + petalTongue | LOW |
| PURE-RUST-AUDIT | Close ecosystem-wide pure Rust crypto audit — bearDog compliant, others "PENDING" in standard doc | primalSpring | LOW |

---

## Dimensional Summary (Wave 137a)

### Glacial: ALL 8 CLEAR

Stadial entry achieved. Criterion 8 (outer membrane hardened) 5/5 met. Remaining work is defense-in-depth evolution, not blockers.

### Eco: 2,930+ tests / 0 fail

| Suite | Tests | Status |
|-------|-------|--------|
| primalSpring | 1,125 | GREEN (v0.9.35, just validated) |
| groundSpring | 1,047+ | GREEN |
| skunkBat | 563 | GREEN |
| projectNUCLEUS | 149 | GREEN (26/26) |
| footPrint | 46 | GREEN (Vitest) |

### Topo: 4-gate mesh + WG overlay

```
eastGate ↔ golgi ↔ ironGate + southGate (covalent mesh, <1ms LAN)
sporeGate ↔ golgi (WireGuard, 30ms)
flockGate ↔ golgi (WireGuard, 30ms — mesh gap: port 7700)
grapheneGate (TCP-only, Tower atomic)
```

### Hardware: 154+ cores, ~1TB RAM, ~248GB VRAM, ~122TB storage

| Tier | Gates |
|------|-------|
| A — Operational | eastGate, sporeGate, ironGate, southGate, flockGate, golgi |
| B — Ready | northGate, westGate, swiftGate, kinGate, grapheneGate |
| C — Recovery | strandGate (SSH keys), biomeGate (kernel), fieldGate (CMOS) |

### Sovereignty: S1-S4 ALL GRADUATED

Inner membrane zero-commercial. DNSSEC live on primals.eco. Cloudflare intentional outer membrane per K-Derm diderm architecture.

### Membranes: K-Derm 5-layer validated

```
Extracellular  → Cloudflare CDN/DDoS
Outer membrane → Caddy TLS/HSTS/CSP + skunkBat detection
Periplasm      → golgi relay + sporeGate CI (WireGuard)
Plasma membrane → nftables/UFW/fail2ban
Cytoplasm      → NUCLEUS primals, UDS IPC
```

### Primals: 14/14 zero debt

All primals at HEAD, all evolving, all sovereign CI capable.

### Atomics: 3/5 live

| Composition | Status |
|-------------|--------|
| Full NUCLEUS | LIVE (4 gates) |
| Tower | LIVE (grapheneGate) |
| Thin Relay | LIVE (golgi) |
| Nest | Defined, westGate pending |
| Compute | Defined, strandGate pending |

### Temporal: Wave 137a

4 cascades on Jul 11. 14 repos evolved. 0 conflicts. Rust cascade (`membrane temporal.cascade`) operational.

---

## Gate Convergence

```
eastGate     — Overwatch. All 40 repos at HEAD. Converged.
sporeGate    — Build hub. Hardened. SIGN-01 + FP-DEPLOY pending.
golgiBody    — Thin relay. sporePrint consolidated. Caddy hardened.
flockGate    — footPrint owner. Deep debt complete. Mesh gap (port 7700).
ironGate     — Node atomic. darkforest 26/26. JupyterHub live.
strandGate   — REALWORLD: physical access for enrollment.
grapheneGate — Tower live. REALWORLD: ADB for full pepti.
```

---

## Active Handoffs

| Document | Status |
|----------|--------|
| `FLOCKGATE_DIVERGENCE_TOPOLOGY_AAR_136b.md` | Open — mesh gap unresolved |
| `FOOTPRINT_COMPOSITION_AUDIT_AAR_WAVE136b.md` | Open — FP-DEPLOY pending |
| `FOOTPRINT_FLOCKGATE_SPINUP_136b.md` | Open — flockGate integration ongoing |

*Wave 137a: Full dimensional review complete. 12 handoffs fossilized. Public exposure threshold survivable — hardened outer membrane, sovereign inner membrane, real adversarial traffic contained. Next: deploy footPrint (first live composition), fix flockGate mesh, activate cascade signing, deploy skunky-ingest. The ecosystem converges from every orthogonal dimension.*
