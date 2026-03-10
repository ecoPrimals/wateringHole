<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# neuralSpring V92 → toadStool/barraCuda/coralReef Upstream Rewire Handoff

**Date**: March 10, 2026
**From**: neuralSpring S137 (968 lib tests, 71 forge tests, 42/42 Python drift PASS, 232 binaries)
**To**: barraCuda team, toadStool team, coralReef team
**Supersedes**: V90 S132 handoff (Mar 8, 2026)
**Synced against**: barraCuda `a898dee`, toadStool S139 (`bfe7977b`), coralReef Iteration 10 (`d29a734`)
**License**: AGPL-3.0-or-later

## Executive Summary

neuralSpring S137 is an **upstream rewire and revalidation release** that
reviews all Mar 8–9 wateringHole handoffs from toadStool (S130+→S139),
barraCuda (cross-spring absorption Sprint 2, deep debt + concurrency),
coralReef (precision architecture), and groundSpring (V98/V100 sovereign
pipeline rewire), then rewires neuralSpring library code to use upstream
constants and documents absorption status across the shader catalog and
pipeline graph.

**What changed since V90 (S132→S137):**
- **`WORKGROUP_SIZE_1D` rewire**: Eliminated 15 hardcoded `256` values in
  library code — `gpu_shader_validation::wg1d` now uses
  `barracuda::device::capabilities::WORKGROUP_SIZE_1D`, and all 14 metalForge
  `ShaderLayout` entries in `bindings.rs` use `WG` (alias for same constant).
- **Shader absorption documentation**: 7 WGSL shaders in `shaders.rs` updated
  from "Absorption target" to "Absorption status — absorbed upstream": Wright-Fisher
  (`WrightFisherGpu`), chi² (`fused_chi_squared_f64`), KL divergence
  (`fused_kl_divergence_f64`), HMM backward/Viterbi (`hmm::hmm_backward`/`hmm_viterbi`),
  matrix correlation (`stats_f64::matrix_correlation`), linear regression
  (`stats_f64::linear_regression`). Local WGSL retained for provenance and
  coralReef corpus reference.
- **toadStool S139 absorption acknowledged**: `graph.rs` module docs updated to
  note that `pipeline_graph` DAG was absorbed upstream into
  `toadstool::universal::pipeline_graph` (S139). Local copy retained because
  toadStool is not a cargo dependency.
- **Lib test count**: 968 (unchanged — no new tests, rewire is doc+constant only)
- **Zero API breakage**: all pins match HEAD, zero clippy warnings, zero doc warnings

**Sessions S133→S137 cumulative** (since V90 S132):
- S133: metalForge PCIe, biomeOS pipeline DAG, petalTongue IPC, V91 handoff
- S135: petalTongue visualization evolution (7 scenario builders, 56/56 validation)
- S136: Deep audit (`headless()` socket, `read_buffer_u32`, validate_gpu refactor, benchmark gap docs)
- S137: This upstream rewire release

*This handoff is unidirectional: neuralSpring → ecosystem. No response expected.*

---

## 1. Upstream Handoffs Reviewed

### toadStool S130+ → S139 (reviewed, no code change needed)

