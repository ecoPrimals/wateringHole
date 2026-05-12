# Squirrel v0.1.0 — Deep Debt: Orphan Removal, Feature Hygiene, Capability Naming

**Date**: April 20, 2026
**From**: Squirrel alpha.52+

## Changes

### Orphaned Code Removal

Deleted `crates/core/auth/src/auth/` (4 files, ~35kb):
- `mod.rs`, `discovery.rs`, `operations.rs`, `tests.rs`
- Referenced `reqwest::Client` via dead `#[cfg(feature = "http-auth")]`
- Never wired from `lib.rs` — completely unmounted since stadial gate cleanup

### Feature Flag Hygiene

Removed placeholder features with **zero** `cfg(feature = "...")` references:

| Crate | Removed Features |
|-------|-----------------|
| `squirrel-ecosystem-integration` | `songbird`, `toadstool` |
| `squirrel` (main) | `enhanced_error_handling`, `optimizations` |
| `squirrel-mcp` | `tls`, `plugins`, `persistence`, `sync-placeholders`, `disabled_until_rewrite` |
| `ecosystem-api` | Dead `#[cfg(test, feature = "http-api")]` test module |

### SDK Feature Name Mismatch

Fixed `cfg(feature = "console_error_panic_hook")` → `cfg(feature = "console")` across
4 sites in `sdk/src/lib.rs`. The Cargo feature name is `console` (which enables the
`console_error_panic_hook` dep); the cfg checks were using the dep name, not the feature name.

### Niche Capability Naming

`DEPENDENCIES` table in `niche.rs` evolved from hardcoded primal names to
capability roles:

| Before | After |
|--------|-------|
| `primal_names::BEARDOG` | `"security"` |
| `primal_names::SONGBIRD` | `"discovery"` |
| `primal_names::TOADSTOOL` | `"compute"` |
| `primal_names::NESTGATE` | `"storage"` |
| `primal_names::PRIMALSPRING` | `"coordination"` |
| `primal_names::PETALTONGUE` | `"visualization"` |

Hardcoded primal names in log messages evolved:
- `"biomeos"` → `"orchestration"` (integration metadata)
- `"BearDog coordination"` → `"security provider coordination"` (auth log)
- `"biomeOS discovery"` → `"orchestrator discovery"` (socket bind log)

### `#[allow()]` → `#[expect(reason)]`

Migrated remaining production `#[allow(dead_code)]` to `#[expect(dead_code, reason)]`
in `interning.rs` and `client.rs` (SDK wasm32 test helpers).

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 passing / 0 failures |
| Clippy | CLEAN (`-D warnings`) |
| `cargo fmt` | PASS |
| Dead code deleted | ~1,140 lines (4 orphan files + dead test module) |
| Features removed | 10 placeholder/unused |

## Upstream Blocks (Unchanged)

1. **Three-tier genetics** — blocked on `ecoPrimal >= 0.10.0`
2. **BLAKE3 content curation** — blocked on NestGate content-addressed storage API
3. **Phase 3 cipher negotiation** — blocked on BearDog `btsp.negotiate` server-side
