SPDX-License-Identifier: AGPL-3.0-or-later

# wetSpring → ecoPrimals Handoff V92D — Deep Debt Evolution + Pedantic Hardening

**Date**: March 2, 2026
**From**: wetSpring (V92D)
**To**: ecoPrimals team
**ToadStool pin**: S79 (`f97fc2ae`)
**License**: AGPL-3.0-or-later
**Supersedes**: V91 (Deep Debt Resolution), V92C (Deep Audit)

---

## Executive Summary

V92D resolves all remaining library-level code quality debt identified in the
V92C audit. The crate is now panic-free in all library code, fully pedantic-clean
under `--all-features`, and modernized to Rust 2024 idiomatic standards. 1,309
tests pass with zero failures.

Key changes:
- ESN bridge: `panic!` → `Result`-based error handling
- IPC handlers: `MetricCtx` struct pattern replaces 8-argument function
- 50+ validation binaries: doc backticks, lossless casts, modern idioms
- Shared `validation::bench()` timing helper
- Full `--all-features -W clippy::pedantic` clean (not just per-target)

---

## Part 1: Code Quality Evolution

### Panic Elimination

The last `panic!` in library code was in `bio/esn/toadstool_bridge.rs`, where
the Tokio runtime builder failure path used `panic!`. V92D converts `block_on()`
to return `Result<O, BarracudaError>`, with all 6 call sites using `??` chaining.

**Impact**: wetSpring library code can now be used in contexts where panics are
unacceptable (e.g., embedded in a long-running primal service, neuromorphic
pipeline). This is the standard other Springs should follow.

### Handler Refactor

`ipc/handlers/science.rs` had an 8-argument `insert_metric_if_requested` function
that violated clippy pedantic `too_many_arguments`. Refactored to:

- `MetricCtx<'a>` struct — holds shared dispatch context (metrics, output map,
  GPU device, threshold)
- `dispatch_metric()` — pure function selecting GPU result or CPU fallback
- `MetricCtx::insert()` — method that checks if metric is requested and dispatches

### Modern Idioms

Applied across 50+ files:

| Pattern | Why |
|---------|-----|
| `f64::from(i)` over `i as f64` | Compile-time guarantee of lossless conversion |
| `f64::midpoint(a, b)` over `(a + b) / 2.0` | Overflow-safe, single-rounding |
| `val.mul_add(b, c)` over `c + val * b` | Hardware FMA when available |
| `println!("{x}")` over `println!("{}", x)` | Inlined format args (Rust 2021+) |
| `if let` over single-arm `match` | Idiomatic destructuring |
| `(lo..=hi).contains(&x)` over manual range | Self-documenting range check |

---

## Part 2: Barracuda/ToadStool Usage Review

### Current State (Fully Lean)

| Metric | V92C | V92D | Change |
|--------|:----:|:----:|--------|
| Tests | 1,276 | 1,309 | +33 |
| ToadStool primitives | 93 | 93 | Stable |
| Local WGSL | 0 | 0 | Stable |
| Unsafe code | 0 | 0 | Stable |
| Panics in library | 1 | 0 | **Eliminated** |
| Clippy warnings | 0 | 0 | Stable (now `--all-features`) |
| Named tolerances | 103 | 103 | Stable |

### Absorption Path

wetSpring is fully lean on ToadStool S79. All 93 primitives are consumed via
`compile_shader_universal`. No new Write or Compose work is needed. The remaining
evolution is upstream:

1. `MultiHeadEsn::from_exported_weights()` — for ESN GPU migration
2. `FitResult` named fields — for safer parameter access
3. `MockGpuF64` — for CI-testable GPU paths

---

## Part 3: Cross-Spring Patterns for Adoption

### Recommended for All Springs

1. **Zero panics in library code**: Convert all `panic!`/`unwrap()`/`expect()` in
   library code to `Result`-based error handling. wetSpring enforces this with
   `#![deny(clippy::expect_used, clippy::unwrap_used)]` crate-wide.

2. **`--all-features` pedantic gate**: Running clippy only on default features
   misses feature-gated code paths. wetSpring V92D runs:
   ```
   cargo clippy --workspace --all-targets --all-features -- -D warnings -W clippy::pedantic
   ```

3. **Provenance classification**: Every validation binary should carry:
   ```rust
   //! Validation class: {Analytical|GPU-parity|Python-parity|Pipeline|Cross-spring|Synthetic}
   //! Provenance: {script path, commit, date, hardware}
   ```

4. **Named tolerances**: No bare float literals in validation checks. All thresholds
   should be named constants with documented scientific justification.

---

## Part 4: Paper Queue Control Summary

All 52 reproduced papers + 6 Gonzales reproductions use open data exclusively.
Three-tier validation is complete for all eligible papers.

| Tier | Description | Status |
|------|-------------|--------|
| **BarraCuda CPU** | Rust math matches Python baselines | 54/54 papers |
| **BarraCuda GPU** | GPU math matches CPU reference | 48/48 papers |
| **metalForge** | Substrate-independent output | 41/41 papers |
| **Controls** | Open data, no proprietary dependencies | 58/58 papers |

Hardware control chain: open data → barracuda CPU → barracuda GPU → metalForge
mixed hardware. Each tier's output is validated against the previous tier.

---

## Part 5: Quality Gate

| Gate | V92C | V92D |
|------|------|------|
| `cargo fmt` | PASS | PASS |
| `cargo clippy --all-features -W pedantic` | PASS (per-target) | PASS (all-features) |
| `cargo test --workspace` | 1,276 (0 fail) | 1,309 (0 fail) |
| `cargo doc --no-deps` | PASS | PASS |
| Zero unsafe | PASS | PASS |
| Zero panics (library) | 1 remaining | **PASS** (0) |
| AGPL-3.0 headers | PASS | PASS |

---

## Part 6: Next Steps

1. **ToadStool S80 sync** — when available, pin update and revalidation
2. **Experiment protocol gap** — Exp267-272 and Exp273-286 need protocol `.md` files
   in `experiments/`. The validation binaries exist and pass; the documentation lags.
3. **Coverage rerun** — `cargo-llvm-cov` should be rerun with the 33 new tests to
   update the 95.86% baseline.
4. **Paper 19 (Liu fungi-bacteria)** — watch for publication; ready to reproduce.

---

*wetSpring V92D — 1,309 tests, 272 experiments, 7,220+ checks, 255 binaries,
93 ToadStool primitives, 0 local WGSL, 0 unsafe, 0 panics. Fully lean and
pedantic-clean across all features.*
