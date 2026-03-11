# petalTongue v1.4.2 — Pedantic Coverage Handoff

**Date**: March 9, 2026  
**From**: petalTongue  
**Status**: All crates compile, 1,816 tests passing, zero clippy warnings

---

## Summary

petalTongue v1.4.2 enables clippy::pedantic workspace-wide, adds 332 tests
(1,484 to 1,816), and raises coverage from 56% to 63% line / 63% to 67%
function. All quality gates pass clean.

---

## Key Changes

### clippy::pedantic (workspace-wide)

Configured via `[workspace.lints.clippy]` in root Cargo.toml. All crates
inherit via `[lints] workspace = true`. Selective allows for:
missing_errors_doc, missing_panics_doc, must_use_candidate,
module_name_repetitions, cast precision/truncation/sign, similar_names,
wildcard_imports, doc_markdown, float_cmp, default_trait_access,
too_many_lines, wildcard_in_or_patterns, items_after_statements,
needless_pass_by_value, unused_async. ~390 pedantic warnings auto-fixed.

### +332 New Tests

- **TUI**: Rendering tests via ratatui TestBackend (all 8 views)
- **Core**: graph validation, session, config, constants, instance, types,
  sensor, dynamic schema, rendering awareness, state sync, awakening coordinator
- **UI**: scenario, proprioception, sensory capabilities, display traits,
  display verification, human entropy, process viewer, graph metrics,
  system dashboard, app panels
- **IPC/discovery**: server, unix socket provider, streaming protocol,
  execution state
- **Other**: doom-core WAD parsing, audio sonification, CLI parsing,
  visual 2D interaction/animation

### Coverage: 56% to 63% line, 63% to 67% function

Logic extraction pattern: pure data transforms extracted from rendering
functions for testing. Remaining gap: egui-dependent rendering code (~27%)
needs headless egui infrastructure.

### Quality Gates

All pass clean: cargo fmt, clippy (pedantic), doc, deny, test.

---

## For Other Primals

- petalTongue's IPC contract unchanged
- JSON-RPC methods unchanged
- No breaking changes

---

## Quality Metrics

- **Tests**: 1,816 passing
- **Clippy**: Zero warnings (pedantic enabled)
- **Coverage**: 63% line, 67% function
- **Formatting**: Clean
- **Unsafe**: Zero (workspace-wide `#![forbid(unsafe_code)]`)
