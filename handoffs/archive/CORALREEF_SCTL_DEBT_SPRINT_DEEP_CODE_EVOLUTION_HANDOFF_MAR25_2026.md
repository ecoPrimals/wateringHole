# coralReef: SCTL Debt Evolution Sprint + Deep Code Quality

**Date:** 2026-03-25
**From:** hotSpring (GPU cracking campaign)
**For:** coralReef, toadStool, barraCuda, primalSpring teams
**Experiments:** 091+ (SCTL myth busted)
**Tests:** 511 pass (coral-driver lib), 4,065 pass (workspace-wide)

---

## What Happened

Two sprints executed back-to-back:

1. **SCTL Debt Evolution Sprint** — debunked the "SCTL blocks PIO" myth that drove multiple experiment decisions, built the `FalconCapabilityProbe` runtime bit solver, and cleaned all false SCTL comments/logic across the codebase.

2. **Deep Code Quality Sprint** — systematic evolution of hardcoded magic numbers → register constants, unsafe code → safe wrappers, mock/placeholder cleanup, and smart refactoring across `coral-driver`.

## Discovery: SCTL Does NOT Block PIO

The IMEMC register on GM200+ falcons uses **BIT(24)** (`0x0100_0000`) for write auto-increment, not BIT(6) (`0x40`). All previous manual `coralctl` PIO tests used the wrong control word format, creating the false impression that SCTL=0x3000 blocks PIO access.

**PIO to IMEM/DMEM/EMEM works regardless of security mode** when the correct format is used. The Rust upload functions already used the correct format — the bug was only in manual CLI commands.

### Impact on Future GPU Cracking

- **FLR is unnecessary** for PIO access — Titan V lacks FLR anyway
- **SBR for SCTL clearing** was unnecessary
- **Warm handoff to preserve firmware** unnecessary for PIO reasons (may still be useful for other reasons)
- **The real remaining blocker is DMA configuration**: FBIF mode, FBHUB MMU initialization, page tables — not security mode

## New Infrastructure: FalconCapabilityProbe

**File:** `coral-driver/src/nv/vfio_compute/falcon_capability.rs`

Runtime bit solver that discovers register layouts on actual hardware instead of hardcoding assumptions:

- `PioCtrl` — newtype for safe PIO control words
- `FalconCapabilities` — aggregated capabilities per falcon instance (version, security mode, PIO layout, CPU control layout)
- `FalconPio` — safe PIO interface backed by discovered capabilities
- `probe_falcon()` / `probe_all_falcons()` — dynamic discovery

**Why this matters for all GPU generations:** The IMEMC bit position varies by falcon version. Hardcoding `BIT(24)` works for GM200+ but fails on earlier generations. The probe discovers the correct layout at runtime, making the PIO interface portable across any NVIDIA GPU.

## Deep Code Evolution (coral-driver)

### Register Constants — 60+ Hardcoded Offsets Eliminated

New constants added to `registers.rs`:

| Constant | Value | Replaces |
|----------|-------|----------|
| `misc::PMC_ENABLE` | `0x0000_0200` | `let pmc_enable: usize = 0x200` (6 sites) |
| `misc::PMC_UNK260` | `0x0000_0260` | `0x000260` in strategy_mailbox |
| `misc::PGRAPH_STATUS` | `0x0040_0700` | `r(0x0040_0700)` in gr_engine_status |
| `misc::PFIFO_SCHED_EN` | `0x0000_2504` | `r(0x0000_2504)` in gr_engine_status |
| `falcon::ENGCTL` | `0x3C0` | `w(0x3C0, 0x01)` (8+ sites across 4 files) |
| `falcon::ITFEN` | `0x048` | `w(0x048, ...)` (10+ sites across 5 files) |
| `falcon::IRQMODE` | `0x00C` | `0x00c` in strategy_mailbox |
| `falcon::WATCHDOG` | `0x034` | `0x034` in strategy_mailbox |
| `falcon::MTHD_DATA/CMD/STATUS/STATUS2` | `0x500..0x804` | Local constants in fecs_method |
| `falcon::EXCEPTION_REG` | `0xC24` | `0x0040_9c24` in strategy_mailbox |
| `falcon::GR_CLASS_CFG` | `0x802C` | `0x0040_802c` in strategy_mailbox |

**Files changed:** `strategy_mailbox.rs`, `strategy_sysmem.rs`, `strategy_hybrid.rs`, `strategy_vram.rs`, `sec2_hal.rs`, `fecs_method.rs`, `diagnostics.rs`, `submission.rs`, `mod.rs`

### Unsafe Code Evolution

| File | Change |
|------|--------|
| `dma.rs` | `*mut u8` → `NonNull<u8>`; removed runtime null asserts; DRY'd `dma_map_with_retry`/`dma_map_once`; added safe `volatile_write_u32/u64` and `volatile_read_u32` methods |
| `submission.rs` | Eliminated 4 `unsafe` blocks via new `DmaBuffer` safe volatile methods |
| `mmio.rs` | Audited — already minimal irreducible unsafe (volatile MMIO) |
| `sysfs_bar0.rs` | Audited — already minimal irreducible unsafe (mmap) |
| `cache_ops.rs` | Audited — already idiomatic cfg-gated stubs |

### Shared Helpers Extracted

New helpers in `boot_result.rs`:
- `poll_falcon_boot()` — shared falcon boot polling with timeout
- `dmem_nonzero_summary()` — shared DMEM diagnostic dump
- `dmem_detail()` — shared DMEM word detail

### Mock/Placeholder Cleanup

Replaced "dummy"/"placeholder" language in 4 production files with accurate descriptions of actual behavior.

## What This Means for Each Team

### coralReef
- **FalconCapabilityProbe** is the foundation for supporting new GPU generations. When cracking a new card, `probe_all_falcons()` discovers the register layout automatically.
- All register constants now centralized in `registers.rs` — new contributors can add GPU support by adding constants, not hunting hex.
- `DmaBuffer::volatile_write_u32/u64/read_u32` eliminates the most common unsafe pattern in GPU dispatch code.

### toadStool / barraCuda
- No direct changes, but the PIO discovery pattern (probe hardware → build capability struct → use safe API) is the same pattern used in `WgslOptimizer` and `GpuDriverProfile`. The primal ecosystem converges on capability-based dispatch.

### primalSpring
- The "discover other primals at runtime" principle is now implemented at the hardware level: `FalconCapabilityProbe` discovers falcon capabilities the same way primals discover each other.

## Quality Metrics

- **511 lib tests pass** (0 failures, 15 ignored)
- **2 pre-existing warnings** (not introduced by this sprint)
- **Zero new `unsafe` blocks** — net reduction of 4 unsafe blocks
- **Zero `unwrap()` in production code**
- **Zero `todo!()` / `unimplemented!()`**
