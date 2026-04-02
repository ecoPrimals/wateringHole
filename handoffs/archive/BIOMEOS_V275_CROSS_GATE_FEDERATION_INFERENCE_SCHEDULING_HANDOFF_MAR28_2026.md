# biomeOS v2.75 — Cross-Gate Federation Graphs + Inference Scheduling Handoff

**Date**: March 28, 2026
**Version**: v2.75 (builds on v2.74 deep debt evolution)
**Tests**: 7,202 passing (0 failures)
**Clippy**: 0 warnings (pedantic + nursery)

---

## Summary

Addresses the four primalSpring evolution targets: cross-gate deployment graphs,
model orchestration, and Pixel deployment readiness. All infrastructure is in place;
remaining work is operational (deploying binaries and validating end-to-end).

---

## Cross-Gate Deployment Graphs

### `graphs/cross_gate_tower.toml`

First real two-biomeOS federation graph. Deploys Tower Atomic (BearDog +
Songbird) on both Eastgate and gate2 (EPYC 9274F), then cross-registers
capabilities using `route.register`.

| Phase | Nodes | Gate |
|-------|-------|------|
| 1 | `local_beardog`, `local_songbird` | local (Eastgate) |
| 2 | `gate2_beardog`, `gate2_songbird` | gate2 (`tcp://192.0.2.132:9001`) |
| 3 | `register_gate2_crypto`, `register_gate2_network` | local (route.register) |
| 4 | `validate_federation`, `verify_cross_gate_crypto` | local (capability.call) |

Graph exercises: `gate` field on nodes → `forward_to_remote_gate()`,
`[graph.env]` → `GateRegistry::from_graph_env()`, `route.register` batch API.

### `graphs/cross_gate_pixel.toml`

ARM64 Pixel cross-gate graph. Assumes biomeOS already running on Pixel (9.6MB
musl binary deployed via ADB). Deploys Tower Atomic on Pixel from Eastgate,
then cross-registers.

| Phase | What |
|-------|------|
| 1 | Verify Eastgate Tower health |
| 2 | Deploy BearDog + Songbird on Pixel via `gate = "pixel"` |
| 3 | route.register Pixel crypto + network on Eastgate |
| 4 | Validate Pixel federation health |

## Inference Scheduling (Model Orchestration)

New `InferenceHandler` in `handlers/inference.rs`:

### `inference.schedule`

```json
{"method": "inference.schedule", "params": {
  "model": "llama-3-70b",
  "prompt": "Explain cross-gate federation",
  "gate": null
}}
```

When `gate` is null (or absent), the handler:
1. Probes all registered gates for `compute.capabilities`
2. Estimates VRAM requirement from model name (70b→40GB, 7b→6GB, API→0GB)
3. Selects the gate with sufficient VRAM and most headroom
4. Forwards `ai.query` via `capability.call` to the selected gate's Squirrel
5. Falls back to local if no remote gates qualify

### `inference.gates`

Lists all registered gates with GPU capabilities and availability status.

### VRAM Estimation

| Model pattern | VRAM estimate |
|--------------|---------------|
| `70b`, `65b` | 40 GB |
| `30b`, `34b` | 20 GB |
| `13b`, `14b` | 10 GB |
| `7b`, `8b` | 6 GB |
| `3b`, `1b` | 3 GB |
| `large` | 24 GB |
| `small`, `mini` | 4 GB |
| API models (gpt-4, claude) | 0 GB |

## Stale Reference Cleanup

| File | Change |
|------|--------|
| `nucleus.rs` | `docs/handoffs/` → `wateringHole/handoffs/` (2 comments) |
| `specs/EVOLUTION_ROADMAP.md` | Updated handoff directory path |
| `specs/MESH_IPC_METHODS_SPEC.md` | Updated related doc path |

CHANGELOG fossil `docs/handoffs/` references preserved as historical record.

## Files Changed

| File | Change |
|------|--------|
| `graphs/cross_gate_tower.toml` | New: 2-gate federation graph (200 lines) |
| `graphs/cross_gate_pixel.toml` | New: Pixel cross-gate graph (170 lines) |
| `crates/biomeos-atomic-deploy/src/handlers/inference.rs` | New: InferenceHandler (290 lines) |
| `crates/biomeos-atomic-deploy/src/handlers/mod.rs` | Added inference module |
| `crates/biomeos-atomic-deploy/src/neural_api_server/mod.rs` | Wired InferenceHandler |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` | `inference.schedule`, `inference.gates` routes |
| `crates/biomeos-atomic-deploy/src/gate_registry.rs` | Added `gate_names()` method |
| `crates/biomeos-atomic-deploy/src/neural_graph_tests.rs` | 3 new cross-gate graph tests |

## Test Delta

| Version | Tests | Delta |
|---------|-------|-------|
| v2.74 | 7,192 | — |
| v2.75 | 7,202 | +10 (3 cross-gate graph tests, 7 inference handler tests) |

## Remaining Operational Targets

1. **biomeOS on gate2** — Deploy binary, start biomeOS, run `cross_gate_tower.toml` end-to-end
2. **Pixel biomeOS** — `adb push` ARM64 binary, start biomeOS, run `cross_gate_pixel.toml`
3. **End-to-end inference scheduling** — With gate2 running, test `inference.schedule` with a real model routing to gate2's RTX 3090
