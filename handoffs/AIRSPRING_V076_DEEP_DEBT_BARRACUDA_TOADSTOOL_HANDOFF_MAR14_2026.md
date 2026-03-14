# airSpring V0.7.6 — Deep Debt Resolution + Execution Handoff to barraCuda / toadStool

SPDX-License-Identifier: AGPL-3.0-or-later
**Date**: March 14, 2026
**From**: airSpring v0.7.6 (87 experiments, 834 lib + 41 integration + 186 forge tests)
**To**: barraCuda (v0.3.5) + toadStool (S147+)
**barraCuda Pin**: v0.3.5 (wgpu 28)
**bingocube-nautilus Pin**: v0.1.0

---

## Executive Summary

airSpring completed two deep debt sessions. Session 1 synced to barraCuda
0.3.5 / bingocube-nautilus 0.1.0 and introduced the `data` module. Session 2
executed all audit findings: 4 compilation blockers resolved, 4 validation
integrity fixes, provenance documentation complete, code quality polish.
All features now compile (`--all-features` including NPU), all 834 lib +
41 integration + 186 forge tests pass, zero clippy pedantic+nursery warnings.

---

## §1 API Migration Patterns — For Other Springs

### SpringDomain Newtype Migration

barraCuda 0.3.5 changed `SpringDomain` from an enum to a newtype struct:

```rust
// barraCuda 0.3.3 (old)
SpringDomain::AirSpring
SpringDomain::HotSpring
SpringDomain::WetSpring

// barraCuda 0.3.5 (new)
SpringDomain::AIR_SPRING
SpringDomain::HOT_SPRING
SpringDomain::WET_SPRING
```

**Migration**: Find-and-replace `SpringDomain::CamelCase` → `SpringDomain::SCREAMING_SNAKE`.
airSpring had 3 files to update.

### F64BuiltinCapabilities New Fields

Test code that constructs `F64BuiltinCapabilities` needs three new fields:

```rust
F64BuiltinCapabilities {
    // ... existing fields ...
    shared_mem_f64: false,          // NEW
    df64_arith: true,               // NEW
    df64_transcendentals_safe: true, // NEW
}
```

### bingocube-nautilus 0.1.0 Migration

| Old | New | Notes |
|-----|-----|-------|
| `NautilusShell::new(ShellConfig { evolution: EvolutionConfig { .. }, .. })` | `NautilusBrain::new(NautilusBrainConfig { .. })` | Flat config |
| `shell.evolve_generation(&observations)` | `brain.train(&beta_observations)` | Input type changed |
| `shell.predict(&features)` | `brain.predict_dynamical(&features)` | Method renamed |
| `DriftMonitor` (public) | Internalized | Build a local replacement if needed |

airSpring's local `FitnessDriftMonitor` (in `gpu/atlas_stream.rs`) is a
minimal replacement that tracks mean/best fitness and consecutive drops.

---

## §2 Data Provider Pattern — For biomeOS / NestGate

airSpring now has a `data` module with a `Provider` trait:

```rust
pub trait Provider {
    fn fetch_daily_weather(
        &self, latitude: f64, longitude: f64,
        start_date: &str, end_date: &str,
    ) -> Result<WeatherResponse>;
}
```

Two implementations:
- `HttpProvider` (standalone, ureq HTTP, feature-gated `standalone-http`)
- `BiomeosProvider` (NUCLEUS, JSON-RPC capability discovery)

**For NestGate**: The `BiomeosProvider` expects a `nestgate.weather.daily`
capability. This needs to be registered in NestGate's capability set.

**For other springs**: This pattern (standalone HTTP + NUCLEUS discovery)
could be extracted to barraCuda as a shared `data::Provider` trait if
multiple springs need similar data fetching.

---

## §3 Evolution Learnings

### ureq v3 API Change

`ureq` v3 removed the `read_json()` method on `Body`. The correct pattern is:

```rust
let text = resp.into_body().read_to_string()?;
let body: serde_json::Value = serde_json::from_str(&text)?;
```

This avoids needing the `json` feature on ureq and gives explicit error handling.

### Hardcoded Path Pattern

Validation binaries should never hardcode absolute paths. The pattern airSpring
now uses:

```rust
fn find_path() -> PathBuf {
    if let Ok(dir) = std::env::var("AIRSPRING_GRAPHS_DIR") {
        return PathBuf::from(dir);
    }
    let manifest = env!("CARGO_MANIFEST_DIR");
    PathBuf::from(manifest).join("../graphs")
}
```

### RPC Default Constants

Domain-specific defaults should be named constants with documentation:

```rust
const DEFAULT_LATITUDE_DEG: f64 = 42.7;   // East Lansing, Michigan
const DEFAULT_ELEVATION_M: f64 = 250.0;    // Typical mid-Michigan
const DEFAULT_DOY: i32 = 180;              // June 29 (mid-growing season)
```

---

## §4 Deep Debt Execution — Upstream Fixes for barraCuda/toadStool

### GPU Stream Smoother Bug (Critical for all springs using MovingWindowStats)

The upstream WGSL shader `barraCuda/crates/barracuda/src/shaders/stats/
moving_window_f64.wgsl` declared `array<f64>` types for input/output
buffers and `f64` internal variables, but the Rust `MovingWindowStats` code
sends and expects `f32` data. `wgpu`/`naga` does not support `f64` storage
buffers, so the shader was silently producing garbage.

**Fix applied**: All `f64` declarations changed to `f32` in the shader.
The `_f64` filename is retained for historical continuity but documented
as a misnomer.

**Action for barraCuda**: Verify this fix is committed upstream. Other
springs using `MovingWindowStats` (wetSpring S28+) should update their
GPU integration test tolerances from exact `f64` equality to `f32`-appropriate
thresholds (`1e-5` for mean, `1e-4` for variance/min/max).

### akida-driver Facade (For toadStool neuromorphic crate)

The `phase1/toadstool/crates/neuromorphic/akida-driver/src/lib.rs` was a
1-line stub (`// stub for local builds`). airSpring evolved it into a
complete pure Rust facade defining 14 types:

- `AkidaDevice`, `DeviceManager`, `Capabilities`
- `InferenceConfig`, `ModelProgram`, `InferenceResult`
- `InputBuffer`, `OutputBuffer`, `PowerMode`, `PowerStats`
- `NeuronStatistics`, `DeviceState`
- `DriverError`, `Result<T>`

This is a **software abstraction**, not a hardware driver. It provides the
API surface so that `airSpring`'s `npu/mod.rs` compiles with `--features npu`.
The real hardware interaction should evolve from here — the facade returns
reasonable defaults and empty device lists.

**Action for toadStool**: Review and adopt this facade. It follows the
Zero Mocks principle — no mock trait implementations, just a clean API
surface that can be backed by real hardware when available.

---

## §5 Current airSpring Status

| Metric | Value |
|--------|-------|
| Version | 0.7.6 |
| Experiments | 87 |
| Python checks | 1,284/1,284 |
| Lib tests | 834 (0 failures) |
| Integration tests | 41 (21 GPU + 20 stats) |
| Forge tests | 186 |
| Validation | 381/381 |
| Cross-spring evolution | 146/146 |
| CPU speedup | 14.5× geometric mean (21/21 parity) |
| barraCuda | v0.3.5 |
| Clippy | 0 warnings (`--all-features --all-targets -W pedantic -W nursery -D warnings`) |
| Unsafe | 0 |
| Max file size | 815 lines |
| `cargo check --features npu` | PASS |
| `cargo doc --no-deps` | PASS |

---

## §6 Potential Deduplication — Sum-of-Squares via barraCuda

During audit, 3 manual sum-of-squares patterns were found that could use
`barracuda::stats::correlation::variance` instead of hand-rolled
`.iter().map(|&xi| (xi - mean).powi(2)).sum()`:

| File | Pattern | Suggestion |
|------|---------|------------|
| `eco/isotherm.rs` | `qe.iter().map(\|&qi\| (qi - mean_qe).powi(2)).sum()` | `barracuda::stats::correlation::variance` × (n-1) |
| `eco/correction.rs` | `y.iter().map(\|&yi\| (yi - mean_y).powi(2)).sum()` | Same |
| `testutil/stats.rs` | `observed.iter().map(\|o\| (o - mean_obs).powi(2)).sum()` | Same |

These already use `barracuda::stats::mean`. Centralizing variance would
improve numerical stability (Welford's algorithm in barracuda) and reduce
code duplication. Low priority — current implementations are correct.

---

## §7 Open Items from V075 (Still Valid)

These items from the V075 handoff remain relevant:

1. **9 upstream absorption candidates** — Available in barraCuda HEAD, not yet wired
   in airSpring (see V075 §5).
2. **14 JSON-RPC science methods** — Ready for toadStool compute.offload (see V075 §2).
3. **FAO-56 GPU input schema** — `actual_vapour_pressure` gap causes ~2mm/day CPU↔GPU divergence.
4. **Hamon daylight formula** — Standardize on Brock (1981) for cross-spring consistency.
5. **`BatchedOdeRK45F64`** — Highest-value absorption target for Richards PDE.
