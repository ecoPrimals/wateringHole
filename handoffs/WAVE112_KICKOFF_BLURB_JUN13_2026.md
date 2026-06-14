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

### cellMembrane / ops — P1

| Task | Detail | Blocked By |
|------|--------|-----------|
| **songBird harvest** | `plasmid.harvest --targets songbird` on VPS | — |
| **VPS cellMembrane update** | Deploy `06f9ad2` (refactored) to VPS | — |
| **sourDough forgejo fix** | Repo corrupt on Forgejo — needs `gitea admin` or repo recreate | VPS access |
| Dev gate cascade | `temporal.cascade --with-restart` on eastGate, southGate | songBird harvest |
| Mesh enrollment | Configure gates with VPS peer address | songBird harvest |
| 2 clean cycles | Zero-intervention cascade validation | Cascade + enrollment |
| NUC canary | `gate.bootstrap` canary-fieldmouse profile | — |

### sourDough — P2

| Task | Detail |
|------|--------|
| `validate ribocipher` | Fleet compliance auditing subcommand |
| Scaffold update | New primals born with riboCipher-compliant accept loops |
| Forgejo parity | **BLOCKED** — server-side repo corruption (HTTP 500 on push AND read) |

### toadStool — P2

| Task | Detail |
|------|--------|
| **TOADSTOOL-AUTO-REGISTER** | PCI/sysfs enumeration on startup — auto-register GPU/NPU with biomeOS |

### ops (eastGate) — P2

| Task | Detail |
|------|--------|
| **westGate** | Power on, network, `gate.bootstrap` (i7-4771 + 76TB ZFS, Nest Atomic) |
| NUC + Pixle | Linux node enrollments |
| DEPLOY-THEN-STALE | Stream 6 validation (after westGate enrolled) |

### primalSpring — P3

| Task | Detail |
|------|--------|
| Proto-nucleate manifest | Sub-NUCLEUS topology definition for partial deployments |

---

## Exit Criteria

| # | Criterion | State |
|---|-----------|-------|
| 1 | VPS cellMembrane deployed | ✅ `0ef6c38` (update to `06f9ad2` pending) |
| 2 | songBird depot rebuilt ≥fe47c012 | ❌ BLOCKER |
| 3 | 2 cascade cycles, zero intervention | ⬜ blocked by #2 |
| 4 | Version skew = 0 after cascade | ⬜ blocked by #3 |
| 5 | riboCipher ERROR 8/8 | ✅ COMPLETE |
| 6 | At least 1 new hardware gate enrolled | ⬜ pending |

---

## sourDough Diagnosis

The Forgejo repo `ecoPrimals/sourDough.git` is returning Internal Server Error on both push AND read (ls-remote). SSH auth succeeds, other repos push fine. The repo itself is likely corrupted on disk.

**Fix options (require VPS shell access):**
1. `ssh golgiBody` → check Forgejo logs for the specific error
2. `gitea admin repo-sync --repo ecoPrimals/sourDough` — attempt repair
3. Delete and recreate the repo via Forgejo admin panel, then force-push

**Impact**: Low operational. Origin (GitHub) is authoritative and current. No team is blocked on forgejo reads for sourDough. Fix is P2.

---

## Priority Order

```
P1: songBird harvest + VPS update + sourDough forgejo fix (all VPS ops)
P2: sourDough tooling | toadStool auto-register | hardware enrollment
P3: primalSpring proto-nucleate
```

---

**The code is done. Unblock the depot, prove the system self-heals.**
