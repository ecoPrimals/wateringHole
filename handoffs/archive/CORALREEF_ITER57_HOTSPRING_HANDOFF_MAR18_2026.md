<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef → hotSpring Handoff — VFIO Sovereign Dispatch Last Mile

**Date**: March 18, 2026
**From**: coralReef (Iteration 57)
**To**: hotSpring (Exp 070 — Twin Titan V Experiment)
**Phase**: 10 — Deep Debt Evolution + All-Silicon Pipeline

---

## Summary

coralReef's VFIO sovereign dispatch pipeline is **software-complete** but blocked
on a **hardware initialization problem**. The pipeline works end-to-end in
software — GPFIFO ring construction, USERD doorbell write, PFIFO channel
creation with V2 MMU 5-level page tables, QMD dispatch construction — but
the GPU's compute engines are cold (PFIFO/GPCCS/FECS not initialized, HBM2
untrained). This is a hardware operations task, not a software bug.

---

## What coralReef Delivered

### VFIO Dispatch Stack (Complete)
- `NvVfioComputeDevice` — full `ComputeDevice` impl via BAR0 + DMA
- GPFIFO ring with DMA-backed entries + USERD doorbell
- PFIFO channel creation: RAMFC, instance block, 5-level V2 MMU, TSG+channel runlist
- USERD_TARGET + INST_TARGET fixed (SYS_MEM_COHERENT/SYS_MEM_NCOH)
- RAMUSERD offsets corrected: GP_GET@0x88, GP_PUT@0x8C
- USERMODE doorbell at BAR0+0x810090
- H1 cache flush: `clflush_range` on GPFIFO + USERD before doorbell (proven insufficient)

### GlowPlug VFIO Broker (Complete)
- `device.lend` / `device.reclaim` JSON-RPC methods
- GlowPlug drops VFIO fd so external consumers can open the VFIO group
- Register snapshot on lend, health verification on reclaim
- 10x lend/reclaim stress cycle validated on both Titan Vs
- Double-lend rejection, reclaim-no-op safety

### Test Harness (Complete)
- `VfioLease` RAII guard — automatic lend/reclaim, transparent fallback
- 35 VFIO hardware tests passing (open, alloc, upload/readback, BAR0, PFIFO, HBM2, hot-swap)
- 9 hot-swap integration tests in `hw_hotswap.rs`
- Drop-order correctness: device drops before lease reclaims

### Quality Gates (All Passing)
- 2560 tests passing (+48 VFIO), 0 failed, 90 ignored
- Zero clippy warnings (pedantic + nursery)
- Zero fmt drift, zero doc warnings
- 59.92% line coverage

---

## The Blocker: Cold Silicon

When Titan V boots with `vfio-pci` preemption (which we need to prevent nvidia
from corrupting GV100 state), the GPU's compute engines never initialize:

```
pfifo_status = 0xbad00200   # PFIFO uninitialized
gpccs_status = 0xbadf3000   # GPCCS/GR engine not loaded
boot0 reads valid (GV100 silicon alive) but VRAM is untrained
```

PBDMA cannot process GPFIFO entries because:
1. **HBM2 is untrained** — cold VFIO bind, no prior driver init
2. **FECS firmware not loaded** — GR engine never started
3. **GPCCS not initialized** — no compute context exists

The H1 cache flush experiment (`clflush_range` + `memory_fence` before doorbell)
confirmed this is **not a CPU cache coherency issue** — it's a fundamental lack
of GPU initialization.

---

## What hotSpring Needs To Do

### Experiment 070: Twin Titan V Warm-Up

**Goal**: Warm one Titan V via `nouveau`, then re-bind to `vfio-pci`, then run dispatch.

**Hardware layout** (why the 5060 matters):
- RTX 5060 (21:00.0) — dedicated display GPU, nvidia-drm, stays running
- Titan V #1 (03:00.0) — oracle card, vfio-pci
- Titan V #2 (4a:00.0) — compute target, vfio-pci

**Sequence** (via GlowPlug JSON-RPC):
1. `device.resurrect` on one Titan V (BDF 03:00.0 or 4a:00.0)
   - Blocked today by `nvidia` module guard (RTX 5060 loads nvidia.ko)
   - **Solution**: Either `rmmod nvidia` (kills display — use TTY) or modify guard to check per-device binding rather than module presence
