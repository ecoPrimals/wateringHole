# hotSpring → Ecosystem Handoff: Primal Evolution Through GPU Cracking

**Date:** 2026-03-25
**From:** hotSpring (biomeGate)
**To:** Primal teams (coralReef, toadStool, barraCuda), Spring teams (all)
**Context:** 104 experiments, 10.5/11 sovereign pipeline layers

---

## How the GPU Cracking Campaign Evolved Each Primal

### coralReef (Sovereign Shader Compiler)

**Before hotSpring GPU cracking:** Basic VFIO binding, partial DRM dispatch.

**After 104 experiments, coralReef gained:**

| Component | What Was Built | Experiments |
|-----------|---------------|-------------|
| `coral-glowplug` | PCIe lifecycle daemon, personality system, hot-swap, health monitor, socket API, systemd service, IOMMU group handling, DRM isolation | Exp 063-065, 069 |
| `coral-ember` | Immortal VFIO fd holder, SCM_RIGHTS passing, atomic swap_device RPC, swap observation journal | Exp 074 |
| `coral-driver::nv::vfio_compute` | Full VFIO compute pipeline: PFIFO init, channel creation, PBDMA context, MMU fault buffer, falcon binding (B1-B7), WPR/ACR construction (W1-W7), sysmem DMA strategy, instance block builder, page table construction (PDE slot fix) | Exp 058-104 |
| `strategy_sysmem.rs` | The primary ACR boot strategy — allocates DMA buffers, builds 5-level page table chain, populates WPR/ACR payload, manages VRAM mirrors, starts SEC2 | Exp 095-104 |
| `FalconCapabilityProbe` | Runtime bit solver for register layouts across GPU generations | Exp 091 |
| `Sec2Queues` / `Sec2Bridge` | SEC2 queue protocol for CMDQ/MSGQ communication | Exp 097 |
| Diagnostic infrastructure | `sec2_exit_diagnostics()`, `sec2_tracepc_dump()`, IMEM/DMEM reads, FBHUB probe, WPR2 probe, Falcon IRQ decode | Exp 096-104 |

**What coralReef should absorb:**
1. The PDE slot fix pattern — apply to any future page table construction
2. The IOMMU catch-all buffer pattern (LOW_CATCH + HIGH_CATCH) — standard for VFIO DMA
3. The Falcon IMEM read fix (byte addressing for v5+, not block addressing)
4. Gap 13 swap safety debt — atomic rollback on failed bind

### toadStool (Sovereign Compute Hardware Discovery)

**How hotSpring informs toadStool:**
- The experiment loop / personality sweep infrastructure (`AdaptiveLifecycle`, `Journal`, `SwapObservation`) is a pattern toadStool can generalize for hardware characterization across all GPU vendors
- The register map infrastructure (`RegisterMap` trait, GV100 + GFX906 maps) should be toadStool-owned for the hardware performance surface
- Silicon science (Exp 096) directly connects: TMU table lookup mapping to QCD operations is a toadStool performance surface entry

### barraCuda (Math Engine)

**How hotSpring informs barraCuda:**
- Silicon science validated that AMD DF64 is 38% faster than NVIDIA DF64 for the same arithmetic
- The precision tier model (f32/df64/f64) maps to concrete hardware via `DeviceCapabilities` — barraCuda's dispatch logic should leverage this
- Strandgate's `validate_silicon_science`, `validate_silicon_capabilities`, `validate_precision_matrix`, `validate_sovereign_roundtrip` binaries are the production face of this work

## How the Springs Should Leverage This

### For All Springs

The sovereign pipeline (when complete) provides:
1. **Zero vendor dependency** for GPU compute — no CUDA, no ROCm, no Vulkan driver
2. **Any GPU vendor** via the same Rust API (`ComputeDevice` trait)
3. **DF64 precision** on consumer hardware at 9.9× native f64 throughput
4. **DRM dispatch today** (AMD fully validated, NVIDIA Blackwell cracked)
5. **Sovereign VFIO dispatch tomorrow** (10.5/11 layers, HS authentication pending)

