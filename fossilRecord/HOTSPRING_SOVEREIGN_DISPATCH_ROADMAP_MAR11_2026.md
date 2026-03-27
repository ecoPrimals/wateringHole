# Sovereign Dispatch Roadmap — Full Hardware Unblock Strategy

**Date:** 2026-03-11
**From:** hotSpring team
**To:** coralReef, toadStool, barraCuda teams
**Priority:** P0 strategic — unlocks GPU compute sovereignty across all ecoPrimals springs

---

## Executive Summary

hotSpring Exp 057 fixed 4 ioctl struct ABI bugs in `coral-driver` (commit
`b783217`) and diagnosed the remaining blockers for sovereign DRM dispatch.
The issues are NOT code bugs — they are firmware/driver architecture gaps
that affect different GPU generations differently. This handoff provides a
complete roadmap for unblocking every NVIDIA GPU generation.

---

## 1. Current Hardware Status Matrix

| GPU | Generation | Chip | DRM Driver | Firmware | Sovereign Status |
|-----|-----------|------|------------|----------|-----------------|
| Titan V | Volta | GV100 | nouveau | ACR+GR+SEC2, **no PMU** | VM_INIT ✓, CHANNEL_ALLOC ✗ |
| RTX 3090 | Ampere | GA102 | nvidia-drm | ACR+GR+SEC2+GSP | UVM not wired |
| RTX 4070 | Ada | AD104 | nvidia-drm | **GSP only** | Untested |
| AMD RX 6950 XT | RDNA2 | Navi21 | amdgpu | N/A | E2E ✓ (verified) |

### What each firmware component does

| Component | Function | Required for compute? |
|-----------|----------|----------------------|
| **PMU** (Power Management Unit) | GPU clock/voltage/thermal management | Yes (Volta/Pascal desktop) |
| **ACR** (Authenticated Code Runtime) | Secure boot chain for Falcon engines | Yes (loads other FW) |
| **GR** (Graphics/Compute) | FECS/GPCCS firmware for compute units | Yes (shader dispatch) |
| **SEC2** (Security Engine v2) | Authenticated firmware loading | Yes (Volta+) |
| **GSP** (GPU System Processor) | Replaces PMU+ACR+GR management on Turing+ | Yes (replaces PMU) |

---

## 2. RTX 3090 (GA102) — nvidia-drm UVM Path

### What exists in `coral-driver`

The `nv::uvm` module has working infrastructure:
- `RmClient::new()` — RM root client allocation via `/dev/nvidiactl` ✓
- `RmClient::alloc_device(gpu_index)` — device object with `Nv0080AllocParams` ✓
- `RmClient::alloc_subdevice(h_device)` — subdevice for GPU control ✓
- `NvUvmDevice::initialize()` — UVM context init ✓
- `UVM_REGISTER_GPU` — ioctl defined but not wired ✗
- Device probe (`NvDrmDevice::open()`) ✓

### What's missing (ordered by dependency)

```
Step 1: UVM GPU Registration
  UVM_REGISTER_GPU — needs GPU UUID from RM query
  RM_CONTROL(NV2080_CTRL_GPU_GET_UUID) → gpu_uuid

Step 2: Channel Allocation
  RM_ALLOC(AMPERE_COMPUTE_A) — compute channel under subdevice
  RM_ALLOC(NV_CHANNEL_ALLOC) — push buffer channel

Step 3: Memory Allocation
  RM_ALLOC(NV_MEMORY_*) — VRAM allocation via RM
  UVM_MAP_EXTERNAL_ALLOCATION — map into GPU VA space

Step 4: Push Buffer Construction
  Build QMD (Queue Management Descriptor) for compute dispatch
  Reference: coral-driver/nv/qmd.rs (already has QMD builder!)

Step 5: Work Submission
  Write QMD + method calls to push buffer
  Submit via channel (RM_ALLOC-ed push buffer → GPU)

Step 6: Sync
  UVM semaphore or RM fence sync
```

### Specific 0x1F error on RTX 3090

hotSpring Exp 051 reported `NV_ERR_OPERATING_SYSTEM (0x1F)` when calling
`RM_ALLOC(NV01_DEVICE_0)`. **This was fixed** in coralReef Iter 31 by
adding `Nv0080AllocParams` with `device_id` field. The fix needs hardware
re-validation on RTX 3090.

