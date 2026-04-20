# Songbird v0.2.1 Wave 149 — Comprehensive Deep Debt Pass

**Date**: April 20, 2026
**Version**: v0.2.1-wave149
**Trigger**: Scheduled deep debt audit + primalSpring v0.9.16 audit follow-up

---

## Summary

Wave 149 resolves 6 categories of deep debt identified by a full-workspace audit:

| Category | Scope | Impact |
|----------|-------|--------|
| Blanket lint suppression | 11 files in `songbird-discovery/src/abstraction/` | 57 clippy issues fixed |
| Hardcoded paths | 3 files, 3 new constants | `/var/run/songbird`, `/run/user/{uid}`, `/var/tmp` |
| Duplicate constants | 3 config files | Re-export from `songbird-types::constants` |
| Mock feature naming | 2 crates, 29 cfg references | `test-utils`/`testing` → `test-mocks` |
| Stale CLI features | 1 file | 5 undeclared feature refs removed |
| Production `expect()` | 3 files | Reason strings added |

## What Was Clean (no action needed)

- 0 `unsafe` keyword usage
- 0 `async-trait` crate usage
- 0 `todo!()`/`unimplemented!()` in production
- 0 files over 800 lines
- 0 production mocks (post-Wave 147)

## Remaining `dyn` Dispatch (35 lines — architectural)

The discovery trait (`DiscoveryProvider`) uses `Pin<Box<dyn Stream>>` return
types and `as_any()` → `&dyn Any`. Eliminating these requires an enum Stream
return type, which is a larger architectural change. The adapters already use
an enum dispatch pattern (`DiscoveryAdapter`), so the `dyn` is contained to
trait boundaries. This is tracked but not urgent.

## Verification

- `cargo check --workspace` — PASS
- `cargo clippy --workspace -- -D warnings` — PASS (0 warnings)
- `cargo fmt --all --check` — PASS
- `cargo deny check` — PASS
- `cargo test --workspace --lib` — **7,377 passed**, 0 failed
