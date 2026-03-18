<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# toadStool Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 17, 2026
**Primal**: toadStool S158 (Rust 2024, MSRV 1.85, 56 crates, 21,156+ tests, ecoBin v3.0)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how toadStool can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers.
Each primal in the ecosystem will produce an equivalent guide. Together,
these guides form a combinatorial recipe book for emergent behaviors.

toadStool provides **sovereign compute infrastructure** — runtime
discovery and orchestration of GPUs, NPUs, and CPUs across any
vendor's hardware. PCIe topology mapping, VFIO-isolated dispatch,
power management, distributed cross-gate routing, and hardware
transport (display, capture, serial). Pure Rust, zero C application
dependencies (ecoBin v3.0).

**Philosophy**: Hardware is sovereign infrastructure. A primal should
never need to know what GPU brand is installed, what driver version is
running, or what bus topology exists. toadStool abstracts hardware into
capabilities — discovered at runtime, probed on demand, and composed
with any math or compiler primal. toadStool owns the hardware; other
primals own the math, the compilation, the storage, the identity.

---

## IPC Methods (Semantic Naming)

All methods follow `{namespace}.{domain}.{operation}` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `toadstool.health` | Health check (name, version, status, capabilities) |
| `toadstool.version` | Version and build metadata |
| `toadstool.query_capabilities` | Full capability manifest |
| `compute.discover_capabilities` | Runtime capability probing |
| `compute.submit` | Submit workload to GPU job queue |
| `compute.status` | Check workload status |
| `compute.result` | Retrieve workload result |
| `compute.hardware.observe` | Observe GPU register state for hw-learn |
| `compute.hardware.distill` | Distill optimal config from observations |
| `compute.hardware.apply` | Apply learned config to hardware (BAR0) |
| `compute.hardware.auto_init` | Auto-detect GPU and apply best recipe |
| `compute.hardware.vfio_devices` | List VFIO-bound GPU devices |
| `compute.dispatch.submit` | Direct dispatch via toadStool mesh |
| `compute.dispatch.forward` | Forward dispatch to remote gate |
| `gpu.info` | Detailed adapter info (driver, f64, workgroups, VRAM) |
| `gpu.memory` | GPU memory usage |
| `ollama.list_models` | List locally available LLM models |
| `ollama.inference` | Run local LLM inference |
| `ollama.load` / `ollama.unload` | Model lifecycle management |
| `gate.update` / `gate.list` / `gate.route` | Distributed cross-gate routing |
| `transport.discover` / `transport.list` / `transport.route` | Hardware transport discovery |
| `shader.compile.wgsl` / `shader.compile.spirv` | coralReef proxy with naga fallback |
| `ecology.*` | 14 ecosystem integration methods |
| `discovery.*` | NUCLEUS capability-based discovery |
| `ai.nautilus.*` | Evolutionary reservoir computing (feature-gated) |

**Transport**: JSON-RPC 2.0 over Unix socket (primary), tarpc/bincode
(high-throughput primal-to-primal), TCP fallback. Capability-based
discovery via `get_socket_path_for_capability()`.

---

## 1. toadStool Standalone

These patterns use toadStool alone — no other primals required.

### 1.1 Hardware Discovery and Probing

**For**: Any spring or primal that needs to know what compute is available.

```rust
// JSON-RPC call
{ "method": "gpu.info", "params": {} }

// Response includes:
// adapter_name, vendor, driver, device_id, f64_support,
// max_workgroup_size, max_buffer_size, vram_bytes,
// f64_shared_memory_reliable, sovereign_binary_capable,
// compute_viable, compute_blockers, firmware_inventory
```

toadStool discovers all GPUs, NPUs, and CPUs at runtime via
sysfs/PCIe/wgpu. No compile-time hardware assumptions. A spring can
ask "what compute is available?" and get a complete manifest without
importing any GPU library.

**Novel pattern**: **Adaptive algorithm selection** — a spring queries
`gpu.info` at startup and selects its algorithm based on what hardware
actually exists. GPU present? Use GPU path. NPU available? Route
inference there. CPU only? Fall back gracefully. The spring code is
identical on all machines.

### 1.2 Multi-Adapter GPU Selection

**For**: Multi-GPU workstations, heterogeneous GPU setups.

```bash
# Select by index, name substring, or auto (best f64 GPU)
TOADSTOOL_GPU_ADAPTER=auto
TOADSTOOL_GPU_ADAPTER=0
TOADSTOOL_GPU_ADAPTER="RTX 3090"
TOADSTOOL_GPU_ADAPTER="RTX 3090,RTX 4070,auto"  # fallback chain
```

toadStool evaluates all adapters and selects the optimal one for the
workload. `GpuAdapterInfo` exposes driver name, vendor/device ID,
f64 support, workgroup limits, and max buffer size.

**Novel pattern**: **Heterogeneous GPU routing** — on a machine with
an NVIDIA RTX 3090 (f64-native) and an AMD RX 6950 XT (Infinity Cache),
toadStool can route f64-heavy lattice QCD to the NVIDIA and
memory-bandwidth-bound FFTs to the AMD, simultaneously.

### 1.3 PCIe Topology Mapping

**For**: Multi-GPU arrays, topology-aware scheduling.

```rust
// JSON-RPC: toadstool.query_capabilities
// Returns PCIe topology graph:
// - PciBridge, GpuPairTopology, PcieTopologyGraph
// - Shared-switch detection, hop count, contention factor
// - Per-link bandwidth (PCIe 3.0/4.0/5.0 × lanes)
```

toadStool maps the full PCIe topology from sysfs — parent bridges,
PCIe switches, lane widths, link speeds. For multi-GPU setups (e.g.,
4× RTX 3050 on a PCIe switch), toadStool identifies which GPUs share
a switch and estimates contention-aware effective bandwidth.

**Novel pattern**: **Topology-aware work partitioning** — a spring
running distributed computation can query the topology graph and
partition work to minimize cross-switch PCIe traffic. GPUs that share
a switch get neighboring data domains; GPUs on separate root ports
handle independent partitions.

### 1.4 NPU Discovery and Dispatch

**For**: Springs using neuromorphic or inference-accelerator hardware.

```rust
// Generic NpuDispatch trait — vendor-agnostic
pub trait NpuDispatch: Send + Sync {
    fn load_model(&self, model: &[u8]) -> Result<NpuModelHandle>;
    fn infer(&self, handle: &NpuModelHandle, input: &[u8]) -> Result<Vec<u8>>;
    fn capabilities(&self) -> NpuCapabilities;
}

// AkidaNpuDispatch adapter for BrainChip Akida NPU
// Capabilities: inference, reservoir computing, on-chip learning,
// spiking networks, batch inference, power monitoring
```

toadStool's `NpuDispatch` trait is vendor-agnostic. The `AkidaNpuDispatch`
adapter drives BrainChip Akida NPUs via VFIO/kernel/mmap backends.
New NPU vendors plug in by implementing the trait.

**Novel pattern**: **GPU-NPU hybrid inference** — toadStool can route
the attention layers of a transformer to the GPU (high throughput) and
the classifier head to the NPU (low latency, low power). The spring
sees a single inference call; toadStool orchestrates the hardware split.

