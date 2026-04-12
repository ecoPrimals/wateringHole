# ToadStool S203d — LD-04 Resolution: BTSP Auto-Detect + Env-Safe Tests

**Date**: April 12, 2026
**Session**: S203d
**Primal**: toadStool
**Author**: toadStool team
**Prior**: S203c (deep debt: smart file refactoring + stub deprecation)
**Context**: primalSpring downstream audit LD-04 partial blocker resolution

---

## Summary

Resolved the LD-04 partial blocker: BTSP-enabled sockets now auto-detect
plain-text connections and degrade gracefully to JSON-RPC, allowing
primalSpring's `CompositionContext` to reach compute capabilities without
implementing BTSP client framing. Also hardened 2 env-dependent tests.

## Changes

### BTSP Plain-Text Auto-Detect

**Problem**: When `FAMILY_ID` is set (production), `serve_unix` routed ALL
connections to `handle_btsp_connection`, which expected a BTSP handshake.
primalSpring sends plain newline-delimited JSON-RPC → `Broken pipe`.

**Fix**: `handle_btsp_connection` reads the first byte of each connection:
- **Binary** (first byte < 0x09): BTSP length-prefixed frame — proceeds
  with full handshake via `PrependByte<S>` adapter that re-injects the
  consumed byte into the stream
- **Text** (first byte >= 0x09): plain JSON-RPC/HTTP — graceful fallback
  to the existing NDJSON/HTTP keep-alive handler

Detection is instant (no timeout) and zero-copy. Both `#[cfg(feature = "btsp")]`
and `#[cfg(not(feature = "btsp"))]` paths updated.

### Env-Dependent Test Hardening

| Test | Before | After |
|------|--------|-------|
| `test_connect_refused` | Hardcoded port 19999 | Ephemeral bind-then-drop |
| `verify_service_localhost_unbound` | Hardcoded port 65535 | Ephemeral bind-then-drop |

## For primalSpring

- **LD-04**: RESOLVED — plain JSON-RPC now works on BTSP-enabled sockets
- `CompositionContext` can connect to `compute.sock` (or `compute-{fid}.sock`)
  and send newline-delimited JSON-RPC without BTSP client framing
- No socket naming changes from S203b (`compute.sock` + `compute-tarpc.sock`)

## Code Health (S203d State)

| Metric | Value |
|--------|-------|
| Clippy | 0 warnings (workspace-wide --all-targets) |
| Tests | 0 failures (full workspace) |
| New tests | +7 (BTSP auto-detect + plaintext byte detection) |
