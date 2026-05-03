# loamSpine v0.9.16 — BTSP Phase 3 + Dependency Security Fix

**Date**: May 2, 2026
**From**: loamSpine v0.9.16
**Responding to**: primalSpring Phase 56c — BTSP Phase 3 `btsp.negotiate`

---

## What Changed

### BTSP Phase 3 `btsp.negotiate` Handler (IMPLEMENTED)

New JSON-RPC method `btsp.negotiate` on the application socket. Returns
`cipher: "null"` (plaintext fallback) for all requests.

**Request format** (primalSpring Phase 3 compatible):

```json
{"jsonrpc":"2.0","method":"btsp.negotiate","params":{
  "session_id": "<from handshake>",
  "preferred_cipher": "chacha20-poly1305",
  "ciphers": ["chacha20-poly1305"],
  "client_nonce": "<base64>",
  "bond_type": "Covalent"
},"id":...}
```

**Response**: `{"cipher":"null"}`

**Why null cipher**: loamSpine delegates all crypto to the BTSP provider
(BearDog). It never holds `handshake_key` or derives session keys locally.
Full Phase 3 encrypted framing (ChaCha20-Poly1305 AEAD + HKDF) requires the
provider API to export session key material — this is new ground for the
ecosystem. The null cipher response is the correct posture: primalSpring
handles fallback gracefully, zero breakage.

**What this unblocks**: primalSpring's `negotiate_phase3()` receives
`cipher: "null"` instead of `-32601 Method not found`. The `#[ignore]`
integration tests can proceed past the negotiate step.

### Dependency Security Fix

- `hickory-proto` 0.26.0 → 0.26.1: RUSTSEC-2026-0119 (O(n²) name compression)
- `hickory-net` 0.26.0 → 0.26.1: RUSTSEC-2026-0120 (NSEC3 unbounded loop)
- `cargo deny check`: all pass clean

### Deep Debt Audit (CLEAN)

10-dimension audit performed same session — zero findings. Hardcoded
`"biomeos"` path literals (2 occurrences) replaced with `BIOMEOS_SOCKET_DIR`
constant in prior commit (April 30).

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,513 (all concurrent, zero flaky) |
| JSON-RPC methods | 38 (+1 `btsp.negotiate`) |
| Source files | 180 `.rs` |
| Max .rs file | 783L (test), 605L (production) |
| Clippy | Clean (pedantic + nursery) |
| cargo deny | Clean (0 advisories) |
| Unsafe | Forbidden |

---

## Phase 3 Evolution Path

When BearDog or the BTSP provider exposes session key material:

1. `btsp.negotiate` handler derives `SessionKeys` via HKDF-SHA256
2. Post-handshake I/O wraps `BufReader`/writer with AEAD framing
3. Wire format: `[4B len BE][12B nonce][ciphertext + Poly1305 tag]`
4. New deps: `chacha20poly1305`, `hkdf`, `sha2` (all RustCrypto, pure Rust)

Until then, authenticated plaintext (Phase 2 + null cipher) is the correct
posture for all primals.

---

*Ref: `LOAMSPINE_V0916_PROVENANCE_RECEIPTS_HANDOFF_APR30_2026.md` for prior session*
