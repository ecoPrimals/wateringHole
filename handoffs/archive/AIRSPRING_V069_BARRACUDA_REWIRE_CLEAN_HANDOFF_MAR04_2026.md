<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# airSpring V0.6.9 — BarraCuda Rewire & Clean Handoff

**Date**: March 4, 2026
**From**: airSpring V0.6.9 (ecology/agriculture validation Spring)
**To**: ToadStool S93+ / barraCuda 0.3.1+ / All Springs
**License**: AGPL-3.0-or-later

---

## Summary

airSpring completed a comprehensive nomenclature and provenance rewire to reflect
the post-S89 architecture: **barraCuda is the standalone sovereign math engine**,
ToadStool is the hardware dispatch layer.

- **~200 references** rewired across **~55 files** in `barracuda/` and `metalForge/`
- **Structural renames**: `toadstool_primitive` → `barracuda_primitive`,
  `ToadStoolIssue` → `BarraCudaIssue`, `TOADSTOOL_ISSUES` → `BARRACUDA_ISSUES`
- **Doc-comment sweep**: All references to ToadStool as the math/shader engine → BarraCuda
- **Preserved**: ToadStool references in NUCLEUS mesh (hardware dispatch), deployment
  graphs, and historical session context
- **1132/1132 tests pass**, 0 clippy warnings (pedantic+nursery), 0 fmt diffs, docs clean

---

## Changes Made

### 1. Structural API Renames (`evolution_gaps.rs`)

| Before | After | Scope |
|--------|-------|-------|
| `toadstool_primitive: Option<&str>` | `barracuda_primitive: Option<&str>` | `EvolutionGap` struct field |
| `ToadStoolIssue` struct | `BarraCudaIssue` struct | Public type |
| `TOADSTOOL_ISSUES` const | `BARRACUDA_ISSUES` const | Public constant |
| `IssueStatus` "resolved in ToadStool" | "resolved in BarraCuda" | Doc-comment |
| Tier C: "Needs New ToadStool" | "Needs New BarraCuda" | Enum variant doc |

### 2. GPU Module Doc-Comments (25 files)

All `gpu/*.rs` modules updated: `ToadStool` → `BarraCuda` where referring to the
math engine, shader provider, or compute primitives. Session numbers (S70+, S79, etc.)
preserved as historical markers.

Key files: `mod.rs`, `device_info.rs`, `hargreaves.rs`, `kc_climate.rs`, `dual_kc.rs`,
`sensor_calibration.rs`, `atlas_stream.rs`, `stream.rs`, `runoff.rs`, `local_dispatch.rs`,
`et0.rs`, `kriging.rs`, `reduce.rs`, plus 12 others.

### 3. Validation Binaries (15 files)

Updated provenance strings, banners, and doc-comments in:
- `bench_cross_spring/main.rs` (14 refs)
- `validate_cross_spring_provenance.rs` (11 refs)
- `validate_gpu_rewire_benchmark.rs` (7 refs)
- `validate_biome_graph.rs` (4 refs + code: `toadstool_primitive` → `barracuda_primitive`)
- Plus 11 other binaries (1-3 refs each)

**Exception kept**: `validate_nucleus_pipeline.rs` — "Cross-primal forwarding:
airSpring → `ToadStool` health" is correct (ToadStool as hardware dispatch target).

### 4. Domain Modules (8 files)

`eco/crop.rs`, `eco/evapotranspiration.rs`, `eco/richards.rs`, `eco/correction.rs`,
`eco/diversity.rs`, `tolerances.rs`, `testutil/stats.rs`, `npu/mod.rs` —
all ToadStool-as-math-engine references → BarraCuda.

### 5. Tests (8 files)

- `tests/gpu_evolution.rs`: `TOADSTOOL_ISSUES` → `BARRACUDA_ISSUES`,
  `toadstool_primitive` → `barracuda_primitive`, test names updated
- 7 other test files: doc-comment and assertion message updates

### 6. metalForge (4 files)

