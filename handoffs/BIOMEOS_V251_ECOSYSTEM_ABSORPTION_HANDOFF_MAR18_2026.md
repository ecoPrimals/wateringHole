# biomeOS v2.51 — Ecosystem Absorption Handoff

**Date**: March 18, 2026
**From**: biomeOS v2.50 (deep debt audit complete)
**To**: biomeOS v2.51 (ecosystem pattern absorption)

## Summary

Reviewed all 8 springs (airSpring v0.10, groundSpring v115, healthSpring v37, hotSpring, ludoSpring v24, neuralSpring v118, primalSpring v0.2.0, wetSpring v128), all phase1 primals (beardog v0.9.0, songbird v0.2.2, squirrel v0.1.0-a12, toadStool S158b, nestgate v4.1.0-dev), and all phase2 primals (loamSpine v0.9.5, petalTongue v1.6.6, rhizoCrypt v0.13.0, sweetGrass v0.7.21, skunkBat, sourDough v0.1.0). Identified 18 ecosystem patterns; absorbed all applicable ones.

## Changes

### New Modules in `biomeos-types`

| Module | Source | Purpose |
|--------|--------|---------|
| `ipc.rs` | loamSpine, petalTongue, sweetGrass, primalSpring, healthSpring | `IpcErrorPhase` enum (7 variants), `extract_rpc_result()`, `extract_rpc_error()`, `RpcExtractionError` |
| `or_exit.rs` | groundSpring, loamSpine, ludoSpring | `OrExit<T>` trait for zero-panic startup validation |
| `cast.rs` | airSpring, wetSpring, groundSpring | 9 type-safe numeric cast helpers (`usize_f64`, `f64_usize`, etc.) with `CastError` |
| `validation.rs` | airSpring, rhizoCrypt, ludoSpring | `ValidationSink` trait, `BufferSink`, `StderrSink`, `ValidationFinding`, `ValidationSeverity` |
| `mcp.rs` | healthSpring (23), airSpring (10), wetSpring (8) | `McpToolDefinition`, `McpToolManifest`, `JsonSchema`, `SchemaBuilder` |
| `primal_capabilities.rs` | beardog, toadStool, nestgate, sourDough | `RelayAuthorizeRequest/Response`, `ComputeSubmitRequest/Response`, `ComputeJobStatus`, `ModelRegisterRequest`, `ModelLocateRequest/Response`, `PrimalLifecyclePhase`, `PrimalIdentityResponse`, `PrimalComplianceCheck` |

### Enhanced `primal_names.rs`

- Added `PRIMALSPRING` constant
- Added `display` submodule with 17 mixed-case display names (absorbed from neuralSpring)
- `display::for_id()` lookup function

### Enhanced `capability.list` (biomeos-atomic-deploy)

- Now returns `cost_estimates` per operation (latency hints for Squirrel Pathway Learner)
- Now returns `operation_dependencies` DAG edges (prerequisite operations)
- Added `locality` field ("local" vs "mesh")
- Added `domains` top-level array

### Socket Registry Discovery (biomeos-core)

- New `DiscoveryMethod::SocketRegistry` variant
- `discover_via_socket_registry()` reads `$XDG_RUNTIME_DIR/biomeos/socket-registry.json`
- Inserted between manifest discovery (step 5) and Neural API query (step 7)
- `SocketRegistryEntry` and `SocketRegistry` types in `result.rs`

### Proptest IPC Fuzzing (biomeos-core)

- 8 proptest fuzz tests in `tests/proptest_ipc.rs`
- Covers: arbitrary string parsing, batch dispatch, deep nesting, result/error extraction, large payloads, unicode, null bytes

### deny.toml Expansion

- Expanded from 9 to 15 banned C-dep crates
- Added: `libsqlite3-sys`, `libz-sys`, `bzip2-sys`, `curl-sys`, `libgit2-sys`, `libssh2-sys`
- Aligned with groundSpring/wetSpring/healthSpring 14-crate ban list

### Workspace Dependencies

- Added `temp-env = "0.3"` to workspace dev-dependencies
- Added `proptest = "1"` to biomeos-core dev-dependencies

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --workspace` | PASS |
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (5,268 tests, 0 failures) |

## Test Delta

- 65 new tests (5,203 → 5,268)
- 8 proptest IPC fuzz tests
- 19 cast module tests
- 14 IPC/extraction tests
- 9 MCP tool definition tests
- 8 validation sink tests
- 7 primal capability routing tests

## Patterns Not Absorbed (with rationale)

| Pattern | Why Deferred |
|---------|-------------|
| `Arc<str>` sweep for hot-path strings | `JsonRpcRequest.method` already uses `Arc<str>`; remaining fields are cold-path |
| Provenance trio `pipeline.attribute` wiring | Requires runtime sweetGrass availability; trio deploy config exists |
| `temp_env` migration of existing tests | Added as dep; migration is incremental (`set_test_env` → `temp_env::with_var`) |

## Next Steps

1. Migrate existing `set_test_env` helpers to `temp_env::with_var` (incremental)
2. Wire `extract_rpc_result` into existing ad-hoc `response["result"]` call sites
3. Add MCP tool definitions for biomeOS's own capabilities
4. Implement `biomeos validate primal` using `ValidationSink` + `PrimalComplianceCheck`
5. Wire `PrimalIdentityResponse` into `identity.get` handler
