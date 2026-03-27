<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# neuralSpring V90 → toadStool/barraCuda/coralReef Upstream Rewire Handoff

**Date**: March 8, 2026
**From**: neuralSpring S132 (902 lib tests, 42/42 Python drift PASS, 218/218 validate\_all, 240 binaries)
**To**: barraCuda team, toadStool team, coralReef team
**Supersedes**: V89 handoff (Mar 7, 2026)
**Synced against**: barraCuda `a898dee`, toadStool S130+ (`bfe7977b`), coralReef Iteration 10 (`d29a734`)
**License**: AGPL-3.0-or-later

## Executive Summary

neuralSpring S132 is an **upstream rewire release** that catches up to the
latest barraCuda (deep debt: typed errors, named constants, lint compliance),
toadStool S130+ (clippy pedantic clean, unsafe audit, dependency audit,
spring sync confirming zero API breakage for all 5 springs, 19,777 tests),
and coralReef Iteration 10 (AMD E2E GPU dispatch verified on RDNA2/GFX1030,
conditional branch fix in `translate_if` + multi-pred RA merge, 990 tests).

**What changed since V89:**
- **Pin updates**: barraCuda `2a6c072` → `a898dee`, toadStool `88a545df` →
  `bfe7977b`, coralReef `72e6d13` → `d29a734`
- **Zero API breakage**: all 902 lib tests pass without code changes
- **Zero new clippy warnings** (pedantic + nursery)
- **42/42 Python drift checks PASS**
- **218/218 validate\_all PASS**
- **Lib test count**: 901 → 902

*This handoff is unidirectional: neuralSpring → ecosystem. No response expected.*

---

## 1. Upstream Changes Absorbed

### barraCuda `2a6c072` → `a898dee` (2 commits, ~1500 insertions)

| Commit | Summary |
|--------|---------|
| `d7ba7f3` | Doc updates: accurate counts post-audit |
| `a898dee` | Deep debt: typed errors (`BarracudaError` hierarchy), named constants (epsilon guards, workgroup sizes), test resilience (deterministic seeds), lint compliance |

**Impact on neuralSpring**: None — barraCuda's internal error refactoring
and constant naming don't change any public API surface that neuralSpring
uses. All 128+ barracuda import sites compile without modification.

