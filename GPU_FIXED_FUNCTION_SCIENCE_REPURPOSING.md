# GPU Fixed-Function Hardware Repurposing for Science

**Date**: March 17, 2026
**From**: ludoSpring V24 (game science audit)
**To**: ALL springs, barraCuda, coralReef, toadStool
**Type**: Ecosystem-wide exploration guidance
**License**: AGPL-3.0-or-later

---

## Executive Summary

The DF64 discovery in hotSpring/coralReef proved that fp32 ALUs — "designed for"
pixel colors — can emulate fp64 at 8-16x the throughput of native fp64 on
consumer GPUs. This was a hidden computer inside the visible one.

A modern GPU die contains at least **eight distinct fixed-function hardware
units** beyond the programmable shader cores. Each was designed for a specific
graphics operation but actually computes a general mathematical function. Every
spring should investigate which of these units accelerates problems in their
domain. Develop locally, validate in experiments, and primals absorb what works.

The principle: **every piece of fixed-function GPU hardware is a special-purpose
computer that can be repurposed if you can map your problem to its
input/output contract.**

---

## The Hidden Computers on the GPU Die

### 1. Shader Cores (CUs / SMs) — The Known Computer

What they do: floating-point arithmetic (add, mul, fma, transcendentals).

What they really are: massively parallel math engines with no opinion about
what the numbers mean. Already used for science via compute shaders.

**Known repurposing**: DF64 (Dekker/Knuth double-float using fp32 pairs).
This is the pattern to follow — find unexpected computational value in
hardware designed for something else.

### 2. Rasterizer — A Spatial Query Engine

**Graphics job**: Given a triangle (3 vertices), determine which pixels it
covers. Interpolate vertex attributes (position, color, normal) across the
surface using barycentric coordinates.

**What it actually computes**: For every pixel (x, y), evaluate three
half-plane equations and perform weighted interpolation. This is a
**point-in-polygon classifier with free attribute interpolation** running
at billions of tests per second on dedicated silicon. Zero shader cycles
consumed.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Voxelization | Render mesh from 3 views → 3D occupancy grid | wetSpring (fluid obstacles), hotSpring (collision geometry) |
| FEM cell assignment | Which grid points fall inside which mesh elements? | hotSpring (thermal FEM), groundSpring (geological FEM) |
| Scattered data interpolation | Data at mesh vertices → values at arbitrary interior points | All springs with unstructured mesh data |
| Conservative rasterization | Which grid cells does a triangle overlap? | hotSpring (particle-in-cell), wetSpring (SPH binning) |
| Spatial binning | Assign particles to cells | hotSpring (MD neighbor assignment) |

**How to explore**: Submit triangles through the graphics pipeline with
vertex attributes carrying scientific data. Read back the framebuffer.
The rasterizer does the spatial query; the fragment shader does nothing
(pass-through). Compare throughput vs compute-shader equivalent.

### 3. Depth Buffer (Z-Buffer) — A Hardware Min/Max Reducer

**Graphics job**: For each pixel, keep the nearest (smallest depth) fragment.
Discard occluded geometry.

**What it actually computes**: A per-pixel **minimum reduction** over all
fragments that map to that pixel. This is fixed-function silicon in the ROPs,
running at framebuffer fill rate.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Voronoi diagrams | Render cone per seed point; depth = distance from apex; Z-buffer keeps nearest | groundSpring (geological tessellation), wetSpring (cell decomposition) |
| Distance fields | Depth buffer = nearest-surface distance at every pixel | All springs (SDF for collision, level sets) |
| Spatial priority | "Nearest object to each grid point" queries | neuralSpring (nearest-neighbor classification) |

**The Voronoi trick**: Render a cone at each seed point (x_i, y_i) where
cone depth at pixel (x, y) = distance((x,y), (x_i, y_i)). The Z-buffer
keeps the minimum depth per pixel. The color buffer (or stencil) records
which seed was nearest. Result: a hardware-accelerated Voronoi diagram.

