# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 11:15 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PHASE 1 COMPLETE. 3-GATE MESH LIVE.** eastGate songBird deployed. sporeGate sprint resolved STALE-PEER + FORGEJO-PERMS + DEPOT-POLICY (`require-signed` system-wide). primalSpring active local evolution (76 LOC, 6 scenarios). 7,750+ tests / 0 fail.

---

## Remaining — by team

### biomeOS team — 3 items

| ID | What | Effort |
|----|------|--------|
| **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Last piece for full lifecycle authority. | 4-8hr |
| **SOCKET-DIR-UNIFY** | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation (hardcoded `/var/run/biomeos/`, actual varies by gate). | 2-4hr |
| **SOCKET-UMASK** | Primals should `fchmod` sockets after bind. | 2hr |

### songBird team — 2 items

| ID | What | Effort |
|----|------|--------|
| **DRAWBRIDGE-CAP** | Drawbridge routes not advertising as capabilities. `capabilities.list` shows 15 native caps, zero drawbridge caps. Blocks `capability.call` for drawbridge services. | 2-4hr |
| **SONGBIRD-LOCAL** | Local drawbridge cleanup (header parsing, dead constant) — 1 file dirty, 27 ins / 129 del. Commit + push. | 30min |

### sporeGate / golgi team — 1 item

| ID | What | Effort |
|----|------|--------|
| **DEPOT-CHECKSUM** | Depot binary BLAKE3 doesn't match `checksums.toml`. Binary is unstripped (26.6MB), checksums were likely signed against stripped build. `RequireSigned` (now active) will reject. Re-harvest: strip → checksum → sign → sync. | 30min |

*Resolved this wave*: ~~STALE-PEER~~ (mesh re-init, ghost eliminated), ~~FORGEJO-PERMS~~ (`chown -R git:git` on 21 repos), ~~DEPOT-POLICY~~ (`require-signed` set system-wide).

### cellMembrane team — 1 item

| ID | What | Effort |
|----|------|--------|
| **FETCH-PATH** | **NEW.** `plasmid.fetch` creates doubled nested path (`primals/x86_64/primals/x86_64/`). Doesn't match systemd template `ExecStart` path. Manual binary placement required on eastGate. | 1-2hr |

### flockGate team — 1 item

| ID | What | Effort |
|----|------|--------|
| **FP-API-CADDY** | Caddy config for footPrint GIS proxy (10 HTTPS hosts). Bypasses SOCKET-DIR-UNIFY. | 1-2hr |

### Operator (REALWORLD) — 1 item

| ID | What | Effort |
|----|------|--------|
| **LIVE-DNS** | Cloudflare DNS: `A live → 157.230.3.183` (grey cloud). Then reload Caddy on golgi. | 5min |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot targets: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Gate Status

```
eastGate     — Overwatch. songBird LIVE (v0.2.1, 2 peers). Neural API 24d. All tasks DONE.
sporeGate    — NUCLEUS. petalTongue :9900. STALE-PEER+FORGEJO-PERMS+DEPOT-POLICY resolved. Depot re-sign needed.
golgiBody    — Full mirror. Forgejo perms fixed. sporePrint + footPrint live. Caddy block ready.
flockGate    — JupyterHub data plane proven. FP-API Caddy next.
ironGate     — Node atomic. Own overwatch agent.
```

**Active Handoffs**: `SONGBIRD_EASTGATE_DEPLOY_AAR_137b.md`, `SPOREGATE_GOLGI_SPRINT_AAR_137b.md`, `DRAWBRIDGE_WEAK_BOND_PATTERN_AAR_137b.md`, `FLOCKGATE_WAN_OVERWATCH_AAR_137b.md`

---

*Wave 137b: Phase 1 COMPLETE. 3-gate mesh live. 9 items remain across 6 teams + 3 discussion. sporeGate sprint closed 3 more. 7,750+ tests / 0 fail.*
