# airSpring V0.7.6 — Deep Debt Resolution Handoff to barraCuda / toadStool

SPDX-License-Identifier: AGPL-3.0-or-later
**Date**: March 14, 2026
**From**: airSpring v0.7.6 (87 experiments, 833 lib + 186 forge tests)
**To**: barraCuda (v0.3.5) + toadStool (S147+)
**barraCuda Pin**: v0.3.5 (wgpu 28)
**bingocube-nautilus Pin**: v0.1.0

---

## Executive Summary

airSpring completed a deep debt resolution session that synced to barraCuda
0.3.5 and bingocube-nautilus 0.1.0. This handoff documents API migration
patterns, a new data provider abstraction, and evolution learnings relevant
to the barraCuda/toadStool teams.

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

## §4 Current airSpring Status

| Metric | Value |
|--------|-------|
| Version | 0.7.6 |
| Experiments | 87 |
| Python checks | 1,284/1,284 |
| Lib tests | 833 (1 pre-existing GPU driver issue) |
| Forge tests | 186 |
| Validation | 381/381 |
| Cross-spring evolution | 146/146 |
| CPU speedup | 14.5× geometric mean (21/21 parity) |
| barraCuda | v0.3.5 |
| Clippy | 0 warnings (pedantic+nursery) |
| Unsafe | 0 |
| Max file size | 815 lines |

---

## §5 Open Items from V075 (Still Valid)

These items from the V075 handoff remain relevant:

1. **9 upstream absorption candidates** — Available in barraCuda HEAD, not yet wired
   in airSpring (see V075 §5).
2. **14 JSON-RPC science methods** — Ready for toadStool compute.offload (see V075 §2).
3. **FAO-56 GPU input schema** — `actual_vapour_pressure` gap causes ~2mm/day CPU↔GPU divergence.
4. **Hamon daylight formula** — Standardize on Brock (1981) for cross-spring consistency.
5. **`BatchedOdeRK45F64`** — Highest-value absorption target for Richards PDE.
