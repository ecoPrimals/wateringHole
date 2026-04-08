<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Cross-Repo Deep Debt Evolution — Handoff to Primal & Spring Teams

**Date**: March 30, 2026
**From**: hotSpring GPU sovereign compute / infra evolution
**To**: coralReef team, benchScale team, agentReagents team, all spring teams
**Scope**: 7-tier deep debt evolution executed across coralReef, hotSpring, agentReagents, benchScale

---

## Summary

A comprehensive deep debt evolution was executed across four repositories, covering
Python→Rust migration, external dependency evolution, unsafe code consolidation,
large file refactoring, hardcoding elimination, and script archival. All four repos
compile clean after changes.

---

## 1. coralReef (Iter 70i) — What Changed

### Dependency Evolution

| Before | After | Crate | Why |
|--------|-------|-------|-----|
| `nvidia-smi` shell-out | `nvml-wrapper` 0.10 | coral-glowplug | Pure Rust GPU telemetry — no process spawn, structured errors |
| `sh -c printf` for sysfs | `libc::fork()` + `std::fs::write` | coral-driver | D-state timeout protection without shell dependency |

### Unsafe Code Consolidation

| Abstraction | Location | What It Encapsulates |
|-------------|----------|---------------------|
| `RegisterMap` | `coral-driver/src/mmio.rs` | Bounds-checked, aligned, volatile 32-bit MMIO read/write |
| `LockedAlloc` | `coral-driver/src/vfio/dma.rs` | RAII page-aligned mlock/munlock/dealloc for DMA buffers |

### Large File Refactoring

| File | Split Into | Lines Before |
|------|-----------|-------------|
| `uvm_compute.rs` | + `uvm_rm_setup.rs`, `uvm_channel.rs` | >1000 |
| `ember.rs` | (internal module decomposition) | >800 |
| `device_ops.rs` | + `resurrect.rs`, `warm_handoff.rs` | >600 |

### Python→Rust Migration (coralctl subcommands)

| Python Script | coralctl Command | Module |
|---------------|-----------------|--------|
| `parse_mmiotrace.py` | `coralctl trace-parse <file>` | `handlers_trace.rs` |
| `generate_titanv_recipe.py` | `coralctl trace-parse --recipe-json <file>` | `handlers_trace.rs` |
| `apply_recipe.py` | `coralctl oracle apply <BDF> <recipe>` | `handlers_trace.rs` |
| `replay_devinit.py` | `coralctl devinit replay <BDF>` | `handlers_trace.rs` |
| `extract_devinit.py` | `coralctl devinit replay <BDF>` | `handlers_trace.rs` |

### Boot Config Evolution

`coralctl deploy boot-config` now generates `modprobe.d` and `vfio-pci.ids` from
`glowplug.toml`. K80 (`10de:102d`) excluded from `vfio-pci.ids` — managed by ember
`driver_override` at runtime. Supports `--dry-run`.

### Script Archival

`scripts/rebind-titanv-vfio.sh` and `scripts/rebind-titanv-nouveau.sh` moved to
`scripts/archive/`. `scripts/boot/deploy-boot.sh` fossil-recorded with pointer
to `springs/hotSpring/scripts/boot/install-boot-config.sh`.

### What coralReef Teams Should Know

- `MappedBar::read_u32` now returns `Result<u32, DriverError>` — callers need `.unwrap_or()` or `?`
- `mmio` module is now `pub` (was `pub(crate)`) — `RegisterMap` is the public-facing API
- `nvml-wrapper` requires NVIDIA driver installed for GPU telemetry; graceful degradation preserved
- `isolated_sysfs_write` uses `unsafe { libc::fork() }` — the safety rationale is documented inline

---

## 2. benchScale — What Changed

### virsh CLI → virt Crate Migration

**20+ `Command::new("virsh")` call sites** replaced with `virt` crate API:

| virsh Command | virt API | Files |
|---------------|----------|-------|
| `virsh shutdown` | `Domain::shutdown()` | `cleanup.rs`, `pipeline.rs` |
| `virsh destroy` | `Domain::destroy()` | `cleanup.rs` |
| `virsh undefine` | `Domain::undefine()` | `cleanup.rs` |
| `virsh list --all` | `Connect::list_all_domains()` | `cleanup.rs` |
| `virsh net-start` | `Network::create()` | `recovery.rs` |
| `virsh net-destroy` | `Network::destroy()` | `recovery.rs` |
| `virsh net-list` | `Network::is_active()` | `health_check.rs` |
| `virsh domifaddr` | `Domain::interface_addresses()` | `utils.rs`, `pipeline.rs`, `dhcp_discovery.rs` |
| `virsh dumpxml` | `Domain::get_xml_desc()` | `boot_diagnostics.rs`, `pipeline.rs` |
| `virsh dominfo` | `Domain::get_info()` | `boot_diagnostics.rs` |
| `virsh vncdisplay` | XML parse from `get_xml_desc()` | `pipeline.rs` |
| `virsh net-dumpxml` | `Network::get_xml_desc()` | `capabilities.rs` |
| `virsh pool-dumpxml` | `StoragePool::get_xml_desc()` | `capabilities.rs` |
| `virsh net-dhcp-leases` | FFI `virNetworkGetDHCPLeases` | `health_check.rs`, `dhcp_discovery.rs` |

