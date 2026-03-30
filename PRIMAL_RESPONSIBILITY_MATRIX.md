# Primal Responsibility Matrix — Cross-Primal Concern Ownership

**Date:** March 30, 2026
**Source:** ludoSpring V35.3 ecosystem evolution review + soft overstep audit
**Purpose:** Define which primal OWNS each concern domain, which primals should DELEGATE, and where OVERSTEP has been identified. This matrix governs boundary evolution and informs deploy graph design.
**Note:** coralReef/glowplug dispatch boundary is deferred — actively in GPU development.

---

## Atomic Compositions (reference)

| Composition | Members | Purpose |
|-------------|---------|---------|
| **Tower Atomic** | bearDog + songBird | Security + Network foundation |
| **Nest Atomic** | Tower + nestGate | Adds storage/permanence |
| **Meta-tier** | biomeOS, Squirrel, petalTongue | Orchestration, AI, Visualization — interact with and extend all atomics |

---

## Concern Matrix

Legend:
- **OWNS** — This primal is the canonical provider for this concern
- **DELEGATES** — This primal should call the owner via IPC for this concern
- **OVERSTEP** — This primal currently implements this concern locally but should delegate
- **EXTENDS** — Meta-tier primal that augments this concern across all atomics
- **N/A** — Not relevant to this primal
- **(deferred)** — Boundary under active development, not yet adjudicated

| Concern | bearDog | songBird | nestGate | toadStool | coralReef | barraCuda | biomeOS | Squirrel | petalTongue |
|---------|---------|----------|----------|-----------|-----------|-----------|---------|----------|-------------|
| **Crypto / Signing** | **OWNS** | OVERSTEP | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A |
| **Network / Transport** | N/A | **OWNS** | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A |
| **Discovery / Registry** | OVERSTEP | DELEGATES | OVERSTEP | OVERSTEP | N/A | N/A | **OWNS** | N/A | N/A |
| **Storage / Permanence** | N/A | OVERSTEP | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A |
| **AI / MCP** | OVERSTEP | N/A | OVERSTEP | OVERSTEP | N/A | N/A | N/A | **OWNS** / EXTENDS | N/A |
| **Compute / GPU dispatch** | N/A | N/A | N/A | **OWNS** | (deferred) | DELEGATES | N/A | N/A | N/A |
| **Shader Compilation** | N/A | N/A | N/A | DELEGATES | **OWNS** (deferred) | N/A | N/A | N/A | N/A |
| **Math / Numerical** | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A |
| **Orchestration** | N/A | N/A | OVERSTEP | OVERSTEP | N/A | N/A | **OWNS** | N/A | N/A |
| **Visualization** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** / EXTENDS |
| **Hardware Inventory** | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A |

---

## Overstep Detail by Primal

### nestGate (ancestor primal — most overstep)

As the oldest primal, nestGate accumulated functionality that now belongs to specialized primals.

| Overstep Area | Crate / Module | Dependencies to Shed | Delegate To |
|--------------|----------------|---------------------|-------------|
| **Crypto** | `nestgate-security` | `aes-gcm`, `argon2`, `ed25519-dalek`, `hmac`, `sha2`, `md5`, JWT, certificates | bearDog via `crypto.*` IPC |
| **Discovery** | `nestgate-discovery` | mDNS, Consul, K8s discovery, capability/service/network discovery | biomeOS Neural API + songBird |
| **Network** | `nestgate-network` | `axum`, `tower`, `reqwest`, `rustls`, load balancer, routing, QoS, HTTP server | songBird via `network.*` IPC |
| **AI / MCP** | `nestgate-mcp` | MCP protocol integration | Squirrel via biomeOS Neural API |
| **Orchestration** | `nestgate-automation` | "Intelligent automation and ecosystem integration" | biomeOS Neural API graph execution |
| **ecoBin violation** | `nestgate-installer` | `reqwest` + `rustls` pulls `aws-lc-rs` (C dependency) | Remove C dep; use songBird for HTTP |

**Priority:** High — nestGate's core domain is storage/permanence (Nest Atomic). Crypto, discovery, network, and orchestration should all flow through Tower Atomic peers (bearDog, songBird) and biomeOS.

### bearDog

