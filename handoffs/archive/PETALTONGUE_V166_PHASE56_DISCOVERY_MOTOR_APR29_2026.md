# petalTongue v1.6.6 — Phase 56 Gap Resolution

**Date**: April 29, 2026  
**Scope**: GAP-01 (discovery heartbeat), Motor P0 (IPC→GUI channel), GAP-17 (capability symlink)  
**Tests**: 6,054+ passing (98 suites), 0 failures, 0 Clippy warnings

---

## 1. GAP-01 (P1): Discovery Heartbeat Socket

**Problem**: `RegistrationClient::new()` built its socket path from
`discovery_service_socket_name()` → `discover_primal_socket("discovery-service")`,
which checked the env var `DISCOVERY-SERVICE_SOCKET` (hyphenated, unusable).
NUCLEUS compositions set `DISCOVERY_SOCKET` but petalTongue never read it.

**Fix**:
- `RegistrationClient::new()` now checks `DISCOVERY_SOCKET` first (highest priority)
- Falls back to existing `DISCOVERY_SERVICE_SOCKET` basename resolution
- Heartbeat task now uses exponential backoff (2^n × interval, cap 64×) instead of
  fixed-interval retries on failure, with recovery logging

**Files**: `crates/petal-tongue-ipc/src/primal_registration.rs`

**Usage**:
```bash
DISCOVERY_SOCKET=/run/user/1000/biomeos/songbird-desktop-nucleus.sock \
  petaltongue live
```

---

## 2. Motor P0: IPC Motor Channel Wired to GUI

**Problem**: In `live_mode.rs`, the IPC server's motor channel (`motor_tx`) was
connected to a dead-end OS thread that only logged commands. The GUI created its
own separate `mpsc` channel. IPC motor commands (`motor.set_panel`, etc.) were
acknowledged on the wire but never reached the `egui` render loop.

**Fix**:
- `live_mode.rs` now creates one `mpsc` channel, passes `motor_tx.clone()` to
  the IPC server AND passes both `motor_tx` + `motor_rx` to the app via
  `PetalTongueApp::replace_motor_channel()`
- Dead-end logging thread removed
- All IPC motor commands now flow to `drain_motor_commands` every frame

**New methods** (dispatch + handler + MotorCommand variants):

| Method | Params | Effect |
|--------|--------|--------|
| `motor.panel.update` | `panel`, `title?`, `content` | Updates panel content in `PanelContentStore` |
| `motor.notification` | `level`, `message`, `duration_ms?` | Queues notification in `NotificationQueue` |

**Files**: `src/live_mode.rs`, `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/{dispatch,motor}.rs`,
`crates/petal-tongue-core/src/rendering_awareness/types.rs`, `crates/petal-tongue-ui/src/app/{mod,init,events,motor_state}.rs`

**Usage**:
```bash
# Push panel content from composition
echo '{"jsonrpc":"2.0","method":"motor.panel.update","params":{"panel":"dashboard","title":"System","content":{"cpu":42}},"id":1}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET

# Send notification
echo '{"jsonrpc":"2.0","method":"motor.notification","params":{"level":"info","message":"Game saved","duration_ms":3000},"id":2}' | socat - UNIX-CONNECT:$PETALTONGUE_SOCKET
```

---

## 3. GAP-17 (P1): Capability Symlink — Already Implemented

**Problem**: `discover_by_capability("visualization")` looks for
`visualization-{family}.sock`. petalTongue creates `petaltongue-{family}.sock`.

**Finding**: `UnixSocketServer::start()` already creates a
`visualization-{family}.sock` symlink via `btsp::domain_symlink_filename()`.
The symlink is created in the same parent directory as the socket and cleaned
up on `Drop`. No code change needed.

**Possible failure modes** (for debugging):
- Symlink creation logged at `debug` level — check logs if missing
- `PETALTONGUE_SOCKET` override moves the socket but symlink is still in socket's parent dir
- Symlink errors are non-fatal (continue without)

---

## Verification

- **Clippy**: 0 warnings (all targets)
- **Tests**: 6,054+ passing (98 suites), 0 failures
- **New tests**: 9 (motor.panel.update, motor.notification, DISCOVERY_SOCKET override,
  PanelContentStore, NotificationQueue)

---

## Remaining (for future UI pass)

- `PanelContentStore` data is collected but not yet rendered in egui panels
- `NotificationQueue` entries are collected but not yet rendered as toast/overlay
- `motor.panel.update` for `PanelId::Custom` needs panel registration/creation in the UI
