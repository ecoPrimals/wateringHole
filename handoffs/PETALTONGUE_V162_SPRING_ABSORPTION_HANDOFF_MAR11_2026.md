<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# petalTongue V1.6.2 — Spring Absorption Handoff — March 11, 2026

**From:** petalTongue V1.6.2 (3,409 tests, 0 failures, 17 ignored)
**To:** biomeOS, hotSpring, neuralSpring, wetSpring, healthSpring, ludoSpring, groundSpring, airSpring, toadStool
**License:** AGPL-3.0-only
**Supersedes:** PETALTONGUE_V161_LIVE_ECOSYSTEM_WIRING_HANDOFF_MAR11_2026

---

## Executive Summary

- **7 cross-spring patterns** absorbed and evolved into petalTongue core
- **Server-side backpressure** for 60 Hz streaming (wetSpring/healthSpring/ludoSpring pattern)
- **JSONL telemetry ingestion** from hotSpring computational physics
- **Diverging color scales** for neuralSpring heatmaps (Kokkos parity)
- **Pipeline DAG orchestration** for multi-stage visualization workflows (neuralSpring/groundSpring)
- **Provider registry** IPC for toadStool S145 capability announcements
- **Session health queries** via `visualization.session.status`
- **Game domain palette** for ludoSpring visualizations
- **3,409 tests**, 0 clippy warnings (pedantic + nursery), 0 unsafe

## What petalTongue Now Provides

### For hotSpring

- **JSONL telemetry ingestion**: `TelemetryAdapter` in `petal-tongue-core` parses
  hotSpring's line-delimited JSON telemetry format (`{t, section, observable, value}`)
  into `DataBinding::TimeSeries` grouped by section and observable.
- **Usage**: hotSpring writes JSONL telemetry to file or streams via IPC;
  petalTongue reads and auto-compiles to time series visualizations.
- **Methods**: `TelemetryAdapter::parse(content)`, `::from_reader(r)`, `::from_file(path)`,
  `::to_data_bindings()`, `::section_to_bindings(section)`.

### For neuralSpring

- **Diverging color scale**: `DivergingScale` provides three-stop interpolation
  (low→mid→high) for continuous heatmap data. `DivergingScale::kokkos_parity()`
  gives the S139-compatible blue-white-red scale.
- **Pipeline DAG**: `PipelineRegistry` manages multi-stage visualization pipelines
  with topological ordering. Supports `submit()`, `update_stage()`, and progressive
  `completed_bindings()` collection. Validates DAG acyclicity and dependency ordering.

### For wetSpring / healthSpring / ludoSpring

- **Server-side backpressure**: `BackpressureConfig` with configurable
  `max_updates_per_sec` (default 120), `cooldown` (200ms), `burst_tolerance` (10).
  Sessions that exceed the rate are cooldown-gated. `StreamUpdateResponse` now includes
  `backpressure_active: bool` so clients can adapt.
- **Session health**: `visualization.session.status` IPC method returns `frame_count`,
  `uptime_secs`, `backpressure_active`, and `is_active` for any session.

### For ludoSpring

- **Game domain palette**: 7th domain palette with warm amber `(220, 160, 80)` base.
  Triggered by `domain: "game"` or `domain: "ludology"` in render requests.

### For toadStool

- **Provider registry**: `provider.register_capability` IPC method accepts capability
  announcements per S145 ProviderRegistry protocol. Accepts `capability`, `socket_path`,
  `provider_name`, `version`, and `methods` fields.

### For groundSpring / airSpring

- **Pipeline DAG**: Same `PipelineRegistry` supports TOML-based graph pipeline
  definitions when parsed to `PipelineStage` structures. Topological sort ensures
  correct execution order for multi-stage analysis workflows.

## New IPC Methods

```
visualization.session.status    → SessionStatusResponse (frame_count, uptime, backpressure)
provider.register_capability    → {registered: true}
```

## Validation Scorecard

| Check | Result |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets` | 0 warnings (pedantic + nursery) |
| `cargo test --workspace` | 3,409 passed, 0 failures, 17 ignored |
| `cargo doc --workspace --no-deps` | Clean |
| `#![forbid(unsafe_code)]` | All crate roots |
| Largest file | 1,086 lines (`animation.rs` — refactor pending) |
| New files | All under 300 lines |

## New Files

| File | Lines | Purpose |
|------|-------|---------|
| `crates/petal-tongue-core/src/telemetry_adapter.rs` | ~140 | hotSpring JSONL telemetry → DataBinding |
| `crates/petal-tongue-ipc/src/visualization_handler/pipeline.rs` | ~260 | Pipeline DAG registry + topological sort |

## Modified Files

| File | Change |
|------|--------|
| `crates/petal-tongue-ipc/src/visualization_handler/types.rs` | +BackpressureConfig, +SessionStatus DTOs, +backpressure_active field |
| `crates/petal-tongue-ipc/src/visualization_handler/state.rs` | Backpressure enforcement, session health, frame counting |
| `crates/petal-tongue-ipc/src/visualization_handler/mod.rs` | Re-exports for new types |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/mod.rs` | 2 new method routes |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/system.rs` | +handle_provider_register |
| `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/visualization.rs` | +handle_session_status |
| `crates/petal-tongue-scene/src/domain_palette.rs` | +DivergingScale, +game palette, +lerp_color |
| `crates/petal-tongue-core/src/lib.rs` | +telemetry_adapter module |
| `crates/petal-tongue-ipc/src/lib.rs` | Re-exports |
| `crates/petal-tongue-scene/src/lib.rs` | +DivergingScale re-export |

## Integration Guide

### Backpressure-Aware Streaming (for all springs)

```json
// Push data at any rate — server enforces limits
{"jsonrpc":"2.0","method":"visualization.render.stream","params":{
  "session_id":"sess-1","binding_id":"vitals","binding":{"TimeSeries":{...}}
},"id":1}

// Response includes backpressure flag
{"jsonrpc":"2.0","result":{"session_id":"sess-1","binding_id":"vitals",
  "accepted":true,"backpressure_active":false},"id":1}

// When backpressure_active is true, client should reduce send rate
```

### Session Health Query

```json
{"jsonrpc":"2.0","method":"visualization.session.status",
  "params":{"session_id":"sess-1"},"id":2}

// Response
{"jsonrpc":"2.0","result":{"session_id":"sess-1","is_active":true,
  "frame_count":1420,"uptime_secs":23.7,"backpressure_active":false},"id":2}
```

### Provider Registration (toadStool S145)

```json
{"jsonrpc":"2.0","method":"provider.register_capability","params":{
  "capability":"display.framebuffer","socket_path":"/run/user/1000/toadstool.sock",
  "provider_name":"toadStool","version":"S145",
  "methods":["display.render","display.clear"]
},"id":3}
```

---

*This handoff is unidirectional: petalTongue → ecosystem. No response expected.*
