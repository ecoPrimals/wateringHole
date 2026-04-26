# biomeOS v3.25 — Graph Bootstrap Pre-Registration + BTSP Escalation

**Date**: April 25, 2026
**From**: biomeOS v3.25
**Scope**: primalSpring Phase 45c downstream audit resolution — graph bootstrapping + BTSP participation

---

## What Changed

### Gap 1 — Graph Bootstrap Pre-Registration (RESOLVED)

**Problem**: `capability.call` returned "Primal not found" because the NeuralRouter
route table was empty at startup. Graph TOML files were parseable, but
`load_translations_from_all_graphs()` only loaded translation mappings (method name
conversions), not actual routes (capability → primal → socket path). Routes were
only populated by `discover_and_register_primals()` which scans for *live* sockets —
useless when biomeOS starts before primals.

**Fix**: New `register_capabilities_from_graphs()` function in `discovery_init.rs`.
Runs after translation loading and before live discovery. For each graph node:
1. Extracts primal name from `primal.by_capability` or `primal.by_name`
2. Extracts capabilities from `node.capabilities` + `node.capabilities_provided`
3. Computes expected socket path: `{socket_dir}/{primal}-{family_id}.sock`
4. Registers all capabilities in the NeuralRouter as `graph-bootstrap` source

Startup sequence is now:
```
4a. load_translations_on_startup()         — Tower Atomic translations
4b. load_translations_from_all_graphs()    — translation overlay from all graphs
4c. register_capabilities_from_graphs()    — PRE-REGISTER routes from graph nodes ← NEW
4d. log_graph_inventory()                  — diagnostic logging
5.  discover_and_register_primals()        — update with live socket endpoints
```

**Test**: After startup, `ipc.resolve --capability tensor` should return the
expected barraCuda socket path. `capability.call("tensor", "tensor.matmul", params)`
will attempt to connect to that socket.

### Gap 2 — BTSP Runtime Escalation (RESOLVED)

**Problem**: biomeOS starts with `BIOMEOS_BTSP_ENFORCE=0` (cleartext bootstrap)
because it launches before BearDog. After Tower is healthy, biomeOS stays in
cleartext mode permanently — no mechanism to escalate.

**Fix**: Added runtime BTSP enforcement via `AtomicBool` flag + two new RPC methods:

- **`btsp.escalate`**: Sets the runtime flag to `true`. All subsequent UDS connections
  require BTSP authentication. One-way transition (cannot un-escalate). Returns
  `{"escalated": true, "previously_escalated": bool}`.

- **`btsp.status`**: Reports `has_family_id`, `static_enforce`, `runtime_escalated`,
  and `effective_enforce` (logical OR of static + runtime).

The `accept_connections` loop now checks:
```rust
let enforce = static_enforce || escalated.load(Ordering::Relaxed);
```

**Usage**: After NUCLEUS is fully up and Tower is healthy:
```json
{"jsonrpc":"2.0","method":"btsp.escalate","id":1}
```
Or call `btsp.escalate` automatically from the bootstrap sequence when
`transition_to_coordinated` confirms Tower health.

### Gap 3 — Tensor Capability Translations (ALREADY RESOLVED)

**Confirmed**: `capability_registry.toml` already contains `[domains.tensor]` +
`[translations.tensor]` with 33 entries covering all barraCuda Sprint 44 methods:
- tensor.create/matmul/matmul_inline/add/scale/clamp/reduce/sigmoid/transpose/batch.submit
- math.sigmoid/log2/relu/tanh/softmax
- stats.mean/std_dev/weighted_mean/variance/median/correlation
- noise.perlin2d/perlin3d/simplex2d/simplex3d
- activation.fitts/hick
- linalg.solve/eigenvalues
- spectral.fft/power_spectrum
- rng.uniform/normal/seed

No code change was needed.

---

## Verification

```
cargo check --workspace     # 0 errors
cargo clippy -- -D warnings # 0 warnings
cargo test --workspace      # 7,814 pass, 0 failures
cargo fmt --check           # clean
```

---

## What Remains (Evolution Targets)

1. **Automatic BTSP escalation**: Wire `btsp.escalate` into `transition_to_coordinated`
   so biomeOS auto-escalates when Tower health is confirmed. Currently requires an
   external caller (e.g., graph executor or launcher).

2. **Graph-based deployment via Neural API**: With routes pre-registered, `biomeos deploy
   --graph nucleus_complete.toml` should now populate the route table. Full end-to-end
   validation with primalSpring's `nucleus_complete.toml` is the next integration test.

3. **Tower routing evolution**: Long-term, biomeOS delegates all transport to Songbird
   mesh relay + BearDog BTSP instead of doing its own socket forwarding.

---

## References

| Document | Location |
|----------|----------|
| primalSpring Phase 45c guidance | `wateringHole/handoffs/PRIMALSPRING_PHASE45C_BTSP_CONVERGED_UPSTREAM_GUIDANCE_APR2026.md` |
| BTSP relay pattern | `wateringHole/SOURDOUGH_BTSP_RELAY_PATTERN.md` |
| BTSP wire convergence | `wateringHole/handoffs/BTSP_WIRE_CONVERGENCE_APR24_2026.md` |
| Graph bootstrap code | `crates/biomeos-atomic-deploy/src/neural_api_server/discovery_init.rs` |
| BTSP escalation code | `crates/biomeos-atomic-deploy/src/neural_api_server/listeners.rs` |
| Route table | `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` |
| Capability registry | `config/capability_registry.toml` |
