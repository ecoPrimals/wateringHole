# Wave 107 — Remaining Scope by Level

**Date**: 2026-06-10
**From**: eastGate primalSpring team
**State**: ZERO P1. S1-S4 ALL GRADUATED. 4-gate mesh collective LIVE.
**Priority cascade**: Fix primals (mountain) → primalSpring absorbs → gates rebuild → gardens automate.

---

## Cross-Level Summary

| Level | P2 | LOW | Key Next Action |
|-------|-----|-----|-----------------|
| **Primals** (mountain) | 3 | 1 | Fix CR-TARPC-01 + BM-UDS-01 + toadStool /tmp |
| **primalSpring** | 1 | 2 | Absorb primal fixes → grapheneGate 13/13 scenario |
| **Springs** | 1 | 15 | healthSpring signal dispatch live test on ironGate |
| **Gates** | 2 | 0 | flockGate power-on, grapheneGate aarch64 rebuild |
| **Gardens** | 3 | 2 | CM depot sync, NDK pipeline, BearDog ACME cutover |
| **TOTAL** | **10** | **20** | **Fix mountain first, everything else follows** |

---

## Level 1: Primals (Mountain)

### P2 — Blocks grapheneGate 13/13

| ID | Owner | Action | primalSpring Tracking |
|----|-------|--------|----------------------|
| `CR-TARPC-01` | coralReef | Skip tarpc `bind()` when `PRIMAL_BIND_MODE=tcp_only`. JSON-RPC TCP :9730 works. | `blocker:cr_tarpc_01` in `s_graphenegate_readiness` |
| `BM-UDS-01` | biomeOS | Skip Neural API UDS `bind()` when `PRIMAL_BIND_MODE=tcp_only`. v4.18 fallback not wired into actual bind path. | `blocker:bm_uds_01` in `s_graphenegate_readiness` |
| `TOADSTOOL-SOCKET-CLEANUP` | toadStool | Migrate compute-tarpc.sock + toadstool-jsonrpc-port to 3-tier resolution. Blocks `ProtectSystem=strict`. | `blocker:toadstool_socket` in `s_graphenegate_readiness` — PASS (3-tier adopted, `temp_dir()` fallback remains) |

### LOW

| ID | Owner | Action |
|----|-------|--------|
| `SKUNKBAT-TCP-9750` | skunkBat | **RESOLVED** — Port 9750 DROPPED from federation registry. Zero-port standard clean. |

---

## Level 2: primalSpring

### P2

| ID | Owner | Action |
|----|-------|--------|
| `GRAPHENEGATE-SCENARIO` | primalSpring | After CR-TARPC-01 + BM-UDS-01 fixes, rebuild aarch64, run `--composition full` on Pixel 8, validate 13/13 in scenarios. grapheneGate readiness Phase 7 tracks blockers structurally. |

### LOW

| ID | Owner | Action |
|----|-------|--------|
| Federation port cleanup | primalSpring | **RESOLVED** — beardog 9900/9101, skunkBat 9750 all DROPPED. Zero droppable ports. |
| Zero-port standard | primalSpring | **RESOLVED** — `federation:droppable_eliminated` check passes. |

---

## Level 3: Springs

### P2

| ID | Owner | Action |
|----|-------|--------|
| `GAP-47-SIGNAL-DISPATCH-LIVE` | healthSpring + biomeOS | Live test nest.store/nest.commit on ironGate biomeOS with signal graphs loaded. |

### LOW (15 healthSpring upstream)

See `impulses/active/2026-06-10T14-20_ironGate__wave107-healthspring-upstream-gaps.toml`.
2 MEDIUM, 13 LOW. All with stable workarounds.

---

## Level 4: Gates

### P2

| ID | Owner | Action |
|----|-------|--------|
| `FLOCKGATE-WAN-E2E` | flockGate ops | Power on → re-fetch from VPS → mesh.init to 157.230.3.183:7700 → verify 5/5. |
| `GRAPHENEGATE-REBUILD` | primalSpring + cellMembrane | aarch64 rebuild on peptidoglycan → push checksums.toml → `deploy_pixel.sh` → 13/13 alive. **Requires CR-TARPC-01 + BM-UDS-01 fixes first.** |

---

## Level 5: Gardens

### P2

| ID | Owner | Action |
|----|-------|--------|
| `CM-VPS-DEPOT-SYNC` | cellMembrane | Automate golgiBody inner→outer membrane binary flow. |
| `NDK-CROSS-COMPILE` | cellMembrane | `aarch64-linux-android` target on peptidoglycan for native grapheneGate. |
| `BEARDOG-ACME-CUTOVER` | cellMembrane + bearDog | TlsProvider wired, awaiting BearDog ACME client to replace Caddy LE. |

### LOW

| ID | Owner | Action |
|----|-------|--------|
| `NG-DOWNCAST-01` | nestGate | `is_platform_constraint()` downcast fails. Workaround: `NESTGATE_SOCKET=""`. |
| `PB-FORWARD-01` | cellMembrane | deploy_pixel.sh ADB port conflict — silent failure. |

---

## Ecosystem-Wide

### LOW

| ID | Owner | Action |
|----|-------|--------|
| `SOURDOUGH-SEGFAULT` | sourDough | `validate depot` segfault. Manual `b3sum` fallback. |
| `INFERENCE-NAMESPACE` | ecosystem | Canonical namespace: `model.*` vs `inference.*` vs `ai.*`. |

---

## Dependency Graph

```
CR-TARPC-01 + BM-UDS-01 (primal code)
    │
    ▼
GRAPHENEGATE-REBUILD (aarch64 rebuild on peptidoglycan)
    │
    ▼
GRAPHENEGATE-SCENARIO (primalSpring validation: 13/13 on Pixel 8)
    │
    ▼
grapheneGate mesh enrollment (future)
```

```
FLOCKGATE-WAN-E2E (independent — just needs power-on)
    │
    ▼
5-gate mesh complete
```

---

## Validation State

| Metric | Value |
|--------|-------|
| primalSpring scenarios | 55 (10 tracks, 3 tiers) |
| lib tests | 901 pass, 2 ignored |
| clippy | zero warnings |
| known_debt | 3 (graphenegate-readiness upstream blockers) |
| federation ports | 2 non-droppable (songbird), 0 droppable |
| zero-port standard | CLEAN |
| cascade | 38/38 parity |
