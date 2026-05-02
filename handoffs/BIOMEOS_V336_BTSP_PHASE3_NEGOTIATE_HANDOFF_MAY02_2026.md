# biomeOS v3.36 — BTSP Phase 3: btsp.negotiate + Deep Debt Sweep

**Date**: May 2, 2026
**Author**: biomeOS team
**Scope**: BTSP Phase 3 cipher negotiation, stale comment purge

---

## Summary

biomeOS v3.36 implements `btsp.negotiate` server-side, making biomeOS the second primal
(after petalTongue) with Phase 3 cipher negotiation support. ChaCha20-Poly1305 and NULL
cipher fallback are both supported. This responds to the primalSpring Phase 57 audit
requesting all primals add `btsp.negotiate` server handlers.

Additionally, 14 remaining stale `EVOLVED` comments were purged across 8 crates.

---

## Changes

### BTSP Phase 3 — `btsp.negotiate` server handler

- **New module**: `biomeos-atomic-deploy/src/neural_api_server/btsp_negotiate.rs`
  - `BtspCipher` enum: `Null`, `ChaCha20Poly1305`
  - `BtspSessionState`: per-session state (session_id, negotiated cipher, server_nonce)
  - `BtspSessionStore`: `Arc<RwLock<HashMap<String, BtspSessionState>>>`
  - `register_session()`: called after Phase 2 handshake
  - `handle_negotiate()`: validates session, generates 12-byte server nonce, returns cipher

- **Route table**: Added `("btsp.negotiate", Route::BtspNegotiate)` to `ROUTE_TABLE`

- **Session registration**: `handle_connection_with_btsp()` now calls
  `register_session()` after `HandshakeOutcome::Authenticated`

- **`btsp.status` upgraded**: Now reports `"phase3_ready": true`,
  `"supported_ciphers": ["chacha20-poly1305", "null"]`, and `"active_sessions"` count

- **Workspace deps**: Added `chacha20poly1305 = "0.10"`, `hkdf = "0.12"` to workspace
  `Cargo.toml` and `biomeos-atomic-deploy/Cargo.toml`

- **Wire format**: `btsp.negotiate` accepts:
  ```json
  {"session_id": "<hex>", "preferred_cipher": "chacha20-poly1305", "bond_type": "Covalent"}
  ```
  Returns:
  ```json
  {"cipher": "chacha20-poly1305", "server_nonce": "<24-char hex>", "allowed": true}
  ```
  If cipher unsupported, returns `{"cipher": "null", ...}`.

### Stale EVOLVED comment purge (14 markers)

Removed across: `deployment_mode.rs`, `lib.rs` (biomeos-api), `config/mod.rs`,
`translation_loader.rs`, `node_handlers.rs`, `primal_impls.rs`, `cache.rs`,
`executor.rs`, `executor/core.rs`, `executor/types.rs`, plus 4 test files.

---

## Verification

- `cargo check`: PASS
- `cargo clippy -- -D warnings`: PASS (0 warnings)
- `cargo fmt --check`: PASS
- `cargo test -p biomeos-atomic-deploy -- btsp`: 14 passed (5 new + 9 existing)
- `cargo test --workspace`: 1,232 passed (2 pre-existing env-dependent failures)

---

## Phase 3 Evolution Path

This v3.36 implements negotiate + session store + cipher selection. The full
encrypted framing (length-prefixed AEAD frames replacing NDJSON) is the next step.
The infrastructure is in place:

1. Session store tracks negotiated cipher per connection
2. `chacha20poly1305` and `hkdf` crates are wired
3. Server nonce is generated and returned to client
4. Next: wrap `handle_stream` with AEAD frame reader/writer when cipher != null

primalSpring's `#[ignore]` integration tests (`phase3_negotiate_with_live_beardog`,
`phase3_transport_full_roundtrip`) should validate once the binary is deployed via
plasmidBin.

---

## Files Changed

| File | Change |
|------|--------|
| `Cargo.toml` (workspace) | Added `chacha20poly1305`, `hkdf` |
| `biomeos-atomic-deploy/Cargo.toml` | Added `sha2`, `hkdf`, `chacha20poly1305` |
| `neural_api_server/mod.rs` | Registered `btsp_negotiate` module, added `btsp_sessions` field |
| `neural_api_server/btsp_negotiate.rs` | **New** — session store, negotiate handler, tests |
| `neural_api_server/routing.rs` | Added `BtspNegotiate` route + dispatch |
| `neural_api_server/connection.rs` | Session registration after Phase 2 handshake |
| `neural_api_server/listeners.rs` | `btsp_status` → async, reports Phase 3 ready |
| 14 files across 8 crates | Stale `EVOLVED` comment removal |
| Root docs (5 files) | Version bumped to v3.36, date to May 2 2026 |
