<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 76 Handoff: primalSpring Phase 56 Gap Resolution

**Date**: April 29, 2026
**From**: BearDog Team
**To**: primalSpring, biomeOS, all consuming primals
**Audit source**: `primalSpring/docs/LIVE_DEPLOYMENT_GAP_REPORT_PHASE56.md`

---

## GAP-23 (P2): `crypto.blake3_hash` error on capability socket — RESOLVED

**Root cause**: Parameter encoding issue on the caller side, not a BearDog bug.

The capability socket (`crypto-desktop-nucleus.sock`) is a filesystem symlink to
`beardog-desktop-nucleus.sock`. BearDog receives the exact same JSON-RPC request
regardless of which socket name was used. The gap report itself confirms
"BearDog BLAKE3 hash | **PASS**" when called with correct parameters.

### Required wire format

```json
{"jsonrpc":"2.0","method":"crypto.blake3_hash","params":{"data":"aGVsbG8gd29ybGQ="},"id":1}
```

| Field | Requirement |
|-------|-------------|
| `params` | **JSON object** (not array, not null) |
| `data` | **Standard base64** string (RFC 4648, `+/=` alphabet) |

### Common caller errors that produce error responses

1. **`params` as positional array**: `["aGVsbG8="]` — BearDog expects `{"data": "aGVsbG8="}`.
2. **Raw UTF-8 instead of base64**: `{"data": "hello world"}` — BearDog decodes as base64, fails.
3. **Missing `data` key**: `{"input": "aGVsbG8="}` — the field must be named `data`.
4. **`params: null`** or omitted — BearDog requires params to be present.

### What we improved

Error messages now include format guidance:
- Missing params: `"expected: {\"data\": \"<standard-base64>\"}"` 
- Missing data: `"(standard base64 encoded string)"`
- Invalid base64: `"use standard base64 (RFC 4648, +/= alphabet)"`

### Semantic aliases

All three method names call the same handler:
- `crypto.blake3_hash` (canonical)
- `crypto.hash` (semantic alias → blake3)
- `beardog.crypto.blake3_hash` (backward-compat)

---

## IONIC-RUNTIME (P1): `crypto.sign_contract` — ALREADY RESOLVED (since Wave 42)

`crypto.sign_contract` has been wired and tested since Wave 42. The gap in
`PRIMAL_GAPS.md` is stale.

### Available methods

| Method | Purpose |
|--------|---------|
| `crypto.ionic_bond.propose` | Propose a bilateral bond (Ed25519 signed) |
| `crypto.ionic_bond.accept` | Accept and counter-sign a proposed bond |
| `crypto.ionic_bond.seal` | Seal an active bond (verify + finalize) |
| `crypto.ionic_bond.verify` | Verify bond signatures |
| `crypto.ionic_bond.revoke` | Revoke an active bond |
| `crypto.ionic_bond.list` | List all bonds |
| `crypto.sign_contract` | Sign arbitrary JSON terms with Ed25519 |
| `crypto.verify_contract` | Verify a contract signature |

### `crypto.sign_contract` wire format

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "crypto.sign_contract",
  "params": {
    "signer": "primal-name-or-agent-id",
    "terms": { "any": "JSON", "object": "as contract terms" },
    "context": "optional-context-string"
  },
  "id": 1
}
```

**Response:**
```json
{
  "terms_hash": "sha256-hex-of-canonical-json-terms",
  "signature": "standard-base64-ed25519-signature",
  "public_key": "standard-base64-ed25519-public-key",
  "signed_at": "2026-04-29T13:00:00Z"
}
```

**Verification:**
```json
{
  "jsonrpc": "2.0",
  "method": "crypto.verify_contract",
  "params": {
    "terms_hash": "sha256-hex-from-sign-response",
    "signature": "base64-from-sign-response",
    "public_key": "base64-from-sign-response"
  },
  "id": 2
}
```

### Terms canonicalization

`terms` JSON is serialized with **sorted keys** (canonical JSON), then SHA-256 hashed.
This means `{"b":1,"a":2}` and `{"a":2,"b":1}` produce the **same** `terms_hash`.
The signature covers the hex-encoded SHA-256 hash, not the raw JSON bytes.

---

## Capability Socket Model (context for GAP-17/18/19/22/23)

BearDog is agnostic to socket naming. Whether a client connects via
`beardog-desktop-nucleus.sock` or `crypto-desktop-nucleus.sock` (symlink),
BearDog receives identical JSON-RPC and applies identical routing.

All "error on capability socket" gaps (GAP-22, GAP-23) in the Phase 56 report
are **parameter encoding issues on the caller side**, not socket-routing
differences. The symlink model is correct — the fix belongs in the caller's
parameter serialization.

The long-term target (per the audit) is Neural API `capability.resolve` RPC
replacing filesystem symlinks. BearDog is ready for this — it advertises
196 methods via `discover_capabilities` and `rpc.methods`.

---

## CI Status

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo deny check` | 4/4 pass |
| `cargo test --workspace` | 0 new failures |
