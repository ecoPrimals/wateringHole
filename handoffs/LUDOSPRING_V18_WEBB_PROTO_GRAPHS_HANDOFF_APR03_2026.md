<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation and creative text in this file: CC-BY-SA-4.0
-->

# ludoSpring V18 — Webb Proto Graph Sketches Handoff

**Date:** April 3, 2026
**From:** ludoSpring (game science spring)
**To:** esotericWebb (garden), primalSpring (ecosystem coordination)
**Status:** Complete
**License:** AGPL-3.0-or-later

---

## Summary

ludoSpring V18 provides 9 proto deploy graph sketches for esotericWebb to
absorb, mirroring the pattern primalSpring used for ludoSpring in V15. Each
sketch translates a validated ludoSpring experiment composition (exp073-exp077)
into Webb's product context.

This completes the three-layer co-evolution chain:

```
primalSpring → ludoSpring → esotericWebb
  (infra)      (science)     (product)
```

Webb references both springs as it evolves: primalSpring for structural
validation patterns and BYOB templates, ludoSpring for game science
composition patterns and novel multi-primal compositions.

---

## What Changed

### New Files (ludoSpring)

**7 proto deploy graph sketches** in `graphs/sketches/`:

| File | Composition | Webb GAP |
|------|-------------|----------|
| `esotericwebb_sovereign_save_deploy.toml` | Tower + trio (rhizoCrypt + loamSpine + BearDog) + ludoSpring | GAP-004, GAP-019 |
| `esotericwebb_session_primal_deploy.toml` | biomeOS lifecycle + rhizoCrypt + ludoSpring | Novel |
| `esotericwebb_attributed_narration_deploy.toml` | Squirrel + sweetGrass + rhizoCrypt + ludoSpring | GAP-003, GAP-007 |
| `esotericwebb_science_overlay_deploy.toml` | petalTongue + rhizoCrypt + ludoSpring | GAP-002, GAP-021 |
| `esotericwebb_sovereign_render_deploy.toml` | toadStool + coralReef + barraCuda | VISION 5 |
| `esotericwebb_multiplayer_deploy.toml` | Songbird mesh + shared DAG + sweetGrass | VISION 4 |
| `esotericwebb_creative_studio_deploy.toml` | petalTongue + nestGate + loamSpine + ludoSpring | GAP-008, GAP-009 |

**2 proto validation graph sketches** in `graphs/sketches/validation/`:

| File | Validates |
|------|-----------|
| `esotericwebb_sovereign_save_validate.toml` | Trio round-trip, BearDog signing, certs, session lifecycle |
| `esotericwebb_full_composition_validate.toml` | All 7 primal domains, session E2E, provenance E2E |

**1 sketches README** at `graphs/sketches/README.md` documenting the taxonomy,
absorption instructions, and cross-references.

### Updated Files

- `graphs/README.md` — added V18 proto sketch section
- `README.md` — bumped to V18, added proto sketch summary and architecture note

---

## Design Decisions

### ludoSpring is optional in all sketches

Webb V6 owns flow/engagement/DDA locally via its `science/` module. In every
proto sketch, the `ludospring` node is `required = false`. When present,
ludoSpring enriches with advanced metrics (WFC, Fitts, accessibility). When
absent, Webb works standalone. This respects Webb's V6 decomposition decision
(GAP-016 superseded).

### `[[graph.node]]` schema

All sketches use the same `[[graph.node]]` TOML schema that ludoSpring's
`deploy` module parses and primalSpring's BYOB template defines. Webb can
validate these graphs using the same typed `DeployGraph` / `GraphNode` parsing
without importing any spring as a Rust dependency.

### PROTO SKETCH convention

Every file includes a comment header stating:
- It is a proto sketch (not a production graph)
- ludoSpring does not own the esotericwebb binary
- esotericWebb takes ownership at graduation
- Which ludoSpring experiment validated the composition
- Which Webb EVOLUTION_GAPS the composition addresses

