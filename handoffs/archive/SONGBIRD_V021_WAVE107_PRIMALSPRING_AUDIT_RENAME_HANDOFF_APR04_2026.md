# Songbird v0.2.1 Wave 107: primalSpring Downstream Audit Response — Rename Wave

**Date**: April 4, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Session**: Wave 107  
**Scope**: Legacy primal-name elimination (beardog/toadstool/squirrel/nestgate → capability-based), SB-02/SB-03 resolution, integration test cleanup

---

## Summary

Response to primalSpring downstream audit. Continued capability-based rename waves: renamed 60+ test functions, 2 test files, and numerous string literals/comments from primal-identity names to capability-domain names. Added missing capability-based API companions. Confirmed SB-02 (ring lockfile ghost) and SB-03 (sled default-on) are already resolved.

## Quality Gate

| Check | Status |
|-------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace -- -D warnings` | Pass (zero warnings) |
| `cargo test --workspace` | Pass (12,495 passed, 0 failed, 252 ignored) |
| `cargo deny check` | Pass |

## primalSpring Audit Findings — Resolution

| Finding | Status | Resolution |
|---------|--------|------------|
| 1016 .rs refs / 189 files | **759 refs / 201 files** | 26% reduction this wave; remaining are `#[deprecated]` aliases, env fallbacks, and doc migration history |
| 1 test failure (`bear_dog_mode_errors_when_security_provider_unavailable`) | **Fixed** | Renamed to `security_provider_mode_errors_when_unavailable` |
| SB-02: ring lockfile ghost | **Confirmed resolved** | `ring` only enters via optional `k8s` feature (`kube→rustls→ring`). Not in default build. Lockfile records all-features resolution — expected. |
| SB-03: sled default-on | **Confirmed resolved** | `sled` is `default = []` / optional in all 3 crates (orchestrator, tor-protocol, sovereign-onion). Opt-in via `--features sled-storage`. |
| Overstep: sled in orchestrator/sovereign-onion | **Feature-gated** | Storage delegation to nestGate tracked as SB-03. Sled is opt-in only. |

## Rename Wave 107 Changes

### Test Functions Renamed (60+)

| Crate | Old Pattern | New Pattern | Count |
|-------|-------------|-------------|-------|
| `songbird-lineage-relay` | `bear_dog_*` / `test_beardog_*` | `security_*` / `test_security_*` | 16 |
| `songbird-tls` | `bear_dog_mode_*`, `test_env_var_priority_legacy_beardog_*` | `security_provider_*`, `test_env_var_priority_legacy_security_*` | 2 |
| `songbird-http-client` | `test_semantic_mapping_unknown_returns_bear_dog_rpc_error` | `test_semantic_mapping_unknown_returns_security_rpc_error` | 1 |
| `songbird-test-utils` (mocks) | `test_mock_squirrel_*`, `test_mock_nestgate_*`, `test_mock_beardog_*`, `test_toadstool_*` | `test_mock_ai_provider_*`, `test_mock_storage_provider_*`, `test_mock_security_provider_*`, `test_compute_provider_*` | 14 |
| `songbird-universal-ipc` | `test_onion_*_without_beardog` | `test_onion_*_without_security_provider` | 2 |
| `songbird-universal` | `test_beardog_phase1_*`, `test_trust_response_deserialize_beardog_*` | `test_security_phase1_*`, `test_trust_response_deserialize_security_*` | 2 |
| `songbird-types` | `test_beardog_phase1_response` | `test_security_phase1_response` | 1 |
| `songbird-sovereign-onion` | `*_beardog_*` test functions | `*_security_*` | 3 |
| `songbird-orchestrator` | `test_e2e_*_beardog`, `test_beardog_client_*` | `test_e2e_*_socket`, `test_security_client_*` | 2 |
| `songbird-tor-protocol` | `test_descriptor_new_requires_beardog_signing` | `test_descriptor_new_requires_security_signing` | 1 |
| `songbird-crypto-provider` | `*_beardog_*` | `*_security_*` | 5 |
| `songbird-discovery` | `test_beardog_encrypt_*`, `test_beardog_decrypt_*` | `test_security_encrypt_*`, `test_security_decrypt_*` | 2 |
| `songbird-nfc` | `discover_security_socket_prefers_*_over_beardog` | `*_prefers_security_provider_env` | 1 |
| Integration tests | `test_nestgate_*`, `test_toadstool_*`, `test_beardog_*` | `test_storage_*`, `test_compute_*`, `test_security_*` | 10+ |

### Test Files Renamed
- `beardog_api_compatibility_e2e.rs` → `security_provider_api_compatibility_e2e.rs`
- `btsp_beardog_integration.rs` → `btsp_security_provider_integration.rs`

### Production API Additions
- `TrustLevel::security_provider_alias()` (non-deprecated; `beardog_alias()` deprecated)
- `storage_provider_endpoint()` on `PrimalConfig` and `ServiceEndpoints`
- `security_provider_endpoint()` on `ServiceEndpoints`
- `ai_socket_candidates()` in `defaults::paths`
- `storage_provider_error()` in `universal-ipc::error`
- `storage_provider()`, `ai_provider()`, `security_provider()` in test fixtures

### String Literal / Comment Updates
- Service registry tests: `"beardog"` → `"security"`, `"squirrel"` → `"ai"`
- BTSP http_provider docs: `"beardog"` → `"security-provider"`
- Genesis identity tests: `"beardog"` → `"security"`, `"toadstool"` → `"compute"`
- Capability discovery tests: URLs updated to `security-provider:8443`, `compute-provider.local:9000`
- Trust types: doc example `beardog:family:nat0` → `security:family:nat0`
- Orchestrator comments: `"ToadStool"` → `"compute provider"`

## Remaining Legacy Refs (759 in .rs)

| Category | Count | Status |
|----------|-------|--------|
| `#[deprecated]` type/module aliases | ~150 | Intentional backward compat |
| `BEARDOG_*` env var fallback chains | ~200 | External interface to beardog binary |
| Doc comments explaining migration | ~100 | Historical documentation |
| `pub mod beardog` re-export aliases | ~30 | Deprecated, will be removed in v0.3.0 |
| Wire-format serde aliases | ~10 | Protocol backward compat |
| Remaining production functions with deprecated attrs | ~100 | Will be removed in v0.3.0 |
| Test assertions on wire values | ~50 | External binary returns "beardog" |
| primal_names.rs constants | ~10 | Used for legacy compat only |

## Standards Compliance

| Standard | Status |
|----------|--------|
| Capability-Based Discovery v1.2.0 | Compliant — zero identity hardcoding in production discovery |
| Primal IPC Protocol v3.1.0 | Compliant |
| ecoBin | Compliant — zero C deps in default build |
| AGPL-3.0-only + scyBorg trio | Compliant |
