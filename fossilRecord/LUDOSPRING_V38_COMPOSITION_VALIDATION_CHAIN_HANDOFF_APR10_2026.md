<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation: CC-BY-SA-4.0
-->

# ludoSpring V38 — Composition Validation Chain Handoff

**Date:** April 10, 2026
**From:** ludoSpring
**To:** All primal teams, primalSpring, esotericWebb
**Scope:** Three-layer validation chain, ecoBin harvest, composition patterns for NUCLEUS deployment

---

## Executive Summary

ludoSpring V38 completes the three-layer validation chain that proves science
methods produce identical results from Python through Rust through IPC composition:

```
Python baseline → Rust library  → IPC composition  → NUCLEUS deployment
(Layer 1: done)   (Layer 2: NEW)  (Layer 3: experiments)
```

The ecoBin has been harvested to `infra/plasmidBin/` (v0.8.0, 3.1M PIE binary,
30 capabilities, sha256-verified). 7 composition parity tests prove Rust library
== IPC within ANALYTICAL_TOL (1e-10). 745 tests pass. 99 experiments.

---

## What Changed (V37.1 → V38)

### New Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| Rust composition targets | `baselines/rust/composition_targets.json` | Golden reference from direct Rust library calls |
| Target generator | `baselines/rust/generate_composition_targets.rs` | Cargo example producing JSON targets |
| 7 composition parity tests | `barracuda/tests/ipc_integration.rs` | Prove IpcServer responses == library calls |
| exp099 experiment | `experiments/exp099_composition_validation/` | 13-check standalone composition validator |
| coralReef IPC client | `barracuda/src/ipc/coralreef.rs` | Typed client for shader compilation via NeuralBridge |
| Condition mapping module | `barracuda/src/game/rpgpt/condition_map.rs` | Extracted from transition.rs for RPGPT plane transitions |
| Primal gaps doc | `docs/PRIMAL_GAPS.md` | 8 gaps (GAP-01 to GAP-08) with owners and severity |
| batch_raycast handler | `barracuda/src/ipc/handlers/gpu.rs` | `game.gpu.batch_raycast` DDA batch line-of-sight |

### ecoBin Deployment

| Field | Value |
|-------|-------|
| Binary | `infra/plasmidBin/ludospring/ludospring` |
| Version | 0.8.0 |
| Size | 3.1M |
| Format | ELF 64-bit PIE x86-64 |
| Checksum | `sha256:2f2ca987a7b57c10fe679b18f1b293b3d9c667cea3c35afe20897e5821472784` |
| Capabilities | 30 (8 science + 5 GPU + 11 delegation + 3 health + 2 MCP + 1 capability) |
| Port | 9650 (TCP), UDS preferred |

---

## Composition Patterns for NUCLEUS Deployment

### Pattern 1: Science Method Parity (validated in V38)

Any ludoSpring science method can be called either:
- **Direct library**: `ludospring_barracuda::interaction::flow::evaluate_flow(0.5, 0.5, width)`
- **IPC**: `{"method": "game.evaluate_flow", "params": {"challenge": 0.5, "skill": 0.5}}`

Both return identical `FlowResult { state, flow_score, in_flow }` within 1e-10.

**Methods validated**: `game.evaluate_flow`, `game.fitts_cost`, `game.engagement`,
`game.generate_noise`, `game.difficulty_adjustment`, `game.accessibility`,
`game.wfc_step`, `game.analyze_ui`

### Pattern 2: GPU Delegation via toadStool

`game.gpu.*` methods route to toadStool's `compute.dispatch.submit` via NeuralBridge.
CPU fallback engages automatically when toadStool is unavailable.

```
ludoSpring → NeuralBridge → toadStool compute.dispatch.submit
                          ↳ (fallback) CPU compute in-process
```

### Pattern 3: Provenance Trio Integration

Session lifecycle methods compose three primals:
- `game.begin_session` → rhizoCrypt `dag.session.create`
- `game.record_action` → rhizoCrypt `dag.vertex.append`
- `game.complete_session` → rhizoCrypt + BearDog `crypto.sign` + NestGate `storage.store`
- `game.mint_certificate` → loamSpine `certificate.mint`

### Pattern 4: AI Delegation via Squirrel

NPC dialogue, narration, and voice checks route to Squirrel:
- `game.npc_dialogue` → Squirrel `ai.query` (constrained by ruleset cert)
- `game.voice_check` → Squirrel `ai.query` (with temperature parameter)
- `game.narrate_action` → Squirrel `ai.complete`

### Pattern 5: Visualization via petalTongue

Scene pushing and dashboard rendering route to petalTongue:
- `game.push_scene` → petalTongue `visualization.render.scene`
- Dashboard subcommands → petalTongue `visualization.render.dashboard`

---

