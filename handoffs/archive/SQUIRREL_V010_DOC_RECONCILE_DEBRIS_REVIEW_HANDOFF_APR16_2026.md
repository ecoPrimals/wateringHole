<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Doc Reconciliation & Debris Review Handoff

**Date**: April 16, 2026 (session final)
**Primal**: Squirrel (AI Coordination)
**Version**: 0.1.0
**Status**: INTERSTADIAL-READY (upstream blocks only: genetics ≥0.10.0, NestGate BLAKE3 API)

## Summary

Final housekeeping pass: root doc reconciliation, stale feature gate cleanup, capability-naming alignment in documentation, and comprehensive debris review.

## Root Doc Updates

| File | Change |
|------|--------|
| `README.md` | File count ~1,037→~1,039, line count ~336k→~337k |
| `CONTEXT.md` | Same count updates |
| `ORIGIN.md` | Ecosystem relationships evolved from primal-specific names to capability-based language |
| `CURRENT_STATUS.md` | Removed stale `ring` known issue (eliminated in stadial gate); removed `local-jwt` and `nvml` from feature gates (features eliminated); `BearDog Crypto`/`ToadStool AI` ecosystem entries → `Security Provider Crypto`/`Compute Provider AI`; `DEPENDENCIES` and `CONSUMED_CAPABILITIES` descriptions use capability roles; `JWT_SIGNING_KEY_ID` usage description evolved from "BearDog key lookup" to "Security provider key lookup" |

## Debris Review

| Category | Result |
|----------|--------|
| TODO/FIXME/HACK in `.rs` files | **0** |
| TODO/FIXME/HACK in `.md` files | 0 live (all are historical changelog references) |
| Scripts (`.sh`, `.py`) | **0** in workspace (none outside archive) |
| Backup/temp files (`.bak`, `.orig`, `.swp`) | **0** |
| OS debris (`.DS_Store`, `__pycache__`) | **0** |
| Orphan/uncompiled code | **0** (all cleaned in prior sessions) |
| Stale spec docs | 8 gen2-era specs marked `historical` in prior session |

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,160 passing / 0 failures |
| Coverage | 90.1% region / 89.6% line |
| `.rs` files | ~1,039 |
| Lines | ~337k |
| Files >800L (prod) | 0 |
| Clippy | CLEAN (`pedantic + nursery + cargo`, `-D warnings`) |
| `cargo fmt` | PASS |
| `cargo deny` | PASS |
| `unsafe` | 0 (`forbid` workspace-wide) |
| `#[allow()]` in prod | 0 (all `#[expect(reason)]`) |
| C deps (default) | 0 (pure Rust) |
| `ring`/`reqwest` in lockfile | ELIMINATED |

## Upstream Blocks (unchanged)

1. **Three-tier genetics** — awaits `ecoPrimal ≥0.10.0` (`mito_beacon_from_env()`)
2. **BLAKE3 content curation** — awaits NestGate content-addressed storage API stability
