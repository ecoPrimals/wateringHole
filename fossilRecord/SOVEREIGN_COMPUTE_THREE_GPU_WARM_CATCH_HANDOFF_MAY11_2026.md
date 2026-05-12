# Sovereign Compute — Three-GPU Warm-Catch Handoff

**Date**: May 11, 2026
**Type**: Ecosystem Handoff
**From**: hotSpring (hardware validation) + coralReef (warm-catch pipeline)
**To**: toadStool, coralReef compiler team, coral naga team, barracuda, all springs
**Status**: ALL 3 GPUs sovereign — dispatch gap remains

---

## Summary

Three local GPUs — RTX 5060 (SM120/Blackwell), Titan V (SM70/Volta), and
Tesla K80 (SM37/Kepler GK210) — are now sovereign via a pure Rust warm-catch
pipeline. The warm-catch mechanism bypasses firmware barriers (SEC2/ACR on Volta,
FECS internal firmware on Kepler) by temporarily loading a binary-patched
`nouveau.ko` that trains memory and initializes FECS/GPCs, then swapping back
to `vfio-pci` before teardown.

The compile side works: WGSL → naga IR → coral-reef SASS/ISA for all three
SM generations. The dispatch infrastructure exists: `VfioChannel::create_warm`,
GPFIFO/pushbuf, semaphore fence. The **gap** is E2E wiring: running physics
workloads (barraCuda QCD shaders) through the sovereign compile → sovereign
dispatch → readback path on warm-caught GPUs.

---

## Three-GPU Sovereign Status

| GPU | Architecture | Status | Key Evidence |
|-----|-------------|--------|-------------|
| RTX 5060 | SM120 / Blackwell (GB206) | **FULL DISPATCH** | VFIO sovereign dispatch live since April 16. f64 div/sqrt polyfills, semaphore fence, QMD v5.0, UVM write access proven. |
| Titan V | SM70 / Volta (GV100) | **SOVEREIGN** | FECS RUNNING via warm-catch. ACR/SEC2 loads FECS natively. FECS_MC = 0x0c060006, PGRAPH enabled, 1 GPC active. GAP-HS-073 RESOLVED. |
| Tesla K80 | SM37 / Kepler (GK210) | **SOVEREIGN** | GDDR5 trained (12 GiB), 5 GPCs active via warm-catch. PMC_ENABLE = 0xfc37b1ef (pop=22), FECS_MC = 0x00060005 (running). GAP-HS-076 RESOLVED. Requires upstream `case 0x0f2` one-line patch for nouveau GK210 recognition. |

---

## Warm-Catch Pipeline — Pure Rust

The pipeline was initially proven via shell scripts and Python ("jelly strings"),
then elevated to pure Rust in coralReef:

| Component | Path | Role |
|-----------|------|------|
| ELF patcher | `coral-driver/src/tools/elf_patcher.rs` | Pure Rust `nouveau.ko` binary patching via `object` crate. NOPs 4 teardown functions at machine-code level. |
| Warm probe | `coral-driver/src/vfio/warm_probe.rs` | Standalone `WarmStateSnapshot` — reads PMC, PRAMIN, FECS, GPC state from BAR0. |
| Orchestrator | `coral-ember/src/ipc/handlers_warm_catch.rs` | `ember.warm_catch` RPC: patch → swap → settle → probe → swap back. |
| Pre-check | `coral-driver/src/vfio/sovereign_init.rs` | `warm_catch_pre_check()` — detects cold GPU with available warm-catch path. |
| CLI | `coralctl warm-catch <BDF>` | Entry point with `--memory-type gddr5|hbm2|gddr6`, `--dry-run`. |
| Cleanup guard | `ModuleCleanupGuard` | RAII — ensures stock `nouveau.ko` restored even on panic. |

Era-aware settle times: GDDR5=10s (K80), HBM2=12s (Titan V), GDDR6=8s.

---

## Dispatch Gap — What's Not Yet Wired

The sovereign pipeline has two halves: **compile** and **dispatch**. Both exist
but are not yet connected end-to-end for physics workloads.

