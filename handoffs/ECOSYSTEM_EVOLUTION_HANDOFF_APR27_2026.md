# Ecosystem Evolution Handoff — April 27, 2026

**From**: primalSpring Phase 46 (v0.9.17+)
**For**: All primal teams, all spring teams, esotericWebb garden
**Context**: Composition template abstraction complete, BTSP converged, interactive NUCLEUS compositions live

---

## Ecosystem State Summary

| Metric | Value |
|--------|-------|
| NUCLEUS primals | 12/12 ALIVE (all UDS, zero TCP ports by default) |
| BTSP authentication | **13/13** capabilities BTSP-authenticated |
| guideStone | **187/187** ALL PASS (41 bare + 146 live, 8 cells BTSP-enforced) |
| Composition parity | exp094 19/19, exp091 12/12 routing, exp096 14/15 cross-arch |
| Deploy graphs | 67 TOMLs (10 cell graphs for spring/garden deployment) |
| Shell composition library | 41 functions, 1 template, 1 reference implementation |
| plasmidBin | 46 cross-arch binaries, 6 targets, Tier 1 39/39 |
| Handoffs | 17 active, 641 archived |

---

## What We Learned — Composition Patterns for NUCLEUS

### 1. Two Deployment Paths Converge

**Graph-based** (biomeOS Neural API):
- Cell graphs define primal topology → `biomeOS deploy` spawns primals
- Production path. Springs define `cells/*.toml`, biomeOS manages lifecycle
- Currently requires schema alignment (primalSpring `[[graph.nodes]]` vs biomeOS `[[nodes]]`)

**Shell-based** (Interactive exploration):
- `composition_nucleus.sh` starts primals from plasmidBin
- Domain scripts source `nucleus_composition_lib.sh` and implement hooks
- Discovery/prototyping path. Springs explore primal interactions directly
- Discoveries feed back into graph-based deployments

### 2. Capability Discovery Works

`discover_by_capability()` resolves `{cap}-{family}.sock` then falls back to `{cap}.sock`.
All 12 primals register capabilities correctly. Family-aware namespacing allows
multiple NUCLEUS instances on the same machine.

### 3. BTSP Default Everywhere

All primals implement the 4-step BTSP handshake server protocol. The `BtspEnforcer`
uses explicit deny semantics — cleartext connections are FAIL. BearDog is the sole
handshake provider. Every relay primal (ToadStool, barraCuda, coralReef, NestGate,
Squirrel) detects `"protocol":"btsp"` in the first JSON line and routes accordingly.

Public seed fingerprints (BLAKE3) in `plasmidBin/manifest.toml` prove binary
authenticity at Layer 0.5 before any IPC occurs.

### 4. Sensor Stream Architecture (petalTongue)

Discrete event types are now properly isolated:
- `pointer_move` → hover metadata (playstyle tracking)
- `click` → explicit user action
- `key_press` → keyboard input
- `sensor_stream.poll` returns batched events; composition library parses them

### 5. Provenance Trio Integration

| Primal | Role | Status |
|--------|------|--------|
| rhizoCrypt | DAG working memory | UDS responds but `dag.session.create` returns empty (PG-06) |
| loamSpine | Permanent ledger | create/append/seal cycle works reliably |
| sweetGrass | Provenance braids | braid recording works; PROV-O documents attach to state transitions |

Compositions degrade gracefully when rhizoCrypt is non-responsive.

### 6. petalTongue as Interactive Surface

`motor.set_panel` creates panels, `visualization.scene.push` renders scene graphs,
`interaction.subscribe` and `sensor_stream.poll` provide bidirectional input.
Grammar of Graphics engine and Manim-style animation available.
Godot bridge via shared-memory texture upload provides external engine integration.

---

## Per-Primal Evolution Status and Requests

