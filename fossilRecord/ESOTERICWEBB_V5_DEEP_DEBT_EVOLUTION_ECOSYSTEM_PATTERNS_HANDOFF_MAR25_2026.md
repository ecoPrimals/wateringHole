<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# HANDOFF: Esoteric Webb V5 — Deep Debt Resolution, Ecosystem Pattern Absorption

- **Date**: 2026-03-25
- **Source**: esotericWebb V5 (sporeGarden / ecoPrimals / ecoSprings)
- **Audience**: All primal teams, all spring teams, ecosystem coordination
- **Type**: Evolution feedback + pattern standardization + absorption opportunities
- **Predecessor**: ESOTERICWEBB_V4_GEN4_FIRST_CONSUMER_HANDOFF_MAR24_2026.md

---

## What Happened

Esoteric Webb V5 completed a comprehensive debt resolution sprint, absorbing
ecosystem patterns from primalSpring and wateringHole standards into the first
gen4 consumer. The codebase evolved from V4's 166 tests / ~8.5k LOC to V5's
329 tests / ~12.5k LOC with 90.84% line coverage, while every quality gate
remains clean (fmt, clippy pedantic+nursery, test, doc, deny).

### By the numbers

| Metric | V4 | V5 | Delta |
|--------|----|----|-------|
| Tests | 166 | 329 | +163 |
| Coverage | ~78% | 90.84% | +13pp |
| Rust files | 32 | 35 | +3 |
| LOC | ~8.5k | ~12.5k | +4k |
| Bridge methods | 23 | 23 | — |
| Unsafe code | `forbid` | `forbid` | — |
| C dependencies | 0 | 0 | — |
| Quality gates | 5/5 | 6/6 (+coverage) | +1 |

---

## Patterns Absorbed from Ecosystem

### 1. Semantic IpcError Classification (from primalSpring)

Webb's `IpcError` now mirrors primalSpring's semantic classification:
`ConnectionRefused`, `Timeout`, `MethodNotFound`, `ProtocolError`,
`ApplicationError`, `PrimalNotFound`, `Serialization`. Helper methods
`is_retriable()`, `is_recoverable()`, `is_connection_error()`,
`is_method_not_found()` enable consistent circuit breaker and retry logic.

`classify_io_error()` normalizes OS-level errors to semantic types before
propagation. All resilience consumers (bridge, retry policy, circuit breaker)
now operate on semantic meaning rather than string matching.

**Recommendation for all primals:** Adopt semantic error classification with
`is_retriable()` / `is_recoverable()` helper methods. Flat error enums lose
operational meaning at IPC boundaries.

### 2. Transport Negotiation (from primalSpring)

`PrimalClient::connect_transport()` now parses `unix:`, `tcp:`, implicit
path, and implicit address formats. TCP is the default for platform
portability; UDS is the performance path for biomeOS-native deployments.

**Recommendation for all primals:** Support `connect_transport(address)` with
protocol prefix parsing. This enables deployment flexibility without
recompilation.

### 3. Canonical Primal Names Module (from wateringHole standards)

Created `ipc/primal_names.rs` as single source of truth for all primal slugs,
domains, and mappings. Eliminates scattered constant duplication.

**Recommendation for Songbird and biomeOS:** Consider establishing an
ecosystem-wide `primal_registry` crate or standard TOML that all consumers
can reference, rather than each consumer maintaining its own list.

### 4. UniBin v1.2 TCP Listener

Webb's `serve` command now supports `--listen addr:port` and `--port N` for
TCP IPC alongside existing UDS, per UniBin v1.2 specification.

---

## Evolution Feedback for Primal Teams

### For petalTongue (visualization)

GAP-002 remains open: Webb defines `DialogueTreeScene` payloads but the
visualization primal has not confirmed support for dialogue tree rendering
with choice highlighting, voice interjection panels, or skill check display.

**Absorption opportunity:** Webb's `push_scene_to_ui()` sends structured
scene JSON with `node`, `description`, `npcs`, `turn`, `is_ending` fields.
petalTongue could add a `dialogue_tree` scene type that renders choices,
voice notes, and skill outcomes.

### For Squirrel (AI)

GAP-003 remains open: NPC personality certs define knowledge bounds, trust
gates, lies with detection DCs, and voice constraints. The AI primal needs
to enforce these as hard constraints, not soft prompt suggestions.

