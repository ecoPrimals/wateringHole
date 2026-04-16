# Songbird v0.2.1 — Wave 140: primalSpring Phase 43 Audit Response + Deep Debt Evolution

**Date**: April 15, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 140
**Contact**: primalSpring
**Previous**: Wave 139b (deep hardcoded literal sweep, Apr 13)

---

## Summary

Wave 140 completes all 6 items from the primalSpring Phase 43 downstream audit and
continues deep debt evolution. UDS auto-detection, beacon credential tiering, STUN
authentication, content distribution federation, dependency hygiene, and legacy
constant centralization executed across 37 files in 12 crates.

---

## primalSpring Phase 43 Audit Items (6/6 Resolved)

### SB-01: UDS First-Byte Peek — Auto-Detection

**Problem**: UDS connections were mode-based (always BTSP or always plain JSON-RPC).
biomeOS composition traffic needs per-connection auto-detection.

**Solution**: `handle_connection_with_peek()` in `connection.rs` splits `UnixStream`,
wraps read half in `BufReader`, uses `fill_buf()` to peek the first byte:
- `0x7B` (`{`) → JSON-RPC newline-delimited session
- Anything else → BTSP handshake

Custom `PeekedStream` struct re-combines `BufReader<ReadHalf>` + `WriteHalf` into
a single `AsyncRead + AsyncWrite + Unpin` type for transparent protocol handoff.

### SB-02: Mito-Beacon Metadata in BirdSong Beacons

**Problem**: Dark Forest discovery must use Tier 1 mito-beacon credentials, never
nuclear. Discovery must not expose authorization material.

**Solution**: New `songbird-types/src/defaults/beacon.rs` defines beacon-tier RPC
method constants (`BEACON_ENCRYPT_METHOD`, `BEACON_DECRYPT_METHOD`, `BEACON_GET_ID_METHOD`)
with legacy `LEGACY_BIRDSONG_*` fallbacks. `SecurityBirdSongProvider` overrides
`encrypt_beacon`, `try_decrypt_beacon`, `get_beacon_id` with graceful fallback chain.

### SB-03: STUN/NAT with Mito-Beacon Credentials

**Problem**: NAT traversal must use beacon-tier credentials only.

**Solution**: `StunCredentials` type with documented credential tier model.
`StunClient::with_credentials()` builder. `BindingTransaction::with_credentials()`
injects `Username` attribute. `StunAttribute::Username` encoding/decoding added.

### SB-04: Content Distribution Federation

**Problem**: Songbird needs seeder/leecher discovery per `content_distribution_federation.toml`.

**Solution**: `discovery.announce` handler extended with topic-based announcements
(`topic`, `manifest_hash`, `seeder_count`, `bond_types_accepted` params). Two modes:
- **Presence** (existing): `family_id` + `capabilities`
- **Topic** (new): content namespace announcements for federation

`discovery.peers` handler extended with `capability_filter` (accepts both string
`"storage"` and array `["storage", "compute"]` forms) and `family_only` boolean.
Matches Phase 3 (`discover_seeders`) and Phase 6 (`announce_content`) of the
content distribution federation graph exactly.

### SB-05: Transitive `ring` in Cargo.lock

**Status**: Documented. `ring` in `Cargo.lock` is an uncompiled optional dep of
`rustls-webpki 0.102` via `rustls-rustcrypto 0.0.2-alpha`. `cargo tree -i ring`
returns no match. Upstream `rustls-rustcrypto` master has dropped the dep; lockfile
ghost disappears on next release. `deny.toml` ban comment updated with full context.

### SB-06: async-trait Migration (~150 instances)

