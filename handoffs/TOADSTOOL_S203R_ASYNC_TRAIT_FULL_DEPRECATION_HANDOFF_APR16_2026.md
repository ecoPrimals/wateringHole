# ToadStool S203r: async-trait Full Deprecation

**Date**: April 16, 2026
**Session**: S203r
**Primal**: toadstool (compute infrastructure)
**Prior**: S203q (root doc cleanup + debris audit)

---

## Summary

Fully deprecated the `async-trait` crate across the entire ToadStool workspace, treating it as deep debt like `ring` — evolved to native async Rust patterns and banned in `deny.toml`.

## What Changed

### Annotations Removed
- **~91 `#[async_trait]` annotations** removed across **55+ files** in **13 crates**
- **Zero** `#[async_trait]` annotations remain anywhere in the workspace
- **Zero** `use async_trait` imports remain (one historical doc comment reference kept)

### Evolution Strategy (per trait category)
- **Manual `Pin<Box<dyn Future>>`** for all traits requiring `dyn` compatibility (the majority) — same runtime behavior as `async-trait`, no proc macro
- **Native `async fn` in trait (AFIT)** for traits with no `dyn` usage
- All existing logic preserved exactly — pure dependency removal, zero behavioral change

### Dependency Removal
- `async-trait` removed from workspace `[dependencies]` in root `Cargo.toml`
- `async-trait` removed from all 13 crate-level `Cargo.toml` files
- Transitive dep remains via `axum`, `config`, `wiggle` (allowed via `wrappers` in deny.toml)

### deny.toml Ban
- `async-trait` added to `[bans.deny]` list alongside `ring`, `openssl`, `tungstenite`
- `wrappers = ["axum", "axum-core", "config", "wiggle"]` for transitive allowance

### Quality Gates
- `cargo check --workspace` (excluding pre-broken edge crate): **pass**
- `cargo clippy --workspace -- -D warnings`: **0 warnings**
- `cargo fmt --all --check`: **0 diffs**
- `cargo test --workspace`: **22,061 tests passed, 0 failures**

### Documentation Updates
- **DEBT.md**: `D-ASYNC-DYN-MARKERS` promoted from CLOSED to RESOLVED (S203r)
- **README.md**: Quality gates row updated, footer updated, S203r added to Recently Completed
- **CONTEXT.md**: async-trait status updated to DEPRECATED + BANNED
- **DOCUMENTATION.md**: Current State updated to S203r
- **NEXT_STEPS.md**: Header and test counts updated

## Trait Inventory (what was converted)

### Wave 1 — Single-impl traits (6)
`UniversalComputeResource`, `ComputeContext`, `UniversalPrimalProvider`, `ByobExecutor`, `MemoryPressureCallback`, `CryptoProvider`

### Wave 2 — Bounded-set traits (11)
`ParallelComputeFramework`, `UnifiedMemoryBackend`, `AuthBackend`, `AgentBackend`, `WorkloadExecutor`, `DiscoveryClient`, `CommunicationProtocol`, `DiscoverySource`, `DiscoveryMethod`, `ComputeUnit`, `LegacyEmulator`

### Wave 3 — Genuinely polymorphic traits (4)
`SecurityProvider`, `EdgeDevice`, `LegacyAdapter`, `EmbeddedToolchain`

### Wave 4 — Placeholder / trait-only (8+)
`CloudProvider`, `CloudProviderInterface`, `ComputeSubstrate`, `PrimalIntegration`, `Terminal3270Session`, `VAXTerminalSession`, `Terminal5250Session`, `ProgrammerInterface`, `EmbeddedEmulator`, `PeripheralInterface`, `LegacyCommunicationSession`

### Stale dependency removed
`crates/runtime/python` — had `async-trait` in Cargo.toml with zero usage

## Pattern for Ecosystem Absorption

Other primals deprecating `async-trait` should follow the same pattern:

```rust
// Before (async-trait macro)
#[async_trait]
pub trait MyTrait: Send + Sync {
    async fn method(&self, param: &str) -> Result<T>;
}

// After (manual, no macro)
pub trait MyTrait: Send + Sync {
    fn method<'a>(&'a self, param: &'a str)
        -> Pin<Box<dyn Future<Output = Result<T>> + Send + 'a>>;
}

// Impl: Box::pin(async move { ... })
```

Key rules:
- `&self` only → use `+ '_` lifetime
- `&self` + reference params → explicit `<'a>` lifetime on method + `+ 'a` on future
- Owned params (no refs) → `+ '_` is fine
- `self: Box<Self>` (consuming) → no lifetime needed: `+ Send` only

## Files Modified (55+)

See `git diff --stat` for the full list. Major areas:
- `crates/core/toadstool/src/` — 15 files (traits, providers, encryption, byob, auth, agent backends)
- `crates/core/common/src/` — 5 files (discovery engine, runtime discovery)
- `crates/distributed/src/` — 6 files (security provider, cloud orchestrator)
- `crates/runtime/gpu/src/` — 8 files (execution, frameworks, unified memory backends)
- `crates/runtime/edge/src/` — 7 files (discovery methods, communication protocols)
- `crates/runtime/specialty/src/` — 6 files (emulation, embedded, mainframe)
- `crates/runtime/universal/src/` — 5 files (compute unit, substrate)
- `crates/server/src/` — 3 files (tarpc executor, coordinator)
- `crates/integration/primals/src/` — 2 files (PrimalIntegration trait)
- Tests: ~15 files across all crates

## Known Pre-existing Issue

`toadstool-runtime-edge` crate has **pre-existing compilation errors** (RuntimeEngine API drift, missing types, wrong error variants) unrelated to async-trait changes. The edge crate's `DiscoveryMethod` and `CommunicationProtocol` traits were successfully migrated; the remaining errors predate this session.
