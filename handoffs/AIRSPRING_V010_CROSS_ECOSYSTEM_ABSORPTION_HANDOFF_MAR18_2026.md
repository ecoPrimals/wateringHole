# airSpring V0.10.0 — Cross-Ecosystem Absorption Handoff

**Date**: March 18, 2026
**From**: airSpring niche
**To**: ecoPrimals ecosystem, barraCuda/toadStool teams

## Summary

airSpring v0.10.0 absorbs patterns from wetSpring, healthSpring, groundSpring,
and sweetGrass to strengthen IPC, precision, safety, and discoverability. This
handoff documents what was absorbed, why, and what upstream evolution it enables.

## Absorbed Patterns

### 1. MCP Tool Definitions (from wetSpring)

`ipc/mcp.rs` — 10 ecology tools for Squirrel AI integration:

| Tool | JSON-RPC Method | Domain |
|------|----------------|--------|
| `airspring_et0` | `science.et0_fao56` | Hydrology |
| `airspring_hargreaves` | `science.et0_hargreaves` | Hydrology |
| `airspring_water_balance` | `science.water_balance` | Irrigation |
| `airspring_soil_moisture` | `science.soil_moisture_topp` | Soil physics |
| `airspring_dual_kc` | `science.dual_kc` | Crop science |
| `airspring_richards` | `science.richards_1d` | Soil hydrology |
| `airspring_yield_response` | `science.yield_response` | Agronomy |
| `airspring_spi_drought` | `science.spi_drought_index` | Drought |
| `airspring_diversity` | `science.shannon_diversity` | Ecology |
| `airspring_pedotransfer` | `science.pedotransfer_saxton_rawls` | Soil |

Includes `list_tools()`, `tool_to_method()`, and validation tests that all tools
map to registered capabilities.

### 2. Python Baseline Provenance Registry

`provenance.rs` — structured `PythonBaseline` records:
- 11 baselines with commit hashes, dates, categories
- `BaselineCategory`: PythonParity, GpuParity, Analytical, Published
- Canonical `commits` module with epoch hashes
- No-duplicate and ISO 8601 date validation tests

### 3. NaN-Safe Float Comparison (from healthSpring)

`f64::total_cmp` replaces `partial_cmp().unwrap_or(Equal)` in drift detection.
Eliminates silent NaN ordering bugs.

### 4. Panicking API → Result Evolution (from groundSpring)

- `wind_speed_at_2m()` → `Result<f64, AirSpringError::InvalidInput>`
- `solar_radiation_from_sunshine()` → `Result<f64, AirSpringError::InvalidInput>`

Pattern: public library APIs return errors; binary callers `.expect()`.

### 5. Kahan Compensated Summation (from barraCuda)

`eco::numerics::kahan_sum()` delegates to `barracuda::shaders::precision::cpu::kahan_sum()`.
O(1) accumulation error for precision-critical ecology paths.

### 6. ecoBin deny.toml Hardening (from groundSpring)

- `unlicensed = "deny"` in `[licenses]`
- 14 C-dependency crates banned (openssl-sys, libz-sys, zstd-sys, curl-sys, ring, etc.)
- Enforces sovereign binary reproducibility

### 7. Lint Convention Evolution

- 53 test modules: `#[allow(reason = "...")]` for blanket suppressions
- `#[expect(reason = "...")]` only where lint is known to fire
- Zero `#[allow(` without documented reason

## Upstream Evolution Enabled

### For barraCuda

- **MCP pattern**: The `McpTool` struct and `tool_to_method()` mapping could be
  promoted to a barraCuda utility crate for all springs to share
- **Provenance registry**: The `PythonBaseline` struct could become a shared type
  in barraCuda for cross-spring provenance tracking
- **kahan_sum**: Already upstream; airSpring now delegates cleanly

### For toadStool

- **Tool discovery**: toadStool can use MCP `tools/list` to discover airSpring's
  10 science capabilities at runtime
- **Capability routing**: MCP tool → JSON-RPC method mapping enables intelligent
  workload routing

### For All Springs

- **deny.toml template**: airSpring's 14-crate C-dependency ban list can serve
  as a shared template
- **Lint convention**: `#[allow(reason)]` for uncertain suppressions,
  `#[expect(reason)]` for known triggers — avoids unfulfilled-expectation errors

## Test Results

- **908 lib tests + 299 integration tests** (up from 894 + 299)
- **Zero clippy warnings** with `--all-targets -- -D warnings`
- **Zero format issues** (`cargo fmt --check`)

## Changed Files

### New
- `barracuda/src/ipc/mcp.rs` — MCP tool definitions
- `barracuda/src/provenance.rs` — Python baseline provenance registry
- `barracuda/src/eco/numerics.rs` — kahan_sum delegation

### Modified
- `barracuda/src/ipc/mod.rs` — MCP module export
- `barracuda/src/lib.rs` — provenance module declaration
- `barracuda/src/eco/mod.rs` — numerics module declaration
- `barracuda/src/gpu/atlas_stream/drift.rs` — total_cmp migration
- `barracuda/src/eco/evapotranspiration/atmosphere.rs` — assert → Result
- `barracuda/src/eco/evapotranspiration/radiation.rs` — assert → Result
- `barracuda/src/eco/evapotranspiration/mod.rs` — test callers updated
- `barracuda/src/eco/drought_index.rs` — allow → expect with reason
- `barracuda/src/gpu/autocorrelation.rs` — allow → expect with reason
- `barracuda/deny.toml` — ecoBin C-dep ban, unlicensed deny
- `barracuda/Cargo.toml` — version 0.10.0
- `barracuda/tests/eco_integration.rs` — tolerance fix + allow reasons
- `barracuda/tests/eco_richards.rs` — allow → expect
- `barracuda/tests/common/mod.rs` — allow with reasons
- `barracuda/src/bin/cross_validate.rs` — Result callers
- `barracuda/src/bin/simulate_season.rs` — Result callers
- 53 test modules — `#[allow(reason)]` lint evolution
- 6 specs files — version v0.10.0
- `README.md` — version, test counts
- `CHANGELOG.md` — v0.10.0 entry