### 4. ROPs / Alpha Blending — A Hardware Accumulator

**Graphics job**: Blend incoming fragment color with existing framebuffer
value. Configurable: `result = src * srcFactor + dst * dstFactor`.

**What it actually computes**: With additive blending (both factors = 1.0),
every fragment that lands on a pixel **adds** its value to the running total.
This is a hardware scatter-add.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Histogram construction | One point per sample at bin position; additive blend = count | All springs (data analysis) |
| Particle deposition | Scatter particle quantities onto grid (PIC method) | hotSpring (plasma PIC), wetSpring (SPH) |
| Splatting (volume rendering) | Each voxel = screen-aligned quad with opacity | healthSpring (medical imaging), wetSpring (fluid viz) |
| Beer-Lambert transmittance | Multiplicative blending = optical depth accumulation | airSpring (atmospheric), hotSpring (radiation transport) |
| Density estimation | Kernel splats with additive blending = KDE | All springs |

### 5. RT Cores — A Nearest-Neighbor Search Engine

**Graphics job**: Traverse a BVH (Bounding Volume Hierarchy) to find
ray-triangle intersections for realistic reflections and shadows.

**What it actually computes**: Given a spatial index (BVH) and a query
(ray), find the nearest object. This is a **spatial index query machine**.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Molecular dynamics neighbors | BVH over atoms; ray from each atom; intersections within cutoff | hotSpring (MD force calculation) |
| Monte Carlo particle transport | Neutron/photon scattering through geometry | hotSpring (radiation), healthSpring (dosimetry) |
| Acoustic simulation | Sound propagation = ray tracing with scattering | ludoSpring (game audio), airSpring (environmental acoustics) |
| Line-of-sight / visibility | Can point A see point B through geometry? | ludoSpring (fog of war), groundSpring (terrain analysis) |
| Building energy / solar | How much sunlight enters through windows per hour? | airSpring (building energy modeling) |

**Hardware availability**: RTX 2000+ (NVIDIA), RDNA 2+ (AMD). Not available
on MI50 (GCN 5.0) or Titan V (Volta). Can be emulated in compute shaders
on any GPU (slower but functional).

### 6. Texture Units (TMUs) — A Hardware Interpolation Engine

**Graphics job**: Fetch texels from texture memory with bilinear, trilinear,
or anisotropic filtering. Hardware-accelerated interpolation with a spatial
cache optimized for 2D locality.

**What it actually computes**: Given coordinates (u, v), look up a 2D array
and interpolate between neighbors. One cycle per lookup.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Function table lookup | Store f(x) or f(x,y) in texture; TMU interpolates | All springs (equation of state, cross-sections) |
| Image resampling | Regrid 2D data with hardware interpolation | wetSpring (ocean data), airSpring (climate data) |
| Stencil operations | Texture gather reads 4 adjacent values in one op | hotSpring (finite differences), wetSpring (fluid PDE) |
| Activation functions | Precomputed activation tables for neural networks | neuralSpring |

**Key insight**: Any smooth 1D or 2D function that you call repeatedly can
be precomputed into a texture. The TMU does lookup + interpolation in a
single cycle. For functions like exp(), log(), erf() at reduced precision
(~fp16), this is effectively free.

### 7. Tessellation Hardware — An Adaptive Mesh Refiner

**Graphics job**: Subdivide geometry adaptively. The hull shader decides
tessellation factors; the fixed-function tessellator generates new vertices;
the domain shader positions them.

**What it actually computes**: Given a coarse mesh and per-element refinement
levels, produce a refined mesh. This is hardware-accelerated h-refinement.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Adaptive mesh refinement (AMR) | FEM mesh → tessellation factors from error estimate → refined mesh | hotSpring, wetSpring, groundSpring |
| Level-of-detail for visualization | Coarse far, fine near | petalTongue, ludoSpring |

