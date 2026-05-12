# biomeOS v3.20 — Deep Debt Evolution Handoff

**Date**: April 20, 2026
**From**: biomeOS Team
**Version**: 3.20
**Tests**: 7,802 passing (0 failures, fully concurrent)
**Clippy**: 0 warnings (pedantic + nursery)

---

## Summary

Deep debt pass addressing 6 items from comprehensive audit: smart refactoring,
hardcoded IP centralization, lint modernization, tensor capability translations,
nucleus graph expansion, and path constant evolution.

---

## Changes

### 1. Smart Refactor — nucleus.rs (820L → 780L)

Extracted `NucleusLaunchProfile`, `NucleusLaunchConfig`, and
`load_nucleus_profiles()` into a sibling module `nucleus_launch.rs`.

- **Motivation**: File was 820 lines, over the 800L production limit.
- **Approach**: Extracted data-driven config types and TOML loader — logically
  separate from nucleus orchestration. Used `#[path = "nucleus_launch.rs"]`
  since `nucleus.rs` is a file module, not a directory module.
- **Result**: `nucleus.rs` = 780 lines, `nucleus_launch.rs` = 58 lines.

### 2. Hardcoded IP Centralization → Constants

Added three new constants to `biomeos-types::constants`:

| Constant | Value | Module |
|----------|-------|--------|
| `DEFAULT_LOCALHOST_V6` | `"::1"` | `endpoints` |
| `EPHEMERAL_UDP_BIND` | `"0.0.0.0:0"` | `endpoints` |
| `LINUX_RUNTIME_DIR_PREFIX` | `"/run/user"` | `runtime_paths` |

Files updated:

| File | Before | After |
|------|--------|-------|
| `discovery_bootstrap.rs` | `"0.0.0.0:0"` | `EPHEMERAL_UDP_BIND` |
| `socket_discovery/strategy.rs` | `"0.0.0.0"` | `PRODUCTION_BIND_ADDRESS` |
| `defaults.rs` | `"::1"` | `DEFAULT_LOCALHOST_V6` |
| `neural-api-client-sync/lib.rs` | `"/run/user"` | local `LINUX_RUNTIME_DIR_PREFIX` const (minimal crate, no biomeos-types dep) |

### 3. `#[allow(missing_docs)]` → `#[expect()]`

Migrated 2 remaining `#[allow]` directives to Rust 2024 `#[expect]` with
documented reason strings:

- `crates/biomeos-compute/src/fractal/parent.rs`
- `crates/biomeos-compute/src/fractal/leaf.rs`

### 4. Tensor Capability Translations (barraCuda)

Added `[domains.tensor]` and `[translations.tensor]` to
`config/capability_registry.toml` with 33 methods covering barraCuda's full
JSON-RPC surface:

| Category | Methods | Count |
|----------|---------|-------|
| Tensor ops | create, matmul, matmul_inline, add, scale, clamp, reduce, sigmoid, transpose, batch.submit | 10 |
| Math | sigmoid, log2, relu, tanh, softmax | 5 |
| Statistics | mean, std_dev, weighted_mean, variance, median, correlation | 6 |
| Noise | perlin2d, perlin3d, simplex2d, simplex3d | 4 |
| Activation | fitts, hick | 2 |
| Linear algebra | solve, eigenvalues | 2 |
| Spectral | fft, power_spectrum | 2 |
| RNG | uniform, normal, seed | 3 |

This resolves the primalSpring upstream audit gap: "capability_registry.toml
has no `[translations.tensor]`".

### 5. nucleus_complete.toml — NestGate Streaming + barraCuda/coralReef

**NestGate streaming ops** added to the existing `nest_nestgate` node:
- `storage.store_blob`
- `storage.retrieve_range`
- `storage.object.size`
- `storage.namespaces.list`

**barraCuda** registered as `register_barracuda` node (30 capabilities):
tensor, math, stats, noise, linalg, spectral ops.

**coralReef** registered as `register_coralreef` node (7 capabilities):
shader compilation (WGSL, SPIR-V), validation, optimization.

`nucleus_validate` node updated to depend on both new nodes. Node count:
11 → 13. E2e test `NUCLEUS_NODE_IDS` updated accordingly.

This resolves two primalSpring upstream audit gaps:
- "nucleus_complete.toml missing NestGate streaming ops"
- "nucleus_complete.toml missing barraCuda/coralReef as separate nodes"

### 6. Test Alignment

`nucleus_composition_e2e.rs` expected node list updated from 11 → 13 entries
to match the expanded graph topology.

---

## Upstream Audit Gap Status

| Gap | Status |
|-----|--------|
| capability_registry.toml no tensor translations | **RESOLVED** (33 methods) |
| nucleus_complete.toml missing NestGate streaming | **RESOLVED** (4 ops) |
| nucleus_complete.toml missing barraCuda/coralReef | **RESOLVED** (2 nodes) |
| biomeOS must route through Tower Atomic | OPEN (architectural) |
| Graph transport metadata / TCP fallback | OPEN (medium) |

---

## Verification

```
cargo check --workspace        # clean
cargo clippy --workspace       # 0 warnings
cargo test --workspace         # 7,802 pass, 0 fail
cargo fmt --check              # clean
```

---

## Files Modified

| File | Change |
|------|--------|
| `crates/biomeos/src/modes/nucleus.rs` | Extracted launch profile types; 820→780L |
| `crates/biomeos/src/modes/nucleus_launch.rs` | **NEW** — launch profile types + loader |
| `crates/biomeos-types/src/constants/mod.rs` | Added `DEFAULT_LOCALHOST_V6`, `EPHEMERAL_UDP_BIND`, `LINUX_RUNTIME_DIR_PREFIX` |
| `crates/biomeos-types/src/defaults.rs` | `"::1"` → `DEFAULT_LOCALHOST_V6` |
| `crates/biomeos-core/src/discovery_bootstrap.rs` | `"0.0.0.0:0"` → `EPHEMERAL_UDP_BIND` |
| `crates/biomeos-core/src/socket_discovery/strategy.rs` | `"0.0.0.0"` → `PRODUCTION_BIND_ADDRESS` |
| `crates/neural-api-client-sync/src/lib.rs` | `/run/user` → local constant |
| `crates/biomeos-compute/src/fractal/parent.rs` | `#[allow]` → `#[expect]` |
| `crates/biomeos-compute/src/fractal/leaf.rs` | `#[allow]` → `#[expect]` |
| `config/capability_registry.toml` | Added tensor domain + 33 translations |
| `graphs/nucleus_complete.toml` | NestGate streaming + barraCuda + coralReef nodes |
| `crates/biomeos-atomic-deploy/tests/nucleus_composition_e2e.rs` | Node count 11→13 |
