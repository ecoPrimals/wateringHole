<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Creative content: CC-BY-SA 4.0 (scyBorg provenance trio) -->

# BearDog v0.9.0 — Wave 12: Cross-Ecosystem Audit, Lint Tightening & Type Safety Evolution

**Date**: March 23, 2026
**Version**: 0.9.0
**Edition**: 2024 | **MSRV**: 1.93.0

---

## Summary

Full cross-ecosystem audit of all wateringHole standards, 8 springs (primalSpring, neuralSpring, airSpring, wetSpring, hotSpring, healthSpring, groundSpring, ludoSpring), and all phase1/phase2 primals. Identified absorption opportunities and executed on compliance gaps, lint tightening, type safety evolution, file refactoring, and documentation alignment.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 14,161 | **14,201** |
| Coverage | 87.0% | 87.0%+ (40+ new tests; re-measure with llvm-cov) |
| Clippy warnings | 0 (but `unwrap_used` allowed) | **0** (`unwrap_used`/`expect_used` = warn) |
| SPDX coverage | 1,997/2,026 | **2,026/2,026 (100%)** |
| Commented-out code | ~10 files | **0** |
| `Box<dyn Error>` in public APIs | 3 files | **0** |
| Files near 1000 LOC | 4 files (970-990) | Split into **14** focused files |
| `#[allow(dead_code)]` in prod | Multiple | Evolved (fields wired to traces) |

---

## Changes

### Lint Tightening (absorption from biomeOS pattern)
- `unwrap_used`/`expect_used` evolved from `allow` → `warn` at workspace level in root `Cargo.toml`
- All 6 production `expect()` sites annotated with `#[expect(clippy::expect_used, reason = "...")]`
- `process_env.rs` (4 sites): mutex poisoning is unrecoverable
- `mdns.rs` Default impl: cannot return Result
- `key_lineage.rs`: evolved `expect` to `unwrap_or` (infallible `split`)
- Unused `AsyncReadExt` import removed from `unix_socket_ipc/server.rs`

### Typed Error Evolution
- `receipt.rs`: `Box<dyn Error>` → `BearDogError` (load_from_file, validate)
- `adapter_certificates.rs`: `Box<dyn Error>` → `BearDogError` (verify)
- `hyperoptimized_zero_copy.rs`: `Box<dyn Error>` → `BearDogError` (new, get_buffer, zero_copy_operation)
- `simd_optimizations/advanced.rs`: `Result<(), String>` → `Result<(), BearDogError>`
- `peer_to_peer_genetics.rs`: `Result<(), String>` → `Result<(), BearDogError>`

### DI-First Discovery (absorption from primalSpring pattern)
- `get_discovery_socket_paths` split into pure `build_discovery_socket_paths(ipc_socket, discovery_socket, dev_socket)`
- Tests now inject params directly — zero env var races, zero process-global state in test assertions
- Added `test_get_discovery_socket_paths_integration_with_env` for real-env smoke test

### SPDX Compliance
- All 29 `showcase/**/main.rs` files now have `// SPDX-License-Identifier: AGPL-3.0-only`

