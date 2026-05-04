# petalTongue v1.6.6 — primalSpring Phase 58 Audit Response

**Date**: May 4, 2026
**Version**: 1.6.6
**Primal**: petalTongue
**Triggered by**: primalSpring Phase 58 downstream debt handoff

---

## Summary

5 audit items triaged — **4 confirmed already resolved**, **1 closed with new code**
(GAP-12 machine-readable method schemas).

## Item-by-Item Status

### 1. Phase 3 transport encryption (HIGH) — ALREADY SHIPPED

Shipped May 3, 2026. `btsp/phase3.rs` implements ChaCha20-Poly1305 AEAD encrypted
frame I/O with HKDF-SHA256 directional key derivation. Both UDS and TCP paths
handle Phase 3 upgrade after `btsp.negotiate`. 13/13 ecosystem parity.

**Ref**: `PETALTONGUE_V166_BTSP_PHASE3_TRANSPORT_SWITCH_HANDOFF_MAY03_2026.md`

### 2. musl/plasmidBin winit threading panic (HIGH) — ALREADY RESOLVED

Fixed April 26–27, 2026 (PG-40 + PG-48). Three-part fix:
1. **PG-40**: eframe runs directly on main thread (not `spawn_blocking`)
2. **PG-48**: `with_any_thread(true)` for both X11 and Wayland in
   `native_options_with_any_thread()` — shared by `ui_mode`, `live_mode`,
   and `backend/eframe.rs`
3. **Workspace Cargo.toml**: explicit `x11` + `wayland` eframe features

Verified: all 3 call sites apply the fix. No musl-specific `cfg` needed —
`#[cfg(target_os = "linux")]` covers both glibc and musl.

**Ref**: `PETALTONGUE_V166_PG48_PG53_MUSL_PROPRIOCEPTION_APR27_2026.md`

### 3. PT-04 HTML export (LOW) — ALREADY COMPLETE

Implemented and tested:
- `ExportFormat::Html` in `petal-tongue-ui-core` trait_def
- `wrap_svg_in_html` + `validate_standalone_html_export` in ui-core
- Headless CLI: `render_html()` for file and stdout
- IPC: `compile_html` calls `wrap_svg_in_html` via modality compiler
- 5+ tests green including `test_html_export_e2e_pt04_full_pipeline`

**Ref**: `PETALTONGUE_V166_PT04_PT09_DEEPDEBT_APR30_2026.md`

### 4. PT-06 push delivery (LOW) — ALREADY ACTIVE

`callback_tx` is wired at server startup:
- `UnixSocketServer::new_with_socket` → `spawn_push_delivery()`
- `handlers.callback_tx = Some(callback_tx)`
- Live mode: `server.callback_sender()` → `PetalTongueApp::set_callback_tx`
- GUI broadcasts: `app.callback_tx.send(cb)` in `update.rs`
- Test: `push_delivery_wired_for_tests()` assertion
- Non-IPC modes intentionally lack push (no subscriber sockets)

**Ref**: `PETALTONGUE_V166_PT04_PT09_DEEPDEBT_APR30_2026.md`

### 5. GAP-12 dashboard param schema (LOW) — CLOSED (NEW CODE)

**Problem**: `visualization.capabilities` returned data binding variants and
output modalities but no machine-readable parameter schema for
`visualization.render.dashboard` or other methods.

**Fix**: Added `methods` key to the capabilities response containing
structured schemas for all visualization methods:

- `visualization.render.dashboard` — required (session_id, title, bindings)
  + optional (domain, modality, max_columns) with types/defaults/descriptions
- `visualization.render.scene` — required (scene) + optional (session_id)
- `visualization.render` — required (session_id, binding) + optional (modality)
- `visualization.export` — required (session_id) + optional (modality)

Dashboard schema also includes result field descriptions (panel_count, columns,
rows, scene_nodes, total_primitives).

**File changed**: `crates/petal-tongue-ipc/src/unix_socket_rpc_handlers/visualization/mod.rs`

## Verification

```
cargo clippy --workspace --all-features: 0 warnings
cargo doc --workspace --no-deps -D warnings: 0 warnings
cargo test --workspace --all-features: 2,900+ passed, 0 failed
```

## Downstream Impact

- **primalSpring**: All 5 Phase 58 audit items resolved. GAP-12 is now closed —
  downstream consumers can programmatically discover dashboard parameters via
  `visualization.capabilities` → `methods.visualization.render.dashboard.params`.
- **Ecosystem**: petalTongue Phase 3 + all LOW gaps closed. No open petalTongue
  items remain in the primalSpring gap registry.

---

*Ref: `PETALTONGUE_V166_BTSP_PHASE3_TRANSPORT_SWITCH_HANDOFF_MAY03_2026.md`*
*Ref: `PETALTONGUE_V166_TRUE_PRIMAL_NAME_EVOLUTION_HANDOFF_MAY03_2026.md`*
