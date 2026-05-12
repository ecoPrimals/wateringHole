<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Creative content: CC-BY-SA 4.0 (scyBorg provenance trio) -->

# BearDog v0.9.0 — Wave 17: Comprehensive Audit, UniBin Compliance, NDJSON & Coverage Push

**Date**: March 27, 2026
**Version**: 0.9.0
**Edition**: 2024 | **MSRV**: 1.93.0
**Supersedes**: Wave 16 handoff (March 24, 2026)

---

## Summary

Full comprehensive audit of the BearDog codebase against wateringHole standards
(PRIMAL_IPC_PROTOCOL, SEMANTIC_METHOD_NAMING, ECOBIN_ARCHITECTURE,
UNIBIN_ARCHITECTURE, ZERO_HARDCODING, primalSpring Leverage Guide), followed by
systematic execution across all identified issues: JSON-RPC batch support and
zero-copy wire types, UniBin `--port` CLI compliance, NDJSON TCP framing fix,
structured tracing migration (emoji removal), production stub evolution,
repository metadata normalization, dead feature flag removal, commented-out code
cleanup, CI workflow corrections, and targeted coverage expansion.

---

## Metrics

| Metric | Before (Wave 16) | After (Wave 17) |
|--------|-------------------|-----------------|
| Tests | 14,499+ | **14,600+** |
| Coverage (lines) | 86.70% | **87.31%** |
| Coverage (regions) | 87.34% | **87.91%** |
| JSON-RPC batch support | No | **Yes** |
| UniBin `--port` CLI | No | **Yes** |
| NDJSON TCP framing | Broken | **Fixed** |
| Emoji in logs | ~15 sites | **0** |
| Dead feature flags | 4 | **0** |
| Commented-out code blocks | 4+ | **0** |
| CI referencing non-existent features | 2 | **0** |
| Repository URL inconsistencies | 22 Cargo.toml | **0** |
| SPDX license conflicts | 1 file | **0** |
| Stale test boilerplate comments | ~68 | **0** |

---

## Changes

### 1. JSON-RPC Batch Support & Zero-Copy Wire Types

- `JsonRpcRequest::jsonrpc` field evolved from `String` to `Cow<'static, str>` (zero-copy)
- New `JSONRPC_VERSION` constant eliminates allocation for the `"2.0"` string
- Constructor helpers: `JsonRpcRequest::new`, `JsonRpcResponse::success`, `JsonRpcResponse::error`
- `JsonRpcMessage` and `JsonRpcResponseMessage` enums with `#[serde(untagged)]` for batch support
- All call sites across `beardog-tunnel`, `beardog-ipc`, and tests updated to use `Cow::Borrowed`

### 2. UniBin `--port` CLI Compliance

- Added `pub port: Option<u16>` to `ServerArgs` with `conflicts_with = "listen"`
- `handle_server` resolves `--port` to `0.0.0.0:<port>` listen address
- Aligns with wateringHole UNIBIN_ARCHITECTURE `server --port` standard

### 3. NDJSON TCP Framing

- TCP JSON-RPC server handler updated to `tokio::io::BufReader::lines()` for proper newline-delimited JSON reading
- Responses explicitly newline-terminated (`\n`)
- Eliminates silent message corruption on multi-message TCP streams

### 4. Structured Tracing Migration

Emoji characters removed from all log messages and CLI output across 7+ files:
- `beardog-tunnel`: `unix_socket_ipc/server.rs`, `health.rs`
- `beardog-ipc`: `client.rs`, `protocol_router.rs`
- `beardog-cli`: `handlers/hsm.rs`, `handlers/entropy.rs`
- `beardog-core`: `ecosystem_listener/discovery.rs`, `universal_adapter/production.rs`
- `beardog-tunnel`: `handlers/btsp.rs`

Interpolated values converted to structured tracing fields.

### 5. Production Stub Evolution

- **HSM Audit Logger** — Bounded `VecDeque` for in-memory audit records with real timestamps and statistics aggregation
- **Graph Security Audit** — `get_security_assessment` derives threat level and vulnerability count from lineage and community metrics
- **Integration Engine Health** — Real health checks against HSM and ecosystem status
- **Port Discovery** — `query_mdns_primal_ports` reads from `BEARDOG_DISCOVERED_PRIMAL_PORTS` env var
- **Monitoring Metrics** — `PerformanceEngine` and `SecurityMetricsEngine` with mutex-backed tracking and derived averages/rates
- **Cross-Primal Messaging** — Replaced `ciphertext: vec![]` with `serde_json::to_vec`, replaced `processing_time_ms: 0` with real timing
- **Self-Knowledge** — `get_self_capabilities` maps `PrimalIdentity::Capability` to `UniversalCapabilityType` taxonomy
- **Evolution Engine** — `diversity_index` computed from unique fitness values in population

### 6. Repository Metadata Normalization

- All 22 workspace `Cargo.toml` `homepage`/`repository` URLs normalized to `https://github.com/ecoPrimals/beardog`
- Fixed casing variants (`eastgate-software`, `your-org`, `beardog/beardog`, `bearDog`)
- SPDX conflict resolved in `beardog-adapters` certificates/verification.rs (duplicate `AGPL-3.0-or-later` removed)

### 7. Dead Feature Flag Cleanup

Removed from `beardog-tunnel/Cargo.toml`:
- `zero-cost-architecture`, `universal-discovery`, `primal-sovereignty`, `ecosystem`
- None had `#[cfg(feature = "...")]` gates in source code

### 8. CI Workflow Fixes

