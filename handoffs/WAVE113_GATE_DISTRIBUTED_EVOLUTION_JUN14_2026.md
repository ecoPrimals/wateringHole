# Wave 113 — Remaining Work

**Date**: 2026-06-14 (rescoped)  
**From**: eastGate overwatch  
**Progress**: 1/6 exit criteria met (riboCipher REJECT shipped)  
**Critical Path**: VPS peer enrollment → persistent federation  
**Convergence Gate**: CLEARED (fossilized to archive)

---

## Priority Blockers (unblock everything else)

| # | Blocker | Owner | Action |
|---|---------|-------|--------|
| 1 | **flockGate not enrolled on VPS** | cellMembrane (ironGate) | Add flockGate to SONGBIRD_PEERS env on VPS relay unit + restart |
| 2 | **aarch64 depot stale** | cellMembrane (ironGate) | `plasmid.harvest --targets beardog,songbird,skunkbat --arch aarch64` from HEAD |
| 3 | **Freshness multi-writer race** | cellMembrane | Designate golgiBody as sole freshness publisher. ironGate stops auto-publishing. |

---

## Remaining Per-Gate Work

### cellMembrane / ironGate — P1

| Task | Notes |
|------|-------|
| Enroll flockGate as persistent VPS peer | Unblocks exit criterion 2 + partition tolerance |
| riboCipher REJECT on VPS primals | hotSpring + strandGate shipped. Remaining: VPS-hosted primals. |
| rootpulse ledger init | First real (non-dry-run) commit chain through trio |
| NUCLEUS-aware probes | Replace socat with neuralAPI capability.call |
| Primal CLI contract standardization | guideStone amendment — each primal's server arg pattern |
| Gate identity file | Write `/etc/membrane/gate_identity` during bootstrap |
| Profile-aware health | Tower-only = 2/2 PASS, not 13/13 |
| Freshness single-writer policy | Stop ironGate from auto-publishing (golgiBody only) |
| aarch64 depot harvest | Unblocks grapheneGate |

### eastGate — P2

| Task | Notes |
|------|-------|
| Cascade recipient validation | Accept VPS cascades, validate zero-skew |
| Overwatch auditing | Monitor cascade logs for manual intervention signals |

### southGate — P2

| Task | Notes |
|------|-------|
| DEPLOY-THEN-STALE simulation | Skip 1-2 cycles, verify mesh detects skew |
| Parallel cascade target | Diversity for cascade validation |

### grapheneGate — P3

| Task | Notes |
|------|-------|
| Cross-arch deploy | Blocked until aarch64 depot harvested from HEAD |
| songBird PID dir fix | Needs `--state-dir` / `SONGBIRD_STATE_DIR` with XDG fallback |

### flockGate — P2

| Task | Notes |
|------|-------|
| Persistent federation | Blocked until VPS enrolls flockGate as peer |
| Partition tolerance validation | Blocked until persistent connection established (reachability is STATIC gap) |

### ops (physical only)

| Task | Notes |
|------|-------|
| NUC placement + power + cable | Then cellMembrane `gate.bootstrap` takes over |
| westGate power on | i7-4771 + 76TB ZFS |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT on ≥1 gate, 0 unsignalled | ✅ DONE |
| 2 | flockGate persistent `active_connections > 0` | ⚠️ BLOCKED (enrollment) |
| 3 | DEPLOY-THEN-STALE (mesh detects intentional skew) | ⬜ |
| 4 | New hardware gate enrolled | ⬜ (ops) |
| 5 | rootpulse real commit chain | ⬜ |
| 6 | Gate-clearing issues (CLI, identity, profile health) | ⚠️ PARTIAL |

---

## Evolution Debt (both short + robust solutions needed)

| Problem | Short-term Fix | Robust Solution |
|---------|---------------|-----------------|
| **Freshness multi-writer** | Single-writer: golgiBody only publishes | `freshness.mesh` via songbird mesh.publish (eliminate VCS coordination) |
| **Reachability static** | Enroll peers → auto-reconnect loop activates | Periodic reachability probing without active connection |
| **Primal CLI divergence** | Document each primal's arg pattern | guideStone amendment: mandatory `--socket`, `--bind-mode` standard |
| **aarch64 depot drift** | Manual harvest from HEAD | Automated cross-arch depot rebuild in pipeline |

---

**Critical path: Enroll flockGate → prove persistent federation → unblock partition tolerance → exit criterion 2.**
