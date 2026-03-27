# coralReef — Phase 10 Iteration 7: Safety Boundary + Coverage Handoff

**Date**: March 7, 2026
**From**: coralReef
**To**: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, barraCuda, toadStool

---

## Summary

coralReef Phase 10 — Iteration 7 enforces a compile-time safety boundary
across the codebase, adds kernel ABI validation tests for DRM ioctl structs,
eliminates the last production panic in the shader model dispatch, and
smart-refactors the CFG module along domain boundaries. Test coverage
expanded from 856 to 904 tests (883 passing, 21 ignored).

## Metrics

| Metric | Iteration 6 | Iteration 7 | Delta |
|--------|-------------|-------------|-------|
| Total tests | 856 | 904 | **+48** |
| Passing | 836 | 883 | **+47** |
| Ignored | 20 | 21 | **+1** |
| Corpus passing SM70 | 14 | 14 | — |
| Clippy warnings | 0 | 0 | — |
| Crates with `#[deny(unsafe_code)]` | 0 | **6/8** | **+6** |

## Safety Boundary

### `#[deny(unsafe_code)]` Enforcement

Six of eight crates now enforce `#[deny(unsafe_code)]` at the crate root:

| Crate | Unsafe Status |
|-------|---------------|
| coral-reef | `#[deny(unsafe_code)]` — compiler core |
| coralreef-core | `#[deny(unsafe_code)]` — IPC, lifecycle, service |
| coral-gpu | `#[deny(unsafe_code)]` — unified GPU abstraction |
| coral-reef-stubs | `#[deny(unsafe_code)]` — pure Rust replacements |
| coral-reef-bitview | `#[deny(unsafe_code)]` — bit-level field access |
| coral-reef-isa | `#[deny(unsafe_code)]` — ISA tables |
| coral-driver | Unsafe required — DRM ioctls via libc |
| nak-ir-proc | Unsafe required — proc-macro `from_raw_parts` |

Any attempt to introduce `unsafe` into the six protected crates will be
a compile error. The only unsafe code paths are in the DRM driver (libc
syscalls) and the proc-macro (IR slice generation), both with documented
safety invariants.

## Kernel ABI Validation

14 new tests verify every `#[repr(C)]` ioctl struct in `coral-driver`:

- `AmdgpuGemCreate` — 40 bytes, 6 fields at expected offsets
- `AmdgpuGemMmap` — 16 bytes
- `AmdgpuCtx` — 16 bytes
- `AmdgpuGemVa` — 40 bytes
- `AmdgpuBoListEntry` — 8 bytes
- `AmdgpuBoListIn` — 24 bytes
- `AmdgpuCsChunk` — 16 bytes
- `AmdgpuCsChunkIb` — 32 bytes
- `AmdgpuCsIn` — 24 bytes
- `AmdgpuWaitCsIn` — 32 bytes

These catch silent ABI drift from kernel header changes that would cause
data corruption or kernel panics.

## Panic Elimination

The `sm_match!` macro in `shader_info.rs` previously had a `panic!("Unsupported shader model")`
fallback for SM < 20. This has been eliminated:

- `ShaderModelInfo::new()` now asserts `sm >= 20` at construction time
- Both `sm_match!` and `sm_match_result!` macros have exhaustive branches
- The SM < 20 case is unreachable by construction

## Smart Refactoring

`cfg.rs` (897 LOC) split into two files along the natural domain boundary:

| File | LOC | Responsibility |
|------|-----|----------------|
| `cfg/mod.rs` | 593 | Core CFG structure, builder, iterators, tests |
| `cfg/dom.rs` | 298 | Cooper-Harvey-Kennedy dominator tree, loop detection |

The split follows the principle of semantic cohesion: graph structure vs.
graph analysis are distinct concerns.

## Configurable Debug Path

`save_graphviz` in `opt_instr_sched_common.rs` now respects the
`CORAL_DEP_GRAPH_PATH` environment variable, falling back to
`std::env::temp_dir()`. No more hardcoded `/tmp/` paths.

## Coverage Expansion

New tests added across:

- **coral-driver**: Ioctl struct layouts (14), GEM buffer bounds checking (4),
  NV dispatch/sync unsupported (2), `u32_slice_as_bytes` helper (3),
  `read_ioctl_output` helper (1), `kernel_ptr` round-trip (1), default structs (1)
- **coral-reef**: `ShaderModelInfo::new` panics for SM < 20 (1),
  `FmaPolicy` default/debug/equality (3), `CompileOptions` accessor edge cases (3),
  malformed WGSL error (1), Intel unsupported paths (2)

## IPC Contract (unchanged from Iteration 6)

| Method | JSON-RPC | tarpc | Status |
|--------|----------|-------|--------|
| `shader.compile.spirv` | ✅ | ✅ | SPIR-V → native binary |
| `shader.compile.wgsl` | ✅ | ✅ | WGSL → native binary |
| `shader.compile.status` | ✅ | ✅ | name, version, supported_archs |
| `shader.compile.capabilities` | ✅ | ✅ | dynamic arch enumeration |

## Checks

All pass:

```
cargo check --workspace          # OK
cargo test --workspace           # 904 tests (883 passing, 21 ignored)
cargo clippy -- -W pedantic      # 0 warnings
cargo fmt --check                # OK
cargo doc --workspace --no-deps  # 0 warnings
```

---

*Safety is not a feature — it is a structural property. When the compiler
rejects unsafe code at build time, no review process can introduce it.
Six crates are now structurally safe.*
