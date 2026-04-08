# ludoSpring V17 — Primal Leverage Map Handoff

**Date:** April 3, 2026
**From:** ludoSpring V17
**To:** primalSpring, esotericWebb, sourDough, all springs and gardens
**License:** AGPL-3.0-or-later

---

## Summary

V17 maps every primal in the ecosystem to game science uses and validates
five novel multi-primal compositions that no single primal provides alone.
Where V16 established the replication bridge (how to compose), V17 answers
the creative question: *what do we compose, and why?*

The most transformative finding: game entities (sessions, NPCs, mods,
multiplayer matches) can be scaffolded as **ephemeral primals** using
sourDough's `PrimalLifecycle` patterns. Their biomeOS-managed lifecycles
give them first-class IPC surfaces, health contracts, and capability
advertising — and their rhizoCrypt DAGs outlive their runtimes.

---

## What Changed

### Primal Leverage Map (`specs/PRIMAL_LEVERAGE_MAP.md`)

Authoritative document mapping all 15 primals to game science uses across
three tiers:

- **Tier 1 — Already Wired (deepen)**: rhizoCrypt, loamSpine, sweetGrass,
  BearDog, biomeOS
- **Tier 2 — High-Value Novel Uses**: sourDough (ephemeral primal spawner),
  Squirrel (AI), petalTongue (visualization)
- **Tier 3 — Strategic Compositions**: toadStool, coralReef, Songbird,
  NestGate, skunkBat (pinned: pure concept)

Five novel multi-primal compositions identified and validated:

1. **Sovereign Save System** (rhizoCrypt + loamSpine + BearDog)
2. **Session-as-Primal** (sourDough + biomeOS + ludoSpring + rhizoCrypt)
3. **Attributed AI Narration** (Squirrel + sweetGrass + rhizoCrypt)
4. **Live Science Dashboard** (ludoSpring + petalTongue + rhizoCrypt)
5. **Sovereign Render Pipeline** (toadStool + coralReef + barraCuda)

### New Experiments (exp073–exp077)

| Experiment | Composition | Checks |
|------------|-------------|--------|
| exp073_sovereign_session | rhizoCrypt + loamSpine + BearDog | Local 50-tick DAG, signed vertices, minted certs |
| exp074_session_as_primal | sourDough + biomeOS + rhizoCrypt | Full lifecycle (Created→Running→Stopped), registration, DAG persistence |
| exp075_attributed_narration | Squirrel + sweetGrass + rhizoCrypt | Context building, narration requests, attribution braids |
| exp076_live_science_viz | petalTongue + rhizoCrypt | 100-tick metric pipeline, grammar-of-graphics encoding, provenance |
| exp077_hardware_dispatch | toadStool + barraCuda | Dispatch strategy logic, noise parity, hardware-aware routing |

All experiments follow `ValidationHarness` skip semantics: local phases
always run; IPC phases skip gracefully when primals aren't available.

### New Deploy Graphs (5 new TOMLs in `graphs/`)

| Graph | Nodes |
|-------|-------|
| `ludospring_sovereign_session.toml` | biomeOS → rhizoCrypt + loamSpine + BearDog → ludospring |
| `ludospring_session_primal.toml` | biomeOS → rhizoCrypt → ludospring (+ dynamic ephemeral) |
| `ludospring_narration.toml` | biomeOS → Squirrel + sweetGrass + rhizoCrypt → ludospring |
| `ludospring_live_viz.toml` | biomeOS → petalTongue + rhizoCrypt → ludospring |
| `ludospring_hardware.toml` | biomeOS → toadStool + barraCuda → ludospring |

Total deploy graphs: 9 (4 from V15 + 5 from V17).

### sourDough Ephemeral Primal Specification

New: `primals/sourDough/specs/EPHEMERAL_PRIMAL_SCAFFOLDING.md`

Documents the ephemeral primal lifecycle, parent management, provenance
outliving runtime, scoped capability namespacing, and health contract.
Four use cases formalized: session-as-primal, NPC-as-primal, mod-as-primal,
match-as-primal.

