# sporePrint Blurb — Demonstration Era LIVE + arXiv Pipeline

**Date**: Aug 1, 2026 | **Wave**: post-155n | **From**: eastGate overwatch
**Posture**: Demonstration era transition COMPLETE. pseudoSpore LIVE. First arXiv draft scaffolded. **Waiting on hotSpring data to submit.**

---

## COMPLETED THIS SESSION

| Phase | Status | What |
|-------|--------|------|
| Phase 1: Nav triage | **DONE** | 334→190 active. 79→foundation. 36→backstory. |
| Phase 2: pseudoSpore section | **LIVE** | Lead nav item. Data catalog. QCD page. Verification guide. |
| Phase 2: Live dashboards | **LIVE (static)** | Gate status, GPU compute, provenance, depot — petalTongue-ready. |
| Phase 2: Hype cleanup | **DONE** | 20 files. All comparative claims qualified. |
| Metric refresh | **DONE** | 116,930 tests (was 101K). 53 metrics synced. |
| Platform resume | **LIVE** | primals.eco/resume/ |
| arXiv draft | **DONE (scaffold)** | `whitePaper/subGen/LATTICE_QCD_CONSUMER_GPU_ARXIV.md` |

---

## PRIORITY: pseudoSpore Downloads + arXiv Data

### pseudoSpore #1 — Science Data Catalog (westGate)

38.2 GB ingested. 11 datasets. 4,752 CAS objects. 100% provenance. All live on the pseudoSpore page.

**Next**: Package downloadable bundles (data + provenance manifest + `validate.sh`). Needs tideGlass + lithoSpore for archive packaging, or a simpler tar+manifest approach.

### pseudoSpore #2 — hotSpring QCD Results (strandGate)

GPU-computed SU(2) lattice QCD trajectories with full provenance. The system producing science, not just storing it.

**Bundle contents**: trajectories, benchmarks, WGSL shaders, hardware profile, full provenance chain, `validate.sh`.

**Update**: arXiv **4/5 sections FILLED** with 8⁴ SU(2) production data. 82× GPU speedup. P2 root-caused (PRNG polyfill bias). `cpu_mom` validated.

**Remaining**: AMD RX 6950 XT benchmarks for Section 3.4 (multi-vendor proof) → sporePrint LaTeX → submit.

### arXiv Publication Path

```
AMD benchmarks (Section 3.4) ← LAST BLOCKER
    ↓
sporePrint reviews for hype compliance
    ↓
markdown → LaTeX (REVTeX4-2)
    ↓
arXiv hep-lat (cross-list cs.DC)
    ↓
sporePrint updates site with arXiv ID
    ↓
JOSS submission (software paper)
```

**Target**: arXiv hep-lat. First publication under ORCID 0009-0004-2141-0321.

---

## REMAINING WORK

| Task | Owner | Blocks | Priority |
|------|-------|--------|----------|
| ~~hotSpring arXiv data~~ | hotSpring team | **4/5 FILLED** — AMD multi-vendor (Section 3.4) remaining | NEARLY DONE |
| AMD GPU benchmarks (RX 6950 XT) | Node Atomic / strandGate | arXiv Section 3.4 | **HIGH** |
| pseudoSpore download packaging | sporePrint + lithoSpore | Download links on catalog page | MEDIUM |
| Live dashboards → petalTongue | petalTongue G19 | Dynamic dashboards | MEDIUM |
| ~~golgi auto-publish~~ | ~~eastGate ops~~ | **FIXED** — 3 compounding bugs resolved | DONE |
| WCAG 2.2 AAA | sporePrint (own) | Accessibility compliance | LOW |

---

## OPS NOTE

golgi auto-publish is **FIXED** (sporeGate AAR, Aug 1 PM). Three bugs resolved: worktree ownership (`git:git` vs `root:root`), missing `--force` on `zola build`, SSH config pointing at wrong golgi IP. sporePrint now deploys correctly to both inner and outer membrane.

---

*Demonstration era is live. P2 resolved. Production data unblocked. The arXiv paper is waiting for validated `cpu_mom` physics data.*
