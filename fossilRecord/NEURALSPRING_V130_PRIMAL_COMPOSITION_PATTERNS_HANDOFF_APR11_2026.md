# NEURALSPRING V130 — Primal Composition Patterns for Ecosystem Absorption

<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

> **From:** neuralSpring (S180) | **To:** primal teams, spring teams, biomeOS, primalSpring
> **Date:** 2026-04-11 | **Scope:** Composition patterns, deployment standard compliance, NUCLEUS deployment via Neural API

---

## Context

neuralSpring completed a full-spectrum audit (S179–S180) against wateringHole
ecosystem standards, primalSpring composition guidance, and plasmidBin deployment
expectations. This handoff documents what we learned, what we fixed, and what
we hand back for primals and sibling springs to absorb.

The evolution path is now four layers:

```
Layer 1 — Science Fidelity:     Python baseline → Rust validation (provenance, tolerances)
Layer 2 — Compute Sovereignty:   Rust reference → barraCuda WGSL → GPU dispatch
Layer 3 — NUCLEUS Composition:   niche.rs → biomeOS IPC → health triad → capability routing
Layer 4 — Deployment:            ecoBin → plasmidBin → benchScale → composition probes
```

---

## What neuralSpring Now Speaks (S180)

### Deployment Health Triad (DEPLOYMENT_VALIDATION_STANDARD)

neuralSpring now implements the full triad required by benchScale:

| Method | Purpose | Handler |
|--------|---------|---------|
| `health.liveness` | Process alive? | `handle_liveness` |
| `health.readiness` | Subsystems ready? | `handle_readiness` |
| `health.check` | Combined health for smoke tests | `handle_health_check` |

**For primal teams:** Ensure your primal implements all three. `health.check`
returns a superset of liveness + readiness. benchScale and plasmidBin smoke
tests probe `health.check` first, falling back to liveness.

### T4 Discovery — `identity.get`

neuralSpring responds to `identity.get` with primal name, niche, version,
domain, license, and full capability list. This satisfies Ecosystem Compliance
Matrix Tier 4.

**For primal teams:** If you only respond to `health` or `capabilities.list`,
add `identity.get`. It enables automated compliance scanning without knowing
primal-specific method names.

### MCP Tool Listing — `mcp.tools.list`

neuralSpring now responds to `mcp.tools.list` directly on the primal JSON-RPC
surface (not only through a separate adapter). Returns all 27 capabilities as
discoverable tools with domain parsed from `domain.verb` naming.

**Pattern choice for springs/primals:** hotSpring exposes `mcp.tools.list` on
the primal. neuralSpring also has a richer MCP adapter in playGround that
registers via Squirrel `capability.announce` with JSON Schema per tool.
Both patterns are valid; the primal-surface one is simpler for composition
validators; the adapter is richer for AI discovery.

### Iterative Method Normalization

neuralSpring's dispatcher now iteratively strips multiple prefix variants
(`neuralspring.`, `neural-spring.`, `neural_spring.`) per SPRING_COMPOSITION_PATTERNS §1.

**For primal/spring teams:** If your dispatcher only strips one prefix,
consider the loop pattern for robustness against cross-spring routing.

---

## Upstream Fixes We Made (primalSpring, plasmidBin)

### primalSpring: Pipeline + Deploy Graph Fixes

**`graphs/neuralspring_inference_pipeline.toml`:**
- `binary = "neuralspring_primal"` → `"neuralspring"` (the actual binary name)
- `health_method = "neural.health"` → `"health.liveness"` (the actual method)

**`graphs/spring_deploy/neuralspring_deploy.toml`:**
- `binary = "neuralspring_primal"` → `"neuralspring"`
- `by_capability = "neural"` → `"inference"` (semantic, not primal-name)
- Capability set replaced: removed stale capabilities that neuralSpring
  doesn't advertise, added the 14 science + 3 inference capabilities
  that it actually does

**For primalSpring team:** These are committed in your tree. Please review.
The pattern issue affects other springs too — check that all `spring_deploy/`
graphs use the actual binary names from plasmidBin and actual health methods
from the primal dispatchers.

### plasmidBin: Metadata Refresh

**`neuralspring/metadata.toml`:**
- version: `0.7.0` → `0.1.0` (matches Cargo.toml)
- domain: `ml` → `science.learning` (matches `config.rs`)
- capabilities: 2 stale `ml.*` → 30-capability surface
- UniBin modes: `["server", "version"]` → `["serve", "health", "capabilities"]`
- built_at: `2026-03-28` → `2026-04-11`

**For infra team:** Other springs may have similar staleness in plasmidBin.

---

## What We Hand Back to Primals

