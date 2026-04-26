# The Ecosystem Evolution Cycle

**Date**: April 22, 2026
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

**Current state (April 2026)**: Delta season — **guideStone Level 4 achieved** for
primalSpring. Live NUCLEUS deployed from plasmidBin as binary depot. Stadial parity
gate cleared across all 13 primals + primalSpring. Springs evolving to self-validating
NUCLEUS deployments via the plasmidBin depot pattern:
- **Stadial gate cleared**: BearDog W56, Songbird W165, NestGate 43w, ToadStool S203t, petalTongue v1.6.7, sweetGrass stadial — zero async-trait, zero finite dyn, Edition 2024
- **primalSpring v0.9.17**: guideStone Level 4 (**187/187 live NUCLEUS ALL PASS — 13/13 BTSP authenticated, 8 cellular graphs BTSP-enforced**, 41/41 bare, BLAKE3 P3, seed provenance Layer 0.5, BTSP escalation Layer 1.5, cellular deployment Layer 7, biomeOS v3.25 absorbed), fragment-first graphs, 631 tests, plasmidBin depot documented, deep debt evolution (capability-based discovery, zero hardcoded primal names, all files under 800 LOC)
- **guideStone pattern**: Self-validating NUCLEUS composition (5 properties: deterministic, traceable, self-verifying, env-agnostic, tolerance-documented). Proven by hotSpring-guideStone-v0.7.0. primalSpring guideStone now validates base composition for all downstream. Standard at `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` v1.1.0.
- **plasmidBin genomeBin depot**: Full cross-architecture binary depot (46 binaries, 6 target triples, Tier 1 39/39). `build_ecosystem_genomeBin.sh` replaces musl-only script with 9-target matrix (Tier 1 MUST / Tier 2 SHOULD / Tier 3 NICE per ecoBin Architecture Standard). All upstream armv7/nestgate gaps closed Phase 45. Springs pull, deploy NUCLEUS, validate externally. See `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md`.
- **Active delta springs**: hotSpring v0.6.32 (guideStone Level 5 — certified), healthSpring V54 (guideStone Level 2), neuralSpring V134 (guideStone Level 2), wetSpring V147 (guideStone Level 3 — bare works)
- **primalSpring guideStone**: `primalspring_guidestone` binary — 9-layer base composition certification (including seed provenance L0.5, BTSP escalation L1.5, cellular deployment L7). **187/187 ALL PASS** against live 12-primal NUCLEUS (**13/13 BTSP authenticated**, 8 cellular graphs BTSP-enforced). Base layer that domain guideStones inherit.
- **Pre-composition springs**: airSpring v0.10.0, groundSpring V124
- **Composing springs**: ludoSpring V49 (guideStone readiness 4 — deep debt resolved: capability-based discovery, MCP 15/15, typed IpcError, base64 dep removed, 799 tests, genomeBin v5.1)

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

**Current priority**: Response schemas are standardized (Sprint 42+). Springs
need to rewire from library deps to IPC calls against your ecobin primal.
Ensure your JSON-RPC surface is discoverable and your capability strings
match the downstream manifest.

### If You're primalSpring

You are the spring — literally. You receive capability meltwater from primals
and validate it forms correct compositions. You provide the validated patterns
that downstream springs absorb.

**Your job**: Start and validate NUCLEUS compositions (Tower, Node, Nest,
FullNucleus). Surface upstream gaps. Provide the `composition` validation
library so springs can test parity.

**Current priority**: Guide spring IPC rewiring. Primals are ready (all 12 ALIVE,
32 barraCuda methods, UDS everywhere). Springs need to drop library deps from
primal binaries and call ecobin primals over IPC for the primal proof.

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

**Current state**: esotericWebb V7 demonstrates the pattern. 342 tests, ~91%
coverage, 7 primal domains consumed via PrimalBridge, all degrading gracefully.
Deploy graphs compose from NUCLEUS fragments (`tower_atomic`, `node_atomic`,
`nest_atomic`, `meta_tier`). Game science absorbed locally — no spring runtime
dependencies. Neural API fallback provides transparent AI evolution.

