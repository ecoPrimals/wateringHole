<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 73: Logic/IO Untangling + Test Consolidation Handoff

**Date**: April 4, 2026
**Primal**: coralReef
**Iteration**: 73
**Phase**: 10 — Deep Debt: Logic/IO Separation Architecture + Pure Logic Extraction

---

## Summary

Iteration 73 established the architectural foundation for separating pure logic from
hardware I/O across the entire coralReef workspace. An exhaustive audit identified
~70 entangled functions (~4,800 lines) mixing computation with I/O, categorized them
into five repeating patterns, and mapped three clean separation strategies. Pure logic
extractions began across coral-driver, and large test files were consolidated below
1000 LOC.

## Architectural Plan

Five entanglement patterns identified across the workspace:

| Pattern | Description | Strategy |
|---------|-------------|----------|
| A: read-mask-write | Read register, compute mask, write back | Snapshot + Interpret |
| B: poll/retry loop | Read register in loop, check condition | Plan + Execute |
| C: build then flush | Compute data structure, write to hardware | Plan + Execute |
| D: read chain | Read multiple registers, interpret | Snapshot + Interpret |
| E: deep interleave | Computation and I/O interleaved throughout | Ports and Adapters |

Target modules: coral-driver (~45 functions, ~3,200 lines), coral-ember (~15, ~900),
coral-glowplug (~8, ~400), coralreef-core (~4, ~200), coral-gpu (~4, ~150).

Plan defined core abstractions: `trait Bar0` (BAR0 register access), `trait SysfsPort`
(filesystem I/O), and snapshot types (VoltaProbeSnapshot, PfifoSnapshot, MmuFaultSnapshot,
WarmFalconSnapshot, DynamicGrInitPlan) for pure interpretation of hardware state.

## What Changed

### Pure Logic Extractions (coral-driver)

| New File | What It Contains |
|----------|-----------------|
| `acr_boot/strategy_sysmem/acr_buffer_layout.rs` | `AcrBufferLayout` (pure IOVA/size planning) + `Sec2PollState` (pure poll logic) |
| `acr_boot/strategy_sysmem/sysmem_decode.rs` | `decode_wpr_status` + `is_acr_success` (pure byte interpretation) |
| `acr_boot/strategy_sysmem/sysmem_vram.rs` | VRAM strategy operations separated from sysmem |
| `nv/vfio_compute/init_plan.rs` | `DynamicGrInitPlan`, `WarmRestartDecision`, `fecs_init_methods` (all pure) |
| `vfio/channel/channel_layout.rs` | `ChannelLayout::compute` (pure channel IOVA planning) |
| `vfio/pci_config.rs` | PCI config space operations |
| `acr_boot/sec2_hal/tests.rs` | SEC2 HAL tests extracted |
| `nv/uvm_compute_tests.rs` | UVM compute pure function tests |

### Test File Consolidation

| Before | After | Rationale |
|--------|-------|-----------|
| `opt_copy_prop/tests.rs` (973 lines) | `opt_copy_prop/tests/` (mod + part_a + part_b) | Under 1000 LOC per file |
| `spill_values/tests.rs` (979 lines) | `spill_values/tests/` (mod + cases_a + cases_b + fixtures) | Under 1000 LOC per file |
| `codegen_coverage_saturation.rs` (982 lines) | 3 parts + shared `codegen_sat/helpers.rs` | Under 1000 LOC per file |

### Other

- `cmd_compile.rs` test uses `tempfile::tempdir()` for isolation (no fixed /tmp paths)
- Pure logic extractions in coral-glowplug: boot safety, health decisions, config classification
- Startup decomposition + reset plan + lifecycle steps in coral-ember

## Metrics

| Metric | Iter 72 | Iter 73 |
|--------|---------|---------|
| Tests passing | 4269 | **4318** |
| Tests ignored | 153 | 153 |
| Clippy warnings | 0 | 0 |
| Files > 1000 LOC | 0 | 0 |
| TODO/FIXME/HACK | 0 | 0 |
| Total Rust LOC | ~100K | ~72K crates (238K incl. generated) |

## Remaining Work

1. **Bar0 trait migration** — define `trait Bar0` and migrate ~47 files from `&MappedBar` to `&dyn Bar0`
2. **SysfsPort trait migration** — define `trait SysfsPort` and migrate coral-ember sysfs operations
3. **Snapshot + Interpret** pattern for nv_metal, mmu_fault, pfifo
4. **Plan + Execute** for ACR boot, PFIFO init, channel creation
5. **Phase 3-4** — coral-ember/glowplug/core/gpu untangling
6. **Coverage push** — pure logic unlocks testing of ~4,800 previously entangled lines

## Cross-Primal Notes

- **barraCuda**: Kernel cache dispatch path unchanged; pure logic extraction improves testability of GPU dispatch path
- **hotSpring**: RingMeta and firmware mailbox interfaces unaffected; coral-ember startup decomposition enables testing of device hold planning
- **toadStool**: No changes to IPC protocol or capability registration

---

**Previous handoff**: [Iter 72 — GPU-Agnostic Evolution](CORALREEF_ITER72_GPU_AGNOSTIC_EVOLUTION_HANDOFF_APR04_2026.md)
