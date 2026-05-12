# Songbird v0.2.1 — Waves 131–133 Handoff

**Date**: April 9, 2026
**Primal**: Songbird (Network Orchestration & Discovery)
**Waves**: 131 (Hardcoded Elimination), 132 (BTSP Phase 2), 133 (Deep Debt Sweep)
**Status**: All 30 crates fmt clean, clippy pedantic+nursery zero warnings, doc zero warnings, cargo-deny passing, 7,265+ lib tests pass (0 failures)

---

## Wave 132 — BTSP Phase 2: Server Handshake on UDS Accept

**Ecosystem blocker resolved.** Songbird is the first consumer primal (after BearDog) to enforce BTSP handshake on its UDS accept path.

### Implementation

- `perform_server_handshake()` in `crates/songbird-orchestrator/src/ipc/btsp.rs`
  - Wire types: `ClientHello`, `ServerHello`, `ChallengeResponse`, `HandshakeComplete`, `HandshakeError`
  - Length-prefixed framing: 4-byte big-endian length prefix per `BTSP_PROTOCOL_STANDARD.md` v1.0
  - 4-step handshake: ClientHello → session.create RPC → ServerHello → ChallengeResponse → session.verify RPC → HandshakeComplete
  - Crypto delegated to security provider via `SecurityRpcClient::btsp_session_create/verify/negotiate`

- `crates/songbird-http-client/src/security_rpc_client/btsp.rs`
  - `btsp_session_create()`, `btsp_session_verify()`, `btsp_negotiate()` RPC methods
  - Wire types: `BtspSessionCreated`, `BtspSessionVerified`, `BtspNegotiation`, `BtspCipher`

- `connection.rs` accept loop: `FAMILY_ID`-gated
  - When `FAMILY_ID` set: BTSP handshake required → length-prefixed JSON-RPC
  - When unset (dev mode): raw newline-delimited JSON-RPC (unchanged)

- `getrandom` added for challenge generation

### primalSpring Audit Resolutions

- **SB-02** (ring ghost in lockfile): Confirmed lockfile-only via optional `k8s` feature. Zero in default builds. `deny.toml` bans it.
- **SB-03** (sled default-on): Confirmed already resolved — feature-gated, non-default since Wave 120.
- **Wire Standard L3**: Confirmed clean.

---

## Wave 133 — Deep Debt Sweep

### Smart Refactoring (4 largest production files)

| Original | Size | → Modules | Max Module |
|----------|------|-----------|------------|
| `ipc/types.rs` | 778L | 7 (`p2p_discovery`, `genetic_tunnel`, `capabilities`, `service_registry`, `time`, `tests`) | 387L |
| `env_config.rs` | 764L | 9 (`btsp`, `identity`, `socket`, `paths`, `security_ipc`, `http`, `dark_forest`, `tests`) | 290L |
| `rpc/tarpc_server.rs` | 702L | 3 (`dispatch`, `accept` macro) | 345L |
| `task_lifecycle/manager.rs` | 711L | 6 (`events`, `storage`, `ops`, `cleanup`, `tests`) | 281L |

All public APIs re-exported from `mod.rs` — zero downstream breakage.

### Lint Migration

- `#[allow(` → `#[expect(` for specific production lints in orchestrator, network-federation, universal-ipc, config `lib.rs` files
- Crate-root `#[allow]` blocks remain where `#[expect]` causes unfulfilled-expectation errors

### Dependency Cleanup

- `parking_lot` removed from workspace (unused since Wave 129)
- `colored` bumped 2.0 → 3.1 (deduplicates with mockito transitive)

### T3 Domain Symlink

- `create_domain_socket_symlink()`: `network.sock` → `songbird.sock` on bind
- `remove_domain_socket_symlink_if_matches()`: cleanup on shutdown

### PII Scan

- 88 hits across codebase: all domain terms (email enum, password config field, crypto keys)
- Documented as false positives — no real PII exposure

---

## Wave 131 — Hardcoded Elimination

- `consul_adapter.rs`: silent localhost fallback → `Result`-based error propagation
- `InterfaceConfig::default()`: `LOCALHOST` → `UNSPECIFIED` (env-configurable via `SONGBIRD_BIND_ADDRESS`)
- Dark Forest beacon `0.0.0.0` fallback removed
- Federation ports → `songbird_types::defaults::ports` with env overrides
- `primal_discovery.rs`: 4-way endpoint duplication → `resolve_capability_endpoint_with` helper (797→760L)

---

## Compliance Matrix Impact (v2.6.0)

| Tier | Before | After | Key Change |
|------|--------|-------|------------|
| T1 Build | B | **A** | fmt PASS, commented-out code PASS |
| T3 IPC | B | **A** | Domain symlink PASS |
| T4 Discovery | D | **C** | Socket naming PASS |
| T8 Presentation | C | **B** | PII scan PASS (documented false positives) |
| **Rollup** | **B** | **A** | 4 tier upgrades |

---

## Remaining Work

1. **Coverage**: 72.29% → 90% target (pure-logic module expansion)
2. **BTSP Phase 3**: Cipher negotiation + encrypted framing (ChaCha20-Poly1305)
3. **Discovery debt**: 935 primal-name refs / 178 files (strongest trajectory but highest absolute)
4. **Security provider e2e**: Tor/TLS stubs blocked on live security provider
5. **NestGate storage e2e**: `storage.*` IPC endpoints needed for validation
