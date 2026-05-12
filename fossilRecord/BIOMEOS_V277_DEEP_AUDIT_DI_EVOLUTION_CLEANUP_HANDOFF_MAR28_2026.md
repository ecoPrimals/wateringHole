# biomeOS v2.77 — Deep Audit + DI Evolution + Cleanup

**Date**: March 28, 2026
**Version**: v2.77
**Tests**: 7,209 passing, 0 failures, 0 Clippy warnings

## Summary

Comprehensive audit and cleanup session addressing flaky test infrastructure, commented-out legacy code, stale configuration, and hardcoded primal references. No new features — pure codebase quality and reliability improvement.

## Changes

### 1. CapabilityRegistry Dependency Injection

**Problem**: 10 socket-based tests in `capability_registry_tests2.rs` mutated `XDG_RUNTIME_DIR` via `TestEnvGuard::set()`, causing race conditions when tests ran in parallel (sporadic `No such file or directory` on socket connect).

**Fix**: Added `CapabilityRegistry::with_socket_path(family_id, socket_path)` constructor. All 10 tests now inject an explicit temp-dir socket path directly — no env-var mutation, no `#[serial_test::serial]` needed, fully parallel-safe.

**Files**:
- `crates/biomeos-core/src/capability_registry.rs` — new `with_socket_path()` constructor
- `crates/biomeos-core/src/capability_registry_tests2.rs` — all 10 socket tests rewritten with `make_registry()` helper

### 2. Commented-Out Legacy Code Removal

Removed `/* Legacy code commented out: ... */` blocks that referenced a defunct `ClientRegistry` / ToadStool integration pattern. Git history preserves the intent; production code no longer carries dead narrative.

**Files**:
- `crates/biomeos-core/src/universal_biomeos_manager/ai.rs` — removed ~75 lines (`enable_ai_optimization`)
- `crates/biomeos-core/src/universal_biomeos_manager/runtime.rs` — removed ~30 lines (ToadStool resource metrics)
- `crates/biomeos-core/src/universal_biomeos_manager/service.rs` — removed ~15 lines (ToadStool replica count)

### 3. Infallible Error Handling

`biomeos-federation` `Capability::from_str` and `from_tags` methods evolved from `.expect("Capability::FromStr is infallible")` to `match never {}` exhaustive pattern on `Infallible`.

**File**: `crates/biomeos-federation/src/capability.rs`

### 4. Hardcoded Primal Name Constants

String literals replaced with `biomeos_types::primal_names::*` constants:
- `crates/biomeos-api/src/handlers/trust.rs` — `"beardog"` → `primal_names::BEARDOG`
- `crates/biomeos-federation/src/subfederation/beardog.rs` — `"beardog"` → `primal_names::BEARDOG`
- `crates/biomeos-atomic-deploy/src/executor/primal_spawner.rs` — `"squirrel"` → `primal_names::SQUIRREL`
- `crates/biomeos-atomic-deploy/src/orchestrator.rs` — role-based constants + `primal_names::*`

### 5. Cargo.toml Hygiene

- Stale `exclude = ["validation"]` (non-existent directory) → `exclude = ["tools", "tools/harvest"]` (actual standalone workspaces)

### 6. Documentation Updates

- `deployments/basement-hpc/README.md`: hardcoded `/path/to/home/Development/...` → `$BIOMEOS_REPO`
- `README.md`, `CURRENT_STATUS.md`, `CONTEXT.md`, `CHANGELOG.md`: version bump v2.76 → v2.77, test count 7,202 → 7,209
- New doc-tests on core types (`identifiers.rs`, `error/core.rs`, `paths.rs`, `config/mod.rs`, `transport.rs`, `atomic_client.rs`, `capability.rs`)

## Audit Findings (Confirmed Clean)

- **Zero** `#[allow]` in production code (all `#[expect]` with reasons)
- **Zero** `unsafe` in production (test-only env helpers)
- **Zero** `todo!()` / `panic!()` / `unimplemented!()` in production
- **Zero** TODO / FIXME / HACK markers in production
- **Zero** mock implementations in production (all `#[cfg(test)]`)
- **Zero** `.unwrap()` in production runtime paths
- **Zero** files >1000 LOC in production
- **Zero** C dependencies
- **Zero** commented-out code blocks (cleaned this session)

## Remaining Work (biomeOS)

| Area | Status | Notes |
|------|--------|-------|
| Songbird mesh state split | Blocked | 3 independent MeshHandler instances need shared Arc |
| Songbird UDP discovery | Blocked | Ephemeral port bug |
| biomeOS on gate2 | Ready | Cross-gate graphs validated, need deployment |
| Pixel biomeOS | Ready | ARM64 binary built, need ADB deployment |

## Cross-Primal Notes

- `capability.call` routing now uses `primal_names::*` constants end-to-end (biomeOS, federation, atomic-deploy)
- `CapabilityRegistry::with_socket_path()` is available for any test that needs a registry without env-var mutation
- All 7,209 tests run fully parallel with 0 failures — flaky test infrastructure is eliminated
