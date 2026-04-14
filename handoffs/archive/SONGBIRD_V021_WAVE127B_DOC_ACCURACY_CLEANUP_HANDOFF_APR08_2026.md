# Songbird v0.2.1 — Wave 127b: Root Doc Accuracy & Debris Cleanup

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 127b  
**Status**: Complete  
**Commits**: `0a23d8a8` (coverage expansion), `ef35a2e1` (doc accuracy)

---

## Summary

Comprehensive audit of root docs, specs, scripts, and codebase for stale claims, outdated metrics, broken links, archive debris, and false-positive markers. No debris found — codebase is clean.

## Doc Fixes

| File | Fix |
|------|-----|
| README.md | Largest file 518L → 711L production / 863L test-only; test count 12,860 → 12,916 |
| CONTEXT.md | Same file size correction |
| REMAINING_WORK.md | File size, async-trait 99/50 → 109/54, coverage dates Apr 7→8 |
| port_fallback_test.rs | Last `// FIX:` marker removed (was test documentation, not actionable) |
| VALIDATION_EXECUTIVE_SUMMARY.md | Broken relative link `../` → `./` (sibling file) |
| PRIMAL_COORDINATION_ARCHITECTURE.md | Removed nonexistent `songbird-gaming` link; fixed `../../` → `../` paths |

## Debris Audit — Clean

| Category | Finding |
|----------|---------|
| `*.bak` / `*.orig` / temp files | None |
| `archive/` / `old/` / `deprecated/` dirs | None |
| `tarpaulin.toml` | Already deleted (Wave 122) |
| `vis_test` binary | Already deleted (Wave 122) |
| Untracked files | None |
| `git status` | Clean |

## Marker Verification

| Marker | Count | Status |
|--------|-------|--------|
| `TODO` in Rust | 0 | Claim holds |
| `FIXME` | 0 | Claim holds |
| `HACK` | 0 | Claim holds |
| `// FIX:` | 0 | Last one removed this wave |
| `todo!()` | 0 | Claim holds |
| `unimplemented!()` | 0 | One false positive (doc text) |
| `BLOCKED:` | 8 | All legitimate — Tor onion crypto, tracked in REMAINING_WORK.md |
| `#[deprecated]` | 47 | All legitimate API migration markers |

## Spec Link Status

- Monorepo-relative `../../../infra/wateringHole/fossilRecord/` links: valid in full checkout
- `PRIMAL_COORDINATION_ARCHITECTURE.md` crate links: fixed
- `VALIDATION_EXECUTIVE_SUMMARY.md` experiment link: fixed
- CHANGELOG `specs/archive/` references: kept as historical record

## Scripts — All Active

| Script | Status |
|--------|--------|
| `scripts/coverage.sh` | Active — referenced in README, tests/README |
| `scripts/health-monitor.sh` | Active — ops tool |
| `scripts/test-with-security-provider.sh` | Active — referenced in README |
| `deployment/` scripts | Active — deployment tooling |
| `examples/jsonrpc_client.sh` | Active — example |
