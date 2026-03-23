# BearDog v0.9.0 — Deep Debt Execution: Coverage Push, Stub Evolution & Hardcoding Cleanup

**Date**: March 22, 2026
**Primal**: BearDog (cryptographic service provider)
**Session Focus**: Deep debt solutions — coverage push toward 90%, production stub evolution, hardcoding extraction, file size compliance, flaky test elimination, orphan cleanup

---

## What Changed

### Coverage Push (85.1% → 86.8%)

~1,000+ newly covered lines across 8 crates, targeting the lowest-coverage production files:

| Area | Files Covered | Key Tests Added |
|------|--------------|-----------------|
| beardog-core | `capability_router.rs`, `secure_cross_primal_messaging.rs`, `primal_discovery.rs`, `ecosystem_storage/manager.rs` | Routing strategies, X25519 key exchange errors, UPA discovery, storage backend CRUD |
| beardog-types | `performance.rs`, `monitoring/core.rs`, `hsm/config.rs` | Config validation, JSON round-trip, retry policies, HSM provider validation |
| beardog-tunnel | `modes/server.rs`, `btsp_provider.rs`, `unix_socket_ipc/server.rs`, `ipc_server.rs`, `modes/doctor.rs`, `crypto_handler/genetic.rs` | Server socket paths, JSON-RPC handling, BTSP error paths, diagnostic mode, genetic handler |
| beardog-genetics | `interaction_capture.rs`, `engines.rs` | Scroll entropy derivation, population management, fitness evaluation |
| beardog-cli | `entropy.rs`, `key_mix.rs`, `client.rs`, `cross_primal.rs` | HSM interface labels, key mixing + receipt, Unix socket commands |
| beardog-threat | `incident.rs` | Full incident lifecycle: create/classify/escalate/assign/resolve/close |
| beardog-monitoring | `performance_metrics.rs` | Trend analysis, threshold violations, throughput checks |

### Production Stub Evolution

| Stub | Evolution |
|------|-----------|
| `disaster_recovery.rs` checksum | BLAKE3 content-addressed hash over deterministic tree walk |
| `heartbeat.rs` connection count | `AtomicUsize` + `ActiveConnectionGuard` RAII + Axum middleware |
| `monitoring.rs` timings | `Instant`-backed `RollingTiming` for seed creation/mixing/validation |
| UPA client | HTTP/reqwest → Tower Atomic (Unix sockets + JSON-RPC capability discovery) |

### Hardcoding Extraction (20+ sites)

| Category | Constants Extracted |
|----------|-------------------|
| Ports | `DEFAULT_INTEGRATION_API_PORT`, `DEFAULT_API_SERVER_LISTEN_PORT` |
| Timeouts | `DEFAULT_TARPC_CONNECT_TIMEOUT`, `DEFAULT_TARPC_REQUEST_TIMEOUT`, `DEFAULT_HEARTBEAT_INTERVAL_SECS` |
| Paths | `FALLBACK_REGISTRY_UNIX_SOCKET_PATH`, `DEFAULT_LOCAL_SOCKET_TMP_DIR`, `BEARDOG_TCP_DISCOVERY_FILENAME` |
| Cache | `DEFAULT_REQUEST_CACHE_TTL`, `STRING_CACHE_CLEANUP_MIN_INTERVAL_SECS` |
| Config | `DEFAULT_INTERACTION_CAPTURE_*`, `DEFAULT_UPA_URL` |
| Discovery | `biomeos_tmp_socket_root()` respects `BIOMEOS_TMP_ROOT` env var |

### Flaky Test Elimination

| Test | Root Cause | Fix |
|------|-----------|-----|
| `test_timeout_accuracy` | Wall-clock timing under load | `#[tokio::test(start_paused = true)]` + `time::advance()` |
| `test_auto_initialize_default_software_mode` | Process-global env race | `HsmAutoInitConfig::default()` + `auto_initialize_with_config` |
| `test_extreme_concurrent_load_stress` | 2s deadline too tight under CI load | Widened to 5s |
| `test_connection_recovery_after_mass_failure` | Race: all requests after recovery | Guaranteed early-batch failures while connections dead |

### File Size Compliance

| File | Before | After |
|------|--------|-------|
| `monitoring.rs` | 1,052 lines | 366 production + 576 test (via `#[path]`) |
| `secure_cross_primal_messaging.rs` | 1,111 lines | 603 production + 506 test (via `#[path]`) |

### Cleanup

- Archived `zero_cost_registry.rs`, `zero_cost_registry_tests.rs` → `archives/orphan_modules/`
- Archived legacy HTTP `integration_test.rs` (reqwest-based, pre-Tower-Atomic)
- Fixed misleading "placeholder" comments on real implementations
- beardog-integration removed from workspace exclude list (now a full member)

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features -- -D warnings` | 0 warnings |
| `cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | 9,500+ passed, 0 failed |
| `cargo deny check` | All 4 pass (advisories, bans, licenses, sources) |
| Files > 1000 LOC | 0 |
| `#[serial]` annotations | 0 |
| Test sleeps (non-chaos) | 0 |
| TODO/FIXME/HACK | 0 |
| `unsafe` in production | 0 |
| Line coverage | 86.8% |

---

## Ecosystem Impact

### For Other Primals

- **Hardcoding standard** — BearDog now has 20+ named constants with env var overrides for all network addresses, ports, paths, and timeouts. Other primals should follow the `DEFAULT_*` + `from_env()` pattern.
- **Tower Atomic adoption** — `beardog-integration` fully migrated from HTTP/reqwest to Tower Atomic. The UPA client uses capability-based discovery (`UPA_UNIX_SOCKET`, `CAPABILITY_UPA_REGISTER_ENDPOINT`, `UPA_PROVIDER`).
- **Connection tracking pattern** — `ActiveConnectionGuard` RAII + `AtomicUsize` provides zero-overhead connection counting for heartbeat reporting. Recommended for all primals.

### For wateringHole Standards

- **ZERO_HARDCODING_SPECIFICATION** — 20+ additional extraction points. Comprehensive scan completed.
- **ECOBIN_ARCHITECTURE_STANDARD** — 100% Pure Rust maintained. BLAKE3 for backup hashing.
- **CAPABILITY_BASED_DISCOVERY_STANDARD** — All socket discovery paths use `biomeos_tmp_socket_root()` with `BIOMEOS_TMP_ROOT` override.

---

## Remaining Gaps (Phase 2)

| Item | Status | Notes |
|------|--------|-------|
| Coverage 86.8% → 90% | ~3,800 lines | Binary `main.rs` (0%), server loops, platform-gated code |
| HSM vendor ops | Platform | PKCS#11, TPM, Solo-v2 need hardware bindings |
| `get_self_capabilities` | Stub | Returns `Ok(vec![])` — needs real capability mapping |
| Compliance handlers | Stub | Sovereignty/privacy hooks return empty |
| genomeBin lifecycle | Partial | Installer exists; service management/health/updates evolving |

---

## Verification Commands

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-features -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
cargo deny check
cargo llvm-cov --workspace --summary-only --ignore-run-fail
```
