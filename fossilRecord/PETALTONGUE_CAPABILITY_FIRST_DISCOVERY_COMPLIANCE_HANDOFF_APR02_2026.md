# petalTongue — Capability-First Discovery Compliance

**Date**: April 2, 2026
**Phase**: Capability-first discovery refactoring (primalSpring audit compliance)
**Previous**: `PETALTONGUE_SENSORY_MATRIX_HANDOFF_APR02_2026.md`

---

## Summary

Refactored all cross-primal connections in petalTongue from hardcoded primal
identity to capability-first discovery. Production routing code no longer
references specific primals by name — it discovers services through biomeOS
Neural API by capability. The `primal_names` module remains for logging context
only; it never appears in routing or socket resolution code paths.

This addresses all violations identified in the primalSpring downstream audit.

---

## Changes

### socket_roles Fix

| Before | After |
|--------|-------|
| `socket_roles::PHYSICS_COMPUTE = "barracuda"` | `socket_roles::PHYSICS_COMPUTE = "physics-compute"` |

Socket roles now contain capability names, never primal names.

### Discovery Service Client (was SongbirdClient)

| Before | After |
|--------|-------|
| `SongbirdClient` | `DiscoveryServiceClient` |
| `SongbirdVisualizationProvider` | `DiscoveryServiceProvider` |
| `songbird_client.rs` | `discovery_service_client.rs` |
| `songbird_provider.rs` | `discovery_service_provider.rs` |
| `SONGBIRD_CONNECT_TIMEOUT` | `DISCOVERY_SERVICE_CONNECT_TIMEOUT` |
| `SONGBIRD_WRITE_TIMEOUT` | `DISCOVERY_SERVICE_WRITE_TIMEOUT` |
| `SONGBIRD_READ_TIMEOUT` | `DISCOVERY_SERVICE_READ_TIMEOUT` |

### Registration Client (was SongbirdClient in IPC)

| Before | After |
|--------|-------|
| `SongbirdClient` (primal_registration.rs) | `RegistrationClient` |
| `PrimalRegistrationError::SongbirdError` | `PrimalRegistrationError::RegistrationRejected` |

### GPU Compute Provider (was ToadstoolCompute)

| Before | After |
|--------|-------|
| `ToadstoolCompute` | `GpuComputeProvider` |
| `ToadstoolServiceInfo` | `ComputeServiceInfo` |
| `discover_toadstool()` | `discover_compute_provider()` |
| `toadstool_compute.rs` | `gpu_compute_provider.rs` |

### Display Backends (was ToadstoolDisplay)

| Before | After |
|--------|-------|
| `ToadstoolDisplay` (v1) | `DiscoveredDisplayBackend` |
| `ToadstoolDisplay` (v2) | `DiscoveredDisplayBackendV2` |
| `BackendPriority::Toadstool` | `BackendPriority::DiscoveredDisplay` |
| `BackendChoice::Toadstool` | `BackendChoice::DiscoveredDisplay` |
| `BackendError::ToadstoolNotAvailable` | `BackendError::DisplayBackendNotAvailable` |
| `BackendError::ToadstoolRequiresBiomeOs` | `BackendError::DisplayBackendRequiresBiomeOs` |
| `DisplayError::NoDisplaysFromToadstool` | `DisplayError::NoDisplaysFromBackend` |

### Audio Provider (was ToadstoolAudioProvider)

| Before | After |
|--------|-------|
| `ToadstoolAudioProvider` | `DiscoveredAudioProvider` |
| `build_toadstool_play_url()` | `build_audio_play_url()` |
| `build_toadstool_stop_url()` | `build_audio_stop_url()` |
| `build_toadstool_synthesize_url()` | `build_audio_synthesize_url()` |
| `TOADSTOOL_URL` env (sole) | `AUDIO_PROVIDER_URL` then `TOADSTOOL_URL` (legacy alias) |

### Physics Bridge (Compute Dispatch)

| Before | After |
|--------|-------|
| `"barracuda.compute.dispatch"` method | `"compute.dispatch"` method |
| `BARRACUDA_SOCKET` env (sole) | `COMPUTE_SOCKET` then `BARRACUDA_SOCKET` (legacy alias) |

