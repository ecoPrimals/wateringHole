<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Compute Trio — Spring Integration Guide

**Date**: March 30, 2026
**Version**: 1.0.0
**Audience**: All springs, primalSpring coordinators
**Primals**: barraCuda v0.3.11, coralReef Iter 70, toadStool S168

---

## Overview

The **Compute Trio** (barraCuda + coralReef + toadStool) provides sovereign
GPU computation. Each primal owns one axis:

| Primal | Role | What It Owns |
|--------|------|-------------|
| **barraCuda** | The Math | WGSL shaders, precision tiers, tolerances, `PrecisionBrain` routing, `op_preamble` WGSL |
| **coralReef** | The Compiler | WGSL/SPIR-V → native GPU binary (SASS/GFX), ISA tables, compilation strategies |
| **toadStool** | The Hardware | VFIO dispatch, DMA, GPU lifecycle, tensor cores, RT cores, silicon exposure |

Springs consume barraCuda directly (library or IPC). The trio coordinates
internally — springs should never call coralReef or toadStool for math.

---

## Decision Tree: How To Use The Trio

```
Does your spring need GPU math?
  ├─ YES: Add barracuda as a cargo dependency
  │   ├─ Need specific precision? → Use PrecisionBrain::recommend(domain)
  │   ├─ Need native compilation? → Enable sovereign-dispatch feature
  │   ├─ Need multi-GPU? → Use GpuPool / MultiDevicePool
  │   └─ Need custom shaders? → Use compute.dispatch IPC method
  └─ NO: You don't need the trio
```

### Library Path (Fastest, No IPC)

```toml
# Full — all domains
barracuda = { path = "../barraCuda/crates/barracuda" }

# Math + GPU only — no domain models (fastest compile)
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false, features = ["gpu"] }

# Pure CPU math — no GPU at all
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false }
```

### IPC Path (Runtime Discovery)

```bash
# Start barraCuda
barracuda server --bind 127.0.0.1:9000

# Call from any language
echo '{"jsonrpc":"2.0","id":1,"method":"compute.dispatch","params":{"op":"zeros","shape":[1024]}}' | nc localhost 9000
```

---

## The 15-Tier Precision Continuum

barraCuda defines precision. Springs select a `PhysicsDomain` and
`PrecisionBrain` routes to the optimal tier:

```
Scale-down (throughput)           Baseline       Scale-up (precision)
Binary→Int2→Q4→Q8→FP8→BF16→F16→TF32 → F32 → DF64→F64→F64Precise→QF128→DF128
```

### Common Spring Patterns

| Spring Need | PhysicsDomain | Expected Tier | Why |
|-------------|---------------|---------------|-----|
| ML inference | `Inference` | `Quantized4` | GGML-class throughput |
| Neural training | `Training` | `Bf16` | Brain float, gradient stability |
| Content hashing | `Hashing` | `Binary` | 1-bit sufficient |
| Molecular dynamics | `MolecularDynamics` | `F64` or `DF64` | Force accuracy |
| Lattice QCD | `LatticeQcd` | `F64Precise` | FMA-separate required |
| Spectral theory | `Spectral` | `F64` | Eigenvalue accuracy |
| Statistics | `Statistics` | `F32` | Sufficient for bootstrap |
| FHE crypto | `Fhe` | `F32` | u32 modular arithmetic |
| Precision reference | `LatticeQcd` | cascades to `DF128` | Maximum available |

### How Precision Routing Works

```rust
use barracuda::device::{PrecisionBrain, PhysicsDomain, HardwareCalibration};

// PrecisionBrain probes hardware at startup
let cal = HardwareCalibration::from_capabilities(&device);
let brain = PrecisionBrain::new(&cal);

// Route your domain — O(1) lookup
let tier = brain.route(PhysicsDomain::MolecularDynamics);
// On RTX 3090: DF64 (f64 throttled, DF64 available)
// On Titan V:  F64 (native f64 at full rate)
// On llvmpipe: F32 (no f64 support)
```

