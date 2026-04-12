# Songbird v0.2.1 — Wave 138b Handoff: Hardcoded Literal Evolution to Canonical Constants

**Date**: April 12, 2026  
**Primal**: Songbird (Network Orchestration & Discovery)  
**Wave**: 138b  
**Scope**: Deep hardcoded literal elimination across config defaults, bind address logic, and service defaults

---

## Problem

Despite prior hardcoding evolution waves (131, 136, 137c), a systematic audit revealed **16 production files** still contained raw IP/port/hostname string literals in `Default` implementations and config constructors — `"0.0.0.0"`, `"127.0.0.1"`, `"localhost"`, port numbers like `8080`, `3000`. These bypassed the canonical constants in `songbird-types::constants` and `songbird-types::defaults::ports`, creating duplicate sources of truth.

## Solution

### New Constants
- `LOCALHOST_HOSTNAME` (`"localhost"`) added to `songbird-types::constants` — disambiguates from `LOCALHOST` (`"127.0.0.1"`) for service config defaults that use the hostname rather than the loopback IP
- `DEFAULT_DASHBOARD_PORT` (8003) added to `songbird-types::defaults::ports` — migrated from deprecated `constants.rs`

### Files Evolved (16 production, 1 test)

**songbird-orchestrator:**
- `core/api.rs` — `ApiConfig::default()` port/host → `DEFAULT_HTTP_PORT`/`DEVELOPMENT_BIND_ADDRESS`
- `bin_interface/doctor.rs` — port availability check → `DEVELOPMENT_BIND_ADDRESS`

**songbird-config:**
- `canonical/service.rs` — `ServiceConfig`/`ServiceInfo` defaults → `LOCALHOST_HOSTNAME`/`DEFAULT_HTTP_PORT`
- `canonical/observability.rs` — `DashboardConfig` → `PRODUCTION_BIND_ADDRESS`/`DEFAULT_DASHBOARD_PORT`
- `canonical/hardcoded_elimination.rs` — `HostConfig` (10 fields) → `LOCALHOST_HOSTNAME`; `from_env_reader` defaults → `LOCALHOST_HOSTNAME`
- `canonical/constants/ports_env.rs` — `get_bind_address_with()` production/development branches → constants
- `canonical/network/core.rs` — `from_env_reader()` bind defaults → `PRODUCTION_BIND_ADDRESS`
- `defaults/hosts.rs` — `default_host()`/`bind_address()` fallbacks → constants
- `defaults/hosts_evolved.rs` — environment-switched host → constants
- `defaults/ports_evolved.rs` — `TcpListener::bind` targets → `PRODUCTION_BIND_ADDRESS`
- `config/environment.rs` — TLS detection comparison → `PRODUCTION_BIND_ADDRESS`
- `discoverable_endpoint.rs` — probe patterns/dev fallback → `LOCALHOST_HOSTNAME`/`LOCALHOST`
- `discovery/runtime_engine/discover_consul.rs` — address fallback → `LOCALHOST`
- `port_discovery.rs` — `is_port_available()` → `PRODUCTION_BIND_ADDRESS`
- `unified/federation.rs` — `FederationNetworkConfig` bind default → `PRODUCTION_BIND_ADDRESS`
- `canonical/observability_tests.rs` — assertions updated to use constants

### New Tests (21)
- **ports_env** (17): bind address env logic (explicit, invalid IP, k8s, container, production env), port ranges (start, end, env override), dashboard port (dev/prod/override), discovery port (default/override), environment offsets (production, staging), user port offset determinism
- **hardcoded_elimination** (4): HostConfig constant validation, single env override, all-defaults, `with_defaults()` parity

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | 0 errors, 0 warnings |
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo doc --workspace --no-deps` | 0 warnings |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace --lib` | 7,319 passed, 0 failed, 22 ignored |

## Ecosystem Impact

- All bind address and hostname defaults now trace to a single source of truth in `songbird-types`
- Changing `PRODUCTION_BIND_ADDRESS`, `DEVELOPMENT_BIND_ADDRESS`, `LOCALHOST`, or `LOCALHOST_HOSTNAME` propagates consistently to all 16+ consuming files
- Port defaults use the canonical `defaults::ports` module exclusively
- No remaining raw IP/port/hostname string literals in production `Default` implementations

## Remaining Debt (unchanged from Wave 138)

- BTSP Phase 3 (cipher negotiation, encrypted framing)
- Tor/TLS paths blocked on live security provider
- Storage validation needs live `storage.*` provider
- Coverage 72.29% vs 90% target
- ~109 `#[async_trait]` usages (require `dyn Trait` dispatch; no mechanical migration possible)
