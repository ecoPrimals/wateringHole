# NestGate Deep Debt Audit — Session 38 Handoff

**Date:** April 8, 2026
**Primal:** NestGate
**Session:** 38
**Commit:** 0c4c1282

---

## Summary

Comprehensive deep debt audit across 8 categories. All production code verified clean
for unsafe, unwrap, todo, FIXME, thread::sleep, block_on. Actionable items fixed.

## Audit Results (clean — no action needed)

| Category | Result |
|----------|--------|
| Production files >800L | Zero (all 4 files >800L are test-only) |
| `#![forbid(unsafe_code)]` | Present on all crate roots |
| `unsafe` in production | Zero |
| `.unwrap()` in production | Zero |
| `todo!()` / `FIXME` / `HACK` | Zero (only in doc examples) |
| `thread::sleep` / `block_on` | Zero |
| Feature-gated mocks | Properly isolated (`dev-stubs`, `mock-metrics`) |

## Changes Made

### 1. ZFS silent-success catch-all (safety fix)

`ZfsRequestHandler::handle_zfs_request` had a wildcard `_ =>` arm returning
`Success` for unimplemented mutating operations (PoolCreate/Destroy, DatasetCreate/Destroy,
SnapshotCreate/Destroy). Callers could believe a pool was destroyed when nothing happened.

**Fix:** Each unimplemented variant now returns an explicit `Err` with guidance to use
the CLI directly.

### 2. `#[allow(dead_code)]` → `#[expect(dead_code)]`

RPC manager `mod.rs` and `types.rs` evolved from `#![allow(dead_code)]` to
`#![expect(dead_code, reason = "...")]`. The `expect` form will auto-warn when
scaffold fields get wired, preventing stale suppression.

### 3. Unused dependencies removed

- **`memmap2`**: In workspace deps, zero crate consumers → removed
- **`log`**: In workspace deps + nestgate-core Cargo.toml, zero imports → removed.
  `tracing` is the sole logging framework.
- **`temp-env`**: Root package duplicated the workspace definition with inline version → now uses `workspace = true`

### 4. Misleading "Mock mode" log

`tier_metrics.rs` logged "Mock mode: returning default performance stats" immediately
before running real `zfs` CLI calls. Stale from development iteration — removed.

### 5. Self-knowledge cleanup

| File | Change |
|------|--------|
| `nestgate-security/src/lib.rs` | Removed "bearDog" from crate docs |
| `infant_discovery_demo.rs` | Replaced "songBird" with "network capability" |
| `services_config.rs` | Replaced "songbird_url" reference with capability language |
| `services.rs` | Replaced "BearDog, custom, etc." with capability language |
| `discovery.rs` | Updated "placeholder" labels to accurate descriptions |

### 6. Pre-existing issues noted (not from this session)

- `nestgate-discovery` test code: `await_holding_lock` clippy warning (2 instances)
- `nestgate-zfs` test code: various unfulfilled `#[expect]` warnings (43 instances)
- `nestgate-observe` test code: pre-existing clippy issues
- 180 `#[deprecated]` markers: all intentional migration markers with active callers
- ~280 `unreachable_pub` warnings: `pub` items that could be `pub(crate)`

## Files Changed

| File | Change |
|------|--------|
| `Cargo.toml` | Remove `memmap2`, `log`; fix `temp-env` duplicate |
| `nestgate-core/Cargo.toml` | Remove `log` dep |
| `nestgate-api/src/rest/rpc/manager/mod.rs` | `#[allow]` → `#[expect]` |
| `nestgate-api/src/rest/rpc/manager/types.rs` | `#[allow]` → `#[expect]` |
| `nestgate-zfs/src/handlers.rs` | Replace catch-all with explicit errors |
| `nestgate-zfs/src/.../tier_metrics.rs` | Remove misleading mock log |
| `nestgate-security/src/lib.rs` | Self-knowledge cleanup |
| `nestgate-core/examples/infant_discovery_demo.rs` | Self-knowledge cleanup |
| `nestgate-config/.../services_config.rs` | Self-knowledge cleanup |
| `nestgate-config/.../services.rs` | Self-knowledge cleanup |
| `nestgate-storage/.../discovery.rs` | Stale label fix |
| `CHANGELOG.md` | Session 38 entry |

## Verification

```bash
cd code && cargo check --workspace   # clean
cd code && cargo test -p nestgate-zfs --lib -- handlers   # 6/6 pass
cd code && cargo test -p nestgate-api --lib -- rpc::manager   # 12/12 pass
```
