# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V58 — Upstream Evolution Handoff

**Date:** May 9, 2026
**From:** ludoSpring V58 (eukaryotic UniBin, zero debt)
**To:** primalSpring, all primals teams, sibling springs
**Context:** Interstadial extinction wave complete for ludoSpring. Tier 3 → targeting Tier 4.

---

## 1. ludoSpring Status

| Metric | Value |
|--------|-------|
| Version | V58 |
| Clippy warnings | 0 |
| Test failures | 0 |
| Bare `#[allow]` | 0 |
| TODO/FIXME/HACK | 0 |
| Unsafe code | 0 (`#![forbid(unsafe_code)]`) |
| Files > 800 LOC | 0 (largest: 758) |
| Mocks in production | 0 |
| C/FFI dependencies | 0 (wgpu optional GPU only) |
| Workspace tests | 665+ |
| guideStone level | L4 (NUCLEUS validated) |
| Default feature | `ipc` (IPC-first) |
| primalSpring pin | v0.9.25 |
| UniBin subcommands | certify, validate, serve, status, version |

---

## 2. Patterns for Ecosystem Absorption

### 2.1 Method Constant Consolidation

ludoSpring's `ipc/methods.rs` has grown to **15 domain modules** with compile-time consistency tests. Pattern:
- Each IPC method gets a `pub const &str` in a domain module
- Certification tiers, validation scenarios, and handlers all reference constants
- A test ensures every constant is dotted (`"domain.method"`) and matches `capability_domains.rs`

**Recommendation for primalSpring:** Consider expanding the canonical 389-method registry to include `stats.*`, `rng.*`, `security.*` domains that ludoSpring now validates via IPC.

### 2.2 Test Module Lint Strategy

The ecosystem standard of `#[expect(..., reason)]` works for code that MUST trigger a lint. For test modules where `unwrap()`/`expect()` usage varies across test functions, use `#[allow(clippy::unwrap_used, clippy::expect_used, reason = "test assertions use unwrap/expect for clarity")]` to avoid unfulfilled expectation warnings.

### 2.3 Certification Organelle Pattern

ludoSpring absorbed guidestone's tier1/tier2/tier3 logic into a `certification/` library module. The UniBin binary delegates to `certification::certify(max_tier)`. The original `ludospring_guidestone` binary now contains one line: `certification::certify(3)`.

### 2.4 Scenario Registry with ScenarioMeta

Five representative experiments were absorbed into `validation/scenarios/` with:
```rust
pub struct ScenarioMeta {
    pub id: &'static str,
    pub track: Track,
    pub tier: Tier,
    pub provenance: &'static str,
}
```
The registry is queryable by tier, track, or ID. `ludospring validate --tier 1` runs only Rust-pure scenarios; `--tier 2` requires live primals.

### 2.5 IPC-First Default (Primal-Proof)

`barracuda/Cargo.toml` now has `default = ["ipc"]`. Library code behind `#[cfg(feature = "ipc")]` includes:
- All primal clients (toadStool, Squirrel, coralReef, petalTongue, NestGate, provenance trio)
- Server/handler infrastructure
- Composition validation

The `barracuda::` library calls (activations, stats, noise, raycaster) remain available unconditionally as the CPU computation layer. The architecture is: **library for validated math, IPC for primal composition**.

---

## 3. Open Gaps (Upstream Blockers)

| GAP | Owner | Impact | Notes |
|-----|-------|--------|-------|
| GAP-01 | coralReef | Shader pipeline not exercised E2E | Typed client exists; game engine still uses `include_str!` |
| GAP-02 | NestGate | storage.store/retrieve wired but not validated E2E | Requires live NestGate |
| GAP-03 | biomeOS | Cell graph exists, no live deploy tested | Blocks Tier 4 |
| GAP-04 | rhizoCrypt | Commit chain deterministic replay not validated | Requires UDS transport (GAP-06) |
| GAP-05 | primalSpring | Trio not in proto-nucleate graph | Graph completeness |
| GAP-06 | rhizoCrypt | No UDS transport | **Critical** — blocks 4 experiments |
| GAP-09 | biomeOS | Neural API registration | -14 checks |
| GAP-12 | primalSpring | 15 ludoSpring methods unregistered in canonical | Handback pending |
| GAP-14 | ludoSpring | Multiple commit hashes across validators | Internal — can resolve without upstream |

