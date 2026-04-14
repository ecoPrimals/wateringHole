# biomeOS v3.15 — Pure Rust YAML & Deep Debt Evolution

**Date**: April 14, 2026
**Scope**: Deep debt cleanup — last C dependency elimination, dead code evolution, agnostic naming
**Validation**: `cargo build` + `cargo clippy --workspace` (0 new warnings) + `cargo test --workspace` (all pass)

## Changes

### 1. Zero C Dependencies — `serde_yaml_ng` → `serde-saphyr`

`unsafe-libyaml` (C libyaml binding via `serde_yaml_ng`) was the only remaining C library
dependency in the biomeOS binary. Replaced with `serde-saphyr` 0.0.23, a pure Rust YAML 1.2
parser/serializer.

- Workspace dep: `serde_yaml = { package = "serde-saphyr", version = "0.0.23" }`
- `serde_yaml::Value` usages (2 sites) evolved to `serde_json::Value`
- `unsafe-libyaml` added to `deny.toml` ban list
- **biomeOS now ships zero C library dependencies**

### 2. Dead Code Evolution

| Item | Before | After |
|------|--------|-------|
| `AiGraphAdvisor::local_patterns` | `#[expect(dead_code)]` | Wired into `get_local_suggestions` — pattern-driven fallback |
| `LocalPattern` struct | `#[expect(dead_code)]` | Active — `name`, `description`, `confidence` flow into detection |
| `AISuggestionManager::family_id` | `#[expect(dead_code)]` | Used in request logging for family-scoped AI context |
| `live_discovery.rs` module | Blanket `#![expect(dead_code)]` | Annotation refined — fully implemented, awaiting REST route wiring |

### 3. Capability-Agnostic Naming

| Before | After | File |
|--------|-------|------|
| `subfederation/beardog.rs` | `subfederation/security.rs` | biomeos-federation |
| `SongbirdServiceInfo` | `DiscoveredServiceInfo` | nucleus/discovery.rs |
| `SongbirdDiscoveryResponse` | `DiscoveryResponse` | nucleus/discovery.rs |

### 4. Silent Catch-All Evolution

Three production `_ => {}` arms replaced with trace/debug logging:
- Config feature match → `debug!("ignoring unknown feature flag: {other:?}")`
- Lifecycle monitoring → `trace!("{name} healthy in state {other:?}")`
- Suggestion feedback → `debug!("Suggestion ... feedback {:?} — kept active")`

## Validation

- `cargo build` — clean
- `cargo clippy --workspace` — 0 new warnings (pre-existing `biomeos-deploy` large-err only)
- `cargo test --workspace` — all pass (1800+ tests)
- `cargo tree | grep unsafe-libyaml` — no matches (C dep eliminated)

## Files Modified

- `Cargo.toml` (workspace dep)
- `deny.toml` (ban unsafe-libyaml)
- `crates/biomeos-types/src/manifest/storage/config.rs`
- `crates/biomeos-types/src/manifest/storage_tests.rs`
- `crates/biomeos-niche/src/error.rs`
- `crates/biomeos-federation/src/modules/manifest.rs`
- `crates/biomeos-chimera/src/error.rs`
- `crates/biomeos-graph/src/ai_advisor.rs`
- `crates/biomeos-graph/src/ai_advisor_local.rs`
- `crates/biomeos-graph/src/ai_advisor_tests.rs`
- `crates/biomeos-ui/src/suggestions/manager.rs`
- `crates/biomeos-api/src/handlers/live_discovery.rs`
- `crates/biomeos-federation/src/subfederation/mod.rs`
- `crates/biomeos-federation/src/subfederation/security.rs` (renamed from beardog.rs)
- `crates/biomeos-federation/src/subfederation/manager.rs`
- `crates/biomeos-federation/src/nucleus/discovery.rs`
- `crates/biomeos-core/src/config/mod.rs`
- `crates/biomeos-atomic-deploy/src/lifecycle_manager/monitoring.rs`
- Root docs: CHANGELOG.md, README.md, CURRENT_STATUS.md, DOCUMENTATION.md, QUICK_START.md, START_HERE.md
