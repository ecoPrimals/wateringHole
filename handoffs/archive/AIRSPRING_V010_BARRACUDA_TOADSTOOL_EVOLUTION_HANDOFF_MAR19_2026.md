# airSpring V0.10.0 — barraCuda / toadStool Evolution Handoff

**Date:** 2026-03-19
**From:** airSpring V0.10.0
**To:** barraCuda + toadStool teams
**License:** AGPL-3.0-or-later
**Covers:** Deep debt resolution, absorption candidates, ecosystem learnings, Transport pattern
**Supersedes:** AIRSPRING_V010_DEEP_AUDIT_EXECUTION_HANDOFF_MAR18_2026.md

---

## Executive Summary

airSpring v0.10.0 completes a comprehensive deep debt pass. This handoff documents:
- 3 absorption candidates for barraCuda upstream
- 1 pattern for ecosystem-wide adoption (Transport enum)
- Learnings from 1222 tests, 97 validation binaries, 63 provenance baselines
- No new math to absorb — barraCuda integration is healthy (zero duplication)

---

## Part 1: barraCuda Dependency Health

### Current Consumption (25+ GPU ops, 15+ CPU primitives)

| Category | Primitives Consumed |
|----------|-------------------|
| **Stats** | `pearson_correlation`, `spearman_correlation`, `rmse`, `mbe`, `mean`, `percentile`, `bootstrap_ci`, `std_dev`, `norm_ppf`, `diversity::*`, `hydrology::*` |
| **Linalg** | `tridiagonal_solve`, `ridge_regression` |
| **GPU Ops** | `BatchedElementwiseF64` (20 ops), `FusedMapReduceF64`, `KrigingF64`, `MovingWindowStats`, `CorrelationF64`, `VarianceF64`, `AutocorrelationF64`, `DiversityFusionGpu` |
| **PDE** | `pde::richards`, `RichardsGpu` |
| **Optimize** | `brent`, `brent_gpu`, `nelder_mead` |
| **Special** | `regularized_gamma_p` |
| **Validation** | `ValidationHarness`, `tolerances::Tolerance`, `tolerances::check` |
| **Device** | `WgpuDevice`, `PrecisionRoutingAdvice` |

### Duplication: None

Two intentional local implementations:
1. `testutil::stats::nash_sutcliffe` — different convention (1.0 for constant-obs)
2. `testutil::stats::index_of_agreement` — same convention difference

All other math delegates to barraCuda. Zero local WGSL shaders (all retired v0.7.2).

---

## Part 2: Absorption Candidates

### 2a. Transport Enum (IPC)

**What:** Platform-agnostic IPC transport abstraction.
**Where:** `barracuda/src/rpc.rs` → `Transport::Unix(PathBuf)` | `Transport::Tcp(SocketAddr)`
**Why:** ecoBin requires cross-platform IPC. Currently every spring implements Unix-only `send()`.
**Candidate for:** `barracuda::ipc::transport` or shared ecoPrimals IPC crate.

```rust
pub enum Transport {
    #[cfg(unix)]
    Unix(PathBuf),
    Tcp(SocketAddr),
}

pub fn resolve_transport(primal: &str) -> Result<Transport, IpcError>
pub fn send_to(transport: &Transport, method: &str, params: &Value) -> Result<Value, IpcError>
```

**toadStool action:** Consider absorbing `Transport` + `resolve_transport()` into barraCuda IPC module. All springs would lean on it instead of reimplementing.

### 2b. PythonBaseline Provenance Registry

**What:** `PythonBaseline` struct with `binary`, `script`, `commit`, `date`, `category`.
**Where:** `barracuda/src/provenance.rs` (63 entries).
**Why:** wetSpring uses identical struct. Upstream absorption enables cross-spring provenance queries.
**Candidate for:** `barracuda::validation::provenance`.

**toadStool action:** Low priority. Both springs work fine with local registries. Absorb when a third spring needs it.

