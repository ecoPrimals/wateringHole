<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.2.0-dev — Build Independence (GAP-28 resolved)

**From**: skunkBat team
**Date**: April 30, 2026
**Triggered by**: primalSpring Phase 56c — GAP-28 audit, genomeBin distribution blocker
**Ref**: `primalSpring/docs/PRIMAL_GAPS.md` GAP-28

---

## Summary

skunkBat was the only primal (out of 13) with a build-time path dependency on
`sourDough`. This handoff resolves GAP-28 by internalizing the consumed
`sourdough-core` types, making skunkBat fully standalone for plasmidBin /
genomeBin CI/CD distribution.

## What Changed

### sourdough-core → primal_foundation internalization

**Problem**: `sourdough-core = { path = "../sourDough/crates/sourdough-core" }`
in workspace `Cargo.toml` required sourDough to be cloned as a sibling for any
build. This made skunkBat the only primal blocked from standalone CI.

**Resolution**:
- Created `skunk-bat-core/src/primal_foundation/` with 6 files:
  - `mod.rs` — module root with re-exports
  - `lifecycle.rs` — `PrimalLifecycle`, `PrimalState` (from sourdough-core)
  - `error.rs` — `PrimalError`, `PrimalResult` (from sourdough-core)
  - `health.rs` — `PrimalHealth`, `HealthReport`, `HealthStatus`, `DependencyHealth` (from sourdough-core)
  - `config.rs` — `CommonConfig` (from sourdough-core)
  - `types.rs` — `Timestamp` (from sourdough-core)
- Replaced `blake3`-based instance ID with `std::hash::DefaultHasher` (no crypto dep needed for disambiguation)
- All types re-exported from `skunk_bat_core` — external API unchanged
- Removed `sourdough-core` from workspace, core, and server `Cargo.toml`
- Rewired **30 call sites** across crates, tests, and examples

### Import path mapping

| Before | After |
|--------|-------|
| `use sourdough_core::PrimalLifecycle` | `use skunk_bat_core::PrimalLifecycle` |
| `use sourdough_core::PrimalHealth` | `use skunk_bat_core::PrimalHealth` |
| `use sourdough_core::{PrimalError, PrimalState}` | `use skunk_bat_core::{PrimalError, PrimalState}` |
| `use sourdough_core::config::CommonConfig` | `use skunk_bat_core::CommonConfig` (or `crate::primal_foundation::config::CommonConfig` internally) |
| `use sourdough_core::health::{HealthReport, HealthStatus}` | `use skunk_bat_core::{HealthReport, HealthStatus}` |

### Dependency tree impact

Removing sourdough-core eliminated its entire transitive chain:
- `blake3`, `cc` (build dep)
- `tarpc`, `opentelemetry`, `opentelemetry_sdk`
- `serde_bytes`, `toml`, `bytes` (sourdough-core's own deps)
- `proptest` (dev)

### deny.toml cleanup

- Removed stale `RUSTSEC-2024-0387` advisory ignore (tarpc → opentelemetry_api)
- Removed `blake3` wrapper from `cc` ban (blake3 gone)
- Removed `opentelemetry_sdk` wrapper from `async-trait` ban
- All bans now have zero wrappers — strictest possible

### CI workflow

Already lean (single-job quality gate). No sourDough checkout steps needed.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 178 | **205** |
| Source files | 30 | **36** |
| Total lines | 6,749 | **7,710** |
| Largest file | 623 L | 623 L (unchanged) |
| Cross-repo path deps | 1 (`sourdough-core`) | **0** |
| Transitive crate count | ~120 | **~40** (est.) |
| cargo check (cold) | ~8s | **~5s** |
| cargo deny advisories | 1 ignored | **0 ignored** |

## Verification

- `cargo check --workspace` — CLEAN (builds without sourDough on disk)
- `cargo fmt --check` — CLEAN
- `cargo clippy --all-targets -- -D warnings` — CLEAN
- `cargo test --workspace` — 205 passed, 15 ignored
- `cargo deny check` — all ok (advisories, bans, licenses, sources)
- `cargo doc --no-deps` — CLEAN

## Action Items for Other Teams

1. **plasmidBin**: Remove `needs_sibling = "ecoPrimals/sourDough"` from `sources.toml`
   skunkBat entry. Build is now fully standalone.
2. **genomeBin**: skunkBat is ready for standard build + distribution. First
   `v0.2.0` tag will trigger the release pipeline.
3. **primalSpring**: GAP-28 can be marked **RESOLVED**.

## Remaining (LOW priority)

1. **First release tag**: Push `v0.2.0` tag to trigger plasmidBin harvest
2. **PeekedStream convergence**: Consolidate with BearDog impl (shared crate, not sourdough-core)
3. **Thymic selection implementation**: Design spec complete; awaits BearDog capability discovery
4. **Composable primitives IPC registration**: Blocked on biomeOS Neural API

---

*Next handoff: after `v0.2.0` tag + genomeBin harvest, or next evolution cycle.*
