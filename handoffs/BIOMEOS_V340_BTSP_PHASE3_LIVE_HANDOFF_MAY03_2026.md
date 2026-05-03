# biomeOS v3.40 — BTSP Phase 3 Live + BTSP-Aware Capability Resolution

**Date**: May 3, 2026
**Scope**: Encrypted framing wired into connection loop; all capability resolution paths BTSP-aware
**Tests**: 7,859 passing (0 failures)
**Status**: PRODUCTION READY

---

## What Changed

Phase 3 encrypted framing is now **live in the connection loop**. After a successful
Phase 1/2 BTSP handshake, if the client sends `btsp.negotiate` as the first message
and negotiates a real cipher (ChaCha20-Poly1305), the connection switches to
length-prefixed encrypted framing. Otherwise it stays on plaintext NDJSON.

All capability resolution paths now perform BTSP client handshakes for family-scoped
sockets in production, with cleartext fallback.

### Phase 3 Encrypted Framing (connection.rs)

- `handle_stream_with_negotiate()` — post-handshake intermediary that checks the
  first incoming message for `btsp.negotiate`. Branches to encrypted or plaintext loop.
- `try_phase3_negotiate()` — parses negotiate request, calls `btsp_negotiate::handle_negotiate`,
  returns `SessionKeys` if real cipher negotiated.
- `handle_encrypted_stream()` — length-prefixed encrypted frame loop.
  Read: `[4B BE u32 len][payload]` → `decrypt_frame(client_to_server)` → JSON-RPC dispatch.
  Write: JSON-RPC response → `encrypt_frame(server_to_client)` → `[4B len][payload]`.
  16 MB frame guard, 30 s read timeout.
- `btsp_negotiate.rs` — `dead_code` annotations removed from `SessionKeys`,
  `encrypt_frame`, `decrypt_frame`, `FrameError` (now live production code).

### BTSP-Aware Capability Resolution

- **executor/node_handlers.rs** (`call_primal_rpc`): family-scoped sockets perform
  `btsp_client::perform_client_handshake` before sending JSON-RPC. Falls back to
  cleartext on handshake failure. Preserves raw JSON-RPC envelope return contract.
- **capability_translation/mod.rs** (`call_capability`): uses `AtomicClient::call_btsp()`
  for family-scoped sockets in production mode, cleartext fallback on failure.

### Remaining Hardcoded Primal Names Eliminated

| Area | Change |
|------|--------|
| `orchestrator.rs` | `BEARDOG_FAMILY_SEED_FILE` → `SECURITY_PROVIDER_FAMILY_SEED_FILE` |
| `btsp_client.rs` | `BEARDOG_SOCKET` / `BIOMEOS_BEARDOG_SOCKET` env var fallbacks removed |
| `primal_impls.rs` | `SONGBIRD_NODE_ID` removed; `NODE_ID` is canonical |
| `config/mod.rs` | `DISCOVERY_PROVIDER` env var for mesh orchestrator resolution |
| `main.rs` | "rhizoCrypt session" → "Provenance session" in CLI help |
| 14 neural_api_server modules | Comments updated to capability-domain language |

---

## Files Modified

| Area | File | Change |
|------|------|--------|
| Connection | `neural_api_server/connection.rs` | Phase 3 framing loop + 7 new tests |
| Crypto | `neural_api_server/btsp_negotiate.rs` | `dead_code` annotations removed |
| Executor | `executor/node_handlers.rs` | BTSP-aware `call_primal_rpc` |
| Capability | `capability_translation/mod.rs` | BTSP-aware `call_capability` |
| Orchestrator | `orchestrator.rs` | Env var name evolved |
| Core | `btsp_client.rs` | Legacy env var fallbacks removed |
| Core | `primal_impls.rs` | Hardcoded `SONGBIRD_NODE_ID` removed |
| Core | `config/mod.rs` | `DISCOVERY_PROVIDER` env var |
| CLI | `main.rs` | Primal-agnostic help text |
| Routing | `neural_api_server/routing.rs` | Comment updated |
| Capability | `handlers/capability.rs` | Comment updated |
| Translation | `neural_api_server/translation_loader.rs` | Comment updated |
| Discovery | `neural_api_server/discovery_init.rs` | Comment updated |
| Lifecycle | `neural_api_server/server_lifecycle.rs` | Comment updated |
| Agents | `neural_api_server/agents/types.rs` | Comment updated |
| Agents | `neural_api_server/agents/mod.rs` | Comment updated |
| Proxy | `neural_api_server/proxy.rs` | Comment updated |
| Agents RPC | `neural_api_server/agents/rpc.rs` | Comment updated |
| API | `biomeos-api/handlers/live_discovery.rs` | Comment cleaned |

---

## Impact on Downstream Springs

- **primalSpring**: `btsp.negotiate` integration tests (`phase3_negotiate_with_live_biomeos`,
  `phase3_transport_full_roundtrip`) should now pass against live biomeOS binary.
- **All springs**: Capability resolution via Neural API now uses authenticated channels
  for family-scoped sockets. No action needed — cleartext fallback is automatic.

## Codebase Health

- 7,859 tests (0 failures, fully concurrent)
- 0 production files >800 LOC
- 0 unsafe in production
- 0 TODO/FIXME/HACK in production
- 0 production mocks/stubs
- `cargo check` + `clippy -D warnings` + `cargo fmt --check`: all clean
