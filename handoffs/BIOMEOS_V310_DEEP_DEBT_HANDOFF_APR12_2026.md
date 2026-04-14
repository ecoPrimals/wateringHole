# biomeOS v3.10 — Deep Debt: Smart Refactoring & Capability-Based Evolution

**Date**: 2026-04-12
**Author**: biomeOS team
**Scope**: 5 files >800L smart-refactored, hardcoding evolved to capability-based, dependency evolution, idiomatic Rust
**Preceded by**: v3.09 (5 NUCLEUS forwarding gaps)

## Smart File Refactoring (5 files >800L → resolved)

| File | Before | After | Strategy |
|------|--------|-------|----------|
| `btsp_client.rs` | 887L | 701L | Tests extracted to `btsp_client_tests.rs` |
| `topology.rs` | 813L | 487L | Tests extracted to `topology_tests.rs` (merged with existing coverage) |
| `capability.rs` | 844L | 782L | Heuristic helpers → `capability_heuristics.rs` |
| `manifest/storage.rs` | 828L | split | Directory module: `volume.rs`, `secret.rs`, `config.rs` |
| `manifest/networking_services.rs` | 812L | split | Directory module: `dns_ipam.rs`, `mesh.rs`, `routing.rs`, `traffic.rs` |

## Hardcoding → Capability-Based Evolution

### Security provider socket resolution
- `beardog_socket_path()` → `security_provider_socket_path()`
- Resolves via `BIOMEOS_SECURITY_SOCKET` → `BEARDOG_SOCKET` (legacy) → `{BIOMEOS_SECURITY_PROVIDER}-{fid}.sock`
- No hardcoded primal name in socket lookup logic
- Legacy `beardog_socket_path()` retained as deprecated alias

### BTSP error types
- `BearDogError(String)` → `SecurityProviderError(String)`
- Display messages updated to "security provider" (primal-agnostic)
- Internal RPC helpers renamed: `create_session_via_security_provider`, `verify_session_via_security_provider`

### Lifecycle subsystem detection
- `probe_songbird_mesh()` → `probe_mesh_provider(provider)` with `BIOMEOS_NETWORK_PROVIDER` env resolution
- Tower/node/nest/mesh primals resolved from env with canonical fallbacks:
  - `BIOMEOS_SECURITY_PROVIDER` (tower security)
  - `BIOMEOS_NETWORK_PROVIDER` (tower network + mesh)
  - `BIOMEOS_COMPUTE_PROVIDER` (node)
  - `BIOMEOS_STORAGE_PROVIDER` (nest)

### HTTP client discovery
- `DISCOVERY_PROVIDER` now checks `BIOMEOS_NETWORK_PROVIDER`
- Socket resolution checks `BIOMEOS_DISCOVERY_SOCKET` before provider-scoped key

### Constants centralized
- Inline broadcast port `9199` → `network::DEFAULT_BROADCAST_DISCOVERY_PORT`
- New `timeouts::DEFAULT_IPC_TIMEOUT` (2 seconds) for local IPC probes

## Dependency Evolution

- `tools/Cargo.toml`: `reqwest` feature `rustls-tls` removed (eliminates ring C/asm dependency); local demo tools don't require TLS
- `biomeos-graph/Cargo.toml`: `criterion` dev-dependency aligned to `workspace = true` for version consistency

## Idiomatic Rust

- `modification.rs` `apply_batch()`: `.expect("successful modification always produces a graph")` → proper `match` with recoverable `ModificationResult::failure()` return

## Audit Summary (full codebase scan)

| Category | Status |
|----------|--------|
| Unsafe code | CLEAN — `#![forbid(unsafe_code)]` on all crate roots |
| TODO/FIXME/HACK/XXX | CLEAN — zero in production code |
| `unimplemented!()` / `todo!()` | CLEAN — zero in production code |
| Production mocks | CLEAN — only intentional graceful degradation |
| `.unwrap()` in production | CLEAN — confined to tests |
| Files >800L | RESOLVED — all 5 production files addressed |

## Validation

- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace --all-targets -- -D warnings`: PASS (0 warnings)
- `cargo test --workspace`: **7,784 passed, 0 failed**
