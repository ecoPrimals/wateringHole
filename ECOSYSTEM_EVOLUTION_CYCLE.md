# The Ecosystem Evolution Cycle

**Date**: April 17, 2026
**Version**: v1.1.0
**License**: AGPL-3.0-or-later

---

## The Water Cycle

The ecoPrimals ecosystem evolves like a water cycle. Understanding the
cycle helps every team know where they sit, what season they're in, and
why the work upstream or downstream matters to them.

```
                    ☁  EVAPORATION  ☁
                Springs hand patterns back up
              gaps discovered → primalSpring → primals
                         ↑
                         |
    ☀ SUNSHINE          |            🌧 RAIN
    Springs solve       |        Primals release new
    domain science      |        capabilities downstream
    (Python → Rust)     |              |
         ↑              |              ↓
         |          🏔 MOUNTAINS (primals)
         |          barraCuda, coralReef, toadStool,
         |          BearDog, Songbird, NestGate, ...
         |              |
         |              | meltwater: capabilities exposed via IPC
         |              ↓
         |          🌊 primalSpring (the spring)
         |          validates compositions, proves parity,
         |          surfaces gaps, provides validation library
         |              |
         |              | validated patterns flow downstream
         |              ↓
         |          🌿 DELTA (other springs)
         |          hotSpring, wetSpring, neuralSpring, ...
         |          each spring absorbs patterns, evolves domain
         |              |
         |              | domain discoveries evaporate back up
         └──────────────┘
```

## The Seasons

The ecosystem has natural seasons. Not calendar seasons — evolution seasons
driven by which altitude is actively evolving.

### Mountain Season (primals evolving)

Upstream primals absorb math, shaders, and IPC patterns from springs.
Downstream gets less "snow melt" — fewer new capabilities flowing down.
Springs focus on validation of what exists, surfacing gaps, tightening.

**Current state (April 2026)**: Spring → Delta transition. Stadial parity gate
cleared across all 13 primals + primalSpring. Four domain springs have entered
active NUCLEUS composition testing. The ecosystem is no longer in mountain
season — it has crossed into delta season for the leading springs:
- **Stadial gate cleared**: BearDog W56, Songbird W147, NestGate 43w, ToadStool S203t, petalTongue v1.6.7, sweetGrass stadial — zero async-trait, zero finite dyn, Edition 2024
- **primalSpring v0.9.15**: Graph consolidation (78→56 TOMLs), fragment-first composition, 570 tests
- **Active delta springs**: hotSpring v0.6.32 (62/62 suites), healthSpring V53 (exp119-121), neuralSpring V131 (science composition), wetSpring V144 (Exp401/402)
- **Pre-composition springs**: airSpring v0.10.0, groundSpring V124
- **Composing springs**: ludoSpring V43 (three-layer validation: Python→Rust→IPC golden chain)

Mountain season work continues for cross-primal protocols: ionic bond
negotiation, BTSP Phase 3, compute.dispatch standardization.

### Spring Season (composition elevation)

primalSpring demonstrates that NUCLEUS compositions produce correct results.
This is where "does 2+2=4 through primals?" gets proven. Springs can then
elevate from "Rust math" to "primal composition math."

**What triggers it**: Primals stabilize their IPC response schemas. primalSpring
can call `tensor.matmul` and get a consistent result format. Composition parity
tests go from SKIP (primal not running) to PASS (parity confirmed).

### Delta Season (springs composing)

Water reaches the delta. Each spring replaces its local Rust math with
primal composition calls. hotSpring QCD runs through barraCuda IPC.
wetSpring biology runs through NUCLEUS. Each spring validating composition
**is** the proof that primals work correctly for that domain.

**What triggers it**: primalSpring shows composition parity for the atomics.
Springs can trust that NUCLEUS compositions are correct and start delegating.

### Evaporation (patterns flow back up)

Springs discover domain-specific gaps as they compose. "barraCuda's
`tensor.matmul` doesn't handle sparse matrices" or "coralReef needs a
multi-stage compilation pipeline for ML shaders." These gaps evaporate
back up through primalSpring to the primal teams.

**The cycle repeats**: Primals absorb, capabilities improve, meltwater
flows, springs validate, gardens compose, gaps evaporate.

---

## How Each Layer Reads the Cycle

### If You're a Primal Team

