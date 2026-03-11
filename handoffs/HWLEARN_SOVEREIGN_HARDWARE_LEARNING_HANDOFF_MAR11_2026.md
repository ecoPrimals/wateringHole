# hwLearn — Sovereign Hardware Learning Implementation Handoff

**Date**: 2026-03-11
**Origin**: hotSpring (integration driver) → toadStool (hw-learn crate) + biomeOS (capability routing)
**Audience**: All springs, coralReef, barraCuda, toadStool, biomeOS teams

---

## What Was Implemented

A vendor-neutral hardware learning system that observes working GPUs, distills init patterns into portable recipes, and applies them to unlock compute on firmware-limited hardware.

### Crate: `hw-learn` (toadStool `crates/core/hw-learn/`)

**46 tests, 24 source files, 0 TODO/FIXME**

| Module | Purpose | Files |
|--------|---------|-------|
| `observer/` | Trace GPU init from kernel facilities | `mmio_trace.rs`, `ioctl_trace.rs`, `gsp_rpc.rs`, `amd_pm4.rs`, `intel_batch.rs` |
| `distiller/` | Extract minimal init recipes from traces | `diff.rs`, `classify.rs`, `recipe.rs` |
| `knowledge/` | Cross-vendor recipe store + AMD baseline | `mod.rs` (JSON-backed store), `arch_map.rs`, `amd_baseline.rs` |
| `applicator/` | Replay recipes on target GPUs | `mod.rs`, `nouveau_drm.rs`, `verify.rs` |
| `brain_ext/` | PrecisionBrain extensions | `learning_advisor.rs`, `firmware_probe.rs`, `capability_gap.rs` |

### sysmon Enhancement: `FirmwareInventory`

`GpuDevice::firmware_inventory()` now probes `/lib/firmware/` for:
- **NVIDIA**: PMU, GSP, ACR, GR, SEC2 (PCI device ID → chip name mapping)
- **Intel**: GuC, HuC (glob-based)
- **AMD**: All not-required (compute always viable)

New exports: `FirmwareInventory`, `FwStatus` (from `toadstool-sysmon`)

### PrecisionBrain `fleet` Module

Feature-gated (`hardware-learning`) module in `nvvm_safety.rs`:
- `fleet::learning_opportunities(fleet: &[FleetMember])` — bridges per-GPU calibration with fleet-level learning
- Maps adapter names to GPU generation/compute class

### biomeOS Capabilities

5 new capabilities in `compute.hardware.*`:

```toml
"compute.hardware.observe"  = { provider = "toadstool", method = "hw_learn.observe" }
"compute.hardware.distill"  = { provider = "toadstool", method = "hw_learn.distill" }
"compute.hardware.apply"    = { provider = "toadstool", method = "hw_learn.apply" }
"compute.hardware.share"    = { provider = "toadstool", method = "hw_learn.share_recipe" }
"compute.hardware.status"   = { provider = "toadstool", method = "hw_learn.status" }
```

Registered in both `capability_registry.toml` (runtime) and `capability_domains.rs` (Rust fallback).

### AMD GFX10 Gold-Standard Baseline

Canonical 7-phase compute init recipe from amdgpu kernel source:
1. Probe → 2. Firmware → 3. Power → 4. Memory → 5. Engine → 6. Context → 7. Verify

21 documented register offsets (GRBM, CP, RLC, SPI, COMPUTE). `UniversalInitPhase` enum encodes the vendor-neutral skeleton.

---

## Live Validation on hotSpring Rig

`fleet_observe` example binary confirmed on biomeGate hardware:

```
card0: NVIDIA 1d81 (Titan V)
  driver: nouveau
  PMU: missing, GSP: missing, ACR: present, GR: present, SEC2: present
  compute viable: false (missing PMU and GSP firmware)

card1: NVIDIA 2204 (RTX 3090)
  driver: nvidia
  PMU: missing, GSP: present, ACR: present, GR: present, SEC2: present
  compute viable: true

Learning Opportunity: card1 (Ampere/sm86) → card0 (Volta/sm70)
  confidence: 40%
  cross-vendor: false
  gap: missing firmware: PMU, GSP
```

---

## What Each Team Needs to Know

### toadStool Team
- **hw-learn** is now a workspace member (`crates/core/hw-learn/`). 46 tests pass.
- **sysmon** has new `FirmwareInventory`, `FwStatus` types and `GpuDevice::firmware_inventory()`.
- **runtime-universal** has optional `hardware-learning` feature that enables `fleet` module in `nvvm_safety.rs`.
- **Next**: Wire `hw_learn.observe/distill/apply/share/status` methods into toadStool server for biomeOS capability calls.

### coralReef Team
- hw-learn's `applicator/nouveau_drm.rs` provides a framework for DRM ioctl-based recipe application.
- The `verify.rs` module's `ComputeReadback` check needs integration with coralReef's dispatch pipeline.
- **Next**: When DRM dispatch works on any GPU, hw-learn can trace and learn the init pattern automatically.

### barraCuda Team
- No direct changes needed. hw-learn operates at the driver/DRM layer, below barraCuda's dispatch abstraction.
- The `GpuBackend` trait and `ComputeDispatch<B>` remain the compute interface.

### wetSpring + neuralSpring Teams (eastgate)
- **eastgate** (RTX 4070 + Titan V) is the ideal testbed. The `fleet_observe` binary and `eastgate_observe.sh` script are ready.
- Run: `cargo run -p hw-learn --example fleet_observe` on eastgate.
- If 4070 compute works via nouveau GSP: capture traces with `eastgate_observe.sh` (requires root for mmiotrace).
- The 4070 (Ada/AD104, GSP-based) is expected to be a teacher for the Titan V (Volta, no PMU).

### biomeOS Team
- 5 new `compute.hardware.*` capabilities registered. Deploy graph template in plan doc.
- **Next**: Create `hw_learn_pipeline` deploy graph for cross-machine learning via Plasmodium.

---

## Known Limitations

1. **Register writes** — direct MMIO register writes not yet implemented (requires debugfs/BAR access or kernel module). The ioctl path is functional.
2. **Compute readback verification** — requires integration with barraCuda/coralReef dispatch for end-to-end validation.
3. **Cross-vendor confidence** — AMD→NVIDIA learning is at ~5% confidence (universal patterns only). Same-vendor learning is 40-90%.
4. **Firmware blocker** — Titan V on nouveau remains blocked (no PMU/GSP firmware for desktop Volta). The 4070 eastgate test is the next step.

---

## Files Changed

### toadStool
- `Cargo.toml` — added `crates/core/hw-learn` to workspace
- `crates/core/hw-learn/` — **new crate** (24 files, 46 tests)
- `crates/core/sysmon/src/gpu.rs` — added `FirmwareInventory`, `FwStatus`, `firmware_inventory()`
- `crates/core/sysmon/src/lib.rs` — re-exported new types
- `crates/runtime/universal/Cargo.toml` — added `hardware-learning` feature
- `crates/runtime/universal/src/backends/nvvm_safety.rs` — added `fleet` module

### biomeOS
- `config/capability_registry.toml` — 5 new `compute.hardware.*` entries
- `crates/biomeos-atomic-deploy/src/capability_domains.rs` — added `hardware` to compute domain + test

### hotSpring
- `README.md` — updated date, added hwLearn + Exp 057 entries
- `CONTROL_EXPERIMENT_STATUS.md` — updated sync references

### wateringHole
- This handoff document
