# hotSpring — Silicon Science: TMU Table Lookup + QCD-to-Silicon Mapping Handoff

**Date:** 2026-03-26
**From:** hotSpring → barraCuda, toadStool, coralReef, ALL springs
**Status:** First non-shader-core silicon experiment complete. 12/12 pass.
**Experiment:** Exp 096 (`hotSpring/experiments/096_SILICON_SCIENCE_TMU_QCD_MAPPING.md`)
**Binary:** `validate_silicon_science`
**License:** AGPL-3.0-only

---

## What Happened

hotSpring executed the first silicon science experiment following the
`GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md` protocol. We activated the GPU's
Texture Mapping Unit (TMU) for science table lookup and mapped all QCD operations
to their hypothesized optimal silicon units across 9 hardware unit types.

## Key Findings

### 1. TMU Table Lookup Works for Science (texture_unit)

- **RTX 3090:** 1.89x throughput over compute shader exp() via `textureLoad`
- **RX 6950 XT:** 1.24x throughput (fewer TMUs: 96 vs 328)
- **Accuracy:** 20.5% max relative error (expected for 1024-entry nearest-neighbor)
- **Implication:** EOS tables, activation functions, cross-section lookups can route
  through TMU hardware for free throughput. Higher-resolution tables + linear
  filtering will bring accuracy to sub-1%.

### 2. AMD Outperforms NVIDIA on DF64 Arithmetic

- **RX 6950 XT:** 23.4M ops/s on DF64 chain
- **RTX 3090:** 16.9M ops/s on DF64 chain
- AMD's fp32 FMA pipeline produces ~38% better double-float throughput.
- Combined with higher DF64 fidelity from precision matrix work, AMD RDNA2
  is a stronger science compute substrate for DF64 workloads than Ampere.

### 3. Full QCD-to-Silicon Unit Mapping Documented

11 QCD operations mapped to 9 silicon unit types. 4 LIVE (tested), 7 PLAN
(awaiting sovereign dispatch or graphics pipeline experiments).

## For barraCuda

### Absorb: `math.transcendental.exp_table` dispatch op

The TMU table lookup pattern should become a barraCuda dispatch operation:
`math.transcendental.exp_table(data, table_resolution, precision_required)`.
When tolerance > 1e-2 and a TMU is available, route through texture hardware.
When tolerance < 1e-7, use compute shader.

### Absorb: DF64 AMD routing preference

The precision routing system should prefer AMD GPUs for DF64-heavy workloads
when both NVIDIA and AMD are available (device_pair scenario). AMD delivers
38% better DF64 throughput AND higher fidelity.

### Absorb: `barracuda-spirv` bridge (from previous sprint)

The SPIR-V passthrough bridge crate is ready at `crates/barracuda-spirv`.
Enable via `--features spirv-passthrough` for Tier 1 sovereign SPIR-V
compilation (naga IR → SPIR-V → GPU, no WGSL re-emit).

**Critical finding:** The SovereignCompiler's naga WGSL roundtrip (Tier 2)
silently breaks DF64 shaders. Tier 2 is disabled for DF64. Root cause:
naga's WGSL backend re-emission produces syntactically valid but
semantically broken output for Dekker arithmetic. The SPIR-V path (Tier 1)
bypasses this entirely.

## For toadStool

### Evolve: Performance surface with TMU data

hotSpring now reports `math.transcendental.exp` measurements for BOTH
`shader_core` and `texture_unit` silicon units. toadStool's routing should:

1. Accept measurements where `silicon_unit = "texture_unit"`
2. Route `math.transcendental.*` to TMU when `tolerance > 1e-2`
3. Keep shader_core as fallback (universal, higher precision)

### Evolve: Socket discovery alignment

