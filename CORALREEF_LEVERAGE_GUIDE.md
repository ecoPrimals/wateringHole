<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# coralReef Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 15, 2026
**Primal**: coralReef (Phase 10, Iteration 47)
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

## References

- `wateringHole/LOAMSPINE_LEVERAGE_GUIDE.md` — Companion guide for LoamSpine
- `wateringHole/RHIZOCRYPT_LEVERAGE_GUIDE.md` — Companion guide for rhizoCrypt
- `wateringHole/SWEETGRASS_LEVERAGE_GUIDE.md` — Companion guide for sweetGrass
- `wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` — Sovereign GPU stack plan
- `wateringHole/PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — Trio contracts
- `wateringHole/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — Provenance integration
- `wateringHole/CROSS_SPRING_SHADER_EVOLUTION.md` — Spring shader evolution
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — IPC naming conventions
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/primals/13_coralreef.md` — coralReef primal specification
- `whitePaper/gen3/primals/14_barracuda.md` — barraCuda primal specification
- `whitePaper/gen3/primals/05_toadstool.md` — toadStool primal specification
