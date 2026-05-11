# biomeOS v3.52 — Content Capability Domain Routing to NestGate

**Date**: May 11, 2026
**Commit**: `116cda38`
**Tests**: 7,940 pass / 0 fail / 113 ignored
**Audit source**: primalSpring stadial gate blurb — all 13 primals (May 11, 2026)

---

## Issue

primalSpring promoted `content` to a first-class capability domain. biomeOS
had NestGate mapped only under `storage`, `versioning`, `persistence`, and
`data` — the `content` domain was completely missing. Calls to `content.get`,
`content.resolve`, etc. through biomeOS's composition routing would fail to
resolve a provider.

## Fix

Registered `content` as a canonical capability domain routing to NestGate
across all resolution layers:

### 1. CAPABILITY_DOMAINS (compiled-in fallback)

```rust
CapabilityDomain {
    provider: NESTGATE,
    capabilities: &["content", "content_addressed", "publishing"],
},
```

### 2. CapabilityTaxonomy (capability → primal resolution)

Added `"content"` and `"publishing"` as aliases for `ContentAddressed`,
which already maps to `NESTGATE` in `default_primal()`.

### 3. Translation Defaults (semantic routing)

Registered 8 `content.*` method translations for NestGate:

| Semantic method | Actual method |
|----------------|---------------|
| `content.put` | `content.put` |
| `content.get` | `content.get` |
| `content.exists` | `content.exists` |
| `content.list` | `content.list` |
| `content.publish` | `content.publish` |
| `content.resolve` | `content.resolve` |
| `content.promote` | `content.promote` |
| `content.collections` | `content.collections` |

### 4. capability_registry.toml (runtime config)

Added `[domains.content]` and `[translations.content]` sections.

### 5. composition.status Enhancement

`primal_health` entries now include a `capabilities` array so consumers
can see that NestGate provides both `storage` and `content` domains.

## Tests Added

| Test | Validates |
|------|-----------|
| `test_capability_to_provider_content_domain` | CAPABILITY_DOMAINS resolves content → nestgate |
| `test_resolve_capability_to_primal_content` | Taxonomy resolves "content" → nestgate |
| `test_resolve_capability_to_primal_content_addressed` | Taxonomy resolves "content_addressed" → nestgate |
| `test_semantic_fallback_content_get_routes_to_nestgate` | content.get routes through capability.call |
| `test_semantic_fallback_content_resolve_routes_to_nestgate` | content.resolve routes through capability.call |
| `test_content_routes_to_nestgate_with_registered_provider` | Full E2E with mock NestGate provider |

## biomeOS Audit Status

| Item | Status | Notes |
|------|--------|-------|
| Content routing | **RESOLVED** (v3.52) | All layers map content → NestGate |
| composition.status | **RESOLVED** (v3.52) | Now includes per-primal capabilities |
| composition.deploy | RESOLVED (v3.51) | Route alias for graph.execute |
| method.register | RESOLVED (v3.51) | GAP-09 spring method registration |
| BearDogVerifier | RESOLVED (v3.51) | JH-11 verify-then-forward |
| composition.status | RESOLVED (v3.51) | pappusCast adaptive daemons |

biomeOS is **structurally clean** per the stadial gate blurb. Remaining
work is validation-dependent on NestGate shipping transport parity for
`content.*` methods across all router paths.
