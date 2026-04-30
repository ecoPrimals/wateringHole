# biomeOS v3.33 — Phase 57: BTSP Opt-Out, Diagnostic Rejection, Spring Compatibility

**Date**: April 30, 2026
**From**: biomeOS team
**Triggered by**: primalSpring v0.9.24 remote plasmidBin validation audit
**Status**: Shipped and pushed

---

## Summary

Resolves 3 gaps from primalSpring Phase 57 audit. All stem from BTSP enforcement silently dropping connections from springs that send raw JSON-RPC without a handshake.

## Changes

### GAP-17/18: graph.list and health.liveness silent failures (P1)
- **Root cause**: `handle_connection_with_btsp` returned `Ok(())` with zero bytes written when BTSP enforcement rejected a raw JSON-RPC client.
- **Fix**: BTSP rejection now sends a JSON-RPC error (`-32000`) explaining the requirement and how to bypass it. Clients get actionable diagnostics instead of silence.
- `graph.list`, `graph.status`, `graph.save`, `health.liveness` — all wired and functional. The issue was transport-layer, not handler-level.

### GAP-19: --btsp-optional flag (P1)
- New CLI: `biomeos neural-api --btsp-optional`
- Disables BTSP enforcement for the server session
- `NeuralApiServer::with_btsp_optional()` builder method
- `btsp.status` RPC reflects the optional state
- Startup banner logs "BTSP: optional (--btsp-optional)"
- Equivalent to `BIOMEOS_BTSP_ENFORCE=0` but explicit and discoverable

## For downstream springs

Instead of:
```bash
BIOMEOS_BTSP_ENFORCE=0 biomeos neural-api --graphs-dir /path/to/graphs
```

You can now use:
```bash
biomeos neural-api --btsp-optional --graphs-dir /path/to/graphs
```

If you forget, the server returns a clear error message explaining the fix.

## Verification

- `cargo check`: PASS
- `cargo clippy -- -D warnings`: PASS (0 warnings)
- `cargo fmt --check`: PASS
- `cargo test --workspace --no-fail-fast`: 8,064+ tests
