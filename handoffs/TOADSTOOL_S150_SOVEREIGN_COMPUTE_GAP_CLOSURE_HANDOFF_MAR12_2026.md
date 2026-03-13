# toadStool S150 — Sovereign Compute Gap Closure Handoff

**Date**: March 12, 2026
**Session**: S150
**Pins**: hotSpring v0.6.31, coralReef Iter 37, barraCuda S149

---

## Summary

Closed the major toadStool-side gaps for sovereign GPU compute,
following the BAR0 breakthrough from hotSpring/coralReef.

---

## Changes

### 1. VFIO GPU Backend (`nvpmu::vfio`)

New `VfioBar0Access` type for NVIDIA GPUs bound to `vfio-pci`:

- Full VFIO lifecycle: container → group → device fd → `VFIO_DEVICE_GET_REGION_INFO` → BAR0 mmap
- Implements `hw_learn::applicator::RegisterAccess` — drop-in for `Bar0Access`
- IOMMU group auto-detection from sysfs
- Bounds-checked register read/write with documented SAFETY invariants
- `Send` for cross-thread use

**File**: `crates/core/nvpmu/src/vfio.rs`

### 2. BAR0 Permissions (`nvpmu::permissions`)

udev rule management for non-root BAR0 access:

- `install_udev_rules()` — writes `/etc/udev/rules.d/99-ecoprimals-gpu-bar0.rules`, reloads udev
- `bar0_accessible(bdf)` — runtime check for BAR0 access without root
- `rules_installed()` — check if rules are already installed
- `set_bar0_permissions(bdf, mode)` — immediate per-GPU permission change

**udev rule**: NVIDIA vendor `0x10de` → `resource0` mode `0660`, group `gpu-mmio`

**File**: `crates/core/nvpmu/src/permissions.rs`

### 3. Setup Script (`scripts/setup-gpu-sovereign.sh`)

Root-only script modeled on `setup-akida-vfio.sh`:

1. Detect NVIDIA GPUs via PCI class (VGA/3D controller)
2. Create `gpu-mmio` group, add current user
3. Install udev rules for BAR0 access
4. Apply permissions immediately (no reboot needed)
5. Report VFIO status and IOMMU availability

### 4. nvpmu Recipe Deduplication

`init::apply_recipe()` now delegates to `hw_learn::RecipeApplicator`:

- Auto-detects format (legacy JSON vs canonical `InitRecipe`)
- Converts legacy `{ chip, steps, verify_reads }` to `InitRecipe` steps
- Maps `RecipeStep` → `InitStep::RegisterWrite` + optional `InitStep::Delay`
- Maps `VerifyRead` → `InitStep::Verify { RegisterMatch }`
- New `apply_init_recipe()` for direct `InitRecipe` use from knowledge store

### 5. Live BAR0 Apply (Gap Closure)

`compute.hardware.apply` JSON-RPC handler evolved:

- **Before**: Dry-run only (`RecipeApplicator::new(true)`)
- **After**: Supports `"live": true` param → opens `Bar0Access` via auto-detected BDF
- BDF auto-detection via `nvpmu::pci::discover_gpus()`
- On success, recipe stored to knowledge base

### 6. Gap 5: Knowledge → Init Wiring

New `compute.hardware.auto_init` JSON-RPC method:

1. Auto-detect NVIDIA GPU (or accept `"bdf"` param)
2. Look up chip architecture from PCI discovery
3. Find best recipe via `KnowledgeStore::best_recipe(target_arch)`
4. Apply via BAR0 (or dry-run with `"dry_run": true`)
5. Update recipe confidence score based on result

This completes the end-to-end path: observe → distill → store → auto_init

---

## Debt Resolved

| ID | Item | Resolution |
|----|------|-----------|
| D-NVPMU-DEDUP | nvpmu apply_recipe duplication | Delegates to hw-learn RecipeApplicator |
| D-BAR0-PERMS | BAR0 requires root | udev rules + setup script |
| D-VFIO-GPU | VFIO limited to Akida NPU | VfioBar0Access for NVIDIA GPUs |
| D-GAP5 | Knowledge → init not wired | compute.hardware.auto_init |
| D-LIVE-APPLY | hw_learn_apply dry-run only | Live BAR0 apply support |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo build --workspace` | PASS |
| `cargo fmt --check` | PASS |
| `cargo test --workspace` | 19,567 passed, 0 failed |
| `cargo check --workspace` | Clean |

---

## Gap Status (Post-S150)

| Gap | Status | Notes |
|-----|--------|-------|
| 1 (dispatch_binary) | **Closed** | coralReef coral cache → dispatch |
| 2 (UVM stubs) | Open | Needs nvidia module for testing |
| 3 (FECS) | **Closed** | BAR0 path (hotSpring) |
| 4 (RegisterAccess) | **Closed** | Bar0Access + VfioBar0Access both impl trait |
| 5 (knowledge→init) | **Closed (S150)** | auto_init wires KnowledgeStore → BAR0 apply |
| 6 (error recovery) | Open | Unified PCI discovery (AMD, Intel) |

### Remaining toadStool Work

- **Validation**: Run `setup-gpu-sovereign.sh` + `compute.hardware.auto_init` on real hardware
- **ecoprimals-mode CLI**: Phase 4 gaming ↔ science mode switch (future)
- **Dynamic GPU arbitration**: Phase 5 idle GPU detection (future)
- **Multi-arch register classifier**: Expand beyond NVIDIA to AMD/Intel

---

## Modified Files

```
NEW    crates/core/nvpmu/src/vfio.rs          VFIO BAR0 access
NEW    crates/core/nvpmu/src/permissions.rs    udev rule management
NEW    scripts/setup-gpu-sovereign.sh          GPU sovereign setup script
MOD    crates/core/nvpmu/src/init.rs           Delegates to hw-learn RecipeApplicator
MOD    crates/core/nvpmu/src/lib.rs            +vfio, +permissions modules
MOD    crates/core/nvpmu/src/error.rs          +Hardware variant
MOD    crates/core/nvpmu/Cargo.toml            rustix 1.1
MOD    crates/server/src/pure_jsonrpc/handler/hw_learn.rs   live apply + auto_init
MOD    crates/server/src/pure_jsonrpc/handler/mod.rs        +auto_init route
MOD    STATUS.md                               S150 entry
MOD    DEBT.md                                 5 items resolved
MOD    EVOLUTION_TRACKER.md                    S150 entry
MOD    NEXT_STEPS.md                           Updated status
```
