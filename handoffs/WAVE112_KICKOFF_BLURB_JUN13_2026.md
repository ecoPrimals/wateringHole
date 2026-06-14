# Wave 112 — Distribution Blurb

**Date**: 2026-06-13  
**From**: eastGate overwatch  
**Theme**: Operational Convergence — the code is done, prove the system self-heals

---

## Status

- **riboCipher WARN→ERROR**: ✅ 8/8 COMPLETE (all primals at ERROR for unsignalled)
- **Deprecation timeline**: Wave 113 REJECT → Wave 114 REMOVE
- **Parity**: 12/12 repos aligned (origin = forgejo = local)
- **Tests**: 929 green across primalSpring, freshness validation passing
- **Convergence Gate**: 3/8 criteria GREEN, 5 pending ops execution

---

## Remaining Work by Team

### cellMembrane — P1 (Critical Path)

| Task | Detail |
|------|--------|
| **VPS deploy** | Install `54eee01` on golgiBody VPS — stops junk auto-publish, enables mito-tier ERROR, unblocks depot |
| **Depot harvest** | `plasmid.harvest --all` after VPS deploy — fixes BLAKE3 mismatches |
| **Cascade validation** | `temporal.cascade --with-restart` on eastGate, southGate, grapheneGate |
| **2 clean cycles** | 2 full cascade cycles, zero manual intervention (Convergence Gate criterion 6) |
| **NUC canary** | `gate.bootstrap` with `canary-fieldmouse` profile (Phase 1 VPS minimization) |

Everything else is blocked until VPS deploy completes.

### sourDough — P2

| Task | Detail |
|------|--------|
| `validate ribocipher` | Fleet compliance auditing subcommand |
| Scaffold update | New primals born with riboCipher-compliant accept loops |
| Forgejo parity | Fix HTTP 500 on `git push forgejo main` |

### toadStool — P2

| Task | Detail |
|------|--------|
| **TOADSTOOL-AUTO-REGISTER** | PCI/sysfs enumeration on startup — auto-register GPU/NPU with biomeOS |

Blocks autonomous `gate.bootstrap` for compute gates (strandGate, future GPU nodes).

### ops (eastGate) — P2

| Task | Detail |
|------|--------|
| **westGate** | Power on, network, `gate.bootstrap` (i7-4771 + 76TB ZFS, Nest Atomic profile) |
| **NUC + Pixle** | Linux node enrollments — quick spin-up |
| DEPLOY-THEN-STALE | Deploy westGate, skip 2 cascade waves, measure skew (Stream 6 validation) |

### primalSpring — P3

| Task | Detail |
|------|--------|
| Proto-nucleate manifest | Sub-NUCLEUS topology definition for partial deployments |

### ALL TEAMS — Wave 113 prep (future, not yet)

| Task | Detail |
|------|--------|
| riboCipher REJECT | Unsignalled connections actively refused (Wave 113 — after 2 clean cascade cycles prove no legacy callers remain) |

---

## Exit Criteria

Wave 112 closes when:

1. ⬜ VPS rebuilt to `54eee01`
2. ⬜ 2 cascade cycles, zero intervention
3. ⬜ Version skew = 0 after cascade
4. ✅ riboCipher ERROR: **8/8 COMPLETE**
5. ⬜ At least 1 new hardware gate enrolled

---

## Priority Order

```
P1: VPS deploy → harvest → cascade (cellMembrane)
P2: sourDough tooling | toadStool auto-register | hardware enrollment
P3: primalSpring proto-nucleate
```

---

**The code is done. Prove the system self-heals.**
