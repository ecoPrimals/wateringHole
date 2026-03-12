# Sovereign Compute Trio — Remaining Wiring Gaps & Ownership

**Date**: March 12, 2026
**From**: barraCuda (audit session — cross-stack gap analysis)
**To**: barraCuda, coralReef, toadStool (nvPmu, hw-learn)
**Type**: Cross-primal evolution plan — the final wiring
**Status**: Active — all components exist, need connection

---

## Executive Summary

The sovereign compute trio is **architecturally complete**. Every major
component — compiler, driver, hardware manager, learning system — exists
as working Rust code. The remaining work is **wiring**: connecting the
components so data flows end-to-end from shader source to GPU execution,
and from hardware observation to knowledge application.

No fundamental capability is missing. Six integration gaps remain.

```
                    THE SOVEREIGN COMPUTE TRIO

     barraCuda                coralReef               toadStool
  ┌──────────────┐      ┌───────────────┐      ┌──────────────────┐
  │ Math engine  │      │ Compiler +    │      │ Hardware mgmt    │
  │              │      │ Driver        │      │                  │
  │ WGSL shaders │─[1]─►│ WGSL→SASS/GFX │      │ nvPmu (sensors,  │
  │ DF64/FP64    │      │               │      │   BAR0, watchdog)│
  │ Precision    │      │ coral-driver  │─[4]─►│                  │
  │   routing    │◄─[2]─│ DRM dispatch  │      │ hw-learn (mmio,  │
  │              │      │               │◄─[3]─│   distiller,     │
  │ dispatch_    │      │ Sovereign GSP │      │   recipes)       │
  │   binary     │─[1]─►│ (knowledge,   │      │                  │
  │              │      │  applicator)  │      │ Firmware probe   │
  └──────────────┘      └───────────────┘      └──────────────────┘
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               ▼
                          GPU Hardware
                    (Volta, Ampere, RDNA2, ...)
```

---

## What's DONE

### barraCuda (math engine)
- [x] WGSL shader library: 15+ DF64 ops, Yukawa, Bessel, spectral
- [x] Precision routing: `Fp64Strategy`, `GpuDriverProfile`, workarounds
- [x] DF64 SPIR-V poisoning workaround (transcendental stripping)
- [x] `GpuBackend` trait with `dispatch_compute` and `dispatch_binary`
- [x] `CoralReefDevice` backend (sovereign dispatch via `coral-gpu`)
- [x] `WgpuDevice` backend (Vulkan fallback, all platforms)
- [x] Zero `unsafe`, zero `todo!()`, zero `FIXME`
- [x] `VoltaNoPmuFirmware` workaround + `needs_software_pmu()` detection

### coralReef (compiler + driver)
- [x] WGSL/SPIR-V/GLSL → native SASS (SM20–SM89) and GFX (RDNA2)
- [x] f64 transcendentals (Newton-Raphson DFMA for NVIDIA, native for AMD)
- [x] `coral-driver`: AMD amdgpu full pipeline (GEM→PM4→submit→fence→readback)
- [x] `coral-driver`: NVIDIA nouveau full pipeline (GEM→VM_BIND→QMD→pushbuf→exec)
- [x] `coral-gpu`: unified compile + dispatch API (`GpuContext`)
- [x] Sovereign GSP: firmware parser (22 chips, legacy + NET_img)
- [x] Sovereign GSP: cross-architecture knowledge base (address spaces, transfer maps)
- [x] Sovereign GSP: dispatch optimizer (workgroup hints, FP64 detection)
- [x] Sovereign GSP: BAR0 applicator (pre-init writes, dry-run, verify)
- [x] 1401+ tests, `#[deny(unsafe_code)]` on 6/8 crates

