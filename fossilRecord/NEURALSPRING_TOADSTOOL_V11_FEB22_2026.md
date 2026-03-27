# neuralSpring → ToadStool / BarraCUDA V11 Handoff

**Date:** February 22, 2026 (Session 42 — deep audit + ToadStool sync)
**From:** neuralSpring (ML validation & evolutionary computation)
**To:** ToadStool / BarraCUDA core team
**License:** AGPL-3.0-or-later
**Full handoff:** `neuralSpring/wateringHole/handoffs/NEURALSPRING_V11_TOADSTOOL_BARRACUDA_HANDOFF_FEB22_2026.md`
**Supersedes:** V10 (deep audit only)

---

## What's New (Session 42 — ToadStool Sync)

Session 42 both performed a comprehensive code quality audit **and** synced
neuralSpring to ToadStool HEAD `5437c170` (10 commits since `d45fdfb3`).

### ToadStool Evolution Acknowledged (d45fdfb3 → 5437c170)

| Session | Key Changes |
|---------|-------------|
| S39 | Spring shader absorption (7 bio + 11 HFB + 3 wetSpring WGSL), S-14/S-15/S-16 fixes, `FlatTree`, `sparse_eigh` |
| S40 | Richards PDE solver, moving window GPU stats |
| S41 | `cpu_conv_pool` made pub, 6 f64 shader compile fixes, API exposure for Springs |
| S42 | 19 new WGSL shaders (chi2, rk45, factorial, spline, etc.), BarraCUDA → BarraCuda doc rename |

### Newly Available Wrapper APIs

| API | Domain | Replaces Local |
|-----|--------|----------------|
| `ops::bio::HillGateGpu` | Signal integration (021) | `hill_gate.wgsl` dispatch |
| `ops::bio::MultiObjFitnessGpu` | Directed evolution (014) | `multi_obj_fitness.wgsl` dispatch |
| `ops::bio::PairwiseL2Gpu` | MODES (012) | `pairwise_l2.wgsl` dispatch |
| `ops::bio::SwarmNnGpu` | Swarm robotics (015) | `swarm_nn_forward.wgsl` dispatch |
| `cpu_conv_pool::conv2d/max_pool2d` | LeNet-5 (Study 003) | Full conv+pool bC path |

### Code Quality (Deep Audit)

| Gate | Result |
|------|--------|
| `cargo fmt` | 0 violations (was 33) |
| `cargo clippy` (pedantic+nursery+unwrap_used+expect_used) | 0 warnings (was 123) |
| `cargo doc` | 0 warnings (was 1) |
| Library tests | 264 pass (was 255) |
| Integration tests | 9 pass (new) |
| Unsafe code | Forbidden — zero blocks |
| Dependencies | Pure Rust — zero C/C++ FFI |
| Line coverage | 94.9% (target ≥90%) |

### Key Changes for BarraCUDA Team

1. **GPU validation helpers deduplicated**: 23 binaries now share `gpu_readback()`,
   `max_abs_diff_gpu_vs_cpu()`, `gpu_tensor!` from `validation.rs`. If BarraCUDA
   adds a `testing` module, these are ready for absorption.

2. **Tolerance introspection system**: `NamedTolerance` struct with
   `all_tolerances()`, `tolerance_by_name()`, `categories()`. Runtime-discoverable,
   categorized, justified. Model for BarraCUDA's own precision system.

3. **16 determinism tests**: Bitwise-identical verification for seeded stochastic
   algorithms. Pattern for any BarraCUDA consumer.

4. **Python baseline drift detection**: `control/check_drift.sh` re-runs all 25
   baselines and verifies no numeric drift. CI-ready pattern.

5. **Provenance enhancement**: Exact `python3 -c` commands for key validation
   targets (softmax, GELU, Rastrigin) with NumPy/SciPy version pinning.

---

## Validation Summary

| Tier | Coverage | Checks |
|------|----------|--------|
| Python (Py) | 25/25 (100%) | 206 |
| Rust CPU (Rs) | 25/25 (100%) | 264 lib + 9 integration |
| BarraCUDA CPU (bC) | 24/25 (96%) | 203 |
| BarraCUDA GPU Tensor (gT) | 23/25 (92%) | 98+ |
| metalForge WGSL (mF) | 15/25 (100%†) | 108 |
| GPU Pipeline (gP) | 15/25 (100%†) | 94 |
| Cross-dispatch (xD) | 15/15 (100%) | 49 |

`†` All applicable papers (Phase 0/0+ use PyTorch training, not WGSL).

---

## Action Items for ToadStool

| Priority | Item | Status | Details |
|----------|------|--------|---------|
| Critical | Fix S-15 matmul hang | Open | Elements ≤ 0.1 magnitude, RTX 4070 Vulkan. Test AMD/Intel to isolate |
| High | Fix S-03b MHA projection | Open | `div_ceil(16)` → `div_ceil(1)` in projections.rs |
| Medium | Wire Conv2D/Pool to GpuExecutor | CPU resolved | `cpu_conv_pool` now `pub` (S41); GPU wiring still pending |
| Medium | Add `ops::prng` module | Open | Absorbs `xoshiro128ss.wgsl` |
| Low | Consider `testing` module | Open | Absorb gpu_readback, require!, NamedTolerance patterns |

---

## Cross-Spring Contributions

| From | Contribution | Beneficiary |
|------|-------------|-------------|
| neuralSpring → BarraCUDA | Householder+QR eigensolver | hotSpring, wetSpring |
| neuralSpring → BarraCUDA | 8 bio-op WGSL shaders | wetSpring |
| neuralSpring → BarraCUDA | 4-tier matmul KernelRouter | All Springs |
| neuralSpring → BarraCUDA | Capability-based dispatch pattern | All Springs |
| hotSpring → BarraCUDA → neuralSpring | Spectral theory stack | neuralSpring validates (17/17) |
| wetSpring → BarraCUDA → neuralSpring | f64 HMM batch | neuralSpring validates (11/11) |
| ToadStool → neuralSpring | 4 new bio-op wrappers (S39) | **Benchmarked: 0.97–1.10×** (negligible overhead) |
| ToadStool → neuralSpring | `cpu_conv_pool` pub (S41) | **LeNet-5 full bC: 13/13 PASS** |
| ToadStool → neuralSpring | 19 new WGSL shaders (S42) | GPU paths for CPU-only ops |

---

*25 papers · 5 disciplines · 4 faculty · 1600+ checks · ALL GREEN.
Session 42: deep audit + ToadStool sync + rewiring (d45fdfb3 → 5437c170).
10-kernel upstream parity bench (0.72–1.10×), 10/10 dual-path correctness (9 bit-identical),
LeNet-5 full bC (13/13), cross-spring lineage documented (hotSpring↔wetSpring↔neuralSpring).*
