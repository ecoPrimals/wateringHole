# Songbird v0.2.1 — Wave 72–73: Capability-First Discovery + Deep Debt Execution

**Date**: March 27, 2026
**Version**: v0.2.1
**Session**: 19 (Comprehensive Audit → Execution)

---

## Summary

Full codebase audit followed by systematic execution on all identified technical debt. Two major waves completed: infrastructure fixes (Wave 72) and capability-first discovery evolution (Wave 73).

---

## Wave 73: Hardcoded Primal Name Elimination

### Problem
Production discovery paths embedded primal identities (`beardog.sock`, `squirrel.sock`) in socket scan lists, fallback paths, and error messages. This violated the "self-knowledge only" principle — Songbird should discover crypto providers by *capability*, not by *identity*.

### Changes (8 files)
- `songbird-types/src/defaults/paths.rs`: Removed `"beardog.sock"` and `"squirrel.sock"` from socket scan constants — capability names only (`crypto.sock`, `security.sock`, `ai.sock`, `neural-api.sock`)
- `songbird-orchestrator/src/app/core.rs`: Crypto socket discovery now prefers `CRYPTO_PROVIDER_SOCKET` env var, falls back to `crypto-{family}.sock` (was `beardog-{family}.sock`)
- `songbird-http-client/src/beardog_client/core.rs`: Direct-mode fallback `/tmp/beardog.sock` → `/tmp/crypto.sock`
- `songbird-crypto-provider/src/socket_discovery.rs`: Renamed `beardog_socket_path_in_biomeos_runtime` → `crypto_socket_path_in_biomeos_runtime` (deprecated alias kept)
- `songbird-crypto-provider/src/rpc.rs`: Error message "BearDog" → "crypto provider"
- `songbird-lineage-relay/src/beardog.rs`: Removed `"beardog.sock"` from XDG scan
- `songbird-nfc/src/config.rs`: Removed `"beardog.sock"` from XDG scan
- `songbird-tls/src/socket_discovery.rs`: Updated test + docs from identity to capability names

### Discovery Priority (unchanged)
1. `$CRYPTO_PROVIDER_SOCKET` (capability env var — preferred)
2. `$BEARDOG_SOCKET` (legacy compat — still supported)
3. `$XDG_RUNTIME_DIR/biomeos/crypto.sock` (XDG capability scan)
4. `/run/user/$UID/biomeos/crypto.sock` (UID fallback)
5. `/tmp/crypto.sock` (legacy fallback)

---

## Wave 72: Infrastructure Fixes

### Port Fallback Tests
- Rewrote all 13 tests in `port_fallback_test.rs` to use OS-assigned ephemeral ports (port 0)
- Eliminated `PortOccupier::occupy(9100)` pattern — tests now fully concurrent-safe

### File Size Discipline
- `core.rs` 1021→816 lines: Extracted 18 broadcast tests to `core_broadcast_tests.rs` via `#[path]`
- `infant_config.rs` 1036→697 lines: Extracted 18 tests to `infant_config_tests.rs` via `#[path]`

### Binary Collision
- Removed `[[bin]]` section from `songbird-orchestrator/Cargo.toml` — root `songbird` is the sole UniBin
- Updated 52 `assert_cmd::cargo_bin!()` → `assert_cmd::cargo::cargo_bin()` across 8 test files

### License Reconciliation
- `LICENSE` text updated from "version 3 or later" to "version 3 only" (aligns with `AGPL-3.0-only` SPDX)

### Lint Evolution
- Bare `#[allow(dead_code)]` → `#[expect(dead_code, reason = "...")]` in `startup_orchestration.rs`
- `#[allow(clippy::too_many_lines)]` → `#[expect(..., reason = "...")]` in `service.rs`

### Test Robustness
- Fixed flaky `test_port_allocation_is_cached` (race condition with `clear_port_registry`)
- Fixed mutex poisoning in `core_broadcast_tests.rs` under `llvm-cov`

---

## Debris Cleanup

### Archived (moved to `ecoPrimals/archive/infrastructure-sept-2025/`)
- `infrastructure/kubernetes/songbird-deployment.yaml` — Pre-UniBin multi-container k8s (Sept 2025)
- `infrastructure/terraform/main.tf` — AWS EKS from Sept 2025
- `man/songbird-gaming.1` — References non-existent "gaming" feature

### Root Docs Updated
- `CONTEXT.md`: Refreshed metrics, fixed stale repo path (`phase1/` → `primals/`), added capability-first discovery notes
- `README.md`: Updated file size metrics
- `REMAINING_WORK.md`: Added Wave 72–73 completion records, updated audit date

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 10,687 passed, 0 failed, 271 ignored |
| Line Coverage | ~67% (llvm-cov; target 90%) |
| Files >1000 LOC | 0 (max 925) |
| Clippy | Zero warnings (pedantic + nursery) |
| Production panics/unwrap/todo | 0 |
| Hardcoded primal names in discovery | 0 |
| `cargo fmt` | Clean |
| `cargo doc` | Clean |
| `cargo test --all` | Clean |

---

## IPC Compliance Status (per wateringHole standards)

| Requirement | Status |
|-------------|--------|
| JSON-RPC 2.0 newline framing | Compliant |
| `$XDG_RUNTIME_DIR/biomeos/*.sock` | Compliant (capability-named) |
| `health.liveness` / `health.readiness` / `health.check` | Compliant |
| `capabilities.list` | Compliant |
| Standalone startup (no orchestrator required) | Compliant |
| `--dark-forest` CLI flag | Gap (P1) |
| `--pid-dir` / `SONGBIRD_PID_DIR` | Gap (P2) |
| Optional `--listen addr:port` | Gap (P2) |
| GAP-006: `discovery.query` capability filter | Gap (P2) |

---

## Next Priority

1. Coverage expansion toward 90% (pure-logic modules first)
2. `--dark-forest` CLI flag (IPC compliance gap)
3. Ring-free workspace (`rcgen` replacement + `quinn` feature reconfiguration)
4. `--pid-dir` for read-only CWD (Android/constrained substrate)
