# toadStool — Display Phase 2 + Compositing + Transport Bridge

**From**: primalSpring v0.9.17 (Phase 45c — Graphics Node)
**Date**: April 26, 2026
**For**: toadStool team

---

## Context

primalSpring has reached full NUCLEUS deployment with BTSP default and a live
petalTongue desktop window. The next architectural goal is **petalTongue as
full graphics system** — capable of embedding external engine output (Godot),
overlaying existing games, and compositing arbitrary visual sources through
NUCLEUS primal capabilities.

Three toadStool evolutions are needed, in priority order.

---

## 1. Display Backend Phase 2 — petalTongue Integration

**Priority**: CRITICAL (prerequisite for everything below)
**Spec**: `specs/DISPLAY_BACKEND_SPEC.md` Phase 2
**Current state**: Phase 1 complete — DRM/KMS backend, window manager,
InputManager, JSON-RPC IPC server with 5/8 methods wired

### What needs to happen

petalTongue currently uses winit/eframe directly for its native window.
Phase 2 replaces that with toadStool-provisioned display surfaces so
petalTongue has ZERO hardware knowledge.

**Server-side (toadStool)**:

Wire the three unimplemented `DisplayMethod` variants in `ipc/dispatch.rs`:

| Method | Status | Needs |
|--------|--------|-------|
| `display.present` | Defined in `DisplayMethod`, not dispatched | Accept `window_id` + pixel data (or memfd handle), page-flip to CRTC. Zero-copy via shared memory (memfd) preferred. |
| `display.subscribe_input` | Defined, not dispatched | Return a stream of `InputEvent` for a given window. Route through existing `InputManager.subscribe_events()`. |
| `display.poll_events` | Defined, not dispatched | Non-streaming alternative — return buffered events since last poll. Fix current `poll_events()` which returns empty `Vec`. |

**Client-side (DisplayClient)**:

Add `present()`, `subscribe_input()`, `poll_events()` to
`ipc/client/operations.rs` — petalTongue will depend on the
`toadstool_display` crate and call these instead of winit.

**petalTongue integration path**:

```
petalTongue main.rs
  ├── `live` mode: DisplayClient::connect() → create_window() → render loop
  │     each frame: flatten SceneGraph → rasterize to pixel buffer → display.present()
  │     input: display.subscribe_input() → feed to interaction engine
  └── eframe/winit: REMOVED (or kept as fallback behind feature flag)
```

### Performance targets from spec

- Frame present: < 16ms (60 FPS)
- Input latency: < 8ms (keyboard/mouse to event)
- IPC roundtrip: < 5ms (Unix socket)

### Key files to modify

- `crates/runtime/display/src/ipc/dispatch.rs` — wire `display.present`, `display.subscribe_input`, `display.poll_events`
- `crates/runtime/display/src/ipc/client/operations.rs` — add client methods
- `crates/runtime/display/src/window/framebuffer.rs` — implement `FramebufferOps::present()` (DRM page-flip)
- `crates/runtime/display/src/input/mod.rs` — fix `poll_events()` and `device_count()`

---

## 2. Display Compositing — Multi-Layer `display.composite`

**Priority**: HIGH (enables external engine embedding)
**Depends on**: Display Phase 2

### The need

Once petalTongue renders to a toadStool-managed framebuffer, the next step
is compositing MULTIPLE framebuffer sources into a single DRM output.
This enables:

- **Godot + petalTongue overlay**: game engine renders to layer 0,
  petalTongue HUD/metrics render to layer 1, toadStool composites and
  presents the final frame
- **External game + NUCLEUS overlays**: any process writes pixels to a shared
  framebuffer, petalTongue overlays on top
- **Multi-session visualization**: multiple petalTongue sessions composited
  into one window

### Proposed IPC method

```json
{
  "jsonrpc": "2.0",
  "method": "display.composite",
  "params": {
    "window_id": "uuid",
    "layers": [
      {
        "source": "memfd://godot-fb-0",
        "z_order": 0,
        "opacity": 1.0,
        "rect": { "x": 0, "y": 0, "width": 1920, "height": 1080 }
      },
      {
        "source": "memfd://petaltongue-overlay",
        "z_order": 1,
        "opacity": 0.9,
        "rect": { "x": 0, "y": 0, "width": 1920, "height": 1080 }
      }
    ],
    "blend_mode": "alpha_over"
  },
  "id": 1
}
```

### Architecture

