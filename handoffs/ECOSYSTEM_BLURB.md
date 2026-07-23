# ecoPrimals Ecosystem Blurb — Wave 150w

**Date**: Jul 23, 2026 08:50 EDT | **Wave**: 150w | **From**: eastGate overwatch
**Posture**: **CONVERGING. Depot pipeline delivered. Parity benchmarks executing.**

---

## REMAINING WORK

### P0 — Operator Deploy (no code, config only)

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | Deploy `golgi-post-receive-ci.sh` to golgiBody | operator | `scp` hook to each primal repo's `hooks/post-receive.d/30-sovereign-ci` |
| 2 | Set `MEMBRANE_BUILD_AUTHORITY=1` on sporeGate | operator | systemd unit override or `membrane.env` |
| 3 | Harvest songBird on sporeGate | sporeGate | `membrane plasmid.harvest --local --primal songbird --force && membrane plasmid.depot_sync --push` |

### P1 — Active (in progress)

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 4 | **LAN parity benchmark** | sporeGate | `songbird benchmark` — sporeGate (.2) ↔ eastGate (.5), same backbone |
| 5 | **WAN parity benchmark** | sporeGate | sporeGate (.2) → golgiBody TURN (.1) → flockGate (.6) |
| 6 | Integrate benchmark results → `s_tower_atomic_parity_live` | eastGate | primalSpring live scenario, calibrate WAN targets |
| 7 | sporePrint primal pipeline | eastGate | Zola replacement: petalTongue + nestGate CAS + cellMembrane |
| 8 | CredentialStore squirrel integration | eastGate | `secrets.*` JSON-RPC, bearDog `FileVault` backend wired |

### P2 — Queued

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 9 | bingoCube WASM WebGL widget | eastGate | Unblocked by petalTongue 150r. `render_color_grid_webgl` ready |
| 10 | `.unwrap()` clippy audit — remaining primals | all teams | `cargo clippy -- -W clippy::unwrap_used`. 5 confirmed 0. |
| 11 | Deploy petalTongue v1.7+ on sporeGate | sporeGate ops | Binary in depot. Activates Webb scene + WASM WebGL |
| 12 | Android Keystore + grapheneGate test | bearDog | CredentialStore TEE/StrongBox backend |
| 13 | Promote 6 pseudoSpores | lithoSpore | Validation Data Stream v1.0 standard defined |
| 14 | footPrint declarative source registry | flockGate | DATA_LAYER_PRIMAL_ABSTRACTION spec committed |

### P3 / Future

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 15 | rootPulse design | ecosystem | Sovereign VCS over nestGate CAS + Provenance Trio |
| 16 | sporePrint pipeline design | ecosystem | Full Zola replacement architecture |
| 17 | pseudoSpore Explorer | esotericWebb | Interactive visualization concept |
| 18 | SHOW_HN readiness | ecosystem | Rubric, narrative, demo path |

### Gate Enrollment (operator, when physically accessible)

| # | Task | Detail |
|---|------|--------|
| 19 | southGate USB enrollment | USB staged, .9 allocated |
| 20 | strandGate enrollment | Dual EPYC, 256GB RAM, RTX 3090. Pending physical access |

---

## WHAT'S DONE

| Achievement | Wave |
|-------------|------|
| Sovereign depot pipeline (4 phases + deep debt sweep, 1110 tests) | 150w |
| Benchmark harness shipped, TURN relay LIVE, all blockers cleared | 150v |
| Tower primals deep debt, gate AARs GREEN, structural 21/21 | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap, cascade 43/43 | 150s-u |
| WASM WebGL, vendor analysis, USB enrollment, workspace reorg | ≤150r |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6, Glacial 8/8, Depot | ≤150i |

---

## TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, TURN relay (:3478), depot
  ├─ sporeGate (10.13.37.2) — build authority, Tower 3/3
  ├─ eastGate  (10.13.37.5) — orchestrator, code hub
  ├─ flockGate (10.13.37.6) — esotericWebb V22, WAN peer
  ├─ ironGate  (10.13.37.7) — compute, GPU [DOWN]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Pending: southGate (.9), strandGate
```

**Sovereignty**:

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | Benchmarking |
| **REPLACE** | Zola | petalTongue + nestGate CAS | Design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk / JupyterHub | Outer membrane | Stays |

**Parity philosophy**: Match WireGuard first, exceed later. Targets relative to WG baseline.

---

*Wave 150w: 3 P0 operator deploys, 5 P1 active tasks, 6 P2 queued, 4 P3 future.
Depot pipeline delivered. Parity benchmarks executing. 43/43 converged.*
