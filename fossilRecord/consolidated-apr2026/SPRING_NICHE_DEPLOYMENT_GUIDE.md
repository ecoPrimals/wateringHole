# Spring-as-Niche Deployment Guide

**How to evolve a spring into a deployable biomeOS niche**

**Date**: March 15, 2026
**Status**: Reference implementations — groundSpring V102, airSpring V081
**License**: AGPL-3.0-only

---

## Overview

A **spring** starts as a validation library — pure Rust proving Python baselines
can be faithfully ported to barraCUDA and eventually promoted to ToadStool. The
evolution path is:

```
Python baseline → Rust validation → GPU acceleration → sovereign pipeline → niche deployment
```

The final step — **niche deployment** — makes the spring a first-class biomeOS
citizen: discoverable, composable, and orchestratable via Neural API graphs.

This guide documents the pattern groundSpring established as the first spring
with the full niche deployment set. Other springs (hotSpring, wetSpring,
airSpring, neuralSpring) can follow this template to evolve their own niches.

---

## What You Need

Four artifacts transform a spring into a deployable niche:

| Artifact | Purpose | groundSpring Reference |
|---|---|---|
| **UniBin binary** | Single executable with `server`, `status`, `version` subcommands | `src/bin/groundspring_primal.rs` |
| **Deploy graph** | TOML DAG defining germination order and capability wiring | `graphs/groundspring_deploy.toml` |
| **Niche YAML** | BYOB definition with organisms, interactions, customization | `niches/groundspring-measurement.yaml` |
| **Capability domain** | Semantic namespace for your capabilities | `measurement.*` (8 methods) |

Optional but recommended:
- **Provenance module** — Trio lifecycle wrappers (`provenance.rs`)
- **Dispatch module** — JSON-RPC method routing (`dispatch.rs`)
- **Server module** — UDS socket binding (`biomeos/server.rs`)

---

## Step 1: Define Your Capability Domain

Choose a semantic namespace that describes what your spring provides. The domain
name should be a single word that captures the domain of expertise.

| Spring | Domain | Example Capabilities |
|---|---|---|
| groundSpring | `measurement` | `measurement.noise_decomposition`, `measurement.anderson_validation` |
| hotSpring | `precision` | `precision.nuclear_mass`, `precision.binding_energy` |
| wetSpring | `ecology` | `ecology.diversity_index`, `ecology.rarefaction` |
| airSpring | `hydrology` | `hydrology.et0_fao56`, `hydrology.water_balance` |
| neuralSpring | `inference` | `inference.surrogate`, `inference.transfer_learn` |

Define capabilities in your `biomeos/mod.rs`:

```rust
pub const MY_DOMAIN: &str = "ecology";

pub const MY_CAPABILITIES: &[&str] = &[
    "ecology.diversity_index",
    "ecology.rarefaction",
    "ecology.community_similarity",
];

pub const MY_MAPPINGS: &[(&str, &str)] = &[
    ("diversity_index", "ecology.diversity_index"),
    ("rarefaction", "ecology.rarefaction"),
    ("community_similarity", "ecology.community_similarity"),
];
```

Registration is two-phase:
1. **Domain registration** — register the domain with semantic mappings
2. **Individual registration** — register each capability

---

## Step 2: Create the UniBin Binary

The UniBin standard requires three subcommands:

```
yourspring server    # Bind UDS socket, register capabilities, accept JSON-RPC
yourspring status    # Connect to own socket, call health.check, print result
yourspring version   # Print version, domain, capabilities, license
```

### Binary structure

```rust
fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(String::as_str) {
        Some("server") => cmd_server(),
        Some("status") => cmd_status(),
        Some("version") => cmd_version(),
        _ => { eprintln!("usage: yourspring <server|status|version>"); ExitCode::FAILURE }
    }
}
```

### Server lifecycle

1. **Bind** UDS socket at `$XDG_RUNTIME_DIR/biomeos/yourspring-{FAMILY_ID}.sock`
2. **Register** capabilities with biomeOS (non-fatal if biomeOS unavailable)
3. **Start provenance** session (optional, via Provenance Trio)
4. **Accept** JSON-RPC connections in a non-blocking loop
5. **Dispatch** each request to the appropriate library function
6. On **shutdown**: deregister capabilities, commit provenance, clean up socket

### Cargo.toml

```toml
[[bin]]
name = "yourspring"
path = "src/bin/yourspring_primal.rs"
required-features = ["biomeos"]
```