You are the mountain. Your capabilities become the water supply for
everything downstream. When you stabilize a response schema or add a new
capability, that's snowpack that will melt when primalSpring validates it.

**Your job**: Close gaps from `PRIMAL_GAPS.md`, standardize your JSON-RPC
response schemas, and make your IPC surface composable. The faster you
stabilize, the faster springs can elevate to composition.

**Current priority**: Response schema standardization. Springs need consistent
result keys (`"result"` not varying across methods) so composition parity
extraction works without guessing.

### If You're primalSpring

You are the spring — literally. You receive capability meltwater from primals
and validate it forms correct compositions. You provide the validated patterns
that downstream springs absorb.

**Your job**: Start and validate NUCLEUS compositions (Tower, Node, Nest,
FullNucleus). Surface upstream gaps. Provide the `composition` validation
library so springs can test parity.

**Current priority**: Composition elevation — prove that NUCLEUS atomics
produce correct math results via IPC, move from SKIP to PASS.

### If You're a Domain Spring (hotSpring, wetSpring, etc.)

You are the delta. You receive validated composition patterns from
primalSpring and apply them to your domain science. Your Rust math code
evolved the primals during mountain season — now you validate that the
primals got it right by checking composition parity against your original
Python baselines.

**Your job**: Use `primalspring::composition::validate_parity()` to confirm
that primal compositions match your Python baselines. Document any gaps
(response schema mismatches, missing capabilities, tolerance surprises)
and hand them back to primalSpring.

**Current priority**: Adopt proto-nucleate graphs from
`primalSpring/graphs/downstream/`. Wire composition parity validation.

### If You're a Garden (esotericWebb, etc.)

You are the ocean — the final destination. Pure compositions of primals
via biomeOS, graph-as-product. You don't write math or validate science.
You compose proven capabilities into products.

**Your job**: Define your niche composition graph. biomeOS executes it.
Your validation is that the product works for users.

**Current priority**: Wait for delta season. When springs confirm
composition parity, gardens can trust the composition layer.

---

## The Acceleration Effect

Each pass through the cycle accelerates the next:

```
Cycle 1: hotSpring QCD (Python → Rust) → barraCuda shaders evolved
Cycle 2: primalSpring validates barraCuda composition → shaders proven
Cycle 3: neuralSpring gets ML shaders for free (same barraCuda)
Cycle 4: All springs get AI via Squirrel (neuralSpring inference)
Cycle 5: Gardens compose everything into products
```

A gap discovered by hotSpring in barraCuda's df64 handling benefits
neuralSpring's ML precision. A bonding model hardened by healthSpring's
compliance work protects every spring's data sovereignty. The atomics
are shared infrastructure — springs are domain laboratories that evolve it.

**The compound effect**: Each spring solving its domain makes every sibling
stronger. This is not parallel development — it's compound evolution.

---

## Current Composition Elevation Priorities

### primalSpring (Phase 34 target)

| Priority | What | Blocked By |
|----------|------|------------|
| 1 | Tower atomic composition parity (BearDog + Songbird via IPC) | Nothing — ready now |
| 2 | Node atomic composition parity (+ barraCuda + coralReef + toadStool) | ~~barraCuda tensor.* response schema standardization~~ RESOLVED (Sprint 42) |
| 3 | Nest atomic composition parity (+ NestGate + provenance trio) | Nothing — storage IPC stable |
| 4 | Full NUCLEUS composition parity | Depends on 1-3 |
| 5 | Chimera compositions via biomeOS | biomeOS graph execution maturity |

### Upstream Primals (composition enablement)

| Primal | Sprint | What Enables Composition | Status |
|--------|--------|------------------------|--------|
| barraCuda | 42+ | Standardize `tensor.*` response schema: `{"result": {"value": N}}` | **RESOLVED** (Sprint 42) |
| coralReef | 80 | Standardize `shader.compile` response format — `SHADER_COMPILE_WIRE_CONTRACT.md` | **RESOLVED** (Iter 80) |
| toadStool | 203+ | Standardize `compute.dispatch` result shape | **OPEN** |
| BearDog | 36+ | Already composable (crypto.sign, btsp.session — stable schemas) | **READY** |
| Songbird | 134+ | Already composable (discovery.*, capability.* — stable schemas) | **READY** |
| NestGate | 43+ | Already composable (storage.store, storage.retrieve — stable on UDS) | **READY** |
| biomeOS | 3.04+ | Graph execution correctness for multi-primal compositions | **PARTIAL** |