---

## Absorption Path for esotericWebb

1. **Review** each proto sketch and the corresponding ludoSpring experiment
2. **Copy** desired sketches to `esotericWebb/graphs/`
3. **Adapt** to Webb's PrimalBridge and V6 architecture:
   - Adjust capability names to match bridge method inventory
   - Set `required` flags based on Webb's degradation preferences
   - Add Webb-specific node ordering if needed
4. **Validate** the graph parses correctly
5. **Graduate** the sketch into an owned deploy graph (remove PROTO SKETCH header)
6. **Update** EVOLUTION_GAPS.md to mark addressed gaps as "wiring in progress"

### Recommended absorption order

1. **Sovereign Save** — most immediately useful (replaces JSON saves)
2. **Attributed Narration** — enriches existing AI DM pipeline
3. **Science Overlay** — visual debugging for game sessions
4. **Session-as-Primal** — most architecturally transformative
5. **Creative Studio** — unlocks content pack distribution
6. **Sovereign Render** — GPU pipeline (deferred until toadStool matures)
7. **Multiplayer** — multi-gate (deferred until Songbird mesh stabilizes)

---

## What Webb Already Has (no duplication)

Webb already owns 8 graphs in `graphs/`:

| Webb graph | Overlap with sketch? |
|------------|---------------------|
| `webb_tower.toml` | No — minimum viable, no provenance or AI |
| `webb_node.toml` | Partial — toadStool compute, but no coralReef/barraCuda |
| `webb_ai_viz.toml` | Partial — Squirrel + petalTongue, but no attribution |
| `webb_provenance.toml` | Partial — rhizoCrypt only, no loamSpine/sweetGrass |
| `webb_provenance_trio.toml` | Partial — trio, but no Tower or Webb node |
| `webb_full.toml` | Partial — comprehensive but monolithic, no validation |
| `webb_nest.toml` | Partial — nestGate, but no loamSpine certification |
| `esotericwebb_full.toml` | Near-complete overlap — this is the full BYOB stack |

The proto sketches are **focused compositions** that Webb can adopt individually.
They are more targeted than `esotericwebb_full.toml` (which tries to do everything)
and address specific gaps that the existing per-domain graphs don't cover.

---

## What primalSpring Already Provided

primalSpring previously provided proto sketches that both ludoSpring and
esotericWebb absorbed:

| primalSpring sketch | Status |
|---------------------|--------|
| `esotericwebb_tower_deploy.toml` | Webb absorbed as `webb_tower.toml` |
| `esotericwebb_composed_deploy.toml` | Webb absorbed as `esotericwebb_full.toml` |
| `ludospring_game_deploy.toml` | ludoSpring absorbed into `graphs/` (V15) |

The V18 ludoSpring sketches extend this: they provide **game-science-validated
compositions** that primalSpring's structural sketches did not cover. The three
layers are complementary:

- **primalSpring sketches** — "here is how deploy graphs work structurally"
- **ludoSpring sketches** — "here is what specific compositions validate scientifically"
- **Webb's own graphs** — "here is how the product deploys"

---

## Cross-References

- ludoSpring graphs/sketches/README.md — full taxonomy and absorption details
- ludoSpring specs/PRIMAL_LEVERAGE_MAP.md — primal-to-game-science mapping
- ludoSpring experiments exp073-exp077 — validation evidence for each composition
- esotericWebb EVOLUTION_GAPS.md — gap registry (GAP-002 through GAP-021)
- esotericWebb specs/VISION_AND_EVOLUTION.md — 6 evolution vectors
- primalSpring graphs/sketches/ — structural proto sketches (upstream of this)
- primalSpring graphs/spring_byob_template.toml — BYOB graph template convention
- sourDough specs/EPHEMERAL_PRIMAL_SCAFFOLDING.md — ephemeral primal lifecycle
- wateringHole PRIMAL_SPRING_GARDEN_TAXONOMY.md — spring/garden/primal roles
