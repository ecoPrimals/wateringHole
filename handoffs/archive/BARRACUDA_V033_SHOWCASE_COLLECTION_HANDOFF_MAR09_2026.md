# barraCuda v0.3.3 — Showcase Collection

**Date**: March 9, 2026
**From**: barraCuda
**To**: coralReef, toadStool, all springs, all primals
**Type**: Showcase / Demonstration Handoff

---

## Summary

barraCuda now has a `showcase/` directory with 10 progressive demos across 3
tiers, following ecosystem conventions. Demos progress from standalone local
capabilities through IPC protocol to the cross-primal compute triangle
(toadStool + barraCuda + coralReef). All cross-primal demos degrade gracefully
when other primals are absent.

---

## What Changed

### showcase/ Directory Structure

```
showcase/
├── README.md
├── 00-local-primal/
│   ├── 01-device-discovery/      GPU caps, precision routing, workgroup sizing
│   ├── 02-precision-tiers/       F32 vs F64 vs DF64 on identical math
│   ├── 03-fused-gpu-ops/         Welford, correlation, GpuView chains
│   └── 04-science-shaders/       Hill kinetics, tolerances, metrics, inventory
├── 01-ipc-protocol/
│   ├── 01-jsonrpc-server/        Start server, exercise 6 JSON-RPC methods
│   └── 02-doctor-validate/       Health diagnostics, GPU validation canary
└── 02-cross-primal-compute/
    ├── 01-coralreef-shader-compile/  WGSL → coralReef native (graceful fallback)
    ├── 02-toadstool-hw-discovery/    Hardware inventory → GPU selection
    └── 03-sovereign-pipeline/        Full pipeline capstone
```

### Tier 0: Local Primal (standalone, no other primals needed)

| Demo | What It Shows |
|------|---------------|
| 01-device-discovery | `WgpuDevice::new()`, `DeviceCapabilities`, `GpuDriverProfile`, `Fp64Strategy` |
| 02-precision-tiers | `VarianceF64::mean_variance()` at F32/F64, error analysis vs CPU reference |
| 03-fused-gpu-ops | Fused Welford, fused 5-accumulator correlation, `GpuViewF64` zero-readback |
| 04-science-shaders | `hill_activation`, `nash_sutcliffe`, tolerance tiers, epsilon guards |

### Tier 1: IPC Protocol (shell scripts + barracuda binary)

| Demo | What It Shows |
|------|---------------|
| 01-jsonrpc-server | Server start, 6 methods: `primal.info`, `capabilities`, `device.list`, `health`, `tolerances`, `validate` |
| 02-doctor-validate | `barracuda doctor`, `barracuda validate`, `barracuda version` |

### Tier 2: Cross-Primal Compute (the compute triangle)

| Demo | What It Shows |
|------|---------------|
| 01-coralreef-shader-compile | `GLOBAL_CORAL.health()`, `compile_wgsl_direct()`, `arch_to_coral()` |
| 02-toadstool-hw-discovery | `$XDG_RUNTIME_DIR/ecoPrimals/` scan, capability-based discovery |
| 03-sovereign-pipeline | Full: discover → route precision → compile → dispatch → validate |

---

## Cross-Primal Patterns Demonstrated

### barraCuda → coralReef (01-coralreef-shader-compile)

```
1. GLOBAL_CORAL.health() → probe shader.compile.status
2. arch_to_coral(profile.arch) → "sm_70" / "gfx1030" / None
3. compile_wgsl_direct(wgsl, arch, fp64) → Some(CoralBinary) or None
4. Fallback: wgpu SPIR-V path (always available)
```

### toadStool → barraCuda (02-toadstool-hw-discovery)

```
1. Scan $XDG_RUNTIME_DIR/ecoPrimals/*.json for "hardware_discovery" capability
2. If found: query toadStool for rich hardware profile (NPU, multi-GPU)
3. If not: barraCuda discovers GPUs locally via wgpu
4. Select best GPU, route precision, dispatch shaders
```

### Full Pipeline (03-sovereign-pipeline)

```
Layer 1: Hardware  → toadStool (or barraCuda local)
Layer 2: Compiler  → coralReef native (or wgpu/naga/SPIR-V)
Layer 3: Dispatch  → GPU via wgpu
Each layer degrades independently. The math never changes.
```

---

## What Other Primals Should Know

- **toadStool**: The showcase probes for your discovery manifest. If you're
  running, `02-toadstool-hw-discovery` will find you via capability scan.
  barraCuda never hardcodes your name or port.
- **coralReef**: The showcase probes `shader.compile.status` via `GLOBAL_CORAL`.
  If you're running, `01-coralreef-shader-compile` will attempt WGSL compilation
  via your Phase 10 IPC.
- **All primals**: The showcase follows ecosystem conventions (numbered subdirs,
  `demo.sh` scripts, standalone Cargo crates). Use as a reference for your own
  showcase structure.
- **Springs**: `04-science-shaders` demonstrates the tolerance architecture
  and Hill kinetics that springs consume.

---

## Quality Gates

| Gate | Status |
|------|--------|
| All 6 Cargo crates compile | Pass (zero warnings) |
| Shell scripts executable | Pass |
| Main workspace unaffected | Pass (`cargo check --workspace` clean) |
| Showcase excluded from workspace | Pass (explicit `members` list) |
| Cross-primal demos degrade | Pass (tested without toadStool/coralReef) |

---

## Files Created

| Path | Type | Lines |
|------|------|-------|
| `showcase/README.md` | doc | 55 |
| `showcase/00-local-primal/01-device-discovery/` | Cargo crate | ~100 |
| `showcase/00-local-primal/02-precision-tiers/` | Cargo crate | ~120 |
| `showcase/00-local-primal/03-fused-gpu-ops/` | Cargo crate | ~140 |
| `showcase/00-local-primal/04-science-shaders/` | Cargo crate | ~130 |
| `showcase/01-ipc-protocol/01-jsonrpc-server/` | shell + readme | ~85 |
| `showcase/01-ipc-protocol/02-doctor-validate/` | shell + readme | ~55 |
| `showcase/02-cross-primal-compute/01-coralreef-shader-compile/` | Cargo crate | ~135 |
| `showcase/02-cross-primal-compute/02-toadstool-hw-discovery/` | shell + readme | ~95 |
| `showcase/02-cross-primal-compute/03-sovereign-pipeline/` | Cargo crate | ~150 |
