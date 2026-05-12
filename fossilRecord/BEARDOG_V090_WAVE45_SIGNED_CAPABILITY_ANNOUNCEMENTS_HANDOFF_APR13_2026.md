# BearDog v0.9.0 — Wave 45: Signed Capability Announcements Handoff

**Date**: April 13, 2026
**Primal**: BearDog
**Version**: 0.9.0
**Wave**: 45
**Upstream Gap**: "Signed capability announcements" (primalSpring Phase 41 gap registry, LOW priority)

---

## Summary

Implements cryptographically signed capability advertisements so that Songbird discovery and Neural API can verify primal authenticity in cross-family federations where socket-level access control is insufficient.

---

## Problem

BearDog had a `signed_announcement` field in `capabilities.list` since early waves, but it suffered from three issues:

1. **Separate identity key** — Announcements used a different Ed25519 key derivation (`"capability-announcement-key:"`) from ionic bonds (`"ionic-bond-identity-seed:"`), so verifiers saw two different public keys for the same primal.
2. **Unsorted methods** — The comment claimed sorted methods but the code signed registry enumeration order, making verification non-deterministic.
3. **Incomplete coverage** — `discover_capabilities` was unsigned, and neural `capability.register` had no attestation.

## Solution

### Unified Primal Identity Key

New `primal_signing` module provides a single derivation:
```
seed = SHA-256("primal-identity-key:" || primal_name || ":" || node_id)
signing_key = Ed25519.from_seed(seed)
```

All subsystems (capability announcements, ionic bonds, contract signing, neural registration) now share one keypair per runtime identity.

### Canonical Message (schema_version 2)

```
message = SHA-256(
    primal || ":" || version || ":" || sorted(methods).join(",")
)
signature = Ed25519.sign(signing_key, message)
```

Hash-then-sign ensures fixed 32-byte input. Methods are lexicographically sorted before hashing.

### Coverage

| Endpoint | Before | After |
|----------|--------|-------|
| `capabilities.list` | Signed (wrong key, unsorted) | Signed (unified key, sorted, schema v2) |
| `discover_capabilities` | Unsigned | Signed |
| `capability.register` (Neural API) | Unsigned | `signed_attestation` included |

---

## Files Modified

### New Files
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/primal_signing.rs` — Unified identity key derivation, signing, canonical message construction, 5 tests.

### Modified Files
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/mod.rs` — Register `primal_signing` module.
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` — Use unified key, canonical sorted message, add signature to `discover_capabilities`.
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/crypto.rs` — Delegate signing to unified `primal_signing`.
- `crates/beardog-ipc/src/neural_registration.rs` — Accept `signed_attestation` parameter, include in `capability.register` payloads.
- `crates/beardog-tunnel/src/modes/server.rs` — Compute and pass attestation to neural registration.
- `crates/beardog-cli/src/handlers/server.rs` — Compute and pass attestation to neural registration.
- `crates/beardog-ipc/src/neural_registration_comprehensive_tests.rs` — Updated for new parameter.
- `crates/beardog/src/neural_registration_extended_tests.rs` — Updated for new parameter.

### Ecosystem Files
- `infra/wateringHole/CAPABILITY_WIRE_STANDARD.md` — New "Signed Capability Announcements (SA-01)" section.

---

## Wire Standard SA-01 Summary

- `signed_announcement` object: `{schema_version, algorithm, public_key, signature, signed_fields}`
- Canonical message: `SHA-256(primal ":" version ":" sorted_methods_joined_by_comma)`
- Identity key: `SHA-256("primal-identity-key:" || name || ":" || node_id)`
- Verification: reconstruct canonical message from response fields, verify Ed25519

---

## Quality Gates

All clean:
- `cargo fmt --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — all passing, zero failures

---

## Upstream Gap Resolution

| Gap | Status | Notes |
|-----|--------|-------|
| Signed capability announcements (neuralSpring ask) | **RESOLVED** | Unified identity, canonical message, full coverage |
