# ludoSpring V53 — Upstream Evolution Handoff

**Date:** April 25, 2026
**From:** ludoSpring V53 (springs/ludoSpring)
**For:** All primal teams, spring teams, biomeOS, primalSpring

---

## Executive Summary

ludoSpring has completed the 3-tier validation ladder: **Python baselines → Rust port
(spring binary) → Primal composition (NUCLEUS graph)**. The spring binary is no longer
in plasmidBin — game science is served by composing 11 existing primals via a 12-node
NUCLEUS cell graph. 817 workspace tests validate the Rust tier. 10 of 12 primals
confirmed live (2 blocked by known upstream gaps).

This handoff documents: composition patterns validated, primal evolution gaps found,
NUCLEUS deployment lessons, and recommendations for all teams.

---

## Part 1: Composition Patterns Validated

### 1.1 Pure Primal Composition (No Spring Binary)

Springs produce primals and define compositions — they are NOT primals.
The `ludospring` binary was removed from `plasmidBin` (V53). The
`plasmidBin/ludospring/metadata.toml` is now a `[composition]` manifest with:

- `cell_graph = "ludospring_cell.toml"` (12 nodes)
- `[compatibility.capability_routing]` — maps game science to primal providers
- `[composition.primals]` — 11 primal dependency list
- `[composition.validation]` — spring binary as tier-2 validation only

**Pattern for all springs:** No spring binary belongs in plasmidBin. Define a
composition manifest instead.

### 1.2 Capability Routing

Game science capabilities map to actual primal providers:

| Capability Domain | Primal | Role | Required |
|------------------|--------|------|----------|
| `math.*`, `activation.*`, `stats.*`, `noise.*`, `rng.*`, `tensor.*` | barraCuda | Science compute | no (skip) |
| `visualization.*`, `interaction.*` | petalTongue | UI/rendering | yes |
| `ai.*`, `inference.*` | Squirrel | AI narration | no (skip) |
| `compute.*` | ToadStool | GPU dispatch | no (skip) |
| `shader.*` | coralReef | Shader compilation | no (skip) |
| `crypto.*` | BearDog | Security | yes |
| `discovery.*` | Songbird | Service discovery | yes |
| `storage.*` | NestGate | Persistence | no (skip) |
| `dag.*` | rhizoCrypt | Provenance DAG | no (skip) |
| `certificate.*` | loamSpine | Certificates | no (skip) |
| `attribution.*` | sweetGrass | Attribution braids | no (skip) |

### 1.3 Graceful Degradation (`is_skip_error`)

The `IpcError::is_skip_error()` pattern (from primalSpring v0.9.17) enables
composition to function when optional primals are offline. Validated live:
barraCuda, petalTongue, Squirrel all respond to health probes; missing primals
(rhizoCrypt UDS, loamSpine) degrade gracefully.

### 1.4 Composite RPC (`game.tick`)

A single RPC call orchestrates: scene push → interaction poll → action record
→ metrics compute. This validates the pattern of a spring defining composite
operations that decompose across multiple primals at runtime.

### 1.5 `ipc::methods` Constants

All hardcoded RPC method strings replaced with typed constants:
`methods::visualization::RENDER_SCENE`, `methods::interaction::POLL`, etc.
Eliminates typo-driven routing failures.

---

## Part 2: Live NUCLEUS Deployment Findings

### 2.1 Primal Status (10/12 live)

| Primal | Transport | Status | Notes |
|--------|-----------|--------|-------|
| BearDog | UDS + TCP:9900 | LIVE | Requires `NODE_ID` env var |
| Songbird | UDS + TCP:8080 | LIVE | Requires `SECURITY_PROVIDER=beardog` |
| barraCuda | UDS (`--unix`) | LIVE | RTX 4060 GPU detected; `--unix` not `--socket` |
| coralReef | UDS + TCP | LIVE | Shader compilation healthy |
| ToadStool | UDS | LIVE | `toadstool.health` (not `health.check`) |
| rhizoCrypt | TCP:9401 only | LIVE | **GAP-06**: no UDS transport |
| loamSpine | — | DOWN | **GAP-07**: runtime nesting panic |
| sweetGrass | UDS | LIVE | Attribution available |
| NestGate | HTTP:9300 | LIVE | Requires `JWT_SECRET`, explicit port to avoid 8080 conflict |
| Squirrel | Abstract socket | LIVE | `@squirrel` abstract socket (not filesystem) |
| petalTongue (IPC) | UDS | LIVE | `server` mode for headless IPC |
| petalTongue (Web) | HTTP:3000 | LIVE | `web` mode for browser UI |

