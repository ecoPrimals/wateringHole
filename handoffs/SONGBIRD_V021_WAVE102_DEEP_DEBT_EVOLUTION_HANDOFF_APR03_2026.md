# Songbird v0.2.1 Wave 102: Deep Debt Evolution & Monolith Refactoring

**Date**: April 3, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Session**: Wave 102  
**Scope**: Production safety, capability-domain completion, smart monolith refactoring, async Mutex migration, root doc cleanup

---

## Summary

Comprehensive deep debt execution across 8 workstreams: eliminated production panic paths in TLS wire code, completed capability-domain migration for IPC field names and routing, refactored 3 largest monoliths by architectural responsibility, migrated async Mutex usage, and updated all root documentation to reflect current state.

## Production Safety

| File | Change |
|------|--------|
| `songbird-http-client/src/tls/handshake_refactored/extensions.rs` | `.expect()` → `Result<Vec<u8>>` with `Error::TlsHandshake` for oversized inputs |
| `songbird-http-client/src/tls/handshake_refactored/client_finished.rs` | `.expect()` → `Result<Vec<u8>>` for wire-format length overflow |
| `songbird-http-client/src/tls/handshake_refactored/handshake_flow.rs` | `build_client_hello` → `Result<Vec<u8>>` |
| `songbird-http-client/src/tls/profiler/profiler_impl.rs` | `RwLock .expect("poisoned")` → `PoisonError::into_inner` recovery |

## Capability-Domain Migration Completion

| Area | Change |
|------|--------|
| IPC field names | `beardog_socket` → `security_socket` across 8 files (tor_handler, onion_handler, birdsong_handler, http_handler) |
| JSON status key | `"beardog_available"` → `"security_provider_available"` |
| IPC routing | `squirrel_handlers` → `coordination_handlers` module + all dispatch references |
| Socket paths | `security.sock` primary, `beardog.sock` legacy fallback in XDG probing |
| Config ports | `compute_provider_port()`, `ai_provider_port()` with deprecated `toadstool_port()`, `squirrel_port()` aliases |
| Config endpoints | `compute_provider_endpoint()`, `ai_provider_endpoint()` with deprecated aliases |
| Path candidates | `coordination_socket_candidates()`, `compute_socket_candidates()` with deprecated aliases |

## Smart Monolith Refactoring

| Original | Lines | Decomposed To | Max Module |
|----------|-------|---------------|------------|
| `runtime_engine.rs` | 798 | 6 modules (env_mdns, consul, etcd, kubernetes, register, mod) | 294 |
| `stun/client.rs` | 766 | 3 modules (client, protocol, transaction) | 393 |
| `anonymous/broadcaster.rs` | 766 | 3 modules (broadcaster, protocol, scheduling) | 369 |

All production modules now under 400 lines.

## Async Safety

| File | Change |
|------|--------|
| `songbird-universal/src/discovery/engine.rs` | `std::sync::Mutex` → `tokio::sync::Mutex` (held across `.await`) |
| `songbird-orchestrator/src/app/core.rs` | Documented as intentional `std::sync::Mutex` (sync-only callers) |
| `songbird-process-env/src/lib.rs` | Documented as intentional (no `.await` while held) |

## Genesis Feature Gate

| File | Change |
|------|--------|
| `songbird-genesis/Cargo.toml` | `solokey` removed from default features (placeholder/demo, opt-in only) |

## Root Doc Updates

| File | Change |
|------|--------|
| `README.md` | Capability-domain language throughout; `#[serial_test]` → 0 suites; architecture diagram updated; test metrics aligned; monolith size updated to <400 lines |
| `CONTEXT.md` | Capability-domain language; file size metric updated |
| `REMAINING_WORK.md` | Wave 102 audit noted; pending sections reconciled; coverage header fixed to ~72%; priority order updated |
| `SECURITY.md` | Capability-domain language; date updated |
| `.env.example` | `SECURITY_PROVIDER_SOCKET` primary; legacy `BEARDOG_SOCKET` as comment |
| `scripts/test-with-beardog.sh` | Renamed to `test-with-security-provider.sh` |

## Verification

- `cargo fmt --all -- --check`: clean
- `cargo clippy --workspace --all-targets -- -D warnings`: 0 warnings
- `cargo test --workspace`: 12,154+ passed, 3 pre-existing env-dependent failures (no crypto provider runtime), ~116 ignored
- `cargo doc --workspace --no-deps`: 0 warnings
