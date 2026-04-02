# primalSpring v0.8.0 — Substrate Validation: Spring Team Handoff

**Date**: March 28, 2026  
**From**: primalSpring (coordination spring)  
**To**: All spring teams (groundSpring, healthSpring, wetSpring, neuralSpring, airSpring, hotSpring, ludoSpring)  
**Scope**: Patterns to model, validation substrate available, evolution guidance

---

## Context

primalSpring has built a deployment validation substrate that springs can leverage for their own
validation. The substrate includes **43-cell deployment matrix**, **15 benchScale topologies**,
**59 deploy graphs**, **7 network presets**, and **chaos engineering tools**. Springs can use these
to validate their deployments across diverse conditions before reaching production.

---

## Patterns for Springs to Model

### 1. Spring Validation Graph Pattern

Every spring should have a validation graph in `graphs/spring_validation/`:

```toml
[graph]
name = "{spring}_validate"
description = "biomeOS substrate → Tower → {spring} primal germination + validation"
coordination = "Sequential"

[[graph.node]]
name = "beardog"
binary = "beardog_primal"
order = 1
required = true
by_capability = "security"

[[graph.node]]
name = "songbird"
binary = "songbird_primal"
order = 2
depends_on = ["beardog"]
by_capability = "discovery"

[[graph.node]]
name = "start_biomeos"
binary = "biomeos_primal"
order = 3
depends_on = ["beardog", "songbird"]
by_capability = "ecosystem"

[[graph.node]]
name = "{spring}"
binary = "{spring}_primal"
order = 4
depends_on = ["beardog", "songbird", "start_biomeos"]
by_capability = "{domain}"
health_method = "{domain}.health"
capabilities = ["{domain}.primary_method", "{domain}.secondary_method"]
```

This pattern is already in place for all 7 springs. Validate yours matches.

### 2. Launch Profile Pattern

Each spring should have a profile in `config/primal_launch_profiles.toml`:

```toml
[profiles.{spring}]
binary = "{spring}"  # or "{spring}_primal"
env = { {SPRING}_MODE = "server", {SPRING}_SOCKET = "" }
depends_on = ["beardog", "songbird"]
health_method = "{domain}.health"
```

### 3. Capability Registry Pattern

Register your spring's capabilities in `config/capability_registry.toml`:

```toml
[[capabilities]]
method = "{domain}.primary_method"
description = "What it does"
domain = "{domain}"
provider = "{spring}"
```

### 4. Deployment Matrix Cell Pattern

Springs should add cells to `config/deployment_matrix.toml` to test their specific conditions:

```toml
[[cells]]
id = "{spring}-x86-homelan-uds"
topology = "nucleus_3node"  # or a spring-specific topology
arch = "x86_64"
preset = "home_lan"
transport = "uds_first"
experiments = "full"
priority = "P2"
status = "untested"
notes = "{spring} specific validation notes"
```

---

## Available Validation Infrastructure

### benchScale Topologies

Springs can request new benchScale topologies in `infra/benchScale/topologies/` or use existing ones:

| Topology | Nodes | Use For |
|----------|-------|---------|
| `ecoprimals-tower-homelan` | 2 | Basic spring deployment |
| `ecoprimals-nucleus-3node` | 3 | Spring with full NUCLEUS |
| `ecoprimals-alpine-minimal` | 2 | musl-static portability |
| `ecoprimals-readonly-fs` | 2 | Mobile/GrapheneOS simulation |
| `ecoprimals-constrained-256m` | 2 | OOM handling |
| `ecoprimals-federation-10node` | 10 | Spring in federated deployment |
| `ecoprimals-agentic-tower` | 3 | Spring with biomeOS + Squirrel + petalTongue |

### Network Presets

| Preset | Latency | Loss | Use For |
|--------|---------|------|---------|
| `localhost` | 0ms | 0% | Baseline performance |
| `basement_lan` | <1ms | 0.001% | HPC cluster |
| `home_lan` | 2ms | 0.01% | Typical home network |
| `friend_remote` | 45ms | 0.5% | Remote friend |
| `mobile_degraded` | 120ms | 5% | Mobile/cellular |
| `urban_congested` | 150ms | 15% | Congested network |
| `deep_space` | 2000ms | 10% | Extreme latency |