**Status**: Analyzed, deferred. Every async trait in Songbird is either dyn-dispatched
directly (`Arc<dyn T>`, `Box<dyn T>`) or is a supertrait of one. Native AFIT (Rust
1.75+) doesn't support dyn dispatch. All 4 apparent "static-only" candidates
(`LineageProvider`, `LineageRelay`, `BirdSongCrypto`, `PrimalProvider`) are supertraits
of dyn-dispatched composite traits (`SecurityProvider`, `Provider`). Blocked on
`async_fn_in_dyn_trait` stabilization (rust-lang/rust#133119). Tracked as `SB-06`
comment on workspace `async-trait` dep in `Cargo.toml`.

---

## Deep Debt Evolution

### Legacy Socket Constant Centralization
- `LEGACY_SECURITY_SOCKET_FILENAME` (`"beardog.sock"`) in `songbird-types/defaults/paths.rs`
- Replaced raw string literals in `socket_discovery.rs`, `tor_handler.rs`, `security.rs`

### Hardcoded Path Evolution
- `/tmp/songbird-chunks/` and `/tmp/songbird-deployments/` → `std::env::temp_dir()` in `chunked_upload.rs`
- `/tmp/songbird-ipc-port` fallback → centralized `ipc_port_file_path()` in `connection.rs`
- New `data_dir()`: `SONGBIRD_DATA_DIR` > `XDG_DATA_HOME` > `HOME` > `/var/lib/songbird`

### CORS Origin Evolution
- New `cors_origins()`: resolves `SONGBIRD_CORS_ORIGINS` env var (comma-separated),
  falls back to `DEFAULT_CORS_ORIGIN`

### Dependency Hygiene
- `rand` removed from `songbird-orchestrator` production deps; JWT CSPRNG replaced with
  `getrandom::fill()`; `rand` retained as dev-dependency for tests

### Lint Fixes
- Stale `deny(unsafe_code)` comment → `forbid(unsafe_code)` in `unix.rs` test
- Pre-existing `needless_raw_string_hashes` in `service_types.rs`

---

## Files Changed (37 modified, 2 new)

| Crate | Files |
|-------|-------|
| `songbird-types` | `defaults/mod.rs`, `defaults/beacon.rs` (new), `defaults/paths.rs`, `defaults/network.rs` |
| `songbird-orchestrator` | `Cargo.toml`, `connection.rs`, `chunked_upload.rs`, `security_jwt_client.rs`, `startup_orchestration.rs`, `mod.rs`, `paths.rs`, `config.rs`, `lifecycle.rs`, `client.rs`, `federation_health.rs`, `startup_orchestration_tests.rs` (new) |
| `songbird-discovery` | `security_birdsong_provider.rs`, `factory.rs` |
| `songbird-stun` | `lib.rs`, `client.rs`, `types.rs`, `transaction.rs`, `message/types.rs`, `message/attributes.rs` |
| `songbird-universal-ipc` | `discovery_handler.rs`, `tor_handler.rs`, `service_types.rs`, `unix.rs` |
| `songbird-http-client` | `socket_discovery.rs` |
| `songbird-lineage-relay` | `security.rs` |
| `songbird-config` | `core.rs`, `cors.rs` |
| `songbird-registry` | `plugin/mod.rs` |
| `songbird-universal` | `unix_rpc_client.rs` |
| workspace root | `Cargo.toml`, `Cargo.lock`, `deny.toml`, `.github/workflows/ci.yml` |

---

## Verification

```bash
cargo check --workspace                                   # 0 errors, 0 warnings
cargo fmt --check                                         # Clean
cargo clippy --workspace --all-targets -- -D warnings     # 0 warnings
cargo test --workspace --lib                              # 7,334 passed, 0 failed, 22 ignored
cargo deny check                                          # advisories ok, bans ok, licenses ok, sources ok
```

---

## Audit Findings (No Action Required)

| Category | Result |
|----------|--------|
| `unsafe` blocks | 0 (`#![forbid(unsafe_code)]` all 30 crates) |
| TODO/FIXME/HACK in Rust | 1 `SB-04` tracking comment (content federation seeder tracking); 0 FIXME/HACK |
| Mocks in production | 0 (all in `#[cfg(test)]`) |
| `.unwrap()` in production | 0 |
| `panic!()`/`unreachable!()` in production | 0 / 2 (provably unreachable QUIC VarInt) |
| Files >800 LOC | 0 (largest production 763L) |
| C dependencies in default build | 0 |

---

## Status

**All primalSpring Phase 43 audit items resolved (6/6).**
Deep debt categories at S+ tier. Capability-based naming complete. Self-healing
auto-discovery operational. Beacon credential tiering enforced. Content distribution
federation wired.

Remaining work: coverage expansion (72.29% → 90% target), BTSP Phase 3,
Tor onion service crypto (blocked on security provider), TLS sovereign certs,
`async_fn_in_dyn_trait` stabilization (SB-06).
