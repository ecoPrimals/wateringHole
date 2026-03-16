# LoamSpine v0.8.9 — Self-Knowledge, temp-env, Deploy Graph Handoff

**Date**: March 15, 2026  
**Version**: 0.8.9  
**Previous**: v0.8.8 (Cross-Spring / Edition 2024)

---

## Summary

LoamSpine v0.8.9 absorbs ecosystem patterns from cross-spring analysis:
- **`primal_names.rs`** centralized identifier constants (groundSpring convention)
- **`niche.rs`** self-knowledge module (capabilities, deps, costs, semantic mappings)
- **`temp-env`** migration for thread-safe env var testing
- **5-tier socket discovery** with `/run/user/{uid}/biomeos/` tier
- **Deploy graph TOML** for biomeOS deployment orchestration

---

## Changes

### New Modules
- `crates/loam-spine-core/src/primal_names.rs` — Single source of truth for IPC identifiers
- `crates/loam-spine-core/src/niche.rs` — Primal self-knowledge (23 methods, 8 domains, 6 consumed capabilities, 4 optional deps, 21 cost estimates)
- `graphs/loamspine_deploy.toml` — 5-phase biomeOS deployment graph

### Production Code
- `neural_api.rs`: `PRIMAL_NAME` delegates to `primal_names::SELF_ID`; socket resolution uses `primal_names::BIOMEOS_SOCKET_DIR`
- `constants/network.rs`: `resolve_socket_base_dir()` adds `/run/user/{uid}/biomeos/` tier via `/proc/self/status` (Linux only, graceful fallback)
- `neural_api.rs`: `resolve_socket_path()` same 5-tier treatment

### Test Infrastructure
- `constants/network.rs`: 26 tests migrated from `unsafe` env mutations to `temp_env::with_vars`
- `neural_api.rs`: 12 sync tests migrated to `temp_env::with_vars`; 2 async tests consolidated
- New: 6 `niche.rs` invariant tests, 3 `primal_names.rs` tests
- Eliminated `cleanup_env_vars()` / `cleanup_neural_env()` helper functions
- Net: 38 `unsafe` blocks removed from test code

### Dependencies
- Added `temp-env = "0.3.6"` to `loam-spine-core` dev-dependencies

---

## Quality Metrics

| Metric | v0.8.8 | v0.8.9 |
|--------|--------|--------|
| Tests | 1,123 | 1,132 |
| Coverage | 89.64% | 89.64% |
| Source files | 112 | 114 |
| Clippy | 0 | 0 |
| Unsafe (prod) | 0 | 0 |
| Unsafe (test) | ~50 blocks | ~12 blocks |
| Max file | 955 | 955 |

---

## Cross-Spring Patterns Absorbed

| Pattern | Source | Status |
|---------|--------|--------|
| `primal_names.rs` | groundSpring, wetSpring | ✅ Adopted |
| `niche.rs` self-knowledge | groundSpring | ✅ Adopted |
| `temp-env` crate | airSpring, healthSpring | ✅ Adopted |
| 5-tier socket discovery | wateringHole standard | ✅ Adopted |
| Deploy graph TOML | groundSpring | ✅ Adopted |

---

## Files Changed
- `Cargo.toml` (version bump)
- `crates/loam-spine-core/Cargo.toml` (temp-env dep)
- `crates/loam-spine-core/src/lib.rs` (module declarations)
- `crates/loam-spine-core/src/primal_names.rs` (new)
- `crates/loam-spine-core/src/niche.rs` (new)
- `crates/loam-spine-core/src/neural_api.rs` (primal_names delegation + temp-env)
- `crates/loam-spine-core/src/constants/network.rs` (5-tier + temp-env)
- `graphs/loamspine_deploy.toml` (new)
- `README.md`, `CHANGELOG.md`, `STATUS.md`, `WHATS_NEXT.md`
- `CONTRIBUTING.md`, `KNOWN_ISSUES.md`, `primal-capabilities.toml`
- `showcase/00_SHOWCASE_INDEX.md`

---

*Next: v0.9.0 — 90%+ coverage, runtime attestation wiring, typed IPC errors*
