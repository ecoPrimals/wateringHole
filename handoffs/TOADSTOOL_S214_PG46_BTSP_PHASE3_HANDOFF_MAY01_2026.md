# ToadStool S214 — PG-46 Resolution + BTSP Phase 3 Assessment

**From**: toadStool compute team
**Date**: 2026-05-01
**Session**: S214
**Context**: Downstream audit from primalSpring Phase 56 identified PG-46 (slow initial socket response). Resolved + Phase 3 readiness assessed.

---

## 1. PG-46: Slow Initial Socket Response — RESOLVED

### Root Cause

The JSON-line BTSP handshake relay opened **two separate UDS connections** to BearDog — one for `btsp.session.create` and another for `btsp.session.verify`. This violated `SOURDOUGH_BTSP_RELAY_PATTERN.md` §Part 2 ("Write to BearDog socket — **same connection**"). Combined with per-RPC timeouts (3s × 2 = 6s) racing against the 5s overall handshake budget, clients with <10s timeouts would hit timeout or empty responses.

### Fix (3 changes)

1. **Connection reuse** — Added `ConnectedJsonRpcClient` (`crates/core/common/src/unix_jsonrpc_client.rs`). Both BearDog RPCs now share a single UDS connection, eliminating one full connect cycle.

2. **Timeout alignment** — `BTSP_RPC_TIMEOUT` reduced from 3s to 2s. Two sequential RPCs (2+2=4s) now fit within the 5s handshake budget with 1s margin. Overridable via `BTSP_RPC_TIMEOUT_SECS` env var.

3. **Timing instrumentation** — Added `Instant`-based `tracing::debug` spans for:
   - BearDog connect latency
   - `btsp.session.create` RPC latency
   - `btsp.session.verify` RPC latency
   - Total handshake duration

### Additional: Configurable Socket Permissions

Socket mode now reads `TOADSTOOL_SOCKET_MODE` env var (octal string, e.g. `"0660"`). Default remains `0600` (owner-only). Set to `0660` for group-accessible deployments where biomeOS/primalSpring runs as the same group.

### Expected Behavior After Fix

| Client timeout | Before fix | After fix |
|---------------|------------|-----------|
| 3s | Failure (handshake exceeds budget) | Possible — depends on BearDog latency |
| 5s | Failure (6s RPC race) | Success — 4s max RPC + margin |
| 10s | Success | Success |

---

## 2. BTSP Phase 3 Readiness Assessment

| Requirement | Status | Detail |
|---|---|---|
| **ECDH X25519 key exchange** | **Implemented** | Client + server: `x25519-dalek` ephemeral keypairs + HKDF-SHA256 session key derivation. Matches `BTSP_PROTOCOL_STANDARD.md` §Handshake. |
| **Cipher negotiation** | **Partial** | Wire shape exists (`preferred_cipher` / `cipher`), but: server accepts client preference verbatim (no intersection/policy); **AES-256-GCM not in `BtspCipher` enum** or JSON-line parsing. |
| **Stream wrapping** | **Not implemented** | `BtspFrameReader`/`BtspFrameWriter` use plaintext framing. `SessionKeys` derived but **unused** post-handshake. No AEAD encrypt/decrypt layer on frames. |

### Dependencies already available

`chacha20poly1305`, `x25519-dalek`, `hkdf`, `sha2`, `hmac` — all in workspace and gated behind `btsp` feature in `toadstool-common`. `aes-gcm` is in workspace but not yet added to `toadstool-common`.

### Phase 3 integration path

Per primalSpring Phase 56 guidance: "We'll provide a reference implementation via sourDough scaffold once BearDog lands the client-side negotiation." ToadStool is **ready to absorb** — ECDH plumbing in place, frame reader/writer ready for wrapping. When sourDough provides the AEAD adapter:

1. Add `aes-gcm` to `toadstool-common` `btsp` feature
2. Add `Aes256Gcm` variant to `BtspCipher` enum + JSON-line parser
3. Implement `EncryptedFrameReader`/`EncryptedFrameWriter` wrapping `SessionKeys`
4. Wire into post-handshake frame loop in `unix.rs` and `jsonrpc_server.rs`

---

## 3. Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy` | 0 warnings |
| `cargo fmt` | 0 violations |
| `cargo deny check bans` | Passes |
| `cargo test --workspace` | **22,423 pass, 0 fail** |
| Edition 2024 | Yes |
| `async-trait` eliminated | Yes (banned in `deny.toml`) |
| BTSP Phase 2 operational | Yes — PG-46 resolved |

---

## 4. Debris Cleanup (S214)

- Removed orphan bench files (`crates/testing/benches/hot_paths.rs`, `crates/runtime/secure_enclave/benches/performance.rs`) — no `[[bench]]` targets
- Removed unused `rmp-serde` workspace dependency
- Fixed stale WebSocket references in `crates/server/src/lib.rs` and `crates/client/src/lib.rs` doc headers
- Unified `examples/Cargo.toml` `temp-env` to `{ workspace = true }`
- Updated root docs: `DEBT.md`, `CHANGELOG.md`, `NEXT_STEPS.md`, `CONTEXT.md`, `DOCUMENTATION.md`

---

## 5. For primalSpring

PG-46 is resolved. Recommended minimum client timeout: **5 seconds** (covers 2× RPC + margin). The `BTSP_HANDSHAKE_TIMEOUT_SECS` env var on the toadStool side defaults to 5s and can be tuned.

For Phase 3: we're ready to absorb the sourDough AEAD scaffold when it lands.

---

**License**: AGPL-3.0-or-later
