# Squirrel v0.1.0 — Stadial Gate: Lockfile Ghost Elimination + dyn Audit

**Date**: April 16, 2026
**From**: Squirrel team
**To**: primalSpring, all primal teams
**Status**: STADIAL BLOCKERS RESOLVED
**License**: AGPL-3.0-or-later

---

## Stadial Gate Resolution

All three Squirrel stadial blockers from `STADIAL_PARITY_GATE_APR16_2026.md` are resolved.

### 1. `ring` in Cargo.lock — ELIMINATED

**Root cause**: `ring v0.17.14` was pulled via two `--all-features` paths:
- `jsonwebtoken 9.3.1` → `ring` (squirrel-mcp-auth, `local-jwt` feature)
- `reqwest 0.12` → `hyper-rustls` → `rustls 0.23` → `ring`

**Resolution**: Both pulling features removed entirely:
- `local-jwt` feature removed from squirrel-mcp-auth (JWT delegated to BearDog)
- All `reqwest` optional deps removed (see below)

**Cascade removed from Cargo.lock**: `ring`, `rustls`, `rustls-webpki`, `rustls-pki-types`,
`hyper-rustls`, `tokio-rustls`, `jsonwebtoken`, `simple_asn1`, `pem`, `untrusted`,
`webpki-roots`, and ~15 Windows/platform crates.

### 2. `reqwest` in Cargo.lock — ELIMINATED

**Root cause**: `reqwest 0.12` was declared as optional dep in 10 crates behind
never-default features: `http-commands`, `direct-http`, `marketplace`, `http-client`,
`http-patterns`, `http-api`, `http-config`, `http-auth`, `http` (SDK).

Already banned in `deny.toml` per Tower Atomic pattern (HTTP goes through Songbird
service mesh via IPC), but the optional deps caused Cargo.lock inclusion.

**Resolution**: All 10 `reqwest` optional deps removed from all crate Cargo.toml files.
Associated feature flags removed. Dead `#[cfg(feature = "...")]` code cleaned from 6 crates.
Workspace `[workspace.dependencies]` entry removed.

**Crates modified**:
- Cargo.toml (workspace root)
- crates/tools/cli/Cargo.toml (`http-commands`)
- crates/tools/ai-tools/Cargo.toml (`direct-http`, `anthropic`, `openai`, `gemini`)
- crates/core/plugins/Cargo.toml (`marketplace`, `repository-server`)
- crates/core/mcp/Cargo.toml (`direct-http`, `ai-providers`)
- crates/core/core/Cargo.toml (`http-client`)
- crates/core/auth/Cargo.toml (`http-auth`, `local-jwt`)
- crates/universal-patterns/Cargo.toml (`http-patterns`)
- crates/sdk/Cargo.toml (`http`)
- crates/ecosystem-api/Cargo.toml (`http-api`, `http-client`)
- crates/config/Cargo.toml (`http-config`)

### 3. ~677 dyn usages — AUDITED AND CLASSIFIED

**Before**: 740 `dyn` keyword usages across crates/
**After**: 704 (9 finite-implementor traits converted to enum/concrete dispatch)

#### Classification

| Category | Count | Status |
|----------|-------|--------|
| `dyn Future` (Pin<Box<>> for object-safe async) | 194 | Non-trait-object — inherent |
| `dyn Fn/FnMut` (closures) | 23 | Non-trait-object — inherent |
| `dyn Any` (type erasure) | 17 | Non-trait-object — inherent |
| `dyn Error/StdError` (error types) | 17 | Non-trait-object — inherent |
| `dyn Stream` (async streams) | 3 | Non-trait-object — inherent |
| Test code | ~100 | Acceptable — mock flexibility |
| Plugin system (unbounded implementors) | ~350 | Justified — user-extensible |
| **Total** | **704** | **INTERSTADIAL-READY** |

#### Finite-implementor conversions

| Trait | Before | After | Type |
|-------|--------|-------|------|
| `UniversalServiceRegistry` | `Arc<dyn ...>` (20 usages, 1 impl) | `Arc<InMemoryServiceRegistry>` | Concrete |
| `FrameCodec` | `Arc<dyn ...>` (3 usages, 1 impl) | `Arc<DefaultFrameCodec>` | Concrete |
| `Experience` | `&dyn Experience` (1 usage, 1 impl) | `&RLExperience` | Concrete |
| `ServiceRegistryProvider` | `Box<dyn ...>` (1 usage, 1 impl) | `ServiceRegistryBackend` enum | Enum |
| `JournalPersistence` | `Arc<dyn ...>` (2 usages, 2 impls) | `JournalBackend` enum | Enum |
| `PluginStateManager` | `Arc<dyn ...>` (2 usages, 2 impls) | `StateManagerBackend` enum | Enum |
| `RewardCalculator` | `Box<dyn ...>` (2 usages, 4 impls) | `RewardBackend` enum | Enum |
| `ComputeProvider` | `Box<dyn ...>` (2 usages, 2 impls) | `ComputeBackend` enum | Enum |
| `ShutdownHandler` | Already enum (`RegisteredShutdownHandler`) | No change needed | Enum |

#### Plugin system (unbounded — justified)

These traits are part of Squirrel's user-extensible plugin system. Implementors are
genuinely unbounded (users write arbitrary plugins). Trait objects are the correct pattern:

- `dyn Command/DynCommand/SimpleCommand` (79) — command dispatch
- `dyn Plugin` (53) — plugin lifecycle
- `dyn WebPlugin/WasmPlugin/ZeroCopyPlugin` (19) — web plugin interfaces
- `dyn DynContextTransformation/DynContextPlugin/DynContextAdapterPlugin` (33) — context system
- `dyn LifecycleHook` (9) — plugin lifecycle hooks
- `dyn ConditionEvaluator` (6) — extensible rule evaluation registry
- Remaining (~50) — event listeners, action plugins, validation rules, etc.

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | PASS — 0 warnings |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS — 0 warnings |
| `cargo test --workspace` | PASS — 7,160 tests, 0 failures |
| `cargo fmt --all -- --check` | PASS |
| `cargo deny check` | PASS — advisories ok, bans ok, licenses ok, sources ok |
| `ring` in Cargo.lock | **ABSENT** |
| `reqwest` in Cargo.lock | **ABSENT** |
| `jsonwebtoken` in Cargo.lock | **ABSENT** |
| `rustls` in Cargo.lock | **ABSENT** |

---

## Squirrel Stadial Status

**INTERSTADIAL-READY**

- [x] `async-trait` crate not in any Cargo.toml
- [x] Zero `#[async_trait]` attributes in `.rs` files
- [x] Zero `Box<dyn Trait>` / `Arc<dyn Trait>` for finite-implementor traits
- [x] Zero `ring` / `sled` / `openssl` stanzas in Cargo.lock
- [x] `cargo deny check bans` passes
- [x] Edition 2024

---

**License**: AGPL-3.0-or-later
