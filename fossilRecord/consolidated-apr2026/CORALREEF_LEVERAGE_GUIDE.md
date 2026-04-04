<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# coralReef Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 17, 2026
**Primal**: coralReef (Phase 10, Iteration 54)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how coralReef can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers.
Each primal in the ecosystem will produce an equivalent guide. Together,
these guides form a combinatorial recipe book for emergent behaviors.

coralReef provides **sovereign GPU shader compilation** — WGSL, SPIR-V,
and GLSL 450 compute shaders compiled to native GPU binaries (NVIDIA
SASS SM70–SM89, AMD GFX1030+) with full f64 transcendental support.
coralDriver provides userspace GPU dispatch via DRM ioctl (amdgpu,
nouveau, nvidia-drm, VFIO). coralGpu unifies compilation and dispatch
into a single vendor-agnostic API. Zero C dependencies, zero FFI, zero
vendor SDK.

**Philosophy**: The compiler is sovereign infrastructure. Any primal or
spring that needs GPU computation can compile and dispatch without
vendor lock-in, without C toolchains, and without trusting proprietary
binaries. Compilation is a capability, not a dependency — discovered at
runtime, invoked over IPC, and replaceable by any implementation that
speaks the same semantic methods.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `shader.compile.wgsl` | Compile WGSL source → native GPU binary for a target architecture |
| `shader.compile.spirv` | Compile SPIR-V binary → native GPU binary for a target architecture |
| `shader.compile.wgsl.multi` | Compile one WGSL shader for multiple GPU targets in a single request |
| `shader.compile.status` | Service name, version, supported architectures |
| `shader.compile.capabilities` | Dynamic enumeration: architectures, FMA policies, input languages |
| `health.check` | Service health, uptime, backend status |
| `health.liveness` | Liveness probe |
| `health.readiness` | Readiness probe |

**Transport**: JSON-RPC 2.0 over Unix socket (primary), tarpc/bincode
(high-perf primal-to-primal), TCP (fallback).

**Response format**: `CompileResponse` contains the native binary
(`bytes`), `CompilationInfo` (GPR count, shared memory bytes, barrier
count, workgroup size), and target architecture metadata.

---

## 1. coralReef Standalone

These patterns use coralReef alone — no other primals required.

### 1.1 WGSL → Native Binary Compilation

**For**: Any spring that authors GPU compute shaders in WGSL.

WGSL is the W3C standard GPU shading language. coralReef compiles it
directly to native machine code — no SPIR-V intermediate, no vendor
toolchain, no ptxas, no ROCm.

```
shader.compile.wgsl {
  source: "@compute @workgroup_size(256) fn main(...) { ... }",
  target: "sm86",
  fma_policy: "allow_fusion"
}
  → { binary: <SASS bytes>, info: { gpr_count: 24, shared_mem: 0, ... } }
```

The same source compiles to different targets:

```
shader.compile.wgsl { source, target: "sm70" }   → Volta SASS
shader.compile.wgsl { source, target: "sm86" }   → Ampere SASS
shader.compile.wgsl { source, target: "rdna2" }  → AMD GFX binary
```

**Spring applications**:

| Spring | What Gets Compiled |
|--------|-------------------|
| hotSpring | Lattice QCD kernels (SU3 gauge, Wilson plaquette), MD integrators (Verlet, cell-list), f64 transcendentals |
| neuralSpring | PRNG kernels (xoshiro), HMM forward/backward, spectral diagnostics, training infrastructure |
| groundSpring | Seismic FFT, calibration chain math, Anderson localization |
| wetSpring | Shannon entropy, DADA2 statistics, O₂-modulated Anderson |
| airSpring | Richards PDE solver, ET₀ models, statistics metrics |
| healthSpring | PK/PD model solvers, Hill dose-response, population dynamics |
| ludoSpring | Physics simulation, procedural generation, game telemetry analytics |
| primalSpring | Indirect validation — coralForge Pipeline graph (exp025) depends on ToadStool GPU dispatch, which uses coralReef for sovereign shader compilation |

> **coralForge evolution**: coralForge is now an emergent neural object composed via Pipeline graph, not a neuralSpring module. The math stays in neuralSpring, the composition is `coralforge_pipeline.toml`, validated by primalSpring exp025.

### 1.2 Multi-Target Cross-Vendor Compilation

**For**: Any spring that needs to compile once and dispatch to whatever
GPU hardware is available.

A single request compiles one shader for multiple architectures.
Results arrive in one response — no sequential compilation needed.

```
shader.compile.wgsl.multi {
  source: wgsl_source,
  targets: [
    { arch: "sm70" },
    { arch: "sm86" },
    { arch: "rdna2" }
  ],
  fma_policy: "no_contraction"
}
  → [
    { target: "sm70",  binary: <SASS>, info: { gpr_count: 28, ... } },
    { target: "sm86",  binary: <SASS>, info: { gpr_count: 24, ... } },
    { target: "rdna2", binary: <GFX>,  info: { gpr_count: 32, ... } }
  ]
```

**Why this matters**: Different GPUs may be present on the same
machine (e.g., AMD RX 6950 XT + NVIDIA RTX 3090). A spring that
discovers hardware at runtime can pre-compile for all available
targets in one IPC call.

### 1.3 f64 Transcendental Compilation

**For**: Any spring doing scientific computation that needs double
precision on consumer GPUs.

Consumer GPUs have limited native f64 support (1/32 rate on NVIDIA
Ampere, 1/16 on AMD RDNA2). coralReef provides full f64 transcendental
lowering — sqrt, exp, log, sin, cos, pow, and 20+ functions — using
software Newton-Raphson on NVIDIA (DFMA polynomial) and native
hardware instructions on AMD.

```
shader.compile.wgsl {
  source: "enable f64; ... exp(x_f64) ...",
  target: "sm86"
}
  → binary with software f64 exp2 lowering (Horner polynomial)

shader.compile.wgsl {
  source: "enable f64; ... exp(x_f64) ...",
  target: "rdna2"
}
  → binary with native v_fma_f64 / v_sqrt_f64 / v_rcp_f64
```

Full f64 function coverage: sqrt, rcp, exp2, log2, sin, cos, exp,
log, pow, tan, atan, asin, acos, sinh, cosh, tanh, asinh, acosh,
atanh, Complex64 arithmetic. All ~52-bit precision via Newton-Raphson
refinement on NVIDIA, hardware-native on AMD.

**Spring applications**:
- hotSpring: EOS fitting, Yukawa force, BCS superconductivity — all f64
- groundSpring: Seismic inversion, Anderson localization eigenvalues
- healthSpring: PK/PD exponentials, Hill function pharmacokinetics
- wetSpring: Shannon entropy log₂, diversity indices
- neuralSpring: Spectral diagnostics, eigenvalue decomposition

### 1.4 FMA Contraction Control

**For**: Any spring where numerical reproducibility matters more than speed.

