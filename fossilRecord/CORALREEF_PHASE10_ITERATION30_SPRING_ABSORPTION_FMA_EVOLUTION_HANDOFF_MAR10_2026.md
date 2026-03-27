# coralReef → Ecosystem: Phase 10 Iteration 30 — Spring Absorption + FMA Evolution

**Date:** March 10, 2026  
**From:** coralReef Phase 10, Iteration 30  
**To:** toadStool / barraCuda / hotSpring / neuralSpring / All Springs  
**License:** AGPL-3.0-only  
**Covers:** Iteration 29 → Iteration 30  

---

## Executive Summary

- **Multi-device compile API**: New `shader.compile.wgsl.multi` endpoint — compile one WGSL shader for multiple GPU targets (cross-vendor, up to 64 targets) in a single request; wired through JSON-RPC, Unix socket, and tarpc
- **FMA contraction enforcement**: SPIR-V `NoContraction` now enforced in codegen — `FmaPolicy::Separate` splits `FFma`→`FMul`+`FAdd` and `DFma`→`DMul`+`DAdd` via a new `lower_fma` pass (resolves ISSUE-011 from wateringHole)
- **FMA hardware capability reporting**: `FmaCapability::for_target()` returns per-architecture FMA capabilities (f32/f64 support, recommended policy, throughput ratio)
- **`PCIe` topology awareness**: `probe_pcie_topology()` discovers and groups GPUs by `PCIe` switch for optimal multi-device scheduling
- **Capability self-description evolution**: `shader.compile.multi` advertised with `max_targets: 64`, `cross_vendor: true`; `shader.compile` now includes GLSL input, all NVIDIA+AMD architectures, and `fma_policies`
- **NVVM bypass test hardening**: Validates sovereign compilation across all FMA policies for both NVIDIA and AMD targets
- **1487 tests passing, 0 failed, 76 ignored; zero clippy warnings; clean docs**

---

## Part 1: Multi-Device Compile API (`shader.compile.wgsl.multi`)

### Problem

toadStool S144 identified the need for a multi-device compilation endpoint — compiling the same shader for multiple GPU targets without issuing separate requests. This is critical for heterogeneous multi-GPU systems (e.g. NVIDIA + AMD on the same host).

### Implementation

- `DeviceTarget` struct: target architecture + optional FMA policy override per device
- `MultiDeviceCompileRequest`: WGSL source + array of `DeviceTarget` + optional global `fma_policy`
- `MultiDeviceCompileResponse`: per-target results with binary, architecture, compile time, errors
- `handle_compile_wgsl_multi()`: iterates over targets, compiles independently, collects results
- Wired into JSON-RPC (`CoralReefRpc` trait), Unix socket dispatch, and tarpc (`ShaderCompileTarpc` trait)

### Impact for springs

Any spring can now compile a shader for SM70 + SM86 + RDNA2 in a single IPC call. barraCuda's multi-backend scheduling benefits directly — one request per shader, not one per target.

---

## Part 2: FMA Contraction Enforcement (ISSUE-011)

### Problem

wateringHole ISSUE-011 documented that `FmaPolicy` was wired into `CompileOptions` but never enforced in codegen. `FmaPolicy::Separate` should produce code without fused multiply-add operations, matching SPIR-V `NoContraction` decoration semantics. This matters for numerical reproducibility in scientific computing.

### Implementation

- New `crates/coral-reef/src/codegen/lower_fma.rs` module with `split_ffma()` and `split_dfma()` functions
- `Shader::lower_fma_contractions()` method called in the compilation pipeline
- Pipeline placement: after optimization passes, before `lower_f64_transcendentals` — this ensures only user-originating FMAs are split, preserving the mathematical integrity of f64 transcendental library sequences (which require FMA for correctness)
- `FmaPolicy::Auto` and `FmaPolicy::Fused` preserve all FMA instructions (no-op pass)

### Impact for springs

hotSpring and neuralSpring shaders that require strict `NoContraction` behavior (e.g. compensated summation, Kahan sum) can now request `fma_policy: "separate"` and get bit-reproducible results across different hardware. The f64 transcendental library is unaffected by this policy.

