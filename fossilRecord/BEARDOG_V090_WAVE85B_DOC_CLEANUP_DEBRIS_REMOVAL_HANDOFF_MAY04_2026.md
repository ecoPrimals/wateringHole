<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 85b Handoff (Doc Cleanup & Debris Removal)

**Date**: May 4, 2026
**Branch**: `main`
**Trigger**: Periodic doc hygiene pass

---

## Summary

### Date Stamps Updated

All root docs, reference docs, and crate READMEs updated to May 4, 2026:
README.md, STATUS.md, ROADMAP.md, ARCHITECTURE.md, CONTEXT.md, START_HERE.md,
SECURITY.md, docs/README.md, docs/references/ROOT_INDEX.md,
docs/PRIMAL_CONTRACTS.md, docs/references/ENVIRONMENT_VARIABLES.md,
docs/references/QUICK_START_ZERO_HARDCODING.md

### Test Count Corrected

All docs updated from `14,800+` to `12,610` — the actual current count from
`cargo test --workspace --lib`. The decrease from prior counts reflects deep
debt passes that removed duplicate coverage tests, orphan test files, and
consolidated test modules.

### Debris Cleaned

- **beardog-tunnel/tests/README.md**: Fixed 3 broken doc links pointing to
  nonexistent files (`HARDWARE_SETUP.md`, `START_HERE_NOW.md`,
  `PHASE1_COMPLETE_SUCCESS.md`). Updated to current valid paths.
- **QUICK_START_ZERO_HARDCODING.md**: Removed stale `dns-sd` discovery mode
  (feature was removed in prior wave).
- **CONFIGURATION_MIGRATION.md**: Updated `WorkingUnifiedConfig` references
  to `SimplifiedBearDogConfig` (alias removed in Wave 85).
- **beardog-traits/README.md**: Removed stale "Week 3-4" migration timeline.
- **beardog-installer/README.md**: Updated "Phase 1 in progress" to
  "Scaffold complete".
- **PRIMAL_CONTRACTS.md**: Fixed contradictory footer date (was February 2026).

---

## Downstream Impact

No code changes. Documentation only.
