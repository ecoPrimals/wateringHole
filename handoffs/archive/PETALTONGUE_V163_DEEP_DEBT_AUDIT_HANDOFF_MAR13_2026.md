# petalTongue v1.6.3 -- Deep Debt Audit & Evolution

**Date**: March 13, 2026
**From**: petalTongue team
**To**: All primals, biomeOS team

---

## Summary

Comprehensive audit and deep debt evolution of petalTongue. All CI checks pass, sovereignty violations resolved, large files refactored, zero-copy patterns improved, test coverage expanded, and pedantic clippy enabled.

---

## Quality

| Metric | Before | After |
|--------|--------|-------|
| Tests | 3,711 | 3,752 (+41 new) |
| Clippy | 1 error (CI fail) | Zero warnings |
| Pedantic clippy | ~30 errors | All resolved or justified |
| Coverage | 79.5% line | 79.8% line, 81.0% function |
| Unsafe | `forbid` on 15/16 crates | `forbid` on all 16 crates + UniBin |
| Largest file | 988 lines | 977 lines (2 large files refactored) |
| Cargo deny | 2 stale ignores | Clean |
| CI thresholds | fail@70%, warn@80% | fail@80%, warn@90% |
| Hardcoded primals | 3 production violations | Zero (capability-based) |

---

## What Changed

### Sovereignty (capability-based discovery)

- `scenario_loader.rs`: Replaced hardcoded spring family matching with suffix-based agnostic parser
- `toadstool.rs` display backend: Changed `toadstool.display.*` RPC methods to semantic `display.*` (provider-agnostic, per SEMANTIC_METHOD_NAMING_STANDARD)
- `tutorial_mode.rs`: Replaced hardcoded `/run/user/1000` with `system_info::get_user_runtime_dir()`
- Protocol priority documented as tarpc PRIMARY, JSON-RPC SECONDARY, HTTP FALLBACK

### Safety

- Added `#![forbid(unsafe_code)]` to `src/main.rs` (UniBin entry point)
- Production `unreachable!()` in `retry.rs` replaced with `expect()` with documented invariant
- All production `unwrap()` verified to be in test code only

### Smart Refactoring

- `visualization_handler/state.rs` (988 lines) → `state/` module with 6 domain-aligned files: types, session lifecycle, stream handler, render handlers, queries, tests
- `petal-tongue-cli/src/lib.rs` (933 lines) → `commands.rs`, `handlers.rs`, `resolve.rs`, `output.rs`
- `scene_graph.rs` → extracted `NodeId` to `node_id.rs` (after proptest additions pushed it over 1000)

### Zero-Copy

- `NodeId`: evolved from `type NodeId = String` to `struct NodeId(Arc<str>)` -- clone is atomic refcount only
- `json_rpc_client.rs`: Response parsing from `read_line→from_str` to `read_until→from_slice` (eliminates intermediate String)
- `state_sync.rs`: `InMemoryPersistence` stores `Arc<DeviceState>` -- lock held shorter, clone outside lock

### Pedantic Clippy

- Fixed `uninlined_format_args`, `while_float`, `cast_precision_loss`, `missing_panics_doc`, `similar_names`, `needless_collect`, `significant_drop_in_scrutinee`, `future_not_send`, `redundant_clone`, `single_char_pattern`, `useless_vec`, `identity_op`, `collapsible_match/if`

### Test Coverage

- `ui_mode.rs`: 3.7% → 45.8% (extracted testable helpers)
- `traffic_view/view.rs`: +7 tests + 1 proptest (bezier symmetry)
- `timeline_view/view.rs`: +9 tests (filtering, formatting, ordering)
- New proptest strategies: scene_graph (3), dynamic_schema (2), tarpc_types (14)
- `# Panics` docs added to `state_sync.rs`, `telemetry/collector.rs`

### Docs & Config

- Cleaned 2 stale advisory ignores from `deny.toml`
- CI coverage thresholds aligned with `llvm-cov.toml` (fail@80%, warn@90%)
- All root docs updated: README, START_HERE, PROJECT_STATUS, QUICK_START
- Fixed broken build script reference in BIOMEOS_INTEGRATION_GUIDE
- Cleaned sandbox README (removed references to non-existent scripts/scenarios)

---

## Standards Compliance

| Standard | Status |
|----------|--------|
| UNIBIN_ARCHITECTURE_STANDARD | Compliant (1 binary, 5 modes) |
| ECOBIN_ARCHITECTURE_STANDARD | Compliant (pure Rust, no C deps) |
| UNIVERSAL_IPC_STANDARD_V3 | Compliant (tarpc primary + JSON-RPC secondary) |
| SEMANTIC_METHOD_NAMING_STANDARD | Compliant (`domain.operation` everywhere) |
| AGPL-3.0-only | All source files, SPDX headers, cargo deny clean |
| Files under 1,000 lines | CI enforced, all pass |
| `#![forbid(unsafe_code)]` | All crates + UniBin |
| Capability-based discovery | Zero hardcoded primal names in production |

---

## Remaining Work

- **Coverage**: 79.8% vs 90% target. Main gaps are egui rendering paths (`traffic_view`, `timeline_view`, `trust_dashboard`) which require headless harness infrastructure
- **Proptest**: Now 20+ strategies but more complex invariants could be tested
- **Benchmarks**: Only grammar compiler benchmarked; scene graph and IPC hot paths need attention

---

## For Downstream Teams

### For biomeOS

- Display backend now uses `display.*` semantic methods (not `toadstool.display.*`)
- Ensure biomeOS routes `display.*` methods to the display capability provider

### For springs

- Scenario domain inference is now suffix-based: any `*spring`/`*Spring` family name resolves automatically
- No changes needed to existing spring JSON scenario format

### For ToadStool

- `toadstool_v2` display backend is the canonical implementation
- Legacy `backend/toadstool.rs` is frozen and deprecated (graceful bail)
- tarpc display methods: `display.query_capabilities`, `display.create_window`, `display.commit_frame`, `display.destroy_window`
