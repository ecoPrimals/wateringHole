# Handoff: hotSpring → Primal & Spring Teams — Sovereign GPU Evolution Lessons

**Date:** 2026-04-02
**From:** hotSpring (biomeGate)
**To:** All primal teams (coralReef, barraCuda, toadStool, nestGate, songBird, bearDog, loamSpine, squirrel, sweetGrass, biomeOS, petalTongue, rhizoCrypt) + all spring teams
**Scope:** Lessons learned, evolution patterns, absorption points from 141+ experiments of sovereign GPU compute work

---

## 1. Architecture Lessons — What We Learned Building Sovereign GPU Compute

### The Firmware Barrier Is a POST Barrier

The fundamental blocker for sovereign GPU compute on modern NVIDIA GPUs (Volta+)
is not firmware signing per se — it is the dependency on VBIOS POST. The GPU
hardware requires specific initialization sequences (DEVINIT scripts) to bring
up clocks, PLLs, memory controllers, and security hardware. Without these,
even correctly-signed firmware cannot authenticate because the crypto engine
itself is uninitialized.

**Lesson for all primals:** Hardware initialization is layered. You can have
correct software at layer N and still fail because layer N-1 was never configured.
The recipe replay approach (capturing and replaying register state) works for
*maintaining* state but not for *establishing* it from cold.

### D-State Resilience Is Non-Negotiable

Any primal that touches PCIe devices (GPUs, NPUs, FPGAs) must handle the case
where a sysfs write enters uninterruptible kernel sleep. The pattern:

```rust
// Spawn child process for risky write, poll with timeout
// If child D-states, kill it — daemon stays alive
guarded_sysfs_write(path, value, timeout_secs)
```

This pattern (implemented in ember Exp 140) should be standard for any
`VendorLifecycle` operation that touches sysfs. biomeOS, nestGate, and any
primal with hardware I/O should adopt this.

### The "Diesel Engine" Pattern

For warm handoff of stateful hardware:
1. **Orchestrator** (glowplug) manages the swap sequence
2. **Keepalive** (ember) holds fds open across swaps, provides MMIO access
3. **Livepatch** freezes kernel driver teardown paths
4. **Active intervention** via MMIO writes during the swap window

This pattern generalizes beyond GPUs to any hardware with firmware state that
must survive driver transitions.

### Virtual DMA Is the Only Safe Path on HS+ Hardware

On Volta+ GPUs with HS+ security:
- FBIF_TRANSCFG is locked in VIRT mode by the boot ROM
- Host writes to DMA configuration registers are silently ignored
- The ONLY way to route DMA is through the falcon's MMU with page tables in VRAM
- System memory access requires SYS_MEM_COH PTEs that route through the IOMMU

**Lesson:** When hardware locks you out of direct configuration, build the
mapping layer that the hardware expects. Don't fight the security model —
work within it.

---

## 2. What hotSpring Used From Each Primal

### coralReef (Primary)

- `coral-driver`: VfioDevice, MappedBar, DmaBuffer, falcon HAL, ACR boot solver
- `coral-ember`: VFIO fd holder, RPC interface, livepatch control, MMIO read/write
- `coral-glowplug`: PCIe broker, personality management, health monitoring
- `coralctl`: CLI for GPU operations (cold-boot, devinit, reset, experiment)

**Evolution contributed back:**
- 7 falcon binding bugs (B1-B7)
- 7 WPR construction bugs (W1-W7)
- PDE slot fix for GV100 MMU v2
- FBIF VIRT mode workaround with page table patching
- K80 Kepler dispatch path (QMD v1.7, push buffer methods)
- Uncrashable safety architecture (D-state resilience)

### barraCuda

- WGSL shaders (99 total) — the compute payload that sovereign dispatch will execute
- DF64 precision tier — proven 9.9× throughput advantage
- Physics validation infrastructure — 870 tests, 39/39 validation suites