| Handoff | Key Item | Impact on neuralSpring |
|---------|----------|----------------------|
| S139 Spring Absorption | `pipeline_graph` DAG absorbed from neuralSpring S134 | Documented in `graph.rs`. Local copy retained (not a cargo dep). |
| S139 Spring Absorption | `streaming_dispatch` absorbed from hotSpring v0.6.24 | No neuralSpring impact (neuralSpring doesn't use streaming dispatch) |
| S139 Spring Absorption | Dual-write discovery + GPU descriptor enrichment | No neuralSpring impact (neuralSpring discovers via `GPU_BACKEND` env, not toadStool IPC) |
| S138 Deep Debt | `sysinfo` elimination, ecoBin v3 | No neuralSpring impact |

### barraCuda (reviewed, `WORKGROUP_SIZE_1D` absorbed)

| Handoff | Key Item | Impact on neuralSpring |
|---------|----------|----------------------|
| Cross-Spring Absorption (Mar 8) | `F64NativeNoSharedMem` Ada reclassification | Already handled — `shared_memory_f64_safe()` matches only `F64Native` |
| Cross-Spring Absorption (Mar 8) | `hill_activation`/`hill_repression` absorbed to `stats::metrics` | Already using `barracuda::stats::hill` — NOTE: these wrappers NOT YET at HEAD |
| Cross-Spring Absorption (Mar 8) | `fused_ops_healthy()` canary | NOT YET at HEAD — neuralSpring uses local variance canary probe |
| Cross-Spring Sprint 2 (Mar 9) | `tridiagonal_ql`, `rng::lcg_step`, `activations`, `WrightFisherF32`, `AttentionDims` | **NOT YET at HEAD** (`a898dee`). Documented in handoff but not committed. |
| Deep Debt + Concurrency (Mar 9) | `WORKGROUP_SIZE_1D` constant | **ABSORBED** — rewired in `wg1d()` + 14 metalForge layouts |
| Deep Debt + Concurrency (Mar 9) | `Arc<str>` hot-path, ring buffer back-off, streaming pipeline | No neuralSpring impact (internal barraCuda) |

### coralReef Precision Architecture (reviewed, no code change needed)

| Handoff | Key Item | Impact on neuralSpring |
|---------|----------|----------------------|
| Precision Architecture (Mar 8) | Three-tier model: F32/Df64/F64 | neuralSpring's `coralForge` already uses df64 (15 shaders) |
| Precision Architecture (Mar 8) | `Fp64Strategy` in `CompileOptions` | neuralSpring uses `Fp64Strategy` from barracuda for dispatch routing |
| Precision Architecture (Mar 8) | Phase 2: IR-level df64 lowering (not yet done) | Future benefit — one f64 shader instead of 3 variants |

### groundSpring V98/V100 (reviewed, no code change needed)

| Handoff | Key Item | Impact on neuralSpring |
|---------|----------|----------------------|
| V98 Upstream Rewire | Same pins — confirms zero API breakage | Aligned |
| V100 Sovereign Pipeline | `SubstrateKind::Sovereign` dispatch priority | Not applicable — neuralSpring doesn't use metalForge substrate discovery |

---

## 2. Quality Gates

```
cargo fmt --check                             → PASS
cargo clippy --workspace --all-targets        → 0 warnings (pedantic + nursery)
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps → PASS (239 files)
cargo test --lib                              → 968 passed, 0 failed
cargo test -p neural-spring-forge --lib       → 71 passed, 0 failed
```

---

## 3. Remaining Absorption Opportunities (when upstream APIs land)

| Item | Upstream Status | neuralSpring Action When Available |
|------|----------------|-----------------------------------|
| `barracuda::activations::{sigmoid, relu, gelu}` (public module) | Handoff only — not at HEAD | Evaluate replacing `primitives.rs` CPU refs (keep for validation provenance) |
| `barracuda::rng::lcg_step` | Handoff only — not at HEAD | Replace inline LCG in 2 validation binaries |
| `barracuda::special::tridiagonal_ql` | Handoff only — not at HEAD | Papers 022-023 can use for Anderson diagonalization |
| `barracuda::ops::WrightFisherF32` | Handoff only — not at HEAD | Already using `WrightFisherGpu` (f64) — f32 variant is new |
| `session::AttentionDims` | Handoff only — not at HEAD | Evaluate for `validate_mha_gpu.rs` head_split/head_concat |
| `fused_ops_healthy()` | Handoff only — not at HEAD | Replace local variance canary probe in `Dispatcher` |
| `ComputeDispatch::CoralReef` backend | Handoff only (groundSpring P0) | Enable sovereign GPU path for f64 reductions |

---

## 4. Evolution Requests (carried + updated)

| Priority | Request | Team | Status |
|----------|---------|------|--------|
| **P0** | Land Sprint 2 APIs (`activations`, `rng`, `tridiagonal_ql`) | barraCuda | Handoff documented, not committed |
| **P0** | Reclassify Ada Lovelace as `F64NativeNoSharedMem` | barraCuda | **RESOLVED** at HEAD |
| **P1** | `fused_ops_healthy()` canary in test harness | barraCuda | Handoff documented, not committed |
| **P1** | Runtime GPU reduction smoke test in `ComputeDispatch` | toadStool | Open (V97) |
| **P2** | GPU tridiagonal eigenvolver | barraCuda | Open |
| **P2** | End-to-end coralReef sovereign path for f64 reductions | toadStool + coralReef | Enabled by Iteration 10 |
| **P2** | Industry GPU parity benchmarks (Kokkos, cuBLAS, Polybench) | barraCuda + toadStool | Documented in `specs/BENCHMARK_ANALYSIS.md` |

---

## 5. Cross-Spring Alignment

neuralSpring is now aligned with:
- groundSpring V98/V100 (same pins)
- All Mar 8–9 wateringHole handoffs reviewed and absorbed where applicable
- ToadStool S139 absorption acknowledged
- coralReef precision architecture understood and compatible

## 6. Validation Binaries with Local Activations / PRNG

neuralSpring's validation binaries (`src/bin/validate_*.rs`) contain local
`sigmoid`, `gelu`, `relu`, `splitmix32` implementations. These are
**intentional CPU reference implementations** that validate against specific
Python baselines. They should NOT be replaced with barracuda ops — the
purpose is independent verification. Library code (`primitives.rs`) serves
the same role for the library test suite.
