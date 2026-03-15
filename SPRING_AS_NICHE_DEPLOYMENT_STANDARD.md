# Spring-as-Niche Cooperative Deployment Standard

**Status**: ECOSYSTEM STANDARD  
**Version**: 1.0.0  
**Date**: March 11, 2026  
**Authority**: wateringHole (ecoPrimals Core Standards)  
**Compliance**: Mandatory for all springs targeting biomeOS deployment  
**Reference Implementations**: ludoSpring (game science), petalTongue (visualization), healthSpring (health science niche)

---

## Purpose

This standard defines how **springs** (science primals) become **deployable niches** within biomeOS. It establishes the contract between spring teams and biomeOS so that any spring can be:

1. **Atomically deployed** via a biomeOS deploy graph
2. **Composed into niches** alongside other primals and chimeras
3. **Discovered by capability** at runtime (zero hardcoded names)
4. **Evolved cooperatively** without cross-spring code dependencies

**Core Principle**: A spring is a sovereign primal that exposes capabilities via JSON-RPC over Unix sockets. biomeOS composes springs into niches via graphs. Springs never embed each other's code.

---

## Terminology

| Term | Definition |
|------|-----------|
| **Spring** | A science primal — a Rust binary that provides domain-specific capabilities (game design, visualization, chemistry, physics, etc.) |
| **Niche** | A composed biome — a set of primals, chimeras, and interactions deployed as a unit |
| **Deploy graph** | A TOML DAG describing the germination order and capability wiring for a niche |
| **Chimera** | A fused multi-primal organism with unified API (e.g., gaming-mesh = Songbird + ludoSpring) |
| **BYOB** | Build Your Own Biome — user-customizable niche with options and templates |
| **Capability domain** | A semantic namespace mapping capabilities to provider primals |
| **Germination** | The process of starting a primal and waiting for its socket to appear |

---

## Requirements

### 1. UniBin Binary (MANDATORY)

Every spring MUST provide a single binary following the UniBin standard:

```bash
<spring> server    # Start IPC server (germination mode)
<spring> status    # Health and capability info
<spring> version   # Version info
```

The `server` subcommand MUST:
- Start a JSON-RPC 2.0 server on a Unix socket
- Register with biomeOS Neural API if available (`lifecycle.register`)
- Respond to `health.check` and `capability.list`
- Exit cleanly on SIGTERM

**Socket path convention**:
```
$XDG_RUNTIME_DIR/biomeos/<spring>-${FAMILY_ID}.sock
```

Overridable via `<SPRING_UPPER>_SOCKET` environment variable.

### 2. Capability Domain Registration (MANDATORY)

Each spring MUST define its capability domain in two places:

**A. biomeOS capability registry** (`config/capability_registry.toml`):

```toml
[domains.<spring>]
provider = "<spring>"
capabilities = ["<domain>", "<alias1>", "<alias2>"]

[translations.<domain>]
"<domain>.<method1>" = { provider = "<spring>", method = "<domain>.<method1>" }
"<domain>.<method2>" = { provider = "<spring>", method = "<domain>.<method2>" }
```

**B. biomeOS capability domains** (`capability_domains.rs`):

```rust
CapabilityDomain {
    provider: "<spring>",
    capabilities: &["<domain>", "<alias1>", "<alias2>"],
},
```

Method names follow the Semantic Method Naming Standard: `{domain}.{operation}[.{variant}]`

### 3. Deploy Graph (MANDATORY)

Each spring MUST provide a deploy graph at `graphs/<spring>_deploy.toml`:

```toml
[graph]
id = "<spring>_deploy"
description = "<Spring> atop Node Atomic"
coordination = "Sequential"

# Phase 1: Tower Atomic (always required)
[[nodes]]
id = "germinate_beardog"
# ... (security foundation)

[[nodes]]
id = "germinate_songbird"
depends_on = ["germinate_beardog"]
# ... (discovery foundation)

# Phase 2: Spring-specific dependencies (optional)
# e.g., ToadStool for GPU, NestGate for storage

# Phase 3: The spring itself
[[nodes]]
id = "germinate_<spring>"
depends_on = ["germinate_beardog", "germinate_songbird"]
output = "<spring>_genesis"
capabilities = ["<domain>", "<cap1>", "<cap2>"]

[nodes.primal]
by_capability = "<domain>"

[nodes.operation]
name = "start"

[nodes.operation.params]
mode = "server"
family_id = "${FAMILY_ID}"

[nodes.operation.environment]
BIOMEOS_SOCKET_DIR = "${XDG_RUNTIME_DIR}/biomeos"
FAMILY_ID = "${FAMILY_ID}"

[nodes.constraints]
timeout_ms = 15000

[nodes.capabilities_provided]
"<domain>.<method1>" = "<domain>.<method1>"
"<domain>.<method2>" = "<domain>.<method2>"

# Phase 4: Validation
[[nodes]]
id = "validate_<spring>_atomic"
depends_on = ["germinate_beardog", "germinate_songbird", "germinate_<spring>"]
output = "<spring>_validated"

[nodes.operation]
name = "health_check"

[nodes.operation.params]
check_<spring> = true
timeout_seconds = 15
```

### 4. Niche YAML Definition (RECOMMENDED)

Springs that compose with other primals SHOULD provide a niche YAML:

