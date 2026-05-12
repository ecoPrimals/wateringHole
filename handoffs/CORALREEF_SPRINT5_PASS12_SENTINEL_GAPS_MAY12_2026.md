<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Sprint 5: Pass 12 Sentinel Gaps

**Date**: May 12, 2026
**From**: coralReef
**Context**: primalSpring upstream audit — Passes 12-14 (Stadial Gate Remaining Work)

---

## Summary

Three Pass 12 sentinel escalation items resolved: `naga::Module` direct ingest API (skip text→parse round-trip for in-process callers), compile deadline on all IPC handlers (prevents unbounded blocking), Volta+/Blackwell cold init wired to attempt PIO FECS/GPCCS falcon boot. 4790 tests (+6), zero clippy warnings.

## Changes

### `naga::Module` Direct Ingest (`lib.rs`, `ptx_emit/mod.rs`)

- New public `compile_module()` and `compile_module_full()` — accept pre-parsed `naga::Module` directly
- New `emit_compute_ptx_module()` — PTX path for SM100+ targets accepts `&naga::Module`
- `pub use naga` re-export for downstream convenience
- 6 new tests: empty module rejection, minimal compute, full metadata, WGSL output parity, AMD target, Intel unsupported

### Compile Deadline (`newline_jsonrpc.rs`, `tarpc_transport.rs`)

- All `shader.compile.*` IPC handlers (JSON-RPC newline + Unix socket + tarpc) wrapped in `tokio::time::timeout`
- Default: 120s, configurable via `CORALREEF_COMPILE_TIMEOUT_SECS`
- Returns structured error on timeout instead of hanging

### FECS/GPCCS Cold Silicon Init (`boot_sequence.rs`, `fecs_boot.rs`)

- `VoltaBoot::cold_init` and `BlackwellBoot::cold_init` now attempt PIO falcon boot (`boot_gr_falcons`) when firmware available on disk
- Graceful fallback: clear tracing diagnostic when firmware missing or ACR/SEC2 required
- `firmware_available()` respects `CORALREEF_NVIDIA_FIRMWARE_ROOT` env var (aligns with GSP firmware parser)

## Quality Gates

- `cargo clippy --all-features -- -D warnings`: **0 warnings**
- `cargo test --all-features`: **4790 passed, 0 failed, 181 ignored**
- `cargo fmt -- --check`: **clean**

## Coordination

### Pass 12 Status (coralReef items)

| Item | Audit description | Status |
|------|-------------------|--------|
| `bind_stat` timeout | Cold-path timeout handling for shader compilation | **RESOLVED** — compile deadline on all IPC handlers |
| FECS/GPCCS cold silicon init | Firmware command sequencing for sovereign GPU init | **RESOLVED** — PIO falcon boot wired in VoltaBoot + BlackwellBoot cold_init |
| `naga::Module` direct ingest | Accept naga IR without WGSL text round-trip | **RESOLVED** — `compile_module` + `compile_module_full` public API |

### Downstream Impact

- **hotSpring**: Titan V (SM70) cold VFIO path now attempts FECS/GPCCS PIO boot — unblocks sovereign GPU validation
- **barraCuda/springs**: `naga::Module` direct ingest available for in-process callers bypassing text round-trip
- **Composition graphs**: Compile deadline prevents IPC server stall on pathological inputs

### Remaining (Pass 14 / convergence)

- `toadstool.validate` wiring (toadStool upstream)
- `barracuda.precision.route` (barraCuda upstream)
- Songbird `capability.resolve` (Songbird upstream)

---

*Supersedes: CORALREEF_SPRINT4_PTX_SM120_SUBGROUP_SCANS_MAY12_2026.md (archived)*
