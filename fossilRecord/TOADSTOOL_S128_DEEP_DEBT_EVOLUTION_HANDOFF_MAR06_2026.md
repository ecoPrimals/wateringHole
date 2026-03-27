# SPDX-License-Identifier: AGPL-3.0-or-later

# toadStool S128 — Deep Debt Evolution Handoff

**Date**: March 6, 2026
**From**: toadStool S128 (0 clippy warnings, 0 test failures, ~85% line coverage)
**To**: barraCuda team (compute math), coralReef team (sovereign compiler), ecoPrimals ecosystem
**License**: AGPL-3.0-or-later

---

## Executive Summary

toadStool S128 absorbs the critical f64 shared-memory bug discovery from groundSpring V84-V85,
adds shader compilation IPC for the coralReef pipeline, and evolves deep debt items including
hardcoded capability lists, architecture stubs, and runtime backend discovery.

---

## 1. GPU Adapter Evolution (groundSpring V84-V85 Absorption)

### 1.1 f64 Shared-Memory Bug

**Discovery**: groundSpring V84-V85 found that naga/SPIR-V f64 shared-memory reductions
return zeros on ALL tested GPUs — both NVIDIA proprietary and NVK drivers. f64 element-wise
arithmetic works. f32 shared-memory works. DF64 paths work. The bug is in the naga→SPIR-V
pipeline for f64 workgroup shared memory.

**New field**: `GpuAdapterInfo::f64_shared_memory_reliable: bool`
- Currently `false` for ALL adapters via the standard wgpu/naga pipeline
- Will become `true` when coralDriver provides native binary submission

### 1.2 sovereign_binary_capable

**New field**: `HardwareFingerprint::sovereign_binary_capable: bool`
- `false` until coralDriver reaches production
- Tracks whether coralReef can compile SPIR-V → native binaries and coralDriver can submit

### 1.3 PrecisionRoutingAdvice

**New enum**: `PrecisionRoutingAdvice` with four variants:
- `F64Native` — f64 works for everything including shared-memory reductions
- `F64NativeNoSharedMem` — f64 element-wise ok, but shared-memory reductions fail
- `Df64Only` — all f64 unreliable (NVK Volta)
- `F32Only` — no f64 support

**New method**: `GpuAdapterInfo::precision_routing() -> PrecisionRoutingAdvice`

**Action for barraCuda**: Call `adapter_info.precision_routing()` to select compute path.
When result is `F64NativeNoSharedMem`, route reduction kernels through DF64 but allow
element-wise f64 kernels to run natively.

### 1.4 Exported Types

`HardwareFingerprint`, `PrecisionRoutingAdvice`, `SubstrateCapabilityKind` are now exported
from `runtime/universal/src/backends/mod.rs` for cross-crate use.

---

## 2. Shader Compile IPC (coralReef Pipeline)

Four new `shader.compile.*` JSON-RPC methods prepare the IPC path for coralReef integration:

| Method | Purpose | Parameters |
|--------|---------|------------|
| `shader.compile.wgsl` | Submit WGSL for compilation | `source` (required) |
| `shader.compile.spirv` | Submit SPIR-V binary | `spirv_binary` (required) |
| `shader.compile.status` | Check compilation status | `compile_id` |
| `shader.compile.capabilities` | Query compiler pipeline | None |

**Current state**: Routes through naga WGSL→SPIR-V pipeline. coralReef integration will
add native binary compilation when `shader.compile.capabilities` reports `coral_reef_available: true`.

**Action for coralReef team**: When coralReef tarpc service is ready, these handlers should
proxy to `tarpc.compiler.compile()`. The `shader.compile.capabilities` response should be
updated to reflect `coral_reef_available: true` and `source_languages: ["wgsl", "spirv"]`.

---

## 3. Capability-Based Evolution (Deep Debt)

### 3.1 Dynamic Capability Discovery

`discover_capabilities` method now builds its method list dynamically from the
`SemanticMethodRegistry`. Adding new methods to the registry automatically updates
the capability advertisement — no more maintaining a hardcoded JSON array.

### 3.2 Runtime Backend Discovery

