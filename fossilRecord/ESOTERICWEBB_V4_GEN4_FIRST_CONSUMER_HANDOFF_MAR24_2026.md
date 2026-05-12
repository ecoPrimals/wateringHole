<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# HANDOFF: Esoteric Webb V4 — First gen4 Consumer, Live Primal Composition

- **Date**: 2026-03-24
- **Source**: esotericWebb V4 (sporeGarden / ecoPrimals / ecoSprings)
- **Audience**: All primal teams, all spring teams, ecosystem coordination
- **Type**: Evolution feedback + absorption opportunities

---

## What Happened

Esoteric Webb is the first gen4 entity in the ecoPrimals ecosystem. It is a
CRPG substrate that composes deployed primals into a playable game system via
JSON-RPC IPC. It does not import any spring or primal Rust crates — all
coordination happens at runtime over TCP/UDS.

As of V4, Webb has a fully wired composition pipeline where every player
action flows through: AI narration → NPC dialogue → flow evaluation →
scene push → provenance lifecycle. All primal domains degrade gracefully
when the corresponding primal is unavailable.

### By the numbers

| Metric | Value |
|--------|-------|
| Tests | 166 |
| Rust files | 32 (~8.5k LOC) |
| Bridge methods | 23 |
| Primal domains consumed | 8 |
| Experiments | 5 |
| Quality gates | 5/5 (fmt, clippy, test, doc, deny) |
| Unsafe code | `#![forbid(unsafe_code)]` |
| C dependencies | Zero |

---

## Primal Capabilities Consumed (Live Wired)

| Domain | Primal | Methods | Wired in act() |
|--------|--------|---------|-----------------|
| game | ludoSpring | `game.evaluate_flow`, `game.npc_dialogue`, `game.narrate_action`, `game.voice_check`, `game.push_scene`, `game.begin_session`, `game.complete_session` | Yes |
| ai | Squirrel | `ai.chat`, `ai.summarize` | Yes |
| visualization | petalTongue | `visualization.render.scene`, `interaction.poll` | Yes |
| dag | rhizoCrypt | `dag.session.create`, `dag.event.append`, `dag.session.complete`, `dag.frontier.get`, `dag.merkle.root`, `dag.query.vertices` | Yes |
| lineage | loamSpine | `certificate.mint` | Bridge ready |
| compute | toadStool | `compute.dispatch.submit` | Bridge ready |
| storage | nestGate | `storage.store`, `storage.retrieve` | Bridge ready |
| provenance | sweetGrass | `attribution.record` | Bridge ready |

---

## Evolution Feedback for Primal Teams

### For rhizoCrypt (DAG)

Webb exercises the full session lifecycle: `dag.session.create` on game start,
`dag.event.append` per player action (each action = vertex with parent hash
linking), `dag.session.complete` when an ending is reached. The game's
cyclic navigation graph (rooms can be revisited) projects onto an acyclic
temporal trace — this is a natural fit for DAG semantics.

**What we need next**: `dag.slice.checkout` for save/load (restore a DAG
frontier as a game save), `dag.event.append_batch` for importing Webb's
local ProvenanceClient vertex log, and confirmed response format for
`dag.query.vertices` (we parse `vertices` array from result).

### For loamSpine (Lineage)

Webb models NPC personality certs as loamSpine certificates — each NPC has
knowledge bounds, trust gates, lies with detection DCs, and voice constraints.
`certificate.mint` is wired but needs the cert schema to support:
- Scoped knowledge fields (what the NPC knows vs. what it will share)
- Trust thresholds (minimum trust to unlock dialogue branches)
- Lie constraints (detection DC, lie probability, max lie chains)

**What we need next**: `certificate.query` for retrieving active certs,
`certificate.revoke` for revoking trust (NPC betrayal), and a schema
extension for personality constraint fields.

### For sweetGrass (Attribution)

Every playthrough is a potential Novel Ferment Transcript. Webb tracks three
attribution sources: authored content (YAML scenes, NPC definitions), AI
narration (Squirrel-generated text per action), and player choices (the
traversal itself). These map to sweetGrass's Creator → Implementation →
Extension chain.

**What we need next**: `attribution.record` to accept structured source
metadata (author, ai_model, player_session), `attribution.query` for
displaying credits, `braid.create` for linking multi-session derivation
chains.

### For Squirrel (AI)

Webb uses Squirrel for two purposes: narration (enriching mechanical outcome
text with literary prose) and NPC dialogue (personality-constrained
conversation). The tiered approach is: ludoSpring's `game.narrate_action`
first (which delegates to Squirrel with game-science context), then direct
`ai.chat` as fallback.

