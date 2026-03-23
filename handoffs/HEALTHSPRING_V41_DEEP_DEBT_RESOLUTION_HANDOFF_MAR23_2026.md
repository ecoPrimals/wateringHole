<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V41 — Deep Debt Resolution Sprint

**Date**: March 23, 2026
**Supersedes**: `HEALTHSPRING_V40_CROSS_ECOSYSTEM_ABSORPTION_SPRINT_HANDOFF_MAR22_2026.md`
**Session**: Deep debt resolution + modern idiomatic Rust evolution

---

## Executive Summary

V41 consolidates lint governance to workspace level, evolves library `println!`
to structured `tracing`, replaces hardcoded primal names with env-driven
capability-based discovery, wires ODE codegen to GPU dispatch, extends proptest
coverage to numerical properties, syncs the tolerance registry, and evolves CI
to validate all experiment binaries in multi-binary crates. 855 tests (up from
848), zero clippy warnings, zero unsafe, zero `#[allow]`.

---

## What Changed

### Workspace Lint Consolidation (31 files changed)
- Added `[workspace.lints.rust]` and `[workspace.lints.clippy]` to root `Cargo.toml`
- `forbid(unsafe_code)`, `deny(clippy::{all,pedantic,nursery,unwrap_used,expect_used})`, `warn(missing_docs)`
- All 3 lib crates inherit via `[lints] workspace = true`
- Removed duplicate crate-level lint attributes from `lib.rs` files
- Experiment `Cargo.toml` files: `edition = "2024"` → `edition.workspace = true`
- Test modules use `#[expect(clippy::unwrap_used, reason = "...")]`

### Library println! → tracing
- `provenance/mod.rs`: `println!`/`print!` → `tracing::info!` with structured fields
- `validation.rs`: `eprintln!` → `tracing::error!`, `println!` → `tracing::info!`
- Auto-init: `ValidationHarness::new()` calls `init_validation_tracing()` via `Once`
- Zero changes required in 83 experiment binaries

### Hardcoded Primal Names → Env-Driven Discovery
- `ipc/tower_atomic.rs`: `BIOMEOS_CRYPTO_PREFIX` / `BIOMEOS_DISCOVERY_PREFIX`
- `visualization/ipc_push/client.rs`: `BIOMEOS_VIZ_PREFIX`
- All fall back to sensible defaults (`"beardog"`, `"songbird"`, `"petaltongue"`)

### ODE Codegen Wired to GPU Dispatch
- `gpu/mod.rs`: `codegen_shader_for_op(GpuOp::MichaelisMentenBatch)` → WGSL via `BatchedOdeRK4`
- 2 new tests: shader validity, None for non-ODE ops
- 3 `OdeSystem` impls exist: MM, OralOneCompartment, TwoCompartment

### Proptest Numerical Properties
- `pkpd/dose_response.rs`: 5 new proptests (boundedness, IC50 identity, monotonicity, EC ordering, zero-at-zero)

### Tolerance Registry Sync
- `TOLERANCE_REGISTRY.md`: 5 toxicology constants updated to match code values

### CI Evolution
- `.github/workflows/ci.yml`: multi-binary experiment crates now validate all binaries (was `head -1`)

### Rustdoc Coverage
- 104 `///` doc comments added to `metalForge/forge/` and `toadstool/` public APIs
- `missing_docs = "warn"` surfaced 548 items for future documentation passes

---

## Quality Metrics

| Metric | V40 | V41 | Delta |
|--------|-----|-----|-------|
| Tests | 848 | 855 | +7 |
| Clippy warnings (non-doc) | 0 | 0 | — |
| `missing_docs` warnings | — | 548 | (new lint) |
| `#[allow()]` in library | 0 | 0 | — |
| Unsafe code | 0 | 0 | — |
| Lint governance | per-crate | workspace | consolidated |
| Library println | ~4 | 0 | -4 |
| Hardcoded primal names | 3 | 0 | -3 |
| ODE codegen ops | 0 | 1 | +1 |

---

## Open Items for Next Session

### P0 — Coverage Push
- Target: 79% → 90% line coverage
- Low-coverage: `toadstool` GPU paths, `visualization/stream.rs`, `wfdb/annotations.rs`

### P0 — Missing Docs
- 548 `missing_docs` warnings — prioritize public API items in `ecoPrimal/src/`
- metalForge/toadstool done; ecoPrimal remains

### P1 — GPU Promotion
- Wire `OralOneCompartmentOde` and `TwoCompartmentOde` to `codegen_shader_for_op`
- `KimuraGpu` integration for mithridatism
- `JackknifeGpu` for NLME diagnostics

### P1 — Ecosystem Absorption (from V40 backlog)
- `DefaultRng` from groundSpring V118
- Validator-fails-on-zero-checks from wetSpring V131
- `OnceLock` GPU device probe cache from neuralSpring V120
- Sleep-free IPC test patterns from biomeOS V254-260

### P2 — Zero-Copy Hot Paths
- `Arc<str>` keys, `Bytes` from `serde_json::to_vec`
- toadStool S163 pattern

---

*Part of [ecoPrimals](https://github.com/syntheticChemistry) — sovereign computing for science.*
