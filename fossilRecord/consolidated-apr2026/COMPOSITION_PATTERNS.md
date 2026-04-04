# Composition Deployment Patterns

**Purpose:** Canonical reference for how primals are composed into deployable
systems using biomeOS deploy graphs, niche YAML, primal launch profiles, and
socket discovery.

**Last Updated:** March 29, 2026

---

## Overview

Primal composition follows a layered model:

```
Graph (TOML DAG)        — what to start, in what order, with what capabilities
Niche (YAML metadata)   — what the deployment IS (organisms, interactions, customization)
Launch Profile (TOML)   — how each binary is invoked (subcommand, ports, health)
Socket Discovery        — how primals find each other at runtime (8-step resolution)
```

biomeOS reads a graph, germinates primals per the graph's dependency order,
discovers their sockets, and wires their capabilities via the Neural API.

---

## 1. Deploy Graph Formats

Two graph schemas exist in the ecosystem. Both are valid TOML and both are
consumed by biomeOS, but they serve different scales.

### Format A: `[[graph.node]]` (Canonical for New Compositions)

Used by primalSpring spring validation graphs, negative-test graphs, and
single-gate compositions. This is the **recommended format for new graphs**.

```toml
[graph]
name = "tower_atomic_bootstrap"
description = "Tower Atomic: BearDog (crypto) + Songbird (discovery)"
version = "0.3.0"
coordination = "sequential"

[[graph.node]]
name = "beardog"
binary = "beardog_primal"
order = 1
required = true
health_method = "health.liveness"
by_capability = "security"
capabilities = ["crypto.encrypt", "crypto.sign", "crypto.verify"]

[[graph.node]]
name = "songbird"
binary = "songbird_primal"
order = 2
required = true
depends_on = ["beardog"]
health_method = "health.liveness"
by_capability = "discovery"
capabilities = ["discovery.find_primals", "discovery.announce"]
```

**Key fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Unique node identifier |
| `binary` | yes | Binary name from plasmidBin |
| `order` | yes | Germination order (integer) |
| `required` | yes | `true` = failure aborts graph; `false` = graceful skip |
| `depends_on` | no | Array of node names that must complete first |
| `health_method` | no | JSON-RPC method for health probe (default `health.check`) |
| `by_capability` | no | Capability domain for Neural API routing |
| `capabilities` | no | Capabilities this node provides after germination |
| `spawn` | no | `false` = connect to existing process; `true` (default) = start new |

**Operation block** (for validation/test nodes):
```toml
[graph.node.operation]
method = "genetic.verify_lineage"
expect = "valid"  # or "invalid", "error", "success"

[graph.node.operation.params]
our_family_id = "family-alpha"
lineage_seed = "${LINEAGE_SEED_B64}"
```

**Metadata block:**
```toml
[graph.metadata]
bond_type = "validation"
trust_model = "genetic_lineage"
negative_tests = true
```

### Format B: `[[nodes]]` (Multi-Node and Product Compositions)

Used by esotericWebb deploy graphs and primalSpring multi-node graphs that
span multiple gates or architectures.

```toml
[graph]
id = "esotericwebb_full"
description = "Esoteric Webb: CRPG niche full deploy"
coordination = "Sequential"
version = "1.0"

[[nodes]]
id = "germinate_beardog"
output = "beardog_genesis"
capabilities = ["security", "crypto"]

[nodes.primal]
by_capability = "security"

[nodes.operation]
name = "start"
[nodes.operation.params]
mode = "server"
family_id = "${FAMILY_ID}"
[nodes.operation.environment]
BIOMEOS_SOCKET_DIR = "${XDG_RUNTIME_DIR}/biomeos"

[nodes.constraints]
timeout_ms = 15000

[nodes.hardware]
arch = "x86_64-linux-musl"
gate = "devGate"

[nodes.capabilities_provided]
"crypto.sign_ed25519" = "crypto.sign_ed25519"
```

**Additional fields in Format B:**

