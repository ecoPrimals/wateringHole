# rhizoCrypt v0.14.0-dev — Session 31 Handoff

**Date**: 2026-04-09
**Focus**: BTSP Phase 2 Server-Side Handshake + Deep Debt Evolution
**Status**: Complete — 1,456 tests pass, zero clippy warnings, `cargo deny` clean
**Supersedes**: `RHIZOCRYPT_V014_S30_DEEP_DEBT_SOVEREIGNTY_HANDOFF_APR08_2026.md`

## Executive Summary

rhizoCrypt is the first primal beyond BearDog to implement BTSP Phase 2
server-side handshake enforcement on UDS accept. Production mocks that
returned fake success have been eliminated in favor of honest errors.
Six large files smart-refactored, rate limiter evolved to lock-free
DashMap, 24 handler construction sites DRY'd up.

## Changes

### BTSP Phase 2: Server-Side Handshake Enforcement

- New `btsp/` module in `rhizo-crypt-rpc` (types, framing, server)
- 4-step X25519 + HMAC-SHA256 handshake on every UDS connection when `FAMILY_ID` is set
- Length-prefixed framing codec (4-byte BE u32, 16 MiB max)
- `BtspSession` with `zeroize(drop)` on session keys
- Environment detection: `is_btsp_required()` + `read_family_seed()`
- Handshake failure → error frame + connection drop, zero RPC surface exposed
- Dev mode (`BIOMEOS_INSECURE=1`) bypasses, serving raw newline JSON-RPC
- New deps (all Pure Rust, ecoBin-compliant): `x25519-dalek`, `hmac`, `sha2`, `hkdf`, `rand`, `zeroize`
- 11 new tests covering full round-trip, wrong-seed rejection, framing, key derivation

### Production Mock Elimination

- `SongbirdClient::register` (no `live-clients`): fake `RegistrationResult { success: true }` → `Err` with feature gate message
- `ComputeProviderClient::subscribe_task/agent/get_events`: silent empty returns → `Err` with clear message
- `TarpcAdapter::ensure_connected`: dummy connection cache → `Err`; stub struct simplified to unit type

### Smart Refactoring

- **Rate limiter**: `Arc<RwLock<HashMap>>` → `DashMap` — `check()` is now sync, no async lock contention
- **Handler DRY-up**: 24 manual struct constructions → `server.clone()` (leveraging `#[derive(Clone)]`)
- **Test extraction** (6 files via `#[path]` pattern):
  - `client.rs`: 692 → 382 lines
  - `rate_limit.rs`: 549 → 279 lines
  - `types.rs`: 644 → 384 lines
  - `session.rs`: 607 → 436 lines
  - `error.rs`: 673 → 497 lines
  - `config.rs`: 515 → 380 lines

### Lint Hygiene

- Removed `#![allow(unused_imports)]` from e2e/chaos test roots
- Fixed 4 actual unused imports across test files
- Aligned all `#[expect]` attributes to match actual lint usage (zero unfulfilled)
- Removed `allow(dead_code)` from tarpc adapter fields

## Ecosystem Impact

- **BTSP Phase 2 cascade**: rhizoCrypt joins BearDog. Remaining priority: Songbird → NestGate → ToadStool → rest.
- **plasmidBin**: musl-static binary verified (5.7 MB, `static-pie linked, stripped`). Ready for harvest.
- **Wire Standard**: L3 composable — unchanged from S30.

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,456 passing (up from 1,441) |
| Source files | 146 `.rs` (up from 136) |
| Max file size | 687 lines (down from 928) |
| Binary | 5.7 MB musl-static (x86_64) |
| Clippy | 0 warnings |
| Unsafe | 0 blocks |
| `cargo deny` | advisories ok, bans ok, licenses ok, sources ok |

## Remaining Debt (Low Priority)

- HTTP client error types (`BearDogHttpError`, `NestGateHttpError`, `ToadStoolHttpError`) share similar variants — could unify into generic adapter error
- Primal names in test data (`registry_tests.rs`, `mocks.rs`) are acceptable for discovery testing
- BTSP Phase 3 (per-frame cipher wrapping) pending ecosystem coordination
- `async_trait` usage on object-safe adapter traits — requires API redesign to remove
- `bincode` v1 transitive from tarpc — acknowledged in `deny.toml`, awaiting tarpc migration

## Gap Matrix Status

| Gap | Status |
|-----|--------|
| RC-01 (UDS registration) | Resolved (v0.14.0-dev, `--unix`) |
| RC-02 (Wire L2) | Resolved (S27) |
| GAP-MATRIX-05 (live validation) | Resolved (S29) |
| GAP-MATRIX-10 (Wire L2→L3) | Resolved (S29) |
| GAP-MATRIX-12 (BTSP Phase 1) | Resolved (S29) |
| BTSP Phase 2 (server accept) | **Resolved (S31)** |
| plasmidBin freshness | **Verified (S31)** — musl-static rebuild clean |
