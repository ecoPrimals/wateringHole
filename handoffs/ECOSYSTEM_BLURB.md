# ecoPrimals Ecosystem Blurb — Wave 137b (Checkpoint)

**Date**: Jul 12, 2026 13:30 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **NEURAL API LIVE + MESH BIDIRECTIONAL.** Phase 1 at 10/12. Neural API systemd on sporeGate. songBird `f05918a` deployed to sporeGate + golgi. Bidirectional WG mesh live. Depot cryptographically signed. 40 repos synced (origin + forgejo). primalSpring 141 scenarios / 1,131 tests. This blurb is the **full debt inventory** — resolve by end of wave.

---

## Phase 1 — Neural API as Deployment Authority: 10/12 DONE

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| ~~NAPI-MEMBRANE~~ | Wire `membrane deploy` to Neural API | cellMembrane | **DONE** (`1df1cfe`) |
| ~~SIGN-01~~ | Resolve SIGN-01 + verify E2E | cellMembrane + sporeGate | **DONE** — depot signed, `sign.verify PASS` |
| ~~FP-DEPLOY~~ | Deploy footPrint SPA | sporeGate | **DONE** — primals.eco/footprint/ (114ms WAN) |
| ~~SKUNKY-DEPLOY~~ | Deploy skunky-ingest | sporeGate | **DONE** — dry-run, log backlog |
| ~~NAPI-START~~ | Start Neural API on sporeGate | sporeGate | **DONE** — 48 primals, 156 translations |
| ~~NAPI-PERMS~~ | Fix socket permissions | cellMembrane + sporeGate | **DONE** — systemd UMask permanent (`d5474df`) |
| ~~FLOCKGATE-MESH~~ | Fix songBird port 7700 | songBird | **DONE** (`f05918a`) — 4 overlay peers |
| ~~NAPI-SYSTEMD~~ | Promote Neural API to systemd | sporeGate | **DONE** — `membrane-neural-api.service` |
| ~~NAPI-CROSS-GATE~~ | Deploy songBird `f05918a` to sporeGate + golgi | sporeGate | **DONE** — bidirectional mesh live |
| ~~GOLGI-WG-BIND~~ | songBird on golgi bind 10.13.37.1:7700 | golgi | **DONE** — `0.0.0.0:7700` |
| NAPI-LIFECYCLE | LifecycleManager registration (lifecycle.status count=0) | biomeOS | **HIGH** |
| SOCKET-DIR-UNIFY | Unify `/run/membrane/`, `/run/biomeos-root/`, `/run/biomeos-default/` | biomeOS | MEDIUM |

---

## Full Debt Inventory — Resolve by End of Wave

### CRITICAL — Blocks SHOW-HN / WAN E2E

| # | ID | Description | Owner | Effort |
|---|-----|-------------|-------|--------|
| 1 | **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Primals aren't registering lifecycle hooks. Code change in biomeOS. | biomeOS | 4-8hr |
| 2 | **DRAWBRIDGE-ROUTES** | Confirm `SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter` on sporeGate. `jupyter` cap not advertised in mesh.status. | sporeGate | 30min |
| 3 | **UDS-HTTP-PROTOCOL** | songBird UDS mesh engine can't register HTTP federation peers. `peer.connect` TCP succeeds but `mesh.peers` stays empty. flockGate can `curl` sporeGate federation but not route via local UDS. | songBird | 4-8hr |

### HIGH — Infrastructure Convergence

| # | ID | Description | Owner | Effort |
|---|-----|-------------|-------|--------|
| 4 | **SOCKET-DIR-UNIFY** | Three socket dirs on sporeGate (`/run/membrane/`, `/run/biomeos-root/`, `/run/biomeos-default/`). Bridged by ExecStartPre symlinks. Unify to `/run/membrane/` only. | biomeOS | 2-4hr |
| 5 | **BRIDGE-ERROR-PROP** | NeuralBridge should propagate Neural API errors instead of falling through silently. | cellMembrane | 2hr |
| 6 | **DEPLOY-DISPATCH-XGATE** | `deploy_dispatch.rs` cross-gate routing still uses `capability.call` envelope — needs dotted method alignment. | cellMembrane | 1hr |
| 7 | **SOCKET-UMASK** | Primals should create sockets with explicit permissions (not umask-dependent). systemd UMask is a band-aid — process-level `fchmod` after bind. | biomeOS | 2hr |
| 8 | **SKUNKY-LIVE** | Remove `--dry-run` from skunky-ingest. Requires skunkBat `baseline.observe` listener on golgi. | skunkBat + golgi | 2-4hr |
| 9 | **DEPOT-POPULATE** | flockGate depot has 0/13 primals. Only songBird binary present. Need `plasmid fetch` or manual sync. | flockGate | 30min |
| 10 | **SONGBIRD-EASTGATE** | Deploy songBird `f05918a` to eastGate for full bidirectional mesh (sporeGate+golgi done, eastGate still old). | eastGate | 30min |

