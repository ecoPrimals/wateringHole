# Evolution Pass 11 — Parallel Shadow Starts

**Date**: May 12, 2026
**From**: primalSpring coordination
**For**: All teams (copy-paste ready)
**Pass**: 11 of 14 toward interstadial exit
**Blocking**: Nothing — all upstream work is shipped. Start immediately.

---

## Context

Pillar 5 (river delta) is **MET**. All 8 springs are Tier 4 IPC-first.
All 13 primals at zero gate debt. Phase 32 atomic model is live
(Tower=3, Node=6, Nest=7, NUCLEUS=10+3=13).

The interstadial exit gate now depends on **shadow runs executing** —
sovereign infrastructure running alongside existing services, producing
comparison data that proves parity. Pass 11 starts the three shadow runs
that have zero blockers.

**Pull before starting**: `infra/wateringHole`, `primalSpring`, all `primals/` repos.

---

## Three Parallel Actions

### 1. BearDog TLS Shadow on :8443

**Owner**: projectNUCLEUS (L4 absorption)
**Upstream**: BearDog Wave 100 shipped TLS termination + rate limiting

**What to do**:
- Deploy BearDog TLS on `:8443` alongside the existing Cloudflare proxy
- Measure request latency, error rates, certificate renewal against
  Cloudflare baselines on the same traffic
- Document parity metrics in `projectNUCLEUS/shadow-runs/beardog-tls/`
- The shadow period runs until parity is proven; cutover is stadial work

**Success**: BearDog TLS serving real traffic on `:8443`, metrics
pipeline producing comparison data vs Cloudflare.

### 2. lithoSpore Tier 1 Integration

**Owner**: lithoSpore team (L4 integration)
**Upstream**: groundSpring B2+B1 reproductions COMPLETE (Python 9/9 + Rust 10/10)

**What to do**:
- Integrate groundSpring B2 (Wiser 2013 fitness) into `ltee-fitness` module
- Integrate groundSpring B1 (Barrick 2009 mutation) into `ltee-mutation` module
- Fetch real data from Dryad (Wiser 2013) and NCBI (Barrick 2009)
- BLAKE3-hash fetched data into NestGate content storage via `fetch_and_hash.sh`
- Run module validation: Python `expected_values.json` + Rust `validate_ltee_*` binary
- neuralSpring B1 Rust binary (`validate_ltee_b1_mutation_accumulation`, S201b)
  is also ready for ML surrogate modules when you get to it

**Success**: At least 2 lithoSpore modules producing PASS at Tier 1
with real hashed data. This satisfies Pillar 4 of the interstadial exit.

### 3. NestGate Content Pipeline

**Owner**: projectNUCLEUS (L4 absorption)
**Upstream**: NestGate Session 60 — `content.*` transport parity on all 4 surfaces

**What to do**:
- Wire `publish_sporeprint.sh` to push sporePrint artifacts to NestGate
  via `content.put` + `content.publish`
- Serve published content via NestGate extracellular (replaces GitHub Pages
  for `primals.eco` static content)
- Validate that `content.get` returns byte-identical content to what was put
- Document the publish pipeline in `projectNUCLEUS/shadow-runs/nestgate-content/`

**Success**: sporePrint artifacts served from NestGate, byte-parity
with existing GitHub Pages content.

---

## What's Next (Passes 12-14)

Pass 11 runs in parallel with no blockers. While shadow runs execute,
the ecosystem advances through:

- **Pass 12** (Upstream Sentinel): toadStool Phase C (coral-driver),
  Songbird VPS relay, coralReef stability — these are escalated because
  upstream issues cascade to all downstream. toadStool team is actively
  working Phase C; we will pull their evolution and may amend this blurb
  with updated contracts as they ship.
- **Pass 13** (Gate Composition): BTSP dual-auth, ABG WCM through
  provenance trio, foundation thread seeding (3, 4, 8, 9, 10)
- **Pass 14** (Convergence): Tier 2 Science API (`toadstool.validate`),
  ionic runtime, skunkBat E2E audit, CompositionContext L2 pass

---

## toadStool Note

toadStool is actively working Phase C (coral-driver absorption: VFIO, DRM,
device abstraction). This is the highest-leverage upstream work — it
unblocks `toadstool.validate` + `toadstool.list_workloads` which in turn
unblocks all 8 springs' Tier 2 convergence.

**For toadStool team**: your Phase C work is Pass 12 priority. Continue
async — we will pull your evolution after this blurb lands and issue an
amended handoff with updated IPC contracts if the `compute.dispatch.execute`
surface changes. The `COMPUTE_TRIO_EVOLUTION.md` in primalSpring documents
the current contract expectations (Phases A+B done, Phase C pending).

**For everyone else**: toadStool Phase C does NOT block Pass 11. Start
your shadow runs now. Phase C blocks Pass 14 (Tier 2 API), not Pass 11.

---

## Sentinel Escalation Model

This pass follows the ecosystem's sentinel model:

- **Downstream surfaces the gap** — springs discover composition failures
- **Upstream owns the fix** — primal teams resolve at the source
- **primalSpring validates closure** — gate tests confirm correct composition
- **Escalation rule**: upstream issues are always higher priority than
  downstream. A primal regression cascades to all 8 springs; a spring
  gap affects only that spring. Primals are sentinels — most exposed to
  the glacial shift, least composed, first to feel schema pressure.

Pass 11 is L4 absorption work (no upstream issues). Pass 12 escalates
the three sentinel items that block downstream chains.

---

## References

| Topic | Location |
|-------|----------|
| Interstadial exit criteria + pass schedule | `infra/wateringHole/INTERSTADIAL_EXIT_CRITERIA.md` |
| Phase 32 atomic model handoff | `infra/wateringHole/handoffs/PRIMALSPRING_PHASE32_ATOMIC_EVOLUTION_MAY12_2026.md` |
| Compute trio evolution (toadStool contracts) | `primalSpring/docs/COMPUTE_TRIO_EVOLUTION.md` |
| Downstream pattern guide | `primalSpring/docs/DOWNSTREAM_PATTERN_GUIDE.md` |
| Live Science API (Tier 2 contract) | `primalSpring/docs/LIVE_SCIENCE_API.md` |
| Temporal ecosystem review | `primalSpring/docs/TEMPORAL_ECOSYSTEM_REVIEW_MAY12_2026.md` |
| Ecosystem evolution cycle | `infra/wateringHole/ECOSYSTEM_EVOLUTION_CYCLE.md` |
| Cross-spring parity scorecard | `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` |
