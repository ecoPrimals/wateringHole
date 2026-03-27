# Sovereign Compute Trio — Remaining Catchup Work & hotSpring Leverage Map

**Date:** March 17, 2026
**From:** hotSpring v0.6.32 (experiments 001–069)
**To:** coralReef, toadStool, barraCuda
**License:** AGPL-3.0-or-later
**Type:** Trio coordination — remaining reverse engineering work + hotSpring leverage points

---

## Executive Summary

hotSpring ran 69 experiments on 2× Titan V (GV100, SM70) via VFIO, proving the
sovereign GPU path from cold silicon through glow plug warming to FECS firmware
execution. The trio has absorbed significant infrastructure since the pin, but
**sovereign dispatch remains blocked** at the GR engine context layer. This
document maps every remaining gap, assigns ownership, and defines what hotSpring
can leverage once each gap closes.

### Scoreboard (March 17, 2026)

| Layer | Component | Owner | Status | Blocker |
|-------|-----------|-------|--------|---------|
| -1 | PCIe power (D3hot→D0) | coralReef (coral-glowplug) | **Complete** | — |
| 0 | Glow plug (PMC_ENABLE warmup) | coralReef (coral-glowplug) | **Complete** | — |
| 1 | BAR2 self-warm (V2 MMU via PRAMIN) | coralReef | **Complete** | — |
| 2 | PFIFO/PBDMA init | coralReef | **Blocked** | MMU fault buffers (Gap 2) |
| 3 | Channel + runlist submission | coralReef | **Blocked** | Runlist encoding (Gap 3) |
| 4 | GR engine context (FECS/GPCCS) | coralReef | **Blocked** | CTXNOTVALID (Gap 5) |
| 5 | Shader compilation (WGSL→SASS) | coralReef (coralNak) | **Operational** | — |
| 6 | Math + shaders | barraCuda | **Complete** | — |
| 7 | Hardware discovery | toadStool | **Partial** | GlowPlug client missing |
| 8 | GlowPlug daemon | coralReef (coral-glowplug) | **Production** | SCM_RIGHTS pending |
| 9 | NVK bridge path | Mesa (external) | **Blocked** | Build from source required |

---

## Part 1: What hotSpring Proved (Fossil Record)

These are hardware truths discovered by experiments 058–069. They do not expire.

| Discovery | Experiment | Impact |
|-----------|-----------|--------|
| D3hot does NOT kill HBM2 training | 062 | VFIO devices keep full VRAM after D0 restore |
| Desktop Volta has no PMU firmware | 059 | All power management is pure BAR0 register writes |
| Glow plug warms GPU in ~50ms | 059–060 | No nouveau/nvidia dependency for GPU init |
| BAR2 self-warm matches nouveau parity | 060 | Kernel driver fully eliminated for warming |
| FECS firmware executes from host IMEM | 066–068 | LS security bypass on clean falcon (D3hot→D0 path) |
| VFIO close triggers PM reset (GV100) | 062 | HBM2 destroyed — must hold fd open forever |
| PRIVRING FATAL on GR power toggle | 068 | Never toggle GR bit 12 without full init |
| 24/26 hardware tests pass via pure Rust VFIO | 062 | VBIOS, VRAM, 15/18 domains from cold |
| DRM render node fencing prevents kernel oops | 065 | Desktop apps must not grab sovereign GPU render nodes |
| Digital PMU: 1,067 registers from oracle | 062 | 71% PRI-faulted (behind Volta clock gates) |

---

## Part 2: coralReef — Remaining Reverse Engineering Work

coralReef owns Layers -1 through 5. Layers -1 through 1 are complete. Layers 2–4
are the active frontier.

### Gap 2 — MMU Fault Buffers (P1, days)

PBDMA cannot dispatch if the MMU has no fault buffer configured. The GPU hangs
silently waiting for fault buffer addresses.

**What we know:**
- GV100 MMU fault buffers use specific BAR0 registers for fault buffer base + size
- Must use system memory DMA buffers (not VRAM) for fault reporting
- Aperture encoding must be correct for system memory access

**What to do:**
1. Allocate 4KB page-aligned system memory for replayable + non-replayable fault buffers
2. Write physical addresses to MMU fault buffer registers
3. Enable fault buffer interrupts
4. Verify no MMU faults on idle channel

**hotSpring leverage:** Once fault buffers work, PBDMA activation (Gap 4) becomes testable.