```yaml
niche:
  id: "<spring>-niche"
  name: "<Spring> Niche"
  version: "1.0.0"
  description: "<Spring> science environment"
  category: "<domain>"
  difficulty: "beginner"
  author: "<team>"
  deploy_graph: "graphs/<spring>_deploy.toml"

  features:
    - "<feature 1>"
    - "<feature 2>"

organisms:
  primals:
    <spring>:
      type: "<spring>"
      required: true
      role: "science"
      capabilities:
        - "<domain>.<method1>"
        - "<domain>.<method2>"
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

  chimeras: {}

interactions:
  - from: "<spring>"
    to: "beardog"
    type: "capability_call"
    config:
      capabilities: ["crypto.encrypt", "crypto.sign"]

  - from: "<spring>"
    to: "songbird"
    type: "capability_call"
    config:
      capabilities: ["discovery.query"]
```

### 5. Chimera Definitions (OPTIONAL)

Springs that fuse with other primals for a unified API MAY define chimeras:

```yaml
chimera:
  id: "<spring>-mesh"
  name: "<Spring> Mesh"
  version: "1.0.0"

components:
  <spring>:
    source: "<spring>"
    modules: ["<domain>"]
  songbird:
    source: "songbird"
    modules: ["discovery", "mesh"]

fusion:
  bindings:
    - provider: "songbird.mesh"
      consumers: ["<spring>"]
      config:
        protocol: "json-rpc"

  api:
    endpoints:
      "<domain>.<method>":
        handler: "<spring>"
      "mesh.discover":
        handler: "songbird"
```

### 6. Discovery Contract (MANDATORY)

Springs MUST support capability-based discovery:

- **No hardcoded primal names** in production code
- Discover peers via `BIOMEOS_SOCKET_DIR` socket scanning or Songbird
- Use `CapabilityTaxonomy` mappings, not primal names
- Support `BIOMEOS_STRICT_DISCOVERY=1` for pure-discovery mode

### 7. Health Contract (MANDATORY)

Springs MUST respond to `health.check`:

```json
{
  "jsonrpc": "2.0",
  "method": "health.check",
  "id": 1
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "healthy",
    "primal": "<spring>",
    "version": "<version>",
    "capabilities": ["<domain>.<method1>", "<domain>.<method2>"],
    "uptime_seconds": 42
  },
  "id": 1
}
```

---

## Coordination Patterns

### Sequential (default)

Standard germination order: security → discovery → dependencies → spring → validate.
Suitable for most springs.

### Continuous (game engine, real-time)

For springs that participate in tick-based coordination (e.g., 60 Hz game loop):

```toml
[graph]
coordination = "Continuous"
tick_hz = 60

[[nodes]]
id = "<spring>_tick"
coordination_mode = "continuous"
```

The continuous coordination pattern is specified in the Game Engine Niche Specification.
Springs participating in continuous niches MUST support `tick` or `frame` JSON-RPC methods.

---

## Compliance Checklist

| # | Requirement | Check |
|---|------------|-------|
| 1 | UniBin binary with `server`, `status`, `version` subcommands | |
| 2 | JSON-RPC 2.0 over Unix socket | |
| 3 | Socket at `$XDG_RUNTIME_DIR/biomeos/<spring>-${FAMILY_ID}.sock` | |
| 4 | `health.check` and `capability.list` methods | |
| 5 | Capability domain in `capability_registry.toml` | |
| 6 | Capability domain in `capability_domains.rs` | |
| 7 | Deploy graph at `graphs/<spring>_deploy.toml` | |
| 8 | No hardcoded primal names in production code | |
| 9 | `#![forbid(unsafe_code)]` | |
| 10 | AGPL-3.0-only license | |
| 11 | Neural API registration (`lifecycle.register`) | |
| 12 | Clean SIGTERM shutdown | |

---

## Reference: Current Spring Status

| Spring | Binary | IPC Server | Deploy Graph | Cap Domain | Niche YAML | Chimera |
|--------|--------|-----------|-------------|-----------|-----------|---------|
| **ludoSpring** | Needs `[[bin]]` | `ipc` feature | `ludospring_deploy.toml` | `capability_domains.rs` | Planned | gaming-mesh |
| **petalTongue** | `petaltongue` | Working | Needs creation | Needs registration | Planned | Planned |
| **wetSpring** | Needs audit | TBD | `wetspring_deploy.toml` | Registered | TBD | TBD |
| **airSpring** | Needs audit | TBD | `airspring_deploy.toml` | Registered | TBD | TBD |
| **hotSpring** | Needs audit | TBD | TBD | TBD | TBD | TBD |
| **healthSpring** | `healthspring_primal` | Working (55+ methods) | `healthspring_niche_deploy.toml` | 6 domains | `healthspring_niche.toml` (5 graphs) | — |

---

## Evolution Path

```
1. Spring implements IPC server (JSON-RPC over Unix socket)
2. Spring registers capability domain in biomeOS
3. biomeOS deploys spring via graph (atomic deployment)
4. Spring composes into niche YAML (usable system)
5. Springs fuse into chimeras (unified APIs)
6. Niches become BYOB templates (user-customizable biomes)
```

Each step is independently valuable. Springs can be deployed atomically (step 3) before niches are defined (step 4).

---

## Related Standards

- `UNIBIN_ARCHITECTURE_STANDARD.md` — Binary naming and subcommand patterns
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Pure Rust, cross-platform compilation
- `UNIVERSAL_IPC_STANDARD_V3.md` — IPC protocol and transport
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming conventions
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC protocol details
- `PRIMAL_REGISTRY.md` — Primal registration and discovery
