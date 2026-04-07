# ToadStool S189 — GAP-MATRIX-05 Resolution: Server Mode Documentation

**Date**: April 7, 2026
**From**: ToadStool team
**To**: primalSpring, biomeOS team, downstream springs
**Re**: GAP-MATRIX-05 (Medium) — "CLI-only, no persistent server mode documented"

---

## Summary

GAP-MATRIX-05 flagged ToadStool as "CLI-only (no persistent server mode)".
This was a **documentation gap, not a feature gap**. ToadStool has had full
persistent server mode since S169. The issue was that reference documentation
had incorrect socket paths and outdated CLI invocations, making it impossible
for primalSpring's live validation matrix to confirm compliance.

## What Was Fixed

### 1. `docs/reference/SERVER_METHODS.md` — Complete Rewrite

**Before**: Documented ~15 methods. Socket path was wrong
(`$XDG_RUNTIME_DIR/toadstool.sock` — missing `biomeos/`). Only mentioned
one socket. No startup instructions.

**After**: Documents all ~67 JSON-RPC methods across 11 namespaces. Correct
dual-socket paths. Full CLI flags reference. Startup/verification examples.

### 2. `docs/daemon/DAEMON_MODE_USER_GUIDE.md` — CLI Corrections

**Before**: `toadstool daemon start` / `toadstool daemon stop` — neither
subcommand exists. The actual invocations are `toadstool server` or
`toadstool daemon` (no `start`/`stop` — just SIGTERM to stop).

**After**: Correct invocations, dual-socket table, `socat` verification
examples for `health.liveness` and `capabilities.list`.

### 3. `CONTEXT.md` — No Changes Needed

Already had correct `$XDG_RUNTIME_DIR/biomeos/toadstool.sock` + `compute.sock`
capability symlink documentation.

## GAP-MATRIX-05 Work Items — Confirmation

### 1. Server/daemon mode exists — CLI flags documented

```bash
toadstool server [--register] [--port PORT] [--socket PATH] [--config PATH]
                 [--max-workloads N] [--biomeos-socket PATH] [--family-id ID]
```

`toadstool daemon` is a backward-compatible alias (same code path).

### 2. `capabilities.list` returns compute capabilities — Confirmed

```
Method: capabilities.list
Aliases: capability.list, primal.capabilities, compute.capabilities
Handler: workload::query_capabilities()
```

Returns the full compute capability set for the running instance.

### 3. GPU capability routing — Confirmed

The `compute.*` namespace provides full GPU job queue access:

- `compute.submit` / `compute.status` / `compute.result` / `compute.cancel` / `compute.list`
- `compute.dispatch.*` (VFIO/DRM passthrough)
- `compute.hardware.*` (hardware learning, auto-init)
- `compute.performance_surface.*` (silicon performance routing)
- `compute.route.multi_unit` (multi-functional-unit routing)
- `shader.dispatch` (sovereign shader dispatch)

### Socket Paths

| Socket | Path |
|--------|------|
| JSON-RPC | `$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock` |
| tarpc | `$XDG_RUNTIME_DIR/biomeos/toadstool.sock` |
| Capability symlink | `$XDG_RUNTIME_DIR/biomeos/compute.sock` |

### Live Validation Command

```bash
# Start ToadStool server
toadstool server &

# Verify health
echo '{"jsonrpc":"2.0","method":"health.liveness","id":1}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock

# Verify capabilities
echo '{"jsonrpc":"2.0","method":"capabilities.list","id":2}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock
```

## Quality Gates

All passing after documentation updates:

- `cargo fmt --all -- --check` — 0 diffs
- `cargo clippy --workspace --all-targets -- -D warnings` — 0 warnings
- `cargo doc --workspace --no-deps --document-private-items` — 0 warnings

---

**License**: AGPL-3.0-or-later