2. If guard cleared: nouveau binds → trains HBM2 → loads FECS → initializes GPCCS/GR
3. nouveau unbinds → vfio-pci rebinds (GlowPlug handles this)
4. Run dispatch:
   ```bash
   CORALREEF_VFIO_BDF=0000:03:00.0 CORALREEF_VFIO_SM=70 \
   cargo test --test hw_nv_vfio --features vfio \
     -- --ignored vfio_dispatch_nop_shader --test-threads=1
   ```

**What to verify**:
- Does GP_GET advance after warm-up? (If yes: software stack works)
- Does GR context survive the nouveau → vfio-pci rebind?
- If GR context is lost: need to submit FECS init after VFIO rebind (coralReef already has `gr_context_init` in pushbuf.rs)

### If GP_GET Advances — Full Battery

```bash
# Dispatch + readback
CORALREEF_VFIO_BDF=0000:03:00.0 CORALREEF_VFIO_SM=70 \
cargo test --test hw_nv_vfio --features vfio -- --ignored --test-threads=1

# Advanced (BAR0 cartography, PFIFO diagnostics)
CORALREEF_VFIO_BDF=0000:03:00.0 CORALREEF_VFIO_SM=70 \
cargo test --test hw_nv_vfio_advanced --features vfio -- --ignored --test-threads=1

# Channel tests
CORALREEF_VFIO_BDF=0000:03:00.0 CORALREEF_VFIO_SM=70 \
cargo test --test hw_nv_vfio_channel --features vfio -- --ignored --test-threads=1
```

### If Still Stuck — Diagnostic Path

1. Dump FECS/GPCCS state post-nouveau-warm, before VFIO rebind
2. Dump FECS/GPCCS state after VFIO rebind — did context survive?
3. If context lost: attempt `gr_context_init` via VFIO BAR0 (coralReef has the code)
4. Check if PBDMA is alive (PBDMA_INTR register should be 0, not 0xbad...)

---

## Key Files

| File | Purpose |
|------|---------|
| `crates/coral-driver/src/nv/vfio_compute/submission.rs` | GPFIFO submit + H1 cache flush |
| `crates/coral-driver/src/vfio/channel/` | PFIFO channel, V2 MMU, runlist |
| `crates/coral-driver/src/vfio/cache_ops.rs` | `clflush_range`, `memory_fence` |
| `crates/coral-glowplug/src/device.rs` | `lend()`, `reclaim()`, `resurrect()` |
| `crates/coral-glowplug/src/socket.rs` | JSON-RPC dispatch for device.* methods |
| `crates/coral-driver/tests/hw_nv_vfio.rs` | VFIO hardware tests (dispatch is `#[ignore]`) |
| `crates/coral-driver/tests/glowplug_client.rs` | `GlowPlugClient` + `VfioLease` RAII |
| `crates/coral-glowplug/tests/hw_hotswap.rs` | Hot-swap integration tests |
| `specs/SOVEREIGN_MULTI_GPU_EVOLUTION.md` | Full pipeline spec |

---

## GlowPlug Socket

Default: `/run/coralreef/glowplug.sock`

```bash
# Health check
echo '{"jsonrpc":"2.0","method":"health.check","id":1}' | socat - UNIX-CONNECT:/run/coralreef/glowplug.sock

# Device list
echo '{"jsonrpc":"2.0","method":"device.list","id":2}' | socat - UNIX-CONNECT:/run/coralreef/glowplug.sock

# Lend device
echo '{"jsonrpc":"2.0","method":"device.lend","params":{"bdf":"0000:03:00.0"},"id":3}' | socat - UNIX-CONNECT:/run/coralreef/glowplug.sock

# Reclaim device
echo '{"jsonrpc":"2.0","method":"device.reclaim","params":{"bdf":"0000:03:00.0"},"id":4}' | socat - UNIX-CONNECT:/run/coralreef/glowplug.sock
```

---

## No Changes Needed in coralReef

The software stack is complete. If hotSpring can warm the GPU and GP_GET advances,
the full dispatch pipeline works. If GR context is lost during driver rebind,
coralReef's existing `gr_context_init` pushbuf method can be submitted after
VFIO open — but this is a hotSpring experiment to determine.
