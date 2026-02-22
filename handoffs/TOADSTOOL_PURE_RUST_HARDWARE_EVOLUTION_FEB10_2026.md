# ToadStool Handoff: Pure Rust Hardware Evolution

**Date**: February 10, 2026
**From**: ecoPrimals Control Team (Eastgate)
**To**: ToadStool / BarraCuda Team
**Priority**: HIGH — Enables full heterogeneous compute pipeline

---

## Executive Summary

BarraCuda already has an extraordinary foundation: **401 WGSL shaders**, a **unified device
abstraction** (CPU/GPU/NPU/TPU), and a **pure Rust Akida driver**. This handoff details what
needs to evolve to achieve a single pure-Rust binary that dispatches computation to the optimal
hardware — GPU via WGSL shaders, NPU via compiled models, or CPU via native Rust — without
any C dependencies, Python SDKs, or kernel module maintenance.

**Key Insight**: GPUs, NPUs, and TPUs are fundamentally different compute architectures.
BarraCuda should not try to make them all look the same. Instead, it should be **agnostic about
which hardware runs**, but **specific about how each hardware type receives work**.

---

## Part 1: Current Inventory

### 1.1 WGSL Shader Inventory (401 total)

| Category | Count | Purpose | Status |
|----------|-------|---------|--------|
| Core ML/Math | 365 | Activations, losses, optimizers, attention, pooling, normalization, etc. | ✅ Production |
| FHE Operations | 13 | NTT, INTT, PolyAdd, PolyMul, PolySub, KeySwitch, ModulusSwitch, Boolean gates | ✅ Production |
| Complex Numbers | 10 | add, sub, mul, div, exp, log, pow, sqrt, abs, conj | ✅ Production |
| MD/Physics Forces | 5 | Coulomb, Lennard-Jones, Yukawa, Morse, Born-Mayer | ✅ Production |
| MD/Physics Integrators | 3 | Velocity-Verlet, RK4, Laplacian | ✅ Production |
| MD/Physics PBC | 1 | Periodic boundary conditions | ✅ Production |
| FFT | 2 | 1D FFT butterfly + IFFT normalize | ✅ Production |
| Utility | 2 | u64_emu, sparse_matmul_quantized | ✅ Production |

### 1.2 Rust Device Backends

| Backend | File | Status | Talks To |
|---------|------|--------|----------|
| **WgpuDevice** | `device/wgpu_device.rs` | ✅ Complete | Any GPU via Vulkan/Metal/DX12 |
| **AkidaExecutor** | `device/akida_executor.rs` | ✅ Complete | Akida NPU via akida-driver |
| **TpuDevice** | `device/tpu.rs` | ⚠️ Scaffolded | TPU via libtpu FFI (not wired) |
| **Unified** | `device/unified.rs` | ✅ Complete | Workload-based auto-dispatch |
| **Substrate** | `device/substrate.rs` | ✅ Complete | Per-vendor GPU selection |
| **Capabilities** | `device/capabilities.rs` | ✅ Complete | Runtime limit discovery |

### 1.3 Pure Rust Akida Driver (`akida-driver` crate)

| Module | Status | Description |
|--------|--------|-------------|
| `discovery.rs` | ✅ Complete | Scans sysfs for BrainChip vendor 0x1E7C |
| `capabilities.rs` | ✅ Complete | Queries NPU count, memory, PCIe config, power, temp |
| `device.rs` | ✅ Complete | Opens `/dev/akida*`, read/write via file I/O |
| `io.rs` | ✅ Complete | Raw FD-based DMA transfers |
| `inference.rs` | ✅ Complete | Input validation → DMA write → read output |
| `loading.rs` | ✅ Complete | Chunked model loading with checksums |
| `error.rs` | ✅ Complete | Typed error hierarchy |

**Dependencies**: `nix` (ioctl), `libc` (O_NONBLOCK), `thiserror`, `tracing`

---

## Part 2: GPU vs NPU vs TPU — How They Actually Differ

This is the core architectural insight. **These are not interchangeable compute units.**
Each has a fundamentally different execution model.

### 2.1 GPU (via WGSL/wgpu)

```
DISPATCH MODEL: Submit shader → GPU runs ALL threads in parallel → Read back results
```

- **Execution**: Massively parallel SIMD. Thousands of threads run the SAME shader simultaneously
- **Input**: Raw buffers (arrays of f32, u32, vec2, etc.) bound to shader bindings
- **Programming**: Write a WGSL shader, dispatch workgroups, read storage buffers
- **Strengths**: Dense computation, matrix ops, FFT, physics forces, everything that's embarrassingly parallel
- **Power**: 100-350W (RTX 3090: 350W, RTX 4070: 200W)
- **What BarraCuda does today**: ✅ Ships 401 WGSL shaders, dispatches via wgpu

