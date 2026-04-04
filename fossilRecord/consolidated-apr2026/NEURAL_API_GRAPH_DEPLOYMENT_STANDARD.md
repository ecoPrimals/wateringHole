# Neural API Graph Deployment - Ecosystem Standard

**Status**: ECOSYSTEM STANDARD v1.0  
**Adopted**: March 21, 2026  
**Authority**: WateringHole Consensus (primalSpring coordination validation)  
**Compliance**: Recommended for all springs and primals deploying via biomeOS  
**Reference Implementation**: primalSpring v0.4.0 (11 deploy graphs, Tower STABLE 24/24, exp060 live biomeOS deploy)

---

## Standard Declaration

**Neural API Graph Deployment** is hereby adopted as the standard for how springs
and primals declare, validate, and execute multi-primal compositions via biomeOS.
This standard codifies the patterns primalSpring established and validated through
40 experiments and 24 Tower Atomic gates.

All springs evolving toward biomeOS-orchestrated deployment should follow these
conventions to ensure interoperability, deterministic startup ordering, and
capability-based discovery.

---

## Core Principle

### Graphs Are the Source of Truth

Deploy graphs are TOML DAGs that declare what a composition needs (capabilities),
not who provides it (primal names). biomeOS resolves providers at runtime via the
Neural API's capability registry.

```
Spring declares what it needs → biomeOS resolves who provides it → Neural API routes calls
```

---

## 1. Deploy Graph Format

### 1.1 Node Structure

Every node in a deploy graph MUST have a `by_capability` field:

```toml
[[nodes]]
name = "security"
by_capability = "security"
depends_on = []

[[nodes]]
name = "discovery"
by_capability = "discovery"
depends_on = ["security"]

[[nodes]]
name = "compute"
by_capability = "compute"
depends_on = ["security", "discovery"]
```

**Rationale**: `by_capability` enables runtime provider resolution. A node
requesting `"compute"` may be served by toadStool today and a different compute
provider tomorrow, without changing the graph.

### 1.2 Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Human-readable node identifier (unique within graph) |
| `by_capability` | String | Yes | Capability domain this node requires |
| `depends_on` | String[] | Yes | Node names that must start before this node |
| `fallback` | String | No | Strategy when provider unavailable: `"skip"`, `"error"` (default) |
| `optional` | Boolean | No | Whether the node can be absent (default: false) |

### 1.3 Graph Metadata

```toml
[metadata]
name = "tower_atomic_bootstrap"
version = "1.0.0"
description = "Tower Atomic: security + discovery"
pattern = "sequential"
```

### 1.4 File Location

Deploy graphs live in `graphs/` within the spring's workspace:

```
myspring/
├── graphs/
│   ├── myspring_deploy.toml
│   ├── tower_atomic_bootstrap.toml
│   └── ...
```

---

## 2. Topological Ordering

### 2.1 Startup Waves

`topological_waves()` computes startup ordering from the DAG using Kahn's
algorithm. Nodes with no unmet dependencies start in the same wave (parallel).
Nodes whose dependencies are in earlier waves start in subsequent waves.

```
Wave 0: [security]           — no dependencies
Wave 1: [discovery]          — depends on security
Wave 2: [compute, storage]   — depends on security + discovery
Wave 3: [ai]                 — depends on compute
```

### 2.2 Cycle Detection

Graphs MUST be acyclic. The `topological_waves()` implementation detects cycles
and returns an error if any exist. This should be validated at test time.

### 2.3 Health Gating Between Waves

Each primal in a wave MUST respond to `health.liveness` before the next wave
starts. The `AtomicHarness` enforces this with a configurable timeout (default
30 seconds per wave).

---

## 3. Capability-Based Provider Resolution

### 3.1 Resolution Order

When biomeOS encounters a `by_capability = "compute"` node, it resolves the
provider using this priority:

1. Neural API capability registry (runtime)
2. Capability-named socket (`compute.sock` in nucleation directory)
3. Socket registry file
4. Manifest file
5. Default socket path conventions

### 3.2 Provider Registration

Primals MUST implement these standard RPC methods to be discoverable:

| Method | Response | Required |
|--------|----------|----------|
| `health.liveness` | `{"status": "alive"}` | Yes |
| `capabilities.list` | Array of capability strings or objects | Yes |

### 3.3 Capability Registry

Springs maintain a `config/capability_registry.toml` that declares all
capabilities in the composition:

```toml
[[capabilities]]
name = "security"
domain = "crypto"
provider = "beardog"
methods = ["crypto.sign", "crypto.verify", "crypto.encrypt"]

[[capabilities]]
name = "ai.query"
domain = "ai"
provider = "squirrel"
methods = ["ai.query", "ai.health"]
```

---

## 4. BYOB Niche Deployment

### 4.1 Springs as Niches

Each spring is a "Bring Your Own Biome" (BYOB) niche — a deployment
configuration that specifies which primals, capabilities, and graphs are needed
for its domain:

```
wetlab niche:    Tower + NestGate + ToadStool + Squirrel (GPU compute + AI + storage)
drylab niche:    Tower + ToadStool + Squirrel (GPU compute + AI, no wet storage)
datascience:     Tower + Squirrel (AI only, minimal infrastructure)
```

### 4.2 Niche Declaration

Springs declare their niche requirements via deploy graphs. The graphs serve as
both documentation and executable deployment specifications.

---

## 5. Validation Requirements

### 5.1 Test-Time Validation

All deploy graphs MUST be validated at test time:

- **Structural**: All required fields present, no unknown fields
- **Topological**: DAG is acyclic, `topological_waves()` succeeds
- **Capability**: All `by_capability` values are registered in the capability registry
- **`by_capability` enforcement**: Every node has `by_capability` (enforced by test)

### 5.2 Live Validation

Springs SHOULD include integration tests that:

- Spawn primals from `plasmidBin` binaries
- Validate health via `health.liveness`
- Verify capability discovery via `capabilities.list`
- Confirm inter-primal communication via capability routing

---

## 6. Environment and Socket Conventions

### 6.1 Socket Nucleation

Primal sockets follow the nucleation pattern:

```
{base_dir}/{family_id}/{primal_name}.sock
```

Where `base_dir` is resolved via 5-tier discovery (env, XDG, tmp, manifest, registry).

### 6.2 Environment Forwarding

When primals need environment configuration (API keys, GPU device selection),
use `passthrough_env` in launch profiles rather than global `set_var`:

```toml
[profiles.myprimal.passthrough_env]
MY_API_KEY = true
CUDA_VISIBLE_DEVICES = true
```

### 6.3 Port Binding

Primals binding TCP ports SHOULD accept `--port 0` for ephemeral port assignment
to avoid conflicts in parallel test environments.

---

## 7. Reference Implementations

| Implementation | Location | Description |
|---|---|---|
| primalSpring deploy graphs | `primalSpring/graphs/*.toml` | 11 graphs, all `by_capability`, topologically validated |
| `topological_waves()` | `primalSpring/ecoPrimal/src/deploy.rs` | Kahn's algorithm with cycle detection |
| `AtomicHarness` | `primalSpring/ecoPrimal/src/harness/mod.rs` | Multi-primal composition lifecycle |
| exp060 biomeOS deploy | `primalSpring/experiments/exp060_biomeos_tower_deploy/` | Live Neural API bootstrap graph execution |
| exp061 AI composition | `primalSpring/experiments/exp061_squirrel_ai_composition/` | 3-primal composition with AI |
| biomeOS graph executor | `biomeOS/biomeos-graph/` | Production graph execution engine |

---

**License**: AGPL-3.0-or-later
