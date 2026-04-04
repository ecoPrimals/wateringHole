# Spring Cross-Evolution - Ecosystem Standard

**Status**: ECOSYSTEM STANDARD v1.0  
**Adopted**: March 21, 2026  
**Authority**: WateringHole Consensus (primalSpring coordination validation)  
**Compliance**: Recommended for all springs and primal teams  
**Reference Implementation**: primalSpring v0.4.0 (40 experiments, 8 tracks, 7 sibling-spring absorptions)

---

## Standard Declaration

**Spring Cross-Evolution** codifies how springs learn from each other, coordinate
through wateringHole, and evolve toward Neural API graph deployment without
creating cross-spring code dependencies. This standard captures the patterns
discovered through primalSpring's coordination of 7+ sibling springs and validated
through 40 experiments across 8 tracks.

---

## Core Principles

### 1. Springs Never Import Each Other

Springs are independent workspaces with no direct Rust dependencies on other
springs. Cross-spring learning flows through:

- **wateringHole handoffs**: Markdown documents describing patterns, learnings, and evolution guidance
- **Shared barraCuda primitives**: Mathematical operations available to all springs via the same upstream library
- **Ecosystem standards**: This document and its siblings in `wateringHole/`
- **primalSpring coordination**: Composition experiments that validate multi-spring patterns

```
           wateringHole (shared standards, handoffs, patterns)
          /        |          |          \          \
   hotSpring  wetSpring  airSpring  groundSpring  neuralSpring
        \         |          |          /          /
         barraCuda (shared math, WGSL shaders, precision strategy)
```

### 2. Coordination Through Composition, Not Coupling

When springs need to interact, they do so through primal coordination:

- Each spring IS a primal (via its niche self-knowledge and RPC server mode)
- biomeOS discovers springs by capability, not by name
- The Neural API routes requests semantically
- primalSpring validates that the composition works

### 3. Evolution Flows Upstream

```
Spring discovers pattern → validates locally → handoff to wateringHole
→ other springs absorb pattern → barraCuda absorbs math → everybody leans
```

---

## The Evolution Path

Every spring follows the same maturity progression:

```
Phase 0: Python Baseline
  Published paper → Python implementation → reproducible results
  
Phase 1: Rust Validation
  Python → Rust port → bit-exact or tolerance-bounded match
  
Phase 2: barraCuda CPU
  Rust math → barraCuda CPU kernels → delegation via IPC
  
Phase 3: barraCuda GPU (via toadStool)
  CPU kernels → WGSL shaders → GPU dispatch via toadStool
  
Phase 4: Fused TensorSession Pipeline
  Individual ops → fused multi-op pipeline → reduced dispatch overhead
  
Phase 5: Sovereign Dispatch (coralReef Native)
  wgpu transitional → coralReef native binary → full hardware sovereignty
```

### Write → Absorb → Lean Cycle

For GPU code (WGSL shaders), the maturity cycle is:

1. **Write**: Spring writes a local WGSL shader for its domain-specific operation
2. **Validate**: Spring validates the shader produces correct results (vs Python baseline)
3. **Handoff**: Spring documents the shader as an absorption candidate in a wateringHole handoff
4. **Absorb**: barraCuda absorbs the shader into its canonical library
5. **Lean**: Spring replaces its local copy with a delegation to the upstream barraCuda version

This prevents duplicate math across the ecosystem while allowing springs to
innovate freely in their own domains.

---

## Cross-Spring Learning Patterns

### Pattern Absorption

When one spring discovers a useful pattern, it should be offered to the ecosystem:

| What | Flow | Example |
|------|------|---------|
| Validation patterns | Spring → wateringHole → all springs | `check_skip()`, `ValidationSink` |
| IPC resilience | Spring → wateringHole → all springs | `CircuitBreaker`, `RetryPolicy` |
| Math kernels | Spring → barraCuda → all springs | GPU WGSL shaders, precision routing |
| Discovery patterns | Spring → biomeOS/primalSpring → all springs | 5-tier discovery, capability parsing |
| MCP tool definitions | Spring → Squirrel → AI routing | Domain-specific MCP tools |

### Handoff Convention

Cross-spring handoffs follow the naming convention:

```
{SPRING}_V{VERSION}_{TOPIC}_HANDOFF_{DATE}.md
```

Example: `PRIMALSPRING_V040_TOADSTOOL_BARRACUDA_EVOLUTION_HANDOFF_MAR21_2026.md`

Handoffs live in the originating spring's `wateringHole/handoffs/` directory.
Superseded handoffs are moved to `wateringHole/handoffs/archive/`.

### What a Handoff Contains

1. **Executive summary**: What changed and why it matters to the receiving team
2. **What the originating spring now provides**: New patterns, APIs, learnings
3. **What the receiving team should absorb**: Prioritized list of adoption items
4. **Learnings**: Cross-cutting insights from the sprint
5. **Evolution path**: Where the collaboration goes next
6. **Metrics**: Test counts, gate status, capability counts
7. **References**: Links to relevant code, experiments, and specs

---

## Neural API Graph Evolution

### The Vision

