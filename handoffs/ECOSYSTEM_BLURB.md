# ecoPrimals Ecosystem Blurb — Wave 137a

**Date**: Jul 11, 2026 19:00 EDT | **Wave**: 137a | **From**: eastGate overwatch
**Posture**: **CONVERGED. Neural API activation.** Full dimensional review complete. biomeOS Neural API live on eastGate 23 days — 320+ translations, 171 routes, 24/24 sockets healthy. 2,930+ tests / 0 fail. All 8 stadial criteria clear. Next phase: Neural API as deployment authority, replacing all ad-hoc patterns.

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

## Phase 1 — Neural API as Deployment Authority (NOW)

**Critical shift**: biomeOS Neural API has been live on eastGate for **23 days** (musl binary, riboCipher enforced, 24/24 sockets healthy). 320+ capability translations, 171 route entries, L4 adaptive routing, LifecycleManager, graph-based deployment — all running, none used operationally. **Every ad-hoc deployment pattern has a Neural API equivalent. Time to use them.**

See: `NEURAL_API_DEPLOYMENT_AUTHORITY_WAVE137a.md`

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| NAPI-MEMBRANE | **Wire `membrane deploy` to Neural API** — `membrane deploy.composition`, `membrane deploy.graph`, `membrane lifecycle.status` call through to Neural API via `capability.call` | cellMembrane | **CRITICAL** |
| NAPI-LIFECYCLE | **LifecycleManager as primary supervisor** — systemd manages biomeOS only, biomeOS manages all 13 primals. Dependency-aware restart, composition health, hot-reload | biomeOS | **CRITICAL** |
| NAPI-CROSS-GATE | **Neural API on every NUCLEUS gate** — deploy biomeOS musl binary + systemd service to sporeGate, ironGate, southGate. Cross-gate `capability.call` via songBird mesh | cellMembrane + all gates | **HIGH** |
| FLOCKGATE-MESH | **Fix songBird federation port 7700 on WG overlay** — flockGate has 0 mesh peers. Blocks cross-gate Neural API routing from WAN | mesh team | **HIGH** |

## Phase 2 — Live Compositions + Visualization (1-2 weeks)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| FP-DEPLOY | Deploy footPrint SPA to primals.eco/footprint/ — rsync + Caddy handle_path + songBird drawbridge API proxy | sporeGate | HIGH |
| SIGN-01-ACTIVATE | Deploy cascade signing keys — 3 blockers in SIGN-01 AAR | cellMembrane | HIGH |
| SKUNKY-DEPLOY | Deploy skunky-ingest to golgi — Caddy log → skunkBat behavioral analysis | skunkBat + sporeGate | HIGH |
| TOPO-VIS | sporePrint live topology viz — petalTongue consumes `topology.primals` + `routing_weights` from Neural API (not hardcoded) | petalTongue | HIGH |
| LIVE-ACTIVATE | `live.primals.eco` — petalTongue NUCLEUS on sporeGate | sporeGate | MEDIUM |
| THREAT-ACTIVATE | Feed 122 attacker IPs into skunkBat `baseline.observe` | skunkBat | MEDIUM |

## Phase 3 — Deprecate Ad-Hoc + Mesh Expansion (2-4 weeks)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| NAPI-NICHE | Gate enrollment via `niche.deploy` — replace manual provision scripts with tower.toml/nest.toml templates | biomeOS + cellMembrane | MEDIUM |
| NAPI-L5 | Activate perceptron shadow mode — `weight_health` against real traffic patterns | biomeOS | MEDIUM |
| STRANDGATE | Enroll strandGate via `niche.deploy compute-node.toml` — **REALWORLD**: SSH keys, physical cable | operator | MEDIUM |
| WESTGATE | Enroll westGate via `niche.deploy nest.toml` — 76TB ZFS cold storage | operator | MEDIUM |
| FP-PARITY | petalTongue visual parity with footPrint — 12 VT areas | petalTongue | MEDIUM |
| CF-DATA | Cloudflare analytics → skunkBat outer→inner data flow | skunkBat | MEDIUM |

## Phase 4 — External Proof + Full Authority (1-3 months)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| NAPI-SOLE | **Neural API sole deployment authority** — ad-hoc patterns deprecated. All deployment through `capability.call` / `graph.execute` / `composition.deploy` | all teams | MEDIUM |
| SHOW-HN | SHOW_HN publication — demonstrate Neural API routing live | primalSpring | MEDIUM |
| BEARDOG-GATEHOUSE | bearDog gatehouse TLS on golgi — sovereign ACME | bearDog + sporeGate | LOW |
| NESTGATE-COORD | nestGate coordination dashboard via Neural API | nestGate + petalTongue | LOW |
| PURE-RUST-AUDIT | Close ecosystem-wide pure Rust crypto audit | primalSpring | LOW |

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
