# Sovereign Compute Evolution — Pure Rust GPU Stack

**Date**: March 8, 2026 (updated — Layer 1 complete)
**From**: hotSpring (validated by Kokkos-CUDA parity testing)
**To**: All primals — toadStool, barraCuda, coralReef, springs
**Type**: Long-term architecture evolution plan
**Goal**: Replace every non-Rust dependency in the GPU compute path with
sovereign Rust implementations, scaffolded off existing open-source systems.

---

## Current Stack (March 2026)

```
Layer 6  barraCuda         Rust     WE OWN    Math, shaders, precision strategy
Layer 5  naga              Rust     Mozilla   WGSL → SPIR-V compiler
Layer 4  wgpu              Rust     gfx-rs    GPU abstraction over Vulkan
Layer 3  Vulkan API        C        Khronos   Spec + loader (libvulkan)
Layer 2  NVK               C+Rust   Mesa      NVIDIA Vulkan driver
Layer 1  NAK               Rust     Mesa      NVIDIA shader compiler (SPIR-V → machine code)
Layer 0  nouveau           C        Linux     Kernel DRM driver (memory, DMA, cmd submit)
         ─────────────────────────────────────────────────
         NVIDIA hardware   silicon  NVIDIA    GA102 (Ampere), GV100 (Volta), etc.
```

**What we own**: Layer 6 (barraCuda + toadStool + springs)
**What we use but don't own**: Layers 1-5 (all open-source, MIT/Apache)
**What we work around**: Layers 1-2 (NAK f64 gaps, NVK allocation limits)
**What we can't change**: Layer 0 (kernel, hardware)

---

## Target Stack (Sovereign)

```
Layer 6  barraCuda         Rust     WE OWN    Math, shaders, precision strategy
Layer 5  naga              Rust     WE FORK   WGSL → SPIR-V (+ direct ISA path)
Layer 4  wgpu / coralGpu   Rust     WE OWN    GPU abstraction (Vulkan or direct)
Layer 3  (optional)        Rust     WE OWN    Minimal Vulkan-compatible dispatch
Layer 2  coralDriver       Rust     WE OWN    Userspace GPU driver (replaces NVK)
Layer 1  coralNak          Rust     WE OWN    Shader compiler (replaces NAK)
Layer 0  vfio-pci / kmod   Rust     WE OWN    Userspace DMA or thin kernel module
         ─────────────────────────────────────────────────
         ANY GPU hardware  silicon  any       Vulkan-capable or direct-mapped
```

Every layer pure Rust. No C dependencies. No vendor lock-in.
Hardware becomes interchangeable — the math is sovereign.

---

## Primal Ownership

| Layer | Component | Owner | Scaffolds From | Status |
|:---:|---|---|---|---|
| 6 | Shader math (WGSL f64/DF64) | **barraCuda** | Original | ✅ Production (zero unsafe) |
| 6 | Precision strategy (Fp64Strategy) | **barraCuda** | Original | ✅ Production (zero unsafe) |
| 6 | Sovereign compiler (FMA, DCE) | **barraCuda** | naga + original | ✅ Safe WGSL roundtrip (all backends) |
| 6 | Physics validation | **springs** | Papers | ✅ Production |
| 5 | WGSL ↔ naga IR ↔ WGSL | **barraCuda** | Mozilla naga | ✅ Using upstream (wgsl-in + wgsl-out) |
| 5 | WGSL → ISA direct (bypass SPIR-V) | **coralReef** | NAK + naga | ⬜ Level 3 |
| 4 | GPU abstraction (wgpu fork/replace) | **toadStool** | gfx-rs wgpu | 🔄 Using upstream |
| 4 | Hardware discovery + capability | **toadStool** | wgpu adapters | ✅ GpuAdapterInfo |
| 4 | Multi-adapter selection | **toadStool** | Original | ✅ TOADSTOOL_GPU_ADAPTER |
| 3 | Vulkan dispatch (minimal) | **toadStool** | ash (Rust Vulkan) | ⬜ Level 4 |
| 2 | Userspace GPU driver | **groundSpring** | NVK (Mesa) | ⬜ Level 4 |
| 2 | Memory management | **groundSpring** | NVK + nouveau | ⬜ Level 4 |
| 2 | Command buffer builder | **groundSpring** | NVK | ⬜ Level 4 |
| 1 | Shader compiler (SPIR-V → ISA) | **barraCuda** | NAK (Mesa) | ⬜ Level 2-3 |
| 1 | ISA instruction tables | **barraCuda** | envytools + NAK | 🔄 contrib/mesa-nak |
| 1 | f64 transcendental codegen | **barraCuda** | Original polyfills | ✅ compile_shader_f64 |
| 0 | Userspace DMA (vfio-pci) | **toadStool** | Linux vfio | 🔄 vfio.rs exists |
| 0 | Kernel module (thin) | **groundSpring** | nouveau | ⬜ Level 4 |

