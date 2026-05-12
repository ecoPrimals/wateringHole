# Songbird v0.2.1 — Wave 129b: Root Doc Accuracy & Debris Cleanup

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 129b  
**Status**: Complete  
**Commits**: `011ac7a8` (Wave 129), `35cf8b84` (doc cleanup)

---

## Summary

Post-Wave 129 doc accuracy audit and debris cleanup. Very few issues found — codebase is clean.

## Fixes Applied

| Item | Fix |
|------|-----|
| Total Rust lines | ~427k → ~430k (1,587 files, measured) |
| REMAINING_WORK.md async-trait | "~90% require dyn" → "100% of remaining 109 verified Wave 129" (resolved contradiction with metrics table) |
| VALIDATION_EXECUTIVE_SUMMARY.md | Broken methodology link `../../methodology/` → `../methodology/` |
| README.md | Added `health-monitor.sh` to scripts section (was undocumented) |
| examples/future/ | `_beardog_host` → `_security_provider_host`, `_toadstool_host` → `_compute_provider_host` |

## Debris Audit — Clean

| Category | Status |
|----------|--------|
| `*.bak` / `*.orig` / temp files | None |
| Archive directories | None |
| Untracked files | None |
| `ai_tests.rs` (deleted Wave 129) | Confirmed gone |
| `parking_lot` in orchestrator Cargo.toml | Confirmed removed |

## Spec Link Status

| Link | Status |
|------|--------|
| `fossilRecord/` monorepo links | Valid (require full ecoPrimals checkout) |
| `VALIDATION_EXECUTIVE_SUMMARY.md` → methodology | Fixed |
| `VALIDATION_EXECUTIVE_SUMMARY.md` → experiment results | Fixed (Wave 127b) |
| `PRIMAL_COORDINATION_ARCHITECTURE.md` → crates | Fixed (Wave 127b) |

## Remaining Notes

- `specs/*.md` contain `TODO` in pseudocode/plan docs — these are roadmap items, not stale markers
- `deployment/graphs/tower_genome.toml` uses `beardog` as binary/genome artifact name — correct (descriptions already capability-based)
- `examples/future/infant_discovery_demo.rs` uses `beardog` in pedagogical "OLD vs NEW" comment — intentional