### 1.5 Cache-Aware Tiling

**For**: Any spring or math primal needing optimal GPU memory tiling.

| Substrate | Largest Cache | Optimal Tile | Impact |
|-----------|---------------|--------------|--------|
| RTX 3090 | L2: 6 MB | 1 MB | 732 tiles/GB |
| RTX 4070 | L2: 48 MB | 11 MB | 92 tiles/GB |
| RX 6950 XT | Infinity: 128 MB | 29 MB | 35 tiles/GB |
| CPU (Zen 3) | L3: 32 MB | 7 MB | 138 tiles/GB |

toadStool discovers L2/Infinity Cache sizes at runtime and recommends
optimal tile sizes. barraCuda or any math primal can use these
recommendations to partition data for maximum cache locality.

**Novel pattern**: **Auto-tiling pipelines** — toadStool provides the
cache geometry, barraCuda tiles its matrix multiply accordingly.
On an RTX 4070 (48 MB L2), a single tile is 11 MB — large enough for
a 1024×1024 f64 matrix without thrashing. On a 3090 (6 MB L2), the
same matrix splits into 6 tiles with automatic prefetch overlap.

### 1.6 Local LLM Lifecycle

**For**: Any spring or primal needing local AI inference.

```
ollama.list_models  → ["llama3.2:3b", "codellama:7b", ...]
ollama.load         → warm model into VRAM
ollama.inference    → run prompt, stream tokens
ollama.unload       → release VRAM
```

toadStool manages Ollama model lifecycle — list available models,
load into GPU VRAM, run inference, unload. This enables any spring to
do local LLM inference without knowing about Ollama, VRAM management,
or model formats.

**Novel pattern**: **VRAM-aware model scheduling** — toadStool knows
the GPU's total VRAM and current usage. When a spring requests inference,
toadStool checks if the model fits. If not, it can evict a less-recently-used
model or route to a different GPU with enough headroom.

### 1.7 Hardware Transport

**For**: Display output, camera capture, serial communication.

```
transport.discover  → find available hardware transports
transport.list      → list active transports
transport.route     → route data between transports (any-to-any)
```

Three implemented transports:
- **DisplayTransport** (DRM/KMS) — HDMI/DP output
- **CaptureTransport** (V4L2) — camera/capture card input
- **SerialTransport** — USB serial devices

**Novel pattern**: **Camera-to-GPU pipeline** — toadStool captures
V4L2 frames, routes them through the TransportRouter directly to
GPU memory, where barraCuda processes them. No CPU copy in the hot
path. For real-time computer vision at 60 fps.

---

## 2. Compute Trio (toadStool + barraCuda + coralReef)

The **Compute Trio** is the sovereign hardware execution stack.
toadStool owns the hardware (where to run), coralReef owns the
compiler (how to compile), barraCuda owns the math (what to compute).

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

### 2.1 VFIO-Isolated GPU Dispatch

**For**: Deterministic, interference-free GPU compute.

toadStool binds GPUs to the VFIO-PCI driver, giving exclusive access
with IOMMU memory isolation. No kernel graphics driver interference.
No desktop compositor contention. Deterministic scheduling.

```
Spring → barraCuda: compute.dispatch(shader, data)
       → coralReef: shader.compile.wgsl → native binary
       → toadStool: compute.dispatch.submit → VFIO dispatch
       → Hardware: DMA transfer → shader execution → result
       → Spring
```

**Novel pattern**: **Science-mode GPU isolation** — on a workstation
with 2 GPUs, toadStool keeps GPU 0 on nvidia/nouveau for the desktop
and binds GPU 1 to VFIO for exclusive scientific computation. A spring
gets a clean, isolated GPU with zero desktop interference. The
`ecoprimals-mode` CLI switches this at will.

### 2.2 Hardware-Calibrated Precision Routing

**For**: Springs that need correct results regardless of hardware quirks.

```
Spring asks toadStool: "what can this GPU do?"
    gpu.info → { f64_support: true, f64_shared_memory_reliable: false,
                  sovereign_binary_capable: true }

Spring asks barraCuda: "what precision should I use?"
    PrecisionBrain → F64NativeNoSharedMem
                   → coralReef compiles DF64 shader for shared-mem ops
                   → toadStool dispatches via VFIO

Spring gets correct results. Never touched hardware details.
```

toadStool provides the hardware truth — what the silicon actually
supports. barraCuda decides the precision strategy. coralReef compiles
appropriately. The spring only asked for a computation.

**Novel pattern**: **f64 shared-memory hazard avoidance** — toadStool
detected that naga/SPIR-V f64 shared-memory reductions return zeros on
certain GPUs (discovered by groundSpring V84). This capability flag
propagates through the trio: coralReef avoids shared-memory f64 codegen,
barraCuda routes shared-mem ops to DF64 emulation.

### 2.3 Cross-Gate Distributed Dispatch

**For**: Multi-machine GPU clusters.

```
Machine A (RTX 3090):
    toadStool discovers local GPU → registers with songBird
Machine B (Titan V):
    toadStool discovers local GPU → registers with songBird

Spring submits workload → barraCuda receives
    → toadStool routes to best GPU across both machines
    → coralReef compiles for target architecture
    → toadStool dispatches on remote machine via gate routing
    → Result returns via songBird encrypted transport
```

toadStool's cross-gate router evaluates all available GPUs across the
network and routes workloads to the optimal one. PCIe topology,
VRAM availability, power state, and current load all factor into
the routing decision.

**Novel pattern**: **Topology-aware distributed LLM** — TinyLlama-1.1B
inference at 39.85 tok/s across two gates with BearDog encrypted
tensor transport. toadStool splits the model layers across GPUs based
on their VRAM and interconnect bandwidth.

### 2.4 hw-learn: Self-Tuning Hardware

**For**: Long-running scientific workloads that benefit from hardware
auto-tuning.

```
compute.hardware.observe   → snapshot GPU register state during workload
compute.hardware.distill   → extract optimal patterns from observations
compute.hardware.apply     → write optimized config to hardware (BAR0)
compute.hardware.auto_init → auto-detect and apply best known recipe
```

toadStool's hw-learn pipeline observes GPU behavior during real workloads,
distills optimal configurations (clock gating, scheduling thresholds,
PBDMA tuning), and applies them via direct BAR0 register writes.

**Novel pattern**: **Workload-specific GPU tuning** — hotSpring runs a
lattice QCD simulation. toadStool observes the dispatch pattern (high
FMA utilization, low memory bandwidth). It distills and applies a config
that favors compute clock over memory clock. Next run is 15% faster
without any spring code changes.

---

## 3. Duo Compositions (toadStool + One Other Primal)

### 3.1 toadStool + bearDog → Sovereign Secure Compute

bearDog provides crypto (signing, encryption, key management).
toadStool provides VFIO-isolated hardware.

**Pattern**: bearDog provisions encryption keys → toadStool isolates
the GPU via VFIO + IOMMU → computation runs in a memory-isolated
enclave → bearDog signs the result for integrity.

