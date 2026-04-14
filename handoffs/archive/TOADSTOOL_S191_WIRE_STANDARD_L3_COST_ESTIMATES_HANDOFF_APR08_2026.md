# ToadStool S191 — Wire Standard L3 Cost Estimates + Deep Debt Audit

**Date**: April 8, 2026
**From**: ToadStool team
**To**: primalSpring / biomeOS / ecosystem
**Re**: Wire Standard L3 partial compliance, deep debt audit, documentation cleanup

---

## Summary

- **Wire Standard L3 (partial)**: `capabilities.list` now returns `cost_estimates` and `operation_dependencies`
- **Cost model**: Energy/time/compute intensity — not monetary. Dollar value is an end-user concern.
- **Last user-visible primal names**: 4 hardcoded strings cleaned from CLI (0 remaining)
- **Deep debt audit**: All clear — 0 production TODOs, unsafe contained, mocks gated
- **Debris**: Stale root `biome.yaml` removed

---

## Wire Standard L3: Cost Estimates

`capabilities.list` response now includes per-method `cost_estimates` with 5 dimensions:

| Field | Values | Purpose |
|-------|--------|---------|
| `cpu` | negligible / low / medium / high / variable | CPU intensity class |
| `gpu_eligible` | true / false | Whether GPU hardware may be engaged |
| `latency_ms` | integer (p50) | Expected response latency |
| `energy` | negligible / low / medium / high / variable | Energy consumption class |
| `memory_pressure` | none / low / medium / high / variable | Memory allocation pressure |

**Coverage**: 55+ methods across all 11 namespaces (health, capabilities, identity, toadstool, compute, shader, gpu, gate, transport, ember, resources).

### Example entries

```json
"cost_estimates": {
  "health.liveness": {"cpu": "negligible", "gpu_eligible": false, "latency_ms": 0, "energy": "negligible", "memory_pressure": "none"},
  "compute.submit":  {"cpu": "variable",   "gpu_eligible": true,  "latency_ms": 50, "energy": "variable",   "memory_pressure": "variable"},
  "shader.dispatch": {"cpu": "high",       "gpu_eligible": true,  "latency_ms": 100, "energy": "high",      "memory_pressure": "high"}
}
```

## Wire Standard L3: Operation Dependencies

`capabilities.list` response now includes `operation_dependencies` — a DAG of method prerequisites:

```json
"operation_dependencies": {
  "compute.status":  ["compute.submit"],
  "compute.result":  ["compute.submit"],
  "transport.stream": ["transport.open"],
  "compute.hardware.distill": ["compute.hardware.observe"],
  ...
}
```

**Coverage**: 20+ dependency chains covering compute lifecycle, hardware learning pipeline, transport sessions, and gate routing.

---

## Socket Verification

```bash
# Start server
toadstool server --socket /run/user/$UID/biomeos/toadstool.jsonrpc.sock

# Verify cost_estimates in capabilities.list
echo '{"jsonrpc":"2.0","method":"capabilities.list","id":1}' | \
  socat - UNIX-CONNECT:/run/user/$UID/biomeos/toadstool.jsonrpc.sock | \
  jq '.result.cost_estimates["health.liveness"]'
# → {"cpu":"negligible","energy":"negligible","gpu_eligible":false,"latency_ms":0,"memory_pressure":"none"}

echo '{"jsonrpc":"2.0","method":"capabilities.list","id":2}' | \
  socat - UNIX-CONNECT:/run/user/$UID/biomeos/toadstool.jsonrpc.sock | \
  jq '.result.operation_dependencies["compute.status"]'
# → ["compute.submit"]
```

---

## Quality Gates (S191)

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | 0 warnings |
| `cargo test --all-targets` | **21,514 tests, 0 failures** |
| Production TODOs | 0 |
| User-visible primal names | 0 |

---

## Remaining L3 Work

Wire Standard L3 is **partial** — the following would complete full compliance:

- **Dynamic cost updates**: Currently static estimates. Could evolve to runtime-adjusted based on actual telemetry (gpu.query_telemetry → power_watts, queue depth → estimated_wait_ms).
- **Workload-specific estimation**: `compute.submit` marked "variable" — could accept workload params and return specific estimates via a `cost.estimate` method.

---

## Changed Files

| File | Change |
|------|--------|
| `crates/server/src/pure_jsonrpc/handler/core.rs` | +`cost_estimates()`, +`operation_dependencies()`, test coverage |
| `crates/cli/src/cli_root.rs` | "BearDog cryptographic security" → "Cryptographic security" |
| `crates/cli/src/commands/dispatch/manifest.rs` | "BearDog Required" → "Security Required" |
| `crates/cli/src/ecosystem/adapters/universal.rs` | 4× "Songbird" → "coordination service" |
| `biome.yaml` (root) | Deleted — stale artifact with hardcoded names |

---

AGPL-3.0-or-later — ecoPrimals sovereign community property
