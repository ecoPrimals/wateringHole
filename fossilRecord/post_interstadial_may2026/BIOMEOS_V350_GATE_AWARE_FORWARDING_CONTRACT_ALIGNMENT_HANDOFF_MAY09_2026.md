# biomeOS v3.50 — Gate-Aware Token Forwarding + primalSpring Contract Alignment

**Date**: May 9, 2026
**Primal**: biomeOS
**Version**: 3.50
**Audit Reference**: primalSpring v0.9.25 Later-Term Evolution, exp108-111
**Tests**: 7,924 (0 failures, fully concurrent)

---

## What Changed

### 1. Gate-aware `capability.call` forwarding (exp111)

**Problem**: When biomeOS routes a `capability.call` to a downstream primal
running in enforced mode, the target primal's MethodGate rejected with `-32001`
because `_bearer_token` was stripped from forwarded args (v3.47 token-leak fix)
but never re-injected.

**Fix**: Bearer tokens are now propagated through all three routing paths:

- **Semantic fallback** — `_bearer_token` injected into `cap_params` after being
  stripped from `args_obj` (the strip prevents double-forwarding; the inject
  ensures the capability handler has it for downstream forwarding).
- **`Route::CapabilityCall`** — `enrich_for_forwarding()` (renamed from
  `enrich_with_envelope()`) now injects both `_resource_envelope` and
  `_bearer_token` from `CallerContext`.
- **`Route::SemanticCapabilityCall`** — same pattern.

`CapabilityHandler::call()` extracts `_bearer_token` from the enriched params
and injects it into the forwarded `args` alongside `_resource_envelope`. This
ensures every downstream primal receives the caller's token for its own
MethodGate check.

### 2. `composition.reload` contract alignment (exp109)

**Problem**: primalSpring's `CompositionContext::reload()` expects
`{"status": "reloaded", "topology_version": N}` but biomeOS returned
`{"reloaded": true, ...}`.

**Fix**: Response now includes both the original fields (backward-compatible)
and the primalSpring contract fields:

```json
{
  "status": "reloaded",
  "reloaded": true,
  "name": "primal_name",
  "socket_path": "/path/to/socket",
  "healthy": true,
  "topology_version": 42
}
```

`LifecycleHandler` gains a monotonic `topology_version` counter (AtomicU64),
incremented on register and reload operations. `lifecycle.register` also
returns `topology_version`.

### 3. `auth.check` primalSpring contract alignment

**Problem**: primalSpring expects `{ authenticated, verified, enforcement,
scopes, subject, expires_in }` but biomeOS returned `{ authenticated, mode,
subject, scope, expired }`.

**Fix**: Response now includes all contract fields:
- `verified` (bool) — whether ionic token claims were successfully parsed
- `enforcement` — alias for `mode` (`"permissive"` or `"enforced"`)
- `scopes` — alias for `scope` (array of patterns)
- `expires_in` — seconds until token expiry (computed from `exp` claim)
- Original fields preserved for backward compatibility.

### 4. `TokenVerifier` trait (primalSpring pattern adoption)

New trait `TokenVerifier` in `biomeos-core::method_gate`:
- `LocalClaimsVerifier` — default, parse-only (no signature verification)
- `NoopVerifier` — test-only (behind `#[cfg(any(test, feature = "test-helpers"))]`)
- `biomeos-core` gains `test-helpers` feature for `NoopVerifier` access

---

## What Lights Up in primalSpring

| Experiment | What it validates | Status |
|------------|-------------------|--------|
| exp111 `gate_routing` | Token propagation through capability.call | **Ready** |
| exp109 `composition_lifecycle` | `composition.reload` contract | **Ready** |
| Contract stubs | `auth.check` field alignment | **Ready** |

---

## What's NOT in This Release

- **`nucleus --mode full` (13 primals)** — current biomeOS launches 5. This is
  a larger scope item requiring additional graph definitions and primal spawning.
- **JH-11 cross-primal token federation** — deferred. Each MethodGate validates
  independently. `_bearer_token` forwarding is the workaround.
- **`bonding.propose` runtime signing** — BearDog-side item.
- **BirdSong beacon privacy** — Songbird-side item.

---

## Verification

```
cargo clippy --all-targets -- -D warnings  # PASS (0 warnings)
cargo fmt --check                           # PASS
cargo test --workspace                      # 7,924 passed, 0 failed
```
