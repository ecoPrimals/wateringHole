# petalTongue v1.6.6 — PG-48 Wayland Fix + Motor P0 Rendering

**Date**: April 30, 2026  
**Scope**: PG-48 musl binary rendering (Wayland), Motor P0 panel/notification egui rendering  
**Tests**: 6,054+ passing (98 suites), 0 failures, 0 Clippy warnings

---

## 1. PG-48: musl Binary Live Mode Panic (Wayland)

**Problem**: plasmidBin musl-static binary panics with "Initializing the event
loop outside of the main thread" when starting `live` mode. The existing fix
(`native_options_with_any_thread`) only applied `with_any_thread(true)` via
the X11 extension trait. On Wayland systems the fix was inert.

**Root cause**: musl libc reports thread IDs differently from glibc, causing
winit's `is_main_thread()` check to fail even on the actual main thread.
The `with_any_thread(true)` call skips this check, but it must be applied
for both X11 and Wayland backends.

**Fix**:
- `src/ui_mode.rs`: `native_options_with_any_thread` now calls both
  `EventLoopBuilderExtX11::with_any_thread` and
  `EventLoopBuilderExtWayland::with_any_thread` using fully-qualified syntax
  (avoids ambiguity when both traits are in scope)
- `crates/petal-tongue-ui/src/backend/eframe.rs`: `EguiBackend::run()` also
  applies the same fix (was missing entirely)
- `crates/petal-tongue-ui/Cargo.toml`: `winit = { workspace = true }` added
  as direct dependency for platform extension traits

**Files changed**: `src/ui_mode.rs`, `crates/petal-tongue-ui/src/backend/eframe.rs`,
`crates/petal-tongue-ui/Cargo.toml`

**Note**: `visualization.render.scene` itself does NOT touch winit — it only
stores scene data in `VisualizationState`. The panic occurs at `live` mode
startup when `eframe::run_native` creates the event loop. Once the binary
can start, IPC scene rendering works normally.

---

## 2. Motor P0: Panel Content + Notification Rendering

**Problem**: `motor.panel.update` and `motor.notification` IPC commands were
received and stored in `PanelContentStore` and `NotificationQueue` (Phase 56
wiring), but the data was never rendered in the egui UI. Compositions sent
panel updates that were acknowledged on the wire but invisible to the user.

**Fix** — `crates/petal-tongue-ui/src/app/panels.rs`:

### Composition Panels
When `PanelContentStore` has entries, a floating "Composition Panels" egui
window renders all pushed content:
- Each panel entry shows its title (or panel key as fallback)
- JSON content is rendered recursively: objects as collapsible sections,
  arrays as indexed lists, leaves as key:value pairs
- Depth limited to 4 levels for performance

### Notification Toasts
`NotificationQueue` entries render as floating toast overlays:
- Up to 5 toasts visible simultaneously
- Centered horizontally at top of screen
- Color-coded by level: info (blue), warn (amber), error (red), success (green)
- `drain_expired()` called each frame to auto-dismiss timed notifications
- Sticky notifications (no `duration_ms`) persist until replaced

### Supporting changes
- `motor_state.rs`: removed module-level `#[allow(dead_code)]`, added
  `iter()` method to `PanelContentStore`, justified `#[expect]` on
  individual fields/methods still reserved for future use

**Usage**:
```bash
# Push panel content
echo '{"jsonrpc":"2.0","method":"motor.panel.update","params":{"panel":"dashboard","title":"Health","content":{"cpu":42,"mem":"3.2G"}},"id":1}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET

# Send auto-dismissing notification
echo '{"jsonrpc":"2.0","method":"motor.notification","params":{"level":"success","message":"Game saved","duration_ms":3000},"id":2}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET

# Send sticky error
echo '{"jsonrpc":"2.0","method":"motor.notification","params":{"level":"error","message":"Connection lost"},"id":3}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET
```

---

## Verification

- **Clippy**: 0 warnings (`--all-targets -- -D warnings`)
- **Tests**: 6,054+ passing (98 suites), 0 failures
- **Build**: Clean on all targets

---

## Remaining

- PG-48 binary needs reharvest to plasmidBin after this fix
- egui texture resolution (`TextureResolver` with `egui::Shape::image`) for
  scene graph `Primitive::Texture` display
- `PanelId::Custom` panels could auto-register in the panel system
- Toast dismiss-on-click interaction
