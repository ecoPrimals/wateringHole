# coralReef Evolution Roadmap — All Remaining Work

**From:** hotSpring (Experiment Lab)
**To:** coralReef Team
**Date:** 2026-03-24 (post Iter 64)
**Purpose:** Single source of truth for all outstanding evolution work

This document consolidates every outstanding item from 15 archived handoffs plus
new architecture requirements. The two companion handoffs contain implementation
specs for their respective features:

- `CORALREEF_TRACE_INTEGRATION_HANDOFF.md` — trace.rs module, VendorLifecycle extension
- `CORALREEF_OPEN_TARGET_REAGENT_HANDOFF.md` — open targets, Custom personality, trace-as-default

---

## Priority 1: Hardware Abstraction Traits (Testability)

Iter 64 delivered `SysfsOps` + `MockSysfs` — a major step. The same pattern should
extend to the remaining hardware-coupled interfaces. CoralReef's own WHATS_NEXT.md
identifies these; hotSpring confirms they are critical for experiment tractability.

### 1a. `BarOps` Trait — Abstract `MappedBar`

**Why:** `MappedBar` in `coral-driver` is a concrete struct coupled to BAR0 MMIO.
Components like `acr_boot/strategy_*`, `diagnostics.rs`, and `mmu_oracle` call
`bar.read_u32()` / `bar.write_u32()` directly. This makes them untestable without
live GPU hardware (~19K untestable lines).

**Pattern (matches SysfsOps):**

```rust
pub trait BarOps: Send + Sync {
    fn read_u32(&self, offset: u32) -> Result<u32, DriverError>;
    fn write_u32(&self, offset: u32, value: u32) -> Result<(), DriverError>;
    fn read_range(&self, offset: u32, len: usize) -> Result<Vec<u8>, DriverError>;
}

pub struct MockBar {
    registers: HashMap<u32, u32>,
    read_log: Vec<u32>,
    write_log: Vec<(u32, u32)>,
}
```

**Scope:** `acr_boot/`, `diagnostics.rs`, `mmu_oracle/`, `nv_metal.rs`, any module
that takes `&MappedBar`. Replace concrete `MappedBar` params with `&dyn BarOps`.

**Benefit:** ACR boot strategies become unit-testable. We can inject known register
states and verify the solver's decisions without hardware.

### 1b. `VfioOps` Trait — Abstract VFIO Device Interactions

**Why:** VFIO open/close/DMA is tied to kernel VFIO ioctls. Abstracting behind a
trait enables testing DMA mapping logic, channel construction, and page table setup
without a VFIO device.

```rust
pub trait VfioOps: Send + Sync {
    fn dma_map(&self, iova: u64, size: usize) -> Result<DmaMapping, DriverError>;
    fn dma_unmap(&self, iova: u64, size: usize) -> Result<(), DriverError>;
    fn irq_set(&self, index: u32, fd: RawFd) -> Result<(), DriverError>;
}
```

### 1c. `DmaOps` Trait — Abstract DMA Buffer Allocation

**Why:** `DmaBuffer` allocates system memory and registers it with IOMMU. Abstracting
this lets us test page table construction with deterministic addresses.

```rust
pub trait DmaOps: Send + Sync {
    fn alloc(&self, size: usize) -> Result<DmaBuffer, DriverError>;
    fn write(&self, buf: &DmaBuffer, offset: usize, data: &[u8]) -> Result<(), DriverError>;
    fn read(&self, buf: &DmaBuffer, offset: usize, len: usize) -> Result<Vec<u8>, DriverError>;
}
```

**Order:** BarOps first (highest ROI — unlocks ACR solver testing), then VfioOps,
then DmaOps.

---

## Priority 2: Native Trace Integration

**Full spec:** `CORALREEF_TRACE_INTEGRATION_HANDOFF.md`

### Summary

Ember already runs as root with `CAP_SYS_ADMIN`. mmiotrace should be a built-in
swap lifecycle capability, not an external script.

- **Phase 1:** New `crates/coral-ember/src/trace.rs` module
- **Phase 2:** `VendorLifecycle::trace_filter_ranges()` trait extension
- **Phase 3:** Wire into `handle_swap_device` (enable before bind, capture after)
- **Phase 4:** IPC propagation (ember.swap + device.swap accept `trace` param)
- **Phase 5:** coralctl CLI (`--trace` flag, `trace-status`, `trace-list` subcommands)
- **Phase 6:** `nvidia_oracle` as a known driver target

### Why This Matters for GPU Cracking

Every driver swap becomes a permanent learning record. The ACR boot solver (Gap 1)
needs mmiotrace data from both nouveau and nvidia to resolve the `bind_stat` blocker.
Without native trace, we cannot systematically capture the initialization sequences
needed to crack the ACR chain.

---

