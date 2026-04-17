# BearDog v0.9.0 — Wave 56: serde_yaml Elimination + Deep Debt

**Date**: April 16, 2026
**From**: BearDog primal team
**License**: AGPL-3.0-or-later

---

## Summary

Wave 56 eliminates the last deprecated external dependency (`serde_yaml` /
`unsafe-libyaml`), converts the sole production `Box<dyn Error>` to typed
errors, migrates `#[allow()]` to `#[expect()]`, and smart-refactors 3 large
test files into domain modules.

## Changes

### serde_yaml Elimination

`serde_yaml` is deprecated upstream and internally uses `unsafe-libyaml` (C FFI).
No YAML config files exist in the repo — only TOML and JSON are used.

| Crate | Change |
|-------|--------|
| `beardog-types` | YAML branches in `unified_impl.rs` now return deprecation error |
| `beardog-production` | YAML load path in `runtime.rs` returns deprecation error |
| `beardog-config` | Removed `ConfigError::YamlParse` variant |
| Workspace root | Removed `serde_yaml` from `[workspace.dependencies]` |

Both `serde_yaml` and `unsafe-libyaml` eliminated from `Cargo.lock`.

### Typed Errors

`Box<dyn std::error::Error + Send + Sync>` in `orchestration.rs` (AI module,
`#[cfg(feature = "ai")]`) converted to `BearDogError`.

### #[allow()] → #[expect()]

Production `#[allow()]` attrs migrated to `#[expect()]` where lints fire.
Cross-target and crate-root `#[allow()]` retained where `#[expect()]` would
cause unfulfilled expectations.

### Test File Refactoring

| File | LOC | Split Into |
|------|-----|-----------|
| `coverage_gap_wave18.rs` | 947 | 8 domain modules (cloud_hsm, service_discovery, etc.) |
| `rustcrypto_tests.rs` | 935 | 11 domain modules (aes, chacha20, ed25519, etc.) |
| `software_hsm/tests.rs` | 912 | 8 domain modules (init, keygen, crypto_ops, etc.) |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | **CLEAN** |
| `cargo clippy -- -D warnings` | **CLEAN** |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | **CLEAN** |
| `cargo test --workspace` | **14,786+ tests, 0 failures** |
| `serde_yaml` in Cargo.lock | **ZERO** |
| `unsafe-libyaml` in Cargo.lock | **ZERO** |
| `async-trait` in Cargo.lock | **ZERO** |
| `ring` in Cargo.lock | **ZERO** |
| Production `Box<dyn Error>` | **ZERO** |
| Production mocks | **ZERO** |
| `unsafe` code | **ZERO** |
| TODO/FIXME | **ZERO** |

## Debt Status

BearDog carries zero known Class 1–4 debt. The only remaining external dep
concern is `syn v2` (required by proc-macro ecosystem — not actionable).
All production files under 800 LOC. Edition 2024.

---

*Previous handoff: Wave 55 — async-trait Lockfile Elimination (archived)*
