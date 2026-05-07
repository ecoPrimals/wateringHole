# barraCuda — Stateful Session API Architecture Advisory

**Date**: 2026-05-07
**From**: barraCuda team
**To**: primalSpring, hotSpring, neuralSpring, toadStool
**Context**: primalSpring Phase 60 flagged 4 remaining JSON-RPC surface gaps (GAP-11: 14/18 closed, 4 deferred) as "pending session infrastructure." This advisory documents that the ecosystem already has building blocks for both architecture paths — no new infrastructure is required.

---

## Status of the 4 Deferred Methods

| Subsystem | Library implementation | JSON-RPC today | Blocker |
|---|---|---|---|
| ESN v2 | Full GPU tensor ESN (`esn_v2/model.rs`) + CPU classifier (`nn/esn_classifier.rs`) | None | Reservoir state persistence across temporal steps |
| Nautilus | Full evolutionary reservoir brain (`nautilus/`) with `to_json`/`from_json` | None | Population state too large to round-trip per call |
| Batched ODE | CPU + GPU integrators (`BatchedOdeRK4`, `BatchedOdeRK45F64`) | None | Multi-step state (`y`, `t`, `dt`) between calls |
| SimpleMlp | Inference only (`nn/simple_mlp.rs`) | `ml.mlp_forward` (stateless) | Training API doesn't exist in library — library gap, not IPC gap |

---

## Two Viable Architecture Paths

### Path A: Stateless with Client-Managed Snapshots

Client sends full state each call; server reconstructs, processes, returns updated state. Already proven by `ml.mlp_forward`.

```
Client                              barraCuda
  |                                    |
  |-- esn.predict({weights, state, input}) -->|
  |                                    |-- deserialize weights + state
  |                                    |-- run predict
  |<-- {result, updated_state} --------|
  |                                    |
  (client persists updated_state)
```

**Pros**: Zero server state, horizontally scalable, crash-safe, no TTL/eviction.
**Cons**: Bandwidth for large state (ESN reservoir: `reservoir_size²` floats). Unusable for Nautilus (population too large).

**Suitable for**: Batched ODE (state vector is small), SimpleMlp (already done), ESN single-shot prediction.

### Path B: Server-Side Session Handles

Adopt toadStool's `job_id` pattern. Server holds state keyed by handle with TTL eviction.

```
Client                              barraCuda
  |                                    |
  |-- esn.create({config}) ----------->|
  |<-- {handle: "abc123"} -------------|  (server allocates ESN, stores by handle)
  |                                    |
  |-- esn.train({handle, data}) ------>|
  |<-- {status: "trained"} ------------|  (server mutates ESN in place)
  |                                    |
  |-- esn.predict({handle, input}) --->|
  |<-- {result, state_hash} -----------|  (reservoir advances)
  |                                    |
  |-- esn.export({handle}) ----------->|
  |<-- {weights_json} -----------------|  (snapshot for persistence)
```

**Pros**: Minimal wire overhead, natural for temporal streaming, matches toadStool patterns.
**Cons**: Server state requires TTL eviction, not horizontally scalable without session affinity.

**Suitable for**: ESN streaming prediction, Nautilus (mandatory), batched ODE multi-step integration.

---

## Existing Building Blocks (Overlooked by Downstream)

### In toadStool (already live)

| Component | Location | Relevance |
|---|---|---|
| `job_id` lifecycle | `crates/server/src/pure_jsonrpc/handler/dispatch/mod.rs` | `compute.dispatch.submit` → `status` → `result` pattern is exactly Path B |
| Pipeline DAG | `crates/server/src/pure_jsonrpc/handler/dispatch/dag.rs` | Topological sort + `previous_results` injection between stages |
| `TrainedESN` type | `crates/distributed/src/types/execution.rs` | Serializable reservoir/input/output weight matrices + metrics |
| `SubstrateCapabilityKind::ReservoirCompute` | `crates/runtime/universal/src/backends/wgpu_backend/types.rs` | ESN already in the capability taxonomy |

### In barraCuda (already live)

| Component | Location | Serialization |
|---|---|---|
| ESN CPU | `crates/barracuda/src/nn/esn_classifier.rs` | `to_json` / `from_json` via `EsnWeights` |
| ESN v2 (GPU) | `crates/barracuda/src/esn_v2/model.rs` | `export_weights` / `import_weights` (`ExportedWeights`) |
| Nautilus Brain | `crates/barracuda/src/nautilus/` | `to_json` / `from_json` on `NautilusBrain` (population + readout + observations) |
| SimpleMlp | `crates/barracuda/src/nn/simple_mlp.rs` | `to_json` / `from_json` |
| Batched ODE | `crates/barracuda/src/numerical/ode_generic/` | State is `Vec<f64>` — trivially serializable |

### hotSpring metalForge — Orthogonal

metalForge is hardware probing/substrate routing. It **consumes** barraCuda for GPU/NPU dispatch but does not implement ESN/Nautilus/ODE/MLP. The implementations live solely in barraCuda's library crate.

---

## Shortest Path to Unblock (per subsystem)

### ESN

**Immediate (Path A, ~30 lines)**: Add `esn.predict` method that accepts `{weights, state, input}`, reconstructs `EsnClassifier` from JSON, runs `predict`, returns `{result, updated_state}`. Unblocks hotSpring QCD single-shot prediction.

**Follow-up (Path B)**: Add `esn.create` / `esn.train` / `esn.predict` / `esn.export` session methods for streaming temporal sequences. Model after toadStool's `compute.dispatch.submit` + status polling.

### Nautilus

**Path B only**: Population state is too large for round-trip. Add `nautilus.create` / `nautilus.observe` / `nautilus.train` / `nautilus.predict` / `nautilus.export` session methods. `NautilusBrain` already has `to_json`/`from_json` for checkpoint/restore.

### Batched ODE

**Path A (natural fit)**: Add `ode.step` method that accepts `{system, y, t, dt, n_steps, params}`, integrates `n_steps`, returns `{y_final, t_final}`. Client manages continuation. State vector is small (batch_size × n_vars floats).

### SimpleMlp

**Already done**: `ml.mlp_forward` implements Path A. Training API is a **library gap** (no `train` method exists in `SimpleMlp`), not a JSON-RPC surface gap. If training is needed, it belongs in the library first.

---

## toadStool Coordination Opportunity

toadStool's `TrainedESN` type + pipeline DAG enables multi-primal ESN workflows:

1. `compute.dispatch.pipeline.submit` on toadStool with stages:
   - Stage 1: Generate reservoir weights (NPU/spectral radius)
   - Stage 2: Forward to barraCuda `esn.train` with training data
   - Stage 3: Export trained weights via `esn.export`
2. toadStool's `previous_results` injection passes state between stages automatically
3. Final trained weights stored in NestGate or returned to caller

This is the "Level 5 primal proof" pattern: toadStool orchestrates, barraCuda computes, NestGate persists.

---

## Recommendation

No blocking infrastructure is missing. The deferred status was correct at the time but the ecosystem has evolved. Suggested sprint ordering:

1. **Sprint N**: `ode.step` (Path A, smallest surface area, immediate value for hotSpring/airSpring)
2. **Sprint N+1**: `esn.predict` (Path A single-shot, unblocks hotSpring QCD)
3. **Sprint N+2**: `esn.create`/`train`/`predict`/`export` (Path B session, streaming temporal)
4. **Sprint N+3**: `nautilus.*` session methods (Path B, larger surface area)

Each sprint is independent and incrementally valuable. No cross-primal coordination required for Sprints N and N+1.
