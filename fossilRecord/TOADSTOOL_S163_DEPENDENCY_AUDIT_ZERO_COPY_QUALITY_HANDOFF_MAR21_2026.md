<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# ToadStool S163 — Dependency Audit + Zero-Copy + Code Quality Handoff

**Date**: March 21, 2026
**Session**: S163
**Primal**: toadStool
**Type**: Dependency audit, zero-copy evolution, code quality, advisory elimination

## Summary

Session S163 executed a deep dependency audit and code quality sweep. **26 phantom
dependencies** removed across 10 crates — including `indicatif` (which eliminated
RUSTSEC-2025-0119), `figment`, `handlebars`, `nom`, `byteorder`, and 21 more. Zero-copy
improvements landed across 6 hot paths: `PrimalIdentity` trait returns references not
clones, `PluginManager` returns `&str` not `String`, protocol handler map uses `Arc<str>`
keys, JSON payload serialization bypasses intermediate String allocation, semantic method
listing returns `&'static str`, and protocol membership checks avoid per-call String
allocation. All `#[allow(dead_code)]` in production code evolved to `#[expect(dead_code,
reason)]` or `#[cfg(test)]`. Clippy zero warnings. All tests pass.

## Changes

### Phantom dependency removal (26 deps across 10 crates)

| Crate | Removed | Reason |
|-------|---------|--------|
| `toadstool-server` | `tracing-subscriber` | Library crate, not binary |
| `toadstool-integration-tests` | `async-trait`, `toadstool-common`, `tracing` | Never imported |
| `toadstool-cli` | `figment`, `handlebars`, `humantime-serde`, `indicatif` | Never imported |
| `toadstool-security-policies` | `indexmap`, `toadstool-config`, `tracing-subscriber` | Never imported |
| `toadstool-security-sandbox` | `indexmap`, `regex`, `serde_yaml_ng`, `thiserror`, `toadstool-config`, `tracing-subscriber` | Never imported |
| `toadstool-testing` | `async-trait`, `thiserror`, `toadstool-common`, `tracing-test` | Never imported |
| `toadstool-examples` | `clap`, `colored`, `futures`, `toadstool-auto-config`, `toadstool-management-resources`, `toadstool-management-performance`, `toadstool-security-policies`, `toadstool-security-sandbox` | Never imported |
| `akida-models` | `nom`, `byteorder` | Never imported |
| `akida-driver` | `tokio` (+ `async` feature) | Never imported |
| `cross-substrate-validation` | `tracing` | Never imported |
| `neurobench-runner` | `csv`, `rand`, `serde_json`, `tokio` | Never imported |

### Advisory elimination

- **RUSTSEC-2025-0119** (`number_prefix`): Eliminated by removing `indicatif` from CLI.
  `deny.toml` ignore entry removed. Down to 2 transitive advisory ignores (both
  unmaintained, no fix available).

### Zero-copy evolution (6 hot paths)

1. **`PrimalIdentity` trait**: `capabilities()` → `&[Capability]`, `endpoints()` → `&[ServiceEndpoint]`, `metadata()` → `&HashMap<String, String>` (eliminates deep clone per call)
2. **`PluginManager`**: `list_plugins()`, `active_plugins()`, `plugins_by_type()` → `Vec<&str>` (eliminates per-key String allocation)
3. **Semantic methods**: `list_semantic_methods()` → `Vec<&'static str>` (eliminates `String::from()` mapping from static registry)
4. **Protocol handler map**: `HashMap<String, Box<dyn MessageHandler>>` → `HashMap<Arc<str>, ...>` with `Arc::from()` on registration (matches `Arc<str>` message_type on lookup)
5. **JSON payload serialization**: 3× `response.payload.to_string().into_bytes().into()` → `Bytes::from(serde_json::to_vec(...))` (eliminates intermediate String allocation)
6. **Protocol membership checks**: `primal.protocols.contains(&"http".to_string())` → `.iter().any(|p| p == "http")` (eliminates per-check String allocation)

### Code quality tightening

- **`#[allow(dead_code)]` → `#[expect(dead_code, reason)]`**: `dispatch.rs` (DispatchJob.id, DispatchStatus::Running), `workload_manager.rs` (WorkloadMetadata), `http_server.rs` (ApiError)
- **`#[allow(dead_code)]` → `#[cfg(test)]`**: `display/ipc/client/mod.rs` (DEFAULT_IPC_TCP_ADDR)
- **Stale import removed**: `use async_trait::async_trait` in `primals/types/primal.rs` (never used)
- **Type alias**: `HandlerMap` for complex `Arc<RwLock<HashMap<Arc<str>, Box<dyn MessageHandler>>>>` (clippy type_complexity)
- **`deny.toml` license comments**: Updated to reflect AGPL-3.0-only as canonical

### async-trait audit conclusion

All ~102 `#[async_trait]` usages are on dyn-compatible traits (`Box<dyn T>` / `Arc<dyn T>`).
Native async fn in trait (Rust 2024) does not yet support dyn dispatch. Migration requires
static dispatch refactoring — deferred as design-level change.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --workspace --all-features` | PASS |
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-features` | PASS (0 warnings) |
| `cargo test --workspace --all-features` | PASS (21,600+ tests, 0 failures) |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo llvm-cov` | ~83% line coverage (188K lines instrumented) |

## Standards compliance vs `wateringHole/STANDARDS_AND_EXPECTATIONS.md`

| Expectation | S163 status |
|-------------|-------------|
| Rust 2024, toolchain | Met (`edition = "2024"` workspace-wide, MSRV 1.85.0) |
| Clippy pedantic + nursery, zero warnings | Met |
| Unsafe policy | 23 crates forbid + 20 deny = 43/43 covered |
| License AGPL-3.0-only | Met (all SPDX headers aligned) |
| Documentation | `cargo doc` clean |
| JSON-RPC / capability-first | No breaking IPC contract changes |
| Test coverage ≥90% | ~83%; remaining gap in hardware-dependent and distributed paths |
| ecoBin v3.0 | Certified; zero C FFI deps in default build path |
| Zero phantom deps | 26 eliminated this session; `cargo-machete` clean for core crates |

## Remaining debt

- **D-COV**: ~83% → 90% target. Gap concentrated in hardware-dependent paths (BAR0,
  thermal, VFIO dispatch), distributed modules, runtime backends.
- **D-ASYNC-TRAIT**: ~102 sites, all dyn-required. Deferred pending Rust dyn async evolution.
- **Edge runtime**: `toadstool-runtime-edge` excluded (libudev/serialport C dependency).

## Cross-primal notes

- No breaking JSON-RPC or capability surface changes.
- `PrimalIdentity` trait signature changed (returns references). Internal only — no
  cross-primal consumers.
- Dependency tree slimmed: `indicatif`, `figment`, `handlebars` removed from CLI. Build
  times may improve slightly for downstream.

---

*AGPL-3.0-only — ecoPrimals sovereign community property.*
