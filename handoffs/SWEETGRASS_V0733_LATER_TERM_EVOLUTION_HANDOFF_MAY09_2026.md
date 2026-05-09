# sweetGrass v0.7.33 — Later-Term Evolution Handoff

**Date**: May 9, 2026
**From**: sweetGrass team
**To**: primalSpring, ecosystem teams
**Ref**: primalSpring v0.9.25 Later-Term Evolution — Upstream Primal Capability Targets

---

## Summary

sweetGrass v0.7.33 absorbs three patterns from primalSpring's later-term evolution audit:

1. **Token scope validation** — `_bearer_token` extracted from JSON-RPC params
2. **Enriched `auth.check`** — returns `{ authenticated, verified, enforcement, scopes, subject, expires_in }`
3. **`attribution.witness`** — JH-5 Phase 3 audit event pipeline endpoint

---

## Changes

### 1. Token Extraction (`_bearer_token`)

`dispatch_classified()` now extracts `_bearer_token` from JSON-RPC params and
threads it through `CallerContext` to the method gate. When a caller sends:

```json
{"jsonrpc":"2.0","method":"braid.create","params":{"_bearer_token":"ionic-abc-123","data_hash":"sha256:..."},"id":1}
```

The gate sees `bearer_token = Some("ionic-abc-123")` and permits the protected
method without logging a permissive-mode warning.

Token is **not stripped** from params — handlers can inspect it if needed.

### 2. Enriched `auth.check` Response

Was:
```json
{"authenticated": false, "mode": "permissive"}
```

Now:
```json
{
  "authenticated": true,
  "verified": false,
  "enforcement": "permissive",
  "scopes": null,
  "subject": null,
  "expires_in": null
}
```

- `authenticated`: true when `_bearer_token` is present in params
- `verified`: always `false` until `auth.verify_ionic` (JH-11) is wired
- `enforcement`: current gate mode
- `scopes`/`subject`/`expires_in`: `null` until BearDog token verification is live

### 3. `attribution.witness` (JH-5 Phase 3)

New method in the dispatch table. Accepts:

```json
{
  "hash": "sha256:...",
  "witness_agent": "did:key:z6MkSkunkBat",
  "event_type": "security",
  "payload": {"severity": "high", "source": "defense.log"}
}
```

Returns a witness record with `hash`, `witness_agent`, `event_type`, `payload`,
`chain_depth`, `witnessed_at`. Logs the attestation at INFO level.

Pipeline: skunkBat `defense.log` -> rhizoCrypt `dag.event.append` -> sweetGrass `attribution.witness`.

---

## What's NOT Yet Implemented (deferred to JH-11)

- `TokenVerifier` trait + `BearDogVerifier` — requires BearDog key distribution
- `auth.verify_ionic` call — requires BearDog `auth.verify_ionic` IPC endpoint
- `scope_permits_method()` enforcement — requires BearDog to return `scopes` array
- Contract test stubs (`#[cfg(feature = "stub-primals")]`) — deferred until
  primalSpring stabilizes the stub harness pattern

---

## Metrics

| Metric | v0.7.32 | v0.7.33 |
|--------|---------|---------|
| Tests | 1,522 | 1,536 |
| LOC | 54,255 | 54,565 |
| Methods | 35 | 36 |
| Clippy | 0 | 0 |
| Deep debt | 0 | 0 |

---

## Verification

```bash
cargo test --all-features    # 1,536 pass, 0 fail
cargo clippy --workspace --all-features --all-targets  # 0 warnings
```
