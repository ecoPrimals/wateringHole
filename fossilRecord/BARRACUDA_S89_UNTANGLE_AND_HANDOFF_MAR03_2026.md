# SPDX-License-Identifier: AGPL-3.0-only

# barraCuda Primal Handoff — S89 Complete Untangle

**Date:** 2026-03-03
**From:** toadStool team (S89)
**To:** barraCuda team, Springs, ecosystem
**Covers:** Current state, zero-cross-dependency goal, QCD validation target, migration guide
**License:** AGPL-3.0-only

---

## Executive Summary

barraCuda is now a **fully standalone math primal** with zero dependencies on
toadStool or any other primal. The budding that began in S88 is complete through
all phases: extraction, demarcation, first-consumer validation (hotSpring),
deprecation of toadStool's embedded copy, rewire of toadStool's workspace, and
final untangle of all cross-dependencies.

**Success metric**: when hotSpring can run QCD workloads with barraCuda providing
the math and toadStool providing hardware dispatch, the architecture is proven.

---

## Part 1: Current State

### barraCuda (ecoPrimals/barraCuda/)

| Metric | Value |
|--------|-------|
| Version | 0.2.1 (commit `b53c3de`) |
| Source files | 957 .rs |
| WGSL shaders | 767 |
| Tests passing | 2,831 (full suite incl shader compilation) |
| Feature flags | `gpu` (default), `domain-models`, 7 domain-specific, `serde`, `parallel` |
| Tests passing | 2,835 (`--lib`, all features, 0 failures) |
| Cross-deps on toadStool | **ZERO** — fully untangled (verified by rg + cargo check) |
| Cross-deps on sourDough | `sourdough-core` via `barracuda-core` (primal lifecycle traits) |
| CI | `.github/workflows/ci.yml` (fmt, clippy, 3-config check, full test) |
| MSRV | 1.87 |
| License | AGPL-3.0-or-later |

### toadStool (ecoPrimals/phase1/toadStool/)

| Metric | Value |
|--------|-------|
| barracuda dependency | External: `ecoPrimals/barraCuda/crates/barracuda` |
| Embedded crates/barracuda/ | Deprecated (removed from workspace, DEPRECATED.md added) |
| Consuming crates | 3: `core/toadstool`, `cli` (optional), `integration-tests` |
| Cross-deps on barraCuda | 3 path deps (expected — toadStool consumes barraCuda) |
| Full workspace builds | Clean |

### hotSpring (first consumer validated)

| Metric | Value |
|--------|-------|
| Tests against standalone barraCuda | 716/716 pass |
| Code changes required | Zero (single-line Cargo.toml path swap) |
| Bug reports filed | 2 (sin_f64_safe, tokio test flavor — both fixed) |

---

## Part 2: Architecture

```
Springs (hotSpring, wetSpring, neuralSpring, airSpring, groundSpring)
    |
    v
barraCuda ── "WHAT to compute"
    |           Pure math: linalg, special, numerical, spectral, stats, sample
    |           GPU math: ops, tensor, 767 WGSL shaders, FHE, QCD
    |           Compute fabric: device, staging, pipeline, dispatch, multi_gpu
    |
    v
toadStool ── "WHERE and HOW"
    |           Multi-framework: CUDA, OpenCL, Vulkan, ROCm, Metal, WebGPU
    |           Orchestration: substrate selection, load balancing, fallback
    |           Adaptive: GPU fingerprinting, workgroup tuning
    |           Distribution: multi-node via songBird, server/client
    |
    v
Infrastructure: songBird (network), bearDog (crypto), nestGate (storage)
```

Full spec: `barraCuda/specs/ARCHITECTURE_DEMARCATION.md` (identical copy in
`toadStool/specs/ARCHITECTURE_DEMARCATION.md`).

### Dependency Direction (enforced)

