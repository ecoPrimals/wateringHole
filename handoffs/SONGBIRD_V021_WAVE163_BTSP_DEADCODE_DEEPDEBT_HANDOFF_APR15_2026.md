# Songbird v0.2.1 — Waves 160–163 Handoff

**Date**: April 15, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Waves**: 160, 161, 162, 163  
**Supersedes**: `SONGBIRD_V021_WAVE161_BTSP_DEEPDEBT_DOC_CLEANUP_HANDOFF_APR15_2026.md` (archived)

---

## Wave 160 — BTSP Wire-Format Integration (primalSpring Phase 45c)

- **`server.rs`**: Refactored into `handle_connection` / `handle_json_rpc_lines` / `dispatch_json_rpc_line`. First-line peek routes `"protocol":"btsp"` → NDJSON BTSP handshake. Both UDS + TCP.
- **`rpc.rs`**: Added `btsp.session.create/verify/negotiate`, `btsp.server.export_keys` to `semantic_to_actual()`.

## Wave 161 — Deep Debt: Port Centralization, Dep Cleanup, Error Typing

- `Box<dyn Error>` → `anyhow::Result<()>` in execution-agent
- Hardcoded `"0.0.0.0"` → `PRODUCTION_BIND_ADDRESS` in server.rs
- 15+ `.unwrap_or(8080)` across 8 crates → canonical `songbird_types::defaults::ports` constants
- Duplicate `DEFAULT_BIND_ADDRESS` in config → re-export from canonical source
- Removed `hostname` crate (consolidated to `gethostname`)
- Removed unused `futures` from bluetooth + lineage-relay; migrated `futures` → `futures-util` in stun, orchestrator, universal-ipc

## Wave 162 — BTSP Wire Fix (primalSpring Phase 45c convergence)

- **Root cause**: `SecurityRpcClient::call_direct()` called `stream.shutdown().await` after writing JSON-RPC request to BearDog. Write-half FIN raced with BearDog's read, causing `btsp.session.create` response loss.
- **Fix**: Removed `stream.shutdown()` from both `call_direct()` and `call_neural_api()`. Connection is per-request; BearDog closes after responding, providing natural EOF.
- **Ref**: `BTSP_WIRE_CONVERGENCE_APR24_2026.md`

## Wave 163 — Dead Deprecated Code Removal + Docker Config Bug

### Bug fix
- `docker.rs:24`: literal string `"tcp://songbird_config::canonical::constants::network::DEFAULT_HOST:2376"` contained Rust path syntax as text instead of resolving the constant → `format!("tcp://{}:2376", songbird_types::constants::LOCALHOST)`

### Removed (zero-caller deprecated items)

| Item | Crate | Superseded By |
|------|-------|---------------|
| `beardog_socket_legacy_path()` | songbird-types | `security_socket_default_path()` |
| `neural_api_socket_fallback_paths()` | songbird-types | `coordination_socket_candidates()` |
| `storage_nestgate` module | songbird-sovereign-onion | `storage_ipc` |
| `storage_nestgate` module | songbird-orchestrator | `storage_ipc` |
| `security_provider_legacy` module | songbird-execution-agent | `security_provider` |
| `LegacySecurityProviderValidator` | songbird-execution-agent | `SecurityProviderValidator` |
| `tls_derive_secrets()` | songbird-http-client | `tls_derive_application_secrets()` |
| `SongbirdHttpClient::with_config()` | songbird-http-client | `with_tls_config()` |
| `SecurityCapabilityClient::new()` | songbird-orchestrator | `from_endpoint()` |

### Full audit findings (Wave 163)

- **Unsafe code**: Zero — all 30 crates `#![forbid(unsafe_code)]`
- **`todo!()`/`unimplemented!()`**: Zero in production
- **`async-trait`**: Fully eliminated from first-party source
- **Mocks**: All gated behind `#[cfg(test)]` or `feature = "test-mocks"`
- **Large files**: Largest production 763L — under 800L threshold
- **`dyn` dispatch**: All remaining architectural (Stream, Any, SerialPort, Fn)
- **No `.bak`/`.old`/`.tmp` debris**
- **Zero `TODO`/`FIXME`/`HACK` in Rust source**

---

## Current State

| Metric | Value |
|--------|-------|
| Build | Clean (zero errors, zero warnings) |
| Clippy | Clean (`-D warnings`, pedantic + nursery, all 30 crates) |
| Formatting | Clean (`cargo fmt --check`) |
| Tests | 7,387 lib passed (0 failures, 22 ignored) |
| Coverage | 72.29% (Apr 8 2026; target 90%) |
| cargo-deny | Fully passing |
| Unsafe | Zero (30/30 `forbid(unsafe_code)`) |

---

## Remaining Deep Debt (documented in REMAINING_WORK.md)

- BTSP Phase 3 encrypted framing (ChaCha20/HMAC via `btsp.server.export_keys`)
- Tor/TLS crypto delegation with live security provider (BLOCKED)
- `serde_yaml` migration (blocked on kube-client transitive dep)
- `bincode` 1.x advisory (transitive via tarpc)
- Coverage expansion (72.29% → 90%)
- Platform backends (NFC, iOS XPC, WASM)
- Remaining deprecated items with active callers (capability-based naming migration ongoing)
