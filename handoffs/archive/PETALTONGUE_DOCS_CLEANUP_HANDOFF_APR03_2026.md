# petalTongue Documentation Cleanup Handoff

**Date**: April 3, 2026
**Previous**: `PETALTONGUE_DEEP_DEBT_EVOLUTION_PHASE5_HANDOFF_APR03_2026.md`
**Commit**: `a5d9fc1`

---

## Summary

Root documentation cleanup, protocol wording reconciliation, stale var removal from
ENV_VARS.md, and debris cleanup. 12 files changed, 74 insertions, 140 deletions.

---

## Changes

### Root Documentation

| File | Changes |
|------|---------|
| `START_HERE.md` | Test count → 6,079+; module maps updated for phase 5 refactors (5 directory modules) |
| `README.md` | Test count → 6,079+ (was 5,952+); largest-module claim updated; spec note |
| `CHANGELOG.md` | Protocol wording reconciled to "JSON-RPC REQUIRED, tarpc MAY" |
| `Cargo.toml` | Migration-era comments neutralized (no dep changes) |

### ENV_VARS.md

**Removed** (no code readers found):
- `RUST_LOG_FILTER`, `PETALTONGUE_AUDIO_ENABLED`, `PETALTONGUE_MAX_FPS`
- `BINGOCUBE_PATH`, `SYSTEM_MONITOR_INTERVAL`, `PETALTONGUE_DEBUG_OVERLAY`
- `PETALTONGUE_TUTORIAL_ENDPOINT_*`

**Fixed**: `PETALTONGUE_REFRESH_INTERVAL` → `PETALTONGUE_REFRESH_INTERVAL_SECS`;
migration note `v1.6.7` → `v1.6.6`

**Added**: `BIOMEOS_NEURAL_API_SOCKET`, `PETALTONGUE_UI_BACKEND`,
`PETALTONGUE_ENABLE_MDNS`, `PETALTONGUE_TCP_BIND_HOST`

### Protocol Reconciliation

Canonical policy: **JSON-RPC 2.0 REQUIRED** for all cross-primal IPC;
**tarpc MAY** for Rust-to-Rust hot paths.

Updated in:
- `CHANGELOG.md` [1.6.6]
- `specs/COLLABORATIVE_INTELLIGENCE_INTEGRATION.md`
- `specs/UNIVERSAL_VISUALIZATION_PIPELINE.md`
- `specs/UNIVERSAL_USER_INTERFACE_SPECIFICATION.md` (songbird → discovery_client)

### Archive

- `PANEL_SYSTEM_EVOLUTION.md` → `archive/specs-archive/` (described "ad-hoc app.rs rendering" as current state; superseded by panel_registry)

### Debris

- `sandbox/scenarios/README.md`: doom count 5→4, date updated
- `crates/petal-tongue-tui/README.md`: fixed workspace example command
- `llvm-cov.toml`: fail-under 90→85 (aligned with CI 85% hard fail)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | **6,079 passing**, 0 failures |

---

## Session Summary (April 3, 2026)

Three commits this session, all pushed via SSH:

1. **`10dda54`** — Wave 99 capability-first compliance: removed 24 primal-specific
   env-var references, cleaned ~20 primal-name violations, completed PT-04/PT-06
2. **`aff8559`** — Deep debt elimination + smart refactoring: test-fixtures isolation,
   stub completions, timeout unification, 5 largest files refactored, dead code cleanup,
   version alignment (-1,985 net lines)
3. **`a5d9fc1`** — Documentation: root docs updated, ENV_VARS cleaned, protocol wording
   reconciled, stale spec archived, debris cleaned

**Net across session**: Zero unsafe code, zero clippy warnings, **6,079 tests passing**,
all crate versions aligned at 1.6.6.