| Half | Status | What Exists |
|------|--------|-------------|
| Compile | Operational | WGSL → naga IR → coral-reef SASS (SM35/SM70/SM120), AMD GFX10/11/9. 1314+ tests. |
| Dispatch | Infrastructure exists | `VfioChannel::create_warm`, GPFIFO/pushbuf, semaphore fence, `vfio_warm_write_42_readback` test. |
| E2E physics | **NOT YET WIRED** | barraCuda `sovereign-dispatch` feature flag exists but not exercised with real QCD on warm GPUs. |
| glowplug dispatch | **CUDA-ONLY** | `device.dispatch` handler returns `CudaFeatureDisabled` without the `cuda` feature. Needs VFIO/DRM mode. |

---

## Primal Domain Split — Nest Atomic Pattern

Following the Nest atomic pattern (NestGate does not embed BearDog's crypto — it
calls `crypto.sign` via IPC), the current `coral-driver` mixes two domains that
should be split:

### What stays in coralReef (HOW — compiler domain)

- `coral-reef` — WGSL → IR → SASS/ISA compiler
- SASS/PTX instruction encoders (SM35/SM70/SM120/GFX10 backends)
- naga_translate (IR construction from naga::Module)
- Optimization passes, register allocation, legalization
- QMD struct generation (dispatch metadata format per generation)
- ELF patcher (kernel module binary patching tooling)
- Serves `shader.compile.wgsl`, `shader.compile.spirv` via IPC

### What moves to toadStool (WHERE — hardware domain)

- BAR0/MMIO register access — hardware interaction is toadStool's domain
- VFIO channel creation, GPFIFO/pushbuf submission — command submission is WHERE
- Sovereign init stages (boot sequence) — device lifecycle is WHERE
- coral-gpu dispatch orchestration — becomes toadStool's `compute.dispatch.execute`
- DRM ioctl wrappers (nouveau EXEC, amdgpu CS) — driver interface is WHERE

### IPC contract (same pattern as Tower atomic)

- `by_domain("shader")` → coralReef compiles WGSL → returns binary blob + ShaderInfo
- `by_domain("compute")` → toadStool dispatches binary to hardware → returns results
- Neither primal links the other's crate at compile time

---

## Ember/Glowplug/Cylinder Absorption into toadStool

**Assessment: READY for absorption.** The implementations are mature and toadStool
already has the trait surface waiting.

### coralReef maturity (what gets absorbed)

| Component | Tests | Capability |
|-----------|-------|-----------|
| coral-ember | 228 | 22 `ember.*` + 8 `mmio.*` + 3 `health.*` RPC methods, per-device lifecycle, MMIO, firmware intermediary, PCIe keepalive |
| coral-glowplug | 436 | ~37 RPC methods, cylinder orchestration (per-device subprocess), ECU RPC, systemd service |
| Multi-vendor | — | NVIDIA (nouveau, nvidia) + AMD (amdgpu) + Intel (xe, i915) personality detection |
| Battle-tested | — | 3 GPU generations (RTX 5060, Titan V, K80) with warm-catch |

### toadStool trait surface (already exists, waiting for implementations)

- `toadstool-ember`: `HeldResource`, `ResourceHandle`, `MetadataStore`, `SwapJournal`, `LendReceipt`
- `toadstool-glowplug`: `DeviceDiscovery`, `DeviceSlot`, `DevicePersonality`, `SwapOrchestrator`, `FirmwareInterface`, `HealthProbe`
- `pci_discovery.rs`: Unified PCI scanner (vendor/device/class filtering)
- `ComputeUnit` trait: CPU/GPU/neuromorphic (universal)
- Akida NPU driver/setup (validates non-GPU generalization)
- AMD GPU detection + hw-learn baselines

### What toadStool absorbs

- Sysfs bind/unbind/swap implementation (behind `SwapOrchestrator` trait)
- Cylinder architecture (per-device subprocess isolation) — generalizable beyond GPU to NPU/USB/HSM
- VFIO hold/release/reacquire implementation (behind `HeldResource`)
- Vendor lifecycle detection (NVIDIA/AMD/Intel strategies behind `DevicePersonality`)
- Warm-catch orchestration wiring (ELF patching stays in coral-driver, but the swap/settle/probe pipeline moves)
- Journal/observation/health implementations (behind existing trait contracts)

