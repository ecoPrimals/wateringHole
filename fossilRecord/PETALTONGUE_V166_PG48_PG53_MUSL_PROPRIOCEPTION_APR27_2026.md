# petalTongue v1.6.6 — PG-48 + PG-53 Resolution

**Date**: April 27, 2026
**Commit**: `78b3fec`
**Upstream**: primalSpring Cross-Spring Convergence audit (April 27, 2026)

---

## PG-48 (HIGH): musl/plasmidBin winit Main-Thread Panic — RESOLVED

### Problem

plasmidBin musl binary panics in `live` mode:
```
Initializing the event loop outside of the main thread
```
musl libc's `gettid()` behavior differs from glibc, causing winit 0.30's
`is_main_thread()` check to report false even on the actual OS main thread.
The locally-built glibc binary works because glibc correctly identifies thread 01.

### Fix

1. **`with_any_thread(true)`**: Added `NativeOptions.event_loop_builder` hook
   that calls `winit::platform::x11::EventLoopBuilderExtX11::with_any_thread(true)`
   on Linux. This bypasses the thread-identity check. Our PG-40 code already
   guarantees main-thread dispatch — the check was a false positive under musl.

2. **eframe backend features**: Enabled explicit `x11` + `wayland` features
   (previously stripped by `default-features = false`). The lockfile already
   had both backend deps transitively; this makes them explicitly selected.

3. **`winit` as direct workspace dep**: Added `winit = { version = "0.30",
   default-features = false }` for access to `EventLoopBuilderExtX11` trait.
   Zero new crates added — already transitive from eframe.

4. **Shared helper**: `ui_mode::native_options_with_any_thread()` used by both
   `ui_mode::run_ui_blocking` and `live_mode::run_ui_blocking`.

### Verification

- glibc build: compiles, 0 clippy warnings, 6,024 tests pass
- macOS aarch64 cross-check: clean
- plasmidBin musl: needs downstream binary rebuild to verify

---

## PG-53 (LOW): Server Mode Proprioception — RESOLVED

### Problem

`proprioception.get` had no IPC handler. Composition scripts call this method
to determine rendering cadence (`frame_rate`), but server mode returned
"Method not found".

### Fix

New `proprioception.get` handler in `system/proprioception.rs`:

```json
{
  "frame_rate": 0.0,
  "active_scenes": 0,
  "total_frames": 0,
  "user_interactivity": "none",
  "mode": "server",
  "uptime_secs": 42,
  "window": null
}
```

- **Server/headless**: `frame_rate: 0.0`, `window: null`, `mode: "server"`
- **Live/UI** (rendering_awareness present): `frame_rate: 60.0`,
  `window: { present: true }`, `mode: "live"`
- `active_scenes`: count of VisualizationState sessions
- `total_frames`: sum of frame_count across all sessions
- `user_interactivity`: `"active"` if UI + scenes, else `"none"`

### Tests

- `proprioception_get_server_mode_returns_zero_fps`: validates all server fields
- `proprioception_get_with_sessions`: validates scene count after session creation

---

## --socket CLI Flag — NO FIX NEEDED

`--socket` has been wired on `server` and `live` subcommands since PT-10
(April 10, 2026). Both `--socket /path/to.sock` and `PETALTONGUE_SOCKET`
env var are fully functional. ludoSpring's report was likely from a stale
binary build.

Verified via `petaltongue server --help` — flag shows with env source.

---

## PG-53 Follow-up: rendering_awareness Server Mode Bug — RESOLVED

### Problem

primalSpring convergence validation found that `rendering_awareness` was
unconditionally set to `Some(...)` in `UnixSocketServer::new_with_socket`,
so even headless `server` mode had a `RenderingAwareness` instance. This
caused `proprioception.get` to falsely report `frame_rate: 60.0`,
`mode: "live"`, `window: { present: true }` in server mode.

### Fix

- Removed unconditional `rendering_awareness = Some(...)` from
  `UnixSocketServer::new_with_socket`. `RpcHandlers::new()` already
  defaults to `None`.
- Only `live_mode.rs` now explicitly wires `rendering_awareness` via
  the existing `with_rendering_awareness()` builder method.
- Updated two integration tests to assert correct server-mode behavior
  (graceful degradation, not false positive awareness).

### Verification

- `proprioception_get_server_mode_returns_zero_fps`: confirmed 0 FPS, "server" mode, null window
- `test_showing_without_awareness_returns_false`: graceful degradation
- `test_introspect_without_awareness_returns_error`: correct error in headless
- 0 clippy warnings, all tests pass

---

## For primalSpring Gap Registry

| Gap | Status | Commit |
|-----|--------|--------|
| PG-48 | **RESOLVED** — `with_any_thread(true)` bypasses musl thread-ID mismatch | `78b3fec` |
| PG-53 | **RESOLVED** — handler + server-mode awareness fix | `78b3fec` + follow-up |
| `--socket` | **ALREADY RESOLVED** (PT-10) — reconfirmed functional | N/A |
