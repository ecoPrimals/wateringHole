<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# loamSpine — v0.9.16 Deep Debt Evolution & Zero-Copy Hardening Handoff

**Date**: April 2, 2026
**Version**: 0.9.16 (continued from concurrent test evolution)
**Priority**: Informational — no blockers
**Cross-reference**: `LOAMSPINE_V0916_CONCURRENT_TEST_EVOLUTION_HANDOFF_APR01_2026.md`

---

## Summary

Deep debt elimination and zero-copy evolution across the loamSpine codebase. Addresses
allocation hotspots in resilient adapter retry loops, JSON-RPC envelope construction,
health check responses, and service advertisement. Eliminates remaining hardcoded
strings and `as` casts in production code. All root docs updated.

## Changes

### Zero-Copy / Allocation Reduction

| Target | Before | After |
|--------|--------|-------|
| `DiscoveryClient.endpoint` | `String` (cloned every resilient adapter call) | `Arc<str>` (O(1) clone) |
| `JsonRpcResponse.jsonrpc` | `"2.0".to_string()` per response | `Cow::Borrowed("2.0")` (zero alloc); `success()` promoted to `const fn` |
| `capability_list()` | Re-builds `serde_json::Value` per call | `OnceLock<Value>` — initialized once, returns `&'static Value` |
| `mcp_tools_list()` | Re-builds `serde_json::Value` per call | `OnceLock<Value>` — initialized once, returns `&'static Value` |
| `HealthStatus.version` | `env!("CARGO_PKG_VERSION").to_string()` per check | `OnceLock` via `cached_version()` |
| `HealthStatus.capabilities` | `ADVERTISED.iter().map(to_string).collect()` per check | `OnceLock` via `cached_capabilities()` |

### Hardcoding Elimination

- **`advertise_self` capabilities**: 7 hardcoded string literals replaced with
  `capabilities::identifiers::loamspine::ADVERTISED` (single source of truth).
- **Protocol identifiers**: `"tarpc"`, `"jsonrpc"`, `"/health"` → `constants::protocol::{TARPC, JSONRPC, HEALTH_PATH}`.
- **Metadata values**: `"rust"`, `"pure-rust"`, `"redb"` → `constants::metadata::{LANGUAGE, RPC_STYLE, STORAGE_BACKEND}`.
- Metadata construction evolved from 6 individual `.to_string()` pairs to a single
  `.map(|(k, v)| (k.to_string(), v.to_string()))` pass over `(&str, &str)` tuples.

### Structured Errors

- `check_health()` and `check_readiness()` evolved from `Result<_, String>` to
  `Result<_, HealthError>` with `thiserror`-derived variants:
  - `HealthError::StorageUnavailable`
  - `HealthError::DiscoveryUnavailable`

### Cast Safety

- `types.rs` hex encoder: `(b >> 4) as usize` → `usize::from(b >> 4)`;
  `as char` → `char::from(...)`.
- `spine.rs`, `proof.rs`, `backup/mod.rs`, `service/certificate.rs`,
  `transport/neural_api.rs`: all `as u64` → `u64::try_from().unwrap_or(u64::MAX)` or
  `.map_err(...)`.

### Test Extraction

- `transport/neural_api.rs` inline `#[cfg(test)] mod tests` (328 lines) extracted
  to `transport/neural_api_tests.rs` via `#[path]` pattern.

### Root Docs Updated

- `CHANGELOG.md`: v0.9.16 entry expanded with deep debt items and updated metrics.
- `STATUS.md`: New "Deep Debt Evolution" section; zero-copy and coverage metrics updated.
- `WHATS_NEXT.md`: `OnceLock` caching marked as completed; v0.9.16 section expanded.
- `README.md`: Coverage badge and quality table updated.
- `primal-capabilities.toml`: Version bumped to 0.9.16.

## Verification

```bash
cargo fmt --all -- --check                              # clean
cargo clippy --all-targets --all-features -- -D warnings # 0 warnings
cargo test --all-features                                # 1,270 passing
RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps  # 0 warnings
cargo deny check                                         # all pass
cargo llvm-cov --all-features --summary-only             # 91.96% line
```

## Metrics

| Metric | Value |
|--------|-------|
| Version | 0.9.16 |
| Tests | 1,270 |
| Coverage (line) | 91.96% |
| Coverage (region) | 87.07% |
| Coverage (function) | 93.39% |
| Clippy warnings | 0 |
| Doc warnings | 0 |
| Unsafe blocks | 0 |
| Source files | 129 |
| Max file size | 899 lines |
| `cargo deny` | all pass |

## Pattern for Other Primals

The `OnceLock` caching pattern for static JSON responses is reusable:

```rust
static CACHE: OnceLock<serde_json::Value> = OnceLock::new();

pub fn capability_list() -> &'static serde_json::Value {
    CACHE.get_or_init(|| serde_json::json!({ /* ... */ }))
}
```

The `Arc<str>` pattern for frequently-cloned config strings applies to any primal
with a resilient adapter or retry wrapper that clones the inner client.
