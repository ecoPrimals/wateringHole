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

## Per-Spring Investigation Guidance

Each spring should explore the units most relevant to their domain. Develop
experiments locally. When something works, document it in baseCamp and hand
off to barraCuda/coralReef for absorption.

### hotSpring (Physics / Thermodynamics)

**Priority targets**:
- RT cores for MD neighbor lists (replaces Verlet list construction)
- Rasterizer for particle-in-cell binning (PIC plasma simulation)
- Depth buffer for distance fields (level-set methods)
- TMUs for equation-of-state table lookups (material properties)
- Alpha blending for charge/mass deposition onto grids

### wetSpring (Fluid Dynamics / Ocean Science)

**Priority targets**:
- Rasterizer voxelization for obstacle geometry in CFD
- Alpha blending for SPH particle deposition
- TMUs for ocean data regridding (bilinear interpolation is the #1 operation)
- Depth buffer for free-surface tracking (level-set interface capture)
- Video encoder for trajectory compression

### airSpring (Atmospheric / Air Quality)

**Priority targets**:
- TMUs for atmospheric lookup tables (absorption coefficients, scattering)
- RT cores for solar radiation tracing through building geometry
- Alpha blending for Beer-Lambert optical depth accumulation
- Rasterizer for terrain shadow casting

### groundSpring (Geology / Seismology)

**Priority targets**:
- Rasterizer for FEM mesh-to-grid mapping
- Depth buffer for Voronoi tessellation (geological cell decomposition)
- Tessellation hardware for adaptive mesh refinement (seismic wave propagation)
- TMUs for material property table lookups

### healthSpring (Biomedical)

**Priority targets**:
- Alpha blending for CT reconstruction (back-projection splatting)
- RT cores for dosimetry (radiation transport through anatomy)
- Video encoder motion estimation for medical image registration
- TMUs for pharmacokinetic lookup tables

### neuralSpring (Neural Networks / ML)

**Priority targets**:
- TMUs for activation function approximation (store sigmoid/GELU in texture)
- Alpha blending for gradient accumulation
- Tensor cores (already used, but explore mixed-precision tricks like DF64)
- Rasterizer for spatial attention (which tokens attend to which regions?)

### ludoSpring (Game Science)

**Priority targets**:
- Rasterizer for fog-of-war computation (which tiles are visible from player?)
- RT cores for acoustic ray tracing (game audio propagation)
- Depth buffer for pathfinding distance fields
- Alpha blending for influence maps (sum of all entity influence radii)
- Tessellation for LOD in procedural terrain

---

## Absorption Path

When a spring discovers a working repurposing technique:

1. **Validate locally**: Experiment in the spring's baseCamp, with Python baseline
2. **Document the mapping**: Which hardware unit, what it computes, measured speedup
3. **Hand off to wateringHole**: `{SPRING}_{VERSION}_{TOPIC}_HANDOFF_{DATE}.md`
4. **barraCuda absorbs the primitive**: New dispatch op (e.g., `math.spatial.voronoi_zbuffer`)
5. **coralReef evolves the compiler**: If new pipeline states are needed (blend mode, depth func), coralReef learns to emit them
6. **toadStool evolves dispatch**: If graphics pipeline commands are needed alongside compute, toadStool learns to submit them
7. **All springs lean on upstream**: Replace local experiment with `barraCuda.math.spatial.voronoi_zbuffer`

---

## Implications for the Sovereign Stack

This direction has a strategic consequence: **the sovereign compute pipeline
must eventually support the graphics pipeline, not just compute dispatch.**

Currently, coralReef compiles WGSL to native GPU ISA and toadStool dispatches
compute workloads. To leverage the rasterizer, depth buffer, ROPs, and
tessellation hardware, the pipeline needs:

1. **Graphics pipeline state objects**: Viewport, scissor, blend mode, depth
   function, rasterizer state — these are GPU register configurations, not
   shader code
2. **Draw commands**: `DRAW(vertex_count)` / `DRAW_INDEXED(index_count)` in
   the GPU command stream alongside `DISPATCH(groups)`
3. **Framebuffer management**: Render targets, depth/stencil attachments

On AMD (GFX9+), draw commands are PM4 packets just like compute dispatches —
coralReef already knows how to emit PM4. On NVIDIA, draw commands use
different GPFIFO classes but the submission mechanism is the same PBDMA
channel that compute uses.

This is NOT a rewrite. It's an extension of the existing sovereign path.
The shader cores are the same; only the fixed-function configuration and
command types differ.

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

**Last Updated**: March 17, 2026
**Maintainer**: ludoSpring V24 / wateringHole
**License**: AGPL-3.0-or-later
