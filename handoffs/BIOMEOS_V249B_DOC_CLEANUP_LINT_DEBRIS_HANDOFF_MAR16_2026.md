# biomeOS v2.49b — Documentation Cleanup, Lint Hygiene, and Debris Removal

**Date**: March 16, 2026
**Session**: Root doc refresh, stale reference cleanup, vestigial lint removal
**Status**: Complete — 5,161 tests passing, 0 failures, 0 clippy warnings

---

## Summary

Post-v2.49 cleanup pass focusing on documentation accuracy, dead reference removal,
and lint hygiene evolution. Used `#[expect]` migration to discover 11 vestigial
`#[allow(clippy::collapsible_if)]` suppressions that were never triggered.

## Changes

### Root Documentation Updates (5 files)
- **README.md**: v2.48 → v2.49, 280+ → 285+ translations, 24 → 25 domains, 5,162+ → 5,161+, removed dead `docs/handoffs/` tree reference
- **START_HERE.md**: Same metric updates, fixed `docs/handoffs/` → `wateringHole/handoffs/`
- **QUICK_START.md**: Fixed `docs/handoffs/` path, updated test count
- **DOCUMENTATION.md**: v2.48 → v2.49, updated test count, version range
- **scripts/README.md**: Updated test count

### Dead Reference Cleanup (7 files)
- `CURRENT_STATUS.md`: 2 `docs/handoffs/` references → `ecoPrimals/wateringHole/handoffs/`
- `crates/biomeos-core/src/connection_strategy.rs`: Updated doc reference
- `crates/biomeos-cli/src/commands/spore.rs`: `harvest-primals.sh` → `cargo run -p biomeos-harvest`
- `crates/biomeos-spore/src/spore/filesystem.rs`: Same harvest script update
- `graphs/node_atomic_compute.toml`: `start_nucleus.sh` → `biomeos nucleus start`
- `graphs/nest_deploy.toml`: Same
- `livespore-usb/README.md`: 2 `start_nucleus.sh` references → `biomeos nucleus start`

### Systemd Service Fix
- `config/systemd/biomeos-beacon-dns.service`: Updated path from gitignored `archive/` to `scripts/`, added migration note

### Lint Hygiene (13 files)
- Attempted `#[allow(clippy::collapsible_if)]` → `#[expect]` migration across 11 production locations
- All 11 expectations were **unfulfilled** — lint was never triggered (workspace-level `collapsible_if = "allow"` in root Cargo.toml made them redundant)
- Removed all 11 vestigial suppressions entirely
- Removed redundant module-level `#![allow(clippy::collapsible_if)]` from `biomeos-cli/src/lib.rs`
- Evolved 2 `#[allow(deprecated)]` → `#[expect(deprecated)]` in `biomeos-primal-sdk` and `biomeos-core::p2p_coordination::adapters`

### Handoff Archive
- Moved 8 superseded Mar 15 handoffs to `wateringHole/handoffs/archive/`

## Audit Findings (No Action Needed)

| Finding | Result |
|---------|--------|
| TODO/FIXME/HACK/XXX in .rs files | 0 found |
| `unwrap()` in production code | 0 found |
| Build artifacts in git | None (target/ and archive/ are gitignored) |
| Orphan files or loose .rs | None |
| Stale TODOs | None |

## Known Items (Not Addressed — Future Work)

- 17 crates still on `edition = "2021"` (workspace default is 2024)
- Port 3492 hardcoded in livespore/pixel8a deployment scripts and configs
- STUN config `multi_tier.toml` duplicated across 4 deployment targets
- `CHANGELOG.md` and `specs/` retain `docs/handoffs/` references as fossil record

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 5,161 passing, 0 failures |
| Clippy | 0 warnings (entire workspace) |
| Vestigial lints removed | 12 |
| Dead references fixed | 11 |
| Files updated | 20 |
| Handoffs archived | 8 |
