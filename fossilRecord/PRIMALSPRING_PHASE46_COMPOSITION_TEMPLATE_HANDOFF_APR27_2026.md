# primalSpring Phase 46 — Composition Template Abstraction & Downstream Handoff

**Date**: April 27, 2026
**From**: primalSpring v0.9.17+ (Phase 46)
**For**: All primal teams + all spring teams

---

## Summary

primalSpring extracted generic NUCLEUS wiring from the TTT reference implementation
into a reusable shell composition library. Springs can now build interactive
compositions by sourcing a single library and implementing domain hooks.

This completes the transition from ad-hoc scripted IPC to structured composition
templates with pluggable domain logic.

---

## What Changed

### New Artifacts

| File | Purpose |
|------|---------|
| `tools/nucleus_composition_lib.sh` | 41 reusable functions: capability discovery, JSON-RPC, petalTongue scenes/interaction/proprioception, rhizoCrypt DAG, loamSpine ledger, sweetGrass braids, sensor stream with discrete event types |
| `tools/composition_template.sh` | Minimal starter skeleton with documented hooks: `domain_init`, `domain_render`, `domain_on_key`, `domain_on_click`, `domain_on_tick` |
| `tools/composition_nucleus.sh` | Parameterized NUCLEUS launcher: `COMPOSITION_NAME`, `FAMILY_ID`, `PRIMAL_LIST`, `PETALTONGUE_LIVE` |
| `tools/ttt_composition.sh` | Refactored reference: only TTT domain logic (game state, rendering, branching DAG, provenance braids) |
| `wateringHole/DOWNSTREAM_COMPOSITION_EXPLORER_GUIDE.md` | Per-spring exploration lanes with full API reference |

### Updated Docs

| File | Change |
|------|--------|
| `wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` | Section 19: Shell Composition Library |
| `wateringHole/UPSTREAM_CROSSTALK_AND_DOWNSTREAM_ABSORPTION.md` | Convergent evolution model for per-spring exploration |
| `wateringHole/PLASMINBIN_DEPOT_PATTERN.md` | Interactive composition path using `composition_nucleus.sh` |
| `whitePaper/baseCamp/README.md` | Phase 46 section documenting composition template abstraction |
| `CONTEXT.md` | Updated graph count (67), shell composition library section |
| `README.md` | Updated architecture tree with new tools, graph count to 67 |

---

## The Composition Pattern

### For Springs (Graph-Based Deployment)
```
cell_graph.toml → biomeOS deploy → primals discover each other → Neural API routes
```

### For Springs (Interactive Exploration)
```
composition_nucleus.sh → starts primals from plasmidBin
composition_template.sh → sources nucleus_composition_lib.sh
domain hooks → interact with live NUCLEUS via UDS JSON-RPC
```

Both paths converge: interactive exploration discovers gaps and patterns that
inform graph-based deployments.

---

## Per-Spring Exploration Lanes

| Spring | Focus | Key Primals |
|--------|-------|-------------|
| **ludoSpring** | Interaction fidelity: mouse/keyboard/touch, playstyle metrics, 60Hz game loop | petalTongue, rhizoCrypt, loamSpine |
| **hotSpring** | Async computation: DAG memoization, non-blocking compute, precision visualization | barraCuda, toadStool, rhizoCrypt |
| **wetSpring** | Data visualization: genome browsers, phylogenetic trees, wet-lab data streams | petalTongue, sweetGrass, nestGate |
| **neuralSpring** | Agentic composition: Squirrel-driven UI, model-as-player, inference metrics | Squirrel, petalTongue, toadStool |

Each lane is complementary — discoveries in one inform all others.

---

## For Primal Teams

### What's Working Well
- All 13/13 capabilities BTSP-authenticated
- UDS JSON-RPC transport reliable across all primals
- Capability discovery via `{cap}-{family}.sock` naming
- petalTongue scene graph rendering via `motor.set_panel` + `visualization.scene.push`
- loamSpine ledger create/append/seal cycle
- sweetGrass braid provenance recording
- BearDog `security.sign` for payload signatures

### Known Upstream Gaps (Composition-Discovered)
| Gap | Primal | Impact | Status |
|-----|--------|--------|--------|
| PG-06 | rhizoCrypt | ~~`dag.session.create` returns empty on UDS~~ **RESOLVED** (S49) | Full JSON-RPC on UDS operational |
| PG-40 | petalTongue | winit requires main thread for live GUI | Workaround: `composition_nucleus.sh` starts petal in live mode |
| — | petalTongue | `xdotool` synthetic events don't propagate through egui/winit | Real user input works; test automation limited |
| — | biomeOS | Graph schema diverges from primalSpring `[[graph.nodes]]` | ludoSpring maintains compatible cell graph |

---

## For Downstream Teams — How to Start

```bash
# 1. Pull primalSpring and infra/wateringHole
# 2. Copy tools to your spring
cp primalSpring/tools/{nucleus_composition_lib.sh,composition_template.sh,composition_nucleus.sh} your_spring/tools/

# 3. Rename and edit composition_template.sh
# 4. Launch NUCLEUS
COMPOSITION_NAME=myspring ./tools/composition_nucleus.sh start

# 5. Run your composition
./tools/my_composition.sh
```

Read `primalSpring/wateringHole/DOWNSTREAM_COMPOSITION_EXPLORER_GUIDE.md` for
the full API reference and your spring's specific exploration goals.

---

## Convergent Evolution Model

Springs explore independently through domain-specific feedback loops. Each
spring discovers different gaps and patterns. primalSpring absorbs discoveries
into the composition library and hands refined patterns back upstream to primals.
This creates structured convergent evolution rather than top-down design.

**What springs hand back**: discovered primal gaps, domain-specific interaction
patterns, timing/polling optimizations, new capability requirements, and validated
composition patterns.

---

**License**: AGPL-3.0-or-later
