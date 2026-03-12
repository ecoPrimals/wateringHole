# ToadStool S147 — hw-learn Wiring + Sovereign Compute Hardening

**Date**: March 12, 2026
**Session**: S147
**Tests**: 20,015 passed (0 failures, 101 skipped)
**Clippy**: Pedantic clean (0 warnings)

---

## Changes

### 1. hw-learn Pipeline Wired (biomeOS v2.30 Capability Registration)

5 new JSON-RPC methods under `compute.hardware.*`:

| Method | Description |
|--------|-------------|
| `compute.hardware.observe` | Parse mmiotrace data into structured MMIO accesses |
| `compute.hardware.distill` | Diff baseline vs compute traces, build init recipe |
| `compute.hardware.apply` | Dry-run recipe application (BAR0 live requires root + opt-in) |
| `compute.hardware.share_recipe` | Save/load/list recipes via `RecipeStore` |
| `compute.hardware.status` | Pipeline state, firmware inventory, stored recipes |

**Files**: `crates/server/src/pure_jsonrpc/handler/hw_learn.rs` (new), `handler/mod.rs`, `handler/core.rs`, `server/Cargo.toml`

**Matches**: biomeOS v2.30 `compute.hardware.observe/distill/apply/share_recipe/status` capability registration.

### 2. RegisterAccess Bridge (nvpmu → hw-learn)

`nvpmu::Bar0Access` now implements `hw_learn::applicator::RegisterAccess`:

```rust
impl hw_learn::applicator::RegisterAccess for Bar0Access {
    fn read_u32(&self, offset: u64) -> std::result::Result<u32, String> { ... }
    fn write_u32(&mut self, offset: u64, value: u32) -> std::result::Result<(), String> { ... }
}
```

This means hw-learn recipes can now be applied directly to GPU hardware via BAR0 MMIO when running as root. The JSON-RPC `compute.hardware.apply` defaults to dry-run mode.

**Files**: `crates/core/nvpmu/src/bar0.rs`, `crates/core/nvpmu/Cargo.toml`

### 3. spirv_codegen_safety Rename

`nvvm_safety.rs` → `spirv_codegen_safety.rs`

Root cause of transcendental poisoning is naga SPIR-V codegen, not NVVM (per hotSpring v0.6.30 handoff). Module renamed. Backward-compatible type alias `SpirvCodegenRisk = NvvmPoisoningRisk` added.

**Files**: `crates/runtime/universal/src/backends/spirv_codegen_safety.rs` (renamed), `backends/mod.rs`

**Wire-compat**: JSON-RPC field in `gpu.info` renamed from `nvvm_safety` to `spirv_codegen_safety`. `science.gpu.capabilities` field renamed from `nvvm_safety` to `spirv_codegen_safety`.

### 4. FirmwareInventory in gpu.info

`gpu.info` now includes a `firmware_inventory` section. For each NVIDIA GPU detected via sysmon, probes `/lib/firmware/nvidia/{chip}/` and reports:

- `compute_viable` (bool)
- `compute_blockers` (array)
- `needs_software_pmu` (bool)
- Full firmware component status (pmu, gsp, acr, gr, sec2, nvdec)

Chip codename inference from PCI device ID via sysfs (Volta→gv100, Turing→tu102, Ampere→ga102, Ada→ad102).

**Files**: `crates/server/src/gpu_system.rs`, `crates/server/src/pure_jsonrpc/handler/core.rs`

### 5. PRIMAL_REGISTRY + genomeBin Updates

- `PRIMAL_REGISTRY.md`: ToadStool entry updated to S147 (20,015 tests, 94+ methods). New capability rows: Hardware Learning, Firmware Inventory, SPIR-V Codegen Safety. Spring versions table updated.
- `genomeBin/manifest.toml`: ToadStool capabilities expanded (hardware_learning, firmware_inventory, spirv_codegen_safety, precision_brain, nvk_zero_guard, provider_registry).

---

## Action Items for Other Primals

### biomeOS
- `compute.hardware.*` methods are live — biomeOS can route hardware learning requests to toadStool.
- `firmware_inventory` in `gpu.info` enables biomeOS to assess compute viability before dispatching.

### hotSpring
- `spirv_codegen_safety` rename completed. hotSpring can update local references from `nvvm_safety` → `spirv_codegen_safety`.
- `FirmwareInventory` now in `gpu.info` — hotSpring can consume firmware status for sovereign engine decisions.

### neuralSpring
- NUCLEUS pipeline GPU dispatch (`PipelineGraph`) absorption into `toadstool::orchestration` is next priority (P2).

### coralReef
- `spirv_codegen_safety` field name in `gpu.info` response reflects the naga root cause.

---

## Remaining Hurdles to Sovereign Compute

| Priority | Item | Status |
|----------|------|--------|
| P2 | Extend hw-learn distiller for GA102/TU102 register ranges | Pending |
| P2 | Absorb neuralSpring PipelineGraph into orchestration | Pending |
| P3 | Multi-vendor PCI discovery (AMD/Intel) in nvpmu | Pending |
| P3 | probe_dispatch for empirical naga poisoning detection | Pending |
| P3 | petalTongue provider.register_capability integration | Pending |

---

## Files Changed

```
crates/server/Cargo.toml
crates/server/src/pure_jsonrpc/handler/hw_learn.rs (NEW)
crates/server/src/pure_jsonrpc/handler/mod.rs
crates/server/src/pure_jsonrpc/handler/core.rs
crates/server/src/pure_jsonrpc/handler/science.rs
crates/server/src/gpu_system.rs
crates/core/nvpmu/Cargo.toml
crates/core/nvpmu/src/bar0.rs
crates/runtime/universal/src/backends/spirv_codegen_safety.rs (RENAMED from nvvm_safety.rs)
crates/runtime/universal/src/backends/mod.rs
```