**Spring application**: healthSpring clinical data. The GPU is
IOMMU-isolated (no other process can read its memory). Patient data
enters encrypted (bearDog), is processed on the isolated GPU
(toadStool), and the result is signed before leaving the enclave.

### 3.2 toadStool + songBird → Federated Hardware Discovery

songBird provides encrypted networking, TLS 1.3, NAT traversal.
toadStool provides hardware discovery.

**Pattern**: toadStool discovers local hardware → songBird announces
capabilities to the federation → remote primals discover available
compute across the network → workloads route to the best hardware.

**Spring application**: neuralSpring distributed training. songBird
discovers all machines in the federation and their GPU capabilities
(via toadStool). The training coordinator assigns layers to machines
based on each machine's GPU VRAM and interconnect bandwidth.

### 3.3 toadStool + nestGate → Hardware-Indexed Storage

nestGate provides content-addressed storage (BLAKE3).
toadStool provides hardware fingerprinting.

**Pattern**: toadStool fingerprints the hardware (GPU model, driver
version, cache sizes) → nestGate stores computation results indexed
by hardware fingerprint + input hash → future runs on the same
hardware retrieve cached results instantly.

**Spring application**: groundSpring GPU optimization profiles.
Each GPU model's optimal tiling parameters are computed once and
stored in nestGate by hardware fingerprint. When the same GPU model
appears on a new machine, the profile is retrieved without re-profiling.

### 3.4 toadStool + squirrel → AI-Aware Hardware Routing

squirrel provides AI coordination (MCP, model routing).
toadStool provides hardware capability probing.

**Pattern**: squirrel receives an inference request → toadStool
reports available hardware (GPU VRAM, NPU capabilities, CPU cores) →
squirrel selects the optimal model size for the available hardware →
toadStool routes the inference to the right accelerator.

**Spring application**: ludoSpring adaptive game AI. squirrel manages
multiple AI models (small for real-time, large for analysis).
toadStool reports available VRAM. squirrel loads the largest model
that fits and routes inference through toadStool to the GPU.

### 3.5 toadStool + petalTongue → Hardware-Direct Rendering

petalTongue provides multi-modal UI.
toadStool provides display transport (DRM/KMS).

**Pattern**: Computation completes on GPU → toadStool routes the
output buffer directly to the display via DRM → petalTongue manages
the UI overlay and interaction. Zero CPU copy for the render path.

**Spring application**: hotSpring real-time simulation visualization.
Molecular dynamics forces computed on GPU (via barraCuda) → particle
positions stay in GPU memory → toadStool's DisplayTransport presents
the framebuffer via DRM → petalTongue overlays interactive controls.

### 3.6 toadStool + biomeOS → Orchestrated Compute Scheduling

biomeOS provides ecosystem orchestration, Neural API.
toadStool provides compute capability registration.

**Pattern**: toadStool registers its capabilities with biomeOS →
biomeOS composes atomics (Node = Tower + toadStool) → biomeOS routes
compute requests from any primal to toadStool via the Neural API.

**Spring application**: Any spring can request compute through biomeOS
without knowing toadStool exists. biomeOS resolves "I need GPU compute"
to the nearest toadStool instance and routes the request.

### 3.7 toadStool + sweetGrass → Attributed Hardware Usage

sweetGrass provides W3C PROV-O provenance braids.

**Pattern**: Before dispatch, toadStool records hardware context
(which GPU, VFIO group, PCIe slot, driver version, power state) →
sweetGrass creates a provenance braid linking the computation result
to the exact hardware environment that produced it.

**Spring application**: wetSpring reproducible science. A metagenomic
analysis result includes not just the algorithm and input data, but
the exact GPU model and driver that executed the compute shaders.
If results differ on different hardware, the provenance braid reveals
why.

### 3.8 toadStool + skunkBat → Hardware Intrusion Detection

skunkBat provides threat detection (metadata-only, no content inspection).

**Pattern**: toadStool monitors hardware state (PCIe devices, VFIO
groups, BAR0 register patterns, DMA activity) → skunkBat watches
for anomalies (unexpected PCIe device appears, VFIO group permissions
change, unauthorized BAR0 writes, unusual DMA patterns).

**Spring application**: Enterprise deployment. skunkBat detects if
someone plugs in a rogue PCIe device or attempts to access a
VFIO-isolated GPU from outside the authorized primal. toadStool
provides the hardware-level telemetry; skunkBat provides the
threat analysis.

---

## 4. Multi-Primal Compositions

### 4.1 Full Sovereign Compute Stack

**toadStool + barraCuda + coralReef + bearDog + songBird**

End-to-end sovereign GPU computation across a federation:

1. songBird discovers the best GPU in the federation (via toadStool capabilities)
2. bearDog encrypts the workload in transit (TLS 1.3 + optional FHE)
3. toadStool on the target machine isolates the GPU via VFIO
4. coralReef compiles the shader to native ISA for that GPU
5. barraCuda dispatches the computation
6. toadStool monitors hardware health and power during execution
7. Result returns via songBird, integrity-signed by bearDog

No vendor SDK. No C FFI. No plaintext in transit. Hardware-isolated.
Pure Rust end-to-end.

### 4.2 Reproducible Science Pipeline

**toadStool + barraCuda + nestGate + sweetGrass + loamSpine**

Every computation is cached, attributed, and permanently recorded:

1. toadStool fingerprints the hardware environment
2. nestGate checks for cached result (input hash + hardware fingerprint)
3. If miss: barraCuda computes on GPU, toadStool dispatches
4. sweetGrass records provenance (hardware, algorithm, input, output)
5. nestGate stores result content-addressed
6. loamSpine commits the provenance braid to permanent ledger

**Spring application**: Any spring running GPU computation gets
automatic caching, hardware-aware cache keys, and a permanent
audit trail. Re-running the same analysis on the same hardware
returns instantly from nestGate.

### 4.3 Adaptive Distributed Inference

**toadStool + squirrel + songBird + barraCuda**

AI inference routed to optimal hardware across a network:

1. squirrel receives inference request with context window size
2. songBird discovers all toadStool instances in the federation
3. toadStool on each machine reports GPU VRAM and capabilities
4. squirrel selects the machine with enough VRAM for the model
5. barraCuda runs inference on that machine's GPU
6. Result returns via songBird to the requesting primal

**Spring application**: neuralSpring model serving. A 7B model needs
14 GB VRAM. squirrel queries toadStool across the federation, finds
the RTX 3090 (24 GB), and routes inference there. Meanwhile, a 3B
model goes to the RTX 4070 (12 GB). Load balancing is hardware-aware.

### 4.4 Real-Time Compute Visualization

**toadStool + barraCuda + coralReef + petalTongue**

GPU computation with zero-copy rendering:

1. barraCuda computes on GPU (force calculation, field solve, etc.)
2. Output stays in GPU memory (no CPU readback)
3. toadStool routes the GPU buffer to the display via DRM
4. petalTongue overlays interactive UI (zoom, rotate, parameter sliders)
5. User adjusts parameters → barraCuda re-computes → display updates
6. Loop at 60+ fps

**Spring application**: hotSpring interactive plasma simulation.
Particle positions computed by barraCuda, rendered by toadStool's
display transport, controlled by petalTongue. The entire frame
pipeline stays on GPU — only UI events cross the PCIe bus.

