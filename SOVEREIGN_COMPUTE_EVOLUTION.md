# Sovereign Compute Evolution — Pure Rust GPU Stack

**Date**: March 12, 2026 (updated — security posture, VFIO→Kokkos parity, CERN-grade goal)
**From**: hotSpring v0.6.31 (sovereign BAR0 path implemented in coralReef)
**To**: All primals — toadStool, barraCuda, coralReef, springs
**Type**: Long-term architecture evolution plan
**Goal**: Replace every non-Rust dependency in the GPU compute path with
sovereign Rust implementations, scaffolded off existing open-source systems.
The endgame is **dual-use hardware** — the same machine runs gaming and science.
The validation goal is **CERN-grade reproducible physics at home, scalable to CERN**.

> **March 12 update (security + Kokkos strategy)**: GPU security posture
> defined — software enclave via BearDog (encryption) + toadStool (VFIO
> exclusivity) + Rust (memory safety). No MIG needed for trusted workloads.
> VFIO dispatch path projects **~4,000 steps/s** Yukawa (vs Kokkos 2,630) via
> DF64 9.9× gain + direct GPFIFO. Precision mix advantage is unique to
> ecoPrimals — Kokkos can't do it. toadStool tree model enables cross-GPU
> learning and software-defined GPU partitioning on any PCIe GPU.
> See `handoffs/GPU_SECURITY_POSTURE_VFIO_KOKKOS_STRATEGY_HANDOFF_MAR12_2026.md`.
> hotSpring extended goal: `SOVEREIGN_VALIDATION_GOAL.md` — CERN-grade
> reproducible physics from `cargo build`, scalable from 1 GPU to 1000.