| Overstep Area | Module | Delegate To |
|--------------|--------|-------------|
| **HTTP REST API** | `beardog-integration` | songBird (network transport is songBird's domain) |
| **TCP JSON-RPC server** | `beardog-ipc` | Standard UDS JSON-RPC per wateringHole conventions |
| **mDNS/DNS-SD discovery** | `beardog-discovery` | biomeOS Neural API capability registration |
| **AI-driven optimization** | `beardog-utils/ai_optimization` | Squirrel via biomeOS |
| **Deployment orchestration** | `beardog-deploy`, `beardog-production` | biomeOS deploy graphs |

**Priority:** Medium — bearDog's core domain is crypto/signing. Transport, discovery, AI, and deployment are outside its boundary.

### songBird

| Overstep Area | Module / Dep | Delegate To |
|--------------|-------------|-------------|
| **Local crypto primitives** | `sha2`, `hmac`, `ed25519-dalek` in various crates | bearDog via `crypto.*` IPC |
| **Embedded persistence** | `sled` database | nestGate via `storage.*` IPC |

**Priority:** Low — songBird's overstep is minimal. Crypto deps may be acceptable for TLS handshake internals, but signing/hashing for application-level operations should route through bearDog.

### toadStool

| Overstep Area | Crate / Module | Delegate To |
|--------------|----------------|-------------|
| **Discovery relay** | `science_domains.rs` forwarding | biomeOS Neural API (toadStool should register capabilities, not relay discovery) |
| **Shader compile proxy** | `shader.rs` compile proxy | coralReef directly (toadStool dispatches compiled shaders, doesn't compile) |
| **AI / Ollama inference** | `ollama.rs`, local LLM | Squirrel via biomeOS Neural API |
| **Security sandbox** | `toadstool-security-sandbox` | bearDog (if crypto) or OS-level sandboxing |
| **HTTP server** | `axum`, `tower` in `toadstool-server` | songBird (or standard UDS JSON-RPC per wateringHole) |
| **Network** | `hyper` in `toadstool-distributed` | songBird for distributed transport |
| **nestGate integration** | `toadstool-integration-nestgate` | Direct IPC to nestGate is fine, but should not duplicate nestGate functionality |
| **barraCuda capability advertising** | Advertising math capabilities | biomeOS (barraCuda registers its own capabilities since v2.80) |
| **Python FFI** | `pyo3` in `akida-driver`/`akida-models` | ecoBin violation — replace with pure Rust or IPC to external process |

**Priority:** Medium-High — toadStool's core domain is hardware inventory and compute dispatch. Discovery relay, shader compilation, AI, and network transport should be delegated.

### coralReef (deferred)

coralReef and its `glowplug` engine are actively under GPU development. The dispatch boundary between coralReef (shader compilation) and toadStool (hardware dispatch) is not yet finalized.

**Known items** (not yet adjudicated):
- Ships a full sovereign GPU driver and dispatch stack (`coral-driver`, `coral-gpu`)
- Direct device access and lifecycle management (may overlap toadStool)
- `coral-glowplug` and `coral-ember` implement execution as well as compilation

**Action:** Revisit once coralReef GPU development stabilizes. The compile-vs-dispatch boundary will be clarified by coralReef + toadStool teams.

---

## Guidance for Deploy Graph Design

When composing primals via biomeOS deploy graphs:

1. **Crypto operations** → route through `crypto.*` capability (bearDog)
2. **Network transport** → route through `network.*` capability (songBird)
3. **Storage** → route through `storage.*` capability (nestGate)
4. **Math/Tensor** → route through `math.*`/`tensor.*` capability (barraCuda)
5. **GPU dispatch** → route through `compute.*` capability (toadStool)
6. **Shader compilation** → route through `shader.*` capability (coralReef)
7. **AI/ML** → route through `ai.*` capability (Squirrel)
8. **Visualization** → route through `viz.*` capability (petalTongue)
9. **Discovery** → biomeOS Neural API handles capability registration and routing; primals register on startup, not via peer relay

Deploy graphs should **never** route a concern to a primal that is listed as OVERSTEP for that concern. If the owning primal is unavailable, the graph node should use `required = false` for graceful degradation rather than falling back to an overstepping primal.

---

## Evolution Actions

| Primal | Action | Priority | Impact on Deploy Graphs |
|--------|--------|----------|------------------------|
| nestGate | Shed crypto → bearDog IPC, shed discovery → biomeOS, shed network → songBird, shed MCP → Squirrel, fix `aws-lc-rs` C dep | High | Graphs currently routing storage through nestGate are fine; crypto/discovery/network nodes need rerouteing |
| toadStool | Stop relaying discovery, stop proxying shader compilation, shed Ollama/AI, shed HTTP server, shed pyo3 | Medium-High | Graphs should route shader compilation directly to coralReef, AI to Squirrel |
| bearDog | Shed HTTP REST, standardize UDS JSON-RPC, shed mDNS discovery → biomeOS, shed AI optimization → Squirrel | Medium | Graphs routing crypto through bearDog are correct; transport nodes should use songBird |
| songBird | Shed local crypto (application-level) → bearDog, shed sled persistence → nestGate | Low | Minimal graph impact — songBird's network role is correct |
| coralReef | (deferred) Clarify compile-vs-dispatch boundary with toadStool | — | Deferred until GPU stabilization |
| biomeOS | Verify `is_known_primal()` covers all socket naming conventions; ensure `graph.execute` dispatches capability.call per node | Medium | Critical for all composition graphs |

---

## Versioning

This matrix will be updated as primals evolve and shed overstep. Each update should reference the ludoSpring composition experiment results that motivated it.

- **V1 (March 30, 2026)**: Initial matrix from ludoSpring V35.3 ecosystem evolution review
