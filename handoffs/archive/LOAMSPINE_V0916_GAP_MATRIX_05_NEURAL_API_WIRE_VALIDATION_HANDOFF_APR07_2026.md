<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — GAP-MATRIX-05 Resolution: Neural API Wire-Format Validation

**Date**: April 7, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Type**: Gap Resolution  
**Gap**: GAP-MATRIX-05 (Medium) — Provenance Trio not live-tested through Neural API  
**Source**: `PRIMALSPRING_V093_LIVE_VALIDATION_GAP_MATRIX_HANDOFF_APR07_2026.md`

---

## Summary

Resolved GAP-MATRIX-05 for loamSpine by adding 3 UDS wire-format integration tests that validate the exact JSON-RPC responses biomeOS Neural API receives when probing `health.liveness` and `capabilities.list` through the Unix domain socket. The existing UDS connectivity test was strengthened from "result or error exists" to full wire-format assertion.

---

## Gap Requirements (from handoff)

| # | Requirement | Status |
|---|---|---|
| 1 | Confirm primal starts and creates a socket | **PASS** — `uds_server_starts_and_accepts_connections` validates socket file creation, `handle.path()` match |
| 2 | Verify `health.liveness` responds correctly | **PASS** — `uds_health_liveness_wire_format` validates full envelope |
| 3 | Verify `capabilities.list` returns biomeOS-parseable format | **PASS** — `uds_capabilities_list_wire_format` validates Format D structure |
| 4 | Report CLI flags needed for socket creation | See below |

---

## Tests Added

### `uds_health_liveness_wire_format`

Sends `health.liveness` over UDS, validates:
- JSON-RPC 2.0 envelope (`jsonrpc: "2.0"`, `id` echo)
- No `error` field
- Result is exactly `{"status": "alive"}` (Semantic Method Naming Standard v2.1)
- Result object contains only the `status` key (no extra fields)

### `uds_capabilities_list_wire_format`

Sends `capabilities.list` (canonical name) over UDS, validates:
- JSON-RPC 2.0 envelope, no error
- `result.primal` is `"loamspine"` (primal identity)
- `result.version` is semver-like string
- `result.capabilities` is non-empty array of strings (biomeOS Format A/D)
  - Contains `"permanence"` and `"session.commit"` (core capabilities)
- `result.methods` is non-empty array of objects, each with `method`, `domain`, `cost`, `deps` keys
- `result.operation_dependencies` is an object (DAG for Pathway Learner)
- `result.cost_estimates` is an object with valid structure (latency_ms, cpu, etc.)

### `uds_capabilities_list_legacy_alias`

Sends `capability.list` (legacy alias) over UDS, validates it resolves to the same capabilities response — ensuring backward compatibility for biomeOS versions using the old method name.

### Strengthened: `uds_server_starts_and_accepts_connections`

Previous assertion: `response.get("result").is_some() || response.get("error").is_some()`

New assertion: Full wire-format validation — `jsonrpc: "2.0"`, `id: 1`, `result.status: "alive"`.

---

## CLI Flags for Socket Creation

LoamSpine creates its UDS socket automatically at startup. No special flags required.

**Default socket path resolution** (5-tier, `neural_api/socket.rs`):
1. `$LOAMSPINE_SOCKET` environment variable (explicit override)
2. `$XDG_RUNTIME_DIR/biomeos/loamspine-{family}.sock` (standard)
3. `/run/user/{uid}/biomeos/loamspine.sock` (Linux procfs fallback)
4. `{temp_dir}/biomeos/loamspine.sock` (cross-platform fallback)

**Relevant CLI flags**:
- `--jsonrpc-port` / `--port`: TCP JSON-RPC port (default 9400, not needed for UDS)
- No flag for socket path — use `$LOAMSPINE_SOCKET` env var to override

---

## biomeOS Format Compatibility

LoamSpine's `capabilities.list` response uses **Format D** from primalSpring's 5-format parser:

```json
{
  "primal": "loamspine",
  "version": "0.9.16",
  "capabilities": ["permanence", "session.commit", ...],
  "methods": [{"method": "spine.create", "domain": "spine", "cost": "low", "deps": []}],
  "operation_dependencies": {"entry.append": ["spine.create"]},
  "cost_estimates": {"health.check": {"latency_ms": 1, "cpu": "low", ...}}
}
```

biomeOS extracts capabilities from `result.capabilities` (string array). The `methods`, `operation_dependencies`, and `cost_estimates` fields are consumed by Pathway Learner for routing optimization.

---

## Verification

```
cargo clippy --all-targets   # 0 warnings
cargo test                   # 1,301 tests, 0 failures
```

---

## Remaining (out of scope for loamSpine team)

- **Live validation run**: These tests validate the wire format in CI. A live validation run with biomeOS v2.93+ routing through Neural API requires biomeOS to be running — coordinated by primalSpring team.
- **rhizoCrypt, sweetGrass**: GAP-MATRIX-05 applies to the full trio; their teams address independently.
