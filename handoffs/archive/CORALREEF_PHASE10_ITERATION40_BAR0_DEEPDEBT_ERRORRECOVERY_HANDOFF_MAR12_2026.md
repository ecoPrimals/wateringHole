# coralReef Phase 10 — Iteration 40: BAR0 Absorption + Deep Debt Evolution + Error Recovery

**Date**: March 12, 2026
**From**: coralReef
**To**: hotSpring, toadStool, barraCuda, all springs
**Type**: Absorption + deep debt evolution + error recovery
**Status**: 1669 tests, 0 failures, zero clippy/fmt/doc warnings

---

## Summary

Iteration 40 absorbs the team's BAR0 breakthrough (sovereign MMIO GR init),
fixes 2 bugs discovered during deep audit, eliminates 11 hardcoded magic
numbers, implements dispatch error recovery (Gap 6), and deduplicates
chip-mapping logic.

---

## Key Changes

### 1. BAR0 Breakthrough Absorbed (from hotSpring)

Commits `23ed6f8`, `e160d89`, `996b7c1` landed via `git pull --rebase`:

- **`nv/bar0.rs`** (NEW): Sovereign BAR0 MMIO via sysfs `resource0` mmap
- **`gsp/applicator.rs`**: Address-aware firmware split (offset > 0x7FFC → BAR0)
- **`nv/mod.rs`**: Phased device open:
  - Phase 0: `try_bar0_gr_init()` — BAR0 register writes BEFORE channel creation
  - Phase 1: `VM_INIT`
  - Phase 2: `CHANNEL_ALLOC`
  - Phase 3: `try_fecs_channel_init()` — remaining FECS channel methods

### 2. Bug Fixes

| Bug | File | Impact | Fix |
|-----|------|--------|-----|
| `sm_version()` derived from `compute_class` instead of stored `sm_version` field | `nv/mod.rs` | Wrong SM reported for Turing (75→86) | Return `self.sm_version` directly |
| `pushbuf::class` unconditionally imports from `uvm` module | `pushbuf.rs` | Breaks nouveau-only builds (no `nvidia-drm` feature) | Import from `ioctl` constants (always available) |

### 3. Hardcoding Evolution (11 magic numbers eliminated)

| Constant | File | Old | New |
|----------|------|-----|-----|
| `SYNCOBJ_TIMEOUT_NS` | `nv/mod.rs` | `5_000_000_000` (×2) | Named constant + `syncobj_deadline()` helper |
| `GPU_PAGE_SIZE` / `GPU_PAGE_MASK` | `nv/mod.rs` | `0xFFF` | Named constants |
| `LOCAL_MEM_WINDOW_VOLTA` | `nv/mod.rs` | `0xFF00_0000_0000_0000_u64` | Named constant |
| `LOCAL_MEM_WINDOW_LEGACY` | `nv/mod.rs` | `0xFF00_0000_u64` | Named constant |
| `INVALIDATE_INSTR_AND_DATA` | `pushbuf.rs` | `0x11` | Named constant in `method` module |
| `DEFAULT_PUSHBUF_WORDS` | `pushbuf.rs` | `64` | Named constant |
| `DEFAULT_NV_SM` / `DEFAULT_NV_SM_NOUVEAU` | `coral-gpu/lib.rs` | bare `86` / `70` | Named constants |
| `FNV1A_OFFSET_BASIS` / `FNV1A_PRIME` | `coral-gpu/lib.rs` | bare hex literals | Named constants with docs |

### 4. Gap 6: Dispatch Error Recovery

`dispatch()` now delegates to `dispatch_inner()` with explicit temp-buffer
tracking. If any step fails (alloc, upload, submit), all temp buffers
are freed immediately instead of leaking until `sync()` or `Drop`.

```
dispatch() {
    temps = []
    result = dispatch_inner(shader, buffers, dims, info, &mut temps)
    if ok  → self.inflight.extend(temps)  // freed at sync()
    if err → free all temps immediately    // no leak
}
```

### 5. Additional Improvements

- **Chip mapping dedup**: `run_open_diagnostics` now calls `sm_to_chip(sm)` instead of duplicated match
- **Error logging**: `try_fecs_channel_init` logs firmware parse errors instead of silent discard
- **Method validation**: `gr_context_init` adds `debug_assert!(addr <= 0x7FFC)` for push buffer encoding limit
- **Doc fix**: `bar0.rs` module doc reference to private `firmware_parser` → plain text
- **Dead code re-fix**: `open_nv_sm70` `#[expect(dead_code)]` re-applied (team's commits overwrote iter 39 fix)

---

## Remaining Gaps (from hotSpring BAR0 handoff)

| Gap | Description | Owner | Status |
|-----|-------------|-------|--------|
| A | BAR0 validation (needs sudo) | hotSpring + toadStool | Code done, needs root |
| B | Root access solutions (udev rule / toadStool daemon) | toadStool | Design ready |
| C | UVM path activation (needs nvidia driver switch) | hotSpring | Code done, needs driver config |
| D | VFIO GPU backend (endgame) | coralReef + toadStool | Design phase |
| 5 | Knowledge base → compute init wiring | coralReef + toadStool | Open |
| 6 | Error recovery | coralReef | **CLOSED** (this iteration) |

---

## Files Changed

| File | Change |
|------|--------|
| `crates/coral-driver/src/nv/mod.rs` | `sm_version()` fix, `syncobj_deadline()`, named constants, `dispatch_inner` refactor, chip mapping dedup, error logging |
| `crates/coral-driver/src/nv/pushbuf.rs` | Class import portability, named constants, method validation |
| `crates/coral-driver/src/nv/bar0.rs` | Doc link fix |
| `crates/coral-driver/tests/hw_nv_nouveau.rs` | Dead code attribute re-applied |
| `crates/coral-gpu/src/lib.rs` | SM default constants, FNV constants |

## Metrics

| Metric | Iter 39 | Iter 40 |
|--------|---------|---------|
| Tests passing | 1667 | 1669 |
| Clippy warnings | 0 | 0 |
| fmt drift | 0 | 0 |
| Doc warnings | 1 | 0 |
| Files > 1000 LOC | 0 | 0 |
| Magic numbers eliminated | — | 11 |
| Bugs fixed | — | 2 |

---

*coralReef Phase 10 Iteration 40 — March 12, 2026*