> **March 12 update (hotSpring)**: Three critical DRM bugs fixed in
> coral-driver (`eb4b4eb`). The sovereign nouveau dispatch pipeline
> (VM_INIT → CHANNEL_ALLOC → VM_BIND → GEM → upload → readback) is now
> **fully operational on both Titan V (GV100) and RTX 3090 (GA102)**.
> Channel allocation was blocked by an ioctl number off-by-two since
> coralReef's inception. 9/11 hardware tests pass. Remaining: QMD compute
> execution tuning (dispatch runs without error, kernel output needs
> field alignment). This opens the deprecation path for naga/NVK/wgpu.
>
> See `handoffs/CORALREEF_SOVEREIGN_DRM_BREAKTHROUGH_HANDOFF_MAR09_2026.md`
>
> **March 12 update (barraCuda)**: All components exist. Six wiring gaps remain.
> See `handoffs/SOVEREIGN_COMPUTE_TRIO_WIRING_GAPS_HANDOFF_MAR12_2026.md`
> for the detailed gap analysis, ownership matrix, and execution plan.
>
> **March 12 update (gap closure)**: Gap 1 (dispatch_binary) **CLOSED** by
> barraCuda `82ff983` — CoralReefDevice now wires coral cache → dispatch.
> Gap 4 (RegisterAccess bridge) **CLOSED** by toadStool S147 — nvPmu
> Bar0Access bridged to hw-learn. Gap 2 (GPFIFO) partially closed by
> coralReef Iter 37 — USERD doorbell + completion polling implemented.
> Gap 3 (FECS) remains unblocked. hotSpring v0.6.31 absorbs all three
> primals and wires `sovereign_resolves_poisoning()` into MD precision
> routing — DF64 transcendentals now available through sovereign bypass.
>
> **March 12 update (dispatch investigation)**: hotSpring deep-debugged
> the dispatch pipeline on both Titan V and RTX 3090. Found and fixed
> **four critical bugs** in coralReef:
> 1. QMD field offsets entirely wrong (bit vs word misread of NVIDIA headers)
> 2. CBUF descriptor indirection missing (shader expects descriptor, got raw VA)
> 3. QMD version wrong for Volta (v2.1→v2.2) and missing v3.0 selection
> 4. No sync on new UAPI path (added DRM syncobj create/signal/wait)
>
> **Remaining blocker**: `CTXNOTVALID` from PBDMA — the GR engine context
> is never initialized. `sw_ctx.bin` content is parsed but discarded;
> FECS method init sequence is built but never submitted. coralReef has
> the pieces (`gsp/gr_init.rs`, `gsp/applicator.rs`) but needs integration
> into the dispatch path. See `handoffs/HOTSPRING_CORALREEF_DISPATCH_INVESTIGATION_HANDOFF_MAR12_2026.md`.
>
> **March 12 update (FECS integration wired)**: hotSpring wired the missing
> FECS GR context init integration into `NvDevice`:
> - `try_gr_context_init()` added to `NvDevice` — maps SM → chip, parses
>   firmware blobs, extracts method_init entries, builds push buffer, submits
>   before first dispatch
> - Called from `open_from_drm()` after channel creation
> - `NvUvmComputeDevice` re-exported for `coral-gpu` consumption
> - coralReef Iter 38-39 absorbed: firmware parser stores `sw_ctx.bin`,
>   `PushBuf::gr_context_init()` implemented, UVM CBUF aligned
> - barraCuda pin updated: `82ff983` → `7c1fd03a` (deep debt sprints, +340 tests)
> - toadStool S148-S149 reviewed: SecretString, credential chain, shader handler
>
> **Gap status**: 1 CLOSED, 2 partially closed, 3 WIRED but CTXNOTVALID persists,
> 4 CLOSED, 5 needs knowledge→init path, 6 needs error recovery.
>
> **March 12 update (CTXNOTVALID root cause)**: Hardware testing reveals
> CTXNOTVALID on **both** GPUs — RTX 3090 (Ampere/GSP) AND Titan V (Volta).
> This proves the issue is NOT missing FECS firmware but a **channel setup
> gap in nouveau on kernel 6.17**: `CHANNEL_ALLOC` creates a channel but
> doesn't bind the compute engine (PGRAPH) context.
>
> Key findings from firmware analysis:
> - `sw_method_init.bin` entries are ALL BAR0 register addresses (0x00400000+)
> - Zero entries are valid push buffer methods (max addr for 13-bit encoding: 0x7FFC)
> - These need BAR0 MMIO access (toadStool nvPmu) or kernel-level init
> - NVK (Mesa Vulkan) likely handles this via a separate PGRAPH init path
>
> **March 12 update (sovereign BAR0 GR init implemented)**:
> hotSpring implemented the **sovereign BAR0 dispatch path** in coralReef:
>
> **New code added:**
> - `nv/bar0.rs`: Pure Rust BAR0 MMIO via sysfs `resource0` mmap, implements
>   `RegisterAccess` trait with volatile read/write. Resolves PCI BAR from
>   DRM render node path. 16 MiB mapping per GPU.
> - `gsp/applicator.rs`: **Address-aware split** — entries with offsets > 0x7FFC
>   now correctly route to BAR0 instead of FECS channel. Push buffer method
>   headers use 13-bit encoding (max 0x7FFC); anything above is a register.
> - `nv/mod.rs`: `try_bar0_gr_init()` runs BEFORE channel creation (Phase 0),
>   writing PGRAPH registers via BAR0 MMIO. `try_fecs_channel_init()` (Phase 3)
>   handles remaining low-address FECS methods after channel creation.
>
> **Firmware analysis (address-aware split results):**
> | GPU | BAR0 writes | FECS entries | Total |
> |-----|------------|-------------|-------|
> | RTX 3090 (GA102) | 2972 | 0 | 2972 |
> | Titan V (GV100) | 1570 | 927 | 2497 |
>
> GA102: ALL init is BAR0 register writes — zero push buffer methods.
> GV100: hybrid — 1570 BAR0 register writes + 927 valid FECS channel methods.
>
> **Validation needed**: Run with `sudo` for BAR0 sysfs access:
> ```
> sudo chmod 666 /sys/class/drm/renderD*/device/resource0
> cargo test --test hw_nv_nouveau --features nouveau -- --ignored --nocapture nouveau_sovereign_bar0_diagnostic
> cargo test --test hw_nv_nouveau --features nouveau -- --ignored --nocapture nouveau_dispatch_diagnostic
> ```
>
> **Three dispatch paths now available:**
> 1. **Sovereign BAR0 + nouveau** (Path A): BAR0 GR init → channel → dispatch. Needs root.
> 2. **UVM** (Path B): Full proprietary driver bypass. Needs nvidia module.
> 3. **Nouveau only** (fallback): Depends on kernel GR init. Current default.
>
> The previous list of fixes remains valid for context, but Path A (BAR0) is
> now the primary sovereign approach — no kernel patch needed.

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

