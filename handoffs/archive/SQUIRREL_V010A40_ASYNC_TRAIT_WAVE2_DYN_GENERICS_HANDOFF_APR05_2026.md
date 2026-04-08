<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.40 Handoff — async-trait Wave 2 + dyn→generics Evolution

**Date**: April 5, 2026
**Scope**: Deep async-trait migration wave 2, dyn-to-generics evolution, dependency hygiene

## Summary

Second wave of `#[async_trait]` removal: 37+ annotations removed (205 → 168) across 56 files.
26 zero-dyn traits migrated to native async; 5 low-dyn traits converted from `dyn` dispatch
to generics and enum dispatch — the first concrete steps in the long-term `dyn` elimination.

## Wave 2 — Zero Dyn Migrations (26 traits)

| Crate | Traits Migrated |
|-------|-----------------|
| core/core | `PrimalCoordinator`, `McpRouter`, `SwarmManager`, `ServiceMeshLoadBalancerIntegration`, `EnhancedMcpRouter` |
| core/mcp | `Transport` (+ SimpleTransport, WebSocketTransport, MockTransport) |
| core/plugins | `AppPlugin`, `CliPlugin`, `PluginLoader`, `PluginDiscovery`, `PluginDistribution`, `MonitoringPlugin`, `WebPluginExt`, `TestUtilsPlugin`, `ToolPlugin`, `PluginManagerTrait`, `LegacyWebPluginTrait` |
| universal-patterns/federation | `FederationNetwork`, `ConsensusManager`, `SovereignDataManager`, `CrossPlatformExecutor`, `UniversalExecutor` |
| universal-patterns/security | `ZeroCopySecurityProvider` |
| main/monitoring | `MetricsExporter` |
| main/tests/chaos | `ChaosScenario` |
| tools/rule-system | `FileWatcher` |

## dyn→Generics Evolution (5 traits)

| Trait | Pattern | Before | After |
|-------|---------|--------|-------|
| `MetricsExporter` | Enum dispatch | `Box<dyn MetricsExporter>` | `MetricsExporterHandle` enum (Prometheus, JSON) |
| `ShutdownHandler` | Enum dispatch | `Arc<dyn ShutdownHandler>` | `RegisteredShutdownHandler` enum |
| `IpcHttpDelegate` | Generics | `Arc<dyn IpcHttpDelegate>` | `IpcRoutedVendorClient<D: IpcHttpDelegate>` |
| `SecurityProvider` family | Enum dispatch | `Arc<dyn UniversalSecurityService>` | `UniversalSecurityProviderBox` enum |
| `ComputeProvider` | Enum dispatch | `Box<dyn ComputeProvider>` | `ComputeProviderImpl` enum |
| `ServiceRegistryProvider` | Concrete type | `Box<dyn ServiceRegistryProvider>` | `Box<UnavailableServiceRegistry>` |

## Dependency Hygiene

`async-trait` moved from `[dependencies]` → `[dev-dependencies]` for:
- `squirrel-context-adapter` (only used in test mocks)
- `squirrel-integration` (only used in test mocks)

## Remaining (168 annotations)

The 168 remaining `#[async_trait]` annotations are on Tier 3 traits with deep `dyn` dispatch:
- `AIClient` (~54 dyn), `Plugin` (~63 dyn), `Command` (~73 dyn)
- `AiProviderAdapter` (~23 dyn), `UniversalServiceRegistry` (~26 dyn)
- Various plugin subtypes in `core/plugins`

These will be progressively removed as `dyn` dispatch is replaced with generics/enum dispatch.

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all` | ✓ |
| `cargo clippy -- -D warnings` | ✓ |
| `cargo clippy --all-features --all-targets -- -D warnings` | ✓ |
| `cargo doc --no-deps` | ✓ |
| `cargo deny check` | ✓ (advisories ok, bans ok, licenses ok, sources ok) |

## Next Steps

1. Tier 3 `dyn`-to-generics for `AIClient`, `Plugin`, `Command` (high-impact, large refactors)
2. Continue `NetworkConnection` deduplication (3 copies of the same trait in federation modules)
3. Remove orphan test files (`providers_tests.rs`, `traits_tests.rs`) that are not wired into crate modules
