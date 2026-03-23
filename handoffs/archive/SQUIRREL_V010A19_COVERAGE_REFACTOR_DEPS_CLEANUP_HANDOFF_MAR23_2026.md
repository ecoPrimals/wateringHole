<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.19 — Coverage, Refactoring, Dependency Modernization & Debris Cleanup

**Date**: March 23, 2026
**Primal**: Squirrel (AI coordination)
**Domain**: `ai`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)
**Baseline**: v0.1.0-alpha.18
**Result**: v0.1.0-alpha.19

## Summary

Continued the deep debt resolution sprint with dependency modernization (base64 0.22),
smart file refactoring (web/api.rs types extraction), ai-tools lint tightening (10 blanket
allows removed, 67 auto-fixes), coverage wave 2 (6 new test suites), and orphan code
debris cleanup (18 dead files removed across 3 crates).

## Quality Gate

| Check | Before (a.18) | After (a.19) |
|-------|---------------|--------------|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --all-targets -D warnings` | PASS | PASS (pedantic+nursery) |
| `cargo doc --no-deps` | PASS (0 warnings) | PASS (0 warnings) |
| `cargo test --workspace` | PASS (5,729 / 0) | PASS (5,777 / 0) |
| `cargo deny check` | PASS | PASS |
| File size max | 977 lines | 859 lines |
| Coverage (llvm-cov) | ~74.3% | ~74.6% |
| Orphan dead code | 18 files | 0 |

## Changes

### Dependency Modernization

- **base64 0.21→0.22**: Unified across workspace root, `squirrel-mcp`, `squirrel` main
  (`squirrel-mcp-auth` was already 0.22); fixed 1 legacy `base64::encode()` call to
  `Engine::encode` API in `domain_objects_test.rs`
- **rand 0.8→0.9**: Analyzed (23 files, moderate effort — `thread_rng`→`rng`,
  `gen_range`→`random_range`, `SliceRandom` split). Deferred for focused PR.
- **mockall 0.11→latest**: Analyzed (1 file, trivial). Deferred — low priority.

### Smart Refactoring

- **web/api.rs** (977→859 lines): Extracted 8 DTO types (`PluginInfo`, `EndpointInfo`,
  `PluginInstallRequest`, `PluginConfigurationRequest`, `PluginExecutionRequest`,
  `PluginSearchRequest`, `PluginMarketplaceEntry`, `WebSocketMessage`) into
  `web/api_types.rs` (131 lines). Backward-compatible re-exports from `web/mod.rs`.

### ai-tools Lint Tightening

- Removed 10 blanket clippy suppressions from `lib.rs`: `unused_imports`,
  `uninlined_format_args`, `use_self`, `redundant_closure_for_method_calls`,
  `redundant_else`, `manual_string_new`, `redundant_clone`, `assigning_clones`,
  `cloned_instead_of_copied`, `needless_raw_string_hashes`
- 67 auto-fixes applied across 11 files via `cargo clippy --fix`
- 32 structural allows remain (documented — require `items_after_test_module` fixes)

### Coverage Expansion (Wave 2)

New inline test suites for:
- `config/unified/types/definitions.rs` — 30 tests (serde roundtrips, defaults, boundaries)
- `core/auth/auth.rs` — auth flow, session, permission, token tests
- `mcp/security/token.rs` — 18 tests (create, validate, revoke, cleanup, stats)
- `core/routing/balancer.rs` — 18 tests (round-robin, weighted, least-conn, adaptive)
- `mcp/protocol/websocket.rs` — 15 tests (config, codec, server, client)
- `mcp/enhanced/session.rs` — session types, storage, concurrency tests

### Debris Cleanup

Removed **18 orphan files** (1,981 lines of dead code) across 3 crates:

| Location | Files | Reason |
|----------|-------|--------|
| `crates/core/mcp/src/tests/` | 3 | Unwired from `lib.rs`; uses obsolete `crate::mcp::*` imports |
| `crates/core/mcp/src/protocol/tests/` | 5 | Unwired from `protocol/mod.rs`; old test tree |
| `crates/services/commands/src/tests/` | 5 | Unwired from `lib.rs`; never compiled |
| `crates/services/commands/src/mod.rs` | 1 | Dead parallel module tree (lib.rs is the crate root) |
| `crates/core/auth/src/errors_test.rs` | 1 | Duplicate of existing inline `#[cfg(test)]` in `errors.rs` |
| `crates/core/mcp/src/transport/memory/standalone_test.rs` | 1 | Unreferenced from memory module |
| `crates/core/mcp/src/protocol/tests/domain_objects_test.rs` | 1 | Part of unwired tests directory |

### Documentation Updates

- `README.md`: Updated test count (5,777), coverage (74.6%), crate count (21)
- `CONTEXT.md`: Updated version (alpha.19), test count, coverage
- `CURRENT_STATUS.md`: Full alpha.19 sprint notes, updated metrics

## Metrics

| Metric | a.18 | a.19 |
|--------|------|------|
| Tests | 5,729 | 5,777 |
| Coverage | ~74.3% | ~74.6% |
| Max file size | 977 | 859 |
| Orphan dead files | 18 | 0 |
| ai-tools blanket allows | 42 | 32 |
| base64 version | 0.21 (mixed) | 0.22 (unified) |

## Impact on Other Primals

### For All Primals

- No breaking API changes; consumers can adopt on their normal cadence.
- Debris cleanup pattern (orphan test file detection) is replicable across all primals.

### For primalSpring / Songbird / BearDog

- No protocol or capability contract changes this sprint; internal Squirrel
  hardening, dependency modernization, and cleanup only.

## Remaining Debt / What's Next

1. **Coverage 74.6% → 90%**: Top uncovered files — `federation.rs` (957L), `primal_provider/core.rs` (922L), `huggingface.rs` (820L), `ecosystem.rs` (760L), `adapter/core.rs` (739L)
2. **rand 0.8→0.9**: 23 files, mechanical renames + `experience.rs` `SliceRandom` migration
3. **ai-tools structural cleanup**: 32 remaining allows need `items_after_test_module` fixes (~140 locations)
4. **protocol/adapter wiring**: `protocol/adapter/` exists but is not wired into `protocol/mod.rs`
5. **commands crate wiring**: `lib.rs` has `#![expect(dead_code)]` — full command service integration pending

## Patterns Worth Adopting

1. **Type extraction refactoring** — DTOs in their own module; re-export for backward compatibility
2. **Iterative lint tightening** — remove machine-fixable allows first, run `--fix`, then tackle structural ones
3. **Orphan file detection** — grep for `mod X` references to find dead test trees that passed CI silently

## Dependencies

No new external dependencies. `base64` version unified to 0.22.

| Primal | Capabilities Used | Required |
|--------|-------------------|----------|
| BearDog | `crypto.*`, `auth.*`, `secrets.*`, `relay.*` | Yes |
| Songbird | `discovery.*` | Yes |
| ToadStool | `compute.*` | No |
| NestGate | `storage.*`, `model.*` | No |
| primalSpring | `coordination.*`, `composition.*` | No |
| petalTongue | `visualization.*`, `interaction.*` | No |
| rhizoCrypt | `dag.*` | No |
| sweetGrass | `anchoring.*`, `attribution.*` | No |
| Domain Springs | `mcp.tools.list`, `health.*` | No |

## Breaking Changes

None. All changes are backward-compatible.
