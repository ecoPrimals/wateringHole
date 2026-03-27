# AIRSPRING V0.10.0 → barraCuda / toadStool Deep Evolution & Absorption Handoff

**Date:** March 23, 2026  
**Supersedes:** `AIRSPRING_V010_BARRACUDA_TOADSTOOL_EVOLUTION_HANDOFF_MAR22_2026.md`  
**License:** AGPL-3.0-or-later

---

## What Changed (airSpring v0.10.0 deep evolution pass)

### Completed Absorptions from Ecosystem

1. **Per-site safe casts** (wetSpring V132): Removed 3 blanket cast allows from Cargo.toml. 54 binaries now use file-level `#[expect(clippy::cast_*)]` with reason strings. Pattern: validation harness casts are bounded by fixture size.

2. **Typed PipelineError** (neuralSpring V121): Added `PipelineError` enum to `seasonal_pipeline` with `DeviceInit`, `ShaderDispatch`, `InvalidConfig`, `Unexpected` variants via `thiserror`. Integrated into `AirSpringError::Pipeline(#[from])`. Added `try_gpu()`/`try_streaming()` methods returning `Result<Self, PipelineError>`.

3. **ValidationSink trait** (wetSpring V132): New `validation::sink` module with `ValidationSink` trait and `JsonSink` implementation. Emits CI-parsable JSON from `ValidationHarness` checks. Stable JSON schema for CI parsers.

4. **default-features = false** (ludoSpring V29): barraCuda dependency now explicitly enables only `gpu` + `domain-pde`. Eliminates compilation of unused domain modules (ESN, genomics, NN, SNN, timeseries, vision).

5. **content_sha256 provenance** (ludoSpring V29): New `control/provenance.py` with `content_sha256()` + `attach_provenance()`. 16 Python benchmark generators now embed SHA-256 hash, python_version, generation_date in `_provenance` sections.

6. **normalize_method()** (barraCuda 0.3.7 semantic naming): Strips legacy `airspring.` prefix from JSON-RPC method names. Integrated into primal dispatch path.

7. **Named numerical guard constants**: New `tolerances::numerics` module centralizes IEEE-754-justified guards (`POSITIVE_DATA_GUARD`, `DIVISION_GUARD`, `LOG_UNIFORM_FLOOR`, `LINEAR_SYSTEM_EPSILON`). Magic numbers removed from 10+ production modules.

8. **TCP transport for IPC**: `ipc::compute_dispatch` now supports TCP alongside Unix sockets via `rpc::resolve_transport` with `TOADSTOOL_ADDRESS` env var.

9. **Release-mode validation CI**: New `validate-release` job catches FMA/LTO numerical divergence.

### Quality Metrics

- 947 lib unit tests + 306 integration/doc tests = 1,253 barracuda total
- 62 forge tests (metalForge)
- 1,314 total tests, 0 failures
- 91 binaries (84 validation, 4 bench, 3 operational)
- 87 experiments, 58 named tolerances, 41 capabilities
- 0 clippy warnings (pedantic + nursery, -D warnings)
- 0 unsafe, 0 C deps, all files < 1000 LOC (max 829)
- cargo fmt clean, cargo clippy clean

---

## Absorption Candidates for barraCuda

These patterns emerged from airSpring's evolution pass and are candidates for upstream absorption:

### 1. `ValidationSink` trait

airSpring's `JsonSink` emits CI-parsable JSON from `ValidationHarness`. If multiple springs want pluggable output, the trait could live in `barracuda::validation`. The JSON schema is: `{ suite, passed, total, all_passed, checks: [{ label, passed, observed, expected, tolerance, mode, rel_tolerance? }] }`.

### 2. `OrExit` trait for validation binaries

Converts `Result<T,E>` / `Option<T>` to `T` with structured tracing::error + process::exit(1). Prevents panic backtraces in CI. Multiple springs have implemented this independently — canonical version in barraCuda would reduce duplication.

### 3. Named numerical guard constants pattern

airSpring's `tolerances::numerics` module centralizes scattered magic numbers (`1e-10`, `1e-15`, `1e-300`, `1e-30`) with IEEE-754 justifications. If barraCuda offered `barracuda::numerics::{POSITIVE_DATA_GUARD, DIVISION_GUARD, ...}`, springs could share the vocabulary.

### 4. `content_sha256` baseline provenance

The pattern of hashing benchmark JSON content (excluding metadata) for drift detection is useful for any spring. A `barracuda::provenance::content_sha256()` Rust helper could complement the Python-side generation.

### 5. TCP transport in IPC

airSpring added TCP fallback alongside Unix sockets. If toadStool standardizes `Transport { Unix(path), Tcp(addr) }` with env-var-based discovery (`*_SOCKET` for Unix, `*_ADDRESS` for TCP), all springs benefit.

### 6. Per-domain feature gating pattern

`default-features = false, features = ["gpu", "domain-pde"]` lets consumers avoid compiling unused domains. If barraCuda adds CI that tests each domain feature independently, it catches breakage earlier.

---

## ToadStool-Specific Notes

- airSpring's `try_gpu_dispatch()` wraps `std::panic::catch_unwind()` to convert shader panics to graceful SKIP. toadStool could offer this as `barracuda::dispatch::try_dispatch()` or in a test utility module.
- The `device_or_skip!` macro pattern is replicated across multiple springs. A canonical version in `barracuda::device::test_pool` would reduce duplication.
- `#[expect]` vs `#[allow]` in shared test modules: when helpers are compiled into multiple test binaries, `#[allow(dead_code)]` with a reason string is more correct than `#[expect]` (which is unfulfilled in binaries that do use the helper).

---

## Deferred Items (not blocking, future work)

- Per-site safe casts in library code (currently handled by cast module, but some validation binaries still use file-level expects)
- `GpuContext` wrapper for lifecycle management (awaiting toadStool standardization)
- `TensorSession` for fused multi-op GPU pipelines (awaiting barraCuda 0.4.x)
- Property-based testing expansion (currently 7 proptest invariants, target: per-module)

---

## Reproduction

```bash
cd airSpring/barracuda
cargo fmt --check                        # clean
cargo clippy --all-targets -- -D warnings # 0 warnings
cargo test                               # 1,253 pass, 0 fail
cd ../metalForge/forge
cargo test                               # 62 pass, 0 fail
```

---

## License

AGPL-3.0-or-later
