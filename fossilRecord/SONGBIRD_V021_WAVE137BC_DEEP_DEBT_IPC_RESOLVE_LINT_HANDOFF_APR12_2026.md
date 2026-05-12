# Songbird v0.2.1 — Wave 137b+c Handoff

**Date**: April 12, 2026  
**Primal**: Songbird  
**Waves**: 137b (LD-02 `ipc.resolve` capability param, SB-02 documentation) + 137c (deep debt sweep)  
**Commits**: `db7a5103` (137b), `d440a80d` (137c)

---

## Wave 137b — LD-02 Resolution + SB-02 Documentation

### ipc.resolve Dual-Mode (LD-02 Resolved)

Springs previously needed to know primal names to call `ipc.resolve`. Now `ResolveParams` accepts either:

- `primal_id` — identity lookup (original behavior)
- `capability` — capability-based routing (new; takes precedence when both provided)

**Files changed**: `songbird-universal-ipc/src/service_types.rs`, `songbird-universal-ipc/src/service/ipc_registry.rs`, `songbird-universal-ipc/src/introspection/rpc.rs`, `songbird-universal-ipc/src/service/service_tests.rs`

### SB-02 Ring Lockfile Ghost — Documented

`ring` appears in `Cargo.lock` as an unactivated optional dependency of `rustls`/`rustls-webpki`. It is NOT compiled in default builds. Documented in `deny.toml` with explicit comment. Invalid `RUSTSEC-2024-0320` advisory removed.

---

## Wave 137c — Deep Debt Sweep

### Stale Feature Flags Removed (5)

| Crate | Feature Removed |
|-------|----------------|
| `songbird-types` | `unsafe-reference` |
| `songbird-canonical` | `compile_time_validation` |
| `songbird-genesis` | `nfc` |
| `songbird-nfc` | `platform-android`, `platform-ios`, `platform-linux` |
| `songbird-universal-ipc` | `nestgate` (cfg guards → `storage_provider` only) |

### Unreachable cfg Gates Fixed

`kubernetes` and `consul` feature flags declared in `songbird-discovery/Cargo.toml` — previously `#[cfg(feature = "kubernetes")]` and `#[cfg(feature = "consul")]` code blocks were unreachable.

### Hardcoded Literals → Constants

All remaining production hardcoded IP/host strings evolved:

| Literal | Constant | Files |
|---------|----------|-------|
| `"0.0.0.0"` | `PRODUCTION_BIND_ADDRESS` | CLI tower, config, UDP peer connector |
| `"127.0.0.1"` | `DEVELOPMENT_BIND_ADDRESS` | config bind_and_ports, IPC connection |
| `"localhost"` | `LOCALHOST` | config advanced (Consul/Docker), BTSP provider |

### Port Constants Fully Canonical

- 9 legacy constants in `songbird-types::constants` deprecated with `#[deprecated(note = "use songbird_types::defaults::ports::*")]`
- New canonical constants: `DEFAULT_ORCHESTRATOR_PORT`, `DEFAULT_HEALTH_PORT`, `DEFAULT_CRYPTO_TRANSPORT_PORT`, `DEFAULT_FEDERATION_BIND_PORT`
- All active call sites migrated: TLS crypto, federation config, orchestrator metrics, AI workload classification, config advanced

### Lint Hygiene

- All bare `#[allow()]` in test files given `reason = "..."` strings (circuit breaker, unibin e2e, error handling, port fallback, AI provider, common helpers)
- TLS integration tests and record layer `#[allow()]` given reason strings
- Clippy `single_match` in UDP peer connector refactored to `if let`
- Legacy `beardog.sock` fallback in tor handler emits `tracing::warn!`

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | 0 errors, 0 warnings |
| `cargo clippy --workspace -D warnings` | 0 warnings |
| `cargo fmt --check` | Clean |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace --lib` | 7,291 passed, 0 failed, 22 ignored |

---

## Ecosystem Impact

- **Springs**: Can now call `ipc.resolve` with `{"capability": "storage.get"}` instead of needing to know primal names — capability-first resolution across the mesh
- **Tower Composition**: Songbird remains fully composable; no blocking debt
- **musl-static**: `ring` is NOT compiled in default builds; pure Rust ecoBin compliance maintained
- **Downstream**: All primalSpring audit items (LD-02, SB-02, SB-03, E0308 test mismatches) resolved or documented
