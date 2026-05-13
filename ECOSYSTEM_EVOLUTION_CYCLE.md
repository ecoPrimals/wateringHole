# The Ecosystem Evolution Cycle

**Date**: May 12, 2026
**Version**: v1.6.0 (Phase C complete, Tier 2 unblocked, ecosystem wave sync)
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

**Current state (May 12, 2026)**: Interstadial convergence — **Pillar 5 (river delta) MET**,
shadow run execution is the remaining gate. Phase 32 atomic model evolution complete.

**Phase 32 Atomic Model** (May 12):

| Atomic | Particle | Primals | Count |
|--------|----------|---------|------:|
| **Tower** | Electron | bearDog + songbird + skunkBat | 3 |
| **Node** | Proton | Tower + toadStool + barraCuda + coralReef | 6 |
| **Nest** | Neutron | Tower + nestGate + provenance trio | 7 |
| **NUCLEUS** | Atom | Tower + Node + Nest (deduplicated) + meta-tier | 10+3=13 |

- **13/13 primals at zero gate debt**: MethodGate, BTSP AEAD Phase 3, Edition 2024, deny.toml — all clean.
- **primalSpring v0.9.25**: guideStone **Level 8** (absorbed certification engine), 602 library tests, 77 deploy graphs, 413 registered methods (301 exercised, 72%), fragment-based composition v3.0.0.
- **Library-to-binary rewiring COMPLETE**: 8/8 springs at **Tier 4** (`default = []`, barraCuda optional). All springs now IPC-first for NUCLEUS deployments.
- **Active delta springs (May 12, all Tier 4 IPC-first)**:

| Spring | gS | Tests | Key Status |
|--------|---:|------:|------------|
| primalSpring | L8 | 602 | Coordinator — 413 methods, 77 graphs |
| hotSpring | L6 | 1,025 | LTEE B2, 3-GPU sovereign |
| healthSpring | L5 | 999 | Thread 3 seeded |
| neuralSpring | L5 | 1,453 | LTEE B1 Py+Rust done |
| wetSpring | L4 | 1,613 | LTEE B7 started, 4 PGs open |
| airSpring | L4 | 1,389 | barraCuda 0.3.13 |
| groundSpring | L4 | 1,125 | LTEE B2+B1 COMPLETE |
| ludoSpring | L4 | 854 | SPDX, composition-only |

- **Interstadial gate**: Pillar 5 met. Tier 2 UNBLOCKED. lithoSpore Module 1+2 integrating real data (Pillar 4 progressing). All 7 springs wiring Tier 2. Songbird VPS relay progressing (`songbird relay` CLI + TURN data plane). **coralReef diesel engine excised** (Sprint 9 — coral-ember/glowplug/driver/gpu deleted, pure compiler primal). Transition now requires **shadow run execution + lithoSpore PASS + Songbird relay ops deployment**. See `INTERSTADIAL_EXIT_CRITERIA.md` v1.4.
- **plasmidBin genomeBin depot**: 46 cross-architecture binaries, 6 targets, Tier 1 39/39.
- **guideStone pattern**: absorbed into UniBin as certification organelle (L8).

Mountain season accelerating: toadStool Phase C **COMPLETE** (S245-S250, 7 batches,
520 cylinder tests, 8,809 workspace), Phase D plumbing in, `toadstool.validate`
**IMPLEMENTED** (S250). `barracuda.precision.route` **IMPLEMENTED** (precision.rs
+ 649 tests). Songbird TURN server shipped (836 lines, VPS relay progressing).
coralReef diesel engine **excised** (Sprint 9 — 153K lines deleted, pure compiler primal). Remaining mountain work:
Songbird VPS relay completion, ionic bond runtime. toadStool Phase D cutover (barracuda rewires file-by-file).

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

### Sentinel Escalation Model

Primals are **sentinels** — the least composed entities, most directly exposed
to the glacial shift between interstadial and stadial. Like alpine species
that respond first to climate change, primals are the earliest to feel schema
pressure, IPC contract drift, and capability regressions.

The escalation rule follows from this:

1. **Downstream surfaces the gap** — springs and products discover composition
   failures (e.g. "toadStool returns unexpected shape for `compute.dispatch.submit`")
