# petalTongue V1.6.5 — Ecosystem Evolution Handoff

**Date**: March 15, 2026  
**Status**: GREEN — 5,113 tests, zero clippy warnings, zero unwrap in production

---

## Changes

### deny(clippy::unwrap_used, clippy::expect_used)

Production code is now **zero-unwrap**. All `RwLock` poison `expect()` calls in
`capabilities.rs`, `registry.rs` evolved to graceful fallbacks (return `None`,
empty `Vec`, skip operation). `SystemTime` `expect()` in `accessibility.rs` →
`map_or(0.0, ...)`. Justified exceptions use `#[expect(..., reason = "...")]`.

Test code uses `#![cfg_attr(test, allow(...))]` per crate, matching the
groundSpring/airSpring/Squirrel ecosystem pattern.

### primal_names module

15 primal identity constants in `capability_names.rs`:
`PETALTONGUE`, `BIOMEOS`, `SONGBIRD`, `TOADSTOOL`, `BARRACUDA`, `CORALREEF`,
`BEARDOG`, `NESTGATE`, `SQUIRREL`, `RHIZOCRYPT`, `SWEETGRASS`, `LOAMSPINE`,
`SKUNKBAT`, `SOURDOUGH`, `PLASMIDBIN`.

For logging and capability filtering only — **not** for hardcoded routing.

### #[allow] → #[expect] migration

All `#[allow(...)]` in production code → `#[expect(..., reason = "...")]`:
- `capability_names.rs`: 5 modules (missing_docs)
- `metrics_dashboard_helpers.rs`: dead_code (cfg_attr conditional)
- `provenance_trio.rs`: missing_const_for_fn
- `petal-tongue-ui/lib.rs`: cast_sign_loss, struct_excessive_bools, too_many_lines, too_many_arguments
- `petal-tongue-ui-core/lib.rs`: format_push_string, unnecessary_wraps
- `petal-tongue-scene/lib.rs`: missing_docs

### Enriched capability.list

`capability.list` now returns ecosystem-standard enriched metadata:

```json
{
  "primal": "petaltongue",
  "version": "1.6.5",
  "transport": ["unix-socket", "tarpc"],
  "capabilities": ["ui.render", "visualization.render", ...],
  "methods": ["visualization.render", "visualization.render.stream", ...],
  "depends_on": [
    { "capability": "display", "required": false },
    { "capability": "gpu.dispatch", "required": false },
    { "capability": "shader.compile", "required": false }
  ],
  "data_bindings": 11,
  "geometry_types": 10
}
```

### SpringAdapterError typed enums

New variants: `MissingField { field, context }`, `UnrecognizedFormat`,
`UnsupportedChannelType(String)`.

### PrimalRegistration uses constants

`PrimalRegistration::petaltongue()` uses `primal_names::PETALTONGUE` and
`self_capabilities::ALL` — zero hardcoded strings.

---

## Explicit Needs from Ecosystem

See `wateringHole/petaltongue/PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md`.

Key gaps:
1. **ToadStool**: `display.present` not wired in dispatch — cannot push frames
2. **barraCuda**: Only 3 dispatch ops (zeros, ones, read) — need stat/tessellate/project
3. **Audio output**: No ecosystem path — need ToadStool `audio.*` or new audioSpring
4. **NestGate**: petalTongue doesn't call `storage.put/get` yet for artifact persistence

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 5,113 passing, 0 failures |
| Clippy | Zero warnings (deny unwrap/expect + pedantic + nursery) |
| Production unwrap/expect | 0 (3 justified #[expect] with reasons) |
| #[allow] in production | 0 (all migrated to #[expect]) |
| Primal name constants | 15 |
| DataBinding variants | 11 |
| Capability constants | 60+ |
