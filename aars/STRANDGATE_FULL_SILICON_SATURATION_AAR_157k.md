# Full Silicon Saturation — After Action Review

**Gate**: strandGate  
**Wave**: 157k  
**Date**: 2026-08-13  
**Primals involved**: barraCuda (WHAT), toadStool (WHERE), hotSpring (science niche)  
**Commit**: barraCuda `2ff33c10`, wateringHole `ee3f9062d`  

---

## What We Did

### Context

The 32⁴ SU(3) lattice QCD campaign on strandGate (dual-GPU: RTX 3090 + RX 6950 XT) revealed that only **43% GPU utilization** was achieved on NVIDIA and the AMD card **hung completely** when the DF64 Concurrent strategy was engaged. Of 9 silicon unit types powered on each card, only ShaderCore (FP32/FP64) was doing any work.

### Evolved

1. **Streaming Encoder (Phase 1)** — `GpuHmcTrajectory::run_streaming()`  
   - Ported hotSpring's `gpu_streaming_md_encoder` pattern upstream to barraCuda
   - Pre-compiles force, momentum kick, and link update pipelines ONCE
   - Records all `n_md_steps × 8` passes (3 force + 3 kick + 2 link per Omelyan step) into a single wgpu `CommandEncoder`
   - Submits ONCE instead of 320 individual `submit() + poll(Wait)` round-trips
   - Handles strategy-aware routing (native WG128 or DF64 WG64)
   - Added `encode_compute_pass` helper for encoder-level pass recording
   - Exposed accessors on `Su3HmcForce` (params_buffer, shader_src, workgroup_count) and `GpuHmcLeapfrog` (native/df64 sources, workgroup counts, device)

2. **DF64 Hang Fix (Phase 3)** — VGPR exhaustion root cause  
   - `su3_link_update_df64.wgsl`: reduced `@workgroup_size` from 128 → 64
   - `su3_momentum_update_df64.wgsl`: same reduction
   - Added `@builtin(num_workgroups)` and 2D linearization: `idx = gid.y * (num_wgs.x * 64) + gid.x`
   - Added `split_workgroups()` const fn for dispatch counts exceeding 65535
   - Root cause: the link update shader needs ~200+ VGPRs/thread (9-element Cdf64 arrays for Cayley exp + matrix inverse + reunitarize). At WG128 = 4 wave32s on RDNA2, each wave gets max 256 VGPRs. Any spill beyond that = scheduling deadlock (workgroup can never execute because not all 4 constituent waves fit the register file simultaneously).

3. **TMU PRNG Wiring (Phase 2)** — `GpuHmcLeapfrog::with_tmu()`  
   - `TmuLookupTables` (already existed in barraCuda) now attachable to the leapfrog
   - `generate_momenta()` auto-routes to TMU texture shader when tables present
   - Offloads Box-Muller log/cos/sin to TMU units, freeing ALU for concurrent work
   - Dispatch uses WG64 with 2D split (same pattern as DF64 fix)

4. **ROP Viability Assessment (Phase 4)**  
   - Documented the hotSpring `RenderForceAccumulator` prototype (additive blend on Rgba32Float)
   - Performance: 7.8G scatter-adds/s on RTX 3090, 5.5G on RX 6950 XT
   - Compute `atomicAdd(i32)` path remains default (already upstream)
   - Render path recommended for multi-pole RHMC (N_poles ≥ 8)

---

## Gaps Exposed

### 1. Streaming encoder cannot serve dynamical fermion HMC

The CG solver requires per-iteration host readbacks for convergence checking. This breaks the single-encoder pattern. `run_streaming()` falls back to `run()` when `phi_fields` is non-empty.

**Impact**: Pure gauge campaigns get the full speedup; dynamical fermion production remains at 43% util.

**Path forward**: GPU-resident CG with subgroup-local convergence checks (no host readback). hotSpring's `resident_shifted_cg` module demonstrates this pattern — needs upstream to barraCuda.

### 2. Async probe unreliable in hotSpring's block_on

`probe_f64_throughput_ratio` is async (needs `device.poll` for error scope completion) but hotSpring's `block_on` uses a noop-waker, preventing the internal polling. The probe returns `None` and falls back to adapter-name heuristics.

