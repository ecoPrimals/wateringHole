# hotSpring → coralReef / toadStool / biomeGate: Sovereign GPU Pipeline Handoff

**Date:** 2026-03-30
**From:** strandgate (hotSpring v0.6.32, Exp 124)
**To:** coralReef team, toadStool team, biomeGate GPU cracking team
**Hardware:** RTX 3090 (SM86) + RX 6950 XT (GFX10.3) on strandgate; Titan V + K80 on biomeGate

---

## What Happened

Two major sovereign pipeline breakthroughs in the same session:

### 1. AMD Scratch/Local Memory — OPERATIONAL (Exp 124)

Per-thread scratch memory now works on RDNA2 through the sovereign DRM pipeline.
Three-layer fix across compiler, driver, and hardware initialization.

**Key discovery for all teams:** The amdgpu DRM Command Processor does NOT
auto-initialize `FLAT_SCRATCH_LO/HI` from `COMPUTE_DISPATCH_SCRATCH_BASE` for
compute IB submissions. This differs from HSA/KFD (ROCm/HIP). The fix is a
24-byte shader prolog that explicitly writes `HW_REG_FLAT_SCR_LO` (ID 20) and
`HW_REG_FLAT_SCR_HI` (ID 21) via `S_MOV_B32` + `S_SETREG_B32`.

**Files changed:**
- `coral-reef/src/codegen/amd/encoding.rs` — `encode_scratch_load/store` methods
- `coral-reef/src/codegen/ops/memory.rs` — `OpLd`/`OpSt` routing for `MemSpace::Local`
- `coral-driver/src/amd/mod.rs` — scratch alloc, PM4 wiring, FLAT_SCRATCH prolog
- `coral-driver/src/amd/pm4.rs` — `build_compute_dispatch` gains `scratch_va` param

**Validation:** 7/8 coral-gpu hardware parity tests pass. 1672 unit tests pass.

### 2. NVIDIA GPFIFO — OPERATIONAL (Previous Session, Confirmed Stable)

RTX 3090 channel initialization sequence fully working. 350 unit tests pass.
NOP smoke test, alloc/free/sync, SM86 compilation all operational.

**Key for biomeGate:** The channel init sequence (BIND + TSG + Context Share +
VRAM USERD + Error Notifier + 48-byte NVOS64) applies to all Volta+ architectures.
Your Titan V and K80 use the same code paths. The remaining Titan V blocker is
solely L10 (WPR2/FWSEC hardware lock), not the dispatch infrastructure.

---

## What This Means for Each Team

### coralReef Team

The compiler and driver changes are in your codebase. Key items to absorb:

1. **AMD scratch codegen** is correct — `SEG=SCRATCH` instructions validated on hardware
2. **FLAT_SCRATCH prolog** is a runtime patch, not a compiler change — `coral-driver`
   prepends it at dispatch time when `local_mem_bytes > 0`
3. **Next compiler frontier:** EXEC masking for divergent control flow. Wilson plaquette
   QCD has if/else/loop patterns that require EXEC save/restore around branches.
   Without this, AMD Wilson plaquette dispatch hangs.
4. **NVIDIA GR context:** The `NvUvmComputeDevice` needs GR context allocation via RM
   (`NV2080_CTRL_CMD_GR_GET_CTX_BUFFER_SIZE` → `NV01_MEMORY_LOCAL_USER` × N buffers
   → `NVC36F_CTRL_CMD_GPFIFO_SET_WORK_SUBMIT_TOKEN`). Without GR context,
   `SKEDCHECK05_LOCAL_MEMORY_TOTAL_SIZE` rejects shaders that use LDL/STL.
5. **QMD v2.2 layout:** `build_qmd_v21` still uses Kepler-era positions. The biomeGate
   team needs correct Volta v2.2 positions from `clc3c0qmd.h`.

### toadStool Team

1. **Silicon exposure evolution:** The scratch memory path means consumer cards can now
   run QCD kernels that require per-thread temporaries. This expands the set of shaders
   dispatchable via `shader.dispatch` to include spill-heavy compute workloads.
2. **Precision routing:** Scratch memory usage is a new dimension for the precision brain.
   Kernels with large `local_mem_bytes` have different performance characteristics
   (memory-bound vs compute-bound) and should be routed differently.
3. **AMD characterization:** The RX 6950 XT now has a proven DRM scratch path. The
   `SiliconCapabilityMatrix` should include scratch memory support as a capability flag.

### biomeGate GPU Cracking Team

1. **FLAT_SCRATCH for GFX9 (MI50/Vega):** The prolog pattern should apply with different
   `HW_REG` IDs. On GFX9, `FLAT_SCRATCH` may use different register numbers — check
   AMD ISA documentation for Vega. The `S_MOV_B32` + `S_SETREG_B32` pattern is the same.
2. **NVIDIA channel init:** The full sequence discovered on strandgate's RTX 3090 is now
   in `coral-driver/src/nv/uvm_compute.rs`. Adapt for your driver version.
3. **K80 (Kepler):** No firmware security → PIO FECS/GPCCS boot should work directly.
   Code is ready in `nv::kepler_falcon`. Channel class is `KEPLER_COMPUTE_B = 0xA1C0`.
4. **Titan V:** L10 remains the sole blocker. WPR2 is hardware-locked, FWSEC inaccessible.
   The VFIO parasitic compute path (sysfs BAR0 while nouveau active) is the next option.

---

## Remaining Sovereign Pipeline Debt

| Item | Vendor | Owner | Difficulty |
|------|--------|-------|------------|
| GR context allocation via RM | NVIDIA | coralReef | Medium — requires RM ioctl sequence |
| EXEC masking for divergent CF | AMD | coralReef | Hard — compiler architecture change |
| QMD v2.2 Volta layout | NVIDIA | coralReef | Easy — field position lookup |
| SSARef LARGE_SIZE panic | Both | coralReef | Medium — allocator redesign |
| GFX9 FLAT_SCRATCH HW_REG IDs | AMD | biomeGate | Easy — ISA doc lookup |
| L10 WPR2/FWSEC bypass | NVIDIA | biomeGate | Hard — hardware security boundary |
| Tensor/RT core utilization | Both | toadStool + hotSpring | Research — ISA exploration |

---

## Test Commands

```bash
# AMD scratch memory test
cd primals/coralReef
cargo test --package coral-gpu --test parity_harness parity_hw_local_memory_f64 -- --nocapture

# Full hardware parity suite
cargo test --package coral-gpu --test parity_harness -- --nocapture

# NVIDIA GPFIFO smoke test
cargo test --package coral-driver nv::uvm -- --nocapture

# All coral-driver unit tests
cargo test --package coral-driver -- --nocapture
```

---

*hotSpring v0.6.32 — strandgate — 2026-03-30*
