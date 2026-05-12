# biomeOS v3.48 — cpu/timeout_ms Dispatch Enforcement (JH-2 Remainder)

**Date**: May 8, 2026
**Primal**: biomeOS
**Version**: 3.48
**Audit Reference**: primalSpring Phase 60, JH-2 remainder (joint with ToadStool)
**Tests**: 7,919 (0 failures, fully concurrent)

---

## What Changed

### JH-2 Remainder: cpu/timeout_ms Enforcement at Dispatch

The primalSpring Phase 60 audit identified two remaining JH-2 items:

1. **`cpu` / `timeout_ms` enforcement at dispatch** — `ResourceEnvelope` carries these fields but biomeOS did not enforce them.
2. **Pipeline internal stages bypass envelope** — ToadStool's `compute.dispatch.pipeline.submit` calls `dispatch_submit` with anonymous context (ToadStool-side fix).

This release addresses item 1 fully on the biomeOS side and prepares the forwarding mechanism for item 2.

### Changes

#### `crates/biomeos-core/src/method_gate.rs`

- **`ResourceEnvelope`**: Added `timeout_ms: Option<u64>` field for dispatch timeout capping.
- **`IonicTokenClaims::dispatch_timeout_ms()`**: Extracts the timeout cap from the resource envelope.
- **`ResourceEnvelope::to_forwarding_value()`**: Serializes `mem`, `cpu`, `timeout_ms` as JSON for injection into forwarded params.
- **`handle_auth_check()`**: Now returns full `resource_envelope` details (`mem`, `cpu`, `timeout_ms`, `method_allowlist_count`).
- **8 new unit tests**: `dispatch_timeout_ms` extraction, `to_forwarding_value` serialization, CPU limit enforcement, enriched `auth.check` response.

#### `crates/biomeos-atomic-deploy/src/neural_router/forwarding.rs`

- **`NeuralRouter::forward_request_with_timeout()`**: New forwarding variant accepting an optional `Duration` cap. Effective timeout is `min(system_default, cap)`, ensuring scoped tokens can tighten but never exceed the system default.
- **`forward_request_inner()`**: Private implementation with explicit timeout parameter.

#### `crates/biomeos-atomic-deploy/src/handlers/capability_call.rs`

- **`CapabilityHandler::call()`**: Now extracts `_resource_envelope.timeout_ms` from enriched params and uses `forward_request_with_timeout()` at all 4 forwarding points:
  1. Cross-gate routing
  2. Tower Atomic relay
  3. Translated routing (via capability translation registry)
  4. Direct routing (no translation)
- Injects `_resource_envelope` into forwarded `args` so downstream primals (ToadStool) can enforce `cpu`/`mem`/`timeout_ms` at their compute dispatch level.

#### `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs`

- **`enrich_with_envelope()`**: Helper method that injects `_resource_envelope` into capability call params when the caller's ionic token carries resource constraints.
- Applied to `Route::CapabilityCall`, semantic fallback path, and `Route::SemanticCapabilityCall`.
- **`_bearer_token` stripped from `SemanticCapabilityCall` args** (same token-leak fix already applied to semantic fallback).

---

## How It Works

1. Caller sends a request with `_bearer_token` containing a BearDog ionic token.
2. `routing.rs` parses the token via `CallerContext::with_bearer_token()` → `IonicTokenClaims::parse()`.
3. `MethodGate::check()` enforces scope, expiry, and method allowlist (existing JH-2).
4. For `capability.call` and semantic routing, `enrich_with_envelope()` injects `_resource_envelope` into params.
5. `CapabilityHandler::call()` extracts `timeout_ms` and passes it to `forward_request_with_timeout()`.
6. The forwarding timeout is capped to `min(30s_default, token_timeout_ms)`.
7. The `_resource_envelope` is also injected into the forwarded `args`, allowing downstream primals (ToadStool) to read `cpu`/`mem` and enforce them at their own dispatch level.

---

## What's Left (ToadStool side)

- ToadStool needs to read `_resource_envelope` from incoming `capability.call` args and enforce `cpu` at its compute dispatch level.
- ToadStool's `compute.dispatch.pipeline.submit` should pass caller context (including the envelope) to nested `dispatch_submit` calls.
- ToadStool's `shader.dispatch` should call `enforce_envelope`.

---

## Verification

```
cargo clippy --all-targets -- -D warnings  # PASS (0 warnings)
cargo fmt --check                           # PASS
cargo test --workspace                      # 7,919 passed, 0 failed
```