Springs **never** select tiers manually. `PrecisionBrain` handles hardware
quirks (NVVM poisoning, f64 throttling, driver bugs) transparently.

---

## Trio Communication Protocol

### Compile → Dispatch Chain

```
Spring → barraCuda.compute.dispatch(wgsl, precision_tier)
  → barraCuda selects op_preamble for tier
  → barraCuda → coralReef: shader.compile.wgsl(source, strategy)
  → coralReef returns compiled binary
  → barraCuda → toadStool: compute.dispatch.submit(binary, workgroups)
  → toadStool dispatches via VFIO
  → Result returns to spring
```

### Error Recovery Chain

```
Spring calls compute.dispatch
  → ShaderCompilation error?
    → PrecisionBrain cascades to lower tier, recompiles via coralReef
  → DeviceLost?
    → toadStool discovers alternative GPU
    → coralReef recompiles for new architecture
    → barraCuda re-dispatches
  → VRAM exhaustion?
    → barraCuda halves batch size, re-dispatches
```

Springs see a single call. The trio self-heals.

---

## What Springs Should NOT Do

1. **Do not call coralReef directly** for shader compilation — barraCuda
   handles the `shader.compile` IPC. coralReef is barraCuda's compiler.
2. **Do not call toadStool directly** for GPU dispatch — barraCuda handles
   routing through `SovereignDevice`.
3. **Do not hardcode precision tiers** — use `PrecisionBrain::recommend()`.
4. **Do not write raw WGSL** unless barraCuda lacks the operation — check
   the 816 shader library first.
5. **Do not parse primal names** — use capability-based discovery.

---

## Spring Feature Matrix

| Feature | Library Path | IPC Path | Sovereign Path |
|---------|-------------|----------|----------------|
| Math operations | Direct Rust API | JSON-RPC | JSON-RPC |
| Precision routing | `PrecisionBrain` | `device.probe` | `PrecisionBrain` |
| Multi-GPU | `GpuPool` | Not yet | `SovereignDevice` |
| Custom shaders | `compile_shader()` | `compute.dispatch` | `shader.compile` → dispatch |
| Tensor ops | `GpuViewF64` | `tensor.*` methods | `GpuViewF64` |
| FHE | `ops::fhe::*` | `fhe.ntt` / `fhe.pointwise_mul` | Same |
| Zero-copy chains | `GpuView` pipeline | N/A | `GpuView` pipeline |

---

## Guidance for primalSpring Coordinators

When coordinating spring evolution that touches GPU compute:

1. **Math gaps** → file against barraCuda. If a spring needs a shader that
   doesn't exist, barraCuda absorbs it.
2. **Compilation gaps** → file against coralReef. If a strategy string isn't
   implemented, coralReef absorbs it.
3. **Hardware gaps** → file against toadStool. If silicon features aren't
   exposed, toadStool absorbs it.
4. **Integration gaps** → file against the spring. The trio provides
   primitives; springs compose them.

### Version Compatibility

| barraCuda | coralReef | toadStool | Notes |
|-----------|-----------|-----------|-------|
| v0.3.11+ | Iter 70+ | S168+ | Full 15-tier support |
| v0.3.5–0.3.10 | Iter 50+ | S156+ | 4-tier precision (F32/DF64/F64/F64Precise) |
| < v0.3.5 | Any | Any | Legacy, pre-typed-errors |

---

## References

- `barraCuda/specs/PRECISION_TIERS_SPECIFICATION.md` — 15-tier ladder spec
- `barraCuda/specs/ARCHITECTURE_DEMARCATION.md` — barraCuda/toadStool boundaries
- `wateringHole/BARRACUDA_LEVERAGE_GUIDE.md` — Full leverage patterns
- `wateringHole/CORALREEF_LEVERAGE_GUIDE.md` — coralReef integration
- `wateringHole/TOADSTOOL_LEVERAGE_GUIDE.md` — toadStool integration
- `wateringHole/STANDARDS_AND_EXPECTATIONS.md` §5 — GPU & numerical standards

---

*The spring sees one call. The trio handles the rest.*
