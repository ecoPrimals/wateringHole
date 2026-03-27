# BarraCUDA Primal Budding Proposal — ToadStool S88

**Date**: March 2, 2026
**From**: ToadStool (S88)
**To**: All Springs, NUCLEUS primals, biomeOS
**Classification**: Architectural evolution — RFC for ecosystem feedback

---

## Summary

We propose **budding BarraCUDA into its own primal** — separating the universal
math/GPU compute engine from ToadStool's orchestration runtime. ToadStool becomes
a lighter orchestration primal; BarraCUDA becomes the ecosystem's sovereign math
primal. Springs depend on BarraCUDA directly for compute.

This also opens the door to **other NUCLEUS primals evolving inside Springs**,
since Springs would no longer couple to the full ToadStool workspace to access
GPU compute.

---

## The Problem

BarraCUDA currently lives inside ToadStool as `crates/barracuda/`. It serves two
roles simultaneously:

1. **Universal math library** — 766 WGSL shaders, tensor ops, FHE NTT, linalg,
   spectral analysis, lattice QCD, hydrology pipelines, device management
2. **ToadStool's GPU backend** — tightly coupled with ToadStool's runtime, IPC,
   primal lifecycle

### What this causes

| Symptom | Root Cause | Affected |
|---------|-----------|----------|
| Springs discover breaking changes by compile failure | No SemVer on BarraCUDA | All 5 springs |
| Shader changes recompile ToadStool runtime | Monolithic workspace | ToadStool dev velocity |
| ToadStool IPC changes rerun 2,866 GPU tests | Monolithic workspace | ToadStool dev velocity |
| `SeasonalGpuParams` needs `bytemuck::zeroed()` workaround | API surface unmanaged | groundSpring, airSpring |
| `anderson_4d` implemented but not re-exported | No API review gate | groundSpring |
| 5 springs independently discovering same breakage | No changelog/versioning | All 5 springs |
| Springs pull full ToadStool to use compute primitives | Coupling exceeds need | All 5 springs |

---

## The Proposal

### BarraCUDA becomes a standalone primal

```
ecoPrimals/
├── barracuda/                  ← NEW: standalone primal, own repo
│   ├── crates/
│   │   ├── barracuda-core/     (tensor, device, shader compilation, dispatch)
│   │   ├── barracuda-ops/      (766 shaders, FHE, linalg, spectral, MD, bio)
│   │   └── barracuda-esn/      (multi-head ESN, nautilus bridge)
│   ├── specs/
│   ├── CHANGELOG.md            (SemVer)
│   └── Cargo.toml              (v1.x.y)
│
├── phase1/toadStool/           ← LIGHTER: orchestration + node atomic
│   ├── crates/
│   │   ├── runtime/            (IPC, discovery, biomeOS, primal lifecycle)
│   │   ├── node/               (basic CPU computation, no GPU required)
│   │   └── bridge-barracuda/   (thin integration, depends on barracuda)
│   └── Cargo.toml              (depends on barracuda = "1.x")
│
├── hotSpring/                  ← depends on barracuda directly
├── groundSpring/               ← depends on barracuda directly
├── wetSpring/                  ← depends on barracuda directly
├── neuralSpring/               ← depends on barracuda directly
└── airSpring/                  ← depends on barracuda directly
```

### ToadStool retains

- Primal lifecycle (start, stop, health)
- IPC server (JSON-RPC 2.0 / tarpc)
- biomeOS integration (capability announcement, discovery)
- Node atomic compute (basic CPU math, no GPU required)
- Bridge to BarraCUDA for GPU workloads

### BarraCUDA owns

- GPU device management (wgpu, adapter discovery, device pool)
- All WGSL shaders (766 and growing)
- Tensor operations, ComputeDispatch builder
- FHE (NTT, INTT, pointwise multiplication)
- Linalg (sparse, dense, eigensolvers)
- Spectral analysis (Anderson, Lanczos)
- Molecular dynamics pipeline
- ESN / reservoir computing
- Multi-head ESN, Nautilus bridge
- Domain ops (stats, hydrology, bio, genomics)
- Tolerances and validation harness
- DF64 emulation stack
- Sovereign shader compilation (naga IR, SPIR-V passthrough)

