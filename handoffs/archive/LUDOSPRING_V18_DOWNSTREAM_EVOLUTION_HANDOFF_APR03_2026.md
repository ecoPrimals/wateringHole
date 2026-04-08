<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation and creative text in this file: CC-BY-SA-4.0
-->

# ludoSpring V18 — Downstream Garden Evolution Tasks

**Date:** April 3, 2026
**From:** ludoSpring (game science spring)
**To:** esotericWebb team
**Status:** Active
**License:** AGPL-3.0-or-later

---

## Context

ludoSpring V18 provides 9 proto deploy graph sketches, a primal leverage map,
and a composition recipe for esotericWebb to absorb. This handoff documents
what Webb needs to evolve to take advantage of that work, plus Webb-owned gaps
that ludoSpring's composition testing surfaced.

---

## Proto Sketch Absorption (P1)

ludoSpring `graphs/sketches/` contains 7 deploy + 2 validation graph sketches.
See `LUDOSPRING_V18_WEBB_PROTO_GRAPHS_HANDOFF_APR03_2026.md` for full details.

**Recommended absorption order** (each builds on the previous):

| Order | Sketch | Unlocks | Depends on |
|-------|--------|---------|------------|
| 1 | Sovereign Save | Replace JSON saves with signed DAG | GAP-019 (crypto bridge) |
| 2 | Attributed Narration | AI DM with ORC attribution | Squirrel available |
| 3 | Science Overlay | Live flow/DDA dashboard | petalTongue available |
| 4 | Session-as-Primal | Ephemeral primal sessions | biomeOS lifecycle.register |
| 5 | Creative Studio | Content pack authoring | nestGate + loamSpine |
| 6 | Sovereign Render | GPU pipeline | toadStool maturity |
| 7 | Multiplayer | Multi-gate sessions | Songbird mesh stability |

**Absorption process:**
1. Copy sketch to Webb `graphs/`
2. Adapt capabilities to PrimalBridge method inventory
3. Set `required` flags based on degradation preferences
4. Validate graph parses correctly
5. Graduate by removing PROTO SKETCH header

---

## Webb-Owned Evolution Tasks

### GAP-019: Wire BearDog crypto into PrimalBridge (P1)

**Blocks:** Sovereign save absorption (sketch 1)
**Evidence:** BearDog V4 has real cryptography (Ed25519, SHA-256, post-quantum).
Webb's PrimalBridge has no crypto domain methods.
**Task:** Add `crypto.sign`, `crypto.verify`, `crypto.hash` bridge delegations.
Feed signed vertex hashes into provenance trio for sovereign saves.

### GAP-008: Content pack format (P1)

**Blocks:** Creative studio absorption (sketch 5)
**Evidence:** Solo author and team profiles need distributable content. Currently
loose YAML directories with no packaging.
**Task:** Define content pack format (zip/tar with manifest, version, author
attribution, optional BearDog signature). Implement `esotericwebb validate --pack`.

### GAP-009: RulesetCert YAML loading (P1)

**Blocks:** Creative studio absorption (sketch 5)
**Evidence:** `CONTENT_AUTHORING_SPEC` defines a `rulesets/` directory but
content loader does not parse or validate against any schema.
**Task:** Load rulesets/ YAML, validate against schema. When game-science primal
emerges (GAP-021), wire `science.ruleset_validate` for composition-time
confirmation.

### GAP-007: Offline voice preview (P2)

**Evidence:** Creators need to preview which internal voices fire during scene
transitions while authoring. Currently requires running AI primal.
**Task:** Offline voice simulation: given VoiceId triggers in `narrative.yaml`
and NPC certs, show which voices would fire and with what priority, using
placeholder text reflecting personality parameters.

---

## What ludoSpring Provides (No Runtime Dependency)

Webb V6 correctly decomposed the ludoSpring dependency. These are what
ludoSpring offers as enrichment, not requirements:

| ludoSpring capability | Webb V6 local fallback | When ludoSpring enriches |
|----------------------|----------------------|------------------------|
| `game.evaluate_flow` | Local `science/flow` | Advanced multi-metric evaluation |
| `game.engagement` | Local `science/engagement` | Cross-session trend analysis |
| `game.difficulty_adjustment` | Local `science/dda` | History-aware difficulty curves |
| `game.fitts_cost` | Not local | UI reachability analysis |
| `game.wfc_step` | Not local | Procedural level generation |
| `game.generate_noise` | Not local | Terrain and item placement |
| `game.analyze_ui` | Not local | Tufte data-ink ratio analysis |
| `game.accessibility` | Not local | WCAG-informed accessibility scoring |

The bottom 5 have no local Webb fallback — they require ludoSpring (or a
future game-science primal per GAP-021) to be available in the composition.

---

## Cross-References

- `ludoSpring/graphs/sketches/README.md` — sketch taxonomy and absorption guide
- `ludoSpring/specs/PRIMAL_LEVERAGE_MAP.md` — primal-to-game-science mapping
- `ludoSpring/specs/ECOSYSTEM_EVOLUTION_MAP.md` — full gap analysis
- `LUDOSPRING_V18_WEBB_PROTO_GRAPHS_HANDOFF_APR03_2026.md` — proto sketch details
- `gardens/esotericWebb/EVOLUTION_GAPS.md` — Webb gap registry
- `gardens/esotericWebb/specs/VISION_AND_EVOLUTION.md` — evolution vectors