### 8. Video Encode/Decode (NVENC / VCN) — A Data Compressor

**Graphics job**: Hardware H.264/H.265/AV1 encoding and decoding for video
streaming and recording.

**What it actually computes**: 2D block-based transform coding with motion
estimation and entropy coding. Operates on 2D arrays of values at hardware
speed.

**Science applications**:

| Application | Mapping | Springs |
|-------------|---------|---------|
| Simulation frame compression | Encode time-series of fields as "video" | All springs (storage of simulation output) |
| Motion estimation for registration | Hardware motion vectors = image registration | healthSpring (medical image alignment) |
| Temporal compression | Exploit frame-to-frame coherence in simulations | hotSpring (MD trajectories), wetSpring (ocean time series) |

---

## The DF64 Pattern: How to Discover Hidden Computers

The DF64 discovery followed a clear pattern that every spring can replicate:

1. **Identify a bottleneck**: fp64 throughput is terrible on consumer GPUs
2. **Study the hardware contract**: fp32 ALUs compute `a + b` and `a * b` exactly for fp32 inputs
3. **Find the mathematical mapping**: Dekker (1971) showed that fp64 arithmetic can be expressed as sequences of fp32 operations
4. **Validate**: Compare DF64 results against native fp64 and CPU fp64
5. **Measure the speedup**: 8-16x on RTX 3090 vs native fp64

The same pattern applies to every unit on the die:

1. **Identify your bottleneck**: What operation is slow in your compute shader?
2. **Study the hardware contract**: What does the fixed-function unit actually compute?
3. **Find the mapping**: Can your operation be expressed as the unit's operation?
4. **Validate**: Compare accuracy and correctness
5. **Measure**: Is it actually faster?

---

## Every Spring Explores Hardware — Every Discovery Benefits All

**This is not optional guidance.** Every spring should dedicate experiment time
to investigating fixed-function hardware for their domain. The DF64 discovery
came from hotSpring exploring fp32 ALUs for physics — but DF64 now benefits
every spring that needs fp64 math. The same cross-pollination will happen with
every hardware unit.

### Why Every Spring Must Explore

1. **Domain experts find domain mappings.** hotSpring knows which MD operations
   are bottlenecks. wetSpring knows which CFD operations are bottlenecks. Only
   the spring team can see the mapping between their science and the hardware.

2. **Discoveries are universal.** When wetSpring discovers that the rasterizer
   accelerates SPH particle binning, that same technique works for hotSpring's
   PIC plasma binning, groundSpring's FEM cell assignment, and ludoSpring's
   entity-to-tile mapping. The science is different; the hardware operation is
   identical.

3. **Primals absorb, all springs benefit.** A spring validates locally. barraCuda
   absorbs the technique as a dispatch op. coralReef learns to emit the
   pipeline state. Every spring then calls the same barraCuda primitive without
   knowing or caring which spring discovered it.

4. **Different springs test different hardware.** hotSpring has the MI50 (no RT
   cores, native fp64, no display) and Titan V (no RT cores, native fp64,
   display). ludoSpring's test cases run on RTX 3090 (RT cores, terrible fp64,
   display). The hardware matrix means each spring naturally explores different
   unit combinations.

### Cross-Benefit Matrix

Every hardware discovery in one spring creates a reusable primitive for all.
The rows are who discovers; the columns are who benefits:

| Discoverer → Primitive | hotSpring | wetSpring | airSpring | groundSpring | healthSpring | neuralSpring | ludoSpring |
|------------------------|-----------|-----------|-----------|-------------|-------------|-------------|-----------|
| **Rasterizer binning** (any spring) | PIC cell assign | SPH binning | Grid mapping | FEM cell assign | Tissue voxelization | Spatial attention | Entity-to-tile |
| **Z-buffer Voronoi** (any spring) | Distance fields | Free-surface tracking | Terrain analysis | Geological tessellation | Organ segmentation | Feature clustering | Pathfinding heuristic |
| **Additive blending** (any spring) | Charge deposition | Particle deposition | Optical depth | Mass accumulation | Back-projection | Gradient accumulation | Influence maps |
| **RT core neighbor search** (any spring) | MD neighbor list | SPH neighbor list | Radiation ray tracing | Seismic ray tracing | Dosimetry transport | kNN classification | Acoustic ray tracing |
| **TMU table lookup** (any spring) | EOS tables | Ocean resampling | Absorption coefficients | Material properties | PK/PD curves | Activation functions | Engagement curves |
| **Tessellation AMR** (any spring) | Thermal refinement | Flow refinement | Terrain LOD | Seismic refinement | Mesh refinement | — | Procedural terrain LOD |
| **Tensor core MMA** (any spring) | CG solver | Linear system solve | Matrix inversion | FEM stiffness solve | Image reconstruction | Training/inference | — |
| **Video encoder compression** (any spring) | MD trajectory compress | Ocean time-series | Climate data compress | Seismic waveform compress | Medical image compress | — | Replay compression |

**Read across a row**: one discovery, eight beneficiaries.
**Read down a column**: each spring benefits from every other spring's discoveries.

### Per-Spring Experiment Assignments

Each spring should create a baseCamp experiment (their own `exp076` equivalent)
exploring the units most relevant to their domain. The experiment naming
convention is the spring's own baseCamp numbering.

### hotSpring (Physics / Thermodynamics)

**Assignment**: Explore RT cores, rasterizer, TMUs, alpha blending for MD/plasma.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| RT core MD neighbor list | RT cores | BVH over particles → neighbor query | 10x+ over Verlet rebuild |
| Rasterizer PIC binning | Rasterizer | Triangle per particle → cell assignment | 10-50x over compute loop |
| TMU equation-of-state | TMU | Precomputed EOS table → hardware interpolation | 10-20x over exp() per pair |
| Blend charge deposition | ROPs | Additive blend → scatter-add onto grid | 5-10x over atomic add |
| Z-buffer distance field | Depth buffer | Cone rendering → Euclidean distance field | 100x over wavefront BFS |

**Cross-benefit**: RT core neighbor finding directly transfers to wetSpring SPH,
groundSpring seismic ray tracing, healthSpring dosimetry, ludoSpring fog of war.

### wetSpring (Fluid Dynamics / Ocean Science)

**Assignment**: Explore rasterizer, alpha blending, TMUs, depth buffer, video encoder.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| Rasterizer voxelization | Rasterizer | Obstacle mesh → occupancy grid | 10-50x over compute voxelizer |
| Blend SPH deposition | ROPs | Kernel splat → density/velocity field | 5-10x over atomic scatter |
| TMU ocean regridding | TMU | Bilinear interpolation on ocean grid | 10-20x over compute interpolation |
| Z-buffer free surface | Depth buffer | Level-set interface capture | 100x over marching cubes |
| Video encoder trajectories | NVENC/VCN | Time-series of fields as video frames | 6:1 compression, hardware speed |

**Cross-benefit**: Rasterizer voxelization transfers to hotSpring collision geometry,
groundSpring geological models, healthSpring anatomy voxelization.

### airSpring (Atmospheric / Air Quality)

**Assignment**: Explore TMUs, RT cores, alpha blending, rasterizer.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| TMU absorption tables | TMU | Gas absorption cross-sections → lookup | 10-20x over compute evaluation |
| RT solar radiation | RT cores | Sunlight through building geometry | 1000x over CPU ray tracing |
| Blend Beer-Lambert | ROPs | Multiplicative blend → optical depth | 5-10x over compute accumulation |
| Rasterizer terrain shadows | Rasterizer | Sun-direction triangle fill → shadow map | 10-50x over compute ray march |

**Cross-benefit**: TMU table lookup pattern transfers to every spring. RT solar
radiation transfers to groundSpring terrain analysis, healthSpring UV dosimetry.

