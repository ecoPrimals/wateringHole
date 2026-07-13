# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 12, 2026 15:00 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **NEURAL API LIVE. MESH BIDIRECTIONAL. DEPOT SIGNED.** Phase 1 at 10/12. 3,960+ tests / 0 fail. 40 repos synced. Full debt inventory below — clear by end of wave.

---

## What Landed (137a-b)

- Neural API **LIVE on sporeGate** — systemd service, 48 primals discovered, capability routing verified
- Neural API **LIVE on eastGate** — 23+ days continuous
- SIGN-01 **E2E verified** — `sign.activate → beardog.sock → Ed25519 → sign.verify PASS`
- songBird `f05918a` deployed to **sporeGate + golgi + flockGate** — bidirectional WG mesh live
- footPrint **LIVE** at `primals.eco/footprint/` (114ms from WAN NYC)
- skunky-ingest **deployed** on golgi (dry-run mode)
- cellMembrane systemd UMask fix **permanent** — all future gate bootstraps socket-accessible
- ironGate **workspace split** — projectNUCLEUS = code only, new ironGate overwatch = hardware + deploys
- primalSpring at **141 scenarios / 1,131 tests**
- Forgejo parity restored (7 repos pushed)

---

## Your Team's Actions

### biomeOS team

| # | ID | What | Effort |
|---|-----|------|--------|
| 1 | **NAPI-LIFECYCLE** | LifecycleManager registration — `lifecycle.status` returns count=0. Primals aren't registering lifecycle hooks. CRITICAL for WAN E2E. | 4-8hr |
| 2 | **SOCKET-DIR-UNIFY** | Unify `/run/membrane/`, `/run/biomeos-root/`, `/run/biomeos-default/` → single `/run/membrane/`. Currently bridged by ExecStartPre symlinks. | 2-4hr |
| 3 | **SOCKET-UMASK** | Primals should `fchmod` sockets after bind (not rely on systemd UMask). | 2hr |

### cellMembrane team

| # | ID | What | Effort |
|---|-----|------|--------|
| 4 | **BRIDGE-ERROR-PROP** | NeuralBridge should propagate Neural API errors instead of falling through silently. | 2hr |
| 5 | **DEPLOY-DISPATCH-XGATE** | `deploy_dispatch.rs` cross-gate routing still uses `capability.call` envelope — needs dotted method alignment. | 1hr |
| 6 | **TIER-PRIORITY** | 7 compositions have tier priority = None. Fill in. | 30min |

### songBird team

| # | ID | What | Effort |
|---|-----|------|--------|
| 7 | **UDS-HTTP-PROTOCOL** | UDS mesh engine can't register HTTP federation peers. `peer.connect` TCP succeeds but `mesh.peers` stays empty. CRITICAL for WAN `capability.call`. | 4-8hr |
| 8 | **FP-API** | Wire footPrint `/api/proxy?url=` through drawbridge. 10-host allowlist already landed (`87b7779`). Caddy rewrite (quickfix) or client-side migration. | 2-4hr |

### skunkBat team

| # | ID | What | Effort |
|---|-----|------|--------|
| 9 | **SKUNKY-LIVE** | Remove `--dry-run` from skunky-ingest on golgi. Requires `baseline.observe` listener. | 2-4hr |
| 10 | **THREAT-ACTIVATE** | Feed 122 real attacker IPs (SSH brute-force, HTTP scanning) into `baseline.observe`. Replace synthetic seed data. | 2hr |
| 11 | **CF-DATA** | Pull Cloudflare analytics → outer→inner data flow for detection correlation. | 2-4hr |

### sporeGate / golgi team

| # | ID | What | Effort |
|---|-----|------|--------|
| 12 | **DRAWBRIDGE-ROUTES** | Confirm `SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter` is set. `jupyter` cap not in mesh.status. | 30min |
| 13 | **LIVE-ACTIVATE** | Stand up `live.primals.eco` — petalTongue NUCLEUS on sporeGate. | 4-8hr |

### nestGate team

| # | ID | What | Effort |
|---|-----|------|--------|
| 14 | **FP-PERSIST** | Replace footPrint Express CRUD (`/api/projects`) with CAS persistence. Content-addressed, rootPulse-traced. | 4-8hr |

### petalTongue team

