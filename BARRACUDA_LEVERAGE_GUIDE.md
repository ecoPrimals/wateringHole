<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 16, 2026
**Primal**: barraCuda v0.3.5 (Sprint 5)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how barraCuda can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

barraCuda provides **sovereign mathematical computation** — GPU-accelerated
scientific computing across any vendor's hardware using 816 WGSL shaders
compiled through wgpu. One source, any GPU, identical results. Pure Rust,
zero unsafe, zero C application dependencies.

**Philosophy**: Math is universal. A shader is just math. The execution
substrate (GPU, CPU, NPU, Android ARM) is a hardware implementation
detail — not a difference in universal math. barraCuda owns the math;
other primals own the hardware, the network, the storage, the identity.

---

## IPC Methods (Semantic Naming)

All methods follow `{namespace}.{domain}.{operation}` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `barracuda.device.list` | List available compute devices (GPU, CPU, NPU) |
| `barracuda.device.probe` | Probe device capabilities, f64 support, VRAM |
| `barracuda.health.check` | Health check (name, version, status, capabilities) |
| `barracuda.tolerances.get` | Numerical tolerances for a named operation |
| `barracuda.validate.gpu_stack` | GPU validation suite (shader compile + dispatch) |
| `barracuda.compute.dispatch` | Dispatch a WGSL compute shader with parameters |
| `barracuda.tensor.create` | Create a GPU-resident tensor |
| `barracuda.tensor.matmul` | Matrix multiply two tensors |
| `barracuda.fhe.ntt` | Number Theoretic Transform (FHE lattice crypto) |
| `barracuda.fhe.pointwise_mul` | Pointwise polynomial multiplication (FHE) |

**Transport**: JSON-RPC 2.0 over TCP/Unix socket (primary), tarpc/bincode
(high-throughput primal-to-primal), capability-based discovery.

---

## 1. barraCuda Standalone

These patterns use barraCuda alone — no other primals required.

### 1.1 Direct Library Dependency

**For**: Any spring that needs math, statistics, or GPU compute.

```toml
# Full (default) — everything
barracuda = { path = "../barraCuda/crates/barracuda" }

# Math + GPU only — no domain models (fastest compile)
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false, features = ["gpu"] }

# Pure CPU math — no GPU at all (sub-2s compile)
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false }
```

Springs get the full library at compile time. No IPC overhead, no
discovery, no runtime dependency on other primals. This is the simplest
and fastest integration path.

**Used by**: All 8 springs (hotSpring, airSpring, wetSpring, groundSpring,
neuralSpring, healthSpring, ludoSpring, primalSpring). primalSpring has
minimal barraCuda requirements — it validates coordination, not math. Its
contribution is validating that the coordination layer correctly composes
the primals that consume barraCuda.

### 1.2 GPU-Accelerated Statistics

**For**: Any spring running bootstrap CI, chi-squared, diversity indices,
or regression on large datasets.

```rust
use barracuda::stats::{bootstrap_ci, chi_squared_uniform_sigma, shannon};
use barracuda::stats::{BootstrapMeanGpu, HistogramGpu, HargreavesBatchGpu};
```

CPU path for small data, GPU path for batch. Same API, same results.
barraCuda auto-selects based on data size and device availability.

**Novel pattern**: Combine `BootstrapMeanGpu` (10,000 resamples on GPU in
milliseconds) with `JackknifeMeanGpu` for cross-validated uncertainty
estimation on datasets too large for CPU resampling.

### 1.3 Precision-Tiered Scientific Compute

**For**: Any spring that needs to control numerical precision per domain.

```rust
use barracuda::device::{PrecisionTier, PhysicsDomain, PrecisionBrain};

let brain = PrecisionBrain::new(&device);
let tier = brain.recommend(PhysicsDomain::LatticeQcd);
// tier = F64Precise (lattice QCD needs FMA-separate, bit-exact)
```

barraCuda's `PrecisionBrain` routes physics domains to the correct
precision tier (F32, DF64, F64, F64Precise) based on runtime hardware
probing. Springs don't need to know about GPU f64 quirks.