### Constants

| Before | After |
|--------|-------|
| `DEFAULT_TOADSTOOL_PORT` | `DEFAULT_DISPLAY_BACKEND_PORT` |
| `toadstool_port()` | `display_backend_port()` (reads `DISPLAY_BACKEND_PORT` then `TOADSTOOL_PORT`) |

---

## Pattern Applied

All cross-primal connections now follow the toadstool_v2.rs pattern:

```
BiomeOsBackend::from_env()
  → CapabilityDiscovery::new(Box::new(backend))
  → discover_one(&CapabilityQuery::new("capability-name"))
```

petalTongue never knows which primal provides a capability. It discovers by
capability string, connects to whatever endpoint biomeOS returns.

---

## Legacy Env Var Aliases (Backward Compatibility)

| New Env Var | Legacy Alias | Notes |
|-------------|-------------|-------|
| `COMPUTE_SOCKET` | `BARRACUDA_SOCKET` | Remove after one release cycle |
| `AUDIO_PROVIDER_URL` | `TOADSTOOL_URL` | Remove after one release cycle |
| `DISPLAY_BACKEND_PORT` | `TOADSTOOL_PORT` | Remove after one release cycle |
| `DISCOVERY_SERVICE_SOCKET` | `SONGBIRD_SOCKET` | Already existed as alias |

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-features -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | 6,090 passing (0 failures) |

---

## Consumer Primal Impact

### primalSpring (Orchestration)
No breaking changes. All JSON-RPC methods are semantic (`compute.dispatch`,
`discovery.query`, etc.). The old `barracuda.compute.dispatch` method is retired.

### Ecosystem env var migration
Existing deployments using `BARRACUDA_SOCKET`, `TOADSTOOL_URL`, `TOADSTOOL_PORT`,
or `SONGBIRD_SOCKET` will continue to work via legacy aliases. New deployments
should use the capability-generic env vars.

---

## Files Changed

### Renamed
- `crates/petal-tongue-core/src/toadstool_compute.rs` → `gpu_compute_provider.rs`
- `crates/petal-tongue-discovery/src/songbird_client.rs` → `discovery_service_client.rs`
- `crates/petal-tongue-discovery/src/songbird_provider.rs` → `discovery_service_provider.rs`

### Modified (production)
- `crates/petal-tongue-core/src/capability_names.rs` (socket_roles fix)
- `crates/petal-tongue-core/src/constants.rs` (port/timeout renames)
- `crates/petal-tongue-core/src/lib.rs` (re-exports)
- `crates/petal-tongue-discovery/src/lib.rs` (module + re-export renames)
- `crates/petal-tongue-ipc/src/physics_bridge.rs` (method + socket renames)
- `crates/petal-tongue-ipc/src/primal_registration.rs` (struct + doc renames)
- `crates/petal-tongue-ipc/src/primal_registration_error.rs` (variant rename)
- `crates/petal-tongue-ipc/src/tarpc_types/mod.rs` (constant rename)
- `crates/petal-tongue-ui/src/audio_providers/toadstool.rs` (type + fn renames)
- `crates/petal-tongue-ui/src/audio_providers/mod.rs` (re-export)
- `crates/petal-tongue-ui/src/backend/mod.rs` (BackendChoice + error renames)
- `crates/petal-tongue-ui/src/display/backends/toadstool.rs` (type rename)
- `crates/petal-tongue-ui/src/display/backends/toadstool_v2.rs` (type rename)
- `crates/petal-tongue-ui/src/display/mod.rs` (re-exports)
- `crates/petal-tongue-ui/src/display/manager.rs` (type + priority renames)
- `crates/petal-tongue-ui/src/display/traits.rs` (BackendPriority rename)
- `crates/petal-tongue-ui/src/error.rs` (error variant renames)
- `crates/petal-tongue-ui/src/app_panels/builders.rs` (env var)

### Modified (tests/docs)
- `crates/petal-tongue-discovery/tests/songbird_integration_test.rs`
- `crates/petal-tongue-discovery/tests/chaos_and_fault_tests.rs`
- `crates/petal-tongue-ui/Cargo.toml` (comment)
- `crates/petal-tongue-tui/README.md` (example)
