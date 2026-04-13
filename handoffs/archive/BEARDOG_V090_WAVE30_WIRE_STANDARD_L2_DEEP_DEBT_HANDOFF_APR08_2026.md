# BearDog v0.9.0 — Wave 29–30 Handoff

**Primal**: BearDog
**Version**: 0.9.0
**Date**: April 8, 2026
**Scope**: Wire Standard Level 2 completion + Deep Debt Sweep

---

## Wire Standard Level 2 — COMPLETE

BearDog now satisfies all Wire Standard Level 2 requirements per `CAPABILITY_WIRE_STANDARD.md`.

### `capabilities.list` — flat `methods` array added

The `capabilities.list` JSON-RPC response now includes a top-level `methods` array alongside the existing `provided_capabilities` structure (Format E, Tier 1 non-breaking migration). The array is dynamically populated from `HandlerRegistry::all_methods()`, filtered to fully-qualified `domain.operation` names per `SEMANTIC_METHOD_NAMING_STANDARD.md`.

### `identity.get` — implemented

New JSON-RPC method returning:

```json
{
  "primal": "beardog",
  "version": "0.9.0",
  "domain": "crypto",
  "license": "AGPL-3.0-or-later"
}
```

### Implementation details

- `CapabilitiesHandler` moved to Phase 2 of `HandlerRegistry::new()` (two-phase construction) to receive `Arc<HandlerRegistry>` for dynamic method enumeration
- `wire_standard_methods()` helper filters `all_methods()` to `domain.operation` style names only
- Legacy `handle_identity` preserved for backward compatibility; new `handle_identity_get` serves L2 response
- `CAPABILITY_WIRE_STANDARD.md` compliance table updated: BearDog L2 → ✓

---

## Deep Debt Sweep (Wave 30)

### Self-Knowledge Violations Fixed

| Item | Before | After |
|------|--------|-------|
| `attempt_songbird_registration` | Named Songbird in function + docs | `attempt_orchestrator_registration`, capability-based language |
| `key_export/types.rs` doc | Named `ToadStool` | "Compatible with any primal" |

### Dead Code / Overstep Removed

| Item | Issue | Resolution |
|------|-------|------------|
| `DatabaseStorageBackend` | All 7 trait methods returned `unsupported_operation` | Removed (beardog-tunnel `software_hsm/types.rs`) |
| `handle_key_generate` v1 | `#[allow(dead_code)]`, superseded by v2 | Removed from `key.rs` (875L → 719L) |
| Security/Storage/Network `MigrationAdapter`s | Domain overstep (not BearDog's responsibility) | Removed from `ecosystem_integration.rs` |
| `generate_aes_key_with_seed` | Only used in tests after v1 removal | Gated `#[cfg(test)]` |

### Stubs Evolved

| Item | Before | After |
|------|--------|-------|
| `PerformanceOptimizer` (beardog-types) | No-op `initialize_optimizations()` + `evaluate_scaling_needs()` | Config holder only; real optimization in beardog-core |
| `effectiveness_score` | Undocumented magic floats | Named constants (`DISTRIBUTED_BASELINE`, etc.) with rationale |
| HSM discoverer stubs (6) | `warn!("not yet implemented")` | `info!` with accurate reason (no credentials, no hardware, etc.) |

### Lint Cleanup

- 35 blanket `#[allow(unused_imports, clippy::nonminimal_bool, dead_code)]` removed from test modules in beardog-utils (clippy confirms they suppressed nothing)

---

## Gate Results

| Gate | Status |
|------|--------|
| `cargo fmt -- --check` | Clean |
| `cargo clippy --workspace --all-targets` | 0 warnings |
| `cargo test --workspace` | All pass |
| `cargo doc --workspace --no-deps` | Builds (pre-existing doc link warnings only) |

---

## Files Changed (key paths)

- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` — Wire Standard L2 (methods array + identity.get)
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/mod.rs` — Two-phase handler construction
- `crates/beardog-cli/src/handlers/server.rs` — `attempt_orchestrator_registration`
- `crates/beardog-cli/src/handlers/key_export/types.rs` — ToadStool reference removed
- `crates/beardog-cli/src/handlers/key.rs` — Dead v1 handler removed (875L → 719L)
- `crates/beardog-tunnel/src/tunnel/hsm/software_hsm/types.rs` — DatabaseStorageBackend removed
- `crates/beardog-types/src/canonical/providers_unified/ecosystem_integration.rs` — Migration adapters removed
- `crates/beardog-types/src/production/optimization.rs` — PerformanceOptimizer evolved
- `crates/beardog-types/src/canonical/relationships/coordination.rs` — Named effectiveness constants
- `crates/beardog-tunnel/src/tunnel/hsm/universal_discovery/discovery_engine.rs` — Discovery messages
- `crates/beardog-utils/src/**` — 35 files: blanket allow removal
- `src/main.rs` — KeyAction::Generate → v2
- `CHANGELOG.md`, `STATUS.md` — Updated
- `SCYBORG_EXCEPTION_PROTOCOL.md` — License consistency fix

---

## Remaining L3 Gaps

BearDog does not yet implement Level 3 (Composable):

- [ ] `consumed_capabilities` declared
- [ ] `cost_estimates` for high-cost methods
- [ ] `operation_dependencies` for methods with prerequisites

These are tracked per `CAPABILITY_WIRE_STANDARD.md` and are not blocking for current ecosystem routing.
