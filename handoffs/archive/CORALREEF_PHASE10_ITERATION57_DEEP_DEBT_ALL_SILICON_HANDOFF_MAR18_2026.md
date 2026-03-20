<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 57 Handoff

**Date**: March 18, 2026  
**Primal**: coralReef  
**Phase**: 10 — Spring Absorption + Compiler Hardening  
**Iteration**: 57

---

## Summary

Deep debt evolution across the entire codebase: specs updated to v0.6.0
targeting all available silicon, smart refactoring, GP_PUT cache flush
experiment for VFIO last-mile dispatch, production error handling evolution,
unsafe code consolidation through VolatilePtr, AMD metal and Intel arch
stubs evolved to real implementations, hardcoded values extracted to named
constants, and coverage expansion (+33 new tests, 2560 total).

---

## Changes

### 1. Specs Evolution (v0.6.0)
- `CORALREEF_SPECIFICATION.md`: Updated target hardware (Titan V x2 VFIO, RTX 5060, MI50 planned), new "Sovereign Pipeline — All Silicon" section with dispatch paths, boot sovereignty, FECS status, sovereignty roadmap
- `SOVEREIGN_MULTI_GPU_EVOLUTION.md`: Fixed stale paths, updated dependency evolution table (DRM/nix/Linux headers all replaced), full NVIDIA evolution table, timeline through Phase 10a-10f

### 2. Smart Refactor — socket.rs (1488 → 556 lines)
- Tests extracted to `socket_tests.rs` (~930 lines)
- Production code well under 1000-line limit
- 131/131 glowplug tests pass unchanged

### 3. GP_PUT Cache Flush (H1 Experiment)
- Added `clflush_range()` on GPFIFO slot + USERD page before doorbell write
- Added `memory_fence()` (x86 mfence) between flush and MMIO doorbell
- Hypothesis: CPU cache holds stale GP_PUT, PBDMA reads zero via DMA
- Location: `nv/vfio_compute/submission.rs`

### 4. Production .expect() Evolution
- Signal handlers: `.expect()` → `.or_exit()` in coralreef-core main
- GSP rm_observer: `.expect("serialize")` → `?` with proper Result
- DMA buffer: SAFETY comment documenting Layout invariant
- SSA repair: clarified ICE messages
- Encoder/RA: verified messages are descriptive compiler invariants

### 5. Unsafe Code Consolidation
- All raw `read_volatile`/`write_volatile` → `VolatilePtr` wrapper
  - VFIO submission (GP_PUT, GPFIFO, doorbell)
  - UVM compute (GPFIFO, doorbell, GP_GET)
  - Diagnostic runner (GP_GET, GP_PUT)
  - SysFS BAR0 (read_u32)
- SAFETY comments on all `from_raw_parts`, `Send/Sync` impls, `OwnedFd::from_raw_fd`

### 6. AMD Metal Evolution
- Evolved from `None` return to full `AmdVegaMetal` with GFX906 register offsets
- Registers: SMC_IND_INDEX/DATA, GRBM_STATUS/STATUS2, GB_ADDR_CONFIG, MC_VM_FB_LOCATION
- Awaiting MI50 hardware for validation

### 7. Intel GPU Architecture
- Added `Dg2Alchemist` (Arc A770/A750/A380) and `XeLpg` (Meteor Lake) variants
- `#[allow(dead_code)]` — backend planned, register addresses TBD

### 8. Hardcoding Evolution
- New `coral-glowplug/src/pci_ids.rs`: NVIDIA_VENDOR_ID, TITAN_V_DEVICE_ID, TITAN_V_VFIO_IDS
- New `coral-driver/src/nv/identity.rs`: unified `chip_name(sm)` table
- Deduplicated sm_to_chip() in probe.rs and vfio_compute/mod.rs

### 9. Coverage Expansion (+33 tests → 2560 total)
- GSP knowledge: all known chip names
- GSP firmware_parser: truncated/empty/out-of-range headers
- GSP applicator: split routing, mock register map, dry run
- MMIO VolatilePtr: construction, read/write roundtrip, clone
- NV identity: all SM versions 30-120
- GlowPlug pci_ids: format validation, cmdline parsing
- Driver error: Display formatting, From conversions

### 10. Clippy Evolution
- `map_or(true, |v| v.is_empty())` → `is_none_or(|v| v.is_empty())` (Rust 1.93)
- `#[expect(clippy::wildcard_imports)]` → `#[allow(...)]` (test-build variance)
- Doc backtick fixes for `lower_f64`, `repair_ssa`, `assign_regs` references
- `pub(crate) use` in private module → `pub use`

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests (workspace) | 2560 pass, 0 fail, 90 ignored |
| Tests (glowplug) | 131 pass |
| Clippy | 0 warnings (`-D warnings`) |
| Files > 1000 LOC | 0 (socket.rs 1488 → 556) |
| Production todo!/unimplemented! | 0 |
| Production .expect() (service) | 0 (evolved to Result) |
| Unsafe blocks (coral-driver) | ~80 (all with SAFETY comments) |
| New files | pci_ids.rs, socket_tests.rs, identity.rs, amd_metal.rs |

---

## Cross-Primal Impact

- **hotSpring**: GP_PUT cache flush may resolve VFIO dispatch last-mile — retest with Titan V
- **toadStool**: AMD metal GFX906 registers prepare for MI50 dispatch validation
- **barraCuda**: Intel Dg2/XeLpg GPU arch variants available for future backend

---

## Next Steps (Iteration 58+)

1. **GP_PUT hardware validation**: Test cache flush on live Titan V VFIO
2. **UVM hardware validation**: RTX 5060 on-site compute dispatch
3. **FECS firmware loader**: Continue from hotSpring Exp 068 breakthrough
4. **AMD MI50 hardware swap**: Validate GFX906 metal register offsets
5. **Coverage target 70%**: Expand coral-driver VFIO and codegen tests