### Resolved This Wave
| GAP | Resolution |
|-----|-----------|
| GAP-13 | `#[cfg(feature = "gpu")]` gate on `for_precision_tier` — pushed to barraCuda upstream |
| GAP-15 | V56: Squirrel node added to gaming niche graph |
| GAP-07 | loamSpine startup panic — PG-33 |
| GAP-08/11 | Fitts/Hick formulation — PG-38 |
| GAP-10 | game.* graph identity — V53 pure composition |

---

## 4. Guidance for Specific Teams

### For primalSpring
- ludoSpring is **ready for Phase 60+ audit confirmation**
- 15 methods need canonical registration (GAP-12): `game.evaluate_flow`, `game.fitts_cost`, `game.engagement`, `game.generate_noise`, `game.wfc_step`, `game.analyze_ui`, `game.accessibility`, `game.difficulty_adjustment`, `game.begin_session`, `game.record_action`, `game.complete_session`, `game.mint_certificate`, `game.query_vertices`, `game.npc_dialogue`, `game.narrate_action`
- `certification/` organelle pattern ready for standard reference

### For barraCuda
- GAP-13 resolved (pushed). No further action needed.
- ludoSpring validates `stats.mean`, `stats.variance`, `stats.std_dev`, `rng.uniform` — potential expansion targets for barraCuda's IPC surface.
- `mul_add` FMA now used in raycaster and BSP — aligns with barraCuda's precision philosophy.

### For rhizoCrypt
- **GAP-06 is critical**: UDS transport blocks provenance trio integration (4 experiments). All wire format tests pass; only transport is missing.
- ludoSpring's `ipc/provenance/{rhizocrypt.rs, loamspine.rs, sweetgrass.rs}` per-trio modules are the ecosystem reference implementation.

### For biomeOS
- GAP-03: ludoSpring's `ludospring_cell.toml` (12 nodes) is ready for live deployment testing.
- GAP-09: Neural API registration endpoint needed for `game.npc_dialogue` etc to route via biomeOS Pathway Learner.
- ludoSpring's `biomeos/` module implements niche registration, domain advertisement, and Neural API — ready for live integration.

### For petalTongue
- 15 `GameChannelType` channels + `VisualizationPushClient` with capability-based discovery working.
- `UniBin` subcommands (`dashboard`, `live-session`, `tufte-dashboard`) serve as integration test harnesses.
- Pattern: `visualization.render` → discover petalTongue → push structured game scene data.

### For Sibling Springs
- **Pattern to absorb:** `ipc/methods.rs` constant consolidation (zero string drift)
- **Pattern to absorb:** `#[allow(..., reason)]` for test modules (avoids unfulfilled expectations)
- **Pattern to absorb:** `certification/` organelle (absorbed guidestone layers)
- **Pattern to absorb:** `validation/scenarios/` with `ScenarioMeta` registry
- **Pattern to absorb:** `circuit_breaker.rs` extracted module (IPC resilience)
- **Pattern to absorb:** `mul_add` for FMA precision in numerical kernels
- ludoSpring's per-trio provenance modules remain the reference for Nest atomic integration

---

## 5. NUCLEUS Composition for biomeOS Deployment

ludoSpring deploys as a **pure composition** — no spring binary in plasmidBin. The composition model:

```
biomeOS deploys ludospring_cell.toml
  → 12 NUCLEUS nodes (barraCuda, petalTongue, Squirrel, provenance trio, Tower Atomic)
  → Capabilities served by composed primals
  → ludospring binary = validation target only (not deployed)
```

The `lifecycle.composition` handler enables runtime proto-nucleate validation: any caller can ask ludoSpring "are your primals healthy?" and get a structured `CompositionReport`.

---

## 6. Next: Tier 4 Targets

1. Close remaining `barracuda::` calls not gated by `ipc` feature
2. Verify 60Hz tick budget with IPC-only (current: 0.6ms per tick, budget: 16.6ms)
3. Expand scenario registry (absorb more prokaryotic experiments as needed)
4. Evolve `discover_primal_tiered()` → `CompositionContext`
5. Live E2E with biomeOS deploying `ludospring_cell.toml`
