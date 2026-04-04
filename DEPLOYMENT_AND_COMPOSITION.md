# Deployment and Composition — Architecture Patterns

**Version:** 1.0.0  
**Date:** April 4, 2026  
**Status:** Active  

This document consolidates: `COMPOSITION_PATTERNS.md`, `NEURAL_API_GRAPH_DEPLOYMENT_STANDARD.md`, `BYOB_DEPLOY_GRAPH_SCHEMA.md`, `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md`, `SPRING_NICHE_DEPLOYMENT_GUIDE.md`, `GEN4_BRIDGE.md`, `SPOREGARDEN_DEPLOYMENT_STANDARD.md`, `FIELDMOUSE_DEPLOYMENT_STANDARD.md`, `GATE_DEPLOYMENT_STANDARD.md`, `WORKSPACE_LAYOUT.md`.

---

## Composition Patterns

### Layered model

| Layer | Role |
|-------|------|
| **Graph (TOML DAG)** | What to start, order, capabilities |
| **Niche (YAML)** | What the deployment *is* (organisms, interactions, customization) |
| **Launch profile (TOML)** | How each binary is invoked (subcommand, ports, health) |
| **Socket discovery** | How primals find each other at runtime (8-step resolution) |

biomeOS reads a graph, germinates primals in dependency order, discovers sockets, and wires capabilities via the Neural API.

**Core principle (Neural API standard):** Deploy graphs declare *what* a composition needs (capabilities), not *who* provides it. biomeOS resolves providers at runtime via the capability registry.

```
Spring declares what it needs → biomeOS resolves who provides it → Neural API routes calls
```

### Deploy graph formats

**Format A — `[[graph.node]]` (canonical for new compositions):** Used by primalSpring validation graphs and single-gate compositions.

```toml
[graph]
name = "tower_atomic_bootstrap"
description = "Tower Atomic: BearDog + Songbird"
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

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Unique node identifier |
| `binary` | yes | Binary name from plasmidBin |
| `order` | yes | Germination order |
| `required` | yes | `true` = abort on failure; `false` = graceful skip |
| `depends_on` | no | Nodes that must complete first |
| `health_method` | no | JSON-RPC health probe (default `health.check` in some stacks; canonical probe is `health.liveness` per Neural API) |
| `by_capability` | no | Capability domain for Neural API routing |
| `capabilities` | no | Capabilities after germination |
| `spawn` | no | `false` = connect to existing process |

**Neural API normative node fields** (when using capability-centric graphs):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Unique within graph |
| `by_capability` | String | Yes | Capability domain this node requires |
| `depends_on` | String[] | Yes | Prerequisite node names |
| `fallback` | String | No | `skip`, `error` (default) |
| `optional` | Boolean | No | Default false |

**Format B — `[[nodes]]`:** Multi-node / product compositions (esotericWebb, multi-gate).

```toml
[graph]
id = "esotericwebb_full"
description = "Esoteric Webb full deploy"
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

| Aspect | `[[graph.node]]` | `[[nodes]]` |
|--------|------------------|-------------|
| Scale | Single-gate | Multi-gate, multi-arch |
| Node id | `name` | `id` |
| Primal routing | `by_capability` on node | `[nodes.primal]` |
| Environment | Not in base schema | `[nodes.operation.environment]` |
| Hardware | Not in base schema | `[nodes.hardware]` |
| Constraints | Not in base schema | `[nodes.constraints]` |

**Migration:** Single-gate `[[graph.node]]` graphs need not migrate until spanning multiple architectures or gates; then convert to `[[nodes]]` and add hardware/environment/constraints.

**Shared features:** `[graph]` header; `[graph.metadata]`; `[graph.bonding_policy]`; dependencies; `${variable}` interpolation; coordination patterns: Sequential, Parallel, ConditionalDag, Pipeline, Continuous.

**Graph metadata example:**