- `workloads.rs`: `ShaderOrigin::Absorbed` docs, section headers, primitive docs
- `validate_nucleus_routing.rs`: "absorbed by ToadStool" → "absorbed by BarraCuda"
- Preserved: `nucleus.rs` and `deploy/*.toml` ToadStool references (hardware dispatch)

### 7. EVOLUTION_READINESS.md

- "ToadStool op pending" → "BarraCuda f64 op pending" (3 Tier A entries)
- Section header updated to "BarraCuda (ToadStool S42–S68+) Evolution"
- Historical handoff references preserved

### 8. Shader Comments

- `local_elementwise.wgsl`: "ToadStool absorption" → "BarraCuda absorption"

---

## Remaining ToadStool References (Intentional)

| File | Count | Reason |
|------|:-----:|--------|
| `evolution_gaps.rs` | 4 | Historical: "`ToadStool` S42–S87", "extracted from `ToadStool`" |
| `validate_nucleus_pipeline.rs` | 1 | Cross-primal forwarding TO ToadStool (hardware dispatch) |
| `nucleus.rs` | 2 | NUCLEUS mesh: "Tower + `ToadStool` (compute/GPU)" — dispatch layer |
| `deploy/airspring_deploy.toml` | 4 | Deployment graph: ToadStool as compute dispatch primal |
| `ABSORPTION_MANIFEST.md` | 5 | Historical absorption context |
| `README.md` (metalForge) | 2 | Historical absorption context |
| `validate_nucleus_routing.rs` | 1 | "Tower + `ToadStool` (compute/GPU dispatch)" |
| `EVOLUTION_READINESS.md` | ~12 | Historical session sync notes |

---

## Naming Convention (Post-Rewire)

| Context | Use |
|---------|-----|
| Math engine, shader provider, ops, stats | **BarraCuda** |
| Hardware dispatch, multi-framework routing | **ToadStool** |
| Historical session references (S42–S87) | Session number + context |
| Deployment graph, NUCLEUS mesh | **ToadStool** (dispatch layer) |
| Struct fields, public API | `barracuda_*` (not `toadstool_*`) |

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --check` (both crates) | **0 diffs** |
| `cargo clippy --all-targets -W pedantic -W nursery -D warnings` (both crates) | **0 warnings** |
| `cargo doc --no-deps` | **0 warnings** |
| `cargo test` (barracuda) | **1132 passed**, 0 failed |
| `cargo test` (metalForge) | **62 passed**, 0 failed |
| `#![forbid(unsafe_code)]` | Both crates |
| All files < 1000 LOC | Yes |
| barraCuda version | **0.3.1** standalone |

---

## Architecture Alignment (Post-Rewire)

```
Springs (airSpring, hotSpring, wetSpring, groundSpring, neuralSpring)
    │
    ▼
BarraCuda ── "WHAT to compute"
    │           Pure math: linalg, special, numerical, spectral, stats, sample
    │           GPU math: ops (767 WGSL), tensor, pipeline, dispatch
    │           Precision: compile_shader_universal → F16/F32/F64/DF64
    │
    ▼
ToadStool ── "WHERE and HOW"
    │           Multi-framework: Vulkan, Metal, DirectX, WebGPU
    │           Orchestration: substrate selection, load balancing, fallback
    │           Distribution: multi-node via SongBird
```

airSpring's code now correctly reflects this architecture:
- All math/shader references → BarraCuda
- All hardware dispatch references → ToadStool
- Public API types use `barracuda_*` naming

---

## For Other Springs

When rewiring from ToadStool-embedded barracuda to standalone BarraCuda:

1. **Cargo.toml path swap** (zero code changes)
2. **Rename `to_toadstool()` → `to_barracuda()`** if any such methods exist
3. **Sweep doc-comments**: `ToadStool` → `BarraCuda` for math engine references
4. **Rename public types/fields**: `toadstool_*` → `barracuda_*`
5. **Keep ToadStool** for hardware dispatch layer references
6. **Backtick** all primal names in doc-comments (`clippy::doc_markdown`)
7. Run full quality gate: fmt + clippy (pedantic+nursery) + test + doc
