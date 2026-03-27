# Squirrel v1.9.0 — Spring Pattern Absorption Handoff

**Date**: March 14, 2026  
**Session**: Spring Absorption & Cleanup  
**Previous**: `SQUIRREL_V180_DEEP_EVOLUTION_PUBLIC_RELEASE_PREP_HANDOFF_MAR14_2026.md`  
**Status**: COMPLETE — ready to push

---

## Session Summary

Absorbed proven patterns from the 7 Spring repositories (neuralSpring, groundSpring, ludoSpring, wetSpring, airSpring, healthSpring, hotSpring) into squirrel, cleaned debris, updated all root documentation, and prepared for push.

---

## Changes Made

### Phase 1: `#[expect]` Migration + Doc Lint Hardening

- **60 `#[allow(...)]` → `#[expect(..., reason = "...")]`** across all crates (Rust 1.81+ self-cleaning pattern from ludoSpring/neuralSpring). 15 unnecessary suppressions removed entirely.
- **`RUSTDOCFLAGS="-D warnings"`** added to `.github/workflows/ci.yml` and `PRE_PUSH_CHECKLIST.md`. Doc warnings now block CI.

### Phase 2: SLO/Tolerance Registry + Provenance

- **`crates/universal-constants/src/slo.rs`**: 18+ named SLO constants covering AI latency (P50/P95/P99/hard timeout), cost (per-query, per-day, per-1K-token), quality (relevance, coherence, hallucination), throughput, availability, and benchmark gates. `all_slos()` / `slos_by_category()` for runtime introspection. Follows neuralSpring `tolerances/mod.rs` pattern.
- **`crates/universal-patterns/src/provenance.rs`**: `Provenance` struct with builder pattern, serde, Display. Fields: script, commit, date, command, environment, timestamp. `Provenance::auto()` captures current environment. Wired into `BenchmarkResult`.
- **Fixed pre-existing `Arc<str>` serde issue** by enabling `serde` `rc` feature in workspace `Cargo.toml`.

### Phase 3: Socket Discovery Alignment

- **`crates/universal-constants/src/network.rs`**: Added `BIOMEOS_SOCKET_SUBDIR`, `BIOMEOS_SOCKET_FALLBACK_DIR`, `get_socket_dir()`, `get_socket_path()` — ecosystem XDG convention.
- **Fixed 7 deviations** in doctor.rs, ipc_client.rs, transport/discovery.rs, registry/discovery.rs, mcp/task/client.rs, mcp/sync/mod.rs, capability_http.rs. All now use `$XDG_RUNTIME_DIR/biomeos/{primal}.sock` with `/tmp/biomeos/` fallback.

### Phase 4: MCP Integration (neuralSpring Adapter Support)

- **`capability.announce`**: Extended request with `primal`, `socket_path`, `tools` fields. Handler now persists announcements in server's `announced_tools` registry for routing.
- **`tool.execute`**: Checks announced-primal registry first. If tool was announced by a remote primal, forwards via Unix socket JSON-RPC.
- **`tool.list`**: New method added to JSON-RPC dispatch. Returns local built-ins + all remote announced tools.

### Phase 5: Bare `unwrap()` Audit

- 9 production `.unwrap()` calls (all in benchmarking/mod.rs) replaced with descriptive `.expect("reason")`.

### Debris Cleanup

- **Orphaned code archived** to `archive/orphaned_code_mar_2026/`:
  - `crates/main/core/` (orphaned duplicate)
  - `crates/tools/arc-str-migrator/` (one-shot migration tool)
  - `crates/plugins/` (not in workspace)
  - `crates/interfaces-test-workspace/` (not in workspace)