### Squirrel — `inference.register_provider`

neuralSpring's `inference.*` handlers are stubs returning
`"provider": "stub", "status": "not_yet_wired"`. The gap is:
- Does Squirrel expose `inference.register_provider`?
- What is the wire format for provider registration?
- How does Squirrel route `inference.complete` to registered providers?

neuralSpring is ready to register as a provider once the wire exists.

### coralReef — `shader.compile.wgsl` for Multi-Stage ML

neuralSpring validates 41 WGSL shaders via barraCuda. For ML inference as
shader composition, we need coralReef to accept multi-stage WGSL programs
(tokenizer → embedding → attention → FFN) and compile them for target GPU.
Does `shader.compile.wgsl` accept pipeline descriptions, or only single shaders?

### toadStool — `compute.dispatch.submit` for Pipeline Scheduling

For fused multi-op inference, neuralSpring needs toadStool to schedule
shader pipelines (not just single dispatches). Is there a wire format for
ordered dispatch sequences? Or should each shader be dispatched individually?

### NestGate — `storage.retrieve` for Weight Tensors

neuralSpring loads model weights via local safetensors. For composed mode,
weights should come from NestGate. Key question: does `storage.retrieve`
support streaming large tensors (100MB+), or is it request/response?

### barraCuda — Feature-Gate Bug (Gap §9)

`special/plasma_dispersion.rs` unconditionally imports from
`ops::lattice::cpu_complex::Complex64`, but `ops::lattice` is gated behind
`domain-lattice`. neuralSpring works around this by enabling `domain-lattice`.
Fix: gate `plasma_dispersion` behind `domain-lattice`, or make `Complex64`
available without it.

### barraCuda — 29 Shader Absorption Candidates

See `docs/PRIMAL_GAPS.md` §10 for the full table. Highest priority:
`head_split.wgsl`, `head_concat.wgsl`, `linear_regression.wgsl`,
`matrix_correlation.wgsl`, `mean_reduce.wgsl` → upstream `stats` /
`ReduceScalarPipeline`.

---

## Proto-Nucleate Fragment Issue

`neuralspring_inference_proto_nucleate.toml` declares:
```
fragments = ["tower_atomic", "node_atomic", "meta_tier"]
```
but includes NestGate as a node. If NestGate is part of the composition,
`nest_atomic` should be in fragments. NestGate is `required = false`
(optional), but the fragment list should document this explicitly.

**For primalSpring team:** Either add `nest_atomic` to the proto-nucleate
fragment list, or add a comment explaining why it's omitted despite NestGate
being present.

---

## Patterns for Other Springs to Absorb

### The Composition Checklist (what S180 taught us)

1. **Deploy graph binary name** must match the actual `[[bin]]` name in Cargo.toml
   and plasmidBin metadata, not an internal source directory name.
2. **Health method** in graph nodes must match what the dispatcher actually routes
   (`health.liveness`, not `neural.health` or `compute.health`).
3. **Capability set** in deploy graphs must be refreshed when the niche surface
   evolves — stale graphs create false expectations for biomeOS.
4. **Fragment list** must include all atomics whose primals appear as nodes —
   even optional ones should be documented.
5. **plasmidBin metadata** drifts silently — add a CI check or manual review
   cadence.
6. **MCP tool definitions** should cover the full capability surface — any
   capability registered in `niche.rs` should have a corresponding MCP tool
   definition for AI discoverability.

### The Four-Layer Validation Stack

Springs validating composition readiness should test at all four layers:

```
1. Science:     validate_* binaries (Python → Rust parity)
2. GPU:         validate_gpu_* binaries (Rust → WGSL parity)
3. Composition: validate_nucleus_*/validate_inference_* (IPC, capabilities, graph)
4. Deployment:  health triad + identity.get + mcp.tools.list + ecoBin checks
```

---

## Status of neuralSpring's Primal Composition

| Primal | Wired? | Via |
|--------|--------|-----|
| biomeOS | YES | nucleus.register, capability.register, heartbeat, deregister |
| BearDog | NO | String constants only (no BTSP) |
| Songbird | NO | Filesystem scanning (no mesh) |
| coralReef | PARTIAL | playGround client; library uses local wgpu |
| toadStool | PARTIAL | playGround client; library uses local dispatch |
| barraCuda | DIRECT | Library import (correct for validation stage) |
| Squirrel | PARTIAL | playGround client + MCP adapter; primal stubs |
| NestGate | NO | Local safetensors only |
| petalTongue | YES | Optional visualization push |

Next priorities: Squirrel provider registration → coralReef pipeline compile →
NestGate weight retrieval → TensorSession adoption for fused pipelines.
