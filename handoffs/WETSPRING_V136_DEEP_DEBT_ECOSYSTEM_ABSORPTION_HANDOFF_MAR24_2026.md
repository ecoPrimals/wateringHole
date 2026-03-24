<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# wetSpring V136 — Deep Debt Resolution + Ecosystem Absorption Handoff

| Field | Value |
|-------|--------|
| **Date** | 2026-03-24 |
| **From** | wetSpring **V136** |
| **To** | All springs, barraCuda, toadStool, ecosystem |
| **License** | AGPL-3.0-or-later |
| **Supersedes** | `WETSPRING_V135_BARRACUDA_TOADSTOOL_ABSORPTION_HANDOFF_MAR24_2026.md` (archived) |

---

## Executive Summary

V136 is a deep debt resolution and cross-spring absorption cycle. Patterns
absorbed from groundSpring V122, neuralSpring S174, airSpring v0.10.0,
healthSpring V42, and ludoSpring V30. Error types evolved to modern idiomatic
Rust. Bare `as` casts replaced with named helpers. Hardcoded primal strings
eliminated. Stochastic determinism tests added. CI pin assertion for upstream
barraCuda. Community docs (CONTRIBUTING.md + SECURITY.md) added.

V135 (preceding) was documentation reconciliation + ecosystem sync — no code
changes. V134 was deep audit + debt resolution: NMF delegation, clippy fixes,
validation harness submodules, primal discovery, SPDX headers, CI feature matrix.

---

## Canonical V136 Metrics

| Metric | Value |
|--------|-------|
| Tests | **1,891** (unit + integration + property + doc, 0 failed) |
| Lib tests (default) | **1,205** |
| Lib tests (ipc+vault+json) | **1,569** |
| Binaries | **355** (333 barracuda + 22 forge) |
| Experiments | 379 indexed (376 completed + 3 PROPOSED) |
| Validation checks | 5,700+ |
| GPU modules | 44 (all Lean) |
| CPU bio modules | 49 |
| Named tolerances | 234 (zero inline literals) |
| Coverage | 91.20% line / 90.30% function (gated at 90%) |
| barraCuda | v0.3.7 standalone (784+ WGSL shaders) |
| Primitives consumed | 150+ |
| Local WGSL | 0 |
| Duplicate math | 0 |
| `#[allow()]` | 0 (all `#[expect(reason)]`) |
| Unsafe | 0 (`forbid(unsafe_code)` workspace-wide) |
| Mocks in production | 0 (all `#[cfg(test)]`) |
| Hardcoded primal strings | 0 (all `primal_names::*` constants) |

---

## What V136 Did

### 1. thiserror migration (ludoSpring V30 / ecosystem standard)
All 6 error types evolved from manual `impl Display` + `impl Error` to
`thiserror::Error` derives: `IpcError`, `Error`, `DispatchError`, `PushError`,
`VaultError`, `RpcError`. ~120 lines of boilerplate removed. `#[from]` for
automatic `From` impls. `#[source]` for error chaining.

### 2. Named cast helpers (groundSpring V122 pattern)
6 new helpers added to `cast.rs`: `f64_f32`, `usize_i32`, `u64_u32_truncate`,
`f64_i64`, `i32_usize`, `i64_usize`. Module now has 20 total named casts with
documented precision semantics and `debug_assert!` guards. ~60 bare `as` casts
replaced across 15 library files: bio/taxonomy, bio/pangenome, bio/chimera,
bio/gillespie, bio/streaming_gpu, bio/rarefaction_gpu, bio/random_forest_gpu,
io/fastq, io/nanopore, ipc/resilience, ipc/handlers, ipc/timeseries.

### 3. Upstream contract pinning (neuralSpring S174 pattern)
New `upstream_contract` module pins barraCuda v0.3.7 with semver comparison
utility and CI-ready version drift detection. Documents the validation baseline.