### 4.5 Defended Hardware Enclave

**toadStool + skunkBat + bearDog + loamSpine**

Hardware-level security with threat detection and permanent audit:

1. toadStool isolates GPU via VFIO + IOMMU
2. bearDog encrypts data in transit and provisions keys
3. skunkBat monitors for hardware-level intrusion attempts
4. loamSpine records all access events with inclusion proofs
5. Any anomaly triggers skunkBat alert → toadStool revokes VFIO access

---

## 5. Per-Spring Leverage Patterns

### 5.1 hotSpring (Plasma Physics, Lattice QCD, Spectral Theory)

| Capability | How toadStool Helps |
|-----------|-------------------|
| Titan V VFIO isolation | Exclusive GPU access for deterministic MD simulation |
| BAR0 register tuning | hw-learn optimizes GPU clocks for FMA-heavy lattice QCD |
| Power management | Glow plug warms GPU before dispatch; thermal throttle avoidance |
| Multi-GPU routing | Route Yukawa forces to GPU 0, Ewald summation to GPU 1 |
| f64 capability probing | Report `f64_shared_memory_reliable: false` → DF64 fallback |

**Novel combo**: hotSpring + toadStool + coralReef + barraCuda =
VFIO-isolated lattice QCD on Titan V with hw-learn auto-tuning.
toadStool observes FMA utilization, distills optimal compute clock,
applies via BAR0. Next HMC trajectory is faster without any algorithm
change.

### 5.2 airSpring (Precision Agriculture)

| Capability | How toadStool Helps |
|-----------|-------------------|
| GPU discovery | Find cheapest available GPU for batch ET₀ |
| Edge device discovery | mDNS/filesystem discovery of field sensors |
| Serial transport | Direct sensor data ingestion via USB serial |
| Distributed routing | Route ET₀ computation to the nearest GPU in the mesh |

**Novel combo**: airSpring + toadStool + songBird + squirrel =
distributed precision agriculture. Field sensors connect via
toadStool's serial transport. ET₀ batch computation routes to the
nearest GPU via songBird-discovered toadStool instances. squirrel
analyzes results and recommends irrigation schedules.

### 5.3 wetSpring (Life Science, Metagenomics)

| Capability | How toadStool Helps |
|-----------|-------------------|
| GPU selection | Route Smith-Waterman alignment to GPU with most VRAM |
| Hardware fingerprint | Cache alignment results indexed by GPU capability |
| VFIO isolation | Isolate GPU for HIPAA-sensitive sequence analysis |
| Cross-gate routing | Distribute metagenome analysis across a lab cluster |

**Novel combo**: wetSpring + toadStool + bearDog + nestGate =
encrypted metagenomic analysis pipeline. Patient 16S sequences
encrypted at ingest (bearDog), processed on VFIO-isolated GPU
(toadStool), results cached content-addressed (nestGate), GPU
isolation prevents any memory leakage.

### 5.4 groundSpring (Uncertainty, Spectral Theory)

| Capability | How toadStool Helps |
|-----------|-------------------|
| Cache-aware tiling | Optimal tile size for eigenvalue decomposition |
| Precision probing | Report exact f64 capability for error propagation |
| Multi-adapter selection | Route eigensolve to best f64 GPU |
| Topology mapping | Minimize PCIe contention for multi-GPU Lanczos |

**Novel combo**: groundSpring + toadStool + barraCuda = hardware-aware
uncertainty quantification. toadStool reports the GPU's actual precision
capability and cache geometry. barraCuda selects precision tier and
tile size accordingly. groundSpring propagates error bounds calibrated
to the actual hardware — not assumed hardware.

### 5.5 neuralSpring (ML Primitives)

| Capability | How toadStool Helps |
|-----------|-------------------|
| VRAM monitoring | Report available VRAM for model size selection |
| Ollama integration | Local LLM lifecycle for inference pipelines |
| Cross-gate training | Distribute training across federated GPU cluster |
| NPU dispatch | Route classifier heads to NPU for low-power inference |

**Novel combo**: neuralSpring + toadStool + squirrel + songBird =
federated model serving. toadStool reports each machine's GPU
capabilities via songBird. squirrel assigns models to machines based
on VRAM. Training gradients flow via songBird. All hardware management
is invisible to the training loop.

### 5.6 healthSpring (Clinical, PK/PD)

| Capability | How toadStool Helps |
|-----------|-------------------|
| VFIO isolation | IOMMU-isolated GPU for HIPAA/GDPR compliance |
| Hardware attestation | Record exact hardware environment in provenance |
| Power management | GPU power state for battery-conscious clinical devices |
| Ollama integration | Local clinical AI inference without cloud dependency |

**Novel combo**: healthSpring + toadStool + bearDog + sweetGrass +
loamSpine = fully sovereign clinical pharmacometrics. Patient PK data
encrypted (bearDog), processed on IOMMU-isolated GPU (toadStool),
results attributed (sweetGrass) with exact hardware provenance
(toadStool fingerprint), permanently recorded (loamSpine). Entire
pipeline auditable for regulatory compliance.

### 5.7 ludoSpring (Game Science, HCI)

| Capability | How toadStool Helps |
|-----------|-------------------|
| Display transport | DRM output for game rendering |
| Capture transport | V4L2 input for gesture recognition |
| Serial transport | Controller/peripheral input |
| Multi-GPU routing | Physics on GPU 0, rendering on GPU 1 |
| Real-time scheduling | VFIO dispatch for deterministic frame timing |

**Novel combo**: ludoSpring + toadStool + petalTongue + barraCuda =
sovereign game engine. Physics and AI computed by barraCuda on
VFIO-isolated GPU (toadStool), rendered via DRM display transport
(toadStool), UI managed by petalTongue, camera input via V4L2
capture transport (toadStool). Zero vendor SDK in the entire stack.

---

## 6. Emergent Ecosystem Patterns

### 6.1 Hardware Abstraction Cascade

Any primal or spring can ask "what compute is available?" without
importing a single GPU library:

```
Spring → biomeOS: "I need GPU compute"
       → biomeOS routes to toadStool (capability: "compute")
       → toadStool: gpu.info → { f64: true, vram: 24GB, ... }
       → Spring adapts algorithm
       → Spring: compute.submit → toadStool dispatches
```

The spring never imports `wgpu`, never links `vulkan`, never checks
for `libcuda.so`. toadStool is the hardware abstraction boundary.

### 6.2 Power-Aware Scheduling

toadStool's power management (Sovereign/Warm/Glow/Sleep/Eco) enables
ecosystem-wide power-aware scheduling:

```
No workloads pending → toadStool: GPU → Sleep (save 200W)
Workload arrives → toadStool: GPU → Warm (50ms glow plug)
Sustained load → toadStool: GPU → Sovereign (full clocks)
Load drops → toadStool: GPU → Eco (reduced clocks, reduced power)
```

Springs don't manage power. toadStool manages power. biomeOS can
set power policy for the entire machine.

### 6.3 Self-Learning Hardware

toadStool's hw-learn pipeline creates a feedback loop:

```
Dispatch workload → observe hardware state → distill optimal config
    → apply to hardware → next dispatch is faster → observe again → ...
```

Over time, each GPU accumulates a KnowledgeStore of optimal configs
for different workload patterns. These configs are shareable —
via nestGate storage or songBird federation. A new machine joining
the federation inherits the best-known configs for its GPU model.

### 6.4 Hardware Transport Composability

toadStool's three transports compose via TransportRouter:

```
Camera (V4L2) → TransportRouter → GPU (compute) → TransportRouter → Display (DRM)
Serial (USB) → TransportRouter → GPU (compute) → TransportRouter → Display (DRM)
```

Any input can route to any output through GPU computation. This
enables zero-copy real-time pipelines for computer vision, robotics,
and industrial control.

---

## 7. Novel Spring Recipes — Concrete Workflows

These recipes show how springs can use toadStool in ways that go beyond
"submit workload, get result." Each recipe produces emergent behavior that
none of the participants could achieve alone.

### 7.1 hotSpring: GPU-Resident Lattice QCD with Live Register Tuning

**Primals**: toadStool + barraCuda + coralReef
**Spring**: hotSpring (SU(3) HMC, 32⁴ lattice)

```
1. hotSpring requests β-scan (12 temperatures, 50 HMC trajectories each)
2. toadStool: compute.hardware.auto_init → apply best known recipe for this GPU
3. coralReef: compile SU(3) plaquette + gauge force shaders → VFIO native binary
4. barraCuda: begin HMC trajectory (GPU-resident CG solver, no CPU readback)
5. toadStool: compute.hardware.observe → snapshot register state every 100 steps
6. toadStool: compute.hardware.distill → identify FMA bottleneck → increase SM clock
7. toadStool: compute.hardware.apply → BAR0 write mid-trajectory (no restart needed)
8. Next trajectory runs 15% faster. toadStool stores recipe indexed by workload hash.
9. Future β-scans on ANY machine with same GPU model inherit the tuned recipe.
```

**Why it matters**: The GPU literally learns how to run lattice QCD better
over time. The recipe propagates through nestGate or songBird federation.
A new postdoc's laptop with the same GPU model starts fast from day one.

### 7.2 airSpring: Field Sensor → GPU → Irrigation in Real-Time

**Primals**: toadStool + barraCuda + songBird + squirrel
**Spring**: airSpring (FAO-56 ET₀, soil moisture, scheduling)

```
1. Field sensor → toadStool serial transport (USB → /dev/ttyUSB0)
2. toadStool: transport.discover → find serial device + local GPU
3. airSpring parses raw sensor frames (temp, humidity, wind, solar radiation)
4. toadStool: compute.submit → barraCuda batches 100 stations of ET₀ on GPU
5. squirrel: interpret results → "Field 7 needs 12mm irrigation by 0600"
6. songBird: route recommendation to field controller via mDNS-discovered gate
7. toadStool on field controller: serial transport → send valve command
```

**Why it matters**: The entire pipeline — from soil sensor to valve actuator —
flows through sovereign infrastructure. No cloud. No vendor API. No internet
required. The GPU batch processes 100 stations in under 50ms; serial latency
is the bottleneck, not compute.

### 7.3 wetSpring: Encrypted Metagenomic Assembly on Heterogeneous GPUs

**Primals**: toadStool + barraCuda + bearDog + nestGate + sweetGrass
**Spring**: wetSpring (Smith-Waterman, 16S rRNA, diversity indices)

```
1. wetSpring receives 16S sequences from hospital sequencer
2. bearDog: encrypt at ingest (ChaCha20-Poly1305), provision session key
3. toadStool: gpu.info → [RTX 3090 (24GB VRAM), RX 6950 XT (16GB)]
4. toadStool routes Smith-Waterman alignment to RTX 3090 (needs f64 + large VRAM)
5. toadStool routes Shannon/Simpson diversity to RX 6950 XT (memory-bandwidth-bound)
6. Both GPUs VFIO-isolated — IOMMU prevents any memory cross-contamination
7. sweetGrass: record provenance braid (input hash, GPU models, driver versions,
   VFIO group IDs, IOMMU isolation proof)
8. nestGate: store result content-addressed (input hash + hardware fingerprint)
9. loamSpine: commit provenance to permanent ledger
```

**Why it matters**: Heterogeneous GPU routing is invisible to the spring.
wetSpring asked for two computations; toadStool decided which GPU gets which.
The provenance braid includes hardware attestation — a regulatory auditor can
verify the computation ran on IOMMU-isolated hardware with specific drivers.

### 7.4 groundSpring: Topology-Aware Multi-GPU Lanczos Eigensolve

**Primals**: toadStool + barraCuda + coralReef
**Spring**: groundSpring (Lanczos, SpMV, spectral analysis)

```
1. groundSpring requests eigenvalue decomposition of 100K × 100K sparse matrix
2. toadStool: query PCIe topology → 4× GPUs, 2 pairs on shared PCIe switches
3. toadStool partitions matrix: pairs 0,1 share Switch A → adjacent rows
                                pairs 2,3 share Switch B → adjacent rows
4. Halo exchange (shared rows) between GPUs on same switch → PCIe P2P, no CPU
5. Cross-switch communication (rare) → CPU bounce, minimal traffic
6. coralReef: compile SpMV shader per-GPU (SASS for NVIDIA, RDNA2 for AMD)
7. barraCuda: parallel Lanczos iterations across all 4 GPUs
8. toadStool: monitor PCIe contention → adjust partition if bandwidth asymmetric
```

**Why it matters**: Without topology awareness, GPU 0 might exchange halos
with GPU 3 across the root bridge — 4× slower than same-switch P2P. toadStool's
topology graph makes the spring's Lanczos iteration 2-4× faster on multi-GPU
setups without the spring knowing anything about PCIe switches.

### 7.5 neuralSpring: VRAM-Aware Federated Model Sharding

**Primals**: toadStool + squirrel + songBird + barraCuda
**Spring**: neuralSpring (distributed training, inference)

```
1. neuralSpring wants to serve a 13B-parameter model (needs ~26GB VRAM)
2. songBird: discover all toadStool instances in federation
3. toadStool@machine-A: gpu.info → RTX 3090 (24GB free) — not enough alone
4. toadStool@machine-B: gpu.info → RTX 4070 (12GB free) — not enough alone
5. squirrel: shard model — layers 0-20 on machine-A, layers 21-40 on machine-B
   (24GB + 12GB = 36GB total, 26GB needed → fits with headroom)
6. toadStool@each: VFIO-isolate GPUs for exclusive inference
7. Inference request → machine-A processes layers 0-20 → intermediate activations
   → songBird encrypted transport → machine-B processes layers 21-40 → result
8. toadStool monitors VRAM pressure on both machines; if A loads another model,
   squirrel rebalances the shard split dynamically
```

**Why it matters**: No single machine has enough VRAM for the model. But the
federation does. toadStool provides per-machine hardware truth; squirrel makes
the sharding decision; songBird moves tensors. The model "lives" across machines.

### 7.6 healthSpring: Clinical Trial GPU Enclave with Audit Trail

