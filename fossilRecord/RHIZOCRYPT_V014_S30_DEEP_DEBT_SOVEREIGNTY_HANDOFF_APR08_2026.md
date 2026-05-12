# rhizoCrypt v0.14.0-dev — Session 30 Handoff

**Date**: 2026-04-08
**Focus**: Deep Debt Cleanup & Sovereignty Evolution
**Status**: Complete — all 1,441 tests pass, zero clippy warnings

## Changes

### Error Type Evolution (Idiomatic Rust)
- `IpcErrorPhase`: Manual `Display` impl → `#[derive(thiserror::Error)]` with `#[error("...")]` attributes
- `BtspConfigError`: New typed error enum replaces `Result<(), String>` for `btsp_env_guard()` — proper variant `FamilyInsecureConflict` with structured `Display`

### Sovereignty: Discovery Coupling Removal
- Added `DiscoveryClient` / `DiscoveryConfig` type aliases in `clients::songbird` module
- Service code (`rhizocrypt-service/src/lib.rs`) now imports capability-neutral aliases instead of vendor-specific types
- Doc comments in constants.rs, rpc lib.rs, service lib.rs, main.rs evolved to capability-neutral language
- Environment variable docs updated: `RHIZOCRYPT_DISCOVERY_ADAPTER` is now the primary documented var

### Smart Refactoring
- `safe_env/mod.rs`: Extracted 427-line test module to `safe_env/tests.rs` (mod.rs: 687 → 260 lines)
- Test assertions in safe_env/tests.rs evolved to use capability-neutral IDs

## Metrics
- **Tests**: 1,441 passing (unchanged)
- **Files**: 136 `.rs` (was 135)
- **Clippy**: 0 warnings (pedantic + nursery enforced)
- **Unsafe**: 0 blocks (`forbid(unsafe_code)` workspace-wide)

## Remaining Debt (Low Priority)
- HTTP client error types (`BearDogHttpError`, `NestGateHttpError`, `ToadStoolHttpError`) share similar `Transport/Status/Parse` variants — could unify
- Primal names in test data (`registry_tests.rs`, `mocks.rs`) are acceptable for a discovery registry testing context
- "Absorbed from" provenance comments are ecosystem fossil record — intentionally preserved
