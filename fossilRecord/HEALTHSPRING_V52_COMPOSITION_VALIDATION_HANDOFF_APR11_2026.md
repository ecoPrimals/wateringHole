<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V52 — Composition Validation (Cross-Ecosystem Handoff)

**Date**: 2026-04-11
**From**: healthSpring V52 (ecoBin 0.8.0, `infra/plasmidBin/healthspring/`)
**To**: All primals, all springs, biomeOS, primalSpring, neuralSpring
**Previous**: V51 Hardened Composition Patterns

---

## Summary

healthSpring V52 completes the shift from **Rust-validates-Python** to
**NUCLEUS-validates-composition**. Three-layer validation is now live:

1. Python validates science (Tier 0 baselines, peer-reviewed DOI citations)
2. Rust validates Python (Tier 1 CPU parity, Tier 2 GPU parity)
3. NUCLEUS validates composition (Tier 4 IPC dispatch parity, Tier 5 deploy graph alignment)

985+ tests, 90 experiments (84 science + 7 composition Tier 4/5), zero clippy
warnings (pedantic+nursery), zero unsafe. barraCuda v0.3.11.

---

## Patterns Proven (available for ecosystem adoption)

### 1. Tier 5 Deploy Graph Validation

exp118 (`exp118_composition_deploy_graph_validation`, 99 checks) structurally
validates the deploy graph TOML against proto-nucleate expectations:

- Fragment metadata accuracy (`tower_atomic`, `nest_atomic`, `meta_tier` booleans)
- Required/optional node presence (beardog, songbird, healthspring, nestgate, etc.)
- Bonding policy (ionic bonds at trust boundaries, `dual_tower_enclave` trust model)
- Capability surface coverage (all 58+ science + 14+ infra capabilities registered)
- Squirrel optional node (`required = false`, `by_capability = "inference"`)
- Primal identity constants match deploy graph node names

**Adoption path**: Every spring with a deploy graph can write an equivalent Tier 5
experiment. healthSpring's exp118 pattern is reusable — parse TOML, assert fragment
metadata, walk nodes, verify bonding, check capabilities. The ValidationHarness
handles pass/fail/exit codes.

### 2. Typed IPC Clients with Resilient Default

`PrimalClient.call()` uses `resilient_send` (retry + exponential backoff) by default.
`try_call()` available for single-attempt paths. `handle_primal_forward` in server
routing migrated from raw RPC to typed client.

**Adoption path**: Any primal forwarding requests to other primals should use typed
clients with resilient defaults. Single-attempt for health probes, resilient for
science dispatch.

### 3. Three-Layer Validation Ladder

```
Tier 0: Python control     → peer-reviewed science (DOI-cited baselines)
Tier 1: Rust CPU            → faithful port (f64-canonical, tolerance-documented)
Tier 2: GPU parity          → barraCuda WGSL (CPU vs GPU bit-identical)
Tier 3: metalForge dispatch → NUCLEUS routing (cross-substrate, PCIe P2P)
Tier 4: Primal composition  → IPC dispatch parity (JSON-RPC wire = direct Rust)
Tier 5: Deploy graph        → TOML graph ↔ proto-nucleate structural alignment
```

At Tier 4+5, Python and Rust both become validation **targets** for composition.
The science stays fixed — we validate that NUCLEUS composition patterns faithfully
preserve it through IPC dispatch and that deploy graph metadata is internally
consistent with proto-nucleate declarations.

### 4. GPU CI on Every PR

`barracuda-ops` feature tests run on every PR (not just weekly). Full GPU features
on weekly schedule. This catches barraCuda API drift early without requiring GPU
hardware on every PR runner.

**Adoption path**: Any spring using barraCuda should add `--features barracuda-ops`
to PR CI and reserve `--features gpu` for scheduled runs.

---

## Composition Patterns for NUCLEUS Deployment

healthSpring demonstrates a complete composition flow suitable for biomeOS Neural
API deployment:

### Deploy Graph Structure (`healthspring_niche_deploy.toml`)