### Gap 3 — Runlist Submission (P1, days)

hotSpring found three bugs in the original runlist code (Exp 061):
- Wrong register base (GV100 uses per-runlist at `0x2270 + rl_id*0x10`)
- Wrong runlist entry encoding (instance block address field format)
- Wrong architecture variant handling (Volta vs Maxwell/Pascal)

**What we know:**
- Register values documented in `GPU_SOVEREIGN_BRING_UP_GUIDE.md` Part 3
- Correct encoding: 12-byte runlist entries with instance_ptr, type, engine mask
- GV100 runlist doorbell at `0x2270 + rl_id*0x10`

**What to do:**
1. Fix runlist register base address
2. Fix entry encoding (instance block pointer format)
3. Submit a minimal runlist with one channel targeting PBDMA 0
4. Verify runlist accepted (read status register, no timeout)

**hotSpring leverage:** Correct runlist enables PBDMA to see channels.

### Gap 4 — PBDMA Activation (P1, days)

`GP_GET` stays 0 despite `GP_PUT=1`. The PBDMA never starts fetching commands
from the GPFIFO.

**What we know (from Exp 058, 061):**
- USERD_TARGET in runlist entry must point to system memory, not VRAM
- MMU fault buffer absence may be the root cause (GPU faults internally, never reports)
- PBDMA needs: valid channel in runlist, valid instance block, valid GPFIFO, MMU fault buffers

**What to do:**
1. Fix MMU fault buffers (Gap 2) first
2. Fix runlist submission (Gap 3) second
3. Re-test GP_PUT → GP_GET advancement
4. If still stuck: check instance block DMA address encoding

**hotSpring leverage:** Once GP_GET advances, GPFIFO commands execute — first sovereign DMA.

### Gap 5 — GR Engine Context (FECS/GPCCS) (P2, weeks)

The GR (Graphics) engine requires context initialization via its Falcon
coprocessors. FECS halted at PC=0x2835 — likely waiting for GPCCS.

**What we know:**
- FECS firmware runs from host IMEM (Exp 068 — 25,582 of 25,632 bytes executed)
- GPCCS address not yet discovered on GV100 (suspected in 0x400000–0x500000 BAR0 range)
- Both falcons must be running for GR context switch to complete
- `sw_ctx.bin` is parsed but currently discarded — needs to be loaded into FECS DMEM

**What to do:**
1. Scan BAR0 0x400000–0x500000 for GPCCS falcon BOOT0 signature
2. Load GPCCS firmware to IMEM/DMEM (same technique as FECS)
3. Start GPCCS, then re-run FECS
4. Verify GR context created (read GR status registers)

**hotSpring leverage:** Once GR context works, compute shader dispatch is possible —
the full WGSL → SASS → GPFIFO → GR pipeline lights up.

### Gap 6 — AMD Vega Metal (P3, days)

MI50/GFX906 register stubs defined in coral-glowplug Iter 52. Full
implementation needed for:
- `power_domains()` → SMC, GRBM, SRBM
- `memory_controllers()` → UMC (HBM2), GC L2
- `compute_engines()` → GFX, SDMA, VCN
- `power_on_sequence()` → D0 init register writes

**hotSpring leverage:** Enables AMD MI50 bring-up (Phase 4 of hotSpring return plan).

### Remaining coralReef Deliverables

| Item | Priority | Status | ETA |
|------|----------|--------|-----|
| MMU fault buffer config | P1 | Not started | Days |
| Runlist encoding fix | P1 | Bugs identified, not fixed | Days |
| PBDMA activation | P1 | Blocked on Gaps 2+3 | Days after 2+3 |
| GPCCS discovery + load | P2 | BAR0 scan needed | Hours–days |
| FECS+GPCCS dual boot | P2 | Blocked on GPCCS | Days after scan |
| SCM_RIGHTS fd passing | P2 | Not started | Days |
| AMD Vega metal impl | P3 | Stubs only | Days |
| DRM consumer fence | P3 | Design documented | Hours |
| Privilege model (CAP_SYS_ADMIN) | P3 | Design documented | Days |

---

## Part 3: toadStool — Remaining Integration Work

toadStool is unblocked by coralReef's JSON-RPC 2.0 delivery (Iter 51–52).

### GlowPlug Socket Client (P1, days)

**Status:** Unblocked, not started.

coralReef delivered the JSON-RPC socket API at `/run/coralreef/glowplug.sock`.
toadStool needs a client crate to consume it.

