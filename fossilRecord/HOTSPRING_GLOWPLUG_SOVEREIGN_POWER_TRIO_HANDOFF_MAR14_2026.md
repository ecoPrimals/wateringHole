# hotSpring — GPU Glow Plug & Sovereign Power Management Trio Handoff

**Source**: hotSpring VFIO glow plug experiments on biomeGate (March 14, 2026)
**Target**: toadStool, barraCuda, coralReef — all three primals
**Hardware**: 2× Titan V (GV100, SM70) + RTX 5060 on `vfio-pci` / `nouveau` / `nvidia`
**coralReef**: Phase 10, Iteration 44+, `coral-driver` crate with `--features vfio`
**Builds on**: `TOADSTOOL_BARRACUDA_VFIO_PBDMA_ABSORPTION_HANDOFF_MAR14_2026.md`
**Chat**: [Glow plug to sovereign PMU](28732f32-750e-4053-a1ae-a8d39a738d7a)

---

## Executive Summary

We discovered that the GPU actively manages its own power state — like a
diesel engine that needs a glow plug before starting. After unbinding any
driver, the GPU enters a two-layer power-down:

1. **PCIe D3hot** — Linux runtime PM suspends the device (BAR0 → `0xFFFFFFFF`)
2. **Internal clock gating** — GPU's PMU gates engine clock domains within
   seconds (`PMC_ENABLE` → `0x40000020`, PFIFO → `0xBAD0DA00`)

We built a Rust self-warming system ("glow plug") that writes `PMC_ENABLE`
from userspace via BAR0 MMIO, enabling all engine clock domains in ~50ms.
**This eliminates the dependency on nouveau for GPU warming** and gives
cleaner PFIFO state than inheriting nouveau's warm state (37→35 faults in
diagnostic matrix).

**Key fact**: Desktop Volta has **no PMU firmware**. NVIDIA doesn't ship it.
nouveau uses a stub. All power management is pure BAR0 register writes —
ideal for a sovereign Rust implementation.

---

## Discovery 1: D3hot Sleep (PCIe Layer)

When `vfio-pci` binds to a GPU and `power/control=auto` (default), Linux
runtime PM puts the device in D3hot sleep if no process holds the device
open. BAR0 returns `0xFFFFFFFF` everywhere — the GPU is off.

**Fix (scripts)**: `echo on > /sys/bus/pci/devices/<BDF>/power/control`

**Fix (Rust)**: Detect `0xFFFFFFFF` on BAR0 read → error with guidance.
Hold VFIO device open to prevent sleep.

| Register | D3hot | D0 (cold) | D0 (warm) |
|----------|-------|-----------|-----------|
| BOOT0 | 0xFFFFFFFF | 0x140000a1 | 0x140000a1 |
| PMC_ENABLE | 0xFFFFFFFF | 0x40000020 | 0x5fecdff1 |
| PFIFO | 0xFFFFFFFF | 0xBAD0DA00 | 0x00000000 |

---

## Discovery 2: Internal Clock Gating (Engine Layer)

Even in PCIe D0, the GPU gates its own engine clock domains within seconds.
`PMC_ENABLE` reverts from `0x5fecdff1` (all engines on) to `0x40000020`
(minimal — just PMC + PTIMER). PFIFO reads `0xBAD0DA00` when gated.

**Fix (Rust)**: Write `0xFFFFFFFF` to `PMC_ENABLE` (offset `0x000200`).
Hardware masks to supported engines, readback shows `0x5fecdff1`. Wait 50ms
for clock stabilization. If PFIFO still returns `0xBAD0DA00`, toggle
`PFIFO_ENABLE` (offset `0x002200`) 0→1.

**Implemented in**: `coralReef/crates/coral-driver/src/vfio/channel.rs`
— both `init_pfifo_engine()` and `diagnostic_matrix()`.

---

## Discovery 3: Cold Start is Cleaner Than Warm

