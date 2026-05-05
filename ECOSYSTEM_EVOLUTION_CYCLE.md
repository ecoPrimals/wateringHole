# The Ecosystem Evolution Cycle

**Date**: May 5, 2026
**Version**: v1.4.0
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

**Current state (May 2026)**: Delta season with convergence phase — **guideStone Level 4 achieved** for
primalSpring. Live NUCLEUS deployed from plasmidBin as binary depot. Stadial parity
gate cleared across all 13 primals + primalSpring. projectNUCLEUS absorbed by primalSpring.
**Library-to-binary rewiring** is now the primary delta season task — springs evolving from
library imports to binary-only IPC calls against ecobin primals. Springs evolving to self-validating
NUCLEUS deployments via the plasmidBin depot pattern:
- **Stadial gate cleared**: BearDog W56, Songbird W188, NestGate 43w, ToadStool S203t, petalTongue v1.6.7, sweetGrass stadial — zero async-trait, zero finite dyn, Edition 2024
- **primalSpring v0.9.21 Phase 55b**: guideStone Level 4 (**187/187 live NUCLEUS ALL PASS — 13/13 BTSP authenticated, 8 cellular graphs BTSP-enforced**, 41/41 bare, BLAKE3 P3, seed provenance Layer 0.5, BTSP escalation Layer 1.5, cellular deployment Layer 7, biomeOS v3.36 absorbed (+ v3.36: BTSP Phase 3 `btsp.negotiate` ChaCha20-Poly1305 + NULL fallback, 14 stale EVOLVED comments purged), NestGate v0.4.70 S48 absorbed (native encrypt-at-rest + auth bypass), Squirrel AN absorbed (HTTP providers + DISCOVERY_SOCKET + crypto foundation), Songbird W178 absorbed (anyhow migration)), fragment-first graphs, 631 tests, two-tier crypto architecture, plasmidBin depot. **Upstream gaps narrowed**: NestGate encrypt-at-rest RESOLVED, Squirrel discovery RESOLVED. Remaining: BearDog purpose-key RPC, rhizoCrypt/sweetGrass Tower delegation, loamSpine BTSP activation
- **guideStone pattern**: Self-validating NUCLEUS composition (5 properties: deterministic, traceable, self-verifying, env-agnostic, tolerance-documented). Proven by hotSpring-guideStone-v0.7.0. primalSpring guideStone now validates base composition for all downstream. Standard at `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` v1.1.0.
- **plasmidBin genomeBin depot**: Full cross-architecture binary depot (46 binaries, 6 target triples, Tier 1 39/39). `build_ecosystem_genomeBin.sh` replaces musl-only script with 9-target matrix (Tier 1 MUST / Tier 2 SHOULD / Tier 3 NICE per ecoBin Architecture Standard). All upstream armv7/nestgate gaps closed Phase 45. Springs pull, deploy NUCLEUS, validate externally. See `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md`.
- **Active delta springs**: hotSpring v0.6.32 (guideStone Level 5 — certified), healthSpring V59 (guideStone Level 5), neuralSpring V138 (guideStone Level 3), wetSpring V151 (guideStone Level 4+)
- **primalSpring guideStone**: `primalspring_guidestone` binary — 9-layer base composition certification (including seed provenance L0.5, BTSP escalation L1.5, cellular deployment L7). **187/187 ALL PASS** against live 12-primal NUCLEUS (**13/13 BTSP authenticated**, 8 cellular graphs BTSP-enforced). Base layer that domain guideStones inherit.
- **Pre-composition springs**: airSpring v0.10.0, groundSpring V124
- **Composing springs**: ludoSpring V53 (pure composition — no spring binary deploys, 12-node cell graph, 30 capabilities, BTSP-enforced, 60Hz tick, 817 tests)

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
| **RESOLVED** | Songbird | 0 `#[async_trait]`, 0 finite `dyn`, 0 production mocks, 0 bare `#[allow]`, 0 blanket lint suppress, 0 hardcoded IPs/ports, 0 unused deps, 0 `Box<dyn Error>` anywhere (production + test-utils), 0 files >800L, 0 unsafe. W188: timeout centralization wave 2 (15 new constants, 10+ literals replaced across TLS/IPC/discovery/relay), JSONRPC_VERSION consolidation (20 allocations eliminated), `Box<dyn Error>` fully eliminated from test-utils (6 files evolved to `anyhow::Result`). W187: smart refactor (`connection.rs` 1043→694L via `#[path]` test extraction), 15 "BearDog" error strings evolved to "security provider", 4 new timeout constants. W186: BTSP Phase 3 live connection verification (4 tests). W185: deep debt (11 timeout constants, JSON-RPC constructors). W184: BTSP Phase 3 dispatch fix. W183: deep debt (lint evolution, 8 timeout constants). W182: BTSP Phase 3 spec alignment. W181: port canonicalization. W180: BTSP Phase 3 `btsp.negotiate`. W179: coverage +92 tests. W178: deep debt (anyhow). W177: signed IPC. W176: smart refactor. Zero `::new()` in production — 7,803 lib tests, 0 failures |
| **RESOLVED** | ToadStool | RPITIT + enum dispatch (S203s), all 11 DEBT.md items resolved (S203t), edge compilation fixed + smart refactoring (S173), edge clippy clean 231→0 (S174), 7,818 lib tests |
| **RESOLVED** | NestGate | ring eliminated, deprecated markers 114→0 (43w), S48: native encrypt-at-rest (ChaCha20-Poly1305), `NESTGATE_AUTH_MODE=beardog` JWT bypass, emoji purge (178 markers), 8,840 tests |
| **RESOLVED** | petalTongue | reqwest+ring+rustls eliminated (v1.6.6), LocalHttpClient via hyper, UUI boundary cleanup, BTSP Phase 2 operational, `cargo deny check bans` clean, `async-trait` banned, 6,191+ tests |
| **RESOLVED** | sweetGrass | 6 traits → RPITIT, sled eliminated, async-trait removed from direct deps |
| **RESOLVED** | biomeOS | RPITIT (`PrimalOperationExecutor`), async-trait removed from types/api production (v3.07) |
| **RESOLVED** | Squirrel | 0 `#[async_trait]` (64 removed), 0 C deps, 0 unsafe, 0 lying stubs, 0 TODO/FIXME, `#[expect(reason)]` policy, HTTP provider support, `DISCOVERY_SOCKET` resolution, crypto foundation (purpose-key RPC surface). 7,182 tests, 90.1% coverage |
| **CLEAN** | barraCuda, coralReef, loamSpine, rhizoCrypt | Already modern or minimal debt |

