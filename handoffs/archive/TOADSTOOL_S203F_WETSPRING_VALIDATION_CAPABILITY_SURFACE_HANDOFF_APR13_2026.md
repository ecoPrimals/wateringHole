# ToadStool S203f — wetSpring Validation + Capability Surface Update

**Date**: April 13, 2026
**Session**: S203f
**Primal**: toadStool
**Prior**: S203e (doc cleanup + network centralization)
**Context**: Cross-validated against wetSpring V143 deploy graphs and gap analysis

---

## Summary

Validated toadStool's IPC surface against wetSpring's V143 expectations
(PG-05 gap). Promoted `compute.execute` to a direct route, added pipeline
methods to `provided_capabilities`, and updated plasmidBin metadata with
the full 46-method capability surface.

## wetSpring Gap Analysis (PG-05)

**Gap**: wetSpring's deploy graphs list `compute.execute` and
`compute.dispatch.submit` as toadStool capabilities. wetSpring uses
barraCuda as a path dependency for math/GPU; toadStool is the NUCLEUS
compute dispatch layer.

**Finding**: `compute.execute` was ALREADY registered in toadStool's
`SemanticMethodRegistry` (mapping to `execute_workload` → `submit_workload`
handler). It was callable via semantic resolution but not advertised as a
direct route.

**Fix (S203f)**:
- Promoted `compute.execute` to direct route in `handle_method` match
- Added to `DIRECT_JSONRPC_METHODS` constant (now 47 direct methods)
- Added `dispatch.pipeline.submit` and `dispatch.pipeline.status` to
  `provided_capabilities` compute group
- Added `execute` to compute group methods list

All methods wetSpring expects are now directly routable AND advertised:

| Method | Status |
|--------|--------|
| `compute.execute` | Direct route (S203f) |
| `compute.dispatch.submit` | Direct route (S199+) |
| `compute.dispatch.pipeline.submit` | Direct route (S199+) |
| `compute.submit` | Direct route (original) |
| `health.liveness` | Direct route (S198) |
| `capabilities.list` | Direct route (S191+) |
| `identity.get` | Direct route (S191+) |

## plasmidBin Update

`plasmidBin/toadstool/metadata.toml` updated:
- Capabilities: 6 stale entries → 46 actual callable methods
- `min_ipc_version`: "1.0" → "2.0"
- Provenance date: 2026-03-25 → 2026-04-12
- Added `tests = 21600`, `wire_standard = "L3-partial"`

## Remaining Gaps (wetSpring PG-* status)

| # | Gap | Status | Owner |
|---|-----|--------|-------|
| PG-01 | Proto-nucleate parsing | **Resolved V141** | wetSpring |
| PG-02 | Provenance trio IPC | Partial (V142) | rhizoCrypt/loamSpine/sweetGrass |
| PG-03 | Name-based discovery | Structural | Songbird/biomeOS |
| PG-04 | NestGate storage IPC | Not wired | NestGate |
| PG-05 | toadStool compute IPC | **Addressed S203f** — all expected methods advertised + directly routable | toadStool |
| PG-06 | Ionic bond negotiation | Metadata only | primalSpring |
| PG-07 | Capability drift | **Resolved V141** | wetSpring |

**PG-05 note**: wetSpring currently uses barraCuda as a path dependency
(correct for validation springs). The IPC path through toadStool becomes
relevant at NUCLEUS deployment. toadStool's compute surface is now
confirmed ready for that transition.

## Quality Gates

| Gate | Value |
|------|-------|
| Clippy | 0 warnings |
| Tests | 9/9 core handler tests pass (including Wire Standard L3 envelope) |
| compute.execute | Direct route confirmed |
| capabilities.list | 47+ methods advertised, sorted, Wire Standard L3 |
