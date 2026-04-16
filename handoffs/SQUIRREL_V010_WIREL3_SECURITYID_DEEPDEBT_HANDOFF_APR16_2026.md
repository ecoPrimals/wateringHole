<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Wire Standard L3, Security Service ID Evolution, Deep Debt Closure

**Date**: April 16, 2026
**Primal**: Squirrel (AI Coordination)
**Sessions**: Z (Wire Standard L3 + security service ID evolution + deep debt final audit)
**Commit range**: `b93e8ca7..HEAD`

---

## Executive Summary

Final evolution pass completing **Wire Standard L3 Composable** compliance, **security service ID constant extraction**, and a **comprehensive deep debt audit** confirming zero remaining actionable items. Squirrel is now at the cleanest state in its history.

---

## Wire Standard L3 Composable

`capabilities.list` upgraded from L2 (flat methods array) to L3 (composable with descriptions).

### Changes

- `niche.rs`: Added `CAPABILITY_GROUP_DESCRIPTIONS` constant — 12 domain descriptions mapping prefixes (inference, ai, capabilities, capability, identity, context, system, health, discovery, tool, lifecycle, graph) to human-readable purpose strings
- `handlers_capability.rs`: `handle_capability_list` now includes `description` field on each capability group, drawn from `niche::CAPABILITY_GROUP_DESCRIPTIONS`
- Test: `capability_group_descriptions_cover_all_domains` ensures all unique domains have descriptions

### Wire Standard L3 Response Shape

```json
{
  "provided_capabilities": [
    {
      "type": "inference",
      "methods": ["inference.complete", "inference.embed", ...],
      "version": "0.1.0",
      "description": "AI model inference: completion, embedding, model registry, provider management"
    }
  ]
}
```

---

## Security Service ID Evolution

Eliminated all `format!("{}-security", primal_names::BEARDOG)` calls across the codebase.

### Constants Added

| Constant | Value | Usage |
|----------|-------|-------|
| `SECURITY_SERVICE_ID` | `"security-provider"` | Service registration, trust level checks |
| `SECURITY_PRIMARY_SERVICE_ID` | `"security-provider-primary"` | Capability requirements, auth requests |
| `BEARDOG_SECURITY_SERVICE_ID` | `"beardog-security"` | `#[deprecated]` backward compat |

### Files Changed (10 files)

- `security/providers/beardog.rs` — Constants defined; `get_capabilities` / `get_service_info` / `authenticate` / `audit_log` use constants
- `security/providers/mod.rs` — Re-exports `SECURITY_SERVICE_ID` public; test-only re-exports for `SECURITY_PRIMARY_SERVICE_ID` / `BEARDOG_SECURITY_SERVICE_ID`
- `security/client.rs` — Import path updated to use re-exported constant
- `security/mod.rs` — Feature key `supports_beardog` → `supports_security_provider`
- `config/validation.rs` — Error messages evolved to capability-agnostic
- `config/builder.rs` — `beardog_*` methods documented as legacy aliases
- `ecosystem/manager.rs` — Session prefix `beardog_session_` → `security_session_`
- `ecosystem/manager_tests.rs` — Assertions updated
- `ecosystem/mod_tests.rs` — Assertions updated
- `security/providers/tests.rs` — Expected values updated to capability constants

### BLAKE3 Crypto Context Strings

Preserved as cryptographic constants — renaming would break token derivation:
- `"ecoPrimals beardog auth-token v1"`
- `"ecoPrimals beardog encrypt v1"`
- `"ecoPrimals beardog sign v1"`

Doc comments added explaining these are cryptographic commitments, not naming references.

---

## Deep Debt Final Audit (Comprehensive)

### All Clear

| Check | Status |
|-------|--------|
| Tests | 7,160 passing / 0 failures |
| Clippy | 0 warnings (`-D warnings`, pedantic + nursery) |
| Formatting | `cargo fmt --all -- --check` clean |
| Advisories | `cargo deny check` clean |
| Production files >800L | 0 |
| Unsafe code | 0 (`unsafe_code = "forbid"`) |
| C/sys dependencies | 0 in default build |
| TODO/FIXME/HACK | 0 |
| `.unwrap()` in production | 0 |
| Mocks in production | 0 (all behind `#[cfg(test)]` or feature gates) |
| `async-trait` annotations | 0 |
| Hardcoded primal names | 0 in routing/discovery (crypto context strings documented) |
| `std::sync::Mutex` held across await | 0 |
| Double-conversion patterns | 0 |

### Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,160 |
| Coverage | 90.1% region / 89.6% line |
| `.rs` files | ~1,037 |
| Lines | ~336k |
| Crates | 22 |
| async-trait | 0 (was 228) |
| Pure Rust | 100% default features |

---

## Remaining Blocked Items (Upstream)

| Item | Blocked On | Status |
|------|------------|--------|
| Three-tier genetics adoption | `ecoPrimal >= 0.10.0` shipping `mito_beacon_from_env()` | Groundwork laid (annotations, BTSP session fields) |
| Content curation via BLAKE3 manifests | NestGate content-addressed storage API stability | Pure BLAKE3 in tree |
| Full Phase 3 cipher negotiation | BearDog server-side `btsp.negotiate` | NULL cipher per-spec |

---

## Quality Gates

```
cargo fmt --all -- --check       ✓
cargo clippy --workspace --all-targets --all-features -- -D warnings  ✓
cargo test --workspace           ✓ (7,160 / 0 / 0)
cargo deny check                 ✓ (advisories ok, bans ok, licenses ok, sources ok)
```

Copyright (C) 2026 ecoPrimals Contributors
