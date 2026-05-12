# ToadStool S183 — Deep Debt Phase 2: Async I/O, Smart Refactoring, String Evolution

**Date**: April 4, 2026
**Session**: S183
**Commit**: `a20d34cd` on `master`
**Quality**: 21,853 tests (0 failures), Clippy clean, fmt clean

---

## Changes

### 1. Async I/O Fix (2 files)
- `server/tarpc_server.rs` `serve_unix`: `std::fs::{create_dir_all,remove_file,metadata,set_permissions}` → `tokio::fs`
- `cli/commands/mode.rs` `execute_mode_command`: `std::fs::{write,read_to_string,remove_file}` → `tokio::fs`

### 2. Large File Smart Refactoring (5 files → 27 new files)

| Original | Lines | New Structure |
|----------|------:|---------------|
| `byob/validation.rs` | 674 | `validation/{mod,types,quota,services,tests}.rs` |
| `scheduler/execution.rs` | 637 | `execution/{mod,discover,native,wasm,primal,biome_os,tests}.rs` |
| `cli/src/lib.rs` | 635 | `lib.rs` (77L) + `error.rs` (94L) + `biome_model.rs` (356L) + `cli_root.rs` (131L) |
| `pure_jsonrpc/connection.rs` | 633 | `connection/{mod,unix,tcp,tests}.rs` |
| `resources/types.rs` | 622 | `types/{mod,requirements,metrics,limits,system,tests}.rs` |

### 3. Production String Evolution Phase 2 (~20 strings, 8 files)

| Old | New | Files |
|-----|-----|-------|
| "Songbird" | "coordination service" | primal_capabilities/adapters, protocols/transport, configurator/core/apply_validate, analytics/implementation |
| "BearDog" | "security/crypto service" | beardog_integration/client, biomeos_integration/auth_backend |
| "NestGate" | "storage service" | biomeos_integration/storage_backend/nestgate, cli/commands/dispatch/ecosystem |

## Cumulative Progress (S176-183)

| Metric | S176 Start | S183 Now |
|--------|-----------|----------|
| Files >630L (production) | ~19 | ~9 |
| Blocking std::fs in async | ~6 files | ~2 files (edge crate, excluded from workspace) |
| Primal-name log/error strings | ~40 | ~5 remaining (println, deep integration) |
| #[allow] / #[expect] ratio | 76% allow | 40% allow |
| Tests | 21,638 | 21,853 |
