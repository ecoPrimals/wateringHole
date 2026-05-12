# primalSpring v0.8.0g — Primal Rewiring + Gap Cleanup Handoff (April 1, 2026)

**From**: primalSpring coordination (Phase 23g)
**For**: All primal teams, spring teams, and ecosystem maintainers
**Reference**: `springs/primalSpring/docs/PRIMAL_GAPS.md` for gap registry

---

## What Changed

Full primal audit and code rewiring cycle. All 10 primals reviewed,
`primalSpring` internals updated to match latest APIs, gap registry
scoped to primal-only concerns, 98% live validation achieved.

## Code Rewiring Summary

### `ecoPrimal/src/ipc/methods.rs`
- `graph::DEPLOY` → `graph::EXECUTE` (matches biomeOS v2.81 actual routing)
- Added `topology::RESCAN` (biomeOS v2.81 topology rescan)
- Added `ember::LIST`, `ember::STATUS` (toadStool S171 hardware lifecycle)
- Added `ai::QUERY`, `ai::LIST_PROVIDERS` (Squirrel alpha.27)
- Added `visualization::*`, `interaction::*` (petalTongue latest)
- Removed `shader::COMPILE_WGSL` (coralReef domain since toadStool S169)
- Removed downstream modules: `game::*`, `webb::*`, `session::*` (springs own these)

### `ecoPrimal/src/ipc/neural_bridge.rs`
- `topology_rescan()` for biomeOS v2.81+ neural API

### `ecoPrimal/src/ipc/discover.rs`
- 6-tier discovery (was 5-tier) with plain socket names
- Supports `{name}.sock` and `{name}-ipc.sock` patterns

### `tools/validate_compositions.py`
- SQ-02 resolved: removed "expected gap" messaging
- NestGate `storage.list` now passes `family_id` parameter
- C7 interactive: live Squirrel check (was hardcoded fail)

## Gap Resolution (5 newly resolved)

| ID | Primal | Issue | Resolution |
|----|--------|-------|------------|
| SQ-02 | Squirrel | `LOCAL_AI_ENDPOINT` not wired | AiRouter wired in alpha.27 |
| PT-05 | petalTongue | `RenderingAwareness` not auto-init | Auto-init in `UnixSocketServer` |
| PT-07 | petalTongue | No periodic discovery refresh | Server-mode discovery refresh added |
| NG-04 | NestGate | ring/aws-lc-rs C dependency | Eliminated — TLS via system curl |
| NG-05 | NestGate | nestgate-security crypto weight | Zero crypto deps — BearDog IPC delegation |

## Remaining Open Gaps (8)

| ID | Primal | Severity | Summary |
|----|--------|----------|---------|
| NG-01 | NestGate | Medium | `storage.list` returns empty without filter semantics |
| NG-02 | NestGate | Low | No `storage.query` for structured queries |
| NG-03 | NestGate | Low | No pagination on list operations |
| PT-04 | petalTongue | Low | `visualization.render.scene` not yet implemented |
| PT-06 | petalTongue | Low | No `visualization.export` endpoint |
| SQ-03 | Squirrel | Low | No `ai.list_models` for model inventory |
| SB-02 | Songbird | Low | `mesh.peers` not yet implemented |
| SB-03 | Songbird | Low | No `mesh.topology` for network map |

## Nucleated Spring Deploy Graphs (6 new)

Created proto-compositions for downstream springs in `graphs/spring_deploy/`:

| Spring | File | Domain Primals |
|--------|------|----------------|
| airSpring | `airspring_deploy.toml` | barraCuda, Squirrel, Provenance Trio |
| groundSpring | `groundspring_deploy.toml` | barraCuda, toadStool, NestGate, Provenance Trio |
| healthSpring | `healthspring_deploy.toml` | Squirrel, NestGate, Provenance Trio |
| hotSpring | `hotspring_deploy.toml` | toadStool, coralReef, barraCuda, NestGate, Provenance Trio |
| neuralSpring | `neuralspring_deploy.toml` | toadStool, coralReef, barraCuda, Squirrel, NestGate, Provenance Trio |
| wetSpring | `wetspring_deploy.toml` | toadStool, barraCuda, NestGate, Provenance Trio |

All share NUCLEUS base: biomeOS + BearDog + Songbird.

## Live Validation Results

**43/44 (98%)** — up from 93% pre-rewiring, 79% pre-evolution

| Composition | Result | Notes |
|-------------|--------|-------|
| C1: Render (petalTongue) | **6/6 PASS** | |
| C2: Narration (Squirrel) | **3/4 PARTIAL** | `ai.query` needs local Ollama — code wired (SQ-02 resolved) |
| C3: Session (esotericWebb) | **8/8 PASS** | |
| C4: Game Science (ludoSpring) | **6/6 PASS** | |
| C5: Persistence (NestGate) | **5/5 PASS** | Was partial — `family_id` parameter fix |
| C6: Proprioception (petalTongue) | **5/5 PASS** | |
| C7: Full Interactive | **10/10 PASS** | Was 9/10 — Squirrel liveness now live |

## Action Items for Teams

### Primal Teams
- **NestGate**: NG-01 (`storage.list` filter semantics) is the only medium-severity gap
- **petalTongue**: PT-04 (scene render) and PT-06 (export) when ready
- **Squirrel**: SQ-03 (model listing) — low priority, nice-to-have
- **Songbird**: SB-02/SB-03 (mesh peers/topology) — low priority

### Spring Teams
- Your nucleated deploy graph in `graphs/spring_deploy/` is your starting point
- Validate against it; gaps you discover flow back upstream to primalSpring
- Follow `wateringHole/COMPOSITION_PATTERNS.md` for graph conventions

---

**Tests**: 403 (all passing), **Clippy**: 0 warnings, **Fmt**: clean, **Unsafe**: forbidden
