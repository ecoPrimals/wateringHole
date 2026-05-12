# coralReef Handoff: Firmware Boundary Pivot + NOP Dispatch (April 7, 2026)

**From:** hotSpring (Exp 159-163)
**To:** coralReef team, toadStool team, spring teams
**Status:** Complete — NOP dispatch proven, PmuInterface created

---

## What Changed

An architectural pivot in how we approach sovereign GPU compute on NVIDIA Volta+ hardware.

### The Old Approach (retired)
Direct BAR0 MMIO control of the PFIFO scheduler, PBDMA programming, runlist submission from host userspace. This worked on Kepler (K80, no firmware security) but is fundamentally blocked on Volta+ because:
- PFIFO_ENABLE and SCHED_EN are PRI-gated by the PMU falcon
- The scheduler is firmware-controlled, not host-controlled
- ACR (Authenticated Code Region) prevents falcon restart after halt

### The New Approach (proven)
**Firmware-agnostic interfacing** — the GPU's falcon firmware (PMU, SEC2, FECS, GPCCS) is its internal operating system. We interface with it through defined protocols, not replace it. This is the same pattern toadStool uses for motherboard BIOS/UEFI.

**Three-layer delineation:**
| Layer | Owner | Examples |
|-------|-------|----------|
| **Driver** | Host CPU (what we write) | BAR0 MMIO, DMA, channel structures, firmware mailbox, DRM ioctls |
| **Firmware** | Falcon processors | PMU (PRI gates, clocks), SEC2 (ACR trust), FECS (GR scheduler) |
| **Hardware** | Silicon | PBDMAs, PFIFO, copy engines, GR, GPU MMU, HBM2 |

## What Was Proven

1. **NOP dispatch via nouveau DRM (pure Rust):** End-to-end GPU command execution on Titan V using coral-driver's Rust DRM ioctl wrappers. Pipeline: `VM_INIT → CHANNEL_ALLOC(VOLTA_COMPUTE_A) → SYNCOBJ → GEM_NEW → VM_BIND → mmap → EXEC → SYNCOBJ_WAIT`. New UAPI (kernel 6.6+). Zero C, zero libc.

2. **NOP dispatch via raw C DRM ioctls:** Validated the same pipeline in C first as proof-of-concept, then ported to Rust.

3. **Hot-handoff channel injection:** Channel 500 injected via PRAMIN alongside running nouveau. Scheduler accepted it. PBDMA loaded our RAMFC context.

4. **PMU mailbox protocol mapped:** GV100 uses register-based mailbox (MBOX0/MBOX1 + IRQSSET for signaling). Queues not available (0xBADF5040). PMU idle at PC=0x3A5D, MBOX0=0x300 (init-complete handshake).

5. **HBM2 preserved through driver swaps:** nouveau warm-cycle + `reset_method` clear on vfio-pci bind avoids FLR. HBM2 training survives.

## New Code in coralReef

| File | What |
|------|------|
| `coral-driver/examples/nvidia_nop_dispatch.rs` | Pure Rust NOP dispatch example |
| `coral-driver/examples/nouveau_nop_submit.c` | C proof-of-concept |
| `coral-driver/examples/hot_handoff_nouveau.rs` | BAR0 coexistence + channel injection |
| `coral-driver/examples/pmu_mailbox_trace.rs` | PMU/SEC2/FECS register tracer |
| `coral-driver/src/nv/vfio_compute/pmu_interface.rs` | `PmuInterface` struct |

### PmuInterface API

```rust
let pmu = PmuInterface::attach(&bar0)?;
println!("PMU state: {:?}", pmu.state());

let resp = pmu.mailbox_exchange(&bar0, cmd, Some(arg), Duration::from_millis(100))?;
println!("Response: mbox0={:#x} mbox1={:#x}", resp.mbox0, resp.mbox1);
```

Provides: `attach()`, `refresh()`, `snapshot()`, `mailbox_exchange()`, `poll_mbox0_bits()`, `probe_queues()`.

## Cross-Generation Firmware Interface Pattern

| Era | Firmware Interface | Driver Role |
|-----|-------------------|-------------|
| Kepler (K80) | None — direct register writes | Full hardware control |
| Volta (GV100) | PMU mailbox + SEC2 ACR + FECS scheduling | Firmware interface + channel structures |
| Turing/Ampere | GSP RPC — host becomes thin RPC client | RPC message formatting |
| Hopper/Blackwell | GSP with extended offloaded functionality | Even thinner RPC layer |

Learning the Volta firmware interface is the foundation for ALL modern NVIDIA cards.

## toadStool Pattern Alignment

| toadStool | GPU Equivalent |
|-----------|---------------|
| `FirmwareInventory::probe()` | `FalconProbe::discover()` |
| `RegisterAccess` trait | `MappedBar` — uniform BAR0 interface |
| `PowerManager::glow_plug()` | `PmuMailbox::enable_engines()` |
| `needs_software_pmu()` | `FalconProbe::pmu_alive()` |
| `compute_viable()` | `FalconProbe::dispatch_viable()` |

## Next Steps (for coralReef team)

1. **Full compute dispatch via DRM:** Use existing `NvDevice` infrastructure (shader upload, QMD, multi-buffer) — already proven in `nvidia_nouveau_e2e.rs`
2. **PMU command vocabulary:** Use `PmuInterface` to discover specific PMU commands (engine enable, clock control, PRI gate management)
3. **GSP RPC client:** Extend the `PmuInterface` pattern to Turing/Ampere GSP message protocol
4. **VFIO + firmware coexistence:** Investigate binding vfio-pci with nouveau-initialized firmware still alive

## For Spring Teams

The DRM path is the fastest route to sovereign GPU compute on Volta+. The VFIO path (direct BAR0 control) remains useful for Kepler and for advanced register-level diagnostics, but command submission should go through DRM ioctls. coral-driver's `nv::ioctl` module already wraps the full pipeline.
