# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 17:00 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** `*.primals.eco` wildcard DNS active — Caddy is sole routing authority. FP-API GIS proxy live (10 hosts). All repos clean. 3 items remain + 3 discussion. 7,750+ tests / 0 fail.

---

## Remaining — 3 items + 3 discussion

### P1

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **DRAWBRIDGE-CAP** | songBird | Drawbridge routes not advertising as capabilities. Blocks `capability.call` for bridged services. | 2-4hr |
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. Last piece for lifecycle authority. | 4-8hr |

### P2

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation for HTTPS outbound. | 2-4hr |

### Discussion

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Harmonization strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. Cosmetic but confusing. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Wave 137b Closures (today)

| Item | Resolved By |
|------|-------------|
| ~~DNS-WILDCARD~~ | Operator — `*.primals.eco` wildcard A record, 5 individual records removed |
| ~~FP-API-CADDY-DEPLOY~~ | sporeGate — 10 GIS proxy routes live via Caddy snippet, CSP tightened |
| ~~SONGBIRD-LOCAL~~ | songBird — drawbridge cleanup absorbed + `to_lowercase()` elimination (17 files) |
| ~~DEPOT-CHECKSUM~~ | sporeGate — jellyfish triage, native BLAKE3, depot restructured |
| ~~STALE-PEER~~ | sporeGate — mesh re-initialized |
| ~~FORGEJO-PERMS~~ | sporeGate — `chown -R git:git` on 21 repos |
| ~~DEPOT-POLICY~~ | sporeGate — `require-signed` system-wide |
| ~~SONGBIRD-EASTGATE~~ | eastGate — deployed from depot, mesh live (2 peers) |
| ~~LIVE-DNS~~ | sporeGate — `live.primals.eco` serving TOPO-VIS |

---

## Domain Identity (documented this wave)

- **`primals.eco`** — ecosystem platform (depot, forge, compositions, public tools)
- **`primal.eco`** — personal sovereign substrate (sporePrint site, mesh API, HPC)
- **`nestgate.io`** — federated data gateway (CAS backbone, drawbridge weak bonds for NCBI, PubMed, USGS, etc.)

Wildcard `*.primals.eco` → Caddy routing. New subdomains need only a Caddy block.

---

## Gate Status

```
eastGate     — Overwatch. 13 primals. songBird v0.2.1 (2 peers). All tasks DONE.
sporeGate    — NUCLEUS. live.primals.eco + FP-API GIS proxy live. Depot 35/35. Jellyfish triaged.
golgiBody    — Full mirror. Wildcard DNS. FP-API Caddy deployed. Forgejo healthy.
flockGate    — 144 scenarios / 1,190 tests. footPrint wiring handoff active.
ironGate     — Node atomic. Own overwatch.
```

**Active Handoffs**: `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md`, `FOOTPRINT_PRIMAL_WIRING_HANDOFF_137b.md`

---

*Wave 137b: 3 items remain + 3 discussion. DNS wildcard active. FP-API GIS proxy live. Domain identity separation documented. All repos clean. 7,750+ tests / 0 fail.*
