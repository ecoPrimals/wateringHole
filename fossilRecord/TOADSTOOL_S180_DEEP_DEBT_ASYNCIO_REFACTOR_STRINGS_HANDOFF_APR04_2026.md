# ToadStool S180 — Deep Debt: Async I/O, Smart Refactoring, String Evolution

**Date**: April 4, 2026
**Session**: S180
**Commit**: `53f8af82` on `master`
**Quality**: 21,853 tests (0 failures), Clippy clean (`-D warnings`)

---

## Summary

S180 targets three deep-debt categories: blocking I/O in async contexts, large file
decomposition, and hardcoded primal-name string literals in production log/error paths.

## Changes

### 1. Async I/O Fix (1 file, 2 functions)

`distributed/universal/detection/mod.rs` — replaced blocking `std::fs::read_dir("/dev")`
with `tokio::fs::read_dir("/dev").await` in:
- `detect_neuromorphic_platforms` (Akida device scanning)
- `detect_edge_iot_platforms` (serial device counting)

Graceful fallback: `if let Ok(mut entries)` handles missing/inaccessible `/dev`.

### 2. Large File Smart Refactoring (5 files → 22 new files)

| Original | Lines | New Structure |
|----------|------:|---------------|
| `server/cross_gate.rs` | 660 | `cross_gate/{mod,types,dispatcher,router,tests}.rs` |
| `common/infant_discovery/capabilities.rs` | 658 | `capabilities/{mod,discovered,discovery_traits,substrate,endpoint,standard_capabilities,tests}.rs` |
| `distributed/crypto_lock/validation.rs` | 652 | `validation/{mod,types,validators,tests}.rs` |
| `toadstool/runtime/mod.rs` | 651 | `mod.rs` (189L) + `tests.rs` (463L) |
| `cli/configurator/core.rs` | 643 | `core/{mod,defaults,apply_validate,tests}.rs` |

All public APIs preserved. Each submodule ≥50 lines. Tests isolated.

### 3. Production String Evolution (8 files)

Evolved primal-name string literals in `format!`, `tracing::*`, and error constructors:

| Old | New | Files |
|-----|-----|-------|
| `"Songbird"` | `"coordination service"` | songbird_integration/{transport,connection,capability_discovery} |
| `"BearDog"` / `"bearDog"` | `"security/crypto service"` | beardog_integration/discovery, integration/beardog/discovery |
| `"NestGate"` | `"storage service"` | integration/nestgate/client |
| `"Squirrel"` | `"AI/routing service"` | biomeos_integration/agent_backend/squirrel, cli/executor/workload/runtime |

`DistributedError::SongbirdRegistration` display evolved to "Coordination service registration failed".

### 4. Test Alignment

- Updated `SONGBIRD_SOCKET` → `BIOMEOS_COORDINATION_SOCKET` in `ipc_helpers/tests.rs`
- Updated all test assertions matching evolved error strings
- Net +229 tests from new module test files

## Remaining Targets

- 19 production files still >600L (next tier: edge/arduino 680L, byob/validation 675L)
- ~2900 primal-name references remaining (mostly structural: module/type names, serde aliases)
- 57 `#[deprecated]` attributes across 36 files
- 3 active DEBT items (D-TARPC-PHASE3, D-EMBEDDED-PROGRAMMER, D-EMBEDDED-EMULATOR)