---

## What This Solves

### Compile complexity

| Change | Current (monolithic) | After budding |
|--------|---------------------|---------------|
| Fix a WGSL shader | Recompile barracuda + toadStool runtime + all tests | barracuda only |
| Change ToadStool IPC | Recompile everything incl. barracuda tests | toadStool only |
| Spring updates barracuda usage | Pull entire toadStool | Pin `barracuda = "1.x"` |
| Add new op | Full workspace rebuild | barracuda rebuild only |

### API stability via SemVer

- `barracuda 1.14.0` → `1.15.0`: new `anderson_4d` re-export (minor)
- `barracuda 1.15.0` → `2.0.0`: `SeasonalGpuParams::new()` constructor (breaking)
- Springs see version bump, read changelog, update when ready
- No more silent breakage discovery

### Surface area clarity

- **barracuda** API: tensors, ops, shaders, device management, tolerances
- **toadStool** API: IPC, discovery, biomeOS, primal lifecycle
- Springs don't navigate both to get compute

---

## Crypto: BearDog Enables Sovereign FHE

With BarraCUDA as a separate primal, the crypto dependency model clarifies:

- **BearDog** owns: signing, encryption, key exchange, hashing, genetic lineage,
  beacon discovery (Ed25519, ChaCha20-Poly1305, BLAKE3, X.509, Argon2id)
- **BarraCUDA** owns: GPU-accelerated FHE arithmetic (NTT, INTT, pointwise mod-mul),
  the bit-by-bit modular reduction for u64 on WGSL

BarraCUDA's FHE is the **compute kernel** — it does the number crunching on GPU.
BearDog provides the **cryptographic scaffolding** — key generation, scheme
parameters, encryption/decryption framing. Neither depends on the other at the
crate level; they compose at the primal IPC level.

This is the only cross-vendor FHE-on-GPU implementation in existence. Every other
FHE GPU library (Zama concrete-cuda, HEaaN, cuFHE, Phantom) requires CUDA.
BarraCUDA does FHE NTT on any GPU via WGSL, using 32-bit arithmetic to emulate
64-bit modular reduction. Making it a proper primal surfaces this capability for
any primal in the ecosystem to discover and use.

---

## Enabling Other Primals in Springs

Today, Springs are compute-focused because they couple to ToadStool for BarraCUDA
access. This limits what other primals can evolve in the Spring environment.

With BarraCUDA as a standalone dependency:

| Spring | Current primals evolved | Enabled by budding |
|--------|----------------------|-------------------|
| hotSpring | BarraCUDA ops (physics) | + BearDog FHE integration, Songbird distributed compute |
| groundSpring | BarraCUDA ops (earth science) | + NestGate data pipelines, BearDog provenance signing |
| neuralSpring | BarraCUDA ops (ML/bio) | + Squirrel inference coordination, BearDog model signing |
| wetSpring | BarraCUDA ops (marine bio) | + NestGate genomic vaults, Songbird federated analysis |
| airSpring | BarraCUDA ops (agriculture) | + NestGate sensor archives, Squirrel edge inference |

Springs become **multi-primal evolution environments** instead of compute-only
sandboxes. A Spring can evolve BearDog's beacon protocol alongside GPU shaders.
A Spring can test NestGate's data pipeline feeding into BarraCUDA's GPU analysis.

The constraint today is that Springs pull ToadStool (heavy, orchestration-focused)
to get BarraCUDA (what they actually use). Remove that coupling, and Springs can
pull exactly the primals they need.

---

## FHE + Lattice QCD as GPU Validation Canary

BarraCUDA as its own primal crystallizes an insight from S87: FHE and lattice QCD
together form a mathematically rigorous GPU stack validation suite.