---

## Evolution Levels

### Level 1 — WGSL Polyfills + Safe Compilation (COMPLETE)

**Status**: ✅ Complete — zero unsafe, zero application C deps

**What**: Work around NAK/NVK limitations from WGSL without touching the
driver or compiler. All fixes live in barraCuda's shader compilation pipeline.

**Implemented**:
- `compile_shader_f64()`: auto-inject polyfills for exp, log, sin, cos, etc.
- `compile_shader_df64()`: DF64 (f32-pair) compilation path for consumer GPUs
- `Fp64Strategy`: auto-select Native/Hybrid/Concurrent based on hardware
- `has_spirv_passthrough()`: detect NVK, skip sovereign SPIR-V
- `yukawa_df64.wgsl`: hand-written DF64 force shader
- NVK workarounds: allocation limits, workgroup tuning, sin/cos Taylor

**Level 1 work**:
- [x] Wire DF64 Yukawa force into hotSpring MD pipeline — **DONE** (9/9 PASS, 293-326 steps/s)
- [x] Wire cell-list O(N) into hotSpring benchmark — **DONE** (CellListGpu, 3 cells/dim)
- [x] Wire Verlet neighbor list — **DONE** (368-992 steps/s, adaptive rebuild)
- [x] Measure gap vs Kokkos-CUDA — **DONE** (gap 3.7× at κ=3, down from 27×)
- [x] Eliminate all `unsafe` from barraCuda — **DONE** (7 blocks → 0)
- [x] Safe WGSL roundtrip (sovereign compiler on all backends) — **DONE**
- [x] Pipeline cache deferred until wgpu safe API — **DONE**
- [x] Capability-based discovery (zero hardcoded ports/primals) — **DONE**
- [ ] Validate DF64 on NVK for Yukawa OCP (sovereignty validation)

**Owner**: barraCuda (shaders), springs (validation)

**Achieved impact**: Closed 27× → 3.7× gap vs Kokkos-CUDA (93% of gap closed).
Verlet neighbor list is now at algorithmic parity with Kokkos/LAMMPS.
Remaining gap is dispatch overhead and GPU occupancy.

---

### Level 2 — coralReef: Sovereign GPU Compiler + Minimal Unsafe

**Status**: ✅ Complete (Phase 10 Iteration 18 — 1138 tests, 63% coverage, 9 unsafe blocks in driver only)

**What**: coralReef is a fully sovereign Rust GPU shader compiler evolved
from Mesa NAK roots. All stubs replaced with pure Rust. f64 transcendentals
implemented (NVIDIA: Newton-Raphson DFMA, AMD: native hardware). tarpc uses
bincode for high-performance binary IPC. Capability-based discovery.
`bytes::Bytes` zero-copy payloads. RAII `MappedRegion` for safe mmap.

**Completed**:
- [x] Sovereign compiler — zero C deps, zero FFI, zero `*-sys`
- [x] f64 transcendentals — sqrt, rcp, exp2, log2, sin, cos, exp, log, pow, tan
- [x] SM70–SM89 NVIDIA backend + SM20–SM50 legacy encoders tested
- [x] AMD RDNA2 backend — E2E verified on RX 6950 XT hardware
- [x] coralDriver — AMD amdgpu + NVIDIA nouveau via DRM ioctl (pure Rust)
- [x] coralGpu — unified compile + dispatch API
- [x] `#[deny(unsafe_code)]` on 6/8 crates; remaining 9 unsafe blocks in driver (RAII-wrapped)
- [x] tarpc + bincode binary IPC; JSON-RPC 2.0 primary
- [x] 1138 tests, 63% line coverage, 47 cross-spring WGSL shaders (36 compiling SM70)

**Architecture**:
```
barraCuda WGSL → naga → coralReef codegen IR → native GPU binary (SASS/GFX)
                                ↓
                        coralDriver (DRM ioctl) → GPU execution
```

**Owner**: coralReef (sovereign primal)

**Expected impact**: Eliminate polyfill overhead. Native f64 transcendentals
at hardware speed. Closes the remaining ~2-3× driver efficiency gap.

**Scaffolding advantage**: NAK is already Rust. We're not rewriting from C.
We're evolving an existing Rust codebase. AI-assisted development means
the ~35K LOC is tractable in weeks, not months.

