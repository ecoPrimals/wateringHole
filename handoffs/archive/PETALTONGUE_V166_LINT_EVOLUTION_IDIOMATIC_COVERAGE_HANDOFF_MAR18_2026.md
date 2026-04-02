# petalTongue v1.6.6 — Lint Evolution, Idiomatic Rust, Coverage to 90%

**Date**: March 18, 2026
**Primal**: petalTongue v1.6.6
**Session**: Deep debt resolution — lint evolution, idiomatic modernization, coverage push
**Status**: Complete — all checks pass

---

## Executive Summary

Systematic evolution of the petalTongue codebase from the previous audit session. Replaced all blanket `#[allow]` lint suppressions with targeted `#[expect]` with reasons, which surfaced and fixed 45 hidden clippy errors. Refactored 4 over-limit files into cohesive submodules. Replaced 3 hardcoded localhost/IP references with configurable constants. Added ~140 new tests pushing line coverage from 89.35% to 90.07%.

**Tests**: 5,833 → 5,973 (+140 new tests)
**Coverage**: 89.35% → 90.07% lines, 90.54% functions
**All checks pass**: fmt, clippy (pedantic+nursery), test, doc

---

## What Was Done

### 1. Lint Evolution: `#[allow]` → `#[expect]` with reasons

- **`petal-tongue-ui/src/lib.rs`**: Replaced 38 blanket `#[allow]` attributes with 10 targeted `#[expect]` attributes, each with a documented reason
- **`petal-tongue-ui-core/src/lib.rs`**: Changed `#![allow(missing_docs)]` to `#![warn(missing_docs)]` — crate was already fully documented
- **`petal-tongue-telemetry/src/lib.rs`**: Cleaned duplicated `#[expect]` attributes
- This surfaced **45 hidden clippy errors** that were previously blanket-suppressed

### 2. Idiomatic Rust Modernization (45 fixes)

All 45 surfaced clippy errors were fixed by modernizing the code:

- `ref_option`: Changed `&Option<T>` → `Option<&T>` across function signatures and all call sites
- `collapsible_if`: Merged nested `if` chains into flat conditionals
- `redundant_clone` / `assigning_clones`: Replaced `.clone()` with `.clone_from()` where applicable
- `should_implement_trait`: Added `FromStr` impl alongside `from_str` methods
- `await_holding_lock`: Restructured async code to release `RwLock` guards before `.await` points
- `let...else`: Converted `match`/`if let` with early returns to `let...else`
- `map_identity`: Removed identity `map_err` calls

### 3. Hardcoded Localhost Removal

- **`petal-tongue-discovery/src/lib.rs`**: Changed `"http://localhost:{}"` in user-facing warning → `"http://<host>:{}"`
- **`petal-tongue-ipc/src/server.rs`**: Replaced `TcpListener::bind("127.0.0.1:0")` with env-configurable `PETALTONGUE_TCP_BIND_HOST`, falling back to `petal_tongue_core::constants::DEFAULT_LOOPBACK_HOST`
- **`petal-tongue-ui/src/universal_discovery.rs`**: Replaced hardcoded `"http://localhost"` default with `format!("http://{}", petal_tongue_core::constants::DEFAULT_LOOPBACK_HOST)`

### 4. Smart File Refactoring (1000-line limit)

| Original File | Lines | Split Into | Result |
|---|---|---|---|
| `biomeos_integration/provider.rs` | 911 | `provider/mod.rs` + `provider/jsonrpc.rs` + `provider/tests.rs` | 467 lines max |
| `proprioception_panel.rs` | 907 | `proprioception_panel/mod.rs` + `helpers.rs` + `tests.rs` | 493 lines max |
| `app/mod.rs` | 905 | `app/mod.rs` + `app/update.rs` + `app/tests.rs` | 527 lines max |
| `mdns_provider.rs` | 904 | `mdns_provider/mod.rs` + `packet.rs` + `tests.rs` | 255 lines max |

### 5. Coverage Push: 89.35% → 90.07%

