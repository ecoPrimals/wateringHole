# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V39 — NUCLEUS Composition Parity Handoff

**Date:** April 10, 2026
**From:** ludoSpring
**To:** primalSpring, barraCuda, rhizoCrypt, loamSpine, biomeOS
**Version:** V39 (session-sequential)

---

## Summary

ludoSpring evolves from Layer 2 (Rust→IPC) validation into full Layer 3
(IPC→NUCLEUS) composition parity. Python validated our Rust; now both
Python and Rust serve as validation targets for ecoPrimal NUCLEUS patterns.

### Three-layer chain (complete)

```text
Python baseline → validates → Rust library code       (Layer 1: 47 parity tests)
Rust library    → validates → IPC composition          (Layer 2: exp099, 13 checks)
IPC composition → validates → NUCLEUS primal graph     (Layer 3: exp100, 27 checks)
```

---

## Key Artifacts

### exp100 — NUCLEUS Composition Parity (NEW)

27-check validator covering:

- **Niche integrity** (7): name, domain, capability count, mapping consistency,
  dependency completeness, cost estimate completeness
- **Health probes** (2): `health.liveness`, `health.readiness`
- **Capability discovery** (4): `capability.list` completeness, game science,
  GPU, health cap presence
- **Science parity** (8): flow (3 states), Fitts (3 distances), engagement,
  noise — all through IPC with `ANALYTICAL_TOL`
- **Golden chain** (6): Python→Rust→IPC round-trip for flow score and Fitts ID

Exit code convention: 0 (pass), 1 (fail), 2 (skip — primals not running).

### capability_registry.toml (NEW)

Machine-readable SSOT at `config/capability_registry.toml` — synced with
`niche.rs`. Follows the neuralSpring registry pattern. Includes:
identity, fragments, capabilities by category, semantic mappings,
external primal dependencies, proto-nucleate reference.

### ecoBin Harvest

- **Binary:** `ludospring` v0.9.0, 3.1M PIE ELF x86-64
- **Staged to:** `infra/plasmidBin/ludospring/`
- **SHA-256:** `89d95ed03dbf8dfd1e1cf351aaf8743f8515251620961fc087d09e263bb6f5d5`
- **Capabilities:** 27 game + 3 infrastructure = 30 methods

---

## Quality Improvements

| Change | Impact |
|--------|--------|
| Coverage enforced in CI | 90% floor now blocks regressions at merge time |
| Shared HUD fixtures | Eliminated ~280 LOC duplication across dashboards |
| Dialogue constants centralized | `D6_SUCCESS_THRESHOLD`, `DIALOGUE_EMA_ALPHA` in tolerances |
| Provenance hash fixed | `python_parity.rs` commit matches current baseline JSON |
| Spec path corrected | `BARRACUDA_REQUIREMENTS.md` matches actual Cargo.toml |
| Forge naming fixed | `fraud_batch` → `anti_cheat_batch` |
| Makefile test parity | Local `make test` now matches CI scope |

---

## Active Gap Matrix (unchanged from V38)

| Gap | Owner | Severity | Impact |
|-----|-------|----------|--------|
| GAP-01: coralReef IPC not wired | coralReef + ludoSpring | Medium | Shader compile path aspirational only |
| GAP-02: barraCuda direct import | barraCuda IPC surface | Medium | composition_model="pure" but has path dep |
| GAP-03: Missing `nest_atomic` | primalSpring graphs | Low | Fragment metadata incomplete |
| GAP-04: TensorSession unused | ludoSpring | Medium | GPU promotion story has no proof |
| GAP-05: Trio not in proto-nucleate | primalSpring graphs | Low | biomeOS won't discover trio |
| GAP-06: rhizoCrypt TCP-only | rhizoCrypt team | **CRITICAL** | 9 composition checks fail |
| GAP-07: loamSpine startup panic | loamSpine team | **CRITICAL** | 6 composition checks fail |
| GAP-08: barraCuda Fitts mismatch | barraCuda team | HIGH | 4 composition checks fail |

---

## Primal Use and Evolution — What ludoSpring Learned

### Validation Chain as Pattern

The three-layer chain (Python → Rust → IPC → NUCLEUS) is a reusable pattern for
any spring. The key insight: each layer's outputs become the next layer's baselines.

