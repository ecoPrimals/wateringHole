# Songbird v0.2.1 — Wave 142: Deep Debt Cleanup + Idiomatic Rust Evolution

**Date**: April 16, 2026
**Primal**: Songbird (network orchestration & discovery)
**Version**: v0.2.1
**Commit**: `07fee91b`
**Previous**: Wave 141 (primalSpring Apr 16 audit response)

---

## Summary

Comprehensive deep debt audit and cleanup pass. All audit axes confirmed green:
zero unsafe, zero TODOs, zero production mocks, zero files >800 lines, pure Rust
deps, zero C dependencies in default build. Legacy hardcoding evolved to
capability-based constants, `/tmp/` hardcoded paths eliminated, idiomatic Rust
patterns applied across 5 crates.

---

## Changes

### Hardcoding Evolution
- **`LEGACY_AI_SOCKET_FILENAME`** and **`LEGACY_COMPUTE_SOCKET_FILENAME`** constants added to `songbird-types/src/defaults/paths.rs` — replaces raw `"squirrel.sock"` and `"toadstool.sock"` literals
- All hardcoded `/tmp/` paths in production replaced with `std::env::temp_dir()`:
  - `songbird-universal-ipc/src/capability/strategy.rs` — filesystem scan root
  - `songbird-remote-deploy/src/deploy/args.rs` — deploy path default (new `default_deploy_path()` function)

### Idiomatic Rust Improvements
- `songbird-registry`: `if let Some/else` → `map_or_else` in `get_plugin_capabilities`
- `songbird-http-client`: eliminated duplicate `hostname.to_string()` allocations in TLS negotiation
- `songbird-discovery`: `collect::<Vec<_>>().join()` → `fold` with direct string building in SSDP parser
- `songbird-remote-deploy`: `collect::<Vec<_>>().join()` → `fmt::Write` loop in SSH env formatting

### Test Coverage
- 14 new tests in `songbird-onion-relay` coordinator:
  - Config: default values, builder pattern, clone preservation, debug output
  - Core: construction, register_peer, replace existing, message dispatch (register, query known, query unknown, heartbeat, punch_request for self, punch_request for other)
- New `peer_count()` public API on `HolePunchCoordinator`

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,350 lib passed, 0 failed, 22 ignored |
| Clippy | Zero warnings (pedantic + nursery, Apr 16) |
| cargo deny | advisories ok, bans ok, licenses ok, sources ok |
| Unsafe | 0 blocks, `#![forbid(unsafe_code)]` all 30 crates |
| Files >800L | 0 |
| TODO/FIXME/HACK | 0 in Rust source |
| Production mocks | 0 |
| C dependencies | 0 in default build |
| `.unwrap()` in production | 0 |

---

## Files Changed

```
CHANGELOG.md
REMAINING_WORK.md
crates/songbird-discovery/src/protocol/ssdp_discovery.rs
crates/songbird-http-client/src/tls/negotiation.rs
crates/songbird-onion-relay/src/coordinator/config.rs
crates/songbird-onion-relay/src/coordinator/core.rs
crates/songbird-registry/src/plugin/mod.rs
crates/songbird-remote-deploy/src/deploy/args.rs
crates/songbird-remote-deploy/src/deploy/ssh.rs
crates/songbird-types/src/defaults/paths.rs
crates/songbird-universal-ipc/src/capability/strategy.rs
crates/songbird-universal-ipc/src/handlers/discovery_handler.rs
```

---

## Audit Confirmation

All deep debt axes verified clean:
- **Unsafe code**: Zero across all 30 crates
- **Large files**: None >800 lines (largest 763L)
- **Production mocks**: All gated behind `#[cfg(test)]`
- **TODOs**: Zero in Rust source
- **C deps**: Zero in default build (no `-sys`, no `cc`, no `build.rs`)
- **Dependency hygiene**: `rand`/`fastrand` correctly split; `ring` not compiled in default build
- **Legacy hardcoding**: All `/tmp/` evolved to `temp_dir()`; legacy socket names centralized as constants; env vars deprecated with warnings

## Next Steps

- Continue test coverage push toward 90% target (currently 72.29%)
- Monitor `async_fn_in_dyn_trait` stabilization for `async-trait` migration (SB-06)
- Upstream `rustls-rustcrypto` release to eliminate `ring` chain A from Cargo.lock
