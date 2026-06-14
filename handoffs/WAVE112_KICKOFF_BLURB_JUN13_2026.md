# Wave 112 — Distribution Blurb

**Date**: 2026-06-14 (cascade update)  
**From**: eastGate overwatch  
**Theme**: Operational Convergence — the code is done, prove the system self-heals

---

## Status

- **riboCipher WARN→ERROR**: ✅ 8/8 COMPLETE
- **VPS cellMembrane**: ✅ DEPLOYED (`0ef6c38`) — 13/13 integrity, 13/13 alive, gate.status GREEN
- **cellMembrane refactor**: `06f9ad2` — extracted jsonrpc module, consolidated XDG/git/path, net -200 lines
- **freshness auto-publish**: ✅ WORKING (dual-push fix `0ef6c38`, Wave 112 IDs correct)
- **Deprecation timeline**: Wave 113 REJECT → Wave 114 REMOVE
- **Parity**: 11/12 (sourDough forgejo HTTP 500 persists)
- **Convergence Gate**: 3/8 GREEN, critical blocker = songBird depot rebuild

---

## Remaining Work by Team

### cellMembrane — P1 (Critical Path)

| Task | Priority | Detail |
|------|----------|--------|
| **songBird depot rebuild** | P1 | `plasmid.harvest --targets songbird` — current depot binary (32a8d700) predates riboCipher, rejects `[0xEC,0x01]` with UTF-8 error |
| **VPS cellMembrane update** | P1 | Deploy `06f9ad2` (refactored, latest) — VPS currently at `0ef6c38`, 6 refactor commits behind |
| **Dev gate cascade** | P2 | `temporal.cascade --with-restart` on eastGate, southGate — bring to post-34e472d |
| **Mesh enrollment** | P2 | Configure dev gates with VPS peer address — hub is listening, awaiting inbound |
| **2 clean cycles** | P2 | 2 full cascade cycles, zero manual intervention (Convergence Gate criterion 6) |
| **NUC canary** | P2 | `gate.bootstrap` with `canary-fieldmouse` profile (Phase 1 VPS minimization) |

**Blocker chain**: songBird depot → VPS songBird deploy → mesh enrollment → cascade cycles → gate clear.

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
| riboCipher REJECT | Unsignalled connections actively refused (after 2 clean cascade cycles prove no legacy callers remain) |

---

## Exit Criteria

Wave 112 closes when:

1. ✅ VPS cellMembrane deployed (0ef6c38 — done, `06f9ad2` pending next cycle)
2. ⬜ songBird depot rebuilt to ≥fe47c012
3. ⬜ 2 cascade cycles, zero intervention
4. ⬜ Version skew = 0 after cascade
5. ✅ riboCipher ERROR: **8/8 COMPLETE**
6. ⬜ At least 1 new hardware gate enrolled

---

## Priority Order

```
P1: songBird harvest → VPS update → mesh enrollment (cellMembrane)
P2: sourDough tooling | toadStool auto-register | hardware enrollment
P3: primalSpring proto-nucleate
```

---

**The code is done. Prove the system self-heals.**
