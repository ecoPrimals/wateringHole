# biomeOS v3.39 — Capability-Based Identity Evolution

**Date**: May 2, 2026
**Scope**: Production code hardcoded primal name elimination
**Tests**: 8,076+ passing (0 failures)
**Status**: PRODUCTION READY

---

## What Changed

All production code now references primals by **capability role** instead of by identity.
biomeOS only has self-knowledge and discovers other primals at runtime via Neural API.

### Orchestrator Roles (orchestrator.rs)
- `BEARDOG_SERVER_ROLE` → `SECURITY_PROVIDER_ROLE` ("security-server")
- `SONGBIRD_ORCHESTRATOR_ROLE` → `MESH_ORCHESTRATOR_ROLE` ("mesh-orchestrator")
- `required_primals()` → `required_roles()` returning capability-domain strings
- Node atomic: `"toadstool"` → `"compute-executor"`
- Nest atomic: `"nestgate"` → `"storage-provider"`
- Env vars: `BEARDOG_FAMILY_ID`/`BEARDOG_NODE_ID` → `FAMILY_ID`/`NODE_ID`
- `SONGBIRD_SECURITY_PROVIDER` → `SECURITY_PROVIDER_SOCKET`

### BTSP API (btsp_client.rs, connection.rs)
- `BearDogUnavailable` → `SecurityProviderUnavailable`
- `BearDogNotFound` → `SecurityProviderNotFound`
- All doc comments and log messages reference "security provider"

### CLI/UI (monitor/handlers.rs, device_management_server/mod.rs)
- Dashboard redirect: "visualization primal" + `biomeos discover --capability visualization`
- Connection logs: primal-agnostic ("visualization primal connection established")

### Niche Templates (handlers/niche.rs)
- 12 descriptions evolved: "BearDog + Songbird" → "crypto + mesh orchestration"
- Parameter descriptions: "rhizoCrypt session" → "Provenance session"
- Federation descriptions: "via Songbird discovery" → "via mesh discovery"

### Dead Code Removed
- `ManagedBearDog` / `ManagedSongbird` legacy type aliases deleted
- Re-exports removed from `biomeos-core/src/lib.rs`

---

## Files Modified (20)

| Area | File | Change |
|------|------|--------|
| Orchestrator | `orchestrator.rs` | Role consts + required_roles() |
| Orchestrator | `orchestrator_tests.rs` | Test assertions updated |
| Integration | `tests/integration_tests.rs` | Capability-based assertions |
| BTSP client | `btsp_client.rs` | Variant rename + doc evolution |
| BTSP test | `btsp_client_tests.rs` | Error variant updated |
| Connection | `connection.rs` | Match arm renames + log messages |
| Negotiate | `btsp_negotiate.rs` | Doc comments |
| Listeners | `listeners.rs` | Doc comments |
| Server mod | `neural_api_server/mod.rs` | Doc comments |
| Translation | `translation_loader.rs` | Comment updated |
| Executor | `neural_executor.rs` | Log message |
| Node handlers | `executor/node_handlers.rs` | Comment |
| Graph integrity | `integrity.rs` | Doc comment |
| Graph handlers | `graph/executor/node_handlers.rs` | Doc comments |
| Graph ops | `modes/graph_ops.rs` | Doc + error context |
| CLI monitor | `commands/monitor/handlers.rs` | Dashboard message |
| Device mgmt | `device_management_server/mod.rs` | Connection logs |
| Niche | `handlers/niche.rs` | 12 template descriptions |
| Core lib | `lib.rs` | Remove legacy re-exports |
| Core impls | `primal_impls.rs` | Remove legacy aliases |

---

## Verification

```
cargo check                                    PASS
cargo clippy --workspace --all-targets -- -D warnings  PASS (0 warnings)
cargo fmt --all -- --check                     PASS
cargo test --workspace --lib                   PASS (6,826 lib tests, 0 failures)
```

## Downstream Impact

- **primalSpring**: No breakage — all JSON-RPC wire protocols unchanged
- **All primals**: No breakage — capability domain constants in `primal_names.rs` untouched
- **wateringHole**: Updated registry reflects v3.39 capability-based identity status