```text
Published paper formula  →  Python reference script  →  combined_baselines.json
combined_baselines.json  →  Rust #[test] parity      →  composition_targets.json
composition_targets.json →  IPC integration tests     →  exp099 (13/13)
exp099 golden targets    →  NUCLEUS graph validation  →  exp100 (27 checks)
```

This pattern is spring-agnostic. wetSpring, hotSpring, or any new spring can
adopt the same chain structure. The key requirements:
1. Python baselines must be stdlib-only (no numpy/scipy) for reproducibility
2. Rust tests must use named tolerance constants with paper citations
3. IPC tests must use `ANALYTICAL_TOL` (1e-10) — any deviation signals a transport bug
4. NUCLEUS tests must validate the full graph composition, not just endpoint calls

### Primal Consumption Summary

| Primal | How ludoSpring Uses It | Transport | Evolution Need |
|--------|----------------------|-----------|---------------|
| **barraCuda** | Direct Cargo dep: `sigmoid`, `dot`, `lcg_step`, `state_to_f64`, `ValidationHarness`, tolerances | Library (path dep) | Expose `tensor.*` IPC → migrate from direct import (GAP-02) |
| **toadStool** | `compute.dispatch.submit/result/capabilities` for GPU workloads | JSON-RPC 2.0 / UDS | 3 game-specific WGSL shaders ready for absorption |
| **coralReef** | Aspirational: `shader.compile/validate` for f64-canonical WGSL | JSON-RPC 2.0 / UDS | Wire IPC client (GAP-01) |
| **petalTongue** | `visualization.render/push_scene` — 15 `GameChannelType` channels, 3 dashboard subcommands | JSON-RPC 2.0 / UDS | Stable — delegation handlers working |
| **Squirrel** | `ai.query/analyze/suggest` — NPC dialogue, narration, internal voices | JSON-RPC 2.0 / UDS | Awaiting Squirrel deployment (5 delegation stubs ready) |
| **NestGate** | `storage.store/retrieve` — game state, NPC snapshots, rulesets | JSON-RPC 2.0 / UDS | Awaiting NestGate deployment |
| **BearDog** | `crypto.sign/hash` — session integrity, action signing, Ed25519 chain | JSON-RPC 2.0 / UDS | Working — exp064 validated wire format |
| **Songbird** | `discovery.query/announce` — capability-based peer lookup | JSON-RPC 2.0 / UDS | Working — exp042 validated |
| **rhizoCrypt** | `provenance.append_vertex/get_dag` — session DAGs, fraud detection | JSON-RPC 2.0 / **TCP only** | **CRITICAL: needs UDS** (GAP-06) |
| **loamSpine** | `certificate.issue/verify` — ruleset certs, NPC personality certs | JSON-RPC 2.0 / UDS | **CRITICAL: startup panic** (GAP-07) |
| **sweetGrass** | `attribution.weave/trace` — player/AI creative attribution braids | JSON-RPC 2.0 / UDS | Waiting on rhizoCrypt UDS first |

### NUCLEUS Composition Patterns Discovered

**Pattern 1: Tower Atomic** (BearDog + Songbird)
- Minimal composable unit. Boot songbird for discovery, beardog for signing.
- ludoSpring validated this in exp042. Pattern works. Every spring should boot this.

**Pattern 2: Node Atomic** (Tower + toadStool)
- Adds compute dispatch. Game science routes GPU workloads through toadStool.
- Validated in exp033 (27 checks). toadStool fallback chain (GPU→NPU→CPU) proven.

**Pattern 3: Nest Atomic** (Node + NestGate + Provenance Trio)
- Adds persistence and provenance. Game sessions become auditable DAG structures.
- **Blocked** by rhizoCrypt UDS (GAP-06) and loamSpine panic (GAP-07).

**Pattern 4: Full NUCLEUS** (Nest + petalTongue + Squirrel + biomeOS orchestration)
- Complete game engine composition. 60Hz continuous coordination.
- Deploy graph at `graphs/ludospring_deploy.toml`. 27 capabilities exposed.
- ludoSpring validated 95/141 composition checks (67.4%) — blocked by GAP-06/07/08.

### neuralAPI / biomeOS Deployment Patterns

ludoSpring registers as a game science domain via `biomeos/niche.rs`:
- Domain registration: `neuralapi.domain.register("game", capabilities_list)`
- Capability discovery: `neuralapi.capability.discover("game.*")`
- Method dispatch: Standard JSON-RPC 2.0 to `game.evaluate_flow`, `game.fitts_cost`, etc.

