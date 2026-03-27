# ToadStool/BarraCuda S82 — Deep Debt & Modernization Handoff

**Date**: March 2, 2026  
**From**: ToadStool S81–S82  
**To**: ToadStool/BarraCuda team (next session)  
**License**: AGPL-3.0-or-later  
**Covers**: Sessions 81–82 (March 2, 2026)

---

## Executive Summary

- **16 GPU ops migrated** to `ComputeDispatch` builder (111/~250 total, +16 from S80)
- **Real OS memory detection** — `estimate_system_memory()` reads `/proc/meminfo` (Linux) / `sysctl hw.memsize` (macOS) instead of hardcoded 8GB/16GB
- **`creation.rs` refactored -13%** (744→645 lines) — extracted `negotiate_features`, `score_physical_device`, `assemble` helpers
- **InterconnectTopology + SubstratePipeline** — Multi-substrate cross-device routing with `BandwidthTier` cost model
- **4 ET₀ methods** added (Thornthwaite, Makkink, Turc, Hamon) — hydrology module now has 6 total
- **IFFT/NTT/INTT buffer fix** — fragile `is_multiple_of(2)` replaced with robust `current_input` tracking
- **`BarracudaError::Io` + `::Json`** — New error variants with `#[source]` and context
- **`enable f64;` stripping** defense-in-depth in `compile_shader_df64` and `for_driver_profile`
- **LocalhostDiscoveryClient** evolved from hardcoded `localhost:8080` to env-based (`TOADSTOOL_LOCAL_PORT`)
- All changes validated: `cargo check --workspace` clean, 17+ targeted tests pass

---

## Part 1: ComputeDispatch Migration (+16 ops)

### Migrated in S82

| Op | File | Complexity | Pattern |
|----|------|-----------|---------|
| FHE XOR | `ops/fhe_xor.rs` | Simple | 2 read + 1 rw + 1 uniform, `.dispatch_1d()` |
| FHE OR | `ops/fhe_or.rs` | Simple | Same as XOR |
| FHE AND | `ops/fhe_and.rs` | Simple | Same as XOR |
| FHE Rotate | `ops/fhe_rotate.rs` | Simple | 1 read + 1 rw + 1 uniform |
| FHE Modulus Switch | `ops/fhe_modulus_switch.rs` | Simple | 1 read + 1 rw + 1 uniform |
| FHE Pointwise Mul | `ops/fhe_pointwise_mul.rs` | Simple | 2 read + 1 rw + 1 uniform |
| Wilson Plaquette | `ops/lattice/plaquette.rs` | Simple | `.f64()`, custom WG size |
| HMC Force SU(3) | `ops/lattice/hmc_force_su3.rs` | Simple | `.f64()` |
| GPU Wilson Action | `ops/lattice/gpu_wilson_action.rs` | Simple | `.f64()` |
| GPU Kinetic Energy | `ops/lattice/gpu_kinetic_energy.rs` | Simple | `.f64()` |
| Mel Scale | `ops/mel_scale.rs` | Simple | f32, `.dispatch_1d()` |
| Pitch Shift | `ops/pitch_shift.rs` | Simple | f32 |
| Smith-Waterman | `ops/bio/smith_waterman.rs` | Simple | Per-diagonal sequential dispatch |
| Felsenstein | `ops/bio/felsenstein.rs` | Simple | Per-level sequential dispatch |
| Batched Bisection | `optimize/batched_bisection_gpu.rs` | Simple | `.f64()` |
| Cubic Spline | `interpolate/cubic_spline.rs` | Simple | `.f64()`, eval_many_gpu |

### Remaining Legacy Files (36 total)

