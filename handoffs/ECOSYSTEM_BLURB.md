# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 11:20 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **CONVERGED. PUBLIC.** `live.primals.eco` is LIVE — petalTongue TOPO-VIS dashboard serving over TLS/HTTP2 with full security headers. 3-gate mesh operational (eastGate + sporeGate + golgi). `require-signed` depot trust active system-wide. 13 primals running on eastGate. flockGate at 144 scenarios / 1,190 tests. primalSpring in heavy local evolution (17 scenarios, 272 LOC).

---

## Priority Work — frontloaded

### P0 — Blocks deployments

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **DEPOT-CHECKSUM** | sporeGate | Depot binary BLAKE3 doesn't match `checksums.toml` (unstripped 26.6MB vs signed checksum). Since `require-signed` is now active, **all `plasmid.fetch` will reject songBird**. Re-harvest: strip → checksum → sign → sync. | 30min |

### P1 — Next capabilities

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **FP-API-CADDY-DEPLOY** | sporeGate / golgi | flockGate drafted `fp-api-caddy.caddyfile` (130 LOC, 10 GIS hosts). Deploy to golgi Caddy config. footPrint gets full GIS proxy at `primals.eco/footprint/`. | 30min |
| **DRAWBRIDGE-CAP** | songBird | Drawbridge routes not advertising as capabilities. `capabilities.list` returns 15 native caps, zero drawbridge. Blocks `capability.call` for any drawbridge service (jupyter, GIS proxy, etc). | 2-4hr |
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` returns count=0. Last piece for full Neural API lifecycle authority. | 4-8hr |

### P2 — Hardening

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation for HTTPS outbound. | 2-4hr |
| **FETCH-PATH** | cellMembrane | `plasmid.fetch` creates doubled nested path (`primals/x86_64/primals/x86_64/`). Doesn't match systemd template. Manual binary placement required. | 1-2hr |
| **SOCKET-UMASK** | biomeOS | Primals should `fchmod` sockets after bind. | 2hr |

### P3 — Cleanup

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SONGBIRD-LOCAL** | songBird | Drawbridge cleanup (header parsing, dead constant) — 1 file dirty. Commit + push. | 30min |

### Discussion (all teams)

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot targets: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Milestones Hit This Wave

- `live.primals.eco` — **PUBLIC.** TOPO-VIS dashboard, 7 mesh peers, SSE live push, TLSv1.3/HTTP2.
- `primals.eco/footprint/` — footPrint SPA live.
- **3-gate mesh** — eastGate (35ms) + sporeGate (71ms) + golgi bidirectional over WireGuard.
- **Depot trust chain enforced** — `require-signed` system-wide, Ed25519 + BLAKE3.
- **13 primals active** on eastGate, all systemd-managed.
- **Drawbridge weak bond pattern** formalized — K-Derm ion channel model for external data.
- **Forgejo full-depth** — 21 repos, permissions fixed, push verified.

---

## Gate Status

```
eastGate     — Overwatch. 13 primals active. songBird v0.2.1 (2 peers). All tasks DONE.
sporeGate    — NUCLEUS. live.primals.eco serving. Neural API systemd. Depot re-sign needed.
golgiBody    — Full mirror. sporePrint + footPrint live. Forgejo healthy. FP-API Caddy ready.
flockGate    — 144 scenarios. FP-API Caddy drafted. Mesh confirmed (74cf7101).
ironGate     — Node atomic. Own overwatch agent.
```

**Active Handoffs**: `DRAWBRIDGE_WEAK_BOND_PATTERN_AAR_137b.md`, `FLOCKGATE_WAN_OVERWATCH_AAR_137b.md`

---

*Wave 137b: live.primals.eco PUBLIC. 7 items remain (1 P0, 3 P1, 3 P2) + 1 cleanup + 3 discussion. Depot checksum mismatch is the only blocker. Everything else is independently actionable.*