**Methods available:**
- `device.list` → `[{bdf, name, personality, vram_alive, power, chip}]`
- `device.health` → `{vram, power, domains, pci_link_width}`
- `device.swap` → `{bdf, target_personality}` → `{ok, snapshot_id}`
- `health.check` → daemon health
- `daemon.status` → full daemon status
- `daemon.shutdown` → graceful stop

**What to build:**
```rust
pub struct GlowPlugClient {
    socket: UnixStream,
}
impl GlowPlugClient {
    pub fn connect(path: &str) -> Result<Self>;
    pub fn list_devices(&self) -> Result<Vec<DeviceInfo>>;
    pub fn health(&self, bdf: &str) -> Result<DeviceHealth>;
    pub fn swap(&self, bdf: &str, target: &str) -> Result<SwapResult>;
    pub fn resurrect(&self, bdf: &str) -> Result<ResurrectResult>;
}
```

Discovery: check `XDG_RUNTIME_DIR/coralreef/glowplug.sock` then `/run/coralreef/glowplug.sock`.

**hotSpring leverage:** hotSpring's `bench_sovereign_dispatch` can auto-discover
VFIO Titan V devices via toadStool instead of hardcoded BDFs.

### VFIO Device Detection in sysmon (P1, days)

`toadstool-sysmon` should detect vfio-pci bound devices:
- Scan `/sys/bus/pci/drivers/vfio-pci/` for bound BDFs
- Read IOMMU group from `/sys/kernel/iommu_groups/`
- Report as `GpuDevice` with `driver: "vfio-pci"` and `sovereign: true`

**hotSpring leverage:** Sovereign device auto-detection in dispatch routing.

### hw-learn GlowPlug Health Feed (P2, weeks)

Feed `DeviceHealth` from GlowPlug into toadStool's learning pipeline:
- VRAM alive/dead transitions → training data for HBM2 lifecycle model
- Power state changes → D0/D3hot pattern recognition
- Domain fault history → predict hardware failures

**hotSpring leverage:** Long-running MD simulation stability — predict GPU health
issues before they corrupt a simulation mid-run.

### SCM_RIGHTS Consumer (P2, blocked on coralReef)

When coralReef implements SCM_RIGHTS fd passing, toadStool needs to receive
VFIO container file descriptors through the GlowPlug socket. This is the key
integration that lets toadStool dispatch compute work on sovereign VFIO devices
without needing root access itself.

**hotSpring leverage:** Full sovereign dispatch through the trio pipeline:
`barraCuda → coralReef (compile) → toadStool (dispatch) → GlowPlug (VFIO fd)`.

### Remaining toadStool Deliverables

| Item | Priority | Blocked On | ETA |
|------|----------|------------|-----|
| GlowPlug socket client | P1 | — | Days |
| VFIO device detection in sysmon | P1 | — | Days |
| PowerManager absorption | P2 | — | Days |
| hw-learn health feed | P2 | Socket client | Days |
| SCM_RIGHTS consumer | P2 | coralReef | Blocked |
| ResourceOrchestrator wiring | P3 | Socket client | Days |

---

## Part 4: barraCuda — Minimal Remaining Work

barraCuda's IPC-first design means it requires zero changes for sovereign
dispatch to work. The compile→dispatch pipeline flows:
`barraCuda → coralReef (compile) → toadStool (dispatch) → GlowPlug (VFIO)`.

### NVK Verification (P1, hours)

Build Mesa from source on Pop!_OS with `-Dvulkan-drivers=nouveau` to get
`libvulkan_nouveau.so`. This enables the NVK Vulkan path on Titan V, which
is the **current operational route** for GPU compute (the sovereign path is
blocked at Layer 2–4).

**GlowPlug Swap Validation Plan** (7 steps):
1. Verify Titan V on VFIO (via `device.list`)
2. Swap target to nouveau (`device.swap(bdf, "nouveau")`)
3. Install NVK ICD (`VK_ICD_FILENAMES`)
4. Enumerate wgpu adapters (should see Titan V via NVK)
5. Run DF64 verification on NVK (`bench_cross_spring_evolution`)
6. Swap back to VFIO (`device.swap(bdf, "vfio")`)
7. Run VFIO sovereign dispatch test (`bench_sovereign_dispatch`)

**hotSpring leverage:** Steps 5+7 produce the first real math comparison between
wgpu/NVK and the sovereign pipeline on identical hardware.