Added ~140 new targeted tests across 21 files:
- `panel_registry.rs`, `output_verification.rs`, `graph_manager.rs`, `graph_metrics_plotter.rs`
- `human_entropy_window/state.rs`, `app_panels/builders.rs`, `app/update.rs`
- `biomeos_ui_manager.rs`, `egui_compiler.rs`, `app_panels/layout.rs`
- `error.rs`, `app/sensory.rs`, `focus_manager.rs`, `accessibility.rs`
- `event_loop.rs`, `graph_editor/graph.rs`, `graph_editor/rpc_methods/mod.rs`
- `live_data.rs`, `tutorial_mode.rs`, `src/main.rs`, `src/ui_mode.rs`

### 6. License Compliance

- **`doom-core/src/lib.rs`**: Added ORC license notice for game mechanics
- **`specs/LICENSE.md`**: Created CC-BY-SA 4.0 license for specifications and documentation
- **`README.md`**: Expanded license section to scyBorg Provenance Trio table

### 7. Documentation Cleanup (this session continuation)

- Fixed stale `specs/archive/` references in 2 spec documents → `archive/specs-archive/`
- Updated `README.md`: "Rust nightly" → "Rust stable 1.85+" (edition 2024 is stable)
- Updated `START_HERE.md`: test count 5,833 → 5,973, date to March 18
- Updated `ENV_VARS.md`: fixed misplaced `PETALTONGUE_TELEMETRY_DIR` heading, updated date
- Aligned showcase timing docs (README, 00_START_HERE, QUICK_START.sh) to "~15 minutes"

---

## Quality Summary

| Metric | Before | After |
|--------|--------|-------|
| Tests | 5,833 | 5,973 |
| Line coverage | 89.35% | 90.07% |
| Function coverage | — | 90.54% |
| Max file size | 911 lines | 901 lines |
| Blanket `#[allow]` | 38+ | 0 |
| `#[expect]` with reasons | 0 | 10+ |
| Clippy warnings | 0 (suppressed) | 0 (real) |
| Hardcoded localhost | 3 | 0 |
| Stale spec refs | 2 | 0 |
| Format violations | 0 | 0 |
| Doc generation | Clean | Clean |

---

## Architecture Compliance (wateringHole standards)

| Standard | Status |
|----------|--------|
| UniBin | PASS — single `petaltongue` binary with subcommands |
| ecoBin | PASS — pure Rust, deny.toml bans C deps |
| JSON-RPC + tarpc | PASS — dual protocol, tarpc primary |
| Capability-based discovery | PASS — zero hardcoded primal names in production |
| Self-knowledge only | PASS — discovers others at runtime |
| Zero-copy (bytes::Bytes, Arc<str>) | PASS — IPC, rendering, audio pipelines |
| AGPL-3.0-or-later | PASS — all crates, workspace inheritance |
| scyBorg Provenance Trio | PASS — AGPL + ORC + CC-BY-SA 4.0 |
| `#![forbid(unsafe_code)]` | PASS — root binary + all crates |
| Files under 1000 lines | PASS — max 901 lines |
| Semantic method naming | PASS — `{domain}.{operation}` |
| No TODO/FIXME in code | PASS |
| `deny(unwrap_used, expect_used)` | PASS — `#[expect]` for justified suppressions |
| `warn(missing_docs)` | PASS — all crates |
| Edition 2024 | PASS — Rust stable 1.85+ |

---

## Files Changed

- Root: `README.md`, `START_HERE.md`, `ENV_VARS.md`
- Specs: `HUMAN_ENTROPY_CAPTURE_SPECIFICATION.md`, `DISCOVERY_INFRASTRUCTURE_EVOLUTION_SPECIFICATION.md`, `LICENSE.md`
- Showcase: `README.md`, `00_START_HERE.md`
- Crates: `petal-tongue-ui` (extensive — lint evolution, 45 clippy fixes, 4 file refactors), `petal-tongue-ui-core`, `petal-tongue-telemetry`, `petal-tongue-discovery`, `petal-tongue-ipc`, `doom-core`, `src/main.rs`
- 21 files with new tests

---

## Next Session Recommendations

1. Consider evolving `provenance_trio.rs` hash from std to blake3 when crate is available
2. Monitor approaching-limit files: `graph_editor/ui_components.rs` (901 lines)
3. Evolve showcase demo timing to be fully data-driven (measure actual runtime)
4. Consider committing `Cargo.lock` for reproducible binary builds (currently gitignored)
