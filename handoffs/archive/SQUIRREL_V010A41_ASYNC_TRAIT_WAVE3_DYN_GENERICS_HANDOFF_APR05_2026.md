<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.41 — async-trait Wave 3: Deep dyn→Generics

**Date**: April 5, 2026
**Commit**: fe78777f (squirrel)
**Previous**: alpha.40 (17f2e70f — wave 2: 26 zero-dyn + 5 dyn→generics)

## Summary

Third wave of async-trait migration. Reduced `#[async_trait]` annotations from
168 → 129 (39 removed) by converting `dyn` dispatch to generics/enum dispatch
across 15+ traits in all tiers, touching 65 files (629 insertions, 981 deletions).

## Migrations by Tier

### Tier A (1-3 dyn usages) — All Migrated

| Trait | Strategy | Files |
|-------|----------|-------|
| `NetworkConnection` (×3 defs) | **Consolidated** 3 → 1 canonical def; `FederationNetwork<C>` / `FederationNetworkManager<C>` | federation/ |
| `EncryptionKeyManager` | `DefaultSovereignDataManager<E, A>` generic | sovereign_data.rs |
| `AccessControlManager` | Same as above | sovereign_data.rs |
| `PlatformExecutor` | `RegisteredPlatformExecutor` enum dispatch | universal_executor.rs |
| `CommandsPlugin` | Native async + concrete `CommandRegistryPluginAdapter` | plugins.rs, factory.rs |
| `MessageHandler` | Native async, renamed router marker to `RouterHandlerSlot` | protocol/types.rs |
| `AiCapability` | `BridgeAdapter<C>` generic, RPITIT for Send futures | bridge.rs, universal.rs |
| `KeyStorage` | `SecurityManagerImpl<K = InMemoryKeyStorage>` generic | key_storage.rs, manager.rs |
| `AuthenticationService` | `SecurityMiddleware<A>` generic | services.rs, middleware.rs |
| `ServiceMeshClient` | `HealthMonitor<C>` / `ServiceDiscovery<C>` generic | mesh.rs, client.rs |

### Tier B (4-6 dyn) — 4 Migrated, 2 Deferred

| Trait | Strategy | Status |
|-------|----------|--------|
| `PluginRegistry` | `WebPluginRegistry<R>` / `PluginManagementInterface<R>` generic | **Done** |
| `SessionManager` | `SquirrelPrimalProvider<S = SessionManagerImpl>` generic | **Done** |
| `MCPInterface` | `AIRouter<M = NoMcpInterface>` / `McpAiToolsAdapter<M>` generic | **Done** |
| `ContextAdapter` | RPITIT + `ContextAdapterDyn` blanket for dyn wrapper | **Done** |
| `ConditionEvaluator` | HashMap registry of heterogeneous evaluators | **Deferred** |
| `ZeroCopyPlugin` | Dynamic plugin loading + batch Vec | **Deferred** |

### Tier C (7-10 dyn) — 1 Migrated, 3 Deferred

| Trait | Strategy | Status |
|-------|----------|--------|
| `ServiceMeshClient` | Generic structs (see Tier A) | **Done** |
| `MonitoringProvider` | `Vec<Arc<dyn>>` multi-provider | **Deferred** |
| `PrimalProvider` | `HashMap<String, Arc<dyn>>` registry | **Deferred** |
| `WebPlugin` | `Vec<Arc<dyn>>` plugin collection | **Deferred** |

## Dependency Hygiene

`async-trait` removed from production dependencies:
- `squirrel-mcp` (Cargo.toml)
- `squirrel-mcp-auth` (Cargo.toml)
- `squirrel-commands` (Cargo.toml)
- Stale `use async_trait::async_trait` removed from `core/auth/src/providers.rs`

## Remaining async-trait (129 annotations)

Traits requiring `#[async_trait]` for dyn-compatibility:
- `Plugin` (~65 dyn), `Command` (~73 dyn), `AIClient` (~54 dyn)
- `ContextPlugin` (~14 dyn), `ContextAdapterPlugin` (~12 dyn)
- `AiProviderAdapter` (~23 dyn), `UniversalServiceRegistry` (~26 dyn)
- `ServiceDiscovery` (~17 dyn), `MonitoringProvider` (7), `PrimalProvider` (7)
- `WebPlugin` (10), `ConditionEvaluator` (4), `ZeroCopyPlugin` (6)
- `ActionPlugin` (2), `ActionExecutor` (2), `RepositoryProvider` (2)

These are all legitimate `dyn` uses in heterogeneous collections or plugin registries.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all` | ✓ |
| `cargo clippy -- -D warnings` | ✓ |
| `cargo clippy --all-features --all-targets -- -D warnings` | ✓ |
| `cargo test` | ✓ |
| `cargo doc --no-deps` | ✓ |
| `cargo deny check` | ✓ |

## Next Steps

1. **Enum dispatch for closed plugin sets** — Where the set of implementations is
   known and small (e.g., `MonitoringProvider` has only `MonitoringServiceProvider`
   in production), convert to enum dispatch
2. **`AIClient` generics** — Major refactor: `AIRouter` dispatches across multiple
   vendor clients; requires generic provider registry or enum of all vendors
3. **`Plugin` system redesign** — The core `Plugin` trait is the largest dyn surface
   (65 uses); may benefit from a typed plugin registry pattern
4. **Continue removing `async-trait` from `Cargo.toml`** as more traits migrate