### 4. CI version pin (healthSpring V42 pattern)
`scripts/check_barracuda_pin.sh` verifies upstream barraCuda version matches
the wetSpring pin. `barracuda-pin` job added to `.github/workflows/ci.yml`.

### 5. Bitwise determinism tests (healthSpring V42 pattern)
3 new tests: `gillespie::bitwise_deterministic_with_seed`,
`bootstrap::bitwise_deterministic_with_seed`,
`rarefaction_gpu::bitwise_deterministic_with_seed`. Seeded algorithms verified
bit-identical across runs using `f64::to_bits()` comparison.

### 6. Provenance headers (airSpring v0.10.0 pattern)
`//! Provenance:` headers added to 5 core validators: `validate_fastq`,
`validate_diversity`, `validate_mzml`, `validate_gillespie`, `validate_hmm`.
Documents algorithm provenance chain: paper → Python baseline → Rust sovereign.

### 7. Hardcoding audit — zero hardcoded primal strings
New `primal_names` constants: `LEGACY_SELF_METHOD_PREFIX`, `VAULT_KEY_CONTEXT`,
`DEPLOY_GRAPH_REL_PATH`. `ipc/protocol.rs`, `ipc/provenance.rs`, `niche.rs`,
`lib.rs` updated to use constants instead of string literals.

### 8. ipc/server.rs refactored
Extracted `dispatch_request` + `dispatch_notification` helpers, eliminating
code duplication between `process_single` and `process_batch`.

### 9. Community docs (neuralSpring S174 pattern)
CONTRIBUTING.md + SECURITY.md added at repo root with ecosystem conventions.

### 10. Mock audit — confirmed clean
Zero mocks/stubs/fakes in production code. All mock patterns isolated to
`#[cfg(test)]` modules.

---

## What Springs / Primals Can Absorb from V136

| Pattern | Source | Recommendation |
|---------|--------|----------------|
| **thiserror derives** | ludoSpring V30 | Any spring with manual Display/Error impls should evolve |
| **Named cast module** | groundSpring V122 | 20 helpers with debug_assert guards — ready to copy/adapt |
| **Upstream contract pinning** | neuralSpring S174 | Pin your barraCuda version in a contract module |
| **Bitwise determinism tests** | healthSpring V42 | Any spring with seeded stochastic algorithms should add |
| **Provenance headers** | airSpring v0.10.0 | Add `//! Provenance:` to your validator binaries |
| **CI version pin script** | healthSpring V42 | Adapt `check_barracuda_pin.sh` for your spring |
| **primal_names constants** | wetSpring V136 | Eliminate hardcoded primal strings; single source of truth |
| **CONTRIBUTING + SECURITY** | neuralSpring S174 | Every spring should have community/security docs |

---

## What wetSpring Needs from Ecosystem

- **barraCuda `VERSION` constant**: Currently not exported. wetSpring works
  around this with Cargo.lock pinning + `PINNED_BARRACUDA_VERSION` doc constant.
  A `pub const VERSION: &str = env!("CARGO_PKG_VERSION");` in `barracuda::lib`
  would let all consumers check at runtime.
- **toadStool S162+**: Continued evolution of `akida-driver` for NPU validation.
- **coralReef Iter 63+**: Sovereign shader compiler for future GPU evolution.

---

## What wetSpring Contributes Back

wetSpring remains a net exporter of these patterns:

- `ValidationSink` / `OrExit` — validation harness primitives (absorbed by
  primalSpring, airSpring, others)
- `normalize_method()` derived from `PRIMAL_NAME` — IPC method normalization
- Named cast module — 20 helpers, ecosystem-ready
- Upstream contract pattern — version pinning for path dependencies
- Bitwise determinism test pattern — seeded reproducibility verification
- `primal_names::*` single source of truth pattern

---

## API Stability

No breaking changes in V136. All existing public APIs preserved. `thiserror`
derives produce identical `Display` output and `Error::source()` chains.
See V135 handoff for detailed barraCuda/toadStool API surface.

---

*wetSpring V136 — Deep debt resolution + ecosystem absorption — 2026-03-24*