- **Stale scripts archived**: `validate_deployment.sh`, `quick_validate.sh`, `test-mcp-connection.sh`, `build-and-run.ps1`
- **CI fixes**: Removed `web_server` binary build (doesn't exist), fixed Docker path to repo-root `Dockerfile`, removed `code-analysis.yml` steps referencing non-existent Python scripts.

### Root Doc Updates

- All docs updated: test count 4,240 → 4,127, Rust 1.80+ → 1.81+
- CHANGELOG.md: new "Spring Pattern Absorption" section under March 14 entry
- ORIGIN.md: test count 4,100 → 4,127

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests passing | 4,240 | 4,127 |
| Test failures | 0 | 0 |
| Line coverage | 66% | 66% |
| Region coverage | 68% | 68% |
| `#[allow]` in prod | ~65 | ~5 (crate-level `#![allow]` only) |
| `#[expect]` in prod | 0 | 60 |
| Bare `.unwrap()` in prod | 9 | 0 |
| Rustdoc warnings | 0 | 0 (CI enforced) |
| Socket path deviations | 7 | 0 |
| `tool.list` handler | missing | implemented |

Note: Test count decreased because some stale/orphaned test modules were archived. No test regressions.

---

## Files Changed (Key)

### New Files
- `crates/universal-constants/src/slo.rs`
- `crates/universal-patterns/src/provenance.rs`

### Modified (Selection)
- `Cargo.toml` (workspace: serde `rc` feature)
- `.github/workflows/ci.yml` (RUSTDOCFLAGS, remove web_server, fix Docker path)
- `.github/workflows/code-analysis.yml` (remove dead steps)
- `crates/universal-constants/src/network.rs` (socket path constants + discovery)
- `crates/universal-constants/src/lib.rs` (slo module)
- `crates/universal-patterns/src/lib.rs` (provenance module)
- `crates/main/src/rpc/types.rs` (AnnounceCapabilitiesRequest extended, ToolListResponse added)
- `crates/main/src/rpc/jsonrpc_handlers.rs` (announce stores, execute forwards, list_tools added)
- `crates/main/src/rpc/jsonrpc_server.rs` (announced_tools registry, tool.list dispatch)
- `crates/main/src/benchmarking/mod.rs` (provenance field, unwrap→expect)
- `crates/main/src/doctor.rs` (XDG socket paths)
- `crates/tools/ai-tools/Cargo.toml` (universal-constants dep)
- `crates/tools/ai-tools/src/capability_http.rs` (XDG socket path)
- 60+ .rs files (`#[allow]` → `#[expect]`)
- All root .md docs (metrics, changelog)

### Archived
- `crates/main/core/`, `crates/tools/arc-str-migrator/`, `crates/plugins/`, `crates/interfaces-test-workspace/`
- `scripts/validate_deployment.sh`, `scripts/quick_validate.sh`, `test-mcp-connection.sh`, `scripts/windows/build-and-run.ps1`

---

## Remaining Work

- **Coverage push**: 66% → 90% target. Focus on config, universal-patterns, ecosystem-api.
- **Streaming pattern**: wetSpring/healthSpring streaming over round-trip for AI context.
- **airSpring Provider trait**: Could inform squirrel's AI provider abstraction.
- **Tolerance crate extraction**: Springs each have their own tolerance modules. A shared ecosystem crate is a wateringHole-level decision.

---

## Verification

```
cargo check --workspace          # PASS (0 errors)
cargo test --workspace           # 4,127 passed / 0 failed
cargo fmt --all -- --check       # CLEAN
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps  # CLEAN
```

---

## wateringHole Compliance

- [x] AGPL-3.0-only on all 31 crates
- [x] `#![forbid(unsafe_code)]` on all lib.rs
- [x] JSON-RPC + tarpc (no gRPC)
- [x] Capability-based discovery (TRUE PRIMAL)
- [x] All files < 1000 lines
- [x] Zero mocks in production code
- [x] `#[expect]` over `#[allow]` (ecosystem standard)
- [x] RUSTDOCFLAGS="-D warnings" in CI
- [x] XDG socket paths (`$XDG_RUNTIME_DIR/biomeos/`)
- [x] SLO registry (no magic numbers)
- [x] Provenance tracking on benchmarks