Each spring evolves toward expressing its domain as a Neural API deploy graph —
a BYOB (Bring Your Own Biome) niche that biomeOS can orchestrate:

```
wetSpring niche:
  graph: wetspring_analysis.toml
  nodes: [security, discovery, storage, compute, ai]
  primals: beardog + songbird + nestgate + toadstool + squirrel
  domain: biological data analysis pipeline

hotSpring niche:
  graph: hotspring_physics.toml
  nodes: [security, discovery, compute]
  primals: beardog + songbird + toadstool
  domain: computational physics simulation
```

### Evolution Steps for Each Spring

1. **Define niche capabilities**: What capabilities does your domain need?
2. **Declare deploy graph**: Create a TOML DAG with `by_capability` on all nodes
3. **Implement RPC server mode**: Expose domain methods via JSON-RPC 2.0
4. **Register capabilities**: Add entries to `config/capability_registry.toml`
5. **Validate composition**: Write integration tests that spawn the full niche
6. **Document handoff**: Create a wateringHole handoff for primalSpring and biomeOS teams

### Niche Adaptation

The same spring can adapt its deploy graph for different deployment contexts:

| Context | Niche Configuration | Use Case |
|---------|-------------------|----------|
| Wet lab | Full NUCLEUS + domain primals | Live instrument data, real-time analysis |
| Dry lab | Tower + compute + storage | Simulation and modeling |
| Data science | Tower + AI | Interactive analysis, ML workflows |
| CI/CD | Minimal (tests only) | Continuous validation, no live primals |
| Edge | Tower only | Lightweight deployment, constrained hardware |

---

## Ecosystem Coordination Role

### primalSpring as Coordination Hub

primalSpring validates composition patterns before other springs adopt them:

1. primalSpring experiments prove a pattern works with live primals
2. Pattern is documented in a wateringHole handoff
3. Other springs adopt the pattern for their domain
4. primalSpring validates the cross-spring composition

### What primalSpring Tracks for Each Spring

| Metric | Description |
|--------|-------------|
| Capability registration | Does the spring expose `health.liveness` + `capabilities.list`? |
| Deploy graph compliance | Does the graph have `by_capability` on all nodes? |
| IPC standard compliance | JSON-RPC 2.0 over Unix sockets? |
| Discovery compliance | 5-tier socket discovery? |
| Handoff currency | Is the latest handoff current with the spring's version? |

---

## Cross-Spring Experiment Tracks

primalSpring's experiment tracks provide the coordination template:

| Track | Domain | What It Validates |
|-------|--------|-------------------|
| 1 | Atomic Composition | Do primals deploy correctly together? |
| 2 | Graph Execution | Do all coordination patterns work? |
| 3 | Emergent Systems | Do higher-order behaviors emerge? |
| 4 | Bonding & Plasmodium | Does multi-gate coordination work? |
| 5 | coralForge | Does the neural object pipeline work? |
| 6 | Cross-Spring | Do cross-spring data flows work? |
| 7 | Showcase-Mined | Do mined patterns from phase1/phase2 hold? |
| 8 | Live Composition | Do real multi-primal compositions work? |

Other springs should model their own validation tracks after this structure,
adapting it to their domain while maintaining the same rigor and honest
scaffolding conventions (no fake passes — `check_skip` when dependencies
are unavailable).

---

## Compliance Checklist

For a spring to be cross-evolution compliant:

- [ ] Implements `health.liveness` and `capabilities.list` RPC methods
- [ ] Has at least one deploy graph with `by_capability` on all nodes
- [ ] Uses 5-tier socket discovery (env → XDG → tmp → manifest → registry)
- [ ] Uses JSON-RPC 2.0 over Unix sockets for IPC
- [ ] Has integration tests for live primal composition
- [ ] Maintains current wateringHole handoffs
- [ ] Follows the Write → Absorb → Lean cycle for GPU code
- [ ] No cross-spring Rust dependencies (coordination via IPC only)
- [ ] Zero C dependencies in application code (ecoBin compliant)
- [ ] `#![forbid(unsafe_code)]` in application code

---

## References

| Document | Location | Description |
|----------|----------|-------------|
| ecoBin Architecture Standard | `wateringHole/ECOBIN_ARCHITECTURE_STANDARD.md` | Pure Rust binary standard |
| UniBin Architecture Standard | `wateringHole/UNIBIN_ARCHITECTURE_STANDARD.md` | Single-binary primal standard |
| Neural API Graph Deployment Standard | `wateringHole/NEURAL_API_GRAPH_DEPLOYMENT_STANDARD.md` | Deploy graph conventions |
| Capability-Based Discovery Standard | `wateringHole/CAPABILITY_BASED_DISCOVERY_STANDARD.md` | Runtime discovery patterns |
| Spring as Niche Deployment Standard | `wateringHole/SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` | BYOB niche conventions |
| Coordination Handoff Standard | `wateringHole/COORDINATION_HANDOFF_STANDARD.md` | Handoff format conventions |
| primalSpring Cross-Spring Evolution | `primalSpring/specs/CROSS_SPRING_EVOLUTION.md` | Detailed cross-spring touchpoints |

---

**License**: AGPL-3.0-or-later
