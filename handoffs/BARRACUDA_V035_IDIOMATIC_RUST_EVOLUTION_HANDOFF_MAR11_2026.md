# barraCuda v0.3.5 — Idiomatic Rust Evolution Handoff

**Date**: 2026-03-11
**Commit**: `d761c5d`
**Scope**: Codebase-wide audit and evolution toward modern idiomatic Rust

## Summary

Comprehensive audit of the barraCuda codebase identified and resolved
allocation inefficiencies, dead code, and redundant clone patterns.
The codebase is in excellent health: zero `unsafe`, zero production
`unwrap()`, zero `todo!()`, zero `#[allow(dead_code)]`, zero mocks
in production code.

## Changes

### 1. Double Allocation Elimination (11 files)

**Pattern**: `Arc::from(format!("...").as_str())` — allocates a `String`
then copies bytes into a separate `Arc<str>` heap allocation.

**Fix**: `Arc::from(format!("..."))` — `From<String> for Arc<str>`
reuses the String's buffer directly, eliminating one heap allocation
per call site.

**Files**: `coral_reef_device.rs`, `bessel_j0_f64_wgsl.rs`,
`bessel_j1_f64_wgsl.rs`, `bessel_i0_f64_wgsl.rs`,
`bessel_k0_f64_wgsl.rs`, `beta_f64_wgsl.rs`,
`covariance_f64_wgsl.rs`, `digamma_f64_wgsl.rs`,
`hermite_f64_wgsl.rs`, `weighted_dot_f64.rs`

### 2. Dead Export Removal

**Removed**: `pub use constants as npu_constants` from `npu/mod.rs`.
The alias was never referenced outside its own module. Constants
remain accessible via `npu::constants::*`.

### 3. Redundant Clone Elimination (rpc.rs)

- `primal_capabilities`: Was calling `self.primal.device()` three times,
  each cloning the entire `WgpuDevice`. Now calls once and reuses
  via `as_ref()`.
- `health_check`: Was cloning `report.name` and `report.version` out
  of an owned struct. Now moves the fields directly.

## Audit Findings (Already Clean)

| Category | Status |
|----------|--------|
| `unsafe` code | `#![deny(unsafe_code)]` enforced |
| Production `unwrap()` | None (all in `#[cfg(test)]`) |
| Production `expect()`/`panic!()` | None (all in `#[cfg(test)]`) |
| `todo!()`/`unimplemented!()` | None |
| `#[allow(dead_code)]` | None |
| Mocks in production | None |
| Hardcoded transport | Capability-based (env/CLI/discovery chain) |
| HashMap caches | Pre-hashed u64 keys, correct `RwLock` patterns |

## Quality Gates

- `cargo check --workspace` — pass
- `cargo fmt --all -- --check` — pass
- `cargo clippy --workspace -- -D warnings` — pass
- `cargo test -p barracuda-core --lib` — 60/60 pass
- `cargo test -p barracuda --lib -- routing driver_profile npu` — 92/92 pass

## Integration Notes

This is a pure internal quality evolution with no API changes.
All downstream consumers (hotSpring, ludoSpring, etc.) are unaffected.
