# petalTongue Deep Debt + Evolution Phase 5 Handoff

**Date**: April 3, 2026
**Previous**: `PETALTONGUE_WAVE99_CAPABILITY_COMPLIANCE_HANDOFF_APR03_2026.md`
**Commit**: `aff8559`

---

## Summary

Comprehensive deep debt elimination and modern Rust evolution pass. Focus areas:
production isolation of test fixtures, stub completions, timeout unification,
dead code cleanup, and smart refactoring of the 5 largest files. Net result:
**-1,985 lines** across 48 files, 14 new submodule files.

---

## Changes

### 1. Production Isolation — Test Fixtures

| Before | After |
|--------|-------|
| `petal-tongue-ui-core` unconditionally enables `test-fixtures` on `petal-tongue-core` | `test-fixtures` in `[dev-dependencies]` only; added opt-in feature |
| Discovery `cache` module compiled in production (only used by tests) | `#[cfg(test)] mod cache` |
| `mdns_discovery` wrappers compiled in production | Demoted to test module |
| `metrics_dashboard_helpers` test-only helpers in production | Gated to `#[cfg(test)]` |
| `health_status_display` in production primal_details | Moved to test module |
| `unix_socket_server` JSON-RPC shims in production | Moved to `#[cfg(test)] impl` block |

### 2. Stub Completions

| Stub | Before | After |
|------|--------|-------|
| `proc_available()` | Hardcoded `false` | Checks `/proc/stat` existence + read access |
| `query_x11_dimensions_legacy()` | Dead code with `#[expect]` | **Removed** (winit replacement working) |
| `ScreenSensor` fields | Dead code | `width()` / `height()` accessors added |
| `WebSocketConnection` | Reserved future fields | Exponential backoff reconnect (1s→60s cap) |
| `spring_adapter` schema field | Dead code | Validated in `adapt_eco_timeseries()` |

### 3. Timeout Unification

| File | Before | After |
|------|--------|-------|
| `biomeos_client.rs` | Inline `Duration::from_secs(30/10/90)` | `discovery_timeouts::HTTP_TIMEOUT` etc. |
| `audio_providers/toadstool.rs` | Inline `Duration::from_secs(30)` | `discovery_timeouts::HTTP_TIMEOUT` |
| `primal_registration.rs` | Inline `Duration::from_millis(100)` | `DISCOVERY_SERVICE_REGISTRATION_PROBE_TIMEOUT` |
| `awakening_coordinator` | Inline `Duration::from_millis(16)` | `FRAME_PACING_60FPS` constant |

### 4. Smart File Refactoring

| File | Lines | Split into |
|------|-------|-----------|
| `scene_bridge/paint.rs` | 828 | `paint/{mod,color,geometry,primitives}.rs` |
| `graph_editor/graph.rs` | 819 | `graph/{mod,validation,serialization,tests}.rs` |
| `discovery_service_client.rs` | 819 | `{mod,protocol,methods,tests}.rs` |
| `app/init.rs` | 814 | `init.rs` + `{panel_init,provider_init,scenario_init}.rs` |
| `device_panel.rs` | 799 | `device_panel/{mod,list_view,detail_view}.rs` |

All splits follow logical concern boundaries. Public APIs maintained via `pub use` re-exports.

### 5. Dead Code Cleanup

| Item | Action |
|------|--------|
| `dns_parser::RecordClass` enum | **Removed** (unused) |
| `dns_parser` AAAA records | **Wired** into response handling (IPv6 support) |
| `dns_parser` header fields | **Wired** into tracing |
| `graph_canvas::world_to_screen` | **Removed** (duplicate of `layout::world_to_screen`) |
| `MetricDisplayState::neural_api_connected` | **Removed** (always true, unused in UI) |

### 6. Version Alignment

| Crate | Before | After |
|-------|--------|-------|
| `petal-tongue-discovery` | `0.1.0` | `1.6.6` |
| `petal-tongue-adapters` | `0.1.0` | `1.6.6` |
| `petal-tongue-entropy` | `0.1.0` | `1.6.6` |
| `petal-tongue-tui` | `0.1.0` | `1.6.6` |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | **6,079 passing**, 0 failures |

---

## Remaining Debt (Low Priority)

- `audio/backends/direct.rs` and `socket.rs` remain stubs (ALSA/PipeWire paths — needs ecosystem backend)
- `audio_providers/toadstool.rs::request_synthesis` reserved for parametric synthesis API
- `biomeos_integration/events.rs::on_connection_lost` reserved for WebSocket client
- Several files in 600-800 line range could benefit from future refactoring
- `rand` 0.8 → 0.9 migration deferred (documented breakage)

## Unsafe Code

Zero `unsafe` blocks in all first-party crate sources. Most crates enforce `#![forbid(unsafe_code)]`.
