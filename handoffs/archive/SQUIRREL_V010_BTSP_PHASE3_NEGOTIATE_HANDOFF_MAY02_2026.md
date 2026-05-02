<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — BTSP Phase 3 `btsp.negotiate` Server Handler (May 2, 2026)

## Session: AT — primalSpring Phase 56c Audit Resolution

### What was done

Implemented the **`btsp.negotiate` JSON-RPC method handler** — the server-side
half of BTSP Phase 3 encrypted channel negotiation. This resolves the
primalSpring audit item "BTSP Phase 3: `btsp.negotiate` server-side" for
Squirrel.

### Implementation details

| Component | Change |
|-----------|--------|
| `crates/main/src/rpc/handlers_btsp.rs` | NEW — handler validates `session_id`, logs preferred_cipher/bond_type, returns negotiated cipher |
| `crates/main/src/rpc/jsonrpc_dispatch.rs` | Added `"btsp.negotiate"` dispatch arm |
| `crates/main/src/rpc/jsonrpc_server.rs` | Added `btsp_sessions: Arc<DashMap<String, BtspSession>>` field; populates on successful Phase 2 handshake in `accept_with_btsp` |
| `crates/main/src/rpc/tarpc_service.rs` | `BtspNegotiateParams`, `BtspNegotiateResult` types + `btsp_negotiate` trait method |
| `crates/main/src/rpc/tarpc_server.rs` | `btsp_negotiate` implementation delegating to JSON-RPC handler |
| `crates/main/src/niche.rs` | `btsp` group description, `btsp.negotiate` in `COST_ESTIMATES`, `cost_estimates_json`, `operation_dependencies` |
| `crates/universal-constants/src/capabilities.rs` | `"btsp.negotiate"` in `SQUIRREL_EXPOSED_CAPABILITIES` |
| `capability_registry.toml` | Full schema entry for `btsp_negotiate` |

### Current behavior

- **Phase 2 handshake** (unchanged): Completes with `cipher: "null"`, session stored.
- **`btsp.negotiate` call**: Validates session_id → returns `{"cipher":"null"}`.
- **primalSpring fallback**: Client receives null cipher, stays on authenticated plaintext. Zero breakage.

### Evolution path to encrypted framing

When ready to activate ChaCha20-Poly1305:
1. Add `chacha20poly1305`, `hkdf`, `sha2` crate dependencies
2. In `handle_btsp_negotiate`: generate 12-byte server_nonce, derive keys via HKDF-SHA256
3. Return `{"cipher":"chacha20-poly1305","server_nonce":"<hex>"}`
4. Switch transport to encrypted framing: `[4B len BE u32][12B nonce][ciphertext + Poly1305 tag]`

### Tests

3 new tests:
- `negotiate_requires_session_id` — rejects missing params
- `negotiate_rejects_unknown_session` — rejects sessions not from Phase 2
- `negotiate_returns_null_cipher_for_valid_session` — confirms null cipher response

### Quality gates

| Check | Result |
|-------|--------|
| `cargo fmt` | PASS |
| `cargo clippy` | 0 warnings |
| `cargo test` | 7,192 passing / 0 failures |
| `cargo deny` | advisories ok, bans ok, licenses ok, sources ok |

### References

- petalTongue reference: `crates/petal-tongue-ipc/src/btsp/json_line.rs` lines 200-223
- primalSpring client: `ecoPrimal/src/ipc/btsp_handshake.rs` `negotiate_phase3()`
- Wire format: `wateringHole/UPSTREAM_CROSSTALK_AND_DOWNSTREAM_ABSORPTION.md` "BTSP Three-Phase Genetics"