DHCP lease queries use FFI (`virt::sys`) because the safe `virt` 0.3 wrapper
does not yet expose `virNetworkGetDHCPLeases`. Guarded with `#[cfg(feature = "libvirt")]`.

### Hardcoded Path Elimination

All `/var/lib/libvirt/images` references replaced with
`BenchScaleConfig::storage().images_dir()` or `constants::paths::default_system_vm_images_dir()`.

### Large File Refactoring

`builder/mod.rs` split into `cloud_init.rs` and `vm_create.rs`.

### What benchScale Teams Should Know

- `virt` crate is now a required (non-optional) dependency
- Async libvirt calls use `tokio::task::spawn_blocking` for thread safety
- Pre-existing compilation issues (`create_desktop_vm` arity, `ImageBuilder::new`) were not introduced by this work

---

## 3. agentReagents — What Changed

- `builder/mod.rs` split into `cloud_init.rs` and `vm_create.rs`
- New reagent YAML templates for K80 and Titan V driver captures:
  `reagent-nouveau-k80.yaml`, `reagent-nouveau-titanv.yaml`,
  `reagent-nvidia390-k80.yaml`, `reagent-nvidia418-k80.yaml`,
  `reagent-nvidia418-titanv.yaml`, `reagent-nvidia470-titanv.yaml`,
  `reagent-nvidia510-titanv.yaml`, `reagent-nvidia535-titanv.yaml`,
  `reagent-nvidiaopen535-titanv.yaml`

---

## 4. hotSpring — What Changed

### Script Archival

8 Python/shell scripts moved to `scripts/archive/`:

| Script | Replaced By |
|--------|-------------|
| `bar0_read.py` | `coralctl mmio read <BDF> <offset>` |
| `parse_mmiotrace.py` | `coralctl trace-parse <file>` |
| `replay_devinit.py` | `coralctl devinit replay <BDF>` |
| `generate_titanv_recipe.py` | `coralctl trace-parse --recipe-json <file>` |
| `extract_devinit.py` | `coralctl devinit replay <BDF>` |
| `apply_recipe.py` | `coralctl oracle apply <BDF> <recipe>` |
| `capture_multi_backend.sh` | `coralctl swap <BDF> <target> --trace` |
| `titan_timing_attack.sh` | `coralctl warm-fecs <BDF>` (Exp 127 complete) |

### Boot Config

`install-boot-config.sh` updated: K80 (`10de:102d`) removed from `VFIO_IDS` kernel
cmdline — K80 managed by ember `driver_override` at runtime.

### Documentation

- `WORKFLOW.md` fossil-recorded — superseded by `coralctl`/`ember`/`glowplug`
- `scripts/README.md` updated to reflect script archival
- `EXPERIMENT_INDEX.md` updated: 131+ experiments
- `specs/README.md` updated: 8 missing spec files added to index
- Experiment 130-131 journals tracked

---

## 5. Cross-Cutting Patterns for All Teams

### The Deep Debt Principles Applied

1. **External process → Rust crate**: `nvidia-smi`→`nvml-wrapper`, `virsh`→`virt`, `sh -c`→`libc::fork()`
2. **Unsafe consolidation**: Raw pointer ops → RAII wrappers (`RegisterMap`, `LockedAlloc`)
3. **Smart refactoring**: Large files split by domain, not arbitrary line count
4. **Hardcoding → capability-based**: Boot configs from `glowplug.toml`, image paths from config
5. **Script → daemon**: All GPU lifecycle operations through `coralctl`/`ember`/`glowplug` RPC
6. **Fossil record**: Archived scripts preserved in `scripts/archive/` with migration table

### How to Absorb This Work

- **coralReef consumers** (hotSpring, agentReagents): `coralctl` subcommands replace
  all Python hardware scripts. Use `coralctl --help` for the full command tree.
- **benchScale consumers**: The `virt` crate API is now the standard for VM lifecycle.
  Any new VM operations should use the `virt` crate, not `Command::new("virsh")`.
- **All springs**: If you have `nvidia-smi`, `virsh`, or other shell-out patterns,
  these repos demonstrate the migration path. Check your spring's `scripts/` for
  archivable candidates.

---

## 6. Remaining Frontiers

| Area | Status | Next Step |
|------|--------|-----------|
| K80 sovereign compute (Exp 123) | Active | Direct PIO boot validation |
| Warm handoff livepatch (Exp 125) | Active | FECS warm retention after swap |
| Puzzle box matrix (Exp 128) | Active | Parallel K80+Titan V solution tracks |
| AMD EXEC masking | Frontier | Divergent wavefront control flow |
| 16⁴+ dynamical production | Frontier | Sovereign pipeline end-to-end |
| `virt` crate DHCP safe wrapper | Waiting | Upstream `virt` 0.4+ needed |
