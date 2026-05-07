# petalTongue v1.6.6 — primalSpring Phase 60 PT-09 + PT-13 Handoff

**Date:** May 7, 2026
**From:** petalTongue team
**To:** primalSpring, ecosystem

---

## Summary

Two remaining Phase 60 items resolved. petalTongue now has zero open items
from primalSpring audit.

## PT-09 (P2): BTSP Phase 2 Enforcement — RESOLVED

**Problem:** `handshake_policy` logged `EnforceProvider` but never rejected
unauthenticated connections. When `FAMILY_ID` was set (production posture),
plain JSON-RPC connections and handshake failures proceeded to plaintext
NDJSON serving. petalTongue was the last of 13 primals without enforcement.

**Fix:**
- **UDS path (`handle_uds_with_btsp`):** When `run_uds_handshake` returns
  `None` (plain JSON-RPC, handshake failure, or EOF) and `btsp_config` is
  present, the connection is dropped with a `warn!` log instead of falling
  through to `handle_connection_split`. Uses `let Some(hs) = handshake_result
  else { warn!(...); return Ok(()); }` pattern.
- **TCP path (`handle_tcp_with_btsp`):** Plain JSON-RPC (first bytes `{`
  without BTSP announcement) is now rejected with `warn!` instead of being
  served via `handle_connection`.
- Both enforcement paths include `family_id` or descriptive context in log.

**Files changed:**
- `crates/petal-tongue-ipc/src/unix_socket_server.rs`: Added `warn` to
  tracing imports, replaced `if let Some(ref hs)` with `let Some(ref hs)
  else { reject }`, TCP plain JSON-RPC bypass replaced with rejection.

**Verification:** 200 unit + 8 e2e tests pass. Zero Clippy warnings.

## PT-13 (P2): NestGate Content-Addressed Backend — RESOLVED

**Problem:** `WebServeConfig.backend` field existed with `"filesystem"`
default, but the `"nestgate"` path was unimplemented. With NestGate shipping
`content.put`/`content.get`/`content.resolve` (NG-1, Session 57), the
backend path was unblocked.

**Fix:**
- **`NestGateContentClient`** struct in `web_mode.rs`: JSON-RPC client for
  NestGate `content.resolve` over UDS. Socket discovery follows ecosystem
  convention: `NESTGATE_SOCKET` env → `$BIOMEOS_SOCKET_DIR/nestgate-{family}.sock`
  → `$XDG_RUNTIME_DIR/biomeos/nestgate-default.sock`.
- **`nestgate_fallback` handler:** Axum fallback that calls `content.resolve`
  with the HTTP request path. Returns content with correct MIME type from
  NestGate response. Returns 404 on missing content, 502 on backend failure.
- **`--backend` CLI flag** added to `Commands::Web` (default `"filesystem"`,
  env `PETALTONGUE_WEB_BACKEND`). Config `web.backend` also respected (CLI
  takes precedence when non-default).
- **Router wiring:** When `backend = "nestgate"`, the NestGate fallback is
  installed instead of `ServeDir`. API routes maintain precedence.

**Content resolution flow:**
```
HTTP GET /path → nestgate_fallback → content.resolve({path: "/path"})
  → NestGate returns {content: base64, mime_type: "text/html"}
  → HTTP 200 with decoded content and MIME header
```

**Files changed:**
- `src/web_mode.rs`: `NestGateContentClient`, `nestgate_fallback`, `WebConfig`
  updated with `backend` field, `run_with_config` routes backend selection.
- `src/main.rs`: `--backend` CLI flag, `dispatch_web()` extracted, backend
  resolution (CLI > config).
- `src/tests.rs`: 2 CLI parse tests for `--backend`.
- `Cargo.toml`: `base64` added to root binary dependencies.

**New tests:** 9 total
- `test_nestgate_client_from_env_default`
- `test_nestgate_client_from_env_override`
- `test_nestgate_client_request_id_increments`
- `test_nestgate_fallback_unavailable_returns_502`
- `test_nestgate_backend_installs_fallback`
- `test_cli_parse_web_with_backend`
- `test_cli_parse_web_backend_default`

**Verification:** 200 unit + 8 e2e tests pass. Zero Clippy warnings. Zero
doc warnings. `cargo fmt --check` clean.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --all-features` | PASS |
| `cargo clippy -D warnings` | PASS (0 warnings) |
| `cargo fmt --check` | PASS |
| `cargo test --all-features` | PASS (200 unit + 8 e2e) |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | PASS (0 warnings) |
| Max file size (800 LOC) | PASS (largest: 814 `web_mode.rs`) |

## Remaining Backlog

All primalSpring Phase 60 items for petalTongue are resolved. Remaining
backlog is internal evolution:

- aarch64 musl cross-compile for headless
- Audio backend wire protocols via `audio.play` capability discovery
- Overlay mode (display capability Phase 2)
- egui texture resolution (`TextureResolver`)
- `crypto.sign` delegation to security provider
- Phase 3 self-hosted sporePrint (petalTongue + Songbird + NestGate)