### BearDog (Security) — v0.9.0+ Wave 69
**What's working**: BTSP handshake provider, Ed25519 sign/verify, BLAKE3 hash,
`FAMILY_SEED` entropy hierarchy (mito tier), capability wire standard L2.
**Request**: Nuclear tier entropy (human-mixed, non-clonable identity).
Three-tier genetic awareness in session management.

### Songbird (Discovery/Network) — v0.2.1 Wave 170
**What's working**: BTSP relay, mesh discovery, STUN NAT traversal, TLS 1.3,
BirdSong beacons, `--beardog-socket` flag alignment.
**Request**: `SecurityRpcClient` pattern for direct BearDog calls should be
the standard pattern for all TCP federation scenarios.

### ToadStool (Compute) — Display Phase 2
**What's working**: BTSP relay, JSON-RPC on UDS, tarpc dual-protocol,
compute dispatch, `graphics.*` node methods.
**Request**: `display.create_node` / `graphics.node.create` for rich graphics
pipeline (textures, shaders, animated nodes). Phase 2 spec in handoff.

### barraCuda (Tensor/GPU) — v0.3.12 Sprint 45
**What's working**: BTSP relay, 50 JSON-RPC methods, stats/ML/spectral/activation.
**Request**: `stats.entropy` method (Shannon/Rényi). Currently missing despite
being in the method registry.

### coralReef (Shader Compiler) — Phase D
**What's working**: BTSP relay, mixed command pipeline, WGSL compilation.
**Request**: Phase D command alignment (mixed command format vs pure JSON-RPC).
LOW priority — functional as-is.

### NestGate (Storage) — v4.70 Session 46
**What's working**: BTSP relay (family_seed base64 fix, BufReader fix),
streaming storage, deep debt eliminated, 8,822 tests, 84%+ coverage.
**Request**: Large-payload streaming guard for HTTP transport.

### Squirrel (AI) — v0.1.0
**What's working**: BTSP relay, MCP tools, inference provider bridge,
provider registration hardening, orphan cleanup.
**Request**: Agentic composition patterns for model-as-player scenarios.
`inference.complete` reliability across provider chains.

### rhizoCrypt (DAG) — Latest
**What's working**: BTSP authenticated, UDS responds to health checks.
**CRITICAL GAP (PG-06)**: `dag.session.create` returns empty response on UDS.
Compositions degrade gracefully but lose DAG functionality.
**Request**: Fix the session creation response format for UDS transport.

### loamSpine (Ledger) — Latest
**What's working**: BTSP authenticated, spine create/append/seal cycle,
linear entry chains, reliable on UDS.
**No blocking gaps**.

### sweetGrass (Provenance) — Latest
**What's working**: BTSP authenticated, braid creation and recording,
PROV-O document attachment to state transitions.
**No blocking gaps**.

### petalTongue (Visualization/UI) — v1.6.6+
**What's working**: Scene graph rendering, Grammar of Graphics, AnimationPlayer,
`motor.set_panel`, `visualization.scene.push`, `interaction.subscribe`,
`sensor_stream.poll`, proprioception snapshots.
**GAPS**:
- PG-40: winit requires main thread for live GUI mode (workaround exists)
- PG-48: plasmidBin binary winit threading (must launch with `composition_nucleus.sh`)
- `xdotool` synthetic events don't propagate through egui/winit (real input works)
- `visualization.texture.attach` is a placeholder (no real texture-to-node binding)
- UV sub-rect selection not implemented

### biomeOS (Orchestration) — v3.27
**What's working**: Neural API, graph executor, `graph.list`, `capability.call`,
socket resolution, `topology.rescan`, cellular deployment.
**GAPS**:
- Graph schema divergence (`[[graph.nodes]]` vs `[[nodes]]`)
- `tick_status` event relay design incomplete
- BTSP Phase 3 deferred (phase readiness fields added)

---

## For Spring Teams — Composition Patterns

### How Springs Consume NUCLEUS

