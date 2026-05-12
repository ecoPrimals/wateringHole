# biomeOS v2.97 — Deep Debt Overstep Cleanup II

**Date**: April 8, 2026
**Scope**: Safety hardening, smart refactors, agnostic naming, dependency cleanup
**Tests**: 7,660+ passing (0 failures), clippy PASS (0 warnings)

---

## Changes

### 1. Safety Hardening — `#![forbid(unsafe_code)]` on all binaries

- **20+ binary entry points** received explicit `#![forbid(unsafe_code)]`:
  neural-api-server, neural-deploy, biomeos-rootfs, init, mkboot, verify-lineage,
  tower, biomeos-deploy, biomeos-verify, device_management_server, gaming-mesh,
  p2p-secure, harvest, all_demos, comprehensive_ecosystem_demo, ecosystem_health,
  integration_test_runner, songbird_universal_ui_demo, test_coverage
- `biomeos/src/main.rs` conditional `cfg_attr(not(test), forbid(...))` → unconditional `#![forbid(unsafe_code)]`
- 6 submodule `#![deny(unsafe_code)]` → `#![forbid(unsafe_code)]` for strict policy enforcement

### 2. Hardcoding → `primal_names` Constants

- `crates/biomeos-atomic-deploy/src/handlers/niche.rs`:
  - 8 template IDs in `json!()` macros (airspring, wetspring, neuralspring, hotspring, groundspring, healthspring, ludospring, petaltongue) → `primal_names::` constants
  - 8 `match template_id` arms → `primal_names::` constants

### 3. Smart Refactors (3 large files)

| File | Before | After | Extracted Modules |
|------|--------|-------|-------------------|
| `genome-deploy/src/lib.rs` | 860 LOC | 35 LOC | `types.rs`, `deployer.rs`, `tests/{mod,types_tests,deployer_tests,helpers}.rs` |
| `primal_orchestrator/orchestrator.rs` | 836 LOC | 36 LOC | `orchestrator_lifecycle.rs`, `orchestrator_health.rs`, `dependency_resolution.rs`, `orchestrator_tests.rs` |
| `neural_router/discovery.rs` | 843 LOC | 94 LOC | `discovery_registry.rs`, `discovery_primal.rs`, `discovery_composite.rs`, `discovery_tests.rs` |

### 4. Dependency Cleanup

- `biomeos-spore` self-referencing dev-dep: added explicit `version = "0.1.0"` to satisfy `cargo deny`
- blake3 `cc` build-dep verified: `pure` feature means no C compilation; `cc` is build-tool only

---

## Files Changed

### Safety hardening (20+ files)
- `crates/biomeos/src/main.rs`
- `crates/biomeos-atomic-deploy/src/neural_api_server/main.rs`
- `crates/biomeos-atomic-deploy/src/neural_deploy/main.rs`
- `crates/biomeos-boot/src/bin/{biomeos-rootfs,init,mkboot}.rs`
- `crates/biomeos-cli/src/bin/main.rs`
- `crates/biomeos-deploy/src/main.rs`
- `crates/biomeos-ui/src/main.rs`
- `bin/chimeras/src/bin/{gaming-mesh,p2p-secure}.rs`
- `tools/harvest/src/main.rs`
- `tools/src/bin/{all_demos,...,test_coverage}.rs`
- 6 submodule files: `protocol_escalation/engine.rs`, `deployment_mode.rs`, etc.

### Hardcoding
- `crates/biomeos-atomic-deploy/src/handlers/niche.rs`

### Smart refactors
- `crates/biomeos-genome-deploy/src/{lib,types,deployer}.rs` + `tests/`
- `crates/biomeos-core/src/primal_orchestrator/{orchestrator,orchestrator_lifecycle,orchestrator_health,dependency_resolution,orchestrator_tests}.rs`
- `crates/biomeos-atomic-deploy/src/neural_router/{discovery,discovery_registry,discovery_primal,discovery_composite,discovery_tests}.rs`

### Dependency
- `crates/biomeos-spore/Cargo.toml`

---

## Verification

```
cargo check --workspace         # PASS
cargo clippy --workspace --all-targets -- -D warnings  # 0 warnings
cargo test --workspace          # 7,660+ tests, 0 failures
```

---

## Builds On

- v2.96: GAP-02 + GAP-09 deploy parser unification and wire method correction
- v2.95: Deep debt overstep cleanup I (safety, agnostic, refactors, dependencies)