Starting from a cold GPU and self-warming via `PMC_ENABLE` produces fewer
PFIFO faults than inheriting nouveau's warm state:

| Metric | Nouveau-warmed | Self-warmed (cold start) |
|--------|---------------|------------------------|
| Total faults | 37 | 35 |
| Experiment M | FAULT (PCCSR=0x15000001) | ok (PCCSR=0x00000001) |
| Stale channels | Yes (nouveau residue) | No (clean PFIFO) |

**Insight**: nouveau leaves stale channel contexts, scheduler state, and
interrupt masks. Cold start + self-warm gives a pristine PFIFO with no
history. This is the correct approach for sovereign GPU control.

---

## Discovery 4: Sub-Unit Level Clock Gating (SLCG)

Probed both GPUs simultaneously — oracle (nouveau) and VFIO target (cold):

| Register | Oracle | VFIO (cold) | Meaning |
|----------|--------|-------------|---------|
| PBUS_EXT_CG (0x1C00) | 0x00000000 | 0x00000000 | Bus-level CG disabled |
| PBUS_EXT_CG1 (0x1C04) | 0x000003FE | 0x000003FE | All 9 SLCG sub-units on |
| GPU_TEMP (0x20460) | ~46°C | ~38°C | 8°C delta for warm vs cold |

**Key finding**: Nouveau does NOT use bus-level idle clock gating. It relies
entirely on sub-unit level gating (SLCG), which is a hardware default that
persists across power states. The bus-level CG registers (IDLE_CG_EN,
STALL_CG_EN) are all zero — untapped headroom for lower idle power.

---

## Power State Model for coralReef

Five states from hottest to coldest:

| State | PMC_ENABLE | PFIFO | PCIe | Est. Power | Wake Latency |
|-------|------------|-------|------|------------|--------------|
| **Sovereign** | 0x5fecdff1 | Channels loaded | D0 | ~25W idle | < 1ms |
| **Warm** | 0x5fecdff1 | Enabled, no channels | D0 | ~20W | ~5ms |
| **Glow** | 0x40000020 | Gated | D0 | ~10W | ~50ms |
| **Sleep** | 0x40000020 | Gated | D3hot | ~3W | ~100ms |
| **Off** | — | — | Powered off | 0W | Seconds |

Standard drivers sit at **Warm + SLCG**. A headless compute GPU can go lower.

---

## Work Items for Each Primal

### toadStool — GPU Power Management Layer

**Priority: P0 — this is toadStool's core domain.**

1. **Absorb the glow plug into `nvpmu`**: The self-warming code in
   `channel.rs` should evolve into toadStool's `GpuPowerController`. The
   register writes are simple, but the state machine matters.

2. **Implement `PowerManager`**:
   ```
   PowerManager {
       set_profile(Sovereign | Warm | Glow | Sleep | Eco | Custom)
       current_state() -> PowerState  // read PMC/PCI/PFIFO, classify
       warm()     // Glow → Warm: write PMC_ENABLE
       cool()     // Warm → Glow: gate selective engines
       sleep()    // Glow → Sleep: D3hot transition
       wake()     // Sleep → Glow: D0 via PCI config
   }
   ```

3. **Implement `PowerPolicy`** for autonomous behavior:
   - `OnDemand`: Sleep when idle, warm on dispatch (edge/batch)
   - `AlwaysWarm`: Engines clocked, SLCG for sub-units (cloud/inference)
   - `AlwaysSovereign`: Channels pre-loaded, instant dispatch
   - `Eco`: Aggressive gating, minimum idle power
   - `Custom(config)`: User-defined register values

4. **Explore bus-level clock gating** (`NV_PBUS_EXT_CG` at 0x1C00):
   - `IDLE_CG_EN` (bit 6): Auto-gate after `IDLE_CG_DLY_CNT` cycles
   - `STALL_CG_EN` (bit 14): Gate during stalls
   - `WAKEUP_DLY_CNT` (bits 19:16): Wake latency
   - Nouveau leaves these at zero — room for power savings