**Primals**: toadStool + bearDog + sweetGrass + loamSpine + rhizoCrypt
**Spring**: healthSpring (population PK, NLME, dose-response)

```
1. healthSpring receives 500-patient Phase III PK dataset (HIPAA-regulated)
2. bearDog: derive session key → encrypt dataset → sign submission
3. toadStool: bind GPU to VFIO (IOMMU group 14, address 0000:06:00.0)
4. toadStool: compute.hardware.vfio_devices confirms isolation (no other processes)
5. barraCuda: run NLME population PK on VFIO-isolated GPU
6. sweetGrass: record provenance braid:
   - Agent: "healthSpring clinical trial CT-2026-0042"
   - Entity: input hash, GPU model, VFIO group, IOMMU status
   - Activity: "population_pk_nlme", duration, convergence metrics
7. rhizoCrypt: hold intermediate results in ephemeral DAG (auto-expire 72h)
8. loamSpine: commit final result + provenance to permanent ledger
9. After 72h, rhizoCrypt auto-dehydrates — intermediate patient data vanishes
10. Permanent record contains: result, provenance, hardware attestation, audit trail
    Intermediate patient data: gone. Unrecoverable.
```

**Why it matters**: The combination of VFIO isolation (toadStool), encryption
(bearDog), ephemeral storage (rhizoCrypt), provenance (sweetGrass), and permanent
ledger (loamSpine) creates a HIPAA/GDPR-compliant computation enclave. An auditor
can verify the hardware was isolated and the intermediate data is provably gone.

### 7.7 Cross-Spring: The Universal Experiment Pattern

Any spring can run a GPU experiment with full provenance, caching, and
reproducibility by composing exactly 5 primals:

```
┌─────────────────────────────────────────────────────────┐
│                    Any Spring                           │
│  "I have data X and want to compute f(X) on GPU"       │
└────────────────────┬────────────────────────────────────┘
                     │
    ┌────────────────▼───────────────┐
    │  nestGate: check cache         │
    │  key = hash(X) + hw_fingerprint│──── cache hit → return cached result
    └────────────────┬───────────────┘
                     │ cache miss
    ┌────────────────▼───────────────┐
    │  toadStool: discover hardware  │
    │  select best GPU for workload  │
    │  VFIO-isolate if needed        │
    └────────────────┬───────────────┘
                     │
    ┌────────────────▼───────────────┐
    │  barraCuda + coralReef:        │
    │  compile shader → dispatch     │
    │  → execute → return result     │
    └────────────────┬───────────────┘
                     │
    ┌────────────────▼───────────────┐
    │  sweetGrass: record provenance │
    │  (input, hardware, algorithm,  │
    │   duration, output hash)       │
    └────────────────┬───────────────┘
                     │
    ┌────────────────▼───────────────┐
    │  nestGate: cache result        │
    │  key = hash(X) + hw_fingerprint│
    └────────────────────────────────┘
```

**Every spring gets this for free.** The spring only submits the workload.
toadStool + nestGate + sweetGrass + barraCuda + coralReef handle the rest.
Second run of the same experiment with the same data on the same hardware:
instant return from cache. Different hardware? Re-computes (different GPU
may produce different floating-point results) and caches separately.

---

## 8. Creative Cross-Primal Patterns

These patterns show toadStool participating in compositions that might not
be obvious from its "hardware infrastructure" description.

### 8.1 toadStool as Provenance Witness

toadStool's hardware fingerprinting makes it a **provenance witness** — it
can attest *where* a computation ran with hardware-level specificity:

```json
{
  "witness": "toadstool",
  "attestation": {
    "gpu_model": "NVIDIA RTX 3090",
    "gpu_driver": "NVK 535.129.03",
    "pcie_slot": "0000:06:00.0",
    "vfio_isolated": true,
    "iommu_group": 14,
    "vram_total_bytes": 25769803776,
    "f64_native": true,
    "thermal_at_dispatch": "42°C",
    "power_at_dispatch": "68W"
  }
}
```

sweetGrass can embed this attestation in any provenance braid. For regulated
science, this means the computation result is linked to the exact silicon,
bus slot, and driver version that produced it. If a GPU firmware bug is later
discovered, every result computed on that firmware version can be identified
and flagged for re-validation.

### 8.2 toadStool as Power Budget Coordinator

In battery-constrained environments (field stations, clinical devices,
edge deployments), toadStool's power states compose with biomeOS scheduling:

```
biomeOS: "Battery at 23%. Restrict to essential compute."
toadStool: GPU → Eco (reduced clocks)
toadStool: NPU → Active (2.8μs inference, 0.3W — negligible power)
squirrel: route inference to NPU instead of GPU (toadStool reported GPU is Eco)
airSpring: accept NPU-quality prediction (good enough for irrigation timing)

biomeOS: "Plugged in. Full compute."
toadStool: GPU → Sovereign (full clocks)
squirrel: route inference back to GPU (toadStool reported GPU is Sovereign)
airSpring: switch to GPU-quality prediction (higher precision)
```

The spring never checks battery level. biomeOS sets policy, toadStool
enforces it at the hardware level, and squirrel adapts routing.

### 8.3 toadStool as Hardware Knowledge Broker

toadStool's hw-learn recipes are shareable knowledge artifacts:

```
Machine A (Titan V, QCD workload):
  1. toadStool observes → distills → optimal QCD recipe for Titan V
  2. nestGate: store recipe (key = "titanv_sm70_qcd_v3")
  3. songBird: announce recipe availability to federation

Machine B (Titan V, brand new):
  1. toadStool: compute.hardware.auto_init → queries nestGate for "titanv_sm70"
  2. Found! Apply "titanv_sm70_qcd_v3" without any local profiling
  3. Machine B is optimized from its first workload

Machine C (RTX 3090, different architecture):
  1. toadStool: queries nestGate for "rtx3090_sm86" → no QCD recipe yet
  2. Falls back to generic sm86 recipe → observes QCD → distills sm86 QCD recipe
  3. nestGate: store "rtx3090_sm86_qcd_v1" → federation gets another recipe
```

Over time, the federation accumulates a growing library of workload-specific
GPU tuning profiles. New hardware joining the federation bootstraps instantly
for known workload classes. This is collective hardware intelligence — each
GPU's lessons benefit every other GPU of the same model.

### 8.4 toadStool as Transport Bridge (Camera → GPU → Display → Serial)

toadStool's three hardware transports compose into real-time pipelines:

```
Scenario: Agricultural drone with camera, GPU, display, and actuator

Camera (V4L2) → toadStool capture transport
  → TransportRouter → GPU memory (zero-copy DMA)
    → barraCuda: crop disease detection shader
  → TransportRouter → Display (DRM) — pilot sees annotated camera feed
  → TransportRouter → Serial (USB) — actuator adjusts spray nozzle

All three outputs from a single camera frame:
  1. GPU processes the frame (inference)
  2. Display shows the annotated frame (visualization)
  3. Serial sends the control signal (actuation)

Latency budget: <16ms (60fps camera → display roundtrip)
```

No other primal touches hardware I/O. toadStool is the only primal that
reads cameras, writes displays, and talks to serial devices. This makes it
the natural bridge between physical world and compute.

