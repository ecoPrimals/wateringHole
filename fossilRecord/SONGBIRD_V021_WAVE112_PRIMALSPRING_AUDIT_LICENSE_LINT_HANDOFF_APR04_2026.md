# Songbird v0.2.1 — Wave 112: primalSpring Audit Response

**Date**: April 4, 2026  
**Commit**: `15388c7f`  
**Trigger**: primalSpring downstream audit (Songbird — C tier)

## Audit Findings Addressed

| Finding | Tier | Before | After |
|---------|------|--------|-------|
| License `AGPL-3.0-only` | T1 Build | `-only` | `-or-later` (1,559 .rs, Cargo.toml, deny.toml, LICENSE, 12+ .md) |
| Commented-out code | T1 Build | 28 lines | 0 lines (30+ removed across 11 files) |
| `#[allow(` vs `#[expect(` | T8 Presentation | 423 allow (49%) | 25 allow (3%) — all `missing_docs` subtree suppression |
| PII in test files | T8 Presentation | 6 files (Alice/Bob/Charlie) | 0 — neutralized to peer-alpha/beta/gamma/delta |
| Stale lint suppressions | T8 Presentation | 50+ stale | 0 — all removed by `#[expect]` migration |
| Primal-name refs | T4 Discovery | 574 refs / 185 files | 543 refs / 181 files |

## Quality Status

| Metric | Value |
|--------|-------|
| Tests | 12,568 passed, 0 failed, 252 ignored |
| Clippy | 30/30 crates clean (pedantic + nursery, `-D warnings`) |
| Format | Clean (`cargo fmt --check`) |
| License | `AGPL-3.0-or-later` — consistent across Cargo.toml, LICENSE, SPDX headers, docs |
| `#[expect(` ratio | 97% (836 expect / 25 allow) |

## Remaining T4 Discovery Work

543 primal-name refs remain, mostly in:
- Wire-compat `serde(alias = "...")` fields (must stay)
- Env var fallback names (`BEARDOG_ENDPOINT`, etc.) (external interface)
- `#[deprecated]` function names and their deprecation messages
- Test files exercising legacy wire compatibility

The 285 env-var refs are capability-first with fallback — correct pattern per wateringHole standards.
