# barraCuda v0.3.12 — Sprint 51b: Phase 3 Transport Switch Verification

**Date**: May 3, 2026
**Primal**: barraCuda
**Sprint**: 51b
**Trigger**: primalSpring Phase 3 audit — transport switch verification / interop gap

---

## Summary

Resolved the primalSpring audit finding: "Verify that after `btsp.negotiate` responds, the accept path enters the encrypted frame loop for all subsequent messages on that connection."

Two interop gaps identified and fixed:

### 1. BufReader Data Loss on Negotiate Transition

**Root cause**: `handle_connection` used `buf_reader.into_inner()` when switching to
encrypted framing. Tokio's BufReader reads ahead in 8KB chunks — any bytes already
buffered (e.g., a pipelined encrypted frame arriving immediately after the negotiate
line) were silently discarded.

**Fix**: Pass `buf_reader` directly to `handle_btsp_connection`. `BufReader<R>`
implements `AsyncRead`, preserving buffered data for the encrypted frame reader.

### 2. Missing `client_nonce` in HKDF Key Derivation

**Root cause**: HKDF salt was `server_nonce` only. Per BTSP spec, salt should be
`client_nonce || server_nonce` so both sides can derive identical session keys.

**Fix**: Extract `client_nonce` from negotiate params (hex-decode), concatenate with
server_nonce as HKDF salt. Backward-compatible — empty client_nonce degrades to
server_nonce-only (existing tests unchanged).

---

## Code Changes

| File | Change |
|------|--------|
| `crates/barracuda-core/src/ipc/transport.rs` | `buf_reader.into_inner()` → `buf_reader` (preserve buffered bytes); loop restructured to release BufReader borrow before move |
| `crates/barracuda-core/src/ipc/btsp.rs` | Extract `client_nonce` from params; HKDF salt = `client_nonce \|\| server_nonce`; `hex_decode` helper added; discovery functions extracted |
| `crates/barracuda-core/src/ipc/btsp_discovery.rs` | **NEW** — 117 lines extracted from btsp.rs (security-provider discovery resolution chain) |
| `crates/barracuda-core/src/ipc/btsp_tests.rs` | +2 tests: `client_nonce_affects_derived_key`, `same_client_nonce_same_server_nonce_yields_same_key` |
| `crates/barracuda-core/src/ipc/transport_tests.rs` | +2 integration tests: `negotiate_then_encrypted_frame_loop` (full e2e encrypted validation), `negotiate_pipelined_frame_not_lost` (BufReader preservation proof) |

---

## Wire Format (unchanged)

```
→ {"jsonrpc":"2.0","method":"btsp.negotiate","params":{"session_id":"...","preferred_cipher":"chacha20-poly1305","client_nonce":"<hex>"},"id":N}
← {"jsonrpc":"2.0","result":{"cipher":"chacha20-poly1305","server_nonce":"<hex>"},"id":N}
← [all subsequent messages: length-prefixed encrypted frames]
```

Key derivation: `HKDF-SHA256(IKM=handshake_key, salt=client_nonce||server_nonce, info="btsp-v1-phase3") → 32 bytes`

---

## Quality Gates

- `cargo fmt --all --check` ✓
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` ✓
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps` ✓
- `cargo deny check` ✓
- `cargo test -p barracuda-core --lib` — 292 pass (was 288; +4 new)
- All production files under 800 lines (btsp.rs 831→721)

---

## Ecosystem Note

The audit flagged "Same interop gap pattern found across the ecosystem on live validation."
Other primals using BufReader-to-binary transition patterns should verify their implementations
preserve buffered data on mode switch.
