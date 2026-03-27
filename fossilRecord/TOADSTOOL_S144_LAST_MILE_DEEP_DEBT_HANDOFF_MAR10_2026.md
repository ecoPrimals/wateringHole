# toadStool S144 — Last Mile Deep Debt Handoff

**Date**: March 10, 2026
**Sprint**: S144
**Primal**: toadStool
**Status**: All 5 phases complete. All quality gates green.

---

## Summary

S144 resolved the final categories of deep technical debt to create a solid
foundation for multi-GPU daisy-chain orchestration, PCIe switch topology, and
spring-primal capability parity. The codebase was already clean (zero clippy,
zero fmt diffs, zero TODO/FIXME, zero production panics) but had ~23 deprecated
API usages in production, ~47 dead code markers without explicit justification,
~111 ignored tests without strategy, no PCIe switch topology modeling, and
single-device-only coralReef compilation.

---

## Phase 1: PCIe Switch Topology

**New module**: `crates/core/sysmon/src/pcie_topology.rs`

- `PciBridge` — models a PCIe bridge/switch (BDF address, generation, width)
- `GpuPairTopology` — per-pair info: common bridge, hops, contention, NUMA
- `PcieTopologyGraph` — full graph with `pair()` and `effective_bandwidth_bps()`
- `discover_topology()` — walks `/sys/class/drm/card*/device/..` parent chains
- `raw_pcie_bandwidth_bps(gen, width)` — PCIe gen/width → bits/sec

**Integration**:
- `PcieLink` enriched with `via_switch`, `hops`, `contention_factor`
- `discover_pcie_links()` now uses `PcieTopologyGraph` for accurate bandwidth
- `WorkloadRouter::route_multi_gpu()` — selects GPU groups sharing switches

**Relevance to springs**: An array of RTX 3050s on a PCIe daisy-chain connected
to a single x16 slot can outperform bigger systems on dynamic QCD when
properly orchestrated. This topology model enables that placement logic.

---

## Phase 2: Deprecated API Migration

Migrated ~23 production call sites from hardcoded primal names to
capability-based discovery:

| Old API | New API | Files |
|---------|---------|-------|
| `primals::TOADSTOOL` | `primal_identity::PRIMAL_NAME` | server, cli, config, display, sandbox (7) |
| `primals::BEARDOG` | `capabilities::CRYPTO` | distributed, integration/beardog (5) |
| `primals::SONGBIRD` | `capabilities::COORDINATION` | distributed/songbird (2) |
| `primals::NESTGATE` | `capabilities::STORAGE` | integration/nestgate (2) |
| `EnvironmentConfig` fields | Direct env var lookups | server config, scheduler (2) |
| `get_socket_path_for_service` | `get_socket_path_for_capability` | nestgate client (1) |
| `well_known::BEARDOG` | `capabilities::CRYPTO` | beardog client (1) |

All `#[allow(deprecated)]` removed from migrated sites. Test assertions
updated to expect capability names (e.g. `"crypto"` not `"beardog"`).

---

## Phase 3: Dead Code Audit

47 `#[allow(dead_code)]` instances upgraded to `#[allow(dead_code, reason = "...")]`
with explicit justification categories:

- **Hardware register definitions** (VFIO ioctls, Akida registers)
- **Kernel ABI structs** (VFIO region info)
- **Serde-required fields** (JSON-RPC response `jsonrpc`/`id`)
- **DRM modesetting pipeline** (used when display hardware available)
- **OpenCL/Vulkan constructors** (used when runtime available)
- **Future-phase placeholders** (auth manager, regex cache)

---

## Phase 4: Ignored Test Evolution

- **`slow-tests` feature flag**: `auto_config`, `cli`, `testing` crates.
  Tests annotated with `#[cfg_attr(not(feature = "slow-tests"), ignore = "...")]`.
  Run with `cargo test --features slow-tests`.
- **`gpu_guards` module** (`toadstool-testing`):
  - `is_wgpu_safe()` — runtime check for NVIDIA proprietary Vulkan drivers
  - `wgpu_skip_reason()` — human-readable explanation
  - `detect_nvidia_proprietary()` — sysfs + env var detection
  - Supports `TOADSTOOL_FORCE_WGPU_TESTS=1` override for CI

---

## Phase 5: coralReef Multi-Device Compile

**New types** in `crates/server/src/coral_reef_client.rs`:
- `MultiDeviceCompileRequest` — WGSL source + target devices + opt level
- `DeviceTarget` — card index + arch hint + PCIe group
- `MultiDeviceCompileResponse` — per-device results + success count

**API changes**:
- `compile_wgsl()` gains `target_device: Option<u32>` parameter
- New `compile_wgsl_multi(&MultiDeviceCompileRequest)` method
- `shader.compile.wgsl.multi` JSON-RPC endpoint wired

---

## Inter-Primal Impact

| Primal | Impact |
|--------|--------|
| **barraCuda** | Can leverage `PcieTopologyGraph` via `toadstool-sysmon` for device selection. Multi-device compile enables per-GPU ISA optimization. |
| **coralReef** | New `shader.compile.wgsl.multi` endpoint for array compilation. `DeviceTarget` carries arch hints (`"gfx1030"`, `"sm89"`). |
| **Springs** | `WorkloadRouter::route_multi_gpu()` enables springs to request N-GPU placement with switch affinity. `gpu_guards` helps springs test safely on NVIDIA. |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo build --workspace` | PASS |
| `cargo fmt --check` | PASS (0 diffs) |
| `cargo clippy --workspace` | PASS (0 new warnings) |
| `cargo test --workspace` | PASS (19,900+ tests, 0 failures) |

---

## Files Changed (96 files, +861/-433 lines)

### New files:
- `crates/core/sysmon/src/pcie_topology.rs`
- `crates/runtime/orchestration/src/workload_routing.rs`
- `crates/runtime/orchestration/src/workload_health.rs`
- `crates/runtime/universal/src/backends/nvvm_safety.rs`
- `crates/testing/src/gpu_guards.rs`

### Key modified files:
- `crates/runtime/display/src/pcie_transport.rs` — topology integration
- `crates/server/src/coral_reef_client.rs` — multi-device compile
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — new endpoint
- 20+ files for deprecated API migration
- 15+ files for dead code `reason` annotations
- 8+ files for slow-tests feature flag