### 2.2 Startup Quirks Discovered

| Issue | Primal | Resolution |
|-------|--------|------------|
| `NODE_ID` required | BearDog | Set `NODE_ID=tower1 BEARDOG_NODE_ID=tower1` |
| `SECURITY_PROVIDER` required | Songbird | Set `SONGBIRD_SECURITY_PROVIDER=beardog` + socket paths |
| `--socket` not recognized | barraCuda | Use `--unix` flag instead |
| Port 8080 conflict | NestGate vs Songbird | NestGate on explicit `--port 9300` |
| Insecure JWT default | NestGate | Set `NESTGATE_JWT_SECRET=$(openssl rand -base64 48)` |
| winit thread panic | petalTongue `ui` mode | Use `web` mode for non-native contexts |
| Abstract socket | Squirrel | Probe via `\0squirrel` path; `ss -lx` to discover |
| Non-standard health method | ToadStool | `toadstool.health` not `health.check` |

### 2.3 Game Science Verified via Composition

Capabilities previously in the monolithic `ludospring` binary now served by
barraCuda as a composed primal:

```
activation.fitts(256, 32)  → {index_of_difficulty: 3.17, movement_time: 0.49}
stats.mean([0.85, ...])    → {result: 0.868}
noise.perlin2d(1.5, 2.3)  → {result: 0.196}
math.sigmoid([0, 0.5, 1]) → {result: [0.5, 0.622, 0.731]}
```

---

## Part 3: Gap Status for Upstream Teams

### 3.1 Critical Gaps (blocking full composition)

| GAP | Owner | Impact | Recommendation |
|-----|-------|--------|----------------|
| GAP-06 | **rhizoCrypt** | No UDS transport — blocks 4 experiments, forces TCP-only | Add UDS listener alongside TCP |
| GAP-07 | **loamSpine** | Startup panic (runtime nesting) — blocks certificate ops | Fix tokio runtime nesting or switch to single-runtime |

### 3.2 Documented Gaps (workarounds in place)

| GAP | Owner | Status |
|-----|-------|--------|
| GAP-01 | coralReef | IPC client not exercised in product paths |
| GAP-02 | barraCuda | Direct Rust import used alongside IPC (tier 2 validation) |
| GAP-04 | barraCuda | TensorSession not exercised in product paths |
| GAP-05 | primalSpring | Trio not in proto-nucleate graph |
| GAP-08 | barraCuda | Formula mismatch — documented via GAP-11 dual-value approach |
| GAP-09 | primalSpring | `nest_atomic` fragment aspirational until GAP-06/07 resolve |
| GAP-11 | barraCuda | Fitts/Hick/variance formulation divergence — dual-value tests |

### 3.3 Resolved

| GAP | Resolution |
|-----|-----------|
| GAP-03 | V42 — `nest_atomic` added to fragment metadata |
| GAP-10 | V53 — pure composition model (no spring binary in graph) |

---

## Part 4: Recommendations by Team

### primalSpring
- Drop `guidestone_binary = "ludospring"` from `downstream_manifest.toml` — use composition-only validation
- Update `graphs/cells/ludospring_cell.toml` to drop any `ludospring` node
- Consider making the "spring = composition, not primal" pattern explicit in standards docs
- GAP-05 and GAP-09 remain upstream blockers for trio integration

### biomeOS
- `ludospring_game` composition in `manifest.lock` is the deployment unit (no binary to fetch)
- `fetch.sh` should naturally skip entries with no binary artifact
- Neural API capability registration (GAP in exp087/088) still outstanding

