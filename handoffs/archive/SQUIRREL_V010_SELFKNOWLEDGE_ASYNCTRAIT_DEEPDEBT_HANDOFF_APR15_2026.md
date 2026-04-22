<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Primal Self-Knowledge, async-trait Elimination, Deep Debt

**Date**: April 15, 2026
**Previous**: SQUIRREL_V010A52_BIND_GAP_HARDCODING_REFACTOR_HANDOFF_APR14_2026.md

---

## Session Summary

Two-phase session: (V) eliminated all `#[async_trait]` annotations (228→0 across
lifecycle), prepped mito-beacon genetics evolution, upgraded `rand` 0.8→0.9.4;
(W) evolved all hardcoded primal names to capability-based patterns, smart-refactored
5 production files under 800L, matured production stubs to real implementations,
switched `blake3` to pure Rust mode, and cleaned/updated all root documentation.

## Build

| Metric | Value |
|--------|-------|
| Tests | 7,012 passing / 0 failures |
| Coverage | 86.0% line (cargo-llvm-cov; target: 90%) |
| Clippy | CLEAN — `-D warnings`, zero warnings |
| Format | PASS |
| Docs | PASS |
| ecoBin | 3.5 MB, static-pie, stripped, BLAKE3 pure, zero host paths, zero dynamic deps |
| Files | ~1,025 `.rs` files, ~333k lines, max 965 lines (test); max ~798 lines (production) |
| cargo deny | `advisories ok, bans ok, licenses ok, sources ok` |

## Changes

### async-trait Fully Eliminated (228→0 across lifecycle)

All 64 remaining `#[async_trait]` annotations removed across 8 crates. Migration
pattern: dyn-safe traits (`Plugin`, `DynPlugin`, `DynContext*`, `ContextPlugin`,
`ConditionEvaluator`, `ActionExecutor`, `WebPlugin`, `ZeroCopyPlugin`,
`CommandAdapter`, `UniversalServiceRegistry`) use explicit
`Pin<Box<dyn Future<Output = …> + Send + '_>>`. Non-dyn traits use native
`async fn in trait` + `#[expect(async_fn_in_trait)]`. `async-trait` removed from
workspace `[dependencies]` and all crate `Cargo.toml`s. Only remains as transitive
dep from external crates (`config`, `wiremock`, `test-context`).

### Primal Self-Knowledge — Capability-Based Naming

Squirrel no longer knows other primals by name. All references evolved to
capability-based patterns with `#[deprecated(since = "0.2.0")]` aliases:

| Before | After | Scope |
|--------|-------|-------|
| `BearDog*` types/methods | `SecurityProvider*` | auth, errors, JWT, coordinator |
| `BEARDOG_BIOMEOS_SOCKET_STEM` | `SECURITY_CAPABILITY_SOCKET_STEM` | capability_crypto |
| `authenticate_with_beardog` | `authenticate_with_security_provider` | security_coordinator |
| `SongbirdLoadBalancerConfig` | `ServiceMeshLoadBalancerConfig` | core/lib.rs |
| `DEFAULT_SONGBIRD_PORT` | `DEFAULT_DISCOVERY_PORT` | universal-constants |
| `SONGBIRD_ENDPOINT` env | `DISCOVERY_ENDPOINT` (primary) | ai-tools, ecosystem-api |
| `ContextStorage::NestGate` | `ContextStorage::ContentAddressed` | routing/context |
| `DatabaseBackend::NestGate` | `DatabaseBackend::ContentAddressed` | config/database |

Serde aliases maintain backward-compatible deserialization. Env var chains prefer
capability names with primal-name fallbacks.

### Smart Large File Refactoring (5 files)

| File | Before | After | Extracted To |
|------|--------|-------|--------------|
| `workflow_manager.rs` | 831 | 403 | `workflow_types.rs`, `workflow_manager/tests.rs` |
| `server/mod.rs` | 840 | 647 | `server/handlers.rs`, `server/server_types.rs` |
| `mcp/client.rs` | 836 | 605 | `client_listener.rs`, `client_interactive.rs` |
| `ecosystem client.rs` | 824 | 659 | `client_types.rs`, `client_mock.rs` |
| `plugins/manager.rs` | 816 | 706 | `manager_metadata.rs`, `manager_test_plugin.rs` |

Zero production files >800 lines remaining.

### Production Mocks → Real Implementations

- Learning integration: wired to live `ContextManager` data (session count,
  intervention detection via `!state.synchronized`)
- Neural engine: tanh stub → ReLU MLP (`new_mlp`, `forward_scores`, 10→64→6 arch)
- Federation: `dead_code` fields wired to real `find_leader_node` + diagnostics
- All test mocks verified behind `#[cfg(test)]` or `feature = "testing"`

### Dependency Evolution

- `blake3 = { default-features = false, features = ["pure"] }` — no SIMD assembly,
  no C code in default build (aligns with `ECOBIN_ARCHITECTURE_STANDARD` v3.0)
- `rand` 0.8→0.9.4 (RUSTSEC-2026-0097); `ed25519-dalek` compat via `rand::fill`
- `ring`/`reqwest`/`zstd-sys` confirmed absent from default build (only via
  `--all-features` optional paths)

### Three-Tier Genetics Prep

BTSP handshake (`btsp_handshake.rs`) annotated with evolution roadmap for
`mito_beacon_from_env()` adoption when `primalspring >= 0.10.0` ships (currently
0.9.14). `family_seed_ref` → mito-beacon fields; Phase 3 cipher negotiation →
`BTSP_CHACHA20_POLY1305` when BearDog server-side ready.

### Documentation Refresh

Root docs (`README.md`, `CONTEXT.md`, `ORIGIN.md`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `docs/CRYPTO_MIGRATION.md`) updated: test counts, file counts,
coverage alignment (86.0%), blake3 pure feature, 800L production policy, capability
naming context. `CHANGELOG.md` has `[Unreleased]` section for April 15 work.

## Remaining Debt

| Item | Priority | Notes |
|------|----------|-------|
| Coverage 86.0% → 90% | LOW | Gap is IPC/network, binary entry points, demo bins |
| Three-tier genetics (mito-beacon) | BLOCKED | Awaits `primalspring >= 0.10.0` |
| Phase 3 cipher negotiation | BLOCKED | Awaits BearDog `btsp.negotiate` server-side |
| BLAKE3 content curation for NestGate | BLOCKED | Awaits NestGate content-addressed API |
| Remaining primal names in specs/ | LOW | `UNIVERSAL_PATTERNS_SPECIFICATION.md` et al. still use ecosystem names in diagrams |
| `ring` via `jsonwebtoken` (--all-features) | LOW | Replace `jsonwebtoken` with RustCrypto-only JWT or delegate to capability |

## Status

**Health PASS.** Zero `#[async_trait]`. Zero hardcoded primal names in production
code. Zero production files >800L. Zero unsafe. Zero TODO/FIXME. AI provider chain
validated. BTSP Phase 2 complete. 7,012 tests passing. All quality gates green.
