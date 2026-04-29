# petalTongue — Desktop Shell Evolution (Phase 56)

**From**: primalSpring v0.9.23 Phase 56
**To**: petalTongue team
**Date**: April 28, 2026
**Priority**: Evolution guidance for multi-surface desktop shell
**Specs**: `primalSpring/specs/LIVE_GUI_COMPOSITION_PATTERN.md`, `DESKTOP_SESSION_MODEL.md`

---

## Summary

petalTongue `live` mode is validated as the Desktop NUCLEUS visualization
surface (Phase 55c). The current implementation is a **single egui window**
with multi-session IPC support. Phase 56 evolves petalTongue into a
**multi-surface desktop shell** that hosts application sessions managed by
biomeOS.

---

## Bug Fix: Motor Channel in Live Mode (P0)

### Problem

In `live_mode.rs`, the IPC server's `motor_tx` sends motor commands to a
**logging-only background thread**, not to the `PetalTongueApp`'s actual
`motor_rx` that drives GUI updates via `drain_motor_commands`.

This means external `motor.*` RPC calls (e.g., `motor.panel.create`,
`motor.navigate`) are acknowledged on the wire but **never reach the GUI**.

### Fix

Pass the `PetalTongueApp`'s `motor_tx` into the IPC server via
`with_motor_sender()` instead of creating a separate channel. Remove the
logging-only receiver thread.

**Before:**
```
IPC server -> motor_tx(server) -> motor_rx(logging thread)  // dead end
App        -> motor_tx(app)    -> motor_rx(drain_motor_commands)  // GUI
```

**After:**
```
IPC server -> motor_tx(shared) -> motor_rx(drain_motor_commands)  // GUI
App internal -> same motor_tx  -> same motor_rx
```

### Validation

After this fix, the following should work:

```bash
echo '{"jsonrpc":"2.0","method":"motor.panel.create","params":{"id":"test","title":"Hello"},"id":1}' \
    | socat - UNIX-CONNECT:$SOCKET_DIR/petaltongue-{family}.sock
```

A new floating panel titled "Hello" should appear in the egui window.

---

## Ask 1: Session-Aware Rendering (P1)

### What

Today, IPC `VisualizationState.sessions` map session IDs to
`RenderSession` data, but all sessions render into panels within the
single window. The desktop model requires **session-aware rendering**
where each application session has its own rendering context.

### Implementation

1. `PetalTongueApp` maintains a `focused_session: Option<String>`
2. The central rendering area displays the focused session's scene graph
3. Non-focused sessions render as thumbnails in a session switcher panel
4. `motor.navigate` switches the focused session

### New IPC Methods

| Method | Effect |
|--------|--------|
| `visualization.session.create` | Create a new session, return session ID |
| `visualization.session.destroy` | Remove session and its render state |
| `visualization.session.focus` | Set which session renders in the main area |
| `visualization.session.list` | List all sessions with metadata |

---

## Ask 2: Desktop Shell Chrome (P1)

### What

petalTongue in desktop mode should render shell chrome — a status bar,
session switcher, and notification area — around the application content.

### Implementation

In `render_all_panels` (or a new `render_desktop_shell`):

1. **Top bar**: Composition health indicators (green/yellow/red per primal),
   clock, focused session name
2. **Session switcher**: Bottom or side panel showing running sessions as
   tabs/cards. Click to switch focus. Shows session name, app icon, state.
3. **Notification overlay**: Toast notifications from `motor.notification`
   commands, auto-dismiss after duration

### Data Source

Shell chrome pulls data from:
- `composition.health` via biomeOS (primal health status)
- `app.list` via biomeOS (running sessions)
- Internal `motor_rx` channel (notifications, navigation commands)

The shell polls biomeOS at 1Hz for status updates (not per-frame).

---

## Ask 3: Multi-Viewport Evolution (P2 — Phased)

petalTongue's CONTEXT.md documents the path:
`EguiPixelRenderer -> DisplayManager -> ecosystem display.* IPC`

The multi-surface evolution has three phases:

### Phase A: egui Multi-Viewport

Use egui's `ViewportBuilder` to create secondary native windows for
application sessions. Each session gets its own `ViewportId`.