### Chaos Engineering

Springs can test resilience using `scripts/chaos-inject.sh`:

```bash
# Partition a spring's container
scripts/chaos-inject.sh partition <container> <target-ip>

# Kill a spring's process
scripts/chaos-inject.sh kill <container> <process-name>

# Fill disk to test graceful degradation
scripts/chaos-inject.sh disk_fill <container> <size-mb>
```

---

## Per-Spring Evolution Guidance

### groundSpring (environment)

- **Pattern**: fieldMouse sensor data → groundSpring analysis. See `graphs/science/fieldmouse_ingestion.toml`.
- **Evolution**: Accept streaming sensor data via Pipeline graph pattern (not just batch).
- **Matrix cell**: Add a fieldMouse + groundSpring cell for edge sensor validation.

### healthSpring (clinical)

- **Pattern**: Continuous health monitoring at 60Hz tick budget. See `graphs/gen4/gen4_storytelling_full.toml` for Continuous pattern.
- **Evolution**: Health metrics streaming to petalTongue dashboards.

### wetSpring (biology)

- **Pattern**: Multi-site federated biology. See `graphs/science/ecology_provenance.toml`.
- **Evolution**: Cross-site diversity analysis with provenance trio stamps per measurement.

### neuralSpring (neural)

- **Pattern**: Edge AI classification. See `graphs/science/neuromorphic_classify.toml`.
- **Evolution**: ToadStool NPU dispatch integration; NeuralSpring as classification backend.

### airSpring (atmospheric)

- **Blocker**: Internal `data::Provider`/`data::NestGateProvider` API drift prevents build.
- **Evolution**: Resolve API drift, then add to plasmidBin. Use `ecoprimals-alpine-minimal` topology.

### hotSpring (physics)

- **Pattern**: GPU burst compute. See `graphs/science/coralforge_federated.toml`.
- **Evolution**: ToadStool GPU dispatch for simulation bursts, provenance per timestep.

### ludoSpring (game science)

- **Critical P0**: Expand IPC surface for esotericWebb. See `specs/STORYTELLING_EVOLUTION.md`.
- **Missing methods**: `game.narrate_action`, `game.npc_dialogue`, `game.voice_check`, `game.push_scene`, `game.begin_session`, `game.complete_session`
- **Deploy**: Build and register in plasmidBin for both x86_64 and aarch64.
- **Matrix cells**: `storytelling-x86-homelan-uds`, `storytelling-x86-localhost-uds`

---

## Graph Composition Patterns to Study

| Pattern | Graph | Description |
|---------|-------|-------------|
| Continuous @ 60Hz | `gen4_storytelling_full.toml` | Tick-budget coordination with AI + game + viz |
| Pipeline streaming | `coralforge_federated.toml` | Multi-site data flow with per-step provenance |
| Bonding models | `ionic_capability_share.toml` | Cross-organization capability sharing |
| Chaos resilience | `partition_recovery.toml` | Network partition → mesh reformation |
| Agentic loop | `gen4_agentic_substrate.toml` | biomeOS routes → Squirrel decides → petalTongue renders |

---

## How to Use the Validation Substrate

1. **Add your spring to a benchScale topology** (or use an existing one)
2. **Create/update your spring validation graph** in `graphs/spring_validation/`
3. **Add a deployment matrix cell** for your spring's specific conditions
4. **Run the matrix**: `scripts/validate_deployment_matrix.sh --cell your-cell-id`
5. **Test under chaos**: `scripts/chaos-inject.sh` to verify resilience
6. **File blockers**: Add `[[blockers]]` to the matrix TOML for known issues

---

## Related Specs

- `specs/AGENTIC_TRIO_EVOLUTION.md` — biomeOS + Squirrel + petalTongue as the agentic loop
- `specs/STORYTELLING_EVOLUTION.md` — ludoSpring + esotericWebb evolution
- `specs/CROSS_SPRING_EVOLUTION.md` — full spring evolution path
- `config/deployment_matrix.toml` — 43-cell deployment matrix