### groundSpring (Geology / Seismology)

**Assignment**: Explore rasterizer, depth buffer, tessellation, TMUs.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| Rasterizer FEM mapping | Rasterizer | Mesh elements → grid points | 10-50x over compute loop |
| Z-buffer Voronoi | Depth buffer | Cone per seed → geological cell decomposition | 100x over Fortune's algorithm |
| Tessellation AMR | Tessellation HW | Error estimate → refined seismic mesh | Hardware-speed mesh refinement |
| TMU material properties | TMU | Rock/fluid property tables → lookup | 10-20x over compute evaluation |

**Cross-benefit**: Z-buffer Voronoi is directly useful for wetSpring cell decomposition,
ludoSpring procedural generation, neuralSpring feature clustering. Tessellation AMR
transfers to hotSpring thermal mesh, wetSpring flow mesh.

### healthSpring (Biomedical)

**Assignment**: Explore alpha blending, RT cores, video encoder, TMUs.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| Blend CT reconstruction | ROPs | Back-projection splatting → image accumulation | 5-10x over compute scatter |
| RT dosimetry | RT cores | Radiation transport through anatomy | 100-1000x over CPU Monte Carlo |
| Video encoder registration | NVENC/VCN | Motion estimation → image alignment | Hardware-speed registration |
| TMU pharmacokinetics | TMU | PK/PD curve lookup → drug concentration | 10-20x over analytical eval |

**Cross-benefit**: RT dosimetry transfers directly to hotSpring radiation transport,
airSpring atmospheric radiation. Video encoder registration transfers to any spring
doing time-series alignment.

### neuralSpring (Neural Networks / ML)

**Assignment**: Explore TMUs, alpha blending, tensor cores (DF64 variants), rasterizer.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| TMU activation functions | TMU | Precomputed sigmoid/GELU/swish → lookup | 10-20x over compute eval |
| Blend gradient accumulation | ROPs | Additive blend → distributed gradient reduce | 5-10x over atomic add |
| Tensor core DF64 | Tensor cores | Dekker arithmetic in MMA pipeline | Unknown — novel exploration |
| Rasterizer spatial attention | Rasterizer | Triangle-based attention mask generation | Unknown — novel exploration |

**Cross-benefit**: TMU activation function pattern is the most universally transferable —
every spring with a smooth function evaluation benefits. Tensor core DF64 could give
every spring a massive TFLOPS boost for mixed-precision linear algebra.

### ludoSpring (Game Science)

**Assignment**: Explore rasterizer, depth buffer, RT cores, alpha blending, TMUs.
See `whitePaper/baseCamp/exp076_gpu_graphics_hardware_for_game_science.md`.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|--------------|
| Rasterizer fog of war | Rasterizer | Wall triangles → visibility mask | 10-50x over per-tile ray march |
| Z-buffer pathfinding | Depth buffer | Cone at destination → distance heuristic | 100x over wavefront BFS |
| Blend influence maps | ROPs | Entity quads → accumulated influence | 5-10x over CPU loop |
| RT acoustic ray tracing | RT cores | Sound propagation through map geometry | 1000x over analytical model |
| TMU engagement curves | TMU | Fitts/Hick/DDA precomputed → lookup | 5-20x over analytical eval |
| Compute-shader rendering | Shader cores | DDA raycaster → RGBA framebuffer | Closes the render gap |

**Cross-benefit**: Rasterizer visibility directly transfers to airSpring terrain analysis,
groundSpring line-of-sight. RT acoustic transfers to airSpring environmental acoustics.
Compute-shader rendering benefits petalTongue and every spring that wants visual output.

---

## Exploration Protocol

Every spring follows the same protocol for hardware experiments:

1. **Create a baseCamp experiment**: Name it in your spring's numbering scheme
2. **Write a Python baseline**: The CPU reference implementation of the operation
3. **Write the compute-shader version**: The current best GPU approach (WGSL compute)
4. **Write the fixed-function version**: Use the target hardware unit
5. **Validate correctness**: Pixel-exact or within documented tolerances
6. **Measure throughput**: Operations/second for both approaches
7. **Document the mapping**: `domain_operation → hardware_unit → speedup`
8. **Hand off to wateringHole**: `{SPRING}_{VERSION}_HARDWARE_REPURPOSING_HANDOFF_{DATE}.md`
9. **Tag for absorption**: Identify which barraCuda dispatch op this becomes

Springs are encouraged to look at each other's experiments for cross-pollination.
If hotSpring validates RT core neighbor finding, wetSpring should immediately try
it for SPH neighbor lists. If ludoSpring validates Z-buffer distance fields,
groundSpring should try it for geological Voronoi tessellation. **Read the
handoffs. Replicate across domains. Evolve together.**

---

## Absorption Path

When a spring discovers a working repurposing technique:

1. **Validate locally**: Experiment in the spring's baseCamp, with Python baseline
2. **Document the mapping**: Which hardware unit, what it computes, measured speedup
3. **Cross-spring replication**: At least one other spring validates the same
   technique in their domain (confirms universality)
4. **Hand off to wateringHole**: `{SPRING}_{VERSION}_{TOPIC}_HANDOFF_{DATE}.md`
5. **barraCuda absorbs the primitive**: New dispatch op (e.g., `math.spatial.voronoi_zbuffer`)
6. **coralReef evolves the compiler**: If new pipeline states are needed (blend mode, depth func), coralReef learns to emit them
7. **toadStool evolves dispatch**: If graphics pipeline commands are needed alongside compute, toadStool learns to submit them
8. **All springs lean on upstream**: Replace local experiment with `barraCuda.math.spatial.voronoi_zbuffer`

The goal: **each hardware unit becomes a barraCuda dispatch op that any spring
can call without knowing the hardware details.** The spring sees
`math.spatial.neighbor_rt` and gets RT core acceleration. The spring sees
`math.spatial.voronoi_zbuffer` and gets depth buffer acceleration. barraCuda
and coralReef handle the hardware. Springs stay in their science.

---

## Infrastructure Portability — The Next Level

### The Portability Ladder

The ecosystem has built four levels of math portability:

```
Level 0: Python baseline           → portable across languages
Level 1: Rust CPU                  → portable across platforms
Level 2: WGSL compute shader       → portable across GPU vendors
Level 3: GPU infrastructure target → portable across hardware ON the card
Level 4: Silicon type              → portable across CPU / GPU / NPU / FPGA
```

Levels 0-2 are proven. Level 3 is the next frontier: **the same abstract
math, compilable to any hardware unit on the GPU die.** Level 4 follows
naturally (toadStool already orchestrates CPU/GPU/NPU dispatch).

### Why Run Math on the "Wrong" Hardware?

Running tensor cores on math that isn't matrix-shaped, or RT cores on
problems that aren't spatial, sounds wasteful. It isn't. It's the same
principle as running Python baselines to establish correctness before GPU
promotion.

**Running math on every hardware unit maps the performance surface.**

For each `(operation, hardware_unit, precision)` triple, you get a data
point: throughput, latency, accuracy. After enough experiments across all
springs, you know the full landscape. Then the compiler places operations
optimally — not from theory, but from measured data.

| Placement | What you learn |
|-----------|---------------|
| Yukawa force on shader cores (DF64) | Baseline throughput at 14-digit precision |
| Yukawa force on tensor cores (FP16) | Precision loss bounds, throughput ceiling at 4x rate |
| Yukawa force on tensor cores (TF32) | Precision vs throughput tradeoff at 2x rate |
| Yukawa force via TMU (potential table) | Lookup throughput when function is precomputable |
| Force accumulation on ROPs (blend) | Scatter-add throughput without atomics |
| Neighbor finding on RT cores (BVH) | Spatial query ceiling for particle methods |

