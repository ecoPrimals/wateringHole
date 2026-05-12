<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 Wave 95 — Deep Debt Cleanup Handoff

**Date**: May 8, 2026
**Primal**: BearDog (beardog-tunnel, beardog-genetics, beardog-types, beardog-utils)
**Wave**: 95
**Previous**: Wave 94 (JH-1 Ionic Tokens)

---

## Summary

Wave 95 is a targeted deep-debt pass addressing the four actionable findings from a
full codebase audit: one over-threshold file, commented-out dead code in 4 files,
a pre-existing signature verification bug in lineage proofs, and a placeholder
documentation gap.

## Changes

### 1. `method_gate.rs` smart refactor (811 → 425 LOC)

- Test suite (389 LOC, 55 tests) extracted to `method_gate_tests.rs` via
  `#[cfg(test)] #[path = "method_gate_tests.rs"] mod tests;`.
- Production module is now 425 lines — well under the 800-line threshold.
- Zero logic changes; all 55 tests pass unchanged.

### 2. Lineage proof signature verification bug fix

- **Root cause**: `sign_relationship()` included `timestamp_millis()` in the signed
  message, but `verify_relationship()` omitted it. The two functions produced
  different messages, so verification always failed. This was the reason the
  `verify_relationship()` call in `verify_proof()` was commented out.
- **Fix**: Extracted `relationship_message()` canonical builder that produces the
  same byte sequence for both signing and verification, using `established_at` from
  the `LineageRelationship` as the shared timestamp.
- **Impact**: `verify_proof()` now performs real Ed25519 signature verification.
  3 previously-failing tests now pass (49 total lineage tests green).

### 3. Commented-out code removal (4 files)

| File | What was removed | What replaced it |
|------|-----------------|------------------|
| `lineage_proof.rs` | 6-line commented `verify_relationship` call | Real verification + failure handling |
| `implementations.rs` | Dead `interval_seconds`/`retention_hours` assignments | Clean `monitoring.enabled = true` |
| `monitoring_migration.rs` | Phantom extraction + empty "would implement" stubs | `tracing::debug!` honest logging |
| `safe_device_detection.rs` | Inline JNI pseudocode comments | Doc comment on function |

### 4. `LockFreeQueue<T>` placeholder documentation

- Doc comment updated to explain capacity-only shape contract.
- `#[allow(dead_code)]` retains explicit `reason` string.

## Files

### New
- `crates/beardog-tunnel/src/method_gate_tests.rs` (389 LOC)

### Modified
- `crates/beardog-tunnel/src/method_gate.rs` (811 → 425 LOC)
- `crates/beardog-genetics/src/birdsong/lineage_proof.rs`
- `crates/beardog-genetics/src/birdsong/lineage_chain.rs`
- `crates/beardog-types/src/canonical/config/unified/implementations.rs`
- `crates/beardog-types/src/canonical/config/monitoring_migration.rs`
- `crates/beardog-tunnel/src/tunnel/hsm/android_strongbox/safe_device_detection.rs`
- `crates/beardog-utils/src/ultimate_performance.rs`
- `STATUS.md`, `CHANGELOG.md`

## Test Results

- **beardog-tunnel**: 55 method_gate tests pass
- **beardog-genetics**: 49 lineage tests pass (3 previously failing now fixed)
- **beardog-types**: 32 monitoring_migration tests pass
- **Clippy**: Clean across all 4 affected crates

## Audit Findings (for primalSpring reference)

The full audit also confirmed these positives:
- **0 `unsafe` blocks** in production — `#![forbid(unsafe_code)]` workspace-wide
- **0 `todo!()` or `unimplemented!()`** in production code
- **0 `Box<dyn Error>`** in production code
- **0 files over 800 LOC** after this wave
- **FIDO2/mobile HSM stubs** use `BearDogError::not_implemented()` / `not_yet_available()` — honest typed errors, not mocks
- **Discovery stubs** return empty with clear logging — correct for runtime discovery
- **`biomeos` references** are ecosystem namespace prefixes, not hardcoded primal names
