<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# petalTongue v1.6.6 — WASM Rendering & Deep Debt Sprint 3 Handoff

**Date**: April 6, 2026
**Primal**: petalTongue (visualization)
**Version**: 1.6.6
**Scope**: Client WASM rendering (Gap 6), comprehensive deep debt audit, smart refactoring, dependency deduplication, root doc refresh

---

## Summary

Resolved wetSpring Gap 6 (client WASM rendering) by extracting portable types
and creating a `wasm_bindgen` crate for offline-capable grammar→SVG rendering.
Conducted comprehensive deep debt audit across all dimensions. Refactored the
last oversized file. Unified split crossterm versions. Archived 11 superseded
handoffs to fossil record.

---

## Gap 6 Resolution: Client WASM Rendering

**Source:** `WETSPRING_SCIENCE_NUCLEUS_GAPS_HANDOFF_APR06_2026.md` Gap 6
**Status:** RESOLVED

| Deliverable | Detail |
|-------------|--------|
| `petal-tongue-types` crate | Portable `DataBinding` + `ThresholdRange` — serde-only, zero platform deps |
| `petal-tongue-wasm` crate | `wasm_bindgen` exports: `render_grammar`, `render_binding`, `compile_scene`, `version` |
| `petal-tongue-scene` decoupled | Removed `petal-tongue-core` dependency; now depends on `petal-tongue-types` directly |
| `petal-tongue-core` backward compat | Re-exports types from `petal-tongue-types` — zero downstream breakage |
| CI WASM gate | `cargo check --target wasm32-unknown-unknown -p petal-tongue-wasm` in CI |
| README | `crates/petal-tongue-wasm/README.md` with API docs, JS usage examples, build instructions |

Springs can now embed `petal_tongue_wasm.js` for offline grammar rendering
without calling petalTongue's server-side RPC.

---

## Deep Debt Audit Results

Comprehensive 6-dimension audit across all production code (excluding archive/):

| Dimension | Finding |
|-----------|---------|
| Large files (>800L) | 1 found (`primitive.rs` 816L) — refactored to directory module |
| TODO/FIXME markers | 0 in production code |
| Hardcoded primal names | 31 instances — all in test fixtures (appropriate) |
| Mock/stub in production | 0 leaks — all 266 hits properly `#[cfg(test)]` or `#[cfg(feature = "mock")]` gated |
| Unsafe code | 0 blocks — all 18 crates `#![forbid(unsafe_code)]` |
| Production panics | 0 — all 198 `panic!()` calls in test code |

---

## Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `primitive.rs` | 816 lines (monolithic) | `primitive/mod.rs` (239L) + `primitive/tests.rs` (576L) |

All workspace files now under 800 lines. Largest production file: 239 lines.

---

## Dependency Deduplication

| Change | Impact |
|--------|--------|
| `crossterm` unified to 0.29 | Eliminated 0.28/0.29 split across `petal-tongue-core`, `petal-tongue-ui-core`, `petal-tongue-ui`, `petal-tongue-tui` |

Remaining duplicates (`base64`, `rustix`, `getrandom`, `thiserror` 1 vs 2, `syn` 1 vs 2) are
transitive via the egui/eframe ecosystem — resolve upstream, not in workspace.

---

## Documentation Refresh

| Document | Changes |
|----------|---------|
| `README.md` | Crate count 16→18, added `petal-tongue-types` + `petal-tongue-wasm` to table, WASM in architecture, test count updated, file size metric updated |
| `CONTEXT.md` | Test count updated |
| `CHANGELOG.md` | Added primitive refactor + crossterm unification entries |
| `START_HERE.md` | Updated `data_channel.rs` description (re-export from types), test count |
| Handoffs | Archived 11 superseded petalTongue handoffs to `handoffs/archive/` |

---

## Verification

| Check | Result |
|-------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS |
| `cargo test --workspace` | 5,967+ passed, 0 failed |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | PASS |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo check --target wasm32-unknown-unknown -p petal-tongue-wasm` | PASS |

---

## Remaining Documented Debt (Accepted)

| Item | Status | Notes |
|------|--------|-------|
| Audio socket/direct backends | Stub (`is_available = false`) | Graceful degradation; evolve when PipeWire protocol lands |
| Toadstool display backend (Tier 1) | Spec only | Blocked on Toadstool `display.*` RPC handlers |
| `base64` 0.21 vs 0.22 | Transitive (`ron`/`egui`) | Resolves upstream |
| Haptic / VR modalities | `ModalityStatus::Unavailable` | Spec'd, not yet implemented |
| `missing_docs` suppressed | `#![expect(missing_docs)]` in discovery + UI | Incremental coverage |

---

## Supersedes

All pre-Apr 6 petalTongue handoffs archived:
- `PETALTONGUE_CAPABILITIES_DOCS_CLEANUP_HANDOFF_MAR31_2026.md`
- `PETALTONGUE_CAPABILITY_FIRST_DISCOVERY_COMPLIANCE_HANDOFF_APR02_2026.md`
- `PETALTONGUE_DEEP_DEBT_EVOLUTION_PHASE{2,3,4,5}_HANDOFF_APR0{1,2,3}_2026.md`
- `PETALTONGUE_DOCS_CLEANUP_HANDOFF_APR03_2026.md`
- `PETALTONGUE_IPC_COMPLIANCE_DEEP_DEBT_EVOLUTION_HANDOFF_MAR31_2026.md`
- `PETALTONGUE_SENSORY_MATRIX_HANDOFF_APR02_2026.md`
- `PETALTONGUE_V166_DEEP_DEBT_EVOLUTION_HANDOFF_APR03_2026.md`
- `PETALTONGUE_WAVE99_CAPABILITY_COMPLIANCE_HANDOFF_APR03_2026.md`

Current active handoffs:
- `PETALTONGUE_V166_EVOLUTION_SPRINT2_HANDOFF_APR06_2026.md` (audit remediation + zero-copy)
- `PETALTONGUE_V166_WASM_DEEP_DEBT_SPRINT3_HANDOFF_APR06_2026.md` (this document)
