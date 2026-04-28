# GPU Solve Tighten and Refactor — Handoff

**From:** hotSpring + coralReef (sovereign GPU pipeline)
**To:** barraCuda, toadStool, primalSpring
**Date:** April 27, 2026
**coralReef iteration:** 85+
**hotSpring version:** v0.6.32
**barraCuda version:** 0.3.12
**License:** AGPL-3.0-or-later

---

## Summary

Comprehensive code quality pass across coralReef coral-driver and hotSpring barracuda.
The monolithic `vfio_compute/init.rs` (5466 LOC) in coral-driver was split into 11
focused modules. Shared abstractions were extracted, dead code removed, and IPC
patterns deduplicated in hotSpring. Both repos pass `cargo fmt` and `cargo clippy
-- -W clippy::pedantic -W clippy::nursery` with zero new errors.

---

## coralReef coral-driver Changes

### init.rs → 11 Modules

The original file handled all of Kepler K80 initialization in a single 5466-line file.
It is now a 19-line re-export facade. The implementation lives in:

| Module | LOC | Responsibility |
|--------|-----|---------------|
| `gr_bar0.rs` | 214 | Firmware-blob-driven BAR0 register writes |
| `warm_channel.rs` | 338 | Warm falcon restart and FECS channel init |
| `kepler_cold.rs` | 425 | Kepler cold-boot (PRI ring → clocks → FECS) |
| `kepler_warm.rs` | 1183 | Warm Kepler GR init |
| `kepler_recovery.rs` | 223 | Cold recovery after bus reset |
| `kepler_fecs_boot.rs` | 1687 | FECS/GPCCS firmware upload and boot |
| `pmu.rs` | 176 | PMU falcon firmware boot |
| `pgob.rs` | 174 | PGOB power gating control |
| `pri.rs` | 321 | PRI ring management |
| `quiesce.rs` | 66 | Engine quiesce before teardown |
| `vbios_devinit.rs` | 561 | VBIOS DEVINIT script interpreter |

### Shared Abstractions

- `write_kepler_hub_station_params()`: Hub station register writes deduplicated across `kepler_cold.rs`, `kepler_warm.rs`, `kepler_recovery.rs`
- `PGOB_POWER_STEPS`: Power gating sequence deduplicated in `pgob.rs`

### Dead Code Removed

- `kepler_pclock_pre_init` (unused clock init)
- `kepler_pri_station_probe` (replaced by `write_kepler_hub_station_params`)

### Polish

- `kepler_csdata.rs`: `pub const` → `pub(crate) const`, `debug_assert!(xfer > 0)`, precondition docs
- `hardware_guard.rs`: Named constants (`PMC_ENABLE`, `PGRAPH_BIT`, `DEAD_SENTINEL`) replace magic numbers

---

## hotSpring barracuda Changes

### IPC Deduplication

- `primal_bridge.rs`: New `jsonrpc_request()` envelope builder centralizes JSON-RPC 2.0 construction
- `glowplug_client.rs`: Refactored to use shared transport
- `niche.rs`: `send_registration` uses shared `send_jsonrpc` + `jsonrpc_request`

### GPU Module DRY

- `gpu/mod.rs`: Extracted `open_from_adapter_inner()` — shared GPU device opening logic
- `hardware_calibration.rs`: Extracted `summarize_tiers()` — tier aggregation dedup
- `precision_brain.rs`: Extracted `finish()` — bootstrap dedup

### Experiment Bin Hygiene

- 6 experiment bins (`exp070`, `exp154`, `exp155`, `exp157`, `exp158`, `exp167`) use `HOTSPRING_BDF` env var fallback
- `exp154`/`exp158` cross-referenced with "See also" notes
- `dual_dispatch.rs`: `#[allow(dead_code)]` → `#[expect(dead_code, reason="...")]`

---

## GPU Hardware Status

| GPU | Generation | Status |
|-----|-----------|--------|
| RTX 5060 | SM120 / Blackwell | **SOLVED** — full sovereign VFIO dispatch |
| Titan V | SM70 / Volta | **ACTIVE** — SEC2/ACR investigation, SBR hot reset |
| Tesla K80 | SM37 / Kepler GK210 | **ACTIVE** — internal firmware protocol, init.rs modularized |

---

## Primal Coordination Impact

### barraCuda
- IPC patterns now use shared `jsonrpc_request` envelope — absorption candidate for upstream utility crate
- GPU constructor dedup pattern (`open_from_adapter_inner`) may inform barraCuda's own adapter management

### toadStool
- Ember firmware management patterns (staged sovereign init) available for absorption into toadStool orchestration layer
- GlowPlug client IPC uses shared transport

### primalSpring
- Experiment bin `HOTSPRING_BDF` env var pattern available for adoption by other springs
- `#[expect(dead_code, reason)]` pattern documented for Rust 2024 compliance

---

## Verification

- `cargo check` passes on both repos
- `cargo fmt --check` clean
- `cargo clippy -- -W clippy::pedantic -W clippy::nursery` — zero new warnings
- `#![forbid(unsafe_code)]` holds in hotSpring library code
- No `#[allow()]` in production code
