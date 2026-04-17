# petalTongue v1.6.7 — UUI Boundary Analysis Handoff

**Date:** April 17, 2026
**Scope:** GUI stack audit, owns-vs-leverages delineation, capability discovery unification

---

## Summary

petalTongue is the UUI (Universal User Interface) engine — pure Rust rendering
to any modality on any device. This sprint delineated what petalTongue owns
versus what it consumes from the ecosystem via `capability.call` / JSON-RPC
over UDS.

## Changes Made

### 1. Dead dependency cleanup
- **Removed `png`** from `petal-tongue-ui/Cargo.toml` — zero usage in source
- **Removed direct `winit`** — never imported; comes transitively via eframe.
  Screen dimensions use `terminal_size` (pure Rust).

### 2. Unified capability discovery pattern
- **`GpuComputeProvider`** (`petal-tongue-core`): now uses
  `CapabilityDiscovery<BiomeOsBackend>` as primary discovery path (queries
  biomeOS for `compute` domain). Env-var overrides and S139 manifest scan
  kept as escape hatches.
- **`physics_bridge`** (`petal-tongue-ipc`): `discover_compute_socket()` now
  queries biomeOS capability discovery first, falls back to env/filesystem.

### 3. Fixed V2 display backend
- **`DiscoveredDisplayBackendV2`** was broken: it used `TarpcClient.call_method`
  for `display.*` operations, but the tarpc whitelist didn't include them.
- **Fix:** Replaced tarpc transport with JSON-RPC 2.0 over UDS — the universal
  IPC protocol. Discovery still via `CapabilityDiscovery<BiomeOsBackend>`.
  The V2 backend now works end-to-end.

### 4. Audio Tier 1 wired
- **New `NetworkBackend`** (`petal-tongue-ui/src/audio/backends/network.rs`):
  discovers `audio` capability provider via biomeOS, delegates `audio.play`
  over JSON-RPC/UDS.
- Registered as Tier 1 (priority 10) in `AudioManager`. Falls back gracefully
  to software/silent tiers when no ecosystem provider exists.
- `AudioBackendImpl` enum extended with `Network` variant.

### 5. `discovered-display` feature gate wired
- `discovered_display.rs` and `discovered_display_v2.rs` now compile only
  when `discovered-display` feature is enabled.
- `DisplayBackendImpl` enum variants, `DisplayManager::init()` discovery
  block, and `DisplayBackend::is_available()` all properly gated.

### 6. Documentation updated
- `CONTEXT.md` updated with owns-vs-leverages boundary map.

## Owns vs Leverages Boundary

### petalTongue Owns (pure Rust, in-crate)
- egui, epaint, tiny-skia, crossterm, symphonia
- Grammar of Graphics, scene graph, animation, modality adapters
- IPC server (`visualization.*`, `interaction.*`, `capabilities.sensory.*`)

### petalTongue Leverages (ecosystem via `capability.call`)
| Domain | Provider | Status |
|--------|----------|--------|
| `display.*` | ToadStool | V1 working (JSON-RPC), V2 fixed (capability discovery + JSON-RPC) |
| `compute.*` / `math.*` | barraCuda via ToadStool | Unified to `CapabilityDiscovery` |
| `btsp.session.*` | BearDog | Working |
| `discovery.*` | Songbird + biomeOS | Working |
| TLS/HTTPS | Songbird | Design ready |
| `audio.play` | ToadStool / future | Tier 1 stub wired |
| `storage.*` | NestGate | Not wired |
| `ai.*` | Squirrel | Not wired |

## Test Results

All 6,120+ workspace tests passing (--all-features). Zero clippy warnings.
Verified both with and without `discovered-display` feature.

## Ecosystem Dependencies (other primal teams)

- **ToadStool**: wire `display.present` for production use; future `audio.play`
- **Songbird**: implement TLS relay for `LocalHttpClient` HTTPS delegation
- **NestGate**: expose `storage.put`/`storage.get`
- **barraCuda**: expand dispatch table (histogram, KDE, tessellation, projection)
