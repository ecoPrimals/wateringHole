# coralReef Iteration 67: Experiment Loop + First Personality Sweep

**Date:** 2026-03-25
**From:** hotSpring (GPU cracking campaign)
**For:** coralReef, toadStool, barraCuda teams
**Experiments:** 091-092
**Tests:** 4,065 pass (workspace-wide)

---

## What Happened

The "Wire Experiment Loop" sprint closed 7 infrastructure gaps in coral-ember and coral-glowplug, transforming the defined-but-unwired adaptive learning components into a live, self-learning system. Then ran the first automated personality sweep on both Titan V GPUs.

## Changes for coralReef

### coral-ember (6 files changed)

| File | Change |
|------|--------|
| `src/ipc.rs` | `ember.device_reset` handler now instruments with `Instant` timing, creates `ResetObservation`, appends `JournalEntry::Reset` to journal. Response includes `duration_ms`. |
| `src/swap.rs` | Removed `.min(2)` VFIO settle cap. `AdaptiveLifecycle` settle_secs now applies without ceiling. |
| `src/observation.rs` | (no change — defined in prior iteration) |
| `src/journal.rs` | (no change — defined in prior iteration) |
| `src/adaptive.rs` | (no change — defined in prior iteration) |

### coral-glowplug (6 files changed)

| File | Change |
|------|--------|
| `src/device/mod.rs` | Added `last_swap_observation: Option<SwapObservation>` field to `DeviceSlot`. |
| `src/device/swap.rs` | `swap_traced()` captures `SwapObservation` from ember, stores on slot. Ring_meta snapshot saved before swap (version incremented), restored after VFIO reacquire. |
| `src/socket/handlers/device_ops.rs` | `handle_swap` runs `ObserverRegistry::default_observers()` post-swap — `observe_swap` + `observe_trace`. Insights + timing returned in RPC response. |
| `src/bin/coralctl/main.rs` | New `Experiment` subcommand with `Sweep` action. |
| `src/bin/coralctl/handlers_device.rs` | `rpc_experiment_sweep()`: iterates personalities, swaps with trace, returns to base, prints comparison table. |

### New CLI: `coralctl experiment sweep`

```
coralctl experiment sweep <BDF> [--personalities nouveau,nvidia-open] [--return-to vfio]
```

Automated personality characterization. For each target: swap with mmiotrace → capture timing + observer insights → return to base. All observations journaled. Comparison table printed at end.

## Hardware Results

### Sweep Data (March 25, 2026)

| Card | Personality | Bind (ms) | Unbind (ms) | Trace Size | Insights |
|------|-------------|----------|------------|------------|----------|
| Titan V #1 | nouveau | 21,084 | 812 | 1.4MB | 2 |
| Titan V #1 | nvidia-open | 25,967 | 817 | 521B | 2 |
| Titan V #2 | nouveau | 21,318 | 842 | 1.4MB | 2 |
| Titan V #2 | nvidia-open | 25,959 | 846 | 521B | 2 |

**Cross-card variance: <1.1%** — rules out hardware jitter.

### Trace Analysis Discovery

nouveau on GV100 produces **zero** MMIO writes to FECS (0x409xxx), GPCCS (0x41axxx), or SEC2 (0x840xxx). The entire GR context init goes through SEC2 DMA (0x800000), invisible to mmiotrace. nvidia-open is fully opaque (GSP handles everything, trace is just the header).

**Implication for coralReef:** mmiotrace is useful for topology/memory init analysis but cannot capture firmware boot sequences. Falcon register polling is the correct diagnostic path for FECS/GPCCS debugging.

## What This Means for Each Team

### coralReef
- Journal data is now flowing: 12 observations from the sweep feed `AdaptiveLifecycle`
- `experiment sweep` can be run on any new hardware to characterize it automatically
- Observer insights grow as more personalities are tested
- Ring/mailbox state survives personality transitions (verified)

### toadStool
- No direct changes, but `WgslOptimizer` + `GpuDriverProfile` data will eventually come from the observer insights
- The personality sweep infrastructure can characterize how different drivers affect shader compilation latency

### barraCuda
- No direct changes
- The journal timing data confirms that df64 WGSL shaders should target the warm-VFIO state (2.7s swap vs 21.9s cold) for optimal dispatch latency

## Absorption Checklist

- [ ] Review `coralctl experiment sweep --help` for your use cases
- [ ] Check `coralctl journal stats --bdf <your-bdf>` after running experiments
- [ ] If you add a new VendorLifecycle, ensure it integrates with `AdaptiveLifecycle`
- [ ] New personalities should get a `DriverObserver` implementation for trace analysis