```
External Engine (Godot, etc.)
  │ writes pixels to shared memfd
  ▼
toadStool Display Backend
  ├── Layer 0: external framebuffer (read from memfd)
  ├── Layer 1: petalTongue overlay (read from memfd)
  └── Compositor: alpha-blend layers → DRM page-flip
        ▼
      Hardware (monitor)
```

### Implementation notes

- Each layer is a `FramebufferHandle` backed by shared memory (memfd)
- Compositor does CPU alpha-blend for initial version; GPU-accelerated
  compositing is Phase D (see coralReef handoff)
- `NativeRuntimeEngine` already spawns child processes — extend it to pass
  memfd file descriptors to the child for zero-copy framebuffer exchange
- Consider DRM overlay planes for hardware compositing on supported GPUs

### Key files to modify/create

- `crates/runtime/display/src/ipc/types.rs` — add `DisplayMethod::Composite`
- `crates/runtime/display/src/window/compositor.rs` — new: multi-layer compositor
- `crates/runtime/display/src/ipc/dispatch.rs` — wire `display.composite`

---

## 3. Transport Bridge — External Process Gateway to NUCLEUS

**Priority**: MEDIUM (enables non-primal consumers)
**Depends on**: Display Phase 2

### The need

External processes (game engines, third-party tools, existing applications)
need to consume NUCLEUS primal capabilities without being primals themselves.
Today, a process must know individual primal sockets and speak their specific
JSON-RPC protocols. A transport bridge provides a single gateway.

### Proposed capability: `transport.bridge`

toadStool already has `transport.*` and `gate.*` method families. The bridge
extends this to create a gateway socket that an external process connects to:

```json
{
  "jsonrpc": "2.0",
  "method": "transport.bridge.create",
  "params": {
    "bridge_id": "godot-bridge-001",
    "capabilities": [
      "activation.fitts",
      "activation.hick",
      "math.sigmoid",
      "noise.perlin2d",
      "visualization.render",
      "dag.event.append",
      "certificate.mint"
    ],
    "auth": "btsp_family"
  },
  "id": 1
}
```

Response includes a socket path the external process connects to. All
capability calls on that socket are routed to the correct NUCLEUS primals.

### How it differs from biomeOS Neural API

biomeOS Neural API orchestrates the full deployment lifecycle (graphs,
topology, rescan). The transport bridge is lightweight — it only routes
capability calls and does not manage primal lifecycle. Think of it as
a reverse proxy scoped to specific capabilities.

### Routing flow

```
External Process (Godot plugin, game mod, CLI tool)
  │ connects to /run/user/$UID/biomeos/bridge-godot-001.sock
  │ sends: {"method": "activation.fitts", "params": {...}}
  ▼
toadStool transport.bridge
  │ looks up capability → barraCuda socket
  │ forwards request, returns response
  ▼
barraCuda (or any primal by capability)
```

### Implementation approach

- Reuse existing `CapabilityProvider::discover()` for socket resolution
- Reuse existing `compute.dispatch.forward` pattern for request proxying
- Bridge socket is a standard JSON-RPC 2.0 UDS — no special client needed
- BTSP authentication: bridge inherits the NUCLEUS family seed, external
  process authenticates once at bridge creation

### Key files to modify/create

- `crates/server/src/pure_jsonrpc/handler/transport/` — add `bridge.rs`
- `crates/server/src/ipc/` — new: bridge socket listener + forwarder

---

## Summary — What We Need From toadStool

| Evolution | Priority | Blocks | Estimated Scope |
|-----------|----------|--------|-----------------|
| Display Phase 2 (present + input IPC) | CRITICAL | Everything below | Wire 3 methods + client ops + DRM page-flip |
| Display Compositing (`display.composite`) | HIGH | External engine embedding | New compositor module + IPC method |
| Transport Bridge (`transport.bridge`) | MEDIUM | Non-primal NUCLEUS consumers | New bridge socket + capability routing |

Display Phase 2 is the prerequisite. Once petalTongue renders through
toadStool's framebuffer, compositing and bridging become natural extensions.

---

**References**:
- Display spec: `toadStool/specs/DISPLAY_BACKEND_SPEC.md`
- Display README: `toadStool/crates/runtime/display/README.md`
- NativeRuntimeEngine: `toadStool/crates/runtime/native/src/engine.rs`
- Existing transport methods: `toadStool/docs/reference/SERVER_METHODS.md`
- primalSpring gap registry: `primalSpring/docs/PRIMAL_GAPS.md`

License: AGPL-3.0-or-later
