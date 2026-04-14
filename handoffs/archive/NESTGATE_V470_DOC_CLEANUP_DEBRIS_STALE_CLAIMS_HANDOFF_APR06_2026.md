# NestGate v4.7.0-dev — Session 33b Handoff: Doc Cleanup & Debris

**Date**: April 6, 2026
**Commits**: `db52c755`, `19c879e7`, `ebc28da8`
**Branch**: `main`

---

## Summary

Comprehensive documentation cleanup aligning all root docs to ground truth, removing stale claims, cleaning debris, and fixing false positives across 18 files.

## Documentation Fixes

### Dates and Counts
- All root docs updated from `2026-04-05` → `2026-04-06`
- Test counts: `11,826 passed` / `461 ignored` / `0 failed` in all docs
- `docs/guides/TESTING.md` banner: `~12,240` → `~11,826`

### Stale Claims Corrected
- **"fossil on disk"** → **"removed from workspace"** for `nestgate-network`, `nestgate-automation`, `nestgate-mcp` (directories don't exist in tree)
- **Env isolation**: Updated from "prefer temp_env" to "prefer EnvSource / MapEnv; temp_env + #[serial] only for direct process env reads"
- **CHANGELOG "zero TODO"**: Corrected to note 11 tracking TODOs in `production_placeholders.rs` for future HTTP wiring; claim narrowed to `todo!()` / `FIXME` / `HACK`
- **tarpc "Coming soon"**: Fixed in `service.rs` to show "tarpc service active" when `tarpc-server` feature is enabled

### Dead Code Removed
- **`tests/common/templates.rs`**: Removed dead `property_test!` macro behind `#[cfg(feature = "proptest")]` — root crate has no proptest feature
- **Stale profraw files**: Cleaned 4 coverage artifacts from `nestgate-bin/`

### Infrastructure Documentation
- **Root `benches/`**: Added status note to `benches/README.md` — files exist but are not wired to workspace `[[bench]]` entries; active benches are in `nestgate-core`
- **Disabled fuzz targets**: Updated comments in `fuzz/Cargo.toml` and 3 source files with accurate status (need API/import fixes before compilation)

## Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 11,826 |
| Tests ignored | 461 |
| Tests failed | 0 |
| Clippy warnings | 0 |
| Docs files updated | 12 |
| Code files updated | 6 |

## Remaining Known Doc Debt

| Item | Notes |
|------|-------|
| `docs/architecture/ARCHITECTURE_OVERVIEW.md` | Historical Nov 2025 doc — says "Version 0.11.0", "15 Unified Crates", references `nestgate-network`. Kept as fossil record. |
| `docs/guides/TESTING.md` body | Nov 2025 baseline — banner updated but body still references old paths. Kept as historical; `tests/README.md` is canonical. |
| Root `benches/*.rs` | 10 files not wired to cargo — kept with status documentation |
| 3 disabled fuzz targets | Non-trivial but need import fixes — kept with updated comments |
