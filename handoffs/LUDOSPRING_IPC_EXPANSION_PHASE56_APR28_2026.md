# ludoSpring — IPC Expansion for esotericWebb (Phase 56)

**From**: primalSpring v0.9.23 Phase 56
**To**: ludoSpring team
**Date**: April 28, 2026
**Priority**: P0 — 6 missing IPC methods block esotericWebb desktop application
**Reference**: `primalSpring/specs/STORYTELLING_EVOLUTION.md`

---

## Summary

esotericWebb V7's `ludospring.rs` bridge calls 6 IPC methods that do not
exist in the current ludoSpring binary's handler dispatch. These methods
are the game-science-enriched narration pipeline that differentiates Webb
from a plain AI chatbot.

ludoSpring V53 has a pure composition model with 60Hz tick, BTSP enforcement,
and 817 tests. The IPC surface needs expansion — not replacement.

---

## Missing Methods

### 1. `game.narrate_action`

Compose flow state + DDA context into a narration prompt. This is the
game-science layer that enriches AI narration with mechanical awareness.

**Request:**
```json
{
  "method": "game.narrate_action",
  "params": {
    "action": "investigate_bookshelf",
    "actor": "player",
    "scene_id": "library_west_wing",
    "flow_state": {
      "engagement": 0.72,
      "challenge": 0.45,
      "pacing": "rising"
    },
    "dda_context": {
      "player_skill_estimate": 0.6,
      "recent_failures": 1,
      "session_duration_secs": 1800
    },
    "resolved_predicates": ["has_key_library", "spoke_to_librarian"],
    "dice_result": { "type": "d20", "roll": 14, "modifier": 3, "total": 17, "dc": 15, "success": true }
  }
}
```

**Response:**
```json
{
  "result": {
    "narration_prompt": {
      "tone": "discovery",
      "pacing_hint": "moderate_detail",
      "mechanical_summary": "Perception check succeeded (17 vs DC 15). Player is engaged (0.72) with rising pacing.",
      "suggested_detail_level": "medium",
      "dda_adjustment": "no_change"
    },
    "flow_score": 0.78
  }
}
```

**Delegation pattern**: ludoSpring composes the narration prompt from its
game science models (flow, DDA, engagement), then the caller (esotericWebb)
passes this prompt to Squirrel `ai.chat` for actual text generation.
ludoSpring does **not** call Squirrel directly.

---

### 2. `game.npc_dialogue`

Evaluate NPC state against the ruleset, return dialogue options with
flow scores.

**Request:**
```json
{
  "method": "game.npc_dialogue",
  "params": {
    "npc_id": "innkeeper_mira",
    "scene_id": "tavern_main",
    "player_stats": { "charisma": 14, "perception": 12, "lore": 8 },
    "relationship": { "trust": 0.4, "encounters": 3 },
    "available_options": [
      { "id": 1, "text": "Tell me about the mountains.", "skill_check": null },
      { "id": 2, "text": "I know what you're hiding.", "skill_check": { "stat": "charisma", "dc": 16 } },
      { "id": 3, "text": "[Leave]", "skill_check": null }
    ]
  }
}
```

**Response:**
```json
{
  "result": {
    "scored_options": [
      { "id": 1, "flow_score": 0.65, "engagement_impact": 0.1, "recommended": true },
      { "id": 2, "flow_score": 0.82, "engagement_impact": 0.3, "check_probability": 0.45, "recommended": false },
      { "id": 3, "flow_score": 0.2, "engagement_impact": -0.15, "recommended": false }
    ],
    "npc_mood": "guarded",
    "dda_hint": "player_struggling_slightly"
  }
}
```

---

### 3. `game.voice_check`

Fitts + engagement metrics for voice/ability interaction assessment.
Used by esotericWebb to validate that a player action is mechanically
sound before narrating it.

**Request:**
```json
{
  "method": "game.voice_check",
  "params": {
    "ability_id": "silver_tongue",
    "actor_stats": { "charisma": 14, "level": 5 },
    "target_dc": 18,
    "modifiers": ["+2 tavern_rapport", "-1 tired"],
    "context": {
      "fitts_distance": 0.3,
      "time_pressure": false,
      "previous_attempts": 0
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "success_probability": 0.35,
    "effective_modifier": 4,
    "fitts_cost": 0.12,
    "engagement_risk": "low",
    "recommendation": "allow",
    "cooldown_remaining": 0
  }
}
```

