<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# LoamSpine v0.9.14 — const fn Promotions, #[non_exhaustive] Forward Compat & Configurable tarpc

**Date**: March 24, 2026  
**From**: LoamSpine  
**To**: All Springs, All Primals, biomeOS  
**Status**: Complete, ready for push

---

## Summary

LoamSpine v0.9.14 deepens idiomatic Rust evolution and forward compatibility:
compile-time evaluation where possible, enum stability for cross-crate
consumers, configurable server limits, and smart domain-based test extraction.

1. **`const fn` promotions** — 11 functions promoted to `const fn`, enabling
   compile-time evaluation. Workspace lint `missing_const_for_fn` evolved
   from `allow` to `warn` to catch future regressions.

2. **`#[non_exhaustive]` forward compatibility** — 14 public enums annotated.
   Downstream crates can add wildcard match arms now; future variant additions
   won't break consumers. Cross-crate `From<LoamSpineError>` updated with
   catch-all arm as reference pattern.

3. **`DiscoveryProtocol` disambiguation** — Infant discovery's `DiscoveryMethod`
   renamed to `DiscoveryProtocol` to eliminate naming collision with
   `config::DiscoveryMethod` (46 references across 3 files).

4. **`TarpcServerConfig` configurable** — Hardcoded `TARPC_MAX_CONCURRENT_REQUESTS`
   (100) and `TARPC_MAX_CHANNELS_PER_IP` (10) evolved to a `TarpcServerConfig`
   struct with `run_tarpc_server_with_config()`. Backward-compatible
   `run_tarpc_server()` preserved.

5. **Smart test refactor** — `sled_tests.rs` 954 → 725 lines via certificate
   test extraction to `sled_tests_certificate.rs` (206 lines), following
   the existing `redb_tests_cert_errors.rs` domain-split pattern.

---

## Code Changes

| File | Change |
|------|--------|
| `loam-spine-core/src/certificate/usage.rs` | `UsageSummary::is_empty` → `pub const fn` |
| `loam-spine-core/src/streaming.rs` | `StreamItem::data` → `pub const fn` |
| `loam-spine-core/src/trio_types.rs` | `default_contribution_weight` → `const fn` |
| `loam-spine-core/src/waypoint.rs` | `AttestationRequirement::is_required`, `RelendingChain::new` → `pub const fn`; `#[non_exhaustive]` on 4 enums |
| `loam-spine-core/src/resilience.rs` | 4 functions → `const fn`; `#[non_exhaustive]` on `CircuitState` |
| `loam-spine-core/src/service/expiry_sweeper.rs` | `ExpirySweeper::new` → `pub const fn` |
| `loam-spine-core/src/error.rs` | `#[non_exhaustive]` on `IpcErrorPhase`, `LoamSpineError` |
| `loam-spine-core/src/spine.rs` | `#[non_exhaustive]` on `SpineState` |
| `loam-spine-core/src/primal.rs` | `#[non_exhaustive]` on `PrimalState`, `HealthStatus` |
| `loam-spine-core/src/service/lifecycle.rs` | `#[non_exhaustive]` on `ServiceState` |
| `loam-spine-core/src/discovery/mod.rs` | `#[non_exhaustive]` on `CapabilityStatus` |
| `loam-spine-core/src/infant_discovery/mod.rs` | `DiscoveryMethod` → `DiscoveryProtocol` |
| `loam-spine-api/src/error.rs` | `#[non_exhaustive]` on `ApiError`, `ServerError`; catch-all arm for `LoamSpineError` |
| `loam-spine-api/src/tarpc_server.rs` | `TarpcServerConfig` struct, `run_tarpc_server_with_config()` |
| `loam-spine-core/src/storage/sled_tests.rs` | Certificate tests extracted (954 → 725 lines) |
| `loam-spine-core/src/storage/sled_tests_certificate.rs` | New: 206 lines of certificate-focused sled tests |
| `Cargo.toml` | `missing_const_for_fn = "warn"`, version bump |

---

## Metrics

| Metric | v0.9.13 | v0.9.14 |
|--------|---------|---------|
| Tests | 1,312 | **1,312** |
| Coverage (line) | 90.02% | **92.11%** |
| Coverage (region) | 91.99% | **90.33%** |
| Coverage (function) | 86.30% | **87.83%** |
| Clippy | 0 | 0 (+ `missing_const_for_fn` at warn) |
| Doc warnings | 0 | 0 |
| Max file | 954 | **885** |
| Source files | 130 | **131** (+1 extracted test) |
| Unsafe | 0 (`forbid`) | 0 (`forbid`) |

---

## What Other Primals Should Know

- **`#[non_exhaustive]` on LoamSpine enums**: If you match on `LoamSpineError`,
  `ApiError`, `ServerError`, `IpcErrorPhase`, or any status enum, you now need
  a wildcard arm. This is the standard forward-compatibility pattern — add it
  now to avoid breakage on future releases.

- **`TarpcServerConfig`**: The default concurrency (100 requests, 10 channels/IP)
  is unchanged. Use `run_tarpc_server_with_config()` if you need to tune these
  for high-throughput inter-primal workloads.

- **`DiscoveryProtocol`**: If you imported `infant_discovery::DiscoveryMethod`,
  it is now `DiscoveryProtocol`. This type was not re-exported from the public
  API, so impact should be limited to direct crate consumers.

- **`missing_const_for_fn` at warn level**: Pattern available for absorption.
  Catches any function that could be `const` but isn't. Zero-cost at runtime,
  enables compile-time evaluation for downstream users.

---

## Patterns Available for Absorption

| Pattern | Where | What |
|---------|-------|------|
| `#[non_exhaustive]` on public enums | 14 enums across core/api | Forward-compatible matching for cross-crate consumers |
| `missing_const_for_fn = "warn"` | workspace `Cargo.toml` | Catches `const fn` candidates at lint time |
| `TarpcServerConfig` struct | `tarpc_server.rs` | Configurable concurrency instead of hardcoded constants |
| Domain-split test extraction | `sled_tests_certificate.rs` | Smart refactoring by domain cohesion, not line count |
| Catch-all arm for `#[non_exhaustive]` | `api/error.rs` `From` impl | Reference pattern for downstream enum matching |

---

## Verification

All checks pass:
- `cargo fmt --check` — clean
- `cargo clippy --all-targets --all-features -- -D warnings` — 0 warnings
- `cargo doc --no-deps` — 0 warnings
- `cargo test --all-features` — 1,312 tests passing
- `cargo llvm-cov --workspace --summary-only` — 92.11% line / 90.33% region / 87.83% function
