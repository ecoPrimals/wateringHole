# petalTongue v1.6.6 — UUI Evolution, Smart Refactoring & Deep Debt Handoff

**Date**: March 16, 2026
**Version**: 1.6.6
**Primal**: petalTongue (Universal User Interface)
**Session**: UUI language evolution, smart refactoring, clone reduction, coverage push, license correction, clippy deep clean, deprecated item evolution
**Status**: GREEN / COMPLETE
**Supersedes**: `PETALTONGUE_V163_TYPED_ERRORS_PEDANTIC_LINTS_SMART_REFACTORING_HANDOFF_MAR16_2026.md`

---

## Session Summary

Comprehensive audit of petalTongue against wateringHole standards followed by
deep execution. Evolved all 16 crates from GUI-centric language to Universal
User Interface vernacular (200+ instances). Created canonical UUI glossary
module. Corrected license from AGPL-3.0-only to AGPL-3.0-or-later per
scyBorg Provenance Trio guidance. Pushed 13 of 15 non-UI crates to 90%+
coverage with 112 new tests. Resolved 500+ clippy pedantic/nursery warnings.
Added `# Errors` documentation to 68 Result-returning functions. Cleaned
root docs, removed orphaned directories, consolidated spec archives.

---

## Key Changes

### Universal User Interface Language Evolution

- 200+ doc comments and user-facing strings updated across all crates + UniBin
- Terminology evolution: "GUI" → "display", "click" → "activate",
  "visible" → "perceivable", "screen" → "display", "see" → "perceive",
  "without GUI" → "without display", "Desktop GUI" → "Desktop display"
- New `petal_tongue_core::uui_glossary` module with canonical constants:
  - `PRIMAL_ROLE`, `INTERFACE_PHILOSOPHY`, `DESIGN_PRINCIPLE`
  - `modality_names`: VISUAL, AUDIO, HAPTIC, TERMINAL, BRAILLE, JSON_API, ACOUSTIC, CHEMICAL
  - `user_types`: HUMAN_SIGHTED, HUMAN_BLIND, HUMAN_MOBILITY_LIMITED, HUMAN_DEAF, AI_AGENT, NON_HUMAN, HYBRID
  - `same_dave`: SENSORY_AFFERENT, MOTOR_EFFERENT
- Module documentation covers Two-Dimensional Universality, Modality Tiers,
  SAME DAVE cognitive model, and Terminology Evolution table

### License Correction

- All `Cargo.toml` license fields: `AGPL-3.0-only` → `AGPL-3.0-or-later`
- All SPDX headers: updated to `AGPL-3.0-or-later`
- Per `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` ecosystem policy

### Coverage Improvements (112 new tests, 5,113 → 5,225)

| Crate | Before | After |
|-------|--------|-------|
| petal-tongue-api | 76.7% | 96.5% |
| petal-tongue-animation | 85.3% | 99.3% (egui) |
| petal-tongue-ui-core | 86.6% | 93.5% |
| petal-tongue-discovery | 83.5% | 91.2% |
| petal-tongue-cli | 87.5% | 90.1% |
| doom-core | 87.6% | 90.6% |
| error.rs (UniBin) | 0% | 100% |
| petal-tongue-ipc | 87.5% | 88.8% |

### Clippy Deep Clean (500+ warnings resolved)

- `cast_precision_loss`: explicit `#[expect]` with documented reasons
- `suboptimal_flops`: replaced `a * b + c` with `mul_add()`
- `significant_drop_tightening`: explicit `drop()` for RwLock guards
- `future_not_send`: restructured async boundaries
- `similar_names`: renamed variables for clarity
- `float_cmp`: epsilon-based comparisons
- `needless_collect`: eliminated intermediate allocations
- `missing_errors_doc`: 68 functions in petal-tongue-core documented

### Smart Refactoring (2 large files decomposed)

| File | Before | After | Modules |
|------|--------|-------|---------|
| doom-core/src/lib.rs | 910 | 47 | error, key, state, instance, tests |
| petal-tongue-tui/src/app.rs | 887 | app/mod (16) | config, tui, render, update, tests |