---

### 4. `game.push_scene`

Forward scene data to petalTongue via `visualization.render.scene`. This
is a convenience method — ludoSpring enriches the scene with game science
overlays (flow indicators, DDA state) before pushing to the display.

**Request:**
```json
{
  "method": "game.push_scene",
  "params": {
    "session_id": "ewebb-game-0",
    "scene": {
      "type": "dialogue",
      "background": "tavern_interior",
      "npc": { "id": "innkeeper_mira", "portrait": "mira_guarded.png", "mood": "guarded" },
      "options": [
        { "id": 1, "text": "Tell me about the mountains." },
        { "id": 2, "text": "I know what you're hiding.", "check": "CHA 16" }
      ],
      "narration": "The innkeeper eyes you warily from behind the bar..."
    },
    "overlays": {
      "flow_indicator": 0.78,
      "engagement_bar": true,
      "dda_state": "balanced"
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "rendered": true,
    "surface_id": "viz-ewebb-game-0"
  }
}
```

**Delegation**: ludoSpring calls petalTongue `visualization.render.scene`
via `capability.call` through biomeOS (or directly via `DISCOVERY_SOCKET`).

---

### 5. `game.begin_session`

Session lifecycle start. Creates a game session with optional provenance
DAG integration.

**Request:**
```json
{
  "method": "game.begin_session",
  "params": {
    "session_name": "disco_isles_run_3",
    "world": "disco_isles",
    "player_name": "Detective",
    "save_slot": 1,
    "tick_hz": 60,
    "provenance": true
  }
}
```

**Response:**
```json
{
  "result": {
    "session_id": "ls-session-abc123",
    "tick_budget_ms": 16.6,
    "dag_session_id": "rz-session-xyz789",
    "started_at": "2026-04-28T20:00:00Z"
  }
}
```

**Delegation**: If `provenance: true`, ludoSpring calls
`rhizocrypt.dag.session.create` via capability discovery to create the
DAG session. Returns the DAG session ID alongside the game session ID.

---

### 6. `game.complete_session`

Session lifecycle end. Flushes state, seals provenance.

**Request:**
```json
{
  "method": "game.complete_session",
  "params": {
    "session_id": "ls-session-abc123",
    "outcome": "save",
    "stats": {
      "duration_secs": 3600,
      "scenes_visited": 23,
      "choices_made": 47,
      "dice_rolls": 12,
      "ai_narrations": 31
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "completed": true,
    "provenance_sealed": true,
    "dag_merkle_root": "a1b2c3d4...",
    "ledger_entry_id": "ls-entry-456"
  }
}
```

**Delegation**: If provenance was enabled at session start, ludoSpring:
1. Appends a final `session_complete` event to rhizoCrypt DAG
2. Calls `loamspine.session.commit` to seal the ledger
3. Returns the merkle root and ledger entry ID

---

## Capability Registration

All 6 new methods should be added to ludoSpring's capability advertisement:

```json
{
  "capabilities": [
    "game.evaluate_flow", "game.fitts_cost", "game.engagement",
    "game.analyze_ui", "game.accessibility", "game.wfc_step",
    "game.difficulty_adjustment", "game.generate_noise",
    "game.narrate_action", "game.npc_dialogue", "game.voice_check",
    "game.push_scene", "game.begin_session", "game.complete_session"
  ]
}
```

Register with Songbird via `ipc.register` or `DISCOVERY_SOCKET` self-registration.

---

## Validation

primalSpring will validate these methods through:

- exp089 (`ludospring_expanded_ipc`): structural + live IPC validation
- exp088 (`storytelling_session_loop`): full loop with esotericWebb
- `desktop_nucleus.sh validate`: extended with ludoSpring checks

---

## Timeline Suggestion

| Priority | Method | Effort | Delegation |
|----------|--------|--------|------------|
| P0 | `game.begin_session` | Small | rhizoCrypt DAG optional |
| P0 | `game.complete_session` | Small | loamSpine + rhizoCrypt seal |
| P0 | `game.narrate_action` | Medium | Flow + DDA composition, no AI call |
| P0 | `game.npc_dialogue` | Medium | Scoring engine, no external calls |
| P1 | `game.voice_check` | Small | Fitts + engagement math |
| P1 | `game.push_scene` | Small | Delegation to petalTongue via capability.call |
