# BearDog v0.9.0 — Wave 44: Documentation & Debris Cleanup Handoff

**Date**: April 13, 2026
**Primal**: BearDog
**Version**: 0.9.0
**Wave**: 44

---

## Summary

Root documentation cleanup, stale spec link repair, showcase fixture fixes, and production readiness notice update. All changes are documentation/config only — zero Rust code changes this wave.

---

## Changes

### Root Docs Aligned to Canonical Metrics

| File | What Changed |
|------|-------------|
| `ROADMAP.md` | 95→100 methods, 14,761→14,780+ tests, dates to April 13 |
| `START_HERE.md` | 95→100 methods, 14,761→14,780+ tests, 90%+→90.51% coverage, date |
| `CONTEXT.md` | 90%+→90.51% coverage |
| `SECURITY.md` | Date April 11→April 13 |

### Broken Spec Links Fixed (5)

| Spec File | Broken Link | Resolution |
|-----------|------------|------------|
| `specs/current/production/PRODUCTION_READINESS_SPECIFICATION.md` | `../../STATUS.md` (wrong depth) | `../../../STATUS.md` |
| `specs/current/security/ENTROPY_SECURITY_SPECIFICATION.md` | `./QUANTUM_RESISTANT_SECURITY_IMPLEMENTATION_2025.md` (nonexistent) | Marked as "(planned)" |
| `specs/current/security/TOR_CAPABILITY_SPECIFICATION.md` | `../../../TOR_PHASE2_EVOLUTION.md` (wrong path) | `../../../docs/references/TOR_PHASE2_EVOLUTION.md` |
| Same | `../../docs/BEARDOG_RPC_API.md` (nonexistent) | `../../../README.md` |
| Same | `../otherTeams/SONGBIRD_INTEGRATION.md` (wrong path) | `../integration/SONGBIRD_INTEGRATION_SPECIFICATION.md` |

### Showcase Fixes

- **`showcase/02-ecosystem-integration/01-songbird-btsp/Cargo.toml`**: Removed `features = ["btsp-api"]` — feature does not exist in `beardog-tunnel`.
- **`run-demo.sh`**: Replaced hardcoded `/home/eastgate/Development/ecoPrimals/songbird` with `$SONGBIRD_PATH` env var or relative discovery.

### Production Readiness Spec Updated

- Stale October 2025 accuracy notice (claiming 100 unsafe blocks, 80% ready, coverage unknown) replaced with April 2026 status reflecting current reality: zero unsafe, 14,780+ tests, 90.51% coverage.

---

## Quality Gates

All pre-existing gates remain clean (no Rust changes this wave):
- `cargo fmt --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 14,780+ tests passing

---

## Files Modified

- `ROADMAP.md`, `START_HERE.md`, `CONTEXT.md`, `SECURITY.md` — metric alignment
- `CHANGELOG.md`, `STATUS.md` — Wave 44 entry
- `specs/current/production/PRODUCTION_READINESS_SPECIFICATION.md` — link fix + notice update
- `specs/current/security/ENTROPY_SECURITY_SPECIFICATION.md` — dead link fix
- `specs/current/security/TOR_CAPABILITY_SPECIFICATION.md` — 3 link fixes
- `showcase/02-ecosystem-integration/01-songbird-btsp/Cargo.toml` — stale feature removed
- `showcase/02-ecosystem-integration/01-songbird-btsp/run-demo.sh` — hardcoded path eliminated
