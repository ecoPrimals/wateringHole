# Songbird v0.2.1 — Wave 124: Deep Debt Lint Hygiene, Coverage Expansion & Doc Evolution

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 124  
**Status**: Complete — all checks green

---

## Changes

### Lint Hygiene (`#[allow(` → `#[expect(reason)]`)

Converted 15+ production `#[allow(` attributes (without reason strings) to `#[expect(lint, reason = "...")]` across 12 files in 8 crates:

- `songbird-http-client` (TLS server, transcript, crypto discovery, security RPC client)
- `songbird-tls` (crypto)
- `songbird-sovereign-onion` (storage NestGate)
- `songbird-universal` (JSON-RPC client)
- `songbird-quic` (UDP endpoint)
- `songbird-network-federation` (security production, gaming)
- `songbird-config` (service registry)
- `songbird-bluetooth` (controller, GATT characteristics, ATT constants)

Where `dead_code` lint does not fire (item referenced elsewhere), kept `#[allow(dead_code, reason = "...")]` to avoid unfulfilled-expectation errors.

### Commented-Out Code Scrub

Removed 14 stale commented-out code blocks across 10 files:

- `songbird-network-federation/src/lib.rs` — stale `// pub mod tls;`
- `tests/chaos/mod.rs` — `// pub mod state_chaos;`
- `tests/e2e/test_primal_self_knowledge.rs` — 5 commented `let`/`use` lines
- `tests/helpers/mod.rs` — archived `http_mock` module
- `songbird-config` — 6 files with commented `use`/`pub use`/struct sketches
- `songbird-cli/src/cli/core/mod.rs` — commented `pub use`

### `// FIX:` Comment Resolution

Resolved all 6 `// FIX:` comments (5 locations) in `songbird-universal-ipc`:

- `service/http.rs` line 55
- `handlers/http_handler/client.rs` lines 42, 48
- `handlers/http_handler/handler.rs` lines 97, 148

All were stale — headers and body parsing already implemented correctly. Comments removed.

### Production `unreachable!()` Evolution

- **QUIC `LongPacketType::from_bits`**: Replaced `Result<Self>` + `_ => unreachable!()` with infallible lookup table indexed by `bits & 0x03`. No panic path remains.
- **QUIC `VarInt` encode/decode**: Kept `_ => unreachable!()` — provably unreachable (2-bit prefix constrains to 4 arms, all covered). Added inline comments documenting invariant.
- **Tor `create_extend2`**: Replaced `let IpAddr::V4(ipv4) = ... else { unreachable!() }` with a `match` returning `Err` for IPv6. No panic path remains.

### Legacy Doc Comment Evolution

Evolved legacy primal names in doc comments across 12 files to capability-based naming:

- "beardog" → "security provider (crypto.delegate)"
- "ToadStool" → "compute provider (compute.schedule)"
- "NestGate" → "storage provider (storage.*)"
- Legacy env vars documented as "Legacy `BEARDOG_SOCKET` (prefer `SECURITY_PROVIDER_SOCKET`)"

No code logic, env var strings, or deprecation attributes were changed.

### `test_sync_env.rs` Gating

Added `#![cfg(test)]` file-level guard to `songbird-orchestrator/src/test_sync_env.rs`. Module was already declared under `#[cfg(test)]` in `lib.rs`, but the file-level guard ensures the module stays test-only even if the declaration changes.

### `/tmp/beardog.sock` Test Path Evolution

Replaced hardcoded `/tmp/beardog.sock` in test constructors and doc examples with `songbird-test-security.sock` using `std::env::temp_dir()` for portability. Affected crates:

- `songbird-http-client` (TLS server, record_io, https connection, security RPC)
- `songbird-universal-ipc` (capability strategy)
- `songbird-universal` (protocol detection tests)
- `songbird-discovery` (security birdsong provider tests)

### Coverage Expansion (+49 tests)

**`songbird-universal` compute adapter** (was 11.83%):
- Discovery fallback chain tests (env vars → runtime → defaults)
- `build_default_transport` error paths
- Legacy `TOADSTOOL_ENDPOINT` deprecation warning verification
- `collect_metrics`, `check_health`, `ComputeMetricsProvider` via `MockTransport`

**`songbird-universal-ipc` STUN client** (was 14.22%):
- `port_pattern_ipc_value` for Sequential/Random/Unknown patterns
- `nat_type_from_dual_probes` for cone/symmetric/unknown
- `map_err` string verification
- Async handler error paths (unresolvable hosts, bind failures)
- Happy paths via `StunServer::run_with_ready`

**`songbird-universal-ipc` HTTP handler dispatch** (was 20%):
- `JsonRpcHandler::handle()` for GET/POST/PUT/DELETE
- Invalid params shape, missing URL/body, unknown methods
- Header parsing (valid map, non-object, bad value types)
- `map_err` error strings: connection failed, internal error, serialization
- Factory failure paths

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,811 | 12,860 |
| Failed | 0 | 0 |
| `#[allow(` without reason (prod) | ~15+ | 0 |
| Commented-out code | 14 locations | 0 |
| `// FIX:` comments | 6 | 0 |
| Production `unreachable!()` | 4 | 2 (provably unreachable VarInt, documented) |
| `/tmp/beardog.sock` in tests | ~12 | 0 |
| Legacy names in docs | ~25 locations | 0 (all evolved to capability-based) |

## Verification

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,860 passed, 0 failed, 252 ignored

## Files Changed

~88 files across 12 crates + root docs + deployment + specs + CHANGELOG + this handoff (in two commits: Wave 124 core + Wave 124b doc/debris cleanup).

### Wave 124b: Doc Accuracy & Debris Cleanup

- Root docs (README, REMAINING_WORK, CONTEXT, CONTRIBUTING): production `unreachable!()` claim corrected (0 → 2 QUIC VarInt arms), test count synchronized (12,860), dates standardized (Apr 8), file size limit aligned (800L), `expect()` policy clarified, tower_atomic metrics corrected
- CHANGELOG.md: Waves 119-124 entries added
- 11 crate `Cargo.toml` descriptions: "BearDog" → "security provider"
- `deployment/config/songbird.toml.example`: `[beardog]` → `[security-provider]`
- `deployment/systemd/songbird.service`: URL casing fixed
- `specs/` archive links: 4 files updated to point at `fossilRecord/consolidated-apr2026/`
- `tests/README.md`: rewritten to reflect current layout and metrics
- 2 test file commented-out code blocks cleaned

---

**Next priorities**: Coverage expansion toward 90% target (currently ~72.29%). Highest ROI remaining: `songbird-orchestrator` aggregate (~56%), `songbird-universal-ipc` aggregate (~67%), `songbird-config` aggregate (~68%).
