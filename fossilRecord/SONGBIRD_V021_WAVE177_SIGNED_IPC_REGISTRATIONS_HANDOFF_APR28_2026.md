# Songbird v0.2.1 — Wave 177: Signed IPC Registrations

**Date**: April 28, 2026
**Trigger**: primalSpring v0.9.20 Phase 55 audit
**Status**: Complete

---

## Summary

`ipc.register` payloads are now cryptographically signed via BearDog Ed25519 delegation when `FAMILY_ID` is set. Consumers calling `ipc.resolve`, `ipc.discover`, or `capability.resolve` receive `signature` and `signed_payload` fields they can verify via `crypto.verify.ed25519`.

## What Changed

### Wire Protocol

All registration-related JSON-RPC responses now include two new optional fields:

- `signature` — base64-encoded Ed25519 signature (via `crypto.sign.ed25519`)
- `signed_payload` — canonical JSON that was signed

Both are `null`/omitted in standalone mode (no `FAMILY_ID`).

### Canonical Payload Format

Deterministic JSON with alphabetical short keys:

```json
{"c":["sorted","capabilities"],"e":"endpoint","p":"primal_id","t":"registered_at_rfc3339"}
```

### Signing Flow

1. `IpcServiceHandler` constructs `CryptoProvider` at startup if `FAMILY_ID` is set
2. On `ipc.register`: build canonical payload → base64-encode → `crypto.sign.ed25519` via BearDog
3. Store `signature` + `signed_payload` in `ServiceEntry`
4. Surface both on all resolution responses

### Graceful Degradation

When `FAMILY_ID` is absent (standalone/dev mode), the crypto provider is `None`, registrations proceed unsigned, and signature fields are omitted from JSON responses.

## Files Modified

| File | Change |
|------|--------|
| `crates/songbird-universal-ipc/src/service_types.rs` | Added `signature`/`signed_payload` to `RegisterResult`, `ResolveResult`, `ProviderInfo`, `CapabilityResolveResult` |
| `crates/songbird-universal-ipc/src/registry.rs` | Added fields to `ServiceEntry`, `ServiceMetadata`; updated `register()` signature |
| `crates/songbird-universal-ipc/src/service/mod.rs` | Added `crypto_provider: Option<Arc<CryptoProvider>>` field |
| `crates/songbird-universal-ipc/src/service/construction.rs` | `build_crypto_provider()` from env; wired into all constructors |
| `crates/songbird-universal-ipc/src/service/ipc_registry.rs` | `build_canonical_payload()`, `sign_payload()`, updated `handle_register`/`handle_resolve`/`handle_discover`/`handle_capability_resolve` |
| `crates/songbird-universal-ipc/Cargo.toml` | Added `songbird-crypto-provider` dependency |
| `docs/ENVIRONMENT_VARIABLES.md` | Updated `FAMILY_ID` description to note signing behavior |

## Validation

- 0 clippy warnings (`-D warnings`)
- 7,692 lib tests pass (9 new)
- `cargo fmt` clean

## Out of Scope (Noted as Remaining Work)

1. **Identity verification before accepting registrations** — probing registering primal via `identity.get` + BearDog BTSP verification
2. **Purpose key derivation** — using BearDog's Ed25519 signing key directly; purpose key derivation is a BearDog-side evolution

## For Downstream (primalSpring)

Consumers can now verify registration authenticity:

```json
// ipc.resolve response
{
  "virtual_endpoint": "/primal/beardog",
  "native_endpoint": "/run/user/1000/biomeos/beardog-nucleus01.sock",
  "capabilities": ["crypto", "security"],
  "signature": "<base64 Ed25519 signature>",
  "signed_payload": "{\"c\":[\"crypto\",\"security\"],\"e\":\"/run/user/1000/biomeos/beardog-nucleus01.sock\",\"p\":\"beardog\",\"t\":\"2026-04-28T14:30:00Z\"}"
}
```

Verify via: `crypto.verify.ed25519({ "data": base64(signed_payload), "signature": signature })`