## Actions for Primal Teams

### barraCuda Team

| Priority | Action | Impact |
|----------|--------|--------|
| HIGH | Fix Fitts formula: use Shannon `log2(2D/W+1)` not `log2(D/W)` | +4 composition checks (exp089) |
| HIGH | Fix Hick formula: use `log2(n)` not `log2(n+1)` | +4 composition checks (exp089) |
| MEDIUM | Fix Perlin3D lattice invariant: `perlin3d(0,0,0)` must return 0 | +1 check (exp091) |
| LOW | Consider `math.flow.evaluate` / `math.engagement.composite` domain methods | exp084 domain routing |

### rhizoCrypt Team

| Priority | Action | Impact |
|----------|--------|--------|
| **CRITICAL** | Add Unix domain socket transport (`--unix` / XDG_RUNTIME_DIR) | Unblocks exp094, 095, 096, 098 (+9 checks) |

### loamSpine Team

| Priority | Action | Impact |
|----------|--------|--------|
| **CRITICAL** | Fix `block_on` inside async runtime panic in `infant_discovery.rs:233` | Unblocks exp095 (+6 checks) |

### biomeOS Team

| Priority | Action | Impact |
|----------|--------|--------|
| HIGH | Auto-register running primals with Neural API capability registry | Unblocks exp087, 088 (+14 checks) |

### toadStool + coralReef Teams

| Priority | Action | Impact |
|----------|--------|--------|
| MEDIUM | Fix inter-primal discovery (toadStool can't find coralReef despite socket existing) | +1 check (exp085) |

---

## Actions for primalSpring

1. **Update `ludospring_validate.toml`** — still V32-era; needs V38 capabilities and graph structure
2. **Add composition validation graph** — `science_validation.toml` tests the IPC parity chain
3. **Verify proto-nucleate graph alignment** — `ludospring_proto_nucleate.toml` nodes match V38 capabilities (30, was 27)

---

## Actions for esotericWebb

1. **Absorb composition patterns** — the 7 composition parity tests demonstrate exactly how to call each science method via IPC; Webb's `LudoSpringClient` should match these call shapes
2. **Use `baselines/rust/composition_targets.json`** as golden reference for Webb's own ludoSpring integration tests
3. **GPU delegation pattern** — `game.gpu.*` → toadStool with CPU fallback is the pattern Webb should use for any compute-heavy operation

---

## Remaining Gap Matrix (from docs/PRIMAL_GAPS.md)

| GAP | Primal | Status | Severity | Impact |
|-----|--------|--------|----------|--------|
| GAP-01 | coralReef | IPC client wired, not exercised | MEDIUM | Shader compilation not live |
| GAP-02 | barraCuda | Direct Rust import (not IPC) | LOW | By design for math lib |
| GAP-03 | nest_atomic | Fragment metadata incomplete | LOW | Proto-nucleate graph accuracy |
| GAP-04 | TensorSession | Not exercised in product paths | LOW | GPU pipeline maturity |
| GAP-05 | Provenance trio | Not in proto-nucleate | MEDIUM | Graph completeness |
| GAP-06 | rhizoCrypt | TCP-only (no UDS) | CRITICAL | Blocks 4 experiments |
| GAP-07 | loamSpine | Startup panic | CRITICAL | Blocks 1 experiment |
| GAP-08 | barraCuda | Fitts/Hick formula mismatch | HIGH | 4 checks failing |

**Current score**: 95/141 (67.4%) + exp099 13/13 = **108/154 composition checks passing (70.1%)**

**Projected with all fixes**: ~143/154 (92.9%)

---

## Test Summary

| Suite | Count | Status |
|-------|-------|--------|
| barracuda lib | 696 | PASS |
| barracuda ipc integration | 23 | PASS |
| metalForge/forge | 26 | PASS |
| **Total** | **745** | **PASS** |
| Python baseline drift | 0 | Clean |
| Experiments | 99 | All compile; composition exps require live primals |

---

## How to Verify

```bash
cd springs/ludoSpring

# Layer 1: Python → Rust
python3 baselines/python/check_drift.py

# Layer 2: Rust → IPC (automated tests, no live server needed)
cargo test -p ludospring-barracuda --features ipc --test ipc_integration composition_

# Layer 2: Generate fresh Rust targets
cargo run --example generate_composition_targets -p ludospring-barracuda 2>/dev/null | diff - baselines/rust/composition_targets.json

# Layer 3: Full composition validation (requires live ludospring server)
cargo run --features ipc --bin ludospring -- server &
cargo run -p ludospring-exp099

# ecoBin verification
sha256sum infra/plasmidBin/ludospring/ludospring
# Expected: 2f2ca987a7b57c10fe679b18f1b293b3d9c667cea3c35afe20897e5821472784
```