```
Springs ──> barraCuda (direct cargo dep)
toadStool ──> barraCuda (direct cargo dep)
barraCuda ──> sourDough (primal traits only)
barraCuda ──> (nothing else)
```

**No reverse dependencies.** barraCuda does not know about toadStool, songBird,
bearDog, nestGate, or any Spring. It is a pure math library.

---

## Part 3: The QCD Validation Target

**Goal**: hotSpring runs lattice QCD with barraCuda providing math and toadStool
providing hardware dispatch.

This proves the architecture works end-to-end:

1. **hotSpring** defines the physics (gauge field, fermion action, HMC trajectory)
2. **barraCuda** executes the math (SU(3) multiply, CG solver, plaquette, FFT)
   on whatever GPU wgpu discovers
3. **toadStool** (optional layer) routes the workload to the best available
   hardware, tunes workgroup sizes, distributes across nodes

When this pipeline produces correct physics results on consumer hardware (RTX
3090, RX 7900 XT, Intel Arc), the sovereign compute vision is validated.

### What exists today

- barraCuda has all QCD shaders: SU(3) gauge, staggered Dirac, CG solver, HMC
  integrator, plaquette measurement
- hotSpring has 664 physics tests including lattice QCD validation
- hotSpring's Rung 0 (Nf=0) and Rung 1 (Nf=4, Nf=8) experiments are running
- toadStool has `runtime/adaptive` for workgroup tuning and `runtime/gpu` for
  multi-framework routing

### What's needed

- toadStool's `runtime/adaptive` needs to be able to tune barraCuda ops without
  importing barraCuda (it already works this way — profiling only, no code dep)
- hotSpring should demonstrate the two-primal flow: `barracuda` for math,
  `toadstool` for hardware intelligence (optional)

---

## Part 4: Feature Flags Reference

### For Springs (typical consumer)

```toml
# Full (default) — all math + all domain models
barracuda = { path = "../../barraCuda/crates/barracuda" }

# Math + GPU only — fastest compile, no domain models
barracuda = { path = "../../barraCuda/crates/barracuda", default-features = false, features = ["gpu"] }

# Specific domain
barracuda = { path = "../../barraCuda/crates/barracuda", default-features = false, features = ["gpu", "domain-pde"] }

# Pure CPU math — no GPU at all (sub-2s compile)
barracuda = { path = "../../barraCuda/crates/barracuda", default-features = false }
```

### Domain model flags

| Flag | Module | Future home |
|------|--------|-------------|
| `domain-nn` | Neural networks | neuralSpring |
| `domain-snn` | Spiking neural networks | neuralSpring |
| `domain-esn` | Echo state networks | neuralSpring |
| `domain-pde` | PDE solvers | hotSpring/groundSpring |
| `domain-genomics` | Bioinformatics | wetSpring |
| `domain-vision` | Computer vision | neuralSpring |
| `domain-timeseries` | Time series (implies domain-esn) | neuralSpring |

These modules will migrate to their natural Spring homes over time. The feature
gates ensure compile times don't bloat for consumers who don't need them.

---

## Part 5: Migration Guide for Springs

### Step 1: Change Cargo.toml (one line)

```toml
# Old (toadStool-embedded, deprecated):
barracuda = { path = "../../phase1/toadStool/crates/barracuda" }

# New (standalone barraCuda primal):
barracuda = { path = "../../barraCuda/crates/barracuda" }
```

### Step 2: Build and test

```bash
cargo check
cargo test
```

### Step 3: That's it

No code changes needed. All `use barracuda::*` imports, trait implementations,
and shader references work identically. hotSpring confirmed this with 716 tests.

---

## Part 6: Developer Onboarding

barraCuda now has full developer documentation:

| Document | Purpose |
|----------|---------|
| `README.md` | Architecture, feature flags, dev setup, test commands |
| `CONTRIBUTING.md` | How to add ops/shaders/modules, PR process, quality gate |
| `CONVENTIONS.md` | Coding standards (inherits sourDough) |
| `CHANGELOG.md` | SemVer history |
| `BREAKING_CHANGES.md` | Migration notes |
| `specs/BARRACUDA_SPECIFICATION.md` | Crate architecture, IPC contract |
| `specs/ARCHITECTURE_DEMARCATION.md` | barraCuda vs toadStool boundaries |
| `crates/barracuda/src/shaders/README.md` | Shader guide (767 shaders) |
| `.github/workflows/ci.yml` | Automated CI (fmt, clippy, 3-config check, tests) |

### Quality gate (run before every PR)

```bash
cargo fmt --check
cargo clippy -p barracuda
cargo check --no-default-features                    # pure math
cargo check --no-default-features --features gpu     # math + GPU
cargo check                                          # everything
RUST_TEST_THREADS=4 cargo test -p barracuda          # full suite
```

---

## Part 7: What Comes Next

| Priority | Task | Owner |
|----------|------|-------|
| P0 | Remaining Springs rewire to standalone barraCuda | Each Spring |
| P0 | hotSpring QCD end-to-end with barraCuda math | hotSpring + barraCuda |
| P1 | toadStool adaptive tuning demo (workgroup opt for barraCuda ops) | toadStool |
| P1 | Domain model migration: `pde` → hotSpring, `genomics` → wetSpring | Springs |
| P2 | bearDog + barraCuda FHE composition (sovereign encrypted compute) | bearDog |
| P2 | barraCuda v1.0.0 (SemVer, published crate) | barraCuda |
| P3 | Remove deprecated embedded `crates/barracuda/` from toadStool | toadStool |

---

## Files Changed (This Session)

### barraCuda (pushed to github.com/ecoPrimals/barraCuda)

- `specs/ARCHITECTURE_DEMARCATION.md` — NEW: 3-layer ownership boundaries
- `CONTRIBUTING.md` — NEW: developer onboarding
- `.github/workflows/ci.yml` — NEW: CI pipeline
- `rustfmt.toml`, `.cargo/config.toml` — NEW: tooling configs
- `README.md` — REWRITTEN: accurate structure, feature flags, dev setup
- `Cargo.toml` — domain-models feature umbrella
- `src/lib.rs` — domain modules individually feature-gated
- `src/shaders/precision/polyfill.rs` — FIX: sin_f64_safe f64 modulo
- `src/device/test_pool.rs` — FIX: tokio multi_thread flavor
- `src/device/toadstool_integration.rs` — DELETED: toadStool coupling eliminated
- `src/device/wgpu_device/creation.rs` — from_selection() removed (was toadstool-gated)
- `src/device/wgpu_device/mod.rs` — 2 toadstool-gated tests removed
- `src/npu/mod.rs` — ml_backend and ops modules removed
- `src/ops/npu_bridge.rs` — akida-driver code removed, is_npu_available() stubbed to false
- `src/ops/matmul.rs` — NPU routing code removed
- `src/ops/softmax.rs` — NPU routing code removed
- `src/lib.rs` — NpuMlBackend re-export removed
- `Cargo.toml` — TPU feature stubs added (no deps, forward-compatible)
- `Cargo.toml` (workspace) — toadStool comment cleaned

### toadStool (pushed to github.com/ecoPrimals/toadStool)

- `Cargo.toml` — crates/barracuda removed from workspace members
- `crates/barracuda/DEPRECATED.md` — NEW: migration guide
- `crates/core/toadstool/Cargo.toml` — rewired to standalone barraCuda
- `crates/cli/Cargo.toml` — rewired to standalone barraCuda
- `crates/integration-tests/Cargo.toml` — rewired to standalone barraCuda
- `specs/ARCHITECTURE_DEMARCATION.md` — NEW: boundaries spec
- `specs/BARRACUDA_PRIMAL_BUDDING.md` — UPDATED: Phase 4 complete
- `CHANGELOG.md` — full S89 history