### 2c. OrExit Trait

**What:** `trait OrExit<T>` — zero-panic `Result`/`Option` unwrap for validation binaries.
**Where:** `barracuda/src/validation/mod.rs` (also in groundSpring V112, wetSpring V125).
**Why:** Already used across 91+ binaries in airSpring, similar in siblings. Reduces boilerplate.
**Candidate for:** `barracuda::validation::OrExit` (already partially there via ValidationHarness).

**toadStool action:** `OrExit` is simple enough that local copies are fine. Absorb if a fourth spring adopts it.

---

## Part 3: Ecosystem Learnings

### 3a. `#[expect]` vs `#[allow]` for Defensive Code

`#[expect(dead_code)]` on defensively-retained GPU wrappers causes unfulfilled lint warnings when the code isn't actually dead in some build configs. Use `#[allow(dead_code)]` instead for code retained for future use.

**Rule:** `#[expect]` for lints you know will fire. `#[allow]` for blanket suppressions on defensive/retained code.

### 3b. Cast Lint Crate-Level Allows

airSpring uses crate-level `cast_precision_loss = "allow"` in `Cargo.toml` to cover 91 validation binaries. Library code denies at module level. The progressive evolution path:
1. Add `use cast::*` when touching a binary
2. Replace raw `as` casts with `cast::usize_f64()` etc.
3. Add per-binary `#[expect]` for remaining casts
4. Eventually remove crate-level allows

**Ecosystem guidance:** This is acceptable during rapid development. Tighten progressively, not in a big-bang refactor.

### 3c. MCP Tool Dispatch Pattern

All springs should wire `tools/list` and `tools/call` into their primal JSON-RPC dispatch:

```rust
"tools/list" => DispatchOutcome::Ok(mcp::list_tools()),
"tools/call" => dispatch_mcp_tool(params),
```

Where `dispatch_mcp_tool` extracts `name` + `arguments`, maps to JSON-RPC method, dispatches, and returns MCP-compliant `content` response.

### 3d. Tolerance Centralization Policy

"Tolerances are never hardcoded inline" is aspirational. Reality: validation binaries accumulate inline values during rapid development. Schedule periodic sweeps (like this one) to centralize. The `tolerances/` module pattern (4 domain submodules, each constant has `name`, `abs_tol`, `rel_tol`, `justification`) works well.

---

## Part 4: GPU Evolution Status

| Tier | Count | Status |
|------|-------|--------|
| **A** (GPU-integrated) | 24 | Validated, GPU-first |
| **B** (Orchestrator) | 2 | `seasonal_pipeline`, `atlas_stream` — need fused dispatch |
| **C** (CPU-only) | 2 | `anderson` (new WGSL needed), `et0_ensemble` (serial orchestration) |

**No new WGSL needed from barraCuda** — all current GPU work uses existing ops (BatchedElementwiseF64, FusedMapReduceF64, KrigingF64, etc.).

**Future:** Anderson θ→S_e→d_eff→QS iterative fixed-point shader would promote the last physics module to Tier A. Not blocking.

---

## Part 5: Quality Snapshot

| Metric | Value |
|--------|-------|
| Library tests | 911 |
| Integration tests | 311 |
| Forge tests | 61 |
| Property tests | 22 |
| Validation binaries | 97 (91 barracuda + 6 forge) |
| Python baselines | 63 (all with provenance) |
| Named tolerances | 58 (4 domain submodules) |
| Clippy warnings | 0 (pedantic + nursery, all targets) |
| Unsafe code | 0 (`#![forbid(unsafe_code)]`) |
| C dependencies | 0 (14 crates banned in `deny.toml`) |
| TODO/FIXME/HACK | 0 |
| Files > 1000 LOC | 0 (largest: 820) |
| Cross-compile | aarch64 checked in CI |

---

## License

AGPL-3.0-or-later
