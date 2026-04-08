<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.39 Handoff — async-trait → Native Rust 2024 Migration

**Date**: April 5, 2026
**Scope**: Migrate `#[async_trait]` to native `async fn` in trait (Rust 2024 edition)

## Summary

Progressive migration of `#[async_trait]` annotations to native Rust 2024 `async fn` in trait.
23 annotations removed (228 → 205) across 10 trait definitions and 13 impl blocks in 11 files.

## What Changed

### Tier 1 — Zero Dyn Dispatch (safe drop-in migration)

| Trait | Crate | Impls Migrated |
|-------|-------|---------------|
| `AIProvider` | ecosystem-api | 0 (no impls) |
| `EcosystemIntegration` | ecosystem-api | 1 (`UniversalSquirrelProvider`) |
| `Primal` | universal-patterns | 5 (3 test + 1 test file + 0 external) |
| `GpuInferenceCapability` | universal-patterns | 0 (no impls) |
| `ServiceMeshCapability` | universal-patterns | 0 (no impls) |
| `OrchestrationProvider` | universal-patterns | 2 (`ServiceMeshIntegration` + mock) |
| `TryFlattenStreamExt` | tools/ai-tools | 1 (Pin<Box<dyn Stream>>) |
| `ContextManager` | core/interfaces | 1 (`context/manager/mod.rs`) |
| `MockAdapter` | adapter-pattern-tests | 3 (RegistryAdapter, McpAdapter, PluginAdapter) |

### Tier 2 — Light Dyn (evaluated and partially migrated)

| Trait | Decision | Reason |
|-------|----------|--------|
| `AuthenticationCapability` | **Migrated** | `dyn` only in doc example + 2 test assertions; updated to `&impl`/concrete types |
| `UniversalPrimalProvider` | **Deferred** | Production `Box<dyn UniversalPrimalProvider>` return in `config.rs` — requires generics refactoring |
| `AuthenticationService` | **Deferred** | Production `Arc<dyn AuthenticationService>` in `SecurityMiddleware` — requires generics refactoring |

### Tier 3 — Heavy Dyn (deferred, paired with dyn-to-generics future work)

205 remaining `#[async_trait]` annotations are on traits deeply embedded in `dyn` dispatch
(e.g. `AIClient` 48 dyn, `Plugin` 63 dyn, `Command` 73 dyn). These will be migrated
alongside the progressive `dyn`-to-generics/enum-dispatch refactoring across the ecosystem.

## Lint Strategy

All migrated traits use `#[expect(async_fn_in_trait, reason = "...")]` to suppress
the `async_fn_in_trait` warning. This is safe because:
- All traits are internal (not public API for external consumers)
- All concrete implementors are `Send + Sync`
- The warning is about the compiler not being able to prove `Send` for the
  returned future without seeing all implementations, which is only relevant
  for `dyn Trait` usage

## Dead Import Cleanup

`use async_trait::async_trait` removed from 4 files where no remaining usages exist:
- `ecosystem-api/src/traits/ai.rs`
- `universal-patterns/src/capabilities.rs`
- `universal-patterns/src/orchestration/mod.rs`
- `universal-patterns/src/traits/primal_tests.rs`

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all` | ✓ |
| `cargo clippy -- -D warnings` | ✓ |
| `cargo clippy --all-features --all-targets -- -D warnings` | ✓ |
| `cargo test` | ✓ (all pass) |
| `cargo doc --no-deps` | ✓ |
| `cargo deny check` | ✓ (advisories ok, bans ok, licenses ok, sources ok) |

## Next Steps

1. **Tier 3 migration** — paired with `dyn`-to-generics refactoring for heavy-dyn traits
   (`AIClient`, `Plugin`, `Command`, `ContextTransformation`, etc.)
2. **`async-trait` dependency removal** — once all annotations are gone, remove from workspace
3. **Evaluate enum dispatch** — for traits with bounded variant sets (e.g. `Plugin` subtypes)