| Field | Description |
|-------|-------------|
| `[nodes.primal]` | Primal resolution metadata |
| `[nodes.operation]` | Start command and params |
| `[nodes.operation.environment]` | Per-node environment variables |
| `[nodes.constraints]` | Timeout, resource limits |
| `[nodes.hardware]` | Architecture and gate targeting |
| `[nodes.capabilities_provided]` | Capability map for downstream wiring |
| `output` | Named output for `${ref}` interpolation |

### Format Comparison

| Aspect | `[[graph.node]]` | `[[nodes]]` |
|--------|-------------------|-------------|
| Scale | Single-gate compositions | Multi-gate, multi-arch |
| Node id field | `name` | `id` |
| Primal routing | `by_capability` on node | `[nodes.primal]` sub-table |
| Environment | Not supported | `[nodes.operation.environment]` |
| Hardware targeting | Not supported | `[nodes.hardware]` |
| Output interpolation | `${node_name.field}` | `${node_name.field}` |
| Constraints | Not supported | `[nodes.constraints]` |

**Migration guidance:** Single-gate `[[graph.node]]` graphs do not need to
migrate. If a graph grows to span multiple architectures or gates, convert
to `[[nodes]]` format and add hardware/environment/constraints blocks.

### Shared Features (Both Formats)

- `[graph]` header with `name`/`id`, `description`, `version`, `coordination`
- `[graph.metadata]` for bond type, trust model, tags
- `[graph.bonding_policy]` for multi-node trust and capability policies
- `depends_on` / dependency edges
- `${variable}` interpolation from env or upstream node outputs
- Five coordination patterns: Sequential, Parallel, ConditionalDag, Pipeline, Continuous

---

## 2. Niche YAML

A niche YAML declares what a deployment IS — its organisms, interactions,
and customization options. This is the metadata contract between a product
(gen4) and biomeOS.

**Reference:** `esotericWebb/niches/esoteric-webb.yaml`

### Structure

```yaml
niche:
  id: "esoteric-webb"
  name: "Esoteric Webb CRPG Niche"
  version: "1.0.0"
  description: "Cross-evolution CRPG substrate"
  category: "narrative"
  deploy_graph: "graphs/esotericwebb_full.toml"

organisms:
  primals:
    beardog:
      type: "beardog"
      required: true
      role: "security"
      capabilities: ["crypto.sign", "crypto.encrypt", "crypto.hash"]
      config:
        mode: "server"
        domain: "crypto"

    toadstool:
      type: "toadstool"
      required: false
      role: "compute"
      capabilities: ["compute.execute"]

  chimeras: {}

interactions:
  - from: "esotericwebb"
    to: "ludospring"
    type: "capability_call"
    config:
      capabilities: ["game.evaluate_flow", "game.engagement"]
      description: "Game science for CRPG substrate"

customization:
  options:
    provenance_enabled:
      type: boolean
      default: true
      description: "Enable Provenance Trio"
      affects: ["rhizocrypt", "loamspine", "sweetgrass"]
```

### Key Conventions

- `required: true` primals cause deployment failure if absent
- `required: false` primals are optional — product degrades gracefully
- `deploy_graph` points to the TOML graph used by biomeOS
- `interactions` define the capability-call wiring between organisms
- `customization.options` allow per-deployment tuning without graph changes

---

## 3. Primal Launch Profiles

A launch profile defines how a product's launcher invokes each primal binary
from plasmidBin. This is the contract between the product and the binary.

**Reference:** `esotericWebb/config/primal_launch_profiles.toml`

### Structure

```toml
[defaults]
subcommand = "server"
port_flag = "--port"
health_method = "health.check"
readiness_timeout_secs = 10
readiness_poll_ms = 100

[profiles.rhizocrypt]
domain = "dag"
default_port = 9401
health_method = "health.check"

[profiles.squirrel]
domain = "ai"
default_port = 9410
health_method = "health.liveness"
```

### Key Fields

