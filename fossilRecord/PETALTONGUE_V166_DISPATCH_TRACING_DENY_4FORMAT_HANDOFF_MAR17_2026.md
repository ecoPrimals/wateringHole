# petalTongue v1.6.6 — DispatchOutcome, Structured Tracing, deny.toml, 4-Format Capabilities

**Date**: March 17, 2026
**Primal**: petalTongue v1.6.6
**Session**: Second ecosystem absorption pass — springs V112-V125, primals I52-S157b
**Status**: Complete — all checks pass

---

## Executive Summary

Second absorption pass after pulling fresh handoffs from all 7 springs and 10+ primals. Identified 5 remaining convergence gaps and executed all.

**Tests**: 5,447 → 5,459 (+12 new tests)
**All checks pass**: fmt, clippy, test, cargo-deny

---

## What Was Absorbed

### P1 — High Priority

#### 1. `DispatchOutcome<T>` dispatch classification
- **Source**: groundSpring V112, loamSpine V093, sweetGrass V0719
- Added to `petal-tongue-ipc/src/ipc_errors.rs`
- `Ok(T)`, `ProtocolError { code, message }`, `ApplicationError { code, message }`
- Methods: `is_ok()`, `is_protocol_error()`, `is_application_error()`, `is_method_not_found()`

#### 2. `eprintln!` → `tracing::error!` in binary entry points
- **Source**: healthSpring V32, neuralSpring V110
- Migrated 6 calls across `petal-tongue-headless/src/main.rs` and `petal-tongue-ui/src/headless_main.rs`
- Updated e2e tests to check stdout (tracing output) instead of stderr
- `or_exit.rs` intentionally kept as `eprintln!` (pre-tracing-init)

#### 3. `deny.toml` hardening
- **Source**: rhizoCrypt S16, neuralSpring V110, coralReef I52
- Added `yanked = "deny"` to advisories
- Upgraded `wildcards` from `"allow"` to `"warn"` (can't deny workspace path deps)
- `cargo deny check` passes clean

### P2 — Medium Priority

#### 4. 4-format capability parsing
- **Source**: airSpring V087 (formats A/B/C/D)
- Enhanced `capability_parse.rs` with `parse_capabilities_from_response()`
- Format A: flat string array
- Format B: enriched objects (name/capability/id keys)
- Format C: double-nested `{"capabilities": {"list": [...]}}`
- Format D: result-wrapped `{"result": {"capabilities": [...]}}`
- Added `id` key support (coralReef `CapabilityRef` pattern)
- 7 new tests for response-level parsing

#### 5. `exit_code` module
- **Source**: sweetGrass V0719
- `SUCCESS` (0), `GENERAL_ERROR` (1), `CONFIG_ERROR` (2), `NETWORK_ERROR` (3), `USAGE_ERROR` (64)

---

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-features --all-targets -- -D warnings` | **PASS** |
| `cargo test --all-features --workspace` | **PASS** (5,459 passed, 0 failed) |
| `cargo deny check` | **PASS** (advisories, bans, licenses, sources all ok) |
| All files < 1000 lines | **PASS** |

---

**License**: AGPL-3.0-or-later
