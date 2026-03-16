# SweetGrass v0.7.17 — Ecosystem Absorption + Lint Tightening + Capability Evolution

**Date**: March 16, 2026
**Version**: v0.7.15 → v0.7.17 (v0.7.16 was internal audit remediation)
**Theme**: Absorb ecosystem patterns, tighten lints to trio parity, evolve capability.list, generic primal discovery
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V0715_DEEP_DEBT_COVERAGE_CONVERGENCE_HANDOFF_MAR16_2026.md` (archived)

---

## Summary

Comprehensive ecosystem review of hotSpring (ground, neural, wet, air, health, ludo),
phase1/phase2 primals, and wateringHole standards. Absorbed the highest-value patterns:
lint parity with trio partners, capability.list ecosystem compatibility, Edition 2024
for shared types, and generic capability-based env var pattern. Smart-refactored four
more large files. Eliminated dead hardcoding.

---

## Changes

### 1. Lint Tightening (Trio Parity)

| Lint | Before | After | Rationale |
|------|--------|-------|-----------|
| `unwrap_used` | `warn` | `deny` | Matches rhizoCrypt + loamSpine |
| `expect_used` | `warn` | `deny` | Matches rhizoCrypt + loamSpine |
| `deny.toml` wildcards | `allow` | `deny` | airSpring V084 ecosystem standard |

All existing test code uses `#[expect(reason)]` — no breakage.

### 2. capability.list Evolution

Response now includes `"capabilities"` key (flat array of method names) alongside
existing `"methods"`, `"domains"`, and `"operations"`. This matches the neuralSpring
S156 consensus format where `parse_capability_list()` looks for either a flat array
or `{"capabilities": [...]}`.

### 3. provenance-trio-types Edition 2024

| Field | Before | After |
|-------|--------|-------|
| edition | 2021 | 2024 |
| rust-version | (none) | 1.87 |
| version | 0.1.0 | 0.1.1 |

All trio partners now share the same edition and MSRV.

### 4. Generic Primal Name Pattern

Replaced 5 dead per-primal socket constants (`RHIZOCRYPT_SOCKET`, `LOAMSPINE_SOCKET`,
etc.) with generic functions:

```rust
pub fn socket_env_var(primal_name: &str) -> String  // "RHIZOCRYPT_SOCKET"
pub fn address_env_var(primal_name: &str) -> String  // "RHIZOCRYPT_ADDRESS"
```

Any new primal works without code changes. Infrastructure env vars (`BIOMEOS_SOCKET_DIR`,
`BIOMEOS_FAMILY_ID`, `XDG_RUNTIME_DIR`) retained as ecosystem constants.

### 5. Smart Refactoring (4 Files)

| File | Before | Production | Tests |
|------|--------|-----------|-------|
| `anchor.rs` | 687 | 446 | 230 |
| `activity.rs` | 621 | 494 | 130 |
| `privacy.rs` | 642 | 377 | 268 |
| `engine.rs` | 586 | 300 | 281 |

Three remaining 500+ line files analyzed and confirmed as single-concern cohesive
modules (store/mod.rs 714, config/mod.rs 630, server/mod.rs 573) — no splitting warranted.

### 6. Storage Path Documentation

All `DEFAULT_*_PATH` constants documented as self-config fallbacks with env override
guidance. Production deployments use `SweetGrassConfig`.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,004 passing (was 1,001) |
| .rs files | 125 (was 122) |
| Clippy | 0 warnings (`-D warnings`) |
| Unsafe | 0 (entire workspace) |
| Max file | 808 lines |
| TODOs | 0 |
| SPDX | All 125 files |

---

## Upstream Impact

### For Trio Partners (rhizoCrypt, loamSpine)

- `provenance-trio-types` bumped to 0.1.1 / Edition 2024 — update dependency
- `capability.list` now includes `"capabilities"` key — consumers can use it

### For biomeOS

- Generic `socket_env_var()` / `address_env_var()` pattern available for any primal
- No primal-specific socket constants needed in orchestration code

### For Springs

- sweetGrass now passes `deny.toml` wildcards=deny — aligned with airSpring V084
- Content Convergence experiment (from v0.7.15) still available as Phase A

---

## What's Next

- Real tarpc integration testing with rhizoCrypt and loamSpine
- Content Convergence Phase 1 implementation (`convergence.query`)
- Pipeline coordination handshakes (toadStool → rhizoCrypt → sweetGrass)
- sunCloud integration for reward distribution
