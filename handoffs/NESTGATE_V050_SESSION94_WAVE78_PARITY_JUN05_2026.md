# NestGate v0.5.0 — Session 94: Wave 78 Parity

**Date**: 2026-06-05  
**Wave**: 78  
**Gate**: ironGate  

## Deliverables

### 1. `config/capability_registry.toml` (Wave 78 ecosystem convention)
- Moved existing root `capability_registry.toml` (294 lines, 18 capability sections, 81+ methods) to `config/` per ecosystem convention (matches biomeOS, petalTongue, sweetGrass)
- Root file retained as backward-compat pointer
- Added HTTP direct content serving (`GET /content/:hash`) documentation to registry

### 2. Coverage sprint: 46 new tests (content pipeline + HTTP API handlers)

| Area | New Tests | Coverage Target |
|------|-----------|-----------------|
| Content dispatch routing (`dispatch_coverage_tests.rs`) | 10 | Every `content.*` through UDS dispatch |
| Storage path builders (`storage_path_tests.rs`) | 19 | `content_key_path`, `manifest_path`, `dataset_key_path`, `blob_key_path`, `extract_namespace`, `resolve_family_id`, `ensure_parent_dirs` |
| Content stream edge cases (`content_stream.rs`) | 9 | Missing params, oversized total, unknown stream_id, bad offset, exceeding size, invalid base64, missing family_id, invalid hash |
| Transport handler content dispatch (`transport/handlers.rs`) | 8 | Every `content.*` through HTTP transport layer |

### 3. Metrics

| Metric | Session 93 | Session 94 | Delta |
|--------|-----------|-----------|-------|
| Total tests | 12,574 | 13,035 | +461 |
| Lib tests | 9,101 | 9,212 | +111 |
| nestgate-rpc tests | 762 | 800 | +38 |
| nestgate-api tests | 2,289 | 2,297 | +8 |
| Clippy warnings | 0 | 0 | — |
| Test failures | 0 | 0 | — |

## Wave 78 Status

- [x] Zero clippy (pedantic + nursery)
- [x] Zero `#[allow]` in production
- [x] `config/capability_registry.toml` (machine-readable, TOML)
- [x] `forbid(unsafe_code)` on every crate root
- [ ] Coverage 84% → 90% (in progress — 46 tests added this session, more needed)

## Files Changed

- `config/capability_registry.toml` — NEW (canonical location)
- `capability_registry.toml` — Updated header to point to canonical
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/tests/dispatch_coverage_tests.rs`
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/tests/storage_path_tests.rs` — NEW
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/tests/mod.rs`
- `code/crates/nestgate-rpc/src/rpc/content_stream.rs`
- `code/crates/nestgate-api/src/transport/handlers.rs`
- `CHANGELOG.md`
- `sporeprint/validation-summary.md`
