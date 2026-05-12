# Songbird v0.2.1 Wave 181 — Port Canonicalization & Hardcoded Elimination

**Date**: May 2, 2026
**Primal**: Songbird
**Wave**: 181
**Type**: Deep Debt — Port canonicalization, hardcoded elimination, capability evolution

---

## Summary

Comprehensive port canonicalization pass and hardcoded elimination across 10 files in 7 crates. Fixed a `discovery_port()` bug, harmonized conflicting tarpc port defaults, added 8 new canonical constants, and evolved remaining hardcoded IPs and primal-name serde aliases.

## What Changed

### New Constants (`songbird-types/defaults/ports.rs`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `DEFAULT_DISCOVERY_SERVICE_PORT` | 8081 | Discovery HTTP service |
| `DEFAULT_OBSERVABILITY_PORT` | 9090 | Prometheus metrics scrape |
| `DEFAULT_DASHBOARD_UI_PORT` | 3000 | Dashboard frontend dev-server |
| `DEFAULT_FEDERATION_COORDINATION_PORT` | 8082 | Federation coordination |
| `DEFAULT_TARPC_RPC_PORT` | 8091 | tarpc binary RPC transport |
| `DEFAULT_GAMING_BASE_PORT` | 6112 | StarCraft IPX / gaming base |
| `EPHEMERAL_BIND_ADDR` | "127.0.0.1:0" | Port-0 ephemeral allocation |

### Bug Fix: `discovery_port()`

`songbird-config/defaults/ports.rs::discovery_port()` was falling back to `canonical::DEFAULT_METRICS_PORT` (the metrics constant, wrong domain) instead of a proper discovery port constant. Now uses `DEFAULT_DISCOVERY_SERVICE_PORT`.

### Tarpc Port Harmonization

Three conflicting defaults existed:
- `DEFAULT_TARPC_PORT = 8001` (types constant)
- `TarpcConfig::default()` → `SafeEnv::get_port(_, 8081)` (orchestrator)
- `tarpc_port()` → `8091` (config function)
- `protocol_api.rs` → local const `"8091"` (orchestrator)

Harmonized: all now use `songbird_config::defaults::ports::tarpc_port()` → `DEFAULT_TARPC_RPC_PORT` (8091).

### Hardcoded IPs Evolved

| File | Before | After |
|------|--------|-------|
| `memory_optimized.rs` | `"localhost"`, `"127.0.0.1"`, `"::1"` literals | `is_loopback_host()` + `LOCALHOST` |
| `capability_port_config.rs` | `"127.0.0.1:0"` | `EPHEMERAL_BIND_ADDR` |
| `compute-bridge/types.rs` | `"0.0.0.0"`, `"9000"` | `PRODUCTION_BIND_ADDRESS`, `DEFAULT_COMPUTE_PORT` |
| `cli/tower.rs` | `"8080"`, `"0.0.0.0"` | `DEFAULT_ORCHESTRATOR_PORT`, `PRODUCTION_BIND_ADDRESS` |

### Duplicate mDNS Constant

`cli/commands/quick/discovery.rs` had a local `const MDNS_MULTICAST_ADDR: &str = "224.0.0.251:5353"` duplicating `songbird_types::constants::{MDNS_MULTICAST_GROUP, MDNS_PORT}`. Replaced with a function deriving from canonical sources.

### Capability-Based Serde Alias

`tokens.rs::TokenType::SecurityProvider` had `#[serde(alias = "BearDog")]` only. Added `alias = "security_provider"` as the capability-based canonical name; `"BearDog"` retained for backward compat.

### SafeEnv::get_port() Cleanup

6 scattered `SafeEnv::get_port("ENV_VAR", magic_number)` calls replaced with canonical port functions from `songbird_config::defaults::ports`.

## Files Modified

- `crates/songbird-types/src/defaults/ports.rs` — 8 new constants
- `crates/songbird-types/src/memory_optimized.rs` — IP canonicalization
- `crates/songbird-config/src/defaults/ports.rs` — 6 functions wired to constants
- `crates/songbird-config/src/unified/core.rs` — metrics port
- `crates/songbird-config/src/config/constants/network_extras.rs` — discovery port
- `crates/songbird-config/src/capability_port_config.rs` — ephemeral bind
- `crates/songbird-orchestrator/src/rpc/tarpc_server/mod.rs` — tarpc config
- `crates/songbird-orchestrator/src/rpc/tarpc_server/dispatch.rs` — protocol lists
- `crates/songbird-orchestrator/src/server/protocol_api.rs` — tarpc port
- `crates/songbird-orchestrator/src/access_control/tokens.rs` — serde alias
- `crates/songbird-universal/src/adapters/security.rs` — security port
- `crates/songbird-universal/src/adapters/security_adapter_tests.rs` — test fix
- `crates/songbird-compute-bridge/Cargo.toml` — songbird-types dep
- `crates/songbird-compute-bridge/src/service/types.rs` — clap defaults
- `crates/songbird-compute-bridge/src/service/mod.rs` — clippy fix
- `crates/songbird-cli/src/cli/commands/tower.rs` — clap defaults
- `crates/songbird-cli/src/cli/commands/quick/discovery.rs` — mDNS + discovery port

## Quality Gates

- **cargo check**: Clean (0 errors, 0 warnings)
- **cargo clippy --workspace --lib --bins -- -D warnings**: Clean (0 warnings)
- **cargo fmt --check**: Clean
- **Tests**: 7,803 lib tests pass, 0 failures, 22 ignored
