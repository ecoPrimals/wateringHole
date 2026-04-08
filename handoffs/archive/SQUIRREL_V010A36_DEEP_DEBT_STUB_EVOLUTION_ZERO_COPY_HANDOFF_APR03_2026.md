<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.36 — Deep Debt Execution, Stub Evolution, Zero-Copy (2026-04-03)

## Summary

Three sessions (I, J) covering primalSpring audit compliance, domain sovereignty
enforcement, production stub evolution, hardcoded self-reference cleanup, dead code
removal, and zero-copy evolution on discovery hot paths.

## Session I — primalSpring Audit Compliance

- **MockAIClient cfg gate hardened**: Removed blanket `#[allow(warnings)]` from
  `ai-tools/tests/basic_test.rs`; replaced with targeted lint allows
- **ed25519-dalek overstep resolved**: Moved to optional dep behind `local-crypto`
  feature; `SecurityManagerImpl` crypto paths gated with `#[cfg(feature)]`; default
  build is zero-crypto (delegates to BearDog capability discovery)
- **sled/sqlx confirmed clean**: sled absent; sqlx properly optional behind `persistence`

## Session J — Deep Debt Execution

### Production stubs evolved to complete implementations

- `create_compute_from_type` — Removed vendor match arms (k8s/docker/nomad/toadstool);
  added `LocalProcessProvider` with workload tracking; non-local delegates via
  `compute.execute` capability discovery
- `auto_detect_compute_provider` — Removed ToadStool-specific detection; uses
  `COMPUTE_ENDPOINT` env for capability-based detection, falls back to local
- `SecurePluginStub::execute` — Returns `SecurityError` (sandbox rejects execution)
- `AiIntelligence` — `analyze_ecosystem_state`, `generate_optimizations`,
  `generate_ecosystem_report` now use actual engine telemetry instead of hardcoded values
- `IntelligenceEngine/OptimizationEngine/PredictionEngine` — `initialize()` logs real
  state; `is_healthy()` checks actual model/strategy availability
- `ContextAnalytics/StateVersioning` — Track actual metrics, log snapshots

### Hardcoded self-references → `niche::PRIMAL_ID`

20+ production files evolved from `"squirrel"` string literals to `crate::niche::PRIMAL_ID`:
adapters (storage, compute, orchestration, security), primal_provider (core,
health_monitoring, ecosystem_integration), rpc (jsonrpc_server, unix_socket),
tool/executor, security/beardog_coordinator, ecosystem/manager, biomeos_integration/mod,
universal_provider, discovery/self_knowledge.

### Dead code cleanup

Removed 42KB of orphaned `sync/manager.rs` (917 lines) and `sync/types.rs` (368 lines) —
never compiled (not declared as submodules of `sync.rs`).

### Zero-copy evolution

`ServiceInfo` string fields (`service_id`, `name`, `category`, `endpoints`) evolved
from `String` → `Arc<str>` — eliminates deep copies in capability discovery queries.

### Docs updated

README.md, CONTEXT.md, CURRENT_STATUS.md synced to accurate metrics.

## Verification

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | 6,856 passed, 0 failed, 107 ignored |
| `cargo doc --no-deps` | PASS |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Metrics

| Metric | Value |
|--------|-------|
| Version | 0.1.0-alpha.36 |
| `.rs` files | 1,004 |
| Lines of Rust | ~341k |
| Tests | 6,856 pass / 0 fail / 107 ignored |
| Clippy warnings | 0 |
| Files >1000 lines | 0 |
| Production mocks | 0 |
| `unsafe` code | 0 (forbid) |
| TODO/FIXME/HACK | 0 |

## Remaining debt

- Coverage ~86% — gap to 90% is IPC/network code needing integration infra, demo bins
- `async-trait` used throughout — progressive migration to native Rust 2024 async trait
- `base64` duplicate (0.21 via `config`/`ron`, 0.22 direct) — transitive, benign
- `ring` transitive via `rustls`/`sqlx`/`jsonwebtoken` — tracked in `docs/CRYPTO_MIGRATION.md`

## Open gaps

None in gap registry. Build green, clippy clean, tests passing.
