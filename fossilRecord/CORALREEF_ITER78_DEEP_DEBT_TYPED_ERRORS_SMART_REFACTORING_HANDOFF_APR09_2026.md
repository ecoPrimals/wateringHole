# coralReef Iter 78 — Deep Debt Evolution: Typed Errors + Smart Refactoring Handoff

**Date**: April 9, 2026
**Primal**: coralReef
**Iteration**: 78
**Matrix**: ECOSYSTEM_COMPLIANCE_MATRIX v2.7.0

---

## Executive Summary

Deep debt evolution across three axes: (1) three-wave typed error migration replacing
`Result<_, String>` with structured `thiserror` enums across coral-driver and coralreef-core,
(2) smart refactoring of 7 production files from 831–882 LOC down to cohesive submodules,
(3) BTSP Phase 2 wired with full BearDog delegation via capability-based crypto-domain discovery.
All quality gates green. 4,459 tests passing.

---

## Part 1: What Changed

### Typed Error Migration (3 Waves)

| Wave | Error Type | Scope | Files |
|------|-----------|-------|-------|
| tarpc | `TarpcCompileError` | tarpc wire protocol: `Serialize`/`Deserialize` typed error replaces raw `String` | tarpc_transport.rs, tests_tarpc.rs, service/types.rs |
| 1 | `PciDiscoveryError` | PCI config space, power management, device info, sysfs I/O | error.rs, config_space.rs, power_mgmt.rs, device_info.rs, pci_config.rs |
| 2 | `ChannelError` | BAR0 oracle (dump/text/live), nouveau page tables, glowplug, sysfs BAR0, HBM2 training | error.rs, oracle.rs, nouveau_oracle.rs, glowplug/mod.rs, sysfs_bar0.rs, hbm2_training/oracle.rs |
| 3 | `DevinitError` | VBIOS parsing, PMU devinit, BIT tables, script interpreter, PMU timeout | error.rs, vbios.rs, pmu.rs, interpreter.rs, scan.rs, glowplug/warm.rs |

All new error types use `thiserror`, have `#[from]` bridges into `DriverError`, and are
re-exported from `coral_driver` lib.rs. Pattern: `DriverError::PciDiscovery(#[from])`,
`DriverError::Channel(#[from])`, `DriverError::Devinit(#[from])`.

### Smart Refactoring (7 Production Files)

| File | Before | After | Submodules |
|------|--------|-------|-----------|
| `nv_metal.rs` | 882 | 6 submodules | reg_offsets, identity, metal, probe, detect, tests |
| `memory.rs` | 874 | 4 submodules | core, regions, topology, tests |
| `vfio_compute/mod.rs` | 866 | 464 + 3 | layout, raw_device, device_open |
| `falcon_capability.rs` | 856 | 4 submodules | types, probe, pio |
| `knowledge.rs` | 852 | 5 submodules | types, chip, gpu_knowledge, tests |
| `device/mod.rs` | 835 | ~32 + 4 | mapped_bar, open, runtime, handles |
| `codegen/ops/mod.rs` | 831 | ~34 + 3 | gfx9, amd_dispatch, encoding_helpers |

All public APIs preserved via `pub use` re-exports. No callers changed.

### BTSP Phase 2 — BearDog Delegation

- `gate_connection()` evolved to async `guard_connection()` with full BearDog delegation
- Capability-based security provider discovery: `crypto-{family_id}.sock` → `crypto.sock` → `.json` capability scan
- `BtspOutcome` enum: `DevMode`, `Authenticated { session_id }`, `Degraded { reason }`, `Rejected { reason }`
- Async implementation for coralreef-core and coral-glowplug; blocking for coral-ember
- Degraded mode: connections accepted with warning when BearDog unreachable (operational resilience)
- `btsp.session.create` RPC over newline-delimited JSON-RPC on Unix domain socket

### Lint Hardening

- `#[allow(clippy::result_large_err)]` → `#[expect]` in sysmem_prepare.rs (2 sites)
- `#[allow(unused_imports)]` → `#[expect]` in shader_header/mod.rs
- `#[allow]` : `#[expect]` ratio improved to ~12:183

---

