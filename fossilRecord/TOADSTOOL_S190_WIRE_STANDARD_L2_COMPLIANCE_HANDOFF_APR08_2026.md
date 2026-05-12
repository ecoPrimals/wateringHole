# ToadStool S190 — Capability Wire Standard L2 Compliance

**Date**: April 8, 2026
**From**: ToadStool team
**To**: primalSpring, biomeOS team, downstream springs
**Re**: GAP-MATRIX-05 catch-up sprint — Wire Standard L1/L2/partial L3

---

## Summary

ToadStool now implements the Capability Wire Standard v1.0 at **Level 2
(Standard)** with **partial Level 3 (Composable)** metadata. All three
required methods (`health.liveness`, `capabilities.list`, `identity.get`)
return wire-standard-compliant JSON envelopes. biomeOS can now auto-discover
and route `compute.*` domain calls.

---

## Wire Standard Compliance Checklist

### Level 1 (Routable) — COMPLETE

- [x] `capabilities.list` responds to JSON-RPC probe over UDS
- [x] Response parseable by biomeOS (`result.methods` flat array — priority 1 parse path)
- [x] `health.liveness` responds with `{"status": "alive", "healthy": true, ...}`

### Level 2 (Standard) — COMPLETE

- [x] `result` contains `"primal"` field (`"toadstool"`)
- [x] `result` contains `"version"` field (SemVer)
- [x] `result` contains `"methods"` flat string array (~67 methods, sorted)
- [x] Every entry in `"methods"` is callable (returns result or param error, not method-not-found)
- [x] Method names follow `domain.operation` dotted convention
- [x] `identity.get` implemented and returns `{primal, version, domain, license}`
- [x] `health.liveness`, `health.check`, `health.readiness` all implemented

### Level 3 (Composable) — PARTIAL

- [x] `provided_capabilities` grouping present (7 groups: compute, toadstool, gpu, gate, transport, shader, ember)
- [x] `consumed_capabilities` declared (security.sign, security.verify, storage.artifact.store/retrieve, coordination.register/discover)
- [ ] `cost_estimates` — not yet implemented
- [ ] `operation_dependencies` — not yet implemented

---

## What Changed

### `health.liveness` (+ aliases `health.check`, `health.readiness`, `toadstool.health`, `compute.health`)

**Before**: Returned `HealthStatus` struct (`healthy`, `version`, `uptime_secs`, etc.) — missing `"status": "alive"`.

**After**: Same rich response **plus** `"status": "alive"` field. biomeOS liveness probes now match.

### `capabilities.list` (+ aliases `capability.list`, `primal.capabilities`)

**Before**: Returned `ComputeCapabilities` hardware metadata (`compute_units`, `supported_workload_types`, `available_resources`). No method list. biomeOS could not extract routing information.

**After**: Returns wire-standard envelope:
```json
{
  "primal": "toadstool",
  "version": "0.1.0",
  "methods": ["ai.local_execute", "ai.local_inference", "capabilities.list", "compute.cancel", "compute.dispatch.submit", ...],
  "provided_capabilities": [
    {"type": "compute", "methods": ["submit", "status", ...], "description": "GPU job queue..."},
    {"type": "toadstool", "methods": ["submit_workload", ...], "description": "High-level workload executor"},
    {"type": "gpu", "methods": ["query_info", "query_memory", "query_telemetry"]},
    {"type": "gate", "methods": ["update", "remove", "list", "route"]},
    {"type": "transport", "methods": ["discover", "list", "route", "open", "stream", "status"]},
    {"type": "shader", "methods": ["dispatch"]},
    {"type": "ember", "methods": ["list", "status"]}
  ],
  "consumed_capabilities": ["security.sign", "security.verify", "storage.artifact.store", ...],
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp"]
}
```

`compute.capabilities` remains the hardware metadata endpoint for compute clients.

### `identity.get`

**Before**: Had `primal`, `version`, `protocol`, `capabilities`, `methods`, `transport`, `socket_name`. Missing `domain` and `license`.

**After**: Added `"domain": "compute"` and `"license": "AGPL-3.0-or-later"`.

---

## Socket Verification

```bash
# Start ToadStool
toadstool server &

# Wire Standard L1: health probe
echo '{"jsonrpc":"2.0","method":"health.liveness","id":1}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock
# → {"status":"alive","healthy":true,"version":"...","uptime_secs":...}

# Wire Standard L2: capabilities envelope
echo '{"jsonrpc":"2.0","method":"capabilities.list","id":2}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock
# → {"primal":"toadstool","version":"...","methods":[...67 methods...],"provided_capabilities":[...]}

# Wire Standard L2: identity
echo '{"jsonrpc":"2.0","method":"identity.get","id":3}' | \
  socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/biomeos/toadstool.jsonrpc.sock
# → {"primal":"toadstool","version":"...","domain":"compute","license":"AGPL-3.0-or-later",...}
```

## Quality Gates

- `cargo fmt --all -- --check` — 0 diffs
- `cargo clippy -p toadstool-server --all-targets -- -D warnings` — 0 warnings
- `cargo test -p toadstool-server --all-targets` — 36 passed, 0 failed
- `cargo test --all-targets` (full workspace) — 21,514+ passed, 0 failed

## Remaining L3 Work

- `cost_estimates` per method (cpu/latency hints for Squirrel AI routing)
- `operation_dependencies` (method DAG for execution planners)

---

**License**: AGPL-3.0-or-later