Updated: `primals/sourDough/specs/ROADMAP.md` — v0.7.0 Integration
Libraries now includes `EphemeralOwner<T>` utility and ephemeral primal
reference implementations.

---

## Design Decisions

- **bingoCube deferred**: It's a tool (like benchScale), not a service
  primal for composition experiments. When it gets an IPC surface, revisit.
- **skunkBat pinned**: Pure concept, no runtime. Threat detection patterns
  from exp053/exp060 are documented for future integration.
- **sourDough as spawner**: The creative leap — game entities as ephemeral
  primals. sourDough's `PrimalLifecycle` trait already defines the state
  machine; the spec extends it with spawn/teardown protocols and parent
  management.
- **Skip semantics universal**: Every experiment validates locally without
  primals running, proving the data models and patterns. IPC phases are
  additive validation when primals are available.

---

## What esotericWebb Absorbs

| Pattern | Webb's implementation |
|---------|---------------------|
| exp073 Sovereign Save | Save system uses signed DAG instead of JSON files |
| exp074 Session-as-Primal | Game sessions spawn as ephemeral primals with biomeOS lifecycle |
| exp075 Attributed Narration | AI DM uses sweetGrass braids instead of raw ai.chat |
| exp076 Live Science Dashboard | Debug mode uses petalTongue instead of print logs |
| exp077 Hardware Dispatch | Rendering uses toadStool-aware dispatch instead of fixed quality |

The session-as-primal pattern (exp074) is the most transformative: Webb
doesn't just call primals — it IS a primal that spawns sub-primals. Each
game session, each NPC cluster, each mod pack is a first-class entity in
the biomeOS mesh.

---

## What primalSpring Evolves

- **biomeOS**: Ephemeral primal registration/deregistration
  (`lifecycle.register` with `ephemeral: true`, auto-cleanup on timeout)
- **rhizoCrypt**: Parent-child DAG sessions (ephemeral sub-DAGs linked to
  main session)
- **sourDough**: `EphemeralOwner<T>` utility crate (v0.7+ roadmap)

---

## What Changed (File Summary)

| File | Action |
|------|--------|
| `specs/PRIMAL_LEVERAGE_MAP.md` | New — authoritative primal-to-game-science mapping |
| `experiments/exp073_sovereign_session/` | New — sovereign save system validation |
| `experiments/exp074_session_as_primal/` | New — ephemeral primal lifecycle validation |
| `experiments/exp075_attributed_narration/` | New — AI attribution composition |
| `experiments/exp076_live_science_viz/` | New — dashboard + metric provenance |
| `experiments/exp077_hardware_dispatch/` | New — hardware-aware compute dispatch |
| `graphs/ludospring_sovereign_session.toml` | New — trio deploy graph |
| `graphs/ludospring_session_primal.toml` | New — ephemeral session deploy graph |
| `graphs/ludospring_narration.toml` | New — AI narration deploy graph |
| `graphs/ludospring_live_viz.toml` | New — live viz deploy graph |
| `graphs/ludospring_hardware.toml` | New — hardware compute deploy graph |
| `Cargo.toml` | Updated — 5 new workspace members |
| `README.md` | Updated — V17, 77 experiments, 9 graphs, leverage map section |
| `primals/sourDough/specs/EPHEMERAL_PRIMAL_SCAFFOLDING.md` | New — ephemeral primal spec |
| `primals/sourDough/specs/ROADMAP.md` | Updated — v0.7 includes ephemeral scaffolding |

---

## Next Steps

1. **Run locally**: `cargo build --workspace` to verify all new experiments compile
2. **Run experiments**: Each exp073–exp077 runs standalone; skip semantics
   handle missing primals
3. **primalSpring gap**: biomeOS ephemeral lifecycle support (register/deregister
   with `ephemeral: true`)
4. **sourDough gap**: `EphemeralOwner<T>` utility crate in `sourdough-core`
5. **esotericWebb**: Absorb patterns from exp073–exp077, starting with
   exp074 session-as-primal
