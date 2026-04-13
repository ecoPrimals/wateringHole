# The Ecosystem Evolution Cycle

**Date**: April 12, 2026
**Version**: v1.0.0
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

**Current state (April 2026)**: Mountain season. Primals are closing debt:
- barraCuda Sprint 41: BC-07/BC-08 resolved, 3-tier GPU fallback wired
- coralReef Iter 80: wire contract, CompilationInfo IPC, hot-path alloc eliminated, 4,477 tests
- NestGate Session 42: ring eliminated, storage IPC stable
- BearDog Wave 35: real Ed25519 ionic bonds, deep debt clean
- biomeOS v3.03: capability.resolve, inference routing, anyhow migration

primalSpring is tightening: inference module archived, stale graphs removed,
composition validation library built. Ready for composition elevation.

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
| coralReef | 80+ | Standardize `shader.compile` response format | **OPEN** |
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
| **HEAVY** | toadStool, Songbird, BearDog, Squirrel | 100+ `#[async_trait]` each, heavy `dyn` dispatch |
| **MEDIUM** | biomeOS, NestGate, petalTongue | Partial migration or `Box<dyn Error>` dominant |
| **LOW/CLEAN** | barraCuda, coralReef, loamSpine, rhizoCrypt | Already modern or minimal debt |

**Resolution**: native `async fn` in traits (rustc 1.75+), enum dispatch where
trait objects have finite implementors, `thiserror`/`anyhow` instead of
`Box<dyn Error>`, `#[expect]` instead of `#[allow]`.

See `primalSpring/docs/PRIMAL_GAPS.md` § "Class 4: Pre-Modern Async Rust"
for the full per-primal matrix.

### Downstream Springs (waiting for composition elevation)

All springs are at "composing" stage. They need primalSpring to prove
composition parity before they can elevate from Rust math to primal
composition. See `NUCLEUS_SPRING_ALIGNMENT.md` for the per-spring matrix.

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
