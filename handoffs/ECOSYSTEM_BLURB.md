# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 08:20 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **CONVERGING.** 21/28 debt resolved. Phase 1 at 11/12. petalTongue TOPO-VIS evolution in progress (87 LOC dirty). Depot trust model gap identified (SIGN-VERIFY-ON-FETCH). Agent content parity AAR absorbed. 7,750+ tests / 0 fail.

---

## Remaining — 9 action items + 3 discussion

### biomeOS — 3 items (1 CRITICAL)

| ID | What | Effort |
|----|------|--------|
| **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. **Last CRITICAL.** Blocks Neural API authority. | 4-8hr |
| **SOCKET-DIR-UNIFY** | Unify 3 socket dirs → `/run/membrane/` only. | 2-4hr |
| **SOCKET-UMASK** | Primals should `fchmod` sockets after bind. | 2hr |

### cellMembrane — 1 item (pre-SHOW-HN)

| ID | What | Effort |
|----|------|--------|
| **SIGN-VERIFY-ON-FETCH** | `plasmid.fetch` must verify `signatures.toml` (Ed25519 via bearDog) before deploying binaries. Currently: fetch → deploy. Required: fetch → verify → deploy (reject unsigned). The depot is intentionally public (defense = math, not obscurity). The trust chain is: `public depot (HTTPS) → SIGN-01 verify → deploy → riboCipher IPC`. The missing link is the verify step on fetch. | 4-8hr |

### sporeGate — 2 items

| ID | What | Effort |
|----|------|--------|
| **DEPOT-REFRESH** | `plasmid.harvest` songBird — depot binary is from Jul 9, missing UDS-HTTP fix (Jul 12) and mesh port fix. Blocks SONGBIRD-EASTGATE. | 30min |
| **LIVE-ACTIVATE** | Stand up `live.primals.eco` — petalTongue NUCLEUS on sporeGate. | 4-8hr |

### songBird + flockGate — 1 item

| ID | What | Effort |
|----|------|--------|
| **FP-API** | Wire footPrint `/api/proxy?url=` through drawbridge. Allowlist landed. Caddy rewrite or client migration. | 2-4hr |

### petalTongue — 1 item (IN PROGRESS)

| ID | What | Effort |
|----|------|--------|
| **TOPO-VIS** | Live topology viz via Neural API. **Active evolution** — 11 files dirty, neural_api_provider/parse.rs + web_mode/handlers.rs + index.html being wired. | 8-16hr |

### eastGate (self) — 1 item

| ID | What | Effort |
|----|------|--------|
| **SONGBIRD-EASTGATE** | Deploy songBird with UDS-HTTP fix. **BLOCKED** on DEPOT-REFRESH. | blocked |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Depot Trust Model (for reference)

```
Public depot (HTTPS)  →  SIGN-01 verify  →  deploy to /run/membrane/  →  riboCipher IPC
    anyone can pull       math proves who      local trust boundary       runtime auth
                          built it
```

- **Depot** is intentionally public — like apt/cargo/npm. Defense = mathematics, not obscurity.
- **SIGN-01** provides Ed25519 signatures in `signatures.toml` — proves sporeGate built those bytes.
- **SIGN-VERIFY-ON-FETCH** is the missing link: `plasmid.fetch` currently skips verification.
- **riboCipher** authenticates post-deployment IPC on UDS sockets. Separate from depot trust.
- **MacGuffin test**: if you can't show the whole depot publicly and still be secure, it's a MacGuffin.

---

## Wave 137b Delivery Log (21 items)

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
| ~~THREAT-ACTIVATE~~ | skunkBat | `b708872` + SKUNKY-LIVE prep + CF-DATA |
| ~~DEPLOY-DISPATCH-XGATE~~ | cellMembrane | `d5506a3` |
| ~~TIER-PRIORITY~~ | projectNUCLEUS | `ea57d6a` |
| ~~SPORE-OWNERSHIP~~ | eastGate | `SPORE_OWNERSHIP_MATRIX.md` created |

---

## Status

**7,750+ tests / 0 fail** | **Mesh**: bidirectional | **Forgejo**: full-depth (20 repos)

```
eastGate     — Overwatch. Neural API 24d. songBird blocked on depot.
sporeGate    — NUCLEUS. Neural API systemd. Depot signed. Forgejo authority.
golgiBody    — Full mirror. sporePrint + footPrint live. Auto-publishing heads.
flockGate    — footPrint owner. Mesh resolved. WAN validated.
ironGate     — Node atomic. Own overwatch agent.
petalTongue  — TOPO-VIS active evolution (11 files, 87 LOC).
sporePrint   — Content evolution + SHOW_HN_PUBLICATION.md drafted.
```

**Active Handoffs**: `SHALLOW_PINGPONG_RESOLUTION_AAR_137b.md`, `NESTGATE_FP_PERSIST_WAVE137b_JUL12_2026.md`, `AGENT_PARITY_AAR_137b.md`

---

*Wave 137b: 21 delivered, 9 remain + 3 discussion. 1 critical (NAPI-LIFECYCLE). New: SIGN-VERIFY-ON-FETCH (depot trust model gap). petalTongue TOPO-VIS in active evolution. sporePrint drafting SHOW-HN publication. 7,750+ tests / 0 fail.*
