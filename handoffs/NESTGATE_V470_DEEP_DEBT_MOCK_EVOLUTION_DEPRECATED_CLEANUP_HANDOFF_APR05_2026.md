# NestGate v4.7.0-dev — Deep Debt Resolution, Mock Evolution & Deprecated Code Cleanup

**Date**: April 5, 2026
**Scope**: Production mock elimination, deprecated dead-code removal, hardcoded-port undeprecation, idiomatic Rust evolution

---

## Summary

Systematic deep debt resolution across the NestGate codebase. Eliminated the only
production mock (hardcoded memory stats), removed 23 dead deprecated functions with
zero callers, undeprecated 4 URL builders that were evolved to runtime-resolved,
and cleaned stale migration documentation.

---

## Changes

### Production mock elimination

| File | Before | After |
|------|--------|-------|
| `nestgate-storage/.../storage_detector/analysis.rs` | Hardcoded `16GB total / 8GB free` mock memory | Real `/proc/meminfo` reader with graceful fallback |

### Deprecated dead-code removal (23 functions, 0 callers)

| Module | Functions removed |
|--------|------------------|
| `config/migration_bridge.rs` | `get_api_port`, `get_api_host`, `get_bind_address`, `get_metrics_port`, `get_zfs_pool`, `get_data_dir`, `get_timeout_secs`, `get_read_timeout_secs`, `reset_for_testing` (9) |
| `constants/network_defaults.rs` | `get_bind_address`, `get_api_host`, `get_db_host`, `get_redis_host`, `is_production`, `is_development` (6) |
| `constants/ports.rs` | `api_server_port`, `dev_server_port`, `metrics_server_port`, `postgres_port`, `redis_port`, `mongodb_port`, `primal_discovery_port` (7) |
| `defaults.rs` | `env_helpers` module (5 fns) + `urls` module (3 fns) removed entirely |

All had **zero** external callers — verified via `rg` before removal. Tests updated accordingly.

### Undeprecated runtime URL builders

`build_api_url()`, `build_websocket_url()`, `build_metrics_url()`, `build_endpoint()` in
`canonical_defaults.rs` were deprecated because they used hardcoded `const` fallbacks.
Now they delegate to the runtime-resolved `default_*_url()` functions (env-var → discovery → fallback).
Removed 3 stale `#[expect(deprecated)]` suppressions from callers.

### Idiomatic Rust fixes

- `format!("{}", x)` → `x.to_string()` in production CLI code
- Misleading `production_placeholders.rs` doc comments updated (it's a real `/proc`-backed implementation)
- Stale "MIGRATION NOTE (Week 2, Dec 2025)" markers removed from 4 module docs
- `DEFAULT_WEB_UI_URL` const now properly `#[deprecated]` (was the only one missing it)
- Unfulfilled `#[expect(deprecated)]` in `biomeos_integration_tests.rs` cleaned

### Root docs updated

- Test counts: ~11,685 → ~11,821 (reflects `--all-features` runs)
- Deprecated API description updated (188 markers, 0 dead callers)
- STATUS.md, README.md, QUICK_REFERENCE.md aligned

---

## Audit results (confirmed)

| Metric | Value |
|--------|-------|
| `#[deprecated]` attributes | 188 (all intentional migration markers) |
| `#[allow(` | 0 (migrated to `#[expect(`) |
| Dead deprecated functions | 0 (23 removed this session) |
| Production mocks | 0 (memory stats replaced with `/proc/meminfo`) |
| Unsafe blocks | 0 (`#![forbid(unsafe_code)]` all crate roots) |
| `AGPL-3.0-only` in code | 0 (all `AGPL-3.0-or-later`) |
| Files > 1000 lines | 0 (max ~712) |
| External C deps | 0 (pure Rust stack) |
| Dev-stubs in defaults | 0 (`dev-stubs` not in any `default` feature) |

---

## Validation

```
cargo fmt --all -- --check       PASS
cargo clippy --all-features --workspace -- -D warnings   PASS (0 warnings)
cargo check --all-features --workspace   PASS
cargo test --all-features --workspace    11,821 passed, 0 failed, 463 ignored
```

---

## Remaining work

| Area | Status |
|------|--------|
| Coverage gap to 90% | ~10pp remaining (80% measured) |
| 188 `#[deprecated]` markers | Intentional — callers migrated; markers guide future cleanup |
| `Box<dyn Error>` in jsonrpc_server | jsonrpsee library boundary; needs `From<jsonrpsee::Error>` for NestGateError |
| `String` param signatures | ~10 functions could take `&str`; API-breaking change, defer |
| Specs from 2024-2025 | Historical design docs — kept as architectural fossil record |