```toml
[metadata]
name = "tower_atomic_bootstrap"
version = "1.0.0"
description = "Tower Atomic: security + discovery"
pattern = "sequential"
```

Deploy graphs live under `graphs/` in the spring workspace.

### Topological ordering

- **Waves:** `topological_waves()` (Kahn's algorithm) — nodes with no unmet dependencies start in the same wave (parallel).
- **Cycles:** Graphs MUST be acyclic; validate at test time.
- **Health gating:** Each primal in a wave SHOULD respond to `health.liveness` before the next wave (AtomicHarness timeout, default 30s per wave).

### Capability resolution (Neural API)

When biomeOS sees `by_capability = "compute"`:

1. Neural API capability registry (runtime)
2. Capability-named socket (`compute.sock` in nucleation directory)
3. Socket registry file
4. Manifest file
5. Default socket path conventions

**Provider methods (discoverable primals):**

| Method | Response | Required |
|--------|----------|----------|
| `health.liveness` | e.g. `{"status": "alive"}` | Yes |
| `capabilities.list` | Array of capability strings/objects | Yes |

**Capability registry example** (`config/capability_registry.toml`):

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

### Validation requirements

- **Structural:** Required fields, no unknown fields (per implementation).
- **Topological:** DAG acyclic; `topological_waves()` succeeds.
- **Capability:** `by_capability` values registered where enforced.
- **Live:** Spawn from plasmidBin; `health.liveness`; `capabilities.list`; inter-primal routing tests.

### Niche YAML

Metadata contract between product (gen4) and biomeOS. Declares organisms, interactions, `deploy_graph`, customization.

```yaml
niche:
  id: "esoteric-webb"
  name: "Esoteric Webb CRPG Niche"
  version: "1.0.0"
  deploy_graph: "graphs/esotericwebb_full.toml"

organisms:
  primals:
    beardog:
      type: "beardog"
      required: true
      role: "security"
      capabilities: ["crypto.sign", "crypto.encrypt"]

interactions:
  - from: "esotericwebb"
    to: "ludospring"
    type: "capability_call"
    config:
      capabilities: ["game.evaluate_flow"]

customization:
  options:
    provenance_enabled:
      type: boolean
      default: true
```

### Primal launch profiles

Contract between product launcher and plasmidBin binaries (`config/primal_launch_profiles.toml`):

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
```

| Field | Role |
|-------|------|
| `subcommand` | Server mode subcommand |
| `health_method` | Readiness probe |
| `default_port` | Fallback TCP |
| `readiness_timeout_secs` / `readiness_poll_ms` | Wait loop |
| `domain` | Capability routing |

**Environment forwarding:**

```toml
[profiles.myprimal.passthrough_env]
MY_API_KEY = true
CUDA_VISIBLE_DEVICES = true
```

TCP: primals SHOULD accept `--port 0` for ephemeral ports in parallel tests.

### Socket discovery (8-step order)

First successful probe wins.

| Step | Method | Example |
|------|--------|---------|
| 1 | Env hint | `BEARDOG_SOCKET=...` or `BEARDOG_TCP=127.0.0.1:9100` |
| 2 | Capability-first sockets | `security.sock`, `crypto.sock` |
| 3 | `XDG_RUNTIME_DIR` | `/run/user/1000/biomeos/beardog-<hash>.sock` |
| 4 | Abstract socket (Linux) | `@biomeos_beardog_<hash>` |
| 5 | Family-scoped `/tmp` | `/tmp/beardog-<hash>.sock` |
| 6 | Socket registry | `$XDG_RUNTIME_DIR/biomeos/socket-registry.json` |
| 7 | Capability registry via Neural API | Query provider endpoint |
| 8 | TCP fallback | e.g. `127.0.0.1:9100` |

**Tiers:** Native (UDS/abstract) vs universal (TCP).

**Family scoping:** Paths include family_id hash for namespace isolation.

| Variable | Role |
|----------|------|
| `BIOMEOS_SOCKET_DIR` | Socket directory override |
| `{PRIMAL}_SOCKET` / `{PRIMAL}_TCP` | Per-primal hints |
| `FAMILY_ID` | Namespace |
| `XDG_RUNTIME_DIR` | Runtime base |

**Nucleation pattern (Neural API):** `{base_dir}/{family_id}/{primal_name}.sock`

### Graph lifecycle (biomeOS)

```
graph.execute(graph_path)
  → parse ([[graph.node]] or [[nodes]])
  → topological sort
  → for each node: spawn if needed → health → register capabilities → optional operation
  → result
```

### Reference implementations

| Item | Location |
|------|----------|
| primalSpring graphs | `primalSpring/graphs/*.toml` |
| `topological_waves()` | `primalSpring/ecoPrimal/src/deploy.rs` |
| AtomicHarness | `primalSpring/ecoPrimal/src/harness/mod.rs` |
| biomeOS executor | `biomeOS/biomeos-graph/` |
| Socket discovery | `biomeOS/crates/biomeos-core/src/socket_discovery/mod.rs` |

---

## BYOB Deploy Graph Schema

**License (source standard):** AGPL-3.0-or-later (documentation: CC-BY-SA-4.0 where noted in original).

Canonical TOML for Build Your Own Biome deploy graphs. Springs, gardens, and primals parse independently; **this document is the shared artifact** (no shared crate).

**Purpose:** BYOB graphs declare *what* to deploy. biomeOS execution graphs (`[[nodes]]` / `[[graph.nodes]]`) describe *how* to execute; biomeOS should ingest BYOB by converting internally.

### Top-level structure

```toml
[graph]
name = "my_niche_deploy"
description = "Human-readable description"
version = "1.0.0"
coordination = "sequential"

[[graph.node]]
# one or more nodes
```

Top-level table is `[graph]`. Nodes: `[[graph.node]]` (singular `node`).

### `[graph]` fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | String | Yes | — | snake_case identifier |
| `description` | String | No | `""` | Human text |
| `version` | String | No | `""` | Semver of graph |
| `coordination` | String | No | null | `sequential`, `parallel`, `continuous` |

### `[[graph.node]]` fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | String | Yes | — | Primal name (lowercase, no hyphens) |
| `binary` | String | Yes | — | Binary to invoke |
| `order` | Integer | Yes | — | Startup order (same order → parallel hint) |
| `required` | Boolean | No | `false` | Fail deployment if node cannot start |
| `spawn` | Boolean | No | `true` | `false` = pre-existing (e.g. substrate) |
| `depends_on` | String[] | No | `[]` | Prerequisites |
| `health_method` | String | Yes | — | JSON-RPC health probe |
| `by_capability` | String | No | null | Discovery domain |
| `capabilities` | String[] | No | `[]` | Provided capabilities |
| `args` | String[] | No | `[]` | CLI args |
| `fallback` | String | No | null | e.g. `skip` |
| `port` | Integer | No | null | TCP hint |

**Capability naming:** `domain.verb[.variant]` (see Semantic Method Naming Standard).

### Phase convention

| Phase | Role | Convention |
|-------|------|------------|
| 0 | biomeOS substrate | `spawn = false`, `required = true`, `order = 0` |
| 1 | Tower Atomic | BearDog + Songbird, `order` 1–2 |
| 2–N | Extensions | Domain primals |
| N+1 | Product | Spring/garden binary |
| 99 | Validation | Often `spawn = false`, `order = 99` |

### Topological rules

- `biomeos_neural_api` in wave 0 (no deps).
- Tower primals wave 1.
- `depends_on` targets must exist; graph acyclic.

### Health contract

Probe via `health_method`. Canonical response shape:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "name": "<primal_name>",
    "status": "healthy",
    "version": "<semver>",
    "capabilities": ["domain.method_one"]
  },
  "id": 1
}
```

Consumers MAY accept `primal` as alias for `name`; **`name` is canonical.**

### Structural validation checklist

1. `graph.name` non-empty  
2. At least one `graph.node`  
3. Each node: non-empty `name`, `binary`, `health_method`  
4. `depends_on` references existing names  
5. Acyclic  
6. Unique node names  

### Minimum viable example

```toml
[graph]
name = "example_tower_deploy"
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
capabilities = ["graph.deploy", "capability.discover"]

[[graph.node]]
name = "beardog"
binary = "beardog_primal"
order = 1
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.check"
by_capability = "security"
capabilities = ["crypto.sign", "crypto.verify", "crypto.identity"]

[[graph.node]]
name = "songbird"
binary = "songbird_primal"
order = 2
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.check"
by_capability = "discovery"
capabilities = ["net.discovery", "net.mesh"]

[[graph.node]]
name = "your_binary"
binary = "your_binary"
order = 3
required = true
depends_on = ["beardog", "songbird"]
args = ["serve"]
health_method = "health.liveness"
by_capability = "your_domain"
```

### BYOB vs biomeOS execution mapping

| BYOB | biomeOS execution |
|------|-------------------|
| `name` | `id` |
| `binary` | resolved from registry |
| `order` | from dependency graph |
| `depends_on` | edges |
| `by_capability` | `capability` |
| `health_method` | health probe config |
| `required` | failure handling |
| `spawn` | pre-existing vs spawned |

Detect BYOB by `[[graph.node]]` vs `[[nodes]]` / `[[graph.nodes]]` and convert.

### Implementations (independent)

- primalSpring `ecoPrimal/src/deploy/mod.rs`
- ludoSpring `barracuda/src/deploy/mod.rs`
- esotericWebb `graphs/*.toml`
- biomeOS: `[[graph.node]]` ingestion (see ecosystem gap notes)

---

## Spring-as-Niche Deployment

**Compliance:** Mandatory for springs targeting biomeOS deployment (standard); deployment guide is procedural reference.

### Terminology

| Term | Definition |
|------|------------|
| Spring | Science primal — domain capabilities over JSON-RPC |
| Niche | Composed biome: primals/chimeras/interactions as a unit |
| Deploy graph | TOML DAG: germination order and wiring |
| Chimera | Fused multi-primal organism |
| BYOB | Build Your Own Biome — customizable niche |
| Germination | Start primal and wait for socket |

**Principle:** A spring is a sovereign primal; biomeOS composes niches via graphs; springs do not embed each other's code.

### Mandatory: UniBin binary

```bash
<spring> server    # IPC server
<spring> status    # Health
<spring> version   # Version info
```

`server` MUST: JSON-RPC 2.0 on Unix socket; register with Neural API when available; `health.check` and `capability.list` (guide also uses `capability.list`; align with registry); clean SIGTERM.

**Socket:** `$XDG_RUNTIME_DIR/biomeos/<spring>-${FAMILY_ID}.sock` (override `<SPRING_UPPER>_SOCKET`).

### Capability domain registration

**A. `config/capability_registry.toml`:**

```toml
[domains.<spring>]
provider = "<spring>"
capabilities = ["<domain>", "<alias1>"]

[translations.<domain>]
"<domain>.<method1>" = { provider = "<spring>", method = "<domain>.<method1>" }
```

**B. `capability_domains.rs`:** `CapabilityDomain { provider, capabilities }`.

### Mandatory: deploy graph

Path: `graphs/<spring>_deploy.toml`. Phases: Tower Atomic → optional deps → spring → validation (see standard for full `[[nodes]]` template with `[nodes.primal]`, `[nodes.operation]`, `[nodes.constraints]`, `[nodes.capabilities_provided]`).

### Recommended: niche YAML

See Composition Patterns for structure; standard includes full template with `organisms.primals`, `interactions`, optional `chimera` fusion.

### Discovery and health

- No hardcoded primal names in production; `BIOMEOS_STRICT_DISCOVERY=1` optional.
- `health.check` response includes status, primal/name, version, capabilities.

### Coordination patterns

Sequential (default), Parallel, ConditionalDag (`condition` / `skip_if`), Pipeline (streaming; NDJSON/stream items; `fallback = "skip"` for optional enrichment), Continuous (`[graph.tick]` `target_hz`, per-node `budget_ms`; methods like `tick`/`frame`).

### Compliance checklist (abbreviated)

UniBin; JSON-RPC UDS; socket convention; `health.check` + capability listing; registry + domains; deploy graph; no hardcoded names; `#![forbid(unsafe_code)]`; AGPL-3.0; `lifecycle.register`; SIGTERM; Pipeline/Continuous extras when used.

### Evolution path (standard + guide)

1. IPC server  
2. Register capability domain  
3. Atomic deploy via graph  
4. Pipeline participation (optional)  
5. Continuous/tick (optional)  
6. Niche YAML  
7. Chimeras  
8. BYOB templates  
9. Emergent systems via Neural API  

**Guide evolution (groundSpring / airSpring pattern):**

```
Python baseline → Rust validation → GPU → sovereign pipeline → niche deployment
```

**Four artifacts:** UniBin; deploy graph; niche YAML; capability domain. Optional: provenance, dispatch, server modules.

**Steps (guide):** Define domain constants; implement UniBin `main` match on `server|status|version`; dispatch module; deploy graph with `by_capability` and optional `fallback = "skip"` for ToadStool/NestGate/Provenance Trio; niche YAML; graph-level Provenance Trio nodes (`fallback = "skip"`); evolve legacy graphs (version pins, capability namespace, `discover_by_capability`, capability_call vs raw RPC).

**Reference spring status (snapshot from sources):** groundSpring, airSpring, ludoSpring listed complete in guide; others partial — see original `SPRING_NICHE_DEPLOYMENT_GUIDE.md` for tables.

---

## Deployment Classes

This section merges **Gate** (operational substrate), **sporeGarden** (gen4 products / BYOB niche), and **fieldMouse** (minimal embedded unit). They are different *scales* of deployment, not interchangeable labels.

### Gate (operational substrate)

A **gate** is any device running the full ecoPrimals stack (sovereign, no required cloud). Examples: Eastgate (dev), biomeGate (multi-GPU HPC), flockGate (remote mesh), pixelGate (aarch64 mobile), friendGate (generic remote bootstrap).

**Desktop/server (x86_64):** Pop!_OS preferred; Ubuntu LTS acceptable; Linux 6.x+; systemd; apt + flatpak; cargo.

**Mobile (aarch64):** GrapheneOS preferred; musl-static via ADB; abstract UDS + TCP; no package manager on device.

**Toolchain:** Rust stable + nightly; clippy/rustfmt; wgpu; no CUDA SDK — portable path via wgpu/Vulkan; coralReef sovereign path may need VFIO (`intel_iommu=on` / `amd_iommu=on`).

**Minimum desktop (typical):** 8-core x86_64; Vulkan GPU; 16 GB RAM; SSD; Linux with Vulkan.

**plasmidBin:** Public `ecoPrimals/plasmidBin` (fetch/harvest/metadata) vs local `infra/plasmidBin/` (deploy_gate, deploy_pixel, doctor, binaries). Fetch: `./fetch.sh`; start: `source ports.env && ./start_primal.sh <name>`; harvest after local builds.

**Canonical TCP ports (`ports.env`):** BearDog 9100; Songbird 9200; NestGate 9300; ToadStool 9400; Squirrel 9500; petalTongue 9600; ludoSpring 9650; biomeOS 9800. Same host prefers UDS; TCP for cross-gate, Docker, firewall, ADB forward.

**Deployment patterns:** Dev (source build + harvest); bootstrap remote (`bootstrap_gate.sh`); mobile ADB (`deploy_pixel.sh`); SSH push (`deploy_gate.sh`).

**Dark Forest seeds:** Beacon seed (shared, discovery) vs lineage seed (per device, authorization). `seed_workflow.sh` lifecycle.

**Network topologies:** LAN; hotspot; WAN+NAT (port forward / STUN / relay).

**Directory on gate (abbrev.):** `~/Development/ecoPrimals/` with `primals/`, `springs/`, `gardens/`, `infra/` — details in Workspace Layout below.

### sporeGarden (gen4 product)

**Definition:** gen4 tool end users run; composes primals via IPC; **never** imports primal source.

**BYOB:** Pre-built ecoBin binaries from `plasmidBin/`; `fetch.sh` populates local store; multi-arch; checksummed releases.

**Reference layout (esotericWebb):** `config/primal_launch_profiles.toml`, `graphs/*.toml`, `niches/*.yaml`, `plasmidBin/`, `src/bridge/` (PrimalBridge).

**Domains consumed (Webb example):** security, discovery, game, visualization, ai; optional compute + provenance trio (graceful skip).

**Graceful degradation:** Mandatory — absent optional primals reduce features, do not crash.

**Deploy flow:** fetch binaries → `biomeos deploy --graph ...` → run product (`cargo run --release --bin ...`).

**Environment:** `FAMILY_ID` required; `BIOMEOS_SOCKET_DIR`, `XDG_RUNTIME_DIR`; per-primal `*_SOCKET` / `*_TCP`; optional Dark Forest vars (Songbird/BearDog beacon).

**Responsibility split:** biomeOS parses graph, germinates, health-probes, registers capabilities, socket discovery. Product defines graph, niche, launch profiles, PrimalBridge, degradation, fetch.

**New product checklist:** Repo in sporeGarden; niche YAML; deploy graph; launch profiles; PrimalBridge; degradation; fetch script; local test. Quality: runs with required primals only; degrades per optional; `biomeos validate --graph`; semantic method names; zero primal source imports.

### fieldMouse (minimal deployable structure)

**Definition:** Smallest deployable unit — **deployment class**, not a primal. As few as one Tower chimera; **no biomeOS**, no deploy graph at runtime; static composition, often one binary (chimera).

**Invariants:** Minimal subset of atomics; embedded-first (RISC-V, ARM, SoCs); ecoBin compliant; mesh via Songbird (UDP/TCP) or serial; provenance via BearDog signing; `health.check` / `capability.list`; deterministic boot.

**Ladder:** NUCLEUS → Niche (biomeOS graph) → **fieldMouse** (minimal, no biomeOS).

**Classes (examples):** Tower (BearDog + Songbird); Sensor; Edge (Tower + ToadStool + barraCuda); Store (Tower + NestGate); Lab (Tower + NestGate + domain spring).

**Chimera:** One process, merged JSON-RPC namespace.

**Hardware reference table (excerpt):** RISC-V MCU; ARM Cortex-M; Pi Zero → Pi 4/5; Coral; Jetson; lab SoC. Build examples:

```bash
cargo build --target riscv32imc-unknown-none-elf --release
cargo build --target thumbv7em-none-eabihf --release
cargo build --target aarch64-unknown-linux-musl --release
```

**fieldMouse frame (concept):** Signed JSON-RPC notification with device id, timestamp, optional geo, readings, provenance (see original standard for JSON).

**Subtypes:** e.g. `fm-soil`, `fm-air`, `fm-pipette`, `fm-classify` — pattern `fm-<domain>[-<specialization>]`.

**Mesh:** Leaf nodes; beacon → gate registers remote provider; offline: buffer signed frames, sync when connected.

**Not:** not a niche (no biomeOS graph); not a gate; not gen4 “product” in the sporeGarden sense — it is an edge/sensor deployment pattern.

**Growth path:** fieldMouse → add NestGate → add barraCuda → add biomeOS (becomes niche) → full NUCLEUS.

---

## gen4 Bridge

**Organizations:**

| Org | Role | Gen |
|-----|------|-----|
| ecoPrimals | Binaries + infrastructure | gen2 |
| syntheticChemistry | Springs | gen3 |
| sporeGarden | Products | gen4 |

**Flow:** Primal builds binary → `harvest.sh` → plasmidBin Release → spring validates → gen4 `fetch.sh` → IPC composition → `EVOLUTION_GAPS.md` → feedback to primals/springs.

**Primal teams:** Binary is the interface; plasmidBin is the deployment surface (`harvest.sh`, GitHub Release, `fetch.sh`).

**Spring teams:** Gap pressure from gen4 products drives evolution (example gaps: petalTongue payloads, Squirrel constraints, Songbird discovery, ludoSpring binary, RulesetCert, automation).

**Product teams:** Consume binaries only; graceful degradation mandatory; BYOB graphs + biomeOS; file gaps + wateringHole handoffs.

**Generational contrast:**

| | gen3 | gen4 |
|---|------|------|
| Output | Papers, checks | Tools, products |
| Primals | Study subjects | Invisible infrastructure |
| Coupling | Source-level | Binary-only IPC |

**primalSpring (composition validation):** Webb graphs may reference `primalspring_primal` with `spawn = false` and capabilities like `composition.webb_*_health` (tower, node, nest, ai_viz, provenance, full) — contracts for bridge work.

**ludoSpring:** `game.*` RPCs; plasmidBin deployment was flagged critical in source doc.

**SporeGarden pattern:** Spring validates → primals ship → product composes → gaps filed → spring evolves → repeat.

---

## Workspace Layout

**Authority:** wateringHole. Canonical root: `ecoPrimals/` (no monorepo).

```
ecoPrimals/
  primals/          # ecoPrimals org — flat list (barraCuda, bearDog, biomeOS, ...)
  springs/          # syntheticChemistry — airSpring, groundSpring, ..., primalSpring, wetSpring
  gardens/          # sporeGarden — esotericWebb, blueFish, ...
  infra/            # ecoPrimals — agentReagents, benchScale, plasmidBin, sporePrint, wateringHole, whitePaper
  sort-after/       # ionChannel, rustChip (see original for status)
```

**Org mapping:**

| Directory | GitHub org |
|-----------|------------|
| `primals/` | ecoPrimals |
| `springs/` | syntheticChemistry |
| `gardens/` | sporeGarden (blueFish transfer pending) |
| `infra/` | ecoPrimals (+ some syntheticChemistry tools) |

**Cross-repo paths (after migration):** From spring root: `../../primals/barraCuda/crates/barracuda`; from nested crates, add `../` segments per depth. See original for migration table from `phase1`/`phase2`/`ecoSprings`.

**Pending transfers:** blueFish → sporeGarden; coralForge rename (future).

**bootstrap.sh:** Sets up or migrates layout; warns on old Cargo path patterns.

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-04-04 | Consolidated deployment and composition standards listed in header. |

**Sources consolidated:** `BYOB_DEPLOY_GRAPH_SCHEMA.md`, `COMPOSITION_PATTERNS.md`, `NEURAL_API_GRAPH_DEPLOYMENT_STANDARD.md`, `SPRING_AS_NICHE_DEPLOYMENT_STANDARD.md`, `SPRING_NICHE_DEPLOYMENT_GUIDE.md`, `GEN4_BRIDGE.md`, `SPOREGARDEN_DEPLOYMENT_STANDARD.md`, `FIELDMOUSE_DEPLOYMENT_STANDARD.md`, `GATE_DEPLOYMENT_STANDARD.md`, `WORKSPACE_LAYOUT.md`.

**Related (not merged):** Semantic Method Naming, Capability Discovery, Primal IPC, UniBin/ecoBin standards, PRIMAL_REGISTRY, whitePaper neuralAPI docs.
