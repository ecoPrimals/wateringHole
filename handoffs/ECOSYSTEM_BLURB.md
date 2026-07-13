# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 09:50 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **NEAR COMPLETE.** 26/28 original debt resolved + 3 new items landed and resolved. LIVE-ACTIVATE done (petalTongue NUCLEUS on sporeGate:9900, Caddy block ready, awaiting DNS). DEPOT-REFRESH done (songBird `74cf7101` in depot). SIGN-VERIFY-ON-FETCH already implemented in cellMembrane (`VerifyIfPresent` default). FP-API superseded by drawbridge weak bond pattern. Phase 1: 12/12 COMPLETE.

---

## Phase 1: COMPLETE (12/12)

All Neural API deployment authority items resolved. No CRITICAL items remain.

---

## Remaining — 5 action items + 3 discussion

### biomeOS — 3 items

| ID | What | Effort |
|----|------|--------|
| **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Blocks full lifecycle authority but no longer CRITICAL (Neural API routes all other capabilities). | 4-8hr |
| **SOCKET-DIR-UNIFY** | Unify 3 socket dirs → `/run/membrane/` only. | 2-4hr |
| **SOCKET-UMASK** | Primals should `fchmod` sockets after bind. | 2hr |

### eastGate (self) — 1 item (UNBLOCKED)

| ID | What | Effort |
|----|------|--------|
| **SONGBIRD-EASTGATE** | Deploy songBird `74cf7101` from pepti depot. **UNBLOCKED** — depot refreshed Jul 13. | 30min |

### Operator — 1 item (REALWORLD)

| ID | What | Effort |
|----|------|--------|
| **LIVE-DNS** | Add Cloudflare DNS `A live → 157.230.3.183` (grey cloud for ACME). Then reload Caddy on golgi. petalTongue NUCLEUS + Caddy block already configured. | 5min |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges. Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Wave 137b Delivery Log (26+ items)

| ID | Resolved By | Commit/AAR |
|----|-------------|------------|
| ~~NAPI-MEMBRANE~~ | cellMembrane | `1df1cfe` |
| ~~SIGN-01~~ | cellMembrane + sporeGate | `471ebf5` — E2E verified |
| ~~FP-DEPLOY~~ | sporeGate | primals.eco/footprint/ live |
| ~~SKUNKY-DEPLOY~~ | sporeGate | dry-run on golgi |
| ~~NAPI-START~~ | sporeGate | 48 primals, 156 translations |
| ~~NAPI-PERMS~~ | cellMembrane + sporeGate | `d5474df` — systemd UMask |
| ~~FLOCKGATE-MESH~~ | songBird | `f05918a` — port 8080→7700 |
| ~~NAPI-SYSTEMD~~ | sporeGate | `membrane-neural-api.service` |
| ~~NAPI-CROSS-GATE~~ | sporeGate | songBird to sporeGate + golgi |
| ~~GOLGI-WG-BIND~~ | golgi | `0.0.0.0:7700` |
| ~~UDS-HTTP-PROTOCOL~~ | songBird | `0d2895b5` |
| ~~FP-PERSIST~~ | nestGate | `88dc4fa2` — CAS, 5 RPC methods |
| ~~SHALLOW-PINGPONG~~ | sporeGate/golgi | 20 repos full-depth |
| ~~DRAWBRIDGE-ROUTES~~ | sporeGate | Confirmed |
| ~~BRIDGE-ERROR-PROP~~ | cellMembrane | `d5506a3` |
| ~~NUCLEUS-MATRIX~~ | projectNUCLEUS | `ea57d6a` |
| ~~BOND-METADATA~~ | projectNUCLEUS | `ea57d6a` |
| ~~THREAT-ACTIVATE~~ | skunkBat | `b708872` |
| ~~DEPLOY-DISPATCH-XGATE~~ | cellMembrane | `d5506a3` |
| ~~TIER-PRIORITY~~ | projectNUCLEUS | `ea57d6a` |
| ~~SPORE-OWNERSHIP~~ | eastGate | `SPORE_OWNERSHIP_MATRIX.md` |
| ~~SIGN-VERIFY-ON-FETCH~~ | cellMembrane | `89bf12f` — already implemented, `VerifyIfPresent` default |
| ~~DEPOT-REFRESH~~ | sporeGate | songBird `74cf7101` + petalTongue `d79f096` built, signed, synced |
| ~~LIVE-ACTIVATE~~ | sporeGate | petalTongue NUCLEUS on :9900, Caddy block configured |
| ~~FP-API~~ | flockGate | Superseded by drawbridge weak bond pattern |
| ~~AGENT-PARITY~~ | sporePrint | `llms.txt` self-identification + validate_agent_parity.sh |

---

## Depot Trust Model — VERIFIED

```
Public depot (HTTPS)  →  SIGN-01 verify  →  deploy to /run/membrane/  →  riboCipher IPC
    anyone can pull       VerifyIfPresent      local trust boundary       runtime auth
```

cellMembrane `89bf12f` confirms the chain is implemented: `plasmid.fetch` → fetch `signatures.toml` → `verify_depot_with_policy()` → download binaries. Default policy `VerifyIfPresent` verifies when signatures exist (they do since SIGN-01). Promote to `RequireSigned` for full lockdown.

---

## Status

**7,750+ tests / 0 fail** | **Phase 1: COMPLETE** | **Forgejo: full-depth**

```
eastGate     — Overwatch. Neural API 24d. songBird upgrade unblocked.
sporeGate    — NUCLEUS. Neural API systemd. petalTongue NUCLEUS :9900. Depot signed+refreshed.
golgiBody    — Full mirror. sporePrint + footPrint live. live.primals.eco Caddy block ready.
flockGate    — footPrint owner. JupyterHub data plane proven. Drawbridge weak bond pattern.
ironGate     — Node atomic. Own overwatch agent.
```

**Active Handoffs**: `LIVE_ACTIVATE_AAR_137b.md`, `DRAWBRIDGE_WEAK_BOND_PATTERN_AAR_137b.md`, `FLOCKGATE_WAN_OVERWATCH_AAR_137b.md`, `FP_API_WIRING_WAVE137b.md`

---

*Wave 137b: Phase 1 COMPLETE (12/12). 26+ items delivered. 5 remain + 3 discussion. petalTongue NUCLEUS live on sporeGate awaiting DNS. Depot trust chain verified. Drawbridge weak bond pattern formalized. SHOW-HN publication drafted. 7,750+ tests / 0 fail.*