### MEDIUM — Composition + Visualization

| # | ID | Description | Owner | Effort |
|---|-----|-------------|-------|--------|
| 11 | **FP-API** | Wire footPrint `/api/proxy?url=` through songBird drawbridge. Caddy rewrite (quickfix) or client-side migration (clean). 10-host allowlist already in songBird (`87b7779`). | songBird + flockGate | 2-4hr |
| 12 | **FP-PERSIST** | Replace footPrint Express CRUD (`/api/projects`) with nestGate CAS. Content-addressed, rootPulse-traced. | nestGate | 4-8hr |
| 13 | **TOPO-VIS** | sporePrint live topology viz — petalTongue consumes `topology.primals` + `routing_weights` from Neural API. | petalTongue | 8-16hr |
| 14 | **LIVE-ACTIVATE** | `live.primals.eco` — petalTongue NUCLEUS on sporeGate. | sporeGate | 4-8hr |
| 15 | **THREAT-ACTIVATE** | Feed 122 attacker IPs into skunkBat `baseline.observe`. Replace synthetic seed data. | skunkBat | 2hr |
| 16 | **CF-DATA** | Cloudflare analytics → skunkBat. Outer membrane data reinforces inner detection. | skunkBat | 2-4hr |

### LOW — Version Skew + Structural

| # | ID | Description | Owner | Effort |
|---|-----|-------------|-------|--------|
| 17 | **VERSION-SKEW** | 3 distinct version ranges across primals: 0.1-0.2 (biomeOS/squirrel/toadStool/coralReef/songBird), 0.4-0.9 (bearDog/barraCuda/sourDough/sweetGrass/loamSpine), 0.14 (rhizoCrypt). Workspace versioning used by nestGate/petalTongue. Coordinate a version strategy. | all teams | discussion |
| 18 | **SPORE-OWNERSHIP** | `SPORE_OWNERSHIP_MATRIX.md` doesn't exist — should document the three-way split between nestGate/rhizoCrypt/sweetGrass. | overwatch | 1hr |
| 19 | **NUCLEUS-MATRIX** | `NUCLEUS_VALIDATION_MATRIX` columns U/V/W undefined — spore ingest/emit/profile spec. | projectNUCLEUS | 1hr |
| 20 | **CERT-OWNER** | Certificate owner shows `loamspine`, expected `beardog`. ACME lifecycle ownership TBD. | bearDog | 30min |
| 21 | **SHADER-SUPPORT** | `shader.list` and `trust.list` in capability_registry.toml but no implementation. | coralReef | discussion |
| 22 | **BOND-METADATA** | 0/16 deployment graphs have `bond_type` metadata. | all teams | 2hr |
| 23 | **TIER-PRIORITY** | 7 compositions have tier priority = None (primalspring, cellmembrane, nucleus, etc.). | cellMembrane | 30min |
| 24 | **PEPTI-TARGETS** | Missing depot targets: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. | cellMembrane | 4hr |
| 25 | **GATE-NAME-ENV** | Set `GATE_NAME=flockGate` in shell profile. Eliminates hostname-detection fallback. | flockGate | 2min |

### DEFERRED — Phase 3-4 (Not This Wave)

| # | ID | Description | Owner |
|---|-----|-------------|-------|
| 26 | NAPI-NICHE | Gate enrollment via `niche.deploy` | biomeOS + cellMembrane |
| 27 | NAPI-L5 | Perceptron shadow mode — `weight_health` | biomeOS |
| 28 | NAPI-SOLE | Neural API sole deployment authority | all teams |
| 29 | SHOW-HN | Demonstrate Neural API routing live | primalSpring |
| 30 | BEARDOG-GATEHOUSE | bearDog gatehouse TLS on golgi | bearDog + sporeGate |
| 31 | NESTGATE-COORD | nestGate coordination dashboard | nestGate + petalTongue |
| 32 | FP-PARITY | petalTongue visual parity — 12 VT areas | petalTongue |
| 33 | STRANDGATE | Enroll strandGate (REALWORLD) | operator |
| 34 | WESTGATE | Enroll westGate — 76TB cold storage | operator |

---

## Primal Mountain — Version + Sync State

All 40 repos at HEAD. 0 dirty. Origin + Forgejo synced (7 repos re-synced this cascade).

