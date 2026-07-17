# ecoPrimals Ecosystem Blurb — Wave 147b

**Date**: Jul 17, 2026 09:10 EDT | **Wave**: 147b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. GATE.ENROLL SHIPPED.**

**This cascade**: cellMembrane shipped `gate.enroll` — automated mesh enrollment
(5 phases, 753L, 8 tests). Codifies the northGate AAR into a repeatable command:
manifest.resolve → wg.keygen → wg.config → mesh.verify → forgejo.verify →
git.remotes (Forgejo-first). songBird completed final cfg-gated IPC → IpcStream
cleanup. 3 handoffs fossilized. northGate repos syncing.

---

## Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` automated enrollment | **SHIPPED** (cellMembrane `467560d`) |
| northGate mesh enrollment | **COMPLETE** — 6th node |
| Depot (59 binaries, 4 arch) | **OPERATIONAL** |

---

## `gate.enroll` — Mesh Enrollment Convergence

`membrane gate.enroll <name> [--dry-run]` replaces the ad-hoc manual
enrollment process (northGate took ~30 min of operator SSH + key exchange).

| Phase | What |
|-------|------|
| `manifest.resolve` | Read gate profile from manifest — IP, transport, roles |
| `wg.keygen` | Generate WireGuard keypair (`0600` perms) |
| `wg.config` | Render wg-quick config from manifest peers |
| `mesh.verify` | Ping hub via WireGuard tunnel |
| `forgejo.verify` | SSH test to Forgejo via mesh |
| `git.remotes` | Configure Forgejo-first remotes on all repos |

**Enrollment standard**: `origin` = Forgejo (inner membrane), `github` =
GitHub (outer membrane). New gates are sovereign-first from minute zero.

**Next**: Hub-side peer addition (currently requires SSH to golgiBody).
songBird beacon protocol for trustless enrollment with BTSP identity proof.

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, relay
  ├─ sporeGate (10.13.37.2) — builder, site router
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — WAN gate, 16 bonds
  ├─ ironGate  (10.13.37.7) — compute, ABG, JupyterHub
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [NEW]
```

---

## Active Evolution Targets

### Gardens (P1 — assigned to gates)

| Garden | Gate | Status |
|--------|------|--------|
| **lithoSpore** / pseudoSpore | ironGate | Portability layer — makes any work USB-deployable. initioChem proved the pattern. |
| **esotericWebb** | flockGate | Living game state — petalTongue UI + primals interactive experience |
| **projectFOUNDATION** | TBD | Data/knowledge layer — thread lineage, validation evidence |
| initioChem | ironGate | Computational chemistry, first pseudoSpore consumer |

### Infrastructure (P1-P2)

| Item | Status |
|------|--------|
| northGate: repo sync + Forgejo-first remotes + depot fetch | IN PROGRESS |
| northGate: NUCLEUS deploy + benchScale validation | NEXT |
| `gate.enroll` hub-side peer addition (automation) | NEAR-TERM |
| songBird beacon protocol (BTSP self-enrollment) | NEAR-TERM |
| footPrint composition wiring (WS_PATH, PROXY_PATH) | P2 |
| bearDog HSM → Android Keystore | P2 |
| DNSSEC on primals.eco | P2 |

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

*Wave 147b: cellMembrane shipped gate.enroll (5 phases, 753L, 8 tests) —
automated mesh enrollment codifying the northGate AAR. Forgejo-first remote
standard enforced. songBird final IpcStream cleanup. 3 handoffs fossilized.
sporePrint deep debt sweep: spore-validate hardcoding evolved to agnostic
(WELL_KNOWN_PEERS → peer_hints(), transport errors decoupled), dead code
wired (edges_for_entity → isolated node report, is_warning → validation
display), constants extracted, 289 tests passing, 0 warnings, 0 clippy.
Root docs refreshed, content-manifest drift fixed, 1.8GB reclaimed.
Next: northGate NUCLEUS deploy, garden evolution on ironGate (lithoSpore)
and flockGate (esotericWebb).*
