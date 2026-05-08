# hotSpring V0.6.32 — Paper Notebooks + Local Debt Resolved

**Date**: May 7, 2026
**From**: hotSpring team
**Absorbed by**: primalSpring (Phase 59)

## Summary

hotSpring shipped 12 publishable-grade paper baseline notebooks (`notebooks/papers/`)
covering all 22 reproduced physics papers. 993/993 tests, clippy clean. 17 total
notebooks CI-ready (Agg backend removed, NumPy 2.x compat, requirements.txt).

## Method Name Drifts Found and Fixed

| Validator | Old (wrong) | New (correct) |
|-----------|-------------|---------------|
| `validate_nucleus_node` | `shader.compile` | `shader.compile.wgsl` |
| `validate_nucleus_nest` | `dag.create_session` | `dag.session.create` |
| `validate_nucleus_nest` | `provenance.create_braid` | `braid.create` |

**Systemic risk**: String literals in validator binaries can drift from capability
registry without detection. primalSpring resolved this as PG-65: `config/capability_registry.toml`
(208 methods) + `tools/check_method_strings.sh` CI check.

## Upstream Gaps Registered

| PG | Priority | Owner | Issue |
|----|----------|-------|-------|
| PG-60 | P1 | rhizoCrypt | Silent timeout on UDS connect |
| PG-61 | P2 | barraCuda | Missing `stats.entropy` IPC method |
| PG-62 | P2 | toadStool | Short timeout, undocumented minimum |
| PG-63 | P2 | sporePrint | Matplotlib Agg guidance conflict (RESOLVED in wateringHole) |
| PG-64 | P1 | sporePrint | `render_notebooks.sh` not implemented |
| PG-65 | P2 | primalSpring | Method string drift CI (**RESOLVED**) |

## primalSpring Absorption

- `downstream_manifest.toml`: hotSpring `depends_on` updated with provenance trio
- Method audit: all 3 drifted strings already correct in primalSpring (`niche.rs`, `composition/tests.rs`)
- PG-65 shipped: `config/capability_registry.toml` + `tools/check_method_strings.sh`
- PG-63 fixed in wateringHole: `SPRING_EVOLUTION_TARGETS.md` Agg guidance corrected
