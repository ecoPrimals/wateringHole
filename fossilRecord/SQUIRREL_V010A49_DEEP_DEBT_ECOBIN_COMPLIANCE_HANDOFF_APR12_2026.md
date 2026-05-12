<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.49 — Deep Debt, ecoBin Compliance, Overstep Cleanup

**Date**: April 12, 2026
**Previous**: SQUIRREL_V010A48_DEEP_DEBT_STUB_EVOLUTION_HARDCODING_CLEANUP_HANDOFF_APR11_2026.md

---

## Session Summary

Resolved both remaining primalSpring audit items (inference.register_provider wire test,
stable ecoBin binary). Executed comprehensive deep debt cleanup across all compliance tiers.

## Build

| Metric | Value |
|--------|-------|
| Tests | 6,903 passing / 0 failures |
| Clippy | CLEAN — `-D warnings`, zero warnings |
| Format | PASS |
| Docs | PASS — zero warnings |
| ecoBin | 3.5 MB, static-pie, stripped, BLAKE3, zero host paths, zero dynamic deps |

## primalSpring Audit Items Resolved

### 1. `inference.register_provider` Wire Test

Created `crates/main/tests/inference_register_provider_tests.rs` with 5 wire tests
exercising the real handler path (no mocks):

- Success registration + discoverable via `inference.models`
- Missing params → INVALID_PARAMS error
- Missing `provider_id` → INVALID_PARAMS error
- Duplicate registration → deduped in `inference.models`
- `inference.complete` routes to registered provider socket (end-to-end)

### 2. Stable ecoBin Binary

- Added `--remap-path-prefix` for `/home/`, `/root/`, `/Users/` to musl rustflags
- Removed `env!("CARGO_MANIFEST_DIR")` from `load_registry()` — uses CWD + embedded fallback
- Binary: 3.5 MB static-pie ELF, stripped, BLAKE3 `5c61eae8...`, zero `/home/` strings

## Compliance Tier Improvements

### T4 — Discovery (was Grade D)

- BTSP handshake discovery: capability-first `BTSP_CAPABILITY_SOCKET` / `SECURITY_SOCKET`
  with legacy `BEARDOG_SOCKET` fallback (was string-literal `"beardog.sock"` probing)
- Ecosystem registry: `capability()` for URL paths instead of product names
- `resolve_socket_path_for_ipc()`: relative paths → `$XDG_RUNTIME_DIR/biomeos/`

### T6 — Overstep (was Grade C)

- `sqlx` removed (unused optional dep in rule-system)
- `sled` confirmed absent (false flag in matrix)
- `ed25519-dalek` documented as correctly feature-gated behind `local-crypto`
- Mock fields in `mcp_adapter.rs` confirmed `#[cfg(test)]` gated

### T8 — Presentation (was Grade B)

- `swarm.rs` cleaned of unfulfilled `#[allow]`/`#[expect]` cycle
- PII audit: all config field names (`api_key`), no real secrets in code
- Doc warnings fixed: unresolved `[AIClient]` link, private `[Self::socket_path]`

### T10 — Composition (was Grade C)

- Filesystem socket added alongside abstract socket for `readdir()` discovery
- Socket path unified: `squirrel_deploy.toml` `squirrel.sock` → `/tmp/biomeos/squirrel.sock`
- Shutdown cleanup wired for filesystem socket

## Deep Debt Evolution

- `Box<dyn Error>` → `anyhow::Error` in SDK, commands, capabilities, port resolver, MCP demo
- Context traits upgraded to `impl Future + Send + '_` (fixes `refining_impl_trait_internal`)
- `AiClientImpl::IpcRouted` boxed (large enum variant)
- `adapter-pattern-examples` modernized: `Command/DynCommand` split pattern
- Commented-out code removed; redundant clones removed
- `docs/DYN_DEPRECATION_ROADMAP.md` and `docs/CRYPTO_MIGRATION.md` archived to fossilRecord

## Downstream Actions

| Audience | Action |
|----------|--------|
| **neuralSpring** | Wire test ready — use `inference.register_provider` against live Squirrel |
| **healthSpring** | ecoBin binary stable; deploy graph integration unblocked (§9) |
| **primalSpring** | Composition elevation: filesystem socket visible for benchscale/validate |
| **All springs** | Standardize on canonical `inference.*` namespace |

## Remaining (follow-up sessions)

- Coverage improvement toward 90% target
- `dyn` in plugin/hook system (object-safe collections — architectural decision)
- `async-trait` on `Dyn*` bridge traits (required for object safety)
- Reduce T4 primal-name ref count further (bulk is test/const/logging — routing migrated)
