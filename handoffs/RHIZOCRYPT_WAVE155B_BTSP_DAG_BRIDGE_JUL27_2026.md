# rhizoCrypt Wave 155b — BTSP-DAG Bridge + Federate Hardening

**Date**: Jul 27, 2026 | **Wave**: 155b

## Summary

Bridges BTSP transport authentication into DAG method authorization and
hardens the federate path for cross-repo provenance. This is Phase 0 of
the Nest Atomic wiring — BTSP-authenticated family members now have
implicit DAG access, mesh trust events are signed, and federated vertices
carry source-gate provenance metadata.

## What Shipped

| Component | Change |
|-----------|--------|
| `ConnectionOrigin::BtspAuthenticated` | New variant — BTSP handshake completion flows into method gate |
| `CallerContext::btsp_authenticated()` | All post-BTSP paths use BTSP-aware caller context |
| `MethodGate::check` | BTSP-authenticated callers auto-granted all method scopes |
| `spawn_mesh_poller` | Signs trust event vertices via `SigningClient` when available |
| `FederateRequest.source_gate` | Cross-repo provenance — gate origin stamped on imported vertices |
| `FederateRequest.verify_signatures` | Opt-in signature verification before accepting remote vertices |
| `FederateResponse.rejected` | Count of vertices rejected due to invalid signatures |

## Architecture

```
Before (parallel, disconnected):
  BTSP handshake → CallerContext::unix() → MethodGate sees "unauthenticated"
  
After (bridged):
  BTSP handshake → CallerContext::btsp_authenticated() → MethodGate auto-grants
```

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,893 (+10) |
| Source files | 225 `.rs` |
| Lines | ~62,282 |
| Coverage | 93.83% |
| Clippy | 0 warnings |
| cargo deny | CLEAN |

## Upstream Status

rhizoCrypt G3 work (Nest Atomic Phase 0) is **in progress**:
- BTSP → DAG bridge: **DONE** (this wave)
- Mesh poller signing: **DONE** (this wave)
- Federate hardening: **DONE** (this wave)
- Cross-repo provenance metadata: **DONE** (this wave)
- Remaining: loamSpine/sweetGrass cross-gate provenance chain push (Phase 1)