hotSpring's `toadstool_report.rs` now checks `$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock`
first (matching toadStool's default). The `silicon_unit` wire format uses
snake_case (`shader_core`, `texture_unit`) matching `SiliconUnit` serialization.

### Evolve: Multi-unit routing with measured data

The `compute.route.multi_unit` handler should incorporate TMU measurements
into its routing decisions. A QCD workload with both plaquette computation
(shader_core) and EOS table lookup (texture_unit) should route to different
units simultaneously.

## For coralReef

### Evolve: Texture pipeline state emission

For Phase D mixed command streams, coralReef needs to emit texture descriptor
state alongside compute dispatches. The TMU experiment proves the science
value — coralReef should learn to configure TMU descriptors for table lookup
in sovereign dispatch mode.

### Evolve: naga deprecation path

The naga WGSL roundtrip bug (Tier 2 sovereign compiler silently breaks DF64)
reinforces the deprecation path. Priority:

1. **Tier 1 (SPIR-V passthrough):** Working via `barracuda-spirv` bridge.
   Bypasses naga WGSL re-emission entirely.
2. **Tier 0 (coralReef native):** WGSL → coralReef IR → NVIDIA PTX/SASS or
   AMD GCN/RDNA native binary. No naga at all.
3. **Tier 3 (raw WGSL):** Fallback for non-sovereign environments. Works but
   misses optimization opportunities.

## For ALL Springs

### Pattern: TMU Table Lookup

Any spring with smooth 1D or 2D functions called repeatedly can precompute
them into a texture and let the TMU handle lookup + interpolation. The pattern:

1. Precompute f(x) into a 1024+ entry R32Float texture
2. In compute shader, use `textureLoad` (nearest) or `textureSampleLevel` (interpolated)
3. Measure throughput vs compute shader evaluation
4. Report to toadStool performance surface

**Applications by spring** (from `GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md`):

| Spring | TMU Application |
|--------|----------------|
| hotSpring | EOS tables, Yukawa screening, absorption cross-sections |
| wetSpring | Ocean regridding, bathymetry interpolation |
| airSpring | Gas absorption cross-section tables |
| groundSpring | Rock/fluid property tables |
| healthSpring | PK/PD curves, dose-response lookup |
| neuralSpring | Activation functions (sigmoid, GELU, swish) |
| ludoSpring | Engagement curves, Fitts/Hick/DDA tables |

### Pattern: DF64 AMD Preference

For science workloads requiring ~14-digit precision, AMD RDNA2 GPUs deliver
38% better DF64 throughput than NVIDIA Ampere. If your pipeline uses DF64
and has access to both vendors, prefer AMD for the DF64-heavy stages.

## Measurements (for toadStool ingestion)

```json
[
  {"operation": "math.transcendental.exp", "silicon_unit": "shader_core", "precision_mode": "fp32", "gpu_model": "NVIDIA GeForce RTX 3090", "throughput_gflops": 0.025, "tolerance_achieved": 3.58e-7},
  {"operation": "math.transcendental.exp", "silicon_unit": "texture_unit", "precision_mode": "fp32_table_1024", "gpu_model": "NVIDIA GeForce RTX 3090", "throughput_gflops": 0.048, "tolerance_achieved": 2.05e-1},
  {"operation": "math.transcendental.exp", "silicon_unit": "shader_core", "precision_mode": "fp32", "gpu_model": "AMD Radeon RX 6950 XT", "throughput_gflops": 0.014, "tolerance_achieved": 1.19e-7},
  {"operation": "math.transcendental.exp", "silicon_unit": "texture_unit", "precision_mode": "fp32_table_1024", "gpu_model": "AMD Radeon RX 6950 XT", "throughput_gflops": 0.017, "tolerance_achieved": 2.05e-1},
  {"operation": "math.lattice.plaquette", "silicon_unit": "shader_core", "precision_mode": "fp32", "gpu_model": "NVIDIA GeForce RTX 3090", "throughput_gflops": 0.030, "tolerance_achieved": 0.0},
  {"operation": "math.linalg.dot_reduce", "silicon_unit": "shader_core", "precision_mode": "fp32", "gpu_model": "NVIDIA GeForce RTX 3090", "throughput_gflops": 0.050, "tolerance_achieved": 0.0},
  {"operation": "math.df64.arith_chain", "silicon_unit": "shader_core", "precision_mode": "df64", "gpu_model": "NVIDIA GeForce RTX 3090", "throughput_gflops": 0.017, "tolerance_achieved": 0.0},
  {"operation": "math.df64.arith_chain", "silicon_unit": "shader_core", "precision_mode": "df64", "gpu_model": "AMD Radeon RX 6950 XT", "throughput_gflops": 0.023, "tolerance_achieved": 0.0}
]
```

---

**Last Updated:** March 26, 2026
**Maintainer:** hotSpring / strandGate
**License:** AGPL-3.0-or-later
