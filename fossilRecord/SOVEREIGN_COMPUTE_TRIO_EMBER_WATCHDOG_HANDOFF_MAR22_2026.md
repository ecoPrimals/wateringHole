# Compute Trio: Ember D-State Resilience + Swap Pipeline Proven

**Date:** March 22, 2026  
**From:** hotSpring  
**To:** coralReef, toadStool, barraCuda  
**License:** AGPL-3.0-only  
**Type:** Trio evolution handoff — Ember D-state resilience, sysfs watchdog, ember/glowplug swap pipeline

---

## Executive Summary

The ember/glowplug swap pipeline is fully operational. Three fixes unlocked stable native/VFIO swaps and IPC under real hardware load:

1. **Process-isolated sysfs watchdog** — Risky sysfs writes run in an isolated process so the main daemon cannot block in uninterruptible sleep (D-state).
2. **IOMMU group peer release** — Peers are released from the VFIO group before `bind_native()`, enabling clean native driver swaps.
3. **EmberClient retry logic** — Transient socket I/O errors are retried with backoff instead of failing the session.

**DRM isolation** (udev + Xorg) is **auto-generated** from device configuration, so rule files do not drift when hardware changes.

**Hardware fleet (biomeGate):** 2× Titan V + RTX 5060 (MI50 removed from the sovereign line).

---

## Patterns (reuse across crates)

- **Risky sysfs** — Never block the main daemon on writes that can stall in D-state; offload or isolate (`guarded_sysfs_write()`).
- **VFIO → native** — Always tear down IOMMU/VFIO group relationships that would keep peers attached before `bind_native()`.
- **Long-lived IPC** — Read full frames, use generous timeouts for control-plane ops, and retry transient socket errors with backoff.
- **DRM + seat policy** — Encode isolation in generated config so CI and new machines match without copy-paste udev.

---

## What Changed

| Area | Change |
|------|--------|
| **coral-ember `sysfs.rs`** | `guarded_sysfs_write()` for risky ops; `sysfs_write_direct()` for safe config-space paths. |
| **coral-ember `swap.rs`** | `release_iommu_group_from_vfio()` before `bind_native()`. |
| **coral-ember `drm_isolation.rs`** | Auto-generate udev rules and Xorg snippets from config. |
| **coral-ember `lib.rs`** | `ensure_drm_isolation()` at startup; socket `chgrp` as required for the pipeline. |
| **coral-glowplug `ember.rs`** | Retry loop, `read_full_response()`, 60s timeout aligned with Ember expectations. |
| **coral-driver `mmu_fault.rs`** | Structured MMU fault decoding for Volta+ (sovereign pipeline debugging). |

---

## coralReef Actions

- **Pull main** — Changes are committed at `6b2202f` on `main`; absorb before building on this stack.
- **Sysfs discipline** — Any new code that writes sysfs for risky paths should use **`guarded_sysfs_write()`** (or the same process-isolation pattern) to avoid D-state risk in long-lived daemons.
- **DRM isolation** — Rely on auto-generated udev/Xorg from config; avoid hand-maintained rules per machine unless debugging.
- **MMU faults** — Use structured Volta+ MMU fault output when triaging sovereign pipeline failures (links cleanly with driver diagnostics).

---

## toadStool Actions

- **GlowPlug client stub** — Adopt the **retry pattern** from EmberClient: classify transient I/O (`is_transient_io` or equivalent), backoff, and avoid failing the whole session on one bad read.
- **Future sysfs** — If toadStool ever writes sysfs directly, use the **same process-isolation pattern** as coral-ember for risky writes.
- **Fleet** — Plan for **2× Titan V + RTX 5060**; **no MI50** on this sovereign line — adjust test matrices and docs accordingly.

---

## barraCuda Actions

- **Fleet** — MI50 is removed from the sovereign VFIO experiment set; **2× Titan V** are the primary cards for those experiments alongside RTX 5060 where relevant.
- **IPC clients** — The EmberClient **retry/backoff** approach applies to any long-lived IPC client (e.g. nursery or future services), not only ember.

---

## Reference

- **Detailed hotSpring handoff:** `wateringHole/handoffs/HOTSPRING_EMBER_WATCHDOG_SWAP_PIPELINE_HANDOFF_MAR22_2026.md`
- **Experiment journal:** `hotSpring/experiments/074_SOVEREIGN_MMU_EMBER_SWAP_EVOLUTION.md`

Paths are relative to the **ecoPrimals** tree (`wateringHole/…` and `hotSpring/…`).

---

## Fleet snapshot (March 22, 2026)

| Item | Note |
|------|------|
| NVIDIA | 2× Titan V, 1× RTX 5060 |
| AMD | MI50 **not** on sovereign line for this stack |
| Isolation | DRM rules + Xorg from coral-ember config generation |

---

*Swap path proven: watchdog-hardened sysfs, clean IOMMU teardown before native bind, resilient Ember↔GlowPlug IPC, and DRM isolation generated from config.*
