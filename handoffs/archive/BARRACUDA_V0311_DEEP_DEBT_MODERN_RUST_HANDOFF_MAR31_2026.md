# barraCuda v0.3.11 — Sprint 25: Deep Debt Evolution & Modern Idiomatic Rust

**Date**: 2026-03-31
**From**: barraCuda team
**To**: All primals, spring teams
**License**: AGPL-3.0-or-later
**Covers**: Deep debt resolution, safety hardening, idiomatic Rust evolution, capability-based naming, smart refactoring

---

## Executive Summary

Major safety and idiom evolution sprint. Zero production panics/expects in naga-exec. All
`#[allow(` migrated to compile-time-verified `#[expect(`. barracuda-spirv unsafe tightened.
Index loops → iterators. Primal-specific naming → capability-based. Smart file refactoring.
HCI formula gaps (BC-01, BC-02) closed. True 3D Perlin noise (BC-03). All quality gates green,
4,100+ tests passing.

---

## Part 1: Safety Hardening

### 1.1 Production panics eliminated (naga-exec)

5 `panic!()` calls in `Value::as_f32/f64/u32/i32/bool` evolved to return
`Result<T, NagaExecError::TypeMismatch>`. Error propagation cascaded through
`eval.rs` (17 call sites) and `executor.rs` (8 call sites) via `?` operator.

**Impact**: Zero production panics in the entire `barracuda-naga-exec` crate.

### 1.2 Production `.expect()` eliminated (naga-exec)

6 `.expect("workgroup var")` calls on `WorkgroupMemory` methods evolved to
return `Result` with typed `NagaExecError::TypeMismatch`. New `get_mut()` helper.

Affected methods: `write()`, `atomic_load_u32()`, `atomic_add_u32()`,
`atomic_max_u32()`, `atomic_min_u32()`, `atomic_add_i32()`, `atomic_store_u32()`.

### 1.3 barracuda-spirv unsafe tightened

- Production `assert!` (panic) → `Result<_, SpirvError>` return type
- New `SpirvError` enum with `Display` + `Error` impls
- `#[allow(unsafe_code)]` → `#[expect(unsafe_code, reason = "wgpu passthrough
  requires unsafe until wgpu#4854 lands")]` — compile-time verified
- Caller in `compilation.rs` updated to handle `Result`

---

## Part 2: Convention Compliance

### 2.1 `#[allow(` → `#[expect(` migration

All 10 `#[allow(` annotations in `barracuda-naga-exec` migrated to `#[expect(`
with `reason` parameters:

| File | Lint | Reason |
|------|------|--------|
| `value.rs` | `cast_possible_truncation`, `cast_precision_loss` | WGSL numeric coercions |
| `eval.rs` | `too_many_lines` | exhaustive MathFunction dispatch |
| `executor.rs` | `dead_code` | retained for future validation |
| `executor.rs` | `too_many_arguments` | invocation context requires all state |
| `executor.rs` | `too_many_lines` | exhaustive naga Expression dispatch |
| `executor.rs` | `cast_possible_truncation` | handle index fits u32 |

Removed 2 unfulfilled `cast_sign_loss` expectations (detected by compiler).

### 2.2 Idiomatic iterator evolution

5 production `for i in 0..vec.len()` loops evolved to iterators:

- `multi_head.rs`: `.iter().enumerate()` for head prediction
- `multi_head.rs`: `.iter().enumerate()` + slice for pairwise disagreement
- `genomics.rs` (2 sites): `.windows(n).enumerate()` for sliding windows
- `df64_rewrite/mod.rs`: `.iter().enumerate()` for overlap detection

---

## Part 3: Capability-Based Naming Evolution

### 3.1 Function names

`submit_to_toadstool` → `submit_dispatch` — function no longer references a
specific primal; it dispatches via the `compute.dispatch` capability.

### 3.2 Provenance strings

`"Production wiring via toadStool."` → `"via compute.dispatch capability."`

### 3.3 Socket namespace constants

Hardcoded `"biomeos"` string literals → named `ECOSYSTEM_SOCKET_DIR` constants
in `transport.rs` and `barracuda.rs`. Test assertions updated to use constants.

---

## Part 4: Smart Refactoring

### 4.1 `coral_compiler/mod.rs`: 982 → 563 lines

Test module (422 lines, 37 tests) extracted to `coral_compiler_tests.rs` using
`#[path = "coral_compiler_tests.rs"]` pattern. Tests retain private field access
for connection state assertions. File now has room to grow to 1000 LOC limit.

### 4.2 `executor.rs`: 1,913 → 991 lines (from BC-04)

Extracted: `sim_buffer.rs` (101 lines), `eval.rs` (404 lines),
`executor_tests.rs` (439 lines). 29 clippy warnings fixed during extraction.

### 4.3 Showcase dependency alignment

6 showcase `Cargo.toml` files: `tokio = "1"` → `"1.50"` matching workspace pin.
(Showcases are standalone packages, not workspace members — explicit pin required.)

---

## Part 5: HCI Formula & Perlin Gaps (from prior session)

| ID | Issue | Resolution |
|----|-------|------------|
| BC-01 | Fitts returns Welford not Shannon | `variant` param, default `"shannon"` |
| BC-02 | Hick includes no-choice by default | `include_no_choice` param, default `false` |
| BC-03 | `perlin3d(0,0,0)` ≠ 0 | True 3D Perlin with gradient vectors |
| BC-04 | executor.rs clippy + 1000 LOC | Split + 29 clippy fixes |

---

## Quality Metrics

| Gate | Status |
|------|--------|
| `cargo fmt` | Clean |
| `cargo clippy -D warnings` | Zero warnings (pedantic + nursery) |
| `cargo doc -D warnings` | Clean |
| `cargo test --all-features` | 4,100+ tests, 0 failures |
| Production panics | Zero |
| Production `.unwrap()` | Zero |
| Production `.expect()` (naga-exec) | Zero |
| `#[allow(` in naga-exec | Zero |
| Files > 1000 LOC | Zero |
| Unsafe code | 1 site (barracuda-spirv, `#[expect]` with evolution path) |

---

## Cross-Primal Notes

- **All primals**: `submit_to_toadstool` renamed to `submit_dispatch` — if any
  cross-primal docs reference the old name, update them.
- **ludoSpring**: BC-01 Fitts variant param resolves 4 exp089 check failures.
  Default `"shannon"` matches ISO 9241-411 standard.
- **coralReef**: barracuda-spirv now returns `Result` from `compile_spirv_passthrough`.
  If coralReef directly called this function, update callers.
