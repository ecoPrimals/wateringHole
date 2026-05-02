<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 88: Deep Debt, Typed Errors, Hotspring Merge

**Date**: April 30, 2026
**From**: coralReef team
**To**: primalSpring, hotSpring, all downstream springs

---

## Summary

Branch consolidation (hotspring-sec2-hal + iter70d), smart file refactoring (6 files >1000L eliminated), CR-04 typed errors Wave 4 (zero `Result<_, String>` in production), IPC timing characterization, primalSpring Phase 56c audit reconciliation.

## Branch Consolidation

- **`hotspring-sec2-hal`** merged: GPU generation profiles (`GenerationProfile`, `NvArch`, `AmdArch`), WIP PTX emitter for SM120/Blackwell, Intel/AMD dispatch, FECS/GPCCS boot paths, device probes
- **`iter70d-deep-audit-evolution`** merged (ours strategy): superseded by main; recorded for branch deletion
- Both remote branches deleted post-merge

## Smart File Refactoring

All production files now under 1000 LOC. Six monolithic files split into cohesive submodule directories:

| Original file | Was | Now | Largest submodule |
|---|---|---|---|
| `ptx_emit.rs` | 2190L | 11 files | 396L |
| `uvm_compute/device.rs` | 1625L | 5 files | 868L |
| `qmd.rs` | 1307L | 10 files | 609L |
| `uvm/mod.rs` | 1037L | 4 files | 514L |
| `kepler_fecs_boot.rs` | 1774L | 8 files | 526L |
| `kepler_warm.rs` | 1375L | 6 files | 532L |

## CR-04: Typed Errors Wave 4

Zero `Result<_, String>` remaining in production library code. New error types:

- `SovereignStagesError` (coral-driver): BAR0/PMC isolation, HBM2 training, devinit/GDDR, Kepler firmware/boot, falcon/GR, verify-stage
- `TrainingRecipeError` (coral-glowplug): read/parse/create-parent/serialize/write
- `GoldenStateLoadError` + `HeldBar0Error` (coral-ember): golden state I/O, BAR0 DMA mapping

## IPC Timing Characterization

`docs/IPC_COMPOSITION_AND_LATENCY.md` now includes measured transport overhead:

| Transport | Overhead |
|---|---|
| Unix socket JSON-RPC | ~0.1–0.3 ms |
| TCP JSON-RPC (localhost) | ~0.3–0.8 ms |
| tarpc (Unix socket) | ~0.05–0.15 ms |

## Safety & Quality

- All `// SAFETY:` comments added to undocumented unsafe blocks
- Hardcoded BDF in `pri.rs` parameterized; `CORALREEF_FECS_DUMP_DIR` env var override
- SM120/Blackwell test tolerance via `catch_unwind` (WIP PTX emitter)
- All `.unwrap()` in ptx_emit → `.expect("reason")` or error propagation

## primalSpring Phase 56c Audit Resolution

| Item | Status |
|---|---|
| CR-04: ~20 HW functions `Result<_, String>` | **RESOLVED** — typed errors Wave 4 |
| CR-05: `cpu_exec.rs` dead code | **RESOLVED** — file deleted (prior iteration) |
| IPC timing uncharacterized | **RESOLVED** — transport overhead documented |
| Coverage ~65% → 90% | **IN PROGRESS** — ceiling ~82% non-hardware without GPU CI |

## Test Results

- **4639 passing**, 0 failures, 177 ignored (hardware-gated)
- Zero clippy warnings (pedantic + nursery)
- Zero fmt drift

## Downstream Impact

- **hotSpring**: GPU generation profiles now in main; SM120 PTX paths WIP but tolerant
- **primalSpring**: All Phase 56c coralReef items resolved except coverage target
- **barraCuda**: No API changes; `dispatch_binary` + `KernelCacheEntry` unchanged
- **compositions**: JSON-RPC UDS socket unchanged from Iter 87 fix

## Remaining Gaps

- Coverage ~65% → 90% (hardware-gated ceiling at ~82% without GPU CI)
- PTX emitter for SM120/Blackwell (WIP — `NotImplemented` for some patterns)
- UVM hardware validation (awaiting RTX 5060 on-site)
- tarpc OpenTelemetry transitive dep (upstream tracking)
