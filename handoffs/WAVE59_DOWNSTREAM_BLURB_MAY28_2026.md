# Wave 59 Downstream Blurb — cellMembrane, Projects, Springs

**Date:** May 28, 2026
**From:** primalSpring coordination
**To:** cellMembrane, projectNUCLEUS, projectFOUNDATION, all spring teams

---

## What primalSpring Shipped (Wave 58b → 59)

| Deliverable | Impact |
|-------------|--------|
| **Dispatch telemetry persistence** | `DispatchMetric` → JSON-lines. `flush_metrics_to_file()` for Layer 4/5 routing evolution training data. |
| **PermissiveVerifier** (was NoopVerifier) | Clarified fail-open auth verifier. Deprecated alias for backward compat. |
| **blake3 correctness** | Fixed misnamed `blake3_hash` that was using SHA-256. Nuclear lineage now genuinely BLAKE3. |
| **Primal name constants** | `primal_names::*` in orchestrator + routing. Zero hardcoded primal strings in production. |
| **21-file doc alignment** | All docs now canonical: 797+17 tests, 56 scenarios, 93 experiments, 97 graphs, 460 methods, v0.9.30. |
| **False readiness signal corrections** | NC-1 "CODE COMPLETE" (not "COMPLETE"). NC-3 "CODE CONSUMED" (sovereignty cutovers open). S2 DNS "DEPLOYED" (NS cutover pending). S4 CI "GitHub Actions" (git is Forgejo). |
| **11 handoffs archived** | wateringHole cleaned: 8 active, 355 archived. |

---

## For cellMembrane

**You remain the critical path.** All code is ready.

| Action | Priority | Blocker |
|--------|----------|---------|
| **Deploy biomeOS v3.84 to VPS** | **P0** | None — ecoBin harvested |
| Test `spring-overlay` with hotSpring | P0b | biomeOS on VPS |
| NS registrar cutover (knot-dns already running) | P3 | External registrar |
| Forgejo releases as sovereign binary channel | P3 | Forgejo config |

**Sovereignty update**: We corrected the S2 DNS status — your knot-dns is
**deployed** (not "planned"). The remaining step is NS record cutover at
your registrar to make it authoritative.

**CI sovereignty gap identified**: S4 git hosting is Forgejo-primary but
CI/CD is still GitHub Actions. This is a glacial gate observation, not a
stadial blocker.

---

## For projectNUCLEUS

**Your Wave 58 work is fully absorbed.** No new actions. NC-4 ADVANCING.

| Tracked | Status |
|---------|--------|
| 166 tests, async-correct, wire-native discovery | Absorbed in PRIMAL_GAPS |
| Deploy script `--uds-only` + socket health | Tracked |
| chrono removed, 68s → 3s test runtime | Acknowledged |

**NC-1 status**: Ensure your local tracking says **CODE COMPLETE** (biomeOS
v3.84 shipped `biomeos-pseudospore`). Live column U gated on VPS deploy.

---

## For projectFOUNDATION

**Phase B elevation complete.** Remaining tracked items:

| Item | Status |
|------|--------|
| FN-5 Phase C (domain-specific crates) | Open — unblocked |
| FN-1 backfill (thiserror, error chains) | Open — incremental |
| CI-R (sovereign CI runner) | Open — aligns with S4 gap |
| `FAMILY_ID` via `family.id` RPC | Verify on v3.84 once deployed |

---

## For All Spring Teams

See **WAVE59_SPRINGS_DELTA_BLURB** for per-spring deployment priorities.

**Key update**: Glacial review confirms software gate ~90% PASS. The
remaining ~60% gap is operational — VPS deploy, gate stabilization, live
mesh. Springs: prepare column U artifacts now.

---

*Wave 59. Code complete. Docs aligned. Sovereignty honest. Deploy.*