Every "wrong" placement constrains the model. The "wrong" placements are
often the most informative — they find the crossover points and surprise
advantages.

### Tensor Cores for Science Math

Tensor cores execute one operation: `D = A × B + C` on small matrices
(4×4 to 16×16). On the RTX 3090:

| Precision | Tensor TFLOPS | Shader TFLOPS | Ratio |
|-----------|--------------|--------------|-------|
| FP16 | ~142 | 35.6 | 4.0x |
| TF32 | ~71 | 35.6 | 2.0x |
| BF16 | ~142 | 35.6 | 4.0x |
| INT8 | ~284 TOPS | — | — |

The question: **can your science be expressed as matrix multiplies?**

| Operation | Matrix reformulation | Tensor core viable? |
|-----------|---------------------|-------------------|
| CG solver (Ax=b) | Matrix-vector product: `A × x` | Yes — 60-70% of HMC runtime, biggest single win |
| Pairwise distances | `diag(A^T A) + diag(B^T B) - 2A^T B` | Yes — the O(N²) part of MD |
| Convolution | Toeplitz matrix × input vector | Yes — spectral analysis, filtering |
| FFT butterfly | Batched 2×2 rotation matrices | Yes — foundational for spectral methods |
| Finite differences | Banded matrix × state vector | Yes — PDE stencils |
| Neural network layers | `W × X + B` | Yes — literally designed for this |
| Dot products | `A^T × B` (1×N × N×1) | Yes — inner products, projections |
| Basis transforms | Change-of-basis matrix × coordinates | Yes — coordinate transforms, rotations |

For hotSpring's lattice QCD: the CG solver is pure matrix-vector products.
At TF32 (71 TFLOPS) vs DF64 on shader cores (3.24 TFLOPS), the solver
could run **~22x faster** for iterations where TF32 precision is
acceptable (e.g., pre-conditioning, initial convergence). The final
refinement uses DF64 for full precision. This mixed-precision CG is a
known technique in HPC — the hardware portability makes it automatic.

### The Dispatch Router Architecture

The evolution target for barraCuda + coralReef + toadStool:

```
Spring calls: barraCuda.math.pairwise.yukawa(particles, params)
                              |
                     Dispatch Router
              (operation shape + precision + hardware map)
                              |
         ┌──────┬──────┬──────┬──────┬──────┬──────┐
         ↓      ↓      ↓      ↓      ↓      ↓      ↓
      Shader  Tensor   RT    TMU    ROP   Raster  CPU
      cores   cores   cores  fetch  blend  fill  fallback
      (WGSL)  (MMA)  (BVH)  (tex)  (add)  (tri)  (Rust)
         |      |      |      |      |      |      |
         └──────┴──────┴──────┴──────┴──────┴──────┘
                              |
                    coralReef compiles each
                    to native ISA per unit
                              |
                    toadStool submits mixed
                    command stream to GPU
```

The router can:
1. **Select the best unit** for a given operation based on measured data
2. **Split across units** — force MMA on tensor cores + neighbor BVH on RT
   cores + potential lookup on TMU + accumulation on ROPs, all pipelined
3. **Fall back gracefully** — no tensor cores? Use shader cores. No RT
   cores? Use compute BVH. Always works, just at different throughput.

This is the infrastructure-portable equivalent of barraCuda's existing
CPU fallback. Today: GPU not available → CPU. Tomorrow: tensor cores not
available → shader cores. RT cores not available → compute BVH. The math
is the same; the hardware target changes.

### What No Existing Framework Does

- **CUDA**: Shader cores + tensor cores (via wmma). No RT/TMU/ROP/rasterizer
  for science.
- **Vulkan**: Shader cores + graphics pipeline. No tensor cores for science.
  No cross-unit dispatch.
- **OpenCL**: Shader cores only. No fixed-function access at all.
- **Kokkos**: Abstracts CPU/GPU. No hardware-unit-level targeting.

