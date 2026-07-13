# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 08:05 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **CONVERGING.** 20/28 debt items resolved. Phase 1 at 11/12. Neural API live on 2 gates. Mesh bidirectional. Depot signed. Forgejo full-depth. 7,750+ tests / 0 fail.

---

## Remaining — 8 action items + 3 discussion

### biomeOS — 3 items (1 CRITICAL)

| ID | What | Effort |
|----|------|--------|
| **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. **Last CRITICAL item.** Blocks full Neural API authority. | 4-8hr |
| **SOCKET-DIR-UNIFY** | Unify 3 socket dirs → `/run/membrane/` only. Currently bridged by ExecStartPre symlinks. | 2-4hr |
| **SOCKET-UMASK** | Primals should `fchmod` sockets after bind (not rely on systemd UMask band-aid). | 2hr |

### songBird + flockGate — 1 item

| ID | What | Effort |
|----|------|--------|
| **FP-API** | Wire footPrint `/api/proxy?url=` through drawbridge. Allowlist landed (`87b7779`). Caddy rewrite (quickfix) or client migration (clean). | 2-4hr |

### sporeGate — 1 item

| ID | What | Effort |
|----|------|--------|
| **LIVE-ACTIVATE** | Stand up `live.primals.eco` — petalTongue NUCLEUS on sporeGate. | 4-8hr |

### petalTongue — 1 item

| ID | What | Effort |
|----|------|--------|
| **TOPO-VIS** | Live topology viz — consume `topology.primals` + `routing_weights` from Neural API. | 8-16hr |

### eastGate (self) — 2 items

| ID | What | Effort |
|----|------|--------|
| **SONGBIRD-EASTGATE** | Deploy songBird `0d2895b5` (includes UDS-HTTP fix). | 30min |
| **SPORE-OWNERSHIP** | Create `SPORE_OWNERSHIP_MATRIX.md` — nestGate/rhizoCrypt/sweetGrass. | 1hr |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Wave 137b Delivery Log

| ID | Resolved By | Commit |
|----|-------------|--------|
| ~~NAPI-MEMBRANE~~ | cellMembrane | `1df1cfe` |
| ~~SIGN-01~~ | cellMembrane + sporeGate | `471ebf5` — E2E verified |
| ~~FP-DEPLOY~~ | sporeGate | primals.eco/footprint/ live (114ms WAN) |
| ~~SKUNKY-DEPLOY~~ | sporeGate | dry-run on golgi |
| ~~NAPI-START~~ | sporeGate | 48 primals, 156 translations |
| ~~NAPI-PERMS~~ | cellMembrane + sporeGate | `d5474df` — systemd UMask permanent |
| ~~FLOCKGATE-MESH~~ | songBird | `f05918a` — port 8080→7700 |
| ~~NAPI-SYSTEMD~~ | sporeGate | `membrane-neural-api.service` |
| ~~NAPI-CROSS-GATE~~ | sporeGate | songBird deployed to sporeGate + golgi |
| ~~GOLGI-WG-BIND~~ | golgi | `0.0.0.0:7700` |
| ~~UDS-HTTP-PROTOCOL~~ | songBird | `0d2895b5` — peers register in BeaconMesh |
| ~~FP-PERSIST~~ | nestGate | `88dc4fa2` — CAS persistence, 5 RPC methods |
| ~~SHALLOW-PINGPONG~~ | sporeGate/golgi | 20 repos full-depth, thin relay retired |
| ~~DRAWBRIDGE-ROUTES~~ | sporeGate | Confirmed operational |
| ~~BRIDGE-ERROR-PROP~~ | cellMembrane | `d5506a3` |
| ~~NUCLEUS-MATRIX~~ | projectNUCLEUS | `ea57d6a` — U/V/W defined |
| ~~BOND-METADATA~~ | projectNUCLEUS | `ea57d6a` — 19 graphs |
| ~~THREAT-ACTIVATE~~ | skunkBat | `b708872` + SKUNKY-LIVE prep + CF-DATA groundwork |
| ~~DEPLOY-DISPATCH-XGATE~~ | cellMembrane | `d5506a3` |
| ~~TIER-PRIORITY~~ | projectNUCLEUS | `ea57d6a` |

---

## Status

**7,750+ tests / 0 fail**

| Suite | Tests | Status |
|-------|-------|--------|
| nestGate | 3,790 | GREEN |
| primalSpring | 1,131 (141 scenarios) | GREEN |
| cellMembrane | 1,024 | GREEN |
| groundSpring | 1,047+ | GREEN |
| skunkBat | 567 | GREEN |
| projectNUCLEUS | 149 (26/26) | GREEN |
| footPrint | 46 | GREEN |

**Mesh**: Bidirectional (sporeGate ↔ golgi ↔ LAN gates). flockGate → 4 WG peers. eastGate songBird upgrade pending.

**Gates**:
```
eastGate     — Overwatch. Neural API 24d. songBird upgrade pending.
sporeGate    — NUCLEUS. Neural API systemd. Depot signed. Forgejo authority.
golgiBody    — Full mirror. sporePrint + footPrint live. Auto-publishing heads.
flockGate    — footPrint owner. Mesh resolved. WAN validated.
ironGate     — Node atomic. Own overwatch agent.
```

**Active Handoffs**: `SHALLOW_PINGPONG_RESOLUTION_AAR_137b.md`, `NESTGATE_FP_PERSIST_WAVE137b_JUL12_2026.md`

---

*Wave 137b: 20 items delivered by 7 teams. 8 remain + 3 discussion. 1 critical (NAPI-LIFECYCLE). Neural API live on 2 gates. Forgejo fixed. Mesh bidirectional. CAS persistence live. 7,750+ tests / 0 fail.*