**Novel pattern**: A spring can ask "what precision can I get on this
hardware?" and adapt its algorithm — e.g., use stochastic rounding on
F32-only devices, or full DF64 on capable hardware.

### 1.4 Deterministic PRNG (CPU–GPU Parity)

**For**: Any spring needing reproducible stochastic simulations.

```rust
use barracuda::rng::Xoshiro128StarStar;

let mut rng = Xoshiro128StarStar::new(42);
let u = rng.next_f64();        // [0, 1)
let n = rng.next_normal();     // N(0, 1)
```

The CPU `Xoshiro128StarStar` matches the GPU WGSL xoshiro128** stream
bit-for-bit. A spring can generate reference sequences on CPU and verify
GPU Monte Carlo results produce identical trajectories for the same seed.

### 1.5 FHE on GPU

**For**: bearDog (crypto), any spring needing encrypted computation.

```rust
use barracuda::ops::fhe::{NttGpu, PointwiseMulGpu};
```

barraCuda is the only cross-vendor FHE GPU implementation in existence —
32-bit emulation of 64-bit modular arithmetic via WGSL. Any spring can
run NTT, INTT, and pointwise modular multiplication on any GPU vendor.

**Novel pattern**: Encrypted statistical analysis — bearDog encrypts
patient data (CKKS scheme), barraCuda runs GPU-accelerated homomorphic
mean/variance, result is decrypted without ever exposing raw data.

### 1.6 Zero-Copy GPU-Resident Pipelines

**For**: Springs with multi-step GPU computation chains.

```rust
use barracuda::pipeline::GpuViewF64;

let view = GpuViewF64::upload(&device, &data)?;
let stats = view.mean_variance().await?;     // no CPU readback
let corr = GpuViewF64::correlation(&a, &b)?; // stays on GPU
let result = corr.download().await?;          // single readback
```

Data stays on GPU across operations. Only the final result crosses the
PCIe bus. For MD simulations: 80×–600× speedup over per-step readback.

### 1.7 Numerical Kinetics and Growth Models

**For**: wetSpring (biogas), healthSpring (PK/PD), airSpring (crop growth).

```rust
use barracuda::numerical::kinetics::{gompertz, gompertz_batch};
use barracuda::numerical::ode::BatchedOdeRK45F64;
```

Gompertz biogas production, Michaelis-Menten pharmacokinetics, adaptive
RK45 ODE integration — all as shared primitives. Springs that previously
duplicated growth model code now delegate to barraCuda.

### 1.8 Typed Error Composition

**For**: Any primal or spring calling barraCuda via IPC or library.

As of Sprint 5, every barraCuda production function returns typed
`BarracudaError` variants instead of opaque strings. Callers can
pattern-match on specific failure modes:

```rust
use barracuda::error::BarracudaError;

match barracuda_result {
    Err(BarracudaError::DeviceLost { .. }) => {
        // GPU crashed or was reset — retry on a different device
        let fallback = gpu_pool.next_device()?;
        retry_on(&fallback, &workload)?;
    }
    Err(BarracudaError::Gpu { .. }) => {
        // Map/poll failure — likely VRAM exhaustion, reduce batch
        retry_with_smaller_batch(&workload)?;
    }
    Err(BarracudaError::ShaderCompilation { .. }) => {
        // Shader won't compile on this arch — fall back to CPU
        compute_cpu_fallback(&workload)?;
    }
    Err(e) => return Err(e.into()),
    Ok(result) => use_result(result),
}
```

**Novel pattern — Resilient pipelines**: A spring running a 10,000-step
MD simulation can catch `DeviceLost` mid-simulation, checkpoint to
rhizoCrypt (ephemeral DAG), migrate to a different GPU via toadStool,
and resume — all without human intervention. Previously, `String` errors
made this impossible to distinguish from shader compilation failures.

