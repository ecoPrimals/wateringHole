# Songbird v0.2.1 — Wave 160/161 BTSP + Deep Debt + Doc Cleanup Handoff

**Date**: April 15, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Waves**: 160, 161  
**Supersedes**: `SONGBIRD_V021_WAVE159_DEEP_DEBT_PORT_CENTRALIZATION_HANDOFF_APR15_2026.md` (archived)

---

## Wave 160 — BTSP Wire-Format Integration (from primalSpring Phase 45c audit)

### Changes

- **`crates/songbird-orchestrator/src/bin_interface/server.rs`** — Refactored connection handling into `handle_connection` (BTSP auto-detection entry point), `handle_json_rpc_lines` (NDJSON line loop), `dispatch_json_rpc_line` (single request parse + dispatch). BTSP auto-detection: first-line peek routes `"protocol":"btsp"` connections through `perform_server_handshake_ndjson()` before JSON-RPC. Both UDS and TCP accept loops pass `Arc<SecurityRpcClient>` for crypto delegation.
- **`crates/songbird-http-client/src/security_rpc_client/rpc.rs`** — Added `btsp.session.create`, `btsp.session.verify`, `btsp.session.negotiate`, `btsp.server.export_keys` identity mappings in `semantic_to_actual()`.

### Verification

- `cargo build --workspace` — clean
- `cargo clippy --workspace -D warnings` — clean
- `cargo fmt -- --check` — clean
- `cargo test --workspace --lib` — 7,387 passed

---

## Wave 161 — Deep Debt Cleanup

### Error Handling

- `songbird-execution-agent/src/bin/agent.rs`: `Box<dyn Error>` → `anyhow::Result<()>`

### Hardcoded Value Elimination

- `server.rs`: hardcoded `"0.0.0.0"` → `songbird_types::constants::PRODUCTION_BIND_ADDRESS`
- `songbird-config::constants::network`: duplicate `DEFAULT_BIND_ADDRESS` → re-export from `bind_and_ports`
- **15+ `.unwrap_or(8080)` across 8 crates** replaced with canonical `songbird_types::defaults::ports` constants:
  - `songbird-config/src/defaults/ports.rs` (8 functions)
  - `songbird-config/src/discoverable_endpoint.rs`
  - `songbird-discovery/src/conversion.rs`
  - `songbird-discovery/src/abstraction/adapters/static_adapter.rs`
  - `songbird-types/src/config/adapters.rs`
  - `songbird-registry/src/types/health.rs`
  - `songbird-universal-ipc/src/handlers/mesh_handler/udp_discovery.rs`
  - `songbird-orchestrator/src/bin_interface/server.rs`

### Dependency Cleanup

| Change | Crates |
|--------|--------|
| Removed unused `futures` | songbird-bluetooth, songbird-lineage-relay |
| `futures` → `futures-util` | songbird-stun, songbird-orchestrator, songbird-universal-ipc |
| Removed `hostname` (→ `gethostname`) | songbird-config |

### Deferred

- `serde_yaml` migration blocked by `kube-client` transitive dep
- `ring` lockfile stanza benign (`cargo deny check bans` passes)
- Port constant value discrepancies (`DEFAULT_DASHBOARD_PORT` 8003 vs 3000, `DEFAULT_FEDERATION_PORT` 8000 vs 8082) deferred for coordinated reconciliation

---

## Doc Cleanup (post-Wave 161)

- `CONTRIBUTING.md`: added "Last Updated" field
- `REMAINING_WORK.md`: added Wave 161 completed items (port centralization update, hostname, futures, Box<dyn Error>); updated serde_yaml entry with kube-client blocker
- `docs/architecture/SOVEREIGN_ONION_TRUE_PRIMAL_ARCHITECTURE.md`: moved to `fossilRecord/songBird/` (self-identified as fossil record since Feb 2026)

---

## Current State

| Metric | Value |
|--------|-------|
| Build | Clean (zero errors, zero warnings) |
| Clippy | Clean (`-D warnings`, pedantic + nursery) |
| Formatting | Clean (`cargo fmt --check`) |
| Tests | 7,387 lib passed (0 failures, 22 ignored) |
| Coverage | 72.29% (Apr 8 2026; target 90%) |
| cargo-deny | Fully passing |

---

## Remaining Deep Debt (documented in REMAINING_WORK.md)

- BTSP Phase 3 encrypted framing
- Tor/TLS crypto with live security provider
- `serde_yaml` migration (blocked on kube-client)
- `bincode` 1.x advisory (transitive via tarpc)
- Coverage expansion (72.29% → 90%)
- Platform backends (NFC, iOS XPC, WASM)