**What we need next**: Hard constraint enforcement on NPC personality certs
(not just system prompt guidance — mechanical enforcement of knowledge bounds
and trust gates). See GAP-003 in Webb's EVOLUTION_GAPS.md.

### For petalTongue (Visualization)

Webb pushes scene state to petalTongue after every action via
`visualization.render.scene`. The payload includes room description, NPC
list, available choices, active conditions, and voice interjections.

**What we need next**: Dialogue tree scene type support (interactive dialogue
UI with choices, voice notes, and skill check displays). See GAP-002 in
Webb's EVOLUTION_GAPS.md.

### For toadStool (Compute)

`compute.dispatch.submit` is bridge-ready but not yet actively used in the
game loop. Future use: GPU-accelerated Perlin noise for procedural
environment generation, batched NPC personality evaluation.

### For ludoSpring (Game Science)

Webb consumes 7 `game.*` methods from ludoSpring. The flow evaluation
(`game.evaluate_flow`) is the most critical — it drives the DDA system
by measuring player engagement per-action. `game.npc_dialogue` delegates
to Squirrel with game-science enrichment (personality cert context, trust
state, active conditions).

**Pattern absorbed from ludoSpring V30**: Handler split into submodules,
MCP JSON Schema, Python tolerance mirror, session decomposition, dual-format
capability discovery.

---

## Evolution Feedback for Spring Teams

### Patterns Webb Discovered (Absorb Freely)

1. **Bridge preservation across IPC restarts**: When an IPC `session.start`
   reinitializes state, the PrimalBridge must survive. `take_bridge()` +
   `with_bridge()` pattern keeps connections alive.

2. **Tiered narration with graceful degradation**: Game science primal →
   direct AI fallback → mechanical text. Three tiers, each cheaper, each
   still functional.

3. **PrimalEnrichment as composition result**: Instead of returning raw
   primal responses, wrap all composition results in a typed struct that
   carries `Option<T>` for each primal contribution. Consumers never need
   to know which primals were available.

4. **Deploy graph topological ordering**: Kahn's algorithm on TOML deploy
   graphs, wave-based spawning, TCP readiness polling. Works for any primal
   composition, not just game engines.

5. **Experiment honest-skip policy**: `check_skip("reason")` when a primal
   is unavailable, never `check_bool("...", true)`. Skips are informational,
   not failures.

### What Springs Can Absorb from Webb

- **ludoSpring**: Webb's `GameDirector` pattern (predicate-guarded outcomes,
  effect application, turn-based state mutation) is a complete implementation
  of RPGPT session evaluation. Consider absorbing as a reference adapter.
- **primalSpring**: Webb's `PrimalLauncher` with deploy graph ordering is
  a consumer-side implementation of primalSpring's deploy graph model.
  Consider absorbing the consumer perspective into deploy graph docs.
- **All springs**: Webb's experiment framework (`check_bool`/`check_skip`/
  `section`/`finish_with_code`) is a minimal, tested validation harness.

---

## Ecosystem Positioning

```
syntheticChemistry/     — Springs (science validation)
ecoPrimals/             — Primals (sovereign infrastructure)
sporeGarden/            — Products (creative surface)
       ↑
  esotericWebb lives here
```

Webb is the first project where the primals are infrastructure, not the
subject. This is the gen3→gen4 boundary. The primals disappear into the
product. A player sees a game, not a DAG engine, not a lineage tracker,
not a GPU compute pipeline.

---

## Open Gaps (Active)

| Gap | Primal | Severity | Status |
|-----|--------|----------|--------|
| GAP-002 | petalTongue (dialogue tree scene) | medium | open |
| GAP-003 | Squirrel (NPC constraint enforcement) | medium | open |
| GAP-006 | Songbird (capability-filtered discovery) | medium | open |
| GAP-007 | Self + Squirrel (voice preview offline) | medium | open |
| GAP-008 | Self (content pack format) | low | open |
| GAP-009 | Self + ludoSpring (RulesetCert YAML) | medium | open |
| GAP-010 | Ecosystem (plasmidBin automation) | medium | open |

---

## Files Modified in V4

- `webb/src/session.rs` — game loop composition pipeline
- `webb/src/ipc/bridge.rs` — 23 bridge methods
- `webb/src/ipc/ludospring.rs` — typed game science client
- `webb/src/ipc/mod.rs` — method constants
- `webb/src/ipc/handlers/session.rs` — bridge preservation
- `webb/src/ipc/handlers/mcp.rs` — test lint fix

Full changelog in `CHANGELOG.md`.
