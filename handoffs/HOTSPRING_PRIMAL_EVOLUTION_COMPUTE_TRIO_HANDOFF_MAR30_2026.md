# hotSpring → Compute Trio + Spring Teams: Primal Evolution & Absorption Handoff

**Date:** 2026-03-30
**From:** strandgate (hotSpring v0.6.32, 124 experiments)
**To:** coralReef team, toadStool team, barraCuda team, spring teams
**Context:** AMD scratch memory breakthrough (Exp 124), NVIDIA GPFIFO operational, silicon saturation profiling complete

---

## How hotSpring Uses the Primals (Current State)

### coralReef — Sovereign Compiler + Driver

**Integration point:** `coral-gpu` crate provides the `ComputeDevice` trait.
hotSpring's `validate_coral_sovereign.rs` and `parity_harness.rs` test the full
WGSL → native binary → dispatch → readback pipeline.

**What hotSpring proved for coralReef:**
1. AMD RDNA2 scratch memory requires FLAT_SCRATCH shader prolog (Exp 124)
2. NVIDIA GPFIFO channel init sequence for 580.x GSP-RM (BIND + TSG + ctx share)
3. AMD PM4 `COMPUTE_DISPATCH_SCRATCH_BASE` is necessary but insufficient without
   FLAT_SCRATCH init — DRM CP behavior differs from KFD/HSA
4. `S_SETREG_IMM32_B32` (opcode 20) may not exist on GFX10.3 — use `S_MOV_B32` + `S_SETREG_B32` instead
5. 24 QCD production shaders compile to native AMD GFX10.3 ISA in 102ms

**Evolution signals for coralReef:**
- EXEC masking is the next compiler frontier — Wilson plaquette QCD needs divergent
  control flow (if/else/loop in SU(3) matrix multiply). Without EXEC save/restore,
  AMD dispatch hangs on complex kernels.
- NVIDIA GR context allocation is the next driver frontier — LDL/STL (local memory)
  instructions are rejected by SKEDCHECK05 without GR context buffers.
- QMD v2.2 layout correction is needed for biomeGate's Titan V/K80 work.
- The SSARef LARGE_SIZE panic (Euler HLL) indicates an allocator design constraint
  that will surface in larger shaders.

### barraCuda — Math Engine + Precision Tiers

**Integration point:** hotSpring's `barracuda/` crate consumes barraCuda for all
physics computation — QCD, MD, transport, spectral, gradient flow, RHMC.

**What hotSpring proved for barraCuda:**
1. 15-tier precision continuum works in production — DF64 forces + F64 Metropolis
   validated across 1,031+ QCD trajectories
2. Silicon saturation profiling: TMU PRNG, subgroup reduce, ROP atomic scatter-add
   are live in production RHMC pipeline
3. Self-tuning RHMC with zero hand-tuned parameters — spectral probe (λ_max/λ_min)
   + acceptance-driven dt/n_md + consistency-driven pole count
4. True multi-shift CG with shared Krylov subspace reduces RHMC cost
5. Consumer GPUs (RTX 3090) can do L=46⁴ dynamical QCD (23.6 GB)

**Evolution signals for barraCuda:**
- The sovereign pipeline (coralReef) bypasses the Naga WGSL→SPIR-V DF64 poisoning bug
  entirely — barraCuda shaders compiled through coralReef don't need NVVM workarounds
- Scratch memory support means QCD kernels with large temporary arrays (Wilson
  plaquette, gauge force) can now run via the sovereign path on AMD
- The `SiliconCapabilityMatrix` should add scratch memory capacity as a routing dimension
- Per-thread local memory usage affects performance characteristics differently from
  register-only shaders — the precision brain should account for this

### toadStool — Hardware Discovery + Dispatch Routing

**Integration point:** toadStool's `shader.dispatch` wiring in S168, PrecisionBrain
routing from barraCuda, GPU discovery and capability probing.

**What hotSpring proved for toadStool:**
1. AMD and NVIDIA have fundamentally different driver initialization requirements —
   toadStool's routing must know which dispatch path each card supports
2. Consumer cards have more silicon diversity than HPC cards — tensor cores, RT cores,
   TMUs, ROPs are all usable for physics (hotSpring Exp 096-107)
3. The precision brain's routing decision (which tier on which card) depends on
   measured performance, not static tables — driver updates change behavior