Fused Multiply-Add (FMA) contracts `a*b + c` into a single instruction.
This is faster but changes rounding behavior. For reproducibility across
hardware, springs can enforce separate multiply and add.

```
shader.compile.wgsl {
  source: wgsl_source,
  target: "sm86",
  fma_policy: "separate"
}
  → OpFFma split into OpFMul + OpFAdd (deterministic rounding)

shader.compile.wgsl {
  source: wgsl_source,
  target: "sm86",
  fma_policy: "allow_fusion"
}
  → OpFFma preserved (hardware FMA, fastest path)
```

**Applications**: Bit-exact reproducibility (groundSpring validation),
cross-vendor numerical parity testing (hotSpring), regulatory-grade
determinism (healthSpring).

### 1.5 Capability Self-Description

**For**: Any primal or spring discovering coralReef at runtime.

Before compiling, callers can query what coralReef supports. This
enables adaptive behavior — compile for the best available target.

```
shader.compile.capabilities {}
  → {
    input_languages: ["wgsl", "spirv", "glsl"],
    architectures: [
      { vendor: "nvidia", targets: ["sm70", "sm75", "sm80", "sm86", "sm89"] },
      { vendor: "amd", targets: ["rdna2"] }
    ],
    fma_policies: ["allow_fusion", "no_contraction", "separate"],
    multi_target: true,
    max_targets: 64,
    f64_support: true
  }
```

**Spring pattern**: Query capabilities, intersect with discovered
hardware, compile for the intersection. Graceful degradation when
a target architecture isn't supported.

### 1.6 SPIR-V and GLSL Input

**For**: Springs migrating from existing GPU compute ecosystems.

coralReef accepts SPIR-V binary (for interop with existing toolchains)
and GLSL 450 compute (for absorbing legacy GPU libraries).

```
shader.compile.spirv { binary: <SPIR-V bytes>, target: "sm86" }
  → native binary (same pipeline as WGSL, different frontend)

// GLSL is compile-time only (not exposed over IPC, used via library API)
compile_glsl("layout(local_size_x=256) in; void main() { ... }", target)
  → native binary
```

Three input languages feed the same optimization and encoding pipeline.
The binary output is identical regardless of input language for
semantically equivalent shaders.

### 1.7 coralDriver — Direct GPU Dispatch (Library API)

**For**: Any Rust crate that wants direct GPU dispatch without IPC.

coralDriver is a library crate (not an IPC service) providing userspace
GPU dispatch via pure Rust DRM ioctl. Four driver backends:

```
coralGpu::GpuContext::auto()      → auto-detect GPU, sovereign default
coralGpu::GpuContext::from_vfio() → VFIO direct BAR0+DMA dispatch

// Driver preference (runtime, not compile-time):
//   vfio → nouveau → amdgpu → nvidia-drm
// Override: CORALREEF_DRIVER_PREFERENCE=nvidia-drm,amdgpu
```

| Backend | GPU | Driver | Sovereignty |
|---------|-----|--------|-------------|
| VFIO | NVIDIA | None (direct BAR0) | Maximum — no kernel GPU driver |
| nouveau | NVIDIA | nouveau (open) | High — open-source DRM |
| amdgpu | AMD | amdgpu (open) | High — open-source DRM |
| nvidia-drm | NVIDIA | nvidia (proprietary) | Compatible — vendor driver |

**Full dispatch pipeline** (library API):

```rust
let ctx = GpuContext::auto()?;
let binary = ctx.compile_wgsl(source, options)?;
let input = ctx.alloc(size)?;
ctx.upload(input, &data)?;
let output = ctx.alloc(size)?;
ctx.dispatch(&binary, &[input, output], workgroups, &shader_info)?;
ctx.sync()?;
let result = ctx.readback(output)?;
```

---

## 2. Sovereign Compute Trio Compositions

The **Sovereign Compute Trio** (coralReef + toadStool + barraCuda) forms
the GPU computation pipeline:

```
barraCuda (Math Engine)       — WGSL shader authoring, 786 kernels
      ↓
coralReef (Compiler)          — WGSL → native GPU binary, f64 lowering
      ↓
toadStool (Dispatch)          — Hardware discovery, workload routing, GPU lifecycle
      ↓
GPU hardware                  — NVIDIA / AMD / Intel (future)
```

coralReef sits at the center. It receives WGSL from above (barraCuda)
and produces native binaries consumed below (toadStool dispatch).
It is the translation layer — the point where portable math becomes
sovereign machine code.

### 2.1 coralReef + barraCuda: Full Math → Binary Pipeline

**The core compilation pattern.** barraCuda authors WGSL shaders for
scientific computation. coralReef compiles them to native GPU binaries.

```
1. barraCuda selects kernel (e.g., "yukawa_force_celllist_f64")
2. shader.compile.wgsl {
     source: barraCuda_wgsl_source,
     target: discovered_gpu_arch,
     fma_policy: precision_strategy.fma_policy()
   }
   → { binary, info: { gpr_count, shared_mem, barrier_count, workgroup } }
3. barraCuda dispatches binary via coralDriver or toadStool
```

**Precision routing**: barraCuda's `Fp64Strategy` (Native / DoubleFloat /
F32Only) determines which WGSL variant to send and which `fma_policy` to
request. coralReef compiles whatever it receives — the precision decision
is barraCuda's domain.

**Kernel caching**: `KernelCacheEntry` (serde-serializable) stores
compiled binaries keyed by `(wgsl_hash, target_arch, fma_policy)`.
`dispatch_precompiled()` bypasses compilation for cached binaries.

```
GpuContext::dispatch_precompiled(&cache_entry, &buffers, workgroups)?;
```

**Spring applications via barraCuda**:

| Spring | barraCuda Kernels → coralReef Compilation |
|--------|------------------------------------------|
| hotSpring | su3_gauge_force_f64, wilson_plaquette_f64, yukawa_force_celllist_f64, batched_hfb_energy_f64 |
| neuralSpring | xoshiro128ss PRNG, HMM viterbi/backward, attention kernels, ESN reservoir |
| groundSpring | FFT, Anderson localization, calibration statistics |
| wetSpring | Shannon entropy, DADA2 reduction kernels, diversity statistics |
| airSpring | Richards PDE solver, ET₀ energy balance |
| healthSpring | Hill dose-response, population PK, Wright-Fisher dynamics |
| ludoSpring | Physics collision, procedural noise, game analytics reduction |

### 2.2 coralReef + toadStool: Hardware-Aware Compilation

**Compilation adapts to discovered hardware.** toadStool discovers GPU
hardware and reports capabilities. coralReef compiles for the exact
target — not a generic profile.

```
1. toadStool discovers GPU:
   compute.discover {} → [
     { vendor: "nvidia", arch: "sm86", vram: "24GB", driver: "nouveau" },
     { vendor: "amd", arch: "rdna2", vram: "16GB", driver: "amdgpu" }
   ]

2. coralReef compiles for discovered targets:
   shader.compile.wgsl.multi {
     source: wgsl,
     targets: [{ arch: "sm86" }, { arch: "rdna2" }]
   }
   → binaries for both GPUs

3. toadStool dispatches to the optimal GPU:
   compute.dispatch { binary: sm86_binary, device: nvidia_gpu }
```

