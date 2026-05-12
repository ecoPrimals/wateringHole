# NestGate v4.7.0 — Doc Cleanup & Debris Audit

**Date**: April 4, 2026
**Scope**: Root doc refresh, stale reference cleanup, debris audit, pre-commit fix
**Verification**: Clippy CLEAN, fmt PASS, 12,085 tests (0 failures, ~468 ignored)

---

## Changes

### Root documentation refresh

All 11 root docs + 3 supplementary docs updated:
- **Dates**: April 3 → April 4, 2026 across STATUS, README, START_HERE, QUICK_START, QUICK_REFERENCE, CONTRIBUTING, CONTEXT, DOCUMENTATION_INDEX, CAPABILITY_MAPPINGS, tests/README, tests/DISABLED_TESTS_REFERENCE, specs/README, docs/operations/OPERATIONS_RUNBOOK
- **Ignored test count**: ~471 → ~468 (actual measured)
- **STATUS.md serial tests**: Updated to reflect EnvSource injection (5 remaining, was ~36)
- **STATUS.md testing section**: Rewritten to document `EnvSource` / `MapEnv` / `ProcessEnv` pattern

### Stale reference cleanup

- **STATUS.md architecture diagram**: 24 → 23 workspace members; removed `nestgate-automation` line
- **README.md**: Removed `nestgate-automation` from crate tree listing
- **START_HERE.md**: Removed `nestgate-automation` from crate tree listing
- **CONTEXT.md**: Removed `nestgate-automation` from authoritative crate list
- **DOCUMENTATION_INDEX.md**: 24 → 23 workspace members, 22 → 21 crates
- **docs/architecture/ARCHITECTURE_OVERVIEW.md**: `nestgate-automation ✅` → `(nestgate-automation removed)`

### CHANGELOG

Added Session 25 entry documenting the full EnvSource injection work (was previously only a one-liner in Session 24).

### Pre-commit hook fix

- `.pre-commit-config.sh`: Fixed inverted clippy check logic (was grepping for empty output); removed `--test-threads=1` serialization

## Debris audit findings (documented, no action needed)

| Item | Status | Notes |
|------|--------|-------|
| `nestgate-automation/` directory | Fossil on disk | Not in workspace; 4,350 lines; retained per fossil policy |
| `production_placeholders.rs` (×2) | Legitimate | Real production code (reads /proc, calls ZFS CLI, returns 501/503) |
| `scripts/setup-test-substrate.sh` | Legitimate | Hardware test substrate setup |
| `uid.rs` "unsafe" grep hit | False positive | Matched doc comment showing old pattern; actual code is 100% safe |
| DEPRECATED markers (~90 across config/discovery) | Intentional | Guide users from primal-specific → capability-based APIs |
| `temp_env` (99 call sites, 38 files) | Known debt | Wrapped in closure isolation; none require `#[serial]`; future EnvSource migration wave |
| Primal name refs in tests | Acceptable | Per wateringHole, test fixtures may reference ecosystem primals |
| `BIOMEOS_SOCKET_DIR` refs | Protocol-level | Ecosystem socket directory convention, not primal coupling |

---

*Last Updated: April 4, 2026*