**Novel pattern — Precision fallback chain**: If `ShaderCompilation`
fails (e.g., DF64 shader on a GPU that can't handle it), the spring
catches the typed error and re-dispatches via `PrecisionBrain` at a
lower tier. The error variant tells the spring *why* it failed, not
just *that* it failed.

### 1.9 Concurrent Async Readback

**For**: Springs with pipelined GPU workflows (submit-many, read-many).

`AsyncReadback::poll_until_ready` now takes `&self` (not `&mut self`),
enabling multiple concurrent readbacks from a single submission:

```rust
let readback_a = submitter.submit_and_map::<f32>(&shader_a, &params_a).await?;
let readback_b = submitter.submit_and_map::<f32>(&shader_b, &params_b).await?;

// Poll both concurrently — no &mut exclusion
let (result_a, result_b) = tokio::join!(
    readback_a.read_f32(),
    readback_b.read_f32(),
);
```

**Novel pattern — Scatter-gather GPU**: Submit N independent shaders
(e.g., N lattice QCD configurations), poll all readbacks concurrently,
aggregate results on CPU. The `&self` change eliminates the serial
bottleneck where each readback had to complete before the next could
start polling.

### 1.10 Production-Hardened Genomics

**For**: wetSpring, healthSpring, any spring processing biological sequences.

The genomics module now has 25 tests covering edge cases that real
bioinformatics pipelines encounter:

```rust
use barracuda::genomics::{gc_content, find_motifs, quality_filter};

// RNA sequences (uracil treated as thymine)
let gc = gc_content("AUGCAUGC");

// Mixed case (real FASTA files are often mixed)
let gc = gc_content("atgcATGC");

// N-heavy sequences flagged by quality filter
let passed = quality_filter(&seqs, &QualityConfig::default());

// Batch processing (GPU-parallel when available)
let results = find_motifs_batch(&sequences, &patterns);
```

**Novel pattern — Field genomics pipeline**: wetSpring collects 16S
reads from environmental samples → barraCuda runs GPU-parallel motif
finding and diversity indices → quality filter rejects N-heavy sequences
before expensive alignment → sweetGrass records provenance braid linking
results to field sample IDs → loamSpine commits to permanent ledger.

---

## 2. Compute Trio (barraCuda + coralReef + toadStool)

The **Compute Trio** is the sovereign hardware execution stack. barraCuda
owns the math (what to compute), coralReef owns the compiler (how to
compile), toadStool owns the hardware (where to run).

```
barraCuda (Layer 1 — WHAT to compute)
    WGSL shaders → naga IR → optimize → WGSL
    ↓
coralReef (Layer 2-3 — HOW to compile)
    WGSL/SPIR-V → native GPU binary (SASS, RDNA2+)
    ↓
toadStool (Layer 3-4 — WHERE to run)
    Hardware discovery, VFIO dispatch, DMA, scheduling
    ↓
Hardware (any GPU, CPU, NPU)
```

### 2.1 Sovereign Shader Compilation

**For**: Performance-critical springs that need native GPU binaries.

```
Spring → barracuda.compute.dispatch(wgsl)
       → coralReef: shader.compile.wgsl → native binary
       → toadStool: compute.dispatch.submit → hardware
       → result ← toadStool ← barraCuda ← Spring
```

barraCuda compiles WGSL through naga (pure Rust IR), coralReef compiles
to native GPU ISA, toadStool dispatches via VFIO for deterministic
scheduling. The spring sees a single `compute.dispatch` call.

**Novel pattern**: **Compile-once, dispatch-many** — coralReef caches
compiled binaries. A spring running 10,000 MD timesteps compiles the
force kernel once, then barraCuda dispatches the cached binary 10,000
times via toadStool VFIO with sub-millisecond overhead per dispatch.

### 2.2 VFIO-Primary GPU Dispatch

**For**: HPC workloads needing deterministic GPU scheduling.

toadStool's VFIO backend gives exclusive GPU access with IOMMU isolation.
barraCuda's `CoralReefDevice` sends shaders through coralReef and
dispatches through toadStool — bypassing Vulkan entirely.

**Novel pattern**: **Multi-GPU work stealing** — toadStool discovers all
GPUs, barraCuda's `GpuPool` distributes work across them, coralReef
compiles for each architecture. A lattice QCD calculation on a 4-GPU node
gets near-linear scaling with zero Vulkan driver contention.

### 2.3 DF64 Sovereign Path

**For**: hotSpring (nuclear physics), groundSpring (spectral theory).

DF64 (double-float64) emulates ~104-bit mantissa on f32 hardware. The
naive wgpu path through naga can poison f64 transcendentals on some NVIDIA
hardware. The sovereign path through coralReef avoids this entirely:

```
barraCuda DF64 shader
    → coralReef compiles directly to SASS (no PTXAS f64 poisoning)
    → toadStool VFIO dispatches
    → 9.9× throughput vs wgpu path on Volta+
```

**Novel pattern**: **Automatic precision escalation** — if `PrecisionBrain`
detects that hardware can't run native f64 correctly, it falls back to
DF64 via the sovereign path. The spring never knows — it just gets
correct results.

### 2.4 Error-Aware Trio Orchestration

**For**: Any spring using the full compute trio with fault tolerance.

Typed errors enable the trio to self-heal without spring intervention:

```
Spring → barracuda.compute.dispatch
  → BarracudaError::ShaderCompilation
    → barraCuda asks coralReef to recompile at lower precision
    → coralReef returns new binary
    → toadStool dispatches on same hardware
  → BarracudaError::DeviceLost
    → toadStool discovers alternative GPU
    → coralReef compiles for new architecture
    → barraCuda re-dispatches
  → BarracudaError::Gpu (VRAM exhaustion)
    → barraCuda halves batch size
    → toadStool reallocates VRAM quota
    → re-dispatch at smaller batch
```

The spring sees a single `compute.dispatch` call. The trio handles the
failure cascade internally. Previously, `String` errors forced the spring
to parse error messages to determine the failure mode.

**Novel pattern — Self-healing lattice QCD**: hotSpring runs a 10,000-
trajectory HMC calculation. At trajectory 4,500, the GPU overheats and
resets. The trio catches `DeviceLost`, toadStool migrates to a cooler GPU,
coralReef recompiles, barraCuda resumes from the last checkpoint stored
in rhizoCrypt. The spring sees 10,000 completed trajectories.

### 2.5 Hardware-Calibrated Compute

**For**: Any spring that needs to know what the hardware can actually do.

```rust
// barraCuda probes, toadStool confirms
let capabilities = barracuda.device.probe(device_id);
// { f64_native: true, shared_mem_f64: false, vram_gb: 12, ... }
```

barraCuda probes GPU capabilities at runtime (f64 support, shared memory,
VRAM). toadStool adds hardware-level details (PCIe topology, VFIO status,
power state). Together they give springs a complete picture of what
computation is feasible and at what precision.

---

## 3. Duo Compositions (barraCuda + One Other Primal)

### 3.1 barraCuda + bearDog → Encrypted Computation

bearDog provides key generation, encryption, and decryption. barraCuda
provides GPU-accelerated FHE operations (NTT, INTT, pointwise multiply).

**Pattern**: bearDog encrypts → barraCuda computes on ciphertext →
bearDog decrypts. Data never appears in plaintext on the compute node.

**Spring application**: healthSpring patient data analysis. Clinical
measurements encrypted at the edge (bearDog), statistical analysis on
GPU (barraCuda FHE), results decrypted only by the authorized physician.

### 3.2 barraCuda + nestGate → Cached Computation

nestGate provides content-addressed storage with BLAKE3 hashing.
barraCuda provides deterministic computation.

**Pattern**: Hash the computation inputs (shader + parameters + data
fingerprint) → check nestGate for cached result → if miss, compute on
GPU → store result in nestGate with the input hash as key.

**Spring application**: groundSpring eigenvalue computation. The same
Anderson Hamiltonian at the same disorder strength always produces the
same eigenvalues. Cache them in nestGate; subsequent runs are instant.

### 3.3 barraCuda + songBird → Distributed Compute

songBird provides encrypted networking (TLS 1.3, NAT traversal, federation).
barraCuda provides compute dispatch.

**Pattern**: songBird discovers remote barraCuda instances on other nodes →
toadStool routes work to the best available GPU across the network →
barraCuda executes on the remote node → results return via songBird.

**Spring application**: neuralSpring training on a GPU cluster. songBird
handles node discovery and encrypted communication, barraCuda handles the
GEMM/attention/softmax on each node's GPU.

### 3.4 barraCuda + sweetGrass → Attributed Computation

sweetGrass provides W3C PROV-O provenance braids.

**Pattern**: Before dispatching a compute shader, record a provenance braid
(Agent = spring, Activity = computation, Entity = result). After the
computation, sweetGrass records the input→output derivation chain.

**Spring application**: wetSpring metagenomic analysis. Every diversity
index, every OTU table, every phylogenetic tree has a provenance braid
linking it to the raw 16S reads, the pipeline version, and the analyst.

### 3.5 barraCuda + squirrel → AI-Guided Computation

squirrel provides MCP (Model Context Protocol) multi-provider inference.

**Pattern**: squirrel suggests computation parameters → barraCuda executes
→ squirrel interprets results → suggests next computation.

**Spring application**: airSpring adaptive irrigation. squirrel analyzes
weather forecast + soil moisture data, barraCuda computes ET₀ via FAO-56
GPU batch, squirrel recommends irrigation schedule based on results.

### 3.6 barraCuda + petalTongue → Visualized Computation

petalTongue provides multi-modal UI (GUI, TUI, web, headless).

**Pattern**: barraCuda computes → petalTongue renders. GPU tensors can
transfer directly to petalTongue's rendering pipeline without CPU
roundtrip (shared GPU buffers via wgpu).

**Spring application**: hotSpring Anderson localization. barraCuda computes
the Hofstadter butterfly spectrum (eigenvalues vs. flux), petalTongue
renders it as an interactive fractal visualization with zoom/pan.

---

## 4. Multi-Primal Compositions

### 4.1 Full Sovereign Stack

**barraCuda + coralReef + toadStool + bearDog + songBird**

Encrypted distributed GPU compute:

1. bearDog encrypts workload (FHE/CKKS)
2. songBird distributes to remote GPU node
3. toadStool discovers hardware, allocates GPU via VFIO
4. coralReef compiles shader to native binary
5. barraCuda dispatches on encrypted ciphertext
6. Result returns via songBird, bearDog decrypts

No plaintext data on the compute node. No vendor SDK dependency.
Pure Rust end-to-end.

### 4.2 Provenance-Tracked Science

**barraCuda + sweetGrass + loamSpine + rhizoCrypt**

Every computation has a permanent, attributed, verifiable record:

1. barraCuda computes (GPU shader dispatch)
2. sweetGrass records provenance braid (who, what, when, how)
3. rhizoCrypt stores intermediate state (content-addressed DAG)
4. loamSpine commits final result to permanent ledger with inclusion proof

**Spring application**: healthSpring clinical trial. Every PK/PD model
fit, every VPC simulation, every dose-response curve has an immutable
provenance chain from raw data to published result.

### 4.3 Adaptive Hardware-Aware Science

**barraCuda + toadStool + squirrel + petalTongue**

AI-guided computation with hardware adaptation and live visualization:

1. squirrel proposes experiment parameters
2. toadStool reports available hardware capabilities
3. barraCuda selects precision tier and dispatches
4. petalTongue renders results in real-time
5. squirrel analyzes results, proposes next experiment
6. Loop until convergence

**Spring application**: neuralSpring hyperparameter search. squirrel
suggests architectures, toadStool finds the best available GPU,
barraCuda trains the model, petalTongue shows loss curves live.

### 4.4 Defended Computation

**barraCuda + skunkBat + bearDog + nestGate**

Computation with active defense and encrypted caching:

1. skunkBat monitors for anomalous access patterns
2. bearDog encrypts computation inputs and outputs at rest
3. barraCuda computes on GPU
4. nestGate stores encrypted results content-addressed
5. skunkBat detects if results are accessed by unauthorized agents

**Spring application**: ludoSpring anti-cheat. Game physics computed by
barraCuda, results signed by bearDog, monitored by skunkBat for
manipulation attempts.

---

## 5. Per-Spring Leverage Patterns

### 5.1 hotSpring (Plasma Physics, Lattice QCD)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| Yukawa OCP molecular dynamics | GPU force kernel + Verlet integrator |
| Lattice QCD HMC | SU(3) gauge action + staggered Dirac + CG solver |
| Anderson localization | Lanczos eigensolver + Hofstadter spectrum |
| Plasma dielectric | Stable `plasma_w` GPU shader (no cancellation) |
| BCS pairing | Stable `bcs_v2` (no f32 tail precision loss) |
| DF64 precision | Sovereign path via coralReef for NVVM-safe f64 |

**Novel combo**: hotSpring + barraCuda + coralReef + toadStool =
sovereign lattice QCD on VFIO-isolated GPU with DF64 precision and
automatic NVVM poisoning avoidance.

### 5.2 airSpring (Precision Agriculture)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| ET₀ computation | 8 methods (FAO-56, Hargreaves, Hamon, etc.) |
| GPU batch ET₀ | `HargreavesBatchGpu` for 10,000+ field points |
| Soil water balance | Richards PDE solver (Crank-Nicolson) |
| Regression | Linear, quadratic, exponential, logarithmic |
| Hydrology stats | SCS-CN, Stewart, Blaney-Criddle |

**Novel combo**: airSpring + barraCuda + squirrel + songBird =
distributed precision agriculture. GPU-accelerated ET₀ across a mesh
of field sensors, AI-guided irrigation scheduling, federated across
cooperative farms via songBird.

### 5.3 wetSpring (Life Science, Metagenomics)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| Diversity indices | Shannon, Simpson, Chao1, Bray-Curtis |
| Smith-Waterman | GPU-accelerated sequence alignment |
| HMM batch forward | GPU batch hidden Markov model |
| Phylogenetics | Bipartition encoding for Robinson-Foulds |
| Gompertz | Biogas production curve fitting |
| NCBI cache | Genomic data fetch and caching |

**Novel combo**: wetSpring + barraCuda + sweetGrass + loamSpine =
provenance-tracked metagenomic analysis. Every OTU table has an
immutable derivation chain from raw 16S reads to published diversity.

### 5.4 groundSpring (Uncertainty, Spectral Theory)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| Bootstrap CI | `BootstrapMeanGpu` (10,000 resamples on GPU) |
| Chi-squared | `chi_squared_uniform_sigma`, `chi2_decomposed` |
| Lanczos | Sparse eigenvalue solver (CPU, GPU tridiag_eigh) |
| Screened Coulomb | Yukawa eigenvalues, critical screening |
| xoshiro128** | CPU PRNG matching GPU stream |
| Freeze-out | Grid-fit + L-BFGS + GPU Nelder-Mead |

**Novel combo**: groundSpring + barraCuda + toadStool = hardware-aware
uncertainty quantification. toadStool reports GPU precision capabilities,
barraCuda selects the appropriate precision tier, groundSpring propagates
uncertainty with hardware-calibrated error bounds.

### 5.5 neuralSpring (ML Primitives)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| GEMM/matmul | GPU tensor matmul |
| Attention | Flash attention WGSL shader |
| Softmax | GPU-parallel softmax |
| ESN | Echo state network reservoir computing |
| Wright-Fisher | GPU population genetics simulation |
| Activations | ReLU, GELU, Swish, sigmoid |

**Novel combo**: neuralSpring + barraCuda + coralReef + songBird =
distributed neural network training with sovereign shader compilation.
Each node compiles attention kernels to native ISA via coralReef,
communicates gradients via songBird, no CUDA/cuDNN dependency. coralForge
is reconceptualized as an emergent neural object — a Pipeline graph
composition rather than a neuralSpring module; barraCuda provides the
compute primitives for structure prediction.

### 5.6 healthSpring (Clinical, PK/PD)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| Michaelis-Menten | GPU batch pharmacokinetics |
| FOCE gradients | GPU population PK (NONMEM-class) |
| VPC simulation | GPU Monte Carlo visual predictive check |
| Beat classification | GPU normalized cross-correlation |
| Hill kinetics | Activation/repression for regulatory networks |
| Dose-response | Emax, sigmoid Emax |

**Novel combo**: healthSpring + barraCuda + bearDog + sweetGrass =
encrypted, attributed clinical pharmacometrics. Patient PK data encrypted
(bearDog FHE), population analysis on GPU (barraCuda FOCE), results
attributed (sweetGrass), audit trail permanent (loamSpine).

### 5.7 ludoSpring (Game Science)

| Capability | How barraCuda Helps |
|-----------|-------------------|
| Perlin noise | GPU-parallel procedural generation |
| Physics | GPU rigid body, fluid simulation |
| Statistics | Player behavior analysis |
| RNG | Deterministic xoshiro128** for replay |

**Novel combo**: ludoSpring + barraCuda + petalTongue + skunkBat =
server-authoritative game physics. barraCuda computes physics on GPU,
petalTongue renders, skunkBat monitors for client-side manipulation,
deterministic PRNG enables replay verification.

---

## 6. Emergent Ecosystem Patterns

### 6.1 Precision Cascading

Any spring can ask barraCuda "what precision can this hardware deliver?"
and adapt its algorithm. This creates a **precision cascade**:

```
Spring asks → PrecisionBrain recommends → Spring adapts
→ If insufficient → toadStool finds better hardware
→ If unavailable → coralReef compiles DF64 fallback
→ Spring gets correct result regardless of hardware
```

### 6.2 Shader Composability

barraCuda's 816 WGSL shaders are composable building blocks. Springs can
chain them into multi-stage GPU pipelines:

```
Read raw data → GPU normalize → GPU FFT → GPU filter → GPU IFFT → Result
```

Each stage is a separate shader. The data stays on GPU between stages
(GpuView). Only the final result crosses the PCIe bus.

### 6.3 Cross-Spring Math Sharing

barraCuda is the **single source of truth** for mathematical primitives.
When one spring evolves a function (e.g., hotSpring discovers a stable
BCS formula), it's absorbed into barraCuda and becomes available to all
springs immediately. No duplication, no drift.

### 6.4 Error-Propagation Across Primal Boundaries

Typed errors propagate cleanly across IPC boundaries. When a spring calls
barraCuda via JSON-RPC, the error variant is serialized in the JSON-RPC
error response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,
    "message": "GPU device lost during readback poll",
    "data": { "variant": "DeviceLost", "context": "poll_until_ready" }
  }
}
```

Any primal — biomeOS, squirrel, springs — can inspect the `variant` field
and route appropriately. biomeOS can trigger toadStool hardware re-discovery.
squirrel can suggest parameter adjustments. A spring can checkpoint and retry.

This is the foundation for **ecosystem-wide fault tolerance**: errors are
not strings to log and forget — they are typed signals that trigger
coordinated recovery across multiple primals.

### 6.5 Concurrent Multi-Domain Pipelines

With `&self` async readback, a spring can run heterogeneous compute
domains simultaneously on the same GPU:

```
                    ┌─ shader A (genomics motif find)  ─┐
