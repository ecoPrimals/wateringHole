# coralReef v0.2.0 — Phase 5 Complete Handoff

**Date**: 2026-03-05
**From**: coralReef (formerly coralNak)
**Status**: Phase 5 Complete — sovereign Rust NVIDIA shader compiler

## Summary

coralReef is the sovereign Rust NVIDIA shader compiler. All core phases (1–5)
are complete. The project was renamed from coralNak → coralReef. The internal
NAK IR architecture name is retained.

## Completed Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Mesa C FFI removal, pure Rust crate | Complete |
| 1.5 | JSON-RPC 2.0 + tarpc IPC, primal lifecycle | Complete |
| 2 | NAK sources wired, workspace compiles clean | Complete |
| 3 | naga frontend (`from_spirv`): WGSL → naga → NAK IR | Complete |
| 4 | f64 transcendental lowering (sqrt, rcp, exp2, log2, sin, cos) | Complete |
| 4.5 | Error safety: production panic → Result propagation | Complete |
| 5 | Standalone: 1000 LOC compliance, test coverage, doc cleanup | Complete |

## Pipeline

```
WGSL → naga (frontend IR) → from_spirv → NAK IR → optimize → lower_f64
  → legalize → assign_regs → encode (SM20–SM120) → native binary
```

## f64 Lowering Precision

| Function | Method | Target ULP |
|----------|--------|------------|
| sqrt | MUFU.RSQ64H + 2× Newton-Raphson DFMA | ≤ 1 |
| rcp | MUFU.RCP64H + 2× Newton-Raphson DFMA | ≤ 1 |
| exp2 | Horner polynomial + integer/fraction range reduction + ldexp | ≤ 2 |
| log2 | MUFU.LOG2 seed + Newton refinement (MUFU.EX2/RCP) | ≤ 2 |
| sin | Cody-Waite reduction + minimax polynomial + quadrant correction | ≤ 4 |
| cos | Cody-Waite reduction + minimax polynomial + quadrant correction | ≤ 4 |

## Test Coverage

- **390 tests**, 0 failures
- Unit tests: IR, builder, optimizer passes, f64 lowering, from_spirv, stubs
- Integration tests: E2E WGSL → binary for compute/vertex/fragment, cross-arch
- Coverage: 37.1% line, 44.9% function (structural floor from encoder tables)

## IPC

- JSON-RPC 2.0 + tarpc, Unix socket + TCP
- Zero-copy `bytes::Bytes` for compiled binary payloads
- Capability-based self-description (no hardcoded primal names)

## Spring Absorption (this session)

- **groundSpring**: BTreeMap for deterministic serialization (from V73 tolerance arch)
- **groundSpring**: Silent-default audit (from V76 "silent defaults are bugs")
- **groundSpring**: Cross-spring provenance doc-comments on f64 lowering
- **groundSpring**: Unsafe code eliminated (builder `unwrap_unchecked` → safe)
- **groundSpring**: Capability-based discovery verified (zero hardcoded primal names)

## Corrections to Spring Handoffs

Several spring handoffs reference coralNAK as "Phase 2 with 17 compile errors".
This is outdated. Current status:

- **0 compile errors**, 390 tests pass
- Phase 5 complete, not Phase 2
- Renamed to coralReef (crate: `coral-reef`)
- GitHub: `ecoPrimals/coralReef`

## What coralReef Needs from Springs

| Need | Source Spring | Priority |
|------|--------------|----------|
| Yukawa/Verlet WGSL shaders for validation | hotSpring | P1 |
| `f64_builtin_test` for precision validation | hotSpring/barraCuda | P1 |
| naga 28 migration patterns | wetSpring/neuralSpring | P2 |
| Fused op WGSL shaders for encoder testing | wetSpring/groundSpring | P2 |
| Level 4 coordination (coralDriver) | groundSpring | P3 |

## What coralReef Provides to Springs

- Native NVIDIA binary compilation from WGSL (via naga)
- f64 transcendental codegen (sqrt, rcp, exp2, log2, sin, cos)
- SM70–SM120 instruction encoding
- Future: direct naga → coralReef path (skip SPIR-V serialization)
- Future: coralDriver for NVK-free GPU execution

## Repository

- **GitHub**: `ecoPrimals/coralReef`
- **Crates**: `coral-reef`, `coralreef-core`, `coral-reef-isa`, `coral-reef-stubs`, `nak-ir-proc`, `bitview`
- **License**: AGPL-3.0-only (NAK-derived files retain MIT)