---

### Level 3 — Standalone coralNak Crate (1-2 months)

**Status**: ⬜ Not started (depends on Level 2)

**What**: Extract NAK from Mesa's build system into a standalone Rust crate.
Make it a first-class barraCuda dependency. Enable WGSL → ISA direct path
(bypass SPIR-V entirely when targeting known hardware).

**Concrete tasks**:
- [ ] Decouple coralNak from Mesa C build (cmake → cargo)
- [ ] Define clean `pub fn compile(spirv: &[u32], target: GpuArch) -> Vec<u8>` API
- [ ] Add direct naga → coralNak path (skip SPIR-V serialization/deserialization)
- [ ] Implement WGSL → NIR → ISA fast path for known shader patterns
- [ ] Support multiple architectures: Volta (sm_70), Ampere (sm_86), Ada (sm_89)
- [ ] Add AMD RDNA support (scaffold from Mesa's ACO compiler, also partially Rust)
- [ ] Publish as `coral-nak` crate (MIT license, standalone)

**Architecture**:
```
barraCuda WGSL → naga → coralNak → NVIDIA ISA (sm_70/86/89)
                    ↘ → coralAco → AMD ISA (gfx10/11)  [future]
```

**Owner**: barraCuda (compiler crate), toadStool (architecture detection)

**Expected impact**: Full control of shader compilation. No Mesa dependency
for compute. ~50% compile-time reduction from SPIR-V elimination.
Multi-vendor ISA from one Rust toolchain.

---

### Level 4 — Sovereign Compute Runtime (3-6 months)

**Status**: ⬜ Not started (depends on Level 3)

**What**: Replace NVK/Vulkan with a minimal pure-Rust compute runtime.
Direct GPU memory management, command submission, and kernel dispatch
from Rust. No Vulkan, no C FFI, no Mesa.

**Concrete tasks**:
- [ ] **coralDriver**: Userspace GPU driver in Rust
  - Memory allocation (VRAM, system, mapped) via ioctl or vfio-pci
  - Command buffer construction (pushbuf for NVIDIA, PM4 for AMD)
  - Fence/semaphore synchronization
  - Multi-GPU dispatch
- [ ] **coralMem**: GPU memory management
  - Buffer create/map/unmap/copy
  - Staging buffer pool
  - Zero-copy where hardware supports it
- [ ] **coralQueue**: Command submission
  - Compute queue management
  - Async dispatch with Rust futures
  - Streaming (single-encoder) support
- [ ] **vfio backend**: Userspace DMA for full kernel bypass
  - toadStool's `vfio.rs` provides the foundation
  - IOMMU-based isolation
  - No kernel driver needed (compute-only, no display)
- [ ] **thin kmod backend**: Minimal kernel module for display-attached GPUs
  - Scaffold from nouveau's memory management
  - Pure Rust via `kernel` crate (Linux Rust-for-Linux)

**Architecture**:
```
barraCuda WGSL
  → naga/coralNak → ISA binary
    → coralDriver (Rust)
      → coralMem (buffer management)
      → coralQueue (command submission)
        → vfio-pci (userspace DMA) OR thin kmod
          → hardware
```

**Owner**: groundSpring (driver, memory, queue), toadStool (vfio, device
discovery), barraCuda (integration, shader → dispatch)

**Expected impact**: Complete sovereignty. Zero C dependencies in the
compute path. Direct hardware control from Rust. Potentially faster than
Vulkan for compute-only workloads (no validation layer overhead, no
Vulkan state machine). Works on hardware that proprietary vendors have
deprecated (Titan V, older Quadros).

---

## Cross-Primal Evolution Cycle

```
Springs (hotSpring, wetSpring, airSpring, neuralSpring)
  │ find gaps, validate physics, benchmark against Kokkos/LAMMPS
  │ contribute domain-specific shaders + NVK edge cases
  ▼
barraCuda
  │ builds precision strategy (Fp64Strategy, DF64, polyfills)
  │ evolves shader compilation (compile_shader_f64, coralNak)
  │ owns math dispatch + ISA codegen
  ▼
toadStool
  │ hardware discovery (GpuAdapterInfo, driver detection)
  │ device management (multi-GPU, NPU, vfio)
  │ runtime orchestration (compute substrate routing)
  ▼
groundSpring
  │ driver-level systems (memory, DMA, command submission)
  │ kernel interface (vfio-pci, thin kmod)
  │ hardware abstraction layer
  ▼
Springs ← absorb improved performance, validate again
```

Each primal ingests, catches up, develops, and hands back.
The springs co-evolve — hotSpring precision shaders benefit wetSpring
bio shaders, neuralSpring ML shaders inform all springs' NPU paths.

---

## Scaffolding Strategy

Every level scaffolds off known, working, open-source systems:

| Level | Scaffolds From | Language | License | LOC (est.) |
|:---:|---|---|---|---:|
| 1 | Our own WGSL | Rust/WGSL | AGPL-3.0 | ~5K |
| 2 | Mesa NAK | Rust | MIT | ~35K |
| 3 | Mesa NAK + ACO | Rust + some C | MIT | ~50K |
| 4 | NVK + nouveau | C + Rust | MIT/GPL | ~100K |

AI-assisted development at our evolution rate (~3 weeks for barraCuda
from zero to 15 DF64 ops + Fp64Strategy + 4 shaders + full test suite):

| Level | Estimated time | Risk |
|:---:|---|---|
| 1 | **days** (wire existing barraCuda DF64 + cell-list) | Low |
| 2 | **2-4 weeks** (fork NAK, fix f64 codegen, contribute upstream) | Low-Medium |
| 3 | **1-2 months** (extract NAK, standalone crate, multi-arch) | Medium |
| 4 | **3-6 months** (full runtime, memory, DMA, multi-vendor) | Medium-High |

The key insight: we are not writing from scratch. We are ingesting Rust
codebases (NAK is already Rust) and evolving them. This is fundamentally
faster than greenfield development. The AI-dev loop (springs find gaps →
primals fix → springs validate) accelerates each level.

---

## Hardware Evolution Context

NVIDIA has deprecated the Titan line. Consumer GPUs (RTX 40xx, 50xx) have
1/64 f64 rate — they're designed for gaming, not science. Proprietary
drivers will eventually stop supporting older hardware.

Our response: **make the software sovereign so hardware is interchangeable**.

| Hardware | Proprietary path | Sovereign path |
|---|---|---|
| Titan V (Volta, 1/2 f64) | nvidia.ko (for how long?) | coralDriver (forever) |
| RTX 3090 (Ampere, 1/64 f64) | nvidia.ko + CUDA | coralDriver + DF64 (f32 cores) |
| RTX 5090 (Blackwell, 1/64 f64) | nvidia.ko + CUDA | coralDriver + DF64 |
| AMD RDNA3 (1/16 f64) | amdgpu + ROCm | coralDriver + coralAco |
| Intel Arc (1/16 f64) | i915 + oneAPI | coralDriver + coralAnv |
| Future neuromorphic | vendor SDK | toadStool NpuDispatch |

DF64 (f32-pair precision) turns every consumer GPU into a scientific
compute device. The sovereign stack ensures these GPUs are usable
indefinitely, regardless of vendor support lifecycle.

---

## Validation Targets

Each level is validated against the same physics:

| Test | Python | barraCuda CPU | barraCuda GPU | Kokkos-CUDA |
|---|:---:|:---:|:---:|:---:|
| 9 PP Yukawa DSF cases | 33 steps/s | ~5,000 | 27 (L1 f64) | 730-3,700 |
| Energy conservation | 0.000% drift | 0.000% | 0.001% | TBD |
| Target (L1 DF64+cell) | — | — | ~1,400 | — |
| Target (L2 NAK fix) | — | — | ~2,500 | — |
| Target (L4 sovereign) | — | — | ~4,000+ | — |

The physics doesn't change. The math is validated at every level.
Only the infrastructure evolves.

---

## Naming Convention

All sovereign compute components use the **coral** prefix:

- **coralNak** — Sovereign shader compiler (scaffolds from Mesa NAK)
- **coralAco** — AMD shader compiler (scaffolds from Mesa ACO, future)
- **coralDriver** — Userspace GPU driver (scaffolds from NVK/nouveau)
- **coralMem** — GPU memory management
- **coralQueue** — Command submission and synchronization
- **coralGpu** — Unified Rust GPU abstraction (replaces wgpu for compute)

Coral: grows slowly, builds reefs, provides habitat for the entire ecosystem.
Sovereign, organic, accumulative.

---

---

## Related Documents

- `wateringHole/PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — cross-primal
  guidance for coralReef Layer 2-4 evolution (contracts, safe evolution paths)
- `barraCuda/PURE_RUST_EVOLUTION.md` — barraCuda layer status tracker
- `barraCuda/specs/REMAINING_WORK.md` — barraCuda remaining work items
- `barraCuda/WHATS_NEXT.md` — C dependency chain evolution map

---

*The shaders are the mathematics. The driver is plumbing.*
*We own the mathematics. Now we evolve the plumbing.*
