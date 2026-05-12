<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.52 — CLI Bind Gap, Hardcoding Evolution, Smart Refactoring

**Date**: April 14, 2026
**Previous**: SQUIRREL_V010A51_DEEP_DEBT_REFACTOR_DEP_EVOLUTION_HANDOFF_APR13_2026.md

---

## Session Summary

Resolved primalSpring benchScale audit finding SQ-04 (CLI bind gap), evolved
remaining hardcoded primal names and `/tmp/` paths to capability-based patterns,
matured production stubs in the learning subsystem, and smart-refactored 9
production files below 800 lines. Removed orphaned dead code files.

## Build

| Metric | Value |
|--------|-------|
| Tests | 7,003 passing / 0 failures |
| Coverage | ~89% line (cargo-llvm-cov) |
| Clippy | CLEAN — `-D warnings`, zero warnings |
| Format | PASS |
| Docs | PASS — zero warnings |
| ecoBin | 3.5 MB, static-pie, stripped, BLAKE3, zero host paths, zero dynamic deps |
| Files | 1,014 `.rs` files, ~333k lines, max 965 lines |

## Changes

### SQ-04 RESOLVED — CLI Bind Gap (primalSpring benchScale finding)

`squirrel server --port 9500` hardcoded TCP bind to `127.0.0.1`, making
Squirrel unreachable from outside Docker containers (exp077 failure).

**Resolution**: Added `--bind` CLI flag + `SQUIRREL_BIND` / `SQUIRREL_IPC_HOST`
environment variable support. Precedence: CLI > env > config > default
(`127.0.0.1`). Docker pattern: `squirrel server --bind 0.0.0.0 --port 9500`.
Aligns with barraCuda's `BARRACUDA_IPC_HOST` pattern.

### Hardcoded Primal Names Eliminated

| Before | After | File |
|--------|-------|------|
| `"toadstool"` socket stem | `"compute"` capability stem | `api/ai/router.rs` |
| `SONGBIRD_SOCKET` env fallback | Removed (prefer `DISCOVERY_SOCKET`) | `capabilities/discovery_service.rs` |
| `"petalTongue"` in logs/docs | "visualization capability discovery" | `visualization/web.rs` |

### Hardcoded Paths Evolved

- `"127.0.0.1"` in universal listener → `LOCALHOST_IPV4` constant
- `/tmp/{sock}` in 5 files → `get_socket_dir()` / `BIOMEOS_SOCKET_FALLBACK_DIR`

### Production Stubs Matured

- RL policy: `get_training_iterations`/`get_last_loss`/`get_performance_metrics`
  now read from real `training_state`/`metrics` fields (were hardcoded 0/placeholders)
- RL policy: `load_weights` performs real file I/O (was stubbed `Ok(())`)
- Context learning: `extract_features` does JSON-aware extraction from context state
  (was returning placeholder feature vector)

### Smart Large File Refactoring (9 files)

| File | Before | After | Extracted To |
|------|--------|-------|--------------|
| `learning/integration.rs` | 881 | 700 | `integration_data.rs` |
| `web/dashboard.rs` | 856 | 605 | `dashboard_types.rs` |
| `zero_copy.rs` | 851 | 670 | `zero_copy_config.rs` |
| `federation/service.rs` | 828 | 723 | `service_swarm.rs` |
| `config/builder.rs` | 827 | 768 | `builder_presets.rs` |
| `rpc/jsonrpc_server.rs` | 872 | 756 | `jsonrpc_dispatch.rs` |
| `api/ai/router.rs` | 828 | 701 | `router_init.rs` |
| `sync.rs` | 819 | 733 | `sync_types.rs` |

All extractions preserve public API and tests. Strategy: extract cohesive type
clusters or trait implementations rather than arbitrary line splits.

### Dead Code Removed

- `crates/config/src/unified/security.rs` — orphaned file not in module graph;
  canonical `SecurityConfig` lives in `unified/types/definitions.rs`
- `zero_copy_types.rs` — duplicate artifact superseded by `zero_copy_config.rs`
- `hostname` workspace dependency — unused by any member crate

## Remaining Debt

| Item | Priority | Notes |
|------|----------|-------|
| Coverage to 90% | LOW | Requires testing binary entry points / WASM / server code |
| Remove `nix` from universal-constants (Linux) | LOW | /proc parsing covers all current usage |
| `inference.register_provider` vs neuralSpring | BLOCKED | Awaiting neuralSpring WGSL shader inference |
| Type rename `Beardog*` → `Security*` | DEFERRED | API-breaking; coordinate across primals |

## Status

**Health PASS.** SQ-04 resolved. Zero production files >800 lines. AI provider
chain operational. No blockers for composition or benchScale integration.