**Power-aware compilation**: toadStool's `PowerManager` (from the glow
plug discovery) can signal GPU readiness. coralReef can pre-compile
while toadStool warms the GPU — hiding compilation latency behind
power-up latency.

**Firmware-aware dispatch**: coralReef's `FirmwareInventory` knows which
GPUs are compute-viable (have GR + PMU/GSP firmware). toadStool can
query `compute_viable()` before requesting compilation for a specific
target.

### 2.3 coralReef + barraCuda + toadStool: NVVM Poisoning Bypass

**The sovereignty killer feature.** NVIDIA's proprietary naga → SPIR-V →
NVVM pipeline has a device-killing bug with f64 transcendentals
(DF64 Yukawa force shader). The wgpu device is permanently poisoned —
no further dispatches succeed.

The sovereign path bypasses this entirely:

```
Standard path (poisoned):
  WGSL → naga → SPIR-V → NVVM (proprietary) → SASS → GPU → DEVICE DEATH

Sovereign path (clean):
  WGSL → coralReef → SASS (direct) → coralDriver → GPU → RESULT

Same shader, same f64 precision, no vendor toolchain, no poisoning.
```

This unlocks 3-12x throughput on consumer GPUs by enabling DF64
emulation paths that the proprietary pipeline cannot handle. Validated
for SM70 (Volta), SM86 (Ampere), SM89 (Ada Lovelace), and RDNA2.

**Spring impact**: Any spring using f64 GPU math via barraCuda benefits
automatically. hotSpring's Yukawa force and BCS superconductivity
shaders — the exact workloads that kill NVVM — compile cleanly through
the sovereign path.

### 2.4 coralReef in the Trio: Responsibility Boundaries

| Concern | Owner |
|---------|-------|
| WGSL shader authoring | barraCuda |
| Precision strategy (DF64 / Native / F32Only) | barraCuda |
| Compilation to native binary | **coralReef** |
| f64 transcendental lowering | **coralReef** |
| FMA contraction policy enforcement | **coralReef** |
| Multi-target compilation | **coralReef** |
| Hardware discovery | toadStool |
| GPU power management | toadStool |
| Workload dispatch / scheduling | toadStool |
| Direct DRM/VFIO dispatch (library) | **coralReef** (coralDriver) |

---

## 3. coralReef + Other Primals

### 3.1 coralReef + LoamSpine: Compilation Provenance

**Every compilation result can be committed permanently.**

```
1. shader.compile.wgsl { source, target: "sm86" }
   → { binary_hash, info }

2. entry.append { spine_id, entry_type: "DataAnchor",
     payload: {
       wgsl_hash: blake3(source),
       binary_hash: blake3(binary),
       target: "sm86",
       gpr_count: 24,
       fma_policy: "allow_fusion",
       compiler_version: "coralreef-0.10.45"
     }
   }
   → permanent record linking source → binary → target → compiler
```

Every binary traces back to its WGSL source, target architecture,
FMA policy, and compiler version. Bit-exact reproducibility is
verifiable: recompile the same WGSL with the same options and compare
binary hashes.

**Applications**: Certified numerical results (hotSpring lattice QCD),
regulatory GPU computation chains (healthSpring PK models),
reproducibility proofs for published results (any spring).

### 3.2 coralReef + sweetGrass: Shader Attribution

**Who authored the shader? Who compiled it? Who validated the result?**

```
1. braid.create {
     agents: [
       { did: "did:eco:hotspring", role: "ShaderAuthor" },
       { did: "did:eco:coralreef", role: "Compiler" },
       { did: "did:eco:toadstool", role: "Dispatcher" }
     ],
     activity: { type: "sovereign_compilation" },
     entity: { wgsl_hash, binary_hash, result_hash }
   }
   → braid_id (attribution chain: author → compiler → dispatcher)
```

Combined with LoamSpine, the attribution braid is committed permanently.
The full provenance chain (shader source → compilation → dispatch →
result) is attributable and auditable.

**Applications**: Publication credit for shader optimizations
(neuralSpring ML kernels), certification of validated computation
pipelines (healthSpring), multi-spring collaboration attribution
(hotSpring provides physics, coralReef compiles, groundSpring validates).

### 3.3 coralReef + rhizoCrypt: Compilation Session Memory

**Track the compilation exploration process, not just the result.**

When a spring iterates on shader optimization (trying different targets,
FMA policies, workgroup sizes), rhizoCrypt records the ephemeral
exploration. The winning configuration dehydrates to LoamSpine.

```
1. dag.create_session { metadata: { purpose: "optimize_yukawa_kernel" } }
   → session_id

2. (iterate compilations)
   shader.compile.wgsl { source, target: "sm86", fma_policy: "allow_fusion" }
   dag.append_vertex { binary_hash, gpr_count: 28, timing: "747ms" }

   shader.compile.wgsl { source_v2, target: "sm86", fma_policy: "separate" }
   dag.append_vertex { binary_hash_v2, gpr_count: 24, timing: "612ms" }

3. dag.dehydrate { session_id }  → select winner
4. commit.session → permanent record of the optimized result
```

**Applications**: Shader optimization history (neuralSpring auto-tuning),
compilation regression detection (hotSpring CI), architecture
comparison studies (any spring evaluating NVIDIA vs AMD performance).

### 3.4 coralReef + Songbird: Compiler Discovery

**Springs discover the shader compiler at runtime via capability.**

```
discovery.query { capability: "shader.compile" }
  → [ { primal: "coralreef-abc123", socket: "/run/biomeos/coralreef.sock" } ]

shader.compile.capabilities {}
  → { architectures: [...], f64_support: true, ... }
```

coralReef never hardcodes other primal names. Other primals never
hardcode coralReef's address. Discovery is mutual, symmetric, and
capability-based. If coralReef is not running, springs fall back
to wgpu or skip GPU compilation entirely.

### 3.5 coralReef + Squirrel: AI-Guided Compilation

**Squirrel can analyze compilation patterns and suggest optimizations.**

```
1. (accumulate compilation metadata over time)
   - kernel sizes, GPR counts, timing, cache hit rates

2. ai.analyze { context: compilation_pattern_summary }
   → { suggestions: [
     "kernel X compiles 3x faster on RDNA2 than SM86 — prefer AMD",
     "workgroup_size(128) reduces GPR pressure for kernel Y by 15%",
     "FMA separate mode adds 8% overhead on SM70 but zero on SM86"
   ]}
```

**Applications**: Auto-tuning compilation flags (neuralSpring),
hardware routing optimization (toadStool + Squirrel), identifying
compilation bottlenecks across the shader corpus.

### 3.6 coralReef + biomeOS: Compilation as a Neural API Capability

**biomeOS routes compilation requests via `capability.call`.**

