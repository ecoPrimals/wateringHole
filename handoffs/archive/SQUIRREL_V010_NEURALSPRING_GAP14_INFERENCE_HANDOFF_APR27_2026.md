<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — neuralSpring Gap 14 Resolution Handoff

**Date**: April 27, 2026
**Primal**: Squirrel (AI Coordination)
**Audit source**: primalSpring Cross-Spring Convergence — neuralSpring Gap 14 (MEDIUM)

## Summary

Resolved neuralSpring Gap 14 from the primalSpring cross-spring convergence audit.
Both `inference.register_provider` and `inference.models` already existed and were
wired end-to-end; the real gaps were:

1. `inference.models` did not surface model names declared at registration
2. `supports_embedding` was hardcoded `false`
3. `inference.embed` was a stub (always METHOD_NOT_FOUND)

## Changes

### `inference.models` enriched response

Before:
```json
{"models": [{"id": "provider-id", "name": "...", "supports_completion": true, "supports_embedding": false}]}
```

After:
```json
{"models": [{"id": "provider-id", "name": "...", "supports_completion": true, "supports_embedding": true, "available_models": ["llama3", "mistral-7b"]}]}
```

- `available_models`: model names from `capabilities.models` at registration time
- `supports_embedding`: derived from `supported_tasks` containing `"embedding"`,
  `"inference.embed"`, or `"text_embedding"`

### `inference.embed` routing

Evolved from stub to production forwarding:
- Routes to first registered provider with embedding support
- Forwards raw params over UDS JSON-RPC to the remote spring
- Returns the remote spring's result directly (transparent proxy)
- Returns METHOD_NOT_FOUND with actionable message when no embedding provider exists

### New router methods

- `AiRouter::list_providers_detailed()` — enriched provider info with model names + embedding flag
- `AiRouter::find_embedding_provider()` — first available provider supporting embedding
- `AiProvider::available_model_names()` / `supports_embedding()` — enum-level introspection
- `RemoteInferenceAdapter::generate_embedding()` — JSON-RPC forwarding for embeddings
- `RemoteInferenceAdapter::model_names()` / `supports_embedding()` — config accessors

## Files modified

| File | Change |
|------|--------|
| `crates/main/src/rpc/handlers_inference.rs` | `inference.models` uses `list_providers_detailed()`; `inference.embed` routes to providers |
| `crates/main/src/api/ai/router.rs` | `list_providers_detailed()`, `find_embedding_provider()` |
| `crates/main/src/api/ai/adapters/mod.rs` | `AiProvider::available_model_names()`, `supports_embedding()` |
| `crates/main/src/api/ai/adapters/remote_inference.rs` | `model_names()`, `supports_embedding()`, `generate_embedding()` |
| `crates/main/tests/inference_register_provider_tests.rs` | 4 new wire tests, mock neuralSpring handles `inference.embed` |

## Verification

- `cargo fmt` — clean
- `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` — 0 warnings
- `cargo test --workspace` — **7,182** tests, 0 failures (4 new)
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok

## primalSpring gap reconciliation

The `PRIMAL_GAPS.md` document in primalSpring has internally inconsistent status for
`inference.register_provider`:
- **RESOLVED** in the per-primal Squirrel task table (alpha.49, wire tests + handler)
- **PARTIAL** in the "Common Cross-Primal Protocol Gaps" section
- **Low/Open** in the "Remaining Open Upstream Gaps" section

The Squirrel implementation is complete: upsert semantics, validation, capability-based
routing, unregistration, model name surfacing, embedding support detection, and
embedding forwarding. The PARTIAL and Low/Open rows should be updated to RESOLVED.
