<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Provider Registration Hardening Handoff

**Date**: April 26, 2026
**Commit**: `4a56a18f` (squirrel main)
**Audit source**: primalSpring — April 26, 2026

## Summary

Production-hardened `inference.register_provider` per primalSpring audit finding. The audit noted that while BTSP has converged and AI capability routing works, springs registering domain-specific inference providers (e.g., neuralSpring for WGSL shader inference) need Squirrel to accept and route multi-provider registrations with proper lifecycle management.

## Changes

### 1. Upsert semantics for `register_remote_provider`

**Before**: `AiRouter::register_remote_provider()` blindly pushed a new `RemoteInferenceAdapter` to the provider list on every call. Re-registering the same `provider_id` caused unbounded list growth. The dedup only happened downstream in `list_providers()`.

**After**: The router now checks for an existing provider with the same ID and replaces it in-place. New providers are appended. The provider list stays bounded at one entry per unique `provider_id`.

### 2. Provider ID validation

**Before**: Any string (including empty or whitespace-only) was accepted as `provider_id`.

**After**: `provider_id` is trimmed and validated: must be 1–256 non-whitespace characters. Invalid IDs return `INVALID_PARAMS`.

### 3. Declared capabilities from registering spring

**Before**: `RemoteProviderConfig` only stored `provider_id`, `socket_path`, `models`, `supports_streaming`, and `max_context_size`. The adapter hardcoded `supports_text_generation = true`, `supports_image_generation = false`, `quality_tier = Standard`, `cost_per_unit = Some(0.0)`.

**After**: `RemoteProviderConfig` now carries `supported_tasks: Vec<String>`, `quality_tier: Option<String>`, and `cost_per_unit: Option<f64>`. The adapter uses these declared values:
- `supports_text_generation()` checks `supported_tasks` for `"text_generation"`, `"chat"`, or `"inference.complete"` (empty = default text support for backward compat)
- `supports_image_generation()` checks for `"image_generation"` or `"inference.image"`
- `quality_tier()` maps declared string to enum
- `cost_per_unit()` returns the declared value

### 4. Dual wire format for capabilities

The `capabilities` field in the registration params now accepts two forms:
- **Object form**: `{"supported_tasks": ["text_generation"], "models": ["llama3"], ...}`
- **Array shorthand**: `["inference.complete", "inference.embed"]`

This supports both the structured form from springs with rich metadata and the simple list form from lightweight springs.

### 5. `inference.unregister_provider` method

New JSON-RPC method for graceful spring shutdown. Params: `{"provider_id": "..."}`. Returns `{"unregistered": true/false}`. Wired in dispatch, registered in niche, capability registry, and universal-constants.

### 6. Missing socket warning

If a spring registers without a `socket` path, a warning is logged but registration succeeds. This supports use cases where the socket will be established after registration.

## Files Modified

| File | Change |
|------|--------|
| `crates/main/src/rpc/handlers_inference.rs` | ID validation, capability parsing extracted to `parse_provider_capabilities()`, new `handle_inference_unregister_provider()` |
| `crates/main/src/api/ai/adapters/remote_inference.rs` | `RemoteProviderConfig` gains `supported_tasks`, `quality_tier`, `cost_per_unit`; adapter uses declared caps |
| `crates/main/src/api/ai/router.rs` | `register_remote_provider()` → upsert; new `unregister_remote_provider()` |
| `crates/main/src/api/ai/router_tests.rs` | 5 new unit tests: upsert, multi-provider, unregister, nonexistent unregister |
| `crates/main/tests/inference_register_provider_tests.rs` | 7 new wire integration tests: empty ID, supported_tasks, array shorthand, unregister success/nonexistent, upsert dedup |
| `crates/main/src/rpc/jsonrpc_dispatch.rs` | `inference.unregister_provider` wired in dispatch |
| `crates/main/src/niche.rs` | `inference_unregister` in SEMANTIC_MAPPINGS, COST_ESTIMATES, semantic/cost JSON |
| `crates/universal-constants/src/capabilities.rs` | `inference.unregister_provider` in SQUIRREL_EXPOSED_CAPABILITIES |
| `capability_registry.toml` | New `[capabilities.inference_unregister_provider]` entry |

## Quality Gates

- `cargo fmt --all`: PASS
- `cargo clippy --workspace --all-targets -D warnings -W clippy::pedantic -W clippy::nursery`: PASS (0 warnings)
- `cargo test --workspace`: PASS (7,178 / 0 failures)
- `cargo deny check`: PASS (advisories ok, bans ok, licenses ok, sources ok)

## async-trait Status

Confirmed: zero `async-trait` / `async_trait` occurrences in crate source. Migration to native async fn in trait was completed in a prior session.

## Wire Contract

The `inference.register_provider` params are backward-compatible — existing registrations that send only `provider_id`, `socket`, and simple `capabilities` will continue to work exactly as before. The new fields are all optional with sensible defaults.

`inference.unregister_provider` is additive — existing springs that don't call it will simply have their entries replaced on re-registration (upsert), which is the correct behavior for springs that restart without explicit cleanup.