**GPU receives**: Raw math instructions (WGSL shaders)
**GPU returns**: Raw computed buffers

### 2.2 NPU/Akida (via akida-driver)

```
DISPATCH MODEL: Load compiled model → Feed input → NPU runs pre-configured neural network → Read output
```

- **Execution**: Event-driven spiking neural network. Neural processors fire ONLY on input events
- **Input**: Quantized uint8 tensors (or sparse events). Must match the compiled model's input shape
- **Programming**: You DON'T write shaders. You train a Keras model → convert with `cnn2snn`/`quantizeml` → compile to binary → load onto NPU
- **Strengths**: Inference of pre-trained models at 1000x lower energy than GPU. Sparse data (mostly zeros) = mostly zero power
- **Power**: 1-2W total (!!!)
- **What BarraCuda does today**: ✅ Discovers device, loads models, runs inference via pure Rust driver

**NPU receives**: Pre-compiled neural network model + quantized input tensor
**NPU returns**: Classification/regression output vector

### 2.3 TPU (via libtpu / Edge TPU)

```
DISPATCH MODEL: Compile TF/JAX graph → TPU executes fused operations → Read results
```

- **Execution**: Systolic array. Fixed matrix multiply units that pipeline data through
- **Input**: TensorFlow/JAX computation graphs, compiled to TPU instructions
- **Programming**: Write in TF/JAX, compiler converts to TPU ops. Coral Edge TPU needs TFLite models
- **Strengths**: Large matrix multiplications, training, sustained throughput
- **Power**: 250W (Cloud TPU v4) or 2W (Coral Edge)
- **What BarraCuda does today**: ⚠️ Scaffolded but not wired

**TPU receives**: Compiled computation graph (XLA)
**TPU returns**: Computed tensors

### 2.4 The Key Insight

```
GPU:  "Here's the math, run it on these buffers"     → PROGRAMMABLE MATH ENGINE
NPU:  "Here's a trained model, classify this input"   → PRE-COMPILED INFERENCE ENGINE
TPU:  "Here's a computation graph, execute it"         → GRAPH EXECUTION ENGINE
```

**BarraCuda should NOT try to run WGSL shaders on an NPU.** That's like trying to run
assembly on a calculator. Instead, BarraCuda should:

1. **Know what each device is good at** (already done: `WorkloadHint`)
2. **Route workloads to the right device** (already done: `Device::select_for_workload`)
3. **Speak each device's native language** (needs evolution)

---

## Part 3: Evolution Roadmap

### 3.1 Priority 1: VFIO Pure Rust NPU Driver (Eliminate C Kernel Module)

**Status**: The C kernel driver (`akida_dw_edma`) was patched for kernel 6.17 but requires
`sudo` to install and breaks with every kernel update. VFIO eliminates all of this.

**Current path**: `Rust → /dev/akida0 → C kernel module → PCIe DMA → AKD1000`
**Target path**: `Rust → /dev/vfio/21 → VFIO userspace DMA → PCIe → AKD1000`

**Eastgate system status** (verified Feb 10, 2026):
- `/dev/vfio/vfio` exists ✅
- IOMMU enabled (DMA-FQ mode) ✅
- AKD1000 is in solo IOMMU group 21 (only `0000:07:00.0`) ✅
- PCIe: Gen2 x1, 5.0 GT/s ✅

**Changes needed in `akida-driver`**:

