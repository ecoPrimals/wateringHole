# petalTongue v1.3.1 -- Grammar Architecture, Audit & Cleanup Handoff

**Date**: March 8, 2026  
**Session**: Comprehensive audit + Grammar of Graphics architecture + root doc cleanup  
**Status**: Handoff ready

---

## What Was Done

### 1. Comprehensive Codebase Audit

Full audit against wateringHole standards. Key findings:

| Area | Result |
|------|--------|
| Tests | 1,309 passing, 0 failures, 23 ignored |
| Formatting | Clean (`cargo fmt --check`) |
| Clippy | 76 errors under `-D warnings`, 487 warnings total |
| Doc warnings | 141 (missing field docs, deprecated egui API) |
| Coverage | 54.10% line (target: 90%) |
| Unsafe | `#![forbid(unsafe_code)]` on 5/17 crates |
| Files > 1000 lines | 0 (max: 833) |
| SPDX headers | 289+ files of ~320 |
| TODOs/stubs | ~60 items |
| License | AGPL-3.0-only (Cargo.toml says `AGPL-3.0`, should be `-only`) |

### 2. Grammar of Graphics Architecture (3 new specs)

- **`specs/GRAMMAR_OF_GRAPHICS_ARCHITECTURE.md`**: Full trait hierarchy
  (Scale, Geometry, CoordinateSystem, Statistic, Aesthetic, Facet),
  GrammarExpr struct, grammar compiler pipeline, Primitive output enum,
  modality compilers, domain applications (molecules, games, universes),
  5-phase evolution path.

- **`specs/UNIVERSAL_VISUALIZATION_PIPELINE.md`**: End-to-end pipeline
  (data ingest → grammar → compiler → barraCuda offload → modality render
  → interaction → inverse scale). Full barraCuda IPC contract with
  semantic method names. Performance targets.

- **`specs/TUFTE_CONSTRAINT_SYSTEM.md`**: 7 machine-checkable constraints
  (data-ink ratio, lie factor, chartjunk, small multiples, data density,
  color accessibility, smallest effective difference). Auto-correction.
  Multi-modal extensions (audio, TUI).

### 3. wateringHole Updates

- **New**: `petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md` -- How other
  primal teams send grammar expressions to petalTongue. Grammar reference,
  domain examples, sovereignty checklist.
- **Updated**: `petaltongue/README.md` -- Grammar evolution, barraCuda
  integration, visualization IPC methods, corrected metrics.
- **Updated**: `PRIMAL_REGISTRY.md` -- petalTongue entry rewritten with
  grammar primitives, Tufte constraints, interaction pipeline.

### 4. Root Doc Cleanup

- **README.md**: Corrected quality metrics to actual state (was claiming
  0 clippy errors, 90% coverage, 16/17 forbid unsafe -- none true).
  Added specs table, grammar evolution section.
- **PROJECT_STATUS.md**: Corrected version to 1.3.0 (was 2.0.0). Added
  known debt section with specific clippy counts, coverage gaps, stubs.
- **START_HERE.md**: Updated architecture rules, added spec references.
- **CHANGELOG.md**: Added 1.3.1 entry, fixed stale links to STATUS.md
  and NAVIGATION.md (files don't exist at root).

### 5. Debris Cleanup

Moved to archive:
- 7 stale root shell scripts (fix_tests.sh, READY_TO_PUSH.sh,
  test-audio-discovery.sh, verify-substrate-agnostic-audio.sh,
  test-with-plasmid-binaries.sh, test_socket_configuration.sh,
  launch-demo.sh)
- 3 scripts from scripts/ directory
- 1 script from tools/scripts/
- web/index.html

Removed empty directories:
- demo/ (python-tools/, toadstool-server/)
- web/ (static/)
- tools/ (scripts/)
- coverage-html/ (html/)
- showcase/06-performance, showcase/logs, showcase/02-biomeos-integration

---

## What Needs Doing Next

### Priority 1: Clippy Clean (76 errors)

Add `clippy.toml` and `rustfmt.toml` to workspace root. Fix:
- 31 missing struct field docs (add `///` doc comments)
- 8 unnecessary Result wrappers (simplify return types)
- 8 structs with > 3 bools (refactor to enums or bitflags)
- 4 unused self args (make associated functions)
- 9 precision-loss casts (use `f64` or explicit `#[allow]` with justification)

### Priority 2: Coverage (54% → 90%)

Worst modules need tests:
- `sensory_ui.rs` (0%), `status_reporter.rs` (0%), `system_monitor_integration.rs` (0%)
- `system_dashboard.rs` (17%), `main.rs` (19%), `traffic_view.rs` (24%)

### Priority 3: Hardcoded Primal Names

Remove from production code (keep in tests/mocks only):
- `biomeos_client.rs`: mock-beardog, mock-toadstool, etc.
- `proprioception_panel.rs`: BearDog, Songbird, Toadstool labels
- `jsonrpc_provider.rs`: songbird-discovery.sock

### Priority 4: Grammar Phase 1

Create `petal-tongue-grammar` crate with core traits. Port topology view
from ad-hoc `graph_canvas.rs` to grammar expression. See
`specs/GRAMMAR_OF_GRAPHICS_ARCHITECTURE.md` Phase 1.

### Priority 5: Missing Infrastructure

- `clippy.toml` with pedantic configuration
- `rustfmt.toml` with edition 2024 settings
- `deny.toml` for dependency auditing
- CI/CD pipeline (GitHub Actions or equivalent)
- Cargo.toml `license = "AGPL-3.0-only"` (currently `AGPL-3.0`)

---

## Version Note

The Cargo.toml says `version = "1.3.0"` but the CHANGELOG had entries up to
`[2.3.0]`. The CHANGELOG versions were aspirational session labels, not semver
releases. The actual published version is 1.3.0. Future CHANGELOG entries should
match Cargo.toml.
