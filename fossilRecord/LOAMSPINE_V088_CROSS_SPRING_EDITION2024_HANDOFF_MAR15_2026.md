<!-- SPDX-License-Identifier: AGPL-3.0-only -->

# LoamSpine v0.8.8 — Cross-Spring Absorption & Edition 2024 Handoff

**Date**: March 15, 2026  
**From**: v0.8.7 → v0.8.8  
**Status**: All quality gates green

---

## What Changed

### Edition 2024 Migration
- Workspace `edition = "2024"` (from 2021). Requires Rust 1.85+.
- 19 `collapsible_if` patterns auto-modernized to let-chains.
- `env::set_var`/`remove_var` wrapped in `unsafe` blocks in 7 test files (178 call sites).
- `env_set!`/`env_rm!` macros reduce verbosity in `infant_discovery/tests.rs` (1017 → 860 lines).
- `unsafe_code` lint: `forbid` → `deny` (allows `#[allow(unsafe_code)]` in test modules; production still protected).

### JSON-RPC 2.0 Batch Support
- `process_request` handles batch arrays per spec: empty batch → parse error, notifications suppress responses, mixed batches processed.
- Aligns with sweetGrass v0.7.11 batch implementation.

### Proptest Roundtrip Invariants
- 7 property-based tests for core newtypes: `Did`, `SpineId`, `ContentHash`, `Signature`, `ByteBuffer`.
- `proptest` v1.10 added as dev dependency.

### Named Resilience Constants
- `CIRCUIT_FAILURE_THRESHOLD`, `CIRCUIT_RECOVERY_TIMEOUT_SECS`, `CIRCUIT_SUCCESS_THRESHOLD`.
- `RETRY_BASE_DELAY_MS`, `RETRY_MAX_DELAY_MS`, `RETRY_MAX_ATTEMPTS`.
- `{DOMAIN}_{METRIC}_{QUALIFIER}` naming convention (aligns with groundSpring/wetSpring).

### Enriched `capability.list`
- Response includes `version`, `methods` array with `method`/`domain`/`cost`/`deps` per operation.
- 23 methods documented with dependency graphs and cost tiers.

### Platform-Agnostic Paths
- Hardcoded `/tmp/biomeos/` → `std::env::temp_dir().join("biomeos")` in socket resolution fallback.
- Aligns with groundSpring/wetSpring/airSpring `temp_dir()` convention.

### Cleanup
- Stale `showcase/IMPLEMENTATION_STATUS.md` deleted (contradicted showcase index).
- Showcase index: fixed broken `ROOT_DOCS_INDEX.md` link, bumped version, aligned references.
- Dockerfile: `rust:1.83` → `rust:1.85` for edition 2024.
- CI: MSRV `1.75.0` → `1.85.0`.

---

## Quality Metrics

| Metric | v0.8.7 | v0.8.8 |
|--------|--------|--------|
| Tests | 1,114 | 1,123 |
| Coverage | 89.64% / 91.71% | 89.64% / 91.71% |
| Edition | 2021 | 2024 |
| Clippy | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe (prod) | 0 | 0 |
| Max file | 955 | 955 |
| Source files | 117 | 112 |

---

## Cross-Spring Patterns Absorbed

| Pattern | From | Applied |
|---------|------|---------|
| Edition 2024 | airSpring v0.2.12 | Full migration, let-chains |
| JSON-RPC batching | sweetGrass v0.7.11 | `process_request` batch handling |
| Proptest roundtrips | groundSpring v0.5.10 | 7 property-based tests |
| Named tolerance constants | groundSpring/wetSpring | `{DOMAIN}_{METRIC}_{QUALIFIER}` |
| `temp_dir()` paths | groundSpring/airSpring | Socket fallback paths |
| Enriched capability.list | ludoSpring convention | deps/cost per method |

---

## Still Available for v0.9.0

- Typed tarpc client wrapper (`LoamSpineClient`) — from wetSpring pattern.
- `niche.rs` self-knowledge module — from neuralSpring pattern.
- 3-tier socket discovery (XDG → /run/user/{uid} → temp_dir) — partial, missing /run/user tier.
- Runtime attestation enforcement (types ready, wiring needed).
- 90%+ line coverage (89.64% currently; main.rs gap).

---

## Files Modified (Key)

- `Cargo.toml` — edition 2024, version 0.8.8
- `crates/loam-spine-api/src/jsonrpc/mod.rs` — batch support
- `crates/loam-spine-core/src/types.rs` — proptest module
- `crates/loam-spine-core/src/resilience.rs` — named constants
- `crates/loam-spine-core/src/neural_api.rs` — enriched capability.list, temp_dir paths
- `crates/loam-spine-core/src/constants/network.rs` — temp_dir paths
- 7 test files — edition 2024 unsafe wrapping
- 11 production files — collapsible_if → let-chains
- Root docs, CI, Dockerfile, showcase — version/edition updates
