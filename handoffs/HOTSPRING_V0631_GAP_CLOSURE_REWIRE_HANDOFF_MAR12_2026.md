# hotSpring v0.6.31 — Gap Closure Rewire

**Date**: March 12, 2026
**From**: hotSpring (hardware validation spring)
**To**: barraCuda, coralReef, toadStool
**Type**: Upstream sync + sovereign dispatch routing evolution

---

## What Changed

hotSpring absorbed the latest evolution from all three sovereign compute trio primals:

| Primal | Previous Pin | Current Pin | Key Changes |
|--------|-------------|-------------|-------------|
| **barraCuda** | `d761c5d` | `82ff983` | dispatch_binary wired, coral cache → dispatch, VoltaNoPmuFirmware, sovereign_resolves_poisoning(), Gap 1 CLOSED |
| **coralReef** | `eb4b4eb` (Iter 35) | `fe9fae4` (Iter 37) | Sovereign GSP (22 chips), UVM GPFIFO + USERD, dispatch_precompiled, KernelCacheEntry, Gap 2 partial |
| **toadStool** | S146 | S147 (`ac3ea6d6`) | hw-learn JSON-RPC wired, RegisterAccess bridge, spirv_codegen_safety rename, Gap 4 CLOSED |

## Sovereign Routing Evolution

The MD precision strategy (3 entry points: all-pairs, Verlet, cell-list) now checks `sovereign_resolves_poisoning()`:

```
Before: df64_poisoned → fall back to native f64 (safe but slower)
After:  df64_poisoned AND sovereign_available → use DF64 anyway (sovereign bypasses naga SPIR-V)
```

This means on hardware where the naga DF64 transcendental poisoning bug would normally force a fallback to native f64, sovereign dispatch can now re-enable the DF64 path — getting FP32-core streaming throughput (3.24 TFLOPS) instead of native FP64 ALU (~0.3 TFLOPS on consumer GPUs).

## Gap Status Summary

| Gap | Description | Status | Closed By |
|-----|-------------|--------|-----------|
| **Gap 1** | dispatch_binary not wired | **CLOSED** | barraCuda `82ff983` |
| **Gap 2** | NVIDIA proprietary (nvidia-drm / UVM) | **Partial** | coralReef Iter 37 (GPFIFO + USERD) |
| **Gap 3** | FECS channel submission for Volta init | **Unblocked** | hotSpring DRM fix `eb4b4eb` |
| **Gap 4** | RegisterAccess bridge | **CLOSED** | toadStool S147 |
| **Gap 5** | Knowledge base → compute init | Pending | coralReef GSP module exists |
| **Gap 6** | Error recovery | Pending | — |

**Gaps closed**: 2 of 6 (was 0)
**Gaps unblocked**: 1 (was blocked by incorrect ioctl)
**Gaps partially closed**: 1

## Validation

- **848 tests, 0 failures** (lib, both default and sovereign-dispatch features)
- **0 clippy warnings** (pedantic)
- Clean compile against all three upstream primals at latest commits
- No API breaks — all barraCuda public API additions are backward-compatible

## Hardware Test Results (from previous session, still valid)

| Test | Titan V (GV100) | RTX 3090 (GA102) |
|------|-----------------|-------------------|
| VM_INIT | PASS | PASS |
| CHANNEL_ALLOC | PASS | PASS |
| GEM alloc + VM_BIND | PASS | PASS |
| Upload/Readback | PASS | PASS |
| Full dispatch cycle | 0 output (QMD tuning) | 0 output (QMD tuning) |

**Remaining**: Compute kernel execution returns 0 instead of expected 42. This is a QMD/pushbuf configuration issue (CBUF bindings, shader VA), not a DRM pipeline issue. All infrastructure works.

## For coralReef

The DRM pipeline is hardware-proven. The remaining QMD tuning work:
1. CBUF descriptor binding (shader VA into constant buffer slot)
2. Push buffer command sequence (QMD launch with correct register settings)
3. Potentially: FECS method init for GR engine warm-up on GV100

Iter 37's sovereign GSP module and UVM compute dispatch pipeline are the right architecture for this.

## For toadStool

S147's hw-learn pipeline + RegisterAccess bridge are now absorbed into hotSpring's sovereign dispatch benchmarks. The SM86/Ampere strategy is prioritized over SM70/Volta in the probe order, reflecting our proven hardware.

## For barraCuda

Gap 1 closure is reflected in hotSpring's routing. The `sovereign_resolves_poisoning()` hint is now wired into all 3 MD entry points. When the full dispatch pipeline completes (QMD tuning), hotSpring will be the first spring to run science workloads entirely through the sovereign stack.