```rust
// In PetalTongueApp::update()
if let Some(session) = self.sessions.get("ewebb-game") {
    ctx.show_viewport_deferred(
        ViewportId::from_hash_of("ewebb-game"),
        ViewportBuilder::default()
            .with_title(&session.title)
            .with_inner_size([1280.0, 720.0]),
        |ctx, _class| {
            session.render(ctx);
        },
    );
}
```

**Prerequisite**: `BackendCapabilities.multi_window = true` in the eframe
backend. This is already a field in `BackendCapabilities` — currently set
to `false`.

### Phase B: DisplayManager

Abstract the viewport management into a `DisplayManager` that maps
session IDs to display targets (viewports, panels, headless buffers):

```rust
pub trait DisplayManager {
    fn create_surface(&mut self, session_id: &str, config: SurfaceConfig) -> SurfaceId;
    fn destroy_surface(&mut self, surface: SurfaceId);
    fn present(&mut self, surface: SurfaceId, frame: &RenderedFrame);
    fn list_surfaces(&self) -> Vec<SurfaceInfo>;
}
```

### Phase C: ToadStool `display.*` IPC

Long-term: ToadStool owns GPU-backed display surfaces. petalTongue submits
render commands to ToadStool via `display.present`, and ToadStool handles
window lifecycle, compositing, and GPU presentation.

This decouples petalTongue from eframe — petalTongue becomes a scene
compiler and interaction handler, while ToadStool becomes the compositor.

---

## Ask 4: Sensor Event Broadcasting (P2)

### What

petalTongue should broadcast semantic `intent` events (not just raw input)
to the NUCLEUS for AI processing.

### Implementation

1. Detect interaction patterns in `collect_sensor_events()`:
   - Click on a dialogue option -> `intent.dialogue.choose`
   - Select a menu item -> `intent.menu.select`
   - Drag a file -> `intent.drag.file`
   - Type in a text field -> `intent.text.input`

2. Push intent events to the `SensorStreamRegistry` with session context

3. Consumers (Squirrel via biomeOS) call `interaction.sensor_stream.poll`
   to receive intent events

### Intent Event Schema

```json
{
  "type": "intent",
  "session": "ewebb-game-0",
  "action": "dialogue.choose",
  "context": {
    "npc": "innkeeper",
    "option_id": 2,
    "option_text": "Tell me about the mountains."
  },
  "timestamp": 1714340000000
}
```

---

## Ask 5: SSE Reconnection Robustness (P1)

### What

petalTongue's SSE client (for biomeOS ecosystem events) needs exponential
backoff reconnection and graceful degradation.

### Implementation

```rust
async fn sse_connection_loop(url: &str) {
    let mut backoff = Duration::from_secs(1);
    let max_backoff = Duration::from_secs(60);
    
    loop {
        match connect_sse(url).await {
            Ok(stream) => {
                backoff = Duration::from_secs(1);
                process_events(stream).await;
                // Stream ended — reconnect
            }
            Err(_) => {
                // Cache last-known state for offline rendering
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(max_backoff);
            }
        }
    }
}
```

When SSE is unavailable, fall back to polling `health.liveness` at the
backoff interval. Cache the last-known ecosystem state so the shell chrome
still renders (with stale indicators).

---

## Validation

primalSpring will validate these evolutions through:

- Motor channel fix: `desktop_nucleus.sh validate` + direct `motor.panel.create` test
- Session management: exp085 (agentic loop) with session create/focus/destroy
- Shell chrome: Visual inspection during desktop NUCLEUS deployment
- SSE robustness: exp078 (intermittent biomeOS availability)

---

## Timeline Suggestion

| Priority | Ask | Effort |
|----------|-----|--------|
| P0 | Motor channel fix in `live_mode.rs` | Small — channel wiring |
| P1 | Session-aware rendering | Medium — render pipeline refactor |
| P1 | Desktop shell chrome | Medium — new panel rendering |
| P1 | SSE reconnection | Small — retry loop |
| P2 | Multi-viewport Phase A | Medium — egui viewport API |
| P2 | Sensor intent broadcasting | Medium — pattern detection + schema |
| P3 | DisplayManager Phase B | Large — abstraction layer |
| P3 | ToadStool display.* Phase C | Large — cross-primal IPC |
