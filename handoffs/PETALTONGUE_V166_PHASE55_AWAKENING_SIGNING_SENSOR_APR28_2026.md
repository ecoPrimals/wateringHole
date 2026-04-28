# petalTongue v1.6.6 — Phase 55 Response: Awakening Evolution, Scene Signing, Sensor Stream

**Date**: April 28, 2026  
**From**: petalTongue  
**Responding to**: primalSpring v0.9.20 Phase 55 audit  
**Status**: All three asks addressed

---

## 1. AWAKENING_ENABLED=false — Composition-Controlled Awakening

### Problem
Awakening experience (default panels, startup overlay) auto-started on `live` mode,
overriding composition intent when `AWAKENING_ENABLED=false`.

### Solution
- **Default changed to OFF**: `AWAKENING_ENABLED` now defaults to `false` (was `true`).
  The fallback chain: `AWAKENING_ENABLED` env var > scenario `awakening_enabled` config > `false`.
- **New IPC method `motor.set_awakening`**: compositions invoke awakening on-demand:
  ```json
  {"jsonrpc": "2.0", "method": "motor.set_awakening", "params": {"enabled": true}, "id": 1}
  ```
- **Bidirectional**: `enabled: true` starts the overlay, `enabled: false` dismisses it.
- **Standalone `ui` mode**: users who want awakening set `AWAKENING_ENABLED=true` or configure
  their scenario file with `awakening_enabled: true`.

### Files Changed
- `crates/petal-tongue-ui/src/app/scenario_init.rs` — default flipped, logging updated
- `crates/petal-tongue-ui/src/app/events.rs` — `SetAwakening` handler now supports `start()`
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/motor.rs` — `motor.set_awakening` route + 3 tests
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/dispatch.rs` — dispatch wiring
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/system/capabilities.rs` — capability advertised

---

## 2. Scene Push Signing — Composition Integrity Verification

### Problem
Scene pushes over IPC were unsigned; rogue IPC could corrupt the display without detection.

### Solution (per NUCLEUS Two-Tier Crypto Model)
- **New module `scene_signer.rs`**: BLAKE3 keyed-hash signing using the `visualization` purpose key.
- **Key source**: `PETALTONGUE_SCENE_KEY` env var (hex-encoded 32-byte key, provided by
  `nucleus_crypto_bootstrap.sh` via `tower_derive_key(family_key, "visualization")`).
- **Signing flow**:
  1. On `visualization.render.scene`, the canonical scene JSON is BLAKE3-keyed-hashed.
  2. Response includes `"signed": true, "signature": "<hex>"` when key is available.
  3. If no key, `"signed": false` — scenes are valid but unverified.
- **Verification**: new `visualization.scene.verify` IPC method:
  ```json
  {"jsonrpc": "2.0", "method": "visualization.scene.verify",
   "params": {"session_id": "s1", "signature": "<hex>"}, "id": 2}
  ```
  Returns `{"valid": true/false}`.
- **Future**: evolve to BearDog `crypto.sign` delegation (Ed25519) when BTSP Phase 3 completes.

### Files Changed
- `crates/petal-tongue-ipc/src/scene_signer.rs` — new module (9 tests)
- `crates/petal-tongue-ipc/src/lib.rs` — module registration + `SceneSigner` export
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/mod.rs` — `scene_signer` field on `RpcHandlers`
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/visualization/mod.rs` — signing in `handle_render_scene`, new `handle_scene_verify`
- `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/dispatch.rs` — `visualization.scene.verify` route

---

## 3. Sensor Stream Evolution — New Discrete Event Types

### Problem
sensor_stream had 5 event types (pointer_move, click, key_press, key_release, scroll).
Compositions needed focus state and text input for full UI control.

### Solution
Added 4 new `SensorEventIpc` variants:
- `focus_gained` — window gained focus (user is present)
- `focus_lost` — window lost focus
- `window_resize` — viewport dimensions changed (available for future wiring)
- `text_input` — composed text string (character input beyond key events)

Focus and text events are collected from egui's `WindowFocused` and `Text` events
in `sensor_feed.rs`. Total: 9 discrete event types.

### Files Changed
- `crates/petal-tongue-core/src/sensor/ipc_types.rs` — 4 new variants + 5 new tests
- `crates/petal-tongue-ui/src/sensor_feed.rs` — focus/text collection + 4 new tests

---

## Verification

- **Clippy**: 0 warnings (all targets)
- **Tests**: 6,045+ passing (98 test suites), 0 failures
- **Compilation**: clean on Linux x86_64

## For primalSpring

### To use awakening control:
```bash
# In composition startup, after petalTongue live mode is running:
echo '{"jsonrpc":"2.0","method":"motor.set_awakening","params":{"enabled":true},"id":1}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET
```

### To use scene signing:
```bash
# Set the visualization purpose key before starting petalTongue:
export PETALTONGUE_SCENE_KEY=$(tower_retrieve_purpose_key "visualization")
petaltongue live

# Push a scene — response includes signature
# Verify with: visualization.scene.verify { session_id, signature }
```

### To subscribe to new sensor events:
```json
{"jsonrpc": "2.0", "method": "interaction.sensor_stream.subscribe", "params": {}, "id": 1}
// Poll returns focus_gained, focus_lost, text_input alongside existing events
```
