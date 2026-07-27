# rhizoCrypt Wave 155b — BTSP-DAG Bridge + Cross-Gate Provenance

**Date**: Jul 27, 2026 | **Wave**: 155b | **Head**: `ed81f19`

## Summary

Two-phase evolution for Nest Atomic G3:

**Phase 0** — BTSP-DAG Bridge: Bridges BTSP transport authentication into
DAG method authorization. Family-authenticated callers auto-granted DAG access.
Mesh trust events signed. Federate hardened with signature verification.

**Phase 1** — Cross-Gate Provenance: Wires the federate path into the
provenance notifier so imported vertices push a `ProvenanceChain` to sweetGrass.
Dehydration wire summaries enriched with `tier: "gateway"` witnesses for
content imported from remote gates.

## What Shipped

| Component | Change |
|-----------|--------|
| `ConnectionOrigin::BtspAuthenticated` | BTSP handshake completion flows into method gate |
| `CallerContext::btsp_authenticated()` | All post-BTSP paths use BTSP-aware caller context |
| `MethodGate::check` | BTSP-authenticated callers auto-granted all method scopes |
| `spawn_mesh_poller` | Signs trust event vertices via `SigningClient` when available |
| `FederateRequest.source_gate` | Gate origin stamped on imported vertices |
| `FederateRequest.verify_signatures` | Opt-in signature verification on import |
| `FederateResponse.rejected` | Count of vertices rejected (invalid signatures) |
| `impl_federate → notify_provenance` | Federated vertices pushed to sweetGrass as ProvenanceChain |
| `provenance_notifier()` getter | RPC layer can now reach the provenance notifier |
| `notify_dehydration_enriched()` | Appends gateway-tier witnesses to dehydration wire summary |
| `collect_gateway_witnesses()` | Scans vertices for `source_gate` → `WireWitnessRef{tier:"gateway"}` |

## Architecture

```
Federate path (cross-gate provenance):
  remote → dag.federate → verify sigs → stamp source_gate
    → federate_vertices() → DAG
    → build ProvenanceChain → notify_provenance() → sweetGrass

Dehydration path (gateway witnesses):
  dehydrate → generate_summary → collect_gateway_witnesses()
    → notify_dehydration_enriched() → sweetGrass
      (witnesses now include tier:"gateway" for federated content)
```

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,901 (+18 over pre-155b) |
| Source files | 225 `.rs` |
| Lines | ~62,665 |
| Coverage | 93.83% |
| Clippy | 0 warnings |
| cargo deny | CLEAN |

## Upstream Status

rhizoCrypt G3 work (Nest Atomic Phase 0) is **SHIPPED**:
- BTSP → DAG bridge: **DONE**
- Mesh poller signing: **DONE**
- Federate hardening: **DONE**
- Cross-repo provenance metadata: **DONE**
- Federate → sweetGrass provenance push: **DONE**
- Gateway-tier dehydration witnesses: **DONE**
- Remaining for full G3: loamSpine certificate minting, sweetGrass attribution braids
