# nestGate Session 107 — Deep Debt Sweep (Wave 139a)

**Date**: Jul 14, 2026
**Wave**: 139a
**Head**: `5e508f5b`
**Posture**: Zero-debt continuation. No blocking tasks from Wave 139a (AlphaFold registration is BLOCKED on westGate hardware).

---

## Changes

### `String::from("literal")` → `.into()` sweep

~125 conversions across 12 production files in 7 crates:

| Crate | File | Count |
|-------|------|-------|
| nestgate-canonical | `error.rs` | 2 |
| nestgate-bin | `error.rs` | 8 |
| nestgate-config | `capability_config.rs` | 8 |
| nestgate-core | `response/mod.rs` | 5 |
| nestgate-core | `response/traits.rs` | 14 |
| nestgate-core | `services/storage/config.rs` | 8 |
| nestgate-discovery | `resolver.rs` | 4 |
| nestgate-discovery | `infant_discovery/mod.rs` | 18 |
| nestgate-installer | `config/mod.rs` | 12 |
| nestgate-zfs | `pool_setup/config.rs` | 47 |
| nestgate-zfs | `command.rs` | 6 |
| nestgate-zfs | `pool/operations.rs` | 7 |

Test code was not modified.

### Hardcoded path → env override

- `/opt/nestgate` install path: 4 hardcoded defaults replaced with `install_path_from_env()` which reads `NESTGATE_INSTALL_PATH` env var (falls back to `/opt/nestgate`).
- Affects `InstallerConfig::default()`, `::production()`, and both `installer_config_factory` functions.

---

## Test Results

- **3,790 passed**, 1 failed (pre-existing `universal_storage_bridge_list_pools`), 73 ignored
- 0 clippy warnings
- No regressions

## Remaining Debt (from audit)

| Priority | Item | Status |
|----------|------|--------|
| P0 | `json_rpc_handler.rs` Result<_, String> → typed errors | Deferred (high effort, cross-cutting) |
| P1 | NestGateError/ValidationError thiserror | Deferred (conditional Option Display) |
| P2 | Top-20 remaining `String::from` files | Partial (test-only remains) |
| P3 | `map_err(format!)` → context helpers (~200 sites) | Deferred |

## Wave 139a nestGate Status

- **AlphaFold CAS registration**: BLOCKED on westGate power-on
- **footPrint server**: Deployment concern (code is ready via FP-PERSIST)
- **No P1/P2 blockers**