### Commented-Out Code Cleanup (wateringHole standard)
- `beardog-tunnel/src/lib.rs`: removed commented `pub mod`/`pub use` (PKCS#11 stubs)
- `beardog-security/src/lib.rs`: removed commented modules
- `beardog-integration/src/api_server.rs`: removed ~300 lines of commented BTSP/birdsong bindings
- `beardog-tunnel/src/btsp_provider.rs`: removed commented `let` lines
- `beardog-tunnel/src/graph_security/validate.rs`: removed commented verification block
- `beardog-core/src/primal_discovery.rs`: removed commented mDNS snippet
- `beardog-core/src/biome_sovereignty.rs`: removed commented engine setup
- `beardog-types/src/.../providers_unified/mod.rs`: removed commented trait exports

### Smart File Refactoring
- `monitoring_error_path_tests.rs` (990) → `common.rs` + `metrics.rs` + `alerts_health.rs`
- `hsm_provider_selection_tests.rs` (980) → `unit.rs` + `integration.rs`
- `crypto_handlers_hashing.rs` (976) → `mod.rs` + `sha.rs` + `onion.rs` + `tests.rs`
- `comprehensive_core_tests.rs` (969) → `core_functionality.rs` + `messaging.rs` + `identity.rs` + `coordination.rs` + `storage.rs`

### Dead Code Evolution
- `api_server.rs`: `#[allow(dead_code)]` removed; struct fields now used in `tracing::info!`
- `ultimate_safety.rs`: `#[allow(dead_code)]` removed; `_safety_token` renamed
- `compliance_validation_tests.rs`: all allows removed; toy validators wired to use fields

### Coverage Push
- 40+ new tests in `beardog-deploy` and `beardog-installer`
- Error paths: ADB spawn failure, devices listing failure, app launch failure, pm list I/O error, logcat follow failure
- Boundary conditions: empty deploy list, invalid slugs, empty display names, WASM arch on Android
- Platform edge cases: unix-only metadata errors, Windows .exe resolution, bin_dir-is-a-file

---

## Gates

```bash
cargo fmt --all -- --check                              # PASS
cargo clippy --workspace --all-features -- -D warnings  # PASS (0 warnings)
cargo doc --workspace --all-features --no-deps          # PASS
cargo test --workspace                                  # 14,201 passed; 0 failed; 186 ignored
```

---

## Cross-Ecosystem Absorption Opportunities Identified

### For Primals (absorption from BearDog Wave 12)

| Pattern | Description | Applicable To |
|---------|-------------|---------------|
| `unwrap_used = "warn"` at workspace | Catches regressions without breaking tests | All primals |
| `#[expect(clippy::..., reason = "...")]` | Per-site lint suppression with documented reason | All primals |
| DI-first discovery functions | Pure logic + env wrapper pattern for testability | Songbird, ToadStool, NestGate |
| `Box<dyn Error>` → typed errors | Public API type safety | Any primal using `Box<dyn Error>` |
| Smart file splitting by domain | Test files split into domain submodules, not arbitrary chunks | All primals |

### For Springs (absorption from BearDog patterns)

| Pattern | Description | Applicable To |
|---------|-------------|---------------|
| `build_*` pure functions for env-dependent logic | Eliminates env var races in concurrent tests | All springs |
| Commented-out code audit | wateringHole standard enforcement | All springs |
| SPDX header automation | Ensure 100% coverage of .rs files | All springs |

### From Springs/Primals (BearDog should absorb)

| Pattern | Source | Status |
|---------|--------|--------|
| `IpcErrorPhase` + `DispatchOutcome` | rhizoCrypt, sweetGrass, neuralSpring | Not yet adopted — next wave |
| `extract_rpc_error()` helper | neuralSpring, airSpring | Not yet adopted |
| `resilient_call()` circuit breaker | neuralSpring, primalSpring | Not yet adopted |
| `normalize_method()` | wetSpring | Not yet adopted |
| `cargo-fuzz` targets | LoamSpine, NestGate | Not yet adopted |
| `--fail-under-lines 90` CI gate | airSpring, groundSpring | Not yet adopted |

---

## Compliance

| Standard | Status |
|----------|--------|
| Edition 2024 | MSRV 1.93.0 pinned |
| Pure Rust (ecoBin) | Zero C deps |
| UniBin | Single `beardog` binary |
| JSON-RPC + tarpc | Both supported |
| AGPL-3.0-only | 100% SPDX coverage |
| `forbid(unsafe_code)` | Workspace-wide |
| Workspace lints | pedantic + nursery + cast + unwrap/expect warn |
| Zero hardcoding | Capability-based discovery |
| Zero TODO/FIXME | All resolved |
| Zero commented-out code | All cleaned |
| File size < 1000 LOC | All compliant |
| Zero `#[serial]` | All tests concurrent |

---

## Follow-ups (Next Wave)

1. Push coverage to **90%** (adopt airSpring `--fail-under-lines 90` gate)
2. Adopt `IpcErrorPhase` / `DispatchOutcome` from rhizoCrypt/sweetGrass IPC patterns
3. Add `extract_rpc_error()` and `resilient_call()` from neuralSpring
4. Add `cargo-fuzz` targets for JSON-RPC parser
5. Clarify ORC license component with wateringHole maintainers
6. Evolve `AGPL-3.0-only` vs `-or-later` discrepancy per scyBorg guidance