**Resolution**: native `async fn` in traits (rustc 1.75+), enum dispatch where
trait objects have finite implementors, `thiserror`/`anyhow` instead of
`Box<dyn Error>`, `#[expect]` instead of `#[allow]`.

See `primalSpring/docs/PRIMAL_GAPS.md` § "Class 4: Pre-Modern Async Rust"
for the full per-primal matrix.

### Downstream Springs — Composition Status

Five springs are in active delta composition. Two are pre-delta:

| Spring | Status | Rewiring Tier | Composition Evidence |
|--------|--------|---------------|---------------------|
| **hotSpring** v0.6.32 | **gS 5 CERTIFIED** | Tier 2 | 993 tests; `composition.rs` dual-lane, `primal_bridge.rs`, `PRIMAL_PROOF_IPC_MAPPING.md`; bulk physics still library-linked |
| **healthSpring** V59 | **gS 5** | Tier 3 | 948 tests; `primal-proof` feature flag, full `src/ipc/`, dual-tower ionic |
| **neuralSpring** V138 | **gS 3** | Tier 2 | 1,234 tests; `ipc_dispatch.rs` only, no `src/ipc/` dir |
| **wetSpring** V151 | **gS 4+** | Tier 2 | 1,594 tests; full `src/ipc/` + 15 handlers, provenance wiring; bulk math library-linked |
| **ludoSpring** V53 | **gS 4** | Tier 3 | 820 tests; pure composition, per-trio-primal IPC modules, 13 deploy graphs |
| **airSpring** v0.10.0 | **Pre-delta** | Tier 2 | 1,364 tests; full `src/ipc/` + `src/rpc/`; no guideStone |
| **groundSpring** V124 | **Pre-delta** | Tier 1 | 1,020 tests; optional barraCuda feature; minimal IPC |

### Library-to-Binary Rewiring (Phase 58 — Primary Delta Task)

The central evolution task for all delta springs: replace library imports of
barraCuda with binary-only IPC calls to ecobin-deployed primals. barraCuda
ecobin already exposes 32+ JSON-RPC methods — springs must rewire to use them.

During earlier evolution, springs were the laboratories where primal math was
developed. hotSpring built precision mixing and df64, wetSpring evolved spectral
analysis, ludoSpring proved game math under tick-budget constraints. Primals
absorbed this work. The spring-local `barracuda/` and `ecoPrimal/` directories
are artifacts of that process. `metalForge/` is distinct — it is the hardware
abstraction layer (GPU/CPU/NPU) informing toadStool and stays spring-local.

