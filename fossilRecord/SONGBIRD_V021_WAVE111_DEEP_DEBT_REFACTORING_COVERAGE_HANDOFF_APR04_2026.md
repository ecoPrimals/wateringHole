# Songbird v0.2.1 — Wave 111: Deep Debt — Smart Refactoring + Coverage Expansion

**Date**: April 4, 2026
**Commit**: `5ca196fa` on `main`
**Previous**: Wave 110 (`3ecdfcfd`) — primalSpring audit response

---

## Summary

Smart file refactoring, production unwrap verification, and test coverage expansion
across lowest-density crates.

## Changes

### Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `concurrent_helpers.rs` | 787L single file | `mod.rs` 44L + 8 submodules (largest 133L) |

Submodules: `readiness.rs`, `completion.rs`, `barrier.rs`, `retry.rs`, `limiter.rs`,
`unix_socket.rs`, `types.rs`, `tests.rs`. Public API unchanged via `pub use` re-exports.

### Production Unwrap Verification

| Target | Result |
|--------|--------|
| sled storage (consent + task) | All 55 unwrap in `#[cfg(test)]` — production uses `?`/`.context()` |
| sovereign-onion (address, crypto, keys) | All unwrap in doc examples or test blocks |
| stun/server.rs | All unwrap in doc examples |
| bluetooth_pure.rs | All unwrap in feature-gated test module |
| **Total production unwrap** | **0** |

### Test Coverage Expansion (+38 tests)

| Crate | Tests Added | Focus |
|-------|-------------|-------|
| songbird-tor-protocol | +16 | Error paths, circuit state, HTTP fetch validation, storage, cell encoding |
| songbird-onion-relay | +12 | Mesh types, endpoint priority ordering, relay fields, IPv6 |
| songbird-lineage-relay | +10 | Bincode round-trips, masking levels, connection types, authorization |

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS |
| `cargo test --workspace` | **12,568 passed**, 0 failed |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 12,568 passed (+38 from W110) |
| Production unwrap | 0 verified |
| Files >800L | 0 (largest production 709L) |
| Primal-name refs | 541 .rs / 174 files (unchanged — this wave focused on hygiene) |