### GB206 (RTX 5060) Profile (P1, hours)

Add device ID `0x2d05` to `GpuArch` enum. Currently reports `Arch: Unknown`
despite DF64 working via `Df64SpirVPoisoning` workaround.

### Future Opportunity — GlowPlugBackend

When PFIFO dispatch works (coralReef Gaps 2–5 closed), barraCuda could add a
`GlowPlugBackend` variant to `GpuBackend` that dispatches directly through
GlowPlug's socket, bypassing wgpu/Vulkan entirely. But this depends on
sovereign dispatch actually working.

---

## Part 5: Critical Path to Sovereign Dispatch

The gaps have a strict dependency chain:

```
Gap 2 (MMU fault buffers)
  └──→ Gap 3 (Runlist encoding)
        └──→ Gap 4 (PBDMA activation)
              └──→ Gap 5 (FECS/GPCCS context)
                    └──→ SOVEREIGN DISPATCH
                          └──→ hotSpring: bench_sovereign_dispatch
                                └──→ Math comparison: wgpu/NVK vs coralReef/DRM
```

**Parallel work (not blocked):**
- toadStool GlowPlug socket client (can start now)
- toadStool VFIO sysmon detection (can start now)
- barraCuda NVK build + swap validation (can start now)
- barraCuda GB206 profile (can start now)
- coralReef AMD Vega metal (independent of NVIDIA path)
- coralReef SCM_RIGHTS (independent of dispatch)

**The NVK bridge path** is the interim solution. hotSpring can run real GPU
compute today by swapping a Titan V to nouveau via GlowPlug, running DF64
shaders through NVK/Vulkan, and swapping back. This validates math while
the sovereign path catches up.

---

## Part 6: What hotSpring Will Leverage (Return Plan)

### Phase 1: NVK Validation (hours)
- Build NVK from Mesa source
- Execute GlowPlug swap validation (7 steps above)
- Run DF64 on real NVK hardware
- Publish comparison: wgpu/nvidia vs wgpu/NVK vs sovereign (when available)

### Phase 2: GPCCS Discovery (hours–days)
- Scan GV100 BAR0 for GPCCS falcon (0x400000–0x500000)
- If found: feed results back to coralReef for firmware loading
- This accelerates Gap 5 resolution

### Phase 3: Sovereign Dispatch Attempt (when Gaps 2–5 close)
- Pull evolved coralReef with fixed runlist + MMU fault buffers
- Submit nop shader through PFIFO
- If it runs: first sovereign compute dispatch on GV100 → Exp 070
- Run Yukawa OCP benchmark: `bench_sovereign_dispatch` (wgpu vs coralReef)

### Phase 4: AMD MI50 Bring-Up (when card arrives)
- Add MI50 BDF to `glowplug.toml`
- Verify auto-discovery + health monitoring
- Run first coralReef → GFX906 compilation → amdgpu dispatch

---

## Part 7: Stability Invariants (Do Not Change)

- **Boot personality:** Both Titans stay on `vfio` at boot. DRM render node kernel
  oops recurs if nouveau boots on non-display GPU.
- **`disable_idle_d3`:** GV100 PM reset blocks indefinitely without this.
- **`reset_method` disable:** Same PM reset issue on shutdown.
- **GlowPlug ownership:** Part of coralReef (PCIe level), not toadStool (abstraction level).
- **Display GPU exclusion:** RTX 5060 on nvidia is NEVER managed by GlowPlug.

---

## Related Documents

- `wateringHole/GPU_SOVEREIGN_BRING_UP_GUIDE.md` — 7 gaps, full bring-up sequence
- `wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` — long-term evolution plan
- `wateringHole/CROSS_SPRING_SHADER_EVOLUTION.md` — shader flow between springs
- `barraCuda/specs/REMAINING_WORK.md` — barraCuda P1–P4 tracker
- `hotSpring/experiments/064_GLOWPLUG_DEVICE_BROKER_ARCHITECTURE.md` — GlowPlug design
- `hotSpring/wateringHole/handoffs/HOTSPRING_BACKEND_ANALYSIS_GLOWPLUG_SWAP_VALIDATION_MAR17_2026.md` — swap validation plan

---

*The math is done. The compiler works. The GPU warms from cold.*
*What remains is plumbing: fault buffers, runlists, context load.*
*Each gap closed brings sovereign dispatch one layer closer.*
