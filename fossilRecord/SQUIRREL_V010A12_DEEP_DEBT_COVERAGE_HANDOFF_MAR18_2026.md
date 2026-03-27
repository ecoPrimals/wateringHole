<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.12 — Deep Debt Resolution & Coverage Expansion

**Date**: 2026-03-18
**Primal**: Squirrel
**Version**: 0.1.0-alpha.12
**Sprint**: Deep Debt Resolution + Test Coverage Expansion
**Previous**: SQUIRREL_V010A11_FULL_EVOLUTION_ABSORPTION_HANDOFF_MAR17_2026

---

## Summary

Deep debt resolution sprint: smart file refactoring (5 files over/near 1000 lines),
hardcoded URL extraction to env-overridable config, discovery stub evolution to
socket-registry-backed implementations, clone reduction on hot paths, and 346+ new
tests across 7 crates. Coverage 67% → 71%. All quality gates pass.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (zero warnings) |
| `cargo test --all-features --lib` | 4,730 pass / 0 failures / 4 ignored |
| `cargo doc --workspace --no-deps` | PASS |
| Files > 1000 lines | 0 (max: 974 — unwired legacy adapter.rs) |
| Coverage | 71% line coverage (target: 90%) |
| TODO/FIXME in source | 0 |
| Hardcoded credentials | 0 |
| Hardcoded URLs | 0 (all env-overridable) |
| Unsafe code | 0 (`#![forbid(unsafe_code)]` all crates) |
| Debris/orphans | 0 |

## Changes

### Smart File Refactoring (P0)

| File | Before | After | Method |
|------|--------|-------|--------|
| `router.rs` | 991 | 155 | Extracted `message_router.rs`, `team_types.rs`, `workflow_manager.rs`; thin re-export |
| `core/lib.rs` | 970 | 245 | Extracted `types/core.rs`, `types/mesh.rs` with backward-compat re-exports |
| `journal.rs` | 969 | 296 (core) | Split into 6 submodules: entry, error, persistence, command_journal, tests, mod |
| `ecosystem-api/types.rs` | 985 | 7 submodules | security, context, primal, request, health, registration, service_mesh |
| Test-overflow files | 1259–1338 | 584–699 | Test modules extracted to `*_tests.rs` via `#[path]` |

### Hardcoded URL Extraction (P0)

New `universal-constants::ai_providers` module with env-overridable functions:

| Function | Env Variable | Default |
|----------|-------------|---------|
| `anthropic_base_url()` | `ANTHROPIC_API_BASE_URL` | `https://api.anthropic.com/v1` |
| `openai_base_url()` | `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` |
| `anthropic_messages_url()` | (derived from base) | base + `/messages` |
| `openai_chat_completions_url()` | (derived from base) | base + `/chat/completions` |

Monitoring endpoints and universal adapter test endpoints also converted to use
`get_service_port()` and `http_url()` from `universal-constants::network`.

### Discovery Stub Evolution (P1)

| Module | Before | After |
|--------|--------|-------|
| `registry.rs` | Empty HTTP stub | `RegistryType::Biomeos` reads `$XDG_RUNTIME_DIR/biomeos/socket-registry.json` |
| `dnssd.rs` | Empty DNS-SD stub | Falls back to socket registry (pure Rust, no C DNS deps) |
| `mdns.rs` | Empty mDNS stub | Falls back to socket registry (pure Rust, no multicast deps) |
| `socket_registry.rs` | N/A | New module: file-based discovery with TTL cache, capability matching |

Socket registry integrated as Stage 2 in `RuntimeDiscoveryEngine`,
`CapabilityResolver`, and `PrimalSelfKnowledge`.

### Test Coverage Expansion (P1)

| Crate | New Tests | Key Coverage |
|-------|-----------|-------------|
| `squirrel-rule-system` | 33 | Action executor, plugins, statistics, serialization |
| `squirrel-commands` | 48 | All 6 built-in commands, edge cases, error paths |
| `squirrel-context` | 58+40 | Rule parser (16%→95%), adaptive learning, manager, integration |
| `squirrel-mcp-auth` | 36+23 | Auth service, capability crypto, security provider, ecosystem JWT, capability JWT, delegated client |
| `squirrel-mcp-config` | 49 | Environment config (31), timeouts (18) |
| `adapter-pattern-tests` | 69 | Auth (28), commands (13), integration (12), types (16) |

### Clone Reduction (P2)

- `tool/executor.rs` — eliminated redundant `tool_id`/`capability`/`request_id` clones
- `discovery/self_knowledge.rs` — cache-and-return pattern saves one clone per discovery hit
- `workflow_manager.rs` — format before assign eliminates `new_status.clone()`
- `tool/management/mod.rs` — move semantics for `tool.id`/`tool.name`/`tool.description`

### Dependency Updates (P2)

- `redis` 0.23.3 → 1.0.5 in `squirrel-mcp`
- `proptest` centralized at 1.10.0 in workspace `[dependencies]`
- `bytes` 1.5 with `serde` feature added to `universal-patterns`

### Bug Fixes

- `test_load_from_json_file` flaky — wrapped in `temp_env::with_vars_unset`
- `RegistryAdapter::clone()` — was creating empty adapter (lost commands)
- mDNS test assertion — `_primal._tcp.local.` → `_biomeos._tcp.local.`
- Benchmark `sample_size(5)` → `sample_size(10)` (criterion minimum)
- `SecurityConfig::default()` impl added for test setup
- Recursive async in `rbac.rs` — boxed the future

### Debris Cleanup

- Removed commented-out module declarations across 10 files
- Cleaned `#[allow]` → `#[expect]` migration remnants
- Removed unused imports after refactoring (via `cargo fix`)

## Remaining Stubs (Intentional)

| Module | Status | Note |
|--------|--------|------|
| `performance_optimizer/batch_processor` | Phase 2 | Simulated batch loading |
| `performance_optimizer/optimizer` | Phase 2 | Simplified plugin loading |
| `model_splitting/` | Redirect | Functionality in ToadStool |
| `InMemoryMonitoringClient` | Intentional | Fallback when no external monitoring |
| `security/crypto.rs` | Stub | BearDog integration pending |
| `protocol/adapter.rs` | Unwired | Not in protocol module tree (974L legacy) |

## Known Issues

1. `chaos_07_memory_pressure` flaky under parallel test load
2. Coverage at 71% — gap to 90% target; remaining gap is network servers, CLI entry points, adapter implementations
3. `adapter.rs` (974L) unwired legacy — protocol module only declares `types` and `websocket`
4. Architectural `#[allow]` for `unused_async` / `unused_self` in BearDog stubs

## Ecosystem Impact

- No API changes — wire-compatible with all ecosystem primals
- Socket registry discovery enables biomeOS-based primal discovery without Songbird
- AI provider URLs now environment-configurable for deployment flexibility
- Discovery mechanisms fall back gracefully (socket registry → empty results)
