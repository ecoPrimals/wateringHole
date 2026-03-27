# LoamSpine v0.9.6 — Standards Compliance & Lint Evolution Handoff

**Date:** March 17, 2026  
**Version:** 0.9.6  
**Previous:** v0.9.5 (DispatchOutcome wiring, streaming sync, zero-copy)

---

## Summary

v0.9.6 focuses on standards compliance (PUBLIC_SURFACE_STANDARD, Semantic Method
Naming v2.1), bulk `#[allow]` → `#[expect(reason)]` migration, and smart
refactoring of the last oversize production module.

---

## Changes

### Standards Compliance
- **`capabilities.list` canonical method**: JSON-RPC dispatcher responds to
  `capabilities.list` (v2.1 standard), `capability.list` (legacy), and
  `primal.capabilities` (ecosystem alias).
- **`health.liveness` response**: Returns `{"status": "alive"}` per Semantic
  Method Naming Standard v2.1 (was `{"alive": true}`). `LivenessProbe` struct
  updated from `alive: bool` to `status: String`.
- **CONTEXT.md**: 65-line AI-discoverable context block per PUBLIC_SURFACE_STANDARD.
- **"Part of ecoPrimals" footer**: Added to README.md per PUBLIC_SURFACE_STANDARD.

### Lint Evolution
- **30+ test files**: `#[allow(clippy::...)]` → `#[expect(clippy::..., reason = "...")]`.
  Dead attributes removed where lints no longer fire (signals, spine, slice,
  discovery_client test modules). `redundant_clone` attributes pruned.

### Smart Refactoring
- **neural_api.rs**: 871 → 384 + 489 lines. Test module extracted to
  `neural_api_tests.rs` via `#[path]` pattern (same as lifecycle.rs, certificate.rs).

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,226 |
| Source files | 126 .rs |
| Max file size | 489 lines |
| Clippy warnings | 0 (pedantic + nursery) |
| Doc warnings | 0 |
| Unsafe in production | 0 |

---

## Ecosystem Alignment

- PUBLIC_SURFACE_STANDARD: CONTEXT.md, README footer — complete
- SEMANTIC_METHOD_NAMING_STANDARD v2.1: `capabilities.list` + `health.liveness` — complete
- SPRING_CROSS_EVOLUTION_STANDARD: `#[expect(reason)]` over `#[allow]` — complete
- COORDINATION_HANDOFF_STANDARD: This handoff — complete

---

## v0.9.7 Targets

- Storage backend error-path test expansion (redb edge cases)
- Signing capability middleware (RPC-layer signature verification)
- Showcase demo expansion
- Collision layer validation (neuralSpring experiments)