The `capability_registry.toml` at `config/capability_registry.toml` is the machine-readable
SSOT. biomeOS should parse this for graph composition rather than hardcoding spring capabilities.

**Deployment sequence** (from `graphs/ludospring_deploy.toml`):
1. Boot Tower Atomic (beardog + songbird)
2. Boot toadStool (compute dispatch)
3. Boot ludospring (game science niche)
4. Register capabilities with biomeOS
5. Optional: boot petalTongue (visualization), NestGate (storage), trio (provenance)

### Absorption Opportunities for barraCuda

ludoSpring has proven these modules to production quality. They should be absorbed
into barraCuda as core primitives available to all springs:

| Module | Lines | What barraCuda Gets | Priority |
|--------|-------|---------------------|----------|
| `procedural::noise` | ~200 | Perlin 2D/3D + fBm (GPU WGSL shaders ready) | P1 |
| `procedural::wfc` | ~265 | Wave Function Collapse (GPU-parallel candidate) | P2 |
| `procedural::bsp` | ~220 | BSP spatial partitioning (deterministic LCG) | P2 |
| `capability_domains.rs` | ~100 | Structured Domain/Method introspection | P1 |
| `GenericFraudDetector` (exp065) | ~300 | Domain-agnostic graph fraud analysis (gaming/science/medical proven) | P3 |
| `compute_distribution` (exp066) | ~200 | Weighted-sum attribution with decay | P3 |

### Cross-Spring Patterns for Other Springs

**For wetSpring:** exp062 (field sample provenance) proved that ludoSpring's fraud detection
works on biological samples. The DAG isomorphism between game item tracking and sample
chain-of-custody is structural, not coincidental. wetSpring can adopt `GenericFraudDetector`.

**For healthSpring:** exp063 (consent-gated medical access) proved the provenance trio
works for patient-owned records with consent lending. Zero-knowledge proof patterns validated.

**For any new spring:** Follow the `exp100` pattern. Create a `capability_registry.toml`,
register your niche domain, build the three-layer validation chain. The `ValidationHarness`
from barraCuda provides the framework.

---

## Actions for Upstream Teams

### barraCuda
- Fix Fitts/Hick formula mismatch (GAP-08) — ludoSpring exp100 will immediately detect the fix
- Expose `tensor.*` IPC surface for spring migration from direct imports
- Absorb Perlin 2D/3D + fBm (P1), capability_domains (P1), WFC/BSP (P2)
- Adopt `D6_SUCCESS_THRESHOLD` / `DIALOGUE_EMA_ALPHA` pattern for game tolerances

### rhizoCrypt
- Add UDS transport alongside TCP (GAP-06) — blocks 9 composition checks across 4 experiments
- ludoSpring has 5 experiments waiting (exp052, 053, 094, 095, 098)

### loamSpine
- Fix runtime nesting panic on startup (GAP-07) — blocks 6 composition checks
- ludoSpring has 2 experiments waiting (exp095, 096)

### primalSpring
- Add `nest_atomic` to ludospring proto-nucleate fragments (GAP-03)
- Add optional trio nodes to proto-nucleate graph (GAP-05)
- Consider adopting `capability_registry.toml` as a cross-spring standard

### toadStool
- Absorb 3 game-science WGSL shaders (fog-of-war, tile lighting, pathfind wavefront)
- Inter-primal discovery gap: `compute.capabilities` returns stale data after hot-reload

### biomeOS
- Parse `capability_registry.toml` for graph composition instead of hardcoded spring capabilities
- neuralAPI capability registration gap blocks exp087/088 (14 checks)

### Squirrel
- ludoSpring has 5 delegation handler stubs (`ai.query`, `ai.analyze`, `ai.suggest`, `ai.narrate`, `ai.voice`) ready for connection once Squirrel deploys

### coralReef
- Wire IPC client for `shader.compile/validate` (GAP-01)
- ludoSpring has f64-canonical WGSL shaders ready for validation

### esotericWebb (gen4 product composition)
- FlowResult, EngagementResult, DifficultyAdjustmentResult, DialogueResponse, NarrationResponse response shapes already aligned to Webb's LudoSpringClient
- 13 MCP tool descriptors (8 science + 5 delegation) ready for AI integration

---

**License:** AGPL-3.0-or-later
