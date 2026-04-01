# Cross-Primal Rewiring — Daemon Architecture Handoff

**Date**: March 31, 2026
**Scope**: coralReef, toadStool, hotSpring, barraCuda
**Prerequisite**: coralReef Iter 70i, toadStool S170, barraCuda v0.3.11
**Hardware**: biomeGate (Titan V GV100, Tesla K80 GK210 ×2, RTX 5060 GB206)

---

## Summary

Fixed stale cross-primal integration across all four repos so the daemon-backed
GPU pipeline is coherent end-to-end. All experiments now run through
coral-ember and coral-glowplug daemons without requiring sudo or direct sysfs
access. Socket paths, method names, and data directories are aligned with the
wateringHole IPC convention.

## Changes by Repository

### coralReef

| File | Change |
|------|--------|
| `crates/coral-driver/tests/hw_nv_vfio_hbm2.rs` | Metal map output uses `optional_data_dir()` instead of `HOTSPRING_DATA_DIR`-only |
| `crates/coral-driver/tests/hw_nv_vfio_advanced.rs` | Metal map output uses `optional_data_dir()` instead of hardcoded `hotSpring/data/` path |
| `showcase/02-compute-triangle/02-full-compute-triangle/src/main.rs` | Socket name `toadstool.jsonrpc` → `toadstool` (wateringHole convention) |
| `showcase/02-compute-triangle/01-toadstool-discovery/src/main.rs` | Display text `shader.compile` → `shader.dispatch` (current method) |
| `EVOLUTION.md`, `ABSORPTION.md`, `CONTRIBUTING.md` | Test counts updated to 4232+/70i |
| `CHANGELOG.md` | Cross-primal rewiring entry added |

### toadStool

| File | Change |
|------|--------|
| `crates/core/toadstool/src/semantic_methods.rs` | Removed 4 stale `shader.compile.*` entries (`.wgsl`, `.spirv`, `.status`, `.capabilities`) — no handler existed |
| `crates/core/toadstool/src/ipc_helpers/tests.rs` | Updated assertion to check `shader.dispatch` instead of removed `shader.compile.wgsl` |
| `crates/server/src/glowplug_client.rs` | Ember socket discovery path: `$XDG_RUNTIME_DIR/coralreef/ember.sock` → `$XDG_RUNTIME_DIR/biomeos/coral-ember-default.sock` |
| `crates/server/src/pure_jsonrpc/handler/mod.rs` | Wired `ember.list` and `ember.status` as forwarded methods through `GlowPlugClient` |
| `CHANGELOG.md` | Fixed stale Links section (removed dead refs to fossilized docs) |

### hotSpring

| File | Change |
|------|--------|
| `experiments/124_VM_CAPTURE_K80_TITANV_CROSS_ANALYSIS.md` | Renamed to `124b_...` (AMD scratch breakthrough is the primary Exp 124) |
| `EXPERIMENT_INDEX.md` | Added entries for Exp 124-AMD, 126, 127, 128; counts updated to 128+ |
| `barracuda/src/bin/validate_coral_sovereign.rs` | Feature name `coral-sovereign` → `sovereign-dispatch` |
| `specs/CORALREEF_DISPATCH_FRONTIER_HANDOFF.md` | Marked as historical; feature name fixed |
| `SOVEREIGN_VALIDATION_GOAL.md`, `CONTROL_EXPERIMENT_STATUS.md` | Fossil headers updated to 128+ experiments |
| `scripts/{7 deploy scripts}` | Archived to `scripts/archive/` — superseded by `coralReef/deploy-dev.sh` |

### barraCuda

No code changes. Verified `CoralCompiler` discovery paths already use
`$XDG_RUNTIME_DIR/biomeos/shader.sock` — fully aligned with wateringHole convention.

## Daemon Socket Convention

All daemon sockets follow the wateringHole `PRIMAL_IPC_PROTOCOL` v3.0 standard:

```
$XDG_RUNTIME_DIR/biomeos/coral-ember-default.sock
$XDG_RUNTIME_DIR/biomeos/coral-glowplug-default.sock
$XDG_RUNTIME_DIR/biomeos/toadstool.sock
$XDG_RUNTIME_DIR/biomeos/shader.sock          (capability symlink → coralreef instance)
```

On biomeGate, system daemons run at `/run/coralreef/{ember,glowplug}.sock` with
user-level symlinks in `$XDG_RUNTIME_DIR/biomeos/` for wateringHole compatibility.

## Validation

- **K80 sovereign test** (exp123k1): PASS — daemon path routing confirmed (`K80Bar0: using daemon path`)
- **Titan V WPR2 state tracking** (exp117): PASS — ember parasitic reads, 28s full cycle
- **toadStool semantic methods**: 20/20 pass (shader.compile.* removal verified)
- **toadStool handler**: 5/5 pass (ember.list/status wiring verified)
- **Ember RPC** via wateringHole path: 3 devices returned (Titan V, K80 die0, K80 die1)
- **Glowplug RPC** via wateringHole path: full fleet (4 GPUs including RTX 5060 display)

## What's Next

Return to GPU solving with the modern primal daemon infrastructure:

1. **Titan V (GV100)**: Firmware interface approach — treat FECS as persistent
   firmware managed by ember, not something to boot from scratch. Revalidate
   Exp 125 (livepatch) and Exp 127 (warm FECS dispatch) with daemon-backed paths.
2. **Tesla K80 (GK210)**: Complete GPFIFO dispatch (Exp 128a3) — FECS boot
   recipe works, channel creation works, dispatch is next.
3. **Cross-primal E2E**: toadStool `shader.dispatch` → coralReef compile →
   coral-glowplug dispatch → readback — the full compute triangle with live hardware.
