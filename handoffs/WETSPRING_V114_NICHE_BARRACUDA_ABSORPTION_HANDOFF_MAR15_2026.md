# wetSpring V114 — Niche Setup + BarraCUDA Absorption (Global Handoff)

**Date:** 2026-03-15
**From:** wetSpring V114
**To:** biomeOS, BarraCUDA/ToadStool, All Springs
**Status:** V114 — 374 experiments, 19 capabilities, niche deployed

---

## Summary

wetSpring V114 delivers documentation cleanup, niche setup guidance, and a
comprehensive BarraCUDA absorption handoff. This positions wetSpring as a
reference implementation for springs modeling themselves as biomeOS niches.

## Changes

| Area | Detail |
|------|--------|
| Documentation | README, CHANGELOG, STUDY, baseCamp, specs all refreshed to V114 |
| Archive Cleanup | 6 superseded handoffs (V111–V113) moved to archive/ |
| Niche Guidance | 7-step checklist: UniBin → socket → capabilities → deploy graph → provenance → time series → workflow graphs |
| BarraCUDA Handoff | 8 GPU primitive opportunities: NMF, adaptive ODE, batched SW, taxonomy, phylogenetics, diversity stream, statistics, signal |
| Experiment 374 | Docs-only experiment documenting this pass |

## For BarraCUDA/ToadStool Team

Priority 1 (high impact):
1. **`SparseGemmF64`** — CSR × Dense GEMM for NMF decomposition
2. **`BatchedOdeRK4Adaptive`** — RK45 with step control for stiff kinetics systems

Priority 2 (medium impact):
3. **`SmithWatermanBatchGpu`** — Multi-pair batched alignment
4. **`KmerHashBatchGpu`** — Streaming k-mer extraction + classification

All algorithms have CPU validation tests in wetSpring that serve as ground truth
for GPU implementations. See `WETSPRING_V114_BARRACUDA_TOADSTOOL_ABSORPTION_HANDOFF_MAR15_2026.md`
in wetSpring's local wateringHole for full details.

## For All Springs

The niche setup guidance handoff provides a 7-step checklist derived from
wetSpring's implementation. Key reference files:
- `graphs/wetspring_deploy.toml` — deploy graph template
- `barracuda/src/ipc/` — IPC server + capability registration

## Quality

- 1,326 tests, 0 failures
- Zero clippy warnings (pedantic + nursery)
- Zero unsafe code