### 8.5 toadStool + sourDough: Hardware-Aware Primal Scaffolding

sourDough scaffolds new primals. toadStool can inform the scaffold:

```
sourDough: "Scaffolding new spring 'forestSpring' (ecology domain)"
sourDough queries toadStool: compute.discover_capabilities
toadStool responds: {
  "gpu": true, "gpu_f64": true, "npu": true, "vfio": true,
  "serial_devices": 2, "capture_devices": 1,
  "optimal_tile_size_bytes": 11534336
}
sourDough generates scaffold with:
  - GPU dispatch boilerplate pre-configured for actual hardware
  - NPU inference path included (NPU detected)
  - Serial sensor input template (2 serial devices found)
  - Camera input template (1 capture device found)
  - Optimal buffer sizes baked into generated config
```

The scaffolded spring starts life aware of its actual hardware environment.
No trial-and-error discovery needed.

### 8.6 Multi-Spring Concurrent Dispatch

toadStool can serve multiple springs simultaneously on different substrates:

```
Concurrent workloads on a machine with GPU + NPU + CPU:

hotSpring  → toadStool → GPU 0 (VFIO)  → lattice QCD HMC trajectory
airSpring  → toadStool → NPU (Akida)   → crop disease classifier (2.8μs/step)
wetSpring  → toadStool → GPU 1 (wgpu)  → Smith-Waterman batch alignment
squirrel   → toadStool → CPU (Ollama)  → 3B LLM inference (Ollama integration)

All four running in parallel. toadStool manages:
  - VFIO isolation for GPU 0 (hotSpring gets exclusive access)
  - NPU routing for airSpring (zero GPU contention)
  - wgpu dispatch for GPU 1 (wetSpring shares with desktop compositor)
  - Ollama lifecycle for CPU inference (squirrel gets LLM without GPU)
  - Power monitoring across all substrates
  - Thermal throttling if any substrate overheats
```

**Why it matters**: The springs don't coordinate with each other. They each
ask toadStool for compute. toadStool routes to the right substrate and
prevents resource conflicts. This is the fundamental value of a hardware
primal — it is the single arbiter of who gets what silicon, when.

---

## 9. How Springs Should Consume toadStool

### Minimal Integration (any spring, no other primals)

```rust
// 1. Discover toadStool via capability
let socket = get_socket_path_for_capability("compute");

// 2. Check what hardware exists
let hw = jsonrpc_call(socket, "gpu.info", {});

// 3. Submit workload
let job_id = jsonrpc_call(socket, "compute.submit", {
    "shader": "my_kernel.wgsl",
    "inputs": { "data": base64_encoded_bytes },
    "workgroup_size": hw.recommended_workgroup_size
});

// 4. Poll for result
let result = jsonrpc_call(socket, "compute.result", { "id": job_id });
```

That's it. Four calls. The spring never imports a GPU library.

### Full Integration (with Compute Trio + Provenance)

```rust
// Capability-based discovery — works even if primals move or scale
let compute = discover_capability("compute");      // toadStool
let shader  = discover_capability("shader");       // coralReef (optional)
let crypto  = discover_capability("crypto");       // bearDog (optional)
let storage = discover_capability("storage");      // nestGate (optional)
let prov    = discover_capability("provenance");   // sweetGrass (optional)

// Each primal is optional. toadStool works standalone.
// coralReef absent? toadStool falls back to naga.
// nestGate absent? No caching, still computes.
// sweetGrass absent? No provenance, still computes.
```

### What NOT to Do

- **Don't hardcode socket paths** — use `get_socket_path_for_capability()`
- **Don't import wgpu/vulkan** — toadStool owns the GPU boundary
- **Don't manage GPU power** — toadStool manages power states
- **Don't assume GPU exists** — toadStool reports CPU fallback when no GPU
- **Don't assume VRAM size** — query `gpu.info` at runtime
- **Don't coordinate GPU access between springs** — toadStool arbitrates

---

## 10. What toadStool Does NOT Do

toadStool is deliberately bounded. It does not:

- **Compute math** — that's barraCuda
- **Compile shaders** — that's coralReef (toadStool proxies with naga fallback)
- **Store data** — that's nestGate
- **Encrypt data** — that's bearDog
- **Route network traffic** — that's songBird
- **Manage identity** — that's bearDog/biomeOS
- **Record provenance** — that's sweetGrass
- **Render UI** — that's petalTongue
- **Coordinate AI models** — that's squirrel
- **Orchestrate the ecosystem** — that's biomeOS

toadStool owns the hardware. The silicon, the bus, the power, the
memory, the display, the camera, the serial port. Everything else
is delegated to the primal that owns that domain. This is the
sovereignty principle.

---

## 11. Every Piece of Silicon — toadStool's Evolution Path

*Driven by the ludoSpring V24 GPU Fixed-Function Science Repurposing audit.
See `wateringHole/GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md`.*

The DF64 discovery proved that "graphics hardware" is really "math hardware
with a graphics API painted on top." A modern GPU die has at least **eight
distinct hardware units**, each a special-purpose computer. toadStool's
role is to discover, route to, and dispatch work across ALL of them.

### 11.1 Current Silicon Map (S158)

| Silicon | toadStool Status | Dispatch Path |
|---------|-----------------|---------------|
| **GPU Shader Cores** | Implemented | wgpu (default), VFIO sovereign (WIP) |
| **GPU (OpenCL)** | Implemented | Feature-gated `opencl`, `ocl` crate |
| **GPU (CUDA)** | Implemented | Feature-gated `cuda`, `cudarc` |
| **GPU (Vulkan)** | Partial | Feature-gated, recommends wgpu |
| **NPU (Akida AKD1000/1500)** | Implemented | Kernel, VFIO, Userspace backends |
| **CPU** | Implemented | rayon, Ollama integration |
| **GPU Tensor Cores** | Not yet | Needs coralReef MMA emission + toadStool routing |
| **GPU RT Cores** | Not yet | Needs coralReef BVH build + toadStool routing |
| **GPU TMUs** | Not yet | Needs graphics pipeline state + texture binding |
| **GPU ROPs / Alpha Blend** | Not yet | Needs graphics pipeline state + framebuffer mgmt |
| **GPU Rasterizer** | Not yet | Needs draw command submission |
| **GPU Tessellator** | Not yet | Needs hull/domain shader pipeline |
| **GPU Video Enc/Dec** | Not yet | Needs NVENC/VCN dispatch |
| **Metal** | Stub | Enum variant only |
| **ROCm** | Stub | Mentioned in docs |
| **DirectCompute** | Stub | Enum variant only |

### 11.2 What toadStool Must Evolve

**Phase A — Sovereign Compute (current P0)**

The sovereign compute pipeline (VFIO dispatch for shader cores) is the
prerequisite for everything that follows. All fixed-function unit access
goes through the same VFIO channel.

| Item | Status | Blocker |
|------|--------|---------|
| VFIO device binding + BAR0 | Done | — |
| DMA allocation | Done | — |
| Power management (nvpmu) | Done | — |
| Compute dispatch (PBDMA) | WIP | coralReef USERD_TARGET fix |
| Buffer readback | Not wired | ~200 LOC plumbing |
| E2E sovereign test | Blocked | Needs dispatch + readback |

