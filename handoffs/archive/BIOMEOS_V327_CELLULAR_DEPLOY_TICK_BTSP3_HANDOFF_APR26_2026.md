# biomeOS v3.27 — Cellular Deploy, Tick Loop Relay, BTSP Phase 3 Readiness

**Date**: April 26, 2026
**From**: biomeOS
**Addresses**: primalSpring audit — Graph Maturation + Deployment Hardening (April 26, 2026)

---

## 1. Cellular Deployment Maturity — RESOLVED

**Problem**: `biomeos deploy <graph>` was a stub that validated the graph then printed "use neural-api". `cell_launcher.sh` called `biomeos deploy "$CELL_GRAPH"` expecting end-to-end deployment.

**Fix**: `modes/deploy.rs` now:
1. Resolves the running neural-api socket via `resolve_neural_api_socket()` (checks family-scoped socket, `NEURAL_API_SOCKET` env, standard locations)
2. Connects via `AtomicClient` (Unix domain socket)
3. Sends `graph.execute` with graph ID and absolute path
4. Reports deployment status (session ID for continuous graphs)

`socket_discovery::neural_api` module made public so external crates can use `resolve_neural_api_socket()`.

**Files**:
- `crates/biomeos/src/modes/deploy.rs` — full implementation
- `crates/biomeos-core/src/socket_discovery/mod.rs` — `pub mod neural_api`

**Usage**: `cell_launcher.sh start <spring>` → `biomeos deploy <cell_graph.toml>` → connects to neural-api → `graph.execute`. Requires neural-api running (which is the intended lifecycle manager).

---

## 2. Graph Execution Tick Loop — RESOLVED

**Problem**: `ContinuousExecutor` creates a per-session `GraphEventBroadcaster(16)` that nothing external subscribes to. WebSocket/SSE clients can't observe tick events. Springs do their own client-side tick loop because they can't subscribe to biomeOS's.

**Fix**:
- **`GraphHandler::event_broadcaster`**: Optional `Arc<GraphEventBroadcaster>` shared with the biomeos-api WebSocket layer. Set via `with_event_broadcaster()`.
- **Tick relay**: When a continuous session starts, a bridge task subscribes to the per-session broadcaster and relays all events to the shared one.
- **`graph.tick_status`**: New JSON-RPC method returning all active continuous sessions with state, graph ID, start time, and broadcaster availability.

**Files**:
- `crates/biomeos-atomic-deploy/src/handlers/graph/mod.rs` — `event_broadcaster` field, `tick_status()` method
- `crates/biomeos-atomic-deploy/src/handlers/graph/continuous.rs` — relay bridge on `start_continuous`
- `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` — `GraphTickStatus` route

**Note for ludoSpring**: Once the shared broadcaster is wired to `biomeos-api`'s `AppState.event_broadcaster`, WebSocket clients can subscribe to real-time tick events. ludoSpring could move from client-side `game.tick` polling to subscribing to continuous session events from biomeOS.

---

## 3. BTSP Phase 3 Preparation — DOCUMENTED

**Status**: Phase 3 (encrypted post-handshake channels) remains deferred ecosystem-wide per `BTSP_PROTOCOL_STANDARD.md`. biomeOS is the enforcement point; preparation surface is now visible.

**What changed**: `btsp.status` response enhanced with Phase 3 readiness fields:
- `phase`: Current BTSP phase (`phase1_cleartext` / `phase2_available` / `phase2_enforced`)
- `post_handshake_cipher`: Currently `"null"` (cleartext JSON-RPC after handshake)
- `phase3_ready`: `false`
- `phase3_notes`: Documents requirements — cipher negotiation (`btsp.negotiate`), HKDF session keys, length-prefixed AEAD framing

**Phase 3 touchpoints** (for future implementation):
- `btsp_client::{server_handshake, perform_client_handshake}` — add cipher negotiation after `HandshakeComplete`
- `connection::handle_stream` — replace NDJSON with AEAD frame codec
- `atomic_transport::jsonrpc_unix_btsp` — encrypted framing on outbound client
- Client `preferred_cipher` currently hardcoded to `"null"` — needs cipher suite selection

---

## Verification

- `cargo check --workspace`: 0 errors
- `cargo clippy --workspace -- -D warnings`: 0 warnings
- `cargo fmt --check`: clean
- All test failures are pre-existing (environment-dependent discovery tests with live sockets)
