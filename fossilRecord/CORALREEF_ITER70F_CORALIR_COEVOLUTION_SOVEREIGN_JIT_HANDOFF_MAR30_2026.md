# coralReef Iteration 70f — CoralIR Coevolution + Sovereign JIT + Progressive Trust

**Date**: March 30, 2026  
**Primal**: coralReef  
**Iteration**: 70f (Phase 10+)  
**Previous**: 70e (Cranelift JIT Backend + Dual-Path Validation)

---

## Summary

Four-phase CoralIR coevolution plan executed in a single session:

1. **CoralIR reference interpreter** — direct evaluation of CoralIR `Op` instructions
   in `coral-reef-cpu`, acting as a trusted oracle for JIT validation
2. **Triple-path test infrastructure** — every shader test runs through JIT, CoralIR
   interpreter, and Naga interpreter (best-effort), comparing within tolerance
3. **Sovereign JIT runtime** — `rustix` mmap/mprotect replaces `cranelift-jit`'s
   `region`/`wasmtime-jit-icache-coherence` dependency chain; `libm` for
   transcendentals replaces libc math functions
4. **Progressive trust model** — `ExecutionStrategy` enum (Interpret/Jit/ValidatedJit)
   with `JitCache` for compiled kernel caching and periodic re-validation

Additionally: workspace dependency consolidation — all 13 crate manifests migrated
to `{ workspace = true }`, codified as `WORKSPACE_DEPENDENCY_STANDARD.md` in
wateringHole.

---

## What Changed

### New Files

| File | Purpose |
|------|---------|
| `coral-reef-cpu/src/coral_ir_exec/mod.rs` | CoralIR interpreter: `execute_coral_ir()`, `RegValue` enum, `InvocationCtx`, synthetic buffer addressing |
| `coral-reef-cpu/src/coral_ir_exec/eval_ops.rs` | Arithmetic/transcendental evaluation helpers (`float_cmp`, `int_cmp`, `eval_transcendental`) |
| `coral-reef-jit/src/runtime.rs` | `JitMemory` allocator: `rustix` mmap/mprotect/munmap, aarch64 icache flush |
| `coral-reef-jit/src/sovereign.rs` | Sovereign compilation: `cranelift-codegen` direct + `libm` relocation patching |
| `coral-reef-jit/src/cache.rs` | `JitCache`: thread-safe compiled kernel cache with `RevalidationPolicy` |
| `wateringHole/WORKSPACE_DEPENDENCY_STANDARD.md` | Ecosystem standard for workspace-level dependency management |

### Modified Files (key changes)

| File | Change |
|------|--------|
| `coral-reef-cpu/src/types.rs` | Added `ExecutionStrategy` enum, extended `ExecuteCpuResponse` with `strategy_used`, `cache_hit`, `revalidated` |
| `coral-reef-jit/src/lib.rs` | Split `execute_jit` into `compile_to_kernel` + `execute_kernel` for cache integration |
| `coral-reef-jit/src/translate.rs` | `CompiledBacking` simplified to Sovereign-only, `LibmResolver` unified, removed `Result` from libm helpers |
| `coralreef-core/src/service/cpu.rs` | Strategy dispatch: `Interpret`/`Jit`/`ValidatedJit` with `JIT_CACHE` static, re-validation logic |
| `coral-reef-jit/tests/jit_validation.rs` | Triple-path helpers: `assert_triple_path_f32`/`u32` |
| Root `Cargo.toml` | 15 new workspace dependencies (naga, bytemuck, toml, base64, tempfile, criterion, syn, proc-macro2, quote, etc.) + 4 internal path crates |
| 13 crate `Cargo.toml` files | All inline version pins → `{ workspace = true }` |

### Dependency Eliminations

| Eliminated | Replaced By |
|-----------|-------------|
| `cranelift-jit` runtime path | `cranelift-codegen` direct + `runtime.rs` (`rustix` mmap) |
| `region` crate (via cranelift-jit) | `rustix::mm::mprotect` |
| `wasmtime-jit-icache-coherence` (via cranelift-jit) | Inline asm icache flush (aarch64) / no-op (x86-64) |
| `libc` libm functions (for JIT) | `libm` crate (pure Rust) |
| Per-crate inline version pins | Workspace `{ workspace = true }` |

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo test --workspace` | PASS (4070+ passing, ~122 ignored) |
| `cargo clippy --workspace -- -D warnings` | PASS (pre-existing coral-driver missing-docs only) |
| `cargo fmt --check` | PASS |
| `cargo tree --duplicates` | Clean (only ecosystem-caused bitflags v1/v2) |
| All production files < 1000 LOC | PASS |

---

## Architecture: Progressive Trust Model

```
shader.execute.cpu request
         │
         ├─ strategy = Interpret
         │    └─ CoralIR interpreter (reference, always correct)
         │
         ├─ strategy = Jit
         │    └─ Sovereign JIT (fast, compiled, cached)
         │
         └─ strategy = ValidatedJit
              ├─ First call: interpret + validate → JIT compile → cache
              ├─ Subsequent: cache hit → execute compiled kernel
              └─ Periodic: re-validate cached kernel against interpreter
```

The `ValidatedJit` path implements "trust but verify": interpret first to
establish correctness, then compile and cache for speed, with configurable
re-validation intervals to detect drift.

---

## Known Limitations

- **Local scratch memory**: CoralIR interpreter and JIT do not yet emulate
  `var<workgroup>` or `var<function>` scratch — blocks `for` loop patterns
- **Naga interpreter**: Best-effort comparison; some shaders fail Naga
  interpretation while passing CoralIR interpreter and JIT
- `cranelift-jit` crate remains in `Cargo.toml` workspace dependencies
  (transitive through test builds) even though the sovereign pipeline
  bypasses it at runtime

---

## Handoff Context

This iteration completes the "CoralIR Interpreter/JIT Coevolution + libc
Elimination" plan discussed in the prior session. The four phases were
executed sequentially with all quality gates passing after each phase.

The workspace dependency standard was created in response to discovering
inline version pins across 13 crate manifests — now consolidated per
the new `WORKSPACE_DEPENDENCY_STANDARD.md` in wateringHole.

**Next priorities**: local scratch memory for JIT loops, MmioRegion safe
RAII wrapper, coverage push toward 90%.
