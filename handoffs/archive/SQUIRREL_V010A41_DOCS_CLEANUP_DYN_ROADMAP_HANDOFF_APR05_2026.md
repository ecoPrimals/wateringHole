<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.41 — Docs Cleanup + dyn Deprecation Roadmap

**Date**: April 5, 2026
**Commits**: fe78777f (wave 3 migration), 13a05fb9 (docs + cleanup)

## Summary

Root documentation brought current with alpha.41. 20 orphan test files
(7,658 lines) removed. `dyn` deprecation roadmap created to guide future
evolution toward modern Rust static dispatch.

## Documentation Updates

- **CHANGELOG.md**: Added entries for alpha.34 through alpha.41 (8 releases)
- **CONTEXT.md**: Version updated to alpha.41, metrics corrected
- **DYN_DEPRECATION_ROADMAP.md**: New document inventorying 27 traits still
  using `#[async_trait]` with migration strategies and priorities

## Debris Removal

20 orphan `*_tests.rs` files deleted — none were compiled by Cargo (the actual
tests run from inline `#[cfg(test)] mod tests` blocks in parent modules):

- `universal-patterns`: 15 files (lib, builder, traits/*, security/*, config, federation)
- `core/context`: 4 files (tests/ directory removed entirely)
- `rule-system`: 1 file (parser_tests.rs)

## Codebase Health

- **Zero TODOs/FIXMEs/stubs** in Rust sources
- **Zero `todo!()` / `unimplemented!()`** macros
- **No orphan scripts, archives, or backup files**
- **129 `#[async_trait]` annotations** remaining (down from 228 at start of migration)

## dyn Deprecation Status

Remaining `dyn` dispatch is in legitimate heterogeneous collections:

| Priority | Traits | dyn count |
|----------|--------|-----------|
| **High** | Plugin (65), Command (73), AIClient (53), AiProviderAdapter (23) | 214 |
| **Medium** | UniversalServiceRegistry (26), ServiceDiscovery (17), ContextPlugin (14), WebPlugin (10) | 67 |
| **Low** | PrimalProvider (7), MonitoringProvider (7), ConditionEvaluator (4), others | ~30 |

See `docs/DYN_DEPRECATION_ROADMAP.md` for detailed migration strategies per trait.

## Quality Gates

All pass: fmt, clippy (-D warnings both modes), test, doc, deny