Key changes in barraCuda that improve quality but require no neuralSpring action:
- Special function ops (Bessel, Hermite, Legendre, etc.) now use named tolerance constants
- `CoralBinary::binary` changed from `Vec<u8>` to `bytes::Bytes` (neuralSpring doesn't use this type)
- `discovery.rs` uses `LOCALHOST` constant instead of inline `"127.0.0.1"`
- Precision tests split into `precision_tests.rs` + `precision_tests_validation.rs`
- DF64 NAK rewriter tests split into `tests_nak.rs`

### toadStool `88a545df` → `bfe7977b` (4 commits, ~9800 insertions)

| Commit | Summary |
|--------|---------|
| `4e575b86` | Clippy pedantic clean, doc update, debris cleanup |
| `a7262515` | Spring sync: all 5 springs confirm zero API breakage |
| `73123cda` | Deep debt: unsafe audit (3 `unsafe fn` → safe alternatives), `flate2`/`procfs` pure Rust backends, hardcoding evolution, ~200 new tests |
| `bfe7977b` | Clean root docs, update test counts (19,777 tests), fix stale TESTING.md |

**Impact on neuralSpring**: None — toadStool's spring sync explicitly
confirms zero API breakage for neuralSpring. The unsafe audit and dependency
evolution are internal improvements.

### coralReef `72e6d13` → `d29a734` (2 commits, ~18700 insertions)

| Commit | Summary |
|--------|---------|
| `d5b51c5` | Iteration 9: E2E wiring, push buffer fix, debt reduction |
| `d29a734` | Iteration 10: AMD E2E GPU dispatch verified (RDNA2/GFX1030), docs updated, 990 tests (953 passing, 37 ignored for hardware) |

**Impact on neuralSpring**: Indirect — neuralSpring does not depend on
coralReef directly. However, coralReef Iteration 10's conditional branch fix
(`translate_if` + multi-pred RA merge) unlocks f64 shared-memory reduction
shaders via the sovereign path. Shaders like `sum_reduce_f64.wgsl` and
`chi_squared_f64.wgsl` with 3+ `workgroupBarrier()` calls now compile to
native SM70/SM89 binaries through coralReef, potentially bypassing the naga
zeros bug that gates 11 neuralSpring fused GPU tests.

---

## 2. P0 Fused GPU Regression — Status

The fused GPU reduction bug (VarianceF64, CorrelationF64, HmmBatchForwardF64
returning 0.0 or 524288 on Ada Lovelace + NVK) remains **open**. neuralSpring
gates 11 tests via canary variance probe. The coralReef sovereign path
(fixed in Iteration 10) provides a future alternative.

**Recommended action for barraCuda team**: Reclassify Ada Lovelace +
proprietary driver as `F64NativeNoSharedMem` in the `PrecisionRoutingAdvice`
path. This matches groundSpring's P0 request in V98.

---

## 3. Quality Gates

```
cargo check                                   → PASS (0 warnings)
cargo fmt --check                             → PASS
cargo clippy --all-targets --all-features     → 0 warnings (pedantic + nursery)
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps → PASS (234 files)
cargo test --lib                              → 902 passed, 0 failed
bash control/check_drift.sh                   → 42/42 PASS
```

---

## 4. neuralSpring BarraCUDA Usage (unchanged)

128+ import sites across 205 files, 25+ submodules exercised:

| Module | Sites | Key Usage |
|--------|-------|-----------|
| `device::WgpuDevice` | 128+ | GPU device initialization |
| `device::driver_profile::*` | ~10 | `Fp64Strategy`, `PrecisionRoutingAdvice`, `GpuDriverProfile` |
| `tensor::Tensor` | 40+ | LSTM, MLP, matmul, validators |
| `ops::bio::*` | 20+ | HMM, fitness, swarm, pairwise, locus variance |
| `ops::variance_f64_wgsl::VarianceF64` | 5+ | Fused Welford (canary-gated) |
| `ops::correlation_f64_wgsl::CorrelationF64` | 3+ | Fused correlation (canary-gated) |
| `ops::logsumexp::LogSumExp` | 3+ | HMM/softmax numerical stability |
| `ops::fft::*` | 5+ | FFT/IFFT/RFFT |
| `spectral::BatchIprGpu` | 5+ | Anderson localization |
| `nn::SimpleMlp` | 10+ | WDM surrogates |
| `nautilus::*` | 5+ | DriftMonitor, NautilusBrain |

---

## 5. Evolution Requests (carried from V89)

| Priority | Request | Team | Status |
|----------|---------|------|--------|
| **P0** | Reclassify Ada Lovelace as `F64NativeNoSharedMem` | barraCuda | Open |
| **P1** | Runtime GPU reduction smoke test in `ComputeDispatch` | toadStool | Open |
| **P2** | GPU tridiagonal eigenvector solver | barraCuda | Open |
| **P2** | End-to-end coralReef sovereign path for f64 reductions | toadStool + coralReef | Enabled by Iteration 10 |

---

## 6. WGSL Shaders Contributed (unchanged)

21 domain-specific WGSL shaders in `metalForge/shaders/` + 15 coralForge df64
shaders. 8 shaders in coralReef corpus (2 compile, 5 need df64 preamble,
1 needs external include). 42 total metalForge WGSL shaders.

---

## 7. Cross-Spring Alignment

neuralSpring is now aligned with groundSpring V98 (same pins: barraCuda
`a898dee`, toadStool `bfe7977b`, coralReef `d29a734`). Both springs confirm
zero API breakage from the upstream deep debt work. All springs are on
the same revision of the ecosystem.
