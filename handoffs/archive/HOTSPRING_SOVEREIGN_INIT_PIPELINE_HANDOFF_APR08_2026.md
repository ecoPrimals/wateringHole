# hotSpring Handoff: SovereignInit Pipeline — nouveau Replaced (April 8, 2026)

**From:** hotSpring (Exp 164-165)
**To:** All spring teams, primal teams (coralReef, toadStool, barraCuda especially)
**Status:** SovereignInit pipeline implemented, firmware-as-ingredient architecture established

---

## What Happened Since Last Handoff (Exp 164-165)

### Experiment 164: Full Compute Dispatch PROVEN
- **5/5 E2E phases pass** on Titan V via nouveau DRM: f32 write, f32 arithmetic, multi-workgroup, f64 write, f64 Lennard-Jones
- 7 bugs found and fixed between NOP dispatch and full compute (NVIF context, subchannel assignment, method offsets, local memory window, QMD v02_02 bitfields, SPH header offset, sign convention)
- Full dispatch pipeline: `WGSL → coral-reef (SM70) → 128B SPH + SASS → NvDevice::dispatch() → GEM+VM_BIND → Push → EXEC → SYNCOBJ_WAIT → readback`
- **Significance**: First end-to-end sovereign GPU compute — WGSL to verified physics output on NVIDIA silicon, zero CUDA, zero C, pure Rust

### Experiment 165: SovereignInit Pipeline — nouveau Replaced Subsystem by Subsystem
- **8-stage pure Rust GPU initialization pipeline** replaces every nouveau init subsystem
- Firmware treated as **ingredient** (proprietary blobs loaded by Rust, executed by hardware)
- `NvVfioComputeDevice::open_sovereign(bdf)` — single function, cold/warm to compute-ready
- `SovereignInitResult` with `compute_ready()` + `diagnostic_summary()` for structured reporting
- GR init functions extracted to standalone module-level fns (reusable by DRM and VFIO paths)
- `FalconBootSolver` with 15 strategies, `legacy-acr` feature flag gates older paths
- `Hbm2Controller` typestate pipeline for HBM2 training (VBIOS interpreter backend)
- FECS method probe validates falcon responsiveness beyond register reads
- Optional Stage 7: GR context allocation + golden save
- 429 coral-driver tests pass, 171 coral-ember tests pass

## Key Insight for All Teams

**The driver/firmware boundary is the same as motherboard BIOS.** We interface with GPU firmware the way toadStool interfaces with motherboard firmware — probe capabilities, inject data, and let the hardware execute its own code. The Rust driver manages the sequencing and orchestration.

**The pattern scales**: Kepler (direct PIO, no security) → Volta (PMU mailbox + ACR) → Turing+ (GSP RPC). Each generation has the same structure with different transport.

## Updated Science Ladder

```
... → Firmware Boundary ✅ → NOP Dispatch ✅ → Full Compute (5/5 DRM) ✅ → SovereignInit Pipeline ✅
→ Hardware validation (cold-boot Titan V) → Production QCD via open_sovereign() → Cross-vendor sovereign
```

## What Each Primal Should Know

### coralReef (primary absorption target)
- **`open_sovereign()`** is the nouveau replacement entry point — absorb this into production paths
- **GR init extraction** (`apply_gr_bar0_init`, `apply_nonctx_writes`, `apply_dynamic_gr_init`) are now standalone fns — both DRM and VFIO paths call them
- **`FalconBootSolver`** with 15 strategies covers SEC2→ACR→FECS boot chain, `legacy-acr` feature gates old paths
- **`Hbm2Controller`** typestate pipeline ready for additional backends (differential replay, falcon upload)
- **`SovereignInitResult`** structured diagnostics integrate into fleet health monitoring
- **Status**: 429 tests, cargo check clean with `--features vfio`

### toadStool (hardware abstraction)
- **Firmware-as-ingredient pattern** aligns with toadStool's `FirmwareInventory::probe()` — same architectural philosophy
- **HBM2 training via VBIOS interpreter** is the GPU equivalent of toadStool's BIOS POST handling
- **Capability discovery** (GPC/TPC/SM/FBP/PBDMA enumeration) follows toadStool's runtime probe pattern
- **Absorption target**: `Hbm2Controller` and `TrainingBackend` may move upstream as toadStool GPU support matures

### barraCuda (GPU compute library)
- **`open_sovereign()` returns a compute-ready device** that barraCuda can dispatch to directly
- **SM version auto-detection** from topology discovery (Stage 2) provides `GpuCapabilities` for shader compilation
- **DF64 + sovereign dispatch** stack is now end-to-end: `WGSL → coral-reef → SovereignInit → VFIO dispatch`

### ember / glowplug (fleet management)
- **`ember.gpu.train_hbm2` RPC** with fork-isolation safety for cold boot HBM2 training
- **warm_handoff_vfio example** now uses SovereignInit for post-handoff validation
- **Fleet health**: `SovereignInitResult::compute_ready()` provides binary go/no-go for each GPU

## What Springs Should Know

1. **165 experiments** in the fossil record — `EXPERIMENT_INDEX.md` is the authoritative ledger
2. **Every nouveau init subsystem** has a Rust equivalent (mc_init, fb_init, gr_init, secboot, fifo_init, gr_init_ctx, devinit)
3. **Firmware handling = BIOS handling** — the GPU runs its own code, we manage the loading/sequencing
4. **Next blocker**: hardware validation of the SovereignInit pipeline on cold-boot Titan V
5. **Cross-vendor target**: same WGSL→compute pipeline on MI50 (AMD) + Titan V (NVIDIA) in one session

## Documents Updated

| Document | What Changed |
|----------|-------------|
| `hotSpring/README.md` | Status section: SovereignInit pipeline, 165+ experiments |
| `hotSpring/EXPERIMENT_INDEX.md` | Experiments 164-165 added, total updated |
| `hotSpring/experiments/165_SOVEREIGN_INIT_PIPELINE.md` | New: full pipeline architecture and changes |
| `hotSpring/whitePaper/baseCamp/sovereign_gpu_compute.md` | Phase 20 (SovereignInit), updated pipeline table |
| `ecoPrimals/infra/whitePaper/gen3/baseCamp/EXTENSION_PLAN.md` | April 8 SovereignInit section |
| `ecoPrimals/infra/whitePaper/gen3/baseCamp/14_sovereign_compute_hardware.md` | April 8 pipeline status |

## Remaining Gaps (for Gaps Review)

| Gap | Owner | Blocker? |
|-----|-------|----------|
| Cold-boot Titan V hardware validation | hotSpring | Yes — pipeline implemented, needs real run |
| HBM2 PHY calibration data | hotSpring + coralReef | Yes — VBIOS interpreter needs real sequence |
| PMU command vocabulary | hotSpring | No — `PmuInterface` exists, commands discoverable |
| Layer 10 HS auth (VFIO only) | coralReef | No — DRM path bypasses entirely |
| GSP RPC client (Turing+) | coralReef | No — pattern known, transport differs |
| AMD sovereign init equivalent | coralReef + hotSpring | No — AMD DRM already proven (6/6 pass) |
| Production QCD dispatch via sovereign | hotSpring + barraCuda | No — waiting on cold-boot validation |
