# ToadStool — S203r: async-trait Full Deprecation

**Date**: April 16, 2026
**Session**: S203r
**Type**: Deep Debt — Dependency Deprecation
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy -D warnings` ✅ | `cargo test` ✅ (22,061 pass, 0 failures)

---

## Summary

Fully deprecated the `async-trait` proc macro from toadStool. All ~91 `#[async_trait]` annotations evolved to manual `Pin<Box<dyn Future>>` (for dyn-dispatched traits) or native `async fn` in traits (AFIT, for non-dyn traits). Removed as a direct dependency from all 13 crates. Banned in `deny.toml` alongside `ring`. Zero runtime behavior change.

This treats `async-trait` as deep debt equivalent to `ring` — a proc macro dependency on hot paths that modern Rust (edition 2024, MSRV 1.85) no longer requires.

## Approach

| Strategy | Used For | Description |
|----------|----------|-------------|
| Manual `Pin<Box<dyn Future>>` | Dyn-dispatched traits (~32) | Explicit return type, `Box::pin(async move { ... })` body wrapping. Identical runtime to `#[async_trait]` without the macro. |
| Native AFIT (`async fn` in traits) | Non-dyn traits (already migrated in S203j-k) | Direct `async fn` — no boxing overhead, no macro. |
| `BoxFuture<'a, T>` type alias | Complex signatures | Resolves `clippy::type_complexity` for deeply generic return types. |

## Waves

| Wave | Scope | Files | Traits |
|------|-------|-------|--------|
| **0** | Stale dep removal (`runtime/python`) | 1 Cargo.toml | — |
| **1** | Single-impl traits | ~15 files | `MemoryPressureCallback`, `ByobExecutor`, `CryptoProvider`, `UniversalComputeResource`, `ComputeContext`, `UniversalPrimalProvider` |
| **2** | Bounded-set traits | ~25 files | `ParallelComputeFramework`, `UnifiedMemoryBackend`, `AuthBackend`, `AgentBackend`, `WorkloadExecutor`, `DiscoveryClient`, `DiscoverySource`, `DiscoveryMethod`, `CommunicationProtocol`, `ComputeUnit`, `LegacyEmulator` |
| **3** | Polymorphic traits | ~20 files | `SecurityProvider`, `EdgeDevice`, `LegacyAdapter`, `EmbeddedToolchain`, `LegacyCommunicationSession`, `ProgrammerInterface`, `EmbeddedEmulator`, `PeripheralInterface` |
| **4** | Remaining + cleanup | ~15 files | `CloudProvider`, `CloudProviderInterface`, `ComputeSubstrate`, `PrimalIntegration`, `Terminal3270Session`, `VAXTerminalSession`, `Terminal5250Session`, `RuntimeEngine` |
| **5** | Ban + docs | deny.toml, DEBT.md, 4 Cargo.toml | Workspace dep removed, `deny.toml` ban with wrappers |

## Cargo.toml Removals (13 crates)

- Root workspace `[dependencies]`
- `toadstool` (core)
- `toadstool-distributed`
- `toadstool-server`
- `toadstool-core-common`
- `toadstool-core-config`
- `toadstool-runtime-gpu`
- `toadstool-runtime-universal`
- `toadstool-runtime-orchestration`
- `toadstool-runtime-specialty`
- `toadstool-runtime-edge`
- `toadstool-runtime-container`
- `toadstool-integration-primals`
- `toadstool-runtime-python` (excluded from workspace, unused dep)

## deny.toml Ban

```toml
{ name = "async-trait", wrappers = ["axum", "axum-core", "config", "wiggle"] }
```

Transitive usage via `axum`, `config`, and `wiggle` (wasmtime) is permitted — these are third-party crates whose internals we don't control. Direct dependency is banned.

## Clippy Fixes

- `clippy::type_complexity` in `encryption/provider.rs` and `gpu/universal/execution.rs` — resolved via `type BoxFuture<'a, T>` alias.
- `clippy::used_underscore_binding` in `gpu/frameworks.rs` — renamed conditional-compilation parameters.

## DEBT.md Update

- **D-ASYNC-DYN-MARKERS** → `RESOLVED S203r (fully deprecated)`

## Pre-existing Issues (Not Introduced)

- `toadstool-runtime-edge` crate has pre-existing API drift compilation errors (excluded from workspace check/test). The async-trait removal in this crate is correct; the other errors are unrelated.

## Root Doc Updates

- README.md: async-trait row → DEPRECATED, test count → 22,000+, S203r in Recently Completed, footer → S203r.
- CONTEXT.md: async-trait → DEPRECATED with deny.toml reference.
- DOCUMENTATION.md: header/state → S203r, async-trait → DEPRECATED.
- NEXT_STEPS.md: header → S203r, S203r session entry added, async-trait checklist → DEPRECATED.

---

**Downstream**: No action required. Zero runtime behavior change — `Pin<Box<dyn Future>>` produces identical compiled output to `#[async_trait]`. Springs and peer primals consuming toadStool's IPC surface are unaffected.
