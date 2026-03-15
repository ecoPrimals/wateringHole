<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda v0.3.5 — Lint Evolution & Refactoring Handoff

**Date**: March 14, 2026
**Primal**: barraCuda
**Version**: 0.3.5
**Type**: Deep debt evolution sprint 3

---

## Summary

Third deep debt sprint following the comprehensive audit. Focused on doc lint
and cast lint promotion, smart file refactoring, zero-copy improvement, CI
hardening (blocking coverage and chaos gates, cross-compile job), and test-file
mul_add evolution. All quality gates green.

---

## Changes

### Lint Promotions (6 lints, 20 total promoted)

- **`missing_errors_doc`** (warn): Promoted in both crates. Zero violations.
- **`missing_panics_doc`** (warn): Promoted in both crates. Zero violations.
- **`cast_possible_truncation`** (warn): Promoted in `barracuda-core`. Zero violations.
- **`cast_sign_loss`** (warn): Promoted in `barracuda-core`. Zero violations.
- **`cast_precision_loss`** (warn): Promoted in `barracuda-core`. Zero violations.
- **`cast_lossless`** (warn): Promoted in `barracuda-core`. Zero violations.
- **`large_stack_frames`** (allow with rationale): Documented as test framework
  artifact — `[&test::TestDescAndFn; 3359]` allocated on stack by test harness.
- **`suboptimal_flops`** (allow with rationale): All test-file sites evolved to
  `f64::mul_add()`. 424 library sites remain in canonical `a*b + c` form.

### Refactoring

| Before | After | Rationale |
|--------|-------|-----------|
| `ode_bio/params.rs` (774 lines) | `params/` directory: `mod.rs` barrel + 6 domain submodules (~100-130 lines each) | Smart modular decomposition by ODE model domain |
| RBF `solution[..n].to_vec()` + `solution[n..].to_vec()` | `weights.split_off(n)` | Zero-copy: eliminates 2 allocations |

### CI Evolution

- **80% coverage gate**: `continue-on-error` removed — now blocking.
- **Chaos/fault tests**: `continue-on-error` removed — now blocking.
- **Cross-compilation job**: New `cross-compile` CI job checking:
  - `x86_64-unknown-linux-musl`
  - `aarch64-unknown-linux-musl`
  - Banned C dependency verification (`-lc`, `-lgcc`) for ecoBin compliance.

### Cleanup

- Dead `ring` clarification removed from `deny.toml` (crate not in dep tree).
- WGSL comment in `batched_bisection_f64.wgsl` corrected: was "hardcoded to
  BCS", now reflects multi-entry-point design.
- Integration test count aligned to 42 across all docs (was stale at 43).
- Test counts aligned to 3,359 across all docs and scripts.

---

## Quality Gates — All Green

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | Pass (zero warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Pass |
| `cargo deny check` | Pass |

---

## Files Changed

### Cargo.toml lint configuration
- `crates/barracuda/Cargo.toml` — `large_stack_frames` allow, `suboptimal_flops` rationale, doc lints promoted
- `crates/barracuda-core/Cargo.toml` — cast lints + doc lints promoted

### Refactored
- `crates/barracuda/src/numerical/ode_bio/params.rs` → deleted
- `crates/barracuda/src/numerical/ode_bio/params/mod.rs` — barrel module + tests
- `crates/barracuda/src/numerical/ode_bio/params/qs_biofilm.rs`
- `crates/barracuda/src/numerical/ode_bio/params/capacitor.rs`
- `crates/barracuda/src/numerical/ode_bio/params/cooperation.rs`
- `crates/barracuda/src/numerical/ode_bio/params/multi_signal.rs`
- `crates/barracuda/src/numerical/ode_bio/params/bistable.rs`
- `crates/barracuda/src/numerical/ode_bio/params/phage_defense.rs`

### Zero-copy
- `crates/barracuda/src/surrogate/adaptive/mod.rs` — `split_off` evolution

### Test mul_add evolution
- `crates/barracuda/src/sample/sparsity/tests.rs`
- `crates/barracuda/src/shaders/precision/precision_tests_cpu.rs`
- `crates/barracuda/src/spectral/hofstadter.rs`
- `crates/barracuda/src/spectral/tridiag.rs`
- `crates/barracuda/src/surrogate/adaptive/tests.rs`
- `crates/barracuda/src/surrogate/rbf/tests.rs`

### CI
- `.github/workflows/ci.yml` — blocking gates + cross-compile job

### Config
- `deny.toml` — dead `ring` config removed

### Shader
- `crates/barracuda/src/shaders/optimizer/batched_bisection_f64.wgsl` — comment fix

### Docs updated
- `README.md`, `STATUS.md`, `CHANGELOG.md`, `WHATS_NEXT.md`
- `CONVENTIONS.md`, `CONTRIBUTING.md`
- `specs/REMAINING_WORK.md`, `specs/BARRACUDA_SPECIFICATION.md`
- `scripts/test-tiered.sh`

---

## Cross-Primal Impact

None. Sprint 3 is entirely internal to barraCuda. No IPC contract changes,
no API changes, no breaking changes.

---

## Next Steps

See `WHATS_NEXT.md` for prioritized roadmap. Key near-term items:
- P1: DF64 NVK end-to-end verification on hardware
- P1: coralNAK extraction (pending org repo fork)
- P2: Test coverage 80% → 90% (requires real GPU hardware)
- P2: Kokkos parity validation baseline
- P3: Zero-copy remaining (`domain_ops.rs` pre-allocated buffers, LSTM state)
