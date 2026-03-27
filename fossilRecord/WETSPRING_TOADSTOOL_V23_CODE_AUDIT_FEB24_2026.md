# wetSpring → ToadStool Handoff v23 — Deep Code Audit & Evolution Learnings

**Date:** February 24, 2026
**Phase:** 38 (post-audit)
**Author:** wetSpring validation pipeline
**Previous:** [v15 — ODE Generic Absorption](WETSPRING_TOADSTOOL_V15_ODE_GENERIC_FEB22_2026.md)

---

## Executive Summary

wetSpring completed a comprehensive code audit across completeness, quality,
validation fidelity, dependency health, evolution readiness, and test coverage.
All issues resolved. This handoff documents findings, learnings, and action
items relevant to ToadStool/BarraCUDA evolution.

**Key metrics:**

| Metric | Before Audit | After Audit |
|--------|:------------|:-----------|
| Library tests | 680 | 728 (+48) |
| Total tests (barracuda + forge) | 759 | 845 (+86) |
| Library coverage (llvm-cov) | ~93% | **95.67%** |
| Production mocks | 1 (ESN diagonal solve) | **0** |
| Deprecated buffering APIs | 0 marked | **3 marked** (`parse_fastq`, `parse_mzml`, `parse_ms2`) |
| Hot-path clones eliminated | — | 2 (merge_pairs, derep) |
| Validation binaries migrated to streaming | 0 | 3 |

---

## Part 1: ESN Ridge Regression — Diagonal → Cholesky

### What Changed

The `Esn::train()`, `train_stateful()`, and `train_stateless()` methods used
a **diagonal approximation** for ridge regression that ignored cross-correlations
between reservoir neurons. This was a production mock — the comment said
"simplified: use diagonal approximation for speed."

**Replaced with:**

1. Proper **Cholesky factorization** (`L·Lᵀ = SᵀS + λI`) with forward/backward
   substitution — O(n³/3) for n_res neurons, exact ridge regression solution.
2. **Flat state buffers** (`Vec<f64>` row-major) replacing `Vec<Vec<f64>>` —
   eliminates `self.state.clone()` in all training loops. Uses
   `extend_from_slice` instead.
3. Defensive fallback to diagonal solve if Cholesky fails (should never happen
   with λ > 0, but robust).
4. Shared `solve_ridge()` free function used by all three training methods.

### Why ToadStool Cares

The Cholesky solver is a reusable primitive. When ToadStool absorbs ESN or
builds a generic reservoir computing module, the solver should use the
upstream `linalg::cholesky` (once it exists) rather than the local
implementation in `esn.rs`. The local implementation is correct and tested
but not optimized for large n_res.

**Absorption candidate:** `cholesky_factor()` and `solve_ridge()` from
`barracuda/src/bio/esn.rs` → ToadStool `linalg::cholesky_solve`.

### Validation Impact

All 8 ESN validation binaries continue to pass — they use threshold-based
quality gates ("> 40% accuracy", "> 70% agreement"), not exact expected values.
The proper Cholesky solve produces **better** readout weights because it
accounts for cross-correlations between reservoir neurons.

---

## Part 2: Streaming I/O Migration

### What Changed

Three validation binaries migrated from deprecated `parse_*()` (buffer entire
file) to streaming APIs:

| Binary | Old API | New API | Rationale |
|--------|---------|---------|-----------|
| `validate_fastq.rs` (bulk loop) | `parse_fastq` → `records.len()` | `stats_from_file` → `stats.num_sequences` | Only needed count |
| `validate_mzml.rs` | `parse_mzml` + `compute_stats` | `stats_from_file` | Only needed aggregate stats |
| `validate_pfas.rs` | `parse_ms2` → iterate all | `stats_from_file` + `Ms2Iter` | Stats + per-spectrum streaming |

### Why ToadStool Cares

The streaming APIs (`FastqIter`, `MzmlIter`, `Ms2Iter`, `stats_from_file`)
are the correct I/O primitives for GPU pipelines. When data streams from
disk → CPU parser → GPU buffer, the parser should never buffer the entire
file. The deprecated `parse_*()` functions remain for backward compatibility
but should not be used in new code.

**Pattern for ToadStool GPU pipelines:**

```
File → streaming iterator → batch into GPU buffer → dispatch
```

The `stats_from_file` path for mzML is particularly efficient — it reads
XML metadata without decoding binary arrays (zero-copy stats).

---

## Part 3: Clone Optimization Learnings

### Eliminated Clones

| Module | Old Pattern | New Pattern | Impact |
|--------|-------------|-------------|--------|
| `merge_pairs.rs` | `if let Some(ref rec)` + `rec.clone()` | `if let Some(rec)` (move) | Eliminates per-record clone in merge loop |
| `derep.rs` | `map.entry(key.clone())` every record | `Entry::Occupied/Vacant` match | Key cloned only for new unique sequences |

### Clones That Cannot Be Eliminated (by design)

| Module | Clone | Reason |
|--------|-------|--------|
| `placement.rs:84` | `tree.clone()` | Recursive tree reconstruction — inherent to persistent data structure |
| `chimera.rs:217` | `seqs[r.query_idx].clone()` | API takes `&[Asv]`, returns `Vec<Asv>` — needs ownership |
| `bootstrap.rs:61` | `columns[idx].clone()` | Resampled columns for new alignment |
| ESN training loops | `extend_from_slice` | Already optimized — flat buffer, no per-neuron Vec allocation |

### Pattern for ToadStool

When designing GPU pipeline APIs, prefer:
- Move semantics over clone (`if let Some(rec)` not `Some(ref rec)`)
- `Entry::Occupied/Vacant` over `entry(key.clone())`
- Flat buffers (`Vec<f64>` row-major) over `Vec<Vec<f64>>`

