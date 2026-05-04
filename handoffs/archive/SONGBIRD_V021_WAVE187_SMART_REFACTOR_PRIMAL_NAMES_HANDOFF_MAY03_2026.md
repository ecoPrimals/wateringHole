# Songbird v0.2.1 — Wave 187 Handoff

**Date**: May 3, 2026
**Primal**: Songbird (Network)
**Wave**: 187
**Focus**: Smart refactor, primal-name evolution, timeout centralization

---

## Summary

Wave 187 addressed three deep debt categories: large file refactoring, hardcoded
primal names in production code, and remaining Duration literals.

## Changes

### Smart Refactor (>800L → 0 files over limit)
- `connection.rs` 1043L → 694L: test module (353L) extracted to
  `connection_tests.rs` via `#[path]` attribute
- Tests retain private method access (required for BTSP Phase 3 verification)
- Zero files >800L remain in the workspace

### Primal-Name Evolution
- 15 "BearDog" references in `btsp.rs` and `btsp_phase3.rs` evolved to
  "security provider" (error messages, doc comments, code comments)
- Songbird discovers security provider by capability at runtime, never by name
- Legacy serde aliases and env-var fallbacks preserved for backward compat

### Duration Centralization
- 4 new constants in `songbird-types/defaults/timeouts.rs`:
  - `DEFAULT_BTSP_HANDSHAKE_TIMEOUT` (15s)
  - `DEFAULT_FEDERATION_HEARTBEAT_INTERVAL` (30s)
  - `DEFAULT_FEDERATION_RENDEZVOUS_INTERVAL` (60s)
  - `DEFAULT_SECURITY_ADAPTER_TIMEOUT` (5s)
- Replaced 4 literals in `btsp.rs`, `federation.rs`, `security.rs`

### Mock Isolation (verified, no changes needed)
- `songbird-network-federation` and `songbird-lineage-relay` already gate
  all `Mock` variants behind `#[cfg(any(test, feature = "test-mocks"))]`

## Verification

- 81 btsp-related tests pass
- 0 clippy warnings across all 30 crates
- 0 unsafe code
- 0 `Box<dyn Error>` in production
- 0 bare `#[allow]` without `reason`
- 0 files >800L

## Status

- BTSP Phase 3: FULL (all 3 transport paths, 32 tests)
- Tests: 7,803 lib passed, 0 failures, 22 ignored
- Clippy: 0 warnings
- Unsafe: 0
- Files >800L: 0