## Priority 3: Open Target Acceptance + Reagent Model

**Full spec:** `CORALREEF_OPEN_TARGET_REAGENT_HANDOFF.md`

### Summary

- **Phase 1:** Replace `KNOWN_TARGETS` hard rejection with open acceptance + validation
- **Phase 2:** Add `Personality::Custom` variant for unknown drivers
- **Phase 3:** Invert trace default to on (configurable via `glowplug.toml`)

### Architecture Reference

`hotSpring/specs/UNIVERSAL_DRIVER_REAGENT_ARCHITECTURE.md` — defines the full
reagent safety taxonomy (Protected, Shared, Managed, Native-Compute).

---

## Priority 4: ACR Boot Solver — Layer 7/8 Continuation

### ROOT CAUSE LIKELY FOUND (Exp 083, hotSpring)

hotSpring Exp 083 (nouveau source analysis) discovered **four bugs** in the
ACR boot strategies that likely explain why `bind_stat` never reaches 5:

| # | Bug | Fix | File |
|---|-----|-----|------|
| **B1** | `SEC2_FLCN_BIND_INST = 0x668` — **wrong register** | Change to `0x054` (nouveau: `gm200_flcn_bind_inst`) | `instance_block.rs` |
| **B2** | Bind value missing bit 30 | Add `(1 << 30)` to value: `(1<<30) \| (target<<28) \| (addr>>12)` | All strategies |
| **B3** | `strategy_chain.rs` uses target=3 ("COH") | Change to 2 — 3 is NCOH, 2 is coherent HOST | `strategy_chain.rs` |
| **B4** | No DMAIDX clear before bind | Add `mask(0x604, 0x07, 0x00)` before bind write | All strategies |

**Evidence:** Upstream nouveau `nvkm/falcon/gm200.c`:

```c
// gm200_flcn_bind_inst — this is what GV100 SEC2 uses
nvkm_falcon_mask(falcon, 0x604, 0x00000007, 0x00000000);  // B4: clear DMAIDX
nvkm_falcon_wr32(falcon, 0x054,                            // B1: offset 0x054
    (1 << 30) | (target << 28) | (addr >> 12));            // B2: bit 30
// target: 0=VRAM, 2=HOST(coherent), 3=NCOH                // B3: 2 not 3
```

**B1 alone could explain everything:** If `0x668` is not the bind register,
the falcon never sees the instance block pointer, so `bind_stat` never advances.

### Recommended Fix Sequence

1. Change `SEC2_FLCN_BIND_INST` from `0x668` to `0x054` in `instance_block.rs`
2. Update bind value construction in all strategies to include `(1 << 30)`
3. Add `bar0.write_u32(base + 0x604, r(0x604) & !0x07)` before bind in all strategies
4. Fix `strategy_chain.rs` `SYS_MEM_COH_TARGET` from 3 to 2
5. Retry ACR boot — if bind_stat reaches 5, the HS bootloader should DMA ACR firmware

### Remaining Steps (after bind fix)

1. **Once SEC2 boots BL:** construct WPR with FECS/GPCCS LS images
2. **Warm handoff path:** capture Nouveau's FECS state via Ember swap
3. **Capture mmiotrace** for nvidia full ACR init (for WPR layout)

### Cross-Reference

- **Exp 083** (hotSpring): Full source analysis with confidence ratings
- **Exp 082**: PTE encoding confirmed, fault buffer register name discrepancy
- **Gap 2 RESOLVED**: SYS_MEM_COH_TARGET = 2 (coherent), not 3

---

## Priority 5: Remaining Infrastructure

### 5a. nvidia_oracle Module Build + Test

Build script: `hotSpring/scripts/build_nvidia_oracle.sh`
- Patches `MODULE_BASE_NAME` and `NV_MAJOR_DEVICE_NUMBER` in NVIDIA open kernel source
- Produces `nvidia_oracle.ko` that coexists with system `nvidia.ko`
- Enables nvidia mmiotrace captures without affecting RTX 5060

**Action:** `sudo ./scripts/build_nvidia_oracle.sh 580.126.18` after trace integration
is complete, then `coralctl swap 0000:03:00.0 nvidia_oracle --trace`.

### 5b. UVM Hardware Validation

RTX 5060 UVM dispatch pipeline is code-complete but needs on-site hardware validation.
`NvUvmComputeDevice` + GPFIFO submission + USERD doorbell + completion polling are all
implemented. Needs a `coralctl dispatch` test cycle on live hardware.

### 5c. RDNA Validation

`AmdRdnaLifecycle` uses conservative Vega 20 defaults. Test on actual RX 5000/6000/7000
hardware to determine if RDNA's FLR support changes the lifecycle picture.

### 5d. SM32 Encoder `frnd.f32`

Kepler codegen triggers ICE on float rounding instructions. Add `FRND` to SM32 encoder
instruction table.