2. **Upstream owns the fix** — primal teams resolve at the source. The fix
   flows downhill as meltwater.
3. **primalSpring validates closure** — gate tests confirm the fix composes
   correctly across atomics.
4. **Escalation priority**: upstream issues are always higher priority than
   downstream. A primal regression cascades to all 8 springs; a spring gap
   affects only that spring. Sentinel sensitivity means primal fixes are
   treated as urgent even when the downstream impact appears small.

This model inverts the usual "closer to user = higher priority" pattern.
In an ecosystem where correctness flows downhill, the source must be
pristine for the delta to be trustworthy.

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

**Current priority**: IPC rewiring is **complete** (8/8 Tier 4). Tier 2 Science API
is **UNBLOCKED** (`toadstool.validate` IMPLEMENTED, `barracuda.precision.route`
IMPLEMENTED). All 7 springs wiring Tier 2. Focus shifts to shadow run execution
(BearDog TLS, lithoSpore Tier 1), primalSpring gate tests for Tier 2 methods,
and CompositionContext L2 coordination pass. All 13 primals at zero gate debt.

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
| **RESOLVED** | Songbird | 0 `#[async_trait]`, 0 finite `dyn`, 0 production mocks, 0 bare `#[allow]`, 0 blanket lint suppress, 0 hardcoded IPs/ports, 0 unused deps, 0 `Box<dyn Error>` anywhere, 0 files >800L, 0 unsafe. W192: sovereign-onion MAX_ONION_FRAME guard (memory-bomb prevention), stale Future import removed. W191: `ipc.register` identity verification (spoofed-name rejection), whitespace-tolerant protocol detection, BufReader safety documented. W190: IP literals centralized, robust `parse_endpoint()` (IPv6/scheme-aware). W189: `ipc.resolve` socket field. W188: 15 timeout constants, JSONRPC_VERSION, `Box<dyn Error>` eliminated. W187: smart refactor (1043→694L). W186–180: BTSP Phase 3 full implementation. Zero `::new()` in production — 7,803+ lib tests, 0 failures |
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

## Sentinel-Stadial Model (May 11, 2026)

Not all layers are in the same season. Primals are **sentinels** — the least
composed, most climate-responsive entities. They feel shifts first and respond
first. They are already in their own **stadial cycle**, with primalSpring as
their external validation gate.

```
Layer         Phase          Gate / Pressure
─────         ─────          ───────────────
L1 Primals    STADIAL        primalSpring (413 registry, MethodGate, graphs)
L2 primalSpring  GATE        validates L1, patterns flow to L3/L4
L3 Springs    INTERSTADIAL   absorbing primal capabilities
L4 Products   INTERSTADIAL   pre-wiring sovereignty, shadow runs pending
L5 Foundation INTERSTADIAL   thread coverage, data anchoring
```

**Upstream primal debt (at the gate)**: **Zero.** All 13 primals pass the
primalSpring gate — 13/13 MethodGate (JH-0 + JH-2), 13/13 BTSP Phase 3
AEAD, 413 methods (zero drift), deny.toml (ring + openssl banned).

## Interstadial Exit Criteria (5 Pillars)

The interstadial is the warm period where the ecosystem pre-wires sovereignty
capabilities. It ends when the plumbing exists and shadow runs can begin. Five
pillars define the exit gate:

1. **Primal Sovereignty (sentinel-stadial)**: **13/13 at the gate** — zero
   upstream debt. Downstream absorption (TLS shadow, NAT relay, content
   pipeline) is L4 work. **Structural: MET. Shadow execution: pending.**
2. **NUCLEUS Deployments**: H2 sub-steps 2b/3a/3b/3c need shadow-run state,
   Foundation Threads 4+7 workloads running — **Pass 11/13 work**
3. **ABG Hosting**: Thread 1 WCM through provenance trio — **Pass 13 work**
4. **lithoSpore**: 2+ modules PASS at Tier 1 with real NCBI/Dryad data — **Pass 11 work**
5. **River Delta**: **PILLAR 5 GATE MET** (May 11) — 8/8 Tier 4, 4 PGs, L4/L5, 7/10 seeded

Full details: `INTERSTADIAL_EXIT_CRITERIA.md`

### Stadial Boundary

