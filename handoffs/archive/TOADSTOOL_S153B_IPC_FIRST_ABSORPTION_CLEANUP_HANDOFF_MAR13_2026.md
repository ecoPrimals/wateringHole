# toadStool S153b — IPC-First Absorption + Doc Cleanup

**Date**: March 13, 2026
**Session**: S153b
**Pins**: hotSpring v0.6.31, coralReef Iteration 43, barraCuda v0.35 (IPC-first)

---

## Summary

Absorbed two significant cross-primal evolutions into toadStool documentation:

1. **barraCuda v0.35 IPC-first** — barraCuda removed all compile-time primal
   dependencies (`coral-gpu` optional dep, `VfioGpuInfo`, `from_vfio_device`,
   `discover_vfio_gpus`). All inter-primal communication is now JSON-RPC 2.0
   at runtime. toadStool is the sole VFIO detection source.

2. **coralReef Iteration 43** — PFIFO hardware channel creation via BAR0 MMIO
   (instance block, V2 MMU page tables, runlist, PCCSR bind/enable). RAMUSERD
   offsets corrected. The critical VFIO dispatch blocker is closed.

---

## Changes

### Doc Updates

- `SOVEREIGN_COMPUTE_GAPS.md` — Architecture diagram updated to IPC-first pipeline.
  Removed stale `from_vfio_device` references. coralReef pinned to Iteration 43.
  Added `ecoprimals-mode` CLI to S152 resolution table.

- `SOVEREIGN_COMPUTE.md` — Note updated for IPC-first architecture and coralReef
  Iteration 43. Footer updated to S153.

- `README.md` — Pin updated: coralReef Iteration 43, barraCuda v0.35 IPC-first.
  Session bumped to S153.

- `SPRING_ABSORPTION_TRACKER.md` — Stale `coral-gpu` reference updated to
  JSON-RPC IPC.

### Debris Audit

- Zero TODO/FIXME/HACK in Rust code (confirmed)
- Zero date-stamped files remaining in ecoPrimals root (JAN29 files archived to fossil/ in prior session)
- All scripts in `scripts/` still valid
- No stale checkboxes identified

---

## Current Pipeline Status

```
barraCuda (806 WGSL shaders, PrecisionBrain routing)
  → [JSON-RPC] coralReef (WGSL → SASS/GFX, PFIFO channel init)
    → [JSON-RPC] toadStool (VFIO detection, dispatch routing, hardware lifecycle)
      → GPU hardware (VFIO BAR0 + DMA + GPFIFO)
```

| Component | Status |
|-----------|--------|
| barraCuda `CoralReefDevice` IPC client | Scaffold done, IPC wiring pending |
| coralReef PFIFO channel | Implemented, hardware validation pending |
| toadStool `compute.dispatch.submit` | Ready (S152) |
| toadStool `compute.hardware.vfio_devices` | Ready (S153) |
| toadStool `ecoprimals-mode` CLI | Ready (S153) |
| E2E sovereign dispatch | Pending hardware validation on Titan V |

---

## Test Status

20,262+ tests passing, 0 failures. 96+ JSON-RPC methods. ~150K production lines.
