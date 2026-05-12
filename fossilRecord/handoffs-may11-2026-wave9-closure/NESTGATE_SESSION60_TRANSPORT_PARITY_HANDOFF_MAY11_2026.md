# NestGate Session 60 — content.* Transport Parity Resolution

**Date**: May 11, 2026
**Primal**: NestGate
**Commit**: `98f5d28a2` (Session 60: content.* transport parity + lifecycle.status)
**Priority**: Was **CRITICAL PATH** — now **RESOLVED**

## What Was the Gap

NestGate had implemented all `content.*` methods (`put`, `get`, `exists`, `list`,
`publish`, `resolve`, `promote`, `collections`) on the **primary
unix_socket_server dispatch path** — but these methods were **not routed** through
the other three transport surfaces:

- `SemanticRouter::call_method` — only `storage.*`, health, session, crypto
- Isomorphic IPC `UnixSocketRpcHandler` — dispatch ended before `content.*`
- HTTP API `NestGateRpcHandler` + `NestGateJsonRpcHandler` — narrow `storage.*` subset

Callers on those paths got "Method not found."

## What Was Shipped

All 8 `content.*` methods wired on **all 4 transport surfaces**:

| Transport | Status |
|-----------|--------|
| Primary `unix_socket_server/dispatch.rs` | YES (existing) |
| `SemanticRouter::call_method` | **YES** — new `content.rs` module |
| Isomorphic IPC `UnixSocketRpcHandler` | **YES** — new delegation block |
| HTTP API `NestGateRpcHandler` + `NestGateJsonRpcHandler` | **YES** — new `handle_content_method` + transport handlers |

Additionally:
- `lifecycle.status` handler added on all 4 surfaces
- Public `content_ops` facade created for stateless cross-crate access

## What This Unblocks

- **projectNUCLEUS Pillars 1-3**: `publish_sporeprint.sh` can now publish content
- **petalTongue `backend=nestgate`**: `content.get`/`content.resolve` reachable
- **Sovereign content pipeline**: content → NestGate → primals.eco serving
- **plasmidBin hosting via NestGate**: binary artifacts addressable
- **Foundation geological layers**: content storage for scientific data
- **primalSpring gate tests**: W7-02/03/04/05/07 all now exercisable

## Validation

primalSpring already has:
- Scenario `s_nestgate_content_pipeline` testing `content.put`/`get`/`exists`/`list`/`resolve`
- 3 gate tests in `server_ecosystem_compose.rs` (Content Gate 1-3)
- Deploy graph `content_pipeline_smoke.toml`
- Inverse drift detection confirming `content.*` domain coverage

## Downstream Impact

This was the **last critical L1 upstream debt item**. With this resolved:
- L1 (Primals): **CLEAN** — 13/13 structural + semantic, zero critical gaps
- All downstream-surfaced per-primal composition debt is closed
- projectNUCLEUS can proceed with re-ingestion and Pillar 1-3 shadow runs
