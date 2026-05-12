# Songbird v0.2.1 — Wave 89–90 Deep Debt Evolution Handoff

**Date**: March 31, 2026  
**Version**: v0.2.1  
**Sessions**: 30–31 (Waves 88–90)  
**Previous**: `SONGBIRD_V021_WAVE89_PURE_RUST_QUIC_QUINN_ELIMINATION_HANDOFF_MAR30_2026.md`

---

## Summary

Deep debt execution across songbird-quic, TLS, orchestrator, discovery, and network-federation crates. Major themes: QUIC clippy clean (322→0 errors), frame.rs smart refactoring (1226→4 files), application-level crypto delegation to BearDog, mock isolation, environment modernization, and orchestrator lint hardening.

---

## What Changed

### songbird-quic: Clippy Clean + Frame Refactoring

- **`packet/frame.rs` refactored** (1226 lines → 4 modules):
  - `frame/mod.rs` (302 lines): Types, enum definition, frame_type constants
  - `frame/decode.rs` (387 lines): Decode with shared helpers (`decode_single_varint`, `decode_stream_data_pair`, `decode_path_data`)
  - `frame/encode.rs` (320 lines): Encode with shared helpers (`encode_varint_frame`, `encode_two_varint_frame`, `encode_path`)
  - `frame/tests.rs` (292 lines): All 25 roundtrip tests preserved
  - Public API unchanged: `songbird_quic::packet::frame::Frame` path identical
- **322 clippy errors → 0**: Fixed doc_markdown (90), use_self (46), missing_errors_doc (32), missing constant docs (17), cast_possible_truncation (38 with `#[expect(reason)]`), dead_code, unused vars, unnecessary_wraps, trivially_copy_pass_by_ref
- **All 178 tests pass**

### Application Crypto → BearDog Delegation

| Crate | Function | BearDog Method | Fallback |
|-------|----------|---------------|----------|
| `songbird-tls` | `encrypt_record_delegated` / `decrypt_record_delegated` | `crypto.aead_encrypt` / `crypto.aead_decrypt` | `TlsError::CryptoUnavailable` |
| `songbird-orchestrator` | `encode_with_crypto` / `decode_with_crypto` (JWT) | `crypto.hmac.sha256` | Local `hmac`+`sha2` + warn |
| `songbird-orchestrator` | `calculate_checksum` (checkpoints) | `crypto.sha256` | Local `sha2` + warn |
| `songbird-discovery` | `sha256_hash` / `sha256_hash_sync` | `crypto.sha256` | Local `sha2` + warn |
| `songbird-network-federation` | `sha256_hash` / `hmac_sha256` | `crypto.sha256` / `crypto.hmac.sha256` | Local `sha2`+`hmac` + warn |

Each crate has a `crypto_helpers.rs` (or equivalent) providing the dual-mode pattern. All fallbacks emit `tracing::warn!` so silent mock crypto is eliminated.

### Mock Isolation

- `MockRendezvousClient`, `MockPeerConnector`, `MockPeerRegistry` in `songbird-universal-ipc` moved from module-level `#[cfg(test)]` into `#[cfg(test)] mod tests_support {}` — no longer re-exported via `pub use handler::*`
- TLS record layer returns `TlsError::CryptoUnavailable` when BearDog is not connected, instead of mock XOR

### Environment Modernization

- `std::env::var` → `songbird_process_env::var` in 3 production files:
  - `songbird-cli/src/cli/config.rs` (`EDITOR`)
  - `songbird-cli/src/cli/commands/tower.rs` (`SONGBIRD_BIND_ADDRESS`)
  - `songbird-config/src/config/hardcoded_elimination.rs` (`HOME`)

### Orchestrator Lint Hardening

- `unwrap_used` / `expect_used` lint levels: `"allow"` → `"warn"` in Cargo.toml
- `ProcessManager::default` uses `#[expect(clippy::expect_used, reason = "...")]`

### Crypto Provider RPC Cleanup

- Merged duplicate match arms in `method_to_capability` and `semantic_to_actual` for AEAD encrypt/decrypt aliases

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| songbird-quic clippy errors | 322 | 0 |
| Files >1000 lines | 1 (`frame.rs`) | 0 |
| BearDog crypto delegation sites | 6 stubs | 6 stubs + 5 new delegation paths (TLS, JWT, checkpoint, discovery, rendezvous) |
| Mock types in production re-exports | 3 | 0 |
| `std::env::var` in production | 8+ | 3 (test-only remainder) |
| Orchestrator `unwrap_used`/`expect_used` lint | `allow` | `warn` |
| Workspace compilation | Clean | Clean |
| Clippy (modified crates) | Clean | Clean |

---

## Build Verification

- `cargo check --workspace` — Clean
- `cargo fmt --all -- --check` — Clean
- `cargo clippy -p songbird-quic ... -p songbird-crypto-provider -- -D warnings` — Clean (9 crates)
- `cargo doc --no-deps` — Clean
- `cargo test -p songbird-quic` — 178 passed
- `cargo test -p songbird-tls -p songbird-universal-ipc -p songbird-crypto-provider` — All pass

---

## Remaining (songbird-specific)

1. **sled → nestGate storage.* IPC**: Orchestrator task lifecycle and consent storage still use embedded sled; evolution pending nestGate storage API availability
2. **songbird-quic header.rs** (583 lines): Under 1000 limit but could benefit from module split for header types vs codec
3. **Coverage**: ~69% → 90% target; primary gaps in integration/e2e paths
4. **`ring-crypto` feature gate**: Rustls ring provider still opt-in on CLI; pending upstream `rustls-rustcrypto` in quinn ecosystem
5. **Placeholder comments**: ~50 "Week N" and "placeholder" references across orchestrator, bluetooth, and tor-protocol crates — editorial cleanup only, no behavioral impact