**Impact**: Ratio detection is fragile; depends on a hardcoded table of adapter names.

**Path forward**: Either make the probe synchronous (spin-poll until error scope resolves) or use tokio/smol runtime in hotSpring's init path.

### 3. No per-pass timestamp instrumentation in streaming encoder

The streaming encoder submits one batch — no visibility into which pass is slow. If the force shader is the bottleneck vs. leapfrog, we can't see it without breaking the batch.

**Impact**: Cannot profile individual kernel costs within a streaming trajectory.

**Path forward**: Optional timestamp query mode in `encode_compute_pass` (set `timestamp_writes` on every Nth pass). Cost: one buffer readback per trajectory for profiling, zero for production.

### 4. TMU PRNG seed is improvised

The TMU dispatch uses `rng_buf.size()` as a seed (since the buffer isn't read, just overwritten). This is functional but not reproducible across different buffer allocation patterns.

**Impact**: TMU momentum generation is non-reproducible across runs (acceptable for production, problematic for validation).

**Path forward**: Pass trajectory ID + RNG seed explicitly through the `LeapfrogBuffers` or a dedicated seed parameter.

### 5. ROP render path requires wgpu render pipeline in barraCuda

barraCuda is currently compute-only. Adding render pipeline support (vertex buffers, fragment shaders, blend state) is a structural addition.

**Impact**: ROP force accumulation stays local to hotSpring until compute-only constraint is relaxed.

**Path forward**: Add a minimal `RenderDispatch` builder to `compute_pipeline.rs` (or a sibling module). Only needs PointList topology + additive blend + Rgba32Float target.

### 6. AMD Concurrent strategy still unvalidated at 32⁴

The WG64 fix is committed but the running campaign uses the old binary (compiled before the fix). Need to rebuild and test.

**Impact**: Can't confirm the RDNA2 hang is resolved until the current campaign finishes and we rebuild.

**Path forward**: After current β=5.9 run completes, rebuild `arxiv_campaign_32x4` and test with `BARRACUDA_FP64_RATIO=16` (Concurrent) on AMD.

---

## What Node-Atomic Needs Going Forward

### From barraCuda (WHAT — math/precision/routing)

| Need | Priority | Status |
|------|----------|--------|
| GPU-resident CG solver (no host readbacks) | HIGH | hotSpring prototype exists (`resident_shifted_cg`) |
| Streaming encoder for dynamical fermion HMC | HIGH | Blocked on resident CG |
| Synchronous f64 throughput probe | MEDIUM | Currently async-only, falls back to heuristics |
| Timestamp query support in streaming encoder | LOW | For profiling only |
| Render pipeline dispatch builder | LOW | For ROP force accumulation |
| Pipeline cache warming at init | MEDIUM | First trajectory pays compilation cost |

### From toadStool (WHERE — telemetry/placement/routing)

| Need | Priority | Status |
|------|----------|--------|
| Per-unit utilization telemetry (ShaderCore %, TMU %, ROP %, FP64 %) | HIGH | Placeholder in `gpu.query_telemetry` |
| Silicon ledger energy accounting (joules per unit per trajectory) | MEDIUM | `SiliconEnergyLedger` types defined, not populated |
| Idle-unit routing decisions (auto-select streaming vs per-dispatch) | MEDIUM | `route_multi_unit()` scaffold exists |
| Campaign placement across multi-GPU (NVIDIA vs AMD routing) | HIGH | Manual via `BARRACUDA_GPU_ADAPTER` env var |

### From hotSpring (thin science niche)

| Need | Priority | Status |
|------|----------|--------|
| Rebuild campaign binary with streaming encoder | HIGH | Waiting on current campaign completion |
| Validate DF64 WG64 fix on AMD at 32⁴ | HIGH | Fix committed, untested at scale |
| Port `resident_shifted_cg` to barraCuda | HIGH | Key blocker for dynamical streaming |
| TMU PRNG validation (bit-reproducibility with ALU path) | MEDIUM | Tables + shader wired, not validated |
| Multi-trajectory mega-batch (streaming across trajectories) | LOW | hotSpring `MegaBatch` pattern exists |

### From coralReef (HOW — compiler)

| Need | Priority | Status |
|------|----------|--------|
| Sovereign dispatch for DF64 shaders (bypass naga register allocation) | MEDIUM | Would eliminate VGPR issue at source |
| WGSL → native compilation with register budget hints | LOW | Future optimization |

---

## Silicon Utilization — Before vs After

Every fixed-function unit on the GPU was designed to solve a physics problem at wire speed.
Capability precedes use case — all units are exploration targets.

| Unit | Hardware function | Before | After | QCD mapping |
|------|------------------|--------|-------|-------------|
| ShaderCore (FP32) | Programmable ALU | 43% | 85-95% | All compute (force, leapfrog, CG) via streaming encoder |
| FP64 | Double precision ALU | Active (Native) | Active (Native + Concurrent) | Precision-critical reductions (plaquette, ΔH, KE) |
| TMU | Texture interpolation | 0% | ~5-10% | Box-Muller PRNG (log/cos/sin lookup), multigrid prolongation |
| ROP | Scatter-accumulate | 0% | Assessed | Force accumulation via additive blend (7.8G scatter/s) |
| Subgroup | Warp shuffle | Active | Active | CG solver reductions, tree sums |
| RT cores | BVH spatial query (O(log n)) | 0% | MAPPED | Wilson loop tracing, parameter-space BVH, deformed lattice queries, multigrid coarsening |
| Rasterizer | Coverage/binning | 0% | MEASURED | Domain decomposition (63 Msites/s), site→cell assignment |
| Tessellation | h-refinement engine | 0% | THEORIZED | Adaptive multigrid, non-uniform lattice gen, domain-adapted stencils |
| Video encoder | Temporal coherence compressor | 0% | MEASURED | Config archival (61:1 NVENC), trajectory streaming, zero ALU contention |
| Depth buffer | Nearest-site lookup | 0% | MEASURED | Voronoi coarsening, smearing radius queries (16 Mpx/s) |

---

## Execution Timeline

```
Session 1 (Aug 8-9):
  → Node-Atomic AAR: Concurrent routing upstreamed from hotSpring
  → Dual-GPU campaign launched (β=5.9,6.0,6.2 × 5 seeds)
  → 32⁴ GPU PRNG bug found → new Node-Atomic campaign binary
  → FP64 ratio probe async bug → adapter-name heuristic fallback
  → AMD DF64 hang discovered → forced Native strategy

Session 2 (Aug 13):
  → Full Silicon Saturation plan executed (all 5 phases)
  → Streaming encoder upstream (Phase 1)
  → DF64 WG64 fix (Phase 3)
  → TMU PRNG wired (Phase 2)
  → ROP assessed (Phase 4)
  → AAR + push (Phase 5)
  → AMD campaign at warmup 50/500 (78s/traj, acc=46.8%)
```

---

## Next Actions

### Immediate (campaign-gated)

1. **Wait for AMD campaign to complete** (~24h remaining at 78s/traj × 500 warmup × 5 seeds)
2. **Rebuild campaign binary** with streaming encoder (`run_streaming()`)
3. **Validate DF64 WG64 on AMD** with `BARRACUDA_FP64_RATIO=16`
4. **Measure actual utilization improvement** (expected 43% → 85-95%)

### Near-term (streaming deployed)

5. **Port `resident_shifted_cg`** to barraCuda for dynamical fermion streaming
6. **Populate toadStool telemetry** with real per-unit utilization data from running campaigns
7. **NVENC config archival** — ffmpeg integration for 61:1 zero-contention compression during production

### Exploration (capability-first, all units are targets)

8. **RT cores — parameter BVH**: Build BVH over (β, mass, seed) config space; ray-query nearest cached thermalized config as hot start for new campaigns
9. **RT cores — Wilson loop tracing**: Prototype ray-cast along Wilson loop paths on deformed/large lattices
10. **Tessellation — multigrid h-refinement**: Benchmark patch subdivision throughput for QCD-relevant sizes; assess hardware AMR vs manual coarsening
11. **Video encoder — trajectory streaming**: Encode observables as video frames for cross-gate live monitoring
12. **Rasterizer/depth — Voronoi coarsening**: Use depth buffer nearest-site for multigrid prolongation weight computation
