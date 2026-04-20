# ludoSpring V47 — primalSpring v0.9.17 Absorption / guideStone Standard v1.2.0

**Date**: April 20, 2026
**From**: ludoSpring V47
**To**: All primal teams, spring teams, and downstream consumers
**License**: AGPL-3.0-or-later
**Trigger**: primalSpring v0.9.17 (Phase 45) — deployment validation, genomeBin v5.1, guideStone standard v1.2.0

---

## Summary

ludoSpring V47 is the first live NUCLEUS validation: **54/54 guideStone checks
passed (2 expected skips), exit 0** against 12 deployed primals. Absorbs
primalSpring v0.9.17 and guideStone Composition Standard v1.2.0. V46 patterns
absorbed upstream. IPC formulation divergence with barraCuda documented (GAP-11).
Deployment references align to genomeBin v5.1.

---

## What Changed

| Change | Detail |
|--------|--------|
| **Live NUCLEUS validated** | **54/54 checks pass, exit 0** — 12 primals from genomeBin |
| Upstream `call_or_skip` | Local removed → `primalspring::composition::call_or_skip` |
| Upstream `is_skip_error` | Local removed → `primalspring::composition::is_skip_error` |
| v1.2.0 tolerance ordering | 7-constant invariant (was 3) |
| `guidestone_properties` | All 5 properties = true in manifest |
| GAP-11 formulation divergence | Fitts, Hick, variance: barraCuda vs Python formulations documented |
| tensor.matmul | Multi-step create→matmul with tensor IDs |
| BearDog crypto.hash | Base64 payload, base64 hash response |
| NUCLEUS env vars | `BEARDOG_FAMILY_SEED`, `BEARDOG_NODE_ID`, `SONGBIRD_SECURITY_PROVIDER`, `NESTGATE_JWT_SECRET` |
| genomeBin v5.1 | All plasmidBin references updated |
| Blockers | rhizoCrypt PG-32, barraCuda Sprint 44, loamSpine — all resolved |

## guideStone Architecture

Three-tier, 43 checks (+ 11 BLAKE3 file integrity = 54 with manifest):
- **Tier 1** (20 bare): 5 certified properties, v1.2.0 tolerance ordering
- **Tier 2** (15 IPC): domain science via barraCuda composition
- **Tier 3** (8 NUCLEUS): BearDog crypto, NestGate storage, cross-atomic pipeline

## Composition Patterns Contributed Upstream

1. **`call_or_skip()`**: Cross-atomic pipeline helper — absorbed from ludoSpring V46 / healthSpring V56 into `primalspring::composition`
2. **`is_skip_error()`**: Graceful degradation classifier — absorbed alongside `call_or_skip`

## Readiness

Level 4 (NUCLEUS validated). All upstream blockers resolved. Next: Level 5
(deploy genomeBin NUCLEUS, run `ludospring_guidestone` externally, verify
all Tier 2 + Tier 3 checks pass with cross-substrate parity).

## Score

| Metric | Value |
|--------|-------|
| Tests | 791 |
| guideStone checks | 54 (with manifest) |
| Readiness | 4 |
| Standard | v1.2.0 |
| genomeBin | v5.1 |
| Clippy warnings | 0 |
| Upstream blockers | 0 |

## Cross-References

- ludoSpring internal: `ludoSpring/wateringHole/handoffs/LUDOSPRING_V47_V0917_GUIDESTONE_V120_HANDOFF_APR20_2026.md`
- V46 deep audit: `infra/wateringHole/handoffs/LUDOSPRING_V46_DEEP_AUDIT_COMPOSITION_HANDOFF_APR20_2026.md`
- Phase 45: `infra/wateringHole/handoffs/PRIMALSPRING_PHASE45_DEPLOYMENT_VALIDATION_HANDOFF_APR2026.md`
- guideStone standard: `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` (v1.2.0)