---

## Step 3: Create the Dispatch Module

Map each capability method to the library function that implements it:

```rust
pub fn dispatch(method: &str, params: &Value) -> Result<Value, String> {
    match method {
        "health.check" => Ok(health_check()),
        "capability.list" => Ok(capability_list()),
        "lifecycle.status" => Ok(lifecycle_status()),

        "ecology.diversity_index" => diversity_index(params),
        "ecology.rarefaction" => rarefaction(params),

        _ => Err(format!("method not found: {method}")),
    }
}
```

Each method function extracts parameters from the JSON `Value`, calls the
library, and returns the result as JSON. The dispatch layer adds zero compute
overhead — it is pure routing.

If your library functions already delegate to barraCUDA, those delegations
flow through unchanged:

```
capability.call("ecology.diversity_index", params)
  → dispatch.rs: diversity_index(params)
    → crate::rarefaction::simpson_diversity(samples)
      → #[cfg(feature = "barracuda-gpu")] barracuda::ops::bio::simpson_diversity_gpu(samples)
```

---

## Step 4: Create the Deploy Graph

The deploy graph is a TOML DAG that biomeOS executes via `neural_api.execute_graph`.

### Standard phases

```
Phase 1: Tower Atomic (BearDog + Songbird) — security + discovery
Phase 2: Optional dependencies (ToadStool, NestGate) — compute + storage
Phase 3: Your spring — germinate with `by_capability = "your_domain"`
Phase 4: Validation — health check
Phase 5: Provenance — session lifecycle (optional)
```

### Key conventions

```toml
[graph]
id = "yourspring_deploy"
name = "YourSpring Measurement Niche"
version = "1.0.0"
coordination = "Sequential"

# Reference primals by CAPABILITY, never by name
[[nodes]]
id = "germinate_yourspring"
depends_on = ["germinate_beardog", "germinate_songbird"]
[nodes.primal]
by_capability = "ecology"

# Optional dependencies use fallback = "skip"
[[nodes]]
id = "germinate_toadstool"
depends_on = ["germinate_beardog"]
fallback = "skip"
[nodes.primal]
by_capability = "compute"

# Provenance Trio nodes use fallback = "skip"
[[nodes]]
id = "provenance_session_start"
depends_on = ["health_check"]
fallback = "skip"
[nodes.operation]
name = "capability_call"
[nodes.operation.params]
capability = "provenance.session_create"
```

### Full reference

See `groundSpring/graphs/groundspring_deploy.toml` for a complete 5-phase
example with 8 measurement capabilities, optional ToadStool/NestGate, and
Provenance Trio wiring.

---

## Step 5: Create the Niche YAML

The niche YAML defines the BYOB (Build Your Own Biome) template:

```yaml
niche:
  id: "yourspring-ecology"
  name: "YourSpring Ecology Niche"
  version: "1.0.0"
  description: "Ecological diversity validation and analysis"
  category: "science"
  deploy_graph: "graphs/yourspring_deploy.toml"

organisms:
  primals:
    yourspring:
      type: "yourspring"
      required: true
      role: "science"
      capabilities:
        - "ecology.diversity_index"
        - "ecology.rarefaction"
      config:
        mode: "server"

    beardog:
      type: "beardog"
      required: true
      role: "security"

    songbird:
      type: "songbird"
      required: true
      role: "discovery"

    toadstool:
      type: "toadstool"
      required: false
      role: "compute"

interactions:
  - from: "yourspring"
    to: "beardog"
    type: "capability_call"
    capabilities: ["crypto.sign"]

customization:
  options:
    gpu_enabled:
      type: boolean
      default: false
      affects: ["toadstool"]
```

### Full reference

See `groundSpring/niches/groundspring-measurement.yaml` for a complete
example with 5 organisms, interaction definitions, and customization options.

---

## Step 6: Wire Provenance at the Graph Level

Provenance Trio integration happens at the graph level, not the library level.
Add session/commit/attribute nodes to your deploy and validation graphs:

```toml
# Start session
[[nodes]]
id = "provenance_session_start"
depends_on = ["health_check"]
fallback = "skip"
[nodes.operation]
name = "capability_call"
[nodes.operation.params]
capability = "provenance.session_create"
params = { agent = "yourspring", experiment_id = "deploy", version = "V1" }

# Store results
[[nodes]]
id = "store_results"
depends_on = ["provenance_session_start"]
fallback = "skip"
[nodes.operation]
name = "capability_call"
[nodes.operation.params]
capability = "storage.put"

# Dehydrate (commit)
[[nodes]]
id = "provenance_commit"
depends_on = ["store_results"]
fallback = "skip"
[nodes.operation]
name = "capability_call"
[nodes.operation.params]
capability = "provenance.session_dehydrate"

# Attribute
[[nodes]]
id = "provenance_attribute"
depends_on = ["provenance_commit"]
fallback = "skip"
[nodes.operation]
name = "capability_call"
[nodes.operation.params]
capability = "contribution.recordDehydration"
```

All provenance nodes use `fallback = "skip"` — the Trio enhances, never blocks.

---

## Step 7: Evolve Existing Graphs

If your spring already has graphs (Tower bootstrap, validation, cross-substrate),
evolve them:

1. **Version pins** — update to your current version
2. **Capability namespace** — `science.*` → `your_domain.*`
3. **Hardcoded primal lists** → `discover_by_capability = true`
4. **Direct RPC** (`rpc_call target = "nestgate"`) → capability routing (`capability_call capability = "storage.put"`)
5. **Provenance** — add Trio lifecycle nodes with `fallback = "skip"`

---

## Checklist

- [ ] Capability domain defined (`MY_DOMAIN`, `MY_CAPABILITIES`, `MY_MAPPINGS`)
- [ ] UniBin binary with `server`, `status`, `version` subcommands
- [ ] Dispatch module mapping capability methods to library functions
- [ ] Deploy graph (`graphs/yourspring_deploy.toml`) with 5 standard phases
- [ ] Niche YAML (`niches/yourspring-niche.yaml`) with organisms and customization
- [ ] Provenance Trio wired at graph level (all nodes `fallback = "skip"`)
- [ ] Existing graphs evolved (capability namespace, version pins, provenance)
- [ ] `cargo clippy --features biomeos -- -D warnings`: PASS
- [ ] `cargo test --features biomeos`: PASS
- [ ] wateringHole handoff documenting the niche deployment
- [ ] Handoff copied to `ecoPrimals/wateringHole/handoffs/`

---

## Current Spring Niche Status

| Spring | UniBin | Deploy Graph | Niche YAML | Provenance | Status |
|---|---|---|---|---|---|
| **groundSpring** | Yes | Yes | Yes | Yes | **Complete** (V102) |
| **airSpring** | Yes | Yes (4 graphs) | Yes | Yes (auto) | **Complete** (V081) |
| **ludoSpring** | Yes | Yes (2 graphs) | Yes | Yes (graph) | **Complete** (V16) |
| **wetSpring** | Audit needed | Yes | No | Yes (graph) | Partial |
| **hotSpring** | Audit needed | No | No | No | Not started |
| **neuralSpring** | TBD | TBD | TBD | TBD | Not started |

groundSpring (V102), airSpring (V081), and ludoSpring (V16) serve as reference implementations.

**groundSpring**: First Spring with full niche set. Follow artifacts in
`groundSpring/crates/groundspring/src/` and `groundSpring/graphs/`.

**airSpring**: First Spring with neuralAPI Pathway Learner integration. Extends
the groundSpring pattern with structured metrics, operation dependencies, cost
estimates, and multi-domain registration. Follow artifacts in
`airSpring/barracuda/src/bin/airspring_primal.rs` and `airSpring/graphs/`.
Key additions over groundSpring:
- `emit_metrics()` on every dispatch (neuralAPI Enhancement 1)
- `operation_dependencies()` and `cost_estimates()` in `capability.list` (Enhancement 2+3)
- `auto_record_provenance()` makes provenance automatic in dispatch
- `ecology.experiment` provides single-call experiment orchestration
- 4 domain registrations (ecology, provenance, data, capability)
- Heartbeat reports composition status for biomeOS graph rewiring

---

## References

- `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md` — the formal standard
- `SPRING_AS_PROVIDER_PATTERN.md` — capability registration pattern
- `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — provenance wiring
- `CROSS_SPRING_DATA_FLOW_STANDARD.md` — inter-spring data exchange
- `whitePaper/neuralAPI/03_GRAPH_EXECUTION.md` — graph coordination patterns
- `whitePaper/neuralAPI/08_NICHE_API_PATTERNS.md` — transactional vs continuous niches

---

*"The spring validates science. The niche deploys it."*
