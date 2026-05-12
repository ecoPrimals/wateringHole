# ToadStool S203g Handoff — Deep Debt: Test Extraction + Deprecated Removal + Idiomatic Evolution

**Date**: April 13, 2026
**Primal**: ToadStool
**Session**: S203g
**Status**: DELIVERED — quality gates green

## Changes

### 1. Smart File Refactoring — 12 Production Files

Extracted inline `#[cfg(test)] mod tests { ... }` blocks from 12 production files >540 LOC
into companion `*_tests.rs` files. Same pattern established in S203c/S203e.

| Source | Companion | Original LOC |
|--------|-----------|-------------|
| `testing/builders.rs` | `builders_tests.rs` | 680 |
| `mainframe/as400/mod.rs` | `as400_tests.rs` | 596 |
| `backends/cpu/mod.rs` | `cpu_tests.rs` | 575 |
| `coordination_integration/client/rpc.rs` | `rpc_tests.rs` | 575 |
| `zero_config/service_discovery.rs` | `service_discovery_tests.rs` | 572 |
| `security_provider/software_hsm.rs` | `software_hsm_tests.rs` | 567 |
| `integration/storage/client.rs` | `client_tests.rs` | 566 |
| `ecosystem/adapters/crypto.rs` | `crypto_tests.rs` | 566 |
| `security/client_evolved/mod.rs` | `client_evolved_tests.rs` | 563 |
| `coordination/distribution.rs` | `distribution_tests.rs` | 554 |
| `service_discovery/service.rs` | `service_tests.rs` | 551 |
| `toadstool-core/npu_dispatch.rs` | `npu_dispatch_tests.rs` | 549 |

Combined with S203c (5 files) and S203e (5 files), **22 total large-file extractions** since deep audit began.

### 2. Deprecated Code Removal — 6 Items (Zero External Callers)

All confirmed zero external callers via workspace-wide grep before removal:

- `FallbackEndpoints::localhost_endpoint` (since 0.3.0) → use `fallback_endpoint()`
- `METRICS_PORT` constant (since 0.1.0) → use `toadstool_config::ports::metrics_port()`
- `capability_typical_provider` + entire `primal_capabilities` module (since 0.92.0) → use `infant_discovery`
- `get_primal_default_port` wrappers in `ConfigUtils` and `config_utils::network` (since 0.15.0) → use `resolve_capability_port`
- `resolve_legacy_primal_default_port` internal function (zero callers after wrapper removal)
- `TarpcClient::address()` (since 0.2.0) → use `endpoint()`

### 3. Idiomatic Rust Evolution

**Async GPU Discovery** (`server/resource_validator/system_query.rs`):
- Before: blocking `std::thread::sleep(50ms)` poll loop inside `async fn` — blocks the tokio executor
- After: `tokio::sync::oneshot` channel from worker thread + `tokio::time::timeout` — fully async-native

**Forward Dispatch Clone** (`server/pure_jsonrpc/handler/dispatch/forward.rs`):
- Before: `p.get("params").cloned().unwrap_or_else(|| p.clone())` — deep-clones entire request when `params` absent
- After: falls back to empty `serde_json::Map` instead of cloning the full payload

## Verification

- `cargo clippy --workspace --all-targets`: 0 warnings
- `cargo test --workspace --lib`: 7,289 tests, 0 failures (43 crate suites)
- `cargo check --workspace --all-targets`: clean

## Remaining Polish

- Coverage 83.6% → 90% target (D-COVERAGE-GAP)
- `async-trait` modernization (~320 instances — Rust language constraint, pending native `async fn in dyn Trait`)
- V4L2 ioctl cleanup
- Fuzz seed corpus + extended campaigns
