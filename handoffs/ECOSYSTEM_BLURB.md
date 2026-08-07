# ecoPrimals Ecosystem Blurb — Wave 157a Remaining Work

**Date**: Aug 7, 2026 5:40PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **15/15 CROSS-ARCH. TRIAD SPECS WRITTEN. REMAINING: activate timer, materialize graphs, deploy gates, wire springs.** biomeOS Neural API is the orchestration substrate — all triad coordination, primal composition, and downstream routing flows through capability calls.

---

## WHAT SHIPPED THIS WAVE

| Delivered | Evidence |
|-----------|----------|
| **G66 COMPLETE** (15th glacial goal) | 15/15 primals, 15/15 cross-arch, sourDough reference |
| **G68 spec written** | `specs/PLATFORM_SUBSTRATE_SPEC.md` — 3 abstraction layers |
| **G68 audit** | `handoffs/G68_CROSS_DEPLOYMENT_AUDIT_AUG07_2026.md` — 15 primals reviewed |
| **Triad activation specs** | Phase A (timer), Phase B (impulse process), Phase C (sync graphs) |
| **biomeOS Stage 2 infra** | riboCipher pool, Bootstrap→Coordinated, TOML caps (578 tests) |
| **barraCuda ComputeDispatch P0** | 92 WGSL ops unified, −10,771 LOC, 4,873 tests |
| **cellMembrane DIV-7** | Harvest exit code reliability — 3 bugs resolved |
| **hotSpring npu-hw** | akida-driver wired via toadStool |
| **Cross-arch** | **15/15 PASS** (toadStool compiles with warnings) |

---

## REMAINING WORK — BY OWNER

### sporeGate Gate Team

| Task | Spec | Effort |
|------|------|--------|
| **Phase A: cascade timer** | `specs/WATERFALL_CASCADE_TIMER_SPEC.md` | 2 systemd units, `systemctl --user enable` |
| **Depot rebuild** (if needed after barraCuda P0) | — | `cargo clean -p barracuda-unibin && cargo build --release` |

### primalSpring Team (eastGate)

| Task | Handoff | Effort |
|------|---------|--------|
| **Phase C: sync graph materialization** | `handoffs/PRIMALSPRING_SYNC_GRAPH_MATERIALIZATION.md` | 3 TOML files, follow `rootpulse_commit.toml` pattern |
| **N2-N5 verification** | G67 spec | `capability.call` routes to bearDog, Tower, Provenance, squirrel |

### biomeOS Code Team

| Task | Notes |
|------|-------|
| **Neural API routing gaps (D8)** | Several primals unregistered via neural-api |
| **Candidate self-test (D4)** | `composition.test_swap` probe needs env passthrough |

### Primal Code Teams — G68 Convergence

| Status | Primals | What they do |
|--------|---------|-------------|
| **SHIPPED** (6) | nestGate, rhizoCrypt, loamSpine, sweetGrass, coralReef, barraCuda | Done — G68 transport + platform substrate |
| **PENDING** (9) | bearDog, songBird, skunkBat, petalTongue, squirrel, sourDough, bingoCube, biomeOS, toadStool | Evolve platform substrate per `specs/PLATFORM_SUBSTRATE_SPEC.md` |

sourDough leads by example: `platform_link` + `PlatformAccess` traits.

### Gate Teams — Deployment

| Gate | Status | Next |
|------|--------|------|
| sporeGate | Depot current, 12/13 | Phase A timer + barraCuda depot refresh |
| eastGate | NUCLEUS, dev gate | primalSpring N2-N5 validation |
| westGate | 14/14 HEALTHY | Deploy after depot refresh |
| strandGate | GPU at 100% QCD | Deploy after depot refresh |
| blueGate | 14/14, primary Windows builder | Deploy after depot refresh |
| ironGate | NUCLEUS | squirrel systemd deploy (E2), springs surface |
| southGate | 13/13 validation | Passive — validates portability |

### Downstream / Springs — After Triad + Deployment

| Project | Depends On | Target |
|---------|-----------|--------|
| tideGlass cell boot (G36) | westGate deploy | GPS reproduction |
| hotSpring QCD viz (G19) | petalTongue WebGL | Reviewer-ready viz |
| esotericWebb browser surface (G20) | petalTongue WebGL | Game engine on NUCLEUS |
| nestgate.io CAS browse (G57) | G60 federated CAS | Data identity surface |
| arXiv reviewer send (G9) | 41/42 done, wire live site | Murillo/Chuna/Bazavov |
| footPrint squirrel agent (E2) | squirrel deploy on ironGate | Agent panel live |

---

## ORDERING

```
1. sporeGate: Phase A timer (unblocks Phase B)
2. primalSpring: Phase C sync graphs + N2-N5
3. sporeGate: depot refresh (barraCuda P0 + any new biomeOS)
4. Gate teams: deploy from golgi depot
5. G68 primals: converge platform substrate (independent, parallel)
6. Springs: tideGlass, hotSpring viz, esotericWebb, arXiv (after gates deployed)
```

---

## METRICS

| Metric | Value |
|--------|-------|
| Cross-arch | **15/15 PASS** |
| G68 shipped | **6/15** (9 pending) |
| Glacial goals | **15 COMPLETE / 26 ACTIVE / 23 GLACIAL — 64 total** |
| Total tests | **~140K+** |
| P0/P1 | **ZERO** |
| Active impulses | **7** |
| Gates with freshness heads | **6** |

---

*Wave 157a — remaining work. Triad specs are written, cross-arch is 15/15, primals are stable. Next: sporeGate activates the cascade timer (Phase A), primalSpring materializes sync graphs (Phase C), gate teams deploy from golgi. biomeOS Neural API orchestrates everything — the triad, the compositions, the downstream routing. Springs and science tracks follow deployment.*