### barraCuda
- Game science routes through your capabilities — absorption opportunities:
  - `activation.fitts`, `activation.hick` for flow/DDA evaluation
  - `noise.perlin2d` for procedural generation
  - `stats.mean`/`stats.std_dev`/`stats.variance` for engagement metrics
- GAP-11 (formulation divergence) documented — dual-value tests as interim
- `--unix` flag (not `--socket`) for UDS startup — document in README

### petalTongue
- `web` mode confirmed working for browser-based UI composition
- `ui` mode has winit thread-safety issue in non-main-thread contexts
- `server` mode works for headless IPC composition

### Squirrel
- Abstract socket discovery works (`\0squirrel` or `@squirrel`)
- 23 AI capabilities confirmed via `capability.list`
- Document abstract socket usage for consuming springs

### BearDog + Songbird
- Both require explicit env vars (`NODE_ID`, `SECURITY_PROVIDER`) — document as mandatory startup params
- Tower Atomic is solid and validated

### NestGate
- Needs explicit port config to avoid conflict with Songbird (both default to 8080)
- `JWT_SECRET` must be set (no insecure default) — document in README

### rhizoCrypt (GAP-06)
- UDS transport is the highest-priority gap for composition — TCP:9401 works but breaks the UDS-only model

### loamSpine (GAP-07)
- Runtime nesting panic is the second critical gap — blocks certificate operations in composition

### All Springs
- **3-tier validation ladder:** Python baselines → Rust port → Primal composition
- Spring binary = validation target. Composition manifest = deployment surface.
- No spring binary in plasmidBin. Define `[composition]` in `metadata.toml`.
- Use `is_skip_error()` for graceful degradation when composing optional primals.
- Use `ipc::methods::*` constants instead of hardcoded method strings.

---

## Part 5: NUCLEUS Composition Patterns for Deployment

### Cell Graph Structure (`ludospring_cell.toml`)

12-node sequential graph with BTSP security on every node:

```
Tower: BearDog → Songbird
Node:  barraCuda → coralReef → ToadStool  (parallel)
Nest:  NestGate → rhizoCrypt → loamSpine → sweetGrass
AI:    Squirrel
Viz:   petalTongue
Cell:  validate_cell (health checks on all required primals)
```

### Neural API Deployment (via biomeOS)

The cell graph is the contract biomeOS uses to deploy the composition.
No `ludospring` process runs — capabilities are addressed by name and
routed to the appropriate primal at runtime.

### Continuous Composition (`game_loop_continuous.toml`)

60Hz game tick loop as a composition of pure primal calls:
push_scene → poll_interaction → evaluate_flow → record_action → tick_health

---

## Files Changed (V53)

| File | Change |
|------|--------|
| `plasmidBin/ludospring/ludospring` | DELETED (binary artifact) |
| `plasmidBin/ludospring/metadata.toml` | Transformed to `[composition]` manifest |
| `plasmidBin/ludospring/ludospring_cell.toml` | NEW — cell graph for biomeOS |
| `plasmidBin/manifest.lock` | `[springs.ludospring]` → `[compositions.ludospring_game]` |
| `graphs/ludospring_cell.toml` | 14→12 nodes, ludospring node removed |
| `graphs/ludospring_gaming_niche.toml` | `germinate_ludospring` → `germinate_barracuda` |
| `niches/ludospring-game.yaml` | v2.0.0, 11 composed primals |
| `docs/PRIMAL_GAPS.md` | GAP-10 RESOLVED |
| All root docs | V53, composition model |
| `infra/wateringHole/PRIMAL_REGISTRY.md` | V53, 817 tests, composition deployment |
| `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` | V53, 817 tests, 12-node cell graph |

---

## Validation

- **817** workspace tests (Rust tier validation)
- **100** experiments across 22+ tracks
- **10/12** primals confirmed live in full NUCLEUS
- **guideStone readiness 4** (three-tier: bare + IPC + NUCLEUS)
- **Zero** clippy warnings (pedantic + nursery)
- **Zero** unsafe code
- **Zero** TODO/FIXME in application code