```rust
let bridge = NeuralBridge::discover()?;

let result = bridge.capability_call("shader", "compile.wgsl", &json!({
    "source": wgsl_source,
    "target": "sm86",
    "fma_policy": "allow_fusion"
}))?;

let binary: Vec<u8> = result["binary"].as_bytes();
let gpr_count: u32 = result["info"]["gpr_count"].as_u32();
```

Springs never import coralReef directly. They discover the `shader`
capability via biomeOS and call `compile.wgsl`. If coralReef is
replaced by another compiler, the spring code is unchanged.

### 3.7 coralReef + petalTongue: Compilation Visualization

**Visualize compilation pipelines, binary sizes, and register pressure.**

```
visualization.render {
  grammar: {
    data: compilation_results,
    geom: "bar",
    x: "target_arch",
    y: "binary_size_bytes",
    color: "fma_policy",
    facet: "shader_name"
  }
}
```

**Applications**: Cross-vendor binary size comparison, GPR pressure
heatmaps across architectures, compilation time benchmarks, shader
corpus coverage dashboards.

### 3.8 coralReef + skunkBat: Compilation Integrity

**Detect anomalous compilation patterns.**

```
(skunkBat monitors compilation requests)
  → alert if unexpected target architectures appear
  → alert if compilation rate spikes (possible abuse)
  → alert if binary hashes change for identical inputs
     (compiler determinism violation)
```

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining coralReef
with multiple primals simultaneously.

### 4.1 Sovereign Science Pipeline

**Springs**: hotSpring/wetSpring/any + barraCuda + coralReef + toadStool + LoamSpine + sweetGrass

The full sovereign science pipeline — from hypothesis to permanently
attributed, GPU-computed, vendor-independent results:

```
1. Spring authors computation (hotSpring: Yukawa force kernel)
2. barraCuda provides WGSL shader (786-kernel library)
3. coralReef compiles → native binary (no vendor SDK)
4. toadStool dispatches to discovered GPU (no vendor driver required)
5. Result verified by spring
6. rhizoCrypt records exploration DAG
7. LoamSpine commits final result permanently
8. sweetGrass attributes all contributors
```

Every step is pure Rust, auditable, and permanently recorded. The
result is a scientific computation that can be reproduced on any
supported GPU, with full provenance from WGSL source to final number.

**Domain applications**:
- **hotSpring + DOE**: Lattice QCD equation of state with full
  compilation provenance — every plaquette traces back to WGSL source
- **healthSpring + FDA**: PK/PD model computation with certified
  compiler, auditable binary, signed result
- **groundSpring + USGS**: Seismic inversion with bit-exact
  reproducibility certificates across hardware vendors

### 4.2 Cross-Vendor Parity Certification

**Springs**: any + coralReef + toadStool + LoamSpine

Compile the same shader for NVIDIA and AMD, dispatch on both, compare
results, and commit the parity proof:

```
1. shader.compile.wgsl.multi {
     source: kernel,
     targets: [{ arch: "sm86" }, { arch: "rdna2" }]
   }
   → nvidia_binary, amd_binary

2. toadStool dispatches nvidia_binary on RTX 3090
   toadStool dispatches amd_binary on RX 6950 XT
   → nvidia_result, amd_result

3. Compare: |nvidia_result - amd_result| < tolerance

4. entry.append { spine_id, entry_type: "Custom",
     payload: {
       type_uri: "coralreef://parity-certificate",
       wgsl_hash, nvidia_hash, amd_hash,
       nvidia_result_hash, amd_result_hash,
       max_ulp_difference: 2,
       status: "PASS"
     }
   }
   → permanent cross-vendor parity certificate
```

**Applications**: Validating that physics results are hardware-
independent (hotSpring), certifying numerical stability across vendors
(groundSpring), proving clinical computation is not hardware-biased
(healthSpring).

### 4.3 Hot-Swap Compiler Evolution

**Springs**: any + coralReef + biomeOS + NestGate

Because coralReef is discovered by capability (not by name), a new
compiler version can be deployed without restarting springs:

```
1. coralReef v45 running → springs compile via capability.call
2. coralReef v46 deployed → registers same capabilities
3. biomeOS routes new requests to v46
4. Old binaries still valid (cached in NestGate by content hash)
5. Springs recompile on next cache miss → get v46 binaries
```

The compiler evolves independently of its consumers. Binary
compatibility is maintained by the ISA — SASS SM86 is SASS SM86
regardless of which compiler produced it.

### 4.4 GPU Kernel Marketplace

**Springs**: any + coralReef + barraCuda + LoamSpine + BearDog + sweetGrass

Pre-compiled GPU binaries as tradeable, attributed, certified assets:

```
1. neuralSpring authors attention_f64.wgsl
2. coralReef compiles for all available targets
3. Binaries stored in NestGate (content-addressed)
4. LoamSpine mints certificates per binary:
   certificate.mint { type: "CompiledKernel",
     metadata: { wgsl_hash, target: "sm86", perf_profile: "..." } }
5. sweetGrass attributes neuralSpring as kernel author
6. hotSpring discovers kernel via capability → loans certificate → uses binary
7. Attribution flows back to neuralSpring
```