### Specific Spring Guidance

| Spring | What to Absorb | Priority |
|--------|---------------|----------|
| **wetSpring** | DRM dispatch for metagenomics GPU offload. DF64 pairwise distance shaders already shared via barraCuda | When DRM dispatch stabilizes |
| **neuralSpring** | GPU Lanczos + SpMV already validated in hotSpring. The sovereign path enables spectral analysis without vendor SDK | When VFIO pipeline completes |
| **airSpring** | NPU + GPU heterogeneous compute pipeline proven in hotSpring (Exp 020-031). PDE ecology simulations on GPU | Already started |
| **groundSpring** | GPU observables pipeline (DSF, RDF, SSF, VACF) validated. Transfer to groundSpring measurement analysis | When needed |
| **healthSpring** | f64 precision guarantees matter for PK/PD simulations. The three-tier model applies directly | Informational |
| **ludoSpring** | Shader compilation via coral-reef. Game shaders can use same WGSL→native pipeline | When DRM dispatch stabilizes |

## Primal Dependency Graph (Current State)

```
barraCuda (math) ──→ toadStool (hardware) ──→ coralReef (driver)
    ↕                       ↕                        ↕
hotSpring (physics) ←──── Experiments ──────→ wateringHole (handoffs)
    ↕                                               ↕
All Springs (science) ←─────────────────── baseCamp (docs)
```

## Key Architectural Lessons from 104 Experiments

1. **Conversation, not command:** The GPU is a complex system with multiple
   microcontrollers (falcons). Treating it as a conversation partner (listen,
   probe, respond) rather than a command target produced better diagnostics.

2. **GlowPlug as mailbox:** The PCIe lifecycle daemon is the right abstraction
   for GPU personality management. Hot-swap between drivers in 1.5-6s.

3. **Ember as immortal state:** Holding VFIO fds open across driver swaps
   eliminates the entire class of "lost device" errors. The SCM_RIGHTS
   pattern is the foundation.

4. **Page tables are the interface:** The MMU page table format is the critical
   interface between host software and GPU hardware. Getting the PDE format
   wrong (wrong 8-byte slot in 16-byte entries) caused 6 experiments of
   misdirected debugging. The reference implementation matters.

5. **DRM dispatch is the parallel track:** While sovereign VFIO is the
   endgame, DRM dispatch through kernel drivers provides immediate access
   to compute. AMD GCN5 is fully validated (6/6 including f64 LJ force).
   NVIDIA RTX 5060 Blackwell is cracked. This is usable today.

## Strandgate Team Contributions (Pulled March 25)

The strandgate team contributed while we focused on GPU cracking:
- `validate_silicon_science.rs` — TMU/silicon unit mapping validation
- `validate_silicon_capabilities.rs` — hardware capability profiling
- `validate_precision_matrix.rs` — precision tier validation matrix
- `validate_sovereign_roundtrip.rs` — end-to-end sovereign pipeline test
- `toadstool_report.rs` — toadStool report generation module
- Exp 096: Silicon Science TMU QCD Mapping
- baseCamp `silicon_science.md`
- barracuda CHANGELOG, device_pair, gpu improvements

## Action Items

| Team | Action | Priority |
|------|--------|----------|
| coralReef | Absorb PDE slot fix pattern, add to page table construction docs | HIGH |
| coralReef | Implement Gap 13 swap safety (atomic rollback) | HIGH |
| toadStool | Absorb RegisterMap trait + silicon science TMU mapping | MEDIUM |
| barraCuda | Absorb DeviceCapabilities DF64 routing based on silicon science | MEDIUM |
| All springs | Review DRM dispatch path for immediate GPU access | LOW (informational) |
| Strandgate | Continue DRM passthrough validation for RTX 3090, RX 6950 XT | ONGOING |
