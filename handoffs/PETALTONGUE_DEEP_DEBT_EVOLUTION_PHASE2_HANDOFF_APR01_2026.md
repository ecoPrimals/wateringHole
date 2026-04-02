# petalTongue Deep Debt Evolution Phase 2 Handoff

**Date**: April 1, 2026
**Phase**: Idiomatic Rust evolution, build optimizations, structural refactoring
**Previous**: `PETALTONGUE_DEEP_DEBT_EVOLUTION_HANDOFF_APR01_2026.md` (→ fossilRecord)

---

## Summary

Comprehensive deep-debt evolution across petalTongue. Modernized lint
suppression idioms, added compiler optimizations, deduplicated constants,
refactored large files, eliminated unnecessary allocations, and reconciled
all documentation with IPC Protocol v3.1.

---

## Changes

### `#[allow]` → `#[expect]` Migration (23 production attrs)

Migrated all production `#[allow(...)]` to `#[expect(..., reason = "...")]`.
This immediately revealed and eliminated **7 unnecessary suppressions**:
- `clippy::missing_errors_doc` and `clippy::missing_panics_doc` on `petal-tongue-graph` (lints not firing)
- `clippy::cast_sign_loss` on `system_monitor_integration` (not firing)
- `unexpected_cfgs` on `human_entropy_window` state/rendering (not firing)
- `dead_code` on `primal_panel::last_refresh` (field IS used)
- `unused_imports` on `mdns_provider` packet re-export (moved to `#[cfg(test)]`)

### Build & CI Optimizations

- **`.cargo/config.toml`**: LTO thin, `codegen-units = 1`, strip for release; dev deps `opt-level = 2`
- **CI `--all-features`**: `clippy`, `doc`, and `test` steps now exercise all feature gates

### Constants.rs Smart Refactoring (818 → 794 lines)

Added typed env-parsing helpers (`env_or<T>`, `env_duration_secs`, `env_duration_ms`)
that replaced 15+ repetitive `std::env::var(...).ok().and_then(parse).unwrap_or(DEFAULT)`
patterns. Consolidated duplicate WS URL builders into `ws_url(path)`. All 39 constants
tests pass.

### Device Panel Test Deduplication (849 → 799 lines)

Added `make_device()` / `make_device_assigned()` test helpers, replacing 21 verbose
7-line `Device { ... }` struct literals. 19 tests pass.

### Zero-Copy / Allocation Elimination

IPC interaction handlers (`handle_subscribe`, `handle_poll`, `handle_unsubscribe`,
`handle_sensor_stream_unsubscribe`, `handle_sensor_stream_poll`) evolved from
`as_str().to_string()` (allocates) to `as_str()` (`&str` binding, zero allocation).

**Analysis confirmed `Cow<str>` not worth complexity**: tarpc uses bincode (no
zero-copy benefit), `PrimalId` already uses `Arc<str>`, most IPC DTOs are short-lived.

### IPC Protocol v3.1 Documentation Reconciliation

Corrected "tarpc PRIMARY" → "JSON-RPC 2.0 REQUIRED, tarpc MAY" in:
- Root `Cargo.toml` workspace dependency comment
- `petal-tongue-api/src/lib.rs` crate docs
- `README.md` architecture section and contributing guide
- `START_HERE.md` architecture rules

### Root Documentation Updates

- Test counts: 5,845+ → 5,987+
- Clippy description: "zero blanket `#[allow]`" → "zero `#[allow]` in production"
- `manifest.toml` already correct (`primary = "json-rpc"`)

### Mock Mode Analysis

Production mock_mode is already properly gated: `#[cfg(not(any(test, feature = "test-fixtures")))]`
returns `Err(MockModeUnavailable)`. No evolution needed — documented as intentional.

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | Zero warnings |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace --all-features` | 5,987+ tests, 0 failures |
| TODO/FIXME/HACK/XXX in production | Zero |
| `todo!()` / `unimplemented!()` | Zero |
| Stale scripts/temp files | Zero |
| All files under 1,000 lines | Yes (largest: 852) |

---

## Codebase Health Snapshot

- **Production `#[allow]`**: Zero (all migrated to `#[expect]` with documented reasons)
- **Production `.unwrap()`**: Zero (only 1 `.expect()` in retry.rs with invariant message)
- **Production `println!`**: All intentional CLI user-facing output
- **Hardcoded ports/names**: All env-overridable via `env_or<T>` pattern
- **Mock mode**: Production builds reject with typed error

---

## Deferred (from prior session, now resolved or triaged)

| Item | Resolution |
|------|-----------|
| `Cow<'_, str>` for IPC params | Not worth complexity — `&str` optimizations applied instead |
| CI `--all-features` | ✅ Done |
| `.cargo/config.toml` | ✅ Done |
| `with_mock_mode` audit | Documented as intentional; properly gated |
| Test-module extraction | Not needed — all files under 1,000 lines |
| `#[allow]` → `#[expect]` | ✅ Done — 7 unnecessary suppressions eliminated |

---

## Not Changed (intentional)

- **`#![expect(missing_docs)]`** on 4 crates: 492 items to document incrementally; `expect` is the modern Rust idiom
- **`archive/`**: 485+ files of fossil record — ecosystem policy to preserve
- **println!/eprintln!**: All CLI user output — correct usage
- **primal_names module**: Used for logging/filtering only, never routing

---

## Ecosystem Impact

- **All primals** benefit from CI `--all-features` pattern (catches hidden feature-gate bugs)
- **Release binaries** benefit from LTO thin + codegen-units 1 + strip
- **IPC Protocol v3.1** documentation now consistent across all petalTongue surfaces
- **`#[expect]`** pattern demonstrates how to surface stale suppressions automatically