| Primal | Version | Sync | Notes |
|--------|---------|------|-------|
| bearDog | 0.9.0 | OK | Crypto provider, Ed25519 signing |
| songBird | 0.2.1 | OK | `f05918a` deployed to 3 gates |
| nestGate | workspace | OK | CAS + RPC + coord backend |
| skunkBat | 0.2.18 | OK | skunky-ingest deployed (dry-run) |
| toadStool | 0.2.0 | OK | Stable |
| barraCuda | 0.4.0 | OK | GPU compute dispatch |
| coralReef | 0.2.0 | OK | Shader compilation |
| biomeOS | 0.1.0 | OK | Neural API live on 2 gates |
| petalTongue | workspace | OK | Awaiting TOPO-VIS + LIVE-ACTIVATE |
| sweetGrass | 0.7.61 | OK | Attribution |
| loamSpine | 0.9.16 | OK | Immutable ledger |
| rhizoCrypt | 0.14.17 | OK | Ephemeral DAG |
| sourDough | 0.4.0 | OK | Stable |
| squirrel | 0.1.0 | OK | Health readiness |
| cellMembrane | — | OK | 1,024 tests, pedantic clean |
| projectNUCLEUS | — | OK | 149 tests, 26/26 darkforest |
| projectFOUNDATION | — | OK | Stable |
| primalSpring | 0.9.36 | OK | 1,131 tests, 141 scenarios |
| groundSpring | — | OK | 1,047+ tests |
| sporePrint | — | OK | Live on primals.eco |
| footPrint | — | OK | Live at primals.eco/footprint/ |

---

## Dimensional Summary (Wave 137b Checkpoint)

### Glacial: ALL 8 CLEAR
Stadial entry achieved. No blockers.

### Eco: 3,960+ tests / 0 fail

| Suite | Tests | Scenarios | Status |
|-------|-------|-----------|--------|
| primalSpring | 1,131 | 141 | GREEN (v0.9.36) |
| cellMembrane | 1,024 | — | GREEN (pedantic, 0 clippy) |
| groundSpring | 1,047+ | — | GREEN |
| skunkBat | 563 | — | GREEN |
| projectNUCLEUS | 149 | — | GREEN (26/26) |
| footPrint | 46 | — | GREEN (Vitest) |

### Topo: Bidirectional Mesh Live

```
eastGate ↔ golgi ↔ ironGate + southGate (covalent mesh, <1ms LAN)
sporeGate ↔ golgi (WG overlay, bidirectional, 30ms)
flockGate → sporeGate + golgi + eastGate + ironGate (WG overlay, 4 peers, 31ms)
  ↳ bidirectional pending: songBird f05918a on eastGate
grapheneGate (TCP-only, Tower atomic)
```

### Sovereignty: S1-S4 ALL GRADUATED
DNSSEC live. Cloudflare intentional outer membrane. Zero-commercial inner.

### Membranes: K-Derm 5-layer validated
```
Extracellular  → Cloudflare CDN/DDoS
Outer membrane → Caddy TLS/HSTS/CSP + skunkBat
Periplasm      → golgi relay + sporeGate CI (WG)
Plasma membrane → nftables/UFW/fail2ban
Cytoplasm      → NUCLEUS primals, UDS IPC, Neural API
```

### Atomics: 3/5 live
Full NUCLEUS (4 gates), Tower (grapheneGate), Thin Relay (golgi). Nest + Compute pending.

---

## Gate Convergence

```
eastGate     — Overwatch. 40 repos at HEAD. Neural API live (23+ days). songBird f05918a pending.
sporeGate    — Build + NUCLEUS. Neural API systemd. Mesh bidirectional. SIGN-01 verified. FP-DEPLOY live.
golgiBody    — Thin relay. songBird f05918a deployed. Mesh bidirectional. sporePrint + footPrint serving.
flockGate    — footPrint owner. 4 overlay peers. WAN validated. Full debt checkpoint filed.
ironGate     — Node atomic. Own overwatch agent (hardware + deploys). projectNUCLEUS = code only.
strandGate   — REALWORLD: physical access.
grapheneGate — Tower live. REALWORLD: ADB.
```

---

## Active Handoffs

| Document | Status |
|----------|--------|
| `NAPI_SYSTEMD_MESH_DEPLOY_AAR_137b.md` | **NEW** — Phase 1 at 10/12, NAPI-SYSTEMD + bidirectional mesh |
| `FLOCKGATE_WAVE137b_DEBT_CHECKPOINT.md` | **NEW** — 4-tier debt inventory from flockGate |
| `PRIMALSPRING_V0936_WAVE137b.md` | **NEW** — +3 scenarios (141 total), 1,131 tests |
| `NEURAL_API_LIVE_AAR_137b.md` | Active — NAPI-START + NAPI-PERMS + SIGN-01 E2E |
| `CELLMEMBRANE_NAPI_PERMS_DEEP_DEBT_AAR_137b.md` | Active — systemd UMask permanent |
| `IRONGATE_OVERWATCH_SPLIT_WAVE137b.md` | Active — ironGate agent owns hardware |
| `NEURAL_API_DEPLOYMENT_AUTHORITY_WAVE137a.md` | Phase 1 largely complete |

---

*Wave 137b checkpoint: 10/12 Phase 1 DONE. Neural API systemd on sporeGate (48 primals). Bidirectional mesh live (sporeGate ↔ golgi). songBird f05918a on 3 gates. Depot signed. 3,960+ tests / 0 fail / 141 scenarios. 40 repos synced. 25 debt items inventoried (3 critical, 7 high, 6 medium, 9 low). 9 deferred to Phase 3-4. Forgejo parity restored (7 repos pushed). ironGate workspace split formalized.*