GAP-007: Voice interjection preview needs offline simulation capability.
Webb could generate placeholder voice text from personality parameters if
Squirrel provided a lightweight "dry run" mode.

### For rhizoCrypt / loamSpine / sweetGrass (provenance trio)

GAP-004 has progressed: Full provenance lifecycle is wired into GameSession.
`dag.session.create` on start, `dag.event.append` per action,
`dag.session.complete` on ending. V5 added comprehensive provenance vertex
tests with session history tracking.

**Next step:** Live end-to-end validation against rhizoCrypt binary from
plasmidBin. Webb is ready — the structural vocabulary (BFS depth layers,
edge classification, DagOverlay) maps directly to rhizoCrypt operations.

### For Songbird (discovery)

GAP-006 remains open: Webb probes filesystem socket directories (tiers 1-4)
but does not call `discovery.query` for tier-5 lookup. When Songbird confirms
response format for capability-filtered queries, Webb will integrate tier-5.

### For ludoSpring (game science)

GAP-009: RulesetCert YAML is loaded as opaque YAML. When ludoSpring
provides a `game.ruleset_validate` endpoint with expected schema, Webb
will add structural validation.

### For biomeOS / primalSpring (deployment)

GAP-010: plasmidBin population and deployment automation remains the key
blocker for moving from "local preview" to "composed niche" mode.

---

## Patterns Available for Ecosystem Adoption

These patterns emerged from Webb's V5 evolution and are available for any
primal or spring team to adopt:

1. **Smart module refactoring** — decompose by semantic boundary (types,
   pipeline, core logic) with `pub(crate)` field access, preserving public
   API. Session refactoring reduced 1192 → 3 files under 1000 lines each.

2. **Graceful degradation as architecture** — every primal interaction
   wrapped in domain-check + attempt + degrade pipeline. 6-phase enrichment
   pipeline demonstrates the pattern at scale.

3. **Coverage as quality gate** — `--fail-under-lines 90` in cargo config.
   Target specific uncovered *behavior paths*, not test count. Achieved
   90.84% by adding 149 targeted tests.

4. **`unsafe_code = "forbid"` in Rust 2024** — `std::env::set_var()` is
   unsafe in edition 2024. Design env-var-dependent code with pure-function
   alternatives for testability. Webb encountered this constraint and adapted
   by testing observable behavior rather than env var mutation.

5. **Structured logging migration** — replace `println!`/`eprintln!` with
   `tracing` crate calls. One-time migration, permanent observability gain.

---

## File Manifest (V5 changes)

| File | Change |
|------|--------|
| `webb/src/ipc/primal_names.rs` | NEW — canonical primal names module |
| `webb/src/ipc/envelope.rs` | Semantic IpcError classification |
| `webb/src/ipc/client.rs` | connect_transport(), 7 new tests |
| `webb/src/ipc/bridge.rs` | primal_names adoption, semantic errors |
| `webb/src/ipc/discovery.rs` | primal_names adoption, 8 new tests |
| `webb/src/ipc/resilience.rs` | Delegate to IpcError::is_recoverable() |
| `webb/src/ipc/launcher.rs` | tracing migration, 15 new tests |
| `webb/src/ipc/listener.rs` | serve_tcp, handle_tcp_connection, 4 new tests |
| `webb/src/ipc/provenance.rs` | Updated Serialization variant |
| `webb/src/ipc/handlers/mod.rs` | ERROR_METHOD_NOT_FOUND constant |
| `webb/src/ipc/handlers/narrative.rs` | Active session tests |
| `webb/src/ipc/handlers/session.rs` | Extensive active session tests |
| `webb/src/session/mod.rs` | Refactored from session.rs, pub(crate) fields |
| `webb/src/session/types.rs` | NEW — extracted data structures |
| `webb/src/session/enrichment.rs` | NEW — 6-phase pipeline, 9 new tests |
| `webb/src/content/mod.rs` | 14 new validation edge-case tests |
| `webb/src/bin/esotericwebb.rs` | --listen/--port CLI args |
| `webb/src/bin/commands/mod.rs` | cmd_replay evolution, tracing |
| `.cargo/config.toml` | --fail-under-lines 90 |
