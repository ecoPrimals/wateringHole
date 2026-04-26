# barraCuda v0.3.12 — Sprint 45/45b Handoff (JSON-RPC Surface Expansion + Deep Debt)

**Date**: April 26, 2026
**Sprint**: 45 (JSON-RPC surface expansion) + 45b (deep debt — smart refactoring + DRY)
**Version**: 0.3.12
**Tests**: 4,393+ passed, 0 failures
**IPC Methods**: 50 registered (+11 from Sprint 44's 39)
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT44_COMPOSITION_AUDIT_HANDOFF_APR20_2026.md`

---

## Context

primalSpring Phase 45 identified ~18 statistical and ML JSON-RPC methods needed for
neuralSpring parity. After analysis, 11 registrations (9 new methods + 2 aliases)
were implemented in Sprint 45, bringing barraCuda to 50 total methods. Sprint 45b
followed with smart refactoring and DRY evolution.

## What Changed

### Sprint 45: 11 New Method Registrations (39→50)

| Method | Type | Implementation |
|--------|------|----------------|
| `stats.eigh` | Alias | → `linalg.eigenvalues` (existing) |
| `stats.pearson` | Alias | → `stats.correlation` (existing) |
| `stats.chi_squared` | New | CPU — Pearson χ² goodness-of-fit |
| `stats.anova_oneway` | New | CPU — one-way ANOVA with F-distribution p-value |
| `linalg.svd` | New | CPU — Jacobi one-sided SVD |
| `linalg.qr` | New | CPU — Householder QR decomposition |
| `spectral.stft` | New | CPU — short-time Fourier transform with Hann window |
| `activation.softmax` | New | CPU — numerically stable softmax |
| `activation.gelu` | New | CPU — GELU activation (tanh approximation) |
| `ml.mlp_forward` | New | CPU — inline MLP forward pass |
| `ml.attention` | New | CPU — scaled dot-product attention softmax(QK^T/√d_k)·V |

### Sprint 45b: Smart Refactoring + DRY Evolution

- **`methods/math.rs`**: 819→641 lines. Spectral handlers extracted to new `methods/spectral.rs`.
- **`methods/params.rs`**: Shared `extract_f64_array`, `extract_f64`, `extract_matrix`
  consolidated from duplicated code in `math.rs` and `ml.rs`.
- **`methods/ml.rs`**: New module for ML inference handlers (`mlp_forward`, `attention`).
- **`methods/spectral.rs`**: New module for spectral analysis (`fft`, `power_spectrum`, `stft`).

### F-Distribution P-Value (ANOVA)

Implemented `f_distribution_sf` using regularized incomplete beta function with
continued-fraction expansion — pure Rust, no external stats library dependency.

### New Tests

- 25 Sprint 45 coverage tests (`sprint45_tests.rs`)
- 11 ML coverage tests (`ml_tests.rs`)
- Total: 36 new tests

---

## 12-Axis Deep Debt Audit (Sprint 45b)

| Axis | Status |
|------|--------|
| File size (>800L) | Zero production files over 800 lines |
| TODO/FIXME | Zero |
| `unwrap()`/`expect()` | Zero in production |
| `unsafe` code | `#![forbid(unsafe_code)]` on barracuda-core |
| `async-trait` | Zero — native RPITIT |
| `Box<dyn Error>` / `Result<T, String>` | Zero in production |
| `println!`/`eprintln!` | Zero in production |
| Mocks in production | Zero |
| Hardcoded primal names | Zero |
| External C/FFI deps | Zero — pure Rust (blake3 `pure`, wgpu default-features=false) |
| `#[allow(` | Zero — all `#[expect(` with reason |
| Large files | Largest production file: 678L (btsp.rs) |

---

## Method Namespace Summary (50 total)

| Namespace | Methods | Count |
|-----------|---------|-------|
| `health.*` | liveness, readiness, check | 3 |
| `capabilities.*` | list | 1 |
| `identity.*` | get | 1 |
| `compute.*` | dispatch | 1 |
| `math.*` | sigmoid, log2 | 2 |
| `stats.*` | mean, std_dev, weighted_mean, variance, correlation, pearson, eigh, chi_squared, anova_oneway | 9 |
| `linalg.*` | solve, eigenvalues, svd, qr | 4 |
| `spectral.*` | fft, power_spectrum, stft | 3 |
| `activation.*` | fitts, hick, softmax, gelu | 4 |
| `noise.*` | perlin2d, perlin3d | 2 |
| `rng.*` | uniform | 1 |
| `ml.*` | mlp_forward, attention | 2 |
| `tensor.*` | create, matmul, matmul_inline, add, scale, clamp, reduce, sigmoid | 8 |
| `fhe.*` | ntt, pointwise_mul | 2 |
| `compute.*` (batch) | batch.submit, batch.status, batch.result | 3 |
| `doctor.*` | validate | 1 |
| `primal.*` | capabilities | 1 |
| `security.*` | session.create, session.verify | 2 |

---

## Outstanding Gaps

**barraCuda has zero open gaps.** All Phase 45c items resolved. BTSP 13/13 converged.
primalSpring live-validated all science calls (activation.fitts, activation.hick,
math.sigmoid, noise.perlin2d).

The only ecosystem item referencing barraCuda is:
- biomeOS `capability_registry.toml` has no `[translations.tensor]` for barraCuda's
  50 methods — this is a biomeOS-owned gap, not barraCuda.

---

**License**: AGPL-3.0-or-later
