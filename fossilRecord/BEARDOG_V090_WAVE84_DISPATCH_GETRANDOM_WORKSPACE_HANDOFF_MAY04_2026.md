<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 84 Handoff

**Date**: May 4, 2026
**Branch**: `main`
**Trigger**: Continuous deep debt pass

---

## Summary

Wave 84 addresses three performance/hygiene debt items identified in a fresh audit:

### 1. O(1) JSON-RPC Method Dispatch

`HandlerRegistry` now builds a `HashMap<&'static str, usize>` at init (Phase 3 of
construction) mapping every registered method name to its handler index.
`route()` performs O(1) lookup instead of iterating all handlers and calling
`.methods().contains()` per handler (was O(n * m) where n = handlers, m = methods per handler).

**Files changed**: `crates/beardog-tunnel/src/unix_socket_ipc/handlers/mod.rs`

### 2. `getrandom` 0.2 → 0.3

Workspace pin upgraded to align with `rand 0.9` / `rand_core 0.9` (which depend on
`getrandom 0.3`). Eliminates duplicate `getrandom` major versions in the dependency tree.
4 call sites in `software_hsm_impl.rs` migrated from `getrandom::getrandom()` to
`getrandom::fill()`.

**Files changed**: `Cargo.toml` (workspace pin), `crates/beardog-types/src/canonical/discovery/software_hsm_impl.rs`

### 3. Workspace Dependency Hygiene

- 5 internal crates migrated from `path = "../..."` to `{ workspace = true }`:
  `beardog-threat`, `beardog-compliance`, `beardog-workflows`, `beardog-production`,
  `beardog-node-registry`
- 3 zero-consumer entries removed from `[workspace.dependencies]`:
  `beardog-deploy`, `beardog-installer`, `beardog-client`

**Files changed**: Root `Cargo.toml`, `crates/beardog/Cargo.toml`, `crates/beardog-core/Cargo.toml`,
`crates/beardog-security/Cargo.toml`, `crates/beardog-tunnel/Cargo.toml`

---

## CI Results

| Gate | Result |
|------|--------|
| `cargo fmt -- --check` | Clean |
| `cargo clippy --workspace` | 0 warnings |
| `cargo test --workspace --lib` | 12,610 passed, 0 failed |

---

## Downstream Impact

- **primalSpring / all springs**: No wire protocol or method naming changes. Dispatch is faster
  but functionally identical.
- **plasmidBin**: Next binary harvest will include the `getrandom` 0.3 alignment, reducing
  transitive dep tree weight slightly.
- **No breaking changes**.