5. **Temperature monitoring**: GPU_TEMP at `0x020460`, bits [15:8] ≈ °C.
   Oracle reads ~46°C warm-idle, ~38°C cold. 8°C delta from clock gating.

### coralReef — Channel Lifecycle Integration

**Priority: P0 — glow plug is already here, needs clean integration.**

1. **Extract self-warming from `diagnostic_matrix()`** into a reusable
   `fn glow_plug(bar0: &MappedBar)` that can be called before any
   channel operation. Currently inline in two places.

2. **Integrate with toadStool's PowerManager** (when available) — check
   power state via IPC before channel creation, request warm-up if needed.

3. **Channel teardown**: When channels are no longer needed, notify
   toadStool that the GPU can transition to Glow or Sleep.

4. **`init_pfifo_engine()` is the prototype** for toadStool's PFIFO init.
   It should eventually call toadStool's PowerManager rather than doing
   PMC_ENABLE writes directly.

### barraCuda — Dispatch Latency Awareness

**Priority: P1 — no code changes yet, but design awareness needed.**

1. **Dispatch pre-warm hint**: When barraCuda knows a dispatch is coming
   (e.g., MD timestep about to begin), it can signal coralReef/toadStool
   to pre-warm the GPU. This hides the 50ms wake latency behind CPU work.

2. **Batch vs stream**: For batch workloads (many dispatches in a row),
   request `AlwaysWarm` or `AlwaysSovereign`. For one-shot dispatches,
   accept `OnDemand` latency.

3. **Power-aware scheduling**: In multi-GPU configurations, prefer
   dispatching to an already-warm GPU over waking a sleeping one.

---

## Scripts Updated

| Script | Change |
|--------|--------|
| `rebind_titanv_vfio.sh` | Adds `echo on > power/control` + `reset_method` disable |
| `setup_dual_titanv.sh` | Adds D3hot prevention for VFIO target |
| `warm_and_test.sh` | New "self" mode (default): no nouveau, Rust self-warms. "nouveau" mode preserved as legacy |

---

## Key Source Files

| File | What's New |
|------|-----------|
| `coralReef/crates/coral-driver/src/vfio/channel.rs` | Glow plug in `diagnostic_matrix()` and `init_pfifo_engine()` |
| `hotSpring/experiments/058_VFIO_PBDMA_CONTEXT_LOAD.md` | Glow plug discovery section |
| `hotSpring/experiments/059_CORALREEF_GPU_POWER_MANAGEMENT_DESIGN.md` | Full power management system design |
| `hotSpring/scripts/warm_and_test.sh` | Self-warm mode (no nouveau dependency) |
| `hotSpring/scripts/setup_dual_titanv.sh` | D3hot prevention |

---

## Register Quick Reference (Power Management)

| Register | Offset | Read (warm) | Read (cold) | Write |
|----------|--------|------------|-------------|-------|
| PMC_ENABLE | 0x000200 | 0x5fecdff1 | 0x40000020 | 0xFFFFFFFF (enable all) |
| PMC_DEV_ENABLE | 0x000204 | 0x00003fff | 0x00003fff | — |
| PFIFO_ENABLE | 0x002200 | 0x00000000 | 0xBAD0DA00 | 0→1 toggle to init |
| PBUS_EXT_CG | 0x001C00 | 0x00000000 | 0x00000000 | TBD (Phase 2) |
| PBUS_EXT_CG1 | 0x001C04 | 0x000003FE | 0x000003FE | SLCG per-subunit |
| GPU_TEMP | 0x020460 | ~46°C | ~38°C | Read-only |
| PCI PM CTRL | Config 0x64 | bits[1:0]=00 (D0) | bits[1:0]=11 (D3) | 0x00 for D0 |

---

*March 14, 2026 — The GPU warms itself. No driver dependency. Pure Rust sovereignty.*
