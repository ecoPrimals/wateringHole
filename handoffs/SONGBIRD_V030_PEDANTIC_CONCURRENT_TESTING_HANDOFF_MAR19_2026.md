# Songbird v0.3.0 Handoff — Pedantic Clippy + Concurrent Testing Evolution

**Primal**: Songbird (Network Orchestration & Discovery)  
**Date**: March 19, 2026  
**Version**: v0.3.0  
**License**: AGPL-3.0 (scyBorg provenance trio)

---

## Session Summary

This session executed a comprehensive deep debt audit and evolution of the Songbird codebase, focusing on three pillars: pedantic clippy compliance, concurrent test evolution, and root documentation cleanup.

---

## What Changed

### 1. Clippy Pedantic + Nursery (1,565 → 399 errors, 74% reduction)

23 of 27 crates now pass `clippy::pedantic` + `clippy::nursery` with `-D warnings`. Systematic patterns fixed across the workspace:

| Pattern | Count | Description |
|---------|-------|-------------|
| `#[must_use]` | ~80 | Added to all pure functions returning values |
| `const fn` | ~30 | Converted applicable functions |
| Inlined format args | ~50 | `format!("{}", x)` → `format!("{x}")` |
| Doc markdown | ~40 | Backtick-wrapped types in doc comments |
| `# Errors` sections | ~25 | Added to fallible public functions |
| `map_or` / `map_or_else` | ~15 | Replaced `option_if_let_else` |
| `significant_drop_tightening` | ~10 | Resolved drop order warnings |

**4 crates remaining**: `songbird-http-client` (172), `songbird-sovereign-onion` (168), `songbird-tor-protocol` (54), `songbird-quic` (1)

### 2. Concurrent Testing Evolution

Eliminated all `sleep`-based synchronization and `#[serial]` test attributes (except legitimate chaos tests):

- **Readiness signals**: Replaced `tokio::time::sleep` after server startup with `tokio::sync::oneshot` channels in relay, TLS fault injection, and XDG discovery tests
- **Injectable environments**: Introduced `_from_map(env: &HashMap<String, String>)` variants for timeout and config functions, replacing `std::env::set_var` global state mutation
- **Poll loops with timeouts**: Replaced fixed sleeps for condition checking with poll loops that wait for specific conditions

### 3. License Compliance

Corrected 8 SPDX headers in `songbird-orchestrator/src/ipc/unix/handlers/` from `MIT` → `AGPL-3.0-only`.

### 4. Root Documentation

- Updated README.md, REMAINING_WORK.md, CHANGELOG.md, CONTRIBUTING.md to current state
- Archived stale `check-tower.sh` and `SONGBIRD_CLI_SPEC_FOR_BIOMEOS.yaml`
- Removed `audit.log` debris
- Fixed stale phase status comment in `songbird-tor-protocol/src/protocol/cells.rs`

---

## Current Quality Metrics

| Metric | Value |
|--------|-------|
| Tests | 8,968 passing, 0 failed, 286 ignored |
| Line Coverage | ~61% (target: 90%) |
| Build | Zero errors |
| Clippy Pedantic | 23/27 crates clean |
| Format | Clean |
| Docs | Clean |
| Safe Rust | 100% (`#![forbid(unsafe_code)]`) |
| Pure Rust | Zero C dependencies |
| Files >1000 lines | 0 |
| Production `todo!()` | 0 |
| `std::env::set_var` in tests | 0 |
| `#[serial]` in tests | 0 (except chaos) |
| Sleep-based polling | 0 (production) |

---

## Remaining TODOs in Production Code (~55)

### BearDog Integration (blocked on BearDog session)
- AES-128-CTR encryption via BearDog (Tor cells)
- Running digest SHA3-256 via BearDog (relay cell integrity)
- HMAC-SHA256 (ESTABLISH_INTRO auth)
- ntor handshake (CREATE2/EXTEND2)
- `ed25519_public_from_secret` (Sovereign Onion)
- X.509 certificate generation + chain validation (TLS)
- CertificateVerify BearDog signing (HTTP client TLS server)

### Genesis Physical Channels (stubs)
- Bluetooth: btleplug integration, real GATT pairing
- QR Code: qrcode generation + scanning
- SoloKey: FIDO2 verification + key exchange

### Platform Backends (stubs)
- NFC: Android JNI, iOS CoreNFC, Linux libnfc
- iOS XPC transport
- WASM primal registry

### Protocol Features
- Tor: HSDir descriptor upload, relay selection intelligence, microdescriptor parsing
- STUN: Full NAT type detection (multiple requests)
- Federation: Actual join logic (currently placeholder)
- Capability router: Selection strategy (currently first-provider)
- Discovery: Cluster support
- GATT/L2CAP: Real operations (currently stubs)
- USB: Bulk endpoint streaming

---

## Ecosystem Notes

### For BearDog
Songbird is blocked on BearDog for:
1. `aes_128_ctr_encrypt` / `aes_128_ctr_decrypt` — Tor cell encryption
2. `sha3_256` — KDF + running digests (already have pure Rust SHA3 for checksums)
3. `ed25519_public_from_secret` — Sovereign Onion key derivation
4. `certificate.generate_self_signed` — TLS certificate generation
5. `crypto.sign` — CertificateVerify in TLS handshake

### For biomeOS / Neural API
- `capability.discover("crypto")` via Neural API is a future enhancement
- All adapters are protocol-agnostic (Unix socket primary, HTTP fallback)

### ecoBin Compliance
- Zero C dependencies
- Cross-compilation verified (x86_64-musl, aarch64-musl)
- Single binary (UniBin) with subcommands: `server`, `doctor`, `config`

### Interprimal Standards Followed
- JSON-RPC 2.0 + tarpc primary IPC
- Semantic method naming (`domain.operation`)
- Capability-first socket discovery
- Self-knowledge only (no hardcoded primal references)
- Runtime discovery of all external services
- Injectable env readers for concurrent testing

---

## Next Session Priorities

1. **Clippy pedantic**: Fix remaining 4 crates (399 errors)
2. **Coverage expansion**: Target pure-logic modules for 90% goal
3. **Edition 2024**: Upgrade workspace edition
4. **SPDX headers**: Add to all source files (not just handlers)
5. **Zero-copy**: Reduce `.clone()` / `.to_string()` in hot paths