The stadial is driven by **external selective pressure**: Cloudflare baselines
(BearDog TLS parity), upstream crate contributions (wgsl-precision,
proc-sysinfo), community engagement (Dimforge, burn, wgpu), lithoSpore USB
to Barrick Lab, and framework parity benchmarks (Kokkos, LAMMPS, SciPy).

The stadial does not start until the interstadial exit gate is cleared. It
ends when shadow runs prove parity and external deployments succeed.

---

## Future Trajectory

### Interstadial Remaining (organized as evolution passes — see `INTERSTADIAL_EXIT_CRITERIA.md`)

**Pass 11 — Parallel Shadow Starts (no blockers, start immediately)**:
- BearDog TLS shadow run on :8443 (H2-3b — upstream shipped)
- lithoSpore Tier 1: integrate groundSpring B2+B1 into modules, fetch real data
- NestGate content pipeline: wire `publish_sporeprint.sh` (Session 60 unblocked)

**Pass 12 — Upstream Sentinel (escalated)** — toadStool **RESOLVED**:
- ~~toadStool Phase C~~ **COMPLETE** (S245-S250, 520 cylinder tests). Phase D plumbing in. `toadstool.validate` IMPLEMENTED.
- Songbird VPS relay — TURN server shipped, relay progressing (blocks NAT shadow)
- ~~coralReef~~ — **Diesel engine migration feature freeze** (Sprint 8, E1/E2/E3 resolved, zero debt)

**Pass 13 — Gate Composition**:
- BTSP JupyterHub dual-auth shadow (H2-2b — ready)
- ABG: Thread 1 WCM compositions through provenance trio
- Foundation Threads 3, 4, 8, 9, 10 expressions + seeding

**Pass 14 — Convergence** — toadStool + barraCuda **RESOLVED**:
- ~~Tier 2 Science API~~ `toadstool.validate` **IMPLEMENTED** (S250), `list_workloads` WIRED (S245+)
- ~~`barracuda.precision.route`~~ **IMPLEMENTED** (precision.rs + 649 tests)
- Ionic runtime live, CompositionContext L2 coordination pass
- skunkBat E2E operational audit validation

**Previously resolved**:
- ~~squirrel MethodGate~~ **RESOLVED** — 13/13 at gate (May 11)
- ~~groundSpring B2 reproduction~~ **DONE** (B2+B1 PASS)
- ~~River delta: airSpring + groundSpring → `optional=true`~~ **DONE** — 8/8 Tier 4
- ~~Foundation: seed Threads 3 + 5~~ **DONE** — 7/10 threads seeded
- ~~JH-5 audit forwarding~~ **DONE** — skunkBat Phase 3 shipped
- ~~NestGate content.put transport parity~~ **RESOLVED** — Session 60

### Stadial (Months — external validation drives evolution)

- Shadow runs vs Cloudflare: BearDog TLS parity → cutover
- Songbird NAT replaces cloudflared: relay parity → cutover
- NestGate replaces GitHub Pages: content parity → cutover
- Upstream crate extraction: wgsl-precision, proc-sysinfo → crates.io
- Dimforge/wgmath proof-of-work engagement
- lithoSpore USB to Barrick Lab (Phase 5)
- ABG users running science on sovereign infrastructure
- Framework parity benchmarks: per-spring vs Kokkos/LAMMPS/SciPy

### Post-Stadial (Quarters — Horizon 3)

- JupyterHub → petalTongue (H3-01)
- GitHub → Forgejo as primary (H3-03/04)
- plasmidBin → NestGate distribution (H3-02)
- All springs at Tier 4 (binary-only IPC, no library deps)
- guideStone artifacts for all springs (deployable, self-validating)
- Every baseCamp paper has a NUCLEUS composition graph
- Gonzales drug repurposing pipeline (wetSpring → ADDRC)
- Faculty network densification

### Longer Term (Years)

- biomeOS evolves into sovereign OS substrate
- Citizen Colossus: federated consumer compute via sunCloud economics
- Novel Ferment Transcripts as economic primitives
- Mobility edge crossed: isolated sovereign nodes begin to conduct
- Every computation is its own presentation (petalTongue universal surface)
- Every result is its own reproducibility proof (sweetGrass universal braiding)

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