**Current priority**: Exercise composition end-to-end as springs confirm
composition parity. File capability gaps back through wateringHole handoffs.
See `ESOTERICWEBB_V7_COMPOSITION_PATTERNS_HANDOFF_APR17_2026.md` for the
per-primal gap matrix and composition patterns.

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

### primalSpring (Phase 43+ — stadial cleared)

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
| toadStool | 203+ | Standardize `compute.dispatch` result shape | **RESOLVED** (S203 — `specs/DISPATCH_WIRE_CONTRACT.md`, canonical envelope) |
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
| **RESOLVED** | Songbird | 0 `#[async_trait]`, 0 finite `dyn`, 0 production mocks, 0 bare `#[allow]`, 0 blanket lint suppress, 0 hardcoded IPs/ports, 0 unused deps, 0 `Box<dyn Error>` in production. W164: BTSP relay silent-fail fix. W165: `serde_yaml` → `serde_yaml_ng`, `hostname` consolidated to `gethostname` (5 crates), `futures` → `futures-util`, 7 zero-caller deprecated items removed, hardcoded bind addresses eliminated. W166: root doc reconciliation. W167: error frames + env fallbacks. W168: routing + seed encoding. W169: remaining `new()` → `new_direct()` in `bin_interface/server.rs` (IPC + TCP paths). W170: CLI flag alignment (`--security-socket` canonical, `--beardog-socket` alias). Zero `::new()` in production — 7,387 lib tests, 0 failures |
| **RESOLVED** | ToadStool | RPITIT + enum dispatch (S203s), all 11 DEBT.md items resolved (S203t), edge compilation fixed + smart refactoring (S173), edge clippy clean 231→0 (S174), 7,818 lib tests |
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
| **hotSpring** v0.6.32 | **guideStone Level 5 CERTIFIED** (v1.2.0) | 64/64 suites; all 5 guideStone properties; `hotspring_guidestone` (BLAKE3 P3, protocol tolerance, family discovery via primalSpring v0.9.17); 13 LOCAL_CAPABILITIES dispatched; genomeBin v5.1 absorbed; `validate-primal-proof.sh` auto-sets NUCLEUS env vars |
| **healthSpring** V53 | **Delta** — Level 5 in progress (guideStone readiness: Level 1) | exp122 IPC parity; `math_dispatch.rs` feature-gated IPC/lib routing; niche.rs; dual-tower ionic |
| **neuralSpring** V133 | **Delta** — Level 5 primal proof | `IpcMathClient` (9 methods); `validate_proto_nucleate_capabilities` (7 caps, exit 0/1/2); `deny.toml` stadial bans; 18 barraCuda surface gaps handed back |
| **wetSpring** V145 | **Delta** — Level 5 primal proof | Exp403 `validate_primal_parity_v1` (5 primals over IPC); 22 CONSUMED_CAPABILITIES in niche.rs |
| **airSpring** v0.10.0 | **Pre-delta** | 90.56% coverage; no NUCLEUS wiring yet |
| **groundSpring** V124 | **Pre-delta** | 92% coverage; no NUCLEUS wiring yet |
| **ludoSpring** V49 | **Delta** — deep debt resolved, idiomatic Rust evolution | Handler tests extracted (mod.rs 818→169L), capability-based discovery, MCP 15/15, base64 dep removed (inline encoder), typed IpcError in btsp.rs, named constants; 799 tests; zero clippy; cell graph ready |

**Common ecosystem blockers** across active delta springs:
- Ionic bond negotiation (BearDog `crypto.sign_contract`) — hotSpring, healthSpring, wetSpring
- BTSP Phase 3 server (encrypted channel) — hotSpring, healthSpring
- ~~toadStool `compute.dispatch` standardization~~ **RESOLVED** S203 — hotSpring, wetSpring, neuralSpring
- Squirrel provider registration — neuralSpring, healthSpring, wetSpring
- NestGate `storage.fetch_external` for cross-spring — wetSpring, healthSpring
- barraCuda IPC rewiring — **spring-side gap** (barraCuda ecobin already exposes 32 JSON-RPC methods; springs must drop library dep and call over IPC) — all delta springs

See `NUCLEUS_SPRING_ALIGNMENT.md` and `primalSpring/wateringHole/GRAPH_CONSOLIDATION_AND_NUCLEUS_DEPLOYMENT_HANDOFF_APR16_2026.md`.

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
