# wetSpring V112 → barraCuda / toadStool: Streaming-Only I/O + Capability Discovery

**Date:** 2026-03-14
**From:** wetSpring V112
**To:** barraCuda / toadStool team
**License:** AGPL-3.0-or-later

---

## Executive Summary

wetSpring V112 completes the streaming-only I/O evolution by removing all
deprecated whole-file buffering parsers (`parse_fastq`, `parse_mzml`,
`parse_ms2`). Hardcoded primal paths replaced with `$PATH` and
`$XDG_RUNTIME_DIR` runtime discovery. All 40 clippy pedantic+nursery warnings
eliminated. Build-breaking compilation errors fixed. Zero warnings across all
quality gates.

## Key Changes for Downstream Teams

### barraCuda: I/O Pattern Recommendation

wetSpring deleted 3 deprecated `parse_*()` functions that loaded entire files
into `Vec<T>`. All I/O now uses streaming iterators:

```
FastqIter::open(path) -> Iterator<Item=Result<FastqRecord>>
MzmlIter::open(path) -> Iterator<Item=Result<MzmlSpectrum>>
Ms2Iter::open(path)  -> Iterator<Item=Result<Ms2Spectrum>>
```

**Recommendation**: New barraCuda I/O modules (e.g., `barracuda::io::biom`)
should adopt this streaming iterator pattern from the start. No `parse_*`
convenience functions.

### toadStool: Capability-Based Discovery

Hardcoded paths eliminated:

- `../../phase2/biomeOS/target/release/biomeos` → `which_primal("biomeos")` via `$PATH`
- `/run/user/1000/biomeos` → `$XDG_RUNTIME_DIR/biomeos`

Primals must discover each other at runtime. Zero compile-time primal coupling.

### Tolerance Architecture

Inline `1e-10` → `tolerances::ANALYTICAL_LOOSE`. wetSpring now has zero inline
tolerance literals. All 180 named constants are documented with scientific
rationale and provenance. Consider absorbing this hierarchy into
`barracuda::tolerances` for ecosystem-wide use.

## Absorption Status

Fully lean on barraCuda v0.3.5 (`0649cd0`). 150+ primitives consumed. 0 local
WGSL. 0 unsafe. 0 clippy warnings. 0 hardcoded primal paths. 0 inline
tolerances. 0 deprecated APIs.

## Test Status

1,384 passed, 4 failed (pre-existing: 1 upstream nautilus bug, 3 GPU f32 parity),
42 ignored. All failures documented in `ABSORPTION_MANIFEST.md`.

## Upstream Requests (Carried Forward from V114)

1. `barracuda::io::biom` — streaming BIOM parser (P0)
2. `barracuda::ncbi::entrez::esearch_ids()` — batch accession fetch (P0)
3. `barracuda::bio::kinetics::gompertz_fit()` — Track 6 biogas (P0)
4. `bingocube-nautilus`: Fix `from_json` observation count restoration

## Full Details

See `wetSpring/wateringHole/handoffs/WETSPRING_V112_STREAMING_PEDANTIC_CAPABILITY_HANDOFF_MAR14_2026.md`
for complete handoff with code examples and evolution roadmap.