| Domain | Validates | Correctness type |
|--------|----------|-----------------|
| FHE NTT round-trip | u32/u64 emulation, modular arithmetic | Exact — zero tolerance |
| FHE polynomial mul | Buffer pipeline, dispatch, shader compilation | Bit-perfect deterministic |
| SU(3) unitarity | DF64 matrix multiply, complex arithmetic | Continuous invariant |
| Plaquette expectation | Full pipeline under sustained load | Physics ground truth |
| CG convergence rate | Iterative solver precision | Sensitivity diagnostic |

A standalone `barracuda validate-gpu` binary that runs both suites would give
any consumer (Spring or primal) a single gate: "is this GPU trustworthy for
scientific compute?" This is more rigorous than per-op parity tests.

---

## Migration Path

### Phase 0 — Preparation (current session)

- [x] This handoff document
- [x] Update ToadStool specs with budding plan
- [ ] Audit `toadstool-core` ↔ `barracuda` coupling surface

### Phase 1 — Clean boundary

- [ ] Ensure barracuda compiles standalone (`cargo check -p barracuda` without
      toadstool-core features)
- [ ] Move `toadstool-core` dependency behind a feature flag in barracuda
- [ ] Extract shared types to a thin `barracuda-types` crate if needed

### Phase 2 — Repo extraction

- [ ] Create `ecoPrimals/barracuda/` repository
- [ ] Move `crates/barracuda/` contents
- [ ] Set up independent CI (fmt, clippy, test, cross-vendor GPU)
- [ ] Publish first SemVer release (1.0.0)

### Phase 3 — Spring rewiring

- [ ] Springs update `Cargo.toml` to depend on barracuda directly
- [ ] ToadStool runtime depends on barracuda as versioned dep
- [ ] Path deps for local development, published for releases
- [ ] Update wateringHole handoff protocol for barracuda versioning

### Phase 4 — Multi-primal Springs

- [ ] Springs add BearDog, NestGate, Songbird deps as needed
- [ ] Spring handoffs evolve to cover multiple primals per session
- [ ] Cross-primal integration tests in Springs

---

## API Contract (Draft)

What BarraCUDA 1.0.0 would guarantee:

### Stable (SemVer-protected)

- `Tensor`, `WgpuDevice`, `DeviceContext`
- `ComputeDispatch` builder
- `compile_shader_universal()`, `compile_shader_f64()`
- `barracuda::tolerances::*`
- `barracuda::error::{BarracudaError, Result}`
- `barracuda::spectral::*` (all re-exports)
- `barracuda::stats::*`
- `barracuda::linalg::*`
- `barracuda::bio::*`
- `barracuda::ops::fhe_ntt::*`, `fhe_pointwise_mul::*`
- `MultiHeadEsn`, `ESN`
- `BatchedStatefulF64`, `UnidirectionalPipeline`, `StatefulPipeline`

### Unstable (feature-gated, may change)

- `barracuda::npu::*` (NPU driver layer, hardware-dependent)
- `barracuda::vision::*` (early stage)
- `barracuda::snn::*` (spiking networks, experimental)
- Internal shader compilation details

---

## What We Need From Springs

1. **Feedback on this proposal** — Does budding help or hurt your workflow?
2. **Coupling audit** — Which barracuda APIs do you use? Any undocumented paths?
3. **Breaking tolerance** — Can you handle a one-time migration to `barracuda = "1.0"`?
4. **Multi-primal interest** — Which other primals would you evolve in your Spring?

---

## References

- S87 deep debt session: FHE shader fixes, test hardening, unsafe audit
- S86 ComputeDispatch evolution: 144 ops migrated
- `SOVEREIGN_COMPUTE_EVOLUTION.md`: BarraCUDA as "unified math language"
- `UNIVERSAL_IPC_EVOLUTION_HANDOFF.md`: JSON-RPC 2.0 primal protocol
- `BEARDOG_BEACON_EVOLUTION_FEB04_2026.md`: BearDog crypto capabilities
- Cross-spring shader evolution docs (groundSpring, wetSpring, hotSpring, airSpring, neuralSpring)
