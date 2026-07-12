# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 12, 2026 11:15 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **NEURAL API LIVE ON SPOREGATE.** NAPI-START done. NAPI-PERMS done. SIGN-01 verified E2E (depot signed). FLOCKGATE-MESH root-caused and fixed (port 8080→7700, `f05918a`). 4 overlay peers connected from flockGate. FP-DEPLOY confirmed live from WAN (114ms NYC). cellMembrane systemd UMask fix permanent (`d5474df`). 19 primals routable via Neural API on sporeGate.

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

**Neural API is LIVE on sporeGate.** 19 primals discovered and routable. `lifecycle.status`, `crypto.sign`, `topology.primals`, `graph.list`, `composition.deploy` all verified. Depot cryptographically signed via `sign.activate → beardog.sock → Ed25519 → signatures.toml → sign.verify PASS`. FLOCKGATE-MESH resolved — 4 overlay peers connected. cellMembrane systemd fix makes socket permissions permanent across all future bootstraps.

See: `NEURAL_API_LIVE_AAR_137b.md`, `FLOCKGATE_MESH_RESOLUTION_AAR_137a.md`, `CELLMEMBRANE_NAPI_PERMS_DEEP_DEBT_AAR_137b.md`, `FLOCKGATE_WAN_OVERWATCH_AAR_137a.md`

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| ~~NAPI-MEMBRANE~~ | ~~Wire `membrane deploy` to Neural API~~ | cellMembrane | **DONE** (`1df1cfe`) |
| ~~SIGN-01~~ | ~~Resolve SIGN-01 + verify E2E~~ | cellMembrane + sporeGate | **DONE** — depot signed, `sign.verify PASS` |
| ~~FP-DEPLOY~~ | ~~Deploy footPrint SPA~~ | sporeGate | **DONE** — live at primals.eco/footprint/ (114ms WAN) |
| ~~SKUNKY-DEPLOY~~ | ~~Deploy skunky-ingest~~ | sporeGate | **DONE** — dry-run, processing log backlog |
| ~~NAPI-START~~ | ~~Start Neural API on sporeGate~~ | sporeGate | **DONE** — 19 primals, 156 translations, 33 capabilities |
| ~~NAPI-PERMS~~ | ~~Fix socket permissions~~ | cellMembrane + sporeGate | **DONE** — runtime + permanent systemd UMask (`d5474df`) |
| ~~FLOCKGATE-MESH~~ | ~~Fix songBird port 7700~~ | songBird | **DONE** (`f05918a`) — 4 overlay peers from flockGate |
| NAPI-SYSTEMD | Promote Neural API to systemd service on sporeGate | sporeGate | **HIGH** |
| NAPI-LIFECYCLE | LifecycleManager registration (lifecycle.status count=0) | biomeOS | **HIGH** |
| GOLGI-WG-BIND | songBird on golgi: bind 10.13.37.1:7700 (currently public IP only) | golgi/sporeGate | **HIGH** |
| NAPI-CROSS-GATE | Deploy songBird `f05918a` to sporeGate + eastGate for bidirectional mesh | all gates | **HIGH** |
| SOCKET-DIR-UNIFY | Unify `/run/membrane/` and `/run/biomeos-root/` | biomeOS | MEDIUM |

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

## Dimensional Summary (Wave 137b)

### Glacial: ALL 8 CLEAR

Stadial entry achieved. Criterion 8 (outer membrane hardened) 5/5 met. Remaining work is defense-in-depth evolution, not blockers.

### Eco: 3,935+ tests / 0 fail

| Suite | Tests | Status |
|-------|-------|--------|
| primalSpring | 1,106 | GREEN (v0.9.36, 136 scenarios) |
| cellMembrane | 1,024 | GREEN (pedantic, 0 clippy warnings) |
| groundSpring | 1,047+ | GREEN |
| skunkBat | 563 | GREEN |
| projectNUCLEUS | 149 | GREEN (26/26) |
| footPrint | 46 | GREEN (Vitest) |

### Topo: 5-gate mesh + WG overlay (FLOCKGATE-MESH RESOLVED)

```
eastGate ↔ golgi ↔ ironGate + southGate (covalent mesh, <1ms LAN)
sporeGate ↔ golgi (WireGuard, 30ms)
flockGate → sporeGate + golgi + eastGate + ironGate (WG overlay, 4 peers, 31ms)
  ↳ bidirectional pending: deploy songBird f05918a to sporeGate/eastGate
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

### Temporal: Wave 137b

5 cascades across Jul 11-12. 18+ repo evolutions absorbed. 0 conflicts. Neural API live on 2 gates (eastGate 23d, sporeGate 137b).

---

## Gate Convergence

```
eastGate     — Overwatch. All 40 repos at HEAD. Neural API live (23+ days).
sporeGate    — Build + NUCLEUS hub. Neural API LIVE (19 primals). SIGN-01 verified. FP-DEPLOY live.
golgiBody    — Thin relay. sporePrint consolidated. Caddy hardened. WG bind gap (10.13.37.1:7700).
flockGate    — footPrint owner. Mesh resolved (4 overlay peers). WAN validation complete.
ironGate     — Node atomic. darkforest 26/26. JupyterHub live.
strandGate   — REALWORLD: physical access for enrollment.
grapheneGate — Tower live. REALWORLD: ADB for full pepti.
```

---

## Active Handoffs

| Document | Status |
|----------|--------|
| `NEURAL_API_LIVE_AAR_137b.md` | **NEW** — NAPI-START + NAPI-PERMS resolved, SIGN-01 E2E verified |
| `CELLMEMBRANE_NAPI_PERMS_DEEP_DEBT_AAR_137b.md` | **NEW** — permanent systemd UMask fix, bridge protocol aligned |
| `FLOCKGATE_MESH_RESOLUTION_AAR_137a.md` | **NEW** — port 8080→7700 root cause, 4 peers connected |
| `FLOCKGATE_WAN_OVERWATCH_AAR_137a.md` | **NEW** — WAN validation, FP-DEPLOY 114ms, 3 mesh blockers mapped, API surface for FP-API |
| `NEURAL_API_DEPLOYMENT_AUTHORITY_WAVE137a.md` | Active — Phase 1 directive (largely complete) |
| `AI_ACCESSIBILITY_DIVERGENCE_STUDY_136b.md` | Open — accessibility findings |

*Wave 137b: Neural API LIVE on sporeGate — 19 primals discovered, capability routing verified, depot cryptographically signed. FLOCKGATE-MESH root-caused and fixed (port 8080→7700). flockGate sees 4 overlay peers, WAN validation confirms 114ms to primals.eco/footprint/. cellMembrane systemd UMask fix makes socket permissions permanent. 7 Phase 1 items DONE, 5 remain (NAPI-SYSTEMD, lifecycle registration, golgi WG bind, bidirectional mesh deploy, socket directory unification). Phase 2 focus: live compositions, FP-API wiring, skunky-ingest live mode, topology visualization via Neural API.*