### 5e. VendorProfile Convergence

`RegisterMap` (barraCuda) and `VendorLifecycle` (coral-ember) both dispatch from PCI
vendor IDs. Candidate for unified `VendorProfile` trait in the triangle architecture.

---

## Priority 6: Coverage + Quality

### Test Coverage Target

| Metric | Current (Iter 64) | Target |
|--------|-------------------|--------|
| Line coverage | 65.9% | 90% |
| Non-hardware coverage | 81.5% | 90% |
| Function coverage | 73.7% | 90% |
| Untestable lines | ~19,009 | Reduce via BarOps/VfioOps/DmaOps |

BarOps trait (Priority 1a) is the highest-leverage item for coverage — it converts
~19K untestable hardware lines into mockable test surface.

### Doc Warnings

2 pre-existing intra-doc links: `DmaBuffer`, `VfioDevice::from_received`.

---

## Priority 7: Late-Stage Architecture (Future)

### Native-Compute Mode

**Spec:** `hotSpring/specs/NATIVE_COMPUTE_ROADMAP.md`

Borrow spare compute from gaming GPUs without unbinding their DRM driver. API-level
interaction (CUDA/Vulkan compute queues) rather than VFIO displacement. Prevents the
"broke the 5060" scenario from early experiments.

### Sovereign HBM2 Training

Eliminate nouveau dependency for HBM2 initialization via coral-driver typestate machine.

### Custom PMU Falcon Firmware

Replace vendor firmware dependency with Rust-implemented PMU microcode for GV100.

### Devinit via VBIOS

VBIOS boot script execution from Rust for cold-start GPU initialization.

---

## Archived Handoff Summary

109 handoffs in `archive/`. Key absorbed items from this cleanup:

| Archived Handoff | Key Items Absorbed |
|------------------|--------------------|
| EMBER_DRM_ISOLATION (Mar 19) | `drm_isolation.rs`, `verify_drm_isolation` |
| IOMMUFD_EMBER_EVOLUTION (Mar 22) | Dual-path VfioDevice, iommufd/cdev backend |
| GCN5_COMPLETE_PRESWAP (Mar 2026) | GCN5 f64 backend, 6/6 preswap validated |
| PRE_PMU_HARDENING (Mar 23) | BOOT0 auto-detect, PfifoInitConfig, FLR |
| EMBER_HARDENING (Mar 22) | VRAM canary, BDF allowlist, preflight checks |
| EMBER_WATCHDOG_SWAP (Mar 22) | D-state resilient sysfs, IOMMU peer release |
| DEEP_DEBT_CROSS_VENDOR (Mar 2026) | BusyGuard, oracle BAR0, pkexec-free pipeline |
| DRM_TRIO_PIPELINE (Mar 22) | GCN5 E2E, RTX 5060 Blackwell cracked |
| TRIO_EVOLUTION_AMD_AKIDA (Mar 20) | VendorLifecycle, AMD D3cold, Akida NPU |
| VENDOR_AGNOSTIC_GLOWPLUG (Mar 18) | SysfsOps, coral-ember split, typed errors |
| REGISTER_MAPS_ABSORPTION (Mar 18) | Register maps expanded in coral-driver |
| BOOT_PERSISTENCE (Mar 16) | systemd service, VFIO-first boot |
| PFIFO_MMU_DISPATCH (Mar 21) | PFIFO hardening, fault buffer diagnosis |
| SOVEREIGN_FALCON_DIRECT (Mar 16) | Falcon register maps, D3→D0 clean state |
| LAYER7_ACR_BOOT_SOLVER (Mar 23) | File splits (all 5 done in Iter 64) |

---

## Quick Reference: What's Where

| Need | Go To |
|------|-------|
| Trace implementation spec | `CORALREEF_TRACE_INTEGRATION_HANDOFF.md` |
| Open target / reagent spec | `CORALREEF_OPEN_TARGET_REAGENT_HANDOFF.md` |
| Reagent safety architecture | `hotSpring/specs/UNIVERSAL_DRIVER_REAGENT_ARCHITECTURE.md` |
| Driver-as-software pattern | `hotSpring/specs/DRIVER_AS_SOFTWARE.md` |
| GPU cracking gap tracker | `hotSpring/specs/GPU_CRACKING_GAP_TRACKER.md` |
| Native-compute roadmap | `hotSpring/specs/NATIVE_COMPUTE_ROADMAP.md` |
| Data inventory | `hotSpring/data/INVENTORY.md` |
| nvidia_oracle build script | `hotSpring/scripts/build_nvidia_oracle.sh` |
| Snapshot comparison tool | `hotSpring/scripts/compare_snapshots.py` |
| Archived handoffs (fossil record) | `hotSpring/wateringHole/handoffs/archive/` (112 documents) |