1. **Pull primalSpring** and `infra/wateringHole`
2. **Copy tools**: `nucleus_composition_lib.sh`, `composition_template.sh`, `composition_nucleus.sh`
3. **Start NUCLEUS**: `COMPOSITION_NAME=myspring ./tools/composition_nucleus.sh start`
4. **Run your composition**: Source the lib, implement domain hooks
5. **Document gaps**: Anything unexpected goes into your `PRIMAL_GAPS.md` and flows back upstream

### Per-Spring Exploration Lanes

| Spring | Primary Focus | Key Primals | Unique Contribution |
|--------|--------------|-------------|---------------------|
| **ludoSpring** | Interaction fidelity — mouse/keyboard/touch events, playstyle metrics, game loops | petalTongue, rhizoCrypt, loamSpine | Tightest feedback loop for UI evolution |
| **hotSpring** | Async computation — DAG memoization for physics, non-blocking tensor ops | barraCuda, toadStool, rhizoCrypt | Precision compute + cache patterns |
| **wetSpring** | Data visualization — genome browsers, phylogenetics, data streams | petalTongue, sweetGrass, nestGate | Scientific visualization patterns |
| **neuralSpring** | Agentic composition — Squirrel-driven UI, model-as-player | Squirrel, petalTongue, toadStool | AI-in-the-loop composition |
| **healthSpring** | Enclave composition — ionic bond isolation, clinical AI | NestGate, Squirrel, BearDog | Security boundary patterns |
| **airSpring** | Environmental sensing — real-time ingestion pipelines | fieldMouse, NestGate, toadStool | Edge/sensor patterns |
| **groundSpring** | Geospatial — multi-resolution terrain, geology | barraCuda, NestGate, sweetGrass | Large-data tiling patterns |

### What Springs Hand Back

- Discovered primal gaps (format: entry in your `PRIMAL_GAPS.md`)
- Domain-specific interaction patterns (what worked, what didn't)
- Timing/polling optimizations for your domain
- New capability requirements (methods you needed that don't exist)
- Validated composition patterns (your working cell graphs)

---

## Deployment via Neural API from biomeOS

### Current Deployment Path
```
plasmidBin binaries → composition_nucleus.sh → primals on UDS
  → domain script sources nucleus_composition_lib.sh → live composition
```

### Target Deployment Path (biomeOS cellular)
```
cell_graph.toml → biomeOS deploy → Neural API → primals auto-discovered
  → garden/spring consumes capabilities via capability.call
```

### What Needs to Converge
1. **Graph schema alignment**: primalSpring `[[graph.nodes]]` ↔ biomeOS `[[nodes]]`
2. **Tick event relay**: `graph.tick_status` for continuous compositions
3. **BTSP Phase 3**: Post-handshake encrypted channels (ChaCha20-Poly1305)
4. **rhizoCrypt UDS**: PG-06 fix for DAG session creation

---

## Archive and Fossil Record

### Archived This Session (April 27, 2026)
- 7 handoffs moved to `handoffs/archive/` (BTSP convergence, Phase 45c, ludoSpring V53 absorption)
- primalSpring `fossilRecord/` contains 3 archived sets (inference module, pre-tower-atomic, stale graphs)
- Zero stale TODOs/FIXMEs in primalSpring Rust source
- Zero temp/backup/merge-conflict files

### Documentation Updates
- `README.md`: architecture tree updated with composition tools, graph count 67
- `CONTEXT.md`: Phase 46, graph count 67, shell composition library section
- `whitePaper/baseCamp/README.md`: Phase 46 composition template section
- `infra/wateringHole/README.md`: updated date, handoff counts, interactive composition section
- `infra/wateringHole/handoffs/`: this handoff + Phase 46 composition template handoff

---

**The ecosystem is at composition-ready state. Springs can deploy NUCLEUS from
plasmidBin, explore interactive compositions via the shell library, and surface
gaps that drive the next upstream evolution cycle.**

**License**: AGPL-3.0-or-later
