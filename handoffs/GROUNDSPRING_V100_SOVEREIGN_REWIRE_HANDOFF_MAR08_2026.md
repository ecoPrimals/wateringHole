<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# groundSpring V100 — Sovereign Pipeline Rewire Handoff

**Date**: March 8, 2026
**From**: groundSpring V100 (940+ tests, 102 delegations, 0 failures, sovereign dispatch wired)
**To**: barraCuda team, toadStool team, coralReef team
**Supersedes**: V99 NUCLEUS Live Handoff
**Synced against**: barraCuda `a898dee`, toadStool S130+ (`bfe7977b`), coralReef Iteration 11 (`d29a734`+)
**License**: AGPL-3.0-only

## Executive Summary

groundSpring V100 begins the **sovereign pipeline rewire** in response to
coralReef Phase 10 reaching E2E verified status. The dispatch layer now
recognizes `SubstrateKind::Sovereign` as a first-class compute target,
prioritized above wgpu GPU dispatch. The coralReef `coral-gpu` API
(`GpuContext::auto()` → `compile_wgsl` → `alloc` → `dispatch` → `sync` → `readback`)
is documented and the integration path is clear.

**What changed since V99:**

- **Sovereign substrate kind**: `SubstrateKind::Sovereign` added to dispatch,
  topology, and workload routing. Sovereign GPUs are preferred over wgpu GPUs.
- **`SovereignCompile` capability**: New capability for substrates that can
  compile WGSL via coralReef without vendor toolchains.
- **Dispatch priority evolved**: Sovereign (NativeF64 first) → wgpu GPU → NPU → CPU.
- **Topology wiring**: Sovereign-to-GPU links classified as PCIe peer.
- **4 new dispatch tests** verifying sovereign priority, f64 preference,
  and fallback chain ordering.
- **`cargo fmt` fixed** (3 pre-existing formatting issues resolved).
- **Stale provenance comment** in `validate_et0_methods.rs` fixed.
- **GPU module docs** updated with coralReef sovereign pipeline architecture.
- **Zero clippy warnings** (pedantic + nursery).
- **940+ tests pass**, 0 failures.

## 1. Sovereign Pipeline Architecture

```
WGSL shader
     │
     ▼
┌────────────────────┐
│  coral-reef        │  WGSL → naga IR → SSA → native binary
│  (compiler)        │  NVIDIA SM70–SM89, AMD RDNA2+
└────────┬───────────┘
         ▼
┌────────────────────┐
│  coral-driver      │  DRM ioctl dispatch (amdgpu, nouveau)
│  (userspace)       │  alloc → upload → dispatch → sync → readback
└────────┬───────────┘
         ▼
┌────────────────────┐
│  coral-gpu         │  Unified compile + dispatch API
│  GpuContext::auto()│  Auto-detects AMD/NVIDIA via DRM render nodes
└────────────────────┘
```

**Status**: AMD RX 6950 XT (RDNA2/GFX1030) E2E verified. NVIDIA nouveau
wired but not hardware-validated. 991 tests (954 passing, 37 hardware-ignored).

## 2. What groundSpring Wired

### Substrate Layer (`metalForge/forge/src/substrate.rs`)

- `SubstrateKind::Sovereign` — GPU via coralReef DRM, no vendor drivers
- `Capability::SovereignCompile` — can compile WGSL without vendor toolchains

### Dispatch Layer (`metalForge/forge/src/dispatch.rs`)

Priority order for f64 workloads:
1. Sovereign + NativeF64 (e.g. Titan V via coralReef nouveau)
2. Sovereign (e.g. RX 6950 XT via coralReef amdgpu)
3. wgpu GPU + NativeF64
4. wgpu GPU
5. NPU
6. CPU

### Topology Layer (`metalForge/forge/src/topology.rs`)

Sovereign ↔ GPU links treated as PCIe peer (same bus, different drivers).

### GPU Module (`crates/groundspring/src/gpu.rs`)

Documented the coralReef integration path. When barraCuda absorbs
`ComputeDispatch::CoralReef`, this module adds a sovereign device
fallback: coralReef DRM → wgpu Vulkan → CPU.

## 3. What Remains (coralReef Integration)

### P0: barraCuda `ComputeDispatch::CoralReef` (barraCuda-owned)

barraCuda needs a `CoralReefDevice` backend that wraps `coral-gpu::GpuContext`
behind the same `WgpuDevice` trait. This is the single blocker for
groundSpring to dispatch compute through the sovereign path.

### P1: coralReef NVIDIA Hardware Validation

NVIDIA nouveau compute dispatch can freeze the system (Titan V).
coralReef needs validated dispatch on at least one NVIDIA GPU before
groundSpring enables `SubstrateKind::Sovereign` for NVIDIA targets.

### P2: FMA Policy Wiring

coralReef supports `FmaPolicy::NoContraction` for bit-exact CPU parity.
groundSpring's validation binaries should pass `NoContraction` when
comparing sovereign GPU results against CPU baselines.

### P2: Sovereign Probe in `metalForge/forge/src/probe.rs`

Add coralReef discovery to the hardware probe:
1. Check for `/dev/dri/renderD*` + DRM driver name
2. Try `coral_gpu::GpuContext::auto()`
3. If successful, emit `SubstrateKind::Sovereign` with capabilities

## 4. Quality Gates

```
cargo fmt --check                         → PASS
cargo clippy --workspace --all-targets    → 0 warnings (pedantic + nursery)
cargo test --workspace                    → 940+ passed, 0 failed
cargo doc --workspace --no-deps           → PASS
AGPL-3.0-only, SPDX headers              → 133/133 .rs files
```

## 5. Evolution Requests

| Priority | Request | Team | Status |
|----------|---------|------|--------|
| **P0** | `ComputeDispatch::CoralReef` backend | barraCuda | New |
| **P0** | Reclassify Ada Lovelace as `F64NativeNoSharedMem` | barraCuda | Open (V97) |
| **P1** | NVIDIA hardware validation for coralDriver | coralReef | New |
| **P1** | Runtime GPU reduction smoke test in `ComputeDispatch` | toadStool | Open (V97) |
| **P2** | `FmaPolicy::NoContraction` wiring for validation | barraCuda + groundSpring | New |
| **P2** | GPU tridiagonal eigenvector solver | barraCuda | Open (V97) |
| **P2** | Sovereign probe in metalForge | groundSpring | New |

## 6. Cross-Spring Notes

The `SubstrateKind::Sovereign` pattern is portable to all springs. Any spring
using metalForge-style dispatch can adopt the same priority chain. The coralReef
`coral-gpu` API is vendor-agnostic — same `GpuContext` works for AMD and NVIDIA.

*This handoff is unidirectional: groundSpring → ecosystem. No response expected.*
