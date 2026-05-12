# petalTongue v1.6.6 — PT-04/PT-09 Fixes + Dev Dep & Rendering Constants

**Date**: April 30, 2026  
**Scope**: primalSpring Phase 56c audit resolution, dev dep consolidation, magic number extraction  
**Tests**: 6,054+ passing (98 suites), 0 failures, 0 Clippy warnings

---

## 1. PT-04: HTML Export Template Deduplication

**Problem**: `compile_html` in `visualization_handler/modality.rs` duplicated the
standalone HTML document shell inline via `format!()`, risking drift from the
canonical `wrap_svg_in_html` in `petal-tongue-ui-core`.

**Fix**: `compile_html` now calls `petal_tongue_ui_core::wrap_svg_in_html` directly.
Single source of truth for the HTML document template.

---

## 2. PT-09: BTSP Negotiate on JSON-Line Path

**Problem**: The JSON-line BTSP handshake relay (`btsp/json_line.rs`) performed
create + verify but skipped the `btsp.negotiate` step. The length-prefixed path
called negotiate but discarded its result silently.

**Fix**:
- JSON-line path now calls `btsp.negotiate` after verify (best-effort, non-fatal)
- Both paths log negotiate failures as `debug!` level
- `HandshakeComplete` cipher field now populated from negotiate result
- `exchange_hello_json_line` extracted to keep function within line limits

**Note**: Negotiate is best-effort — null cipher until Phase 3 encryption. BearDog
returns the negotiated cipher; petalTongue relays it to the client.

---

## 3. PT-06: Push Delivery Confirmed Active

**Status**: Already resolved (stale audit note). `callback_tx` is activated in all
IPC server modes:
- `UnixSocketServer::new_with_socket` always calls `spawn_push_delivery()`
- `live_mode` clones sender to GUI app for bidirectional push
- Non-IPC modes (ui, tui, headless, web) intentionally lack push — no subscriber sockets

---

## 4. Dev Dependency Consolidation

7 dev deps moved to `[workspace.dependencies]`:

| Dependency | Previous location |
|------------|-------------------|
| `tokio-test` | entropy, discovery, adapters |
| `wiremock` | discovery, api |
| `assert_cmd` | headless |
| `predicates` | headless |
| `criterion` | root |
| `temp-env` | core (optional + dev) |
| `mdns-sd` | discovery (optional) |

---

## 5. Graph Rendering Constants

Magic numbers extracted from `graph.rs` and `visualization/mod.rs` to
`petal_tongue_core::constants::display`:

| Constant | Value | Usage |
|----------|-------|-------|
| `GRAPH_NODE_RADIUS` | 8.0 | Node circle radius |
| `GRAPH_NODE_STROKE_WIDTH` | 1.5 | Node border width |
| `GRAPH_EDGE_STROKE_WIDTH` | 1.0 | Edge line width |
| `GRAPH_LABEL_OFFSET_X` | 12.0 | Label X offset from node |
| `GRAPH_LABEL_OFFSET_Y` | -6.0 | Label Y offset from node |
| `GRAPH_LABEL_FONT_SIZE` | 11.0 | Label font size |
| `RGBA8_BYTES_PER_PIXEL` | 4 | Texture byte size multiplier |

---

## Comprehensive Audit Metrics

| Metric | Status |
|--------|--------|
| `unsafe` in production | **0** |
| `dyn` in production | **0** |
| `TODO`/`FIXME`/`HACK` | **0** |
| `#[allow(` in production | **0** |
| Bare `#[expect(` without reason | **0** |
| Hardcoded `/tmp` in production | **0** |
| Mocks in production (ungated) | **0** |
| Files >700 lines | **1** (visualization/mod.rs at 712) |
| Tests | 6,054+ (98 suites) |
| Clippy warnings | **0** |

---

## Remaining

- BTSP Phase 3 encryption (HSM integration path)
- aarch64 musl cross-compile for headless
- Audio backend wire protocols (ToadStool `audio.play`)
- Overlay mode (toadStool Display Phase 2)
- egui texture resolution (`TextureResolver` with `egui::Shape::image`)
- BearDog crypto.sign delegation for scene signing
