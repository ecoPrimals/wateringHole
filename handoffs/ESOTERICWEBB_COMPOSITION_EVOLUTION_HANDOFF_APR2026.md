# esotericWebb Composition Evolution Handoff
## From: primalSpring v0.9.17 (Phase 45) + ludoSpring (V46)
## For: esotericWebb garden team
## Date: April 20, 2026

## What Happened

primalSpring certified the NUCLEUS base composition (**86/86 guidestone checks**,
15/18 exp094 parity, 12/12 primals deployed). ludoSpring validated game science
math against the live NUCLEUS (152/152 local, 30/31 composed, 11/11 pipeline).
The gaming niche composition (Tower + ludoSpring + petalTongue + toadStool) was
deployed and all IPC flows were proven. Local gaps were refined and solved:
barraCuda tensor parity, BearDog ed25519 encoding, capability symlink automation,
and three new Webb-required game methods wired. The composition is ready for Webb
to absorb.

## Architecture: Primals Provide, Springs Validate, Gardens Compose

```
Primals     Springs           Gardens
(building   (science          (usable products —
 blocks)     validation)       composition graphs)
   │            │                    │
   │  ┌─────── primalSpring ────┐   │
   │  │  certifies NUCLEUS      │   │
   │  │  84/86 guidestone       │   │
   │  └────────────────────────┘   │
   │                                │
   │  ┌─────── ludoSpring ──────┐  │
   │  │  validates game math    │   │
   │  │  152/152 + 30/31        │   │
   │  └────────────────────────┘   │
   │                                │
   └────────────────────────────────┘
                                    │
                              esotericWebb
                              (composes primals
                               into CRPG via
                               biomeOS graph)
```

Springs are NOT binaries — they are validation environments whose guidestones
prove science math against a live NUCLEUS. Gardens are NOT binaries — they are
composition graphs that biomeOS deploys, composing primals into products.

## Proven IPC Flows

### Game Science (ludoSpring primal)

| Method | Params | Response |
|--------|--------|----------|
| game.evaluate_flow | {challenge, skill} | {state: "flow"/"boredom"/"anxiety"} |
| game.fitts_cost | {distance, target_width} | {index_of_difficulty, movement_time_ms} |
| game.engagement | {session_duration_s, action_count, exploration_breadth, challenge_seeking, retry_count, deliberate_pauses} | {composite, actions_per_minute, exploration_rate, persistence, challenge_appetite, deliberation} |
| game.generate_noise | {x, y, z?, octaves?, lacunarity?, persistence?} | {value: f64} |
| game.wfc_step | {width, height, n_tiles, collapse?} | grid state |
| game.accessibility | {audio_cues, descriptions, braille, haptic, color_independent, scalable_text} | score |
| game.difficulty_adjustment | {outcomes, target_success_rate?} | adjustment |
| game.begin_session | {session_id?} | {session_id} |
| game.complete_session | {session_id} | summary |
| game.session_state | {session_id} | state |
| game.record_action | {session_id, challenge, skill, outcome?, label?} | {vertex_index, tick_count, flow_state} |
| game.push_scene | {session_id, title, data, target?} | {accepted, routed_to} |
| game.query_vertices | {session_id, limit?} | {total_vertices, vertices: [{index, label, challenge, skill, outcome, parent}]} |

### Visualization (petalTongue primal)

| Method | Notes |
|--------|-------|
| visualization.render | Spring data format — needs session_id + binding |
| visualization.render.stream | Streaming updates |
| visualization.render.grammar | Grammar of Graphics spec |
| visualization.render.dashboard | Panel-based dashboard |
| visualization.render.scene | Scene graph rendering |
| visualization.capabilities | Returns data_binding_variants + grammar_geometry_types |

petalTongue has a `SpringDataAdapter` that recognizes ludoSpring `GameScene`
and `GameChannel` payloads. The exact parameter format for `visualization.render`
with spring-specific data needs alignment between ludoSpring's push client
format and petalTongue's adapter expectations.

### Compute (toadStool primal — optional)

| Method | Notes |
|--------|-------|
| compute.health | {healthy, status, active_workloads, uptime_secs} |
| compute.dispatch | Submit compute workloads |
| display.* | DRM/KMS window management (when display backend active) |

## Socket Discovery

All primals use `$XDG_RUNTIME_DIR/biomeos/` with family-qualified names:

```
beardog-{FAMILY_ID}.sock       → security, crypto, btsp
songbird-{FAMILY_ID}.sock      → discovery, network
ludospring-{FAMILY_ID}.sock    → game.*
petaltongue-{FAMILY_ID}.sock   → visualization.*
toadstool → compute-{FAMILY_ID}.sock + compute-{FAMILY_ID}-tarpc.sock
```

