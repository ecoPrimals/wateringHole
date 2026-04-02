# biomeOS v2.74 — Deep Debt Evolution: Config-Driven Capabilities Handoff

**Date**: March 28, 2026
**Version**: v2.72 → v2.74 (3 commits: v2.72 ARM64, v2.73 cross-gate, v2.74 deep debt)
**Tests**: 7,192 passing (0 failures)
**Clippy**: 0 warnings (pedantic + nursery)

---

## Summary

This handoff covers three evolution sessions building on the primalSpring
composition foundation. v2.72 closed the ARM64 gap, v2.73 implemented
cross-gate deployment orchestration, and v2.74 executed deep debt resolution
targeting hardcoded patterns, large file maintainability, and config-driven
capability resolution.

---

## ARM64 Cross-Compilation (v2.72)

| Component | Detail |
|-----------|--------|
| Target | `aarch64-unknown-linux-musl` static binary |
| Binary size | 9.6 MB stripped |
| Fix | `relocation-model=static` (same approach as NestGate) |
| `.cargo/config.toml` | Created with `aarch64` + `x86_64` musl profiles |
| Deployed to | `livespore-usb/aarch64/primals/biomeos`, `pixel8a-deploy/primals/biomeos` |

## Cross-Gate Deployment Evolution (v2.73)

### `route.register` Batch API

New JSON-RPC method for batch capability registration:

```json
{"method": "route.register", "params": {
  "primal": "beardog", "transport": "tcp://192.0.2.100:9001",
  "capabilities": ["crypto.sign", "crypto.verify"], "gate": "pixel"
}}
```

Registers all capabilities for a remote primal in one call instead of
individual `capability.register` calls per capability.

### Graph-Driven Cross-Gate Deployment

| Component | Change |
|-----------|--------|
| `GraphNode.gate` | New `Option<String>` field on both graph schemas |
| `Graph.env` | New `HashMap<String, String>` from `[graph.env]` TOML section |
| `GateRegistry` | New module: gate name → `TransportEndpoint` mapping |
| `GraphExecutor` | Checks `node.gate` → resolves via `GateRegistry` → forwards via `AtomicClient` |
| `forward_to_remote_gate` | Wraps node as `graph.execute` JSON-RPC to remote biomeOS |

## Deep Debt Evolution (v2.74)

### Lint Hygiene

- `#![allow(clippy::doc_markdown)]` → `#[expect(clippy::doc_markdown, reason = "...")]` in biomeos-ui
- Zero `#[allow]` remaining in production code (all migrated to `#[expect]` with reasons)

### Dependency Cleanup

- Removed unused `mockall` from workspace `[dependencies]` and `biomeos-core` `[dev-dependencies]`
- No `.rs` file in the codebase references `mockall` or `automock`

### Hardcoding → Convention-Based

**Before** (orchestrator.rs + primal_launcher.rs):
```rust
let socket_env = match primal_name {
    "beardog-server" => "BEARDOG_SOCKET",
    "songbird-orchestrator" => "SONGBIRD_SOCKET",
    "toadstool" => "TOADSTOOL_SOCKET",
    "nestgate" => "NESTGATE_SOCKET",
    _ => return Err(anyhow!("Unknown primal: {primal_name}")),
};
```

**After** (biomeos-types shared utility):
```rust
pub fn socket_env_key(primal_name: &str) -> String {
    let base = primal_name
        .strip_suffix("-server")
        .or_else(|| primal_name.strip_suffix("-orchestrator"))
        .unwrap_or(primal_name);
    format!("{}_SOCKET", base.to_uppercase().replace('-', "_"))
}
```

New primals work automatically — no match table maintenance.

### Smart Refactoring

`neural_executor.rs`: **957 → 533 lines**

Extracted to `neural_executor_node_impls.rs` (418 lines):
- `node_verification` — ecosystem socket verification
- `node_health_check_all` — socket directory health scan
- `node_rpc_call` — circuit-breaker-protected JSON-RPC calls
- `node_capability_call` — dual-strategy capability routing
- `send_jsonrpc_async` — Unix socket JSON-RPC helper

Main file retains: executor loop, phase execution, topological sort, cross-gate
forwarding, env substitution.

### Config-Driven Capability Resolution

**Before**: Hardcoded `CAPABILITY_DOMAINS` const table in `capability_domains.rs`
required recompilation when domain mappings changed.

**After**: New `CapabilityRegistry` struct:
1. Loads `[domains.*]` sections from `config/capability_registry.toml` at runtime
2. Falls back to compiled-in `CAPABILITY_DOMAINS` const for zero-config environments
3. Wired into `GraphExecutor` via `with_capability_registry()` builder method
4. Graph handler automatically loads from config when executing graphs

### Stale Reference Cleanup

- Updated `docs/handoffs/` → `wateringHole/handoffs/` in `nucleus.rs`, `EVOLUTION_ROADMAP.md`, `MESH_IPC_METHODS_SPEC.md`
- CHANGELOG `docs/handoffs/` references preserved as fossil record

---

## Files Changed (v2.72 → v2.74)

| File | Change |
|------|--------|
| `.cargo/config.toml` | New: ARM64 + x86_64 musl cross-compilation profiles |
| `Cargo.toml` | Removed `mockall` from workspace deps |
| `crates/biomeos-core/Cargo.toml` | Removed `mockall` from dev-deps |
| `crates/biomeos-ui/src/lib.rs` | `#![allow]` → `#[expect]` with reason |
| `crates/biomeos-types/src/defaults.rs` | New `socket_env_key()` convention utility |
| `crates/biomeos-atomic-deploy/src/orchestrator.rs` | Hardcoded match → `socket_env_key()` |
| `crates/biomeos-atomic-deploy/src/primal_launcher.rs` | Hardcoded match → `socket_env_key()` |
| `crates/biomeos-atomic-deploy/src/neural_executor.rs` | 957 → 533 lines (node impls extracted) |
| `crates/biomeos-atomic-deploy/src/neural_executor_node_impls.rs` | New: 418-line node handler module |
| `crates/biomeos-atomic-deploy/src/capability_domains.rs` | New `CapabilityRegistry` + TOML loader |
| `crates/biomeos-atomic-deploy/src/gate_registry.rs` | New: gate name → endpoint registry |
| `crates/biomeos-atomic-deploy/src/handlers/graph.rs` | Wired `CapabilityRegistry` + graph env merge |
| `crates/biomeos-atomic-deploy/src/handlers/capability.rs` | New `register_route()` batch method |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` | `BatchRouteRegister` variant + dispatch |
| `crates/biomeos-atomic-deploy/src/neural_graph.rs` | `gate` field + `env` map + TOML parsing |
| `crates/biomeos-graph/src/node.rs` | `gate: Option<String>` field |

---

## Test Delta

| Version | Tests | Delta |
|---------|-------|-------|
| v2.71 | 7,167 | — |
| v2.73 | 7,186 | +19 (cross-gate, route.register, graph parsing) |
| v2.74 | 7,192 | +6 (CapabilityRegistry: TOML, fallback, wildcard, override, real config) |

---

## Remaining Evolution Targets

1. **biomeOS on gate2** — deploy to EPYC 9274F for two-biomeOS federation validation (operational, not code)
2. **engine.rs** (917 lines) — socket discovery engine, candidate for smart refactor
3. **`#[deprecated]` API cleanup** — `capability_from_primal_name` in primal-sdk, named accessors in biomeos-ui
4. **bincode v1 advisory** — tied to tarpc/tokio-serde; tracked in `deny.toml` as RUSTSEC-2025-0141