**Rewiring tiers**:
- **Tier 1**: Minimal IPC; barraCuda optional or library-only
- **Tier 2**: IPC routing exists; bulk science still links library
- **Tier 3**: IPC parity validation active; library and IPC lanes side-by-side
- **Tier 4**: Library dep dropped; all compute through IPC (target)

**Rewiring priority** (from `SPRING_NUCLEUS_AUDIT_MAY2026.md`):
1. ludoSpring (3→4) — pure composition, cleanest test case
2. healthSpring (3→4) — `primal-proof` feature already gates compilation
3. hotSpring (2→3) — biggest barraCuda contributor validating absorption
4. wetSpring (2→3) — rich IPC handlers, route compute through ecobin
5. airSpring (2→3) — good IPC foundation despite pre-delta
6. neuralSpring (2→3) — needs `src/ipc/` dir; latency-sensitive
7. groundSpring (1→2) — expand `ipc.rs` into `src/ipc/` tree

**Cross-spring standardization patterns** (see `NUCLEUS_SPRING_ALIGNMENT.md` Phase 58):
- Per-trio-primal IPC modules (from ludoSpring)
- `primal-proof` Cargo feature flag (from healthSpring)
- `composition.rs` dual-lane validation (from hotSpring)
- `PRIMAL_PROOF_IPC_MAPPING.md` per spring (from hotSpring)
- Deploy graph per science pipeline (from ludoSpring)

### petalTongue and sweetGrass Subtasks

Alongside rewiring, two subtasks drive convergence:

**petalTongue visualization**: Every spring's science output maps to existing
DataBinding channel types (`timeseries`, `heatmap`, `spectrum`, `scatter`,
`gauge`, `bar`, `fieldmap`, `scatter3d`, `distribution`, `game_scene`,
`soundscape`). When springs rewire to IPC, the JSON-RPC result payloads become
direct DataBinding inputs — the computation presents itself. healthSpring is
the reference exemplar. See `PETALTONGUE_SPRING_SCIENCE_MAP.md`.

**sweetGrass braiding**: Each spring's experiments should produce attribution
braids linking agents, activities, and entities into W3C PROV-O documents.
ludoSpring is the reference implementation with per-trio-primal modules.
See `SWEETGRASS_SPRING_BRAID_PATTERNS.md`.

**Common blockers** across delta springs:
- Ionic bond negotiation (BearDog `crypto.sign_contract`) — hotSpring, healthSpring, wetSpring
- ~~BTSP Phase 3 server (encrypted channel)~~ **RESOLVED** — 13/13 primals FULL AEAD (May 2, 2026)
- ~~toadStool `compute.dispatch` standardization~~ **RESOLVED** S203
- Squirrel provider registration — neuralSpring, healthSpring, wetSpring
- NestGate `storage.fetch_external` for cross-spring — wetSpring, healthSpring
- ~~barraCuda IPC rewiring~~ **ACTIVE** — primary delta task (Phase 58+)

See `NUCLEUS_SPRING_ALIGNMENT.md`, `SPRING_NUCLEUS_AUDIT_MAY2026.md`.

---

---

## Convergent Evolution Evidence (April 27, 2026)

The seven springs' independent evolution produced convergent discoveries —
patterns that emerged in multiple springs without coordination. This is
strong evidence that the constrained evolution model (no shared crates,
capability-based discovery, AGPL) is producing genuine fitness, not
accidental similarity.

### Confirmed Convergences

| Pattern | Discovered By | Ecosystem Impact |
|---------|---------------|-----------------|
| UDS transport portability (socat → python3 → nc) | hotSpring, wetSpring, healthSpring, neuralSpring | `nucleus_composition_lib.sh` PG-49 RESOLVED |
| Missing default primals (nestgate, squirrel) | healthSpring, neuralSpring | `composition_nucleus.sh` PG-50 fix |
| Temporal heterogeneity (tick vs convergence vs seasonal) | ludoSpring, hotSpring, airSpring | `COMPOSITION_TICK_MODEL_STANDARD.md` |
| Cross-spring validation patterns | healthSpring, neuralSpring | `CROSS_SPRING_COORDINATION_STANDARD.md` |
| Deploy graph schema divergence | ludoSpring, primalSpring | biomeOS dual-format ingestion |

### What This Proves

The constrained evolution model produces compound returns:

