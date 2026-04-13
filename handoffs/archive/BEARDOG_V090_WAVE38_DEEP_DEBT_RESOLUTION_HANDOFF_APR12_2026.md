# BearDog v0.9.0 — Wave 38: Deep Debt Resolution

**Date**: April 12, 2026
**Wave**: 38
**Primal**: bearDog
**Prior**: Wave 37 (primalSpring Audit Resolution — Contract Signing, BTSP Relay Path, Encoding Docs)
**Context**: Continuing deep debt cleanup and evolution per primalSpring downstream audit

---

## Summary

Systematic deep debt resolution: smart refactoring of the last >1000 LOC file,
production stub evolution to real implementations, hardcoded path elimination,
dead feature cleanup, and idiomatic Rust improvements.

## Changes

### Smart Refactoring

- **`ionic_bond.rs` (1022 LOC → 4 submodules)** — Extracted by logical concern:
  `crypto.rs` (129 LOC, signing/verification helpers), `lifecycle.rs` (261 LOC,
  propose/accept/verify/revoke/list), `contract.rs` (75 LOC, sign/verify contract),
  `mod.rs` (101 LOC, dispatch + struct). Tests in `tests.rs` (482 LOC). All 14
  tests pass, all public APIs preserved via re-exports.

### Production Stub Evolution

- **iOS Secure Enclave key agreement** — Placeholder returning `vec![0u8; 32]`
  replaced with real X25519 Diffie-Hellman via `x25519-dalek`. Non-iOS platforms
  get genuine software-fallback ECDH; iOS path logs explicit platform warning.

- **Load balancing simulated metrics** — 4 algorithm implementations evolved:
  - `least_connections_balance`: reads real `service_connections` from `LoadBalancerState`
  - `weighted_round_robin_balance`: reads real `service_weights` from state
  - `least_response_time_balance`: reads `avg_response_ms` from service metadata
  - `resource_based_balance`: reads `resource_usage` from service metadata
  - 6 unnecessary `Vec::clone()` calls eliminated from dispatch path

### Hardcoded Path Elimination

- `SoftwareHsmConfig` in `beardog-types` → `resolve_temp_dir()` (XDG/env-first)
- `SoftwareHsmConfig` in `beardog-tunnel` → `resolve_key_storage_dir()` (consolidated)
- `doctor.rs` key-storage check → `resolve_key_storage_dir()` (was manual 4-tier fallback)
- `/tmp/beardog*` constants remain as documented Tier-5 last-resort fallbacks only

### Lint Evolution

- `#[allow(clippy::cast_precision_loss)]` → `#[expect(...)]` with reason strings
  in `monitoring/service.rs` (CPU/memory ratio calculations)
- `#[allow(` count: 75 → 67; `#[expect(` count: 476 → 629

### Debris Cleanup

- Dead Cargo features removed: `beardog-genetics` (5 unused architecture flags +
  `genetics_tests_disabled_during_refactor`), `beardog-utils` (`bytes`),
  `beardog-cli` (`system-commands`)
- Empty directory removed: `crates/beardog-types/tests/`
- Stale `tests/integration/README.md` replaced (was referencing retired `btsp-api`
  feature, hardcoded "Songbird" names, HTTP patterns, dead file paths)
- Root docs updated with accurate metrics (1,967 Rust files, 14,906+ tests)

## Code Health (Wave 38 State)

| Metric | Value |
|--------|-------|
| Tests | 14,906+ passing (0 failures) |
| Coverage | 90.51% lines |
| Clippy | 0 warnings (workspace `-D warnings`) |
| Doc warnings | 0 (`RUSTDOCFLAGS="-D warnings"`) |
| Unsafe blocks | 0 production (`forbid(unsafe_code)`) |
| TODO/FIXME | 0 |
| Files > 1000 LOC | 0 production |
| `#[allow(` | 67 (all with reason strings or documented lib+bin incompatibility) |
| `#[expect(` | 629 |
| Dead features | 0 (7 removed this wave) |
| Production mocks | 0 (iOS SEP + load balancing evolved this wave) |

## For primalSpring Gap Registry

- **IONIC-RUNTIME**: RESOLVED (Wave 37) — `crypto.sign_contract` + `crypto.verify_contract`
- **BTSP-BARRACUDA-WIRE**: RESOLVED (Wave 37) — `btsp.server.export_keys`
- **LD-01**: RESOLVED (Wave 37) — Encoding contract documented
- **DEEP-DEBT**: RESOLVED (Wave 38) — All production stubs evolved, hardcoding eliminated

## Remaining Debt (Low Priority)

- Bond persistence (NestGate/LoamSpine integration for durable bonds — external)
- HSM/BTSP Phase 3 signing path (FIDO2/TPM hardware wiring — blocked on hardware)
- `serde_yaml` deprecated upstream — tracking `yaml_serde` successor (4 files, minimal usage)
- Coverage 90.51% → maintain above 90% target
