# biomeOS v3.00 — Deep Debt Cleanup IV: Dependency Evolution, Native Async Traits, Doc Ground Truth

**Date**: April 9, 2026
**Scope**: Dependency cleanup, async-trait migration, hardcoding evolution, orphan deletion, license harmonization, root doc ground truth
**Tests**: 7,724 passing (0 failures) | **Clippy**: 0 warnings | **fmt**: PASS | **doc**: PASS

---

## Dependency Cleanup

| Crate | Dependency Removed | Reason |
|-------|-------------------|--------|
| `biomeos-core` | `itertools` | Unused in source; resolved 0.10/0.12 version duplication (0.10 remains as transitive dev-dep from criterion) |
| `biomeos-niche` | `async-trait` | Zero `#[async_trait]` usage in source |
| `biomeos-chimera` | `async-trait` | Zero `#[async_trait]` usage in source |
| `biomeos-test-utils` | `async-trait` | Zero `#[async_trait]` usage in source |

## Async Trait Migration (Edition 2024)

| Trait | File | Change |
|-------|------|--------|
| `BiomeOSStandardAPI` | `biomeos-types/src/primal/standard_api.rs` | `#[async_trait]` → native `async fn in trait` + `#[expect(async_fn_in_trait)]` |
| `UniversalPrimalService` | `biomeos-types/src/primal/service.rs` | `#[async_trait]` → native `async fn in trait` + `#[expect(async_fn_in_trait)]` |

Both traits had zero `dyn Trait` usage — callers use generic bounds only, making `async-trait` unnecessary overhead. The remaining `async-trait` usages in 4 other crates are retained where `dyn Trait` dispatch is needed.

## Hardcoding Evolution

| File | Before | After |
|------|--------|-------|
| `biomeos-atomic-deploy/src/handlers/topology.rs` `get_socket_directories()` | Hardcoded `/tmp/biomeos-{USER}` + bare `/tmp` fallback | `fallback_runtime_dir()` + `FALLBACK_RUNTIME_BASE` from `biomeos_types::constants::runtime_paths` |

## Orphan Code Deletion

| File | LOC | Reason |
|------|-----|--------|
| `biomeos-graph/src/nucleus_executor.rs` | 288 | Not referenced from `lib.rs`, never compiled, imported nonexistent types (`NucleusConfig`, `NucleusState`, `NucleusExecutionError`) |

## License Harmonization

| File | Before | After |
|------|--------|-------|
| `LICENSE-ORC` Notice block | `AGPL-3.0-only` | `AGPL-3.0-or-later` |
| `CURRENT_STATUS.md` Standards Compliance | `AGPL-3.0-only License` | `scyBorg Triple-Copyleft: AGPL-3.0-or-later + ORC + CC-BY-SA 4.0` |
| `docs/SPRING_NICHE_DEPLOYMENT_GUIDE.md` | `AGPL-3.0-only` in prerequisites | `AGPL-3.0-or-later` |

All license references now consistently use `AGPL-3.0-or-later`, matching `LICENSE`, all `Cargo.toml` files, and all 692 SPDX headers.

## Root Doc Ground Truth

All root documents updated to reflect v3.00 state:

| Document | Updates |
|----------|---------|
| `README.md` | Version 2.99→3.00, date Apr 8→Apr 9, tests 7,695→7,724 |
| `CURRENT_STATUS.md` | Version, date, test count, license compliance table |
| `START_HERE.md` | Version, date, test count in header and footer |
| `QUICK_START.md` | Version, date, test count in footer |
| `DOCUMENTATION.md` | Date, test count, handoff section (added April 2026 handoffs v2.90–v3.00) |
| `CONTEXT.md` | Test count |
| `CHANGELOG.md` | New v3.00 entry |
| `specs/README.md` | Last Updated April 1→April 9 |
| `specs/NEURAL_API_ROUTING_SPECIFICATION.md` | Removed broken links to `GRAPH_BASED_ORCHESTRATION_SPEC.md` and `BIOMEOS_AS_PRIMAL_SPECIALIZATION.md` (files don't exist), status "Active Development"→"Implemented" |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | 7,724 passed, 0 failed |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |
| Unsafe code | 0 production (`#[forbid(unsafe_code)]` all roots + binaries) |
| TODO/FIXME/HACK | 0 |
| Files >1000 LOC | 0 |
| Production mocks | 0 |

## What Remains

- Zero blocking debt
- Zero open gaps (GAP-MATRIX-01 resolved in v2.99)
- Ecosystem blocker: BTSP Phase 2 rollout (BearDog enforcing, other primals need wiring — Songbird → NestGate → ToadStool priority)
- plasmidBin harvest: all x86_64 binaries stale (pre-April 8); musl-static rebuild needed

---

**biomeOS**: v3.00 | **Tests**: 7,724 | **Clippy**: PASS | **License**: scyBorg (AGPL-3.0-or-later + ORC + CC-BY-SA 4.0)