Capability symlinks are now **automatically created** by `start_primal.sh` after
each primal launches (e.g., `security.sock → beardog-*.sock`, `tensor.sock →
math-*.sock`). No manual `ln -sf` required. Webb should use capability-based
discovery (probe `.sock` files with `health.check` or `lifecycle.status`), not
hardcoded socket names.

## BTSP (BirdSong Trust and Security Protocol)

- Export `BEARDOG_FAMILY_SEED` before launching BearDog
- rhizoCrypt and sweetGrass enforce BTSP on UDS — plain JSON-RPC probes are rejected
- biomeOS speaks HTTP on UDS — classify as reachable-but-incompatible (SKIP, not FAIL)
- Use `is_protocol_error()` / `is_transport_mismatch()` for protocol tolerance

## Capability Gaps: Webb Wants vs. ludoSpring Has

Webb's `esotericwebb_full.toml` lists capabilities ludoSpring doesn't implement yet:

| Webb Wants | Status | Notes |
|------------|--------|-------|
| game.npc_dialogue | NOT YET | Narrative extension — needs AI (Squirrel) integration |
| game.narrate_action | NOT YET | Narrative description of game actions |
| game.voice_check | NOT YET | Voice-based interaction validation |
| game.push_scene | **WIRED** | Queues scene payload to viz layer, routes to petalTongue |
| game.record_action | **WIRED** | Records action tick into session DAG with flow/DDA update |
| game.query_vertices | **WIRED** | Returns session action DAG vertices with parent links |
| game.mint_certificate | NOT YET | Provenance certificate creation (sweetgrass integration) |

ludoSpring HAS these that Webb doesn't reference yet:

| ludoSpring Has | Notes |
|----------------|-------|
| game.fitts_cost | Fitts' law movement time calculation |
| game.generate_noise | Perlin/fBm noise generation |
| game.wfc_step | Wave Function Collapse step |
| game.accessibility | IGDA/XAG accessibility scoring |
| game.analyze_ui | Tufte data-ink ratio analysis |

These are evolution targets. ludoSpring's existing capabilities provide the
validated math foundation; the missing methods are product-specific extensions
that can be added as ludoSpring evolves toward Webb's needs.

## What Gardens Own vs. What Springs Own

### Gardens own:
- UX and product experience
- PrimalBridge (capability routing for their specific composition)
- Graceful degradation (fall back when primals are absent)
- Product deploy graphs (consumed by biomeOS)
- Niche YAML (BYOB configuration)

### Springs own:
- Science validation (guidestone math)
- Correctness baselines (peer-reviewed reference values)
- Evolution experiments (exp001–exp077+)
- Primal gap documentation

### Primals own:
- Their capability surface (JSON-RPC methods)
- Socket creation and capability advertisement
- BTSP security enforcement

## Standalone Degradation

Webb MUST work without ludoSpring (per GAP-016). When ludoSpring is absent:
- Webb owns flow/engagement/DDA locally
- ludoSpring is `required = false` in proto sketches
- Discovery gracefully skips unavailable primals

## aarch64 (Pixel) Deployment

- All 13 primal binaries available for `aarch64-unknown-linux-musl`
- Deploy in headless/server mode (petalTongue `server`, no display)
- Same socket conventions as x86_64
- Validated: composition patterns are architecture-independent

## Validation Results Summary

| Component | Result |
|-----------|--------|
| primalSpring guidestone | **86/86 PASS** (6 expected SKIP — BTSP/loamspine) |
| primalSpring exp094 parity | 15/18 (Songbird name-resolution gaps) |
| ludoSpring lib tests | 152/152 |
| ludoSpring exp067 tower composition | **18/19** (1 expected SKIP — game primal not deployed) |
| ludoSpring exp068 barracuda parity | **6/6 PASS** (was 3/6) |
| ludoSpring exp072 composition | 24/31 (biomeOS HTTP + ludoSpring not deployed as primal) |
| ludoSpring exp033 pipeline | 11/11 |
| ludoSpring IPC methods | **15 methods** (was 12 — +record_action, push_scene, query_vertices) |
| ludoSpring deploy graphs | 14/14 structural |
| Gaming niche IPC flows | All game.* methods verified |
| Webb product graphs | 8/8 valid TOML |
| ludoSpring proto sketches | 7/7 valid, 6-8 nodes each |

## Next Steps for Webb

1. Pull latest `plasmidBin` — all 13 primals for x86_64 and aarch64
2. Deploy gaming niche: `biomeOS gaming_niche_deploy.toml` or Webb's own `esotericwebb_full.toml`
3. Validate game.* IPC flows against live ludoSpring
4. Align `visualization.render` params with petalTongue's `SpringDataAdapter` format
5. Implement missing capabilities or add graceful degradation per GAP-016
6. Test standalone mode (no ludoSpring) — flow/engagement/DDA should work locally
