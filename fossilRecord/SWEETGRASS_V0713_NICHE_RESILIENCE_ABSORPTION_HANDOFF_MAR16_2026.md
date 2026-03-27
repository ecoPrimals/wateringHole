# SweetGrass v0.7.13 — Niche Architecture & Resilience Absorption

**Date**: March 16, 2026
**Version**: v0.7.12 → v0.7.13
**Theme**: Cross-spring absorption, niche self-knowledge, resilience patterns

## Summary

SweetGrass absorbs ecosystem patterns from springs (airSpring, groundSpring, wetSpring, ludoSpring, neuralSpring), phase1 primals (beardog, squirrel, songbird), and phase2 primals (biomeOS, loamSpine, rhizoCrypt) to achieve full niche compliance, resilient IPC, and DI-based testability.

## Changes

### 1. Niche Self-Knowledge Module (`sweet_grass_core::niche`)
- 21 CAPABILITIES, 8 CONSUMED_CAPABILITIES, 4 DEPENDENCIES
- `operation_dependencies()` — per-method depends_on + cost metadata
- `cost_estimates()` — domain-level cost tiers for biomeOS scheduling
- `semantic_mappings()` — 17 intent → method mappings for Neural API
- Follows groundSpring V106 / airSpring V082 / ludoSpring V18 pattern

### 2. Centralized Primal Names (`sweet_grass_core::primal_names`)
- `names::RHIZOCRYPT`, `LOAMSPINE`, `BEARDOG`, `NESTGATE`, `SONGBIRD`, `TOADSTOOL`, `SQUIRREL`, `BIOMEOS`
- `env_vars::RHIZOCRYPT_SOCKET`, `BIOMEOS_SOCKET_DIR`, `XDG_RUNTIME_DIR`, etc.
- Follows groundSpring V106 / wetSpring V119 pattern

### 3. biomeOS Integration Files
- `config/capability_registry.toml` — 21 methods across 8 domains
- `graphs/sweetgrass_deploy.toml` — BYOB deploy graph with dependency ordering
- Follows rhizoCrypt V013 / neuralSpring V105 pattern

### 4. UniBin Completion
- `sweetgrass capabilities` — offline capability dump
- `sweetgrass socket` — print resolved socket path
- Follows loamSpine V088 / rhizoCrypt V013 pattern

### 5. DI Socket Resolution
- `SocketConfig` struct + `resolve_socket_path_with(config)` — no env var mutation
- 9 new DI-based tests (no `#[serial]`, no `unsafe`)
- Follows airSpring V082 / biomeOS V239 pattern

### 6. Resilience Module (`sweet_grass_integration::resilience`)
- `CircuitBreaker` — lock-free via atomics, configurable threshold + cooldown
- `RetryPolicy` — base-2 exponential backoff with max delay cap
- `with_resilience()` — async helper combining circuit breaker + retry
- Follows loamSpine `ResilientAdapter` pattern

### 7. Error Enum Hardening
- `#[non_exhaustive]` on ALL 10 error enums across workspace
- New `ServiceError::Transport` and `ServiceError::Discovery` IPC variants
- Follows groundSpring V106 / wetSpring V119 pattern

### 8. Capability List Evolution
- `capability.list` now delegates to `niche.rs` (single source of truth)
- Response includes `consumed_capabilities` and `cost_estimates`
- UDS module uses `primal_names::env_vars` constants

## Metrics

| Metric | v0.7.12 | v0.7.13 |
|--------|---------|---------|
| Tests | 903 | 941 |
| Clippy warnings | 0 | 0 |
| New modules | — | niche, primal_names, resilience |
| Error enums with #[non_exhaustive] | 2 | 10 |
| UniBin subcommands | 2 | 4 |
| biomeOS config files | 0 | 2 |

## Spring Absorption Sources

| Pattern | Source | Status |
|---------|--------|--------|
| niche.rs self-knowledge | airSpring, groundSpring, ludoSpring, neuralSpring | ✅ Done |
| primal_names.rs | groundSpring V106, wetSpring V119 | ✅ Done |
| capability_registry.toml | rhizoCrypt V013, biomeOS V240 | ✅ Done |
| Deploy graph | rhizoCrypt, neuralSpring, airSpring | ✅ Done |
| DI socket resolution | airSpring V082, biomeOS V239 | ✅ Done |
| Circuit breaker + retry | loamSpine V088 | ✅ Done |
| #[non_exhaustive] errors | groundSpring, wetSpring, airSpring | ✅ Done |
| UniBin subcommands | loamSpine, rhizoCrypt | ✅ Done |

## Remaining Opportunities

- `temp_env` crate for simpler env var tests (squirrel pattern)
- Songbird mesh registration + heartbeat
- Tolerance hierarchy with citations (airSpring pattern)
- tarpc endpoint registration for biomeOS tarpc-first routing