**Applications**: Cross-spring kernel reuse (hotSpring uses
neuralSpring's FFT kernel), compiled binary caching across the
ecosystem, shader IP with attribution tracking.

### 4.5 Adaptive Precision Routing

**Springs**: hotSpring/any + barraCuda + coralReef + toadStool

Different hardware has different f64 throughput. The trio adapts
precision strategy per GPU:

```
1. toadStool discovers:
   - RTX 3090 (SM86): f64 rate = 1/32 of f32
   - RX 6950 XT (RDNA2): f64 rate = 1/16 of f32
   - Titan V (SM70): f64 rate = 1/2 of f32

2. barraCuda selects precision:
   - RTX 3090: DF64 emulation (uses f32 cores, ~3x throughput vs native f64)
   - RX 6950 XT: Native f64 (1/16 rate, but no emulation overhead)
   - Titan V: Native f64 (1/2 rate, hardware strength)

3. coralReef compiles with matching strategy:
   - RTX 3090: WGSL with DF64 preamble → f32 SASS (software f64)
   - RX 6950 XT: WGSL with enable f64 → GFX (native v_fma_f64)
   - Titan V: WGSL with enable f64 → SASS (native DFMA)
```

The spring doesn't know or care about the precision routing. It
asks for f64 computation and gets the optimal path for each GPU.

### 4.6 Compilation-as-a-Service for Game Worlds

**Springs**: ludoSpring + coralReef + toadStool + petalTongue

Real-time shader compilation for dynamic game content:

```
1. ludoSpring generates procedural shader (terrain, weather, physics)
2. coralReef compiles in <100ms (hot path, cached on second compile)
3. toadStool dispatches to GPU
4. petalTongue renders result
5. Player interacts → new shader variant → repeat
```

**Applications**: Procedural terrain shaders that adapt to player
exploration, physics simulation shaders compiled for exact hardware,
real-time shader hot-reloading during game development.

### 4.7 Distributed Compilation Farm

**Springs**: any + coralReef + Songbird + biomeOS

Multiple coralReef instances across machines, discovered via Songbird:

```
discovery.query { capability: "shader.compile" }
  → [
    { primal: "coralreef-host-a", arch: ["sm86", "rdna2"] },
    { primal: "coralreef-host-b", arch: ["sm70", "sm89"] }
  ]

biomeOS routes compilation to the instance that supports the target:
  sm86 request → host-a
  sm70 request → host-b
```

**Applications**: CI/CD shader compilation across heterogeneous build
farms, pre-compilation of large shader corpora (barraCuda's 786
kernels × N targets), distributed test compilation.

### 4.8 Sovereign Reproducibility Proofs

**Springs**: any + coralReef + LoamSpine + BearDog + rhizoCrypt

Prove that a published result is bit-exact reproducible:

```
1. Original computation:
   shader.compile.wgsl { source, target, fma_policy }
   → binary_hash_original, result_hash_original
   commit.session → LoamSpine entry (permanent)

2. Reproduction attempt (different time, different machine):
   shader.compile.wgsl { same source, same target, same fma_policy }
   → binary_hash_repro  (should match binary_hash_original)
   dispatch → result_hash_repro

3. Verification:
   binary_hash_original == binary_hash_repro
     → compiler is deterministic ✓
   result_hash_original == result_hash_repro
     → computation is reproducible ✓

4. BearDog signs the proof
5. LoamSpine commits as sealed reproducibility certificate
```

**Applications**: Journal-quality reproducibility badges for GPU
computations, certified regression test suites, regulatory submission
of validated computation chains.

---

## 5. Integration Patterns for Springs

### Minimal Integration (IPC only)

Add to your spring's `Cargo.toml` under an optional feature:

```toml
[dependencies]
neural-api-client-sync = { path = "../../phase2/biomeOS/crates/neural-api-client-sync", optional = true }

[features]
gpu-compile = ["neural-api-client-sync"]
```

Then call via the Neural API bridge:

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;

// Check if coralReef is available
let caps = bridge.capability_call("shader", "compile.capabilities", &json!({}))?;
let targets: Vec<String> = caps["architectures"].as_array()
    .iter().flat_map(|a| a["targets"].as_array()).flatten()
    .map(|t| t.as_str().to_string()).collect();

// Compile for best available target
let result = bridge.capability_call("shader", "compile.wgsl", &json!({
    "source": wgsl_source,
    "target": targets[0],
    "fma_policy": "allow_fusion"
}))?;

let binary: Vec<u8> = result["binary"].as_bytes();
let gpr_count: u32 = result["info"]["gpr_count"].as_u32();
```

The spring never imports coralReef directly. If coralReef is not
running, the capability query returns empty and the spring gracefully
degrades (e.g., falls back to CPU computation or wgpu).

### Library Integration (Direct Rust API)

For primals that need compilation without IPC overhead:

```toml
[dependencies]
coral-reef = { path = "../../coralReef/crates/coral-reef" }
coral-gpu = { path = "../../coralReef/crates/coral-gpu", optional = true }

[features]
sovereign-dispatch = ["coral-gpu"]
```

```rust
use coral_reef::{compile_wgsl, CompileOptions, FmaPolicy};
use coral_reef::gpu_arch::GpuTarget;

let options = CompileOptions {
    target: GpuTarget::nvidia(86),
    fma_policy: FmaPolicy::AllowFusion,
    ..Default::default()
};

let result = compile_wgsl(wgsl_source, &options)?;
// result.binary, result.info.gpr_count, result.info.shared_mem_bytes
```

### Deploy Graph (biomeOS orchestration)

For automated compute pipelines:

```toml
# biomeOS deploy graph: sovereign_compute.toml
[[graph.steps]]
name = "compile_shader"
capability = "shader"
operation = "compile.wgsl"
params = { source = "${WGSL_SOURCE}", target = "${GPU_ARCH}" }

[[graph.steps]]
name = "dispatch_kernel"
capability = "compute"
operation = "dispatch"
depends_on = ["compile_shader"]
params = { binary = "${compile_shader.binary}", device = "${GPU_DEVICE}" }

[[graph.steps]]
name = "commit_result"
capability = "commit"
operation = "session"
depends_on = ["dispatch_kernel"]
```

---

## 6. What coralReef Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| WGSL shader authoring | barraCuda |
| Precision strategy selection | barraCuda |
| GPU hardware discovery | toadStool |
| GPU power management | toadStool |
| Workload scheduling | toadStool / biomeOS |
| Ephemeral working state | rhizoCrypt |
| Permanent records | LoamSpine |
| Attribution / provenance | sweetGrass |
| Content blob storage | NestGate |
| Signing / encryption | BearDog |
| Discovery / networking | Songbird |
| Visualization | petalTongue |
| AI inference | Squirrel |
| Security monitoring | skunkBat |
| Orchestration | biomeOS |

coralReef answers "what is the native GPU binary for this shader?"
It does not author shaders, discover hardware, manage GPU power,
schedule workloads, or store results. It compiles. Everything else is
discovered at runtime and composed by biomeOS. The compiler is a pure
function: source + target + options → binary + metadata.

---

## 7. Per-Spring Recipe Cards

These are concrete, novel leverage patterns for each spring. Not just
"compile my shader" — these are compositions where coralReef's unique
properties (multi-target, f64 lowering, FMA control, compilation metadata,
zero-vendor-dependency) enable things the spring couldn't do otherwise.

### 7.1 hotSpring — Lattice QCD Compilation Observatory

**Primals**: hotSpring + barraCuda + coralReef + LoamSpine + petalTongue

hotSpring runs the most computationally demanding shaders in the
ecosystem: lattice QCD HMC with SU(3) gauge updates, Wilson plaquettes,
and f64 fermion determinants. coralReef is uniquely positioned to provide
**compilation telemetry** that feeds back into physics optimization.

```
1. hotSpring requests compilation of su3_gauge_force_f64 for SM70 + SM86 + RDNA2
2. coralReef returns:
   - SM70:  binary (12,272 B), GPR: 42, shared_mem: 0, barriers: 0
   - SM86:  binary (11,840 B), GPR: 36, shared_mem: 0, barriers: 0
   - RDNA2: binary (10,496 B), GPR: 38, shared_mem: 0, barriers: 0

3. hotSpring observes: SM86 uses 6 fewer GPRs → higher occupancy → better latency hiding
4. hotSpring + Squirrel: correlate GPR pressure with physics accuracy per architecture
5. LoamSpine: commit the (shader, arch, GPR, occupancy, physics_result) tuple permanently
6. petalTongue: render GPR pressure heatmap across the lattice QCD shader corpus
```

**The novel insight**: Compilation metadata (GPR count, binary size) is
itself physics data. A shader that uses fewer GPRs achieves higher
occupancy, which affects the timescale of Monte Carlo thermalisation.
coralReef doesn't just compile — it produces metadata that becomes input
to the science.

**Pattern: Compilation-Guided Workgroup Tuning**

```
for wg_size in [64, 128, 256, 512]:
    rewrite wgsl with @workgroup_size(wg_size)
    compile for each target
    record (wg_size, gpr_count, binary_size, estimated_occupancy)
select wg_size that maximises occupancy for the target GPU
```

hotSpring can use coralReef's multi-target compilation to empirically
discover the optimal workgroup size per GPU architecture — without ever
dispatching. The compilation metadata is sufficient.

### 7.2 neuralSpring — Evolutionary Shader Optimisation

**Primals**: neuralSpring + barraCuda + coralReef + Squirrel + rhizoCrypt

neuralSpring already uses evolutionary algorithms (genetic, swarm,
Wright-Fisher). The novel pattern: **evolve the WGSL shader itself**.

```
1. neuralSpring generates N shader variants (different unroll factors,
   memory access patterns, loop structures)
2. coralReef compiles all N variants for the target architecture
3. Squirrel evaluates fitness: binary_size * gpr_pressure * estimated_latency
4. neuralSpring selects, mutates, recombines — next generation
5. rhizoCrypt tracks the exploration DAG (which mutations improved fitness)
6. After K generations: winning shader is dispatched via toadStool
```

coralReef is the **fitness evaluator** — compilation metadata is the
fitness function. The shader evolves without ever touching the GPU.
Only the winner dispatches.

**Pattern: Architecture-Specific Shader Breeding**

```
shader_v1 compiled for SM70 → GPR: 42
shader_v1 compiled for RDNA2 → GPR: 38

neuralSpring breeds two populations:
  - SM70-optimised lineage (minimise GPR for Volta's 65536 register file)
  - RDNA2-optimised lineage (minimise VGPR for RDNA2's 1024-per-CU pool)

Different selection pressures → different optimal shaders per architecture.
```

This is computational speciation: the same algorithm, compiled for
different hardware, produces architecture-adapted shader variants through
evolutionary pressure on compilation metadata.

### 7.3 groundSpring — Cross-Vendor Numerical Certification

**Primals**: groundSpring + coralReef + toadStool + LoamSpine + BearDog

groundSpring validates numerical methods. coralReef enables a pattern
that no vendor toolchain can: **bit-exact cross-vendor certification**.

```
1. groundSpring authors a calibration shader (known analytical solution)
2. coralReef compiles for SM70, SM86, SM89, RDNA2
3. toadStool dispatches each binary on its target hardware
4. groundSpring compares all 4 results against the analytical solution
5. groundSpring computes max ULP (Units in Last Place) difference
   across all vendors
6. BearDog signs the certification: "this shader produces results within
   N ULP of the analytical solution across 4 GPU architectures"
7. LoamSpine commits the signed certificate permanently
```

**The novel insight**: Because coralReef compiles to native code (not
PTX or SPIR-V intermediate), the binary IS the final form. There's no
vendor JIT between coralReef's output and the hardware. The compilation
is deterministic: same source + same target + same options = same binary.
This makes cross-vendor numerical certification possible.

### 7.4 wetSpring — Adaptive Diversity Index Pipelines

**Primals**: wetSpring + barraCuda + coralReef + toadStool

wetSpring computes Shannon entropy, Simpson's index, and Bray-Curtis
dissimilarity on metagenomic datasets. These are embarrassingly parallel
but precision-sensitive (log₂ in Shannon, division in Simpson's).

```
1. wetSpring probes hardware: "what GPUs are available?"
   toadStool responds: [Titan V (SM70, f64 1/2), RTX 5060 (SM89, f64 1/64)]

2. wetSpring decides:
   - Shannon entropy (log₂ f64): route to Titan V (native f64 throughput)
   - Simpson's index (f32 sufficient): route to RTX 5060 (more f32 cores)

3. coralReef compiles:
   - Shannon shader for SM70 with native f64
   - Simpson shader for SM89 with f32-only

4. toadStool dispatches each to the optimal GPU
```

**Pattern: Precision-Aware Multi-GPU Routing**

coralReef's `shader.compile.capabilities` + toadStool's hardware
discovery together enable precision-aware routing: f64-heavy shaders
go to the GPU with best f64 throughput, f32 shaders go to the GPU with
most cores. The routing decision is made at compile time based on
compilation metadata, before any dispatch occurs.

### 7.5 airSpring — Richards PDE Solver with JIT Parameterisation

**Primals**: airSpring + coralReef

airSpring models soil moisture using the Richards equation. The PDE
parameters (hydraulic conductivity K(θ), retention curve h(θ)) vary by
soil type. Instead of compiling a generic solver with runtime parameters,
airSpring can **JIT-compile a specialised solver**.

```
1. airSpring generates WGSL with soil-specific constants baked in:
   const K_sat: f32 = 0.0342;   // sandy loam
   const alpha: f32 = 0.036;
   const n: f32 = 1.56;

2. coralReef compiles → the constants are folded into immediate operands
   by the optimizer. No runtime lookup, no CBuf read — the parameters
   ARE the machine code.

3. When soil type changes (different field), regenerate WGSL and recompile.
   coralReef's compilation is fast enough for per-field specialisation.
```

**The novel insight**: Compilation is cheap. Constants baked into WGSL
become instruction immediates in the native binary — faster than reading
from a constant buffer. coralReef's compilation speed (<100ms for typical
shaders) makes JIT specialisation practical for domain-specific PDE solvers.

### 7.6 healthSpring — Certified PK/PD Model Chains

**Primals**: healthSpring + barraCuda + coralReef + LoamSpine + sweetGrass + BearDog

Pharmacokinetic/pharmacodynamic models need regulatory-grade reproducibility.
The full chain: model parameters → GPU computation → result must be
auditable and reproducible.

```
1. healthSpring parameterises a Hill dose-response model
2. barraCuda provides hill_dose_response_f64.wgsl
3. coralReef compiles with fma_policy: "separate" (IEEE 754 deterministic rounding)
4. Compilation metadata committed to LoamSpine:
   { wgsl_hash, binary_hash, target, fma_policy, compiler_version }
5. toadStool dispatches and returns results
6. sweetGrass creates attribution braid:
   { model_author: healthSpring, compiler: coralReef, dispatcher: toadStool }
7. BearDog signs the full chain
8. LoamSpine commits: signed (model → compilation → dispatch → result) certificate

Months later: regulatory reviewer asks "can you reproduce this result?"
Answer: recompile same WGSL with same options → same binary_hash.
Dispatch on any SM86 GPU → same result_hash. Proof is in LoamSpine.
```

### 7.7 ludoSpring — Procedural GPU Shader Generation

**Primals**: ludoSpring + coralReef + toadStool + petalTongue

ludoSpring generates procedural content for games. The novel pattern:
**procedurally generate the GPU shader itself**, not just the data.

```
1. ludoSpring's terrain generator produces a noise function specification:
   { octaves: 6, lacunarity: 2.1, persistence: 0.45, seed: 42 }

2. ludoSpring generates WGSL with the specific noise function baked in:
   @compute @workgroup_size(256)
   fn terrain(@builtin(global_invocation_id) gid: vec3<u32>) {
     let x = f32(gid.x) * 0.01;
     var height = 0.0;
     // 6 octaves, unrolled, constants inlined
     height += noise(x * 1.0) * 1.0;
     height += noise(x * 2.1) * 0.45;
     height += noise(x * 4.41) * 0.2025;
     // ... (fully unrolled by ludoSpring, not the GPU)
     output[gid.x] = height;
   }

3. coralReef compiles → constants folded, loops unrolled at IR level
4. toadStool dispatches → terrain heights computed on GPU
5. petalTongue renders the terrain

Player changes biome → new noise parameters → new WGSL → recompile.
```

**Pattern: Shader-as-Content**

The GPU shader IS the procedural content. Every biome, every weather
system, every physics variant is a different WGSL source. coralReef's
sub-100ms compilation makes this practical for interactive content.
ludoSpring + coralReef turns the compiler into a content pipeline.

---

## 8. Cross-Spring Shader Economy

When multiple springs produce and consume compiled shaders, an economy
emerges. coralReef enables this by producing content-addressable,
architecture-specific binaries with rich metadata.

### 8.1 Shared Kernel Library

**Primals**: any spring + barraCuda + coralReef + NestGate

Multiple springs need the same math operations: FFT, matrix multiply,
reduction, scan. Instead of each spring compiling independently:

```
1. barraCuda publishes 806 WGSL shaders as a kernel library
2. First spring to need fft_1d compiles via coralReef:
   shader.compile.wgsl { source: fft_1d, target: "sm86" }
   → binary_hash_abc123

3. NestGate stores: content_hash(binary) → binary blob
4. Second spring needs fft_1d for SM86:
   - Checks NestGate: content_hash(fft_1d, sm86, allow_fusion) → HIT
   - Skips compilation, uses cached binary
   - coralReef's dispatch_precompiled() accepts the cached binary directly
```

**The novel insight**: Compiled GPU binaries are content-addressable. The
key is `(wgsl_hash, target_arch, fma_policy, compiler_version)`. Any
spring that needs the same shader for the same target gets the same
binary — guaranteed by coralReef's deterministic compilation.

### 8.2 Cross-Spring Pipeline Composition

**Primals**: multiple springs + coralReef + toadStool

Springs can compose GPU pipelines where one spring's output is another's
input, all through compiled binaries on the GPU:

```
1. wetSpring: Shannon entropy shader → diversity_index buffer (on GPU)
2. neuralSpring: ESN reservoir update shader → takes diversity_index as input (on GPU)
3. groundSpring: calibration shader → validates ESN output (on GPU)

All three shaders compiled by coralReef.
All three dispatched sequentially by toadStool on the same GPU.
Data stays on GPU memory — zero CPU roundtrip between stages.
```

**Pattern: Multi-Spring GPU Pipeline**

```
toadStool allocates GPU buffers: [diversity_in, esn_state, calibration_out]
toadStool dispatches:
  shannon_binary(diversity_in)         → diversity_out (same buffer reused)
  esn_update_binary(diversity_out)     → esn_state
  calibration_binary(esn_state)        → calibration_out
toadStool readback: calibration_out → CPU
```

Three springs, three shaders, one GPU, zero copies between stages.
coralReef compiles all three; toadStool orchestrates the pipeline.
Each spring authored its own shader independently — the composition
emerges from compatible buffer layouts, not from shared code.

### 8.3 Compilation Diff for Shader Evolution

**Primals**: any spring + coralReef + rhizoCrypt

When a spring updates a shader, coralReef can quantify the impact:

```
shader_v1: compile → { gpr: 28, binary: 8192 B, barriers: 0 }
shader_v2: compile → { gpr: 24, binary: 7680 B, barriers: 0 }

Compilation diff:
  GPR pressure: -4 (better occupancy)
  Binary size: -512 B (smaller instruction footprint)
  Estimated throughput: +12% (from occupancy improvement)
```

rhizoCrypt records the evolution: `shader_v1 → shader_v2 → shader_v3`,
with compilation diffs at each step. Springs can track whether shader
optimisations actually improve the compiled output — without dispatching.

---

## 9. Wider Primal Compositions

Compositions involving 4+ primals where coralReef plays a non-obvious role.

### 9.1 The Full Compute Provenance Chain

**Primals**: spring + barraCuda + coralReef + toadStool + rhizoCrypt + LoamSpine + sweetGrass + BearDog

The maximal provenance pattern — every step from hypothesis to result
is captured, attributed, signed, and committed:

```
rhizoCrypt:  create session → "optimise yukawa kernel for Titan V"
barraCuda:   author WGSL shader (versioned)
coralReef:   compile → binary + metadata (GPR, shared_mem, binary_hash)
rhizoCrypt:  record compilation variant (target, fma_policy, metrics)
toadStool:   dispatch on Titan V → result
rhizoCrypt:  record dispatch (device, timing, power)
spring:      validate result against analytical solution
sweetGrass:  attribute { author, compiler, dispatcher, validator }
BearDog:     sign the attribution chain
LoamSpine:   commit the full provenance record permanently
rhizoCrypt:  dehydrate session (ephemeral exploration → permanent record)
```

Every step has a responsible primal. Every transition is over IPC.
The full chain is auditable: "who wrote this shader?" → barraCuda.
"Who compiled it?" → coralReef v0.10.51. "What hardware ran it?" →
Titan V SM70 via toadStool. "Who validated the result?" → hotSpring.
"Who signed it?" → BearDog with family key.

### 9.2 Sovereign CI/CD for Shader Libraries

**Primals**: barraCuda + coralReef + NestGate + skunkBat + biomeOS

Continuous compilation and validation of the shader corpus:

```
biomeOS orchestrates nightly:
  for each of barraCuda's 806 shaders:
    for each target in [sm70, sm86, sm89, rdna2]:
      coralReef compiles → binary
      NestGate stores binary by content hash
      skunkBat verifies:
        - binary_hash matches previous (determinism check)
        - binary_size within 5% of baseline (regression check)
        - GPR count within expected range (quality check)

skunkBat alerts on:
  - binary_hash changed for identical source (compiler non-determinism!)
  - binary_size increased >10% (possible regression)
  - new shader fails to compile (compiler gap)
```

coralReef is the build system for GPU binaries. NestGate is the artifact
store. skunkBat is the quality gate. biomeOS orchestrates the pipeline.
No Jenkins. No GitHub Actions. Pure primal composition.

### 9.3 Distributed Cross-Gate Compilation

**Primals**: coralReef + Songbird + biomeOS + toadStool

Multiple machines (gates) in the basement HPC, each with different GPUs:

```
gate-01: 2× Titan V (SM70) — coralReef instance knows SM70
gate-02: RTX 3090 (SM86) — coralReef instance knows SM86
gate-03: RX 6950 XT (RDNA2) — coralReef instance knows RDNA2

Spring requests: compile yukawa_force for [sm70, sm86, rdna2]

biomeOS routes via Songbird:
  sm70 request  → gate-01's coralReef (local GPU for validation)
  sm86 request  → gate-02's coralReef
  rdna2 request → gate-03's coralReef

Each coralReef instance compiles locally, can optionally validate
by dispatching on its own GPU via coralDriver.
```

**The novel insight**: Compilation doesn't need the target GPU present.
coralReef is a cross-compiler — it can produce SM86 binaries on a
machine that only has an AMD GPU. But when the target GPU IS present,
coralReef can compile AND dispatch locally for immediate validation.
Distributed compilation across gates with heterogeneous GPUs leverages
both capabilities.

### 9.4 sourDough + coralReef: Fermentation Simulation on GPU

**Primals**: sourDough + barraCuda + coralReef + toadStool

sourDough models microbial fermentation: population dynamics, metabolite
production, pH kinetics. These are systems of ODEs that parallelise
well on GPU — each simulation instance (different initial conditions,
different microbial strains) is independent.

```
1. sourDough parameterises 1000 fermentation simulations
   (varying inoculation density, temperature, substrate concentration)
2. barraCuda provides ode_integrator_f64.wgsl
3. coralReef compiles with fma_policy: "no_contraction"
   (fermentation models are stiff — numerical stability matters)
4. toadStool dispatches 1000 instances on GPU in one batch
5. sourDough collects results: population curves, metabolite profiles
6. Squirrel analyses: which fermentation conditions produce optimal
   lactic acid yield? → feeds back into sourDough's recipe database
```

### 9.5 skunkBat + coralReef: Compilation Anomaly Detection

**Primals**: skunkBat + coralReef

skunkBat monitors the ecosystem for anomalies. coralReef produces a
unique signal: compilation patterns.

```
Normal: 50 compilations/hour, all for SM70/SM86/RDNA2, <100ms each
Anomaly: 5000 compilations/hour for SM120 (unknown architecture!)
  → skunkBat alert: "unknown target architecture in compilation requests"

Normal: binary_hash stable for same source+target+options
Anomaly: binary_hash changed without source change
  → skunkBat alert: "compiler determinism violation — possible tampering"

Normal: compilation latency <200ms
Anomaly: compilation latency spikes to 30s
  → skunkBat alert: "compilation resource exhaustion — possible DoS"
```

coralReef's compilation is deterministic. Any deviation from deterministic
behaviour is a signal. skunkBat doesn't need to understand shaders — it
just monitors the invariants.

### 9.6 NestGate + coralReef: Content-Addressed Binary Store

**Primals**: NestGate + coralReef

NestGate's content-addressed storage is a natural fit for compiled
binaries:

```
binary_key = blake3(wgsl_source || target || fma_policy || compiler_version)

NestGate stores:
  binary_key → {
    binary: <native GPU bytes>,
    metadata: { gpr_count, shared_mem, binary_size, workgroup, target },
    provenance: { wgsl_hash, compiler_version, compilation_timestamp }
  }
```

Any primal that knows the key (source + target + options) can retrieve
the pre-compiled binary from NestGate without invoking coralReef at all.
fieldMouse deployments can use this pattern for edge GPU compute. This
turns NestGate into a global compilation cache for the ecosystem.

---

## 10. Anti-Patterns — What NOT to Do with coralReef

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|---------------|-------------------|
| Compiling at dispatch time in a hot loop | Compilation is ~50-200ms; dispatch is ~1ms | Compile once, cache the binary, dispatch many times |
| Hardcoding coralReef's socket path | Breaks multi-instance, multi-family deployment | Use capability discovery via biomeOS or `$XDG_RUNTIME_DIR/biomeos/` |
| Sending binary data over JSON-RPC | JSON base64 overhead is 33% | Use tarpc/bincode for binary-heavy paths between Rust primals |
| Requesting SM120 compilation (not yet supported) | Will return an error | Query `shader.compile.capabilities` first, intersect with available targets |
| Skipping FMA policy when reproducibility matters | Default is `allow_fusion` which is non-deterministic across runs | Explicitly set `fma_policy: "separate"` for certified computations |
| Treating coralReef as a runtime library in non-Rust primals | coralReef is a Rust crate; IPC is the cross-language boundary | Use JSON-RPC 2.0 — any language can call it |
| Compiling the same shader N times for the same target | Deterministic compiler = same output every time | Cache by `(wgsl_hash, target, fma_policy)` via NestGate or local HashMap |

---

## References

### Primal Leverage Guides (Companion Recipes)

- `wateringHole/BARRACUDA_LEVERAGE_GUIDE.md` — barraCuda: math engine, 806 WGSL shaders, precision routing
- `wateringHole/TOADSTOOL_LEVERAGE_GUIDE.md` — toadStool: hardware discovery, dispatch, VFIO, power management
- `wateringHole/LOAMSPINE_LEVERAGE_GUIDE.md` — LoamSpine: permanent records, provenance chains
- `wateringHole/RHIZOCRYPT_LEVERAGE_GUIDE.md` — rhizoCrypt: ephemeral DAG, session memory
- `wateringHole/SWEETGRASS_LEVERAGE_GUIDE.md` — sweetGrass: attribution braids, provenance metadata
- `wateringHole/BIOMEOS_LEVERAGE_GUIDE.md` — biomeOS: orchestration, Neural API, capability routing
- `wateringHole/PETALTONGUE_LEVERAGE_GUIDE.md` — petalTongue: visualisation, grammar of graphics
- `wateringHole/SQUIRREL_LEVERAGE_GUIDE.md` — Squirrel: AI inference, analysis, suggestions
- `wateringHole/RHIZOCRYPT_LEVERAGE_GUIDE.md` — rhizoCrypt: ephemeral memory, exploration DAGs

### Ecosystem Standards

- `wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` — Sovereign GPU stack plan
- `wateringHole/PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — Trio contracts
- `wateringHole/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — Provenance integration
- `wateringHole/CROSS_SPRING_SHADER_EVOLUTION.md` — Spring shader evolution
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — IPC naming conventions
- `wateringHole/PRIMAL_IPC_PROTOCOL.md` — Socket paths, discovery, transport

### Primal Specifications

- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue (14 primals)
- `whitePaper/gen3/SPRING_CATALOG.md` — Spring catalogue (8 springs)
- `whitePaper/gen3/primals/INTERACTIONS.md` — Interaction matrix and bonding model
- `whitePaper/gen3/primals/13_coralreef.md` — coralReef primal specification
- `whitePaper/gen3/primals/14_barracuda.md` — barraCuda primal specification
- `whitePaper/gen3/primals/05_toadstool.md` — toadStool primal specification