### toadStool / nvPmu / hw-learn (hardware management)
- [x] PCI GPU discovery (NVIDIA via sysfs)
- [x] Sensor monitoring: hwmon (nouveau/amdgpu) + nvidia-smi (proprietary)
- [x] BAR0 MMIO: mmap, read_u32, write_u32, bounds checks, RAII unmap
- [x] Init recipe applicator: BAR0 writes with delays and verification
- [x] Thermal watchdog: background polling, emergency power cap
- [x] Firmware probe: PMU/GSP/ACR/GR/SEC2 presence, `compute_viable()`
- [x] mmiotrace parser: baseline/compute diff
- [x] Recipe distiller: register classification (GV100), JSON recipes
- [x] Recipe store: `$XDG_DATA_HOME/hw-learn/recipes/`, save/load/list
- [x] Capture script: root mmiotrace + ioctl trace for proprietary driver

---

## The Six Remaining Gaps

### Gap 1: `dispatch_binary` not wired

**Owner**: barraCuda (implementation) + coralReef (API surface)

**What**: `CoralReefDevice` has the `dispatch_binary` trait method but uses
the default stub that returns an error. coralReef compiles WGSL to native
SASS/GFX binaries. `spawn_coral_compile` caches them. But nothing calls
`dispatch_binary` to use the cached result.

**Impact**: Highest. Without this, every dispatch recompiles at runtime.
The sovereign compiler's output is produced then discarded.

**Work**:

| Task | Owner | Depends On |
|------|-------|------------|
| Implement `dispatch_binary` on `CoralReefDevice` | **barraCuda** | coral-gpu dispatch API |
| Call `coral_gpu::GpuContext::dispatch()` with pre-compiled `CompiledKernel` | **barraCuda** | — |
| Wire `spawn_coral_compile` cache → `dispatch_binary` path | **barraCuda** | — |
| Ensure `CompiledKernel` metadata (workgroup size, bindings) passes through | **coralReef** (coral-gpu) | — |
| Add `dispatch_binary` to `BatchedComputeDispatch` path | **barraCuda** | dispatch_binary impl |

**Acceptance**: `cargo test` demonstrates WGSL → compile once → dispatch N
times without recompilation. Benchmark shows compile-time amortized to zero.

---

### Gap 2: NVIDIA proprietary driver path (nvidia-drm / UVM)

**Owner**: coralReef (coral-driver)

**What**: RM client and channel setup are done. Five stubs remain:
`UVM_MAP_EXTERNAL_ALLOCATION`, CPU mmap for RM memory, readback, GPFIFO
submission, and completion sync.

**Impact**: High. Can't run sovereign compute on the RTX 3090 via the
proprietary driver. Must use wgpu or nouveau.

**Work**:

| Task | Owner | Depends On |
|------|-------|------------|
| Wire `UVM_MAP_EXTERNAL_ALLOCATION` for GPU VA mapping | **coralReef** | RM alloc (done) |
| Implement mmap on `/dev/nvidia0` for RM system memory | **coralReef** | — |
| Implement readback (mmap read from mapped region) | **coralReef** | mmap impl |
| Implement GPFIFO push (upload QMD + push buffer, write to GPFIFO doorbell) | **coralReef** | VA mapping |
| Implement semaphore/fence polling for completion | **coralReef** | GPFIFO impl |

**Acceptance**: E2E test: allocate buffer → upload data → compile shader →
dispatch via GPFIFO → readback result → verify on RTX 3090 proprietary.

---

### Gap 3: FECS channel submission for Volta init

**Owner**: coralReef (coral-driver GSP + nv module)

> **UPDATE (March 12 — hotSpring hardware validation)**: Channel allocation
> is now PROVEN WORKING on Titan V (GV100) via the standard nouveau DRM path
> (`eb4b4eb`). The channel alloc failure was not a PMU firmware issue — it was
> an ioctl number off-by-two in coral-driver. With `CHANNEL_ALLOC = 0x42`
> (was incorrectly 0x40), all 5 channel allocation variants succeed on both
> Titan V and RTX 3090. This means FECS method submission via compute channel
> is now UNBLOCKED — the channel exists, the pushbuf infrastructure works.

