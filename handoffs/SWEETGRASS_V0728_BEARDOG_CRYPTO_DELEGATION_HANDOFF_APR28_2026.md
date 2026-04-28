# sweetGrass v0.7.28 — BearDog Crypto Signing Delegation

**Date**: April 28, 2026
**Primal**: sweetGrass (Nest — Provenance/Attribution)
**Triggered by**: primalSpring Phase 55 — `NUCLEUS_TWO_TIER_CRYPTO_MODEL`

## Summary

Braid signing is now delegated to BearDog's `crypto.sign` Ed25519 over UDS
JSON-RPC. Braids created via `braid.create` carry Tower-level provenance
witnesses when BearDog is reachable, falling back to unsigned (`tier: "open"`)
witnesses when BearDog is unavailable.

## What Changed

### New Module: `crypto_delegate.rs`
- UDS JSON-RPC client for BearDog `crypto.sign` / `crypto.verify`
- Socket resolution: `BEARDOG_SOCKET` → `SECURITY_PROVIDER_SOCKET` →
  `BIOMEOS_SOCKET_DIR/security.sock` → `XDG_RUNTIME_DIR/biomeos/security.sock`
- Base64 wire encoding per `CRYPTO_WIRE_CONTRACT.md`

### New Witness Constructor: `Witness::from_tower_ed25519`
- Sets `tier: "tower"` (distinguishes from `tier: "local"` for same-gate signing)
- Agent DID constructed from BearDog's Ed25519 public key (`did:key:z6Mk...`)

### New Environment Constants
- `BEARDOG_SOCKET` — direct path to BearDog crypto socket
- `DISCOVERY_SOCKET` — Songbird discovery service socket

### Handler Evolution: `braid.create`
- After `factory.from_hash()`, computes `braid.compute_signing_hash()` (SHA-256)
- Calls `crypto.sign(base64(signing_hash))` via `CryptoDelegate`
- On success: `braid.witness = Witness::from_tower_ed25519(did, sig_bytes)`
- On failure: logs warning, leaves braid with `Witness::unsigned()` (current default)

### Bootstrap
- `CryptoDelegate::resolve()` runs at startup in Phase 4b
- Info-level log on success/unavailability

### New DID Constructor: `Did::from_public_key_bytes`
- Constructs `did:key:z6Mk{base64url(public_key)}` from raw bytes

## Test Coverage

- **6 unit tests** in `crypto_delegate::tests` (roundtrip, unavailable, error
  response, env resolution x3)
- **1 UDS integration test** (`test_uds_braid_create_tower_signed`) with mock
  BearDog — verifies `witness.kind == "signature"`, `witness.tier == "tower"`,
  `witness.algorithm == "ed25519"`, non-empty evidence, `did:key:z6Mk` agent
- **Total**: 1,461 tests passing, zero failures

## What Did NOT Change

- `Witness::unsigned()` and `Witness::from_ed25519()` — untouched
- tarpc-based `SigningBackend` — separate high-throughput path
- `braid.query`, `braid.get`, `provenance.graph` — read-only, unaffected
- BTSP module — transport security, separate concern
- Braids without BearDog remain valid (unsigned is the prior standard)

## Wire Format

```json
// Request → BearDog
{"jsonrpc":"2.0","method":"crypto.sign","params":{"message":"<base64>"},"id":1}

// Response ← BearDog
{"jsonrpc":"2.0","id":1,"result":{"signature":"<base64>","algorithm":"ed25519","public_key":"<base64>"}}
```

## Anchor Signing (Phase 55b)

Per primalSpring v0.9.21 Phase 55b, `anchoring.anchor` now also delegates
signing to BearDog. Anchor preparation responses carry Tower-signed Ed25519
witnesses bound to the `(braid, spine)` pair via `compute_anchor_preimage`.
Same graceful degradation as `braid.create`.

### Hash Delegation — Deferred

`crypto.hash` in the BearDog wire standard is BLAKE3, not SHA-256.
Delegating would change the hash algorithm, breaking backward compatibility.
The signing preimage is deterministic (no secret material) — no security
benefit to delegation. The Ed25519 signature IS the audit trail. If BearDog
ships `crypto.sha256.hash` and there is a concrete audit requirement, it
can be added later as a one-line change.

## Metrics

- `.rs` files: 187
- Tests: 1,462 (was 1,454)
- Clippy: zero warnings (`pedantic` + `nursery`)
- `unsafe`: none
