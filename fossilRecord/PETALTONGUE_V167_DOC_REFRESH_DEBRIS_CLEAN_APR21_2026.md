# petalTongue v1.6.7 — Doc Refresh + Debris Cleanup

**Date**: April 21, 2026
**From**: petalTongue team

## Summary

Root documentation refresh to reflect `live` mode, BTSP wire-format fix,
and deep debt zero-warnings. Stale scenario panel types fixed. Version
bumped to 1.6.7 across context files.

## Documentation Updates

| File | Changes |
|------|---------|
| `README.md` | Added `petaltongue live` to Quick Start + architecture tree (7 subcommands). Clippy badge wording simplified. |
| `CONTEXT.md` | Version → 1.6.7. Added `live` mode, BTSP peek fix, deep debt zero entries to Current State. Subcommand count → 7. |
| `START_HERE.md` | Added `live` mode to CLI examples. Updated date. Fixed stale `ecoPrimals/wateringHole/` → `infra/wateringHole/` path. |
| `CHANGELOG.md` | New `[Unreleased]` section for `live` mode, BTSP wire-format, DoomPanelWrapper boxing, futures-util, unused_async. |
| `ENV_VARS.md` | Updated date to April 21. |

## Scenario Fixes

| File | Fix |
|------|-----|
| `sandbox/scenarios/doom-with-stats.json` | `"type": "doom"` → `"doom_game"` (matches `DoomPanelFactory` registration) |
| `sandbox/scenarios/doom-simple-test.json` | `"type": "doom"` → `"doom_game"` (same) |

## Debris Audit Results

| Item | Status |
|------|--------|
| `.bak`/`.orig`/`.old`/`.tmp`/`.swp` files | None found |
| Extra `target/` dirs | None (only root) |
| Stale `TODO.md`/`BACKLOG.md` | None |
| `.plan.md` artifacts | None |
| `sandbox/mock-biomeos/Cargo.lock` | Retained — standalone mock binary, expected |
| Shell scripts (34) | All current, SPDX-tagged, consistent `common.sh` pattern |
| `graph-studio.json` | Retained — aspirational scenario, serde ignores unknown keys |
| Spec cross-ref to `NEURAL_API_EVOLUTION_ROADMAP.md` | Noted — file missing but spec is not blocking |

## Current petalTongue State

- **Version**: 1.6.7
- **Subcommands**: 7 (ui, tui, web, headless, server, live, status)
- **Clippy**: 0 warnings (pedantic + nursery)
- **Tests**: 6,144+ passing
- **Unsafe**: Zero (`#![forbid(unsafe_code)]` all 18 crates + UniBin)
- **async-trait**: Zero (all RPITIT)
- **dyn**: 4 remaining, all idiomatic (callbacks + error trait)
- **reqwest/ring/rustls**: Gone from dependency tree
- **BTSP**: Phase 1 + Phase 2 + wire-format peek (three-way classification)
- **Live mode**: IPC server + egui GUI in single process via shared `Arc<RwLock<>>`
