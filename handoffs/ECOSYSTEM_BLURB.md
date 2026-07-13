# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 08:00 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **DEBT BURN-DOWN ACCELERATING.** Overnight: 8 items resolved by 5 teams. UDS-HTTP-PROTOCOL fixed (songBird). FP-PERSIST landed (nestGate CAS). SHALLOW-PINGPONG eliminated (20 Forgejo repos full-depth). BRIDGE-ERROR-PROP done (cellMembrane). NUCLEUS-MATRIX + BOND-METADATA done (projectNUCLEUS). THREAT-ACTIVATE + SKUNKY-LIVE prep + CF-DATA groundwork landed (skunkBat). DRAWBRIDGE-ROUTES confirmed. Phase 1 at 11/12. 20/28 debt items resolved.

---

## Overnight Closures (Jul 12-13)

| # | ID | Resolved By | Commit |
|---|-----|-------------|--------|
| 1 | ~~UDS-HTTP-PROTOCOL~~ | songBird | `0d2895b5` — `peer.connect` now registers peers in BeaconMesh |
| 2 | ~~FP-PERSIST~~ | nestGate | `88dc4fa2` — CAS-backed project persistence, 5 RPC methods, 9 tests |
| 3 | ~~SHALLOW-PINGPONG~~ | sporeGate/golgi | 20 Forgejo repos converted to full-depth mirrors. Thin relay pattern retired |
| 4 | ~~DRAWBRIDGE-ROUTES~~ | sporeGate | Confirmed operational — `jupyter` is HTTP proxy route, not mesh cap (expected) |
| 5 | ~~BRIDGE-ERROR-PROP~~ | cellMembrane | `d5506a3` — NeuralBridge propagates errors, plus deep debt |
| 6 | ~~NUCLEUS-MATRIX~~ | projectNUCLEUS | `ea57d6a` — U/V/W columns defined |
| 7 | ~~BOND-METADATA~~ | projectNUCLEUS | `ea57d6a` — `bond_type` on all 19 graphs |
| 8 | ~~THREAT-ACTIVATE~~ | skunkBat | `b708872` — 122 attacker IPs, SKUNKY-LIVE prep, CF-DATA groundwork |

Also: golgiBody `heads/` auto-publishing is live (~130 commits overnight — automated gate health tracking).

---

## Remaining Debt — 8 items

### biomeOS team

| # | ID | What | Effort |
|---|-----|------|--------|
| 1 | **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Last CRITICAL item. | 4-8hr |
| 2 | **SOCKET-DIR-UNIFY** | Unify `/run/membrane/`, `/run/biomeos-root/`, `/run/biomeos-default/` → single `/run/membrane/`. | 2-4hr |
| 3 | **SOCKET-UMASK** | Primals should `fchmod` sockets after bind. | 2hr |

### songBird + flockGate

| # | ID | What | Effort |
|---|-----|------|--------|
| 4 | **FP-API** | Wire footPrint `/api/proxy?url=` through drawbridge. Caddy rewrite or client migration. | 2-4hr |

### sporeGate

| # | ID | What | Effort |
|---|-----|------|--------|
| 5 | **LIVE-ACTIVATE** | Stand up `live.primals.eco` — petalTongue NUCLEUS on sporeGate. | 4-8hr |

### petalTongue team

| # | ID | What | Effort |
|---|-----|------|--------|
| 6 | **TOPO-VIS** | Live topology viz — consume Neural API `topology.primals` + `routing_weights`. | 8-16hr |

### eastGate overwatch (self)

| # | ID | What | Effort |
|---|-----|------|--------|
| 7 | **SONGBIRD-EASTGATE** | Deploy songBird `0d2895b5` to eastGate. (Now includes UDS-HTTP fix.) | 30min |
| 8 | **SPORE-OWNERSHIP** | Create `SPORE_OWNERSHIP_MATRIX.md`. | 1hr |

### Cleared since last blurb

| ID | Status |
|----|--------|
| ~~DEPLOY-DISPATCH-XGATE~~ | Absorbed into cellMembrane `d5506a3` |
| ~~TIER-PRIORITY~~ | Absorbed into projectNUCLEUS `ea57d6a` |
| ~~SKUNKY-LIVE~~ | Prep landed in skunkBat `b708872` |
| ~~CF-DATA~~ | Groundwork landed in skunkBat `b708872` |
| ~~DEPOT-POPULATE~~ | flockGate local |
| ~~GATE-NAME-ENV~~ | flockGate local |
| ~~NAPI-IRONGATE~~ | ironGate overwatch |
| ~~SYSTEMD-UMASK~~ | ironGate overwatch |

### Discussion items (all teams)

| # | ID | What |
|---|-----|------|
| 9 | **VERSION-SKEW** | 3 version ranges. Coordinate strategy. |
| 10 | **CERT-OWNER** | Certificate owner `loamspine` vs `beardog`. |
| 11 | **PEPTI-TARGETS** | Missing depot targets. |

---

## Status

### Tests: 4,000+ / 0 fail

| Suite | Tests | Status |
|-------|-------|--------|
| primalSpring | 1,131 (141 scenarios) | GREEN |
| cellMembrane | 1,024 | GREEN |
| groundSpring | 1,047+ | GREEN |
| nestGate | 3,790 (73 ignored) | GREEN |
| skunkBat | 567 (+4) | GREEN |
| projectNUCLEUS | 149 (26/26) | GREEN |
| footPrint | 46 | GREEN |

### Mesh: Full bidirectional (pending eastGate songBird upgrade)

```
eastGate ↔ golgi ↔ ironGate + southGate  (LAN, <1ms)
sporeGate ↔ golgi                        (WG, bidirectional, 30ms)
flockGate → 4 overlay peers              (WG, 31ms)
grapheneGate                             (TCP-only, Tower)
```

### Forgejo: RESOLVED — all 20 repos full-depth on golgi

### Gate Status

```
eastGate     — Overwatch. Neural API live 24d. songBird upgrade pending.
sporeGate    — NUCLEUS hub. Neural API systemd. Depot signed. Forgejo authority.
golgiBody    — Full mirror (no longer shallow). sporePrint + footPrint live. Auto-publishing heads.
flockGate    — footPrint owner. Mesh resolved. WAN validated.
ironGate     — Node atomic. Own overwatch agent.
```

---

## Active Handoffs

| Document | Status |
|----------|--------|
| `SHALLOW_PINGPONG_RESOLUTION_AAR_137b.md` | **NEW** — 20 repos full-depth, thin relay retired |
| `NESTGATE_FP_PERSIST_WAVE137b_JUL12_2026.md` | **NEW** — CAS persistence, 5 RPC methods |
| `NAPI_SYSTEMD_MESH_DEPLOY_AAR_137b.md` | Phase 1 complete (absorbed) |
| `NEURAL_API_LIVE_AAR_137b.md` | Phase 1 complete (absorbed) |
| `CELLMEMBRANE_NAPI_PERMS_DEEP_DEBT_AAR_137b.md` | Done |

---

*Wave 137b: 20/28 debt items resolved. 8 remain (1 critical, 2 high, 2 medium, 3 discussion). Phase 1 at 11/12 — only NAPI-LIFECYCLE left. Forgejo shallow relay permanently fixed. UDS-HTTP mesh protocol fixed. nestGate CAS persistence live. 4,000+ tests / 0 fail. Teams are converging.*
