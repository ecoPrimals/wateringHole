# coralReef Iteration 71 — Sovereign Compiler Frontend + Deep Debt Resolution

**Date**: March 30, 2026
**Primal**: coralReef
**Phase**: 11 — Sovereign Compiler Frontend
**From**: hotSpring (GPU solving pipeline)
**To**: Primal teams, Spring teams, GPU solving (hotSpring)

---

## Summary

`coral-parse` crate is now the sovereign compiler frontend for coralReef. Pure-Rust
WGSL/SPIR-V/GLSL parsers replace naga for all shader parsing. naga is now an optional
Cargo feature for diff-testing only. 28 transitive dependencies eliminated from the
default build. The lowering pass from AST to CoralIR has been fully implemented and
refactored into 6 focused submodules.

## What Changed

### New: `coral-parse` crate (sovereign frontend)

- Pure-Rust WGSL lexer + recursive-descent parser (full WGSL spec)
- Pure-Rust SPIR-V binary reader (two-pass: headers/names/decorations → types/functions)
- Pure-Rust GLSL 450/460 lexer + parser
- Sovereign AST: `Module`, `Type`, `Expression`, `Statement`, `Arena<T>`, `Handle<T>`
- AST → CoralIR lowering in 6 submodules:
  - `math.rs` — MathFunction → OpTranscendental/OpFFma/OpF2I/OpI2F
  - `binary.rs` — BinaryOp/UnaryOp → IR ops (div via rcp+mul, mod via floor-sub)
  - `convert.rs` — Expression::As → OpF2I/OpI2F/OpSel
  - `stmt.rs` — store/if/loop/atomic/switch/kill/texture store
  - `builtin.rs` — BuiltIn → OpS2R system register reads
  - `mod.rs` — FuncLowerer coordination + SSA/block management

### naga made optional

- `coral-reef` `Cargo.toml`: `naga` is now `optional = true`, default features = `[]`
- `NagaFrontend` gated behind `#[cfg(feature = "naga")]`
- `CoralFrontend` (from `coral-parse`) is the default
- Cyclic dependency resolved: `coral-reef` no longer depends on `coral-parse` directly;
  users pass a `Box<dyn Frontend>` to the compiler

### Deep debt resolved

- Production `unwrap()` in `spirv/reader.rs` and `glsl/parser.rs` → proper `Result` propagation
- Magic GLSL.std.450 opcodes → named constants (`glsl_ext::*`)
- Monolithic `lower/mod.rs` (1439 lines) → 6 submodules (2225 lines of complete implementations)
- ShaderInfo metrics computed dynamically (instr_count, barrier_count, shared_mem_size)
- Uniform load uses actual buffer binding (not hardcoded `CBuf::Binding(0)`)
- Always-true `|| true` removed from WGSL switch parser
- Unused `tracing` dependency removed from coral-parse
- WGSL parser tracks expression types for struct field resolution
- `bitcast` emits proper `Expression::As` instead of passthrough

## Test Status

| Suite | Tests | Status |
|-------|-------|--------|
| `cargo test -p coral-parse -p coral-reef --no-default-features` | 1264 | PASS (zero naga) |
| `cargo test -p coral-parse -p coral-reef --features naga` | 1999 | PASS (with naga) |
| `cargo test --workspace` | 4200+ | PASS |
| Zero regressions | — | Confirmed |

## Impact on Other Primals

### barraCuda
- WGSL shaders now compiled via `coral-parse` by default (no naga in path)
- `CoralCompiler` IPC client unchanged — API is stable
- barraCuda can depend on coralReef without pulling in naga

### toadStool
- `shader.compile.*` proxy unchanged — API is stable
- Reduced transitive dependency tree when proxying to coralReef

### hotSpring
- Sovereign pipeline now complete: WGSL → coral-parse → CoralIR → SASS
- Ready for Tesla K80 (SM35) + Titan V (SM70) hardware validation
- No external parser dependency in the compilation path

### All primals
- 28 fewer transitive dependencies in the ecosystem when using coralReef
- Same JSON-RPC 2.0 API surface — no breaking changes

## Files Modified (coralReef)

| Path | Change |
|------|--------|
| `crates/coral-parse/src/lower/mod.rs` | Refactored to coordinating module + 5 submodule dispatches |
| `crates/coral-parse/src/lower/math.rs` | New — MathFunction lowering |
| `crates/coral-parse/src/lower/binary.rs` | New — BinaryOp/UnaryOp lowering |
| `crates/coral-parse/src/lower/convert.rs` | New — type conversion lowering |
| `crates/coral-parse/src/lower/stmt.rs` | New — statement lowering |
| `crates/coral-parse/src/lower/builtin.rs` | New — BuiltIn variable lowering |
| `crates/coral-parse/src/spirv/reader.rs` | Error handling + expanded GLSL.std.450 |
| `crates/coral-parse/src/glsl/parser.rs` | Error handling for vector types |
| `crates/coral-parse/src/wgsl/parser.rs` | Type tracking, bitcast, switch fix |
| `crates/coral-parse/Cargo.toml` | Removed unused `tracing` dep |
| `crates/coral-reef/Cargo.toml` | naga → optional |
| `crates/coral-reef/src/frontend.rs` | `CoralFrontend` default, `NagaFrontend` gated |

## Next Steps (GPU Solving)

1. Tesla K80 (SM35, Kepler) — cold boot sovereign pipeline validation
2. Titan V (SM70, Volta) — VFIO dispatch with sovereign frontend
3. Full dispatch pipeline gap analysis with complete toolchain
4. Diff-testing: coral-parse output vs naga output for parity validation

---

*Sovereign compiler frontend complete. No naga. No vendor parsers. Pure Rust.*
