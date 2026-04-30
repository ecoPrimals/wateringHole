# NestGate v4.7.0-dev Session 50 Deep Debt Audit & Cleanup

**Date**: April 30, 2026
**Session**: 50
**Trigger**: Comprehensive deep debt audit — all dimensions

---

## Audit Results (Pre-Cleanup)

| Dimension | Status |
|-----------|--------|
| Files >800 lines | **Zero** (largest: 787L `types_tests.rs`) |
| `unsafe` code | **Zero** |
| `#[deprecated]` | **Zero** |
| `todo!()` / `unimplemented!()` | **Zero** |
| `Box<dyn Error>` in production | **Zero** (test-only) |
| `async_trait` | **Zero** (fully native async traits) |
| Production `.unwrap()` / `.expect()` | **Zero** (workspace denies `unwrap_used` / `expect_used`) |
| `#[allow(dead_code)]` in production | **Zero** (test/example only) |

---

## What Changed

### 1. Unused Dependencies Purged (14 crates removed)

Verified zero imports in `.rs` code, then removed:

**Root `Cargo.toml`**: `portpicker`, `test-log`, `rstest` (workspace entry + dev-dep)
**`nestgate-api`**: `rstest`
**`nestgate-zfs`**: `proptest`, `quickcheck`, `wiremock`, `testcontainers`, `assert_matches`, `approx`, `fake`, `test-log`, `rstest`
**`nestgate-installer`**: `nix` (unix), `winreg`, `windows-service`, `winapi` (windows)

All were declared but never imported. Lockfile shrinks accordingly.

### 2. Hardcoding Evolved to Capability-Based

**`BEARDOG_SOCKET` env var** (`storage_encryption.rs`):
- Renamed function `resolve_beardog_socket` to `resolve_security_provider_socket`
- Primary env var now `SECURITY_PROVIDER_SOCKET` with `BEARDOG_SOCKET` as backward-compat fallback

**Auth mode** (`run.rs`):
- `NESTGATE_AUTH_MODE=delegated` is the canonical value (capability-agnostic)
- `beardog` remains as backward-compat alias

**BTSP handshake comments** (`btsp_server_handshake/mod.rs`):
- Replaced primal-specific "BearDog" references with "security provider" in comments

**XDG socket discovery** (`btsp_client.rs`):
- Socket directory now configurable via `ECOSYSTEM_SOCKET_DIR` env var
- Defaults to `biomeos` for backward compat

### 3. Hardware Tuning Stubs Evolved to Real Implementations

**`handlers.rs`** — Four benchmark methods (`run_cpu_benchmark`, `run_memory_benchmark`, `run_gpu_benchmark`, `run_io_benchmark`) returned fabricated scores. Replaced with a single `snapshot_benchmark` method that samples live `/proc` metrics. Module documentation updated to remove "DEVELOPMENT STUBS" label.

### 4. Streaming Registry + fetch_external Dispatch (Phase 56c)

(From earlier in this session)
- Streaming methods added to `capability_registry.toml`
- `storage.fetch_external` wired into semantic router and isomorphic adapter
- Streaming wire protocol documented in QUICK_START_BIOMEOS.md and transport README

---

## Verification

```
cargo check --workspace              PASS
cargo clippy --workspace -- -D warnings   PASS (zero warnings)
cargo fmt --check                    PASS
cargo test --workspace --lib         8,841 passed, 0 failed, 60 ignored
```

---

## Remaining Known Debt (Low Priority)

- **Clone hotspots**: 15 files with 10+ `.clone()` calls; most are ownership-necessary (locks, async, DTOs)
- **`/tmp/` fallback paths**: Many socket/cache defaults use `/tmp/`; operationally correct but could use `XDG_RUNTIME_DIR` more consistently
- **`BIOMEOS_*` env vars**: Ecosystem naming convention; not primal coupling per se
- **`FAMILY_SEED` fallback chain**: Has `BEARDOG_FAMILY_SEED` and `BIOMEOS_FAMILY_SEED` as last-resort fallbacks (canonical `FAMILY_SEED` and `SECURITY_FAMILY_SEED` checked first)

---

## Files Modified

- `Cargo.toml` (root) — removed `portpicker`, `test-log`, `rstest`
- `code/crates/nestgate-api/Cargo.toml` — removed `rstest`
- `code/crates/nestgate-zfs/Cargo.toml` — removed 9 unused dev-deps
- `code/crates/nestgate-installer/Cargo.toml` — removed `nix`, `winreg`, `windows-service`, `winapi`
- `code/crates/nestgate-rpc/src/rpc/storage_encryption.rs` — capability-based provider discovery
- `code/crates/nestgate-rpc/src/rpc/btsp_client.rs` — configurable socket directory
- `code/crates/nestgate-rpc/src/rpc/btsp_server_handshake/mod.rs` — primal-agnostic comments
- `code/crates/nestgate-bin/src/cli/run.rs` — delegated auth mode
- `code/crates/nestgate-api/src/handlers/hardware_tuning/handlers.rs` — live benchmarks
- Root docs updated to Session 50
