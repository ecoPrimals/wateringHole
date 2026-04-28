<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Deep Debt: C Dep Elimination, Auth Security, Stub Evolution

**Date**: April 27, 2026
**Primal**: Squirrel (AI Coordination)

## Summary

Deep debt session addressing C dependency elimination, authentication security
hardening, production stub evolution, deprecated code removal, and capability-first
environment variable evolution.

## Changes

### C Dependency Elimination

- `zstd`, `flate2`, `lz4_flex` removed from workspace `[dependencies]` and `squirrel-mcp` `Cargo.toml`
- `compression` feature on `squirrel-mcp` is now empty (`compression = []`)
- `CompressionFormat` enum retained as metadata-only (no codec implementation exists)
- `zstd-sys`, `zstd-safe`, `zstd`, `flate2`, `lz4_flex` all eliminated from `Cargo.lock`
- `--all-features` builds are now 100% pure Rust (no C build tooling required)

### Authentication Security Hardening

- `DefaultIdentityManager::authenticate` evolved from accept-any-password stub to explicit rejection
- Known users now receive `MCPError::Authentication` with message directing to security capability provider
- Unknown users still receive `Ok(None)` (no identity found)
- `SecurityManagerImpl` tests updated to expect authentication failure for known users

### Deprecated Code Removal

- `AuthError::BeardogUnavailable(String)` — removed (zero callers)
- `AuthError::BeardogError(String)` — removed (zero callers)
- `AuthError::beardog_error()` constructor — removed
- Capability-based equivalents `CapabilityProviderUnavailable` / `CapabilityProviderError` remain

### Ecosystem Coordination Stub Evolution

- `register_with_ecosystem`: now checks socket existence, logs honest status ("sovereign mode" vs "socket exists")
- `discover_via_service_mesh`: clarified log message (no more "not yet implemented")
- `probe_primal_endpoint`: checks socket existence before returning error

### Capability-First Environment Variables

- `ECOSYSTEM_ORCHESTRATOR_SOCKET` → `BIOMEOS_SOCKET` fallback in `find_biomeos_socket()`
- `API_VERSION` constant: `"biomeOS/v1"` → `"ecosystem/v1"`
- `capability_registry.toml`: `lifecycle.biomeos` → `lifecycle.ecosystem`

## Verification

- `cargo fmt` — clean
- `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` — 0 warnings
- `cargo test --workspace` — **7,182** tests, 0 failures
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok
- `Cargo.lock` verified: zero `zstd`/`flate2`/`lz4_flex` entries
