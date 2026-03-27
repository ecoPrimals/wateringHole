# barraCuda v0.3.5 — Documentation Cleanup & Debris Removal Handoff

**Date**: 2026-03-13
**From**: barraCuda
**Type**: Maintenance — doc cleanup, count correction, debris removal

---

## Summary

Systematic cleanup of all barraCuda root docs, specs, and scripts to correct
stale counts, update dates, and remove 165+ lines of duplicated historical
content that already lives in `CHANGELOG.md`.

## Changes

### Count Corrections (verified against codebase)

| Metric | Old (stale) | New (verified) |
|--------|-------------|----------------|
| Total tests | 3,698 | 3,415 (3,346 lib + 69 core) |
| .rs files | 1,062 | 1,064 |
| SPDX headers | 1,062/1,062 | 1,064/1,064 |
| WGSL shaders | 806 | 806 (unchanged) |

### Date Updates to March 13

- `STATUS.md`, `SPRING_ABSORPTION.md`, `WHATS_NEXT.md`
- `specs/BARRACUDA_SPECIFICATION.md`, `specs/ARCHITECTURE_DEMARCATION.md`,
  `specs/REMAINING_WORK.md`, `specs/PRECISION_TIERS_SPECIFICATION.md`
- `crates/barracuda/src/shaders/README.md`, `crates/barracuda/src/shaders/CATEGORIES.md`

### Priority Correction

- `STATUS.md`: Kokkos validation baseline documentation moved from P2 to P1
  (aligned with `WHATS_NEXT.md` after VFIO strategy unblocked it)

### Debris Removal

- **`WHATS_NEXT.md`**: Trimmed from 346 → 163 lines. Removed 183 lines of
  historical "Recently Completed" entries (Mar 7–10) that duplicated
  `CHANGELOG.md`. Kept only Mar 11–13 completions with pointer to CHANGELOG.
- **`specs/REMAINING_WORK.md`**: 14 "Achieved" sprint sections (275 lines)
  wrapped in `<details>` collapse with summary. Added 12-line consolidated
  achievement summary at top.
- **`scripts/test-tiered.sh`**: Updated stale test counts in comments.

### Debris Audit (no issues found)

- No `.bak`, `.orig`, `.tmp`, or `~` files in repo
- No empty tracked files
- No orphaned directories
- `Cargo.lock` correctly tracked (binary workspace)
- `.gitignore` covers all build artifacts
- `showcase/` demos clean (only source files tracked)
- Single script (`test-tiered.sh`) — well-structured, no debris

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -D warnings` | Pass |
| No code changes | Documentation and comments only |

## Files Modified

11 files: `README.md`, `SPRING_ABSORPTION.md`, `STATUS.md`, `WHATS_NEXT.md`,
`crates/barracuda/src/shaders/CATEGORIES.md`,
`crates/barracuda/src/shaders/README.md`, `scripts/test-tiered.sh`,
`specs/ARCHITECTURE_DEMARCATION.md`, `specs/BARRACUDA_SPECIFICATION.md`,
`specs/PRECISION_TIERS_SPECIFICATION.md`, `specs/REMAINING_WORK.md`

Net: -165 lines (45 added, 210 removed)
