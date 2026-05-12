# Songbird v0.2.1 Wave 134 — primalSpring Gap Resolution + Deep Debt Cleanup

**Date**: April 11, 2026
**Primal**: Songbird
**Version**: v0.2.1
**License**: AGPL-3.0-or-later

---

## Summary

Wave 134 resolves all 6 gaps from the primalSpring cross-spring upstream gap synthesis
(April 11, 2026) and completes a deep debt cleanup pass across all 30 crates.

**Tests**: 13,031 passed, 0 failed, 252 ignored (+22 from Wave 133)
**Clippy**: Zero warnings (`clippy::pedantic + nursery`, `--all-targets`, `-D warnings`)
**Fmt**: Clean (`cargo fmt --check` passes)
**cargo-deny**: Fully passing, now enforced in CI

---

## primalSpring Gap Resolution

### 1. `capability.resolve` Single-Step Routing (Medium — RESOLVED)

**Source**: wetSpring PG-03, healthSpring §3, all springs

Springs need `capability.resolve` returning a single best endpoint for a given
capability, not a list. This is the IPC equivalent of DNS resolution.

**Implementation**:
- `CapabilityResolveParams` / `CapabilityResolveResult` DTOs in `service_types.rs`
- `resolve_by_capability()` on `ServiceRegistry` (returns single best provider)
- `handle_capability_resolve()` handler in `ipc_registry.rs`
- `CapabilitiesMethod::Resolve` variant in `JsonRpcMethod` enum
- Dispatch wired in `dispatch.rs` for `"capability.resolve"`

### 2. Deploy-Time `consumed_capabilities` Completeness Check (Low — RESOLVED)

**Source**: wetSpring V143 handoff

biomeOS should verify all `consumed_capabilities` are satisfiable before graph deployment.

**Implementation**:
- `ValidateConsumedResult` DTO with per-capability satisfaction status
- `handle_validate_consumed()` handler checks registry for each consumed capability
- `CONSUMED_CAPABILITIES` exported from `capability_tokens.rs` (made `pub`)
- Dispatch wired for `"lifecycle.validate_consumed"`

### 3. `lifecycle.composition` for Live Dashboards (Low — RESOLVED)

**Source**: ludoSpring handoff

Wire method returning current composition state for real-time monitoring.

**Implementation**:
- `CompositionState` / `CompositionPrimalInfo` DTOs
- `handle_lifecycle_composition()` returns registered primals, live capabilities, health
- `LifecycleMethod` enum with `Composition` and `ValidateConsumed` variants
- Dispatch wired for `"lifecycle.composition"`

### 4. Canonical Naming — Discovery Dual Fallback (RESOLVED)

**Source**: healthSpring §3

`discovery.find_by_capability` vs `net.discovery.find_by_capability` dual fallback.

**Implementation**:
- `normalize_json_rpc_method_name()` now absorbs both aliases → `ipc.discover`
- Also absorbs `capability.discover` → `ipc.discover`
- Zero-config: callers using any variant hit the same handler

### 5. CI-01: `cargo deny check` Enforcement (Medium — RESOLVED)

**Source**: primalSpring infrastructure

`cargo deny check bans` was not enforced in any primal's CI pipeline.

**Implementation**:
- `.github/workflows/ci.yml`: added `cargo-deny` install step + `cargo deny check` step
- Runs full check (bans + licenses + advisories + sources) on every PR/push

### 6. Canonical Inference Namespace (Medium — RESOLVED)

**Source**: healthSpring §4, neuralSpring Gap 1, ludoSpring GAP-10

Springs accept `inference.*` / `model.*` / `ai.*` inconsistently.

**Implementation**:
- `InferenceMethod` enum: `Infer`, `Status`, `List`, `Load`
- `normalize_json_rpc_method_name()` absorbs `model.*`/`ai.*` → `inference.*`
- Dispatch wired for all `inference.*` methods
- Songbird canonical: `inference.*` is the standard namespace

---

## Deep Debt Cleanup

### `#[expect(dead_code)]` → `#[allow(dead_code)]` Migration

45+ `#[expect(dead_code)]` attributes across 30 files converted to `#[allow(dead_code)]`.

**Root cause**: `dead_code` lint is cfg-dependent — items used only from `#[cfg(test)]`
modules appear dead in non-test builds but alive in test builds. Using `#[expect]`
causes `unfulfilled-lint-expectations` errors when the lint doesn't fire (test builds).
`#[allow]` is the correct suppression for cfg-dependent lints.

Also converted module-level `#![expect(clippy::clone_on_ref_ptr)]`,
`#![expect(clippy::expect_used)]`, `#![expect(clippy::missing_errors_doc)]` to
`#![allow(...)]` in `songbird-universal-ipc` and `songbird-network-federation`.

### Dead Code Removal (6 functions)

| Function | Crate | Reason |
|----------|-------|--------|
| `display_error_with_troubleshooting()` | songbird-cli | Unused, superseded |
| `print_banner()` | songbird-cli | Unused, superseded |
| `save_internet_config()` | songbird-cli | Unused stub |
| `InternetConnectionWizard::setup()` | songbird-cli | Unused stub |
| `detect_system_resources_fast()` | songbird-cli | Unused stub |
| `normalize_inference_namespace()` | songbird-types | Superseded by inline normalization |

### Reserved Fields Wired (3 modules)

- `HealthMonitor.nodes`: `register_node()`, `update_node_health()`, `get_all_node_health()`
- `ObservabilityManager.metrics_store`: `update_metrics()`, `get_metrics()` (reads store), `get_all_metrics()`
- `RuntimeDiscoveryEngine.capabilities`: `required_capabilities()` accessor

### Clippy Fixes

- `clippy::manual_string_new` in `discovery_bridge.rs` test
- `clippy::let_else` in `tower_atomic/tests/mod.rs`
- `clippy::redundant_pub_crate` in `discovery_test_sync.rs` and sovereignty test helpers
- `clippy::type_complexity` in `http_handler/handler.rs` test (extracted `type CapturedRequest`)
- `clippy::unwrap_used` in `btsp_client.rs` test (→ `expect` + module-level allow)

### Test Fixes

- `biomeos_e2e_deployment.rs`: assertion updated `network-{family}.sock` → `songbird-{family}.sock`
- `biomeos_fault_injection.rs`: same socket naming fix

---

## Downstream Impact

| Consumer | Impact |
|----------|--------|
| **biomeOS** | Can now call `capability.resolve` for single-step routing; `lifecycle.composition` available for dashboards; `lifecycle.validate_consumed` for deploy-time graph validation |
| **Springs** | `inference.*` canonical namespace standardized; `model.*`/`ai.*` aliases absorbed transparently |
| **All primals** | `discovery.find_by_capability` / `net.discovery.find_by_capability` → `ipc.discover` normalization eliminates dual-fallback |
| **primalSpring** | CI-01 resolved for Songbird; pattern available for other primals |

---

## Verification

```
cargo fmt --check                                           # PASS
cargo clippy --workspace --all-targets -- -D warnings       # PASS (zero warnings)
cargo test --workspace                                      # 13,031 passed, 0 failed
cargo deny check                                            # PASS
```
