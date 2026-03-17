# petalTongue v1.6.6 — Deep Audit, Coverage Evolution, Capability-Based Cleanup

**Date**: March 17, 2026
**Primal**: petalTongue v1.6.6
**Session**: Comprehensive audit + deep debt resolution + coverage push
**Status**: Complete — all checks pass

---

## Executive Summary

Full-spectrum audit against wateringHole standards followed by systematic debt resolution. Fixed a pre-existing `Arc<str>` serde bug, removed deprecated code, evolved hardcoded demo data to capability-based patterns, refactored over-limit files, and pushed coverage from 85.87% to 89.20% lines (90.02% functions).

**Tests**: 5,484 → 5,833 (+349 new tests)
**Coverage**: 85.87% → 89.20% lines, 86.90% → 90.02% functions
**All checks pass**: fmt, clippy (pedantic+nursery), test, doc, cargo-deny

---

## What Was Done

### Bug Fixes

#### 1. `Arc<str>` serde deserialization (pre-existing)
- `DataSourceId` and `GrammarId` (type aliases for `Arc<str>`) failed to serialize/deserialize in test builds
- Root cause: workspace `serde` missing `rc` feature
- Fix: Added `features = ["derive", "rc"]` to workspace serde dependency
- Impact: Unblocked serialization for interaction engine types across all test suites

### Compliance & Licensing

#### 2. License field harmonization
- 4 crates had inline `license = "AGPL-3.0-or-later"` instead of `license.workspace = true`
- Fixed: `petal-tongue-adapters`, `petal-tongue-tui`, `petal-tongue-entropy`, `petal-tongue-discovery`
- All 16 crates now use workspace license inheritance

### Dead Code Removal

#### 3. Deprecated `backend/toadstool.rs` removed
- 241-line frozen stub behind never-enabled `legacy-toadstool` feature
- Removed: file, module declaration, feature flag, all cfg references
- Active backends unaffected: `display/backends/toadstool.rs`, `display/backends/toadstool_v2.rs`, `audio_providers/toadstool.rs`

### Capability-Based Evolution

#### 4. Demo provider: hardcoded primal names → capability domains
- `demo-beardog-1` → `demo-security-1`
- `demo-songbird-1` → `demo-discovery-1`
- `demo-toadstool-1` → `demo-compute-1`
- Endpoints: `http://demo-beardog:9000` → `capability://security.trust:demo`
- Names: `BearDog Security (Demo)` → `Security Provider (Demo)`
- Updated all test assertions across workspace

### Smart Refactoring (1000-line limit)

#### 5. `primal_panel.rs` (854 lines) → directory module
- `mod.rs` (650), `filter.rs` (13), `display.rs` (34), `stats.rs` (24), `render.rs` (183)

#### 6. `sensory_ui/renderers.rs` (1,228 lines) → 7 focused modules
- `formatting.rs`, `minimal_renderer.rs`, `simple_renderer.rs`, `standard_renderer.rs`, `rich_renderer.rs`, `immersive_renderer.rs`, `mod.rs`

#### 7. `adaptive_ui.rs` (1,032 lines) → directory module
- `mod.rs` (110), `formatting.rs` (103), `renderers.rs` (342), `tests.rs` (491)

#### 8. `timeline_view/tests_extended.rs` (1,111 lines) → split
- `tests_extended.rs` (726), `tests_rendering.rs` (390)

### Coverage Push

#### 9. Systematic test additions across 30+ files
- trust_dashboard: 38% → covered (headless egui render tests)
- scene_bridge/paint: 56% → covered (all primitive types, hit map)
- sensors/audio: 67% → covered (poll, discover, beep paths)
- ui_mode: 68% → covered (scenario paths, error variants)
- timeline_view: 70% → covered (details panel, CSV export, zoom)
- sensory_ui: 64-71% → covered (all 5 renderer tiers)
- graph_editor, metrics_dashboard, adaptive_ui, biomeos_provider, proprioception_panel, device_panel, doom_panel, traffic_view, system_monitor, display_verification, graph_metrics_plotter, provenance_trio, songbird_client, mdns_provider, TUI update, app init/mod, graph_canvas interaction, display renderer/backends

### Documentation & Cleanup

#### 10. Stale content cleaned
- Fixed misleading "reqwest with rustls-tls" comment in discovery Cargo.toml
- Removed placeholder comment in human_entropy_window/tests.rs
- Updated README and START_HERE test counts
- Removed archive scripts, showcase-legacy, and archived crates (34 .sh scripts, 33 .rs files)
- Archive now contains only documentation (fossil record)

---

## Quality Summary

| Metric | Before | After |
|--------|--------|-------|
| Tests | 5,484 | 5,833 |
| Line coverage | 85.87% | 89.20% |
| Function coverage | 86.90% | 90.02% |
| Max file size | 854 lines | 908 lines |
| Clippy warnings | 0 | 0 |
| Format violations | 0 | 0 |
| Doc generation | Clean | Clean |
| TODO/FIXME/HACK in code | 0 | 0 |
| Unsafe code | 0 | 0 |
| Files changed | - | 53 files, +4,523 / -2,969 |

---

## Remaining Coverage Gap (89.2% → 90% lines)

The remaining 0.8% gap is concentrated in:
- `biomeos_integration/provider.rs` — async network fetch paths requiring live Unix sockets
- `app/mod.rs` — egui event loop requiring display context
- `display/backends/*` — toadstool/toadstool_v2 requiring real biomeOS socket
- `graph_manager.rs` — Neural API render paths

These require either real IPC infrastructure or display context for full coverage. Function coverage has already crossed 90.02%.

---

## Architecture Compliance (wateringHole standards)

| Standard | Status |
|----------|--------|
| UniBin | PASS — single `petaltongue` binary with subcommands |
| ecoBin | PASS — pure Rust, deny.toml bans C deps |
| JSON-RPC + tarpc | PASS — dual protocol, tarpc primary |
| Capability-based discovery | PASS — zero hardcoded primal names in production |
| Self-knowledge only | PASS — discovers others at runtime |
| Zero-copy (bytes::Bytes) | PASS — IPC, rendering, audio pipelines |
| AGPL-3.0-or-later | PASS — all crates, workspace inheritance |
| `#![forbid(unsafe_code)]` | PASS — root binary + all crates |
| Files under 1000 lines | PASS — max 908 lines |
| Semantic method naming | PASS — `{domain}.{operation}` |
| No TODO/FIXME in code | PASS |

---

## Next Session Recommendations

1. Push line coverage to 90% via integration tests with mock Unix sockets
2. Consider removing `specs/ECOBLOSSOM_EVOLUTION_PLAN.md` references to deleted `ToadstoolBackend`
3. Evolve `provenance_trio.rs` hash from std to blake3 when crate is available
4. Monitor approaching-limit files: `biomeos_integration/provider.rs` (908), `proprioception_panel.rs` (907)
