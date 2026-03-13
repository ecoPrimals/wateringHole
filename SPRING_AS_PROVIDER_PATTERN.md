# Spring-as-Provider Pattern — biomeOS Capability Registration

**Version**: 1.0.0
**Status**: Active
**Last Updated**: March 13, 2026
**Resolves**: SPRING_EVOLUTION_ISSUES ISSUE-007

---

## Overview

This document defines the standard pattern for a Spring (or any science primal)
to register as a capability provider with biomeOS's Neural API. Once registered,
biomeOS can route `capability.call` requests to the Spring, enabling cross-primal
coordination, graph execution, and niche deployment.

## Prerequisites

- biomeOS Tower Node running (BearDog + Songbird at minimum)
- Neural API socket available at `$XDG_RUNTIME_DIR/biomeos/neural-api.sock`
- Spring has a JSON-RPC 2.0 server over Unix domain socket

---

## Architecture

```text
Spring                        biomeOS Neural API            Consumer
  │                                │                           │
  │ 1. Bind UDS socket             │                           │
  │ 2. capability.register ──────► │                           │
  │                                │ ◄── capability.call ──── │
  │ ◄── forwarded JSON-RPC ─────── │                           │
  │ ──── response ───────────────► │ ──── response ──────────► │
```

## Step-by-Step

### Step 1: Bind a JSON-RPC Socket

The Spring starts a JSON-RPC 2.0 server on a Unix domain socket following
the ecosystem socket naming convention:

```
$XDG_RUNTIME_DIR/biomeos/{spring_name}-{family_id}.sock
```

Fallback order (same as all primals):
1. `$XDG_RUNTIME_DIR/biomeos/{spring}-{family}.sock`
2. `/run/user/{uid}/biomeos/{spring}-{family}.sock`
3. `/tmp/{spring}-{family}.sock`

The Spring should serve at least:
- `lifecycle.status` — returns `{ "name": "...", "capabilities": [...] }`
- `health` — basic health check
- All domain-specific methods listed in the capability translations

### Step 2: Register Capabilities with Neural API

After binding the socket, call `capability.register` on the Neural API:

```json
{
  "jsonrpc": "2.0",
  "method": "capability.register",
  "params": {
    "capability": "ecology",
    "primal": "airspring",
    "socket": "/run/user/1000/biomeos/airspring-abc123.sock",
    "source": "startup",
    "semantic_mappings": {
      "et0_fao56": "science.et0_fao56",
      "water_balance": "science.water_balance",
      "yield_response": "science.yield_response"
    }
  },
  "id": 1
}
```

**Parameters**:
- `capability` — the domain name (e.g., `ecology`, `game`, `science`)
- `primal` — Spring identifier
- `socket` — absolute path to the Spring's Unix socket
- `source` — registration source (e.g., `"startup"`, `"graph"`)
- `semantic_mappings` — maps semantic operation names to actual JSON-RPC methods

Multiple domains can be registered with separate calls.

### Step 3: Handle Incoming `capability.call` Requests

When biomeOS routes a `capability.call` to the Spring, the Spring receives a
standard JSON-RPC request with the translated method name:

```json
{
  "jsonrpc": "2.0",
  "method": "science.et0_fao56",
  "params": {
    "temperature_max": 30.5,
    "temperature_min": 18.2,
    "wind_speed": 1.8,
    "solar_radiation": 22.4
  },
  "id": 42
}
```

The Spring processes the request using its internal barracuda library and
returns a standard JSON-RPC response.

### Step 4: Participate in Graph Workflows

Once registered, the Spring can be referenced in biomeOS deploy graphs and
workflow graphs via `capability_call` nodes:

```toml
[[nodes]]
id = "compute-et0"
action = "capability_call"
params = { capability = "ecology.et0_fao56" }
depends_on = ["verify-airspring"]
```

---

## Example: Minimal Spring Provider

```rust
// Simplified example — actual implementation uses barracuda IPC module
use std::os::unix::net::UnixListener;

fn main() -> std::io::Result<()> {
    let socket_path = format!(
        "{}/biomeos/myspring-{}.sock",
        std::env::var("XDG_RUNTIME_DIR").unwrap_or_else(|_| "/tmp".into()),
        std::env::var("FAMILY_ID").unwrap_or_else(|_| "dev".into()),
    );

    let listener = UnixListener::bind(&socket_path)?;

    // Register with Neural API
    register_capabilities(&socket_path);

    // Accept and handle JSON-RPC requests
    for stream in listener.incoming() {
        // ... handle JSON-RPC 2.0 requests ...
    }

    Ok(())
}

fn register_capabilities(socket_path: &str) {
    // Connect to Neural API and call capability.register
    // See ludoSpring barracuda/src/ipc/server.rs for production example
}
```

## Deploy Graph Node Template

Use this template when adding a Spring to a deploy graph:

```toml
[[nodes]]
id = "germinate_myspring"
depends_on = ["germinate_beardog", "germinate_songbird"]
output = "myspring_genesis"
capabilities = ["mydomain"]

[nodes.primal]
by_capability = "mydomain"

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
"mydomain.operation_a" = "mydomain.operation_a"
"mydomain.operation_b" = "mydomain.operation_b"
```

## Registry Configuration

Add the domain to `config/capability_registry.toml`:

```toml
[domains.mydomain]
provider = "myspring"
capabilities = ["mydomain", "sub_capability_1", "sub_capability_2"]

[translations.mydomain]
"mydomain.operation_a" = { provider = "myspring", method = "actual.method_a" }
"mydomain.operation_b" = { provider = "myspring", method = "actual.method_b" }
```

---

## Currently Registered Springs

| Spring | Domain | Capabilities | Status |
|--------|--------|-------------|--------|
| wetSpring | `science` | diversity, anderson, qs_model, kinetics, NMF | Active |
| airSpring | `ecology` | 30+ ET₀, soil, crop, drought, biodiversity | Active |
| ludoSpring | `game` | UI analysis, flow, Fitts, noise, WFC, accessibility | Active |
| neuralSpring | `science` (shared) | spectral, Anderson, Hessian, training trajectory | Active |
| healthSpring | `medical` | anatomy, tissue, surgical tools, biosignal, PK | Active |
| groundSpring | `measurement` | (pending registration) | Planned |
| hotSpring | `physics` | (pending registration) | Planned |

---

## Sovereignty Principles

- Each Spring is autonomous — registration is voluntary, not mandatory
- biomeOS routes by capability, never by hardcoded primal name
- Springs can serve multiple domains and share capabilities
- No Spring has privileged access — all routing goes through Neural API
- Springs can deregister at any time by shutting down their socket
