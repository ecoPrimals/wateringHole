<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# biomeOS v2.48 — Cross-Ecosystem Absorption + Capability Registry Evolution

**Date**: March 16, 2026
**Primal**: biomeOS v2.48
**Scope**: Capability registry expansion, graph executor fallback, hardcoding evolution, dependency cleanup
**Supersedes**: BIOMEOS_V247_EDITION2024_DEEP_AUDIT_EXECUTION_HANDOFF_MAR16_2026.md

---

## Summary

Pulled and reviewed all 7 springs (hotSpring v0.6.32, groundSpring V110, neuralSpring V110/S159, wetSpring V124, airSpring v0.8.6, healthSpring V30, ludoSpring V14), all 13 primals (phase1 + phase2), and wateringHole handoffs. Absorbed cross-ecosystem patterns into biomeOS:

1. **5 new capability domains** in the registry (compute.dispatch, secrets, relay, model, hardware)
2. **fallback=skip** support in the Neural API graph executor
3. **Hardcoded primal names → constants** in nucleus identity and discovery
4. **once_cell dependency removed** (LazyLock migration complete)
5. **Leverage guide expanded** with per-spring deep recipes and emergent orchestration patterns

---

## Detailed Changes

### Capability Registry (config/capability_registry.toml)

| New Domain | Provider | Methods | Source |
|-----------|----------|---------|--------|
| `compute.dispatch` | ToadStool | submit, result, capabilities, status, cancel | 5 springs (groundSpring, wetSpring, airSpring, healthSpring, ludoSpring) |
| `secrets` | BearDog | store, retrieve, list, delete | BearDog v0.9.0 |
| `relay` | BearDog | authorize, status | BearDog v0.9.0 |
| `model` | NestGate | register, exists, locate, metadata | NestGate v4.1-dev |
| `hardware` | ToadStool | observe, distill, apply | ToadStool S156 |

Registry: 260+ → 280+ semantic translations, 19 → 24 capability domains.

### Graph Executor Fallback (biomeos-atomic-deploy)

- `GraphNode.fallback: Option<String>` — `"skip"` makes nodes optional
- `GraphNode.is_optional()` — clean helper for fallback checks
- `execute_phase()` — optional node failures logged and skipped; non-optional failures still abort
- `convert_deployment_node()` — carries `fallback` from TOML graph definitions
- Aligns `biomeos-atomic-deploy` with `biomeos-graph` (which already had fallback)

### Hardcoding Evolution (biomeos-nucleus)

- `identity.rs`: `"beardog"` → `primal_names::BEARDOG` (socket path, filename match, error messages)
- `discovery.rs`: `"songbird"`, `"beardog"` → `primal_names::SONGBIRD`, `primal_names::BEARDOG`
- Test fixtures retain string literals as documentation

### Dependency Evolution

- Removed `once_cell` from workspace `Cargo.toml` and `biomeos-core/Cargo.toml`
- No code references remain — `std::sync::LazyLock` replacement complete
- `async-trait` retained: native async traits in Edition 2024 do not yet support `dyn Trait` dynamic dispatch

### Leverage Guide (wateringHole/BIOMEOS_LEVERAGE_GUIDE.md)

Added ~800 lines:

- **Section 7: Per-Spring Deep Leverage Recipes** — Solo, Trio, and Ecosystem Combo patterns for all 7 springs
- **Section 8: Emergent Orchestration Patterns** — Capability Cascading, Spring-as-Provider Mesh, Scientific Method as Graph, Federated Citizen Science, Self-Optimizing Graphs, Cross-Spring Discovery Chains, Capability Versioning, Observation Loop

---

## Audit Results

| Metric | Status |
|--------|--------|
| Files >1000 lines | 0 (largest: 963) |
| Unsafe in production | 0 (test-utils only) |
| Mocks in production | 0 (all `#[cfg(test)]`) |
| Clippy warnings | 0 (pedantic + nursery) |
| Tests | 5,162+ passing, 0 failures |
| Edition | 2024 (all 25 crates) |
| `once_cell` | Removed |

---

## Cross-Ecosystem Patterns Identified

These patterns were independently adopted by 5+ springs and are now documented:

| Pattern | Springs | biomeOS Status |
|---------|---------|---------------|
| `compute.dispatch.*` protocol | groundSpring, wetSpring, airSpring, healthSpring, ludoSpring | Added to registry |
| `OrExit<T>` zero-panic validation | wetSpring, neuralSpring, groundSpring, healthSpring, airSpring | Documented; adoption pending |
| Dual-format capability parsing | groundSpring, neuralSpring, wetSpring, healthSpring, ludoSpring | Format standardization P1 |
| `#[expect(reason)]` lint migration | neuralSpring, groundSpring, wetSpring, ludoSpring | Already adopted |
| `deny.toml` supply-chain hygiene | groundSpring, wetSpring, airSpring, healthSpring, neuralSpring | TODO in deny.toml |

---

## Remaining Evolution Paths

| Priority | Item | Blocked By |
|----------|------|-----------|
| P1 | Typed `CapabilityClient` SDK | neuralSpring, rhizoCrypt waiting |
| P1 | Standardize `capability.list` format (flat vs nested) | Cross-primal coordination |
| P2 | `async-trait` → native async traits | Rust stabilization of dyn async traits |
| P2 | Wire petalTongue SSE event subscription | petalTongue integration |
| P2 | Wire skunkBat Phase 3 | BearDog + Songbird + ToadStool |
| P3 | `bincode` v1 → v2 | tarpc upstream |
| P3 | tarpc upgrade for sweetGrass/NestGate/Songbird (0.34 → 0.37) | Per-primal coordination |

---

## Test Verification

```
cargo check:   PASS (0 errors, 0 warnings)
cargo clippy:  PASS (0 warnings, pedantic + nursery)
cargo test:    5,162+ passed, 0 failed
```

---

**License**: AGPL-3.0-only