`science.gpu.capabilities` and `gpu.info` now use `query_available_backends()` which
probes the host at runtime:
- `/proc/driver/nvidia` → vulkan
- `/dev/dri` → vulkan (Linux)
- Platform detection for Metal (macOS) / DX12 (Windows)

Removes the hardcoded `["vulkan", "metal", "dx12"]` that was returned regardless of platform.

### 3.3 Precision Notes in GPU Capabilities

`science.gpu.capabilities` response now includes `precision_notes`:
```json
{
  "precision_notes": {
    "f64_shared_memory_reliable": false,
    "f64_native_element_wise": true,
    "df64_reductions": true,
    "routing_advice": "Use DF64 for shared-memory reductions until coralDriver is available"
  },
  "sovereign_binary_pipeline": false
}
```

---

## 4. Architecture Stubs → Typed Implementations

### 4.1 common::auth

Evolved from empty module to:
- `TrustLevel` enum: `Untrusted → LocalPeer → Authenticated → MutuallyVerified` (ordered)
- `CapabilityToken` struct: issuer, capabilities, expiry with `is_expired()` and `has_capability()` methods
- Full test coverage (4 tests)

### 4.2 common::scheduling

Evolved from empty module to:
- `SchedulingPriority` enum: `Background → Normal → High → Critical` (ordered)
- `PlacementConstraint` struct: capability name + minimum resource
- `SchedulingDecision` enum: `ExecuteLocal` / `Delegate { endpoint }` / `Reject { reason }`
- Full test coverage (4 tests)

Both modules export types via `common::mod.rs` for use across the distributed crate.

---

## 5. Semantic Method Registry

Expanded from 66 → 70 methods:
- `shader.compile.wgsl`
- `shader.compile.spirv`
- `shader.compile.status`
- `shader.compile.capabilities`

Total direct + semantic JSON-RPC methods: 61+

---

## 6. Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | 0 diffs |
| `cargo clippy --workspace` | 0 warnings |
| All tests | 0 failures |
| New tests added | +25 (GPU adapter: 6, server handler: 6, semantic: 4, auth: 4, scheduling: 4, gpu_system: 1) |

---

## 7. Files Changed

| File | Changes |
|------|---------|
| `runtime/universal/src/backends/wgpu_backend.rs` | +f64_shared_memory_reliable, +sovereign_binary_capable, +PrecisionRoutingAdvice, +precision_routing(), test refactoring |
| `runtime/universal/src/backends/mod.rs` | Export HardwareFingerprint, PrecisionRoutingAdvice, SubstrateCapabilityKind |
| `core/toadstool/src/semantic_methods.rs` | +4 shader.compile.* methods, +tests |
| `core/toadstool/src/ipc_helpers/tests.rs` | Method count 66→70 |
| `server/src/pure_jsonrpc/handler/mod.rs` | +shader compile handlers, evolved discover_capabilities, precision_notes, +tests |
| `server/src/gpu_system.rs` | +query_available_backends(), is_ok_and migration |
| `distributed/src/common/auth/mod.rs` | TrustLevel, CapabilityToken, tests |
| `distributed/src/common/scheduling/mod.rs` | SchedulingPriority, PlacementConstraint, SchedulingDecision, tests |
| `distributed/src/common/mod.rs` | Export new types |

---

## 8. Recommended Next Steps

### For barraCuda
1. Consume `precision_routing()` in `GpuDriverProfile` — replace raw flag checks
2. Route f64 shared-memory reduction kernels to DF64 when `F64NativeNoSharedMem`
3. Add `ComputeDispatch::CoralReef` variant when coralDriver becomes available

### For coralReef
1. Implement tarpc compiler service matching `shader.compile.*` method signatures
2. Update toadStool handlers to proxy to tarpc when available
3. Set `sovereign_binary_capable = true` on HardwareFingerprint for supported GPUs

### For toadStool
1. D-COV: Push test coverage toward 90% (focus: CLI, distributed, auto_config, edge)
2. When coralDriver ships: set `f64_shared_memory_reliable = true` for native binary path
3. Evolve `PlacementConstraint` into full scheduling policy when distributed Phase 4 begins
