# Compute Trio Wave 8 — Node Atomic Evolution Handoff

**Date**: May 11, 2026
**From**: primalSpring (L2 gate)
**To**: toadStool, coralReef, barraCuda, hotSpring teams
**Status**: Local sketch complete — upstream implementation pending

---

## Summary

Wave 8 defines the compute trio (coralReef + toadStool + barraCuda) as the
Node atomic's sovereign compute pipeline. primalSpring has sketched the
architecture, defined IPC contracts, created validation scenarios, gate tests,
and deploy graphs locally. This handoff provides upstream teams with contracts
and expectations for their implementation work.

## The HOW / WHERE / WHAT Domain Split

| Domain | Primal | Owns | IPC Surface |
|--------|--------|------|-------------|
| **HOW** (compiler) | coralReef | WGSL → naga IR → SASS/ISA compilation | `shader.compile.wgsl`, `shader.compile.spirv`, `shader.compile.capabilities` |
| **WHERE** (hardware) | toadStool | Device lifecycle, VFIO, GPFIFO, dispatch | `compute.dispatch.submit`, `compute.capabilities`, `compute.status` |
| **WHAT** (math) | barraCuda | 826+ WGSL shaders, tensor ops, statistics | `tensor.*`, `stats.*`, `math.*`, `noise.*` |

Key principle: **neither primal links the other's crate**. All composition
is JSON-RPC over IPC. This follows the provenance trio precedent
(rhizoCrypt + loamSpine + sweetGrass).

## Sovereign Dispatch E2E Contract

```
barraCuda → shader.compile.wgsl → coralReef
         → returns {binary_b64, shader_info}
         → compute.dispatch.submit → toadStool
         → returns {dispatch_id, status, buffers, timing}
```

### shader.compile.wgsl

Request: `{ source, target, entry_point, workgroup_size }`
Response: `{ binary_b64, shader_info: { gprs, shared_memory, barriers, workgroup, wave_size, local_memory }, target, compile_time_ms }`

### compute.dispatch.submit

Request: `{ binary_b64, shader_info, dispatch_dims, buffers: [{ binding, data_b64, size, usage }], target_bdf? }`
Response: `{ dispatch_id, status, buffers: [{ binding, data_b64 }], timing: { dispatch_ms, readback_ms } }`

## Ember/Glowplug Absorption Path (toadStool)

toadStool absorbs coralReef's hardware-domain components in 6 phases:

1. **coral-ember** (228 tests): `HeldDevice` → `ResourceHandle`, device hold/release, swap journal
2. **coral-glowplug** (436 tests): `sovereign_boot` → `SwapOrchestrator`, personality detection
3. **coral-driver hardware**: BAR0/MMIO, VFIO channel, DRM ioctl wrappers
4. **Validate generalization**: Akida NPU, AMD RDNA, Intel Arc
5. **Generalize cylinder**: per-GPU → per-device subprocess isolation
6. **Serve compute.dispatch.execute**: universal dispatch entry point

Known issue: BrainChip vendor ID mismatch (0x1e96 vs 0x1E7C) — reconcile in Phase 4.

## primalSpring Validation Surface (shipped locally)

| Item | What | File |
|------|------|------|
| Architecture doc | HOW/WHERE/WHAT split, IPC contracts, absorption path | `docs/COMPUTE_TRIO_EVOLUTION.md` |
| Scenario | 5-phase sovereign dispatch contract test | `s_compute_triangle.rs` (evolved) |
| Gate tests | 4 new: capabilities + math round-trip + E2E | `server_ecosystem_compose.rs` |
| Deploy graph | 6-phase health + capabilities + math smoke | `compute_trio_smoke.toml` |
| gen4 sketch | Composition pattern + warm-catch sovereignty | `whitePaper/gen4/.../SOVEREIGN_COMPUTE_TRIO_SKETCH.md` |
| Inverse drift | Compute domain coverage audit (5 aliases uncovered) | `check_method_coverage.sh` output |

## Per-Team Handoff

### toadStool

**What primalSpring provides**: Architecture doc, IPC contract definitions
(`compute.dispatch.submit` shape), gate test expectations (Gate 2 + Gate 4),
deploy graph with `compute.capabilities` verification.

**What toadStool does**: Absorb ember/glowplug (Phases 1-3), wire
`compute.dispatch.execute`, validate on Akida/AMD/Intel, generalize cylinder
from per-GPU to per-device subprocess isolation.

### coralReef

**What primalSpring provides**: Domain split boundary (compiler-only after
absorption), `shader.compile.*` contract shape expectations (Gate 1).

**What coralReef does**: Keep compiler domain (`shader.compile.wgsl`,
`shader.compile.spirv`, `shader.compile.capabilities`), extract hardware
code (coral-ember, coral-glowplug, coral-driver hardware access) to
toadStool. After extraction, coralReef is a pure compiler primal.

### barraCuda

**What primalSpring provides**: Sovereign dispatch E2E contract (compile →
dispatch → readback), `stats.mean` gate test expectations (Gate 3).

**What barraCuda does**: Absorb bearDog crypto IPC (Wave 101 shipped the
IPC surface), wire `SovereignDevice` through trio IPC for sovereign dispatch,
exercise the 4-tier degradation model (sovereign GPU → wgpu → CPU → scalar).

### hotSpring

**What primalSpring provides**: Compute trio smoke graph, validation scenarios.

**What hotSpring does**: Continue local dispatch validation on Titan V + K80
via warm-catch pipeline, exercise `sovereign-dispatch` with real GPU hardware.

## References

- `primalSpring/docs/COMPUTE_TRIO_EVOLUTION.md`
- `primalSpring/docs/PRIMAL_GAPS.md` (Wave 8 section)
- `primalSpring/graphs/spring_validation/compute_trio_smoke.toml`
- `whitePaper/gen4/architecture/SOVEREIGN_COMPUTE_TRIO_SKETCH.md`
- `wateringHole/handoffs/SOVEREIGN_COMPUTE_THREE_GPU_WARM_CATCH_HANDOFF_MAY11_2026.md`
