# petalTongue Capabilities Alignment + Doc Cleanup

**Date**: March 31, 2026 (session 2)
**Primal**: petalTongue (Universal User Interface)
**Phase**: Capability contract alignment, error type evolution, doc hygiene
**Follows**: `PETALTONGUE_IPC_COMPLIANCE_DEEP_DEBT_EVOLUTION_HANDOFF_MAR31_2026.md`

---

## Summary

Second-pass audit and evolution driven by cross-referencing wateringHole standards
against the post-PT-01/PT-02/PT-03 codebase. Focused on contract accuracy
(capabilities.list matching dispatch), typed error evolution, and eliminating
stale documentation references.

---

## Changes

### 1. capabilities.list Method Array — Expanded to Match Dispatch (was 20 → now 41)

`crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/system.rs`

The `get_capabilities()` response now lists every method the RPC dispatch table
actually serves, organized by domain:

- **System**: `health.check`, `health.liveness`, `health.readiness`, `health.get`,
  `identity.get`, `lifecycle.status`, `capabilities.list`, `capability.announce`,
  `topology.get`, `provider.register_capability`
- **Visualization**: all 16 `visualization.*` methods
- **Interaction**: `interaction.subscribe`, `.poll`, `.unsubscribe`,
  `interaction.sensor_stream.subscribe`, `.unsubscribe`, `.poll`
- **UI**: `ui.render`, `ui.display_status`
- **Motor**: `motor.set_panel`, `.set_zoom`, `.fit_to_view`, `.set_mode`, `.navigate`
- **Graph**: `visualization.render.graph`

### 2. self_capabilities::ALL — Expanded (30 → 36)

`crates/petal-tongue-core/src/capability_names.rs`

Added missing constants:
- `MOTOR_FIT_TO_VIEW`, `MOTOR_NAVIGATE` (dispatched but unlisted)
- `IDENTITY_GET`, `LIFECYCLE_STATUS` (system methods)
- `HEALTH_LIVENESS`, `HEALTH_READINESS` (health triad)
- Renamed `CAPABILITY_LIST` → `CAPABILITIES_LIST` (canonical plural form)

### 3. cost_estimates Key Fix

`system.rs`: Changed `"capability.list"` → `"capabilities.list"` to match
the canonical method name in the dispatch table.

### 4. HealthCheckSource — Concrete Error Types

`crates/petal-tongue-discovery/src/errors.rs`

Replaced `Box<dyn std::error::Error + Send + Sync>` on `HealthCheckFailed`
with a concrete `HealthCheckSource` enum:
- `Io(std::io::Error)` — Unix socket connect failures
- `Http(reqwest::Error)` — HTTP request failures
- `Other(Box<dyn Error>)` — cross-subsystem errors (UI integration)

Callers in `neural_api_provider.rs`, `http_provider.rs`, and
`biomeos_integration/provider_trait.rs` updated to use `.into()` or
`HealthCheckSource::Other(Box::new(e))`.

### 5. Geometry Placeholder Removed

`crates/petal-tongue-scene/src/compiler/geometry.rs:316`

Changed user-visible `"Geometry {:?} (placeholder)"` to
`"Unsupported geometry: {:?}"` — proper fallback text for unimplemented
geometry types in the catch-all arm.

### 6. Stale Socket Path References Cleaned

Three files still referenced the pre-PT-01 socket format:
- `tutorial_mode.rs`: `petaltongue/petaltongue-nat0-default.sock` → `biomeos/petaltongue.sock`
- `json_rpc_client.rs` (doc examples): `/tmp/petaltongue-nat0-default.sock` → `/tmp/biomeos/petaltongue.sock`
- `lib.rs` (ASCII diagram): `/tmp/petaltongue/{uuid}.sock` → `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`

### 7. IPC_COMPLIANCE_MATRIX.md — v1.2 → v1.3

Updated all petaltongue rows to reflect current state:
- Wire Framing: P → **C** (newline TCP via `--port`)
- Socket Path: X → **C** (`biomeos/petaltongue.sock`)
- Health Methods: ? → **C** (full triad + aliases)
- `--port`: X → **C** (`server --port <N>`)
- Health Transport: ? → **C** (UDS + optional TCP)
- Mobile Transport: X → **C** for TCP; aarch64 pending
- Priority actions 5 and 13 marked RESOLVED

### 8. Root Doc Updates

- `README.md`: Test count 5,834 → 5,839
- `ENV_VARS.md`: Matrix version ref v1.2 → v1.3, last-updated → March 31

---

## Quality Verification

| Check | Result |
|-------|--------|
| `cargo check` | Clean |
| `cargo clippy --all-targets --all-features` | Zero warnings |
| `cargo test --workspace` | 5,839 passed, 0 failed |
| Stale socket path grep | Zero non-archive hits |

---

## Remaining Deferred Items

| Item | Priority | Notes |
|------|----------|-------|
| aarch64 headless cross-compile | Medium | Egui deps need cross-compile investigation |
| `OperationFailed` Box<dyn Error> in retry.rs | Low | Generic closure boundary; Box is correct here |
| Capability-domain symlinks | Low | SHOULD not MUST per discovery standard |
| `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 health schemas | Low | Publish in wateringHole (ecosystem-level) |

---

## Ecosystem Impact

- **primalSpring**: `capabilities.list` responses from petalTongue now include
  the full 41-method surface — Springs can rely on this for composition planning.
- **biomeOS**: Socket scanning at `$XDG_RUNTIME_DIR/biomeos/` will now find
  petalTongue without special configuration.
- **Other primals**: `identity.get` and `lifecycle.status` are now advertised
  in capabilities, enabling automated health dashboards.