**Status**: ✅ Complete (Phase 10 Iteration 43 — 1693+47 tests, 64% coverage, VFIO PFIFO channel + V2 MMU, WGSL+SPIR-V+GLSL frontends)

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
- [x] 1693+47 tests, 64% line coverage, 93 cross-spring WGSL shaders (84 compiling SM70), GLSL 450 + SPIR-V roundtrip (10/10)
- [x] Multi-GPU sovereignty (Iter 24), math debt elimination (Iter 25), sovereign pipeline unblock (Iter 26), deep debt evolution (Iter 27)
- [x] **Sovereign GSP Phase 2** (March 12): firmware parser (22 chips, legacy + NET_img.bin),
  cross-architecture knowledge base (address space awareness, register transfer maps),
  dispatch optimizer (workgroup sizing, FP64 hints), BAR0 applicator (pre-init + verify)
- [ ] **Remaining**: `dispatch_binary` wiring, FECS channel submission, UVM dispatch path

**Architecture**:
```
barraCuda WGSL/GLSL → naga → coralReef codegen IR → native GPU binary (SASS/GFX)
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

**Status**: 🔄 Partially achieved — coralReef already compiles standalone; `coral-gpu` provides clean API

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

**Status**: 🔄 Core implemented — **nouveau DRM pipeline PROVEN on hardware** (Titan V + RTX 3090, `eb4b4eb`); AMD amdgpu pipeline operational; UVM path stubbed; GSP learning system operational

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

## Dual-Use Architecture: Gaming + Science

The endgame isn't "choose between gaming and science." A single machine
should do both — nvidia proprietary for Steam when you're gaming, VFIO
sovereign compute when you're not.

```
                       DUAL-USE GPU

     ┌─────────────────────────────────────────┐
     │               HARDWARE                   │
     │         GPU (e.g. RTX 3090)              │
     └─────────────┬───────────────────────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
    ┌──────────┐      ┌──────────┐
    │  GAMING  │      │ SCIENCE  │
    │   MODE   │      │   MODE   │
    └────┬─────┘      └────┬─────┘
         │                 │
    nvidia driver     vfio-pci
    (proprietary)     (generic)
         │                 │
    Steam/Proton     ecoPrimals
    Vulkan, DLSS     sovereign
    ray tracing      BAR0 + DMA
