# petalTongue v2.0.0 -- Deep Debt Evolution Handoff

**Date**: March 8, 2026
**Scope**: Comprehensive audit, deep debt evolution, healthSpring absorption

---

## Summary

petalTongue underwent a full audit and deep debt evolution session:
- 1,300+ tests passing (0 failures)
- 16/17 crates have `#![forbid(unsafe_code)]`
- All files under 1,000 lines
- Zero hardcoded ports, paths, or primal names in production
- All production `unwrap()`/`expect()` evolved to proper error handling
- Clippy pedantic warnings reduced ~60%
- Entropy stubs evolved to real Shannon entropy implementations
- healthSpring DataChannel types, chart renderers, and clinical theme absorbed
- Root docs cleaned, stale session docs archived

---

## What Changed

### New Modules
- `petal-tongue-core/src/constants.rs` -- Centralized self-knowledge
- `petal-tongue-core/src/data_channel.rs` -- DataChannel + ClinicalRange (from healthSpring)
- `petal-tongue-graph/src/chart_renderer.rs` -- egui_plot chart rendering
- `petal-tongue-graph/src/clinical_theme.rs` -- Clinical color palette

### New Dependencies
- `egui_plot = "0.29"` (workspace)
- `bytes = "1"` with serde feature (workspace, for zero-copy IPC)

### Refactored Modules
- `app.rs` -> `app/mod.rs` + `app/init.rs` + `app/sensory.rs`
- `visual_2d.rs` -> `visual_2d/mod.rs` + `visual_2d/nodes.rs` + `visual_2d/interaction.rs`
- `form.rs` -> `form/mod.rs` + `form/field.rs` + `form/validation.rs`

### Key API Changes
- `InstanceRegistry` now has `load_from(&Path)` and `save_to(&Path)` for test isolation
- `SessionManager` now has `with_session_path(PathBuf)` constructor
- `RenderRequest`/`RenderResponse` buffers changed from `Vec<u8>` to `bytes::Bytes`
- `ProviderCache` now returns `Arc<T>` instead of cloning
- `prompt_for_display_server` is now `async`

---

## For Other Springs/Primals

### healthSpring
petalTongue now natively renders healthSpring diagnostic data via `DataChannel`:
- `TimeSeries`, `Distribution`, `Bar`, `Gauge` variants
- `ClinicalRange` for threshold annotations
- Clinical theme colors: HEALTHY (green), WARNING (yellow), CRITICAL (red)
- `NodeDetail` struct for full node panel rendering
- Test scenario: `sandbox/scenarios/healthspring-diagnostic.json`

### biomeOS
- Socket discovery uses `constants::BIOMEOS_SOCKET_NAME` ("biomeos-neural-api")
- WebSocket fallback uses `constants::DEFAULT_HEADLESS_PORT`
- Legacy path uses `constants::biomeos_legacy_socket()`

### ToadStool
- toadstool_v2 tarpc complete
- Socket paths use centralized constants
- Display backend discovery is capability-based

---

## Remaining Work

~58 valid TODOs, mostly Phase 2/3:
- ToadStool audio/display backend (external team)
- mDNS full packet building
- WebSocket biomeOS event subscription
- Canvas rendering with tiny-skia
- Video modality in entropy
- llvm-cov coverage analysis
