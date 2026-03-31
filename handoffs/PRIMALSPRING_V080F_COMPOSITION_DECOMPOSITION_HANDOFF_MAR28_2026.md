# primalSpring v0.8.0f — Composition Decomposition Handoff

**Date**: March 28, 2026
**From**: primalSpring coordination
**Phase**: 23f — Composition Decomposition

---

## Summary

primalSpring decomposed its monolithic interactive composition into 7 independently
deployable subsystem compositions (C1-C7), each with its own biomeOS deploy graph
and validation graph. A structured primal gap registry documents 22 gaps across
6 primals. The gateway was refactored from a monolithic orchestrator to a thin
WebSocket-to-IPC bridge with zero business logic.

## What Changed

### New: 7 Composition Subsystems (`graphs/compositions/`)

Each subfunction is a separately deployable biomeOS graph:

| ID | Name | Primals | Purpose |
|----|------|---------|---------|
| C1 | Render | biomeOS + petalTongue | Dashboard render, SVG export, scene storage |
| C2 | Narration | biomeOS + Squirrel | AI narration via Ollama/HuggingFace |
| C3 | Session | biomeOS + Tower + esotericWebb | Narrative session lifecycle |
| C4 | Game Science | biomeOS + Tower + ludoSpring | Flow evaluation, Fitts, WFC, engagement |
| C5 | Persistence | biomeOS + Tower + NestGate | Storage round-trip, blob management |
| C6 | Proprioception | biomeOS + petalTongue | Interaction subscribe/poll/apply, awareness |
| C7 | Full Interactive | All of the above | The composed product |

### New: Primal Gap Registry (`docs/PRIMAL_GAPS.md`)

22 documented gaps with severity, composition exposure, and fix paths:

**High priority** (blocks interactive product):
- PT-02: petalTongue web_mode has no WebSocket/SSE for live push
- SQ-01: Squirrel AiRouter cannot reach Ollama HTTP natively
- EW-01: esotericWebb push_scene_to_ui sends wrong format for petalTongue

**Medium priority** (improves composition quality):
- NG-01: NestGate in-memory KV stub, not persisted
- PT-05: petalTongue rendering_awareness not initialized in server mode
- EW-02: esotericWebb poll_input not wired into game loop
- LS-01: ludoSpring flow params hardcoded instead of derived from game state

### Changed: Thin Gateway Bridge

`tools/ws_gateway.py` refactored from ~400 lines of mixed business logic to a
generic WebSocket-to-IPC bridge:
- Generic `rpc`, `ollama`, `health`, `discover`, `batch` message types
- Socket resolution via biomeOS `capability.discover` with local fallback
- Zero binding construction, zero narration prompting, zero state mapping
- Business logic moved to client (composition monitor) and primals

### Changed: Composition Monitor

`web/play.html` reclassified from "game UI" to "COMPOSITION MONITOR":
- Primal health grid with composition membership
- C1-C7 subsystem cards with click-to-test validation
- Game session moved to "Debug" section
- All RPC calls use thin bridge protocol

### Live Validation Results

| Composition | Result | Notes |
|-------------|--------|-------|
| C1: Render | **6/6 PASS** | Dashboard, export, SceneGraph, session awareness |
| C2: Narration | 0/3 FAIL | Expected — Squirrel not running (SQ-01) |
| C3: Session | **8/8 PASS** | Full lifecycle, actions, act, graph |
| C4: Game Science | **6/6 PASS** | Flow, Fitts, WFC, engagement |
| C5: Persistence | 1/5 PARTIAL | Expected — NestGate stopped (NG-01) |
| C6: Proprioception | **5/5 PASS** | Subscribe, apply, poll, showing |
| C7: Full Interactive | 8/10 PARTIAL | Only C2+C5 gaps propagate |
| **TOTAL** | **34/43 (79%)** | All failures traced to documented gaps |

## What This Means for Other Teams

### For Primal Teams

Each primal team can now test their primal in isolation via the corresponding
composition graph. Gaps are documented with severity and fix paths in
`docs/PRIMAL_GAPS.md`. See the team-specific handoffs below.

### For Spring Teams

Springs should reference primalSpring's composition patterns when building
their own deployed science. The thin gateway pattern (WebSocket → capability.discover
→ primal IPC) is the recommended integration model for any spring that wants
to expose interactive capabilities.

### For biomeOS

The composition subsystems validate biomeOS's capability.discover and graph.execute
end-to-end. The primal gap registry documents where biomeOS interop breaks
(BM-02: no health.liveness on Neural API, BM-03: unix:// prefix inconsistency —
both already worked around in primalSpring).

## Files Created/Changed

```
graphs/compositions/render_standalone.toml          # NEW — C1
graphs/compositions/narration_ai.toml               # NEW — C2
graphs/compositions/session_standalone.toml          # NEW — C3
graphs/compositions/game_science_standalone.toml     # NEW — C4
graphs/compositions/persistence_standalone.toml      # NEW — C5
graphs/compositions/proprioception_loop.toml         # NEW — C6
graphs/compositions/interactive_product.toml         # NEW — C7
graphs/spring_validation/composition_*_validate.toml # NEW — 7 validation graphs
docs/PRIMAL_GAPS.md                                  # NEW — gap registry
tools/ws_gateway.py                                  # REFACTORED — thin bridge
tools/validate_compositions.py                       # NEW — live validator
web/play.html                                        # REFACTORED — composition monitor
README.md, CHANGELOG.md, CONTEXT.md                  # UPDATED
whitePaper/baseCamp/README.md                        # UPDATED
wateringHole/README.md                               # UPDATED
experiments/README.md                                # UPDATED
```

## Next Steps

1. **Primal teams**: Fix high-priority gaps (PT-02, SQ-01, EW-01)
2. **ludoSpring**: Focus on game science + function while primalSpring focuses on composition
3. **Springs**: Build deployed science compositions referencing wateringHole patterns
4. **primalSpring**: Focus on biomeOS deployment, composition gaps, and functional primal debt
5. **esotericWebb**: Evolve from composition product to standalone deployable