| Category | Count | Examples | Notes |
|----------|-------|---------|-------|
| **Simple** | 15 | matmul_tiled, mosaic, probe/runner | Straightforward migration |
| **Medium** | 10 | fhe_key_switch, gemm_f64, compute_graph | Multiple entry points or caching |
| **Complex** | 6 | fhe_ntt, fhe_intt, pipeline/mod, bicgstab, cg_gpu/* | Need ComputeDispatch multi-stage API |
| **Infrastructure** | 5 | autotune, batched_encoder, stateful, fma | Dynamic bind groups, caching |

**toadStool action:** The 6 complex ops (iterative solvers, multi-pass FFT) will need a `ComputeDispatch::multi_pass()` or `ComputeDispatch::submit_and_continue()` API extension before they can be migrated.

---

## Part 2: Production Stub Evolution

| Stub | Before | After |
|------|--------|-------|
| `estimate_system_memory()` | Hardcoded 8GB/2GB by pointer width | Reads `/proc/meminfo` (Linux), `sysctl hw.memsize` (macOS), fallback to constants |
| `detect_system_memory_bytes()` | Did not exist | New public API returning `Option<u64>` |
| `CpuExecutor::detect_capabilities()` | `DEFAULT_MEMORY_BYTES = 16GB` | Uses `detect_system_memory_bytes()` with `FALLBACK_MEMORY_BYTES` |
| `LocalhostDiscoveryClient::new()` | Hardcoded `localhost:8080` | Empty by default; `with_local_compute()` reads `TOADSTOOL_LOCAL_PORT` |
| `storage::AMQP_PORT` | Inline `5672` in URL string | Named constant `AMQP_PORT = 5672` |

**toadStool action:** `WebGpuFramework::execute_kernel()` still echoes inputs (deeper architectural work needed to bridge to barracuda's wgpu device). Track as D-WGF debt item.

---

## Part 3: Architecture Improvements

### creation.rs DRY Refactoring (744→645 lines)

Extracted 3 shared helpers to eliminate 6x code duplication:

| Helper | Deduplicates | Used By |
|--------|-------------|---------|
| `negotiate_features(adapter, wanted)` | Feature negotiation block (5 lines × 4) | `from_adapter`, `from_adapter_index`, `new_with_limits`, `new_cpu_relaxed` |
| `score_physical_device(device)` | Adapter scoring (8 lines × 2) | `discover_best_adapter`, `discover_primary_and_secondary_adapters` |
| `assemble(device, queue, info)` | Device construction (12 lines × 6) | All constructors except `from_existing` |

### InterconnectTopology + SubstratePipeline (S81)

New modules in `barracuda::multi_gpu`:
- `interconnect.rs` — `BandwidthTier` (Local/NvLink/PciePeer/PcieHost/PcieLow/Network), `Link`, `InterconnectTopology`
- `pipeline_dispatch.rs` — `SubstratePipeline`, `PipelineStage`, `FallbackPolicy` (Degrade/Skip/Fail), capability-based routing

Absorbed from groundSpring V61, adapted to barracuda's existing `Substrate`/`SubstrateCapability` types.

---

## Part 4: Science & Math Additions (S81)

| Addition | Module | Notes |
|----------|--------|-------|
| `thornthwaite_et0()` | `stats::hydrology` | Monthly temperature-only ET₀ (Thornthwaite 1948) |
| `makkink_et0()` | `stats::hydrology` | Radiation-based ET₀ (Makkink 1957) |
| `turc_et0()` | `stats::hydrology` | Radiation-temperature with humidity (Turc 1961) |
| `hamon_et0()` | `stats::hydrology` | Temperature + daylight hours (Hamon 1963) |
| `complex_polyakov_average()` | `ops::lattice::wilson` | (Re, Im) deconfinement diagnostic |
| `anderson_eigenvalues()` | `spectral::anderson` | 1D Anderson Hamiltonian eigenvalues |
| `FitResult::slope/intercept/coefficients` | `stats::regression` | Named accessors for model params |
| `BarracudaError::Io` + `::Json` | `error` | Structured error variants with context |

---

## Part 5: Bug Fixes (S81)

| Bug | File | Root Cause | Fix |
|-----|------|-----------|-----|
| IFFT wrong output buffer | `ops/fft/ifft_1d.rs` | `is_multiple_of(2)` failed for odd stages | Use `current_input` (always holds last-written buffer) |
| FHE NTT fragile buffer | `ops/fhe_ntt/compute.rs` | Same `is_multiple_of(2)` pattern | `std::ptr::eq(current_input, &intermediate_buffer)` |
| FHE INTT fragile buffer | `ops/fhe_intt/compute.rs` | Same pattern | Direct `current_input` reference |
| `enable f64;` not stripped | `shaders/precision/mod.rs`, `compilation.rs` | `for_driver_profile` and `compile_shader_df64` missing strip | Added `.filter(\|l\| l.trim() != "enable f64;")` |

---

## Part 6: Audit Findings (Informational)

### God Files >600 Lines (28 identified)

| Crate | Count | Top File | Lines |
|-------|-------|----------|-------|
| barracuda | 7 | `shaders/precision/precision_tests.rs` | 891 |
| cli | 3 | `templates/specialized_templates.rs` | 729 |
| core | 10 | `toadstool/src/ecosystem/communication/tests.rs` | 793 |
| runtime | 8 | `specialty/src/lib.rs` | 791 |

**toadStool action:** Priority refactors: `specialized_templates.rs` (one template per file), `security.rs` (split types + policy), `specialty/src/lib.rs` (extract platform adapters).

### Unsafe Code

45 blocks total, all necessary and SAFETY-documented. No reducible blocks. 2 in barracuda (wgpu pipeline cache, SPIR-V passthrough), rest in runtime FFI/hardware.

### Dependency Notes

- `config` vs `figment` overlap in workspace — consolidation opportunity
- `notify` uses `inotify-sys` (C FFI on Linux) — only C dep besides `pyo3`
- All other deps are pure Rust

---

## Action Items for Next Session

1. **ComputeDispatch multi-stage API** — Design `submit_and_continue()` for iterative solvers (bicgstab, cg_gpu) and multi-pass FFT (fhe_ntt, fhe_intt)
2. **Migrate 15 simple remaining ops** — matmul_tiled, mosaic, bio ops, probe/runner, etc.
3. **WebGPU framework** — Either bridge to barracuda's wgpu device or convert to honest error returns
4. **God file refactoring** — `specialized_templates.rs`, `security.rs`, `specialty/src/lib.rs`
5. **Config consolidation** — Evaluate standardizing on `figment` across workspace (currently `config` + `figment`)
6. **Test coverage** — Target 90% (currently 41.86%); major gap in GPU ops and neuromorphic
7. **Archive** — Move `DEBT_ANALYSIS_REPORT.md` to `fossil/toadStool/` (superseded by EVOLUTION_TRACKER)

---

*This handoff follows the ecoPrimals wateringHole convention. Supersedes TOADSTOOL_BARRACUDA_S80_EVOLUTION_HANDOFF_MAR02_2026.md.*
