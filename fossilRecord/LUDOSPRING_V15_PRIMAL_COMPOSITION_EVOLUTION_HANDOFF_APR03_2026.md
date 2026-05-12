# ludoSpring V15 — Primal Composition Evolution Handoff

**Date:** April 3, 2026
**From:** ludoSpring V15
**To:** primalSpring, esotericWebb, barraCuda, ecosystem
**License:** AGPL-3.0-or-later

---

## Summary

ludoSpring transitions from science validation (Python → Rust parity) to
**primal composition** — consuming deployed primals via IPC, validating that
their composition solves game science problems, and surfacing gaps back to
the ecosystem through wateringHole handoffs.

This handoff documents the changes, new capabilities, and upstream requests.

---

## What Changed

### Audit Debt Cleanup (Phase 0)

- Fixed `AGPL-3.0-only` → `AGPL-3.0-or-later` in `barracuda/src/bin/ludospring.rs`
- Added `lifecycle.status` to IPC dispatch (discovery clients send this)
- Added `health.liveness` and `health.readiness` dispatch aliases per IPC compliance matrix
- Replaced bare `.unwrap()` in `wfc.rs` test with `.expect()` with rationale

### NUCLEUS Deploy Graphs (Phase 1)

Created `ludoSpring/graphs/` with four deploy graphs, graduating from
primalSpring's PROTO SKETCH status:

| Graph | Purpose | Coordination |
|-------|---------|-------------|
| `ludospring_tower_deploy.toml` | Minimum viable: biomeOS + Tower + ludospring | sequential |
| `ludospring_nucleated_deploy.toml` | Full niche: Tower + barraCuda + toadStool + provenance trio + ludospring | sequential |
| `ludospring_validate.toml` | Composition validation: substrate, Tower, 8 capabilities, round-trip | sequential |
| `ludospring_continuous_session.toml` | 60Hz tick budget under composition | continuous |

**Action for primalSpring:** The PROTO SKETCHes in `graphs/sketches/` can be
archived to fossilRecord — ludoSpring now owns its graphs locally.

### IPC Surface Expansion (Phase 2)

Four new JSON-RPC methods for session lifecycle composition:

| Method | Purpose |
|--------|---------|
| `game.begin_session` | Initialize a game science session with flow/DDA/engagement state |
| `game.complete_session` | Finalize session, return aggregate metrics |
| `game.session_state` | Query current session state snapshot |
| `game.tick_health` | Report tick budget health for continuous graphs |

The `lifecycle.status` dispatch was also fixed (Phase 0) to respond to
discovery probes.

**Total IPC surface:** 12 methods (8 existing + 4 new).

**Action for esotericWebb:** `game.begin_session` / `game.complete_session`
provides the session lifecycle that GAP-021 requested. Webb can consume
these when ready.

### ValidationResult Evolution (Phase 4)

Upgraded `barracuda/src/validation/mod.rs` to the full hotSpring contract:

- `ValidationHarness` struct with experiment-level lifecycle
- `check_bool(id, condition, description)` — boolean pass/fail
- `check_skip(id, reason)` — explicit skip (exit 2)
- `exit()` — consolidated exit with summary output (0/1/2)
- Pass/fail/skip counters
- Backward compatible with existing `ValidationResult::check()` API

### Composition Experiments (Phase 3)

Five new experiments validating primal composition:

| Experiment | What it validates |
|------------|-------------------|
| exp067 — Tower Composition | Graph structure + live Tower probe + capability routing |
| exp068 — barraCuda Parity | Local math vs primal math over IPC (dot, mean, l2_norm) |
| exp069 — Session Lifecycle | begin/complete session round-trip, local + IPC |
| exp070 — Continuous Tick | 100-tick budget at 60Hz, local + IPC latency |
| exp071 — Cross-Spring Smoke | Discover all running primals, probe health, readiness report |

All experiments use `ValidationHarness` with skip semantics: they pass
structurally even when primals are not running, and validate live
composition when primals are available.

### wateringHole Taxonomy Refinement (Phase 5)

- Created `PRIMAL_SPRING_GARDEN_TAXONOMY.md` — the authoritative reference
  for the three-layer model (primals/springs/gardens) and co-evolution loop
- Fixed GLOSSARY.md: Spring definition corrected from "science primal" to
  "validation and evolution environment"; added Garden as first-class term
- Fixed SPRING_INTEROP_LESSONS.md: esotericWebb corrected from "consumer
  spring" to "first garden"
- Updated wateringHole README.md: added "Three Layers" section and taxonomy
  document to Master Index

---

## Gaps Surfaced

### For primalSpring

1. **PROTO SKETCH graduation:** ludoSpring now owns its deploy graphs. The
   sketches at `graphs/sketches/ludospring_game_deploy.toml` and
   `graphs/sketches/validation/ludospring_game_validate.toml` can be
   archived to fossilRecord.
2. **`nucleus_game_session.toml`** in `graphs/science/` references
   `ludospring_primal` as the binary name — the actual binary is
   `ludospring`. Graph should be updated or archived.

### For esotericWebb

1. **GAP-021 resolution path:** `game.begin_session` / `game.complete_session`
   / `game.session_state` provide the session lifecycle Webb requested.
   When Webb is ready to re-wire from local science to IPC, these methods
   are available.

### For barraCuda

1. **IPC math parity:** exp068 validates `dot`, `mean`, `l2_norm` locally.
   When barraCuda exposes `math.dot`, `math.mean`, `math.l2_norm` over IPC,
   exp068 will validate parity between local and primal math.

---

## Stats

- **71 experiments** (was 66)
- **12 IPC methods** (was 8)
- **4 deploy graphs** (was 0, promoted from primalSpring sketches)
- **`ValidationHarness`** with full hotSpring contract
- **0 unsafe**, **0 `#[allow()]`**, **AGPL-3.0-or-later** throughout