### Recommendation

The UVM path has the most infrastructure already built. Priority steps:
1. Wire `UVM_REGISTER_GPU` with GPU UUID from RM control query
2. Implement `RM_ALLOC(AMPERE_COMPUTE_A)` for channel creation
3. Implement `RM_ALLOC + UVM_MAP_EXTERNAL_ALLOCATION` for memory
4. Wire the existing `qmd.rs` QMD builder to push buffer submission

**Effort estimate:** ~2 iterations of focused work (Steps 1-3 are
well-documented in NVIDIA open-gpu-kernel-modules).

---

## 3. RTX 4070 (AD104, Ada Lovelace) — Critical Test Target

### Why test on RTX 4070

Ada Lovelace GPUs have **ONLY GSP firmware** — no ACR, GR, SEC2, or PMU.
This means:

```
/lib/firmware/nvidia/ad104/
  └── gsp/    (GSP firmware only — nothing else)

vs. /lib/firmware/nvidia/gv100/
  ├── acr/
  ├── gr/
  ├── nvdec/
  └── sec2/   (everything EXCEPT PMU)
```

**On Ada Lovelace, nouveau MUST use GSP for everything** — including compute
channel creation. If compute works at all on AD104/nouveau, it works through
GSP, proving that GSP can replace PMU for compute.

### Test plan for RTX 4070

1. Install on a machine with kernel 6.6+ (new UAPI support)
2. Load nouveau driver for the RTX 4070
3. Verify `dmesg | grep nouveau` shows GSP firmware loaded
4. Run `coralReef/examples/diag_ioctl` to test:
   - VM_INIT (should succeed with our struct fixes)
   - CHANNEL_ALLOC (should succeed IF GSP provides compute)
   - GEM_NEW + VM_BIND + EXEC pipeline
5. If CHANNEL_ALLOC works, run hotSpring `bench_sovereign_dispatch`

### What to watch for

- **GSP firmware loading**: `dmesg` should show "gsp" firmware loaded, not "pmu"
- **Compute class**: AD104 is Ada Lovelace → should use `ADA_COMPUTE_A` (0xC9C0)
  or `AMPERE_COMPUTE_A` (0xC6C0) — check what NVK uses
- **VA space init**: Our VM_INIT fix ensures correct struct size

### If it works on RTX 4070

This proves the **GSP compute path** and means:
- All Turing (RTX 20xx) GPUs with GSP should also work
- All Ampere (RTX 30xx) GPUs with GSP should also work
- Only Volta (Titan V, V100) remains blocked (no GSP, no PMU)

### If it doesn't work on RTX 4070

