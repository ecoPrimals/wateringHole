# Handoff: primalSpring v0.1.0 → toadStool / barraCuda — Coordination Validation Intelligence

**Date:** March 17, 2026  
**From:** primalSpring (coordination validation spring)  
**To:** toadStool (hardware dispatch), barraCuda (math primitives), coralReef (shader compiler)  
**License:** AGPL-3.0-or-later  
**Covers:** primalSpring v0.1.0 Phase 0→1

---

## Executive Summary

- primalSpring validates the coordination layer — it does NOT consume barraCuda math
- Zero direct dependency on barraCuda, toadStool, or coralReef crates
- All interaction is via IPC: `discover_primal()` + `PrimalClient` over Unix sockets
- 10 experiments directly exercise toadStool/barraCuda/coralReef coordination patterns
- The compute triangle (exp050) is the canonical integration test for the trio
- primalSpring's IPC patterns can inform toadStool/barraCuda JSON-RPC evolution

---

## What primalSpring Tests About toadStool/barraCuda/coralReef

### Direct Experiments

| Exp | What | Primals Exercised |
|-----|------|-------------------|
| 002 | Node Atomic bootstrap | Tower + toadStool: GPU dispatch via capability routing |
| 010 | Sequential graph | biomeOS coordinates toadStool in a dependency chain |
| 011 | Parallel graph | Concurrent toadStool capability calls |
| 012 | ConditionalDag graph | GPU dispatch with CPU fallback when toadStool unavailable |
| 014 | Continuous 60Hz tick | toadStool under sustained compute load |
| 025 | coralForge pipeline | coralReef compile → toadStool dispatch → barraCuda execute |
| 050 | Compute triangle | **Canonical test**: coralReef → toadStool → barraCuda live pipeline |
| 051 | Socket discovery sweep | Enumerate all primal sockets including toadStool/barraCuda |
| 052 | Protocol escalation | HTTP → JSON-RPC → tarpc negotiation (toadStool/NestGate) |
| 055 | Wait-for-health | Health probe pattern applied to toadStool startup ordering |

### Deploy Graph References

| Graph | toadStool Role |
|-------|----------------|
| `coralforge_pipeline.toml` | GPU dispatch node (compile → dispatch → execute) |
| `continuous_tick.toml` | Continuous compute at 60 Hz tick rate |
| `conditional_fallback.toml` | GPU dispatch with CPU fallback path |
| `parallel_capability_burst.toml` | Concurrent capability burst |
| `primalspring_deploy.toml` | Full niche deployment includes toadStool |

---

## IPC Conventions primalSpring Validates

### Socket Discovery

primalSpring implements and validates the standard discovery convention:

1. `$TOADSTOOL_SOCKET` env var (explicit override)
2. `$XDG_RUNTIME_DIR/biomeos/toadstool-default.sock` (XDG standard)
3. `{temp_dir}/biomeos/toadstool-default.sock` (fallback)

Same pattern for `barracuda` and `coralreef`.

### JSON-RPC 2.0 Protocol

primalSpring's `ipc::protocol` module validates the JSON-RPC 2.0 contract:

```json
{
  "jsonrpc": "2.0",
  "method": "compute.dispatch",
  "params": { "shader": "add.wgsl", "inputs": [...] },
  "id": 1
}
```

The `JsonRpcRequest` uses `AtomicU64` for unique IDs across concurrent calls.
This ensures no ID collision when multiple experiments interact with toadStool
simultaneously.

### Health Check Pattern

```
method: "health.check"
params: {}
response.result: true/false
```

primalSpring's `PrimalClient::health_check()` wraps this as a typed call.
The wait-for-health pattern (exp055) validates repeated probes with timeout.

---

## What toadStool/barraCuda/coralReef Should Know

### No Absorption Candidates

primalSpring contributes zero math, zero shaders, zero numerical primitives.
Its contribution is **validation coverage** — testing that the trio's IPC
contracts work correctly under composition.

### IPC Contract Expectations

primalSpring expects these capabilities from the trio:

| Primal | Expected Methods | Used In |
|--------|-----------------|---------|
| toadStool | `health.check`, `compute.dispatch`, `discovery.topology` | exp002, exp010-015, exp050 |
| barraCuda | `health.check` (if exposed as primal) | exp050 |
| coralReef | `health.check`, `shader.compile` | exp025, exp050 |

### Graceful Degradation

primalSpring's exp012 (`ConditionalDag`) explicitly tests the fallback path
when toadStool is unavailable. The deploy graph `conditional_fallback.toml`
should dispatch to CPU when GPU/toadStool is missing.

primalSpring currently uses `check_skip()` for all IPC-dependent checks,
meaning these experiments will automatically transition to real validation
once toadStool/barraCuda/coralReef expose their sockets.

### Phase 1 Activation

When toadStool exposes its socket at the standard path, primalSpring's
exp002 (Node Atomic) and exp050 (Compute Triangle) will automatically
detect it via `discover_primal("toadstool")` and attempt real IPC.
No code changes needed in primalSpring — only live primals.

---

## Cross-Spring Intelligence

### Patterns Learned from Phase1/Phase2 Showcases

primalSpring mined 13 coordination patterns from phase1/phase2 showcases
(see `specs/SHOWCASE_MINING_REPORT.md`). Key findings relevant to the trio:

1. **Compute triangle is the canonical integration pattern** — coralReef compiles,
   toadStool orchestrates, barraCuda executes. Every spring that does GPU work
   implicitly exercises this triangle.

2. **Socket-per-family convention** — bonding tests (exp030-034) use
   `{primal}-{family_id}.sock`. toadStool and barraCuda should support this
   for multi-gate deployments.

3. **Protocol escalation** — phase1/NestGate showcases demonstrate HTTP → JSON-RPC
   → tarpc escalation. If toadStool/barraCuda evolve beyond JSON-RPC, the
   escalation pattern from exp052 should be the reference.

### What Other Springs Tell Us

| Spring | toadStool/barraCuda Pattern | Notes |
|--------|----------------------------|-------|
| wetSpring V125 | 354 binaries, `compute.dispatch.*` direct dispatch | Heaviest consumer |
| hotSpring v0.6.31 | coralReef sovereign compile 46/46, VFIO PBDMA | Deepest GPU integration |
| airSpring v0.8.7 | 6 local WGSL → upstream absorption pipeline | Write→Absorb→Lean reference |
| groundSpring V110 | 102 delegations (61 CPU + 41 GPU) | Mixed-hardware dispatch |
| ludoSpring V22 | `compute.dispatch.*` direct dispatch | Game-engine real-time |
| healthSpring V30 | 6 WGSL shaders + 3 ODE→WGSL codegen | Domain-specific codegen |
| neuralSpring S163 | `DispatchOutcome`, circuit breaker | Resilience patterns |

primalSpring's role is to validate that all of these patterns compose correctly
when deployed together via biomeOS. The trio's IPC stability directly determines
how many primalSpring experiments can move from `check_skip` to real validation.

---

*primalSpring: 38 experiments, 7 tracks, 55 unit tests. The spring that validates
the coordination layer the trio depends on. Zero math, zero shaders, pure IPC.*