```toml
[graph]
name = "healthspring_niche_deploy"
type = "deployment"
fragments = "node_atomic"     # NUCLEUS atomic level
particle_profile = "niche"    # Niche = composed set of primals
proto_nucleate = "healthspring_enclave_proto_nucleate"

[graph.nodes.healthspring]
binary = "healthspring_primal"
capabilities = ["science.pkpd.*", "science.microbiome.*", ...]  # 58+ methods
depends_on = ["beardog", "songbird"]
```

### Fragment Metadata Pattern

Deploy graphs must accurately declare which NUCLEUS atomics are present:
- `tower_atomic`: true if BearDog + Songbird are in the graph (trust boundary)
- `node_atomic`: true if toadStool + barraCuda + coralReef are present (compute)
- `nest_atomic`: true if NestGate + rhizoCrypt + loamSpine + sweetGrass (storage)
- `meta_tier`: true if biomeOS/Squirrel/petalTongue (orchestration/AI/UI)
- `nucleus`: true only if all three atomics are present (full NUCLEUS)

### Bonding Policy at Atomic Boundaries

Cross-atomic compositions declare:
- Bond type: `ionic` (at tower↔node, tower↔nest boundaries)
- Trust model: `dual_tower_enclave` (BearDog enforces both sides)
- Encryption tier per boundary

### Optional Nodes (Squirrel Pattern)

Primals that enhance but aren't required are declared `required = false` with
`by_capability = "inference"`. biomeOS discovers them at runtime; springs gain
capabilities (e.g., `inference.complete`) without code changes when providers
appear on the socket bus.

---

## Remaining Primal Gaps (from healthSpring perspective)

| # | Gap | Status | Blocker |
|---|-----|--------|---------|
| 2 | Ionic bridge enforcement | Blocked | BearDog `crypto.ionic_bond` / `crypto.verify_family` |
| 4 | Inference canonical namespace | Partial | primalSpring/Squirrel alignment (`inference.*` vs `model.*` vs `ai.*`) |
| 10 | BTSP server endpoint | Client ready | BearDog BTSP server implementation |

Gaps #11 (Typed IPC Clients) and #12 (Deploy Graph Validation) resolved in V52.

---

## For Each Team

| Team | Action |
|------|--------|
| **primalSpring** | (1) Validate `healthspring_enclave_proto_nucleate.toml` trust_model alignment (`btsp_enforced` vs `dual_tower_enclave`). (2) Consider harvesting exp118 pattern as ecosystem-wide `composition_validate` crate. (3) Update deployment_matrix.toml for healthSpring V52 Tier 5 validation cell. |
| **biomeOS** | healthSpring deploy graph validated via exp118; ready for Neural API graph execution. Capability surface documented. TCP+UDS transport active. Domain symlink `health.sock` available. |
| **barraCuda** | `TensorSession` still blocks local shader removal (Write→Absorb→Lean cycle paused). `SovereignDevice` API confirmed stable. `barracuda-ops` feature tests passing on every PR. |
| **coralReef** | Sovereign dispatch feature flag ready; `SovereignDevice` wired. Awaiting device availability for end-to-end. |
| **neuralSpring / Squirrel** | Squirrel optional node in deploy graph (`required = false`). `inference.*` capabilities auto-discovered. Canonical namespace coordination still needed (Gap #4). |
| **BearDog** | BTSP client handshake module ready (pure Rust, zero deps). Ionic bond runtime needed for deploy graph bonding policy enforcement. |
| **All springs** | Adopt Tier 5 pattern for deploy graph validation. Adopt typed IPC clients with resilient default. Add `barracuda-ops` to PR CI. Use three-layer validation narrative in handoffs. |

---

## Validation Evidence

```
cargo clippy --workspace -- -D warnings -W clippy::pedantic -W clippy::nursery  → 0 warnings
cargo fmt --check --all                                                         → pass
cargo test --workspace                                                          → 985+ tests, 0 failures
exp118_composition_deploy_graph_validation                                      → 99/99 PASS
```
