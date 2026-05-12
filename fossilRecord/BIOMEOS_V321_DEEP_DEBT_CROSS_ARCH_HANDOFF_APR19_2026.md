# biomeOS v3.21 — Deep Debt Evolution: Cross-Arch Fix + Path/IP Centralization

**Date**: April 19, 2026
**From**: biomeOS team
**Version**: v3.20 → v3.21
**Status**: PRODUCTION READY — zero blocking debt, armv7 cross-arch resolved

---

## Summary

Two-part evolution pass: (1) resolved the final primalSpring audit gap — armv7 (32-bit) build failure in `cast.rs`, and (2) completed hardcoded IP and runtime path centralization across all remaining production files.

---

## Changes

### 1. Cross-Arch Fix: armv7 (32-bit) Build — `cast.rs`

**Reporter**: primalSpring v0.9.17 genomeBin cross-arch matrix
**Severity**: MEDIUM (blocked armv7 builds only)

**Problem**: `const MAX_EXACT: usize = 1_usize << 53` overflows on 32-bit targets where `usize` is 32 bits.

**Fix**:
- `MAX_EXACT` changed from `usize` to `u64`: `const MAX_EXACT: u64 = 1_u64 << 53`
- Comparison casts `v` to `u64`: `if (v as u64) <= MAX_EXACT`
- Tests updated with `cfg!(target_pointer_width = "64")` conditional assertions
- On 32-bit, `usize::MAX < 2^53` so all values are exact — no overflow possible

**Files**: `crates/biomeos-types/src/cast.rs`

### 2. Hardcoded IP Centralization — `dns_sd.rs`, `init.rs`

Replaced 5 remaining raw IP literals in production code with `biomeos-types::constants` references:

| File | Before | After |
|------|--------|-------|
| `dns_sd.rs:225` | `"0.0.0.0:0"` | `endpoints::EPHEMERAL_UDP_BIND` |
| `dns_sd.rs:354` | `"127.0.0.1"`, `"::1"` | `endpoints::DEFAULT_LOCALHOST`, `DEFAULT_LOCALHOST_V6` |
| `dns_sd.rs:385` | `"0.0.0.0:0"` | `endpoints::EPHEMERAL_UDP_BIND` |
| `dns_sd.rs:388` | `"192.0.2.1:80"` | `network::RFC5737_ROUTE_PROBE` (new) |
| `init.rs:338` | `"127.0.0.1:0"` | `endpoints::DEFAULT_LOCALHOST` |

**New constant**: `network::RFC5737_ROUTE_PROBE = "192.0.2.1:80"` — sovereignty-compliant route probe (RFC 5737 TEST-NET, never routed).

### 3. Runtime Path Centralization — `path_builder.rs`, `defaults.rs`

Replaced 4 remaining raw path literals with `biomeos-types::constants::runtime_paths` references:

| File | Before | After |
|------|--------|-------|
| `path_builder.rs:57,69` | `"/run/user/{uid}/biomeos"` (×2) | `runtime_paths::LINUX_RUNTIME_DIR_PREFIX` + `BIOMEOS_SUBDIR` |
| `path_builder.rs:78` | `"/data/local/tmp/biomeos"` | `runtime_paths::ANDROID_RUNTIME_BASE` (new) |
| `path_builder.rs:85` | `"/tmp/biomeos"` | `runtime_paths::FALLBACK_RUNTIME_BASE` |
| `defaults.rs:215` | `"/run/user/{uid}/biomeos"` | `runtime_paths::LINUX_RUNTIME_DIR_PREFIX` + `BIOMEOS_SUBDIR` |

**New constant**: `runtime_paths::ANDROID_RUNTIME_BASE = "/data/local/tmp/biomeos"` — Android runtime socket directory.

---

## Verification

- `cargo check --workspace` — PASS
- `cargo clippy --workspace --all-targets` — 0 warnings
- `cargo test --workspace` — 7,802 tests, 0 failures
- `cargo fmt --all -- --check` — PASS

---

## Audit Status

All primalSpring audit gaps are now **RESOLVED**:

| Gap | Status | Version |
|-----|--------|---------|
| `biomeos-types` missing `secret` module (PG-34) | RESOLVED | v3.18 |
| TCP port binding conflicts | RESOLVED | v3.18 |
| Running primals not auto-registered | RESOLVED | v3.18 |
| Tick-loop scheduling (60Hz) | RESOLVED | v3.16 |
| `async-trait` elimination | RESOLVED | v3.00 |
| `genetics_tier` enforcement | RESOLVED | v3.16 |
| Deploy class auto-resolution | RESOLVED | v3.16 |
| Capability routing contract | RESOLVED | v3.16 |
| armv7 (32-bit) build failure | **RESOLVED** | **v3.21** |

**primalSpring v0.9.17 stated**: "this is the **only biomeOS gap**" — now closed.

---

## Zero Hardcoding Status

After v3.21, production code has **zero** raw literals for:
- IP addresses (all via `endpoints::*` or `network::*` constants)
- Filesystem runtime paths (all via `runtime_paths::*` constants)
- Primal names (all via `primal_names::*` constants)
- Ports (all via `ports::*` constants)
- Nucleus/spawner config (all via TOML-driven launch profiles)

---

**biomeOS v3.21** | 7,802 tests | 0 clippy warnings | 0 unsafe | 0 C deps | 0 hardcoded values | cross-arch safe (x86_64 + aarch64 + armv7)