---

## Part 3: FMA Hardware Capability Reporting

### Implementation

- `FmaCapability` struct: `f32_fma` (bool), `f64_fma` (bool), `recommended_policy` (`FmaPolicy`), `f32_fma_throughput_ratio` (f32)
- `FmaCapability::for_target(GpuTarget)`: returns hardware-specific capabilities
  - NVIDIA SM70+: f32 FMA at 1.0 ratio, f64 FMA (DFMA), recommended `Fused`
  - AMD RDNA2+: f32 FMA at 1.0 ratio, f64 via `v_fma_f64`, recommended `Fused`
- `GpuContext::fma_capability()`: exposed on the unified GPU context

### Impact for springs

barraCuda's precision routing can query FMA capabilities before deciding compilation strategy. Springs doing numerical analysis can use this to document expected precision behavior per target.

---

## Part 4: `PCIe` Topology Awareness

### Implementation

- `PcieDeviceInfo` struct: render node path, `PCIe` address, switch group, GPU target
- `probe_pcie_topology()`: discovers all render nodes, reads `PCIe` addresses from sysfs, groups devices sharing the same `PCIe` switch
- `assign_switch_groups()`: groups devices by common `PCIe` bridge prefix

### Impact for springs

Multi-GPU scheduling can now prefer peer-to-peer transfers between GPUs on the same `PCIe` switch, avoiding cross-switch traffic. This is the foundation for topology-aware workload distribution.

---

## Part 5: Codebase Quality Evolution

### Pedantic Rust evolution

- `primal-rpc-client`: removed redundant `Serialize` trait bounds, `const fn` for constructors, `#[expect(dead_code)]` with reason strings
- `coral-driver`: `#[must_use]` annotations, `# Errors` doc sections, `const unsafe fn new`, `std::fmt::Write` refactoring, GPU identity probing extracted to `nv/identity.rs` (962→818 LOC)
- `coral-gpu`: `Option::map_or_else` for idiomatic control flow, `const fn sm_to_nvarch`
- `coralreef-core`: hardcoded `"biomeos"` → `ECOSYSTEM_NAMESPACE` constant
- `#![warn(missing_docs)]` expanded to all crates in workspace

### Capability self-description

- `shader.compile` now advertises: GLSL input format, all `NvArch` + `AmdArch` variants, `fma_policies: ["auto", "fused", "separate"]`
- New `shader.compile.multi` capability: `max_targets: 64`, `cross_vendor: true`

---

## Verification

| Check | Status |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo test --workspace` | PASS (1487 passing, 0 failed, 76 ignored) |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo fmt --check` | PASS |
| `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps` | PASS |
| Unsafe blocks | 17 in coral-driver (kernel ABI only); 0 in 8/9 crates |

---

## Known Gaps (Iteration 31 candidates)

| Gap | Priority | Detail |
|-----|----------|--------|
| Nouveau EINVAL on Volta | P1 | Channel creation rejected — diagnostic suite ready for on-site investigation |
| nvidia-drm UVM compute dispatch | P2 | RM client allocated; next: `UVM_REGISTER_GPU`, buffer mapping |
| Coverage 63% → 90% | P2 | Structural floor from encoder match arms |
| Cross-spring shader corpus expansion | P2 | 84/93 compiling; 9 blocked on Discriminant, vec3\<f64\>, f64 edge cases |
| RDNA3/RDNA4 backend | P3 | Architecture variants defined, encoding path needed |

---

## For hotSpring / Springs

The multi-device compile API means springs can request compilation for all their target GPUs in a single IPC call. FMA contraction enforcement means reproducibility-sensitive shaders (compensated summation, Kahan, BCS bisection) can request `fma_policy: "separate"` with confidence that the compiler will honor the constraint.

The `PCIe` topology awareness lays groundwork for topology-aware multi-GPU scheduling — relevant for any spring doing distributed computation across GPU arrays.

---

*coralReef Iteration 30 — from single-device compilation to multi-device sovereignty, with FMA precision control at every layer.*