## Part 2: Quality Gate

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-features -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS='-D warnings' cargo doc --all-features --no-deps` | PASS |
| `cargo test --all-features` | 4,459 passed, 0 failed, 153 ignored |
| All files <1000 lines | PASS (max 982, test file) |
| Zero TODO/FIXME/HACK in production | PASS |
| SPDX headers | PASS |

---

## Part 3: Patterns Worth Absorbing

### Typed Error Wave Pattern

The 3-wave migration strategy works well for large codebases:
1. Start with leaf modules (PCI discovery — no callers outside the module)
2. Next, modules with moderate fan-out (channel oracles — ~5 callers)
3. Finally, modules with broad fan-out (devinit — touches glowplug, pmu, interpreter)

Each wave adds a new `thiserror` enum with `#[from]` into the crate-level `DriverError`,
keeping existing callers working via `?` propagation.

### Smart Refactoring vs Arbitrary Split

Files were only split when clear cohesive boundaries existed:
- **Data + behavior**: register offsets separated from runtime logic (nv_metal)
- **Lifecycle phases**: open/init vs runtime vs cleanup (device/mod.rs)
- **Abstraction layers**: types vs probing vs PIO access (falcon_capability)
- Auto-generated data tables (ISA, stubs) were NOT split — they fight the generator.

---

## Part 4: Compliance Matrix Update

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T1 Build | A | A+ | 3 new typed error enums; 7 files smartly split |
| T2 UniBin | A | A | No change |
| T3 IPC | A | A | tarpc error type evolved from String to typed |
| T4 Discovery | B | B | BTSP Phase 2 wired (BearDog delegation); no self-register change |
| T5 Naming | A | A | No change |
| T6 Responsibility | A | A | No change |
| T7 Workspace | A | A | No change |
| T8 Presentation | A | A | Root docs updated to Iter 78 |
| T9 Deploy | C | C | musl-static not yet verified |
| T10 Live | N/T | N/T | Not deployed |
| **Rollup** | **A** ↑ | **A+** ↑ | T1 elevated: typed errors + refactoring depth |

---

## Remaining Work

- **coral-driver `Result<_, String>` wave 4+**: ~20 remaining functions in deep hardware interaction code (mmu_oracle/capture internals, devinit/pmu internals, hbm2_training/oracle)
- **musl-static verification (T9)**: Cross-compile both x86_64 and aarch64
- **plasmidBin submission (T9/T10)**: Requires musl-static builds
- **Coverage push**: Target 90% via `cargo llvm-cov`; hardware tests need local GPU
- **BTSP Phase 2 end-to-end**: Needs BearDog `btsp.session.create` service running for integration test

---

## Files Changed (71 files, +6,147 / -5,345)

### New files
- `crates/coral-driver/src/gsp/knowledge/` (5 submodules)
- `crates/coral-driver/src/nv/vfio_compute/falcon_capability/` (4 submodules)
- `crates/coral-driver/src/nv/vfio_compute/device_open.rs`
- `crates/coral-driver/src/nv/vfio_compute/layout.rs`
- `crates/coral-driver/src/nv/vfio_compute/raw_device.rs`
- `crates/coral-driver/src/vfio/device/` (mapped_bar, open, runtime, handles)
- `crates/coral-driver/src/vfio/memory/` (core, regions, topology)
- `crates/coral-driver/src/vfio/nv_metal/` (6 submodules)
- `crates/coral-reef/src/codegen/ops/` (gfx9, amd_dispatch, encoding_helpers)
- `crates/coralreef-core/src/service/types.rs` — `TarpcCompileError`

### Key modified files
- `crates/coral-driver/src/error.rs` — `PciDiscoveryError`, `ChannelError`, `DevinitError`
- `crates/coralreef-core/src/ipc/tarpc_transport.rs` — `TarpcCompileError` replaces `String`
- `crates/coralreef-core/src/ipc/btsp.rs` — `guard_connection()` BearDog delegation
- `crates/coral-glowplug/src/socket/btsp.rs` — `guard_connection()` BearDog delegation
- `crates/coral-ember/src/btsp.rs` — blocking `guard_connection()` BearDog delegation
- 40+ VFIO channel/devinit/discovery files — typed error migration