- `beardog-ci.yml`: Replaced `cargo check -p beardog-types --features zero-cost` with `--all-features` (no `zero-cost` feature exists)
- `beardog-ci.yml`: Fixed `./archive/*` exclude path to `./archives/*` (matching actual directory name)
- `beardog-ci.yml`: File size check threshold aligned to 1000 LOC (was 2000)

### 9. Commented-Out Code Cleanup

- `beardog-core/tests/core_integration_tests.rs` — Removed entirely (62 lines of broken commented-out test code)
- `beardog-core/src/external_functions/safety.rs` — Removed ~51-line commented `PolicyEngine` impl block
- `beardog-tunnel/src/unix_socket_ipc/crypto_handlers_ecdsa.rs` — Removed ~13-line commented P-521 handler stub

### 10. Lint & Cast Evolution

- `clippy::cast_lossless` promoted to `warn` at workspace level
- Policy updated: new code should use `From`/`Into` or `#[expect]` per-site

### 11. Hardcoding Evolution

- `LICENSE_PRICING_URL` constant replaces hardcoded `https://beardog.dev/pricing` (configurable via `BEARDOG_LICENSE_PRICING_URL` env)
- `DEFAULT_SOLO_V2_RELYING_PARTY_ID` constant replaces hardcoded `"beardog.dev"` in Solo V2 types
- Repository references in error messages normalized (`ecoPrimals/bearDog` → `ecoPrimals/beardog`, `eastgate-software/beardog` → `ecoPrimals/beardog`)

### 12. False-Positive TODO Cleanup

- 68 stale `// Test passes (placeholder removed)` comments removed from genetics and monitoring test suites
- `specs/PROJECT_STATUS.md` clarified: "0 TODO/FIXME markers" (not implying zero Phase-2 stubs)
- E2e network resilience scaffolds marked as `// Phase 2: Network resilience e2e tests`

### 13. Coverage Push (+100 tests across 15+ modules)

| Target | Focus |
|--------|-------|
| `beardog-tunnel` | Server modes, BTSP provider, IPC server, crypto TLS certificates, hashing handlers, genetic handlers, BTSP handlers |
| `beardog-integration` | UPA client, Tower Atomic, heartbeat, connection tracking |
| `beardog-cli` | Client, cross-primal, birdsong, key, entropy handlers |
| `beardog-core` | Crypto service implementation, hybrid intelligence |
| `beardog-types` | Workflow types, unified config utils |
| `beardog-genetics` | Human entropy interaction capture |
| Root crate | main/lib coverage extensions |

---

## Gates

```bash
cargo fmt --check                               # Clean
cargo clippy --workspace --all-features \
  -- -D warnings                                # 0 warnings (2 pre-existing test-only)
cargo check --workspace --all-features          # Clean
cargo test --workspace                          # 14,600+ passed, 0 failures
cargo doc --workspace --no-deps                 # Clean (1 minor HTML tag warning)
cargo llvm-cov --workspace --summary-only       # 87.31% line, 87.91% region
```

---

## What's Next (Wave 18)

- **Coverage → 90%**: Continue targeting lowest-coverage crates (beardog-deploy ~82%, beardog-tunnel ~83%, beardog-cli ~83%)
- **CI pipeline consolidation**: 8 overlapping workflow files risk drift; consolidate `ci.yml`, `beardog-ci.yml`, `production-ci-cd.yml`, `production-ready.yml`
- **Missing CI scripts**: Add or remove references to `scripts/migrate-config.sh`, `scripts/run_benchmarks.sh`, and 9 production-ci-cd deployment scripts
- **Dockerfile binary name**: `CMD ["./beardog-core"]` should be `CMD ["./beardog"]`; features `production,quantum-resistant,simd` don't exist
- **Showcase compilation**: Verify standalone `exclude`d showcase crates still compile against current APIs
- **Phase-2 stubs**: ~90+ `// placeholder` / `// stub` comments remain in production code — candidates for real implementation or documented architectural boundaries
- **deploy.sh**: `scripts/active/deployment/deploy.sh` references nonexistent Helm charts; reconcile with `scripts/deployment/deploy-unified-ecosystem.sh`

---

## Files Changed (Summary)

- Root docs: `STATUS.md`, `CHANGELOG.md`
- Specs: `specs/PROJECT_STATUS.md`
- Protocol: `beardog-ipc/src/protocol.rs`, `beardog-ipc/src/multi_transport.rs`
- CLI: `beardog-cli/src/lib.rs`, `beardog-cli/src/handlers/server.rs`, `beardog-cli/src/handlers/daemon.rs`
- Tunnel: 15+ files (BTSP, IPC, crypto handlers, server modes, health, tracing)
- Core: 10+ files (self-knowledge, compliance, integration engine, secure messaging, evolution engine, safety)
- Types: workflow, unified config
- Config: port discovery
- Monitoring: performance, security metrics engines
- CI: `.github/workflows/beardog-ci.yml`
- Manifests: 22 `Cargo.toml` files (URLs)
- Cleanup: `core_integration_tests.rs` deleted, commented blocks removed from 3 files
- Tests: 15+ test files added/expanded

---

## Inter-Primal Notes

- No new compile-time coupling to any primal
- JSON-RPC wire contracts remain the only integration boundary
- JSON-RPC batch support is additive — existing single-request consumers unaffected
- BearDog continues to discover peers at runtime via capability registry
- Repository URLs now consistently point to `ecoPrimals/beardog` across all manifests
- `get_self_capabilities` now maps to `UniversalCapabilityType` taxonomy for ecosystem-wide capability advertisement

---

Part of ecoPrimals — sovereign, capability-based Rust ecosystem.
