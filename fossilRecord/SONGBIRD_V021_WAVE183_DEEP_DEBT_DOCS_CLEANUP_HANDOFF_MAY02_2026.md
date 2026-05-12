# Songbird v0.2.1 — Wave 183 Deep Debt + Documentation Cleanup

**Date**: May 2, 2026
**Primal**: Songbird (orchestrator)
**Wave**: 183
**Scope**: Lint evolution, timeout centralization, hardcoded elimination, docs cleanup, spec archival

---

## Summary

Wave 183 combined a deep debt code pass with comprehensive documentation and debris cleanup.

### Code Changes (Wave 183)
- **Lint evolution**: 8 crate `lib.rs` files — added `reason` strings to all `#[cfg_attr(test, allow(...))]` blocks
- **Timeout centralization**: 8 new named constants in `songbird-types/src/defaults/timeouts.rs`; replaced 10 scattered `Duration::from_secs(N)` literals across `songbird-orchestrator`
- **Hardcoded elimination**: `PRODUCTION_BIND_ADDRESS_IPV6` constant; `orchestrator_port()` for port fallback; documented `DEFAULT_CORS_ORIGIN` derivation
- **Legacy deprecation**: Formally `#[deprecated]` `legacy_beardog_socket_path_in_biomeos_runtime` with controlled call-site allow
- **Unused import cleanup**: Removed `use std::time::Duration` from 2 files after constant replacement
- **Dependency refresh**: `cargo update` for all compatible semver ranges

### Documentation Cleanup (Wave 183+)
- **Root docs**: README.md verification dates (Apr 30 → May 2); SECURITY.md BTSP Phase 2 → Phase 3 (ChaCha20-Poly1305 encrypted framing)
- **Spec archival**: 16 stale specs moved to `specs/archived/` — referenced non-existent crates (`songbird-client`, `songbird-primal-sdk`, `songbird-federation`, `songbird-rpc`, `songbird-universal-primals`)
- **specs/README.md**: Updated to reflect active specs and archive rationale

### wateringHole Updates
- `ECOSYSTEM_EVOLUTION_CYCLE.md`: Date → May 2, 2026; added W183; fixed stadial bullet (W165 → W183)
- `README.md`: Handoff counts corrected (32 → 14 active, 681 → 740+ archived)
- Wave 182 handoff archived to `handoffs/archive/`

## Files Modified

### songBird
- `README.md` — verification dates
- `SECURITY.md` — BTSP Phase 3 description
- `REMAINING_WORK.md` — Wave 183 tracking
- `CHANGELOG.md` — v0.2.1-wave183 entry
- `specs/README.md` — updated active/archive sections
- 16 files moved from `specs/` to `specs/archived/`
- 8 crate `lib.rs` — lint reason strings
- `crates/songbird-types/src/constants.rs` — IPv6 bind constant
- `crates/songbird-types/src/defaults/timeouts.rs` — 8 new timeout constants
- `crates/songbird-types/src/defaults/network.rs` — CORS origin documentation
- `crates/songbird-orchestrator/src/server/protocol_api.rs` — hardcoded IP/port elimination
- `crates/songbird-orchestrator/src/server/mod.rs` — timeout constant
- `crates/songbird-orchestrator/src/server/compute_api/compute_handlers.rs` — timeout constant
- `crates/songbird-orchestrator/src/access_control/auth.rs` — timeout constants
- `crates/songbird-orchestrator/src/app/health.rs` — timeout constant
- `crates/songbird-orchestrator/src/app/discovery_bridge.rs` — timeout constant
- `crates/songbird-orchestrator/src/core/routing/enhanced_router.rs` — timeout + import cleanup
- `crates/songbird-orchestrator/src/core/routing/router/execution.rs` — timeout + import cleanup
- `crates/songbird-orchestrator/src/ipc/pure_rust_server/server/connection.rs` — timeout constant
- `crates/songbird-crypto-provider/src/socket_discovery.rs` — legacy deprecation

### wateringHole
- `ECOSYSTEM_EVOLUTION_CYCLE.md` — W183, date, stadial
- `README.md` — handoff counts
- Wave 182 handoff → archive

## Test Results
- 28/28 btsp_phase3 tests pass
- 0 new clippy warnings across workspace
- Pre-existing flaky tests (env var leakage) unchanged
- 7,803 lib tests total
