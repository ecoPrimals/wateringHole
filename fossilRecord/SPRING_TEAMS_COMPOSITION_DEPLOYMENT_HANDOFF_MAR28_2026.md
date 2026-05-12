# Spring Teams Handoff — Composition & Deployment Patterns (March 28, 2026)

**From**: primalSpring coordination (Phase 23f)
**For**: airSpring, groundSpring, healthSpring, hotSpring, neuralSpring, wetSpring, ludoSpring
**Reference**: `infra/wateringHole/` for ecosystem patterns and standards

---

## What primalSpring Did

primalSpring decomposed interactive composition into 7 independently deployable
subsystem compositions (C1-C7). Each is a biomeOS deploy graph that can be tested
and deployed in isolation. This pattern is available for all springs to adopt.

## The Pattern: Composition as Deployed Science

Springs validate domain science. That science becomes deployable when it's composed
with primals via biomeOS deploy graphs. The progression:

```
Python experiment → Rust validation → Primal composition → biomeOS deployment
```

### What this means for each spring

1. **Your science runs as a primal** (or behind one). Your JSON-RPC methods are your
   scientific API surface. biomeOS discovers and routes to them.

2. **Deploy graphs define your composition**. A TOML file declares what primals
   your science needs (Tower for identity/networking, Squirrel for AI, etc.).

3. **Validation graphs test your composition**. A matching TOML file defines
   what checks to run against your deployed composition.

4. **The thin gateway bridges to users**. A WebSocket-to-IPC bridge (no business
   logic) lets browser clients call your science via capability discovery.

## Reference: primalSpring's Composition Structure

```
graphs/compositions/
├── render_standalone.toml          # petalTongue — visualization
├── narration_ai.toml               # Squirrel — AI
├── session_standalone.toml         # esotericWebb — narrative (example product)
├── game_science_standalone.toml    # ludoSpring — game science (example science)
├── persistence_standalone.toml     # NestGate — storage
├── proprioception_loop.toml        # petalTongue — interaction feedback
└── interactive_product.toml        # all composed — the full product

graphs/spring_validation/
├── composition_render_validate.toml
├── composition_narration_validate.toml
├── composition_session_validate.toml
├── composition_game_science_validate.toml
├── composition_persistence_validate.toml
├── composition_proprioception_validate.toml
└── composition_interactive_validate.toml
```

## How to Create Your Spring's Composition

### Step 1: Identify your science API

What JSON-RPC methods does your spring expose? Examples:

| Spring | Example methods |
|--------|-----------------|
| hotSpring | `physics.simulate`, `physics.gpfifo_status`, `shader.compile` |
| wetSpring | `biology.diversity_index`, `biology.nmf_decompose` |
| groundSpring | `geology.erosion_rate`, `geology.spectral_classify` |
| neuralSpring | `neural.classify`, `neural.train_step` |
| healthSpring | `health.metabolic_rate`, `health.population_model` |
| airSpring | `air.weather_forecast`, `air.et0_compute` |
| ludoSpring | `game.evaluate_flow`, `game.wfc_step`, `game.engagement` |

### Step 2: Create your deploy graph

Template (adapt from `graphs/compositions/game_science_standalone.toml`):

```toml
[graph]
name = "yourspring_science"
description = "Your science subsystem"
version = "1.0.0"
coordination = "sequential"

[[graph.node]]
name = "biomeos_neural_api"
binary = "biomeos"
order = 0
required = true
spawn = false
health_method = "graph.list"
by_capability = "orchestration"

[[graph.node]]
name = "beardog"
binary = "beardog_primal"
order = 1
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.liveness"
by_capability = "security"

[[graph.node]]
name = "songbird"
binary = "songbird_primal"
order = 2
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.liveness"
by_capability = "discovery"

[[graph.node]]
name = "yourspring"
binary = "yourspring_primal"
order = 3
required = true
depends_on = ["beardog", "songbird"]
health_method = "health.check"
by_capability = "your_domain"
args = ["server"]
capabilities = ["your.method1", "your.method2"]
```

### Step 3: Create your validation graph

Template (adapt from `graphs/spring_validation/composition_game_science_validate.toml`):

```toml
[graph]
name = "yourspring_validate"
description = "Validates your science composition"
version = "1.0.0"
coordination = "sequential"

# ... biomeOS substrate check ...
# ... Tower health check ...
# ... Your spring liveness ...
# ... Your science method checks with expected params ...
```

### Step 4: Test it

```bash
python3 tools/validate_compositions.py  # or write your own validator
```

## What to Reference in wateringHole

- `infra/wateringHole/STANDARDS_AND_EXPECTATIONS.md` — coding standards
- `infra/wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — JSON-RPC method naming
- `infra/wateringHole/BIOMEOS_LEVERAGE_GUIDE.md` — biomeOS integration
- `primalSpring/docs/PRIMAL_GAPS.md` — known primal gaps to work around
- `primalSpring/graphs/compositions/` — composition graph examples

## The Division of Labor

| Team | Focus |
|------|-------|
| **primalSpring** | Composition, deployment, gap resolution, biomeOS substrate |
| **ludoSpring** | Game science and function (flow, engagement, WFC) |
| **esotericWebb** | Narrative product evolution |
| **Science springs** | Composition to useable science deployed via primals |
| **Primal teams** | Fix gaps documented in `PRIMAL_GAPS.md` |
| **biomeOS** | Substrate improvements per team feedback |

## Key Lesson

The thin gateway pattern works: browser → WebSocket → biomeOS capability.discover
→ primal IPC. Zero business logic in the transport layer. All domain logic lives
in primals. All routing lives in biomeOS. All validation lives in graphs.
This is the model for all spring deployments.
