# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 10:35 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PHASE 1 COMPLETE.** Neural API deployment authority: 12/12. 26+ debt items delivered. Depot trust chain verified (SIGN-01 + SIGN-VERIFY-ON-FETCH). petalTongue NUCLEUS live on sporeGate:9900 awaiting DNS. Drawbridge weak bond pattern formalized. 7,750+ tests / 0 fail.

---

## Remaining — by team

### biomeOS team — 3 items

| ID | What | Effort |
|----|------|--------|
| **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Last piece for full lifecycle authority. | 4-8hr |
| **SOCKET-DIR-UNIFY** | Unify socket dirs → `/run/membrane/` only. Also unblocks songBird TLS delegation (hardcoded to `/var/run/biomeos/` but actual path is `/run/membrane/`). | 2-4hr |
| **SOCKET-UMASK** | Primals should `fchmod` sockets after bind. | 2hr |

### songBird team — 2 items

| ID | What | Effort |
|----|------|--------|
| **DRAWBRIDGE-CAP** | Drawbridge routes not advertising as capabilities. sporeGate's `capabilities.list` shows 15 native caps but no drawbridge-provided caps (e.g. `jupyter`). Env var `SONGBIRD_DRAWBRIDGE_ROUTES` may be set but routes aren't registering. Blocks `capability.call` for drawbridge services. | 2-4hr |
| **SONGBIRD-LOCAL** | Local drawbridge cleanup (header parsing, dead constant) needs commit + push. 1 file dirty, 27 ins / 129 del. | 30min |

### sporeGate / golgi team — 3 items

| ID | What | Effort |
|----|------|--------|
| **STALE-PEER** | Ghost peer `10.13.37.0:8080` (pre-port-fix) in sporeGate's mesh. `mesh.remove_peer` or songBird restart. Wastes time in `capability.call` routing. | 15min |
| **FORGEJO-PERMS** | Forgejo on golgi has file permission errors (`unable to write file ./objects/…: Permission denied`). Blocks push alignment to forgejo remote. Origin (GitHub) unaffected. | 30min |
| **DEPOT-POLICY** | Promote depot trust default from `VerifyIfPresent` → `RequireSigned` in gate systemd units. Code is ready (`89bf12f`), just a config decision. | 15min |

### flockGate team — 1 item

| ID | What | Effort |
|----|------|--------|
| **FP-API-CADDY** | Draft Caddy config snippet for footPrint GIS proxy route (10 HTTPS hosts). Caddy handles TLS natively — bypasses SOCKET-DIR-UNIFY blocker. Once live, footPrint has full GIS at `primals.eco/footprint/`. | 1-2hr |

### eastGate (self) — 1 item

| ID | What | Effort |
|----|------|--------|
| **SONGBIRD-EASTGATE** | Deploy songBird `74cf7101` from pepti depot. Unblocked since Jul 13 DEPOT-REFRESH. | 30min |

### Operator (REALWORLD) — 1 item

| ID | What | Effort |
|----|------|--------|
| **LIVE-DNS** | Add Cloudflare DNS: `A live → 157.230.3.183` (grey cloud for ACME HTTP-01). Then reload Caddy on golgi. petalTongue NUCLEUS + Caddy block already configured on both sides. | 5min |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot targets: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Gate Status

```
eastGate     — Overwatch. Neural API 24d. songBird upgrade ready.
sporeGate    — NUCLEUS. Neural API systemd. petalTongue :9900. Depot signed+refreshed.
golgiBody    — Full mirror (20 repos). sporePrint + footPrint live. Forgejo perms issue.
flockGate    — JupyterHub data plane proven (202ms WAN). FP-API Caddy next.
ironGate     — Node atomic. Own overwatch agent. JupyterHub v5.4.5 reachable.
```

**Active Handoffs**: `DRAWBRIDGE_WEAK_BOND_PATTERN_AAR_137b.md`, `FLOCKGATE_WAN_OVERWATCH_AAR_137b.md`

---

*Wave 137b: Phase 1 COMPLETE. 11 items remain across 6 teams + 3 discussion. All are independently actionable — no cross-team blockers except SOCKET-DIR-UNIFY (biomeOS) which unblocks songBird TLS. 7,750+ tests / 0 fail.*