```

**Multi-GPU split**: One GPU stays on nvidia for display + gaming, another
on VFIO for science. The natural state for research machines with two GPUs.

**Single-GPU dynamic switch**: toadStool manages the transition —
stop display server, unbind nvidia, bind VFIO, run science, reverse when done.
toadStool already has the VFIO backend (Akida NPU) and device management
infrastructure to own this.

**Phase plan**:
1. Validate sovereign BAR0 + nouveau (code done, needs root test)
2. Validate UVM path (RTX 3090 with nvidia driver)
3. Build VFIO GPU backend in coralReef (extend toadStool's Akida VFIO pattern)
4. Build `ecoprimals-mode` CLI in toadStool for gaming ↔ science switching
5. Dynamic GPU arbitration — toadStool detects idle GPU, claims for science

See `handoffs/SOVEREIGN_COMPUTE_BAR0_BREAKTHROUGH_DUAL_USE_HANDOFF_MAR12_2026.md`
for implementation details, scripts, and per-gap ownership.

---

## March 13 Update — CUDA-as-Oracle Evolutionary Debugging

> **Breakthrough insight**: After extensive VFIO PFIFO debugging (PDE/PTE
> encoding, GPFIFO format, PMC enable, PBDMA discovery, memory ordering),
> the `FenceTimeout` persists. The remaining gap is post-FLR initialization
> steps that open source docs don't cover.
>
> **Strategy**: Bind the Titan V TEMPORARILY to the nvidia driver (same
> driver already loaded for the 3090), read BAR0 registers to see a
> healthy Volta PFIFO state, compare register-by-register against our
> VFIO init, identify every delta, and fix. Then rebind to vfio-pci.
>
> **Key finding**: The 3090 (Ampere) cannot serve as reference — it uses
> GSP firmware for all PFIFO management (registers read as `0xbadf1100`
> sentinel). We need a Volta reference — i.e., the Titan V itself under
> nvidia. Same silicon, same architecture, different driver.
>
> **Evolutionary insight**: This approach was NOT possible as a one-shot.
> We needed Phase 1 (open source vocabulary), Phase 2 (Rust reimplementation
> as fitness test), before Phase 3 (CUDA as calibration oracle) becomes
> meaningful. Without independent understanding, BAR0 register dumps are
> meaningless hex. With it, every value tells a story.
>
> **Dual-use evolution**: The nvidia ↔ vfio-pci rebind naturally becomes
> the toadStool `gpu mode` switcher — gaming (nvidia) vs science (vfio)
> on the same chip, managed by toadStool's process tree.
>
> See `handoffs/HOTSPRING_CUDA_ORACLE_EVOLUTIONARY_DEBUGGING_HANDOFF_MAR13_2026.md`

---

## Related Documents

- `wateringHole/PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — cross-primal
  guidance for coralReef Layer 2-4 evolution (contracts, safe evolution paths)
- `wateringHole/handoffs/SOVEREIGN_COMPUTE_TRIO_WIRING_GAPS_HANDOFF_MAR12_2026.md` —
  detailed gap analysis with ownership, priority, and acceptance criteria
- `wateringHole/handoffs/SOVEREIGN_COMPUTE_BAR0_BREAKTHROUGH_DUAL_USE_HANDOFF_MAR12_2026.md` —
  BAR0 breakthrough details, dual-use architecture, VFIO roadmap, sudo solutions
- `wateringHole/handoffs/GPU_SECURITY_POSTURE_VFIO_KOKKOS_STRATEGY_HANDOFF_MAR12_2026.md` —
  GPU security posture (software enclave), VFIO performance, Kokkos parity strategy
- `wateringHole/handoffs/HOTSPRING_CUDA_ORACLE_EVOLUTIONARY_DEBUGGING_HANDOFF_MAR13_2026.md` —
  CUDA-as-oracle strategy, BAR0 reference capture plan, evolutionary debugging insight
- `hotSpring/SOVEREIGN_VALIDATION_GOAL.md` — CERN-grade reproducible physics goal,
  scaling from home to CERN, the extended validation ladder
- `barraCuda/PURE_RUST_EVOLUTION.md` — barraCuda layer status tracker
- `barraCuda/specs/REMAINING_WORK.md` — barraCuda remaining work items
- `barraCuda/WHATS_NEXT.md` — C dependency chain evolution map

---

*The shaders are the mathematics. The driver is plumbing.*
*We own the mathematics. Now we evolve the plumbing.*
*The hardware is yours — for gaming, for science, for both.*
