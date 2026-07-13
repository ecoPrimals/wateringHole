# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 17:50 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** DRAWBRIDGE-CAP resolved (songBird). ironGate redeployed (14 binaries, 0 crash loops). 2 items remain + 4 new from ironGate triage. 7,750+ tests / 0 fail.

---

## Remaining — 2 original + 4 new

### P1

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. Last piece for lifecycle authority. | 4-8hr |

### P2

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation. | 2-4hr |
| **BIOMEOS-TEMPLATE** | cellMembrane | `membrane-nucleus@.service` assumes `server` subcommand — biomeOS doesn't have one. Needs alias or template exclusion. | 1-2hr |
| **STALE-PEERS** | wateringHole | Gate head files (golgi 154hrs, sporeGate 68hrs stale) not refreshed by cascade. | 2hr |
| **ROGUE-BIN-PATH** | ironGate ops | `/usr/local/bin/songbird` rogue binary outside depot path caused port conflict. Remove + enforce depot-only path. | 30min |

### P3

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **TARPC-BIND** | songBird | `tarpc listener: Address in use` on startup. Non-fatal but logged as ERROR. | 1hr |

---

## Incoming This Cascade

### songBird — DRAWBRIDGE-CAP resolved (6 commits)

| Commit | What |
|--------|------|
| `73b0c7d` | **DRAWBRIDGE-CAP**: Runtime caps in `capabilities.list`, `capability.call` drawbridge fallback, `capability.resolve` for proxy-router |
| `74cf710` | HTTPS outbound proxy via `tokio-rustls` + system CA certs |
| `a3c2871` | Per-request allocation elimination in drawbridge hot path |
| `718d18d` + `6463876` | `to_lowercase()` elimination across 17 files / 5 crates (zero-alloc) |

Drawbridge-served services (jupyter, inference, GIS proxy) now visible to `capability.call`. Three-layer solution: runtime cap merge, call fallback, resolve endpoint. Verified: 0 regressions, 0 blockers.

### primalSpring — ironGate redeployment AAR

14 binaries refreshed (31 days stale). 3 crash loops resolved (biomeOS template mismatch: 101,997 restarts, gate-watchdog path error: 52,233 restarts, stale forgejo-sync: disabled). Rogue songBird PID killed. Mesh restored (2 peers via WireGuard). 13/13 services active, 26 UDS sockets, 0 failures.

---

## Wave 137b Closures (cumulative)

| Item | Resolved By |
|------|-------------|
| ~~DRAWBRIDGE-CAP~~ | songBird — 3-layer runtime cap merge + `capability.call` fallback |
| ~~DNS-WILDCARD~~ | Operator — `*.primals.eco` wildcard A record |
| ~~FP-API-CADDY-DEPLOY~~ | sporeGate — 10 GIS proxy routes |
| ~~SONGBIRD-LOCAL~~ | songBird — drawbridge cleanup + hot-path alloc elimination |
| ~~CERT-OWNER~~ | Terminology fix — Loam Certificate vs TLS credential |
| ~~VERSION-SKEW~~ | Documented as intentional differential evolution |
| ~~PEPTI-TARGETS~~ | Elevated to next glacial goal — universal substrate evolution |
| ~~ironGate crash loops~~ | ironGate — template mismatch, path error, stale script |

---

## Gate Status

```
eastGate     — Overwatch. 13 primals. songBird v0.2.1 (2 peers). Clean.
sporeGate    — NUCLEUS. live.primals.eco + FP-API live. Depot 35/35.
golgiBody    — Full mirror. Wildcard DNS. Forgejo healthy.
flockGate    — 144 scenarios / 1,190 tests. songBird deep debt AAR shipped.
ironGate     — REDEPLOYED. 14 fresh binaries. 13/13 active. Mesh restored.
```

**Next Glacial Goal**: Universal Substrate Evolution — multi-arch NUCLEUS.

---

*Wave 137b: 2 original items + 4 new from ironGate triage. DRAWBRIDGE-CAP resolved. ironGate redeployed. All repos clean. 7,750+ tests / 0 fail.*