1. **Independent discovery validates patterns** — when two springs independently
   evolve the same solution, the solution is correct for the ecosystem, not just
   one domain.

2. **Constraints drive convergence** — no shared crates forces each spring to
   solve IPC independently, but the JSON-RPC + UDS + capability model ensures
   they converge on composable solutions.

3. **The water cycle works** — gaps discovered in springs (delta season) evaporate
   up to primalSpring (spring season), which absorbs them into shared patterns
   that flow back down. Each cycle is faster than the last.

### Current Season Assessment

**Delta season — convergence phase.** Five springs are actively composing
(hotSpring, wetSpring, neuralSpring, healthSpring, ludoSpring). airSpring and
groundSpring are pre-delta with high coverage and ready to unpause.

The primary delta task is **library-to-binary rewiring** — replacing spring-local
barraCuda library imports with IPC calls to ecobin primals. This is not just
a technical cleanup; it is the structural transformation that makes every spring's
science composable, visualizable (via petalTongue), and attributable (via
sweetGrass). When a spring rewires to IPC:
- Its compute results are JSON-serialized → directly streamable to petalTongue
- Its computation is routed through ecobin primals → provenance-trackable
- Its science is expressed as NUCLEUS compositions → reproducible by anyone

The ecosystem is approaching the **garden season** — when enough primal
compositions are proven that gen4 products can be built purely from IPC
composition without spring-level validation. The `GARDEN_COMPOSITION_ONRAMP.md`
standard is the bridge. esotericWebb (ludoSpring's garden) is the first
consumer.

### Convergence Trajectory

```
Phase 58 (now):    Springs audit rewiring status
                   Standardization patterns identified
                   (ludoSpring IPC, healthSpring feature flag,
                    hotSpring composition model)

Phase 59 (next):   ludoSpring + healthSpring reach Tier 4
                   hotSpring + wetSpring reach Tier 3
                   petalTongue DataBindings wired for top 4 springs
                   sweetGrass braids operational for ludoSpring

Phase 60 (after):  All active springs at Tier 3+
                   airSpring + groundSpring begin delta absorption
                   Cross-spring provenance braids in production
                   Science papers expressed as NUCLEUS composition graphs

Garden season:     Springs reach Tier 4
                   Every paper has a NUCLEUS composition
                   Every result has a provenance braid
                   Every output is a petalTongue presentation
                   Gardens compose from proven binary-only IPC
```

---

## Future Trajectory

### Near Term (Weeks)

- ~~PG-52 provenance trio UDS empty response~~ **RESOLVED** (April 27)
- ~~PG-48 petalTongue musl threading~~ **ADDRESSED** (April 27)
- ~~BTSP Phase 3 full AEAD~~ **RESOLVED** — 13/13 primals (May 2)
- ludoSpring + healthSpring advance to Tier 4 (binary-only)
- hotSpring creates `src/ipc/` directory, expands Tier 3 coverage
- petalTongue DataBinding wiring for healthSpring (exemplar), ludoSpring, wetSpring
- sweetGrass braid adoption in ludoSpring (reference for siblings)

### Short Term (Months)

- All active springs at Tier 3+ rewiring status
- airSpring and groundSpring begin delta absorption
- `esotericWebb` ships as first garden product from composition
- Cross-spring provenance braids in production
- Each spring has a `PRIMAL_PROOF_IPC_MAPPING.md` for its domain
- biomeOS adaptive tick scheduling (PathwayLearner observing frame budgets)
- guideStone certification propagation: hotSpring L5 → all springs L4+
- ABG collaboration workflows expressed as NUCLEUS compositions

### Medium Term (Quarters)

- All springs at Tier 4 (binary-only IPC, no library deps)
- guideStone artifacts for all springs (deployable, self-validating binaries)
- Every baseCamp paper has a corresponding NUCLEUS composition graph
- Gonzales drug repurposing pipeline operational (wetSpring → ADDRC screening)
- Faculty network densification (Chuna lattice QCD, Gonzales pharmacology)
- biomeOS cellular deployment as standard for all compositions
- metalForge → toadStool dispatch contract refined across all springs

### Longer Term (Years)

- biomeOS evolves into sovereign OS substrate
- Citizen Colossus: federated consumer compute via sunCloud economics
- Novel Ferment Transcripts as economic primitives
- Mobility edge crossed: isolated sovereign nodes begin to conduct
- Every computation is its own presentation (petalTongue universal surface)
- Every result is its own reproducibility proof (sweetGrass universal braiding)

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
