# Wave 59 Springs Delta Blurb — Deploy & Emit

**Date:** May 28, 2026
**From:** primalSpring coordination
**To:** All spring teams

---

## Glacial Review Complete. Software Ready. Awaiting Deploy.

Glacial gate assessment: **~90% structural/software PASS; ~35-40% operational.**
The gap is VPS deployment and live mesh — not your code.

primalSpring: 797+17 tests, 56 scenarios, 460 methods, zero debt markers,
dispatch telemetry for Layer 4/5 routing evolution. All 21 docs aligned.

---

## VPS Deployment — 3 Steps (unchanged)

```
1. cellMembrane deploys NUCLEUS base (13 primals, UDS-only)
   → deploy_membrane.sh --composition nucleus --uds-only

2. cellMembrane deploys your spring overlay
   → deploy_membrane.sh spring-overlay root@<ip> --cell <yourspring>

3. Your spring runtime discovers primals via UDS
   → CompositionContext::from_live_discovery()
```

Cell graphs: `graphs/cells/<yourspring>_cell.toml` in primalSpring.
All 6 spring cells: `vps_standard = true`, `spawn = false`.

---

## Per-Spring Priorities

| Spring | Gate | Priority | Status |
|--------|------|----------|--------|
| **hotSpring** | biomeGate (Nest Atomic) | **P0 — first emitter** | GATED on v3.84 VPS deploy |
| **groundSpring** | eastGate (Full NUCLEUS) | **P1 — second emitter** | GATED on hotSpring pass |
| wetSpring | southGate (Node Atomic) | P2 | GATED on southGate 13/13 |
| neuralSpring | southGate (Node Atomic) | P2 | GATED on southGate 13/13 |
| airSpring | eastGate (Full NUCLEUS) | P3 | Ready after first 2 emissions |
| healthSpring | ironGate (Full NUCLEUS) | P3 | Ready after first 2 emissions |
| ludoSpring | ironGate (desktop-only) | — | Not on VPS path |

---

## Column U Preparation Checklist

Prepare now while waiting for P0 deploy:

- [ ] Cell graph exists with `vps_standard = true`
- [ ] `domain_profile.toml` prepared for lithoSpore emission
- [ ] `source_dir` content ready for pseudoSpore packaging
- [ ] `CompositionContext::from_live_discovery()` tested locally
- [ ] `health.liveness` responds correctly
- [ ] Binary in plasmidBin depot (`plasmidbin harvest`)

---

## What Changed This Wave (primalSpring 58b→59)

| Change | Why it matters to springs |
|--------|--------------------------|
| Dispatch telemetry persistence | Your dispatches through Neural API now produce training data for routing evolution |
| False readiness signals corrected | NC-1 "CODE COMPLETE" not "COMPLETE" — live column U is the real gate |
| Sovereignty reality check | knot-dns deployed (not planned); CI still GitHub; ~50% cutover done |
| 21 docs aligned to canonical metrics | Version/count references you consume are now accurate |

---

## Timeline

```
NOW    → Prepare column U artifacts (hotSpring, groundSpring first)
NEXT   → biomeOS v3.84 VPS deploy (cellMembrane action)
THEN   → hotSpring column U (first emission via biomeos nucleus ingest)
THEN   → groundSpring column U (NC-5 universality proven)
THEN   → lithoSpore postPrimordial (emission pipeline operational)
TARGET → Stadial: NC-1(2+) + NC-2(3+) + NC-4(all 4 gates healthy)
```

---

*Wave 59. Glacial review done. Infrastructure converged. Springs: prepare to emit.*
