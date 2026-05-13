<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Diesel Engine Migration Handoff — May 13, 2026

**Date**: May 13, 2026
**From**: coralReef (compiler primal)
**For**: toadStool (hardware primal), hotSpring (validation spring), barracuda (compute layer)
**Signal**: Feature freeze on diesel stack; E1/E2 upstream reference; E3 shipped.

---

## Context

hotSpring audited barracuda's compute layer and found 15+ source files wired to
coralReef's diesel engine stack (`coral-ember`, `coral-glowplug`, `coral-driver`
hardware runtime). This handoff documents what toadStool needs to replicate and
where to find the reference implementations.

## coralReef Action Items — Status

| Item | What | Status |
|------|------|--------|
| **Feature freeze** | No new features in coral-ember/coral-glowplug/coral-driver hardware paths | **DONE** — soft-deprecated since Sprint 6, feature freeze markers added Sprint 8 |
| **E1: Cylinder translation** | Document subprocess isolation pattern for toadStool reference | **DONE** — see §Reference below |
| **E2: Warm API** | Document warm handoff/capture API for toadStool reference | **DONE** — see §Reference below |
| **E3: FECS cold silicon init** | Compiler-domain work that stays in coralReef | **SHIPPED** (Sprint 7) — `boot_gr_falcons_with_recovery()`, PMC GR reset, `GrBootOutcome` |

## E1: Cylinder Subprocess Model (toadStool reference)

The "cylinder" pattern in coral-glowplug isolates per-GPU-domain work in child
processes. Key files:

| File | What it does |
|------|-------------|
| `coral-glowplug/src/sovereign.rs` | Boot orchestration: detect→warm→swap→init sequence, `BootResult`/`BootStep` structs |
| `coral-glowplug/src/socket/mod.rs` | ECU routing: dispatches JSON-RPC to per-device handlers ("diesel mode") |
| `coral-glowplug/src/observer/vfio.rs` | VFIO device observation — monitors device state during subprocess lifecycle |
| `coral-glowplug/src/device/health.rs` | Per-device health monitoring within cylinder context |

toadStool C1 should implement `toadstool-cylinder` with per-PCIe-domain process
isolation. The glowplug pattern spawns a handler per BDF that owns the device
lifecycle. ECU routing dispatches incoming RPCs to the correct cylinder by BDF.

## E2: Warm Handoff/Capture API (toadStool reference)

The warm API orchestrates cold→warm→capture→diff→save for sovereign GPU boot.
Key files:

| File | What it does |
|------|-------------|
| `coral-glowplug/src/capture.rs` | Full capture flow: cold BAR0 snapshot → swap to warm driver → settle → warm BAR0 snapshot → diff → save recipe JSON |
| `coral-ember/src/vendor_lifecycle/nvidia.rs` | NVIDIA-specific warm handoff validation (PCIe link check before vfio-pci bind) |
| `coral-driver/src/vfio/channel/hbm2_training/` | HBM2 domain capture/diff engine (register-level cold vs warm comparison) |
| `coral-driver/src/nv/vfio_compute/boot_sequence.rs` | `SovereignBootSequence` trait — `cold_init` uses `boot_gr_falcons_with_recovery()` |

toadStool C5 (warm-fecs pipeline) should reference the capture flow in
`capture.rs` and the HBM2 training diff in `hbm2_training/`. The recipe JSON
format (`TrainingRecipe` struct) is the interchange contract.

## Socket Paths (barracuda dependency)

barracuda's `fleet_client.rs` depends on coralReef socket paths. Current layout:

| Path | Resolution | Env Override |
|------|-----------|-------------|
| ember socket | `$XDG_RUNTIME_DIR/coral-ember-{family}.sock` | `$CORALREEF_EMBER_SOCKET` |
| glowplug socket | `$XDG_RUNTIME_DIR/coral-glowplug-{family}.sock` | `$CORALREEF_GLOWPLUG_SOCKET` |
| coralreef IPC | `$XDG_RUNTIME_DIR/coralreef.sock` | `$CORALREEF_SOCKET` |

toadStool should define equivalent `$TOADSTOOL_*` env vars. During transition,
barracuda can point env vars at toadStool sockets without code changes.

## What Stays in coralReef Permanently

- Compiler pipeline: `coral-reef/` (WGSL/SPIR-V/GLSL → native GPU binary)
- ISA tables, stubs, bitview: `coral-reef-isa/`, `coral-reef-stubs/`, `coral-reef-bitview/`
- Compile-side GPU API: `coral-gpu/` (compile + dispatch facade)
- GSP firmware handling: `coral-driver/src/gsp/`
- `naga::Module` direct ingest: `coral-reef/src/lib.rs` (`compile_module`/`compile_module_full`)
- FECS cold silicon recovery: `coral-driver/src/nv/vfio_compute/fecs_boot.rs`
- Linux path helpers: `coral-driver/src/linux_paths.rs`

## Excision Complete (Sprint 9, May 13 2026)

The following were **deleted** from coralReef in Sprint 9:
- `coral-ember` crate (52 .rs files)
- `coral-glowplug` crate (70 .rs files)
- `coral-driver` crate (367 .rs files — entire crate, including compiler-adjacent modules)
- `coral-gpu` crate (unified compile+dispatch)
- `showcase/` directory (hardware dispatch demos)

Total: 153K lines deleted. coralReef is now a pure compiler primal with zero unsafe.
toadStool should reference this handoff for E1/E2 patterns before the code was excised.
Git history preserves the full implementation for reference (`git log --all -- crates/coral-driver/`).

## Post-Excision Capability Alignment (hotSpring audit response)

hotSpring's post-excision trio alignment (May 13, 2026) confirmed coralReef is
operational for `shader.compile.wgsl/spirv`. One gap identified and resolved:

- **Discovery filter evolved**: coralReef's ecosystem discovery now matches
  toadStool's capability names (`compute.dispatch.*`, `gpu.*`, `compute.hardware.*`)
  in addition to legacy `gpu.dispatch`. This ensures coralReef finds toadStool's
  discovery JSON when determining available GPU targets for compilation.
- **Requires declaration updated**: `gpu.dispatch` → `compute.dispatch` with
  `legacy_id` metadata for backward compatibility.
- **3117 tests passing**, including 2 new tests for toadStool-style discovery JSON.

No remaining coralReef action items from the hotSpring audit.

---

## References

| Topic | Location |
|-------|----------|
| Diesel engine audit (hotSpring) | primalSpring downstream audit, May 13 2026 |
| Post-excision trio alignment (hotSpring) | hotSpring post-excision audit, May 13 2026 |
| Phase C completion | `handoffs/ECOSYSTEM_WAVE_SYNC_MAY12_2026.md` |
| FECS stability proof | `handoffs/ECOSYSTEM_WAVE_SYNC_MAY12_2026.md` (Sprint 7) |
| Interstadial exit criteria | `INTERSTADIAL_EXIT_CRITERIA.md` v1.4 |