Spring → barraCuda ─┤─ shader B (stats bootstrap CI)    ├─→ aggregate
                    └─ shader C (linalg eigensolve)     ─┘
```

All three readbacks poll concurrently. The spring gets results as they
complete (not in submission order). This enables **domain fusion** —
combining results from different scientific domains in a single
computation round-trip.

**Novel pattern — Integrated clinical trial analysis**: healthSpring
submits three concurrent GPU workloads via barraCuda: (1) PK/PD model
fit, (2) bootstrap confidence intervals on clearance, (3) VPC simulation.
All three complete in parallel, results merge into a single report.
Previously each would block serially.

### 6.6 Hardware-Agnostic Science

A spring written against barraCuda runs on any GPU vendor:

- NVIDIA (Vulkan/VFIO)
- AMD (Vulkan)
- Intel (Vulkan)
- Apple (Metal)
- CPU fallback (llvmpipe)
- Future: NPU, browser (WebGPU)

**fieldMouse deployments** use ecoBin-compliant chimera binaries built from
barraCuda-consuming primals, targeting constrained hardware (RISC-V,
Raspberry Pi, edge sensors).

The science is the same. The hardware is interchangeable.

### 6.7 Cross-Spring Discovery via barraCuda Capabilities

Springs don't know about each other directly, but they share barraCuda
as a common math substrate. This enables indirect collaboration:

```
airSpring calls barracuda.compute.dispatch("richards_pde")
wetSpring calls barracuda.compute.dispatch("diversity_index")
groundSpring calls barracuda.compute.dispatch("bootstrap_ci")

