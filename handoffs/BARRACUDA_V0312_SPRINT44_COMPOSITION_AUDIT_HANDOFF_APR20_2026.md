# barraCuda v0.3.12 — Sprint 44 Handoff (primalSpring Composition Audit)

**Date**: April 20, 2026
**Sprint**: 44 (composition audit — unblocks Level 5 for 3 springs)
**Version**: 0.3.12
**Tests**: 4,393+ passed, 0 failures
**IPC Methods**: 39 registered (+7 from Sprint 43's 32)
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT43_BTSP_PHASE3_DEEP_DEBT_HANDOFF_APR15_2026.md`

---

## Context

primalSpring v0.9.16 consolidated validation results from 5 springs (hotSpring L5,
healthSpring L4, wetSpring L4, ludoSpring L4, neuralSpring L3). barraCuda was
identified as the **single biggest blocker** — 6 missing JSON-RPC methods
blocked Level 5 certification for wetSpring, healthSpring, and neuralSpring.

## What Changed

### 6 New JSON-RPC Methods (32→39)

| Method | Domain | Implementation | Who Needs It |
|--------|--------|----------------|-------------|
| `stats.variance` | stats | CPU — `barracuda::stats::correlation::variance` | wetSpring, healthSpring |
| `stats.correlation` | stats | CPU — `barracuda::stats::correlation::pearson_correlation` | wetSpring, healthSpring |
| `linalg.solve` | linalg | CPU — Gaussian elimination with partial pivoting | wetSpring |
| `linalg.eigenvalues` | linalg | CPU — Jacobi iteration for symmetric matrices | wetSpring, neuralSpring |
| `spectral.fft` | spectral | CPU — Cooley-Tukey radix-2, zero-padded | wetSpring |
| `spectral.power_spectrum` | spectral | CPU — |X(k)|²/N from FFT | wetSpring |

### tensor.matmul_inline Convenience Path

Inline-data matrix multiply — springs send `lhs`/`rhs` as nested arrays, receive
product matrix directly. Eliminates the create→operate→extract three-call pattern.

### Fitts' Law Shannon Formula Fix

Corrected from `log₂(2D/W + 1)` to `log₂(D/W + 1)` per MacKenzie 1992 / ISO 9241-411.

### Response Schema Standardization

All scalar-returning methods now include a `"result"` key:
- `activation.fitts`: added `"result": mt` alongside `"movement_time"`
- `activation.hick`: added `"result": rt` alongside `"reaction_time"`
- `tensor.reduce`: added `"result": value` alongside `"value"`

Springs can uniformly extract `response["result"]` for any method.

### stats.std_dev Convention Documented

`stats.std_dev` and `stats.variance` responses include:
`"convention": "sample", "denominator": "N-1"` — explicit Bessel's correction.

### Verified (No Code Change Needed)

- **Hick's law**: default already uses `log₂(N)` (not `log₂(N+1)`)
- **perlin3d(0,0,0)**: returns 0.0 — existing test covers all integer lattice points

## Files Changed

- `crates/barracuda-core/src/ipc/methods/math.rs` — 6 new handlers + Fitts fix + schema
- `crates/barracuda-core/src/ipc/methods/mod.rs` — 7 new dispatch arms + REGISTERED_METHODS
- `crates/barracuda-core/src/ipc/methods/tensor.rs` — matmul_inline + reduce schema
- `crates/barracuda-core/src/ipc/mod.rs` — wire documentation tables
- `crates/barracuda-core/src/discovery.rs` — linalg/spectral domain descriptions
- `crates/barracuda-core/src/ipc/methods_tests/registry_tests.rs` — count 32→39

## Remaining

- `OdeRK45F64` batching for Richards PDE (airSpring-specific, low priority)

---

**License**: AGPL-3.0-or-later
