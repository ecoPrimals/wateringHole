# hotSpring v0.6.32 Deep Debt Evolution Phase 3 Handoff

**Date**: May 9, 2026
**From**: hotSpring v0.6.32
**Context**: Deep debt evolution following Interstadial Eukaryotic Evolution wave
**License**: AGPL-3.0-or-later

---

## Summary

Deep Debt Evolution Phase 3 targeted production code quality: hardcoded paths,
large file refactoring, API ergonomics, dependency freshness, and error handling.
All changes verified with full test suite (1002 pass, 0 fail).

---

## Changes Made

### 1. Hardcoded Paths → Capability-Based Resolution (6 sites)

All hardcoded `/tmp` fallbacks in production code replaced with platform-agnostic
resolution via `niche::socket_dirs()` or `std::env::temp_dir()`:

| File | Before | After |
|------|--------|-------|
| `primal_bridge.rs` | `XDG_RUNTIME_DIR` → `/tmp/biomeos` | `niche::socket_dirs()` multi-path scan |
| `toadstool_report.rs` | `/tmp` string literal | `std::env::temp_dir()` |
| `fleet_client.rs` | `PathBuf::from("/tmp")` | `std::env::temp_dir()` |
| `brain_persistence.rs` | `HOME` → `/tmp` fallback | `std::env::temp_dir()` |
| `validate_cross_vendor_dispatch.rs` | `/tmp` string literal | `std::env::temp_dir()` |
| `precision_brain.rs` | `/usr/local/share:/usr/share` | Already XDG spec-compliant (no change) |

### 2. Smart Refactoring: rhmc/mod.rs (802L → 363L)

Extracted cohesive subsystems without losing domain semantics:

| New Module | Lines | Content |
|------------|-------|---------|
| `rhmc/rational.rs` | 215 | `RationalApproximation` + Remez-optimized partial-fraction generation + golden-section pole search |
| `rhmc/multishift_cg.rs` | 210 | Multi-shift CG solver with extracted update helpers |
| `rhmc/mod.rs` | 363 | Config structs (deduplicated via `from_spectral()`), RHMC physics functions, tests |

Config builder boilerplate reduced: 5 NfX constructors now use shared
`RhmcFermionConfig::from_spectral()` and `RhmcConfig::single_sector()` helpers
with named constants (`DEFAULT_DT`, `DEFAULT_CG_TOL`, etc.).

### 3. API Signature Evolution

| Function | Before | After |
|----------|--------|-------|
| `niche::set_family_id` | `fn(String)` | `fn(impl Into<String>)` |
| `TelemetryWriter::with_substrate` | `fn(String)` | `fn(impl Into<String>)` |

### 4. Dependency Updates

| Dependency | Before | After |
|------------|--------|-------|
| `cudarc` | 0.19.3 | 0.19.4 |
| `tokio` | 1.50.0 | 1.52.3 |
| `mio` | 1.1.1 | 1.2.0 |
| `tokio-macros` | 2.6.1 | 2.7.0 |

**Upstream gap**: `pollster` 0.3 + 0.4 duplicate caused by barraCuda primal
depending on pollster 0.3 while hotSpring uses 0.4. Requires upstream bump.

### 5. Production Error Handling

- `production_dynamical.rs`: tokio runtime init and JSON output use proper
  error paths with exit codes instead of `unwrap()`
- `validate_fpeos.rs`: All 6 `unwrap()` calls replaced with `if let Some`
  patterns reporting through `ValidationHarness`
- `gpu_physics_proxy.rs`: NaN-safe sort via `unwrap_or(Ordering::Equal)`

### 6. Validation Matrix Correction

`cells.rs` runtime-printed table updated to reflect implemented features:
- ILDG/Lime config I/O: ✗ todo → ✓ done (lattice::ildg + lime modules)
- Autocorrelation analysis: ✗ todo → ✓ done (stats::autocorrelation)
- HISQ/Continuum extrapolation: relabeled as "gap" (accurate status)

### 7. Documentation Updates

- CHANGELOG: new Phase 3 entry
- whitePaper/README.md: test count 993→1002, binary count 166→148
- whitePaper/baseCamp/README.md: eukaryotic UniBin references
- docs/PRIMAL_GAPS.md: fixed duplicate GAP-HS-030/031 IDs (→ GAP-HS-048/049)
- experiments/README.md: eukaryotic evolution section
- Local `wateringHole/handoffs/` duplicate removed (canonical is infra/)

---

## Build Verification

```
cargo fmt --check    → zero drift
cargo clippy --lib   → zero warnings
cargo test --lib     → 1002 passed, 0 failed, 6 ignored
```

---

## Remaining Upstream Gaps (for primal teams)

| Gap | Owner | Action |
|-----|-------|--------|
| pollster 0.3→0.4 | barraCuda | Bump pollster dep to 0.4 |
| nestgate IPC validation | hotSpring + nestGate | Add IPC probes for `storage.*` methods |
| UniBin `serve` subcommand | hotSpring | CLI `about` mentions IPC server but no serve command |
| barracuda optional dep | hotSpring | `optional = true` + `#[cfg]` gating for Tier 3 |
| 13 methods not in primalSpring registry | primalSpring | GAP-HS-044 |
| projectNUCLEUS workload TOML | projectNUCLEUS | GAP-HS-047 binary name mismatch |
