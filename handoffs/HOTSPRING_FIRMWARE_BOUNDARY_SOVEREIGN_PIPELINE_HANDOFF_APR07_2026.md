# hotSpring Handoff: Firmware Boundary & Sovereign Pipeline Status (April 7, 2026)

**From:** hotSpring (Exp 144-163)
**To:** All spring teams, primal teams
**Status:** Firmware boundary delineated, NOP dispatch proven, pipeline status updated

---

## What Happened Since Last Handoff (Exp 144-163)

### Experiments 144-150: Ember Hardening + Crash Vector Hunt
- PMC bit5 SEC2 discovery and ACR pipeline progression (Exp 144)
- PRAMIN isolated as crash/lockup vector on cold VRAM (Exp 150)
- Cold VRAM (`0xbad0ac0X`) now detected and reported gracefully
- Full revalidation + ember survivability hardening complete (Exp 151)

### Experiments 152-158: Multi-Backend + K80 + SEC2
- Compute dispatch provenance validation across backends (Exp 152)
- Ember flood/resurrection proof under continuous fault injection (Exp 153)
- K80 warm FECS dispatch (Kepler PIO path), DEVINIT replay risks (Exp 155-157)
- SEC2 real firmware execution — stalls on DMA without HBM2 training (Exp 158)

### Experiments 159-163: Firmware Boundary Pivot (THE BREAKTHROUGH)
- **Exp 159**: HBM2 trained via nvidia-535 VM passthrough. FLR kills training. nouveau warm-cycle + `reset_method` clear preserves HBM2.
- **Exp 160-162**: MMIOTRACE capture, NVDEC attempt, sovereign compute pipeline design
- **Exp 163**: **Architectural pivot.** Driver/firmware/hardware delineation established. NOP dispatch proven via DRM (C + pure Rust). PMU mailbox protocol mapped. `PmuInterface` struct created.

## Key Insight for All Teams

**GPU falcon firmware = GPU's BIOS.** The correct approach is firmware-agnostic interfacing (probe → interface → inject), not firmware replacement. This is the same pattern toadStool uses for motherboard firmware.

**Practical impact:** The DRM path (through nouveau kernel driver) handles all firmware interaction. The sovereign Rust pipeline uses DRM ioctls for command submission — no need to understand the internal firmware state machine. The VFIO path remains for Kepler (no firmware) and advanced diagnostics.

## Updated Science Ladder

```
... → Sacrificial Ember Architecture ✅ → Firmware Boundary Pivot ✅ → NOP Dispatch (pure Rust DRM) ✅
→ Full compute dispatch via DRM → AMD EXEC masking → 16⁴+ dynamical production on sovereign pipeline
```

## Primal Evolution Summary (What Each Primal Contributed)

### coralReef (sovereign GPU driver)
- **coral-driver**: DRM ioctl wrappers (new UAPI: VM_INIT, VM_BIND, EXEC), `PmuInterface`, `FalconProbe`, `MappedBar`, GEM management
- **coral-ember**: Survivability hardening (fork isolation, FdVault, warm cycle), multi-ember fleet architecture
- **coral-glowplug**: Fleet orchestrator, standby pool, fault-informed resurrection

### barraCuda (GPU compute library)
- 870 tests, 99 WGSL shaders, 139 binaries
- DF64 precision tier validated (3.24 TFLOPS, 14 digits)
- Absorption cycle: hotSpring writes extensions → barraCuda absorbs → hotSpring leans on upstream

### toadStool (hardware abstraction)
- `shader.dispatch` orchestration (S168)
- f64 precision pipeline fixes (Sprint 23)
- Pattern alignment: `FirmwareInventory::probe()` ↔ `FalconProbe::discover()`

## What Springs Should Know

1. **nouveau DRM path is green on Titan V** — NOP dispatch proven, full compute pipeline exists in coral-driver
2. **PMU mailbox protocol** is register-based on GV100, queue-based on Turing+ — `PmuInterface` abstracts this
3. **HBM2 training** survives nouveau warm-cycle with `reset_method` clear — no VM needed for warm state
4. **The firmware boundary pattern scales**: Kepler (direct) → Volta (PMU mailbox) → Turing+ (GSP RPC)
5. **163 experiments** now in the fossil record — full validation table in `EXPERIMENT_INDEX.md`

## Documents Updated

| Document | What Changed |
|----------|-------------|
| `hotSpring/README.md` | Status section, science ladder updated |
| `hotSpring/EXPERIMENT_INDEX.md` | Experiments 144-163 added |
| `hotSpring/experiments/163_FIRMWARE_BOUNDARY.md` | NOP dispatch results, PmuInterface, updated paths forward |
| `hotSpring/whitePaper/baseCamp/sovereign_gpu_compute.md` | Phase 18 (firmware boundary), updated pipeline status table |
| `ecoPrimals/infra/whitePaper/gen3/baseCamp/14_sovereign_compute_hardware.md` | April 7 firmware boundary section |