| # | ID | What | Effort |
|---|-----|------|--------|
| 15 | **TOPO-VIS** | Live topology visualization — consume `topology.primals` + `routing_weights` from Neural API (not hardcoded). | 8-16hr |

### flockGate overwatch

| # | ID | What | Effort |
|---|-----|------|--------|
| 16 | **DEPOT-POPULATE** | Local depot has 0/13 primals. `plasmid fetch` or manual sync from pepti. | 30min |
| 17 | **GATE-NAME-ENV** | Set `GATE_NAME=flockGate` in shell profile. | 2min |

### eastGate overwatch (self)

| # | ID | What | Effort |
|---|-----|------|--------|
| 18 | **SONGBIRD-EASTGATE** | Deploy songBird `f05918a` for full bidirectional mesh. | 30min |
| 19 | **SPORE-OWNERSHIP** | Create `SPORE_OWNERSHIP_MATRIX.md` — document nestGate/rhizoCrypt/sweetGrass split. | 1hr |

### projectNUCLEUS (code only)

| # | ID | What | Effort |
|---|-----|------|--------|
| 20 | **NUCLEUS-MATRIX** | Define columns U/V/W in validation matrix — spore ingest/emit/profile. | 1hr |
| 21 | **BOND-METADATA** | Add `bond_type` to all 16 deployment graphs. | 2hr |

### ironGate overwatch (new agent)

| # | ID | What | Effort |
|---|-----|------|--------|
| 22 | **NAPI-IRONGATE** | Deploy songBird `f05918a` + start `biomeos neural-api` on ironGate. | 1hr |
| 23 | **SYSTEMD-UMASK** | Regenerate systemd units with new UMask via `membrane gate.bootstrap`. | 30min |

### cellMembrane / sporeGate — Forgejo Relay

| # | ID | What | Effort |
|---|-----|------|--------|
| 24 | **SHALLOW-PINGPONG** | Shallow Forgejo relay (depth=1 bare repos on golgi) causes SHA divergence on every rebase — burns cycles every cascade (7 repos affected). **Fix: move Forgejo authority to sporeGate** (full-depth repos, build authority). golgi becomes a thin read-only mirror that syncs from sporeGate — provides async WAN access without VPN (flockGate pushes in from outside, internal teams work from within). golgi Forgejo stays up as a mirror endpoint, but sporeGate is the source of truth. | 2-4hr |

### Discussion items (all teams)

| # | ID | What |
|---|-----|------|
| 25 | **VERSION-SKEW** | 3 distinct version ranges (0.1-0.2, 0.4-0.9, 0.14). Coordinate a versioning strategy. |
| 26 | **SHADER-SUPPORT** | `shader.list` / `trust.list` in capability_registry but no impl. Keep or remove? |
| 27 | **CERT-OWNER** | Certificate owner shows `loamspine`, expected `beardog`. Clarify. |
| 28 | **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Status

### 3,960+ tests / 0 fail

| Suite | Tests | Status |
|-------|-------|--------|
| primalSpring | 1,131 (141 scenarios) | GREEN |
| cellMembrane | 1,024 | GREEN |
| groundSpring | 1,047+ | GREEN |
| skunkBat | 563 | GREEN |
| projectNUCLEUS | 149 (26/26) | GREEN |
| footPrint | 46 | GREEN |

### Mesh Topology

```
eastGate ↔ golgi ↔ ironGate + southGate  (LAN, <1ms)
sporeGate ↔ golgi                        (WG, bidirectional, 30ms)
flockGate → 4 overlay peers              (WG, 31ms, bidirectional pending eastGate)
grapheneGate                             (TCP-only, Tower)
```

### Gate Status

```
eastGate     — Overwatch. Neural API live 23d. songBird upgrade pending.
sporeGate    — NUCLEUS hub. Neural API systemd. Mesh bidirectional. Depot signed.
golgiBody    — Thin relay. sporePrint + footPrint serving. Mesh bidirectional.
flockGate    — footPrint owner. 4 overlay peers. WAN validated.
ironGate     — Node atomic. New overwatch agent. projectNUCLEUS = code only.
strandGate   — REALWORLD: physical access.
grapheneGate — Tower live. REALWORLD: ADB.
```

---

*Wave 137b: 10/12 Phase 1 done. 28 items remain across 11 teams. 3 critical, 8 high, 5 medium, 4 discussion. Clear by end of wave.*
