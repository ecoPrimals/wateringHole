# petalTongue v1.6.6 — Spring Absorption & Pattern Evolution Handoff

**Date**: March 16, 2026
**Version**: v1.6.6 (incremental, same version)
**Scope**: Cross-ecosystem pattern absorption, safe cast evolution, test isolation, UUI doc propagation

---

## What Changed

### Pattern Absorption from Springs

Audited 7 Springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, healthSpring, ludoSpring) and 10+ Primals for reusable patterns. Key absorptions:

| Pattern | Source | Status in petalTongue |
|---------|--------|----------------------|
| `temp_env` safe env testing | wetSpring V121, squirrel alpha.7, sweetGrass v0.7.15 | Already absorbed — `env_test_helpers` wraps `temp_env` |
| `TryFrom` safe casts | rhizoCrypt v0.13 | **Evolved** — doom-core `wad_loader.rs` migrated 3 dangerous `as` casts to `TryFrom` |
| Structured tracing (no `println!`) | squirrel alpha.7 | Already clean — all production `println!` is legitimate CLI/headless output |
| `tempfile::TempDir` for test sockets | wetSpring V121 | **Evolved** — 12 tests across 2 files migrated from `/tmp/` to `tempfile` |

### Safe Cast Evolution (doom-core)

`wad_loader.rs::read_directory` had 3 dangerous `i32 as u64`/`i32 as usize` casts on WAD file format values. Negative i32 values from malformed WAD files would silently produce invalid seeks or huge allocations. Replaced with `TryFrom` + `DoomError::InvalidWad` error propagation.

### Test Socket Isolation

Migrated 12 tests from hardcoded `/tmp/test-*.sock` paths to `tempfile::tempdir()`:
- `petal-tongue-discovery/src/jsonrpc_provider/tests.rs` (5 tests)
- `petal-tongue-discovery/tests/jsonrpc_integration_tests.rs` (7 tests)

Benefits: no cross-test socket collision, automatic cleanup, no stale socket files.

### UUI Ecosystem Documentation

Updated ecosystem-facing documents with Universal User Interface language:

| Document | Key Changes |
|----------|-------------|
| `PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md` | v1.6.6, UUI primal identity, SAME DAVE model, AGPL-3.0-or-later |
| `PETALTONGUE_LEVERAGE_GUIDE.md` | v1.1.0, "Universal User Interface primal", UUI philosophy, modality tiers |
| `petaltongue/README.md` | Smart refactoring results, absorption patterns |

---

## Metrics (unchanged from previous handoff)

| Metric | Value |
|--------|-------|
| Tests | 5,244 |
| Coverage | ~86% line / ~87% branch |
| Clippy | 0 warnings |
| Largest file | 902 lines |
| C dependencies | 0 |
| Edition | 2024 |
| License | AGPL-3.0-or-later |

---

## Ecosystem Integration State

### Springs WITH petalTongue Push Clients
- healthSpring V28 (6 DataBinding types, interaction roundtrip)
- wetSpring V121 (backpressure streaming, Scatter 2D)
- ludoSpring V14 (GameScene, Soundscape, 60 Hz sensor)
- neuralSpring S156 (ipc_push, learning curves)

### Springs WITHOUT Push Clients (future work)
- hotSpring (MD energy curves, phase diagrams)
- groundSpring V108 (ET0 time series, uncertainty budgets)
- airSpring v0.8.3 (CytokineBrain network, ET0)

### Primal Capabilities Not Yet Leveraged
- rhizoCrypt `dag.session.create` → session-scoped undo/redo
- sweetGrass `provenance.create_braid` → attribution tracing
- loamSpine `commit.session` → permanent dashboard snapshots
- NestGate `storage.put` → ecosystem-wide artifact sharing
- barraCuda `math.stat.*`, `math.tessellate.*` → blocked on dispatch table
- ToadStool `display.present` → blocked on dispatch wiring

---

## For Other Primals

petalTongue v1.6.6 demonstrates:
- **Pattern**: `TryFrom` instead of `as` for WAD/binary format parsing
- **Pattern**: `tempfile::tempdir()` for all test Unix socket paths
- **Pattern**: `temp_env` via wrapper module for environment variable testing
- **Standard**: UUI glossary (`petal_tongue_core::uui_glossary`) for canonical modality/user-type terminology

---

**Maintainer**: ecoPrimals / petalTongue
**License**: AGPL-3.0-or-later
