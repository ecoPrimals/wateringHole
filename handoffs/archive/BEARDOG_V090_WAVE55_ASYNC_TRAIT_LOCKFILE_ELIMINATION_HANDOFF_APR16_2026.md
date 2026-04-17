# BearDog v0.9.0 — Wave 55: async-trait Lockfile Elimination

**Date**: April 16, 2026
**From**: BearDog primal team
**License**: AGPL-3.0-or-later

---

## Summary

BearDog clears the stadial async-trait gate as the 13th and final primal.
`async-trait` is fully eliminated from both source code and `Cargo.lock`.

## Root Cause

`async-trait` remained in `Cargo.lock` as a transitive dependency through two
never-enabled optional features:

1. `hickory-resolver v0.24` (optional `dns-sd` feature in `beardog-discovery`)
   pulled `hickory-proto` which depends on `async-trait`
2. `tarpc v0.34` (optional `tarpc` feature in `beardog-ipc`) pulled
   `opentelemetry v0.18` → `opentelemetry_sdk v0.18` → `async-trait`

Both features were never enabled in any workspace crate, but Cargo v4 lockfile
format resolves all optional dependencies.

Additionally, `hickory-resolver` was listed as a non-optional dependency in
`beardog-core/Cargo.toml` with zero source references — a leftover from an
earlier wave.

## Changes

| Change | File |
|--------|------|
| Remove unused `hickory-resolver` | `beardog-core/Cargo.toml` |
| Remove `tarpc` optional dep + all associated optional crypto deps | `beardog-ipc/Cargo.toml` |
| Delete 3 orphan tarpc source files (71 KB) | `beardog-ipc/src/{tarpc_client,tarpc_types,multi_transport}.rs` |
| Remove dead `#[cfg(feature = "tarpc")]` module declarations | `beardog-ipc/src/lib.rs` |
| Suspend `dns-sd` feature | `beardog-discovery/Cargo.toml`, `beardog-discovery/src/lib.rs` |
| Ban `async-trait` in `deny.toml` | `deny.toml` |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | **CLEAN** |
| `cargo clippy -- -D warnings` | **CLEAN** |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | **CLEAN** |
| `cargo test --workspace` | **14,786+ tests, 0 failures** |
| `async-trait` in Cargo.lock | **ZERO** |
| `tarpc` in Cargo.lock | **ZERO** |
| `opentelemetry` in Cargo.lock | **ZERO** |
| `ring` in Cargo.lock | **ZERO** |
| `sled` in Cargo.lock | **ZERO** |
| `openssl` in Cargo.lock | **ZERO** |
| `unsafe` in production | **ZERO** |

## Stadial Gate Status

BearDog is the **13th of 13 primals** to clear the ecosystem async-trait gate.
The stadial phase can now end.

---

*Previous handoff: Wave 54 — Deep Debt Pass (archived)*
