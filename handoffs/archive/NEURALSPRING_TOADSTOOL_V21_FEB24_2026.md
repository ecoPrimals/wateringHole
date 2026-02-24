# neuralSpring → ToadStool/BarraCUDA — V21 Summary (February 24, 2026)

**Session**: 56 (ToadStool S53 Sync + Upstream Rewiring + Dispatch Expansion)
**Full handoff**: `neuralSpring/wateringHole/handoffs/NEURALSPRING_V21_SESSION56_HANDOFF_FEB24_2026.md`
**ToadStool HEAD**: `f78cf3b0`

---

## What Changed

ToadStool S53 sync + upstream rewiring + 3 new validators.

- **4 functions rewired to upstream**: `graph_laplacian`, `disordered_laplacian`,
  `belief_propagation_chain`, `numerical_hessian` → BarraCUDA `linalg::graph`
  and `numerical` modules (confirmed absorbed from Sessions 51–53 handoffs)
- **3 new validators**: `validate_basecamp_dispatch` (19), `validate_barracuda_parity`
  (34), `validate_metalforge_pcie` (36) — 89 new checks
- **metalForge PCIe tiers**: `BandwidthTier` enum, chained transfer costs,
  P2P vs staged comparison
- **Total**: 2010+ checks, 478 lib tests, 155 binaries, 0 warnings

## Absorption Candidates for BarraCUDA

### Priority 1 — Dispatcher Routing Pattern

The `gpu_or_cpu` pattern (29 methods, 89 dispatch checks) should be
generalized into BarraCUDA as a generic dispatch function/trait.

### Priority 2 — PCIe Cost Model

`BandwidthTier`, `transfer_cost_for_tier`, `chained_transfer_cost`,
`compare_transfer_paths` — generic infrastructure for device-layer routing.

### Priority 3 — baseCamp GPU Shaders

4 candidates for dedicated WGSL: symmetric matmul (W^T·W), parallel
numerical Hessian, sparse graph Laplacian, batch belief propagation GEMV.

## Key Learnings

1. **Handoff→absorb→rewire cycle proven**: 4 functions handed off, absorbed,
   rewired — zero API disruption, all tests pass
2. **f64 is non-negotiable**: graph Laplacian spectra, belief propagation
   normalization, Hessian eigenvalues all require f64
3. **PCIe x4 is 4× slower than x16**: matters for NPU routing decisions
4. **Tolerance registry scales**: 95 named constants, centralized, justified

## Validation State

| Gate | Result |
|------|--------|
| `cargo test --lib` | 478 PASS |
| `cargo clippy (pedantic+nursery)` | 0 warnings |
| `validate_all` | 155 binaries PASS |
| Paper coverage | bC 96% · gT 92% · xD 100% · dispatch 100% |
