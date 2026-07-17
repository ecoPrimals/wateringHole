# ecoPrimals Ecosystem Blurb — Wave 147c

**Date**: Jul 17, 2026 10:45 EDT | **Wave**: 147c | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. ENROLLMENT FULLY AUTOMATED.**

**This cascade**: Absorbed 5 team deliveries. cellMembrane added `hub.peer`
phase — `gate.enroll` is now 7 phases, fully automated (no operator SSH needed).
songBird shipped `mesh.enroll` JSON-RPC method for BTSP enrollment.
lithoSpore completed Silicon Atheism (`Platform` trait, 216 tests, 0 debt).
footPrint hardened protocol security (deep wire validation, `MutableEntity` store,
228 tests). sporePrint deep debt sweep (289 tests, `peer_hints()` agnostic).
primalSpring added `gate-enroll-pipeline` scenario (170 scenarios, 1203 tests).
5 handoffs fossilized. primalSpring divergence resolved.

---

## Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** (incl. hub.peer) |
| northGate mesh enrollment | **COMPLETE** — 6th node |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## `gate.enroll` — Fully Automated (7 Phases)

`membrane gate.enroll <name> [--dry-run]` — zero operator SSH required.

| # | Phase | What |
|---|-------|------|
| 1 | `manifest.resolve` | Read gate profile from manifest |
| 2 | `wg.keygen` | Generate WireGuard keypair |
| 3 | `wg.config` | Render wg-quick config |
| 4 | `hub.peer` | **SSH to hub, register peer via `wg set`** |
| 5 | `mesh.verify` | Ping hub via WireGuard |
| 6 | `forgejo.verify` | SSH test to Forgejo via mesh |
| 7 | `git.remotes` | Forgejo-first remotes on all repos |

**songBird** shipped `mesh.enroll` JSON-RPC method — BTSP enrollment
endpoint ready for cellMembrane integration. Trustless enrollment path is
now structurally wired: manifest → WireGuard → mesh → songBird beacon.

---

## Ecosystem Test Health

| Project | Tests | Clippy | Unsafe | Debt Markers |
|---------|-------|--------|--------|-------------|
| cellMembrane | 1,089 | 0 | forbidden | 0 |
| songBird | full pass | 0 | forbidden | 0 |
| lithoSpore | 216 | 0 | forbidden | 0 |
| footPrint | 228 | clean | N/A (TS) | 0 |
| sporePrint | 289 | 0 | forbidden | 0 |
| primalSpring | 1,203 | 0 | — | 1 (graphenegate aarch64 depot) |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, relay
  ├─ sporeGate (10.13.37.2) — builder, site router
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — WAN gate, 16 bonds
  ├─ ironGate  (10.13.37.7) — compute, ABG, JupyterHub
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

## Active Evolution Targets

### Gardens (P1 — assigned to gates)

| Garden | Gate | Status |
|--------|------|--------|
| **lithoSpore** / pseudoSpore | ironGate | Silicon Atheism COMPLETE. 216 tests. Next: pseudoSpore pack/unpack for initioChem. |
| **esotericWebb** | flockGate | NOT STARTED. Living game state — petalTongue UI + primals interactive experience. |
| **projectFOUNDATION** | TBD | NOT STARTED. Data/knowledge layer — thread lineage, validation evidence. |
| initioChem | ironGate | NOT STARTED. First pseudoSpore consumer — computational chemistry. |

### Infrastructure (P1-P2)

| Item | Status |
|------|--------|
| northGate: repo sync + Forgejo-first remotes | IN PROGRESS (northGate agent) |
| northGate: NUCLEUS deploy + benchScale validation | NEXT |
| songBird BTSP → cellMembrane `gate.enroll` integration | NEAR-TERM |
| footPrint composition wiring (WS_PATH, PROXY_PATH, PROJECTS_PATH) | P1 |
| bearDog HSM → Android Keystore | P2 |
| DNSSEC on primals.eco | P2 |
| `protokarya-wan-deploy` scenario (1 primalSpring gap remaining) | P2 |

### Upstream Gaps (for primal teams)

| Gap | Owner | Source |
|-----|-------|--------|
| `PROXY_PATH` drawbridge wiring for footPrint | songBird | footPrint 145b |
| `PROJECTS_PATH` CAS wiring for footPrint projects | nestGate | footPrint 145b |
| `WS_PATH` agent bridge for footPrint WebSocket | petalTongue | footPrint 145b |
| Caddy blocks for footPrint API endpoints | cellMembrane | footPrint 145b |
| `@protokarya` npm org for RustScript publish | primalSpring | footPrint 145b |

### Future

| Item | When |
|------|------|
| helixVision (sovereign genomics) | Post-FOUNDATION |
| blueFish (analytical chemistry) | Post-FOUNDATION |
| tideGlass (sovereign GPS) | Post-footPrint |

---

## Depot (59 binaries — 4 architectures)

```
x86_64-linux-musl     16   FRESH
aarch64-linux-musl    16   FRESH
aarch64-android       13   FRESH
x86_64-windows-gnu    14   FRESH

BLAKE3 + Ed25519 signed. VPS depot serving.
```

---

*Wave 147c: 5 team deliveries absorbed. gate.enroll now 7-phase fully
automated (hub.peer eliminates operator SSH). songBird mesh.enroll BTSP
method shipped. lithoSpore Silicon Atheism complete (Platform trait, 216
tests). footPrint protocol security hardened (228 tests). sporePrint deep
debt (289 tests). primalSpring gate-enroll-pipeline scenario (170 scenarios,
1203 tests). 5 handoffs fossilized, 4 active remain (blurb, ABG guide,
protokarya gaps, startup template). All divergence resolved.*