---

## Part 4: Coverage Analysis

### Overall: 95.67% Line Coverage

| Category | Coverage | Notes |
|----------|---------|-------|
| Bio modules (45) | 94–100% | Most above 96% |
| I/O parsers | 87–99% | Error paths in streaming |
| Encoding/error/tolerances | 95–100% | Well-covered |
| `ncbi.rs` | 76% | Network/curl paths — untestable without external service |
| `bench/power.rs` | 60% | GPU power monitoring — requires nvidia-smi |
| `bio/ncbi_data.rs` | 69% | Large synthetic data generators, many branches |

### Modules Added by This Audit (48 new tests)

| Module | New Tests | Coverage Δ |
|--------|:---------:|-----------|
| `bio/esn.rs` | 21 | First unit tests for ESN: Lcg, EsnConfig, train, predict, NPU |
| `bio/ncbi_data.rs` | 17 | JSON helpers, data loaders, synthetic fallback, biome params |
| `ncbi.rs` | 10 | encode_entrez_term edge cases, parse_api_key_toml, http_get error |

---

## Part 5: External Dependency Audit

### Runtime Dependencies (1)

| Dep | Version | Purpose | ecoBin Status |
|-----|---------|---------|--------------|
| `flate2` | 1.0 | zlib decompression (mzML, FASTQ .gz) | `rust_backend` — pure Rust, no C |

### Build/Optional Dependencies

| Dep | Feature Gate | Purpose |
|-----|-------------|---------|
| `barracuda` | `gpu` | ToadStool GPU compute primitives |
| `wgpu` | `gpu` | WebGPU compute (Vulkan/Metal/DX12) |
| `tokio` | `gpu` | Async runtime for GPU device creation |
| `serde_json` | `json` | JSON parsing for 2 validation binaries |
| `bytemuck` | always | Zero-copy GPU buffer casting |

### Subprocess Dependencies (not Rust crates)

| Tool | Module | Purpose | Evolution Path |
|------|--------|---------|---------------|
| `curl` | `ncbi.rs` | HTTPS without TLS crate deps | metalForge HTTP substrate (when available) |
| `nvidia-smi` | `bench/hardware.rs`, `bench/power.rs` | GPU discovery + power | Standard; no Rust equivalent without NVML bindings |

All subprocess dependencies have graceful fallback to cached/synthetic data.

---

## Part 6: Recommendations for ToadStool Evolution

### 1. Cholesky Solver Primitive

wetSpring implemented a local Cholesky decomposition for ESN ridge regression.
This should be absorbed into BarraCUDA as `linalg::cholesky_solve(a, b, n)` —
reusable for any SPD system solve (kriging, RBF interpolation, GP regression).

### 2. ODE Generic Absorption (reiterated from v15)

The 5 local WGSL ODE shaders remain the primary absorption target:
`BatchedOdeRK4Generic<N_VARS, N_PARAMS>`. No change from v15 — still the
highest-priority pending item.

### 3. Streaming I/O Patterns

ToadStool's bio parsers should follow the streaming-first pattern:
- `Iterator<Item = Result<Record>>` for per-record processing
- `stats_from_file()` for aggregate statistics (zero-copy where possible)
- Deprecated: `parse_*()` functions that buffer entire files

### 4. Edition 2024 + deny(unsafe_code) Pattern

wetSpring proved that `#![deny(unsafe_code)]` is viable for a 24K-line
scientific computing crate. The only `#[allow(unsafe_code)]` is for
`std::env::set_var` in test-only `EnvGuard` (edition 2024 made this unsafe).
ToadStool should adopt the same pattern.

### 5. Tolerance Architecture

wetSpring's `tolerances.rs` (53 named constants) is a proven pattern for
managing numerical precision across CPU/GPU/NPU. Each constant documents
its scientific justification. ToadStool should consider a similar centralized
tolerance registry.

---

## Part 7: Files Changed in This Audit

| File | Change |
|------|--------|
| `barracuda/src/bio/esn.rs` | Cholesky solver + flat buffers + 21 tests |
| `barracuda/src/bio/ncbi_data.rs` | 17 tests |
| `barracuda/src/ncbi.rs` | 10 tests + evolution path docs |
| `barracuda/src/bin/validate_fastq.rs` | Streaming migration (bulk loop) |
| `barracuda/src/bin/validate_mzml.rs` | Streaming migration (stats_from_file) |
| `barracuda/src/bin/validate_pfas.rs` | Streaming migration (Ms2Iter) |
| `barracuda/src/bin/validate_reconciliation.rs` | Migrated to Validator struct |
| `barracuda/src/bin/validate_mapping_sensitivity.rs` | `partial_cmp().unwrap()` → `total_cmp()` |
| `barracuda/src/io/fastq/mod.rs` | `parse_fastq` deprecated |
| `barracuda/src/io/mzml/mod.rs` | `parse_mzml` deprecated |
| `barracuda/src/io/ms2.rs` | `parse_ms2` deprecated |
| `barracuda/src/bio/merge_pairs.rs` | Clone eliminated (move semantics) |
| `barracuda/src/bio/derep.rs` | Clone eliminated (Entry API) |
| `barracuda/fuzz/Cargo.toml` | Added missing license field |

---

## Verification

```
cargo fmt --check          # Clean
cargo clippy -D warnings   # Clean
cargo doc --no-deps        # Clean
cargo test                 # 728 pass, 1 ignored (845 total with forge + doc)
cargo llvm-cov --lib       # 95.67% line coverage
```

All 3,028+ validation checks PASS. All 845 tests PASS.
