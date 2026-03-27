# biomeOS v2.66 — primalSpring-Aligned Capability Discovery Evolution

**Date**: March 22, 2026
**Author**: AI Assistant (Cursor Agent)
**Status**: Complete — 7,135 tests passing, 0 warnings

---

## Summary

This release aligns biomeOS with primalSpring's validation expectations by fixing
the Neural API socket readiness blocker, centralizing capability discovery into a
single 5-tier protocol, and evolving identity-based discovery patterns to
capability-based ones.

## Key Changes

### 1. Neural API Socket Early-Bind (exp060 Fix)

`server_lifecycle.rs` `serve()` now binds the Unix socket **before** mode
detection, bootstrap, and translation loading. External probes (primalSpring
exp060) can connect immediately.

### 2. Centralized 5-Tier Capability Discovery

New `biomeos_types::capability_discovery` module:

1. `{CAPABILITY}_PROVIDER_SOCKET` env override
2. `{PRIMAL}_SOCKET` identity env fallback (taxonomy)
3. XDG runtime dir filesystem probe
4. `/tmp/biomeos` fallback
5. Socket-registry.json file lookup

5 identity-based callsites evolved:
- `biomeos-nucleus/identity.rs`
- `biomeos-nucleus/discovery.rs`
- `biomeos-ui/songbird.rs`
- `biomeos-federation/discovery/mod.rs`
- `biomeos/modes/enroll.rs`

### 3. Taxonomy & Translation Fixes

- `GeneticLineage` default primal: `biomeos` → `beardog`
- `"genetic"` alias added to `from_str_flexible`
- Genetic/lineage domain translations in `defaults.rs`
- `BIOMEOS_GENETIC_PROVIDER` env override

### 4. Niche Self-Knowledge

- `BIOMEOS_SELF_CAPABILITIES` constant in `primal_names.rs`
- `register_self_in_registry` data-driven
- `capability_sockets.rs` match → taxonomy-driven
- Science bootstrap hints use canonical constants

## Cross-Spring Impact

| Spring | Impact |
|--------|--------|
| primalSpring | exp060 socket readiness blocker resolved; 5-tier protocol aligned |
| All springs | Centralized discovery means consistent behavior across ecosystem |
| beardog | Now canonical owner of genetic/lineage capabilities |

## Metrics

- **Tests**: 7,135 passing (0 failures)
- **Clippy**: 0 warnings (pedantic+nursery)
- **Files modified**: 18 production + 5 test files
- **New module**: `biomeos_types::capability_discovery` (5-tier protocol)

---

*biomeOS v2.66 | March 22, 2026 | scyBorg triple-copyleft (AGPL-3.0-only + ORC + CC-BY-SA 4.0)*
