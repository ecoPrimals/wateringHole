# wetSpring V144 — biomeOS v3.04 Composition Alignment

**Date**: April 12, 2026
**Spring**: wetSpring
**Version**: V144
**License**: AGPL-3.0-or-later

---

## Summary

V144 aligns wetSpring with biomeOS v3.04's composition elevation. Universal
`composition.*_health` methods (tower, node, nest, nucleus) are removed from
wetSpring in favor of biomeOS orchestrator-owned endpoints per
`COMPOSITION_HEALTH_STANDARD.md`. The blocking `akida-driver` path case
mismatch is fixed.

**Tests**: 1,949 passed, 0 failed
**Clippy**: Zero warnings (pedantic + nursery, `-D warnings`)
**Docs**: Clean (`missing_docs = "deny"` workspace-wide)

---

## Changes

### BLOCKING: akida-driver path case mismatch (RESOLVED)

`barracuda/Cargo.toml` referenced `../../../primals/toadstool/` but the
actual directory is `toadStool` (camelCase). On case-sensitive Linux
filesystems, the workspace could not resolve — even without `--features npu`,
Cargo loads all path dependencies at manifest resolution.

**Fix**: `toadstool` → `toadStool`

### Composition evolution: universal methods → biomeOS

Per `COMPOSITION_HEALTH_STANDARD.md`, universal composition health methods
are owned by "primalSpring or biomeOS", not individual springs.

**Removed from wetSpring:**
- `composition.tower_health` (biomeOS owns Tower health)
- `composition.node_health` (biomeOS owns Node health)
- `composition.nest_health` (biomeOS owns Nest health)
- `composition.nucleus_health` (biomeOS owns NUCLEUS health)
- `probe_capability()` function (only used by removed handlers)

**Retained:**
- `composition.science_health` — spring-specific domain health per standard

**Updated:**
- `CAPABILITIES`: 46 → 42
- `capability_domains::DOMAINS` methods: 41 → 37
- `capability_registry.toml`: universal entries removed
- Dispatch table: universal arms removed
- Integration tests: universal roundtrip tests → method-not-found assertion
- Count assertions across dispatch, capability_domains, niche tests

### Impact

- Eliminates routing ambiguity where Neural API could route universal
  composition queries to wetSpring instead of biomeOS
- Aligns with the COMPOSITION_HEALTH_STANDARD ownership model
- Reduces wetSpring's surface area to only what it owns

---

## Quality Gates

| Gate | Status |
|------|--------|
| Tests | 1,949 passed (0 failed) |
| Clippy | PASS (pedantic + nursery, `-D warnings`) |
| Docs | PASS (`missing_docs = "deny"`) |
| Unsafe | 0 (`#![forbid(unsafe_code)]` workspace-wide) |
| TODO/FIXME | 0 |
| Edition | 2024 (all crates) |
| MSRV | 1.87 |

---

## For biomeOS / primalSpring

- wetSpring no longer advertises universal composition methods
- biomeOS's Neural API will route `composition.tower_health` etc. to its
  own handlers (v3.04+) without ambiguity
- `composition.science_health` remains for spring-specific health queries
- wetSpring's `capability.list` response now shows 37 methods (was 41)