| File | Change | Effort |
|------|--------|--------|
| `device.rs` | Add `VfioBackend` alongside `FileBackend` for device I/O | 2-3 days |
| `io.rs` | Implement VFIO DMA transfer via `nix::ioctl` on `/dev/vfio/{group}` | 3-5 days |
| `discovery.rs` | Add VFIO device detection path (check IOMMU groups in sysfs) | 1 day |
| New: `vfio.rs` | VFIO setup: open container, get group, set IOMMU type, get device FD | 2-3 days |
| New: `bar.rs` | PCIe BAR memory mapping from userspace (mmap via VFIO region info) | 2-3 days |
| New: `dma.rs` | DMA engine programming (replace what C driver's eDMA code does) | 5-7 days |

**Total**: ~3-4 weeks

**Reference**: The C driver's DMA logic is in `akida-pcie-core.c`. Key constants:
- BAR_0: Main register space
- DMA RAM at physical `0x20000000`
- Max DMA transfer chunk: 1024 bytes
- Uses DesignWare eDMA (linked-list mode, 2 TX + 2 RX channels)

**Benefits**:
- No `sudo` needed (user owns VFIO device)
- No kernel version compatibility issues (never breaks on kernel upgrade)
- Single `cargo build` produces working binary
- Can run in containers/sandboxes

### 3.2 Priority 2: NPU Model Pipeline (Train → Compile → Deploy from Rust)

The NPU can't run arbitrary shaders. It needs **pre-compiled neural network models**. Currently
this requires the Python SDK (`akida` + `cnn2snn`/`quantizeml`). The goal is a pure Rust pipeline.

**Current Python workflow**:
```
Keras model → quantizeml (quantize to 4-bit/1-bit) → cnn2snn (convert to SNN) → .fbz model → akida SDK → NPU
```

**Target Rust workflow**:
```
BarraCuda tensor ops → Quantize (Rust) → Model binary format → akida-driver → NPU
```

**What ToadStool should build**:

| Component | Description | Effort |
|-----------|-------------|--------|
| `npu/quantize.rs` | Quantize f32 weights to 1/2/4-bit using existing `quantize.wgsl` shader | 1 week |
| `npu/model_format.rs` | Parse/generate Akida model binary format (reverse-engineer `.fbz`) | 2-3 weeks |
| `npu/compiler.rs` | Map BarraCuda layers → Akida layer configs (CNP/FNP types) | 2-3 weeks |
| `npu/calibration.rs` | Post-training calibration using representative dataset | 1 week |

**Priority order**: `quantize.rs` first (enables mixed CPU+NPU inference immediately).

**Important AKD1000 V1 constraints** (discovered on Eastgate):
- V1 chip uses `InputConvolutional` + `FullyConnected` layers (NOT V2's `InputConv2D`/`Dense1D`)
- `InputConvolutional` runs in software (CPU) on V1 — only `FullyConnected` runs on hardware NPU
- Max weight precision: 1-bit for V1 conv, 1-bit for FC
- 78 neural processors available (CNP1: 26, CNP2: 26, FNP2: 13, FNP3: 13)
- 320 memory units

### 3.3 Priority 3: Hardware-Agnostic Dispatch Router

The `unified.rs` and `WorkloadHint` system is already well-designed. It needs deepening:

**Current** (working but coarse):
```rust
match workload {
    WorkloadHint::SparseEvents => Device::NPU,
    WorkloadHint::LargeMatrices => Device::GPU,
    WorkloadHint::SmallWorkload => Device::CPU,
    _ => if GPU.available() { GPU } else { CPU }
}
```

**Target** (fine-grained, science-aware):
```rust
match workload {
    // Physics: Always GPU (needs WGSL shaders for arbitrary math)
    WorkloadHint::PhysicsForce { particle_count } => Device::GPU,
    WorkloadHint::FFT { size } => Device::GPU,
    WorkloadHint::EigenDecomp { matrix_size } => Device::GPU,

    // Pre-screening: NPU ideal (binary classify, ultra-low power)
    WorkloadHint::BinaryClassifier { input_shape, sparsity }
        if sparsity > 0.5 && Device::NPU.is_available() => Device::NPU,

    // Surrogate evaluation: GPU for RBF kernel, NPU for pre-filter
    WorkloadHint::SurrogatePredict { n_points } => Device::GPU,
    WorkloadHint::SurrogatePrescreen { n_candidates } => Device::NPU,

    // Matrix ops: GPU for large, CPU for small
    WorkloadHint::MatMul { m, n, k } if m * n > 10_000 => Device::GPU,
    WorkloadHint::MatMul { .. } => Device::CPU,

    // Training: GPU always (needs gradient shaders)
    WorkloadHint::Training { .. } => Device::GPU,

    // Inference: NPU if model fits, GPU otherwise
    WorkloadHint::Inference { model_size, quantized: true } => Device::NPU,
    WorkloadHint::Inference { .. } => Device::GPU,
}
```

**Key addition**: `WorkloadHint` should carry enough metadata for the router to make
intelligent decisions about data size, sparsity, and whether a pre-compiled model exists.

### 3.4 Priority 4: Missing Shaders for Scientific Computing

The 401 existing shaders cover ML comprehensively. For the physics pipeline, these are still needed:

| Shader | Category | Purpose | Ancestor |
|--------|----------|---------|----------|
| `fft_2d.wgsl` | FFT | 2D FFT for spatial transforms | `fft_1d.wgsl` |
| `fft_3d.wgsl` | FFT | 3D FFT for PPPM | `fft_1d.wgsl` |
| `rfft.wgsl` | FFT | Real-to-complex optimization | `fft_1d.wgsl` |
| `bessel_j0.wgsl` | Special Functions | Bessel J₀ for cylindrical coords | `lgamma.wgsl` |
| `bessel_j1.wgsl` | Special Functions | Bessel J₁ | `lgamma.wgsl` |
| `bessel_i0.wgsl` | Special Functions | Modified Bessel I₀ | `lgamma.wgsl` |
| `bessel_k0.wgsl` | Special Functions | Modified Bessel K₀ | `lgamma.wgsl` |
| `spherical_harmonics.wgsl` | Special Functions | Y_lm for multipole | trig suite |
| `cholesky.wgsl` | Linear Algebra | Cholesky decomposition for RBF | `inverse.wgsl` |
| `eigh.wgsl` | Linear Algebra | Eigenvalue decomposition | `determinant.wgsl` |
| `linsolve.wgsl` | Linear Algebra | Linear system solve for RBF | `inverse.wgsl` |
| `rbf_kernel.wgsl` | Interpolation | RBF kernel evaluation | `cdist.wgsl` |
| `loo_cv.wgsl` | Statistics | Leave-one-out cross-validation | `reduce.wgsl` |
| `prng_xoshiro.wgsl` | Random | High-quality PRNG for MC/Langevin | new |
| `sparse_matvec.wgsl` | Sparse | Sparse matrix-vector product | `sparse_matmul_quantized.wgsl` |

**Total**: 15 new shaders, all with clear ancestral code in the existing codebase.

---

## Part 4: How the Hardware Pipeline Works (End-to-End)

Here's the vision for a single-binary heterogeneous compute pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                    BarraCuda Pure Rust Binary                    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  WorkloadHint │  │ DeviceRouter │  │  FallbackChain       │  │
│  │  (metadata)   │→│ (capability  │→│  GPU→CPU (always)     │  │
│  │              │  │  matching)   │  │  NPU→CPU (sparse)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│         │                  │                    │                │
│    ┌────┴────┐      ┌─────┴─────┐      ┌──────┴──────┐        │
│    │ GPU Path│      │ NPU Path  │      │  CPU Path   │        │
│    │ (WGSL)  │      │ (Model)   │      │  (Rust)     │        │
│    └────┬────┘      └─────┬─────┘      └──────┬──────┘        │
└─────────┼─────────────────┼────────────────────┼────────────────┘
          │                 │                    │
     ┌────▼────┐      ┌────▼────┐         ┌────▼────┐
     │  wgpu   │      │  VFIO   │         │ Native  │
     │ Vulkan/ │      │ PCIe    │         │  Rust   │
     │ Metal   │      │ DMA     │         │  Code   │
     └────┬────┘      └────┬────┘         └────┬────┘
          │                │                    │
     ┌────▼────┐      ┌────▼────┐         ┌────▼────┐
     │ RTX 4070│      │ AKD1000 │         │  i9-12K │
     │  200W   │      │   2W    │         │  125W   │
     │  GPU    │      │  NPU    │         │  CPU    │
     └─────────┘      └─────────┘         └─────────┘
```

### GPU Path (WGSL Shaders)
1. BarraCuda selects WGSL shader for the operation
2. Binds input/output storage buffers
3. Dispatches compute workgroups via wgpu
4. Reads results from GPU memory
5. **Works on ANY GPU**: NVIDIA (Vulkan), AMD (Vulkan), Intel (Vulkan), Apple (Metal)

### NPU Path (Pre-compiled Models)
1. BarraCuda checks if a compiled model exists for this workload
2. Quantizes input (f32 → uint8) via `EventCodec`
3. Writes quantized tensor to NPU via VFIO DMA
4. NPU runs compiled neural network on spiking hardware
5. Reads output, dequantizes back to f32
6. **Key**: Only useful for inference of pre-trained models, NOT arbitrary math

### CPU Path (Native Rust)
1. BarraCuda runs the operation directly in Rust
2. Uses SIMD intrinsics where available (via `packed_simd2` or `std::simd`)
3. Leverages `rayon` for data parallelism across CPU cores
4. **Always available as fallback**

### Can the NPU Do Arbitrary Math?

**No.** The NPU is a fixed-function neural inference engine. It can only run pre-compiled
neural network models with quantized weights. You cannot run "FFT" or "eigenvalue decomposition"
on it directly.

**However**, the NPU can participate in scientific workflows as:
- **Pre-screening filter**: Train a small classifier (physical/unphysical) and run it at 1000x
  lower energy to filter candidates before expensive GPU computation
- **Surrogate evaluator**: Train a neural network to approximate expensive objective functions,
  then run the approximation on the NPU at near-zero power
- **Reservoir computer**: Echo State Networks (ESN) use fixed random weights — the NPU's
  fixed-weight architecture is a natural fit. ToadStool already has `esn_v2.rs`!

### Can Weights Be Manipulated Directly?

**Yes, partially.** For reservoir computing / echo state networks:
- The NPU's weights are fixed after loading (that's the design — spiking architecture)
- But the readout layer (linear regression on reservoir states) can be computed on CPU/GPU
- The reservoir itself (fixed random weights + nonlinear activation) can potentially run on NPU
  with manually crafted weight matrices loaded via the driver

This is a key research opportunity: use `akida-driver`'s `ModelLoader` to load hand-crafted
weight matrices (not from `cnn2snn`) and exploit the spiking dynamics directly. The AKD1000
has 78 neural processors — each one IS a reservoir.

---

## Part 5: Immediate Action Items

### For ToadStool Team

1. **VFIO Backend for `akida-driver`** (3-4 weeks)
   - Add `vfio.rs` module with VFIO container/group/device management
   - Implement BAR mapping and DMA from userspace
   - Update `discovery.rs` to detect VFIO-eligible devices
   - Test on Eastgate (AKD1000 in IOMMU group 21)

2. **Fix `is_npu_available()`** (1 day)
   - Currently hardcoded to `false` in `unified.rs:354`
   - Should check `/dev/akida*` or `/dev/vfio/*` at runtime

3. **Add Science-Aware WorkloadHints** (1 week)
   - `PhysicsForce`, `FFT`, `EigenDecomp`, `SurrogatePrescreen`, etc.
   - Route physics to GPU, pre-screening to NPU

4. **Remaining FFT Shaders** (2-3 weeks)
   - `fft_2d.wgsl`, `fft_3d.wgsl`, `rfft.wgsl`
   - All evolve from existing `fft_1d.wgsl` (row-column decomposition)

5. **Linear Algebra Shaders** (2-3 weeks)
   - `cholesky.wgsl`, `eigh.wgsl`, `linsolve.wgsl`
   - Critical for surrogate learning (RBF training) on GPU

6. **Bessel Function Shaders** (2 weeks)
   - `bessel_j0.wgsl`, `bessel_j1.wgsl`, `bessel_i0.wgsl`, `bessel_k0.wgsl`
   - Follow `lgamma.wgsl` pattern (polynomial/rational approximation)

### For ecoPrimals Control Team

7. **Keep C kernel driver operational** (done — patched for 6.17)
   - This is the bridge until VFIO backend is ready

8. **Train NPU pre-screening model** (after VFIO)
   - Use existing L1 surrogate data to train binary classifier
   - Physical/unphysical Skyrme parameters at near-zero power

---

## Part 6: Strandgate Configuration Note

Strandgate tower has **2× Akida chips** (PCIe slots). The VFIO approach enables:
- Both chips accessible without any kernel module
- Round-robin scheduling via existing `AkidaExecutor` (already supports multi-board!)
- 160 total neural processors across 2 boards
- ~4W total power for dual-NPU inference

The existing `akida_executor.rs` multi-board scheduling is already designed for this:
```rust
pub struct AkidaExecutor {
    boards: Arc<Vec<AkidaBoard>>,
    current_board: Arc<AtomicUsize>,  // Round-robin
    total_npus: usize,
}
```

---

## Summary

| Component | Status | What's Needed | Weeks |
|-----------|--------|---------------|-------|
| GPU (WGSL) dispatch | ✅ Working | 15 new science shaders | 6-8 |
| NPU (Akida) dispatch | ✅ Working (C driver) | VFIO backend for pure Rust | 3-4 |
| TPU dispatch | ⚠️ Scaffolded | Wire to actual hardware (low priority) | TBD |
| WorkloadHint router | ✅ Working (coarse) | Science-aware hints | 1 |
| Unified Device | ✅ Working | Fix `is_npu_available()` | 1 day |
| Model pipeline (NPU) | ❌ Python-only | Rust quantizer + model format | 4-6 |
| **TOTAL for pure Rust heterogeneous compute** | | | **~15-20 weeks** |

**The architecture is sound.** BarraCuda already thinks about hardware the right way — it
discovers capabilities at runtime, routes workloads by hint, and provides fallback chains.
The evolution is about deepening each path (GPU: more shaders, NPU: VFIO + model pipeline)
and connecting them to the scientific computing workflow.

**One binary. Three hardware paths. Zero C dependencies. Zero Python dependencies.**

---

*Repository*: `toadStool` (all relevant code in `crates/barracuda/` and `crates/neuromorphic/akida-driver/`)
*Contact*: ecoPrimals Control Team
*License*: AGPL-3.0

