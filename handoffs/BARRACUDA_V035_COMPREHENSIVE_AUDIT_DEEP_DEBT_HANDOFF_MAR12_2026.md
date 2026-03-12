<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda v0.3.5 — Comprehensive Audit & Deep Debt Handoff

**Date**: March 12, 2026
**Primal**: barraCuda
**Version**: 0.3.5
**Type**: Deep debt evolution + wateringHole standards compliance audit

---

## Summary

Full codebase audit against wateringHole standards (uniBin, ecoBin, semantic
naming, sovereignty, zero-copy, license compliance, code quality). 12-item
remediation completed. All quality gates green. 3,688 tests pass, 0 fail.

---

## Changes

### wateringHole Standards Compliance

1. **`#![forbid(unsafe_code)]`**: Upgraded from `deny` (overridable) to `forbid`
   (irrevocable) in both `barracuda` and `barracuda-core` crate roots.

2. **Namespace-derived IPC method names**: All 12 hardcoded `"barracuda.method.name"`
   string literals evolved to `LazyLock<Vec<String>>` built from `PRIMAL_NAMESPACE`
   + `METHOD_SUFFIXES`. Dispatch routing uses `method_suffix()` to strip the
   namespace prefix. Discovery, tarpc, and CLI all consume the derived names.
   Primal code only has self-knowledge — no hardcoded references to other primals.

3. **SPDX license headers**: 648 WGSL shaders were missing
   `// SPDX-License-Identifier: AGPL-3.0-only` headers. All 805 shaders now have
   them. All 1,062 Rust files already had them.

4. **BufferBinding import**: Added missing import in `coral_reef_device.rs` so
   `--all-features` clippy passes (sovereign-dispatch feature gate).

### Code Quality Evolution

5. **9 pedantic lints promoted**: `needless_raw_string_hashes`,
   `redundant_closure_for_method_calls`, `bool_to_int_with_if`,
   `cloned_instead_of_copied`, `map_unwrap_or`, `no_effect_underscore_binding`,
   `format_push_string`, `explicit_iter_loop`, `used_underscore_binding` — all
   promoted from bulk-allow to warn, all violations fixed, enforced via
   `-D warnings`. 2 lints kept as `allow` with documented rationale
   (`needless_range_loop`: 56 sites in scientific code, `if_same_then_else`:
   7 sites in numerical branching).

6. **erfc_f64 recursion fix**: `stable_f64.wgsl` had recursive `erfc_f64` (WGSL
   forbids recursion). Refactored to non-recursive `erfc_x_nonneg_f64` helper.
   This was the only test failure in the suite.

7. **Magic numbers extracted**: `CONSERVATIVE_GPR_COUNT` (128), `DEFAULT_WORKGROUP`
   ([64,1,1]), `CORAL_CACHE_ARCHITECTURES` constants in `coral_reef_device.rs`.

8. **Zero-copy evolution**: `async_submit::read_bytes()` and `ncbi_cache::load()`
   evolved to return `bytes::Bytes` instead of `Vec<u8>`.

9. **`unreachable!` evolved**: Production `unreachable!()` in `df64_rewrite`
   evolved to `debug_assert!` + graceful fallback.

10. **Rustdoc zero warnings**: Fixed broken `transport::resolve_bind_address`
    link and private `wgsl_templates` link.

11. **`cargo clippy --fix`**: Auto-fixed applicable violations across workspace.

12. **5 underscore-binding lint violations**: Fixed manually in examples and tests.

---

## Quality Gate Results

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -- -D warnings` | Pass (all configs including default, no-default, all-features) |
| `cargo doc --no-deps` | Pass (zero warnings) |
| `cargo deny check` | Pass (advisories, bans, licenses, sources) |
| `cargo nextest --no-fail-fast` | 3,688 pass / 0 fail / 15 skip |

---

## Remaining Known Debt

### P1 (Immediate)
- DF64 NVK end-to-end verification (blocked on hardware)
- coralNAK extraction (blocked on org repo fork)

### P2 (Near-term)
- Test coverage ~75% (target 90%; CI floor 80%)
- Kokkos validation baseline
- `needless_range_loop` (56 sites) manual refactoring
- `if_same_then_else` (7 sites) manual refactoring
- `clippy::nursery` lint group not yet enabled
- 100+ `as` casts (inherent to GPU compute, all cast lints documented)

### P3 (Medium-term)
- Pipeline cache re-enable (waiting on safe wgpu API)
- Multi-GPU dispatch
- Shader hot-reload
- Further zero-copy evolution

---

## Files Changed

### barracuda crate
- `src/device/coral_reef_device.rs` — BufferBinding import, magic number extraction
- `src/device/async_submit.rs` — `read_bytes()` returns `bytes::Bytes`
- `src/ops/bio/ncbi_cache.rs` — `load()` returns `bytes::Bytes`
- `src/shaders/sovereign/df64_rewrite/mod.rs` — `unreachable!` -> `debug_assert!`
- `src/shaders/special/stable_f64.wgsl` — erfc_f64 recursion fix
- `src/numerical/ode_generic/mod.rs` — rustdoc private link fix
- `src/lib.rs` — `#![forbid(unsafe_code)]`
- `Cargo.toml` — 9 lints promoted, 2 kept with rationale
- 648 WGSL shaders — SPDX headers added
- Various — `cargo clippy --fix` auto-fixes

### barracuda-core crate
- `src/lib.rs` — `#![forbid(unsafe_code)]`
- `src/ipc/methods.rs` — `LazyLock<Vec<String>>` REGISTERED_METHODS, `METHOD_SUFFIXES`, `method_suffix()`
- `src/ipc/methods_tests.rs` — tests use `PRIMAL_NAMESPACE`-derived method names
- `src/ipc/mod.rs` — rustdoc link fix
- `src/discovery.rs` — capability-based comparison via `method_suffix()`
- `src/rpc.rs` — `.cloned()` instead of `.map(|m| m.clone())`
- `src/bin/barracuda.rs` — `.clone()` instead of `to_string()` for implicit clone

### Root docs
- `README.md` — updated counts, `forbid(unsafe_code)`, shader count
- `STATUS.md` — new achievements section, updated grades and counts
- `WHATS_NEXT.md` — new recently completed section
- `specs/REMAINING_WORK.md` — new achieved section, updated quality gates

---

## Cross-Primal Impact

None. All changes are internal to barraCuda. No API changes visible to consumers.
The IPC wire format is unchanged — method names are the same strings, just now
derived from constants instead of hardcoded.
