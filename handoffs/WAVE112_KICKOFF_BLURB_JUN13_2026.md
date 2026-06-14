# Wave 112 — Remaining Work

**Date**: 2026-06-14  
**From**: eastGate overwatch  
**Theme**: Operational Convergence — prove the system self-heals

---

## Status

| Milestone | State |
|-----------|-------|
| riboCipher WARN→ERROR | ✅ 8/8 COMPLETE |
| VPS cellMembrane deploy | ✅ DONE (`0ef6c38`, 13/13 alive) |
| cellMembrane refactor | ✅ `06f9ad2` (net -200 lines, VPS pending update) |
| freshness auto-publish | ✅ WORKING (dual-push, Wave 112 IDs) |
| songBird depot rebuild | ❌ BLOCKER — depot binary `32a8d700` predates riboCipher |
| sourDough forgejo | ❌ BROKEN — Forgejo Internal Server Error (repo corrupt) |
| Parity | 11/12 (sourDough exception) |
| Convergence Gate | 3/8 GREEN |

---

## Critical Path

```
songBird depot harvest → VPS songBird deploy → mesh enrollment → cascade cycles → gate clear
```

Everything downstream is blocked until the songBird depot binary is rebuilt from ≥`fe47c012`.

---

## Remaining Work by Team

### cellMembrane (ironGate) — P1

Owns VPS (golgiBody). All VPS operations are cellMembrane/ironGate team scope.

| Task | Detail | Blocked By |
|------|--------|-----------|
| **songBird harvest** | `plasmid.harvest --targets songbird` on VPS | — |
| **VPS cellMembrane update** | Deploy `06f9ad2` (refactored) to VPS | — |
| **sourDough forgejo fix** | Repo corrupt — `gitea admin repo-sync` or recreate | — |
| Dev gate cascade | `temporal.cascade --with-restart` on eastGate, southGate | songBird harvest |
| Mesh enrollment | Configure gates with VPS peer address | songBird harvest |
| 2 clean cycles | Zero-intervention cascade validation | Cascade + enrollment |
| NUC canary bootstrap | `gate.bootstrap` canary-fieldmouse profile | — |

### sourDough — P2

| Task | Detail |
|------|--------|
| `validate ribocipher` | Fleet compliance auditing subcommand |
| Scaffold update | New primals born with riboCipher-compliant accept loops |

### toadStool (strandGate) — P2

| Task | Detail |
|------|--------|
| **TOADSTOOL-AUTO-REGISTER** | PCI/sysfs enumeration on startup — auto-register GPU/NPU with biomeOS |

### primalSpring (eastGate) — P3

| Task | Detail |
|------|--------|
| Proto-nucleate manifest | Sub-NUCLEUS topology definition for partial deployments |

### ops (physical only) — P2

Hardware that requires human hands. Cannot be agentified.

| Task | Detail |
|------|--------|
| **westGate** | Power on, network cable, physical setup (i7-4771 + 76TB ZFS) |
| **NUC + Pixle** | Physical placement, power, network cable |

After physical setup, `gate.bootstrap` is cellMembrane's job.

---

## Exit Criteria

| # | Criterion | State |
|---|-----------|-------|
| 1 | VPS cellMembrane deployed | ✅ `0ef6c38` (update to `06f9ad2` pending) |
| 2 | songBird depot rebuilt ≥fe47c012 | ❌ BLOCKER |
| 3 | 2 cascade cycles, zero intervention | ⬜ blocked by #2 |
| 4 | Version skew = 0 after cascade | ⬜ blocked by #3 |
| 5 | riboCipher ERROR 8/8 | ✅ COMPLETE |
| 6 | At least 1 new hardware gate enrolled | ⬜ pending (ops physical + cellMembrane bootstrap) |

---

## sourDough Forgejo Diagnosis

Forgejo Internal Server Error on push AND read (`ls-remote`). SSH auth succeeds, other repos push fine. Server-side repo corruption.

**Fix (cellMembrane/ironGate — owns VPS):**
1. Check Forgejo logs: `journalctl -u forgejo`
2. Attempt: `gitea admin repo-sync --repo ecoPrimals/sourDough`
3. Nuclear: delete repo via admin panel, recreate, `git push forgejo main --force`

---

## Priority Order

```
P1: songBird harvest + VPS update + forgejo fix (cellMembrane/ironGate)
P2: sourDough tooling | toadStool auto-register
P3: primalSpring proto-nucleate
ops: westGate + NUC physical setup (when human has time)
```

---

**The code is done. Unblock the depot, prove the system self-heals.**
