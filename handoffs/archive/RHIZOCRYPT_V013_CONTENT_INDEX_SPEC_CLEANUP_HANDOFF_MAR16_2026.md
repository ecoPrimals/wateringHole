<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Content Index Spec & Documentation Cleanup Handoff

**Date**: March 16, 2026 (session 13)
**Primal**: rhizoCrypt v0.13.0-dev
**Status**: Production Ready + Experiment Proposed

---

## Summary

Published the content similarity index experiment specification for rhizoCrypt
(locality-sensitive cross-session discovery), created Spring participation guide
for wateringHole, opened ISSUE-012 for cross-primal coordination, refreshed all
root documentation with current metrics, and performed archive/debris cleanup.

---

## Changes

### 1. Content Index Experiment Spec

- New spec: `specs/CONTENT_INDEX_EXPERIMENT.md`
- Proposes a locality-sensitive hash (LSH) secondary index for cross-session
  vertex similarity discovery
- Feature-gated behind `content-index` — zero impact on default builds
- Three implementation phases: LSH function → query integration → capability discovery
- Bridges rhizoCrypt's branching DAG with LoamSpine's linear spine through
  intentional hash collision analysis
- Inspired by hash collision sub-indexing research and fungal anastomosis biology

### 2. Spring Participation Guide

- New guide: `wateringHole/CONTENT_SIMILARITY_EXPERIMENT_GUIDE.md`
- Defines three participation phases for Springs:
  - Phase A (now): Audit vertex event types and metadata schemas
  - Phase B: Normalize event naming to `{domain}.{action}` convention
  - Phase C: Propose domain-specific LSH input features
- Includes per-Spring feature proposals (neuralSpring, wetSpring, airSpring, etc.)
- Privacy considerations for sensitive-data Springs

### 3. Cross-Primal Coordination

- ISSUE-012 opened in `SPRING_EVOLUTION_ISSUES.md`
- Tracks content similarity experiment as P3 (experimental, non-blocking)
- Links to both spec and participation guide

### 4. Documentation Refresh

- `specs/00_SPECIFICATIONS_INDEX.md`: Added experimental specs section, updated date
- `README.md`: Test count 1188→1222, coverage 91.63→92.32%, SPDX 107→110 files
- `CHANGELOG.md`: Session 13 entry with quality gates

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo test --workspace --all-features` | 1222 pass, 0 fail |
| Coverage | 92.32% lines (`--fail-under-lines 90`) |
| SPDX headers | All 110 `.rs` files |
| Max file size | All under 1000 lines |
| TODOs/FIXMEs in source | 0 |
| Production unwrap/expect | Zero |

---

## Artifacts

### New Files
- `rhizoCrypt/specs/CONTENT_INDEX_EXPERIMENT.md` — Experiment spec
- `wateringHole/CONTENT_SIMILARITY_EXPERIMENT_GUIDE.md` — Spring guide
- `wateringHole/handoffs/RHIZOCRYPT_V013_CONTENT_INDEX_SPEC_CLEANUP_HANDOFF_MAR16_2026.md` — This handoff

### Modified Files
- `rhizoCrypt/specs/00_SPECIFICATIONS_INDEX.md` — Added experimental section
- `rhizoCrypt/README.md` — Updated metrics
- `rhizoCrypt/CHANGELOG.md` — Session 13 entry
- `wateringHole/SPRING_EVOLUTION_ISSUES.md` — ISSUE-012

---

## Next Steps

1. **rhizoCrypt Phase 1**: Implement LSH function and `content_index` redb table
2. **Springs Phase A**: Each Spring audits their vertex event types and metadata schemas
3. **LoamSpine coordination**: Align on complementary linear collision experiments
4. **biomeOS**: Prepare `Capability::ContentSimilarity` registration when Phase 3 begins

---

## Cumulative Session Stats (sessions 1–13)

| Metric | Value |
|--------|-------|
| Tests | 1222 passing |
| Coverage | 92.32% line coverage |
| Clippy warnings | 0 |
| `unsafe` blocks | 0 |
| Source files | 110 `.rs` |
| Max file size | All under 1000 lines |
| Specs | 8 complete + 1 experimental |
| AGPL-3.0 SPDX | All files |

---

*rhizoCrypt: The memory that knows when to forget — and now knows what rhymes.*
