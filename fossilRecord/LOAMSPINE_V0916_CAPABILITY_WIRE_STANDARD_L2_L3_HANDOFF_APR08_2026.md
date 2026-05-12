# loamSpine v0.9.16 — Capability Wire Standard L2/L3 Compliance

**Date**: April 8, 2026
**From**: loamSpine team
**To**: primalSpring (coordinator), biomeOS team, downstream springs
**Context**: primalSpring audit identified loamSpine `capabilities.list` as Wire Standard L2 partial — `methods` was an array of objects (Format D), not the required flat string array. `identity.get` was not implemented.

---

## Resolved Gap

**Source**: primalSpring Phase 26 live validation → Capability Wire Standard v1.0 → loamSpine catch-up sprint

### Before

```json
{
  "primal": "loamspine",
  "version": "0.9.16",
  "capabilities": ["permanence", "session.commit", ...],
  "methods": [
    {"method": "spine.create", "domain": "spine", "cost": "low", "deps": []},
    ...
  ],
  "operation_dependencies": {...},
  "cost_estimates": {...}
}
```

- `methods` was Format D (array of objects) — biomeOS had to traverse `method` key per entry
- Only 24 methods advertised (missing `health.liveness`, `health.readiness`, `permanence.*`, `tools.*`, `identity.get`)
- No `identity.get` method
- No `provided_capabilities` grouping
- No `consumed_capabilities` declaration

### After

```json
{
  "primal": "loamspine",
  "version": "0.9.16",
  "methods": [
    "spine.create", "spine.get", "spine.seal",
    "entry.append", "entry.get", "entry.get_tip",
    "certificate.mint", "certificate.transfer", "certificate.loan",
    "certificate.return", "certificate.get", "certificate.verify",
    "certificate.lifecycle",
    "slice.anchor", "slice.checkout", "slice.record_operation", "slice.depart",
    "proof.generate_inclusion", "proof.verify_inclusion",
    "session.commit", "braid.commit",
    "anchor.publish", "anchor.verify",
    "health.check", "health.liveness", "health.readiness",
    "capabilities.list", "tools.list", "tools.call", "identity.get",
    "permanence.commit_session", "permanence.verify_commit",
    "permanence.get_commit", "permanence.health_check"
  ],
  "provided_capabilities": [
    {"type": "spine", "methods": ["create", "get", "seal"], ...},
    {"type": "entry", "methods": ["append", "get", "get_tip"], ...},
    {"type": "certificate", "methods": ["mint", "transfer", ...], ...},
    {"type": "proof", "methods": ["generate_inclusion", "verify_inclusion"], ...},
    {"type": "anchor", "methods": ["publish", "verify"], ...},
    {"type": "session", "methods": ["commit"], ...},
    {"type": "braid", "methods": ["commit"], ...},
    {"type": "slice", "methods": ["anchor", "checkout", ...], ...},
    {"type": "health", "methods": ["check", "liveness", "readiness"], ...}
  ],
  "consumed_capabilities": ["crypto.sign", "artifact.store", ...],
  "capabilities": ["permanence", "session.commit", ...],
  "cost_estimates": {...},
  "operation_dependencies": {...}
}
```

- **L2 compliant**: `{primal, version, methods}` envelope with flat string array
- **L3 compliant**: `provided_capabilities` grouping (9 domains), `consumed_capabilities`, `cost_estimates`, `operation_dependencies`
- All 32 callable methods advertised
- Backward compatible: `capabilities` array retained for legacy biomeOS format parsers

### identity.get

```json
{"jsonrpc":"2.0","method":"identity.get","id":1}
→
{"jsonrpc":"2.0","result":{"primal":"loamspine","version":"0.9.16","domain":"permanence","license":"AGPL-3.0-or-later"},"id":1}
```

---

## Changes

| File | Change |
|------|--------|
| `crates/loam-spine-core/src/neural_api/mod.rs` | `methods` → flat string array from `niche::METHODS`. Added `provided_capabilities`, `consumed_capabilities`. New `identity_response()` function with `OnceLock` cache. |
| `crates/loam-spine-core/src/neural_api/mcp.rs` | Added `identity_get` MCP tool. Updated `capability_list` mapping to canonical `capabilities.list`. |
| `crates/loam-spine-core/src/neural_api/tests.rs` | Updated MCP tool coverage test for flat methods. Added `identity_response_fields` test. Updated canonical method references. |
| `crates/loam-spine-core/src/niche.rs` | Added `identity.get` + `permanence.*` to `METHODS`. `capability.list` → `capabilities.list` in `METHODS`, `SEMANTIC_MAPPINGS`, `COST_ESTIMATES`. |
| `crates/loam-spine-api/src/jsonrpc/mod.rs` | Added `identity.get` dispatch handler. |
| `crates/loam-spine-api/src/jsonrpc/tests.rs` | Updated `capability_list_method` for flat methods. Added `identity_get_method` test. |
| `crates/loam-spine-api/src/jsonrpc/tests_protocol.rs` | Updated `uds_capabilities_list_wire_format` for Wire Standard L2/L3 assertions. Added `uds_identity_get_wire_format` test. |
| `graphs/loamspine_deploy.toml` | Expanded capabilities from 20 → 32 methods. Uses canonical `capabilities.list`. |
| `CHANGELOG.md`, `STATUS.md`, `WHATS_NEXT.md` | Updated with Wire Standard L2/L3 entries. Test count 1,301 → 1,304. |

---

## Verification

```
cargo clippy --all-targets   → 0 warnings
cargo test                   → 1,304 passed, 0 failed
```

---

## Wire Standard Compliance Matrix

| Level | Requirement | Status |
|-------|------------|--------|
| L1 | `capabilities.list` responds over UDS | PASS |
| L1 | Response parseable by biomeOS | PASS |
| L1 | `health.liveness` implemented | PASS |
| L2 | `result.primal` field | PASS |
| L2 | `result.version` field | PASS |
| L2 | `result.methods` flat string array | **PASS** (was FAIL) |
| L2 | All methods callable | PASS |
| L2 | Method names follow `domain.operation` | PASS |
| L2 | `identity.get` implemented | **PASS** (was FAIL) |
| L2 | Health triad (liveness/check/readiness) | PASS |
| L3 | `provided_capabilities` grouping | **PASS** (was MISSING) |
| L3 | `consumed_capabilities` declared | **PASS** (was MISSING) |
| L3 | `cost_estimates` present | PASS |
| L3 | `operation_dependencies` present | PASS |

**loamSpine is now Wire Standard Level 3 compliant.**

---

## Remaining Debt (out of scope)

- biomeOS live validation against new wire format (biomeOS team)
- `permanence.*` methods not yet exposed via MCP tools (low priority — these are legacy JSON-RPC aliases)
- `health.liveness`/`health.readiness`/`tools.*` not in MCP tools (meta methods, not user-facing)

---

**License**: AGPL-3.0-or-later
