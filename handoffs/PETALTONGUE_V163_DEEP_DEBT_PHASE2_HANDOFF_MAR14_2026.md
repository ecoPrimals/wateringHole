# petalTongue v1.6.3 -- Deep Debt Phase 2 Handoff

**Date**: March 14, 2026
**Primal**: petalTongue
**Version**: 1.6.3
**Session**: Modern idiomatic Rust evolution -- deep debt phase 2

---

## Summary

Comprehensive modernization pass evolving petalTongue to modern idiomatic Rust.
All `#[allow]` attributes justified, clone abuse eliminated, API ergonomics
improved with `impl Into<String>`, TRUE PRIMAL compliance hardened, production
stubs replaced with real implementations, and threading modernized to async.
3,940 tests passing, zero clippy warnings, zero unsafe.

---

## Changes Made

### TRUE PRIMAL Compliance

- `shader_lineage.rs`: Hardcoded primal names ("hotSpring", "barraCuda") replaced
  with generic origins ("spring-a", "spring-b", "compiler", "dispatcher")
- `build_demo_lineage()` and `ShaderLineageScenario::demo()` gated with
  `#[cfg(any(test, feature = "test-fixtures"))]`
- All external primal references verified capability-based, zero hardcoding

### Lint Discipline (`#[allow]` → `#[expect]`)

9 bare `#[allow(...)]` attributes converted to `#[expect(..., reason = "...")]`:

| File | Lint | Reason |
|------|------|--------|
| `raycast_renderer.rs` (×2) | `clippy::while_float` | angle normalization requires iterative float wrapping |
| `animation/lib.rs` | `clippy::while_float` | spawn accumulator drains integer units from float counter |
| `collector.rs` (×2) | `clippy::cast_precision_loss` | f64 mantissa covers u64 counts for running-average math |
| `engine.rs` | `clippy::significant_drop_tightening` | RwLock guard must span both initialize and render awaits |
| `sensor/registry.rs` | `missing_docs` | field names self-documenting for runtime sensor statistics |
| `http_provider.rs` | `deprecated` | PrimalInfo conversion retained for backward-compatible API consumers |
| `tui/state.rs` / `tui/app.rs` | `clippy::cast_sign_loss` | test timestamps/counts are always positive |

### Clone Elimination

- `graph_validation/structure.rs`: 50+ `String` clones replaced with borrowed
  `&str` lifetimes via `build_adj_list()` and `topo_sort_borrowed()` helpers.
  `HashMap<String, Vec<String>>` → `HashMap<&str, Vec<&str>>`.
- `property_panel.rs`: Unnecessary `node_id.clone()` removed (fn already owns value).
- `engine.rs` 16 `.clone()` calls confirmed as `Arc::clone()` (O(1) ref-count).

### API Ergonomics (`impl Into<String>`)

Functions migrated from `String` to `impl Into<String>`:
- `GraphNode::set_parameter(key, value)`
- `GraphEdge::new(from, to, edge_type)` / `dependency(from, to)`
- `VisualGraph::new(name)`
- `GraphCanvas::new(graph_name)` / `select_node(node_id)` / `toggle_node_selection(node_id)`
- `DeviceState::new(device_id, ...)` / `set_ui_state(key, ...)` / `set_preference(key, ...)`
- `StateSyncManager::init(device_id, ...)` / `set_ui_state(key, ...)`

### Trait Evolution

`ScenarioBuilder` trait: `id()`, `name()`, `domain()` return `&'static str`
(was `&str`), eliminating `unnecessary_literal_bound` warnings across all 9
implementations in `ground_spring.rs`, `air_spring.rs`, `shader_lineage.rs`.

### Threading Modernization

`neural_registration::spawn_heartbeat`: Replaced `std::thread::Builder::new().spawn()`
+ `rt.block_on()` with `tokio::spawn(async move { ... })`. Eliminates an unnecessary
OS thread and redundant Tokio runtime.

### Production Stub Elimination

`mdns_discovery.rs`: Stub functions (`discover_via_mdns()`, `query_capability()`)
replaced with delegation to real `MdnsVisualizationProvider::discover()` for
actual UDP multicast discovery.

### Precision

`ground_spring.rs`: Manual `((x-cx).powi(2) + (y-cy).powi(2)).sqrt()` replaced
with `(x - cx).hypot(y - cy)`.

### Version Fix

`demo_device_provider.rs`: Stale `"version": "1.5.0"` updated to `"1.6.3"`.

---

## Verification State

| Check | Status |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features` | Zero warnings |
| `cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | 3,940 tests, 0 failures, 17 ignored |
| Unsafe code | Zero (`#![forbid(unsafe_code)]` on all 16 crates) |
| License | AGPL-3.0-only, SPDX on all source files |

---

## Remaining Work

1. **Coverage**: ~83% line, target 90% -- remaining gap is thin egui rendering adapter layer
2. **ecoBin v2.0**: Windows named-pipe IPC, TCP fallback transport
3. **Cross-compilation**: armv7, macOS, Windows, WASM targets
4. **Provenance trio**: sweetGrass/rhizoCrypt/loamSpine integration
5. **Fuzz testing**: No `cargo-fuzz` harness yet

---

## wateringHole Compliance

| Standard | Status |
|----------|--------|
| UNIBIN_ARCHITECTURE | Compliant |
| ECOBIN_ARCHITECTURE | Compliant (v1.0); partial v2.0 (missing cross-platform IPC) |
| GENOMEBIN_ARCHITECTURE | Compliant (manifest.toml) |
| UNIVERSAL_IPC_STANDARD_V3 | Compliant (JSON-RPC primary, tarpc secondary) |
| SEMANTIC_METHOD_NAMING | Compliant |
| PRIMAL_IPC_PROTOCOL | Compliant |
| PURE_RUST_SOVEREIGN_STACK | Compliant |
| Code quality | 3,940 tests, 0 clippy, forbid(unsafe), all files <1000 lines |