The issue is likely in how `coral-driver` handles GSP-based channel creation.
NVK (Mesa's Vulkan for nouveau) already works on Ada Lovelace — we can trace
NVK's ioctl calls to see the exact sequence.

---

## 4. Rust-Based GPU Power Management Tool

### The PMU gap problem

Desktop NVIDIA GPUs (Volta+) require signed PMU firmware for compute.
NVIDIA distributes this only for Tegra SoCs, not desktop cards. The PMU
handles:

| Function | PMU Role | Impact without PMU |
|----------|----------|-------------------|
| Clock management | Set/query GPU clocks | Fixed at boot clocks |
| Voltage regulation | Dynamic voltage scaling | No power optimization |
| Thermal monitoring | Temperature + fan control | No throttle protection |
| Power budgeting | TDP management | Default power states |
| Compute init | Engine initialization | **Cannot create channels** |

### Proposed: `nvPmu` — Sovereign GPU Power Manager

A Rust-based tool that provides PMU-equivalent functionality through
userspace MMIO or GSP delegation:

```
nvPmu (Rust crate)
├── clock/          — Clock domain management via MMIO/sysfs
│   ├── probe.rs    — Read current clocks from PLL registers
│   ├── set.rs      — Clock frequency setting (where allowed)
│   └── monitor.rs  — Real-time clock monitoring
├── thermal/        — Temperature + fan via MMIO/hwmon
│   ├── sensor.rs   — Read GPU temp from THERM registers
│   ├── fan.rs      — PWM fan control
│   └── policy.rs   — Thermal throttle policies
├── power/          — Power monitoring via MMIO/sysfs
│   ├── budget.rs   — TDP limits, power caps
│   ├── rail.rs     — Voltage rail monitoring
│   └── shunt.rs    — Power sensor readback
├── gsp/            — GSP firmware management
│   ├── load.rs     — Load GSP firmware into Falcon
│   ├── rpc.rs      — GSP RPC command interface
│   └── compute.rs  — Compute channel creation via GSP
└── hwmon/          — Linux hwmon integration
    ├── export.rs   — Export metrics to hwmon sysfs
    └── nvidia_smi.rs — nvidia-smi compatible CLI output
```

### What this unlocks

| GPU Generation | Current State | With nvPmu |
|---------------|--------------|------------|
| Volta (GV100) | ✗ No compute | ✓ If MMIO PMU init works |
| Turing (TU10x) | ? GSP path | ✓ GSP-managed compute |
| Ampere (GA10x) | ? GSP path | ✓ GSP-managed compute |
| Ada (AD10x) | ? GSP path | ✓ GSP-managed compute |
| All generations | No nvidia-smi alternative | ✓ Sovereign monitoring |

### Phase 1: Power monitoring (immediate value)

Even before solving compute, a Rust power monitoring tool provides:
- `nvidia-smi` replacement for sovereign systems (no proprietary driver)
- GPU temperature, clock, power monitoring via hwmon/sysfs
- Useful for all ecoPrimals springs doing GPU compute
- Foundation for toadStool hardware discovery integration

### Phase 2: GSP compute enablement

For Turing/Ampere/Ada, the GSP firmware IS the compute enabler:
- Load GSP firmware via Falcon processor
- Send GSP RPC commands for compute channel creation
- This is exactly what nouveau does internally — we'd expose it cleanly

### Phase 3: Volta PMU emulation (stretch goal)

The hardest problem: Volta has no GSP and no PMU firmware for desktop.
Options:
- **MMIO register programming** — direct PMU register initialization from
  userspace (risky, hardware-specific, but possible)
- **Falcon microcode** — write minimal PMU microcode that initializes the
  compute engine (requires reverse-engineering the Falcon ISA for PMU)
- **Accept Volta limitation** — focus on Turing+ where GSP works

### Integration with ecoPrimals

```
toadStool (hardware discovery)
  └── nvPmu (GPU power management)
      ├── Reports GPU capabilities to toadStool
      ├── Provides thermal/power telemetry
      └── Enables compute on more hardware

coralReef (sovereign compilation)
  └── Uses nvPmu for compute channel creation on GPUs
      where nouveau PMU is unavailable

barraCuda (GPU compute abstraction)
  └── Falls back to nvPmu-managed dispatch when
      neither wgpu nor nouveau can create compute channels

All springs benefit:
  hotSpring   → more hardware for MD simulations
  wetSpring   → bio compute on older cards
  neuralSpring → ML training on budget hardware
  ludoSpring  → procedural generation everywhere
```

---

## 5. Cooperative GPU Learning — 4070 Teaches Titan V

### The idea

eastgate (wetSpring/neuralSpring dev machine) has **both an RTX 4070 AND
a Titan V**. The 4070's GSP firmware successfully initializes compute — the
Titan V's compute is blocked by missing PMU firmware. If we can observe
what the 4070's GSP does to bring up compute and distill that into a
replayable sequence, we can teach the Titan V to initialize itself.

This is not just a one-off hack. It's a **cooperative hardware learning
system** — a software layer that observes working GPUs, extracts
initialization patterns, and applies them to GPUs that lack firmware.

### Architecture: `nvLearn` — Cross-GPU Initialization Learning

```
                    ┌─────────────────────────────────────┐
                    │  nvLearn (Cooperative GPU Learning)  │
                    └──────────┬──────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────────┐
         ▼                     ▼                          ▼
   ┌───────────┐      ┌──────────────┐          ┌──────────────┐
   │  Observer  │      │  Knowledge   │          │  Applicator  │
   │  (4070)    │      │  Store       │          │  (Titan V)   │
   └─────┬─────┘      └──────┬───────┘          └──────┬───────┘
         │                    │                         │
    Traces GSP          Stores register           Replays learned
    init sequence       write sequences           sequences on
    via MMIO log        per GPU generation        target GPU
    or ioctl trace      + arch signatures
```

### How it works

**Phase 1: Observe (on RTX 4070)**

When the 4070 initializes compute via GSP, the kernel performs a series
of register writes, memory allocations, and engine configurations. We
capture this by:

1. **MMIO trace**: `nouveau` has `mmiotrace` support in the kernel.
   Boot with `trace_options=mmiotrace`, initialize compute, capture the
   register write log.
2. **GSP RPC log**: nouveau logs GSP RPC commands at debug level.
   `dmesg` with `nouveau.debug=trace` captures the full RPC sequence.
3. **ioctl trace**: `strace` on NVK (Mesa Vulkan) to capture the exact
   ioctl sequence that creates a working compute channel.

**Phase 2: Distill**

The raw traces are noisy (thousands of register writes for display, audio,
etc.). The learning system:

1. Diff the trace WITH compute vs WITHOUT compute — isolate compute-specific
   register writes
2. Classify registers by function (clock, power, engine enable, channel)
3. Build a minimal "compute initialization recipe" for the GPU architecture
4. Tag the recipe with generation metadata (SM version, chip family)

**Phase 3: Apply (on Titan V)**

The Titan V shares significant register-level architecture with later
generations (Volta → Turing → Ampere share the compute engine design).
The applicator:

1. Maps 4070 (AD104) register addresses to Titan V (GV100) equivalents
   using public NVIDIA hardware documentation + envytools register database
2. Applies the minimal compute initialization sequence via MMIO or
   nouveau debugfs
3. Attempts `CHANNEL_ALLOC` after initialization
4. Validates with a simple compute dispatch

### What makes this feasible

- **Register address databases exist**: envytools (nouveau project) has
  extensive register maps for all NVIDIA generations
- **Compute engine is architecturally stable**: Volta → Ada share the same
  fundamental compute engine design (warps, SMs, compute classes)
- **nouveau already does partial init**: The Titan V gets display working
  without PMU — only the compute engine init is missing
- **We have both GPUs on one machine**: eastgate can run observer +
  applicator simultaneously, comparing behavior in real time

### Cross-spring evolution

This system embodies the ecoPrimals philosophy — primals that learn from
their environment and evolve. The knowledge flows both ways:

```
4070 (Ada, GSP)  ──teaches──►  Titan V (Volta, no PMU)
     │                              │
     │  "Here's how I init          │  "I'll try those register
     │   compute engines"           │   writes adapted for GV100"
     │                              │
     ▼                              ▼
Knowledge Store ◄──validates──  Success/failure feedback
     │
     ▼
Can teach ANY GPU missing firmware:
  - Turing without GSP → learn from Ampere
  - Ampere without GSP → learn from Ada
  - Future unknown → learn from working neighbor
```

### eastgate test plan

**Owner:** wetSpring + neuralSpring teams
**Hardware:** eastgate — RTX 4070 (AD104) + Titan V (GV100)
**Kernel:** 6.6+ required (new nouveau UAPI)

```
Week 1: Observe
  1. Boot eastgate with both GPUs on nouveau
  2. Run coralReef diag_ioctl on BOTH GPUs — capture baseline
  3. If 4070 CHANNEL_ALLOC succeeds:
     a. Run bench_sovereign_dispatch on 4070
     b. Capture dmesg GSP RPC log (nouveau.debug=trace)
     c. Capture mmiotrace of compute initialization
  4. If 4070 CHANNEL_ALLOC fails:
     a. Check kernel version (need 6.6+)
     b. Check GSP firmware loading in dmesg
     c. Compare with NVK ioctl trace (strace vulkaninfo)

Week 2: Distill
  5. Diff compute vs no-compute traces
  6. Identify compute-specific register writes
  7. Map registers to envytools database
  8. Build GV100 equivalent register map

Week 3: Apply
  9. Write register programming tool (Rust, uses nouveau debugfs)
  10. Apply minimal compute init on Titan V
  11. Test CHANNEL_ALLOC after init
  12. If successful: run full hotSpring benchmark

Week 4: Generalize
  13. Package as nvLearn crate
  14. Document the learned initialization sequences
  15. Handoff to toadStool for hardware discovery integration
```

### Integration with nvPmu

`nvLearn` and `nvPmu` are complementary:

| Tool | Purpose | Scope |
|------|---------|-------|
| **nvPmu** | Power/thermal/clock management | All GPUs, immediate |
| **nvLearn** | Compute init learning from working GPUs | Cross-generation, research |

Both feed into toadStool's hardware capability model and coralReef's
dispatch routing. Together they form a **sovereign GPU enablement stack**
that progressively unlocks compute on every NVIDIA card without depending
on proprietary firmware distribution.

---

## 6. Specific Next Steps (Prioritized)

### P0 — Immediate (this week)

1. **coralReef**: Accept the 4 struct ABI fixes from `b783217`
2. **coralReef**: Add compile-time size assertions for all UAPI structs
3. **coralReef**: Re-validate RM client on RTX 3090 (0x1F may be fixed)

### P1 — Short term (next iteration)

4. **coralReef**: Wire `UVM_REGISTER_GPU` + GPU UUID query
5. **coralReef**: Implement `RM_ALLOC(AMPERE_COMPUTE_A)` for RTX 3090
6. **wetSpring + neuralSpring (eastgate)**: Test nouveau + `diag_ioctl` on
   RTX 4070 (AD104) — GSP compute validation. eastgate has both 4070 AND
   Titan V, making it the ideal testbed for cross-GPU learning.
7. **wetSpring + neuralSpring (eastgate)**: If 4070 works, capture GSP RPC
   + mmiotrace logs for the nvLearn knowledge store

### P2 — Medium term (2-3 iterations)

8. **coralReef**: Complete UVM dispatch pipeline (alloc → map → submit → sync)
9. **toadStool**: Add PMU/GSP firmware probe to hardware discovery
10. **New crate**: `nvPmu` Phase 1 — power monitoring via hwmon/sysfs
11. **wetSpring + neuralSpring (eastgate)**: Begin nvLearn Phase 1 —
    observe GSP init on 4070, diff against Titan V, build register map

### P3 — Long term (evolution)

12. **nvPmu**: Phase 2 — GSP compute enablement for Turing+
13. **nvLearn**: Phase 3 — Apply learned init sequences to Titan V on eastgate
14. **barraCuda**: Integrate `nvPmu`/`nvLearn`-managed dispatch as fourth backend tier
15. **All springs**: Package nvLearn knowledge store so any ecoPrimals machine
    with a working GPU can teach its neighbors

---

## 7. Hardware Test Matrix for Validation

### Available test rigs

| Machine | GPUs | Driver Config | Owner |
|---------|------|--------------|-------|
| **hotSpring rig** | RTX 3090 (GA102) + Titan V (GV100) | nvidia-drm + nouveau | hotSpring |
| **eastgate** | RTX 4070 (AD104) + Titan V (GV100) | nouveau + nouveau | wetSpring + neuralSpring |

### Test matrix

| GPU | Machine | Driver | Tests | Purpose |
|-----|---------|--------|-------|---------|
| RTX 4070 | eastgate | nouveau | diag_ioctl + bench | **GSP compute (highest priority)** |
| Titan V | eastgate | nouveau | diag_ioctl + nvLearn | Cross-GPU learning target |
| RTX 3090 | hotSpring rig | nvidia-drm | UVM pipeline | Proprietary dispatch path |
| Titan V | hotSpring rig | nouveau | diag_ioctl | PMU investigation baseline |
| Any AMD | TBD | amdgpu | Full E2E | Baseline reference (already verified) |

### eastgate is the key

eastgate is uniquely positioned: it has a 4070 (GSP-only, Ada Lovelace)
AND a Titan V (no PMU, Volta) in the same machine. This enables:

1. **Simultaneous testing** — run diag_ioctl on both GPUs in one session
2. **Cross-GPU tracing** — observe what GSP does on the 4070, apply to Titan V
3. **Real-time validation** — if learned init works, immediately benchmark
4. **Two springs developing** — wetSpring (bio compute) and neuralSpring
   (ML) both benefit from unlocked hardware and can share the workload

The RTX 4070 test is the **highest ROI** — if GSP works on Ada, it
retroactively proves Turing and Ampere via the same code path. And with
the Titan V right next to it, we can immediately test cross-GPU learning.
