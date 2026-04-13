# biomeOS v3.03 — Deep Debt Cleanup VI Handoff

**Date**: April 11, 2026
**Primal**: biomeOS
**Scope**: Error type evolution, lint attribute modernization, hot-path performance

---

## Executive Summary

biomeOS v3.03 completes a deep debt cleanup pass across 128 files:

1. **`Box<dyn Error>` → `anyhow` evolution** — eliminates type-erased error boxing
2. **`#[allow(` → `#[expect(` migration** — 119 test files with documented reasons
3. **Hot-path clone elimination** — `dispatch()` takes owned `Value`, zero clones on success

---

## Changes

### Error Type Evolution

| File | Before | After |
|------|--------|-------|
| `biomeos-api/handlers/topology.rs` | `Result<..., Box<dyn std::error::Error + Send + Sync>>` | `anyhow::Result<...>` |
| `biomeos-boot/init_error.rs` | `HardwareDetection(Box<dyn Error + Send + Sync>)` | `HardwareDetection(anyhow::Error)` |
| `biomeos-boot/init_error.rs` | `NetworkConfig(Box<dyn Error + Send + Sync>)` | `NetworkConfig(anyhow::Error)` |
| `biomeos-boot/init_hardware.rs` | `Box::new(e)` | `e.into()` |
| `biomeos-boot/init_network.rs` | `Box::new(e)` | `e.into()` |

### Lint Attribute Modernization

- **119 test files**: `#![allow(clippy::unwrap_used, clippy::expect_used)]` → `#![expect(clippy::unwrap_used, clippy::expect_used, reason = "test assertions")]`
- **Exception**: `biomeos-test-utils/src/lib.rs` retains `#[allow(` — crate-level library `#[expect]` would trigger unfulfilled-expect warnings when lints aren't active in all code paths
- **All** `#[expect(` attributes now include `reason = "..."` documentation

### Hot-Path Performance

- `dispatch()` in `neural_api_server/routing.rs`: signature changed from `id: &Value` to `id: Value`
- Eliminates **one `Value::clone()` per successful JSON-RPC request** (most common code path)
- Error paths use move semantics (mutually exclusive branches eliminate all remaining clones)
- 50+ dispatch call sites + 2 test call sites updated

---

## Quality Gates

| Metric | Value |
|--------|-------|
| Tests | 7,749 (0 failures) |
| Clippy | PASS (0 warnings, pedantic+nursery, `-D warnings`) |
| Unsafe | 0 production |
| `#[allow(` in production | 0 |
| `#[allow(` in test utils | 1 (intentional, documented) |
| Files changed | 128 |

---

## Impact on Downstream

- **Springs**: No wire-level changes. Internal optimization only.
- **Squirrel/neuralSpring**: No API changes from v3.02 inference wire.
- **primalSpring**: `ECOSYSTEM_COMPLIANCE_MATRIX.md` updated to v2.10.0 reflecting v3.03.

---

## Archived Handoffs

7 biomeOS v2.x handoffs (v2.90–v2.99) moved to `handoffs/archive/` — superseded by v3.x series.