**What**: Sovereign GSP parses GV100's 958 bundle + 1,537 method init
entries and splits them into BAR0 pre-init (2 writes) and FECS method data.
The BAR0 applicator works. But the FECS method data must be submitted
through a falcon channel, not written directly to BAR0.

GV100's `sw_bundle_init.bin` uses **FECS method offsets** (0x000xxxxx),
not BAR0 register addresses. The data must be pushed through a compute
channel as FECS methods after the pre-init enables the engine.

**Impact**: High for Titan V. This is the final step to bring up Volta
compute from scratch without any proprietary firmware.

**Work**:

| Task | Owner | Depends On | Status |
|------|-------|------------|--------|
| Build FECS method push path in `coral-driver::nv` | **coralReef** | nouveau channel | **Unblocked** (`eb4b4eb`) |
| After BAR0 pre-init (PMC + FIFO enable), create nouveau channel | **coralReef** | BAR0 applicator (done) | **Unblocked** — channel alloc now works |
| Push bundle_init entries as FECS methods via channel | **coralReef** | FECS path | Pending |
| Push method_init entries via channel | **coralReef** | FECS path | Pending |
| Verify GR engine state after init sequence | **coralReef** | — | Pending |
| Test on Titan V hardware (requires device swap) | **coralReef** | All above | **Available** — Titan V in UVM |

**Acceptance**: nouveau channel creation succeeds on GV100 after sovereign
pre-init. GR engine responds to compute dispatch. No PMU firmware required.

> **Note**: Channel creation already succeeds on GV100 via the standard nouveau
> DRM path (without sovereign pre-init). The DRM fix means this gap is about
> FECS method formatting and pushbuf construction, not about channel availability.

---

### Gap 4: `RegisterAccess` trait bridge

**Owner**: toadStool (nvPmu) + coralReef (GSP applicator)

**What**: Three separate `RegisterAccess` interfaces exist that do the
same thing:

| Interface | Offset type | Crate |
|-----------|-------------|-------|
| `hw_learn::applicator::RegisterAccess` | `u64` | hw-learn |
| `coral_driver::gsp::applicator::RegisterAccess` | `u32` | coral-driver |
| `nvpmu::bar0::Bar0Access` (concrete impl) | `u64` | nvpmu |

`Bar0Access` now implements `hw_learn::applicator::RegisterAccess` (S147).
nvPmu still duplicates hw-learn's applicator logic in `init.rs` — needs
dedup. coralReef's GSP applicator needs a thin adapter to use hw-learn's trait.

**Impact**: Medium. Prevents the sovereign GSP from applying init sequences
to real hardware via nvPmu.

**Work**:

| Task | Owner | Depends On |
|------|-------|------------|
| Add `hw-learn` as optional dependency in nvPmu | **toadStool** | — | **DONE** (S147) |
| Implement `hw_learn::applicator::RegisterAccess` for `Bar0Access` | **toadStool** | — | **DONE** (S147) |
| Add thin adapter in coral-driver GSP to accept `hw_learn::RegisterAccess` | **coralReef** | — | Pending |
| Remove duplicated `apply_recipe` from `nvpmu::init` (use hw-learn's) | **toadStool** | RegisterAccess impl | Pending |
| Wire `nvpmu-apply` to use `apply_recipe_safe` (thermal checks) | **toadStool** | — | Pending |

**Acceptance**: `coralReef GSP → hw-learn recipe → nvPmu BAR0 → hardware`
flows without manual format conversion.

---

### Gap 5: Multi-architecture register classifier

**Owner**: toadStool (hw-learn) + coralReef (GSP knowledge)

**What**: `hw_learn::distiller::classify_register` only knows GV100's
MMIO register ranges. Can't distill recipes from RTX 3090 (GA102) or
Turing (TU102) mmiotrace captures. coralReef's GSP knowledge base has
the firmware data but no register classification for post-Volta.

**Impact**: Medium. Limits the learning loop to Volta. Can't learn from
the RTX 3090 (our primary modern hardware) to improve older card init.

**Work**:

| Task | Owner | Depends On |
|------|-------|------------|
| Add GA102 (Ampere) register ranges to hw-learn distiller | **toadStool** | envytools / firmware analysis |
| Add TU102 (Turing) register ranges | **toadStool** | envytools / firmware analysis |
| Add address space translation (method offset ↔ BAR0) to GSP knowledge | **coralReef** | NET_img parser (done) |
| Cross-reference hw-learn register classes with GSP firmware register sets | **coralReef** + **toadStool** | Both classifiers |
| Capture mmiotrace on RTX 3090 and distill recipe | **toadStool** | GA102 classifier |

**Acceptance**: `hw-learn-distill` produces valid recipes from GA102 and
TU102 mmiotrace captures. Recipes pass dry-run validation.

---

### Gap 6: Unified PCI discovery (multi-vendor)

**Owner**: toadStool (nvPmu)

**What**: `nvpmu::pci` only scans for NVIDIA (vendor `0x10de`). AMD GPUs
(`0x1002`) and Intel GPUs (`0x8086`) are discovered through separate hwmon
scanning in the monitor binary, not through PCI enumeration.

**Impact**: Low. Quality-of-life for multi-vendor systems. The sovereign
GSP knowledge base already understands AMD firmware structure; PCI discovery
would complete the hardware-side integration.

**Work**:

| Task | Owner | Depends On |
|------|-------|------------|
| Generalize `nvpmu::pci` to accept vendor IDs as parameter | **toadStool** | — |
| Add AMD vendor `0x1002` and PCI class for display controllers | **toadStool** | — |
| Add Intel vendor `0x8086` | **toadStool** | — |
| Rename crate consideration: `nvpmu` → `gpupmu` or keep NVIDIA-focused | **toadStool** | — |
| Wire unified PCI scan into `nvpmu-monitor` to replace ad-hoc hwmon scan | **toadStool** | — |

**Acceptance**: `nvpmu-monitor` discovers all GPUs (NVIDIA, AMD, Intel)
through unified PCI enumeration on a multi-vendor system.

---

## The Learning Loop — What's Wired, What's Not

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    THE LEARNING LOOP                         │
  │                                                             │
  │   OBSERVE ──────► DISTILL ──────► TRANSFER ──────► APPLY   │
  │   [DONE]          [PARTIAL]       [DONE]           [PARTIAL]│
  │                                                             │
  │   mmiotrace       register        cross-arch       BAR0     │
  │   firmware        classifier      mapper           pre-init │
  │   parser          (GV100 only)    teacher          FECS     │
  │                                   selection        channel  │
  │                                                    [MISSING]│
  └─────────────────────────────────────────────────────────────┘
```

### Observe (DONE)
- **22 NVIDIA chips parsed** from `/lib/firmware/nvidia/`: GV100, TU102-TU117,
  GA102-GA107, GM200-GM20b, GP100-GP10b
- **Dual format support**: Legacy `sw_bundle_init.bin` (Maxwell→Turing) and
  `NET_img.bin` container (Ampere+)
- **Address space detection**: Method offsets (0x000xxxxx) vs BAR0 MMIO (0x004xxxxx)
- **mmiotrace capture script** ready for proprietary driver observation
- **Sensor reading**: hwmon (nouveau/amdgpu), nvidia-smi (proprietary)

### Distill (PARTIAL — Gap 5)
- **GV100 register classification**: Engine, Clock, Power, Thermal, Memory, Channel
- **Recipe format**: JSON with chip, steps (offset/value/width/class/delay), verify_reads
- **Missing**: GA102/TU102 register ranges, method↔BAR0 address translation

### Transfer (DONE)
- **Cross-architecture register mapper**: Overlap comparison between any two chips
- **Best teacher selection**: gp10b → GV100 at 98.2% register coverage
- **Generational evolution**: Maxwell→Pascal→Volta→Turing→Ampere tracked
- **Dispatch optimizer**: Per-chip hints (workgroup size, FP64, sovereign needs)

### Apply (PARTIAL — Gaps 3 + 4)
- **BAR0 pre-init**: 2 writes (PMC_ENABLE, FIFO_ENABLE), dry-run, verify
- **Recipe applicator**: hw-learn `apply_via` + nvPmu `apply_recipe`
- **Thermal watchdog**: Emergency power cap during init
- **Missing**: FECS channel submission (Gap 3), RegisterAccess bridge (Gap 4)

---

## Ownership Matrix

| Component | Primary Owner | Contributes To | Dependencies |
|-----------|---------------|----------------|--------------|
| WGSL shaders, DF64 math | **barraCuda** | coralReef (test input) | — |
| Precision routing | **barraCuda** | — | coralReef (profile data) |
| `dispatch_binary` impl | **barraCuda** | — | coralReef (coral-gpu API) |
| `CoralReefDevice` backend | **barraCuda** | — | coralReef (coral-gpu) |
| WGSL→SASS/GFX compiler | **coralReef** | barraCuda (binaries) | naga |
| `coral-driver` AMD | **coralReef** | barraCuda (dispatch) | — |
| `coral-driver` nouveau | **coralReef** | barraCuda (dispatch) | — |
| `coral-driver` nvidia-drm/UVM | **coralReef** | barraCuda (dispatch) | — |
| Sovereign GSP knowledge | **coralReef** | toadStool (recipes) | toadStool (firmware) |
| Sovereign GSP applicator | **coralReef** | toadStool (BAR0 bridge) | toadStool (BAR0) |
| FECS channel submission | **coralReef** | — | nouveau channel (done) |
| nvPmu sensors + BAR0 | **toadStool** | coralReef (thermal safety) | — |
| nvPmu thermal watchdog | **toadStool** | coralReef (init safety) | — |
| hw-learn observer | **toadStool** | coralReef (GSP data) | — |
| hw-learn distiller | **toadStool** | coralReef (recipes) | — |
| hw-learn applicator | **toadStool** | coralReef (bridge) | nvPmu (BAR0) |
| PCI discovery | **toadStool** | all | — |
| Firmware probe | **toadStool** | coralReef (GSP) | — |

---

## Priority Execution Order

```
Phase 1 — WIRING (immediate, unblocks sovereign dispatch)
  [Gap 1] dispatch_binary        ← barraCuda
  [Gap 4] RegisterAccess bridge  ← toadStool

Phase 2 — HARDWARE (unblocks Volta + proprietary NVIDIA)
  [Gap 3] FECS channel submit    ← coralReef
  [Gap 2] UVM dispatch path      ← coralReef

Phase 3 — LEARNING (completes the learning loop)
  [Gap 5] Multi-arch classifier  ← toadStool + coralReef
  [Gap 6] Unified PCI discovery  ← toadStool
```

Phase 1 can be done **in parallel** by barraCuda and toadStool.
Phase 2 is coralReef-internal.
Phase 3 can start as soon as Phase 1 is done.

---

## What "Done" Looks Like

When all six gaps are closed:

1. `barraCuda WGSL shader` → coralReef compiles to SASS → `dispatch_binary`
   sends cached native binary → coral-driver submits to GPU → result returns.
   **No wgpu. No Vulkan. No naga at dispatch time. Pure Rust.**

2. Titan V boots from cold via sovereign GSP: nvPmu writes BAR0 pre-init →
   coralReef submits FECS bundle/method init → nouveau creates compute channel →
   barraCuda dispatches DF64 Yukawa kernel → FP64 at full rate. **No proprietary
   firmware. No NVIDIA driver.**

3. RTX 3090 mmiotrace → hw-learn distills GA102 recipe → coralReef GSP
   knowledge base learns Ampere init patterns → knowledge transfers to Volta
   (98% register overlap within same address space) → recipe applied to
   Titan V. **Modern cards teach old cards.**

4. Any future GPU: plug it in → hw-learn observes firmware → distiller
   classifies registers → knowledge base absorbs → older cards benefit.
   **The system gets smarter with every new card.**

---

## Validation Targets

Each gap's closure is validated by the same physics:

| Validation | Gap Required |
|------------|-------------|
| hotSpring 9-case Yukawa via sovereign dispatch | Gap 1 |
| DF64 transcendentals via sovereign (not stripped) | Gap 1 |
| Titan V compute from cold boot | Gaps 3 + 4 |
| RTX 3090 sovereign dispatch via nvidia-drm | Gap 2 |
| Cross-gen recipe transfer (GA102 → GV100) | Gap 5 |
| Multi-vendor sensor dashboard | Gap 6 |

---

## Key Numbers from This Session

| Metric | Value |
|--------|-------|
| NVIDIA chips with parsed firmware | 22 |
| GV100 unique registers | 893 |
| GA102 unique registers (NET_img) | 923 |
| GV100→gp10b register coverage | 98.2% |
| GV100→TU102 register coverage | 85.4% |
| GV100→GA102 direct overlap | 0% (different address spaces) |
| BAR0 pre-init writes for Volta | 2 (PMC_ENABLE + FIFO_ENABLE) |
| FECS bundle entries for GV100 | 958 |
| FECS method entries for GV100 | 1,537 |
| coral-driver tests passing | 151 |
| Total unsafe blocks in sovereign stack | 9 (all in coral-driver RAII) |

## hotSpring Hardware Validation Update (March 12)

| Metric | Value |
|--------|-------|
| DRM bugs found and fixed | 3 (ioctl off-by-two, VA collision, gem_info) |
| Channel alloc variants passing (per GPU) | 5/5 |
| GPUs with working sovereign DRM pipeline | 2 (Titan V GV100 + RTX 3090 GA102) |
| Nouveau hardware tests passing | 9/11 |
| Remaining failures | 2 (QMD compute execution — dispatch completes, output needs tuning) |
| coralReef commit | `eb4b4eb` |
| Kernel tested | 6.17.9-76061709-generic |
| Mesa version | 25.1.5 |

### Impact on Gap Status

| Gap | Before | After Breakthrough |
|-----|--------|--------------------|
| Gap 1 (dispatch_binary) | Blocked by no working dispatch | **Unblocked** — DRM pipeline proven |
| Gap 2 (UVM path) | RM infrastructure done, stubs remain | Unchanged (separate path) |
| Gap 3 (FECS channel) | Believed blocked by PMU firmware | **Unblocked** — channel alloc works on GV100 |
| Gap 4 (RegisterAccess) | Unchanged | Unchanged |
| Gap 5 (Multi-arch classifier) | Unchanged | Unchanged |
| Gap 6 (Unified PCI) | Unchanged | Unchanged |

### Deprecation Path Opened

With sovereign DRM dispatch proven on hardware:

| External Dependency | Status | Replacement |
|---|---|---|
| naga (WGSL → SPIR-V) | **Deprecatable** | coralReef compiler (WGSL → SASS) |
| NVK/NAK (Mesa Vulkan) | **Deprecatable** | coralReef DRM dispatch |
| wgpu (Vulkan abstraction) | **Deprecatable** | coralReef `ComputeDevice` trait |
| nouveau (kernel module) | Still needed | DRM ioctls route through nouveau |

The DF64 SPIR-V poisoning, NAK compiler crashes, and ReduceScalarPipeline
regression all become irrelevant once sovereign dispatch is compute-complete —
those are naga/NVK bugs that don't exist in the sovereign SASS path.

---

*The components exist. The knowledge is gathered. The DRM pipeline is proven.*
*Wire them together and the stack is sovereign.*