**Phase B — Performance Surface Database (new)**

toadStool needs a measured performance surface — the
`(operation, hardware_unit, precision, throughput)` tuples from spring
experiments — to make routing decisions based on real data:

```
compute.performance_surface.report {
  "operation": "math.pairwise.yukawa",
  "hardware_unit": "tensor_core",
  "precision": "tf32",
  "throughput_gflops": 71000,
  "tolerance_achieved": 1e-7,
  "gpu_model": "RTX 3090",
  "measured_by": "hotSpring exp076"
}

compute.performance_surface.query {
  "operation": "math.pairwise.yukawa",
  "tolerance_required": 1e-14,
  "available_units": ["shader_core", "tensor_core", "tmu"]
}
→ { "recommended": "shader_core", "mode": "df64", "throughput": 3240 }
```

This is an extension of hw-learn — from profiling one GPU as a whole
to profiling each hardware unit on the GPU for each operation class.

**Phase C — Multi-Unit Routing (new)**

Extend the dispatch router from "which GPU" to "which unit ON the GPU":

```
compute.route {
  "workload": [
    { "op": "neighbor_search", "tolerance": 1e-2, "data_size": 1000000 },
    { "op": "force_eval", "tolerance": 1e-14, "data_size": 1000000 },
    { "op": "accumulation", "tolerance": 1e-7, "data_size": 1000000 }
  ]
}
→ {
  "plan": [
    { "op": "neighbor_search", "unit": "rt_core", "reason": "spatial query, 10x over compute" },
    { "op": "force_eval", "unit": "shader_core", "mode": "df64", "reason": "14-digit tolerance" },
    { "op": "accumulation", "unit": "rop_blend", "reason": "additive scatter, 5x over atomics" }
  ]
}
```

Graceful degradation: RT cores unavailable → route neighbor_search to
shader cores (compute BVH). Tensor cores unavailable → route matrix ops
to shader cores. The math is the same; the throughput changes.

**Phase D — Mixed Command Stream Submission (new)**

The sovereign VFIO path submits compute dispatches via PBDMA. For
fixed-function units, toadStool needs to submit mixed command streams:

| Command Type | GPU Mechanism | toadStool Role |
|--------------|--------------|----------------|
| Compute dispatch | PBDMA `DISPATCH(groups)` | Current path (Phase A) |
| Draw (rasterizer) | PBDMA `DRAW(vertices)` | New: vertex buffer + pipeline state |
| RT trace | PBDMA `TRACE_RAY(...)` | New: BVH + ray generation |
| Framebuffer ops | ROP config registers | New: blend mode, depth func |
| Texture binding | TMU descriptor | New: texture handle + sampler |
| Tensor MMA | SM ISA (`HMMA`/`IMMA`) | New: coralReef emits MMA instructions |

This is NOT a rewrite — it's extending the existing PBDMA submission
with additional command types. The submission mechanism is identical;
the payloads differ per hardware unit.

### 11.3 Tolerance-Based Routing — The Key Innovation

The precision spectrum from `GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md`:

```
Tolerance → Precision → Cheapest Hardware (RTX 3090) → Throughput
1e-2        ~3 digits   FP16 tensor cores               ~142 TFLOPS
1e-4        ~5 digits   FP16 tensor cores               ~142 TFLOPS
1e-7        ~7 digits   FP32 shader cores                ~35.6 TFLOPS
1e-10       ~10 digits  TF32 tensor cores (accumulated)  ~71 TFLOPS
1e-14       ~14 digits  DF64 on FP32 shader cores        ~3.24-8.9 TFLOPS
1e-16       ~16 digits  Native FP64                      ~0.33 TFLOPS
1e-30       ~30 digits  Software arbitrary precision      ~0.01 TFLOPS
```

**toadStool picks the row. coralReef compiles for it. Springs never see
the table.** A spring calls `barraCuda.math.pairwise.yukawa(tolerance=1e-14)`
and toadStool routes to DF64 shader cores on the RTX 3090, native fp64 on
the Titan V, or software emulation on a Raspberry Pi. The math is identical.

### 11.4 ludoSpring-Specific Silicon Opportunities

ludoSpring's game science experiments (`exp076`) target:

| Experiment | Hardware Unit | Expected Gain |
|------------|--------------|---------------|
| Fog of war visibility | Rasterizer | 10-50x over per-tile ray march |
| Pathfinding heuristic | Z-buffer (depth) | 100x over wavefront BFS |
| Influence maps | ROPs (blend) | 5-10x over CPU loop |
| Acoustic ray tracing | RT cores | 1000x over analytical model |
| Engagement curves | TMUs | 5-20x over analytical eval |
| DDA raycaster rendering | Shader cores | Closes the render gap |

These discoveries flow upstream: rasterizer visibility → airSpring terrain
analysis; RT acoustics → airSpring environmental acoustics; Z-buffer
distance → groundSpring geological Voronoi.

### 11.5 Sovereign Pipeline — What Unlocks What

```
Phase A (current): VFIO compute dispatch
  → Every spring gets sovereign shader core compute
  → hotSpring Kokkos gap closes
  → neuralSpring coralForge pipeline runs sovereign
  → ludoSpring game shaders dispatch without Vulkan

Phase B: Performance surface database
  → toadStool makes data-driven routing decisions
  → hw-learn evolves from "whole GPU" to "per-unit" profiling

Phase C: Multi-unit routing
  → Single workload splits across shader + tensor + RT + TMU
  → Compound throughput: 50-100 effective TFLOPS per RTX 3090
  → No existing framework does this

Phase D: Mixed command streams
  → Graphics pipeline state for rasterizer/depth/blend science
  → RT pipeline state for BVH-accelerated neighbor search
  → Tensor MMA instructions alongside compute shaders
  → Single dispatch uses ALL silicon on the die
```

**Compound effect**: A single RTX 3090 today delivers 0.33 native fp64
TFLOPS. With DF64: 3.24 TFLOPS. With the full hardware budget — all
eight units running in parallel on different parts of the problem — the
effective science throughput could reach 50-100 TFLOPS equivalent. That
is a small HPC cluster in a single PCIe slot.

---

## References

- `toadStool/README.md` — Full primal documentation
- `toadStool/STATUS.md` — Detailed technical status
- `toadStool/DEBT.md` — Active debt register and evolution paths
- `toadStool/specs/PRIMAL_CAPABILITY_SYSTEM.md` — Capability system spec
- `toadStool/specs/SOVEREIGN_COMPUTE_EVOLUTION.md` — Sovereign compute plan
- `wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` — Full sovereign stack plan
- `wateringHole/GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md` — All-silicon targeting
- `wateringHole/BARRACUDA_LEVERAGE_GUIDE.md` — barraCuda leverage guide
- `wateringHole/CORALREEF_LEVERAGE_GUIDE.md` — coralReef leverage guide
- `wateringHole/INTER_PRIMAL_INTERACTIONS.md` — IPC coordination
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming convention
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/SPRING_CATALOG.md` — Spring catalogue
