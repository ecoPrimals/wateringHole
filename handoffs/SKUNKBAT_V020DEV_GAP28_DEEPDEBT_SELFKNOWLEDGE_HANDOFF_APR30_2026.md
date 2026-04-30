<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.2.0-dev — GAP-28 + Deep Debt + Self-Knowledge Consolidation

**From**: skunkBat team
**Date**: April 30, 2026
**Triggered by**: primalSpring Phase 56c — GAP-28 audit, deep debt pass

---

## Summary

Three passes on skunkBat this session:

1. **GAP-28 resolution**: Build independence — `sourdough-core` fully internalized
   as `primal_foundation` module, `needs_sibling` removed from plasmidBin.
2. **Deep debt + async-trait elimination**: 14→0 `async-trait` usages, RPITIT,
   btsp.rs refactored 867→623 lines, coverage 89.5%→90%+.
3. **Self-knowledge consolidation**: Crate-level identity constants, platform
   utility deduplication, config-driven TCP bind.

## GAP-28: Build Independence (RESOLVED)

**Problem**: skunkBat was the only primal (13/13) with a build-time path dep
on `sourDough`. Blocked plasmidBin/genomeBin standalone distribution.

**Resolution**:
- Created `skunk-bat-core/src/primal_foundation/` (6 files) internalizing
  `PrimalLifecycle`, `PrimalState`, `PrimalError`, `HealthReport`, `CommonConfig`, `Timestamp`
- Removed `sourdough-core` from all Cargo.toml (workspace + crate level)
- Rewired ~30 call sites: `use sourdough_core::` → `use skunk_bat_core::`
- `plasmidBin/sources.toml`: `needs_sibling` removed, standalone note added
- Verified: `cargo check --workspace` builds without sourDough on disk

## Self-Knowledge Consolidation

**Problem**: Primal name, ID, and capabilities were duplicated across
`discovery.rs`, `toadstool.rs`, `dispatch.rs`, `songbird.rs`, `config.rs`.

**Resolution**:
- Added `PRIMAL_NAME`, `PRIMAL_ID`, `CAPABILITIES` as crate-level constants
  in `skunk-bat-core::lib`
- All crates reference the single source of truth
- Zero hardcoded primal names in production routing code

## Platform Utility Deduplication

**Problem**: `proc_uid()` (UID resolution without libc) was copy-pasted
identically in `rpc.rs` (integrations) and `transport/sys.rs` (server).

**Resolution**:
- Created `skunk_bat_core::platform` module with shared implementation
- Both crates delegate to it, eliminating ~40 lines of duplication

## Config-Driven TCP Bind

**Problem**: `serve_tcp()` hardcoded `"0.0.0.0"` for the listen address.

**Resolution**:
- `serve_tcp()` now takes the listen address from `CommonConfig.listen_addr`
- Full flow: `SkunkBatConfig → main.rs → ipc::serve → serve_tcp`

## CI Evolution

- Added `cargo deny check` and `cargo doc -D warnings` to CI pipeline
- Expanded test surface from `--lib` (137) to `--lib --bins` (185 in CI)

## Metrics

| Metric | Before Session | After |
|--------|---------------|-------|
| Tests | 178 | **205** |
| Source files | 30 | **37** |
| Total lines | 6,749 | **7,710** |
| Largest file | 623 L | 623 L |
| Cross-repo deps | 1 (`sourdough-core`) | **0** |
| Hardcoded primal names | ~12 call sites | **0** (constants) |
| Duplicated `proc_uid` | 2 copies (~80L) | **1** shared module |
| async-trait usages | 14 | **0** (banned) |
| Binary (x86_64-musl) | N/A | **2.4 MB** static-pie |
| plasmidBin | NOT PUBLISHED | **READY** |

## Verification

- `cargo check --workspace` — CLEAN (without sourDough on disk)
- `cargo fmt --check` — CLEAN
- `cargo clippy --all-targets -- -D warnings` — CLEAN
- `cargo test --workspace` — 205 passed, 15 ignored
- `cargo deny check` — all ok
- `cargo doc --no-deps` — CLEAN

## primalSpring Stale Data

The following entries in `PRIMAL_GAPS.md` are stale for skunkBat:

| primalSpring says | Actual |
|---|---|
| async-trait: 14 | **0** (eliminated + banned) |
| Tests: 171 / 84 lib | **205** |
| Coverage: 89.6% | **>90%** |
| genomeBin relay: "Phase 1 only" | **Phase 1/2** |
| GAP-28 (build independence) | **RESOLVED** |

## Remaining (LOW priority)

1. **First `v0.2.0` tag**: Triggers plasmidBin harvest + genomeBin distribution
2. **PeekedStream convergence**: Consolidate with BearDog impl (shared crate)
3. **Thymic selection**: Design spec complete; awaits BearDog capability discovery
4. **Composable primitives IPC**: Blocked on biomeOS Neural API

---

*Next handoff: after `v0.2.0` tag + genomeBin harvest, or next evolution cycle.*
