# Songbird v0.2.1 Wave 135 — SB-02 + SB-03 Fully Resolved

**Date**: April 11, 2026
**Primal**: Songbird
**Version**: v0.2.1
**License**: AGPL-3.0-or-later
**Source**: primalSpring portability debt audit (April 11, 2026)

---

## Summary

Wave 135 resolves the last two Songbird items from the primalSpring `PRIMAL_GAPS.md`:
**SB-02** (`ring-crypto` opt-in feature) and **SB-03** (`sled` persistence).
Both are fully eliminated — not feature-gated, not deprecated, **removed**.

**Tests**: 13,030 passed, 0 failed, 252 ignored (-1 from sled test removal)
**Clippy**: Zero warnings (`clippy::pedantic + nursery`, `--all-targets`, `-D warnings`)
**Fmt**: Clean
**cargo-deny**: Fully passing (bans, licenses, advisories, sources)
**Build**: Zero errors, zero warnings

---

## SB-02: `ring-crypto` Feature Removed (RESOLVED)

**Before**: `songbird-cli` had an opt-in `ring-crypto = ["rustls/ring"]` feature for
standalone testing without security provider. The feature was never compiled by default,
but its presence kept `ring` as an optional dependency of `rustls` in `Cargo.lock`.

**After**: Feature deleted. The single `#[cfg(feature = "ring-crypto")]` block in `tower.rs`
replaced with unconditional `rustls_rustcrypto::provider().install_default()`. Pure Rust
TLS bootstrap for both production (Tower Atomic delegation) and standalone scenarios.

**Lockfile**: `ring` remains in `Cargo.lock` as an **unactivated** optional dependency of
`rustls` — this is standard Cargo behavior (lockfile captures all possible resolutions
including optional deps). `cargo tree -i ring` confirms ring is **never compiled**.
The only path that could activate `ring` is the optional `k8s` feature (via `kube` → `rustls`).

**Files changed**: `crates/songbird-cli/Cargo.toml`, `crates/songbird-cli/src/cli/commands/tower.rs`

---

## SB-03: `sled` Dependency Fully Removed (RESOLVED)

**Before**: `sled-storage` feature (non-default, deprecated) in `songbird-orchestrator` and
`songbird-sovereign-onion`. 1,482 lines of sled storage code across 3 files. `sled` in `Cargo.lock`.

**After**: All sled code, features, and dependencies removed:
- **Deleted**: `songbird-orchestrator/src/task_lifecycle/storage_sled.rs` (689 lines)
- **Deleted**: `songbird-orchestrator/src/consent_management/storage_sled.rs` (462 lines)
- **Deleted**: `songbird-sovereign-onion/src/storage_sled.rs` (331 lines)
- **Cleaned**: All `#[cfg(feature = "sled-storage")]` gates removed from 7+ files
- **Adapted**: `songbird-onion-relay` switched from `OnionStorage` (sled) to `InMemoryOnionStorage`
- **Lockfile**: `sled` no longer appears in `Cargo.lock`

**Storage architecture (final)**:
1. **NestGate** (production): `NestGateStorage` / `NestGateOnionStorage` via `storage.*` JSON-RPC
2. **InMemory** (fallback): `InMemoryStorage` / `InMemoryOnionStorage` when no storage provider

No sled code remains anywhere in the 30-crate workspace.

---

## QUIC/TLS Frontier Status (Documented)

Not debt — ongoing evolution:
- **QUIC**: 6,352 lines, pure Rust, `forbid(unsafe_code)`, zero ring/quinn/rustls deps,
  security provider crypto delegation. RFC 9000/9001/9002 compliant.
- **TLS**: 8,513 lines, pure Rust, `forbid(unsafe_code)`, TLS 1.3 RFC 8446.
- No `todo!()`, no `BLOCKED:` comments, no unsafe blocks.
- Frontier: middlebox compatibility, federation patterns, multi-path.

---

## primalSpring Gap Status (Songbird — All Clear)

| ID | Status | Wave |
|----|--------|------|
| SB-01 | **RESOLVED** | Wave 89-90 |
| SB-02 | **RESOLVED** | Wave 135 (this handoff) |
| SB-03 | **RESOLVED** | Wave 135 (this handoff) |

**Songbird has zero open gaps in primalSpring `PRIMAL_GAPS.md`.**

---

## Verification

```
cargo fmt --check                                           # PASS
cargo clippy --workspace --all-targets -- -D warnings       # PASS (zero warnings)
cargo test --workspace                                      # 13,030 passed, 0 failed
cargo deny check                                            # advisories ok, bans ok, licenses ok, sources ok
cargo tree -i ring                                          # "did not match any packages" (not compiled)
grep -c 'name = "sled"' Cargo.lock                          # 0 (fully removed)
```
