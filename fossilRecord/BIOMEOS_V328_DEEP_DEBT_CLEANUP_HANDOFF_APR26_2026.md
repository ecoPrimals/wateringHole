# biomeOS v3.28 — Deep Debt Cleanup Handoff

**Date**: April 26, 2026
**From**: biomeOS team
**To**: All ecosystem teams (primalSpring, ludoSpring, petalTongue, etc.)

## Summary

v3.28 is a systematic deep debt cleanup pass across the biomeOS codebase. No new features — purely improving constants centralisation, idiomatic Rust patterns, real system queries, and runtime efficiency.

## Changes

### 1. Centralised `DEFAULT_FAMILY_ID` constant

`biomeos_types::defaults::DEFAULT_FAMILY_ID` (`"default"`) replaces ~20 scattered string literals across 16 production files. Downstream primals that import `biomeos-types` can use this constant instead of hardcoding `"default"`.

**Affected crates**: biomeos-core, biomeos-primal-sdk, biomeos-spore, biomeos-cli, biomeos-ui, biomeos-atomic-deploy, biomeos-graph, biomeos-types.

### 2. Primal name constants in tools

`tools/harvest` and `tools/ecosystem_health` now use `primal_names::*` constants instead of raw string literals. The harvest roster is synced with the full canonical set.

### 3. thiserror migration (4 types)

| Type | Crate | Before | After |
|------|-------|--------|-------|
| `NeuralError` | neural-api-client-sync | manual Display+Error | `#[derive(thiserror::Error)]` |
| `BtspHandshakeError` | biomeos-core | manual Display+Error | `#[derive(thiserror::Error)]` |
| `CastError` | biomeos-types | manual Display+Error | `#[derive(thiserror::Error)]` |
| `EnrollmentValidationError` | biomeos (enroll) | manual Display+Error | `#[derive(thiserror::Error)]` |

Error message strings are preserved exactly — no breaking changes to error formatting.

### 4. Real system queries in ecosystem_health

- **Sovereignty check**: live socket discovery + UDS connect probe (was canned output)
- **Resource monitoring**: `/proc/meminfo`, `/proc/loadavg`, `df`, `/proc/net/route` (was hardcoded "2.1GB / 16GB", "15%")

### 5. GraphExecutor Arc optimisation

`execute()` builds `HashMap<String, Arc<GraphNode>>` once. Phase workers share `Arc` references instead of deep-copying `GraphNode` per spawn. Lookup is O(1) HashMap vs linear Vec scan. Relevant to springs using `graph.execute` with large graphs.

### 6. Event system refactor (biomeos-api)

`detect_and_emit_changes` split into 5 focused subfunctions. Per-event string clones eliminated. `#[expect(clippy::too_many_lines)]` removed. No change to `EcosystemEvent` types or SSE/WebSocket wire format.

### 7. Path constant deduplication

- `neural-api-client-sync` local `LINUX_RUNTIME_DIR_PREFIX` → import from `biomeos_types`
- `continuous.rs` raw `"/tmp"` → `DEFAULT_SOCKET_DIR`

### 8. rtnetlink dependency documented

`rtnetlink` confirmed active in `biomeos-deploy/src/network.rs` (Linux bridge lifecycle). Documented as accepted thin FFI for kernel AF_NETLINK. Reorganised in workspace Cargo.toml under "OS interfaces".

## Verification

- `cargo check --workspace`: 0 errors
- `cargo clippy --workspace -- -D warnings`: 0 warnings
- `cargo fmt --check`: clean
- All test failures are pre-existing (environment-dependent discovery tests)

## Impact on downstream

- **No breaking API changes** — all changes are internal
- **Error message strings preserved** — downstream string-matching (if any) is unaffected
- `DEFAULT_FAMILY_ID` is available for downstream use if desired
- GraphExecutor performance improvement is transparent to callers