All public APIs preserved via re-exports. No breakage to external callers.

### Clone Reduction & Idiomatic Rust

- `property_panel.rs`: replaced per-parameter clones with bulk clone, `mem::take` for moves
- `server.rs`: eliminated redundant clones via variable reuse
- `interaction/engine.rs`: moved `Vec` by value instead of cloning in `apply_intent`
- `engine.rs`, `structure.rs`: Arc/test clones verified necessary — no changes

### IPC Coverage Push (19 new tests)

- `json_rpc_client`: fallback method chains (primal.list → discover_primals, topology → get_topology)
- `socket_path`: edge cases (socket exists, directory, nonexistent, custom parent)
- `server`: malformed JSON handling, TCP request routing, socket cleanup on drop
- `client`: error response handling, unexpected response types

### Deprecated Items Evolution

- All deprecated code confirmed behind feature gates (`legacy-toadstool`, `legacy-audio`, `mock`)
- HTTP provider fallback docs improved with "When to Use" guidance
- PrimalInfo deprecated fields handled with `#[allow(deprecated)]` in tests

### Infrastructure Cleanup

- Removed empty orphan directories: `graph_manager/`, `ipc/server/`
- Consolidated `specs/archive/` → `archive/specs-archive/`
- Hardcoded bind addresses → `config.network.web_addr()` / `headless_addr()`
- Fixed flaky `test_discover_graceful_degradation_returns_ok` (mDNS isolation)

---

## Verification State

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | Zero warnings (pedantic + nursery) |
| `cargo test --workspace` | 5,244 passed, 0 failed |
| `cargo doc --workspace --no-deps` | Clean |
| `cargo llvm-cov --workspace --summary-only` | 85.76% line / 86.91% branch |
| Files over 1000 lines | None (largest: 902) |
| `anyhow` in production | Zero (dev-dependencies only) |
| TODO/FIXME/HACK in production | Zero |
| Dead code warnings | Zero |
| SPDX headers | All source files (AGPL-3.0-or-later) |

---

## Remaining Work

1. **Coverage**: petal-tongue-ipc ~87% → 90% (deep async socket/timeout paths)
2. **Coverage**: petal-tongue-ui 75.7% → 90% (requires render/logic separation)
3. **petal-tongue-ui architectural evolution**: Extract remaining render logic to pure functions
4. **Incremental doc completion**: Crates with `#![expect(missing_docs)]`
5. **Public API renames**: `visible` → `perceivable`, `Click` → `Activate` (with proper versioning)
6. **Live integration testing**: End-to-end with running springs
7. **Fuzz testing**: `cargo-fuzz` harnesses for JSON-RPC, grammar, scenarios

---

## wateringHole Compliance

| Standard | Status |
|----------|--------|
| PRIMAL_IPC_PROTOCOL | Compliant — 35 capabilities, ipc.register |
| ECOBIN_ARCHITECTURE_STANDARD | Compliant — zero C deps, pure Rust |
| UNIBIN_ARCHITECTURE_STANDARD | Compliant — 6 subcommands (ui, tui, web, headless, server, status) |
| SEMANTIC_METHOD_NAMING | 40+ methods, domain.operation[.variant] |
| GATE_DEPLOYMENT_STANDARD | Compliant — AGPL-3.0-or-later, SPDX headers |
| SCYBORG_PROVENANCE_TRIO | Client wired (rhizoCrypt + sweetGrass + loamSpine) |
| SPRING_AS_NICHE_DEPLOYMENT | Full niche.yaml with organisms/interactions |
| UNIVERSAL_USER_INTERFACE_SPEC | Compliant — UUI glossary, multi-modal, SAME DAVE |
| PRIMAL_MULTIMODAL_RENDERING | Glossary-aligned modality names and user types |

---

## Explicit Needs from Ecosystem

See `wateringHole/petaltongue/PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md`.

No new needs discovered this session. Existing gaps remain:
- 3D rendering pipeline (barraCuda tessellation/projection ops)
- Audio hardware playback (capability provider, not in petalTongue itself)
- GPU compute parity (math.stat.*, math.tessellate.*, math.project.*)