**No changes needed in barraCuda** — it is correctly insulated from driver-level work.

### toadStool

- `shader.dispatch` orchestration layer
- `PcieTransport`, `ResourceOrchestrator`
- GPU sysmon telemetry

**Absorption point:** The `shader.dispatch → compute.dispatch.execute` pipeline
is architecturally correct. Once sovereign boot completes on Titan V, toadStool's
orchestration layer connects directly to coralReef's dispatch.

### nestGate

- Not directly used in sovereign GPU work
- IPC patterns from nestGate influenced ember's RPC design

### Other Primals

- **songBird**: Ring/sled concurrency patterns informed ember's async design
- **petalTongue**: Capability-first discovery pattern mirrors GPU adapter enumeration
- **squirrel**: Dependency tracking patterns relevant to hardware init ordering

---

## 3. Absorption Opportunities

### For coralReef

| Component | Location | What to Absorb |
|-----------|----------|---------------|
| VBIOS DEVINIT executor | `devinit/script/interpreter.rs` | Execute BIT 'I' scripts — the missing link for Titan V ACR auth |
| Sysmem PTE encoding | `instance_block.rs` | `encode_sysmem_pte` + PT construction for VIRT mode DMA |
| K80 dispatch | `nv/kepler_falcon.rs` | QMD v1.7 builder, Kepler push buffer methods |
| Safety architecture | `ember/guarded_sysfs_write` | D-state resilient sysfs operations |
| Falcon capability probe | `falcon_capability.rs` | Runtime register layout discovery |

### For toadStool

- Once L10 is resolved, integrate `fecs_method.rs` GR context init into orchestration
- The silicon saturation profiling data (Exp 107) informs `GpuDriverProfile` tuning

### For All Primals

- **Capability-based discovery** over hardcoded assumptions (learned from 10+ SDK assumptions overturned on AKD1000 NPU)
- **Tolerance centralization** — zero inline magic numbers (pattern proven across 870+ tests)
- **Provenance tracking** — every constant traceable to a published reference

---

## 4. Evolution Timeline

```
Exp 060-069: GlowPlug + VFIO lifecycle (D3hot recovery, HBM2 training)
Exp 070-085: Falcon boot chain (10 sovereign layers, 14 bugs found and fixed)
Exp 086-095: Cross-driver profiling, sysmem HS breakthrough, WPR2 root cause
Exp 096-107: Silicon characterization, self-tuning RHMC, saturation profiling
Exp 110-122: Consolidation matrix, WPR2 hardware lock definitive
Exp 123-128: K80 sovereign compute, VM capture, livepatch, puzzle box matrix
Exp 130-131: Reset architecture, daemon wiring
Exp 132-141: Dual GPU sovereign boot, D-state safety, ACR HS auth root cause
```

**Key milestone:** The transition from "cracking the GPU" to "solving the GPU" —
treating falcon microcontrollers as firmware interfaces to probe and understand,
not barriers to overcome by force.

---

## 5. Current Frontier

| Track | Status | Next Step |
|-------|--------|-----------|
| **Titan V sovereign boot** | L10 blocked (VBIOS DEVINIT) | Execute BIT 'I' scripts via VBIOS interpreter |
| **K80 sovereign boot** | FECS running, PGRAPH blocked | Resolve PRI-faults above 0x409504 |
| **RTX 3090 GPFIFO** | ✅ Operational | Production compute workloads |
| **AMD RDNA2 DRM** | ✅ 7/8 parity | EXEC masking for divergent wavefronts |
| **Science pipeline** | ✅ 500+ checks pass | 16⁴+ dynamical production on sovereign pipeline |

---

## 6. Fossil Record

All experiment journals, register traces, and recipes are preserved in
`hotSpring/experiments/` (141 experiments) and `hotSpring/data/` (K80/Titan V
captures, oracle registers, metal maps). This is the canonical record of how
vendor-free GPU compute was systematically debugged on real hardware.
