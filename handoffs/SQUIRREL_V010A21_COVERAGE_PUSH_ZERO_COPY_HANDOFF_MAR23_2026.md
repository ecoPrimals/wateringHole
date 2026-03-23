<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.21 — Coverage Push & Zero-Copy Evolution

**Date**: March 23, 2026
**Primal**: Squirrel (AI coordination)
**Domain**: `ai`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)
**Baseline**: v0.1.0-alpha.20
**Result**: v0.1.0-alpha.21

## Summary

Massive coverage push from 74.8% to 86.8% via 22 parallel test waves across all 21
workspace crates. Zero-copy evolution of clone hotspots. Five production bugs discovered
and fixed through the testing effort. Test count grew from 5,828 to 6,717 (+889).

## Quality Gate

| Check | Before (a.20) | After (a.21) |
|-------|---------------|--------------|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --all-targets -D warnings` | PASS | PASS (pedantic+nursery) |
| `cargo doc --no-deps` | PASS (0 warnings) | PASS (0 warnings) |
| `cargo test --workspace` | PASS (5,828 / 0) | PASS (6,717 / 0) |
| `cargo deny check` | PASS | PASS |
| File size max | 965 lines | 965 lines |
| Coverage (llvm-cov) | 74.8% | 86.8% |
| Unsafe code | 0 | 0 |
| SPDX coverage | 100% | 100% |

## Coverage Breakdown

22 test waves targeted every major subsystem:

| Wave | Target | Impact |
|------|--------|--------|
| 4 | MCP security (rbac, identity, key_storage, manager, audit) | 5%→60%+ |
| 5 | Core context (rules/actions, sync, plugins/mod) | 40%→70%+ |
| 6 | Services (hooks, lifecycle, journal) | 10%→60%+ |
| 7 | MCP error types + task types + protocol types | 30%→70%+ |
| 8 | SDK (client/fs, client/http, mcp/client, events, conversions) | 30%→60%+ |
| 9 | AI tools (capability_ai, optimization, neural_http, config) | 20%→50%+ |
| 10 | Learning modules (experience, metrics, policy) + visualization | 45%→70%+ |
| 11 | Plugin web (api, dashboard, example, http, endpoint) | 10%→55%+ |
| 12 | Main RPC (tarpc_server, jsonrpc_server, ecosystem manager, AI router) | 20%→65%+ |
| 13 | Universal adapters (compute, storage, security, orchestration) | 0%→60%+ |
| 14 | MCP task/client + protocol processor + marketplace/registry | 0%→55%+ |
| 15 | Biomeos integration + primal_provider + cli plugins | 0%→65%+ |
| 16 | CLI (plugins/manager, mcp/server, mcp/client, formatter) | 0%→55%+ |
| 17 | Main (tarpc_client, health monitor, constraint_router, integrations) | 0%→60%+ |
| 18 | AI dispatch + learning metrics + rule-system directory/utils | 40%→65%+ |
| 19-22 | Deep extensions across all remaining gaps | Various→80%+ |

## Production Bugs Found via Testing

1. **`task/manager.rs` deadlock** — `assign_task` held write lock across async
   prerequisite check → fixed via snapshot-check-relock pattern
2. **`web/api.rs` route shadowing** — `/api/plugins/health` and `/metrics` shadowed
   by generic plugin-details route → moved health/metrics matchers first
3. **`handlers_tool.rs` spring hijacking** — spring tools could intercept built-in
   `system.health` → built-ins now resolve before spring routing
4. **`resource_manager/core.rs` stale stats** — `get_usage_stats` reported stale
   background task count → now queries live task list
5. **`dispatch.rs` flaky test** — HashMap iteration order under llvm-cov → fixed by
   sequential provider registration

## Zero-Copy Evolution

- `MetricType` / `ConsensusStatus` → `Copy` (eliminates clone overhead on hot paths)
- `mem::take` replaces payload clone in consensus vote handling
- `Arc::clone(&state)` clarity across federation and RPC modules
- Redundant `String` clones removed in metric registration
- `AnnouncedPrimal` fields moved instead of cloned in capability handlers

## Remaining Gap to 90%

~3.2% gap is dominated by:
- Binary entry points (`main.rs`, demo bins, CLI main) — ~3,000 uncovered lines, untestable via unit tests
- WASM-dependent SDK paths — require browser environment to exercise
- Excluding binaries, testable library coverage is approximately **89%**

## Ecosystem Impact

- No interface changes — all existing JSON-RPC methods and tarpc service methods unchanged
- No dependency additions or removals
- All 24 exposed capabilities unchanged
- `CURRENT_STATUS.md`, `README.md`, `CONTEXT.md`, `CHANGELOG.md` updated with current metrics

## Next Steps

1. Consider `wasm-pack test` for SDK WASM paths (would push toward 90% overall)
2. Integration test expansion for `main.rs` entry point paths
3. Continue toward Phase 2 items (performance optimizer evolution)

## Files Changed

889 new tests across 50+ files in all 21 workspace crates. Production fixes in 5 files.
Zero-copy improvements in 6 files. Root docs updated (README, CONTEXT, CHANGELOG,
CURRENT_STATUS). Adapter-pattern-examples README license corrected (MIT→AGPL-3.0-only).