→ biomeOS sees all three springs using barraCuda
→ squirrel notices: "soil moisture (airSpring) + microbial diversity
   (wetSpring) + measurement uncertainty (groundSpring) form a coherent
   analysis of soil health"
→ squirrel proposes a combined pipeline via capability routing
→ No spring needed to know the others existed
```

**Novel pattern — Emergent multi-spring science**: The math capabilities
advertised by barraCuda serve as a **lingua franca** for cross-spring
discovery. squirrel or biomeOS can compose springs that share barraCuda
domains into novel pipelines that no individual spring was designed for.

### 6.8 Provenance-Tracked GPU Error Recovery

When barraCuda reports a typed error and retries on different hardware,
the provenance trio can record the full recovery chain:

```
sweetGrass braid:
  Activity: "lattice_qcd_hmc"
  Entity[0]: "trajectory_batch_1-4500" → computed on GPU_A
  Entity[1]: "device_lost_event" → GPU_A reset at trajectory 4500
  Entity[2]: "migration_event" → toadStool routed to GPU_B
  Entity[3]: "trajectory_batch_4501-10000" → computed on GPU_B
  Entity[4]: "final_result" → merged from Entity[0] + Entity[3]
  wasGeneratedBy: barraCuda v0.3.5
  wasAssociatedWith: hotSpring experiment_042
