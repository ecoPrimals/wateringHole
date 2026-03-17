# petalTongue v1.6.3 — Primal Interaction Wiring Handoff

**Date**: March 15, 2026
**Version**: 1.6.3
**Primal**: petalTongue (Universal Representation)
**Session**: Primal interaction wiring, provenance trio, compute bridge, niche standard

---

## Session Summary

Wired petalTongue into the broader ecoPrimals ecosystem with full primal interaction
support. Expanded capability registration from 7 to 35 announced capabilities. Created
provenance trio client for rhizoCrypt + sweetGrass + loamSpine session lineage. Evolved
the physics bridge into a general compute bridge supporting math.stat, math.tessellate,
and math.project operation families for barraCuda offload. Completed niche YAML with
organisms, interactions, and customization sections for BYOB deployment.

---

## Key Changes

### Capability Registration (primal_registration.rs)

Expanded `PrimalRegistration::petaltongue()` capabilities from 7 to 35:

| Domain | Capabilities |
|--------|-------------|
| UI | ui.render, ui.visualization, ui.graph, ui.terminal, ui.audio |
| Visualization | visualization.render, .render.stream, .render.grammar, .render.dashboard, .interact, .interact.subscribe, .provenance, .export, .validate |
| Graph | graph.topology, graph.builder |
| Interaction | interaction.subscribe, interaction.poll |
| Sensor | sensor.stream.subscribe |
| Motor | motor.set_panel, motor.set_zoom, motor.set_mode |
| Modality | modality.visual, .audio, .terminal, .haptic, .braille, .description |
| System | health.check, capability.list |

### Provenance Trio Client (provenance_trio.rs — NEW)

Capability-based discovery of the provenance trio:

- **Ephemeral DAG** (`dag.session`): Creates visualization session vertices
- **Attribution** (`braid.create`): Records data source contributions
- **Permanent Ledger** (`spine.create`): Archives exported visualizations

All primals discovered by capability, not name. Graceful degradation when unavailable.

### Compute Bridge Expansion (physics_bridge.rs)

Evolved from physics-only to general compute bridge:

| Operation Family | Methods |
|------------------|---------|
| Physics | math.physics.nbody (existing) |
| Statistics | math.stat.kde, math.stat.smooth, math.stat.bin, math.stat.summary |
| Tessellation | math.tessellate.sphere, math.tessellate.cylinder, math.tessellate.isosurface |
| Projection | math.project.perspective, math.project.lighting |

All operations fall back gracefully when barraCuda is unavailable.

### Niche YAML (niche.yaml)

Added spring-as-niche standard sections:

- **Organisms**: 8 primals (petaltongue required, beardog/songbird required, 5 optional)
- **Interactions**: 8 interaction definitions (security, discovery, compute, provenance)
- **Customization**: 4 BYOB options (mode, provenance, GPU, modalities)
- **Inbound**: Wildcard `* → petaltongue` for spring data push

---

## Spring Data Integration Status

| Spring | Push Path | Channel Types | Status |
|--------|-----------|---------------|--------|
| neuralSpring | visualization.render + stream | All 9 (TimeSeries through Spectrum) | Ready |
| wetSpring | visualization.render + stream | 9 types inc. Spectrum | Ready |
| healthSpring | visualization.render | PK/PD, biosignal, clinical | Ready |
| airSpring | visualization.render | ET0, water balance, biodiversity | Ready |
| groundSpring | visualization.render | Measurement uncertainty, spectral | Ready |
| hotSpring | visualization.render | MD trajectories, energy curves | Ready |

---

## Verification State

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --all-targets --all-features -- -D warnings` | Zero warnings |
| `cargo test --all --all-features` | 5,188 passed, 0 failed |
| Files over 1000 lines | None |

---

## Remaining Work

1. **Coverage**: 85% → 90% target
2. **Live integration testing**: End-to-end with running springs
3. **Capability registry**: Register in biomeOS `capability_registry.toml`
4. **Display backend**: toadStool display backend wiring
5. **Cross-compilation**: armv7, macOS, Windows, WASM
6. **Fuzz testing**: `cargo-fuzz` harness

---

## wateringHole Compliance

| Standard | Status |
|----------|--------|
| PRIMAL_IPC_PROTOCOL | Compliant — 35 capabilities registered via ipc.register |
| SPRING_AS_NICHE_DEPLOYMENT_STANDARD | Compliant — full niche.yaml with organisms/interactions |
| SEMANTIC_METHOD_NAMING | 40+ methods, domain.operation[.variant] |
| GATE_DEPLOYMENT_STANDARD | Compliant — UniBin, ecoBin, AGPL-3.0 |
| SOVEREIGN_COMPUTE_EVOLUTION | Compute bridge wired for barraCuda offload |