### Modernization Debt (parallel work while blockers resolve)

Pre-modern async Rust patterns (`async-trait` crate, `Box<dyn Error>`,
`Pin<Box<dyn Future>>`) add dependency weight, allocate on every async call,
and prevent the compiler from monomorphizing IPC-hot paths. These should be
resolved in parallel with composition schema work.

| Severity | Primals | Debt |
|----------|---------|------|
| **RESOLVED** | BearDog | 0 `#[async_trait]`, 0 `Box<dyn Error>` in production (W56), serde_yaml eliminated, 14,786+ tests |
| **RESOLVED** | Songbird | 0 `#[async_trait]`, 0 finite `dyn`, 0 production mocks, 0 bare `#[allow]` — Wave 147, 7,377 tests |
| **RESOLVED** | ToadStool | RPITIT + enum dispatch (S203s), all 11 DEBT.md items resolved (S203t), 7,784 tests |
| **RESOLVED** | NestGate | ring eliminated, deprecated markers 114→0 (43w), 8,695 tests |
| **RESOLVED** | petalTongue | reqwest+ring+rustls eliminated (v1.6.7), LocalHttpClient via hyper, UUI boundary cleanup |
| **RESOLVED** | sweetGrass | 6 traits → RPITIT, sled eliminated, async-trait removed from direct deps |
| **RESOLVED** | biomeOS | RPITIT (`PrimalOperationExecutor`), async-trait removed from types/api production (v3.07) |
| **WIP** | Squirrel | async-trait reduction ongoing; core AI routing operational |
| **CLEAN** | barraCuda, coralReef, loamSpine, rhizoCrypt | Already modern or minimal debt |

**Resolution**: native `async fn` in traits (rustc 1.75+), enum dispatch where
trait objects have finite implementors, `thiserror`/`anyhow` instead of
`Box<dyn Error>`, `#[expect]` instead of `#[allow]`.

See `primalSpring/docs/PRIMAL_GAPS.md` § "Class 4: Pre-Modern Async Rust"
for the full per-primal matrix.

### Downstream Springs — Composition Status

Four springs have entered active NUCLEUS composition testing:

| Spring | Status | Composition Evidence |
|--------|--------|---------------------|
| **hotSpring** v0.6.32 | **Delta** — Tier 3 NUCLEUS validators | 62/62 suites; 13 LOCAL_CAPABILITIES dispatched; IPC wiring with honest skip |
| **healthSpring** V53 | **Delta** — Live IPC parity | exp119 (parity), exp120 (provenance), exp121 (health); niche.rs; dual-tower ionic |
| **neuralSpring** V131 | **Delta** — Science composition | validate_science_composition (spectral, IPR, Hessian, disorder sweep); cross-team handoff |
| **wetSpring** V144 | **Delta** — Full tier validation | Exp401 (43/43), Exp402 (63/63); 18 IPC roundtrip tests; provenance registry |
| **airSpring** v0.10.0 | **Pre-delta** | 90.56% coverage; no NUCLEUS wiring yet |
| **groundSpring** V124 | **Pre-delta** | 92% coverage; no NUCLEUS wiring yet |
| **ludoSpring** V43 | **Delta** | Three-layer validation (Python→Rust→IPC); validate_composition binary; 790+ tests; plasmidBin v0.10.0 |

**Common ecosystem blockers** across active delta springs:
- Ionic bond negotiation (BearDog `crypto.sign_contract`) — hotSpring, healthSpring, wetSpring
- BTSP Phase 3 server (encrypted channel) — hotSpring, healthSpring
- toadStool `compute.dispatch` standardization — hotSpring, wetSpring, neuralSpring
- Squirrel provider registration — neuralSpring, healthSpring, wetSpring
- NestGate `storage.fetch_external` for cross-spring — wetSpring, healthSpring
- barraCuda IPC migration (path dep → capability IPC) — neuralSpring, all implicit

See `NUCLEUS_SPRING_ALIGNMENT.md` and `primalSpring/wateringHole/GRAPH_CONSOLIDATION_AND_NUCLEUS_DEPLOYMENT_HANDOFF_APR16_2026.md`.

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
