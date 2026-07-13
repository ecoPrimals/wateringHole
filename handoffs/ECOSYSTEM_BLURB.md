# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 12:15 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** `live.primals.eco` serving TOPO-VIS. `primals.eco/footprint/` live. 3-gate mesh (eastGate + sporeGate + golgi). Depot pipeline 100% Rust (build → BLAKE3 → sign → verify → deploy). 2,801 lines of bash fossilized. `require-signed` active. 35 binaries / 3 architectures verified. primalSpring: 17 scenarios thickening locally (272 LOC). flockGate: 144 scenarios / 1,190 tests.

---

## Remaining — 6 items + 3 discussion

### P1 — Next capabilities

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **FP-API-CADDY-DEPLOY** | sporeGate / golgi | flockGate drafted `fp-api-caddy.caddyfile` (130 LOC). Deploy to golgi → footPrint gets full GIS proxy. | 30min |
| **DRAWBRIDGE-CAP** | songBird | Drawbridge routes not advertising as capabilities. 15 native caps shown, zero drawbridge. Blocks `capability.call` for any bridged service. | 2-4hr |
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. Last piece for full lifecycle authority. | 4-8hr |

### P2 — Hardening

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation. | 2-4hr |
| **SOCKET-UMASK** | biomeOS | Primals should `fchmod` sockets after bind. | 2hr |

### P3 — Cleanup

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SONGBIRD-LOCAL** | songBird | Drawbridge cleanup — 1 file dirty. Commit + push. | 30min |

### Discussion

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. |

---

## Next Wave — Jellyfish Evolution Targets

From `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md`: 7 scripts have Rust equivalents ready. 14 scripts need new Rust commands. See AAR for full ownership matrix.

**cellMembrane** (next wave): deprecate `fetch.sh`, `update.sh`, `sync.sh`, `doctor.sh`, `validate_gate.sh`, `validate_mesh.sh`, `validate_composition.sh` — 2,546 lines replaceable by existing `membrane` CLI commands.

---

## Gate Status

```
eastGate     — Overwatch. 13 primals active. songBird v0.2.1 (2 peers). All tasks DONE.
sporeGate    — NUCLEUS. live.primals.eco serving. Depot 35/35 verified. Jellyfish triaged.
golgiBody    — Full mirror. Forgejo healthy. FP-API Caddy config ready to deploy.
flockGate    — 144 scenarios / 1,190 tests. FP-API drafted. Mesh confirmed.
ironGate     — Node atomic. Own overwatch. pS 818cf11, pN da2e4f0.
```

**Active Handoff**: `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md` — evolution roadmap for 14 scripts across 4 teams.

---

*Wave 137b: 6 items remain + 3 discussion. P0 cleared (depot checksum + layout). Deployment pipeline fully sovereign Rust. 2,801 lines of bash retired. 35 depot binaries verified across 3 architectures.*
