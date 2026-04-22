# ToadStool S203s — Stadial Parity Gate Cleared

**Date**: April 16, 2026
**Session**: S203s
**Primal**: toadStool
**Gate**: Stadial Parity Gate (primalSpring `STADIAL_PARITY_GATE_APR16_2026.md`)

## Summary

Cleared the stadial parity gate by eliminating all finite-implementor `Box<dyn Trait>` /
`Arc<dyn Trait>` dispatch via **enum dispatch + RPITIT** (Return Position `impl Trait` in
Traits). This was the single largest remaining stadial blocker in the ecosystem.

## What Changed

### Traits converted to RPITIT + enum dispatch (~32 traits)

**Wave 1 — Core toadstool (10 traits):**
AuthBackend, AgentBackend, StorageBackend, CompatibilityLayer, MemoryPressureCallback,
ByobExecutor, CloudProvider (generic), CryptoProvider (generic), ResourceMonitor,
UniversalPrimalProvider

**Wave 2 — Server + distributed (3 traits):**
WorkloadExecutor, SecurityProvider, CloudProviderInterface (generic)

**Wave 3 — Specialty runtime (5 traits + 3 macro-generated):**
LegacyAdapter (9 impls), LegacyEmulator, EmbeddedToolchain, EmbeddedEmulator,
ProgrammerInterface

**Wave 4 — GPU + universal runtime (5 traits):**
ParallelComputeFramework, UnifiedMemoryBackend, UniversalComputeResource, ComputeContext,
ComputeUnit

**Wave 5 — Cross-crate discovery (2 traits):**
DiscoveryClient (enum in `core/config`), DiscoverySource (enum in `core/common`)

**Wave 6 — RuntimeEngine cross-crate (1 trait, 7 runtime crates):**
RuntimeEngine genericized: `EngineRegistry<E>`, `UniversalScheduler<P, E>`,
`UniversalPlatform<E>`, `RuntimeOrchestrator<E>`. `RuntimeEngineDispatch` enum in
`server` crate (composition root). Test mocks use generics directly.

**Wave 7 — Misc (5+ traits):**
HardwareTransport, AsyncStream, KernelOptimizer (concrete), LoadBalancer (concrete),
MetricsCollector, NpuBackend, ComputeSubstrate (generic), terminal session stubs,
PeripheralInterface stubs

### Pin<Box<dyn Future>> cascade

~864 `Pin<Box<dyn Future>>` usages cascaded away when traits moved to RPITIT.
Remaining (justified): infant discovery plugin traits (dyn required for object safety),
PrimalIntegration (unbounded external primals), mockall macro limitation.

## Gate Criteria Status

| Criterion | Status |
|-----------|--------|
| Zero `#[async_trait]` attributes | **PASS** (0) — since S203r |
| Zero `async-trait` dep in Cargo.toml | **PASS** (0) — since S203r |
| Zero finite-implementor `dyn Trait` objects | **PASS** (0) — S203s |
| Zero lockfile ghosts | **PASS** — no ring, no sled |
| Edition 2024 | **PASS** |
| `cargo deny check bans` | **PASS** |
| `cargo clippy -- -D warnings` | **PASS** |

## Remaining dyn (justified unbounded)

| Trait | Count | Justification |
|-------|-------|---------------|
| EndpointSource | 10 | Infant discovery plugin registry |
| SubstrateDetector | 6 | Infant discovery plugin registry |
| PrimalIntegration | 5 | External primal integration |
| MessageHandler | 2 | User-defined protocol handlers |
| Generator<T> | 1 | Generic testing utility |
| RandomNumberGenerator | 1 | Testing utility |

## Verification

- `cargo check --workspace --exclude toadstool-runtime-edge`: **PASS**
- `cargo clippy --workspace --exclude toadstool-runtime-edge -- -D warnings`: **PASS**
- `cargo deny check bans`: **PASS**
- `cargo test` key packages: **5,211 tests, 0 failures**
- `cargo fmt --all --check`: **0 diffs**

## Architecture Notes

- Traits with only test-mock impls use **generics** (not enums): `CloudProviderRegistry<P>`,
  `EncryptionContext<P>`, `CloudProviderInterface` orchestrator
- Traits with production impls use **dispatch enums**: match delegation, `#[cfg(test)]`
  variants for test doubles
- Cross-crate traits use **generic core + concrete server**: e.g. `EngineRegistry<E>` in
  core, `RuntimeEngineDispatch` enum in server crate
- Infant discovery plugin traits keep `Pin<Box<dyn Future>>` — RPITIT is not object-safe
  and these registries accept unbounded external sources

## Files Changed

~80+ files across ~30 crates. Key files:
- `crates/core/toadstool/src/execution/mod.rs` — RuntimeEngine RPITIT
- `crates/server/src/runtime_engine_dispatch.rs` — composition root enum
- `crates/core/toadstool/src/biomeos_integration/auth_backend.rs` — AuthBackendDispatch
- `crates/distributed/src/security_provider/dispatch.rs` — SecurityProviderDispatch
- `crates/runtime/specialty/src/types/dispatch.rs` — LegacyAdapterDispatch
- `crates/runtime/gpu/src/parallel_framework_dispatch.rs` — GPU dispatch
- `crates/runtime/universal/src/types/compute_unit_dispatch.rs` — ComputeUnitDispatch
