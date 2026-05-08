# loamSpine v0.9.16 — BTSP Phase 3 Transport Switch VERIFIED

**Date**: May 3, 2026
**From**: loamSpine v0.9.16
**Responding to**: primalSpring Phase 3 transport switch verification request — "verify that after `negotiate_btsp` returns `cipher: "chacha20-poly1305"`, the accept path enters `read_encrypted_frame`/`write_encrypted_frame` for subsequent messages"

---

## Summary

The BTSP Phase 3 transport switch is **VERIFIED AND WIRED** into the UDS
accept loop. After a successful `btsp.negotiate` that returns
`cipher: "chacha20-poly1305"`, the server enters `handle_encrypted_stream`
for all subsequent JSON-RPC messages on that connection. The ionic bond
blocker is **RESOLVED**.

## What Changed (Transport Switch)

### `jsonrpc/uds.rs` — Post-Handshake Flow

New function chain wired into the UDS accept loop after BTSP Phase 2 handshake:

1. **`handle_post_handshake()`** — Entry point after any successful BTSP handshake.
   Registers the `handshake_key` from `BtspSession` with the RPC service.
   Reads the first JSON-RPC line (expected `btsp.negotiate`). Processes it
   in plaintext. If the response contains `cipher: "chacha20-poly1305"`,
   derives `SessionKeys` and switches to encrypted streaming.

2. **`extract_negotiate_client_nonce()`** — Parses the `btsp.negotiate`
   request to extract the base64-encoded `client_nonce`.

3. **`try_derive_phase3_keys()`** — Extracts `server_nonce` from the
   plaintext negotiate response, then derives `SessionKeys` via
   HKDF-SHA256 (`is_server=true`).

4. **`handle_encrypted_stream()`** — The encrypted message loop.
   Reads length-prefixed encrypted frames via `read_encrypted_frame()`,
   decrypts, dispatches as JSON-RPC, encrypts the response via
   `write_encrypted_frame()`, writes back as encrypted frame.

### Connection Flow

```
Client connects → BTSP Phase 2 handshake (4-step) → BtspSession with handshake_key
  → handle_post_handshake()
    → register handshake_key in session registry
    → read first line: btsp.negotiate { session_id, preferred_cipher, client_nonce }
    → process_request() returns { cipher: "chacha20-poly1305", server_nonce }
    → write plaintext response back to client
    → try_derive_phase3_keys() → SessionKeys
    → IF chacha20-poly1305:
        → handle_encrypted_stream() ← ALL subsequent messages encrypted
    → ELSE (null cipher):
        → handle_stream_buffered() ← plaintext as before
```

### Wire Format (Post-Negotiate)

```
[4 bytes: length (big-endian u32)] [12 bytes: nonce] [ciphertext + 16-byte Poly1305 tag]
```

## Tests Added

4 new integration tests in `tests_phase3_transport.rs` using
`UnixStream::pair()` for realistic IPC simulation:

| Test | What It Verifies |
|------|-----------------|
| `phase3_transport_switch_encrypted_roundtrip` | After negotiate returns `chacha20-poly1305`, a `health.check` round-trip succeeds via encrypted frames |
| `phase3_multiple_encrypted_requests` | Multiple sequential encrypted request/response pairs work correctly |
| `phase3_no_key_stays_plaintext` | Without a handshake key, connection remains plaintext |
| `phase3_negotiate_null_stays_plaintext` | With an unregistered session, negotiate returns `null` cipher and plaintext continues |

## Prior Phase 3 Work (Preserved)

All Phase 3 crypto primitives from the May 2 handoff remain unchanged:

- `btsp/phase3.rs` — `SessionKeys`, HKDF derivation, ChaCha20-Poly1305 AEAD, encrypted frame I/O
- Pattern B key acquisition — `session_key` from BearDog `btsp.session.verify`
- Graceful null cipher degradation for unauthenticated covalent bonds
- 5 RustCrypto dependencies (all pure Rust, deny clean)

## Bond Compliance (Unchanged)

| Bond Type | Min Cipher | loamSpine |
|-----------|-----------|-----------|
| Covalent | Null | **PASS** (null fallback) |
| Metallic | HmacPlain | **PASS** (via Tower) |
| Ionic | ChaCha20Poly1305 | **PASS** (Phase 3 FULL + transport verified) |
| Weak | ChaCha20Poly1305 | **PASS** (Phase 3 FULL + transport verified) |

## Deep Debt Audit (CLEAN)

10-dimension audit — zero findings:

| Dimension | Status |
|---|---|
| TODO/FIXME/HACK | Zero |
| Mocks in production | Zero (all cfg-gated) |
| Hardcoded primal names | Zero in production |
| Large files (>800L prod) | Zero (max 605L) |
| Unsafe code | Forbidden |
| `Result<_, String>` | Zero in production |
| `#[allow]` audit | 2 justified (feature-conditional) |
| Dead code | 2 justified |
| Dependencies | All RustCrypto pure Rust, deny clean |
| Security advisories | Zero |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,490 (all concurrent, zero flaky) |
| JSON-RPC methods | 38 |
| Source files | 180+ `.rs` |
| Max .rs file | 807L (test), 605L (production) |
| Clippy | Clean (pedantic + nursery) |
| cargo deny | Clean (0 advisories) |
| Unsafe | Forbidden |

---

## primalSpring Phase 58 Audit Response (May 4, 2026)

| Audit Item | Priority | Resolution |
|-----------|----------|------------|
| Phase 3 transport encryption | HIGH | **VERIFIED** — transport switch wired in `45de0cd` (May 3). After `negotiate_btsp` returns `chacha20-poly1305`, UDS accept loop enters `handle_encrypted_stream` using `read_encrypted_frame`/`write_encrypted_frame`. 4 integration tests confirm. Doc comment fixed (8→16 MiB guard alignment with `MAX_FRAME_SIZE`). |
| `ring` lockfile ghost | LOW | **COSMETIC ONLY** — `cargo tree -i ring` returns nothing. `ring` is an optional dep of `hickory-proto` (DNSSEC feature, not activated). `cargo deny check` passes (`bans ok`). Cannot be removed from `Cargo.lock` without upstream `hickory` changes. |
| `sled` lockfile ghost | LOW | **FALSE POSITIVE** — `sled` is NOT in `Cargo.lock`. `sled` was removed during stadial compliance (memory + redb only). |
| 178 source files | LOW | **NO ACTION NEEDED** — actual count is 182: 97 production `src/`, 73 test, 10 examples, 2 benches. Zero production files under 30 lines. Smallest is 35L (`storage_ext.rs`). No consolidation candidates. |

---

*Ref: `archive/LOAMSPINE_V0916_BTSP_PHASE3_FULL_CHACHA20_HANDOFF_MAY02_2026.md` for Phase 3 crypto implementation details*
*Ref: `wateringHole/CRYPTO_CONSUMPTION_HIERARCHY.md` for the ecosystem cipher standard*
