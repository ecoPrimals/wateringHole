# coralReef — Iteration 47: Deep Debt Evolution + Modern Idiomatic Rust

**Date**: March 15, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 47
**Builds on**: CORALREEF_PHASE10_ITERATION46_STRUCTURAL_REFACTOR_COVERAGE_HANDOFF_MAR15_2026

---

## Summary

Deep debt evolution pass: unsafe code elimination, zero-copy evolution
(`KernelCacheEntry.binary` → `bytes::Bytes`), driver string centralization
(4 constants in `preference.rs`), production panic elimination (6 `panic!()`
→ `warn!` + `debug_assert!`), `runner.rs` experiment delegation (2509→778
LOC), `rm_client.rs` helper extraction (1000→944 LOC), FenceTimeout constant,
unwrap → `Option::zip`. +15 new tests. 1819 tests passing. All checks green.

## Changes

### Unsafe Code Elimination

Removed `unsafe { std::slice::from_raw_parts_mut }` in NOP pushbuf
initialization (`diagnostic/runner.rs`) → safe `nop_pb.as_mut_slice()`.
`DmaBuffer` already provides a safe mutable slice API.

### Zero-Copy Evolution

`KernelCacheEntry.binary: Vec<u8>` → `bytes::Bytes`. Eliminates data
copies in `to_cache_entry()` / `from_cache_entry()` by leveraging `Bytes`'s
Arc-based cheap cloning. Serde roundtrip verified.

### Driver String Centralization

Four driver name constants in `coral-gpu/src/preference.rs`:

| Constant | Value |
|----------|-------|
| `DRIVER_VFIO` | `"vfio"` |
| `DRIVER_NOUVEAU` | `"nouveau"` |
| `DRIVER_AMDGPU` | `"amdgpu"` |
| `DRIVER_NVIDIA_DRM` | `"nvidia-drm"` |

All match arms and string comparisons in `coral-gpu/src/lib.rs` use these
constants. No string literals for driver names in production code.

### Production Panic Elimination

6 `panic!()` calls in `sm70_instr_latencies.rs` replaced with `warn!` +
`DEFAULT_LATENCY` or `debug_assert!`. The compiler now gracefully degrades
on unexpected instruction patterns rather than crashing.

### runner.rs Experiment Delegation

`diagnostic/runner.rs` still contained a 2000+ line inline experiment
dispatch that duplicated the `experiments/` module logic. Replaced with
a single call to `experiments::run_experiment(&mut ctx)`. File reduced
from 2509 to 778 lines.

### rm_client.rs Helper Extraction

UUID parsing (`parse_gid_to_uuid`, `hex_nibble`) and raw ioctl
(`raw_nv_ioctl`) extracted to `rm_helpers.rs`. `rm_client.rs` reduced
from 1000 to 944 lines. 9 new unit tests for UUID parsing.

### FenceTimeout Constant

Hardcoded `5000` in `DriverError::FenceTimeout` → `SYNC_TIMEOUT.as_millis()`.

### Production unwrap Elimination

`pb2.unwrap()` in runner.rs → `alt_pbdma.zip(pb2)` pattern with
graceful skip when secondary PBDMA is unavailable.

### Metrics

| Metric | Before (Iter 46) | After (Iter 47) |
|--------|-------------------|------------------|
| Tests passing | 1804 | 1819 |
| Tests ignored | 61 | 61 |
| Line coverage | 66.43% | 66.43% |
| Clippy warnings | 0 | 0 |
| Files >1000 lines | 0 | 0 |
| unsafe from_raw_parts_mut | 1 | 0 |
| Hardcoded driver strings | ~20 | 0 (4 constants) |
| panic!() in latencies | 6 | 0 (warn + debug_assert) |

### Key Source Files

| File | Change |
|------|--------|
| `crates/coral-driver/src/vfio/channel/diagnostic/runner.rs` | 2509→778 LOC, experiment delegation, unsafe fix, unwrap fix |
| `crates/coral-driver/src/nv/uvm/rm_helpers.rs` | NEW — UUID parsing + raw ioctl (extracted from rm_client.rs) |
| `crates/coral-gpu/src/lib.rs` | KernelCacheEntry.binary → Bytes, driver string constants |
| `crates/coral-gpu/src/preference.rs` | DRIVER_VFIO/NOUVEAU/AMDGPU/NVIDIA_DRM constants |
| `crates/coral-reef/src/codegen/nv/sm70_instr_latencies.rs` | 6 panic!() → warn! + debug_assert! |
| `crates/coral-driver/src/nv/vfio_compute.rs` | FenceTimeout → SYNC_TIMEOUT constant |

## For toadStool

No action required. Public API unchanged. Driver constants are
`pub` if toadStool needs them for display — accessible via
`coral_gpu::preference::DRIVER_*`.

## For hotSpring

No action required. Diagnostic matrix works identically. The unsafe
NOP pushbuf init is now safe.

## For barraCuda

`KernelCacheEntry.binary` is now `bytes::Bytes` instead of `Vec<u8>`.
If barraCuda constructs `KernelCacheEntry` directly, update the field
type. `Bytes::from(vec)` is a zero-cost conversion. serde roundtrip
unchanged.

---

*coralReef Iteration 47 — Deep debt evolution. Unsafe eliminated.
Zero-copy Bytes. Driver constants. Production panics → graceful degradation.
1819 tests. Modern idiomatic Rust.*
