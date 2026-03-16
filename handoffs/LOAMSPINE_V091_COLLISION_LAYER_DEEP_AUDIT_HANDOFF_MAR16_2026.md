# LoamSpine v0.9.1 — Collision Layer Architecture, Deep Audit & Idiomatic Evolution

**Date**: March 16, 2026  
**Version**: 0.9.1  
**Previous**: v0.9.0 (Deep Debt, ecoBin, Attestation Enforcement)  
**Supersedes**: LOAMSPINE_V090_DEEP_DEBT_ECOBIN_ATTESTATION_HANDOFF_MAR16_2026.md

---

## Summary

Research and audit session. Introduced the Collision Layer Architecture proposal —
a hash-based collision resolution system bridging LoamSpine's linear spine with
rhizoCrypt's DAG, inspired by sub-hash collision resolution, 19th century cross-
writing, and mycelial network anastomosis. Published experiment guidance for
neuralSpring and healthSpring.

Simultaneously completed deep audit execution: evolved StubAttestationProvider to
real JSON-RPC implementation, added 29 new tests across attestation, discovery,
and CLI signer modules, smart-refactored oversized test files.

---

## Changes

### Research

1. **Collision Layer Architecture** — `specs/COLLISION_LAYER_ARCHITECTURE.md`: Hash resolution hierarchy (Blake3-256 → truncated projections), sub-hash resolution trees, cross-writing information recovery model, bidirectional bridge (linear ↔ DAG), data science applications
2. **Spring experiment guidance** — `wateringHole/COLLISION_LAYER_EXPERIMENT_GUIDANCE.md`: 3 experiment protocols for neuralSpring (collision topology as clustering, cross-writing recovery) and healthSpring (domain-specific projections), validation criteria, integration path

### Audit & Evolution

3. **`StubAttestationProvider` → `DiscoveredAttestationProvider`** — Production stub evolved to real JSON-RPC TCP implementation. Sends `attestation.request` to capability-discovered endpoint; degrades gracefully with tracing warning when unreachable.
4. **29 new tests** — Attestation provider lifecycle (8), infant discovery extended (10), CLI signer extended (11)
5. **tarpc server named constants** — `TARPC_MAX_CONCURRENT_REQUESTS`, `TARPC_MAX_CHANNELS_PER_IP`
6. **JSON-RPC Content-Length warning** — Silent parse failure evolved to `tracing::warn`
7. **`fuzz/Cargo.toml` license** — Added `AGPL-3.0-or-later`
8. **Smart file split** — `infant_discovery/tests.rs` (1,116 → 532 + 589)

---

## Quality Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,180+ |
| Coverage | 92% line / 90% region |
| Clippy | 0 warnings (pedantic + nursery, all features, -D warnings) |
| Unsafe (prod) | 0 |
| Max file | 955 lines (all under 1,000) |
| Source files | 119 `.rs` files |
| ecoBin | PASS (blake3 pure, zero C deps) |
| License | AGPL-3.0-or-later |
| All checks | `cargo check`, `cargo clippy`, `cargo fmt`, `cargo doc`, `cargo test` — PASS |

---

## Cross-Spring Patterns

| Pattern | Source | Status |
|---------|--------|--------|
| Collision layer experiments | specs/COLLISION_LAYER_ARCHITECTURE.md | Published to neuralSpring |
| Cross-writing hypothesis | wateringHole/COLLISION_LAYER_EXPERIMENT_GUIDANCE.md | Experiment 2 protocol |
| Domain collision projections | wateringHole/COLLISION_LAYER_EXPERIMENT_GUIDANCE.md | healthSpring protocol |

---

## What's Next (v0.9.2)

- Signing capability middleware (capability-discovered)
- Showcase demos expansion
- neuralSpring collision layer validation (Python baseline)
- PostgreSQL/RocksDB backends (v1.0.0)

---

*Supersedes: LOAMSPINE_V090_DEEP_DEBT_ECOBIN_ATTESTATION_HANDOFF_MAR16_2026.md*