### What toadStool can validate that hotSpring cannot

- **Akida NPU**: device hold/swap/health/dispatch patterns on non-GPU silicon
- **AMD GPUs**: full lifecycle (bind/unbind/swap/warm) + dispatch on RDNA hardware
- **Intel Arc**: xe driver personality + dispatch validation
- **Cross-device cylinder orchestration**: GPU + NPU + USB simultaneously
- **Universal `DeviceDiscovery`**: across all PCI device classes

### toadStool evolution path (from GPU primal to universal hardware primal)

```
Phase 1: Absorb coral-ember/glowplug implementations behind existing traits
Phase 2: Absorb coral-driver hardware access (BAR0/MMIO/VFIO/DRM) into toadStool driver layer
Phase 3: Validate with Akida NPU (non-GPU dispatch) + AMD (non-NVIDIA dispatch)
Phase 4: Generalize cylinder from "per-GPU subprocess" to "per-device subprocess"
Phase 5: Unify nvpmu + future amdpmu + npupmu behind a common PowerManagement trait
Phase 6: Serve compute.dispatch.execute — receive compiled binary from coralReef, dispatch to any hardware
```

---

## Local Wiring Plan (hotSpring + coralReef — what we do next)

These are the tasks the local team (hotSpring hardware lab) continues to wire:

1. **Dispatch validation on warm-caught Titan V**: Run `vfio_warm_write_42_readback` test after `coralctl warm-catch` — prove dispatch works on warm GPU.
2. **Dispatch validation on warm-caught K80**: Same test on Kepler — prove Kepler dispatch after warm-catch.
3. **barracuda sovereign-dispatch exercise**: Run barraCuda `sovereign-dispatch` feature with real Yukawa MD on warm GPUs via coral-gpu.
4. **glowplug VFIO dispatch mode**: Extend glowplug `device.dispatch` handler to accept VFIO/DRM mode (currently CUDA-only, returns `CudaFeatureDisabled` without the feature).

---

## Upstream Delegation (leave to respective teams)

| Team | Responsibility |
|------|---------------|
| **toadStool team** | Absorb coral-ember/glowplug implementations, absorb coral-driver hardware access, validate on Akida/AMD/Intel, generalize cylinder, serve `compute.dispatch.execute` IPC |
| **coral naga team** | naga WGSL parser evolution, IR-to-IR stability validation loop |
| **coralReef compiler team** | SM120 native SASS encoder (replacing PTX emitter) |
| **coralReef kernel team** | `coral-kmod` C code evolution to pure Rust |
| **coralReef team** | cudarc optional dep removal (after sovereign dispatch is default) |

---

## External Dependencies — Honest Inventory

| Dependency | Status | Path to Sovereignty |
|------------|--------|---------------------|
| naga (WGSL parser) | Still external | coral naga team owns IR-to-IR stability validation loop |
| wgpu (GPU compute) | Still external | toadStool team evolves; `sovereign-dispatch` feature bypasses |
| PTX for SM120 | Still external | coralReef compiler team building native SM120 SASS encoder |
| cudarc (optional) | Feature-gated | Removed after sovereign dispatch is default |
| `coral-kmod` C modules | Still C | coralReef kernel team evolving to pure Rust |

---

## References

- `infra/wateringHole/fossilRecord/consolidated-may2026/GPU_AND_COMPUTE_EVOLUTION.md` — full layer status tables
- `infra/wateringHole/PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` — cross-primal guidance
- `springs/hotSpring/wateringHole/handoffs/HOTSPRING_SOVEREIGN_RUST_EVOLUTION_HANDOFF_MAY11_2026.md` — local lab handoff
- `springs/hotSpring/experiments/README.md` — Experiment 190 milestone details
- `primals/coralReef/coral-driver/src/tools/elf_patcher.rs` — ELF patcher source
- `primals/coralReef/coral-ember/src/ipc/handlers_warm_catch.rs` — warm-catch orchestrator