| Field | Description |
|-------|-------------|
| `subcommand` | Binary subcommand to start server mode (default: `server`) |
| `port_flag` | CLI flag for port assignment (default: `--port`) |
| `health_method` | JSON-RPC method to probe readiness |
| `default_port` | Fallback port if no env override |
| `readiness_timeout_secs` | Max seconds to wait for health response |
| `readiness_poll_ms` | Polling interval during readiness wait |
| `domain` | Semantic domain for capability routing |

The launcher reads the profile, spawns the binary, waits for the health method
to succeed, then registers the primal with biomeOS.

---

## 4. Socket Discovery Resolution Order

biomeOS discovers primal sockets at runtime using an 8-step resolution order.
The first successful probe wins. Each step falls through to the next on failure.

| Step | Method | Example |
|------|--------|---------|
| 1 | **Environment variable hint** | `BEARDOG_SOCKET=/run/user/1000/beardog.sock` or `BEARDOG_TCP=127.0.0.1:9100` |
| 2 | **Capability-first sockets** | `security.sock`, `crypto.sock` in socket dir |
| 3 | **XDG_RUNTIME_DIR** | `/run/user/1000/biomeos/beardog-1894e909e454.sock` |
| 4 | **Abstract socket** (Linux/Android) | `@biomeos_beardog_1894e909e454` |
| 5 | **Family-scoped /tmp** | `/tmp/beardog-1894e909e454.sock` |
| 6 | **Socket registry** | `$XDG_RUNTIME_DIR/biomeos/socket-registry.json` |
| 7 | **Capability registry via Neural API** | Query biomeOS for capability provider endpoint |
| 8 | **TCP fallback** | `127.0.0.1:9100` (from launch profile or default) |

### Transport Tiers

- **Tier 1 (Native):** Unix sockets, abstract sockets — zero-copy, lowest latency
- **Tier 2 (Universal):** TCP — cross-device, WASM, restricted environments

### Family Scoping

Socket paths include a family_id hash (`1894e909e454`) derived from the family
seed. This provides namespace isolation — primals from different families cannot
accidentally discover each other via filesystem enumeration.

### Key Environment Variables

| Variable | Description |
|----------|-------------|
| `BIOMEOS_SOCKET_DIR` | Override socket directory (default: `$XDG_RUNTIME_DIR/biomeos`) |
| `{PRIMAL}_SOCKET` | Direct socket path hint for a specific primal |
| `{PRIMAL}_TCP` | Direct TCP endpoint hint (host:port) |
| `FAMILY_ID` | Family seed identifier for namespace scoping |
| `XDG_RUNTIME_DIR` | XDG base directory for runtime files |

**Implementation:** `biomeOS/crates/biomeos-core/src/socket_discovery/mod.rs`

---

## 5. Putting It Together

A complete composition deployment follows this sequence:

```
1. Product defines niche YAML (what organisms, interactions, options)
2. Product defines deploy graph (germination order, dependencies, capabilities)
3. Product defines launch profiles (how to invoke each binary)
4. Product deploys binaries from plasmidBin/ to the gate
5. biomeOS reads the graph, germinates primals in order
6. Each primal starts, creates its socket, responds to health probe
7. Socket discovery wires primal endpoints into the Neural API
8. Capability-based routing becomes active
9. Product (or biomeOS graph) exercises capabilities via JSON-RPC
```

### Graph Lifecycle (from biomeOS perspective)

```
graph.execute(graph_path)
  → parse graph (either [[graph.node]] or [[nodes]])
  → resolve dependencies (topological sort)
  → for each node in order:
      if spawn=true: start binary (subcommand from launch profile)
      wait for health_method to succeed (readiness_poll_ms * readiness_timeout_secs)
      register capabilities with Neural API
      if operation: execute method, check expect condition
  → return graph result (success/partial/failure)
```

---

## Related Documents

- `SPOREGARDEN_DEPLOYMENT_STANDARD.md` — How gen4 products compose primals (BYOB model)
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 wire protocol
- `UNIVERSAL_IPC_STANDARD_V3.md` — Multi-transport IPC behavioral specification
- `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` — How springs deploy as biomeOS niches
- `PRIMALSPRING_COMPOSITION_GUIDANCE.md` — primalSpring's capabilities for composition validation
