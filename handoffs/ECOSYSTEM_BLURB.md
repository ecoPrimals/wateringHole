# ecoPrimals Ecosystem Blurb — Wave 137a

**Date**: Jul 12, 2026 09:45 EDT | **Wave**: 137a | **From**: eastGate overwatch
**Posture**: **NEURAL API ACTIVATION IN PROGRESS.** cellMembrane wired `deploy.*` + `lifecycle.*` as Neural API front-end (443 LOC). SIGN-01 blockers resolved. FP-DEPLOY **LIVE** at primals.eco/footprint/. skunky-ingest deployed (dry-run). primalSpring v0.9.36 (1,106 tests, 136 scenarios). sporeGate AAR: Neural API not running yet (api ≠ neural-api), socket permissions cross-cutting blocker.

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
| ~~NAPI-MEMBRANE~~ | ~~Wire `membrane deploy` to Neural API~~ | cellMembrane | **DONE** (`1df1cfe`) — `deploy_dispatch.rs` (443 LOC), `deploy.composition`, `deploy.graph`, `lifecycle.status` wired |
| ~~SIGN-01-ACTIVATE~~ | ~~Resolve SIGN-01 activation blockers~~ | cellMembrane | **DONE** (`471ebf5`) — signing dispatch + deep debt resolved |
| ~~FP-DEPLOY~~ | ~~Deploy footPrint SPA to primals.eco/footprint/~~ | sporeGate | **DONE** — Vite build, Caddy handle_path, CSP, 200 OK |
| ~~SKUNKY-DEPLOY~~ | ~~Deploy skunky-ingest to golgi~~ | sporeGate | **DONE** — dry-run mode, systemd enabled, processing log backlog |
| NAPI-START | **Start `biomeos neural-api` on sporeGate** — api ≠ neural-api (different modes). Neural API not running yet. Single command to activate | sporeGate | **CRITICAL** |
| NAPI-PERMS | **Fix socket permissions** — `/run/membrane/*.sock` are `root:root srw-------`. Blocks Neural API routing. Same root cause as SIGN-01 | sporeGate + all gates | **CRITICAL** |
| NAPI-LIFECYCLE | **LifecycleManager as primary supervisor** — systemd → biomeOS → primals | biomeOS | **HIGH** |
| NAPI-CROSS-GATE | **Neural API on every NUCLEUS gate** — start on eastGate (already running), sporeGate (pending NAPI-START), ironGate, southGate | cellMembrane + all gates | **HIGH** |
| FLOCKGATE-MESH | **Fix songBird federation port 7700 on WG overlay** — 0 mesh peers from flockGate | mesh team | **HIGH** |

## Phase 2 — Live Compositions + Visualization (1-2 weeks)

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| FP-API | Wire footPrint API proxy through songBird drawbridge — Express `?url=` → songBird path-based routing alignment | songBird + flockGate | MEDIUM |
| FP-PERSIST | footPrint project persistence via nestGate CAS (replace Express CRUD) | nestGate | MEDIUM |
| SKUNKY-LIVE | Remove `--dry-run` from skunky-ingest — requires skunkBat `baseline.observe` listener on golgi | skunkBat | HIGH |
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
| primalSpring | 1,106 | GREEN (v0.9.36, 136 scenarios) |
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
| `NEURAL_API_DEPLOYMENT_AUTHORITY_WAVE137a.md` | Active — Phase 1 directive |
| `NEURAL_API_ACTIVATION_ASSESSMENT_137a.md` | Active — sporeGate gap analysis, NAPI-START + NAPI-PERMS pending |
| `FP_DEPLOY_SKUNKY_DEPLOY_AAR_137a.md` | **DONE** — footPrint live, skunky-ingest dry-run |
| `PRIMALSPRING_V0936_WAVE137a.md` | **DONE** — 4 new scenarios, 1,106 tests |
| `FLOCKGATE_DIVERGENCE_TOPOLOGY_AAR_136b.md` | Open — mesh gap unresolved |
| `FOOTPRINT_COMPOSITION_AUDIT_AAR_WAVE136b.md` | Superseded by FP-DEPLOY AAR |
| `FOOTPRINT_FLOCKGATE_SPINUP_136b.md` | Open — flockGate integration ongoing |

*Wave 137a: Neural API activation sprint. cellMembrane wired `deploy.*` + `lifecycle.*` (443 LOC, `1df1cfe`). SIGN-01 resolved (`471ebf5`). footPrint **LIVE** at primals.eco/footprint/ — first composition on sovereign infrastructure. skunky-ingest deployed (dry-run). primalSpring v0.9.36 (1,106 tests, 136 scenarios, +4 new). sporeGate AAR reveals critical gap: Neural API mode not started (api ≠ neural-api), socket permissions `root:root srw-------` block routing. NAPI-START + NAPI-PERMS are the critical path.*
