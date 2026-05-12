<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Sprint 4: PTX SM120 Evolution + Coverage Push

**Date**: May 12, 2026
**From**: coralReef
**Context**: Compute Trio Evolution Sprint 4 — Phase C Execution + Convergence

---

## Summary

PTX emitter evolved for SM120/Blackwell readiness: subgroup inclusive/exclusive prefix scans implemented via `shfl.sync.up` butterfly accumulation, silent statement catch-all replaced with explicit error reporting, and expression evaluator extended for subgroup operation results. `coral-reef-isa` API expanded with `IsaTarget` methods and `Hash` derive. Coverage pushed to 4784 tests (+19).

## Changes

### PTX Emitter — Subgroup Scans (`statements.rs`)

- **Inclusive scan**: 5-iteration `shfl.sync.up.b32` butterfly with predicated accumulation
- **Exclusive scan**: Same as inclusive + lane shift via `selp` with type-appropriate identity element
- Supports all naga `SubgroupOperation` variants: Add, Mul, Min, Max, And, Or, Xor
- Identity elements: 0 (add/or/xor), 1 (mul), all-ones (and), +/-inf (min/max float), INT_MAX/INT_MIN (min/max int)

### PTX Emitter — Silent Catch-All Eliminated (`statements.rs`)

- `_ => Ok(())` replaced with exhaustive match
- `ImageStore`, `ImageAtomic`, `Call`, `RayQuery`, `WorkGroupUniformLoad` now return `CompileError::NotImplemented`
- Prevents silent code generation bugs when new naga statement types are added

### PTX Expression Evaluator (`expr_eval.rs`)

- `SubgroupOperationResult`: Pre-allocates typed register matching the result scalar type
- `SubgroupBallotResult`: Pre-allocates u32 register for ballot mask

### coral-reef-isa (`lib.rs`, `latency.rs`, `sph.rs`)

- `IsaTarget`: Added `Hash` derive, `ALL` constant, `sm_version()`, `has_independent_thread_scheduling()`, `has_uniform_datapath()`
- Latency and SPH test coverage expanded (edge cases, max values, format validation)

## Quality Gates

- `cargo clippy --all-features -- -D warnings`: **0 warnings**
- `cargo test --all-features`: **4784 passed, 0 failed, 181 ignored**
- `cargo fmt -- --check`: **clean**

## Coordination

### QMD Split Boundary (Phase C)

Already documented in `coral-driver/src/nv/qmd/mod.rs` header:
- **toadStool absorbs**: QMD encoding (bitfield packing, version dispatch)
- **coralReef provides**: Values via `CompilationInfo` (gpr_count, shared_mem_bytes, barrier_count, local_size, local_mem_bytes)

### Remaining (blocked on hardware or external)

- **PTX texture/surface instructions**: Requires naga `Image`/`Sampler` compute support; medium-term
- **UVM hardware validation**: Code-complete for RTX 5060, needs on-site hardware
- **Falcon boot FBP=0**: Three parallel paths active (system-memory WPR, hybrid WPR, Nouveau warm handoff)
- **Phase C/D IPC cutover**: Waiting on toadStool Phase C completion

### Downstream

- ludoSpring GAP-01 (sovereign compile) and hotSpring cold-boot path both reference "SM rebuild" — the compiler pipeline is operational; these unblock when the full E2E dispatch path is wired (Phase D)

---

*Supersedes: CORALREEF_SPRINT3_CLEANUP_ICE_CONSISTENCY_MAY12_2026.md (archived)*
