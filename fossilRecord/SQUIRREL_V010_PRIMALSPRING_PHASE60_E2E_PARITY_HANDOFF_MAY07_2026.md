<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — primalSpring Phase 60: E2E Inference Parity Handoff

**Date**: May 7, 2026
**Session**: AZ
**Commit**: (see below)

## Audit Item

> **Squirrel E2E inference parity** — `validate_squirrel_roundtrip` in primalSpring
> experiments exits with `skip` because it needs a live native inference provider.
> Currently Squirrel's `inference.complete` bridges to external providers (Ollama,
> OpenAI-compatible). For full E2E parity without external deps, neuralSpring needs
> to provide a native inference endpoint that Squirrel can route to. Not blocking
> NUCLEUS deployment.

## Investigation Result

**Squirrel is fully functional.** The gap is a downstream dependency on neuralSpring.

### Evidence

1. `inference.complete` handler → `AiRouter::generate_text` → `RemoteInferenceAdapter`
   correctly routes to any provider registered via `inference.register_provider`.

2. **15 dedicated wire tests** pass in `inference_register_provider_tests.rs`:
   - `wire_inference_complete_routes_to_registered_socket`
   - `wire_inference_embed_routes_to_registered_provider`
   - `wire_inference_models_returns_merged_list`
   - `wire_register_provider_upsert`
   - `wire_unregister_provider`
   - Error paths (missing params, no provider, unavailable socket)

3. The test infrastructure already demonstrates the exact pattern primalSpring needs:
   a mock UDS server implements `inference.complete` → register via JSON-RPC →
   Squirrel forwards requests → mock responds → Squirrel returns result to caller.

### What primalSpring / neuralSpring needs to do

neuralSpring must:
1. Implement `inference.complete` on a UDS JSON-RPC server
2. Register with Squirrel via `inference.register_provider { provider_id, socket }`
3. Handle forwarded `inference.complete` calls and return `{ text, model, provider }`

Squirrel's wire protocol is stable and tested. No changes needed on Squirrel's side.

## Additional Fix: Merge Conflict Resolution

Found and resolved 3 unresolved merge conflict markers in production code:

| File | Issue | Resolution |
|------|-------|------------|
| `crates/main/src/rpc/mod.rs` | `handlers_provider` missing | Kept — file exists |
| `crates/main/src/rpc/jsonrpc_server.rs` | Stale inline dispatch | Removed — superseded by `jsonrpc_dispatch.rs` |
| `crates/main/src/niche.rs` | Duplicate capabilities list | Kept `universal_constants::SQUIRREL_EXPOSED_CAPABILITIES` (centralized) |

## Quality Gates

```
cargo fmt --all -- --check     ✓
cargo clippy --workspace       ✓ (0 warnings)
cargo test --workspace         ✓ (7,213 passed, 0 failed)
```
