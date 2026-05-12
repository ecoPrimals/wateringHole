# Songbird v0.2.1 Wave 85–86 Handoff

**Date**: March 30, 2026
**Version**: v0.2.1
**Sessions**: 27–28 (Waves 85–86)
**Primal**: Songbird (Network Orchestration & Discovery)

---

## Wave 85: Comprehensive Audit Execution

### License Reconciliation
- All project files aligned to `AGPL-3.0-only` (was `AGPL-3.0-or-later` in Cargo.toml, README, CONTRIBUTING)
- Consistent with wateringHole `STANDARDS_AND_EXPECTATIONS.md`, LICENSE body, and SPDX headers

### Sovereignty Fixes
- Google STUN servers (`stun.l.google.com:19302`) replaced with sovereign alternatives: `stun.nextcloud.com:3478`, `stun.cloudflare.com:3478`, `stun.sip.us:3478`
- Google DNS `8.8.8.8:53` replaced with RFC 5737 documentation address `192.0.2.1:80`
- All replacements are environment-variable configurable

### CI Modernization
- `cargo test --workspace` → `--all-features` (exposed 11,825 tests; was only ~150 without feature gates)
- Workflows updated: `Swatinem/rust-cache@v2`, `codecov/codecov-action@v4`, `actions/upload-artifact@v4`

### Production Stub Evolution
- `discover_nodes()`, `QueryStatus`, `QueryServices`, `establish_connection` → proper implementations or explicit error returns
- tarpc hardcoded ports → `SafeEnv::get_port`; `"127.0.0.1"` literals → `LOCALHOST` constant
- `runtime_engine.rs` test module extracted (997→789 lines)

---

## Wave 86: Ring Removal + BearDog Wiring + Live Test Harness

### Track 1: Ring Removal

**Problem**: `ring` (C dependency) entered production through `rcgen` and `quinn`.

**Solution**:
- `rcgen` removed from `songbird-quic` entirely — replaced with `cert_gen.rs` (pure-Rust DER construction via `ed25519-dalek`)
- `quinn` minimized: `default-features = false, features = ["runtime-tokio", "rustls-ring"]`
- **Result**: `cargo tree -i ring -e normal` → ring only from `quinn` → `quinn-proto` → `rustls`
- **Upstream blocker**: quinn lacks `rustls-rustcrypto` feature; runtime already uses `rustls-rustcrypto` (ring compiled but unused at runtime)

**Files changed**:
- `crates/songbird-quic/Cargo.toml` — removed `rcgen`, added `ed25519-dalek` + `rand`
- `crates/songbird-quic/src/cert_gen.rs` — new: pure-Rust self-signed Ed25519 cert generation
- `crates/songbird-quic/src/config.rs` — uses `cert_gen::generate_self_signed_ed25519()`

### Track 2: BearDog Wiring (6 CryptoUnavailable stubs → live JSON-RPC)

| Crate | File | Stub | Wired To |
|-------|------|------|----------|
| `songbird-tor-protocol` | `descriptor.rs` | `request_beardog_key()` | `CryptoProvider::call()` (async) |
| `songbird-http-client` | `tls/server/messages.rs` | `build_certificate_verify()` | `CryptoProvider::call("crypto.sign.ed25519")` |
| `songbird-network-federation` | `beardog/birdsong.rs` | `encrypt_broadcast()` | `CryptoProvider::call("crypto.encrypt_chacha20_poly1305")` |
| `songbird-network-federation` | `rendezvous/client.rs` | `get_public_key_fingerprint()` | `CryptoProvider` primary + legacy fallback |

All wired stubs fall back gracefully to `CryptoUnavailable` when BearDog is unreachable.

### Track 3: Live BearDog Test Harness

- `crates/songbird-test-utils/src/fixtures/beardog.rs`: `BearDogFixture` — discovers binary from `$BEARDOG_BIN` / `$ECOPRIMALS_PLASMID_BIN` / workspace walk to `infra/plasmidBin/primals/beardog`; spawns on temp Unix socket; kills on Drop
- `scripts/test-with-beardog.sh`: fetches beardog via `plasmidBin/fetch.sh`, starts on temp socket, exports env vars, runs `cargo test --workspace --all-features`

---

## Metrics

| Metric | Before (Wave 84) | After (Wave 86) |
|--------|------------------|-----------------|
| Tests | 11,471 | 11,831 |
| `ring` paths | `quinn` + `rcgen` | `quinn` only |
| `CryptoUnavailable` stubs | 6 unconnected | 6 wired to `CryptoProvider` |
| BearDog test harness | None | `BearDogFixture` + `test-with-beardog.sh` |
| Clippy | Clean | Clean |
| Format | Clean | Clean |

---

## Remaining Upstream Blockers

- **quinn `rustls-rustcrypto`**: quinn 0.11 gates `quinn::crypto::rustls` behind `rustls-ring` or `rustls-aws-lc-rs`. No `rustls-rustcrypto` feature exists. A quinn PR or workspace `[patch]` adding `rustls-only` would fully eliminate ring from the compile-time dependency graph.

---

## Ecosystem Impact

- **Other primals using `songbird-crypto-provider`**: The `CryptoProvider::call()` pattern is now validated end-to-end across 4 crates. Any primal can wire crypto stubs the same way.
- **plasmidBin integration**: The `BearDogFixture` pattern can be generalized to test any primal binary from plasmidBin.
- **ecoBin compliance**: `rcgen` removal brings Songbird closer to full ecoBin compliance. Only `quinn`'s transitive `ring` remains.
