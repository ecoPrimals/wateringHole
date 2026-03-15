# wetSpring V113 — Provenance Trio + Deploy Graph (Global Handoff)

**Date:** 2026-03-15
**From:** wetSpring
**To:** biomeOS, BarraCUDA, ToadStool, Provenance Trio
**Status:** V113 — 19 capabilities, provenance trio, deploy graph

---

## Summary

wetSpring V113 is the first spring to fully implement the provenance trio
integration pattern. IPC surface expanded from 9 to 19 capabilities.
Cross-spring time series exchange format adopted. biomeOS deploy graph
created following `SPRING_AS_NICHE_DEPLOYMENT_STANDARD`.

## Changes

| Area | Detail |
|------|--------|
| Provenance Trio | `provenance.begin/record/complete` — rhizoCrypt → loamSpine → sweetGrass |
| New Capabilities | kinetics, alignment, taxonomy, phylogenetics, NMF, timeseries (×2) |
| Deploy Graph | `graphs/wetspring_deploy.toml` — full DAG with optional enrichment nodes |
| Time Series | `ecoPrimals/time-series/v1` ingest + outbound builders |
| Total Capabilities | 19 (was 9) |

## Upstream Requests

1. **biomeOS**: Integrate `wetspring_deploy.toml` into graph library
2. **BarraCUDA**: `SparseGemmF64` for NMF GPU acceleration
3. **Trio**: Consider `complete_experiment` convenience operation

## Quality

- 1,326 tests, 0 failures
- Zero clippy warnings (pedantic + nursery)
- Zero unsafe code
- Full graceful degradation when trio offline