4. Scratch memory support is a per-card capability that affects shader dispatchability

**Evolution signals for toadStool:**
- `SiliconCapabilityMatrix` should include: scratch memory support, FLAT_SCRATCH
  initialization method, max per-thread scratch bytes, tensor core availability,
  RT core BVH capability, TMU count for table-lookup routing
- The sovereign dispatch path (coralReef → coral-driver) operates alongside the
  wgpu/Vulkan path — toadStool should be able to route to either
- Per-workgroup scratch allocation affects occupancy — routing should consider this

---

## Cross-Team Learnings

### For biomeGate (Titan V / Tesla K80 HMB2 Cracking)

The work done on strandgate directly unblocks biomeGate:

1. **NVIDIA channel init** — the full BIND + TSG + Context Share + VRAM USERD +
   Error Notifier sequence is now documented and tested on RTX 3090 (SM86).
   The same sequence applies to all Volta+ architectures.
2. **FLAT_SCRATCH prolog** — if biomeGate's MI50 (GFX9/Vega) needs scratch memory,
   the same `S_MOV_B32` + `S_SETREG_B32` pattern applies with GFX9 HW_REG IDs.
3. **K80 path** — Kepler has no firmware security. PIO FECS/GPCCS boot code is
   ready in `nv::kepler_falcon`. K80 compute class is `KEPLER_COMPUTE_B = 0xA1C0`.
4. **QMD v2.2** — `build_qmd_v21` needs correct Volta positions from `clc3c0qmd.h`
   for Titan V dispatch.

### For Spring Teams (wetSpring, neuralSpring, groundSpring, airSpring)

1. **Sovereign dispatch eliminates the Naga DF64 bug** — any spring that
   experienced zero-output DF64 transcendental shaders through wgpu/Vulkan can
   bypass the issue entirely via coralReef sovereign compilation
2. **All springs can benefit from silicon saturation** — TMU PRNG, subgroup
   reduce, and ROP atomics are generic GPU patterns applicable to any domain
3. **The sovereign path requires no driver changes** — AMD uses `amdgpu` (open),
   NVIDIA uses existing RM/UVM. Springs don't need to change their code; the
   routing happens at the toadStool/coralReef layer

---

## Pending Debt (Owned by hotSpring + coralReef)

| Item | Owner | Status | Impact |
|------|-------|--------|--------|
| NVIDIA GR context via RM | coralReef | Pending | Unblocks NVIDIA local memory (LDL/STL) |
| AMD EXEC masking | coralReef | Pending | Unblocks AMD Wilson plaquette QCD |
| QMD v2.2 Volta layout | coralReef | Pending | Unblocks biomeGate Titan V dispatch |
| SSARef LARGE_SIZE | coralReef | Pending | Unblocks Euler HLL and larger shaders |
| nvidia_headers.rs stubs v3.0 | coralReef | Pending | Correct QMD positions for SM86 |
| Silicon saturation profiling | hotSpring | Pending | Benchmark both cards via sovereign path |
| AMD vs NVIDIA sovereign comparison | hotSpring | Pending | Throughput/latency/coverage comparison |

---

## Compute Trio Evolution Summary

```
coralReef (Iter 70c)                barraCuda (v0.3.11)              toadStool (S168)
├── Compiler: WGSL→SASS/GFX        ├── 15-tier precision            ├── shader.dispatch wiring
├── coral-driver: AMD DRM+NV UVM   ├── SiliconCapabilityMatrix      ├── PrecisionBrain routing
├── AMD scratch: FLAT_SCRATCH       ├── QCD/MD/transport/spectral    ├── GPU discovery + probe
├── NVIDIA GPFIFO: channel init     ├── Self-tuning RHMC             ├── Hardware lifecycle
├── 1672 unit tests                 ├── True multi-shift CG          ├── Silicon inventory
└── Remaining: GR ctx, EXEC mask    └── Remaining: sovereign absorb  └── Remaining: scratch routing
```

The trio's capability surface has expanded significantly: AMD scratch memory,
NVIDIA GPFIFO, and silicon saturation profiling are all new since the last handoff.
The next convergence point is **sovereign QCD dispatch** — a Wilson plaquette
trajectory running entirely through coralReef on both cards.

---

*hotSpring v0.6.32 — strandgate — 2026-03-30*