```

This creates an auditable record of *why* a computation was split across
hardware — critical for reproducibility in published science. The typed
error variants (`DeviceLost`, `Gpu`, `ShaderCompilation`) become
first-class provenance events.

---

## 7. What barraCuda Does NOT Do

barraCuda is deliberately bounded. It does not:

- **Store data** — that's nestGate
- **Encrypt data** — that's bearDog
- **Discover hardware** — that's toadStool (barraCuda queries via IPC)
- **Route network traffic** — that's songBird
- **Manage identity** — that's bearDog/biomeOS
- **Record provenance** — that's sweetGrass
- **Render UI** — that's petalTongue
- **Orchestrate primals** — that's biomeOS

barraCuda owns the math. Period. Everything else is delegated to the
primal that owns that domain. This is the sovereignty principle.

---

## References

- `barraCuda/README.md` — Full primal documentation
- `barraCuda/specs/BARRACUDA_SPECIFICATION.md` — Crate architecture + IPC contract
- `barraCuda/WHATS_NEXT.md` — Prioritized roadmap
- `barraCuda/crates/barracuda/src/error.rs` — `BarracudaError` typed error variants
- `wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` — Full sovereign stack plan
- `wateringHole/INTER_PRIMAL_INTERACTIONS.md` — IPC coordination
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming convention
- `wateringHole/handoffs/BARRACUDA_V035_TYPED_ERRORS_NURSERY_COVERAGE_HANDOFF_MAR16_2026.md` — Sprint 5 handoff
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/SPRING_CATALOG.md` — Spring catalogue
