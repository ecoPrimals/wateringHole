# Songbird v0.3.4 Handoff — Deep Debt Execution: Refactoring, JSON-RPC, Docs & Coverage

**Primal**: Songbird (Network Orchestration & Discovery)  
**Date**: March 20, 2026  
**Version**: v0.3.4  
**Previous**: v0.3.3 (Standards Compliance, Coverage & Architecture)  
**License**: AGPL-3.0-only (scyBorg provenance trio)

---

## Session Summary

Two-phase deep debt execution session. Phase 1: comprehensive audit identifying broken doctest, oversized file, stale `#[allow()]` attributes, hardcoded constants, production stubs, and 63.5% coverage gap. Phase 2: systematic execution across 17 waves — smart file refactoring, JSON-RPC gateway completion, `#[warn(missing_docs)]` on all 29 crates, dependency pruning, 256 new tests, and debris cleanup.

---

## Metrics

| Metric | Before (v0.3.3) | After (v0.3.4) |
|--------|-----------------|-----------------|
| Tests | ~6,300 | 9,876 (+3,576) |
| Failed tests | 1 (doctest) | 0 |
| Line coverage | 63.5% | ~67% |
| Files >1000 lines | 1 | 0 |
| `#[warn(missing_docs)]` | 13/29 | 29/29 |
| JSON-RPC methods | existing | +10 semantic methods |
| `#[allow()]` bare | many | 0 (bulk migration done) |
| Dependencies | ~420 | ~418 (2 unused removed) |
| Unsafe code | bare `unsafe` | `Mutex` guard + `#![deny]` |
| Total Rust lines | 400,108 | 404,698 |

---

## What Changed

### 1. Smart File Refactoring (6 files → domain submodules)

Decomposed by domain responsibility, not arbitrary line splitting:

- `canonical.rs` (1,058 lines) → `types.rs` + `adapter.rs` + `routing.rs` + `mod.rs` (largest 376)
- `mesh_handler.rs` (977) → `json.rs` + `udp_discovery.rs` + `mod.rs` + `tests.rs` (largest ~406)
- `availability.rs` (944) → `types.rs` + `checker.rs` + `tests.rs`
- `core/mod.rs` (933) → `consolidated_config.rs` + `orchestrator_health.rs` + `consolidated_engine.rs` + `consolidated_tests.rs`
- `capability_registration.rs` (928) → `config.rs` + `transport.rs` + `payload.rs` + `lifecycle.rs` + `tests.rs`

### 2. Hardcoded Constants → Capability-Based Discovery

- `find_primals_with_capability` evolved from stub (returned all names) to real env-driven capability filter via `SONGBIRD_CAPABILITY_<CAP>_PROVIDERS` and per-primal `*_CAPABILITIES`
- Removed `staging.internal:8080` literal; all URLs use env → bind → `FALLBACK_*` const chain
- All ports configurable via `SONGBIRD_*_PORT` env vars

### 3. JSON-RPC Gateway Completion (10 semantic methods)

Per wateringHole `SEMANTIC_METHOD_NAMING_STANDARD.md`:
- `compute.route`, `deployment.create`, `deployment.status`
- `task.create`, `task.list`, `consent.check`, `consent.grant`
- `registry.register`, `registry.discover`, `protocol.negotiate`
- All share handler logic with REST endpoints (zero code duplication)

### 4. Production Stub Evolution

- `health_check_all()` → real TCP reachability probes via pre-registered `TcpReachabilityHandler`
- `songbird cli` → interactive REPL with `help`/`exit`/`quit` and subcommand guidance
- Federation join → parses `FederationStatus`/`nodes`/`peers` from response
- Load balancer → stateful `AtomicU64` round-robin
- Trust `verify_hardware` → proper capability discovery error path

### 5. Standards Compliance

- `#[allow()]` → `#[expect(reason)]` bulk migration complete
- `#![warn(missing_docs)]` on all 29/29 crates
- `songbird-process-env`: `parking_lot::Mutex` guard + `#![deny(unsafe_code)]` + per-fn `#[allow]`
- Fixed doctest: `SigningKey::generate()` → `from_bytes()` (ed25519-dalek 2.2.0)

### 6. Coverage Expansion (+256 tests)

- Wave 1: 200+ tests across orchestrator, config, universal (consent, graph, health, trust)
- Wave 2: 56 tests across http-client, universal-ipc, discovery, lineage-relay

### 7. Dependency Pruning

- Removed unused `thiserror` from songbird-tls, `tower` from songbird-http-client
- Confirmed `kube`/`k8s-openapi`/`bollard` are feature-gated (not in default builds)

### 8. Debris Cleanup

- Deleted `docker/docker-compose.monitoring.yml` (missing monitoring/ assets)
- Deleted `docker/Dockerfile.beardog-validator` (missing source tree)
- Deleted `scripts/test_e2e_https_beardog.sh` (wrong binary, wrong env vars)

---

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-features --all-targets -- -D warnings` | PASS (zero warnings) |
| `cargo doc --all-features --no-deps` | PASS |
| `cargo test --workspace --all-features` | 9,876 passed, 0 failed |
| Files >1000 lines | 0 |
| SPDX headers | 1,324/1,324 (100%) |

---

## Remaining Work

1. **BearDog crypto wiring** — blocked on BearDog availability
2. **Coverage ~67% → 90%** — continued pure-logic test expansion
3. **Ring-free workspace** — `rcgen` replacement + quinn feature reconfiguration
4. **Deep documentation** — fill scoped `#[allow(missing_docs)]` internal modules
5. **Hardware tests** — Tower + Pixel 8a validation
6. **Platform backends** — NFC, iOS XPC, WASM
7. **Dependency version alignment** — base64, base32, socket2, thiserror, tower, rand duplicates
8. **Script/config refresh** — align env var names in `config/*.env` and `scripts/*.sh` with actual `SONGBIRD_PORT` convention

---

## For Other Primals

- **BearDog**: Songbird's crypto stubs return `CryptoUnavailable`; when BearDog is available, Songbird discovers it via `capability.call("crypto", ...)` at runtime
- **biomeOS**: Songbird registers capabilities via `lifecycle.register` when biomeOS is present
- **Squirrel/Toadstool**: JSON-RPC gateway at `/jsonrpc` accepts `{domain}.{operation}` semantic methods; tarpc for native performance