None of them offer a single dispatch that places different parts of a
computation on different hardware units simultaneously. The sovereign
stack — coralReef compiling to native ISA per unit, toadStool submitting
mixed command streams — can. This is a unique capability.

### Implications for the Sovereign Stack

This direction requires the sovereign compute pipeline to support more
than compute dispatch:

1. **Tensor core instructions**: coralReef emits `wmma`/`mma` (NVIDIA SASS)
   or `v_mfma`/`v_wmma` (AMD GFX) for MMA operations
2. **Graphics pipeline state objects**: Viewport, scissor, blend mode, depth
   function, rasterizer state — GPU register configurations, not shader code
3. **Draw commands**: `DRAW(vertex_count)` / `DRAW_INDEXED(index_count)` in
   the GPU command stream alongside `DISPATCH(groups)`
4. **RT pipeline state**: BVH build, ray generation, intersection testing
5. **Framebuffer management**: Render targets, depth/stencil attachments
6. **Mixed command streams**: Compute + graphics + RT in a single submission

On AMD (GFX9+), draw commands and MMA instructions are PM4 packets and ISA
instructions — coralReef already knows how to emit PM4 and GFX ISA.
On NVIDIA, draw commands use different GPFIFO classes but the submission
mechanism is the same PBDMA channel that compute uses. Tensor core MMA
instructions are part of the SM instruction set.

This is NOT a rewrite. It's an extension of the existing sovereign path.
The shader cores are the same silicon; the instructions and configuration
differ per target unit.

---

## What We Might Find

The DF64 discovery showed that repurposing yields not just alternative paths
but **unique advantages** — the Dekker/Knuth precision mix is something CUDA
and Kokkos cannot easily replicate. Each fixed-function unit might yield
similar advantages:

- The rasterizer's spatial query throughput may exceed compute shader
  equivalents by 10-100x for triangle-heavy problems
- The depth buffer's per-pixel reduction may beat atomic operations for
  nearest-neighbor problems
- The TMU's interpolation may be faster than compute shader texture loads
  because the hardware cache is purpose-built for 2D spatial locality
- RT cores' BVH traversal may beat hand-written kd-tree search by 10x+
  for sparse neighbor queries

The ecosystem's sovereign position — bare-metal access via coralReef and
toadStool, no API restrictions from Vulkan/CUDA — means we can combine these
units in ways that vendor APIs do not expose. A single dispatch could use
compute for physics, the rasterizer for binning, and the depth buffer for
distance fields, all in one pass. No existing framework allows this.

---

---

## The Compound Effect

The DF64 discovery alone closed 93% of the gap to Kokkos (27x → 3.7x). If
each of the seven remaining hardware units yields even a 3-5x improvement on
the operations it accelerates, the compound effect is transformative.

A single RTX 3090 running compute-only delivers 0.33 TFLOPS of native fp64.
With DF64: 3.24 TFLOPS. With the full hardware budget — shader cores, tensor
cores, RT cores, TMUs, ROPs, rasterizer, tessellator, all running in parallel
on different parts of the problem — the effective science throughput could
reach **50-100 TFLOPS equivalent**. That's a small HPC cluster in a single
PCIe slot.

And because the sovereign stack (coralReef + toadStool) gives bare-metal
access without Vulkan/CUDA API restrictions, we can combine these units in
ways no existing framework supports. A single dispatch using compute for
physics, the rasterizer for binning, RT cores for neighbors, TMUs for
lookups, and ROPs for accumulation — all in one pass. No existing framework
allows this. This is unique to ecoPrimals.

Every spring that explores, every experiment that validates, every handoff
that documents — they all compound. The more springs explore, the faster
the primals evolve, the more every spring benefits. This is the ecosystem
working as designed.

---

**Last Updated**: March 17, 2026 (updated — cross-benefit matrix, per-spring assignments, exploration protocol)
**Maintainer**: ludoSpring V24 / wateringHole
**License**: AGPL-3.0-or-later
